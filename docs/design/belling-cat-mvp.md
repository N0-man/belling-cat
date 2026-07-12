# Belling Cat MVP Design Decisions

This document contains local, increment-specific design decisions that are reasonably reversible and don't require full ADR treatment.

---

## DD-001: Terminal UI Framework Selection

**Status:** accepted  
**Related requirements/stories:** PRD Requirements 1-2, 7-8, 17-20 (User interaction, real-time display, verdict formatting)  
**Related code:** `belling_cat/cli.py`

### Context

The Belling Cat MVP requires a terminal-based user interface with:
- ASCII art banner display
- Real-time streaming of investigation findings
- Formatted verdict display (panels, tables, color coding)
- Progress indicators during long-running operations
- Command input and error message display

The terminal UI needs to be rich enough for good UX but simple enough for fast MVP development.

### Decision

Use **Rich library** for structured terminal output (tables, panels, progress indicators, colors) and **Yachalk** for terminal color/styling primitives where Rich is too heavyweight.

- Rich provides built-in components (Panel, Table, Progress, Live Display)
- Yachalk used for simple color formatting in CLI commands
- ASCII art banner generated programmatically and cached at startup
- Progress indicators and real-time streaming use Rich's `Live` display functionality

### Rationale

**Why Rich:**
- Mature Python library with extensive terminal UI components
- Built-in support for panels, tables, progress bars, syntax highlighting
- `Console` abstraction makes testing easy (record mode for output capture)
- Active development and good documentation
- No TUI event loop required (just formatted output)

**Why Yachalk as supplement:**
- Lightweight for simple color formatting
- Complements Rich for cases where Rich components are overkill
- Similar API to Node's chalk library (familiar patterns)

**Why not alternatives:**
- **Textual:** Full TUI framework with widgets and event loop - too heavyweight for MVP streaming workflow
- **blessed/curses:** Lower-level, requires more manual layout management
- **click.echo with ANSI:** Too primitive, would need to build panels/tables ourselves
- **Plain ANSI codes:** Hardest to maintain, no cross-platform guarantees

### Consequences

**Positive:**
- Rapid development of good-looking terminal UI
- Easy testing via Rich's `Console(record=True)`
- Cross-platform terminal support (Windows, macOS, Linux)
- Rich ecosystem of components for future features

**Negative:**
- Rich dependency adds ~1MB to package size
- Yachalk adds another dependency (though small)
- Rich's API can be verbose for simple cases
- Limited customization compared to building custom TUI

**Testing impact:**
- Tests use `StringIO` + `Console` to capture and verify output
- Can test formatting without actual terminal
- Example: `tests/test_cli.py:238-312` (verdict display tests)

### Alternatives considered

**Alternative 1: Textual (full TUI framework)**
- Pros: Widget-based, event-driven, very polished
- Cons: Overkill for streaming workflow, steeper learning curve, requires event loop
- Rejected: MVP doesn't need interactive widgets, just formatted output

**Alternative 2: blessed (curses wrapper)**
- Pros: Full terminal control, mature library
- Cons: Lower-level API, manual layout management, harder to test
- Rejected: Too much boilerplate for panels/tables we need

**Alternative 3: Plain ANSI escape codes**
- Pros: No dependencies, maximum control
- Cons: Manual color/formatting, no cross-platform guarantees, high maintenance
- Rejected: Would spend more time on UI primitives than core features

---

## DD-002: Report Format and Storage

**Status:** accepted  
**Related requirements/stories:** PRD Requirements 21-23 (Report persistence), Item 05  
**Related code:** `belling_cat/infrastructure/persistence/report_writer.py` (planned)

### Context

Investigations produce findings that users want to save, share, and reference later. The report format must:
- Be human-readable without special tools
- Support structured content (metadata, findings, verdict)
- Include source citations
- Be suitable for sharing (email, GitHub, documentation)
- Work with version control (git-friendly)

### Decision

Save reports as **Markdown files** in `.reports/` directory with filename format: `belling-cat-{timestamp}.md`

