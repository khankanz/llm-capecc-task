"""Pydantic data model for the DCIS Resection template."""
from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# SPECIMEN SECTION
# ---------------------------------------------------------------------------


class ProcedureExcision(BaseModel):
    kind: Literal["Excision (less than total mastectomy) (38394.100004300)"]


class ProcedureTotalMastectomy(BaseModel):
    kind: Literal[
        "Total mastectomy (including nipple-sparing and skin-sparing mastectomy) (48903.100004300)"
    ]


class ProcedureOther(BaseModel):
    kind: Literal["Other (specify) (5296.100004300)"]
    specification: str


class ProcedureNotSpecified(BaseModel):
    kind: Literal["Not specified (5299.100004300)"]


ProcedureSelection = Union[
    ProcedureExcision,
    ProcedureTotalMastectomy,
    ProcedureOther,
    ProcedureNotSpecified,
]

SpecimenLaterality = Literal[
    "Right (5423.100004300)",
    "Left (5424.100004300)",
    "Not specified (5427.100004300)",
]


class SpecimenSection(BaseModel):
    procedure: Optional[ProcedureSelection] = Field(
        default=None, discriminator="kind"
    )
    specimen_laterality: Optional[SpecimenLaterality] = None


# ---------------------------------------------------------------------------
# TUMOR SECTION
# ---------------------------------------------------------------------------


class TumorSiteSimple(BaseModel):
    kind: Literal[
        "Upper outer quadrant (5432.100004300)",
        "Lower outer quadrant (5433.100004300)",
        "Upper inner quadrant (5434.100004300)",
        "Lower inner quadrant (5437.100004300)",
        "Central (5438.100004300)",
        "Nipple (5439.100004300)",
        "Not specified (5450.100004300)",
    ]


class TumorSiteClockPosition(BaseModel):
    kind: Literal["Clock position (42527.100004300)"]
    clock_positions: List[
        Literal[
            "1 o'clock (6659.100004300)",
            "2 o'clock (6660.100004300)",
            "3 o'clock (6665.100004300)",
            "4 o'clock (6682.100004300)",
            "5 o'clock (6697.100004300)",
            "6 o'clock (6713.100004300)",
            "7 o'clock (6714.100004300)",
            "8 o'clock (6715.100004300)",
            "9 o'clock (6716.100004300)",
            "10 o'clock (6717.100004300)",
            "11 o'clock (6718.100004300)",
            "12 o'clock (6719.100004300)",
        ]
    ] = Field(..., min_items=1)


class TumorSiteDistanceFromNipple(BaseModel):
    kind: Literal[
        "Specify distance from nipple in Centimeters (cm) (51229.100004300)"
    ]
    distance_cm: float


class TumorSiteOther(BaseModel):
    kind: Literal["Other (specify) (5444.100004300)"]
    description: str


TumorSiteSelection = Union[
    TumorSiteSimple,
    TumorSiteClockPosition,
    TumorSiteDistanceFromNipple,
    TumorSiteOther,
]


class SizeExtentEstimated(BaseModel):
    kind: Literal[
        "Estimated size (extent) of DCIS is at least in Millimeters (mm) (58329.100004300)"
    ]
    minimum_extent_mm: float
    additional_dimension_mm_1: Optional[float] = None
    additional_dimension_mm_2: Optional[float] = None


class SizeExtentCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (50300.100004300)"]
    explanation: Optional[str] = None


SizeExtentSelection = Union[SizeExtentEstimated, SizeExtentCannotDetermine]


class ArchitecturalPatternSimple(BaseModel):
    kind: Literal[
        "Comedo (5497.100004300)",
        "Paget disease (DCIS involving nipple skin) (5498.100004300)",
        "Cribriform (5499.100004300)",
        "Micropapillary (5506.100004300)",
        "Papillary (5510.100004300)",
        "Solid (5522.100004300)",
    ]


class ArchitecturalPatternOther(BaseModel):
    kind: Literal["Other (specify) (5524.100004300)"]
    description: str


ArchitecturalPatternSelection = Union[
    ArchitecturalPatternSimple,
    ArchitecturalPatternOther,
]


class MicrocalcificationSimple(BaseModel):
    kind: Literal[
        "Not identified (5776.100004300)",
        "Present in DCIS (5777.100004300)",
        "Present in nonneoplastic tissue (5825.100004300)",
    ]


