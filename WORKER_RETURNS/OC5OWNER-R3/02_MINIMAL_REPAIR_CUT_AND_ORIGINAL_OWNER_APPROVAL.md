# OC5OWNER-R3 — minimal repair cut and original-owner approval

**OWNER_DECISION_REQUIRED — NO POLICY ISSUED.** These six binary propositions are *candidate rules for the competent original owner to decide*, not analyst-issued contracts. Each needs owner identity, competence, source/grant SHA, scoped effective date, exception/legacy decision, distinct reviewer and separate protected HQ CAS.

## Six explicit owner YES/NO decisions

| Decision | YES proposition (not yet approved) | If NO, owner must supply |
|---|---|---|
| **D1 / A6 — 11 cases** | At both capsule_envelope_commitment and EscrowState.commit reject identity fields of wrong type *before* hash/state mutation. Candidate schema: nonempty str schema_version/digests, non-bool int version >=1, finite positive non-bool real freeze_timestamp, owner-selected TypeError/ValueError; all 18 fields still bind signed commitment. | Exact types/ranges, digest syntax, serializer/version, freeze units, exception class, explicit legacy migration. No default=str identity coercion by fiat. |
| **D2 / A1 — 10** | Reject more than one raw key mapping to a single normalized allowed key in top/public map, including fullwidth/CGJ/accented variants; LeakageError. Keep canonical generated packet valid. | Canonical-only vs single-alias policy, normalization table/version, exact nested scope and denial type. |
| **D3 / A2 — 6** | Accept a finite/version-pinned confusable token threat map for specified Cyrillic/Greek/Armenian leak-token substitutions; deny owner-adopted cases with LeakageError while preserving benign multilingual words. | Which six exact values count as protected tokens (mixed-script case requires separate judgment), codepoints, token-boundary/false-positive policy or explicit deferral. |
| **D4 / A3 — 18** | Check both signature arguments are actual MockSignature before any attribute access; malformed primary/second raises SignatureError. Valid same-person/conflicting roles still ConflictError. | Owner-approved typed alternative, structural external-signature adapter and exact precedence; no implicit duck-typing. |
| **D5 / A4 — 1** | Non-Role signature role, including plain string 'CUSTODIAN', raises SignatureError at require_second_signature; no silent enum conversion. | Legacy enum conversion, exception distinction at direct MockSigner constructor vs dual gate, role-conflict ordering. |
| **D6 / A5 — 3** | After existing capsule/ledger checks, non-string/empty/unhashable holder raises IdentityMismatchError before holder_roles.get, without state change; valid fixture authorization remains separate. | Precise holder namespace and legacy hashable identifiers, exception and invalid-capsule precedence. |

For D1–D6 separately: `YES [ ] NO [ ]`; `ORIGINAL_OWNER_NAME [UNKNOWN]`; `COMPETENCE_AND_OWNER_GRANT_SHA [NONE_FOUND]`; `VERSIONED_POLICY_REF [PENDING]`; `LEGACY_DECISION [PENDING]`; `DISTINCT_REVIEWER [NOT_ASSIGNED]`; `HQ_CAS [HELD]`. Neither GitHub repo admin, this worker, OC4 patch author, OC5 author nor OC5E reviewer is automatically the original issuer.

## Minimal future implementation sequence

1. **A6 first — highest-risk acceptance bypass:** original custody_protocol.py blob af2b7e943018077cb36808b5af1cd67704624bec, lines 160–179 (CustodyCapsule), 366–380 (canonical envelope), 426–441 (EscrowState.commit). Centralize owner-versioned type/serialization validation before any signature/commit/seal/journal state. Preserve valid frozen capsule and signed all-18-field identity.
2. **A1:** same module lines 640–707. Count normalized mapping keys before recursive scanning; preserve exact generated packet schema and wrong-type denial.
3. **A2:** same lines; only add explicitly adopted finite confusable rules; do not claim arbitrary semantic non-leakage from a lexical scanner.
4. **A3/A4/A5:** lines 566–605, 113–121 and 443–457; typed boundary denials, no new acceptance, no removal of the full capsule or role separation.

Only a **new** qualified implementer on an isolated branch may author these after policy. No edits to OC4 author source, OC5/OC5E original tests, source-native survey, PR514/516/519/521, PRE-MAIN/main or owner CAS.

## Exact candidate acceptance — original sourcefree entrypoints

Original module: WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py at 0caaec590f6a8bf6744f22dc9c948c5fe233bc94, blob af2b7e943018077cb36808b5af1cd67704624bec, reported SHA256 447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a.

Frozen test: WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/tests/test_oc5e_native_hostiles.py at 67a4f1561cdad40192f00797d66b24fc4cd91589, blob 9837579ebb5b2fbf3a41c967e584a166786e46b9, reported SHA256 a9faf7ace27d0f3f3cfd1102de5c6c8d6888c12f16c7bbdde8b32bb232b84512.

Use the independent reviewer's frozen full import closure manifest, WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/freezes/01_STAGED_SOURCE_MANIFEST.json, and verify Git blobs before execution. The original runner's exact per-court command family, relative to a staged source/ directory, is:

