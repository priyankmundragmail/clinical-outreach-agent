"""
Logging and Display Utilities for Clinical Outreach Agent

This module provides clean, formatted output functions to separate
presentation logic from business logic.
"""

import traceback
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Initialize console with fixed width
console = Console(width=120, force_terminal=True)

class WorkflowLogger:
    """Centralized logging for the clinical outreach workflow."""
    
    @staticmethod
    def print_header(title: str, subtitle: str = None):
        """Print a formatted header for the application."""
        print("=" * 60)
        print(f"🏥 {title}")
        if subtitle:
            print(subtitle)
        print("=" * 60)
    
    @staticmethod
    def print_section(title: str, width: int = 80):
        """Print a section separator."""
        print("\n" + "=" * width)
        print(title)
        print("=" * width)
    
    @staticmethod
    def print_subsection(title: str, width: int = 50):
        """Print a subsection separator."""
        print("\n" + "-" * width)
        print(title)
        print("-" * width)
    
    @staticmethod
    def print_step(step_num: int, description: str):
        """Print a workflow step."""
        print(f"\n{step_num}. {description}")
    
    @staticmethod
    def print_success(message: str):
        """Print a success message."""
        print(f"✅ {message}")
    
    @staticmethod
    def print_warning(message: str):
        """Print a warning message."""
        print(f"⚠️ {message}")
    
    @staticmethod
    def print_error(message: str):
        """Print an error message."""
        print(f"❌ {message}")
    
    @staticmethod
    def print_info(message: str):
        """Print an info message."""
        print(f"ℹ️ {message}")
    
    @staticmethod
    def print_llm_reasoning(content: str):
        """Print LLM reasoning with proper formatting."""
        WorkflowLogger.print_section("🧠 LLM REASONING PROCESS:")
        print(content)
        print("=" * 80)
    
    @staticmethod
    def print_tool_calls(tool_calls: list):
        """Print tool calls in a formatted way."""
        print(f"\n🔧 LLM wants to call {len(tool_calls)} tool(s):")
        
        for i, tool_call in enumerate(tool_calls, 1):
            tool_name = tool_call.get('name', 'Unknown')
            tool_args = tool_call.get('args', {})
            
            print(f"\n{i}. Tool: {tool_name}")
            print(f"   Args: {tool_args}")
    
    @staticmethod
    def print_tool_execution(tool_num: int, tool_name: str, tool_args: dict):
        """Print tool execution start."""
        WorkflowLogger.print_subsection(f"🔧 EXECUTING TOOL #{tool_num}: {tool_name}")
        print(f"📋 Tool Arguments:")
        for key, value in tool_args.items():
            print(f"   • {key}: {value}")
    
    @staticmethod
    def print_tool_result(tool_name: str, result: str, execution_time: float = None):
        """Print tool execution result."""
        if execution_time:
            print(f"✅ {tool_name} completed in {execution_time:.2f}s")
        else:
            print(f"✅ {tool_name} completed")
        
        print(f"\n📊 TOOL OUTPUT:")
        print("-" * 30)
        
        # Handle long results
        if len(str(result)) > 200:
            print(f"{str(result)[:200]}...")
            print(f"\n[Full output: {len(str(result))} characters]")
        else:
            print(str(result))
        print("-" * 50)
    
    @staticmethod
    def print_tool_error(tool_name: str, error: Exception, tool_args: dict = None):
        """Print tool execution error."""
        print(f"❌ Tool '{tool_name}' failed: {str(error)}")
        print(f"   Error type: {type(error).__name__}")
        if tool_args:
            print(f"   Tool args: {tool_args}")
        
        print("📋 Full error traceback:")
        traceback.print_exc()
    
    @staticmethod
    def print_routing_decision(last_message, has_tool_calls: bool, tool_count: int = 0):
        """Print routing decision information."""
        print(f"\n🔄 ROUTING DECISION:")
        print(f"   Last message type: {type(last_message).__name__}")
        print(f"   Has tool_calls: {has_tool_calls}")
        
        if has_tool_calls:
            print(f"   ✅ Routing to tools: {tool_count} tool(s) to execute")
        else:
            print("   🏁 Routing to END: Workflow complete")
    
    @staticmethod
    def print_workflow_complete(message_count: int):
        """Print workflow completion message."""
        WorkflowLogger.print_section(f"🏁 TOOL EXECUTION COMPLETE - {message_count} result(s)")
    
    @staticmethod
    def print_validation_warning(patient_id: int, issue: str):
        """Print validation warning."""
        print(f"   ⚠️  WARNING: Patient {patient_id} {issue}")
    
    @staticmethod
    def print_graph_architecture():
        """Print the workflow architecture diagram."""
        WorkflowLogger.print_subsection("🏗️ WORKFLOW ARCHITECTURE:")
        print("START → Planning → LLM (with reasoning)")
        print("                     ↓")
        print("                 Router")
        print("                ↙      ↘")
        print("           Tools    →  END")
        print("              ↓")
        print("            LLM")
        print("=" * 50)
    
    @staticmethod
    def debug_workflow_state(result):
        """Debug function to analyze workflow execution."""
        WorkflowLogger.print_section("🔍 WORKFLOW DEBUG ANALYSIS")
        
        if not result or 'messages' not in result:
            print("❌ No result or messages found")
            return
        
        messages = result['messages']
        print(f"📊 Total messages in workflow: {len(messages)}")
        
        for i, msg in enumerate(messages, 1):
            msg_type = type(msg).__name__
            content_preview = str(msg.content)[:100] + "..." if len(str(msg.content)) > 100 else str(msg.content)
            
            print(f"\n{i:2d}. {msg_type}")
            print(f"    Content: {content_preview}")
            
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"    Tool calls: {len(msg.tool_calls)}")
                for j, tool_call in enumerate(msg.tool_calls, 1):
                    print(f"      {j}. {tool_call.get('name', 'Unknown')}: {tool_call.get('args', {})}")
            
            # Check for fire_reminder calls
            if 'fire_reminder' in str(msg.content).lower():
                print(f"    🔔 REMINDER DETECTED in message {i}")
        
        print("=" * 60)

class ProgressTracker:
    """Progress tracking utilities."""
    
    @staticmethod
    def create_spinner(description: str):
        """Create a progress spinner."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        )
    
    @staticmethod
    def print_progress_steps():
        """Print the main workflow steps."""
        print("\n📋 Workflow Steps:")
        print("1. Planning Phase")
        print("2. LLM Analysis")
        print("3. Tool Execution")
        print("4. Result Processing")