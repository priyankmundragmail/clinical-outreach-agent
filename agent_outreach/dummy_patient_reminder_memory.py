"""
Clinical Outreach Agent Main Module

Main entry point for the clinical patient outreach automation system.
This module orchestrates the complete workflow using modularized components.
"""

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_outreach.executor.workflow_executor import WorkflowExecutor

def main():
    """Main entry point for the clinical outreach agent."""
    executor = WorkflowExecutor()
    return executor.run()

if __name__ == "__main__":
    main()
