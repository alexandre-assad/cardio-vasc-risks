"""File to handle determined profiles and BMI"""

from enum import auto, Enum
from typing import Dict, List


class BmiLevel(Enum):
    """Generic status enum"""

    UNDERWEIGHT = auto()
    NORMAL = auto()
    OVERWEIGHT = auto()
    OBESITY_1 = auto()
    OBESITY_2 = auto()
    OBESITY_3 = auto()


class AgeGroup(Enum):
    """Enum class for different age groups"""

    KID = auto()
    TEEN = auto()
    KIDS = auto()
    YOUNG_ADULT = auto()
    ADULT = auto()
    SENIOR = auto()
    ADULTS = auto()


AGE_GROUP_VALUES: Dict[AgeGroup, range] = {
    AgeGroup.KID: range(10, 14),
    AgeGroup.TEEN: range(14, 20),
    AgeGroup.YOUNG_ADULT: range(20, 30),
    AgeGroup.ADULT: range(30, 60),
    AgeGroup.SENIOR: range(60, 110),
}

AGE_GROUP_REFERENCE: Dict[AgeGroup, List[AgeGroup]] = {
    AgeGroup.KIDS: [AgeGroup.KID, AgeGroup.TEEN],
    AgeGroup.ADULTS: [AgeGroup.YOUNG_ADULT, AgeGroup.ADULT, AgeGroup.SENIOR],
}

GENERIC_GROUP_VALUES: Dict[AgeGroup, range] = {
    AgeGroup.KIDS: range(10, 20),
    AgeGroup.ADULTS: range(20, 110),
}


BMI_VALUES: Dict[AgeGroup, Dict[BmiLevel, range]] = {
    AgeGroup.KIDS: {
        BmiLevel.UNDERWEIGHT: range(2, 5),
        BmiLevel.NORMAL: range(5, 18),
        BmiLevel.OVERWEIGHT: range(18, 25),
        BmiLevel.OBESITY_1: range(25, 30),
        BmiLevel.OBESITY_2: range(30, 35),
        BmiLevel.OBESITY_3: range(35, 40),
    },
    AgeGroup.ADULTS: {
        BmiLevel.UNDERWEIGHT: range(5, 18),
        BmiLevel.NORMAL: range(18, 25),
        BmiLevel.OVERWEIGHT: range(25, 30),
        BmiLevel.OBESITY_1: range(30, 35),
        BmiLevel.OBESITY_2: range(35, 40),
        BmiLevel.OBESITY_3: range(40, 50),
    },
}