class MicrocalcificationOther(BaseModel):
    kind: Literal["Other (specify) (38432.100004300)"]
    description: str


MicrocalcificationSelection = Union[
    MicrocalcificationSimple,
    MicrocalcificationOther,
]


class TumorSection(BaseModel):
    tumor_site: Optional[List[TumorSiteSelection]] = Field(
        default=None, discriminator="kind"
    )
    histologic_type: Optional[
        Literal[
            "Ductal carcinoma in situ (6454.100004300)",
            "Paget disease (49894.100004300)",
            "Encapsulated papillary carcinoma without invasive carcinoma (48537.100004300)",
            "Solid papillary carcinoma without invasive carcinoma (45964.100004300)",
        ]
    ] = None
    size_extent: Optional[SizeExtentSelection] = Field(
        default=None, discriminator="kind"
    )
    number_of_blocks_with_dcis: Optional[int] = Field(default=None, ge=0, le=100)
    number_of_blocks_examined: Optional[int] = Field(default=None, ge=0, le=100)
    architectural_patterns: Optional[List[ArchitecturalPatternSelection]] = Field(
        default=None, discriminator="kind"
    )
    nuclear_grade: Optional[
        Literal[
            "Grade I (low) (6449.100004300)",
            "Grade II (intermediate) (6450.100004300)",
            "Grade III (high) (6451.100004300)",
        ]
    ] = None
    necrosis: Optional[
        Literal[
            "Not identified (5531.100004300)",
            "Present, focal (small foci or single cell necrosis) (5532.100004300)",
            'Present, central (expansive "comedo" necrosis) (5547.100004300)',
        ]
    ] = None
    microcalcifications: Optional[List[MicrocalcificationSelection]] = Field(
        default=None, discriminator="kind"
    )


# ---------------------------------------------------------------------------
# MARGINS SECTION
# ---------------------------------------------------------------------------


class ClosestMarginDistanceExact(BaseModel):
    kind: Literal["Exact distance (350819.100004300)"]
    millimeters: float


class ClosestMarginDistanceLessThan(BaseModel):
    kind: Literal["Less than (350822.100004300)"]
    millimeters: float


class ClosestMarginDistanceGreaterThan(BaseModel):
    kind: Literal["Greater than (350820.100004300)"]
    millimeters: float


class ClosestMarginDistanceOther(BaseModel):
    kind: Literal["Other (specify) (350816.100004300)"]
    description: str


class ClosestMarginDistanceCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350817.100004300)"]
    explanation: str


ClosestMarginDistanceSelection = Union[
    ClosestMarginDistanceExact,
    ClosestMarginDistanceLessThan,
    ClosestMarginDistanceGreaterThan,
    ClosestMarginDistanceOther,
    ClosestMarginDistanceCannotDetermine,
]


class ClosestMarginSimple(BaseModel):
    kind: Literal[
        "?Not applicable (45701.100004300)",
        "Anterior (26979.100004300)",
        "Posterior (26980.100004300)",
        "Superior (26981.100004300)",
        "Inferior (26982.100004300)",
        "Medial (26983.100004300)",
        "Lateral (26984.100004300)",
    ]


class ClosestMarginOther(BaseModel):
    kind: Literal["Other (specify) (26985.100004300)"]
    description: str


class ClosestMarginCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (58062.100004300)"]
    explanation: str


ClosestMarginSelection = Union[
    ClosestMarginSimple,
    ClosestMarginOther,
    ClosestMarginCannotDetermine,
]


class MarginInvolvedDetail(BaseModel):
    kind: Literal[
        "Anterior (specify extent, if possible) (350826.100004300)",
        "Posterior (specify extent, if possible) (350827.100004300)",
        "Superior (specify extent, if possible) (350828.100004300)",
        "Inferior (specify extent, if possible) (350829.100004300)",
        "Medial (specify extent, if possible) (350830.100004300)",
        "Lateral (specify extent, if possible) (350831.100004300)",
        "Other (specify margin(s) and, if possible, extent) (350832.100004300)",
        "Cannot be determined (explain) (350833.100004300)",
    ]
    detail: str


MarginInvolvedSelection = MarginInvolvedDetail


class MarginStatusAllNegative(BaseModel):
    kind: Literal["All margins negative for DCIS (350811.100004300)"]
    distance_to_closest_margin: Optional[ClosestMarginDistanceSelection] = Field(
        default=None, discriminator="kind"
    )
    closest_margins: Optional[List[ClosestMarginSelection]] = Field(
        default=None, discriminator="kind"
    )


