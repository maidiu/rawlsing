# `R31E_EXPRESSION_PORT@1` — future intake boundary

This is the reusable boundary for a later R31J/R30G first-session integration. It is not a dependency on unreturned sibling code.

## Inputs

The caller supplies one of:

- `actor_contract` (`R31E_ACTOR_REALIZATION_CONTRACT@1`) compiled from the actual actor/world/readset; or
- the equivalent fields needed by `r31e.expression.compile_contract`: session with `world()`, `events()`, `episodes()`, M6 perceptions, `product.seed.custody()`, `scene_open()`, `contact_status()`, branch/clock.

The contract must include actor-authorized state and M6 knowledge; it must exclude user attention/preferences from causal generation.

## Operation

```text
contract -> propose() -> candidates
         -> validate() -> one bounded candidate
         -> admit() -> exact world event / C12 episode + admission record
         -> user phenomenal compositor (separate)
```

## Outputs

- `R31E_EXPRESSION_CANDIDATE@1` (selected and alternatives);
- `R31E_EXPRESSION_ADMISSION@1` with contract hash, source/target/consumed identity, exact event/episode ids, validation checks, motive status, attention-excluded flag;
- exact `SPEECH`/`REPAIR`/`MESSAGE`/`SILENCE` occurrence bound in actual C12/world history.

## Required invariants

1. No candidate text without successful template re-render and fact/knowledge checks.
2. No user attention or preference input to `propose()`/actor strategy.
3. No private actor field in the user surface.
4. No invented B/private/unobserved fact.
5. No unbounded rerender/reviewer loop; at most one bounded fallback/silence.
6. Exact admitted text is immutable for cold/replay/perception.
7. Source/readset identity remains in the admission record.

## Integration note

A future R31J source-backed GM01→BP2/C9/C12 product can compile the same contract from its actual readset and call this port. It must not treat this deterministic TEST_ONLY grammar as native CAN008/V2 semantics, and it must not claim live external model calls unless actually executed and separately authorized.
