# GT34 OBL056 — INDEPENDENT HOSTILE ATTACK MATRIX R1

Status: `FROZEN_BEFORE_A1_FOCUSED_TEST_RATIONALE_REVIEW`

Profile: `HOSTILE_AUDIT`

Frozen working ancestry: `658fcd191546c8d3f4918e0bf34b3840e6d518b4`

Frozen semantic target: `966aea1a42b30840670f4b69f779999bfd4a2307`

A1 final tip (target identity only): `3960b0e021ae2b145345d060cca295dcaf4bae03`

Frozen grain: `IS_EXACT_AUTHORITY_X_ACCEPTED_FOR_ROLE_R_FOR_ADP010_CONSUMER_SCOPE_S?`

Exact consumer: `V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`

Required roles: `CAUSAL_USE_PERMISSION`, `POSITIVE_APPLICABILITY`, `CONTACT_OCCURRENCE_WITNESS`, `CONTACT_WITNESS_INDEPENDENCE`.

Current-positive registry count: `0`; empty is lawful and must fail closed. Synthetic positives are lawful only as `NONCURRENT_SYNTHETIC_TEST_ONLY`.

## Independence statement

This matrix was derived before consuming A1 focused-test rationale in detail, from the hostile-review handoff, frozen HQ/W4 defect boundary, A1 candidate authority/receipt artifacts, and the frozen candidate module. It deliberately does not rely on A1's test names, test commentary, or implementer rationale.

## Attack matrix

| # | Attack | Independent hostile proposition / required result |
|---:|---|---|
| 1 | Caller-selected authority ID/version/hash/currentness self-issuance | Caller-shaped identity plus recomputed hashes must not create acceptance. |
| 2 | Forged/recomputed registry-entry identity | Recomputed entry ID/hash without exact competent membership must fail. |
| 3 | Forged/recomputed receipt identity | Recomputed receipt ID/hash alone must not create competence. |
| 4 | Receipt-body mutation + attacker rehash | Mutation plus a correct new content hash must still fail absent exact registry authority. |
| 5 | Issuer/registry substitution | Alternate acceptance-authority or registry refs must fail. |
| 6 | Absent registry membership | Well-formed receipt with no exact positive entry must fail closed. |
| 7 | Duplicate/ambiguous membership | If constructible, non-unique exact membership must fail closed rather than select arbitrarily. |
| 8 | Accepted-authority ID mutation | Must fail or require a separately competent exact entry. |
| 9 | Accepted-authority version mutation | Must fail or require a separately competent exact entry. |
| 10 | Accepted-authority content-hash mutation | Must fail or require a separately competent exact entry. |
| 11 | Role mutation | Must fail; role relabel cannot inherit competence. |
| 12 | Consumer mutation | Must fail exact-consumer binding. |
| 13 | Transition/use-scope mutation | Must fail exact transition/use scope binding. |
| 14 | Family/subject/object-scope mutation | Each scope axis must be exact-bound and fail on mutation. |
| 15 | Owner/jurisdiction evidence mutation | Must fail exact owner/jurisdiction evidence binding. |
| 16 | Source acceptance/adoption/current-selection evidence mutation | Must fail exact source acceptance evidence binding. |
| 17 | Negative/limit reference mutation | Must fail exact limits binding. |
| 18 | Provenance mutation | Must fail immutable provenance binding. |
| 19 | Currentness mutation | Synthetic/current flipping plus rehash must not upgrade competence. |
| 20 | Decision-state mutation | Nonpositive/mutated decision must fail. |
| 21 | Receipt ID/hash mutation | Any mismatch must fail integrity; valid rehash still must not create authority. |
| 22 | Cross-role receipt reuse | Receipt valid for one role must not satisfy another. |
| 23 | Same accepted authority for contact occurrence + independence | Pair must fail even with distinct receipt identities. |
| 24 | Same receipt for contact occurrence + independence | Pair must fail. |
| 25 | Role relabel + rehash | Rehashing a relabeled role must not confer acceptance. |
| 26 | Synthetic issuer relabeled current | Must fail. |
| 27 | Synthetic registry relabeled current | Must fail. |
| 28 | Synthetic receipt currentness flipped + rehashed | Must fail. |
| 29 | Synthetic accepted authority copied into current-shaped receipt | Must fail current acceptance. |
| 30 | No-current-entry/no-receipt fail-closed | Current path with zero current entries must reject with no fallback. |
| 31 | Future current-adoption operability | Contract must be able to represent and validate a future exact HQ-adopted/current positive entry without redesigning semantic authority after adoption. Static hostile hypothesis: candidate code contains an unconditional `required_currentness == CURRENT_ACCEPTED` rejection and `_CURRENT_ENTRIES` is permanently empty; test whether adoption would freeze an unusable current contract. |
| 32 | API composition/bypass | `validate_contact_acceptance_pair` or any helper must not substitute for validating each constituent receipt. |
| 33 | Authority/registry/entry/receipt content-address recomputation | Independently recompute domain-separated canonical hashes and compare exact constants/fixtures; caller recomputation must remain only integrity, not competence. |
| 34 | Canonical ordering/NFC/replay/idempotence | Key order/NFC equivalence should canonicalize deterministically; repeated validation must not mutate or mint authority. |
| 35 | Candidate-to-evidence compatibility | Evidence execution delta beyond semantic target must be proof-only and target the exact candidate/module/artifacts. |
| 36 | Authority-ceiling escape | Candidate must create none of causal-use truth, applicability truth, contact occurrence/independence, encounter, exposure, external-event admission, generic project-wide authority, comparator, PSEPF, metabolism, CAN-008, V2, or positive-V3 actor mutation. |

## Critical static hypotheses to prove/refute independently

1. **Future-current operability risk:** the frozen module defines `_CURRENT_ENTRIES=()` and unconditionally raises `AcceptanceMissingAuthority` whenever `required_currentness == CURRENT_ACCEPTED`, before any current-entry lookup. If no separately data-driven/adoptable current registry surface exists, adoption would freeze a contract that cannot ever validate a future current positive without code redesign.
2. **Composition risk:** `validate_contact_acceptance_pair` visibly checks only pair distinctness/roles; hostile tests must prove whether unvalidated caller-constructed receipts can pass this helper. A helper is lawful only if it is not usable as a substitute for constituent receipt validation.
3. **Integrity-vs-competence distinction:** content-address recomputation must prove tamper detection, not mint acceptance.

No defect is repaired by this worker. A reproduced adoption blocker yields an exact `FAIL__GT34_OBL056_...` terminal even if the hostile court itself is green because it successfully reproduces the defect.
