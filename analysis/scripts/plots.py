import enum
from pydantic import BaseModel
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Any, Callable, Dict, List
from pandas.core.frame import DataFrame
from enum import Enum

from scripts.patient import Patient
from scripts.create_patient import create_patient
from scripts.bmi import AgeGroup, BmiLevel
from scripts.definitions import ApHighLevel, ApLowLevel


class Status(Enum):
    VALID = "Valid"
    INVALID = "Invalid"


def plot_patients_by_status(
    dataset: DataFrame, status_function: Callable[[Patient], Status]
) -> None:
    status_counts = dataset.apply(
        lambda row: status_function(create_patient(row)), axis=1  # type: ignore
    ).value_counts()

    status_function_name = status_function.__name__

    status_counts.index = [
        (
            status_function_name
            if status == Status.VALID
            else f"not {status_function_name}"
        )
        for status in status_counts.index
    ]

    sns.barplot(x=status_counts.index, y=status_counts.values)
    plt.ylabel("Count")
    plt.xlabel("")
    plt.title(f"Distribution of Patients if {status_function_name}")
    plt.show()


def create_all_patients(dataset: DataFrame) -> List[Patient]:
    """Create all patients object"""
    patients = []
    for _, row in dataset.iterrows():
        patients.append(create_patient(row))
    return patients


def count_by_bmi_category(
    patients: List[Patient],
) -> tuple[Dict[BmiLevel, int], Dict[BmiLevel, int]]:
    """Count the number of patients in each BMI category."""
    counts = {level: 0 for level in BmiLevel}
    cardio_occurences = counts
    for patient in patients:
        counts[patient.bmi_status] += 1
        if patient.cardio:
            cardio_occurences[patient.bmi_status] += 1
    return counts, cardio_occurences


def count_by_age_group(
    patients: List[Patient],
) -> tuple[Dict[AgeGroup, int], Dict[AgeGroup, int]]:
    """Count the number of patients in each age group."""
    counts = {group: 0 for group in AgeGroup}
    cardio_occurences = counts
    for patient in patients:
        counts[patient.broader_age_group] += 1
        if patient.cardio:
            cardio_occurences[patient.broader_age_group] += 1
    del counts[AgeGroup.KID]
    del counts[AgeGroup.SENIOR]
    del counts[AgeGroup.TEEN]
    del counts[AgeGroup.YOUNG_ADULT]
    del counts[AgeGroup.ADULT]
    del cardio_occurences[AgeGroup.KID]
    del cardio_occurences[AgeGroup.SENIOR]
    del cardio_occurences[AgeGroup.TEEN]
    del cardio_occurences[AgeGroup.YOUNG_ADULT]
    del cardio_occurences[AgeGroup.ADULT]
    return counts, cardio_occurences


def count_by_ap_hi_status(
    patients: List[Patient],
) -> tuple[Dict[ApHighLevel, int], Dict[ApHighLevel, int]]:
    """Count the number of patients in each ap_hi status."""
    counts = {level: 0 for level in ApHighLevel}
    cardio_occurences = counts
    for patient in patients:
        counts[patient.ap_hi_status] += 1
        if patient.cardio:
            cardio_occurences[patient.ap_hi_status] += 1
    del counts[ApHighLevel.INVALID]
    del cardio_occurences[ApHighLevel.INVALID]
    return counts, cardio_occurences


def count_by_ap_lo_status(
    patients: List[Patient],
) -> tuple[Dict[ApLowLevel, int], Dict[ApLowLevel, int]]:
    """Count the number of patients in each ap_lo status."""
    counts = {level: 0 for level in ApLowLevel}
    cardio_occurences = counts
    for patient in patients:
        counts[patient.ap_lo_status] += 1
        if patient.cardio:
            cardio_occurences[patient.ap_lo_status] += 1
    del counts[ApLowLevel.INVALID]
    del cardio_occurences[ApLowLevel.INVALID]
    return counts, cardio_occurences


def count_by_age_group_2(
    patients: List[Patient],
) -> tuple[Dict[AgeGroup, int], Dict[AgeGroup, int]]:
    """Count the number of patients in each age group."""
    counts = {group: 0 for group in AgeGroup}
    cardio_occurences = counts
    for patient in patients:
        counts[patient.age_group] += 1
        if patient.cardio:
            cardio_occurences[patient.age_group] += 1
    del counts[AgeGroup.KID]
    del counts[AgeGroup.KIDS]
    del counts[AgeGroup.TEEN]
    del counts[AgeGroup.YOUNG_ADULT]
    del counts[AgeGroup.ADULTS]
    del cardio_occurences[AgeGroup.KID]
    del cardio_occurences[AgeGroup.KIDS]
    del cardio_occurences[AgeGroup.TEEN]
    del cardio_occurences[AgeGroup.YOUNG_ADULT]
    del cardio_occurences[AgeGroup.ADULTS]
    return counts, cardio_occurences


def plot_counts(res: tuple[Dict[Enum, int], Dict[Enum, int]]) -> None:
    occ, sick_count = res
    total_counts = []
    sick_counts = []

    for age_group in occ.keys():
        total_counts.append(occ[age_group])
        sick_counts.append(sick_count.get(age_group, 0))

    sns.barplot(
        x=[age_group.name for age_group in occ.keys()],
        y=total_counts,
        color="blue",
        label="Total",
    )

    sns.barplot(
        x=[age_group.name for age_group in occ.keys()],
        y=sick_counts,
        color="red",
        label="Sick",
    )

    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.xlabel("")
    plt.title("Distribution of Patients by Status")
    plt.legend()
    plt.show()


from icecream import ic


def get_attrs(obj: object) -> set[str]:
    """gets all the attributes, and properties of an object
    excluding default object attributes"""
    attrs = set()
    for attr in dir(obj):
        if not (attr.startswith("__") or attr.startswith("_")):
            attrs.add(attr)
    return attrs


def create_row(obj: object, attrs: set[str]) -> dict[str, Any]:
    """Creates row, ommit enum types"""
    row = {}
    for attr in attrs:
        att = getattr(obj, attr)
        if isinstance(att, Enum):
            att = att.name
        row[attr] = att
    return row


def pydantic_to_df(pydantic_objs: List[BaseModel]) -> DataFrame:
    """Converts a list of Pydantic objects to a DataFrame using attributes from get_attrs."""
    attrs = get_attrs(pydantic_objs[0]) - get_attrs(BaseModel)
    data = []
    for obj in pydantic_objs:
        row = create_row(obj, attrs)
        data.append(row)
    return DataFrame(data)
