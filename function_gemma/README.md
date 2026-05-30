# Building Function Gemma (fine-tuned from Gemma-3 270M model)

![banner](../media/function-gemma-banner.jpeg)

The aim of this exercise is to produce a [Function Gemma](https://ai.google.dev/gemma/docs/functiongemma) like model.

> About Function Gemma: FunctionGemma is a specialized version of our `Gemma 3 270M` model tuned for function calling. It is designed as a strong base for further training into custom, fast, private, local agents that translate natural language into executable API actions.

Function Gemma is a **270 Million** parameter model, can be downloaded from [HuggingFace](https://huggingface.co/google/functiongemma-270m-it).

## Introduction

This repo focuses on reproducing a `Function Gemma` like model capable of function calling. Our model will take APIs / Functions documentation (structure) as an input from the user along with user's query and will perform Function Call with right arguments wherever needed.

> Note: The Functions / APIs structure is generally provided as a part of the System Instructions.

An Example User-Model communication will look like this:

```
SYSTEM: You are a helpful assistant with access to the following functions. Use them if required -
{
    "name": "calculate_factorial",
    "description": "Calculate the factorial of a given number",
    "parameters": {
        "type": "object",
        "properties": {
            "number": {
                "type": "integer",
                "description": "The number to calculate factorial for"
            }
        },
        "required": [
            "number"
        ]
    }
}

USER: Hi, I need to calculate the factorial of 5. Can you help me with that?


ASSISTANT: <functioncall> {"name": "calculate_factorial", "arguments": '{"number": 5}'} <|endoftext|>


FUNCTION RESPONSE: {"result": 120}


ASSISTANT: The factorial of 5 is 120. <|endoftext|>


USER: That was quick! Can you also calculate the factorial of 7?


ASSISTANT: <functioncall> {"name": "calculate_factorial", "arguments": '{"number": 7}'} <|endoftext|>


FUNCTION RESPONSE: {"result": 5040}


ASSISTANT: The factorial of 7 is 5040. <|endoftext|>


USER: Great! Thanks for your help.


ASSISTANT: You're welcome! If you have any other calculations or questions, feel free to ask. <|endoftext|>
```

To reproduce the Function Gemma model, we pick the existing [Gemma-3 270M](https://huggingface.co/google/gemma-3-270m) base model and fine-tune it on the Tool Calling dataset: [glaiveai/glaive-function-calling-v2](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2).

## Experiment 1

In my first experiment, I didn't explore much around data and straight away fine-tuned the Gemma-3 270 million parameter model on the Glaive Function Calling dataset.

I fine-tuned the model for around `5339` Steps where each step trained a batch of `8` (batch_size) items.
I achieved a final loss of `0.2511`.

<img src="../media/function_gemma_train_1.png" width="720px">

### The Loss Curve:

![loss-curve](../media/function-gemma-loss_1.png)

The detailed inference analysis for the 1st experiment can be found [here](./model_inference_analysis1.md)