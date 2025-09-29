"""Utilities for interacting with Hugging Face chat models."""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)

JSON_START = "<JSON_START>"


def build_hf_chat(model_id: str):
    """Load a Hugging Face chat model and tokenizer.

    Parameters
    ----------
    model_id:
        The identifier of the model to load from the Hugging Face hub.

    Returns
    -------
    tuple
        A tuple ``(tokenizer, model)`` ready for inference.
    """

    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()
    return tokenizer, model


class ContainsTokenStopper(StoppingCriteria):
    """Stop generation when the decoded text ends with a target string."""

    def __init__(self, tokenizer, stop_string: str) -> None:
        super().__init__()
        self.tokenizer = tokenizer
        self.stop_string = stop_string

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs):
        if input_ids.numel() == 0:
            return False

        text = self.tokenizer.decode(input_ids[0], skip_special_tokens=False)
        return text.endswith(self.stop_string)


def _get_model_device(model) -> torch.device:
    if hasattr(model, "device"):
        return model.device

    try:
        first_parameter = next(model.parameters())
    except StopIteration:
        return torch.device("cpu")
    else:
        return first_parameter.device


def hf_reason_until_json_start(
    tokenizer,
    model,
    system: str,
    user: str,
    max_new_tokens: int = 700,
):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(prompt, return_tensors="pt")
    device = _get_model_device(model)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    stopping_criteria = StoppingCriteriaList([ContainsTokenStopper(tokenizer, JSON_START)])

    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs.get("attention_mask"),
        max_new_tokens=max_new_tokens,
        do_sample=False,
        stopping_criteria=stopping_criteria,
        pad_token_id=tokenizer.eos_token_id,
    )

    new_tokens = output_ids[0, inputs["input_ids"].shape[1] :]
    generated_text = tokenizer.decode(new_tokens, skip_special_tokens=False)
    return generated_text

