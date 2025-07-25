# tools/cohort_analysis_tools.py

from .access_cohort_definitions import (
    get_all_cohort_definitions, 
    get_key_indicators, 
    get_intervention_criteria
)

def classify_patient_to_cohorts(patient_data: dict):
    """
    Tool to help LLM classify a patient into appropriate cohorts based on their data.
    
    Args:
        patient_data (dict): Patient information including supporting_facts
        
    Returns:
        list: Suggested cohorts this patient might belong to (for LLM to validate)
    """
    suggested_cohorts = []
    supporting_facts = patient_data.get("supporting_facts", [])
    all_cohorts = get_all_cohort_definitions()
    
    for cohort_name, cohort_info in all_cohorts.items():
        key_indicators = cohort_info.get("key_indicators", [])
        
        # Check if any key indicators match supporting facts
        for indicator in key_indicators:
            for fact in supporting_facts:
                if indicator.lower() in fact.lower():
                    if cohort_name not in suggested_cohorts:
                        suggested_cohorts.append(cohort_name)
                    break
    
    return suggested_cohorts

def analyze_intervention_need(patient_data: dict, cohort_name: str):
    """
    Tool to help LLM analyze if a patient in a specific cohort needs intervention.
    
    Args:
        patient_data (dict): Patient information
        cohort_name (str): Name of the cohort to analyze for
        
    Returns:
        dict: Analysis results with criteria and recommendations
    """
    criteria = get_intervention_criteria(cohort_name)
    analysis = {
        "cohort": cohort_name,
        "intervention_criteria": criteria,
        "patient_data_summary": {
            "supporting_facts": patient_data.get("supporting_facts", []),
            "key_metrics": {}
        },
        "llm_should_evaluate": True
    }
    
    # Add relevant metrics based on cohort type
    if cohort_name == "diabetic":
        analysis["patient_data_summary"]["key_metrics"] = {
            "hba1c": patient_data.get("last_hba1c"),
            "glucose": patient_data.get("fasting_glucose"),
            "medication_adherence": patient_data.get("medication_adherence"),
            "medications": patient_data.get("medications", [])
        }
    elif cohort_name == "obesity":
        analysis["patient_data_summary"]["key_metrics"] = {
            "bmi": patient_data.get("bmi"),
            "weight_trend": patient_data.get("current_weight_trend"),
            "exercise_compliance": patient_data.get("exercise_compliance"),
            "complications": [fact for fact in patient_data.get("supporting_facts", []) 
                           if "sleep apnea" in fact.lower() or "metabolic" in fact.lower()]
        }
    elif cohort_name == "cancer_screening":
        analysis["patient_data_summary"]["key_metrics"] = {
            "age": patient_data.get("age"),
            "screening_status": patient_data.get("screening_status"),
            "last_screening": patient_data.get("last_colonoscopy") or patient_data.get("last_mammography"),
            "family_history": patient_data.get("family_history", [])
        }
    
    return analysis

def match_patient_to_interventions(patient_data: dict, cohort_name: str, analysis_results: dict):
    """
    Tool to help LLM match a patient to specific interventions within a cohort.
    
    Args:
        patient_data (dict): Patient information
        cohort_name (str): Name of the cohort
        analysis_results (dict): Results from analyze_intervention_need
        
    Returns:
        dict: Recommended interventions with reasoning
    """
    from .access_cohort_definitions import get_available_interventions
    
    available_interventions = get_available_interventions(cohort_name)
    recommendations = {
        "cohort": cohort_name,
        "patient_id": patient_data.get("patient_id"),
        "patient_name": patient_data.get("name"),
        "needs_intervention": False,
        "recommended_interventions": [],
        "reasoning": []
    }
    
    # LLM should use this data to make intelligent intervention decisions
    # This is a helper tool that structures the data for LLM analysis
    
    recommendations["available_options"] = available_interventions
    recommendations["analysis_summary"] = analysis_results
    recommendations["llm_should_decide"] = True
    
    return recommendations

def evaluate_cohort_membership(patient_data: dict, cohort_name: str):
    """
    Tool to help LLM evaluate if a patient truly belongs to a specific cohort.
    
    Args:
        patient_data (dict): Patient information
        cohort_name (str): Name of the cohort to evaluate
        
    Returns:
        dict: Evaluation framework for LLM decision-making
    """
    from .access_cohort_definitions import get_classification_criteria, get_key_indicators
    
    classification_criteria = get_classification_criteria(cohort_name)
    key_indicators = get_key_indicators(cohort_name)
    
    evaluation = {
        "cohort": cohort_name,
        "classification_criteria": classification_criteria,
        "key_indicators": key_indicators,
        "patient_supporting_facts": patient_data.get("supporting_facts", []),
        "patient_medical_data": {
            "age": patient_data.get("age"),
            "medications": patient_data.get("medications", []),
            "bmi": patient_data.get("bmi"),
            "lab_values": {
                "hba1c": patient_data.get("last_hba1c"),
                "glucose": patient_data.get("fasting_glucose"),
                "blood_pressure": patient_data.get("blood_pressure")
            }
        },
        "llm_evaluation_needed": True,
        "membership_confidence": None  # LLM should set this
    }
    
    return evaluation

def generate_cohort_summary():
    """
    Tool to generate a summary of all available cohorts for LLM reference.
    
    Returns:
        dict: Summary of all cohorts with key information
    """
    all_cohorts = get_all_cohort_definitions()
    summary = {
        "total_cohorts": len(all_cohorts),
        "cohort_overview": {}
    }
    
    for cohort_name, cohort_info in all_cohorts.items():
        summary["cohort_overview"][cohort_name] = {
            "name": cohort_info.get("name"),
            "description": cohort_info.get("description"),
            "key_indicators": cohort_info.get("key_indicators", [])[:3],  # First 3 indicators
            "intervention_count": len(cohort_info.get("available_interventions", []))
        }
    
    return summary