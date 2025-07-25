# tools/access_cohort_definitions.py

from .cohort_definitions import COHORT_DEFINITIONS

def get_all_cohort_definitions():
    """
    Tool to retrieve all available cohort definitions with classification criteria.
    
    Returns:
        dict: Complete cohort definitions with classification and intervention criteria
    """
    return COHORT_DEFINITIONS

def get_cohort_definition(cohort_name: str):
    """
    Tool to retrieve specific cohort definition by name.
    
    Args:
        cohort_name (str): Name of the cohort (e.g., 'diabetic', 'obesity', 'cancer_screening')
        
    Returns:
        dict or None: Cohort definition if found, None if not found
    """
    return COHORT_DEFINITIONS.get(cohort_name)

def get_all_cohort_names():
    """
    Tool to get list of all available cohort names.
    
    Returns:
        list: List of cohort names
    """
    return list(COHORT_DEFINITIONS.keys())

def get_classification_criteria(cohort_name: str):
    """
    Tool to get classification criteria for determining if a patient belongs to a cohort.
    
    Args:
        cohort_name (str): Name of the cohort
        
    Returns:
        list: Classification criteria for the cohort
    """
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    return cohort.get("classification_criteria", []) if cohort else []

def get_intervention_criteria(cohort_name: str):
    """
    Tool to get intervention criteria for determining if a patient needs outreach.
    
    Args:
        cohort_name (str): Name of the cohort
        
    Returns:
        list: Intervention criteria for the cohort
    """
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    return cohort.get("intervention_criteria", []) if cohort else []

def get_available_interventions(cohort_name: str):
    """
    Tool to get available intervention types and message templates for a cohort.
    
    Args:
        cohort_name (str): Name of the cohort
        
    Returns:
        list: Available interventions with types, descriptions, and message templates
    """
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    return cohort.get("available_interventions", []) if cohort else []

def get_key_indicators(cohort_name: str):
    """
    Tool to get key medical indicators/keywords for a specific cohort.
    
    Args:
        cohort_name (str): Name of the cohort
        
    Returns:
        list: Key medical indicators for the cohort
    """
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    return cohort.get("key_indicators", []) if cohort else []