# Belling Cat Fact-Checking Context

A terminal-based fact-checking application that investigates user-submitted claims using open-source intelligence techniques.

## Language

**Claim**:
A factual assertion submitted by the user for investigation. A Claim is the immutable subject of an Investigation.
_Avoid_: Query, statement, hypothesis

**Sub-claim**:
A discrete factual assertion derived from a Claim that can be investigated independently. Example: “An elephant was present near Changi Airport yesterday” and “The elephant was observed flying.”
_Avoid_: Keyword, claim fragment, search term

**Investigation** _(Aggregate Root, where this classification is useful)_:
The fact-checking process and accumulated state for one Claim. It owns the lifecycle from in-progress to complete and coordinates Findings, Evidence, and the final Verdict.
_Avoid_: Session, generic workflow, fact-check result

**Finding**:
An immutable intermediate observation produced during an Investigation, such as a search step completed or relevant material discovered.
_Avoid_: Debug log, final evidence, verdict

**Evidence**:
A sourced fact used to evaluate a Sub-claim, including its content, Source, credibility assessment, and relevant timestamp.
_Avoid_: Finding, unsourced assertion, raw search result

**Source**:
The origin of Evidence, including provenance such as URL, publisher or authority, and publication date. Credibility is assessed in context rather than inferred from a fixed label alone.
_Avoid_: Citation text, evidence, finding

**Verdict**:
The final assessment of a Claim or Sub-claim: **Supported**, **Contradicted**, or **Unsupported**. Unsupported means authoritative evidence is insufficient; it does not mean the assertion is proven false.
_Avoid_: Result, judgment without evidence, confidence score

**Report** _(Read Model)_:
A Markdown projection of a completed Investigation for sharing or archival. It contains investigation metadata, Findings, Evidence, and Verdicts but is not itself a domain entity.
_Avoid_: Investigation, raw output, session file
