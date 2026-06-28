# Multi-Agent Architecture with LangGraph

We're using LangGraph to orchestrate three specialized agents (Claim Decomposition, Investigation/Fact Finder, Verifier) rather than a simple sequential LLM call chain. This adds architectural complexity but enables parallel processing of independent sub-claims during fact-finding, reducing total investigation latency. LangGraph provides workflow state management and error recovery that would otherwise need to be built manually. The trade-off is increased dependency surface and learning curve, but the parallelism and built-in state management justify the complexity for a multi-step investigation workflow.

## Considered Options

- **Sequential LLM calls** - Simpler but slower, no built-in state management
- **Custom workflow orchestrator** - Full control but reinvents state management and recovery
- **LangGraph** - Chosen for parallel execution support and built-in workflow primitives

## Consequences

- Agent execution order is managed by LangGraph's graph execution model
- Session persistence must serialize LangGraph workflow state
- Testing requires understanding LangGraph's execution model for proper mocking
- Future enhancements (e.g., conditional branching, retries) can leverage LangGraph's features
