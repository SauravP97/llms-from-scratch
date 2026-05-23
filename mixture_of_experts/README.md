# Mixture of Experts

Imagine you run a consulting firm. You could hire a team of generalists who know a little bit about everything. They’ll do an okay job on most tasks, but they’ll struggle with highly complex, niche problems. Alternatively, you could hire a team of specialists—an accountant, a lawyer, an engineer, and a marketer—and hire a manager to route incoming client problems to the right expert.

MoE takes the second approach. Instead of forcing one massive neural network to learn everything, it divides the workload among multiple smaller, specialized networks (the "experts") and uses a "router" to decide which expert handles which piece of information.

## The Architecture: Where does MoE live?

In a standard Large Language Model (like the original GPT-3 or Llama 2), the architecture is made of stacked Transformer blocks. Each block has two main parts:

  1. Self-Attention: This helps the model understand the context of the sentence by looking at how words relate to each other.
  
  2. Feed-Forward Network (FFN): A dense neural network that acts as the model's memory and reasoning engine.
  
In an MoE model, the Self-Attention layers usually stay exactly the same. However, the single dense FFN is replaced by a Mixture of Experts layer.

This new layer contains:

  - The Experts: A set of $N$ separate, identical Feed-Forward Networks (e.g., 8 experts).
  - The Router (Gating Network): A small linear layer that looks at an incoming token (like a word) and predicts which experts are best equipped to process it.

## The Step-by-Step Flow

When a token enters the MoE layer, here is what happens:

  - The Assessment: The token is passed to the Router.
  - The Scoring: The Router calculates a probability score for every available expert.
  - The Routing (Sparse Activation): Instead of sending the token to all experts, the Router selects only the Top-$K$ experts (usually the top 1 or 2) to process the token.
  - The Merge: The chosen experts process the token, and their outputs are multiplied by their routing scores and added together.
  
Because we only activate a small subset of experts for any given token, this is called sparse activation.

## References

  - Cai, W., Jiang, J., Wang, F., Tang, J., Kim, S., & Huang, J. (2024). A Survey on Mixture of Experts in Large Language Models. IEEE Transactions on Knowledge and Data Engineering (TKDE) 2025. https://arxiv.org/pdf/2407.06204 (Cited by: 370)

  - Jiang, A. Q., Sablayrolles, A., Roux, A., Mensch, A., Savary, B., Bamford, C., ... & Lacroix, T. (2024). Mixtral of Experts. arXiv. https://arxiv.org/pdf/2401.04088 (Cited by: 3294)