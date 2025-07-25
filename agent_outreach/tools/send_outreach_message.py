def send_outreach_message(patient_data: dict) -> str:
    if patient_data.get("due_for_screening"):
        return f"Message sent to {patient_data['name']} for screening reminder."
    return "No message sent."
