# tools/access_patient_data.py

from .mock_data import PATIENTS

def get_all_patients():
    """
    Tool to retrieve all patient data for LLM analysis.
    
    Returns:
        list: Complete list of all patients with their medical information
    """
    print("\n🔍 GET_ALL_PATIENTS - Retrieving all patient data...")
    print(f"📊 Found {len(PATIENTS)} patient(s) in database")
    
    for i, patient in enumerate(PATIENTS, 1):
        print(f"   {i}. Patient {patient.get('patient_id', 'Unknown')}: {patient.get('name', 'Unknown Name')}")
    
    result = PATIENTS
    print(f"✅ Returning {len(result)} patient records")
    return result

def get_patient_by_id(patient_id: int):
    """
    Tool to retrieve specific patient data by patient ID.
    
    Args:
        patient_id (int): The unique identifier for the patient
        
    Returns:
        dict or None: Patient data if found, None if not found
    """
    print(f"\n🔍 GET_PATIENT_BY_ID - Searching for Patient ID: {patient_id}")
    
    result = next((p for p in PATIENTS if p["patient_id"] == patient_id), None)
    
    if result:
        print(f"✅ Found patient: {result.get('name', 'Unknown Name')}")
        print(f"   📋 Supporting facts: {result.get('supporting_facts', [])}")
        print(f"   📅 Age: {result.get('age', 'Unknown')}")
        print(f"   📞 Contact: {result.get('phone', 'No phone')} | {result.get('email', 'No email')}")
    else:
        print(f"❌ Patient ID {patient_id} not found in database")
    
    return result

def search_patients_by_supporting_facts(search_terms: list):
    """
    Tool to search patients based on supporting facts/medical conditions.
    
    Args:
        search_terms (list): List of terms to search for in supporting facts
        
    Returns:
        list: Patients whose supporting facts contain any of the search terms
    """
    print(f"\n🔍 SEARCH_PATIENTS_BY_SUPPORTING_FACTS - Searching for terms: {search_terms}")
    
    matching_patients = []
    for patient in PATIENTS:
        supporting_facts = patient.get("supporting_facts", [])
        for term in search_terms:
            if any(term.lower() in fact.lower() for fact in supporting_facts):
                matching_patients.append(patient)
                print(f"   ✅ Match found: Patient {patient.get('patient_id')} ({patient.get('name')}) - {supporting_facts}")
                break
    
    if not matching_patients:
        print("   ❌ No patients found matching the search terms")
    
    print(f"📊 Total matches: {len(matching_patients)} patient(s)")
    return matching_patients

def get_patients_by_age_range(min_age: int = None, max_age: int = None):
    """
    Tool to filter patients by age range.
    
    Args:
        min_age (int, optional): Minimum age filter
        max_age (int, optional): Maximum age filter
        
    Returns:
        list: Patients within the specified age range
    """
    age_filter = f"min_age={min_age}, max_age={max_age}"
    print(f"\n🔍 GET_PATIENTS_BY_AGE_RANGE - Filtering by age: {age_filter}")
    
    filtered_patients = []
    for patient in PATIENTS:
        age = patient.get("age")
        if age is None:
            print(f"   ⚠️  Skipping Patient {patient.get('patient_id')} - no age data")
            continue
            
        if min_age is not None and age < min_age:
            print(f"   ❌ Patient {patient.get('patient_id')} (age {age}) below minimum age {min_age}")
            continue
        if max_age is not None and age > max_age:
            print(f"   ❌ Patient {patient.get('patient_id')} (age {age}) above maximum age {max_age}")
            continue
            
        filtered_patients.append(patient)
        print(f"   ✅ Patient {patient.get('patient_id')} ({patient.get('name')}, age {age}) matches criteria")
    
    print(f"📊 Age filter results: {len(filtered_patients)} patient(s) match the criteria")
    return filtered_patients

def get_patient_contact_info(patient_id: int):
    """
    Tool to get patient contact information for sending reminders.
    
    Args:
        patient_id (int): The unique identifier for the patient
        
    Returns:
        dict or None: Contact info (name, phone, email) if patient found
    """
    print(f"\n🔍 GET_PATIENT_CONTACT_INFO - Getting contact info for Patient ID: {patient_id}")
    
    patient = get_patient_by_id(patient_id)
    if patient:
        contact_info = {
            "patient_id": patient["patient_id"],
            "name": patient["name"],
            "phone": patient.get("phone"),
            "email": patient.get("email")
        }
        
        print(f"📞 Contact Information:")
        print(f"   • Name: {contact_info['name']}")
        print(f"   • Phone: {contact_info['phone']}")
        print(f"   • Email: {contact_info['email']}")
        
        return contact_info
    else:
        print(f"❌ Cannot get contact info - Patient ID {patient_id} not found")
        return None

# Additional helper function to find patients needing intervention
def find_patient(patient_id: int):
    """
    Enhanced patient finder with detailed logging.
    
    Args:
        patient_id (int): The unique identifier for the patient
        
    Returns:
        str: Formatted patient information or error message
    """
    print(f"\n🔍 FIND_PATIENT - Detailed lookup for Patient ID: {patient_id}")
    
    patient = next((p for p in PATIENTS if p["patient_id"] == patient_id), None)
    
    if not patient:
        error_msg = f"Patient with ID {patient_id} not found in database"
        print(f"❌ {error_msg}")
        return error_msg
    
    # Format detailed patient information
    patient_info = f"""
Patient {patient['patient_id']}: {patient['name']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Supporting Facts: {', '.join(patient.get('supporting_facts', []))}
📅 Age: {patient.get('age', 'Unknown')}
📞 Phone: {patient.get('phone', 'Not provided')}
📧 Email: {patient.get('email', 'Not provided')}
"""
    
    # Add condition-specific details
    if 'diabetes' in str(patient.get('supporting_facts', [])).lower():
        if 'last_hba1c' in patient:
            patient_info += f"🩸 Last HbA1c: {patient['last_hba1c']}\n"
        if 'fasting_glucose' in patient:
            patient_info += f"🍯 Fasting Glucose: {patient['fasting_glucose']}\n"
        if 'medications' in patient:
            patient_info += f"💊 Medications: {', '.join(patient['medications'])}\n"
    
    if 'cancer' in str(patient.get('supporting_facts', [])).lower():
        if 'last_colonoscopy' in patient:
            patient_info += f"🔬 Last Colonoscopy: {patient['last_colonoscopy']}\n"
        if 'family_history' in patient:
            patient_info += f"👨‍👩‍👧‍👦 Family History: {', '.join(patient['family_history'])}\n"
    
    patient_info += f"🏥 Last Visit: {patient.get('last_visit', 'Unknown')}"
    
    print(f"✅ Patient found and detailed information compiled")
    print(patient_info)
    
    return patient_info