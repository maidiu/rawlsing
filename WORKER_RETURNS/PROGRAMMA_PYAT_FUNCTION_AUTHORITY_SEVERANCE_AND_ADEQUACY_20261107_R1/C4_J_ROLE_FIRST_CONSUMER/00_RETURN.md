# C4 — J-family role/component first consumer (O14)

**Lane:** C4_J_ROLE_FIRST_CONSUMER, issue #777.
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer`.
**Branch:** `agent/pyat777-joint-consumer-20261107-r1`.
**Base:** `b132fa4a02b31ba539b33f24ad022846bb81acb8` (C2 accepted; not reopened).
**Scope:** historical F17_J_REGISTRY / F19_J_PATTERN / F20_J_PACKET / F21_J_STRUCT vs current O14 only; no production/runtime/native/science/actor effect.

## FINDING

Historical F17/F19/F20/F21 are present as **static historical callsite/code pins only** at the F1 cut. No selected original J release is established: AR-0051 is a draft GSS registry; AR-0052/AR-0053 are rules; AR-0058 is conceptual/no current P3C release. F1 A02-AUTH-010/023 and the four function IDs remain unmatched to a selected executable release.

Current O14 is an installed generic J-role/certification mechanism:
`JFamilyRoleAssignment` / `build_j_family_item_role_vector` (`pre553_j_role_certification.py:356-388`) and `j_component_certification_validator` (`:1257-1329`).

No non-test **invocation/call-through** was found in static source: **`NONE_FOUND_IN_STATIC_SOURCE`**. This is not proof of absence. The exact M1 registration mechanism exists in non-test source: `build_j_validator_registry` (`pre553_j_role_certification.py:1018-1027`) constructs `FamilyValidatorRegistration.from_binding(binding, j_component_certification_validator)` into an exact `M1ValidatorRegistry`; `M1ValidatorRegistry.resolve_exact` has no latest/default/fuzzy/alias fallback; `compose_learned_world` accepts the caller-supplied exact registry on the M01_M1_M2_B5 route and dispatches through M1. The author's earlier constructor grep omitted this builder/bare-callable path and remains preserved as a historical incomplete search log. The seven named sourcefree tests exercise the mechanism, not a selected original issuer.

Historical F17 semantics include dynamic `family_cfg.item_role_groups` roles/order, `target_resolution_rules`, `boundary_rules`, `response_role_rules`; F19 runs `compile_v550j_family_tables`; F20 verifies V550J manifest/readiness and writes typed stops; F21 performs structural handoff. O14 uses a fixed six-token role vocabulary and M1 role certification. These are **different responsibilities**; historical equivalence is `UNPROVED`. No actual current O14 operation/demand is established that would require the full dynamic historical surface.

## INTERPRETATION

- **Historical selection status:** historical static callsite/source pins are proved; selected original release/row/version is `UNPROVED`; this is **not historical absence**. `STATIC_CALLSITE_ONLY`, not `HISTORICAL_SELECTION_PROVED`.
- **Current O14 status:** `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED`.
- **Historical J verdict:** `STATIC_CALLSITE_ONLY__HISTORICAL_SELECTION_UNPROVED`.
- No proven severance, no proved equivalence, no global absence, no blanket demand gate.
- The current generic mechanism may be adequate for an actual current operation; the registration mechanism exists, but no non-test invocation/call-through or selected operation demand is established. This is a precise provenance/demand limit, not an arithmetic-mechanism failure or proof that historical J is absent.
- Old-version/shadow/revocation original behavior remains explicitly `NOT_RUN__NO_SELECTED_J_RELEASE`; this is not an absence claim or a new authority gate.
- F21/M3 structural work is a potential C3 handoff only; no overlap or merge was performed.

## ACTION

No production build. Preserve current O14 mechanism and all four historical IDs/source pins.

Conditional owner action: if an actual non-test invocation/call-through or selected operation demands the historical dynamic family/target/boundary/measurement authority, route the exact selected release through the existing O14/M1 ABI; otherwise retain the current generic sourcefree O14 mechanism. The absence of a found static invocation is `NONE_FOUND_IN_STATIC_SOURCE`, not a mandatory original-J reinstatement or a no-demand gate. Do not restore old private caches/compilers.

## OWNER

- Current O14/M1 owner: `pre553_j_role_certification.py` + `pre553_learned_empirical_adjudication.py`.
- Historical J source/selection: original J registry/source owner and #753 B1/B5 receiving owner.
- F21/M3 potential handoff: C3 structural/M3 owner only after separate demand evidence.
- No production/test-existing/HQ/peer/original/protected writes.

## Evidence

- `01_CASES.jsonl`, `02_CASES.tsv` — A–J cases for current O14 and historical static J.
- `03_TEST_RECEIPTS.md` — commands, 7 passed sourcefree mechanism tests, source hashes, NOT_RUN.
- `04_MINIMAL_OWNER_ACTIONS.tsv` — no-build owner actions.
- `05_REGISTER_ANTIJOIN.tsv` — F17/F19/F20/F21 preserved static/unmatched; O14 and A02/AR candidates.
- `logs/pytest_j_role_o14.log`; `logs/non_test_caller_search.txt`.

## Limits

No original respondent/SAV/DTA/DB access; no selected original J release/row; no native/science/actor/current grant; no production patch; no old private cache/compiler; no whole-pipeline absence or no-demand claim. C3 FF/post-FF, Q86/T01/R9 owners untouched.
