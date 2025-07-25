"""
Workflow Executor for Clinical Outreach Agent

Handles the execution and management of the clinical outreach workflow.
"""

import time
from langchain_core.messages import HumanMessage, SystemMessage

from ..graph.graph_builder import GraphBuilder
from ..prompts.prompt_templates import PromptTemplates
from ..utils.logging_utils import WorkflowLogger, ProgressTracker
from ..utils.exception_handler import ErrorHandlingContext  # Updated import

class WorkflowExecutor:
    """Executes the clinical outreach workflow."""
    
    def __init__(self):
        # Initialize workflow executor with graph builder and empty app state
        self.graph_builder = GraphBuilder()
        self.app = None
    
    def initialize(self):
        # Create and compile the LangGraph workflow application
        """Initialize the workflow application."""
        WorkflowLogger.print_info("Initializing enhanced agent...")
        self.app = self.graph_builder.create_graph()
        WorkflowLogger.print_success("Enhanced agent ready!")
    
    def execute_workflow(self):
        # Execute the main workflow with system and human messages
        """Execute the complete clinical outreach workflow."""
        if not self.app:
            raise ValueError("Workflow not initialized. Call initialize() first.")
        
        WorkflowLogger.print_info("Starting enhanced clinical outreach workflow...")
        ProgressTracker.print_progress_steps()
        
        # Generate unique thread ID for this workflow execution
        thread_id = f"enhanced-test-{int(time.time())}"
        
        # Invoke the workflow with system and workflow start prompts
        result = self.app.invoke({
            "messages": [
                SystemMessage(content=PromptTemplates.SYSTEM_PROMPT),
                HumanMessage(content=PromptTemplates.WORKFLOW_START_PROMPT)
            ]
        }, config={"configurable": {"thread_id": thread_id}})
        
        return result
    
    def analyze_results(self, result):
        # Analyze workflow output and check if reminders were successfully fired
        """Analyze and report workflow results."""
        WorkflowLogger.print_section("🎯 WORKFLOW COMPLETED SUCCESSFULLY!")
        
        if result and 'messages' in result and result['messages']:
            # Print the final message content from the workflow
            print(result['messages'][-1].content)
            
            # Check if reminders were fired based on final message content
            final_content = result['messages'][-1].content.lower()
            if 'reminder sent' in final_content or 'fire_reminder' in final_content:
                WorkflowLogger.print_success("Reminders were fired successfully!")
            else:
                WorkflowLogger.print_warning("No reminders appear to have been fired")
        else:
            WorkflowLogger.print_warning("No valid result returned from workflow")
    
    def run(self):
        # Main entry point that orchestrates the complete workflow execution with error handling
        """Run the complete workflow with proper error handling."""
        with ErrorHandlingContext("Clinical Outreach Agent v2.0"):  # Updated usage
            # Print workflow header and initialize components
            WorkflowLogger.print_header("Clinical Outreach Agent v2.0", "Enhanced with Reasoning & Validation")
            
            # Execute initialization, workflow, and result analysis phases
            self.initialize()
            result = self.execute_workflow()
            self.analyze_results(result)
            
            return result