```sh
export PYTHONPATH="$PWD" PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
python3 -m pytest -q test_custody_hostiles.py test_positive_lifecycle.py test_ocr1_independent_hostile.py test_oc2_regressions.py test_oc3_independent_hostile.py --tb=line --import-mode=importlib -p no:cacheprovider --junitxml=inherited_131.xml
python3 -m pytest -q test_oc4_repair_controls.py --tb=line --import-mode=importlib -p no:cacheprovider --junitxml=oc4_new_36.xml
python3 -m pytest -q test_oc5e_native_hostiles.py --tb=line --import-mode=importlib -p no:cacheprovider --junitxml=oc5e_native_hostiles.xml
python3 -m pytest -q test_oc5_prior_predictions.py --tb=line --import-mode=importlib -p no:cacheprovider --junitxml=oc5_prior_predictions.xml
```

These commands are future candidate tests, **NOT_RUN by OC5OWNER**. Original recorded 131=121P/10R, 36=36P, 159=110P/49R, 23=16P/7R, total 349=283P/66R, zero errors/skips. Preserve original JUnit and all ten historical REDs, seven earlier prediction REDs and 110 current PASS observations in complete per-case records; never change source assertions, xfail, skip or manufacture an expected green.

| Repair | Concrete pre-existing normative test node to execute | Mandatory acceptance and counterexample |
|---|---|---|
| A6 | test_oc5e_native_hostiles.py::test_capsule_identity_field_types_must_be_validated (11 parametrizations) | Each bad type typed-refused *before any committed/seal/ledger/event changes*; valid full capsule pair/18-field tamper controls remain live. |
| A1 | ::test_normalization_equivalent_allowed_field_alias_must_be_refused (10) | Collision LeakageError; generated packet and wrong-type/extra-key controls preserve accurate results. |
| A2 | ::test_confusable_leak_token_substitution_must_be_flagged (6, owner per-case scope) | Owner-adopted tokens refused; test_genuinely_different_confusable_string_is_correctly_admitted and benign controls survive. |
| A3 | ::test_malformed_signature_object_must_fail_typed (18) | Both positions and all nine wrong types SignatureError, valid pair remains bound, valid conflicts remain ConflictError. |
| A4 | ::test_non_enum_role_string_must_fail_typed (1) | Non-enum role typed refusal without converting string to valid role. |
| A5 | ::test_unblind_unhashable_holder_must_fail_typed (3) | IdentityMismatchError, unchanged escrow state; legal sourcefree holder still unblinds and journals. |

A precise focused invocation (after staging the actual import closure) is:

```sh
python3 -m pytest -q test_oc5e_native_hostiles.py::test_capsule_identity_field_types_must_be_validated test_oc5e_native_hostiles.py::test_normalization_equivalent_allowed_field_alias_must_be_refused test_oc5e_native_hostiles.py::test_malformed_signature_object_must_fail_typed --tb=line
```

## Frozen positive controls, observed-hole trap and prospective additions

Do not weaken the **36 OC4 author controls**, all 18 capsule fields bound to the envelope, full-capsule mock signer positive, authorized purposes, clone/ID/arm refusals, escrow event tamper detection, no premature commit/release, and generated visible/coder packets. The valid fixture is TEST_ONLY and has a publicly derived signing secret.

The frozen OC5E file also asserts old behavior in tests named test_alias_holes_are_observed_not_theorised, test_confusable_holes_are_observed_only_for_nfkc_invisible_scripts, test_malformed_signature_holes_are_observed_as_attributeerror, test_non_enum_role_string_hole_is_observed_as_attributeerror, test_unblind_unhashable_holder_hole_is_observed_as_typeerror (3 variants), and test_capsule_identity_field_type_hole_is_observed. Correct repair makes some currently passing before-state witnesses RED. Preserve these literal snapshots; add a new **versioned** post-policy suite, frozen before candidate output, and record all before/after changes separately. The preexisting generated-packet positive also contains an inert conditional expression; a newly authored test must rely on its actual later packet assertions, not the inert expression, per proof-integrity law.

Prospective owner-approved names and assertions:
- test_a6_reject_before_state_mutation: deepcopy escrow before each of 11 wrong-type commits; assert typed refusal and exact equality of committed, seals, ledger, event proofs and sequence, and typed refusal from capsule_envelope_commitment. Verify valid pinned canonical envelope across fresh processes after serialization is issued.
- test_a1_alias_collision_detected_before_release: all ten frozen variants fail as owner specifies; generated public/coder inputs remain accepted; one-key normalized behavior follows explicit D2.
- test_a2_confusable_scope_and_benign_boundary: approved finite token/codepoint table yields deterministic yes/no for each of six, including mixed-Cyrillic and benign controls.
- test_a3_a4_full_capsule_typed_signature: malformed objects/role string typed-fail, valid distinct role pair passes, same-person valid role conflicts and content-only signatures remain refused.
- test_a5_unblind_wrong_holder_no_mutation: list/dict/set and scalar/blank holder fail typed with unblind/ledger unchanged; valid issued fixture holder still works.
- test_direct_guard_fault_injection: remove just the new source validator/normalization check, keep tests unchanged, and demand an assertion-level RED on the corresponding named test in a fresh process; restore source. A later C12/BP4 integration claim additionally requires direct producer→reader→real-consumer severance, not coincident parallel outputs.

No future **159/159** or **349/349** forecast is made; original historic-observation tests and the ten inherited REDs prevent a truthful blanket green. Owner decisions, independent negative causality, real native permission, source material and original first consumer are distinct gates.

**Owner receipt status:** policy signer UNKNOWN; all six choices UNANSWERED; scientific/source/actor grants HELD; new implementer NOT_LAUNCHED; original source and test SHAs frozen; independent reviewer NOT_ASSIGNED; QF2/PR/CAS STOP.
