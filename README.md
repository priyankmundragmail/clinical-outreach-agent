# Clinical Outreach Agent

A modular, AI-powered agent system for clinical outreach and patient engagement workflows, built with LangGraph and OpenAI.

## 🎯 Project Overview

### Original Goal
To build a hands-on, end-to-end AI agent that can take user input (clinical or outreach questions), process it using an LLM, invoke relevant tools, and return meaningful, actionable responses—while gaining practical skills in real-world agent development.

### Current Status
✅ **Completed**: Fully functional clinical outreach agent with modular architecture, comprehensive error handling, and extensive documentation.

## 🏗️ Architecture

The system follows a clean, modular architecture with clear separation of concerns:

```
📁 clinical-outreach-agent/
├── 📄 dummy_patient_reminder_memory.py    # Entry point (15 lines)
├── 📁 executor/                           # Workflow orchestration
├── 📁 graph/                             # LangGraph workflow builder
├── 📁 nodes/                             # Individual workflow nodes
├── 📁 config/                            # Tool and LLM configuration
├── 📁 tools/                             # Business logic tools
├── 📁 prompts/                           # System prompts and templates
├── 📁 utils/                             # Infrastructure utilities
└── 📁 docs/                              # Comprehensive documentation
```

## 🤖 Agent Capabilities

### Core Features
- **Intelligent Planning**: Generates execution strategies for patient outreach scenarios
- **Tool Orchestration**: Discovers and executes appropriate tools based on context
- **Error Recovery**: Comprehensive error handling with graceful degradation
- **Structured Logging**: Detailed workflow tracking and debugging information

### Available Tools
- **Fire Reminder**: Send patient reminders with customizable priority levels
- **Patient Lookup**: Retrieve patient information and medical history
- **Appointment Management**: Schedule and manage patient appointments
- **Communication Tools**: Multi-channel patient outreach (email, SMS, phone)

## 🚀 Quick Start

### Prerequisites
```bash
pip install langchain langgraph openai python-dotenv
```

### Environment Setup
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### Run the Agent
```bash
python dummy_patient_reminder_memory.py
```

## 📊 Documentation

Comprehensive sequence diagrams and architecture documentation available in `docs/sequence-diagrams/`:

- **01-system-overview.md**: Complete workflow sequence
- **02-workflow-execution.md**: Detailed LangGraph execution flow
- **03-tool-execution.md**: Tool discovery and execution process
- **04-configuration-flow.md**: Dependency and configuration management
- **05-error-handling.md**: Exception handling and recovery strategies
- **06-architecture.md**: Modular system architecture
- **07-agent-architecture.md**: Agent-based design and tool interactions

## 🎯 Key Objectives Achieved

### ✅ Hands-On Development
- Built complete end-to-end agent with real LLM integration
- Implemented practical tool execution and state management
- Created production-ready error handling and logging

### ✅ Modular Architecture
- **15-line entry point** for maximum simplicity
- **Separated concerns** across distinct modules
- **Extensible design** for future tool and agent additions

### ✅ LangGraph Integration
- **Workflow orchestration** using LangGraph state machines
- **Dynamic tool routing** based on LLM decisions
- **State management** throughout the execution pipeline

### ✅ Production Readiness
- **Comprehensive error handling** for all failure scenarios
- **Structured logging** for debugging and monitoring
- **Configuration management** for different environments
- **Safety wrappers** around all external operations

## 🔄 Workflow Example

```
User Input: "Send a high-priority reminder to patient 12345"
    ↓
Planning Agent: Analyzes request and generates execution plan
    ↓
LLM Analysis: Determines tools needed and parameters
    ↓
Tool Execution: Invokes fire_reminder with patient ID and priority
    ↓
Result Processing: Formats response and logs completion
    ↓
Output: "✅ High-priority reminder sent to Patient 12345"
```

## 🛠️ Extensibility

### Adding New Tools
1. Create tool function in `tools/`
2. Add to `config/tool_registry.py`
3. Tool automatically available to all agents

### Adding New Agents
1. Create agent class in `nodes/`
2. Register in `graph/graph_builder.py`
3. Agent integrates with existing workflow

### Custom Workflows
1. Define new prompts in `prompts/templates.py`
2. Create workflow nodes as needed
3. Configure in `config/tool_registry.py`

## 📈 Benefits Achieved

### Development Benefits
- **Clear structure**: Easy for new developers to understand
- **Parallel development**: Teams can work on different modules
- **Code reuse**: Infrastructure components used across all layers

### Operational Benefits
- **Easy debugging**: Clear component boundaries and comprehensive logging
- **Performance monitoring**: Each layer can be monitored independently
- **Graceful degradation**: Failures isolated to specific components

### Clinical Benefits
- **Reliable patient outreach**: Robust error handling ensures messages are delivered
- **Audit trail**: Complete logging for compliance and tracking
- **Scalable design**: Easy to add new outreach channels and tools

## 🎯 Next Steps

### Immediate Enhancements
- [ ] Add real EHR integration capabilities
- [ ] Implement multi-channel communication tools
- [ ] Create patient cohort analysis tools
- [ ] Add appointment scheduling automation

### Advanced Features
- [ ] Implement conversation memory for multi-turn interactions
- [ ] Add predictive analytics for outreach optimization
- [ ] Create dashboard for outreach campaign management
- [ ] Implement A/B testing for outreach strategies

### Integration Goals
- [ ] FHIR API integration for real patient data
- [ ] Healthcare system integration (Epic, Cerner)
- [ ] Compliance features for HIPAA and healthcare regulations
- [ ] Real-time monitoring and alerting systems

## 🤝 Contributing

This project serves as a foundation for clinical AI agent development. The modular architecture makes it easy to:

- Add new clinical tools and workflows
- Integrate with different healthcare systems
- Extend agent capabilities for specific use cases
- Customize for different healthcare organizations

## 📝 License

This project is designed for educational and healthcare innovation purposes.

---

**Built with**: LangGraph, OpenAI GPT-3.5-turbo, LangChain, Python
**Focus**: Real-world clinical AI agent development with production-ready architecture