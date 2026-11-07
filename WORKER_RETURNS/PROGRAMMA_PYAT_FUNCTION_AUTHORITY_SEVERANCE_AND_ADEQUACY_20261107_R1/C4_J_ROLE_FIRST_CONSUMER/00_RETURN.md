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

A non-test producer/caller was **not found**: the only non-test occurrences are the definitions in `pre553_j_role_certification.py`. O14 is caller-supplied only. The seven named sourcefree tests exercise the mechanism, not a selected original issuer.

Historical F17 semantics include dynamic `family_cfg.item_role_groups` roles/order, `target_resolution_rules`, `boundary_rules`, `response_role_rules`; F19 runs `compile_v550j_family_tables`; F20 verifies V550J manifest/readiness and writes typed stops; F21 performs structural handoff. O14 uses a fixed six-token role vocabulary and M1 role certification. This is **narrower** and not proven equivalent to the historical family/order/target/measurement semantics.

## INTERPRETATION

- **Historical selection status:** `STATIC_CALLSITE_ONLY`, not `HISTORICAL_SELECTION_PROVED`.
- **Current O14 status:** `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED`.
- **Historical J verdict:** `STATIC_CALLSITE_ONLY__HISTORICAL_SELECTION_UNPROVED`.
- No proven severance, no proved equivalence, no global absence, no blanket demand gate.
- The current generic mechanism may be adequate for an actual current operation, but no actual non-test producer/consumer or selected operation demand is established. This is a precise provenance/demand limit, not an arithmetic-mechanism failure.
- Old-version/shadow/revocation original behavior is `NOT_RUN__NO_SELECTED_J_RELEASE`.
- F21/M3 structural work is a potential C3 handoff only; no overlap or merge was performed.

## ACTION

No production build. Preserve current O14 mechanism and all four historical IDs/source pins.

Minimal owner action: establish an actual non-test producer/first consumer and a selected original J release/operation demand, or confirm that the current generic O14 operation is the intended current use and does not require the historical dynamic family/target/boundary/measurement registry. If demanded, route the exact selected release through the existing O14/M1 ABI; otherwise retain UNPROVED and do not restore old private caches/compilers.

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
