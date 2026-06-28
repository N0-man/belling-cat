# Item 05: Report Generation via /save Command

## Status

to-do

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Implement the `/save <report-name>` command that formats the investigation findings as a Markdown report and persists it to the `.reports/` directory. The report includes metadata (claim, timestamp, agents involved), step-by-step findings, and the final verdict.

The Markdown file should be human-readable and suitable for sharing or archiving.

## Acceptance criteria

- [ ] `/save <report-name>` command handler implemented
- [ ] Report formatted as Markdown with sections: Metadata, Investigation Log, Verdict
- [ ] Metadata includes: original claim, timestamp, agents used, session ID
- [ ] Step-by-step findings formatted chronologically with source citations
- [ ] Final verdict section categorizes each sub-claim clearly
- [ ] Report saved to `.reports/belling-cat-{report-name}-{timestamp}.md`
- [ ] `.reports/` directory created automatically if it doesn't exist
- [ ] User receives confirmation message after successful save
- [ ] Integration test verifies Markdown structure and file persistence
- [ ] Edge case: duplicate report names handled gracefully (append timestamp or counter)

## Blocked by

Item 04