class MarginStatusPresent(BaseModel):
    kind: Literal["DCIS present at margin (350823.100004300)"]
    margins_involved: Optional[List[MarginInvolvedSelection]] = Field(
        default=None, discriminator="kind"
    )


class MarginStatusOther(BaseModel):
    kind: Literal["Other (specify) (350834.100004300)"]
    description: str


class MarginStatusCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350835.100004300)"]
    explanation: str


class MarginStatusNotApplicable(BaseModel):
    kind: Literal["Not applicable (no DCIS in specimen) (350836.100004300)"]


MarginStatusSelection = Union[
    MarginStatusAllNegative,
    MarginStatusPresent,
    MarginStatusOther,
    MarginStatusCannotDetermine,
    MarginStatusNotApplicable,
]


class AnteriorMarginDistanceExact(BaseModel):
    kind: Literal["Exact distance (350841.100004300)"]
    millimeters: float


class AnteriorMarginDistanceLessThan(BaseModel):
    kind: Literal["Less than (350843.100004300)"]
    millimeters: float


class AnteriorMarginDistanceGreaterThan(BaseModel):
    kind: Literal["Greater than (350842.100004300)"]
    millimeters: float


class AnteriorMarginDistanceOther(BaseModel):
    kind: Literal["Other (specify) (350838.100004300)"]
    description: str


class AnteriorMarginDistanceCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350839.100004300)"]
    explanation: str


AnteriorMarginDistanceSelection = Union[
    AnteriorMarginDistanceExact,
    AnteriorMarginDistanceLessThan,
    AnteriorMarginDistanceGreaterThan,
    AnteriorMarginDistanceOther,
    AnteriorMarginDistanceCannotDetermine,
]


class PosteriorMarginDistanceExact(BaseModel):
    kind: Literal["Exact distance (350848.100004300)"]
    millimeters: float


class PosteriorMarginDistanceLessThan(BaseModel):
    kind: Literal["Less than (350850.100004300)"]
    millimeters: float


class PosteriorMarginDistanceGreaterThan(BaseModel):
    kind: Literal["Greater than (350849.100004300)"]
    millimeters: float


class PosteriorMarginDistanceOther(BaseModel):
    kind: Literal["Other (specify) (350845.100004300)"]
    description: str


class PosteriorMarginDistanceCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350846.100004300)"]
    explanation: str


PosteriorMarginDistanceSelection = Union[
    PosteriorMarginDistanceExact,
    PosteriorMarginDistanceLessThan,
    PosteriorMarginDistanceGreaterThan,
    PosteriorMarginDistanceOther,
    PosteriorMarginDistanceCannotDetermine,
]


class SuperiorMarginDistanceExact(BaseModel):
    kind: Literal["Exact distance (350855.100004300)"]
    millimeters: float


class SuperiorMarginDistanceLessThan(BaseModel):
    kind: Literal["Less than (350857.100004300)"]
    millimeters: float


class SuperiorMarginDistanceGreaterThan(BaseModel):
    kind: Literal["Greater than (350856.100004300)"]
    millimeters: float


class SuperiorMarginDistanceOther(BaseModel):
    kind: Literal["Other (specify) (350852.100004300)"]
    description: str


class SuperiorMarginDistanceCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350853.100004300)"]
    explanation: str


SuperiorMarginDistanceSelection = Union[
    SuperiorMarginDistanceExact,
    SuperiorMarginDistanceLessThan,
    SuperiorMarginDistanceGreaterThan,
    SuperiorMarginDistanceOther,
    SuperiorMarginDistanceCannotDetermine,
]


class InferiorMarginDistanceExact(BaseModel):
    kind: Literal["Exact distance (350862.100004300)"]
    millimeters: float


class InferiorMarginDistanceLessThan(BaseModel):
    kind: Literal["Less than (350864.100004300)"]
    millimeters: float


class InferiorMarginDistanceGreaterThan(BaseModel):
    kind: Literal["Greater than (350863.100004300)"]
    millimeters: float


class InferiorMarginDistanceOther(BaseModel):
    kind: Literal["Other (specify) (350859.100004300)"]
    description: str


class InferiorMarginDistanceCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350860.100004300)"]
    explanation: str


InferiorMarginDistanceSelection = Union[
    InferiorMarginDistanceExact,
    InferiorMarginDistanceLessThan,
    InferiorMarginDistanceGreaterThan,
    InferiorMarginDistanceOther,
    InferiorMarginDistanceCannotDetermine,
]


