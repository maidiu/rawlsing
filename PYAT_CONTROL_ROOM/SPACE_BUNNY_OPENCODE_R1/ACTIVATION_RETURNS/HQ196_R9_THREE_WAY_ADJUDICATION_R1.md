# HQ196 — R9 HQ195 three-way adjudication

Status:
`R9_CONTRACT_MEANING_SETTLED__ARCHITECTURE_WARRANT_NOT_ADOPTED__BROKER_FEASIBILITY_CANDIDATE__SELECTED_READ_IMPLEMENTATION_GAP_CANDIDATE`

## Inputs

Stage/authority return:
`agent/rabochii-pyat-hq195-r9-stage-ownership-architecture-warrant-r1 @ 66929dad727410b8bfd33831cd2d8c632d5ccf4a`

Runtime feasibility:
`agent/rabochii-pyat-hq195-r9-instrumented-runtime-feasibility-r1 @ 63f10827e673a4b3c53a0a123303b2b9bb96c59a`

Independent contract review:
`agent/reviewer-pyat-hq195-r9-contract-independent-interpretation-r1 @ 6df3257c5e362947c988d3260302cef2372e0809`

## Contract meaning — accepted

HQ adopts the shared stage/independent-review interpretation:

- O1-C07 is not stage-contradictory.
- `Freeze expected budgets and instrumentation before launch; retain measured counts` deliberately separates:
  - pre-launch authorization/budget/instrumentation/basis;
  - during-run exact observation;
  - return-time retained accounting.
- `REQUIRED_EXACT_COUNT` does not mean the final observed number must already have been observed before launch.
- Literal path-level opens, reader invocations and decoder invocations are separately named/non-substitutable quantities.
- A higher-level proxy cannot simply be renamed `path_opens`.

## Architecture-warrant candidate — NOT adopted

The stage worker's architecture-warrant candidate was correct against the evidence available to it at return time: the then-known path-string runtime could not lawfully measure/enforce literal compiled-reader opens.

The parallel feasibility lane later produced a materially new fact:
- pyreadstat 1.3.6 accepts an object with `.read/.seek`;
- on that route it installs Python-bridging ReadStat handlers and supplies an empty path/no-op compiled open handler;
- the application therefore owns the path-level open;
- synthetic proof observed one application-owned path open and zero compiled-reader path opens;
- no pyreadstat binary rebuild, privilege, DYLD interposition or R7 runtime-package identity change is required.

Therefore the predicate `cannot lawfully succeed under the current runtime` is **not established for the brokered route**.

HQ does not adopt an architecture warrant while this lower-cost existing-runtime route remains viable.

This does not yet close R9. The broker finding is:
`FEASIBILITY_CANDIDATE__HOSTILE_REVIEW_AND_EQUIVALENCE_REQUIRED`

## Broker candidate — exact outstanding proof

Before adoption, independently establish:

1. the file-like route truly causes zero compiled-reader path opens;
2. the application-owned `open` is therefore the complete literal path-open account at the declared route;
3. every relevant reader call site can be brokered — no raw path-string escape remains;
4. pyreadstat version pinning makes the private/de-facto seam fail detectable rather than silently changing;
5. DTA chunk/batch operation uses a fresh broker per chunk or an equivalently correct reset law;
6. full source-free 55-carrier path-vs-broker equivalence at the prior court grain;
7. enforcement failure is loud and pre-operation;
8. R7 package/interpreter identity is unchanged, while the changed application path receives the necessary C3/C4C3 requalification.

## New candidate finding — selected-read implementation mismatch

Frozen O1-C07 operation expectations at exact freeze `8ff40d37...` state:

- SRC02: `expected_selected_reads=1`, `expected_full_reads=0`;
- SRC06: `expected_selected_reads=1`, `expected_full_reads=0`;
- SRC14: `expected_selected_reads=1`, `expected_full_reads=0`.

Exact decoder at the freeze:
`rawlsing_next/pre553_physical_decoder.py`

contains:
- no `usecols` argument;
- metadata read through `reader(... metadataonly=True ...)`;
- full compatibility read when encoding is non-null;
- `PhysicalSourceIncidence.iter_batches` calls `pyreadstat.read_file_in_chunks(reader, source_path, ...)` without a selected-column configuration.

Current control preserves the same relevant shape.

Therefore HQ records:
`R9-SEL-03_CANDIDATE_IMPLEMENTATION_GAP__HOSTILE_REVIEW_REQUIRED`

The likely issue is not merely that a selected-read COUNT lacks an owner. The current reader route appears not to perform the frozen selected-variable read operation at all.

HQ does not yet classify this as an adopted blocker until the independent review attacks the exact call path and any relevant consumers.

## DQ-01 — warrant instrument completeness

HQ accepts as a documentary finding that the later warrant candidate dropped C4B's per-source `source_access_accounting` block.

A successor instrument must restore per-source accounting and explicitly distinguish:
- frozen/pre-launch expected budget;
- measurement basis/instrumentation;
- runtime observed exact count;
- typed null/reason only where the governing law permits null.

Restoring the fields does not itself close the technical accounts and authorizes nothing.

## Next wave

1. DeepSeek hostile review of the broker candidate + selected-read call-path finding.
2. Space Bunny source-free brokered/selected-reader implementation candidate + 55-corpus requalification.
3. Space Bunny documentary warrant/accounting schema successor.

All are `SPARSE_REQUIRED`.

## State

R9 remains the sole warrant-instrument technical blocker.
Host disk policy/capacity remains the separate live-run blocker.
R7 remains closed at runtime-identity grain.
HQ182 C4 non-adoption hold remains pending reserved Astra decision.

No source access, locator discovery, warrant issuance, live C4, C7 or actor/person work is authorized.
