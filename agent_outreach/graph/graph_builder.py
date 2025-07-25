"""
Graph Builder for Clinical Outreach Workflow

Handles the construction and configuration of the LangGraph workflow.
"""

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from ..state import OutreachState
from ..nodes.workflow_nodes import WorkflowNodes
from ..utils.logging_utils import WorkflowLogger
from ..utils.exception_handler import ExceptionHandler, GraphBuildError

class GraphBuilder:
    """Builder for the clinical outreach workflow graph."""
    
    def __init__(self):
        self.nodes = WorkflowNodes()
    
    def create_graph(self):
        """Create and configure the clinical outreach graph."""
        WorkflowLogger.print_info("Building Clinical Outreach Graph with Reasoning...")
        
        builder = StateGraph(OutreachState, name="ClinicalOutreachGraph")
        
        # Add nodes
        builder.add_node("planning", self.nodes.planning_node)
        builder.add_node("llm", self.nodes.call_llm)
        builder.add_node("tools", self.nodes.enhanced_tool_node)
        
        # Add edges
        builder.add_edge(START, "planning")
        builder.add_edge("planning", "llm")
        builder.add_edge("tools", "llm")
        
        # Add conditional routing
        builder.add_conditional_edges("llm", self._routing_with_validation)
        
        # Compile graph with safe error handling
        try:
            memory = MemorySaver()
            graph = builder.compile(checkpointer=memory)
            WorkflowLogger.print_success("Enhanced Graph built successfully with reasoning support!")
        except Exception as e:
            try:
                ExceptionHandler.handle_graph_build_error(e)
            except GraphBuildError:
                # Fallback: build without memory
                WorkflowLogger.print_info("Attempting to build graph without memory...")
                graph = builder.compile()
                WorkflowLogger.print_success("Graph built successfully (without memory)!")
        
        WorkflowLogger.print_graph_architecture()
        return graph
    
    def _routing_with_validation(self, state):
        """Enhanced routing logic with validation."""
        last_message = state["messages"][-1]
        has_tool_calls = hasattr(last_message, 'tool_calls') and last_message.tool_calls
        tool_count = len(last_message.tool_calls) if has_tool_calls else 0
        
        WorkflowLogger.print_routing_decision(last_message, has_tool_calls, tool_count)
        return "tools" if has_tool_calls else END
