---
status: accepted
increment: belling-cat-mvp
related_decisions:
  - ADR-0001 (Multi-Agent Architecture with LangGraph)
---

# Session Persistence and Recovery Strategy

## Context

Fact-checking investigations may take several minutes to complete, involving multiple LLM calls, web searches, and agent interactions. Users may experience:

- Application crashes (bugs, system failures)
- Intentional interruptions (Ctrl+C, closing terminal)
- Network failures during long-running investigations
- Power outages or system restarts

Losing investigation progress creates poor user experience and wastes LLM API costs (already paid for partial work). The system must support:

1. Continuous state persistence during active investigations
2. Detection of incomplete sessions on restart
3. Recovery mechanism to resume from last checkpoint
4. Cleanup of completed sessions

The solution must serialize LangGraph workflow state (from ADR-0001) including agent outputs, intermediate findings, and current execution position.

## Decision

Implement **continuous auto-save to file-based session storage** with:

- **Storage location:** `.session/` directory in user's workspace
- **File naming:** `session-{id}-{timestamp}.json` (metadata) + `session-{id}-{timestamp}.pkl` (LangGraph state)
- **Format:** JSON for human-readable metadata, Python pickle for LangGraph workflow state objects
- **Persistence frequency:** After each agent node completion (decomposition → investigation → verification)
- **Recovery flow:** On startup, detect incomplete sessions and prompt user to resume or archive
- **Cleanup:** Completed sessions archived or deleted after successful report generation

## Rationale

### File-Based Storage

- **Simplicity:** No database dependency for MVP
- **Local ownership:** User's data stays on their machine (privacy)
- **Easy inspection:** JSON metadata human-readable, pickle debuggable
- **No server required:** Pure client-side application
- **Git-friendly:** Can `.gitignore` sessions without losing code

### Dual Format (JSON + Pickle)

- **JSON metadata:** Session ID, claim text, timestamp, phase, status (human-readable, portable)
- **Pickle state:** LangGraph `InvestigationState` TypedDict with complex objects (Evidence, Verdict, SubClaim)
- **Separation rationale:** Humans read metadata to decide resume/archive; pickle for exact workflow restoration

### Storage Location

- **`.session/` directory:** Standard convention for temporary state (like `.cache/`, `.config/`)
- **User workspace:** Stays with project, no global state pollution
- **Gitignore-able:** Sessions are user-specific, not committed to repository

### Persistence Frequency

- **After each agent node:** Balance between recovery granularity and I/O overhead
- **Node completion:** Clean state boundaries (decomposition done → investigation started → verification done)
- **Not after every LLM call:** Too frequent, minimal additional recovery value

### Recovery Strategy

- **Prompt user on startup:** Transparent, user controls resume vs restart
- **Resume from last checkpoint:** Restore workflow state, continue from next node
- **Archive declined sessions:** Preserve for debugging, don't block new investigations

## Consequences

### Positive

- Users can recover from crashes without losing progress or API costs
- Debugging aided by inspectable session files
- No external dependencies (database, message queue)
- Privacy-preserving (local storage only)
- Simple MVP implementation

### Negative

- **LangGraph state coupling:** Pickle format tied to LangGraph internals (version-sensitive)
- **Portability limitation:** Pickle files not portable across Python versions or platforms
- **No multi-device sync:** Sessions locked to single machine
- **Manual cleanup required:** Old sessions accumulate unless cleaned
- **Limited querying:** Cannot easily search/filter across sessions (would need database)

### Mitigation Strategies

- **Version LangGraph dependency:** Pin version to avoid pickle deserialization issues
- **Metadata JSON separately:** Provides portable session info even if pickle fails
- **Document cleanup process:** User guide for managing .session/ directory
- **Future migration path:** JSON metadata enables future migration to database if needed

### Testing Impact

- Tests can verify session files are created at correct checkpoints
- Recovery tests can serialize/deserialize mock workflow state
- Cleanup tests can verify old sessions are archived/deleted
- No need to test LangGraph's own state management (trust the library)

### Security Considerations

- **Sensitive data:** Claims and findings stored in plaintext (acceptable for MVP)
- **File permissions:** Rely on OS file permissions (user-readable only)
- **No encryption:** MVP assumption that user's machine is trusted
- **API keys:** Never stored in session files (read from environment)

### Storage Requirements

- **Per session:** ~1-5 KB JSON + ~10-50 KB pickle (depending on claim complexity)
- **Cleanup strategy:** Archive after 7 days, delete after 30 days (configurable)
- **Expected volume:** <100 MB for typical user (hundreds of sessions)

## Considered alternatives

### Alternative 1: SQLite Database

**Approach:** Store session state in local SQLite database with structured schema.

