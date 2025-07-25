from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage
from typing_extensions import Annotated

class OutreachState(TypedDict, total=False):
    """State for the clinical outreach workflow"""
    # Graph messages
    messages: Annotated[List[AnyMessage], add_messages]   
    # cohort_info: 
    cohorts: Dict[str, List[str]]
    patient_to_cohort: Dict[str, str]
    cohort_criteria: Optional[str]
