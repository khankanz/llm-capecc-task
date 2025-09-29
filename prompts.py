"""Utilities for constructing structured prompting messages."""

from __future__ import annotations


JSON_START = "<JSON_START>"
"""Sentinel indicating where JSON output should begin."""


JSON_END = "<JSON_END>"
"""Sentinel indicating where JSON output should end."""


SYSTEM = (
    "You are an assistant that must think step-by-step before responding. "
    "Only emit JSON output between the delimiters {start} and {end}."
).format(start=JSON_START, end=JSON_END)
"""System prompt instructing the model how to format its response."""


REASONING_INSTRUCTIONS = (
    "Use a scratchpad to reason about the report before generating JSON. "
    "Ensure that intermediate thoughts stay outside the {start}/{end} "
    "delimiters so that only the final structured answer is enclosed."
).format(start=JSON_START, end=JSON_END)
"""Guidance for free-form reasoning prior to producing structured output."""


def build_user_prompt(report_text: str) -> str:
    """Create a user-facing prompt embedding the report text.

    The returned prompt reminds the model to avoid emitting JSON until the
    ``JSON_START`` delimiter appears, while presenting the supplied report for
    analysis.
    """

    reminder = (
        "Review the following report carefully. Do not produce any JSON output "
        f"until you explicitly encounter the token {JSON_START}."
    )

    return f"{reminder}\n\nReport:\n{report_text.strip()}\n"

