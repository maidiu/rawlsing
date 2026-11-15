# V553-P2 — Exact Sparse Key and Observation Core

**Launch status:** `BLOCKED_BY_P1_ACCEPTANCE`

## Mission

Promote the exact sparse V553 path to canonical semantic authority for `TEMPORAL_KEY` and `TEMPORAL_OBSERVATION`, with strict V552J↔V552 fact/scope coherence, finalized source/wave identity preservation, and the accepted TD-R00 terminal reference contract.

## Base law

Read, in order: the V553 implementation ruling; TD-R00 `RESULT.md` + `RESULT.json`; S00.5 result; S00 ruling; P1 accepted result; finalized upstream identity contract.

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
- **TD-R00 amendment:** freeze and implement `GOVERNED_STRUCTURAL_REFERENCE_SET` as a required field/reference contract, not a fifth semantic family.
- **TD-R00 amendment:** separate `identity_basis_refs` from `contextual_terminal_refs`; contextual terminal refs may survive without silently changing temporal-key identity unless governed comparison authority says they are identity-defining.
- **TD-R00 amendment:** preserve exact relation-axis, source/driver-position, target/receiving-position, structural-channel, semantic/directionality/position/use authority refs and inherited relation/incompatibility refs where supplied upstream.
- **TD-R00 amendment:** preserve 0..n role-qualified finite-stratum refs without forcing singular cardinality; preserve generic Horizon refs separately; explicit `absolute_horizon_authority_refs` may be populated only from governed designation authority.
- **TD-R00 amendment:** carry `reference_contract_version` and exact producer/association lineage so later stages can reach original authority rather than rematch labels.

## Proof required

- V552J authorizes fact A while direct V552 exposes conflicting fact B → hard fail, no rematch.
- stable key identity across compatible waves;
- key identity changes or comparison blocks when governed identity-basis authority differs;
- contextual-terminal-only ref differences do not silently alter key identity absent governing rule;
- exact nonblank source/wave UID propagation where required;
- one exact fact per observation;
- measured zero remains zero and is not gap/absence;
- readiness/probe scores cannot populate structural pressure;
- multi-valued governed stratum refs survive cardinality-preserving;
- explicit absence of Absolute-Horizon designation remains empty/absent rather than inferred;
- structural direction refs survive independently of any later temporal-delta direction.

## Prohibited

- no relation/delta completion beyond what is necessary to keep code compiling;
- no aggregate projection redesign;
- no V554 consumer changes;
- no invented qualitative thresholds or event causation;
- no stratum/Horizon assignment or cross-key conflict derivation.

## Return

Write `RESULT.md` and `RESULT.json` in this packet cell, commit to the P2 branch, and open a draft PR to the V553 completion integration branch. Return head SHA, PR, tests, changed files, and any cross-hook.