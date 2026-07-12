# PRD: Belling Cat - Fact-Checking Terminal Interface (MVP)

## Problem Statement

Users need a way to fact-check news stories, events, or claims using open intelligence investigative techniques. Traditional fact-checking requires manual research across multiple sources, which is time-consuming and prone to bias. There's no readily available terminal-based tool that combines LLM reasoning with real-time fact-finding to investigate claims systematically.

## Solution

A terminal-based fact-checking application called "Belling Cat" that accepts user queries in the form of `/investigate <claim>` commands. The system uses a multi-agent LLM architecture to decompose claims, investigate each sub-claim using web search, verify information against authoritative sources, and present findings step-by-step to the user. The final output includes a verdict (supported/contradicted/unsupported) and a saveable Markdown report.

## Scope

### User Interaction & Entry Point
1. GIVEN the user starts the Belling Cat terminal app, WHEN the app initializes, THEN it should display an ASCII art banner with "Belling Cat" text
2. GIVEN the app is running and idle, WHEN the user types, THEN they should see a text input box prompting for commands
3. GIVEN the user enters `/investigate elephant was seen flying near Changi Airport yesterday`, WHEN they press Enter, THEN the system should accept the claim and begin investigation

### Claim Decomposition
4. GIVEN a user claim is submitted, WHEN the Claim Decomposition Agent processes it, THEN it should break the claim into discrete sub-claims (e.g., "elephant", "flying", "Changi Airport", "yesterday") and return them as structured JSON
5. GIVEN a complex multi-faceted claim, WHEN decomposed, THEN each sub-claim should be independently verifiable
6. GIVEN a simple single-fact claim, WHEN decomposed, THEN the system should recognize it and treat it as a single sub-claim

### Investigation & Real-Time Findings
7. GIVEN the claims have been decomposed, WHEN the Investigation Agent begins searching, THEN the user should see real-time intermediate findings (e.g., "Searching for elephant sightings...", "Found 3 relevant news articles...", "Analyzing source credibility...")
8. GIVEN an investigation is in progress, WHEN new findings are discovered, THEN they should be streamed to the terminal immediately without buffering
9. GIVEN an investigation is searching multiple sub-claims, WHEN searching proceeds in parallel where possible, THEN the user should see multiple findings streaming concurrently
10. GIVEN the system is searching, WHEN it finds sources, THEN it should identify the source authority level (government database, news outlet, academic, social media, etc.)

### Fact-Finding & Evidence Gathering
11. GIVEN a sub-claim requires verification, WHEN the Fact Finder Agent searches, THEN it should use OpenAI's GPT (with real-time web search enabled) to locate authoritative sources
12. GIVEN multiple sources are found for a sub-claim, WHEN they are gathered, THEN the system should capture the source URL, publication date, credibility assessment, and the specific evidence
13. GIVEN a source contradicts another, WHEN facts are compiled, THEN both sources should be recorded with their contradictions noted

### Verification & Credibility Assessment
14. GIVEN evidence has been gathered, WHEN the Verifier Agent evaluates it, THEN it should assess source credibility using a hierarchy (government > academic > established news > other)
15. GIVEN conflicting evidence exists, WHEN the Verifier Agent processes it, THEN it should flag the contradiction and explain why one source may be more credible
16. GIVEN evidence lacks authoritative sources, WHEN the Verifier evaluates it, THEN it should mark the claim as "unsupported" rather than "false"

### Summary & Verdict
17. GIVEN all agents have completed their analysis, WHEN a summary is generated, THEN the system should present findings in order: step-by-step investigation log, then a clear verdict section
18. GIVEN a verdict is ready, WHEN displayed, THEN it should categorize each sub-claim as: "Supported" (multiple authoritative sources agree), "Contradicted" (sources directly contradict the claim), or "Unsupported" (insufficient evidence from authoritative sources)
19. GIVEN unsupported claims exist, WHEN the verdict is presented, THEN they should be clearly marked as lacking evidence (not proven false)
20. GIVEN the user reviews the verdict, WHEN they read recommendations, THEN the system should prioritize findings by credibility rather than overwhelming them with information

### Report Persistence
21. GIVEN the investigation is complete, WHEN the user sees the verdict, THEN they should have an option to save the report
22. GIVEN the user elects to save, WHEN the save command is issued, THEN a Markdown file should be generated with the investigation metadata (timestamp, original claim), step-by-step findings, and final verdict
23. GIVEN a report is saved, WHEN the file is written, THEN it should be human-readable and suitable for sharing or archiving

### Session Flow
24. GIVEN a report has been saved, WHEN the save completes, THEN the terminal should return to the idle state ready for a new investigation
25. GIVEN the user is in idle state, WHEN they enter a new `/investigate` command, THEN the system should begin a fresh investigation independent of prior sessions
26. GIVEN the user enters an invalid command, WHEN it is processed, THEN the system should display a helpful error message and return to idle state

