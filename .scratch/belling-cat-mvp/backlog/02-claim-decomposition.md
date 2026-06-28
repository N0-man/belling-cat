# Item 02: Claim Decomposition Agent

## Status

done

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Implement the Claim Decomposition Agent using LangGraph and OpenAI's GPT-4o mini model. This agent receives a user's claim and breaks it into discrete, independently verifiable sub-claims returned as structured JSON.

The agent should handle both simple single-fact claims (keeping them as-is) and complex multi-faceted claims (splitting them logically). This is the first agent in the investigation pipeline.

## Acceptance criteria

- [x] LangGraph workflow node created for Claim Decomposition Agent
- [x] Agent uses GPT-4o mini model (configured via OpenAI SDK)
- [x] Given a complex claim, agent returns JSON array of sub-claims
- [x] Given a simple claim, agent recognizes it and returns single-element array
- [x] Sub-claims are independently verifiable and logically separated
- [x] Agent prompt engineered to produce consistent JSON structure
- [x] Integration test with mocked LLM responses verifies decomposition logic
- [x] End-to-end test with real OpenAI API call (marked as integration/slow test)

## Blocked by

Item 01
