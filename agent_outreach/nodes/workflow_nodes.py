"""
Workflow Node Definitions

Individual node functions for the LangGraph workflow.
"""

import time
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage

from ..config.tool_registry import ToolRegistry
from ..prompts.prompt_templates import PromptTemplates
from ..utils.logging_utils import WorkflowLogger
from ..utils.exception_handler import safe_execute, safe_tool_execution, ExceptionHandler

class WorkflowNodes:
    """Collection of workflow node functions."""
    
    def __init__(self):
        self.llm = ToolRegistry.get_llm()
        self.llm_with_tools = ToolRegistry.get_llm_with_tools()
        self.tools = ToolRegistry.get_tools()
    
    @safe_execute("LLM call")
    def call_llm(self, state):
        """Call the LLM with explicit reasoning requirement."""
        WorkflowLogger.print_info("Calling LLM with reasoning...")
        
        # Enhance messages with reasoning prompt
        enhanced_messages = []
        for msg in state["messages"]:
            if isinstance(msg, SystemMessage):
                enhanced_content = PromptTemplates.get_enhanced_system_message(msg.content)
                enhanced_messages.append(SystemMessage(content=enhanced_content))
            else:
                enhanced_messages.append(msg)
        
        try:
            WorkflowLogger.print_info("Sending request to OpenAI...")
            response = self.llm_with_tools.invoke(enhanced_messages)
            WorkflowLogger.print_success("Received response from OpenAI")
            
            # Display LLM reasoning
            WorkflowLogger.print_llm_reasoning(response.content)
            
            # Analyze tool calls
            if hasattr(response, 'tool_calls') and response.tool_calls:
                WorkflowLogger.print_tool_calls(response.tool_calls)
                self._validate_tool_calls(response.tool_calls)
            else:
                WorkflowLogger.print_info("LLM provided final response (no tool calls)")
            
            return {"messages": [response]}
            
        except Exception as e:
            ExceptionHandler.handle_llm_call_error(e, "reasoning workflow")
    
    @safe_execute("planning")
    def planning_node(self, state):
        """Generate execution plan with detailed reasoning requirements."""
        WorkflowLogger.print_info("Generating detailed execution plan...")
        
        planning_messages = state["messages"] + [SystemMessage(content=PromptTemplates.PLANNING_PROMPT)]
        
        try:
            plan_response = self.llm.invoke(planning_messages)
            
            WorkflowLogger.print_section("�� DETAILED EXECUTION PLAN:")
            print(plan_response.content)
            WorkflowLogger.print_section("")
            
            # Validation check
            if "patient 5" in plan_response.content.lower():
                WorkflowLogger.print_success("Plan includes Patient 5 validation!")
            else:
                WorkflowLogger.print_warning("Plan should mention Patient 5 validation!")
            
            return {"messages": state["messages"] + [AIMessage(content=f"ENHANCED PLAN:\n{plan_response.content}")]}
        
        except Exception as e:
            ExceptionHandler.handle_llm_call_error(e, "planning phase")
    
    def enhanced_tool_node(self, state):
        """Enhanced tool node with detailed logging and safe execution."""
        WorkflowLogger.print_section("🛠️ TOOL EXECUTION PHASE")
        
        try:
            last_message = state["messages"][-1]
            
            if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
                WorkflowLogger.print_error("No tool calls found in message")
                return {"messages": []}
            
            tool_messages = []
            
            for i, tool_call in enumerate(last_message.tool_calls, 1):
                tool_name = tool_call.get('name', 'Unknown')
                tool_args = tool_call.get('args', {})
                tool_id = tool_call.get('id', 'unknown')
                
                WorkflowLogger.print_tool_execution(i, tool_name, tool_args)
                
                # Find tool function
                tool_func = self._find_tool_function(tool_name)
                
                if not tool_func:
                    error_msg = f"Tool '{tool_name}' not found"
                    WorkflowLogger.print_error(error_msg)
                    tool_messages.append(ToolMessage(content=error_msg, tool_call_id=tool_id))
                    continue
                
                # Execute tool safely
                start_time = time.time()
                WorkflowLogger.print_info(f"Executing {tool_name}...")
                
                success, result = safe_tool_execution(tool_name, tool_func, tool_args)
                execution_time = time.time() - start_time
                
                if success:
                    WorkflowLogger.print_tool_result(tool_name, result, execution_time)
                
                tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_id))
            
            WorkflowLogger.print_workflow_complete(len(tool_messages))
            return {"messages": tool_messages}
            
        except Exception as e:
            error_msg = f"Critical error in tool execution: {str(e)}"
            WorkflowLogger.print_error(error_msg)
            return {"messages": [ToolMessage(content=error_msg, tool_call_id="error")]}
    
    def _find_tool_function(self, tool_name: str):
        """Find tool function by name."""
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.func
        return None
    
    def _validate_tool_calls(self, tool_calls):
        """Validate tool calls for suspicious actions."""
        for tool_call in tool_calls:
            if tool_call.get('name') == "fire_reminder":
                patient_id = tool_call.get('args', {}).get('patient_id')
                reminder_type = tool_call.get('args', {}).get('reminder_type', '')
                
                if patient_id == 5 and "hba1c" in reminder_type.lower():
                    WorkflowLogger.print_validation_warning(patient_id, "is cancer screening, not diabetic!")
                    user_input = input("\n⚠️ Suspicious action detected! Continue? (y/n): ")
                    if user_input.lower() != 'y':
                        raise ValueError("Action cancelled due to classification concern.")
