# Flash Attention

Flash Attention is one of the most brilliant and impactful optimizations in modern AI. It is the reason we can now run Large Language Models (LLMs) with context windows of 100k+ tokens.

It can seem intimidating because it sits exactly at the intersection of deep learning mathematics and low-level hardware engineering.

## The Bottleneck: Standard Attention

To understand Flash Attention, we first have to understand what was broken. Standard scaled dot-product attention looks like this:

  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V$$

Where $Q$ (Queries), $K$ (Keys), and $V$ (Values) are matrices of shape $N \times d$ ($N$ is sequence length, $d$ is embedding dimension).

The Problem: Calculating $QK^T$ creates an $N \times N$ matrix. If our sequence length $N$ is 2,000, that's fine. If $N$ is 100,000, that matrix becomes enormous. The time complexity is $O(N^2)$, but more importantly, the memory complexity is $O(N^2)$.

## The Hardware Reality: Compute vs. Memory Bound

GPUs have a specific memory hierarchy:

  1. HBM (High Bandwidth Memory): The main GPU memory (e.g., 80GB on an A100). It's massive, but relatively slow to read from and write to.
  2. SRAM (Static RAM): The memory sitting directly next to the compute cores. It is incredibly small (e.g., 20MB per GPU), but lightning fast.

Standard Attention is Memory Bound. The GPU cores are waiting around doing nothing because they are constantly waiting for the massive $N \times N$ attention matrix to be saved to, and read from, the slow HBM.

## The Solution: Flash Attention

Flash Attention solves this by keeping the intermediate $N \times N$ matrix completely in the ultra-fast SRAM and never writing it to the slow HBM. It does this using two techniques: Tiling and Online Softmax.

### Tiling

Instead of computing the whole matrix at once, we chop $Q$, $K$, and $V$ into "blocks" or "tiles". We load a block of $Q$ and a block of $K$ into the fast SRAM, compute their attention scores, multiply by a block of $V$, and write only the final, much smaller output back to HBM.

### The "Online Softmax" Trick

Tiling sounds easy, but there is a mathematical roadblock: Softmax.
To calculate the softmax of a single row, we need the sum of the entire row as the denominator:

  $$\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{N} e^{x_j}}$$

How can we calculate softmax block-by-block if we don't have the sum of the whole row yet? Flash Attention uses "Online Softmax." We keep track of a "running maximum" and a "running denominator" for each row. As we process new blocks, we update these running values and mathematically correct the older blocks on the fly.

### Why Flash Attention keeps running Maximum

To understand why Flash Attention tracks a running maximum, we first need to look at a standard machine learning trick called the Safe Softmax, and why exponentials are a nightmare for computer hardware.

#### The Hardware Problem: Exponential Overflow

The standard softmax formula is:

  $$\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j} e^{x_j}}$$
    
The mathematical function $e^x$ grows incredibly fast.

  - If $x = 10$, $e^{10} \approx 22,026$. (Fine)
  - If $x = 100$, $e^{100} \approx 2.68 \times 10^{43}$. (Problematic)
  - If $x = 1000$, $e^{1000} \approx \text{Infinity}$. (Fatal)

GPUs typically calculate deep learning models using 16-bit or 32-bit floating-point numbers (FP16/FP32). FP16 maxes out at a value of 65,504. If your model generates an attention score of even $12$, $e^{12}$ is over $162,000$, which causes an Overflow. The GPU will output NaN (Not a Number) or Inf, and your entire training process will instantly crash.

#### The Solution: Safe Softmax

To fix this, scientists realized you can subtract a constant from every input before calculating the exponential, and the final softmax result will remain mathematically identical.

The smartest constant to subtract is the maximum value in the vector. Let $m = \max(x)$. The formula becomes:

  $$\text{softmax}(x_i) = \frac{e^{x_i - m}}{\sum_{j} e^{x_j - m}}$$

Why does this work mathematically?By rules of exponents, we can pull $e^{-m}$ out of the fraction:

  $$\frac{e^{x_i - m}}{\sum e^{x_j - m}} = \frac{e^{x_i} \cdot e^{-m}}{\sum (e^{x_j} \cdot e^{-m})} = \frac{e^{-m} \cdot e^{x_i}}{e^{-m} \cdot \sum e^{x_j}} = \frac{e^{x_i}}{\sum e^{x_j}}$$

Because the $e^{-m}$ term is on both the top and the bottom, it perfectly cancels out.

Why does this fix the hardware problem?

If you subtract the maximum value from every element in the array, the largest number in your array becomes exactly $0$ (because $\max - \max = 0$). All other numbers become negative.

  - $e^0 = 1$
  - $e^{\text{negative number}}$ is a fraction between $0$ and $1$.

By doing this, it is physically impossible for the GPU to calculate a number larger than $1$. Overflow is completely eliminated.

#### Why Flash Attention Needs a Running Maximum

In standard attention, you have the entire row of attention scores sitting in memory at the same time. Finding the maximum value $m$ is trivial.

But remember the core trick of Flash Attention: Tiling.
We are computing the attention scores block-by-block. If we are on Block 1, we do not know the scores for Block 2, Block 3, or Block 10. Therefore, we do not know the true global maximum of the row yet.

If we just guess, or use the local maximum of Block 1, and then later find a much larger number in Block 5, our denominator and outputs for Block 1 will be completely wrong.

The Online Softmax Trick:
Flash Attention solves this by keeping a running maximum.

  - It finds the local maximum of Block 1 and calculates a partial softmax.

  - It moves to Block 2. It finds the local max of Block 2.

  - It compares them to find a new global maximum.

  - The magic step: If the global maximum has changed, Flash Attention uses a simple mathematical correction (the correction_factor in the previous code) to retroactively scale the results from Block 1 down so they match the new reality.

Without the running maximum, Flash Attention would either suffer from fatal arithmetic overflow, or it would require loading the entire matrix into memory to find the global maximum—which defeats the entire purpose of the algorithm!