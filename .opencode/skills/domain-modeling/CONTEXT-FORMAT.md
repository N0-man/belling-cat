# CONTEXT.md format

```md
# <Domain or context name>

<One or two sentences describing its purpose.>

## Language

**Claim**:
A concise domain definition in one or two sentences.
_Avoid_: Query, assertion

**Investigation** _(Aggregate Root, only if useful)_:
A definition that makes identity, lifecycle, or ownership clearer.
```

## Rules

- Pick one canonical term and list misleading synonyms only when helpful.
- Define domain meaning, not implementation mechanics.
- Include domain-specific language that reduces ambiguity; omit obvious everyday terms.
- Tactical DDD labels are optional.
- Keep ownership unambiguous when lifecycle or invariants matter.
- Create `CONTEXT-MAP.md` only when distinct contexts with different language or ownership truly exist.