**Markdown structure:**
```markdown
# Investigation Report: [Claim]

## Metadata
- **Timestamp:** 2026-07-12 10:30:00 UTC
- **Session ID:** uuid
- **Agents:** Decomposition (GPT-4o mini), Investigation (GPT-4 Turbo), Verification (GPT-4o)

## Investigation Log
[Step-by-step findings with timestamps]

## Verdict
### Sub-claim 1: [text]
**Status:** Supported | Contradicted | Unsupported
**Confidence:** High | Medium | Low
**Explanation:** [reasoning]
**Sources:**
- [citation with URL]

## Contradictions
[Detected contradictions between sources]
```

### Rationale

**Why Markdown:**
- Human-readable in plain text editors
- Renders beautifully in GitHub, GitLab, VS Code preview
- Git-friendly (line-based diffing, version control)
- Supports formatting (bold, lists, links) without proprietary format
- Easy to convert to HTML/PDF if needed later
- Standard for technical documentation

**Why `.reports/` directory:**
- Clear separation from code and temporary state
- Easy to `.gitignore` or commit depending on use case
- Standard location pattern (similar to `.cache/`, `.config/`)

**Why timestamp-based naming:**
- Avoids filename conflicts
- Natural chronological sorting
- User can still rename files manually if desired
- Format: `YYYY-MM-DD-HHMMSS` for sortability

### Consequences

**Positive:**
- Reports viewable without Belling Cat installed
- Can be committed to git for documentation
- Shareable via any text medium (email, Slack, GitHub)
- Future HTML export is straightforward (markdown → HTML converters)
- Standard format makes automation easy

**Negative:**
- No machine-readable metadata (would need frontmatter or separate JSON)
- No built-in search/indexing (would need external tool)
- Manual organization required (no tagging, categorization)
- File system clutter if many reports generated

**Testing impact:**
- Tests can verify Markdown structure with regex or markdown parser
- Use `pytest.TempPathFactory` for isolated test reports
- Can snapshot-test report format

### Alternatives considered

**Alternative 1: JSON format**
- Pros: Machine-readable, easy to parse, structured data
- Cons: Not human-readable, requires tool to view, poor git diffs
- Rejected: MVP prioritizes human sharing over machine processing

**Alternative 2: HTML format**
- Pros: Rich formatting, embeddable images, consistent rendering
- Cons: Verbose, harder to edit, requires browser to view
- Rejected: Markdown can be converted to HTML if needed; start simpler

**Alternative 3: PDF format**
- Pros: Fixed layout, professional appearance, self-contained
- Cons: Binary format (not git-friendly), requires library, not editable
- Rejected: Too heavy for MVP, Markdown serves 95% of use cases

**Alternative 4: SQLite database**
- Pros: Structured querying, relationships, versioning
- Cons: Not shareable as individual files, requires tool to extract
- Rejected: Out of scope for MVP (no search/comparison features)

---

## DD-003: Command Routing and State Machine

**Status:** accepted  
**Related requirements/stories:** PRD Requirements 3, 24-26 (Command parsing, session flow), Item 01  
**Related code:** `belling_cat/cli.py`

### Context

The CLI needs to:
- Parse user commands (`/investigate`, `/save`, potentially others)
- Route commands to appropriate handlers
- Manage application state (idle, investigating, displaying, error)
- Provide helpful error messages for invalid input
- Allow extension for future commands

### Decision

Implement **simple command routing** with **linear state machine**:

**Commands:**
- `/investigate <claim>` - Start investigation
- `/save <report-name>` (optional) - Save current investigation report
- `/help` - Display available commands
- `/quit` or `/exit` - Exit application

**State machine:**
```
idle → [/investigate] → investigating → displaying results → idle
                ↓                              ↓
              error ←------------------→ error → idle
```

**Implementation approach:**
- Dictionary-based command dispatch: `{"investigate": investigate_handler, "save": save_handler}`
- Simple state tracking: `current_state: str` variable
- State transitions enforced by handlers (only allow `/save` when in `displaying` state)
- Invalid commands return helpful error with available commands

### Rationale

**Why simple dispatch:**
- MVP has minimal commands (2-3 primary commands)
- Dictionary dispatch is easy to understand and extend
- No need for command framework overhead (Click, Typer)
- State validation happens in handlers, not routing layer

