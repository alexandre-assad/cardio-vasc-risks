from typing import Any, Dict
from pandas import Series
from scripts.definitions import CholesterolLevel, GlucLevel
from scripts.patient import Patient

ID_STR = "id"
AGE_STR = "age"
HEIGHT_STR = "height"
WEIGHT_STR = "weight"
AP_LO_STR = "ap_lo"
AP_HI_STR = "ap_hi"
CHOLESTEROL_STR = "cholesterol"
GENDER_STR = "gender"
SMOKE_STR = "smoke"
ALCO_STR = "alco"
ACTIVE_STR = "active"
CARDIO_STR = "cardio"
GLUC_STR = "gluc"

LVL_MAP: Dict[int, str] = {1: "NORMAL", 2: "ABOVE_NORMAL", 3: "WELL_ABOVE_NORMAL"}


def create_patient(data_row: Series) -> Patient:
    """Abstraction of creating patient from data_row"""
    return Patient(
        id=data_row[ID_STR],
        sex=data_row[GENDER_STR],
        age=data_row[AGE_STR],
        height=data_row[HEIGHT_STR],
        weight=data_row[WEIGHT_STR],
        ap_lo=data_row[AP_LO_STR],
        ap_hi=data_row[AP_HI_STR],
        cholesterol=CholesterolLevel[LVL_MAP[data_row[CHOLESTEROL_STR]]],
        gluc=GlucLevel[LVL_MAP[data_row[GLUC_STR]]],
        smoke=data_row[SMOKE_STR],
        alco=data_row[ALCO_STR],
        active=data_row[ACTIVE_STR],
        cardio=data_row[CARDIO_STR],
    )
