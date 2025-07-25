"""
Clinical Outreach Agent Graph Module

This module defines the LangGraph workflow for clinical patient outreach automation.
It orchestrates the process of finding unmet patient needs and sending reminders.
"""

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState

# Rich imports for beautiful logging and output
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
import logging

from .tools.find_unmet_patients import find_unmet_patients, FindUnmetPatientsInput
from .tools.fire_reminder import fire_reminder, FireReminderInput

# Install rich traceback handler
install(show_locals=True)

# Set up Rich console and logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)
logger = logging.getLogger("clinical_outreach")

# Load environment variables from .env file
load_dotenv()

# Initialize the language model for clinical outreach tasks
llm = ChatOpenAI(model="gpt-3.5-turbo")
tools = [
    StructuredTool.from_function(
        func=find_unmet_patients,
        name="find_unmet_patients",
        description="Find all patients who have unmet needs requiring intervention.",
        args_schema=FindUnmetPatientsInput
    ),
    StructuredTool.from_function(
        func=fire_reminder,
        name="fire_reminder",
        description="Send a reminder to a specific patient.",
        args_schema=FireReminderInput
    )
]

llm_with_tools = llm.bind_tools(tools)

def call_llm(state):
    """Call the LLM with current state and return response."""
    logger.info("🤖 [bold blue]Calling LLM...[/bold blue]", extra={"markup": True})
    
    # Log current message count
    msg_count = len(state["messages"])
    logger.info(f"📊 Processing {msg_count} messages in conversation")
    
    # Log the last message for context
    last_msg = state["messages"][-1]
    if isinstance(last_msg, HumanMessage):
        console.print(Panel(
            f"[green]Human:[/green] {last_msg.content}", 
            title="🗣️ User Input", 
            border_style="green"
        ))
    elif isinstance(last_msg, ToolMessage):
        console.print(Panel(
            f"[blue]Tool Result:[/blue] {last_msg.content[:100]}...", 
            title="🔧 Tool Output", 
            border_style="blue"
        ))
    
    try:
        response = llm_with_tools.invoke(state["messages"])
        
        # Log LLM response details
        if hasattr(response, 'tool_calls') and response.tool_calls:
            logger.info(f"🔧 [yellow]LLM wants to call {len(response.tool_calls)} tool(s)[/yellow]", extra={"markup": True})
            
            # Create table for tool calls
            table = Table(title="🛠️ Tool Calls Requested")
            table.add_column("Tool Name", style="cyan")
            table.add_column("Arguments", style="green")
            
            for i, tool_call in enumerate(response.tool_calls, 1):
                console.print(f"[cyan]Tool Call #{i}:[/cyan]")
                console.print(f"  Name: {tool_call.get('name', 'Unknown')}")
                console.print(f"  ID: {tool_call.get('id', 'Unknown')}")
                console.print(f"  Args: {tool_call.get('args', {})}")
                table.add_row(
                    f"{i}. {tool_call.get('name', 'Unknown')}",
                    str(tool_call.get('args', {}))[:50] + "..."
                )
            console.print(table)
        else:
            logger.info("💬 [green]LLM provided final response[/green]", extra={"markup": True})
            console.print(Panel(
                f"[green]{response.content}[/green]", 
                title="🤖 AI Response", 
                border_style="green"
            ))
            
        return {"messages": [response]}
        
    except Exception as e:
        logger.error(f"❌ [red]Error calling LLM: {str(e)}[/red]", extra={"markup": True})
        raise

def create_graph():
    """Create and configure the clinical outreach graph."""
    logger.info("🏗️ [bold cyan]Building Clinical Outreach Graph...[/bold cyan]", extra={"markup": True})
    
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("llm", call_llm)
    builder.add_node("tools", ToolNode(tools))
    
    # Add edges
    builder.add_edge(START, "llm")
    builder.add_edge("tools", "llm")
    builder.add_conditional_edges("llm", tools_condition)
    
    logger.info("✅ [green]Graph built successfully![/green]", extra={"markup": True})
    return builder.compile()

# Add this to test
if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold blue]🏥 Clinical Outreach Agent[/bold blue]\n[dim]Automating patient care reminders[/dim]",
        border_style="blue"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Initializing agent...", total=None)
            app = create_graph()
            progress.update(task, description="Agent ready!")
            
        logger.info("🚀 [bold green]Starting clinical outreach workflow...[/bold green]", extra={"markup": True})
        
        result = app.invoke(
            {"messages": [HumanMessage(content="Find patients with unmet needs, then send exactly ONE reminder to each patient. Do not send duplicate reminders to the same patient.")]},
            config={"configurable": {"thread_id": "test-1"}}
        )
        
        # Display final result
        console.print("\n" + "="*50)
        console.print(Panel(
            f"[bold green]Workflow Complete![/bold green]\n\n[white]{result['messages'][-1].content}[/white]",
            title="🎯 Final Result",
            border_style="green"
        ))
        
        # Display conversation summary
        table = Table(title="📊 Conversation Summary")
        table.add_column("Step", style="cyan", width=8)
        table.add_column("Message Type", style="yellow", width=15)
        table.add_column("Content Preview", style="white")
        
        for i, msg in enumerate(result["messages"], 1):
            msg_type = type(msg).__name__
            content = str(msg.content)[:60] + "..." if len(str(msg.content)) > 60 else str(msg.content)
            table.add_row(str(i), msg_type, content)
            
        console.print(table)
        
    except Exception as e:
        logger.error(f"❌ [bold red]Workflow failed: {str(e)}[/bold red]", extra={"markup": True})
        console.print_exception()

