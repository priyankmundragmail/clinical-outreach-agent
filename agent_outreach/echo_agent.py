from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
import os

# Define a simple tool that just echoes the input
def echo_tool(input_text: str) -> str:
    return f"You said: {input_text}"

tools = [echo_tool]
tool_executor = ToolExecutor(tools)

# Set up the language model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define a simple function to call the LLM and convert output to ToolInvocation
def call_llm(state):
    input_msg = state["messages"][-1].content
    return {
        "messages": state["messages"] + [
            ToolInvocation(tool="echo_tool", tool_input=input_msg)
        ]
    }

# Define a function to call the tool and return its response
def call_tool(state):
    tool_input = state["messages"][-1].tool_input
    tool_response = echo_tool(tool_input)
    return {
        "messages": state["messages"] + [ToolMessage(content=tool_response, tool_call_id="1")]
    }

# Define state structure
class GraphState(dict):
    pass

# Create the LangGraph
graph = StateGraph(GraphState)
graph.add_node("llm", call_llm)
graph.add_node("tool", call_tool)
graph.set_entry_point("llm")
graph.add_edge("llm", "tool")
graph.add_edge("tool", END)

# Compile the graph with in-memory checkpointing
app = graph.compile(checkpointer=MemorySaver())

# Run the agent
if __name__ == "__main__":
    config = RunnableConfig()
    result = app.invoke({"messages": [HumanMessage(content="Hello, world!")]} , config)
    print("Final Output:", result["messages"][-1].content)