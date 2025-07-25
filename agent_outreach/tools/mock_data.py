# tools/mock_data.py

PATIENTS = [
    # DIABETIC COHORT - Patient 1: Needs intervention (poor control)
    {
        "patient_id": 1, 
        "name": "Alice Johnson",
        "phone": "555-0101",
        "email": "alice.johnson@email.com",
        "supporting_facts": ["Type 2 Diabetes", "Hypertension"],
        "last_hba1c": "8.2%",
        "last_visit": "2024-05-15",
        "medications": ["Metformin", "Lisinopril"],
        "age": 58,
        "bmi": 28.5,
        "blood_pressure": "140/90",
        "fasting_glucose": "185 mg/dL",
        "last_medication_refill": "2024-04-10"
    }
    ,

    # DIABETIC COHORT - Patient 2: No intervention needed (well controlled)
    {
        "patient_id": 2, 
        "name": "Grace Thompson",
        "phone": "555-0102",
        "email": "grace.thompson@email.com",
        "supporting_facts": ["Type 2 Diabetes", "Excellent Glycemic Control"],
        "last_hba1c": "6.5%",
        "last_visit": "2024-06-20",
        "medications": ["Metformin", "Lifestyle Management"],
        "age": 62,
        "bmi": 25.8,
        "blood_pressure": "118/72",
        "fasting_glucose": "105 mg/dL",
        "medication_adherence": "Perfect compliance",
        "diabetes_education_completed": "Yes - Annual refresher completed"
    },
    
    # OBESITY COHORT - Patient 3: Needs intervention (severe obesity with complications)
    {
        "patient_id": 3, 
        "name": "David Wilson",
        "phone": "555-0103",
        "email": "david.wilson@email.com",
        "supporting_facts": ["Morbid Obesity", "Sleep Apnea", "Metabolic Syndrome"],
        "bmi": 35.2,
        "last_visit": "2024-03-15",
        "medications": ["CPAP Machine Usage"],
        "age": 42,
        "weight": "280 lbs",
        "height": "5'10\"",
        "waist_circumference": "48 inches",
        "sleep_study_results": "Severe OSA - AHI 45"
    },
    
    # OBESITY COHORT - Patient 4: No intervention needed (actively managing well)
    {
        "patient_id": 4, 
        "name": "Henry Rodriguez",
        "phone": "555-0104",
        "email": "henry.rodriguez@email.com",
        "supporting_facts": ["Obesity Class I", "Active Weight Management"],
        "bmi": 31.2,
        "last_visit": "2024-06-15",
        "medications": ["Multivitamin", "Prescribed Exercise Program"],
        "age": 46,
        "weight": "210 lbs",
        "height": "5'8\"",
        "current_weight_trend": "Losing 2 lbs per month consistently",
        "nutrition_counselor": "Meeting weekly with registered dietitian",
        "exercise_compliance": "Excellent - 5 days per week"
    },
    
    # CANCER SCREENING COHORT - Patient 5: Needs intervention (overdue screening)
    {
        "patient_id": 5, 
        "name": "Frank Miller",
        "phone": "555-0105",
        "email": "frank.miller@email.com",
        "supporting_facts": ["Family History of Colorectal Cancer"],
        "age": 52,
        "last_colonoscopy": "2022-08-15",
        "family_history": ["Father: Colon Cancer diagnosed at 58", "Brother: Adenomatous polyps at 45"],
        "risk_factors": ["Age over 50", "Strong family history", "Overdue for screening"],
        "last_visit": "2024-01-10",
        "screening_status": "Overdue by 6 months for follow-up colonoscopy"
    },
    
    # CANCER SCREENING COHORT - Patient 6: No intervention needed (up to date)
    {
        "patient_id": 6, 
        "name": "Irene Kim",
        "phone": "555-0106",
        "email": "irene.kim@email.com",
        "supporting_facts": ["Family History of Breast Cancer", "Current with Screenings"],
        "age": 48,
        "last_mammography": "2024-05-30",
        "last_clinical_exam": "2024-06-01",
        "family_history": ["Mother: Breast Cancer at 52", "Aunt: Ovarian Cancer at 60"],
        "risk_factors": ["Family history", "Age appropriate for screening"],
        "last_visit": "2024-06-01",
        "screening_status": "Up to date with all recommended screenings",
        "genetic_counseling": "Completed - no mutations detected"
    }
]
