"""Colletion of methods to convert and filter the dataset"""
from pathlib import Path
from typing import Callable

from pandas import DataFrame, read_csv

from scripts.definitions import Patient

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


_CARDIO_DATASET_PATH = Path("../data/object_compatible/cardio_train.csv")
CARDIO_DATASET = read_csv(_CARDIO_DATASET_PATH, sep=";")


def booleanize_dataset(dataset: DataFrame) -> DataFrame:
    """Method to convert dataset to boolean values"""
    dataset[GENDER_STR] = dataset[GENDER_STR].apply(lambda x: bool(x - 1))
    dataset[SMOKE_STR] = dataset[SMOKE_STR].apply(lambda x: bool(x))
    dataset[ALCO_STR] = dataset[ALCO_STR].apply(lambda x: bool(x))
    dataset[ACTIVE_STR] = dataset[ACTIVE_STR].apply(lambda x: bool(x))
    dataset[CARDIO_STR] = dataset[CARDIO_STR].apply(lambda x: bool(x))
    return dataset

def save_compatible_dataset(dataset: DataFrame) -> None:
    """Method to save dataset in a booleanized format"""
    comp_dataset_path = Path("../data/object_compatible/cardio_train.csv")
    comp_dataset = booleanize_dataset(dataset)
    comp_dataset.to_csv(comp_dataset_path, sep=";", index=False)


def drop_by_filter(
    dataset: DataFrame, filter: Callable[[Patient], bool]
) -> DataFrame:
    """Method to filter dataset
    Pass a function that takes a Patient object and returns a boolean value
    All patients that return True will be removed from the dataset
    """
    for index, patient_row in dataset.iterrows():
        patient = Patient(
            id=patient_row[ID_STR],
            age=patient_row[AGE_STR],
            height=patient_row[HEIGHT_STR],
            weight=patient_row[WEIGHT_STR],
            ap_lo=patient_row[AP_LO_STR],
            ap_hi=patient_row[AP_HI_STR],
            cholesterol=patient_row[CHOLESTEROL_STR],
            gluc=patient_row[GLUC_STR],
            smoke=patient_row[SMOKE_STR],
            alco=patient_row[ALCO_STR],
            active=patient_row[ACTIVE_STR],
            cardio=patient_row[CARDIO_STR],
            sex=patient_row[GENDER_STR],
        )
        if filter(patient):
            dataset = dataset.drop(index)
    return dataset