### Session Persistence & Recovery
27. GIVEN an investigation is in progress, WHEN the system continuously auto-saves, THEN it should persist the session state to `.session/session-{id}-{timestamp}.{format}`
28. GIVEN session state is being persisted, WHEN saved, THEN it should include: original claim, decomposed sub-claims, partial investigation findings, current agent state, and streaming output log
29. GIVEN the application terminates unexpectedly (crash, Ctrl+C), WHEN the user restarts the application, THEN the system should detect the incomplete session and offer to resume
30. GIVEN the user chooses to resume, WHEN the session is restored, THEN the investigation should continue from the last saved checkpoint without losing context
31. GIVEN the user chooses not to resume, WHEN declined, THEN the system should archive the incomplete session and start fresh

## Decision References

Technical implementation decisions have been extracted to dedicated decision records for better maintainability and traceability.

### Architecture Decision Records (ADRs)

Cross-cutting, long-lived decisions affecting multiple modules:

- **[ADR-0001: Multi-Agent Architecture with LangGraph](../../docs/adr/0001-multi-agent-architecture-with-langgraph.md)** - Workflow orchestration strategy
- **[ADR-0002: Three-Tier LLM Model Strategy](../../docs/adr/0002-three-tier-llm-model-strategy.md)** - Model selection per agent
- **[ADR-0003: LLM Provider and Web Search Integration](../../docs/adr/0003-llm-provider-web-search-integration.md)** - OpenAI as LLM provider
- **[ADR-0004: Session Persistence and Recovery Strategy](../../docs/adr/0004-session-persistence-recovery.md)** - File-based state management

### Increment Design Decisions

Local, reversible decisions specific to this MVP:

- **[Belling Cat MVP Design Decisions](../../docs/design/belling-cat-mvp.md)**
  - DD-001: Terminal UI Framework Selection (Rich + Yachalk)
  - DD-002: Report Format and Storage (Markdown in `.reports/`)
  - DD-003: Command Routing and State Machine (Simple dispatch)
  - DD-004: Verification Strategy (LLM-based credibility, evidence association, confidence)

## Testing Decisions

### Testing Approach: Workflow Integration Seam

Tests should verify the complete `/investigate` command flow end-to-end without mocking internal agent logic:

- **Input**: User provides `/investigate <claim>` via CLI
- **Output**: Streamed real-time findings to terminal + final Markdown report file
- **Seam level**: CLI interface → workflow orchestration → file output (highest-level integration point)

### What Makes a Good Test
- Tests should verify **external behavior only**: claims submitted, real-time findings displayed, reports saved with expected structure
- Tests should NOT verify implementation details like exact agent call order, LLM prompt wording, or internal state
- Tests should use realistic test data: actual news stories or well-known events that can be fact-checked

### Modules to Test
- **CLI interface**: Command parsing, error handling for invalid inputs, routing to investigation workflow
- **LangGraph workflow**: Full orchestration from claim submission to verdict generation (with mocked LLM responses using deterministic fixtures)
- **Report generation**: Markdown output format, metadata accuracy, file persistence
- **Real-time output streaming**: Intermediate findings appear in order, formatting is readable

### Test Data & Fixtures
- Mock LLM responses representing typical findings (supported claims, contradicted claims, unsupported claims)
- Fixture claims: a mix of verifiable facts (easily supported), false claims (contradicted by sources), and ambiguous claims (unsupported)
- Pre-recorded web search results to avoid actual API calls during testing

### Prior Art
- Similar integration tests in Python projects often use `pytest` with fixtures and parametrization
- Terminal output testing can use `pytest-caplog` or Rich's built-in `Console` with `record=True` to capture output
- File I/O testing uses temporary directories (`pytest.TempPathFactory` or `tmpdir`)

## Out of Scope

- **`/interview me` mode**: Post-MVP feature where the system interviews users to clarify their claim before investigating
- **Historical fact-checking sessions**: Retrieving, comparing, or re-investigating prior reports
- **User authentication or multi-user support**: This is a single-user CLI tool
- **Caching of investigation results**: Each new investigation is independent
- **Export formats beyond Markdown**: JSON, PDF, or other export formats are deferred
- **Claim monitoring over time**: Detecting when a previously-checked claim changes (longitudinal tracking)
- **Interactive drill-down during investigation**: User cannot interrupt or modify the investigation once started

## Further Notes

- The feature prioritizes **clarity over information volume**: the system should guide users to important findings rather than overwhelming them with raw data
- Real-time streaming is critical for user engagement; investigations should feel interactive, not like a black-box processing delay
- The three-tier LLM model strategy (fast decomposer, mid-tier investigator, strong verifier) balances cost, latency, and reasoning capability for MVP
- The MVP assumes the user submits well-formed English-language claims; non-English or extremely ambiguous submissions are out of scope
- Future phases may add the `/interview` mode, result persistence, or other features once the core MVP is validated
