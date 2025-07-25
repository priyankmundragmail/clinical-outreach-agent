"""
Workflow Executor for Clinical Outreach Agent

Handles the execution and management of the clinical outreach workflow.
"""

import time
from langchain_core.messages import HumanMessage, SystemMessage

from ..graph.graph_builder import GraphBuilder
from ..prompts.prompt_templates import PromptTemplates
from ..utils.logging_utils import WorkflowLogger, ProgressTracker
from ..utils.exception_handler import WorkflowContext

class WorkflowExecutor:
    """Executes the clinical outreach workflow."""
    
    def __init__(self):
        self.graph_builder = GraphBuilder()
        self.app = None
    
    def initialize(self):
        """Initialize the workflow application."""
        WorkflowLogger.print_info("Initializing enhanced agent...")
        self.app = self.graph_builder.create_graph()
        WorkflowLogger.print_success("Enhanced agent ready!")
    
    def execute_workflow(self):
        """Execute the complete clinical outreach workflow."""
        if not self.app:
            raise ValueError("Workflow not initialized. Call initialize() first.")
        
        WorkflowLogger.print_info("Starting enhanced clinical outreach workflow...")
        ProgressTracker.print_progress_steps()
        
        thread_id = f"enhanced-test-{int(time.time())}"
        
        result = self.app.invoke({
            "messages": [
                SystemMessage(content=PromptTemplates.SYSTEM_PROMPT),
                HumanMessage(content=PromptTemplates.WORKFLOW_START_PROMPT)
            ]
        }, config={"configurable": {"thread_id": thread_id}})
        
        return result
    
    def analyze_results(self, result):
        """Analyze and report workflow results."""
        WorkflowLogger.print_section("🎯 WORKFLOW COMPLETED SUCCESSFULLY!")
        
        if result and 'messages' in result and result['messages']:
            print(result['messages'][-1].content)
            
            # Check if reminders were fired
            final_content = result['messages'][-1].content.lower()
            if 'reminder sent' in final_content or 'fire_reminder' in final_content:
                WorkflowLogger.print_success("Reminders were fired successfully!")
            else:
                WorkflowLogger.print_warning("No reminders appear to have been fired")
        else:
            WorkflowLogger.print_warning("No valid result returned from workflow")
    
    def run(self):
        """Run the complete workflow with proper error handling."""
        with WorkflowContext("Clinical Outreach Agent v2.0"):
            WorkflowLogger.print_header("Clinical Outreach Agent v2.0", "Enhanced with Reasoning & Validation")
            
            self.initialize()
            result = self.execute_workflow()
            self.analyze_results(result)
            
            return result
