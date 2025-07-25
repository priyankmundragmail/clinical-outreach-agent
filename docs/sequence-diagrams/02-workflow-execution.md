# Detailed Workflow Execution Sequence

This diagram shows the detailed flow through the LangGraph workflow nodes.

```mermaid
sequenceDiagram
    participant Executor as WorkflowExecutor
    participant Graph as LangGraph
    participant Planning as planning_node
    participant LLM as call_llm
    participant Tools as enhanced_tool_node
    participant ToolRegistry as ToolRegistry
    participant FireReminder as fire_reminder.py
    participant Logger as WorkflowLogger

    Note over Executor: Workflow Starts
    Executor->>+Graph: app.invoke(messages)
    
    Note over Graph: Planning Phase
    Graph->>+Planning: planning_node(state)
    Planning->>+Logger: print_info("Generating plan...")
    Logger-->>-Planning: success
    Planning->>+ToolRegistry: llm.invoke(planning_messages)
    ToolRegistry-->>-Planning: execution_plan
    Planning->>+Logger: print_section("EXECUTION PLAN")
    Logger-->>-Planning: success
    Planning-->>-Graph: {"messages": [plan_message]}
    
    Note over Graph: LLM Analysis Phase
    Graph->>+LLM: call_llm(state)
    LLM->>+Logger: print_info("Calling LLM...")
    Logger-->>-LLM: success
    LLM->>+ToolRegistry: llm_with_tools.invoke(enhanced_messages)
    ToolRegistry-->>-LLM: response_with_tool_calls
    LLM->>+Logger: print_llm_reasoning(response.content)
    Logger-->>-LLM: success
    LLM->>+Logger: print_tool_calls(tool_calls)
    Logger-->>-LLM: success
    LLM-->>-Graph: {"messages": [llm_response]}
    
    Note over Graph: Tool Execution Phase
    Graph->>+Tools: enhanced_tool_node(state)
    Tools->>+Logger: print_section("TOOL EXECUTION PHASE")
    Logger-->>-Tools: success
    
    loop For each tool_call
        Tools->>+Logger: print_tool_execution(tool_name, args)
        Logger-->>-Tools: success
        Tools->>+FireReminder: fire_reminder(patient_id, type, priority)
        FireReminder->>FireReminder: print("Firing reminder...")
        FireReminder-->>-Tools: "Reminder sent to Patient X"
        Tools->>+Logger: print_tool_result(result, time)
        Logger-->>-Tools: success
    end
    
    Tools-->>-Graph: {"messages": [tool_results]}
    
    Note over Graph: Final LLM Processing
    Graph->>+LLM: call_llm(state)
    LLM->>+ToolRegistry: llm_with_tools.invoke(messages_with_results)
    ToolRegistry-->>-LLM: final_response
    LLM->>+Logger: print_llm_reasoning(final_response)
    Logger-->>-LLM: success
    LLM-->>-Graph: {"messages": [final_message]}
    
    Graph-->>-Executor: workflow_result
```

## Workflow Phases:
1. **Planning**: Generate execution strategy
2. **LLM Analysis**: Analyze data and determine actions
3. **Tool Execution**: Execute fire_reminder and other tools
4. **Final Processing**: Generate summary and results