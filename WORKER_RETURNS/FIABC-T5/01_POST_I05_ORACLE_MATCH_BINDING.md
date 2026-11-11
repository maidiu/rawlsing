# FIABC-T5 — Post-I05 Independent Oracle Match Binding

## Ownership boundary

T3 owns oracle creation/freeze.

T5 owns only the post-I05 comparison/control binding.

The candidate process never receives the oracle as expected-truth state.

## Required causal order

`SOURCE IDENTITY FREEZE`
→ `AUTHORITY / WORKLOAD FREEZE`
→ `INDEPENDENT ORACLE MATERIALIZE / FREEZE`
→ `FRESH CANDIDATE PROCESS`
→ `C11`
→ `I03`
→ `I05`
→ `CANDIDATE OBSERVATION LEAVES PROCESS`
→ `INDEPENDENT ORACLE MATCH`.

The live execution gate requires material source-local oracle documents before any candidate process may start.

Each T3 oracle entry must bind:

- `oracle_identity_sha256`;
- `oracle_freeze_authority_ref`;
- `oracle_document_path`;
- `oracle_document_sha256`.

T5 verifies the oracle document bytes and accepted frozen-oracle semantic identity before execution.

## Actual candidate observation

S05 emits a governed observation produced from the actually executed current cell.

It binds:

- exact source identity;
- frozen court/workload identity;
- actual semantic-authority closure and digest;
- actual C11 projection/release/replay refs;
- full I05 frontier and digest;
- candidate-level typed fact/state rows;
- complete I05 learned-product coverage;
- exact constituent-I03 fact closure;
- replay/dependency closure;
- exact refs;
- negative-state law;
- semantic/replay/output identities.

T5 re-executes every exact I05 candidate query role through the same bound I03 executor and requires its exact fact-ref set to equal that candidate's declared I05 fact refs.

The global constituent I03 ref set must equal the complete I05 empirical fact-ref set.

## Neutral parent comparison

Only after the child returns does the neutral parent call:

1. `verify_frozen_oracle(...)`;
2. `validate_candidate_observation(...)`.

The resulting receipt is candidate-specific and binds one exact source-local oracle identity.

Performance admission is downstream of the independent oracle match.

There is no transition:

`SELF_REPLAY_OK -> SEMANTIC_PARITY_PASS`.

## Three-way source gate

When Candidate C completes S05, T5 requires actual stored observations for A, B and C for that source.

It then calls:

`validate_three_way_parity(frozen_oracle, {"A": A, "B": B, "C": C})`.

The gate fails if:

- C is absent;
- one candidate identity is substituted;
- one candidate mismatches;
- candidates do not bind the same oracle identity;
- the frozen oracle was mutated.

A/B agreement is not sufficient.

Candidate A is never expected truth for B/C.

Majority vote is never expected truth.

## Comparison grain

The accepted I05 comparison checks full governed identity, not scalar/value equality:

- source;
- authority/court closure;
- projection/release;
- full frontier;
- typed I03 facts/states;
- full I05 product/coverage;
- semantic/replay/output identity;
- exact refs;
- negative-state law.

## Replay separation

T4 S15 fresh replay is retained as lifecycle/replay evidence.

It is not used to define the oracle.

It cannot retroactively rewrite expected truth.

Its only terminal role is to prove later reproduction of the same governed terminal.
