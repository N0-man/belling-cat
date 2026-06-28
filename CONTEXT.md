# Belling Cat Fact-Checking Context

A terminal-based fact-checking application that investigates user-submitted claims using open-source intelligence techniques.

## Language

**Claim** _(Aggregate Root)_:
A factual assertion submitted by the user for investigation. The aggregate root that owns the investigation lifecycle and all associated findings. Example: "elephant was seen flying near Changi Airport yesterday".
_Avoid_: Query, assertion, statement, hypothesis

**Sub-claim** _(Value Object)_:
A discrete, independently verifiable component extracted from a Claim during decomposition. Immutable once created. Example: from the claim above, sub-claims might be "elephant", "flying", "Changi Airport", "yesterday".
_Avoid_: Claim fragment, sub-assertion, component claim

**Investigation** _(Aggregate Root)_:
The complete fact-checking process and its accumulated state for a single Claim, including all findings, evidence, and the final verdict. Has identity and lifecycle (in-progress → complete).
_Avoid_: Session, verification process, fact-check

**Finding** _(Value Object)_:
An intermediate discovery or progress update logged during an investigation. Immutable records streamed to the user in real-time. Example: "Searching for elephant sightings...", "Found 3 relevant news articles...".
_Avoid_: Log entry, progress update, intermediate result

**Evidence** _(Value Object)_:
A sourced fact discovered during investigation, including the content, source reference, credibility assessment, and timestamp. More structured than a Finding.
_Avoid_: Fact, source data, finding

**Source** _(Value Object)_:
An information origin with credibility attributes (URL, authority level, publication date). Authority hierarchy: government > academic > established news > other.
_Avoid_: Reference, link, citation

**Verdict** _(Value Object)_:
The final categorization of a claim's veracity: "Supported" (authoritative sources agree), "Contradicted" (sources directly refute it), or "Unsupported" (insufficient authoritative evidence).
_Avoid_: Result, conclusion, determination, judgment

**Report** _(Read Model)_:
A Markdown file projection of a completed Investigation, saved to disk for archival. Contains metadata, findings log, and verdict. Not a domain entity - it's a persistence artifact.
_Avoid_: Output, summary, investigation file
