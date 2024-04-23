"""Some definitions for the analysis module"""

from enum import Enum, auto
from typing import Dict

from pydantic import BaseModel


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


_AP_HIGH_VALUES: Dict[ApHighLevel, int] = {
    ApHighLevel.LOW: 90,
    ApHighLevel.NORMAL: 120,
    ApHighLevel.ELEVATED: 129,
    ApHighLevel.HYPERTENSION_STAGE_1: 135,
    ApHighLevel.HYPERTENSION_STAGE_2: 140,
}

_AP_LOW_VALUES: Dict[ApLowLevel, int] = {
    ApLowLevel.LOW: 60,
    ApLowLevel.NORMAL: 80,
    ApLowLevel.ELEVATED: 89,
    ApLowLevel.HYPERTENSION_STAGE_1: 90,
    ApLowLevel.HYPERTENSION_STAGE_2: 100,
}

_ALLOWED_HEIGHT = range(60, 250)
_ALLOWED_WEIGHT = range(30, 250)
_ALLOWED_AGE = range(10, 110)


class Patient(BaseModel):
    """Patient model class"""

    id: int
    sex: bool
    age: float
    weight: float
    height: float
    ap_hi: float
    ap_lo: float
    cholesterol: float
    gluc: float
    smoke: bool
    alco: bool
    active: bool
    cardio: bool

    @property
    def gender(self) -> str:
        """Quick Repr of gender"""
        return "Male" if not self.sex else "Female"

    @property
    def ap_hi_status(self) -> ApHighLevel:
        """Method to get ap_hi status"""
        ceilings = _AP_HIGH_VALUES.values()
        accepted_range = range(min(ceilings), max(ceilings) + 1)
        if self.ap_hi not in accepted_range:
            return ApHighLevel.INVALID
        for level, value in _AP_HIGH_VALUES.items():
            if self.ap_hi <= value:
                return level
        raise ValueError("Invalid ap_hi value")

    @property
    def ap_lo_status(self) -> ApLowLevel:
        """Method to get ap_lo status"""
        floors = _AP_LOW_VALUES.values()
        accepted_range = range(min(floors), max(floors) + 1)
        if self.ap_lo not in accepted_range:
            return ApLowLevel.INVALID
        for level, value in _AP_LOW_VALUES.items():
            if self.ap_lo <= value:
                return level
        raise ValueError("Invalid ap_lo value")

    @property
    def height_is_valid(self) -> bool:
        """Method to get height status"""
        return self.height in _ALLOWED_HEIGHT

    @property
    def weight_is_valid(self) -> bool:
        """Method to get weight status"""
        return self.weight in _ALLOWED_WEIGHT

    @property
    def age_is_valid(self) -> bool:
        """Method to get age status"""
        return self.age in _ALLOWED_AGE

    @property
    def is_valid(self) -> bool:
        """Method to check if patient is valid"""
        return all(
            [
                self.ap_hi_status != ApHighLevel.INVALID,
                self.ap_lo_status != ApLowLevel.INVALID,
                self.height_is_valid,
                self.weight_is_valid,
                self.age_is_valid,
            ]
        )
