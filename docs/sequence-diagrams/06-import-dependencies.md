# Module Import Dependencies

This diagram shows the import relationships between all modules.

```mermaid
graph TD
    subgraph "Entry Point"
        A[dummy_patient_reminder_memory.py]
    end
    
    subgraph "Orchestration Layer"
        B[executor/workflow_executor.py]
        C[graph/graph_builder.py]
    end
    
    subgraph "Processing Layer"
        D[nodes/workflow_nodes.py]
    end
    
    subgraph "Configuration Layer"
        E[config/tool_registry.py]
        F[prompts/prompt_templates.py]
    end
    
    subgraph "Utility Layer"
        G[utils/logging_utils.py]
        H[utils/exception_handler.py]
    end
    
    subgraph "Business Logic Layer"
        I[tools/fire_reminder.py]
        J[tools/access_patient_data.py]
        K[tools/cohort_tools.py]
        L[state.py]
    end
    
    subgraph "External Dependencies"
        M[langchain]
        N[langgraph]
        O[openai]
        P[pydantic]
    end

    %% Import flows
    A --> B
    B --> C
    B --> F
    B --> G
    B --> H
    
    C --> D
    C --> L
    C --> G
    C --> H
    
    D --> E
    D --> F
    D --> G
    D --> H
    
    E --> I
    E --> J
    E --> K
    E --> M
    E --> N
    E --> O
    
    I --> P
    J --> P
    K --> P
    
    G --> M
    H --> G
    
    %% Styling
    classDef entryPoint fill:#e8f5e8
    classDef orchestration fill:#fff2cc
    classDef processing fill:#e1f5fe
    classDef config fill:#fce4ec
    classDef utility fill:#f3e5f5
    classDef business fill:#e8eaf6
    classDef external fill:#ffcdd2
    
    class A entryPoint
    class B,C orchestration
    class D processing
    class E,F config
    class G,H utility
    class I,J,K,L business
    class M,N,O,P external
```

## Import Hierarchy:
1. **Entry Point**: Ultra-clean main module
2. **Orchestration**: High-level workflow management
3. **Processing**: Individual workflow nodes
4. **Configuration**: Tool and prompt management
5. **Utility**: Cross-cutting concerns (logging, errors)
6. **Business Logic**: Core tools and state
7. **External**: Third-party dependencies