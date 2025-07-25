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
        SafeDecorator-->>Component: result
    else Exception Occurs
        Component->>+ExceptionHandler: Exception caught
        
        alt LLM Error
            ExceptionHandler->>+Logger: handle_llm_call_error()
            Logger->>User: print_error("LLM call failed")
            Logger->>User: print_error("Error type details")
            Logger->>User: print_error("Full traceback")
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler-->>SafeDecorator: LLMCallError raised
        else Tool Error
            ExceptionHandler->>+Logger: handle_tool_execution_error()
            Logger->>User: print_tool_error(tool_name, error, args)
            Logger->>User: print("Tool failed message")
            Logger->>User: print("Error type details")
            Logger->>User: print("Full traceback")
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler-->>SafeDecorator: error_message_string
        else Graph Build Error
            ExceptionHandler->>+Logger: handle_graph_build_error()
            Logger->>User: print_error("Graph build failed")
            Logger->>User: print_info("Attempting fallback")
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler-->>SafeDecorator: GraphBuildError raised
        else Import Error
            ExceptionHandler->>+Logger: handle_import_error()
            Logger->>User: print_error("Import error message")
            Logger->>User: print_info("Install suggestion")
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler-->>Component: sys.exit(1)
        else General Error
            ExceptionHandler->>+Logger: handle_general_exception()
            Logger->>User: print_error("Unexpected error")
            Logger->>User: print_error("Full traceback")
            Logger-->>-ExceptionHandler: logged
            ExceptionHandler-->>Component: sys.exit(1)
        end
        
        ExceptionHandler-->>-Component: handled
        SafeDecorator-->>-Component: error_or_exception
    end

    Note over Component,User: Graceful Degradation
    alt Recoverable Error
        Component->>Component: continue_with_fallback()
    else Non-Recoverable Error
        Component->>User: Clean shutdown with error message
    end
```

## Error Handling Strategy

### Exception Types and Responses

#### 1. LLM Errors
- **Cause**: OpenAI API failures, rate limits, network issues
- **Response**: Detailed error logging with retry suggestions
- **Action**: Raise LLMCallError for caller to handle

#### 2. Tool Execution Errors
- **Cause**: Tool function failures, invalid arguments
- **Response**: Log tool name, arguments, and error details
- **Action**: Return error message string to continue workflow

#### 3. Graph Build Errors
- **Cause**: LangGraph construction failures, node configuration issues
- **Response**: Log error and attempt fallback configuration
- **Action**: Raise GraphBuildError if no fallback available

#### 4. Import Errors
- **Cause**: Missing dependencies, module import failures
- **Response**: Clear error message with installation instructions
- **Action**: Clean system exit with error code

#### 5. General Exceptions
- **Cause**: Unexpected errors, programming bugs
- **Response**: Full traceback logging for debugging
- **Action**: Clean system exit to prevent corruption

## Error Handling Features

### Centralized Management
- All error handling logic in ExceptionHandler
- Consistent error formatting across the system
- Single place to modify error handling behavior

### Contextual Responses
- Different handlers for different error types
- Appropriate recovery strategies for each scenario
- Clear distinction between recoverable and fatal errors

### User Experience
- Clear, actionable error messages
- Installation suggestions for missing dependencies
- Graceful degradation where possible

### Development Support
- Full traceback logging for debugging
- Detailed error context and suggestions
- Easy to add new error types and handlers

## Recovery Strategies

### Recoverable Errors
- Tool execution failures: Continue with error message
- LLM temporary failures: Retry or fallback
- Graph build issues: Attempt simplified configuration

### Non-Recoverable Errors
- Missing critical dependencies: Clean exit with instructions
- Fatal configuration errors: Immediate shutdown
- Unexpected system errors: Safe termination with logs