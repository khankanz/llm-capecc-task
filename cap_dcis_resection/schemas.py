"""Data models for CAP DCIS resection prompts."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class SpecimenDetail:
    """Information about an individual specimen."""

    identifier: str
    description: str
    margin_status: Optional[str] = None

    def __post_init__(self) -> None:
        normalized = self.identifier.strip()
        if not normalized:
            msg = "identifier must contain non-whitespace characters"
            raise ValueError(msg)
        self.identifier = normalized
        if self.margin_status is not None:
            self.margin_status = self.margin_status.strip() or None

    def to_dict(self) -> dict[str, Optional[str]]:
        return {
            "identifier": self.identifier,
            "description": self.description,
            "margin_status": self.margin_status,
        }


@dataclass
class PatientContext:
    """Structured data that accompanies a prompt sent to a language model."""

    patient_id: str
    clinical_history: str
    report_date: date = field(default_factory=date.today)
    specimens: List[SpecimenDetail] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.patient_id or not self.patient_id.strip():
            msg = "patient_id must contain non-whitespace characters"
            raise ValueError(msg)
        self.patient_id = self.patient_id.strip()
        self.clinical_history = self.clinical_history.strip()
        self.specimens = list(self.specimens)

    def to_dict(self) -> dict[str, object]:
        return {
            "patient_id": self.patient_id,
            "report_date": self.report_date.isoformat(),
            "clinical_history": self.clinical_history,
            "specimens": [spec.to_dict() for spec in self.specimens],
        }


@dataclass
class ResectionPrompt:
    """Payload ready for prompt templating."""

    context: PatientContext
    instructions: str = (
        "Use the CAP protocol for ductal carcinoma in situ (DCIS) resection."
    )
    model_name: str = "gpt-4o"

    DEFAULT_MODEL_NAME = "gpt-4o"

    def to_prompt_dict(self) -> dict[str, object]:
        """Convert the payload to a JSON-serializable dictionary."""

        payload = self.context.to_dict()
        payload["instructions"] = self.instructions
        payload["model_name"] = self.model_name
        return payload
