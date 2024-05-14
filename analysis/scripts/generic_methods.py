"""Colletion of methods to convert and filter the dataset"""

from pathlib import Path
from typing import Callable
from pandas import DataFrame, read_csv

from scripts.create_patient import (
    ACTIVE_STR,
    ALCO_STR,
    CARDIO_STR,
    GENDER_STR,
    SMOKE_STR,
    create_patient,
)
from scripts.patient import Patient


def load_dataset(path: str | Path, sep: str) -> DataFrame:
    dataset = read_csv(path, sep=sep)
    return dataset

def _booleanize_dataset(dataset: DataFrame) -> DataFrame:
    """Method to convert dataset to boolean values"""
    dataset[GENDER_STR] = dataset[GENDER_STR].apply(lambda x: bool(x - 1))
    dataset[SMOKE_STR] = dataset[SMOKE_STR].apply(lambda x: bool(x))
    dataset[ALCO_STR] = dataset[ALCO_STR].apply(lambda x: bool(x))
    dataset[ACTIVE_STR] = dataset[ACTIVE_STR].apply(lambda x: bool(x))
    dataset[CARDIO_STR] = dataset[CARDIO_STR].apply(lambda x: bool(x))
    return dataset


def _save_compatible_dataset(dataset: DataFrame) -> None:
    """Method to save dataset in a booleanized format"""
    comp_dataset_path = Path("../data/object_compatible/cardio_train.csv")
    comp_dataset = _booleanize_dataset(dataset)
    comp_dataset.to_csv(comp_dataset_path, sep=";", index=False)


def drop_by_filter(dataset: DataFrame, filter: Callable[[Patient], bool]) -> DataFrame:
    """Method to filter dataset
    Pass a function that takes a Patient object and returns a boolean value
    All patients that return True will be removed from the dataset
    """
    new_dataset = dataset.copy()
    for index, patient_row in new_dataset.iterrows():
        patient = create_patient(patient_row)
        if filter(patient):
            new_dataset = new_dataset.drop(index)
    return new_dataset


def convert_to_broader_df(dataset: DataFrame) -> DataFrame:
    new_dataset = dataset.copy()
    for index, patient_row in new_dataset.iterrows():
        patient = create_patient(patient_row)
        new_dataset.at[index, "age"] = patient.broader_age_group