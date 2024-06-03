"""Some definitions for the analysis module"""

from enum import Enum, auto
from typing import Dict

class CholesterolLevel(Enum):
    """Enum class for cholesterol levels"""

    NORMAL = auto()
    ABOVE_NORMAL = auto()
    WELL_ABOVE_NORMAL = auto()

class GlucLevel(Enum):
    """Enum class for glucose levels"""

    NORMAL = auto()
    ABOVE_NORMAL = auto()
    WELL_ABOVE_NORMAL = auto()


class ApHighLevel(Enum):
    """Enum class for ap_hi levels"""

    LOW = auto()
    NORMAL = auto()
    ELEVATED = auto()
    HYPERTENSION_STAGE_1 = auto()
    HYPERTENSION_STAGE_2 = auto()
    INVALID = auto()


class ApLowLevel(Enum):
    """Enum class for ap_lo levels"""

    LOW = auto()
    NORMAL = auto()
    ELEVATED = auto()
    HYPERTENSION_STAGE_1 = auto()
    HYPERTENSION_STAGE_2 = auto()
    INVALID = auto()


AP_HIGH_VALUES: Dict[ApHighLevel, int] = {
    ApHighLevel.LOW: 90,
    ApHighLevel.NORMAL: 120,
    ApHighLevel.ELEVATED: 129,
    ApHighLevel.HYPERTENSION_STAGE_1: 135,
    ApHighLevel.HYPERTENSION_STAGE_2: 140,
}

AP_LOW_VALUES: Dict[ApLowLevel, int] = {
    ApLowLevel.LOW: 60,
    ApLowLevel.NORMAL: 80,
    ApLowLevel.ELEVATED: 89,
    ApLowLevel.HYPERTENSION_STAGE_1: 90,
    ApLowLevel.HYPERTENSION_STAGE_2: 100,
}

