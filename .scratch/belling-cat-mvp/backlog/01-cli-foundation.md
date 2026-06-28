# Item 01: CLI Foundation & Command Parsing

## Status

to-do

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Build the terminal UI foundation using Rich and Yachalk. This slice delivers a working CLI that displays the "Belling Cat" ASCII art banner, presents an input prompt, and parses two commands: `/investigate <claim>` and `/save <report-name>`.

The CLI should validate command syntax, route valid commands to placeholder handlers (stubbed for now), and display helpful error messages for invalid input. The terminal should feel responsive and polished.

## Acceptance criteria

- [ ] ASCII art banner "Belling Cat" displays on application startup using Rich
- [ ] Input prompt appears using Rich's prompt functionality
- [ ] `/investigate <claim>` command parsed correctly, extracts claim text
- [ ] `/save <report-name>` command parsed correctly, extracts report name
- [ ] Invalid commands display helpful error messages with usage guidance
- [ ] Command routing infrastructure in place (handlers can be stubbed/mocked)
- [ ] Terminal styling uses Yachalk for colors where appropriate
- [ ] Integration test verifies banner display and command parsing end-to-end

## Blocked by

Item 00
