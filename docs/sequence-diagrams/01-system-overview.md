# System Overview - Complete Workflow Sequence

This diagram shows the high-level flow through all modules in the clinical outreach system.

```mermaid
sequenceDiagram
    participant Main as dummy_patient_reminder_memory.py
    participant Executor as WorkflowExecutor
    participant GraphBuilder as GraphBuilder
    participant Nodes as WorkflowNodes
    participant ToolRegistry as ToolRegistry
    participant Prompts as PromptTemplates
    participant Logger as WorkflowLogger
    participant ExceptionHandler as ExceptionHandler

    Note over Main: Entry Point
    Main->>+Executor: main() → WorkflowExecutor()
    Main->>+Executor: executor.run()

    Note over Executor: Initialization Phase
    Executor->>+Logger: print_header("Clinical Outreach Agent v2.0")
    Logger-->>-Executor: ✅ Header displayed
    
    Executor->>+Executor: initialize()
    Executor->>+GraphBuilder: GraphBuilder()
    GraphBuilder->>+Nodes: WorkflowNodes()
    Nodes->>+ToolRegistry: get_llm(), get_tools(), get_llm_with_tools()
    ToolRegistry-->>-Nodes: llm, tools, llm_with_tools
    Nodes-->>-GraphBuilder: configured nodes
    GraphBuilder-->>-Executor: graph_builder instance
    
    Executor->>+GraphBuilder: create_graph()
    GraphBuilder->>+Logger: print_info("Building Graph...")
    Logger-->>-GraphBuilder: ✅
    GraphBuilder-->>-Executor: compiled_graph
    
    Note over Executor: Execution Phase
    Executor->>+Executor: execute_workflow()
    Executor->>+Prompts: SYSTEM_PROMPT, WORKFLOW_START_PROMPT
    Prompts-->>-Executor: prompt_messages
    
    Executor->>+Executor: app.invoke(messages)
    Note over Executor: LangGraph execution begins
    
    Note over Executor: Results Analysis
    Executor->>+Executor: analyze_results(result)
    Executor->>+Logger: print_section("WORKFLOW COMPLETED")
    Logger-->>-Executor: ✅
    
    Executor-->>-Main: workflow_result
    
    Note over Main,ExceptionHandler: Error Handling (if needed)
    alt Exception occurs
        Executor->>+ExceptionHandler: handle_*_error()
        ExceptionHandler->>+Logger: print_error()
        Logger-->>-ExceptionHandler: ✅
        ExceptionHandler-->>-Executor: error_handled
    end
```

## Key Components:
- **Main Module**: Ultra-clean entry point (15 lines)
- **WorkflowExecutor**: Orchestrates the entire workflow
- **GraphBuilder**: Constructs the LangGraph workflow
- **WorkflowNodes**: Individual processing nodes
- **ToolRegistry**: Centralized tool and LLM configuration
- **PromptTemplates**: All prompts and templates
- **WorkflowLogger**: All output formatting
- **ExceptionHandler**: Centralized error management