from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Callable, Dict, List, Mapping
from pandas.core.frame import DataFrame
from enum import Enum
from scripts.patient import Patient
from scripts.create_patient import create_patient
from icecream import ic


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
    patients = []
    for _, row in dataset.iterrows():
        patients.append(create_patient(row))
    return patients


def plot_counts(res: tuple[Dict[Enum,int],Dict[Enum,int]]) -> None:
    occ, sick_count = res
    total_counts = []
    sick_counts = []
    
    for age_group in occ.keys():
        total_counts.append(occ[age_group])
        sick_counts.append(sick_count.get(age_group, 0))

    sns.barplot(x=[age_group.name for age_group in occ.keys()], y=total_counts, color='blue', label='Total')

    sns.barplot(x=[age_group.name for age_group in occ.keys()], y=sick_counts, color='red', label='Sick')

    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.xlabel("")
    plt.title("Distribution of Patients by Status")
    plt.legend()
    plt.show()
