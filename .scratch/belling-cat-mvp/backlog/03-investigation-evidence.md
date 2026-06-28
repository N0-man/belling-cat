# Item 03: Investigation & Evidence Gathering

## Status

to-do

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Implement the Investigation Agent that searches for evidence using OpenAI's GPT model with web search enabled. This agent takes decomposed sub-claims, searches for authoritative sources, and streams real-time findings to the terminal.

The user should see live progress updates like "Searching for elephant sightings...", "Found 3 news articles...", etc. Evidence gathered includes source URLs, publication dates, and relevance assessments.

## Acceptance criteria

- [ ] LangGraph workflow node created for Investigation Agent
- [ ] Agent uses GPT-4 Turbo (or equivalent mid-tier model) with web search capability
- [ ] Given sub-claims, agent searches for evidence from authoritative sources
- [ ] Real-time findings streamed to terminal using Rich's Live Display
- [ ] Evidence captured includes: source URL, publication date, credibility hint, specific quote/fact
- [ ] Multiple sub-claims can be investigated in parallel where dependencies allow
- [ ] Source authority levels identified (government, academic, news, social media, etc.)
- [ ] Integration test with mocked streaming responses verifies terminal output
- [ ] End-to-end test with real OpenAI API verifies evidence gathering

## Blocked by

Item 02
