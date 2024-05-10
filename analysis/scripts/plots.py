import seaborn as sns
import matplotlib.pyplot as plt
from typing import Callable
from pandas.core.frame import DataFrame
from enum import Enum
from pydantic import BaseModel
from scripts.patient import Patient
from scripts.create_patient import create_patient

# Define your status enums here if not already defined
# Replace these with your actual enums
class Status(Enum):
    VALID = "Valid"
    INVALID = "Invalid"


def plot_patients_by_status(dataset: DataFrame, status_function: Callable[[Patient], Status]):
    status_counts = dataset.apply(lambda row: status_function(create_patient(row)), axis=1).value_counts()
    sns.barplot(x=status_counts.index, y=status_counts.values)
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.title("Distribution of Patients by Status")
    plt.show()


# Example usage:
# Assuming you have a DataFrame called 'patients_df' containing your patient data
# and a status function called 'is_valid' that checks if a patient is valid
