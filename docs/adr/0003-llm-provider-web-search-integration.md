# LLM Provider and Web Search Integration

**Status:** Accepted
**Related PRD:** [belling-cat-mvp](../../.scratch/belling-cat-mvp/PRD.md)

## Decision

Use OpenAI Chat Completion API as the primary LLM provider with built-in web search capability.

The LLM's web search is the primary investigative mechanism. No external search APIs required (no separate Tavily, Perplexity, or Google Search integration).

## Why

PRD requires OpenAI's GPT with real-time web search enabled for fact-finding (PRD Requirements 11, 30). Investigation must use LLM's web search as primary investigative mechanism and capture source URL, publication date, credibility assessment, and specific evidence (PRD Requirement 12).
