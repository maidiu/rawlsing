# RABOCHII SUB-VOZHD E — OBL059 BOUNDED REPAIR R2 — COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E2 / OBL059 — DIRECT POSITIVE APPLICABILITY R2 BOUNDED REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r2`

EXACT STARTING HEAD:
`3892f32912dba21177f9663797e3f847822f4c7b`

IMMUTABLE FAILED R1 CANDIDATE:
`8f209b52f81a5c1bf5ed158782f25f56153ac68e`

R1 HOSTILE TERMINAL:
`FAIL__OBL059_FROZEN_CANDIDATE_HOSTILE_REVIEW`

## Read first

Read and obey exactly the Sub-Vozhd E campaign charter, initial flight state, the OBL059 R1 frozen candidate/court/hostile-review/return packet, and the campaign-wide orchestration law.

## Exact defect to repair

The R1 candidate correctly recognizes some malformed required bindings as malformed, but its negative-receipt path then attempts to JSON-hash the malformed packet. Non-JSON-serializable values such as `bytes`, `set`, or arbitrary objects can cause `json.dumps()` to raise `TypeError` instead of returning a fail-closed negative receipt.

## Exact objective

Produce the smallest R2 repair that eliminates that defect while preserving the commissioned OBL059 semantics and all R1 non-ownership boundaries.

The R1 candidate is immutable history. Do not amend, rewrite, or relabel it as passing.

Freeze a NEW R2 candidate identity and commit.

## Bounded repair law

The repair may change only what is necessary to guarantee that malformed/non-serializable binding inputs fail closed without an uncaught serialization exception, plus directly necessary tests/evidence/version identifiers.

Do not broaden accepted input classes merely to make hashing work. Do not coerce malformed objects into semantically valid bindings. Do not silently stringify arbitrary objects and then treat them as valid.

A malformed input may yield a bounded negative receipt only if the negative receipt itself can be constructed safely and deterministically without depending on unsafe serialization of the malformed raw object. Otherwise fail closed through the candidate's governed error contract. No uncaught generic `TypeError` is acceptable.

## Governed bounded court

Run a governed bounded court for the new R2 candidate. Preserve all material R1 court coverage and add explicit regression attacks for at least:

- `bytes` in each required binding position where applicable;
- `set` values;
- arbitrary non-serializable objects;
- nested non-serializable malformed values if the contract permits nested structures to reach validation;
- malformed values that implement misleading `__str__`/`__repr__` behavior;
- confirmation that malformed inputs do not become positive applicability by normalization/coercion;
- confirmation that valid NONCURRENT_SYNTHETIC positive and negative controls retain R1 semantics;
- project-current issuance remains hard-blocked.

All malformed cases must be deterministic fail-closed outcomes, not uncaught serialization crashes.

## Review separation

This is a repair-only role. Do NOT perform or claim the fresh independent hostile review of the new R2 candidate.

After the new R2 candidate and governed court are frozen, return them to SUB-VOZHD E. SUB-VOZHD E will commission exactly ONE fresh independent hostile reviewer for that R2 candidate.

Do not obtain a second review of the failed R1 candidate.

## Hard prohibitions

Do NOT create/activate an actor, execute ADP-008, admit ADP-019 occurrence, own OBL058 permission or OBL060 independence, create ENCOUNTER, realize OEE, execute OBL055, install current-positive OBL056, or create project-current applicability.

No comparator, PSEPF, OBL032, architecture/topology selection, or sibling campaign work.

## Required return

Return a durable repository packet containing:

- immutable R1 failed candidate reference;
- exact smallest-defect statement;
- exact patch/diff scope;
- new frozen R2 candidate identity and commit;
- governed bounded-court identity and exact result;
- regression evidence for the hostile defect;
- explicit attestation that no hostile review was self-performed;
- no-current-effect attestation;
- PASS/FAIL recommendation for commissioning one fresh R2 hostile review;
- smallest blocker if repair/court FAIL.

Terminal:

`RABOCHII_SUBV_E_OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R2__RETURN_FOR_INDEPENDENT_HOSTILE_REVIEW`
