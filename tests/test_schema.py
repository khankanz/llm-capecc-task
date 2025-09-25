import json

import pytest
from pydantic import ValidationError, parse_obj_as

import dcis_resection_model as schema


def test_size_extent_requires_choice():
    """SizeExtent must specify either an estimated size or the cannot determine flag."""
    with pytest.raises(ValidationError):
        parse_obj_as(schema.SizeExtentSelection, {})


def test_distance_mm_requires_value():
    """Distance measurements require a millimeter value when the relation is exact."""
    exact_distance_payload = {
        "kind": "Exact distance (350819.100004300)",
        "millimeters": None,
    }

    with pytest.raises(ValidationError):
        parse_obj_as(schema.ClosestMarginDistanceSelection, exact_distance_payload)


def test_minimal_dcis_form_round_trip_json():
    """A minimal, valid DCIS form should parse and re-serialize to JSON."""
    minimal_payload = {
        "tumor": {
            "size_extent": {
                "kind": "Estimated size (extent) of DCIS is at least in Millimeters (mm) (58329.100004300)",
                "minimum_extent_mm": 5.0,
            }
        }
    }

    if hasattr(schema.DCISResection, "model_validate"):
        model = schema.DCISResection.model_validate(minimal_payload)
        serialized = model.model_dump()
    else:
        model = schema.DCISResection.parse_obj(minimal_payload)
        serialized = model.dict()

    assert serialized["tumor"]["size_extent"]["minimum_extent_mm"] == 5.0

    json_round_trip = json.loads(json.dumps(serialized))
    assert json_round_trip == serialized
