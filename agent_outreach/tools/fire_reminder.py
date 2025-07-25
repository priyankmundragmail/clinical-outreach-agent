from pydantic import BaseModel
import traceback

class FireReminderInput(BaseModel):
    """Input schema for firing reminders."""
    patient_id: int
    reminder_type: str = "general"

def fire_reminder(patient_id: int, reminder_type: str, priority: str = "normal") -> str:
    """Send a reminder to a specific patient with enhanced error logging."""
    try:
        print(f"🔔 Firing reminder for Patient {patient_id}")
        print(f"   Type: {reminder_type}")
        print(f"   Priority: {priority}")
        
        result = f"Reminder sent to Patient {patient_id}: {reminder_type}"
        print(f"✅ {result}")
        return result
        
    except Exception as e:
        error_msg = f"Failed to send reminder to Patient {patient_id}: {str(e)}"
        print(f"❌ {error_msg}")
        print(f"Error type: {type(e).__name__}")
        print("📋 Fire reminder error traceback:")
        traceback.print_exc()
        raise