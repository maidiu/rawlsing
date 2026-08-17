# V553-P2 — Exact Sparse Key and Observation Core

**Launch status:** `BLOCKED_BY_P1_ACCEPTANCE`

## Mission

Promote the exact sparse V553 path to canonical semantic authority for `TEMPORAL_KEY` and `TEMPORAL_OBSERVATION`, with strict V552J↔V552 fact/scope coherence and finalized source/wave identity preservation.

## Base law

Read the V553 implementation ruling, S00.5 result, S00 ruling, P1 accepted result, and finalized upstream identity contract.

## Authorized terrain

Primary:
- `data/ddm_build_copy/ddm_v553_temporal_pressure.py`
- `data/ddm_build_copy/ddm_v553_schema.py`
- `data/ddm_build_copy/compile_v553_temporal_pressure_field.py`
- focused sparse temporal contract tests

Do not alter V552/V552J producer semantics.

## Required outcomes

- Require every admitted V552J candidate to resolve to the exact referenced V552 fact in the same governed scope; mismatch fails closed.
- Never search for or substitute a different V552 fact after V552J admission.
- Carry V552 structural fact ID, V552 temporal-key-source lineage, V552J association/admission lineage, canonical source/country/wave/year identity, and governed source/wave UIDs where applicable.
- Form stable wave-independent exact temporal keys from governed structural identity, never synthetic `shared_*` or country:year labels.
- One authoritative observation must reference one exact V552 structural fact and copy its structural pressure value/status.
- Preserve measured zero as an observed value.
- Represent missing/blocked/noncomparable states separately; do not create semantic values for them.
- Make sparse key/observation schemas explicitly primary.

## Proof required

- V552J authorizes fact A while direct V552 exposes conflicting fact B → hard fail, no rematch.
- stable key identity across compatible waves;
- key identity changes or comparison blocks when governed structural identity differs;
- exact nonblank source/wave UID propagation through key/observation lineage where the finalized contract requires it;
- one exact fact per observation;
- measured zero remains zero and is not gap/absence;
- readiness/probe scores cannot populate structural pressure.

## Prohibited

- no relation/delta completion beyond what is necessary to keep code compiling;
- no aggregate projection redesign;
- no V554 consumer changes;
- no invented qualitative thresholds or event causation.

## Return

Write `RESULT.md` and `RESULT.json` in this packet cell, commit to the P2 branch, and open a draft PR to the V553 completion integration branch. Return head SHA, PR, tests, changed files, and any cross-hook.