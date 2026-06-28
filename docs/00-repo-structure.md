# Repository Structure

Belling Cat follows Clean Architecture with explicit layer separation. Inner layers must not import from outer layers.

## Layer Structure

```
belling_cat/
├── domain/           # Core business logic (innermost layer)
│   ├── claim.py      # Claim aggregate root
│   ├── investigation.py  # Investigation aggregate root
│   └── value_objects.py  # SubClaim, Evidence, Source, Verdict, Finding
│
├── application/      # Use case orchestration
│   ├── ports/        # Interfaces for external dependencies
│   │   ├── llm.py    # LLM adapter interface
│   │   ├── repository.py  # Investigation persistence interface
│   │   └── report_writer.py  # Report generation interface
│   │
│   └── services/     # Application services (orchestration)
│       ├── decomposition_service.py    # Orchestrates claim decomposition
│       ├── fact_finder_service.py      # Orchestrates evidence gathering
│       └── verifier_service.py         # Orchestrates verdict generation
│
├── infrastructure/   # External integrations (outermost layer)
│   ├── llm/          # LLM provider adapters
│   │   └── openai_adapter.py  # OpenAI API implementation
│   │
│   ├── persistence/  # Storage implementations
│   │   ├── session_repository.py  # Investigation state persistence
│   │   └── report_writer.py       # Markdown file generation
│   │
│   └── langgraph/    # LangGraph workflow orchestration
│       └── workflow.py  # LangGraph graph definition
│
└── cli.py            # Entry point & terminal UI (adapter layer)
```

## Building Block Placement

| Building Block | Layer | Examples |
|---|---|---|
| **Aggregate Root** | Domain | Claim, Investigation |
| **Value Object** | Domain | SubClaim, Evidence, Source, Verdict, Finding |
| **Domain Service** | Domain | _(none identified yet)_ |
| **Port** | Application | LLMPort, RepositoryPort, ReportWriterPort |
| **Application Service** | Application | DecompositionService, FactFinderService, VerifierService |
| **Repository** | Infrastructure | SessionRepository _(implements RepositoryPort)_ |
| **Adapter** | Infrastructure | OpenAIAdapter _(implements LLMPort)_ |

## Dependency Rule

- **Domain** has zero external dependencies (pure Python)
- **Application** may import from Domain, defines Ports for external dependencies
- **Infrastructure** may import from Domain and Application, implements Ports
- **CLI** may import from all layers, wires dependencies at startup

## Module Guidelines

- Domain objects are immutable where possible (especially Value Objects)
- Application services are stateless and orchestrate domain objects
- Infrastructure adapters translate between external APIs and domain/application interfaces
- All business rules live in the Domain layer; Application services only coordinate
