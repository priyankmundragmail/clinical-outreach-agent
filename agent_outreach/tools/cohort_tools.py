from .cohort_definitions import COHORT_DEFINITIONS
from .mock_data import PATIENTS
from rich.console import Console
from rich.panel import Panel

console = Console()
  
def get_all_cohorts():
    """Get complete list of all available cohorts with their definitions and criteria."""
    return COHORT_DEFINITIONS

def get_cohort_info(cohort_name: str):
    """
    Get detailed information about a specific cohort.
    
    Args:
        cohort_name: Name of the cohort ("diabetic", "obesity", "cancer_screening")
        
    Returns:
        Dictionary with cohort definition, criteria, and interventions
    """
    return COHORT_DEFINITIONS.get(cohort_name)

def classify_patient(patient_data: dict):
    """
    Classify a patient into appropriate cohorts based on their medical data.
    
    Args:
        patient_data: Patient dictionary with supporting_facts and medical info
        
    Returns:
        List of cohorts this patient likely belongs to
    """
    suggested_cohorts = []
    supporting_facts = patient_data.get("supporting_facts", [])
    
    for cohort_name, cohort_info in COHORT_DEFINITIONS.items():
        key_indicators = cohort_info.get("key_indicators", [])
        
        # Check if any key indicators match supporting facts
        for indicator in key_indicators:
            for fact in supporting_facts:
                if indicator.lower() in fact.lower():
                    if cohort_name not in suggested_cohorts:
                        suggested_cohorts.append(cohort_name)
                    break
    
    return suggested_cohorts

def get_intervention_options(cohort_name: str):
    """
    Get available intervention types and message templates for a cohort.
    
    Args:
        cohort_name: Name of the cohort
        
    Returns:
        List of available interventions with types, descriptions, and templates
    """
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    return cohort.get("available_interventions", []) if cohort else []

def analyze_intervention_need(patient_data: dict, cohort_name: str):
    """
    Analyze if a patient in a specific cohort needs clinical intervention.
    
    Args:
        patient_data: Patient medical information
        cohort_name: Name of the cohort to analyze for
        
    Returns:
        Dictionary with analysis framework for LLM decision-making
    """
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    if not cohort:
        return {"error": f"Cohort '{cohort_name}' not found"}
    
    analysis = {
        "cohort": cohort_name,
        "intervention_criteria": cohort.get("intervention_criteria", []),
        "patient_data_summary": {
            "supporting_facts": patient_data.get("supporting_facts", []),
            "key_metrics": {}
        },
        "needs_llm_evaluation": True
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

def get_cohort_summary():
    """
    Generate a summary overview of all available cohorts for quick reference.
    
    Returns:
        Dictionary with overview of all cohorts and their key characteristics
    """
    summary = {
        "total_cohorts": len(COHORT_DEFINITIONS),
        "cohort_overview": {}
    }
    
    for cohort_name, cohort_info in COHORT_DEFINITIONS.items():
        summary["cohort_overview"][cohort_name] = {
            "name": cohort_info.get("name"),
            "description": cohort_info.get("description"),
            "key_indicators": cohort_info.get("key_indicators", [])[:3],  # First 3 indicators
            "intervention_count": len(cohort_info.get("available_interventions", []))
        }
    
    return summary

def classify_patient_with_debug(patient_id: int) -> str:
    """Classify patient with detailed debugging output."""
    
    patient = next((p for p in PATIENTS if p["patient_id"] == patient_id), None)
    if not patient:
        return f"Patient {patient_id} not found"
    
    # Debug output
    console.print(Panel(
        f"[bold]Patient {patient_id}: {patient['name']}[/bold]\n"
        f"Supporting Facts: {patient.get('supporting_facts', [])}\n"
        f"Age: {patient.get('age', 'Unknown')}\n"
        f"Key Indicators: {list(patient.keys())}",
        title="🔍 Patient Classification Debug",
        border_style="blue"
    ))
    
    # Classification logic with reasoning
    supporting_facts = patient.get("supporting_facts", [])
    
    # Check for diabetes markers
    diabetes_indicators = [
        "last_hba1c" in patient,
        "fasting_glucose" in patient,
        any("diabetes" in str(fact).lower() for fact in supporting_facts),
        "medications" in patient and any("metformin" in str(med).lower() for med in patient.get("medications", []))
    ]
    
    # Check for cancer screening markers  
    cancer_indicators = [
        "family_history" in patient,
        "last_colonoscopy" in patient,
        "last_mammography" in patient,
        any("cancer" in str(fact).lower() for fact in supporting_facts)
    ]
    
    # Check for obesity markers
    obesity_indicators = [
        "bmi" in patient and float(str(patient.get("bmi", "0")).replace(">", "")) >= 30,
        any("obesity" in str(fact).lower() for fact in supporting_facts)
    ]
    
    console.print(f"🔬 [yellow]Classification Analysis:[/yellow]")
    console.print(f"  Diabetes indicators: {diabetes_indicators} (Count: {sum(diabetes_indicators)})")
    console.print(f"  Cancer indicators: {cancer_indicators} (Count: {sum(cancer_indicators)})")
    console.print(f"  Obesity indicators: {obesity_indicators} (Count: {sum(obesity_indicators)})")
    
    # Determine cohort
    if sum(diabetes_indicators) >= 2:
        classification = "DIABETIC COHORT"
    elif sum(cancer_indicators) >= 1:
        classification = "CANCER SCREENING COHORT"
    elif sum(obesity_indicators) >= 1:
        classification = "OBESITY COHORT"
    else:
        classification = "NO SPECIFIC COHORT"
    
    console.print(f"🎯 [green]Final Classification: {classification}[/green]")
    
    return f"Patient {patient['name']} (ID: {patient_id}) classified as: {classification}"