# tools/cohort_definitions.py

COHORT_DEFINITIONS = {
    "diabetic": {
        "name": "Diabetic Management",
        "description": "Patients with diabetes requiring ongoing management and monitoring",
        "classification_criteria": [
            "Supporting facts include any form of diabetes (Type 1, Type 2, etc.)",
            "HbA1c levels documented in patient data",
            "Taking diabetes medications (Metformin, Insulin, etc.)",
            "Elevated fasting glucose levels (>126 mg/dL)",
            "History of diabetic complications"
        ],
        "intervention_criteria": [
            "HbA1c > 7.0% indicates need for better glucose control",
            "Fasting glucose > 130 mg/dL suggests intervention needed",
            "Poor medication adherence or missed refills",
            "Poor glucose monitoring compliance",
            "Recent complications or concerning symptoms"
        ],
        "key_indicators": [
            "diabetes", "diabetic", "hba1c", "insulin", "metformin", 
            "glucose", "blood sugar", "diabetic retinopathy"
        ],
        "available_interventions": [
            {
                "type": "medication_adherence",
                "description": "Reminder about taking diabetes medications consistently",
                "message_template": "Don't forget to take your diabetes medication as prescribed. Consistent medication helps control blood sugar."
            },
            {
                "type": "glucose_monitoring", 
                "description": "Reminder to check blood glucose levels regularly",
                "message_template": "Please remember to check your blood glucose levels daily and log the results."
            },
            {
                "type": "routine_followup",
                "description": "Reminder for regular diabetes check-up appointments",
                "message_template": "It's time to schedule your routine diabetes follow-up appointment with your healthcare provider."
            },
            {
                "type": "hba1c_testing",
                "description": "Reminder for HbA1c lab testing",
                "message_template": "You're due for your HbA1c test to monitor your diabetes control over the past 3 months."
            }
        ]
    },
    
    "obesity": {
        "name": "Obesity Management", 
        "description": "Patients with BMI ≥30 requiring weight management support",
        "classification_criteria": [
            "BMI ≥30 or supporting facts explicitly mention obesity",
            "Weight-related health conditions (sleep apnea, metabolic syndrome)",
            "Joint problems related to excess weight",
            "Documentation of weight management needs"
        ],
        "intervention_criteria": [
            "BMI ≥35 (severe obesity) requires immediate intervention",
            "Weight-related complications (sleep apnea, joint pain)",
            "No active weight management program in place",
            "Poor dietary habits or sedentary lifestyle",
            "Weight gain trend or lack of progress"
        ],
        "key_indicators": [
            "obesity", "obese", "bmi", "overweight", "weight management",
            "sleep apnea", "metabolic syndrome", "weight loss"
        ],
        "available_interventions": [
            {
                "type": "weight_management",
                "description": "General weight management program reminder",
                "message_template": "Join our comprehensive weight management program to achieve your health goals safely and effectively."
            },
            {
                "type": "nutrition_counseling",
                "description": "Reminder for nutritionist consultation",
                "message_template": "Schedule a consultation with our registered dietitian to develop a personalized nutrition plan."
            },
            {
                "type": "exercise_program",
                "description": "Physical activity and exercise program",
                "message_template": "Our supervised exercise program can help you start a safe and effective fitness routine."
            },
            {
                "type": "behavioral_support",
                "description": "Behavioral and lifestyle modification support",
                "message_template": "Consider joining our behavioral support group to develop healthy lifestyle habits."
            }
        ]
    },
    
    "cancer_screening": {
        "name": "Cancer Screening",
        "description": "Patients due for preventive cancer screening",
        "classification_criteria": [
            "Age-appropriate for cancer screening (varies by screening type)",
            "Family history of cancer",
            "Overdue for routine cancer screening",
            "High-risk factors for specific cancers"
        ],
        "intervention_criteria": [
            "Overdue for age-appropriate screening (>1 year past due)",
            "High-risk family history without recent screening",
            "Never had baseline screening at appropriate age",
            "Concerning symptoms requiring follow-up",
            "Previous abnormal results requiring monitoring"
        ],
        "key_indicators": [
            "screening", "cancer", "family history", "overdue", "colonoscopy", 
            "mammography", "pap smear", "risk factors"
        ],
        "available_interventions": [
            {
                "type": "overdue_screening",
                "description": "Reminder for overdue cancer screening",
                "message_template": "You are overdue for your cancer screening. Please contact us to schedule your appointment."
            },
            {
                "type": "screening_reminder",
                "description": "General screening reminder",
                "message_template": "It's time for your routine cancer screening. Early detection saves lives."
            },
            {
                "type": "appointment_scheduling",
                "description": "Help with scheduling screening appointment",
                "message_template": "We can help you schedule your cancer screening appointment. Call us at your convenience."
            },
            {
                "type": "high_risk_counseling",
                "description": "Genetic counseling for high-risk patients",
                "message_template": "Given your family history, consider genetic counseling to assess your cancer risk."
            }
        ]
    }
}

# Helper functions for LLM to use
def get_cohort_definitions():
    """Get cohort definitions with classification criteria and interventions."""
    return COHORT_DEFINITIONS

def get_cohort_by_name(cohort_name):
    """Get specific cohort definition by name."""
    return COHORT_DEFINITIONS.get(cohort_name)

def get_all_cohort_names():
    """Get list of all available cohort names."""
    return list(COHORT_DEFINITIONS.keys())

def get_classification_criteria(cohort_name):
    """Get classification criteria for a specific cohort."""
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    return cohort.get("classification_criteria", []) if cohort else []

def get_intervention_criteria(cohort_name):
    """Get intervention criteria for a specific cohort."""
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    return cohort.get("intervention_criteria", []) if cohort else []

def get_available_interventions(cohort_name):
    """Get available interventions for a specific cohort."""
    cohort = COHORT_DEFINITIONS.get(cohort_name)
    return cohort.get("available_interventions", []) if cohort else []