class MedialMarginDistanceExact(BaseModel):
    kind: Literal["Exact distance (350869.100004300)"]
    millimeters: float


class MedialMarginDistanceLessThan(BaseModel):
    kind: Literal["Less than (350871.100004300)"]
    millimeters: float


class MedialMarginDistanceGreaterThan(BaseModel):
    kind: Literal["Greater than (350870.100004300)"]
    millimeters: float


class MedialMarginDistanceOther(BaseModel):
    kind: Literal["Other (specify) (350866.100004300)"]
    description: str


class MedialMarginDistanceCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350867.100004300)"]
    explanation: str


MedialMarginDistanceSelection = Union[
    MedialMarginDistanceExact,
    MedialMarginDistanceLessThan,
    MedialMarginDistanceGreaterThan,
    MedialMarginDistanceOther,
    MedialMarginDistanceCannotDetermine,
]


class LateralMarginDistanceExact(BaseModel):
    kind: Literal["Exact distance (350876.100004300)"]
    millimeters: float


class LateralMarginDistanceLessThan(BaseModel):
    kind: Literal["Less than (350878.100004300)"]
    millimeters: float


class LateralMarginDistanceGreaterThan(BaseModel):
    kind: Literal["Greater than (350877.100004300)"]
    millimeters: float


class LateralMarginDistanceOther(BaseModel):
    kind: Literal["Other (specify) (350873.100004300)"]
    description: str


class LateralMarginDistanceCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350874.100004300)"]
    explanation: str


LateralMarginDistanceSelection = Union[
    LateralMarginDistanceExact,
    LateralMarginDistanceLessThan,
    LateralMarginDistanceGreaterThan,
    LateralMarginDistanceOther,
    LateralMarginDistanceCannotDetermine,
]


class OtherMarginDistanceSpecified(BaseModel):
    kind: Literal["Other margin(s) and distance(s) (specify) (350880.100004300)"]
    detail: str


class OtherMarginDistanceCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (352293.100004300)"]
    explanation: str


OtherMarginDistanceSelection = Union[
    OtherMarginDistanceSpecified,
    OtherMarginDistanceCannotDetermine,
]


class MarginsSection(BaseModel):
    margin_status: Optional[MarginStatusSelection] = Field(
        default=None, discriminator="kind"
    )
    distance_to_anterior_margin: Optional[AnteriorMarginDistanceSelection] = Field(
        default=None, discriminator="kind"
    )
    distance_to_posterior_margin: Optional[PosteriorMarginDistanceSelection] = Field(
        default=None, discriminator="kind"
    )
    distance_to_superior_margin: Optional[SuperiorMarginDistanceSelection] = Field(
        default=None, discriminator="kind"
    )
    distance_to_inferior_margin: Optional[InferiorMarginDistanceSelection] = Field(
        default=None, discriminator="kind"
    )
    distance_to_medial_margin: Optional[MedialMarginDistanceSelection] = Field(
        default=None, discriminator="kind"
    )
    distance_to_lateral_margin: Optional[LateralMarginDistanceSelection] = Field(
        default=None, discriminator="kind"
    )
    distance_to_other_margins: Optional[OtherMarginDistanceSelection] = Field(
        default=None, discriminator="kind"
    )
    margin_comment: Optional[str] = None


# ---------------------------------------------------------------------------
# REGIONAL LYMPH NODES SECTION
# ---------------------------------------------------------------------------


class MacrometastasisCountExact(BaseModel):
    kind: Literal["Exact number (specify) (44655.100004300)"]
    count: int = Field(..., ge=0, le=100)


class MacrometastasisCountAtLeast(BaseModel):
    kind: Literal["At least (specify) (46862.100004300)"]
    count: int = Field(..., ge=1, le=100)


class MacrometastasisCountOther(BaseModel):
    kind: Literal["Other (specify) (350893.100004300)"]
    description: str


class MacrometastasisCountCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (44824.100004300)"]
    explanation: str


MacrometastasisCountSelection = Union[
    MacrometastasisCountExact,
    MacrometastasisCountAtLeast,
    MacrometastasisCountOther,
    MacrometastasisCountCannotDetermine,
]


class MicrometastasisCountExact(BaseModel):
    kind: Literal["Exact number (specify) (58873.100004300)"]
    count: int = Field(..., ge=0, le=100)


