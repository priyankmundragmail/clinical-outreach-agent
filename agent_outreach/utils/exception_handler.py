"""
Exception Handling Utilities for Clinical Outreach Agent

This module provides centralized exception handling and error management
to keep the main workflow logic clean and focused.
"""

import traceback
import sys
from typing import Callable, Any, Dict, Optional
from functools import wraps
from .logging_utils import WorkflowLogger

class ClinicalOutreachException(Exception):
    """Base exception class for clinical outreach operations."""
    pass

class ToolExecutionError(ClinicalOutreachException):
    """Exception raised when tool execution fails."""
    def __init__(self, tool_name: str, error: Exception, tool_args: Dict = None):
        self.tool_name = tool_name
        self.original_error = error
        self.tool_args = tool_args or {}
        super().__init__(f"Tool '{tool_name}' failed: {str(error)}")

class LLMCallError(ClinicalOutreachException):
    """Exception raised when LLM call fails."""
    def __init__(self, error: Exception, message_count: int = 0):
        self.original_error = error
        self.message_count = message_count
        super().__init__(f"LLM call failed: {str(error)}")

class GraphBuildError(ClinicalOutreachException):
    """Exception raised when graph building fails."""
    def __init__(self, error: Exception):
        self.original_error = error
        super().__init__(f"Graph build failed: {str(error)}")

class WorkflowExecutionError(ClinicalOutreachException):
    """Exception raised when workflow execution fails."""
    def __init__(self, error: Exception, phase: str = "unknown"):
        self.original_error = error
        self.phase = phase
        super().__init__(f"Workflow failed in {phase} phase: {str(error)}")

class ExceptionHandler:
    """Centralized exception handling for the clinical outreach workflow."""
    
    @staticmethod
    def handle_tool_execution_error(tool_name: str, error: Exception, tool_args: Dict = None) -> str:
        """Handle tool execution errors with detailed logging."""
        WorkflowLogger.print_tool_error(tool_name, error, tool_args)
        return f"Tool '{tool_name}' failed: {str(error)}"
    
    @staticmethod
    def handle_llm_call_error(error: Exception, context: str = "") -> None:
        """Handle LLM call errors with detailed logging."""
        error_msg = f"LLM call failed: {str(error)}"
        if context:
            error_msg += f" (Context: {context})"
        
        WorkflowLogger.print_error(error_msg)
        WorkflowLogger.print_error(f"Error type: {type(error).__name__}")
        
        # Log additional context for common errors
        if "timeout" in str(error).lower():
            WorkflowLogger.print_info("This appears to be a timeout error. Consider increasing timeout settings.")
        elif "rate limit" in str(error).lower():
            WorkflowLogger.print_info("This appears to be a rate limit error. Please wait and try again.")
        elif "api key" in str(error).lower():
            WorkflowLogger.print_info("This appears to be an API key error. Check your OpenAI API key configuration.")
        
        # Log full traceback for debugging
        WorkflowLogger.print_error("Full error traceback:")
        traceback.print_exc()
        
        raise LLMCallError(error)
    
    @staticmethod
    def handle_graph_build_error(error: Exception) -> None:
        """Handle graph building errors with fallback options."""
        WorkflowLogger.print_error(f"Error building graph: {str(error)}")
        WorkflowLogger.print_error("Full error traceback:")
        traceback.print_exc()
        
        # Provide helpful suggestions based on error type
        if "import" in str(error).lower():
            WorkflowLogger.print_info("This appears to be an import error. Check that all dependencies are installed.")
        elif "memory" in str(error).lower():
            WorkflowLogger.print_info("Memory-related error detected. Will attempt to build graph without memory.")
        
        raise GraphBuildError(error)
    
    @staticmethod
    def handle_workflow_execution_error(error: Exception, phase: str = "execution") -> None:
        """Handle workflow execution errors with context."""
        WorkflowLogger.print_error(f"Workflow failed in {phase} phase: {str(error)}")
        WorkflowLogger.print_error(f"Error type: {type(error).__name__}")
        WorkflowLogger.print_error("Full error traceback:")
        traceback.print_exc()
        
        raise WorkflowExecutionError(error, phase)
    
    @staticmethod
    def handle_user_interruption() -> None:
        """Handle user interruption (Ctrl+C)."""
        WorkflowLogger.print_warning("Workflow interrupted by user")
        WorkflowLogger.print_info("Cleaning up resources...")
        sys.exit(0)
    
    @staticmethod
    def handle_import_error(error: ImportError) -> None:
        """Handle import errors with helpful suggestions."""
        WorkflowLogger.print_error(f"Import error: {str(error)}")
        
        # Provide specific suggestions based on the missing module
        error_str = str(error).lower()
        if "langchain" in error_str:
            WorkflowLogger.print_info("Install LangChain: pip install langchain langchain-openai")
        elif "langgraph" in error_str:
            WorkflowLogger.print_info("Install LangGraph: pip install langgraph")
        elif "dotenv" in error_str:
            WorkflowLogger.print_info("Install python-dotenv: pip install python-dotenv")
        elif "rich" in error_str:
            WorkflowLogger.print_info("Install Rich: pip install rich")
        else:
            WorkflowLogger.print_info("Make sure all dependencies are installed: pip install -r requirements.txt")
        
        sys.exit(1)
    
    @staticmethod
    def handle_general_exception(error: Exception, context: str = "") -> None:
        """Handle general exceptions with context."""
        error_msg = f"Unexpected error occurred: {str(error)}"
        if context:
            error_msg += f" (Context: {context})"
        
        WorkflowLogger.print_error(error_msg)
        WorkflowLogger.print_error(f"Error type: {type(error).__name__}")
        WorkflowLogger.print_error("Full error traceback:")
        traceback.print_exc()
        
        sys.exit(1)

