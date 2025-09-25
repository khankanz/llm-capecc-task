"""Schema definitions for the CAP DCIS resection form.

This module contains a condensed, Pydantic v2 representation of the
structured data captured by the CAP DCIS resection template.  The model aims
at surfacing the high-value cancer registry concepts while remaining simple to
validate and reason about.

The ``DCISResectionForm`` model is intentionally opinionated: it enforces a
single path through the template for the most commonly used reporting options
and captures optional staging details when they are available.

Doctest examples
----------------
>>> form = DCISResectionForm(  # doctest: +NORMALIZE_WHITESPACE
...     procedure=Procedure(kind=ProcedureKind.EXCISION),
...     specimen_laterality=SpecimenLaterality.RIGHT,
...     tumor_site=TumorSite(site=TumorSiteType.UPPER_OUTER, clock_positions=[ClockPosition.ONE_OCLOCK]),
...     size_extent=SizeExtent(estimated_size_mm=18.4),
...     histologic_type=HistologicType.CRIBRIFORM,
...     nuclear_grade=NuclearGrade.G3,
...     necrosis=Necrosis.CENTRAL_COMEDO,
...     microcalcifications=Microcalcifications.PRESENT_IN_DCIS,
...     margins=Margins(
...         status=MarginStatus.NEGATIVE,
...         negative_details=[
...             MarginMeasurement(
...                 face=MarginFace.SUPERIOR,
...                 distance=DistanceMM(relation=DistanceRelation.EXACT, mm=2.5),
...             )
...         ],
...     ),
...     regional_nodes=RegionalNodes(
...         status=RegionalNodeStatus.NEGATIVE,
...         nodes_examined=2,
...         nodes_positive=0,
...     ),
... )
>>> form.margins.negative_details[0].distance.mm
2.5

>>> try:
...     SizeExtent()
... except ValidationError:
...     True
True

>>> try:
...     DistanceMM(relation=DistanceRelation.EXACT)
... except ValidationError:
...     True
True
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, field_validator


class ProcedureKind(str, Enum):
    """Enumeration describing surgical procedure categories."""

    EXCISION = "excision"
    TOTAL_MASTECTOMY = "total_mastectomy"
    OTHER = "other"
    NOT_SPECIFIED = "not_specified"


class Procedure(BaseModel):
    """Procedure performed for the DCIS resection."""

    kind: ProcedureKind = Field(..., description="Procedure type")
    specification: Optional[str] = Field(
        default=None,
        description="Additional free-text detail when the procedure is 'other'.",
    )

    @field_validator("specification")
    @classmethod
    def _require_specification_for_other(cls, value: Optional[str], info):
        kind: ProcedureKind = info.data.get("kind")
        if kind == ProcedureKind.OTHER and not value:
            raise ValueError("specification is required when kind is 'other'")
        return value


class SpecimenLaterality(str, Enum):
    """Reported laterality of the resected specimen."""

    RIGHT = "right"
    LEFT = "left"
    BILATERAL = "bilateral"
    NOT_SPECIFIED = "not_specified"


class TumorSiteType(str, Enum):
    """Primary anatomic site of the ductal carcinoma in situ."""

    UPPER_OUTER = "upper_outer_quadrant"
    LOWER_OUTER = "lower_outer_quadrant"
    UPPER_INNER = "upper_inner_quadrant"
    LOWER_INNER = "lower_inner_quadrant"
    CENTRAL = "central"
    NIPPLE = "nipple"
    DIFFUSE = "diffuse"
    OTHER = "other"
    NOT_SPECIFIED = "not_specified"


class ClockPosition(str, Enum):
    """Clock position for lesion localisation."""

    ONE_OCLOCK = "1_oclock"
    TWO_OCLOCK = "2_oclock"
    THREE_OCLOCK = "3_oclock"
    FOUR_OCLOCK = "4_oclock"
    FIVE_OCLOCK = "5_oclock"
    SIX_OCLOCK = "6_oclock"
    SEVEN_OCLOCK = "7_oclock"
    EIGHT_OCLOCK = "8_oclock"
    NINE_OCLOCK = "9_oclock"
    TEN_OCLOCK = "10_oclock"
    ELEVEN_OCLOCK = "11_oclock"
    TWELVE_OCLOCK = "12_oclock"


class TumorSite(BaseModel):
    """Tumor site description with optional clock positions."""

    site: TumorSiteType = Field(..., description="Primary tumor site")
    clock_positions: Optional[List[ClockPosition]] = Field(
        default=None,
        min_length=1,
        description="Optional list of clock positions for site localisation.",
    )
    distance_from_nipple_cm: Optional[float] = Field(
        default=None, ge=0, description="Optional distance from the nipple in centimetres."
    )
    description: Optional[str] = Field(
        default=None,
        description="Free-text description when site is classified as 'other'.",
    )

    @field_validator("description")
    @classmethod
    def _description_required_for_other(cls, value: Optional[str], info):
        site: TumorSiteType = info.data.get("site")
        if site == TumorSiteType.OTHER and not value:
            raise ValueError("description is required when site is 'other'")
        return value


class DistanceRelation(str, Enum):
    """Relation of the recorded distance measurement."""

    EXACT = "exact"
    LESS_THAN = "less_than"
    GREATER_THAN = "greater_than"
    NOT_APPLICABLE = "not_applicable"
    CANNOT_BE_DETERMINED = "cannot_be_determined"


class DistanceMM(BaseModel):
    """Distance expressed in millimetres with relation metadata."""

    relation: DistanceRelation = Field(..., description="How the distance relates to the value")
    mm: Optional[float] = Field(
        default=None,
        ge=0,
        description="Distance in millimetres when applicable.",
    )
    note: Optional[str] = Field(
        default=None,
        description="Optional free-text clarification.",
    )

    @field_validator("mm")
    @classmethod
    def _require_mm_for_specific_relations(cls, value: Optional[float], info):
        relation: DistanceRelation = info.data.get("relation")
        if relation in {
            DistanceRelation.EXACT,
            DistanceRelation.LESS_THAN,
            DistanceRelation.GREATER_THAN,
        } and value is None:
            raise ValueError("mm must be provided when relation specifies a numeric comparison")
        return value


class SizeExtent(BaseModel):
    """Overall size or extent of ductal carcinoma in situ."""

    estimated_size_mm: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated greatest dimension of DCIS in millimetres.",
    )
    additional_dimension_mm_1: Optional[float] = Field(
        default=None, ge=0, description="Optional additional dimension in millimetres."
    )
    additional_dimension_mm_2: Optional[float] = Field(
        default=None, ge=0, description="Optional second additional dimension in millimetres."
    )
    cannot_determine_note: Optional[str] = Field(
        default=None,
        description="Explanation when the size cannot be determined.",
    )

    @field_validator("cannot_determine_note")
    @classmethod
    def _require_estimate_or_note(cls, value: Optional[str], info):
        estimated = info.data.get("estimated_size_mm")
        if estimated is None and not value:
            raise ValueError(
                "either estimated_size_mm or cannot_determine_note must be provided"
            )
        return value


class HistologicType(str, Enum):
    """Histologic type options for DCIS."""

    COMEDO = "comedo"
    CRIBRIFORM = "cribriform"
    MICROPAPILLARY = "micropapillary"
    PAPILLARY = "papillary"
    SOLID = "solid"
    PAGET_DISEASE = "paget_disease"
    OTHER = "other"


class NuclearGrade(str, Enum):
    """Nuclear grade of the DCIS lesion."""

    G1 = "grade_1"
    G2 = "grade_2"
    G3 = "grade_3"
    NOT_ASSESSED = "not_assessed"


class Necrosis(str, Enum):
    """Necrosis pattern in DCIS."""

    ABSENT = "absent"
    FOCAL = "focal"
    CENTRAL_COMEDO = "central_comedo"
    EXTENSIVE = "extensive"


class Microcalcifications(str, Enum):
    """Microcalcifications findings."""

    NOT_IDENTIFIED = "not_identified"
    PRESENT_IN_DCIS = "present_in_dcis"
    PRESENT_IN_NONNEOPLASTIC_TISSUE = "present_in_nonneoplastic_tissue"
    OTHER = "other"


class MarginStatus(str, Enum):
    """Overall margin status."""

    NEGATIVE = "negative"
    POSITIVE = "positive"


class MarginFace(str, Enum):
    """Specimen face for margin assessment."""

    SUPERIOR = "superior"
    INFERIOR = "inferior"
    MEDIAL = "medial"
    LATERAL = "lateral"
    ANTERIOR = "anterior"
    POSTERIOR = "posterior"
    DEEP = "deep"
    SUPERFICIAL = "superficial"


class MarginMeasurement(BaseModel):
    """Measurement of a negative margin distance."""

    face: MarginFace
    distance: DistanceMM


class PositiveMarginDetail(BaseModel):
    """Description of a positive margin face."""

    face: MarginFace
    involvement_description: Optional[str] = Field(
        default=None, description="Optional free-text description of involvement."
    )


class Margins(BaseModel):
    """Margin assessment with separate handling for positive and negative cases."""

    status: MarginStatus
    negative_details: List[MarginMeasurement] = Field(
        default_factory=list,
        description="Distances for negative margins.",
    )
    positive_details: List[PositiveMarginDetail] = Field(
        default_factory=list,
        description="Faces involved when margins are positive.",
    )

    @field_validator("negative_details")
    @classmethod
    def _validate_negative_details(cls, value: List[MarginMeasurement], info):
        status: MarginStatus = info.data.get("status")
        if status == MarginStatus.NEGATIVE:
            return value
        if value:
            raise ValueError("negative_details must be empty when status is positive")
        return value

    @field_validator("positive_details")
    @classmethod
    def _validate_positive_details(cls, value: List[PositiveMarginDetail], info):
        status: MarginStatus = info.data.get("status")
        if status == MarginStatus.POSITIVE:
            if not value:
                raise ValueError("positive_details must describe the involved margins")
            return value
        if value:
            raise ValueError("positive_details must be empty when status is negative")
        return value


class RegionalNodeStatus(str, Enum):
    """Regional lymph node status."""

    NOT_SUBMITTED = "not_submitted"
    NEGATIVE = "negative"
    POSITIVE = "positive"
    NOT_ASSESSED = "not_assessed"


class RegionalNodes(BaseModel):
    """Regional lymph node evaluation."""

    status: RegionalNodeStatus
    nodes_examined: Optional[int] = Field(default=None, ge=0)
    nodes_positive: Optional[int] = Field(default=None, ge=0)
    largest_metastatic_deposit: Optional[DistanceMM] = None
    extranodal_extension_present: Optional[bool] = None
    extranodal_extension_size: Optional[DistanceMM] = None

    @field_validator("nodes_positive")
    @classmethod
    def _non_negative_positive_nodes(cls, value: Optional[int], info):
        status: RegionalNodeStatus = info.data.get("status")
        if status == RegionalNodeStatus.POSITIVE and (value is None or value == 0):
            raise ValueError("positive node count required when status is positive")
        if value is not None and value < 0:
            raise ValueError("nodes_positive must be zero or greater")
        return value

    @field_validator("extranodal_extension_size")
    @classmethod
    def _ene_size_requires_presence(cls, value: Optional[DistanceMM], info):
        ene_present = info.data.get("extranodal_extension_present")
        if value is not None and ene_present is not True:
            raise ValueError("extranodal_extension_size requires extranodal_extension_present=True")
        return value


class DistantMetastasisStatus(str, Enum):
    """Distant metastasis information."""

    NOT_ASSESSED = "not_assessed"
    ABSENT = "absent"
    PRESENT = "present"


class DistantMetastasis(BaseModel):
    """Optional distant metastasis reporting."""

    status: DistantMetastasisStatus
    details: Optional[str] = None


class DCISResectionForm(BaseModel):
    """Aggregate data model capturing CAP DCIS resection content."""

    procedure: Procedure
    specimen_laterality: SpecimenLaterality
    tumor_site: TumorSite
    size_extent: SizeExtent
    histologic_type: HistologicType
    nuclear_grade: NuclearGrade
    necrosis: Necrosis
    microcalcifications: Microcalcifications
    margins: Margins
    regional_nodes: RegionalNodes
    distant_metastasis: Optional[DistantMetastasis] = None
    pathologic_stage_pT: Optional[str] = Field(default=None, description="AJCC pT stage")
    pathologic_stage_pN: Optional[str] = Field(default=None, description="AJCC pN stage")
    pathologic_stage_pM: Optional[str] = Field(default=None, description="AJCC pM stage")
    rationale: Optional[str] = Field(
        default=None,
        description="Narrative rationale for selections or deviations.",
    )


__all__ = ["DCISResectionForm"]
