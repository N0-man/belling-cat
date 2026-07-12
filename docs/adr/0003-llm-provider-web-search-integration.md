---
status: accepted
increment: belling-cat-mvp
related_decisions:
  - ADR-0001 (Multi-Agent Architecture)
  - ADR-0002 (Three-Tier LLM Model Strategy)
---

# LLM Provider and Web Search Integration Strategy

## Context

The Belling Cat application requires both LLM reasoning capabilities and real-time web search to investigate user claims. The Investigation/Fact Finder Agent must locate authoritative sources, retrieve current information, and provide citations for evidence. This requires deciding:

1. Which LLM provider to use (OpenAI, Anthropic, open-source models)
2. How to integrate web search capabilities (built-in, third-party API, custom implementation)
3. How tightly to couple the application to a specific provider

The multi-agent architecture (ADR-0001) and three-tier LLM strategy (ADR-0002) require a provider that supports multiple model tiers and web search integration.

## Decision

Use **OpenAI Chat Completion API** as the primary LLM provider with **built-in web search capability** (ChatGPT search feature or equivalent real-time web search integration).

- The LLM's web search is the **primary investigative mechanism**
- No external search APIs required (no separate Tavily, Perplexity, or Google Search integration)
- Real-time search results are integrated into agent reasoning and returned with source citations
- All three agents (Decomposition, Investigation, Verification) use OpenAI models per ADR-0002

## Rationale

### Provider Selection: OpenAI

- **Multi-tier model availability:** Provides GPT-4o mini (fast), GPT-4 Turbo (mid-tier), and GPT-4o (strong) as required by ADR-0002
- **Mature ecosystem:** Well-documented API, stable Python SDK, extensive community support
- **Web search integration:** Built-in capability reduces integration complexity
- **Citation quality:** Web search returns structured source citations (URL, title, publication date)
- **Cost/performance balance:** Pricing tiers align with three-tier model strategy

### Web Search Integration: Built-In

- **Reduced integration complexity:** Single API call handles both reasoning and search
- **Maintained citation quality:** LLM can directly reference search results in responses
- **No additional API keys:** Simplifies configuration and deployment
- **Unified rate limiting:** Single provider manages all quotas
- **Consistent formatting:** Search results formatted consistently with LLM responses

### Trade-offs Accepted

- **Provider coupling:** Application is tightly coupled to OpenAI's API structure and pricing
- **Search quality dependency:** Reliant on OpenAI's search implementation and source selection
- **Limited search control:** Cannot customize search parameters, ranking, or source filtering
- **Cost structure:** Bundled search+reasoning pricing (no ability to optimize search separately)

## Consequences

### Positive

- Faster MVP development (single provider integration)
- Consistent API patterns across all agents
- Simplified error handling and retry logic
- Built-in citation handling reduces parsing complexity
- Unified monitoring and cost tracking

### Negative

- **Vendor lock-in risk:** Migration to alternative provider would require significant refactoring
- **Search quality limitations:** Cannot supplement with specialized search APIs (e.g., academic databases, government sources)
- **Cost optimization constraints:** Cannot use cheaper search-only APIs for fact-finding
- **Availability coupling:** OpenAI outages affect all application functionality
- **Rate limit coupling:** High search usage affects reasoning quota and vice versa

### Mitigation Strategies

- Abstract LLM interactions behind `LLMPort` interface (already implemented in application layer)
- Use adapter pattern for OpenAI-specific implementation (already implemented as `OpenAIAdapter`)
- Document OpenAI-specific assumptions in adapter implementation
- Design system to allow future multi-provider support if needed

### Testing Impact

- Tests can mock the `LLMPort` interface without dependency on OpenAI
- Integration tests use mocked LLM responses with deterministic fixtures
- Web search results can be pre-recorded for reproducible tests
- Real OpenAI calls reserved for manual validation and smoke tests

### Configuration Requirements

- `OPENAI_API_KEY` environment variable required
- Model selection per agent role (already defined in ADR-0002):
  - Decomposition: `gpt-4o-mini`
  - Investigation: `gpt-4-turbo`
  - Verification: `gpt-4o`
- Optional: Rate limiting configuration for cost control

## Considered alternatives

### Alternative 1: Tavily Search API + Any LLM Provider

**Approach:** Use Tavily (or similar specialized search API) for web search, separate from LLM provider choice.

**Pros:**
- Decoupled search from LLM provider (could use Anthropic, open-source models, etc.)
- Specialized search quality (Tavily designed for fact-checking use cases)
- Independent cost optimization (cheaper search API)
- More search control (filters, ranking parameters)

**Cons:**
- Additional integration complexity (two APIs to manage)
- Requires separate API key and quota management
- Citation format differences between search and LLM responses
- Higher latency (sequential search → LLM calls)
- More complex error handling (two failure points)

**Why rejected for MVP:** Increased complexity not justified for initial validation. Built-in search sufficient for MVP fact-checking quality.

### Alternative 2: Perplexity API (Search-Augmented LLM)

**Approach:** Use Perplexity's search-first LLM designed for fact-finding.

**Pros:**
- Purpose-built for fact-checking and research
- Excellent citation quality
- Single API for search + reasoning
- Good source diversity

**Cons:**
- No multi-tier model strategy (single model quality level)
- Smaller ecosystem and less mature SDK
- Limited model selection (cannot optimize per agent)
- Higher cost per query (premium search integration)
- Less flexible for non-search reasoning tasks

**Why rejected:** Conflicts with ADR-0002 three-tier model strategy. Need different model strengths per agent.

### Alternative 3: Custom Web Search + LLM Synthesis

**Approach:** Implement custom web scraping/search (Google Custom Search, Bing API, or crawling) and feed results to any LLM for synthesis.

**Pros:**
- Maximum flexibility in source selection
- Could prioritize specific authoritative sources (government, academic)
- Independent optimization of search and reasoning
- Full control over citation formatting

**Cons:**
- Significant engineering complexity (web scraping, parsing, reliability)
- Requires managing multiple rate limits and quotas
- Search quality challenges (ranking, relevance, spam filtering)
- Higher maintenance burden (handling site changes, robots.txt)
- Likely slower and less reliable than specialized search APIs

**Why rejected:** Far too complex for MVP. Engineering effort better spent on core fact-checking workflow.

## Related Requirements

From PRD:
- Requirement 11: "Fact Finder Agent searches using OpenAI's GPT with real-time web search enabled"
- Requirement 12: "System captures source URL, publication date, credibility assessment, and specific evidence"
- Requirement 30: "Investigation uses LLM's web search as primary investigative mechanism"

## Future Considerations

If provider migration becomes necessary:

1. **Tavily integration:** Add Tavily adapter alongside OpenAI for specialized search
2. **Multi-provider support:** Abstract model selection to support OpenAI + Anthropic + open-source
3. **Search optimization:** Consider dedicated search API if citation quality becomes insufficient
4. **Cost optimization:** Evaluate cheaper search-only providers if OpenAI costs escalate

For now, OpenAI's built-in search provides the fastest path to validating the core fact-checking workflow.
