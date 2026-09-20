# CLOSED35-R2-LAT2011 — Synthetic Qualification Test Protocol

## Status

`TESTS_AUTHORED__NOT_EXECUTED`

This browser worker authored synthetic/source-independent Python rejection tests. It did not execute them because the commissioned surface is GitHub/browser only. No raw `Latinobarometro 2011.sav` carrier was opened or processed.

The executable synthetic test file is:

`rawlsing_next/tests/test_closed35_r2_lat2011_realization.py`

## Qualification invariant

Every future candidate A/B/C must consume one frozen:

`CLOSED35_R2_LAT2011_SOURCE_REALIZATION@1.0.0`

after exact-source/R35 physical prerequisites are satisfied.

A candidate-local semantic repair or source-specific reinterpretation is nonconforming even when terminal values happen to agree on one fixture.

## T01 — Exact source SHA fail-closed

Synthetic incidence:

- exact native SAV reader configuration;
- mutated source SHA.

Required:

`REJECT`

The canonical 2011 realization may not attach to an alternate source snapshot.

## T02 — Native reader/config drift fail-closed

Synthetic incidence mutates native reader configuration, including an unauthorized encoding override.

Required:

`REJECT`

2011 is not a compatibility-decoding source. No family member's compatibility rule may be imported.

## T03 — One A/B/C semantic owner

Construct A, B and C bindings with the exact canonical SHA and one realization identity.

Required:

- all three converge to the same source-specific realization identity.

Mutate C's realization identity.

Required:

`REJECT`

## T04 — Replay identity is SHA + row ordinal

Construct two synthetic rows with different physical row ordinals.

Required:

- distinct replay identities;
- replay identity contains only source SHA and preserved row ordinal.

`NUMENTRE` or `IDENPA+NUMENTRE` may remain source-native attributes but cannot replace the replay key.

A candidate fails if it deduplicates/reindexes rows through native interview fields.

## T05 — Exact source-local variable identity

Construct a synthetic source variable identity from:

- exact canonical SHA;
- exact variable name;
- physical variable ordinal.

Required:

- identity remains scoped to the exact 2011 source.

Fail if exact-name equality in another Latinobarometro wave is treated as semantic/source identity.

## T06 — 18-country coordinate structure

Supply the exact accepted 2011 `IDENPA` count map.

Required:

- 18 codes;
- total 20,204;
- exact frozen count map accepted.

Mutate any count or code.

Required:

`REJECT`

This is a synthetic comparison to the inherited packet expectation, not a remeasurement of source bytes.

## T07 — Physical/user missingness survives

Synthetic pair:

1. `P1ST=-2` with `FORMAT_USER_MISSING_RANGE` and the range declaration;
2. a separate `P1ST` system-missing cell.

Required:

- raw `-2` survives;
- user-missing state survives;
- exact declaration survives;
- system missing remains a distinct state.

Fail if both become one generic null/missing state.

Fail if either physical state alone becomes refusal, don't-know, not-asked or routing authority.

## T08 — Questionnaire/released-storage layer separation

Given an instrument-layer response-code description and a released SAV physical missing state for the same question family:

Required:

- preserve both layers;
- source storage remains source storage;
- questionnaire coding remains documentary instrument authority.

Fail if one is used to rewrite the other.

## T09 — WT preserved without synthesized estimand

Synthetic `WT` physical cell with an observed numeric value.

Required:

- raw carrier preserved;
- documentary role `Weighting` may be retained;
- aggregate estimand authority remains `NO_AGGREGATE_ESTIMAND_AUTHORIZED`;
- default selection remains unauthorized.

Request a universal 18-country population estimand.

Required:

`REJECT`

Request automatic default use.

Required:

`REJECT`

## T10 — No 1995 law leakage

Attempt to apply either:

- the 1995 Brazil 120-row release/methodology discrepancy;
- the 1995 interview-ID special case.

Required:

`REJECT`

The 2011 realization contains no 1995 exception machinery.

## T11 — No 2024 law leakage

Attempt to apply any of:

- `nominal_case_size=174` versus 332 raw-layout exception;
- 2024 WT published-domain conflict;
- 2024 P2ST/P13ST/P19ST repurposing rules.

Required:

`REJECT`

The 2011 realization contains no 2024 exception machinery.

## T12 — Minimal S35/R35 edge scope

Required exact S35 set:

`EC01; EC05; EC12; EC13`

Required R35 hooks:

- I01 physical metadata;
- I02 derivative parentage if a non-direct source is supplied;
- I03 exact source physical scope/expectation/candidate realization/whole-source equivalence receipt.

Fail if browser semantic implementation is substituted for an R35 physical-equivalence receipt.

## T13 — Semantic agreement cannot erase physical divergence

Future candidate fixture:

- candidate semantic output matches the 2011 owner;
- candidate physical receipt changes row order without reversible ordinal identity, drops a user-missing declaration, loses a country carrier, or rewrites/drops WT.

Required:

`REJECT`

A semantic match does not cure physical non-equivalence.

## T14 — Browser claim boundary

Inspect the realization payload.

Required:

- `SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__NOT_PHYSICAL_EQUIVALENCE_QUALIFIED`;
- no claim that source bytes ran;
- no claim that A/B/C ran;
- no I05 claim;
- no measured P2X claim.

## Later court order

1. canonical filename + SHA freeze;
2. exact native SAV reader/config freeze;
3. R35 applicable-edge physical expectation and exact-source whole-source receipt;
4. freeze one LAT2011 source-specific realization identity;
5. bind exact physical carriers to that owner without inference;
6. execute T01-T14 candidate-neutrally;
7. start/compare A/B/C under one semantic owner;
8. require common terminal replay/semantic result without weakening physical prerequisites.

## Current execution boundary

No synthetic tests were executed by this worker.

No canonical source bytes were opened.

No real source processing occurred.

No A/B/C candidate ran.

No I05 ran.

No measured P2X ran.

Current status remains:

`TESTS_AUTHORED__NOT_EXECUTED`
