# Terminal UI Framework

**Status:** Accepted
**Related PRD:** [belling-cat-mvp](../../.scratch/belling-cat-mvp/PRD.md)

## Decision

Use Rich library for structured terminal output (tables, panels, progress indicators, colors) and Yachalk for terminal color/styling primitives where Rich is too heavyweight.

## Why

PRD requires terminal UI with ASCII art banner, text input, real-time intermediate findings display, and formatted verdict output (PRD Requirements 1-2, 7-8, 17-20).