class MicrometastasisCountAtLeast(BaseModel):
    kind: Literal["At least (specify) (55415.100004300)"]
    count: int = Field(..., ge=1, le=100)


class MicrometastasisCountOther(BaseModel):
    kind: Literal["Other (specify) (350894.100004300)"]
    description: str


class MicrometastasisCountCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (46991.100004300)"]
    explanation: str


MicrometastasisCountSelection = Union[
    MicrometastasisCountExact,
    MicrometastasisCountAtLeast,
    MicrometastasisCountOther,
    MicrometastasisCountCannotDetermine,
]


class IsolatedTumorCellsNotApplicable(BaseModel):
    kind: Literal["?Not applicable (52647.100004300)"]


class IsolatedTumorCellsExact(BaseModel):
    kind: Literal["Exact number (specify) (51319.100004300)"]
    count: int = Field(..., ge=0, le=100)


class IsolatedTumorCellsAtLeast(BaseModel):
    kind: Literal["At least (specify) (57579.100004300)"]
    count: int = Field(..., ge=1, le=100)


class IsolatedTumorCellsOther(BaseModel):
    kind: Literal["Other (specify) (350895.100004300)"]
    description: str


class IsolatedTumorCellsCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (48966.100004300)"]
    explanation: str


IsolatedTumorCellCountSelection = Union[
    IsolatedTumorCellsNotApplicable,
    IsolatedTumorCellsExact,
    IsolatedTumorCellsAtLeast,
    IsolatedTumorCellsOther,
    IsolatedTumorCellsCannotDetermine,
]


class NodalDepositExact(BaseModel):
    kind: Literal["Exact size (40874.100004300)"]
    millimeters: float


class NodalDepositLessThan(BaseModel):
    kind: Literal["Less than (351430.100004300)"]
    millimeters: float


class NodalDepositGreaterThan(BaseModel):
    kind: Literal["Greater than (351431.100004300)"]
    millimeters: float


class NodalDepositOther(BaseModel):
    kind: Literal["Other (specify) (351432.100004300)"]
    description: str


class NodalDepositCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (55601.100004300)"]
    explanation: str


NodalDepositSelection = Union[
    NodalDepositExact,
    NodalDepositLessThan,
    NodalDepositGreaterThan,
    NodalDepositOther,
    NodalDepositCannotDetermine,
]


class TotalNodesExact(BaseModel):
    kind: Literal["Exact number (specify) (350901.100004300)"]
    count: int = Field(..., ge=0, le=100)


class TotalNodesAtLeast(BaseModel):
    kind: Literal["At least (specify) (350903.100004300)"]
    count: int = Field(..., ge=1, le=100)


class TotalNodesOther(BaseModel):
    kind: Literal["Other (specify) (350905.100004300)"]
    description: str


class TotalNodesCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350904.100004300)"]
    explanation: str


TotalNodesSelection = Union[
    TotalNodesExact,
    TotalNodesAtLeast,
    TotalNodesOther,
    TotalNodesCannotDetermine,
]


class SentinelNodesNotApplicable(BaseModel):
    kind: Literal["?Not applicable (350911.100004300)"]


class SentinelNodesExact(BaseModel):
    kind: Literal["Exact number (specify) (350906.100004300)"]
    count: int = Field(..., ge=0, le=100)


class SentinelNodesAtLeast(BaseModel):
    kind: Literal["At least (specify) (350908.100004300)"]
    count: int = Field(..., ge=1, le=100)


class SentinelNodesOther(BaseModel):
    kind: Literal["Other (specify) (350910.100004300)"]
    description: str


class SentinelNodesCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350909.100004300)"]
    explanation: str


SentinelNodesSelection = Union[
    SentinelNodesNotApplicable,
    SentinelNodesExact,
    SentinelNodesAtLeast,
    SentinelNodesOther,
    SentinelNodesCannotDetermine,
]


class RegionalLymphNodesNegative(BaseModel):
    kind: Literal["All regional lymph nodes negative for tumor (350889.100004300)"]