def safe_execute(operation_name: str = "operation"):
    """Decorator for safe execution of functions with exception handling."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except ToolExecutionError as e:
                WorkflowLogger.print_error(f"{operation_name} failed: {str(e)}")
                raise
            except LLMCallError as e:
                WorkflowLogger.print_error(f"{operation_name} failed: {str(e)}")
                raise
            except Exception as e:
                ExceptionHandler.handle_general_exception(e, operation_name)
        return wrapper
    return decorator

def safe_tool_execution(tool_name: str, tool_func: Callable, tool_args: Dict) -> tuple[bool, Any]:
    """Safely execute a tool and return success status and result."""
    try:
        if tool_args:
            result = tool_func(**tool_args)
        else:
            result = tool_func()
        return True, result
    except Exception as e:
        error_msg = ExceptionHandler.handle_tool_execution_error(tool_name, e, tool_args)
        return False, error_msg

class ErrorHandlingContext:
    """Context manager for workflow execution with proper exception handling."""
    
    def __init__(self, workflow_name: str):
        self.workflow_name = workflow_name
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        WorkflowLogger.print_info(f"Starting {self.workflow_name}...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            import time
            duration = time.time() - self.start_time
            WorkflowLogger.print_success(f"{self.workflow_name} completed successfully in {duration:.2f}s")
        elif exc_type == KeyboardInterrupt:
            ExceptionHandler.handle_user_interruption()
        elif exc_type == ImportError:
            ExceptionHandler.handle_import_error(exc_val)
        elif issubclass(exc_type, ClinicalOutreachException):
            # Already handled by specific exception handlers
            return False
        else:
            ExceptionHandler.handle_general_exception(exc_val, self.workflow_name)
        
        return False  # Don't suppress exceptions

class ErrorHandlingContext:
    """Context manager for error handling and exception management during workflow execution."""
    
    def __init__(self, operation_name: str):
        # Track operation name and timing for error context
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        # Start timing and log operation begin
        import time
        self.start_time = time.time()
        WorkflowLogger.print_info(f"Starting {self.operation_name}...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Handle completion or exceptions with proper error management
        if exc_type is None:
            import time
            duration = time.time() - self.start_time
            WorkflowLogger.print_success(f"{self.operation_name} completed successfully in {duration:.2f}s")
        elif exc_type == KeyboardInterrupt:
            ExceptionHandler.handle_user_interruption()
        elif exc_type == ImportError:
            ExceptionHandler.handle_import_error(exc_val)
        elif issubclass(exc_type, ClinicalOutreachException):
            # Already handled by specific exception handlers
            return False
        else:
            ExceptionHandler.handle_general_exception(exc_val, self.operation_name)
        
        return False  # Don't suppress exceptions