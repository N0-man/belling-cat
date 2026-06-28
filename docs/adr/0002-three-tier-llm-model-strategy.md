# Three-Tier LLM Model Strategy

Each agent uses a different LLM model optimized for its phase: fast model for decomposition (GPT-4o mini), mid-tier for fact-finding (GPT-4 Turbo), and strong reasoning model for verification (GPT-4o). This balances cost, latency, and reasoning capability across the investigation workflow. Decomposition is deterministic and benefits from speed; fact-finding requires moderate reasoning and web search integration; verification demands nuanced credibility assessment. Using the strongest model everywhere would increase cost 3-5x and latency by ~40% with minimal quality improvement for simple decomposition tasks. Using the weakest model everywhere would compromise verification accuracy.

## Considered Options

- **Single model for all agents** - Simpler but either too slow/expensive or insufficiently accurate
- **Two-tier (fast + strong)** - Middle ground but doesn't optimize fact-finding cost/latency balance
- **Three-tier** - Chosen for optimal cost/latency/quality across distinct reasoning requirements

## Consequences

- Configuration must specify model per agent role
- Cost monitoring needs per-agent attribution for optimization
- Future model updates must be evaluated per role, not globally
- Testing fixtures need to account for different model capabilities per agent