class RegionalLymphNodesTumorPresent(BaseModel):
    kind: Literal["Tumor present in regional lymph node(s) (350890.100004300)"]
    macrometastases: Optional[MacrometastasisCountSelection] = Field(
        default=None, discriminator="kind"
    )
    micrometastases: Optional[MicrometastasisCountSelection] = Field(
        default=None, discriminator="kind"
    )
    isolated_tumor_cells: Optional[IsolatedTumorCellCountSelection] = Field(
        default=None, discriminator="kind"
    )
    largest_metastatic_deposit: Optional[NodalDepositSelection] = Field(
        default=None, discriminator="kind"
    )
    extranodal_extension: Optional[
        Literal[
            "Not identified (56397.100004300)",
            "Present, 2 mm or less (56915.100004300)",
            "Present, greater than 2 mm (350900.100004300)",
            "Present (351449.100004300)",
            "Cannot be determined (351450.100004300)",
        ]
    ] = None


class RegionalLymphNodesOther(BaseModel):
    kind: Literal["Other (specify) (350891.100004300)"]
    description: str


class RegionalLymphNodesCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (explain) (350892.100004300)"]
    explanation: str


RegionalLymphNodesFindingsSelection = Union[
    RegionalLymphNodesNegative,
    RegionalLymphNodesTumorPresent,
    RegionalLymphNodesOther,
    RegionalLymphNodesCannotDetermine,
]


class RegionalLymphNodesPresent(BaseModel):
    kind: Literal["Regional lymph nodes present (374352.100004300)"]
    findings: Optional[RegionalLymphNodesFindingsSelection] = Field(
        default=None, discriminator="kind"
    )
    total_nodes_examined: Optional[TotalNodesSelection] = Field(
        default=None, discriminator="kind"
    )
    sentinel_nodes_examined: Optional[SentinelNodesSelection] = Field(
        default=None, discriminator="kind"
    )


class RegionalLymphNodesNotApplicable(BaseModel):
    kind: Literal[
        "Not applicable (no regional lymph nodes submitted or found) (350887.100004300)"
    ]


RegionalLymphNodeStatusSelection = Union[
    RegionalLymphNodesNotApplicable,
    RegionalLymphNodesPresent,
]


class RegionalLymphNodesSection(BaseModel):
    regional_lymph_node_status: Optional[RegionalLymphNodeStatusSelection] = Field(
        default=None, discriminator="kind"
    )
    regional_lymph_node_comment: Optional[str] = None


# ---------------------------------------------------------------------------
# DISTANT METASTASIS SECTION
# ---------------------------------------------------------------------------


class DistantSiteNotApplicable(BaseModel):
    kind: Literal["?Not applicable (352355.100004300)"]


class DistantSiteNonRegionalNodes(BaseModel):
    kind: Literal[
        "Non-regional lymph node(s) (specify, if possible) (352352.100004300)"
    ]
    detail: Optional[str] = None


class DistantSiteLung(BaseModel):
    kind: Literal["Lung (352349.100004300)"]
    detail: Optional[str] = None


class DistantSiteLiver(BaseModel):
    kind: Literal["Liver (352350.100004300)"]
    detail: Optional[str] = None


class DistantSiteBone(BaseModel):
    kind: Literal["Bone (352351.100004300)"]
    detail: Optional[str] = None


class DistantSiteBrain(BaseModel):
    kind: Literal["Brain (352348.100004300)"]
    detail: Optional[str] = None


class DistantSiteOther(BaseModel):
    kind: Literal["Other (specify) (352353.100004300)"]
    detail: str


class DistantSiteCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (352354.100004300)"]
    detail: Optional[str] = None


DistantSiteSelection = Union[
    DistantSiteNotApplicable,
    DistantSiteNonRegionalNodes,
    DistantSiteLung,
    DistantSiteLiver,
    DistantSiteBone,
    DistantSiteBrain,
    DistantSiteOther,
    DistantSiteCannotDetermine,
]


class DistantMetastasisSection(BaseModel):
    distant_sites: Optional[List[DistantSiteSelection]] = Field(
        default=None, discriminator="kind"
    )


# ---------------------------------------------------------------------------
# PATHOLOGIC STAGE CLASSIFICATION SECTION
# ---------------------------------------------------------------------------


class TNMDescriptorNotApplicable(BaseModel):
    kind: Literal["?Not applicable (6391.100004300)"]
    comment: Optional[str] = None


class TNMDescriptorRecurrent(BaseModel):
    kind: Literal["r (recurrent) (6392.100004300)"]


TNMDescriptorSelection = Union[TNMDescriptorNotApplicable, TNMDescriptorRecurrent]


class RegionalLymphNodesModifierNotApplicable(BaseModel):
    kind: Literal["?Not applicable (58417.100004300)"]


