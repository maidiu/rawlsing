# RABOCHII SUB-VOZHD E — OBL060 BOUNDED REPAIR R2 — COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E3 / OBL060 — CONTACT-WITNESS-INDEPENDENCE R2 BOUNDED REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl060-contact-witness-independence-bounded-repair-r2`

EXACT STARTING HEAD:
`0fa24d2eec0dea8257b975b2ef357b6adbc716a1`

IMMUTABLE FAILED R1 CANDIDATE:
`996e89a1c44317174733d182f30208af5173126b`

R1 HOSTILE TERMINAL:
`FAIL__FROZEN_OBL060_CANDIDATE_ACCEPTS_BOOLEAN_AS_INTEGER_TIMESTAMP`

## Read first

Read and obey exactly the Sub-Vozhd E campaign charter, initial flight state, the OBL060 R1 candidate/court/hostile-review/return packet, and the campaign-wide orchestration law.

## Exact defect to repair

The R1 candidate validates receipt timestamps with Python integer checks that accept `bool` because `bool` is a subclass of `int`. Consequently malformed inputs such as `issued_at_epoch=True` can be accepted rather than failing closed.

## Exact objective

Produce the smallest R2 repair that requires exact integer timestamp types while explicitly rejecting booleans for every receipt-time input governed by this authority, while preserving all R1 semantics and non-ownership boundaries.

The R1 candidate is immutable history. Do not amend, rewrite, or relabel it as passing.

Freeze a NEW R2 candidate identity and commit.

## Bounded repair law

Use exact-type validation or an equivalently explicit contract such that booleans cannot satisfy integer timestamp requirements. Make only directly necessary code, test, evidence, and version-identity changes.

Do not broaden timestamp coercion. Strings, floats, booleans, arbitrary numeric-like objects, or custom `int`-convertible objects must not become valid timestamps unless the already-governed contract explicitly authorizes them. Preserve the intended valid integer domain and all stale/future/window semantics.

## Governed bounded court

Run a governed bounded court for the new R2 candidate. Preserve all material R1 court coverage and add explicit regression attacks for at least:

- `issued_at_epoch=True` and `issued_at_epoch=False`;
- boolean values in every other governed receipt-time field, including expiry/evaluation-time inputs where applicable;
- integers `0`, `1`, and ordinary valid epoch integers remain handled according to the existing contract;
- floats, numeric strings, subclasses/custom numeric-like objects, and malformed timestamp objects fail closed according to the existing contract;
- stale, future, inverted-window, wrong-occurrence, wrong-authority and wrong-scope receipts remain rejected;
- occurrence authority and independence source-owner identity remain distinct;
- all mandatory rejection bases and laundering mixtures remain rejected;
- the lawful `NONCURRENT_SYNTHETIC` positive control still passes only through the distinct source-owner contract;
- project-current issuance remains hard-blocked.

## Review separation

This is a repair-only role. Do NOT perform or claim the fresh independent hostile review of the new R2 candidate.

After the new R2 candidate and governed court are frozen, return them to SUB-VOZHD E. SUB-VOZHD E will commission exactly ONE fresh independent hostile reviewer for that R2 candidate.

Do not obtain a second review of the failed R1 candidate.

## Hard prohibitions

Do NOT admit/create an occurrence, become occurrence authority, create/activate an actor, issue OBL058 permission or OBL059 applicability, create ENCOUNTER, realize OEE, execute OBL055, install current-positive OBL056, or create project-current independence.

ADP-019 must remain occurrence admission authority only and must not become witness-independence authority.

No comparator, PSEPF, OBL032, architecture/topology selection, or sibling campaign work.

## Required return

Return a durable repository packet containing:

- immutable R1 failed candidate reference;
- exact smallest-defect statement;
- exact patch/diff scope;
- new frozen R2 candidate identity and commit;
- governed bounded-court identity and exact result;
- regression evidence for boolean timestamps across all governed time fields;
- explicit occurrence-vs-independence non-identity attestation;
- explicit attestation that no hostile review was self-performed;
- no-current-effect attestation;
- PASS/FAIL recommendation for commissioning one fresh R2 hostile review;
- smallest blocker if repair/court FAIL.

Terminal:

`RABOCHII_SUBV_E_OBL060_CONTACT_WITNESS_INDEPENDENCE_BOUNDED_REPAIR_R2__RETURN_FOR_INDEPENDENT_HOSTILE_REVIEW`