**Why linear state machine:**
- Investigation workflow is inherently sequential (can't decompose before investigating)
- No complex branching or parallel states needed for MVP
- Easy to reason about and debug
- State transitions explicit in code (no hidden state)

**Why not command framework:**
- Click/Typer add abstraction for minimal value in MVP
- Custom routing gives full control for future features
- State management would still be manual even with framework
- Simpler testing (just call handlers directly)

### Consequences

**Positive:**
- Fast to implement and modify
- Easy to test (mock command dispatch dictionary)
- Clear state transitions
- Low cognitive overhead for contributors

**Negative:**
- Manual command parsing (no automatic arg validation)
- Need to handle edge cases manually (wrong state, invalid args)
- No built-in help generation
- Would need refactoring if command set grows significantly (>10 commands)

**Testing impact:**
- Tests can directly invoke handler functions
- Can test state transitions in isolation
- Example: `tests/test_cli.py` (command parsing tests)

### Alternatives considered

**Alternative 1: Click or Typer framework**
- Pros: Automatic arg parsing, help generation, validation, testing utilities
- Cons: Abstraction overhead, learning curve, less control over state management
- Rejected: Overkill for 2-3 commands, state machine still manual

**Alternative 2: REPL with command history (cmd module)**
- Pros: Built-in Python module, readline support, history, tab completion
- Cons: Synchronous blocking model conflicts with streaming output
- Rejected: Rich Live display works better for streaming investigations

**Alternative 3: Event-driven state machine (asyncio)**
- Pros: More flexible for future features, non-blocking
- Cons: Much more complex, unnecessary for sequential workflow
- Rejected: MVP doesn't need concurrent commands or async state

---

## DD-004: Verification Strategy

**Status:** accepted  
**Related requirements/stories:** PRD Requirements 14-16, Item 04, Item 04.1  
**Related code:** `belling_cat/application/services/verifier_service.py`, `belling_cat/infrastructure/llm/openai_adapter.py`

### Context

The Verifier Agent must:
- Assess source credibility using a hierarchy (government > academic > news > other)
- Detect contradictions between sources
- Generate verdicts (Supported/Contradicted/Unsupported) with explanations
- Handle evidence-to-subclaim association
- Include confidence levels in verdicts

During Item 04 validation, several design decisions were identified that were implemented but not documented. Item 04.1 will add confidence to the domain model and improve evidence association.

### Decision

**Credibility Assessment Approach:** Delegate to GPT-4o via prompt engineering

**Rationale:**
- Leverages GPT-4o's strong reasoning for nuanced credibility evaluation
- Avoids rigid rule-based logic that may miss context-dependent factors
- Simpler MVP implementation without complex domain algorithms
- Credibility hierarchy encoded in LLM prompt: "Use the authority hierarchy: government > academic > established news > other"

**Trade-offs:**
- Non-deterministic behavior (LLM may assess differently on retries)
- Harder to unit test credibility logic independently of LLM
- Coupled to LLM prompt design
- Cannot easily inspect credibility scoring algorithm

**Contradiction Detection Approach:** LLM-based semantic analysis

**Rationale:**
- GPT-4o can detect semantic contradictions beyond simple keyword matching
- Handles temporal contradictions, numerical conflicts, negations
- Provides natural language explanations of contradictions
- Prompt: "Detect contradictions between sources and explain them"

**Trade-offs:**
- Non-deterministic detection (may miss subtle contradictions)
- Cannot verify detection accuracy without manual review
- Prompt tuning required if detection quality insufficient

**Evidence Association Strategy:** Associate evidence with sub-claims during investigation (User Decision from Validation)

**Rationale:**
- Each sub-claim should be verified independently with relevant evidence
- Passing all evidence to all sub-claims creates incorrect verification context
- Workflow state tracks: `evidence: dict[str, list[Evidence]]` (key = subclaim.text)
- Investigation node preserves association during evidence gathering
- Verification node uses only relevant evidence per sub-claim

**Implementation:**
```python
# Investigation node preserves association
evidence_by_subclaim = {}
for subclaim in subclaims:
    evidence = investigation_service.investigate(subclaim.text)
    evidence_by_subclaim[subclaim.text] = evidence

# Verification node uses relevant evidence
for subclaim in subclaims:
    relevant_evidence = evidence_by_subclaim.get(subclaim.text, [])
    verdict, contradictions = verifier_service.verify_with_contradictions(
        subclaim, relevant_evidence
    )
```

**Confidence in Verdict Domain Model:** Include confidence field (User Decision from Validation)

**Rationale:**
- LLM provides confidence assessment ("high", "medium", "low")
- Useful for highlighting low-confidence verdicts to users
- Helps users understand when to review findings more carefully
- `Verdict` value object updated to include `confidence: str`

**Implementation:**
```python
@dataclass(frozen=True)
class Verdict:
    subclaim: SubClaim
    category: str  # "Supported", "Contradicted", "Unsupported"
    explanation: str
    confidence: str  # "high", "medium", "low" (NEW in Item 04.1)
```

**Display strategy:**
- Low confidence: Yellow styling with "(Low Confidence - Review Carefully)" note
- Medium confidence: Add "(Medium Confidence)" note
- High confidence: Standard styling

### Rationale

**Why LLM-based approach for MVP:**
- Fastest path to validating core fact-checking workflow
- GPT-4o's reasoning sufficient for initial quality assessment
- Can add domain logic later if LLM quality insufficient
- Flexibility for complex credibility scenarios

**Why evidence association matters:**
- Independent verification is a core fact-checking principle
- Mixing evidence across sub-claims can produce incorrect verdicts
- Example: Evidence that "Paris is in France" shouldn't influence verdict on "Eiffel Tower built in 1889"

**Why confidence is valuable:**
- Transparency for users about verdict certainty
- Allows users to prioritize review of low-confidence findings
- Natural output from LLM reasoning process

### Consequences

**Positive:**
- Fast MVP implementation without complex algorithms
- Flexible for context-dependent credibility assessment
- Natural language explanations from LLM
- Evidence isolation improves verification accuracy
- Confidence helps users make informed decisions

**Negative:**
- Non-deterministic behavior (retries may differ)
- Harder to test verification logic independently
- Credibility assessment opaque (can't inspect scoring)
- Prompt engineering becomes critical business logic
- Evidence association requires workflow state refactoring

**Testing impact:**
- Tests use mocked LLM responses with deterministic verdicts
- Integration tests verify confidence preservation through layers
- Cannot easily test credibility hierarchy compliance (LLM black box)
- Evidence association testable via workflow state inspection

### Alternatives considered

**Alternative 1: Domain-layer credibility scoring algorithm**
- Pros: Deterministic, testable, inspectable, no LLM dependency
- Cons: Rigid rules miss context, requires maintaining credibility database
- Deferred: Can implement if LLM quality insufficient post-MVP

**Alternative 2: Rule-based contradiction detection**
- Pros: Deterministic, testable, handles obvious contradictions (dates, numbers)
- Cons: Misses semantic contradictions, requires complex rule engine
- Deferred: Can supplement LLM detection if gaps identified

**Alternative 3: No evidence association (pass all evidence to all sub-claims)**
- Pros: Simpler workflow state, no association tracking
- Cons: Incorrect verification context, violates independent verification principle
- Rejected: User decision favored Option B (association) during validation

**Alternative 4: Omit confidence from domain model**
- Pros: Simpler domain model, fewer fields to maintain
- Cons: Loses valuable transparency signal for users
- Rejected: User decision included confidence during validation

### Related Validation Findings

This design decision documents the resolution of:
- **F-002:** Evidence filtering strategy (User Decision: Option B - associate with sub-claims)
- **F-004:** Confidence field usage (User Decision: include in domain model)
- **F-007:** Verification strategy undocumented (material design decisions)

### Future Considerations

If verification quality becomes insufficient:

1. **Hybrid approach:** Use LLM for nuanced cases, rules for obvious patterns
2. **Credibility database:** Maintain known source credibility scores
3. **Contradiction taxonomy:** Classify contradiction types (temporal, numerical, semantic)
4. **Confidence calibration:** Measure LLM confidence accuracy and adjust thresholds

For MVP, LLM-based approach with evidence association and confidence provides best balance of quality, flexibility, and implementation speed.