class RegionalLymphNodesModifierSN(BaseModel):
    kind: Literal[
        "(sn): Sentinel node(s) evaluated. If 6 or more nodes (sentinel or nonsentinel) are removed, this modifier should not be used. (6403.100004300)"
    ]


class RegionalLymphNodesModifierF(BaseModel):
    kind: Literal[
        "(f): Nodal metastasis confirmed by fine needle aspiration or core needle biopsy. (54656.100004300)"
    ]


RegionalLymphNodesModifierSelection = Union[
    RegionalLymphNodesModifierNotApplicable,
    RegionalLymphNodesModifierSN,
    RegionalLymphNodesModifierF,
]


class PMCategoryNotApplicable(BaseModel):
    kind: Literal[
        "?Not applicable - pM cannot be determined from the submitted specimen(s) (6431.100004300)"
    ]


class PMCategoryM1(BaseModel):
    kind: Literal["pM1: Histologically proven metastases larger than 0.2 mm (6433.100004300)"]
    case_number: Optional[str] = None


PMCategorySelection = Union[PMCategoryNotApplicable, PMCategoryM1]


class PathologicStageSection(BaseModel):
    tnm_descriptors: Optional[List[TNMDescriptorSelection]] = Field(
        default=None, discriminator="kind"
    )
    pT_category: Optional[
        Literal[
            "pTis (DCIS): Ductal carcinoma in situ (6396.100004300)",
            "pTis (Paget): Paget disease of the nipple NOT associated with invasive carcinoma and / or DCIS in the underlying breast parenchyma# (38652.100004300)",
        ]
    ] = None
    regional_lymph_nodes_modifier: Optional[
        List[RegionalLymphNodesModifierSelection]
    ] = Field(default=None, discriminator="kind")
    pN_category: Optional[
        Literal[
            "pN not assigned (no nodes submitted or found) (327738.100004300)",
            "pN not assigned (cannot be determined based on available pathological information) (327739.100004300)",
            "pN0: No regional lymph node metastasis identified or ITCs only# (39161.100004300)",
            "pN0 (i+): ITCs only (malignant cell clusters no larger than 0.2 mm) in regional lymph node(s) (39167.100004300)",
            "pN0 (mol+): Positive molecular findings by reverse transcriptase polymerase chain reaction (RT-PCR); no ITCs detected (39169.100004300)",
            "pN1mi: Micrometastases (approximately 200 cells, larger than 0.2 mm, but none larger than 2.0 mm) (39120.100004300)",
            "pN1a: Metastases in 1-3 axillary lymph nodes, at least one metastasis larger than 2.0 mm## (6417.100004300)",
            "pN1b: Metastases in ipsilateral internal mammary sentinel nodes, excluding ITCs (39166.100004300)",
            "pN1c: pN1a and pN1b combined (39168.100004300)",
            "pN2a: Metastases in 4-9 axillary lymph nodes, at least one tumor deposit larger than 2.0 mm## (6418.100004300)",
            "pN2b: Metastases in clinically detected internal mammary lymph nodes with or without microscopic confirmation; with pathologically negative axillary nodes (39013.100004300)",
            "pN3a: Metastases in 10 or more axillary lymph nodes (at least one tumor deposit larger than 2.0 mm)##; or metastases to the infraclavicular (Level III axillary lymph) nodes (39175.100004300)",
            "pN3b: pN1a or pN2a in the presence of cN2b (positive internal mammary nodes by imaging); or pN2a in the presence of pN1b (39177.100004300)",
            "pN3c: Metastases in ipsilateral supraclavicular lymph nodes (39178.100004300)",
        ]
    ] = None
    pM_category: Optional[PMCategorySelection] = Field(
        default=None, discriminator="kind"
    )


# ---------------------------------------------------------------------------
# ADDITIONAL FINDINGS SECTION
# ---------------------------------------------------------------------------


class AdditionalFindingsSection(BaseModel):
    additional_findings: Optional[str] = None


# ---------------------------------------------------------------------------
# SPECIAL STUDIES SECTION
# ---------------------------------------------------------------------------


class ERNuclearPositivitySpecify(BaseModel):
    kind: Literal["Specify % (42853.100004300)"]
    percentage: int = Field(..., ge=0, le=100)


class ERNuclearPositivityOneToTen(BaseModel):
    kind: Literal["1-10% (specify)# (41293.100004300)"]
    percentage: int = Field(..., ge=1, le=10)


