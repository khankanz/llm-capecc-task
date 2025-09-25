from datetime import date

from cap_dcis_resection.schemas import PatientContext, ResectionPrompt, SpecimenDetail


def test_resection_prompt_to_dict():
    specimen = SpecimenDetail(identifier="  A1  ", description="Lumpectomy specimen")
    context = PatientContext(
        patient_id="XYZ",
        report_date=date(2024, 1, 1),
        clinical_history="History of DCIS",
        specimens=[specimen],
    )
    prompt = ResectionPrompt(context=context, model_name="gpt-test")

    payload = prompt.to_prompt_dict()
    assert payload["patient_id"] == "XYZ"
    assert payload["report_date"] == "2024-01-01"
    assert payload["specimens"][0]["identifier"] == "A1"
    assert payload["model_name"] == "gpt-test"
