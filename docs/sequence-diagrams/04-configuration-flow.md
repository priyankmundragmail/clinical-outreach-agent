# Configuration and Dependency Flow

This diagram shows how configuration and dependencies are loaded and used.

```mermaid
sequenceDiagram
    participant Main as dummy_patient_reminder_memory.py
    participant Executor as WorkflowExecutor
    participant GraphBuilder as GraphBuilder
    participant Nodes as WorkflowNodes
    participant Registry as ToolRegistry
    participant Tools as Individual Tools
    participant OpenAI as ChatOpenAI
    participant LangChain as LangChain Tools

    Note over Main: Application Startup
    Main->>+Executor: WorkflowExecutor()
    Executor->>+GraphBuilder: GraphBuilder()
    GraphBuilder->>+Nodes: WorkflowNodes()
    
    Note over Nodes: Node Initialization
    Nodes->>+Registry: get_llm()
    Registry->>+OpenAI: ChatOpenAI(model="gpt-3.5-turbo", timeout=30, max_retries=2)
    OpenAI-->>-Registry: configured_llm
    Registry-->>-Nodes: llm_instance
    
    Nodes->>+Registry: get_tools()
    Registry->>+Tools: Import all tool functions
    Tools-->>-Registry: function_references
    Registry->>+LangChain: StructuredTool.from_function(func, name, description, schema)
    LangChain-->>-Registry: structured_tools_list
    Registry-->>-Nodes: tools_list
    
    Nodes->>+Registry: get_llm_with_tools()
    Registry->>+Registry: llm.bind_tools(tools)
    Registry-->>-Nodes: llm_with_tools
    
    Note over Nodes: Configuration Complete
    Nodes-->>-GraphBuilder: configured_nodes
    GraphBuilder-->>-Executor: graph_builder
    Executor-->>-Main: executor_ready

    Note over Main: Runtime Tool Access
    Main->>+Executor: executor.run()
    Note over Executor: During workflow execution...
    Executor->>+Nodes: Any node execution
    Nodes->>+Registry: Access pre-configured llm/tools
    Registry-->>-Nodes: cached_instances
    Nodes-->>-Executor: execution_result
```

## Configuration Benefits:
- **Centralized**: All tool and LLM config in ToolRegistry
- **Lazy Loading**: Configuration loaded once at startup
- **Cached**: Instances reused across workflow
- **Modular**: Easy to swap configurations
- **Testable**: Easy to mock for testing