class ERNuclearPositivityRange(BaseModel):
    kind: Literal[
        "11-20% (41296.100004300)",
        "21-30% (41379.100004300)",
        "31-40% (42868.100004300)",
        "41-50% (42870.100004300)",
        "51-60% (41385.100004300)",
        "61-70% (42876.100004300)",
        "71-80% (41302.100004300)",
        "81-90% (42879.100004300)",
        "91-100% (41388.100004300)",
    ]


ERNuclearPositivitySelection = Union[
    ERNuclearPositivitySpecify,
    ERNuclearPositivityOneToTen,
    ERNuclearPositivityRange,
]


class ERStatusPositive(BaseModel):
    kind: Literal["Positive (42845.100004300)"]
    nuclear_positivity: Optional[ERNuclearPositivitySelection] = Field(
        default=None, discriminator="kind"
    )


class ERStatusNegative(BaseModel):
    kind: Literal["Negative (42400.100004300)"]


class ERStatusCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (indeterminate) (58158.100004300)"]


ERStatusSelection = Union[
    ERStatusPositive,
    ERStatusNegative,
    ERStatusCannotDetermine,
]


class PgRNuclearPositivitySpecify(BaseModel):
    kind: Literal["Specify % (41405.100004300)"]
    percentage: int = Field(..., ge=0, le=100)


class PgRNuclearPositivityOneToTen(BaseModel):
    kind: Literal["1-10% (specify)# (42893.100004300)"]
    percentage: int = Field(..., ge=1, le=10)


class PgRNuclearPositivityRange(BaseModel):
    kind: Literal[
        "11-20% (41413.100004300)",
        "21-30% (41777.100004300)",
        "31-40% (41419.100004300)",
        "41-50% (41428.100004300)",
        "51-60% (41780.100004300)",
        "61-70% (41445.100004300)",
        "71-80% (41453.100004300)",
        "81-90% (41454.100004300)",
        "91-100% (42896.100004300)",
    ]


PgRNuclearPositivitySelection = Union[
    PgRNuclearPositivitySpecify,
    PgRNuclearPositivityOneToTen,
    PgRNuclearPositivityRange,
]


class PgRStatusPositive(BaseModel):
    kind: Literal["Positive (41402.100004300)"]
    nuclear_positivity: Optional[PgRNuclearPositivitySelection] = Field(
        default=None, discriminator="kind"
    )


class PgRStatusNegative(BaseModel):
    kind: Literal["Negative (53779.100004300)"]


class PgRStatusCannotDetermine(BaseModel):
    kind: Literal["Cannot be determined (indeterminate) (58107.100004300)"]


PgRStatusSelection = Union[
    PgRStatusPositive,
    PgRStatusNegative,
    PgRStatusCannotDetermine,
]


class BiomarkerTestER(BaseModel):
    kind: Literal["Estrogen Receptor (ER) (52865.100004300)"]
    status: Optional[ERStatusSelection] = Field(
        default=None, discriminator="kind"
    )


class BiomarkerTestPgR(BaseModel):
    kind: Literal["Progesterone Receptor (PgR) (50432.100004300)"]
    status: Optional[PgRStatusSelection] = Field(
        default=None, discriminator="kind"
    )


BreastBiomarkerTestingSelection = Union[
    BiomarkerTestER,
    BiomarkerTestPgR,
]


class SpecialStudiesSection(BaseModel):
    breast_biomarker_testing: Optional[List[BreastBiomarkerTestingSelection]] = Field(
        default=None, discriminator="kind"
    )
    testing_performed_on_case_number: Optional[str] = None


# ---------------------------------------------------------------------------
# COMMENTS SECTION
# ---------------------------------------------------------------------------


class CommentsSection(BaseModel):
    comments: Optional[str] = None


# ---------------------------------------------------------------------------
# ROOT MODEL
# ---------------------------------------------------------------------------


class DCISResection(BaseModel):
    specimen: Optional[SpecimenSection] = None
    tumor: Optional[TumorSection] = None
    margins: Optional[MarginsSection] = None
    regional_lymph_nodes: Optional[RegionalLymphNodesSection] = None
    distant_metastasis: Optional[DistantMetastasisSection] = None
    pathologic_stage: Optional[PathologicStageSection] = None
    additional_findings: Optional[AdditionalFindingsSection] = None
    special_studies: Optional[SpecialStudiesSection] = None
    comments: Optional[CommentsSection] = None
