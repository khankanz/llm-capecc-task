"""Simple example of building a prompt payload."""
from __future__ import annotations

from rich import print

from cap_dcis_resection import DEFAULT_PROMPT, PatientContext, ResectionPrompt


def main() -> None:
    context = PatientContext(
        patient_id="ABC123",
        clinical_history="Screen detected calcifications with stereotactic biopsy showing DCIS.",
    )
    prompt = ResectionPrompt(context=context)
    print({"template": DEFAULT_PROMPT, "payload": prompt.to_prompt_dict()})


if __name__ == "__main__":
    main()
