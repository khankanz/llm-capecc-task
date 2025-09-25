"""Utilities for filling the DCIS resection eCC form with LLMs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Tuple

from outlines import generate, models
from outlines.models.transformers import Transformers

from dcis_resection_model import DCISResectionForm

JSON_START = "<JSON_START>"
JSON_END = "<JSON_END>"


@dataclass
class CranePrompts:
    """Container for the reasoning and JSON prompts."""

    reasoning: str
    json_prefix: str


def build_crane_prompts(report_text: str) -> CranePrompts:
    """Build the prompts used for reasoning and JSON constrained generation."""

    shared_context = (
        "You are a pathology assistant preparing the CAP DCIS Resection form.\n"
        "Use the following pathology report to populate the structured data form.\n\n"
        f"Report:\n{report_text.strip()}\n\n"
    )

    reasoning = (
        shared_context
        + "Think step by step about the report to decide on each form field.\n"
        + f"When you are ready to emit the structured data, write {JSON_START} on a new line."
        " This signals the start of the JSON object."
    )

    json_prefix = (
        shared_context
        + "Now emit only the JSON representation of the DCIS Resection form."
        " The JSON must follow the DCISResectionForm pydantic model schema.\n"
    )

    return CranePrompts(reasoning=reasoning, json_prefix=json_prefix)


def outlines_constrained_json(model: Any, tokenizer: Any, prompt_prefix: str) -> str:
    """Generate JSON constrained by the :class:`DCISResectionForm` schema.

    Parameters
    ----------
    model:
        A Hugging Face causal language model instance.
    tokenizer:
        The tokenizer paired with ``model``.
    prompt_prefix:
        Text shown to the model before ``JSON_START``.
    """

    hf_model = Transformers(model=model, tokenizer=tokenizer)
    prompt = f"{prompt_prefix}{JSON_START}"
    generator = generate.json(hf_model, DCISResectionForm)
    json_result = generator(prompt)
    if isinstance(json_result, str):
        return json_result
    return json.dumps(json_result)


def crane_fill(model_id: str, report_text: str) -> str:
    """Run the Crane pipeline to fill the structured form for ``report_text``."""

    prompts = build_crane_prompts(report_text)
    prefix_result = hf_reason_until_json_start(model_id, prompts.reasoning)

    if not isinstance(prefix_result, tuple) or len(prefix_result) != 3:
        raise ValueError(
            "hf_reason_until_json_start must return a tuple of"
            " (prefix, model, tokenizer)."
        )

    prefix, model, tokenizer = prefix_result
    json_payload = outlines_constrained_json(model, tokenizer, prompts.json_prefix)
    return f"{prefix}{json_payload}{JSON_END}"


# The huggingface reasoning helper is provided elsewhere at runtime. The
# attribute is expected to be injected/monkeypatched by the calling code or
# tests prior to invoking :func:`crane_fill`.
hf_reason_until_json_start: Any

