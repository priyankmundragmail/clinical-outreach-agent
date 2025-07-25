# Error Handling and Exception Flow

This diagram shows how errors are caught, handled, and reported throughout the system.

```mermaid
sequenceDiagram
    participant Component as Any Component
    participant SafeDecorator as @safe_execute
    participant ExceptionHandler as ExceptionHandler
    participant Logger as WorkflowLogger
    participant User as User/Console

    Note over Component: Normal Execution
    Component->>+SafeDecorator: function_call()
    SafeDecorator->>+Component: execute_function()
    
    alt Successful Execution
        Component-->>-SafeDecorator: result
        SafeDecorator-->>-Component: result
    else Exception Occurs
        Component->>+ExceptionHandler: Exception caught
        
        alt LLM Error
            ExceptionHandler->>+Logger: handle_llm_call_error()
            Logger->>+User: print_error("LLM call failed")
            Logger->>+User: print_error("Error type details")
            Logger->>+User: print_error("Full traceback")
            User-->>-Logger: error_displayed
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler-->>-SafeDecorator: LLMCallError raised
        else Tool Error
            ExceptionHandler->>+Logger: handle_tool_execution_error()
            Logger->>+User: print_tool_error(tool_name, error, args)
            Logger->>+User: print("Tool failed message")
            Logger->>+User: print("Error type details")
            Logger->>+User: print("Full traceback")
            User-->>-Logger: error_displayed
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler-->>-SafeDecorator: error_message_string
        else Graph Build Error
            ExceptionHandler->>+Logger: handle_graph_build_error()
            Logger->>+User: print_error("Graph build failed")
            Logger->>+User: print_info("Attempting fallback")
            User-->>-Logger: error_displayed
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler-->>-SafeDecorator: GraphBuildError raised
        else Import Error
            ExceptionHandler->>+Logger: handle_import_error()
            Logger->>+User: print_error("Import error message")
            Logger->>+User: print_info("Install suggestion")
            User-->>-Logger: error_displayed
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler->>+Component: sys.exit(1)
        else General Error
            ExceptionHandler->>+Logger: handle_general_exception()
            Logger->>+User: print_error("Unexpected error")
            Logger->>+User: print_error("Full traceback")
            User-->>-Logger: error_displayed
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler->>+Component: sys.exit(1)
        end
        
        SafeDecorator-->>-Component: error_or_exception
    end

    Note over Component,User: Graceful Degradation
    alt Recoverable Error
        Component->>+Component: continue_with_fallback()
    else Non-Recoverable Error
        Component->>+User: Clean shutdown with error message
    end
```

## Error Handling Features:
- **Centralized**: All error handling in ExceptionHandler
- **Contextual**: Specific handlers for different error types
- **Informative**: Detailed error messages with suggestions
- **Graceful**: Fallback options where possible
- **User-Friendly**: Clear error reporting to console