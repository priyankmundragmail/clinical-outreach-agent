from .mock_data import PATIENTS
from pydantic import BaseModel
from typing import Optional

class FindUnmetPatientsInput(BaseModel):
    """Input schema for finding unmet patients."""
    condition_filter: Optional[str] = None
    
def find_unmet_patients(condition_filter: Optional[str] = None) -> str:
    """
    Find all patients who have unmet needs requiring intervention.
    
    Args:
        condition_filter: Optional filter for specific conditions (can be left empty to find all)
    
    Returns:
        A formatted string listing patients who need intervention
    """
    unmet_patients = [
        patient for patient in PATIENTS 
        if patient.get("needs_intervention", False)
    ]
    
    if not unmet_patients:
        return "No patients found with unmet needs."
    
    result = f"Found {len(unmet_patients)} patients with unmet needs:\n"
    for patient in unmet_patients:
        result += f"- {patient['name']} (ID: {patient['patient_id']}) - Phone: {patient.get('phone', 'N/A')}\n"
    
    return result