**Pros:**
- Structured querying (search sessions by claim, date, status)
- Better data integrity (ACID transactions)
- Easier cleanup (DELETE WHERE timestamp < X)
- Portable format (SQL standard)
- Better for future features (session history, comparison)

**Cons:**
- Requires SQLAlchemy or similar ORM
- Schema migrations needed for LangGraph state changes
- Serializing complex objects (Evidence, Verdict) requires mapping layer
- Overkill for MVP (no querying required yet)
- Additional dependency and complexity

**Why rejected:** Too complex for MVP. File-based sufficient for single-session recovery. SQLite useful when multi-session features added (historical search, comparison).

### Alternative 2: Redis or Key-Value Store

**Approach:** Use Redis/Memcached for in-memory session state with optional persistence.

**Pros:**
- Fast read/write (in-memory)
- Built-in TTL for automatic cleanup
- Atomic operations for state updates
- Could support future multi-user scenarios

**Cons:**
- Requires Redis server (not pure client-side)
- Deployment complexity (Docker, managed Redis)
- Over-engineered for local single-user tool
- Serialization challenges remain (pickle or JSON)
- Not privacy-preserving (external service)

**Why rejected:** Violates MVP constraint of terminal-based single-user tool. Redis appropriate for server-side multi-user deployment, not local CLI.

### Alternative 3: Event Sourcing

**Approach:** Store sequence of events (ClaimDecomposed, EvidenceFound, VerdictGenerated) and replay to reconstruct state.

**Pros:**
- Full audit trail of investigation steps
- Can replay from any point in history
- Supports future features (investigation analysis, optimization)
- More resilient to state schema changes

**Cons:**
- Significant engineering complexity (event store, replay logic)
- Larger storage footprint (all events vs final state)
- Slower recovery (must replay all events)
- Unclear value for MVP (audit trail not required)

**Why rejected:** Over-engineered for MVP recovery needs. Event sourcing valuable for analytics/audit requirements not present in MVP scope.

### Alternative 4: No Persistence (Accept Data Loss)

**Approach:** Accept that crashes lose progress, rely on fast execution and stability.

**Pros:**
- Zero implementation complexity
- No storage or serialization concerns
- Forces focus on application stability

**Cons:**
- Poor user experience (wasted time and API costs)
- Unacceptable for long investigations (5+ minutes)
- Contradicts PRD requirements (27-31 explicitly require recovery)
- Higher user frustration and churn risk

**Why rejected:** PRD explicitly requires session persistence and recovery (requirements 27-31). User experience priority outweighs implementation simplicity.

## Related Requirements

From PRD:
- Requirement 27: "System continuously auto-saves session state to `.session/session-{id}-{timestamp}.{format}`"
- Requirement 28: "Persisted state includes: claim, sub-claims, findings, agent state, streaming log"
- Requirement 29: "On restart, detect incomplete session and offer to resume"
- Requirement 30: "Resume restores investigation from last checkpoint without losing context"
- Requirement 31: "Declined sessions archived, user starts fresh"

## Implementation Notes

### Session File Structure

**Metadata JSON (`session-{id}-{timestamp}.json`):**
```json
{
  "session_id": "uuid",
  "created_at": "2026-07-12T10:30:00Z",
  "updated_at": "2026-07-12T10:32:15Z",
  "claim": "Original user claim text",
  "status": "in_progress | completed | archived",
  "phase": "decompose | investigate | verify | display",
  "agent_state": "decomposition_complete | investigation_complete | verification_complete"
}
```

**Workflow State Pickle (`session-{id}-{timestamp}.pkl`):**
- Python pickle of `InvestigationState` TypedDict
- Contains: `claim`, `subclaims`, `evidence`, `verdicts`, `contradictions` (per Item 04.1)

### Recovery Logic

1. On app startup, scan `.session/` for files with `status: in_progress`
2. Present list of incomplete sessions to user (claim text, timestamp)
3. User selects resume, archive, or start fresh
4. If resume: deserialize pickle, restore LangGraph workflow, continue execution
5. If archive: move session files to `.session/archived/`, start fresh
6. If start fresh: leave session files untouched, create new session

### Cleanup Strategy

- **After successful report generation:** Mark session `status: completed`, move to `.session/archived/`
- **Manual cleanup command:** `belling-cat clean` removes archived sessions older than 30 days
- **Future:** Optional auto-cleanup on startup (configurable threshold)

## Future Considerations

If feature scope expands beyond single-session recovery:

1. **Historical session querying:** Migrate to SQLite for structured search
2. **Multi-device sync:** Cloud storage backend (S3, Dropbox) for session files
3. **Collaboration features:** Server-side session storage with sharing
4. **Audit requirements:** Event sourcing for full investigation trail
5. **Performance at scale:** Consider binary format other than pickle (protobuf, msgpack)

For MVP, file-based JSON+pickle provides the simplest path to crash recovery without compromising core fact-checking workflow development.
