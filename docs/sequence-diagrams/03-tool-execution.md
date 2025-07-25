# Tool Execution Sequence

This diagram shows how tools are discovered, executed, and handled.

```mermaid
sequenceDiagram
    participant LLM as call_llm_node
    participant ToolNode as enhanced_tool_node
    participant Registry as ToolRegistry
    participant SafeExec as safe_tool_execution
    participant FireRem as fire_reminder
    participant Logger as WorkflowLogger
    participant ExceptionHandler as ExceptionHandler

    Note over LLM: LLM decides to use tools
    LLM->>ToolNode: tool_calls in response
    ToolNode->>Logger: print_section("TOOL EXECUTION PHASE")
    
    loop For each tool_call
        ToolNode->>ToolNode: extract tool_name, args, id
        ToolNode->>Logger: print_tool_execution(tool_name, args)
        
        ToolNode->>ToolNode: _find_tool_function(tool_name)
        ToolNode->>Registry: search in tools list
        Registry-->>ToolNode: tool_function or None
        
        alt Tool found
            ToolNode->>SafeExec: safe_tool_execution(tool_name, func, args)
            SafeExec->>FireRem: fire_reminder(**args)
            
            alt Successful execution
                FireRem->>FireRem: print("Firing reminder...")
                FireRem->>FireRem: print type and priority info
                FireRem->>FireRem: create result message
                FireRem->>FireRem: print success message
                FireRem-->>SafeExec: result_string
                SafeExec-->>ToolNode: (True, result)
                ToolNode->>Logger: print_tool_result(tool_name, result, time)
            else Exception in tool
                FireRem->>ExceptionHandler: Exception caught
                ExceptionHandler->>Logger: print_tool_error(tool_name, error)
                ExceptionHandler-->>SafeExec: error_message
                SafeExec-->>ToolNode: (False, error_msg)
            end
            
        else Tool not found
            ToolNode->>Logger: print_error("Tool not found")
        end
        
        ToolNode->>ToolNode: create ToolMessage(content, tool_call_id)
    end
    
    ToolNode->>Logger: print_workflow_complete(message_count)
    ToolNode-->>LLM: return tool_messages
```

## Tool Execution Process

The tool execution follows these key steps:

### 1. Tool Discovery
- LLM sends tool calls to the enhanced tool node
- Each tool call contains name, arguments, and call ID
- Tool node logs the start of execution phase

### 2. Function Resolution
- Tool node searches the registry for the requested function
- Uses `_find_tool_function()` to locate the tool
- Registry returns the function or None if not found

### 3. Safe Execution
- Found tools are executed through the safety wrapper
- `safe_tool_execution()` wraps all tool calls
- All exceptions are caught and handled gracefully

### 4. Tool Implementation
- `fire_reminder()` is called with patient data
- Prints firing status and reminder details
- Returns formatted result string or error

### 5. Result Processing
- Successful results are formatted and logged with timing
- Error messages are created for failed executions
- All results are converted to ToolMessage objects with call IDs

### 6. Response Generation
- All tool messages are returned to the LLM
- LLM can then continue with the workflow using the results
- Complete workflow status is logged

## Error Handling

The system includes comprehensive error handling:

### Tool Not Found
- Unknown tools result in clear error messages
- Execution continues with other tools

### Execution Errors
- Exceptions during execution are caught by ExceptionHandler
- Full error details are logged with context
- Error messages include suggestions where possible

### Safety Features
- All tool execution is wrapped in try-catch blocks
- No tool failure stops the entire workflow
- Graceful degradation ensures system stability