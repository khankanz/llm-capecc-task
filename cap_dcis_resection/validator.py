"""Helpers for validating input payloads."""
from __future__ import annotations

from datetime import date
from typing import Any, Tuple

from .schemas import PatientContext, SpecimenDetail


def _build_specimens(items: list[dict[str, object]] | None) -> list[SpecimenDetail]:
    specimens: list[SpecimenDetail] = []
    if not items:
        return specimens
    for raw in items:
        specimens.append(
            SpecimenDetail(
                identifier=str(raw.get("identifier", "")),
                description=str(raw.get("description", "")),
                margin_status=(
                    str(raw["margin_status"]) if raw.get("margin_status") is not None else None
                ),
            )
        )
    return specimens


def _parse_report_date(value: object) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise TypeError("report_date must be a date or ISO string")


def validate_context(payload: Any) -> Tuple[bool, PatientContext | None, list[str]]:
    """Validate a payload and return (ok, context, errors)."""

    errors: list[str] = []
    if not isinstance(payload, dict):
        return False, None, ["payload must be a dictionary"]
    try:
        kwargs: dict[str, object] = {
            "patient_id": str(payload.get("patient_id", "")),
            "clinical_history": str(payload.get("clinical_history", "")),
            "specimens": _build_specimens(payload.get("specimens")),
        }
        parsed_date = _parse_report_date(payload.get("report_date"))
        if parsed_date is not None:
            kwargs["report_date"] = parsed_date
        context = PatientContext(**kwargs)
    except Exception as exc:  # pragma: no cover - exercised indirectly
        errors.append(str(exc))
        return False, None, errors
    return True, context, errors
