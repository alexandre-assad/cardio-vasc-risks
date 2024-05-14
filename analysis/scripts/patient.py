"""Patient definition and validation"""

from enum import Enum, auto
from typing import Dict
from pydantic import BaseModel
from icecream import ic

from scripts.bmi import (
    AGE_GROUP_REFERENCE,
    AGE_GROUP_VALUES,
    BMI_VALUES,
    AgeGroup,
    BmiLevel,
)
from scripts.definitions import (
    ApHighLevel,
    ApLowLevel,
    AP_HIGH_VALUES,
    AP_LOW_VALUES,
    CholesterolLevel,
    GlucLevel,
)

_DAY_TO_YEAR_RATIO = 0.00273973

_ALLOWED_HEIGHT = range(60, 250)
_ALLOWED_WEIGHT = range(30, 250)
_ALLOWED_AGE = range(10, 110)
_ALLOWED_BMI_PER_GROUP: Dict[AgeGroup, range] = {
    AgeGroup.KIDS: range(2, 40),
    AgeGroup.ADULTS: range(5, 50),
}

MALE_STR = "MALE"
FEMALE_STR = "FEMALE"


class Gender(Enum):
    """Simple gender enum"""

    MALE = auto()
    FEMALE = auto()


class Patient(BaseModel):
    """Patient model class"""

    id: int
    sex: bool
    age: float
    weight: float
    height: float
    ap_hi: float
    ap_lo: float
    cholesterol: CholesterolLevel
    gluc: GlucLevel
    smoke: bool
    alco: bool
    active: bool
    cardio: bool

    @property
    def years(self) -> int:
        """Days to years to repr"""
        return int(self.age * _DAY_TO_YEAR_RATIO)

    @property
    def gender(self) -> Gender:
        """Quick Repr of gender"""
        return Gender[MALE_STR] if not self.sex else Gender[FEMALE_STR]

    @property
    def age_group(self) -> AgeGroup:
        """Returns the age group"""
        for age_group, valid_range in AGE_GROUP_VALUES.items():
            if self.years in valid_range:
                return age_group
        raise ValueError(f"Age exceeding limit set ({_ALLOWED_AGE})")

    @property
    def broader_age_group(self) -> AgeGroup:
        """Simplifies the age group"""
        for broader_age_group, sub_groups in AGE_GROUP_REFERENCE.items():
            if self.age_group in sub_groups:
                return broader_age_group
        raise ValueError(f"Couldn't find broader age group for {self.age_group}")

    @property
    def bmi(self) -> float:
        """Returns the bmi"""
        bmi = self.weight / ((self.height / 100) ** 2)
        return round(bmi, 2)

    @property
    def bmi_status(self) -> BmiLevel:
        """Method to get the BMI Status"""
        for level, group_range in BMI_VALUES[self.broader_age_group].items():
            if int(self.bmi) in group_range:
                return level
        raise ValueError(f"Absurd BMI Value ({self.bmi})")

    @property
    def bmi_is_valid(self) -> bool:
        """Checks if bmi is in accepted range"""
        return int(self.bmi) in _ALLOWED_BMI_PER_GROUP[self.broader_age_group]

    @property
    def ap_hi_status(self) -> ApHighLevel:
        """Method to get ap_hi status"""
        ceilings = AP_HIGH_VALUES.values()
        accepted_range = range(min(ceilings), max(ceilings) + 1)
        if int(self.ap_hi) not in accepted_range:
            return ApHighLevel.INVALID
        for level, value in AP_HIGH_VALUES.items():
            if self.ap_hi <= value:
                return level
        raise ValueError("Invalid ap_hi value")

    @property
    def ap_lo_status(self) -> ApLowLevel:
        """Method to get ap_lo status"""
        floors = AP_LOW_VALUES.values()
        accepted_range = range(min(floors), max(floors) + 1)
        if int(self.ap_lo) not in accepted_range:
            return ApLowLevel.INVALID
        for level, value in AP_LOW_VALUES.items():
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
        return self.years in _ALLOWED_AGE

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
                self.bmi_is_valid,
            ]
        )

    @property
    def in_hypertension(self) -> bool:
        """Returns if patient is in hypertension"""
        return (
            self.ap_hi_status == ApHighLevel.HYPERTENSION_STAGE_1
            or self.ap_lo_status == ApLowLevel.HYPERTENSION_STAGE_1
            or self.ap_hi_status == ApHighLevel.HYPERTENSION_STAGE_2
            or self.ap_lo_status == ApLowLevel.HYPERTENSION_STAGE_2
        )

    @property
    def is_overweight(self) -> bool:
        """Returns the patient is overweight"""
        return (
            (self.bmi_status == BmiLevel.OBESITY_1)
            or (self.bmi_status == BmiLevel.OBESITY_2)
            or (self.bmi_status == BmiLevel.OBESITY_3)
            or (self.bmi_status == BmiLevel.OVERWEIGHT)
        )

    @property
    def is_underweight(self) -> bool:
        """Returns if the patient is underweight"""
        return self.bmi_status == BmiLevel.UNDERWEIGHT

    @property
    def is_healthy(self) -> bool:
        """No pathologies"""
        return not (self.in_hypertension or self.is_overweight or self.is_underweight)
    
