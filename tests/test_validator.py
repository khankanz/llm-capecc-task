from cap_dcis_resection.validator import validate_context


def test_validate_context_success():
    payload = {"patient_id": "123", "clinical_history": "History"}
    ok, context, errors = validate_context(payload)
    assert ok is True
    assert context is not None
    assert errors == []


def test_validate_context_failure():
    payload = {"patient_id": "", "clinical_history": ""}
    ok, context, errors = validate_context(payload)
    assert ok is False
    assert context is None
    assert any("patient_id" in message for message in errors)
