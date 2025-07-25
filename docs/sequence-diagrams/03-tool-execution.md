# Tool Execution Sequence

This diagram shows how tools are discovered, executed, and handled.

```mermaid
sequenceDiagram
    participant LLM as call_llm node
    participant ToolNode as enhanced_tool_node
    participant Registry as ToolRegistry
    participant SafeExec as safe_tool_execution
    participant FireRem as fire_reminder
    participant Logger as WorkflowLogger
    participant ExceptionHandler as ExceptionHandler

    Note over LLM: LLM decides to use tools
    LLM->>+ToolNode: tool_calls in response
    ToolNode->>+Logger: print_section("TOOL EXECUTION PHASE")
    Logger-->>-ToolNode: success

    loop For each tool_call
        ToolNode->>+ToolNode: extract tool_name, args, id
        ToolNode->>+Logger: print_tool_execution(tool_name, args)
        Logger-->>-ToolNode: success
        
        ToolNode->>+ToolNode: _find_tool_function(tool_name)
        ToolNode->>+Registry: search in tools list
        Registry-->>-ToolNode: tool_function or None
        
        alt Tool found
            ToolNode->>+SafeExec: safe_tool_execution(tool_name, func, args)
            SafeExec->>+FireRem: fire_reminder(**args)
            
            alt Successful execution
                FireRem->>FireRem: print firing reminder
                FireRem->>FireRem: print type and priority info
                FireRem->>FireRem: create result message
                FireRem->>FireRem: print success message
                FireRem-->>-SafeExec: result_string
                SafeExec-->>-ToolNode: (True, result)
                ToolNode->>+Logger: print_tool_result(tool_name, result, time)
                Logger-->>-ToolNode: success
            else Exception in tool
                FireRem->>+ExceptionHandler: Exception caught
                ExceptionHandler->>+Logger: print_tool_error(tool_name, error)
                Logger-->>-ExceptionHandler: success
                ExceptionHandler-->>-SafeExec: error_message
                SafeExec-->>-ToolNode: (False, error_msg)
            end
            
        else Tool not found
            ToolNode->>+Logger: print_error tool not found
            Logger-->>-ToolNode: success
        end
        
        ToolNode->>ToolNode: create ToolMessage(content, tool_call_id)
    end
    
    ToolNode->>+Logger: print_workflow_complete(message_count)
    Logger-->>-ToolNode: success
    ToolNode-->>-LLM: return tool_messages
```

## Tool Execution Steps:
1. **Discovery**: Find tool function by name
2. **Safety**: Wrap execution in error handling
3. **Logging**: Comprehensive execution logging
4. **Results**: Format and return results
5. **Errors**: Graceful error handling and reporting