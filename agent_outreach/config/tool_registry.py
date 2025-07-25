"""
Tool Registry and Configuration

Centralized tool definitions and LLM configuration.
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import StructuredTool
from dotenv import load_dotenv

from ..tools.find_unmet_patients import find_unmet_patients, FindUnmetPatientsInput
from ..tools.fire_reminder import fire_reminder, FireReminderInput
from ..tools.access_patient_data import get_all_patients, find_patient
from ..tools.cohort_tools import get_all_cohorts, get_cohort_info, get_cohort_summary

# Load environment variables
load_dotenv()

class ToolRegistry:
    """Centralized tool registry and LLM configuration."""
    
    @staticmethod
    def get_llm(model: str = "gpt-3.5-turbo", timeout: int = 30, max_retries: int = 2):
        """Get configured LLM instance."""
        return ChatOpenAI(model=model, timeout=timeout, max_retries=max_retries)
    
    @staticmethod
    def get_tools():
        """Get all available tools."""
        return [
            StructuredTool.from_function(
                func=fire_reminder, 
                name="fire_reminder", 
                description="Send a reminder to a specific patient.", 
                args_schema=FireReminderInput
            ),
            StructuredTool.from_function(
                func=get_all_patients, 
                name="get_all_patients", 
                description="Get complete list of all patients for analysis and cohort classification."
            ),
            StructuredTool.from_function(
                func=find_patient, 
                name="find_patient", 
                description="Find a specific patient by their ID for detailed information."
            ),
            StructuredTool.from_function(
                func=get_all_cohorts, 
                name="get_all_cohorts", 
                description="Get complete list of all available cohorts with their definitions and criteria."
            ),
            StructuredTool.from_function(
                func=get_cohort_info, 
                name="get_cohort_info", 
                description="Get detailed information about a specific cohort including classification and intervention criteria."
            ),
            StructuredTool.from_function(
                func=get_cohort_summary, 
                name="get_cohort_summary", 
                description="Generate a summary overview of all available cohorts for quick reference."
            )
        ]
    
    @staticmethod
    def get_llm_with_tools():
        """Get LLM bound with all tools."""
        llm = ToolRegistry.get_llm()
        tools = ToolRegistry.get_tools()
        return llm.bind_tools(tools)
