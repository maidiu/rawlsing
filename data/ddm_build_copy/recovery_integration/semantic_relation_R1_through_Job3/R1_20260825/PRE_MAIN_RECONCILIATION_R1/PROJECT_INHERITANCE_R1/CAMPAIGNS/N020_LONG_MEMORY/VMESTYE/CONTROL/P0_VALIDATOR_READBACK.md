# ZL-00 P0 validator static readback and negative-control expectations

**Source inspected:** `validation/validate_vmestye.py` at original protected PRE-MAIN `0f4a446af12896aa742c42d5ff06e9222cc378cc`, still the same file blob at refreshed protected `2162d85db5e6822707e5cdff7aac2656ebef4761`, Git blob `fb39e939ef4bdd21e52bce78d5a50825317acc6f`; its `validation/README.md` read at blob `d584786561dbc093b0411572c22ad962460fb1e1`. This is a **static S0–S1 code/readback**, not an executed Python test.

**Runner decision:** `AUTHORIZED_S2_RUNNER_NOT_INDEPENDENTLY_VERIFIED`. This session has authenticated GitHub source access but no independently established right to claim its scratch executor is a qualified project S2 runner, nor an authenticated local mainMac/source-native environment. **Python validator: NOT_RUN. Deliberate negative mutations: NOT_RUN. CI: NOT_RUN by this worker. S3/source-native: NOT_RUN.** Do not convert our deterministic connector-side source parsing into a test receipt.

## What the unchanged bootstrap validator actually enforces

| Static guard read in script | Deterministic connector-side source observation | Ceiling |
|---|---|---|
| Pinned Git blobs of five projected seed TSVs | Protected blobs `f09548a0`, `e9aece88`, `d571847a`, `49513d30`, `cf644642`; direct source D01 44/30 IDs and C6 94 row-type partition matched projection IDs | Source identity/byte drift contract, not complete field-semantic equivalence |
| Exact LMX 44 / LMQ 30 / F 29 / AR 58 / auxiliary 7 | Read 44/30 unique D01 first-column IDs and distinct C6 `ROW_TYPE+ID`: 29 FUNCTION, 58 RELEASE, 6 DENOMINATOR, 1 CROSSREF; source primary blobs `f1252e90`, `f6d4c7b6`, `ba39d8f9` | Documentary parsing only |
| Atlas 73 seed identities & `NOT_ASSESSED_CURRENT` | Atlas source file inspected; baseline currentness cells remain not assessed at protected cut | Seed count cannot determine unique semantic functions |
| 30 RM locators, corrected RM09/23/24/30 | Exactly RM01..RM30 distinct, with 2 short unresolved historical cut locators; corrected values retained | Locator coverage, no per-function current join |
| SR-01 2,416/1,314 counts and statuses | Worker returns and source count manifest read; both branch HEADs equal pin; class tallies sum to claimed row count. Large JSONL source bodies came back empty through this connector while blob identities were returned | **No ZL-00 exact manifest ID anti-join** |
| Sorok 304/144/100/38/83, 48 unread bodies | Underlying Sorok source registers directly parsed and uniqueness checked; exact 48 IDs are a subset of 304 asset IDs | Not science, actor or current first consumer |
| 18 `NOT_DISPATCHED` flights and 9 `NOT_RUN` phase gates | Protected pre-dispatch snapshot read; **ZL-00 is now user-dispatched**, so the flight-board snapshot is historical, not live execution state | Validator must be versioned before it can attest live dispatch |
| Required prong landing/table files | Static path-existence assertions read; not exercised in an authenticated project runner | Not an independent P0 acceptance |
| Required no-drop and source acceptance beyond bootstrap | The script **does not** check every original 2,416/1,314 composite manifest key against source registries, all 55/R157/PROG/Sorok actual links, or semantic/authority/consumer equivalence | ZL-01 and #799 independent court required |

## Falsifier examples (expected outcomes from code inspection; NOT executed)

| Mutation / counterexample | Expected observed validator behavior if run | Missing additional P0 invariant |
|---|---|---|
| Change one byte in `DATA/LMX44_SEED.tsv` | `frozen seed source-content drift` | Recheck source meaning, not only blob |
| Duplicate `LMX-001` and omit `LMX-044` | duplicate / exact-set mismatch | Same-grain semantic duplicates and aliases must remain distinct |
| Remove `RM24` | 30-record `exact_ids` mismatch | Sorok underlying branch/source assets not yet joined |
| Alter Pyat SR-01 class total or mark `INDEPENDENT_REVIEW=PASS` | source count/status contract mismatch | Exact 2,416 IDs not presently read from large manifest |
| Remove one of 48 index-only Sorok bodies from semantic queue but keep count metadata | **May pass bootstrap** | Explicit 48-element anti-join and `INDEX_ONLY` state at ZL-01 |
| Flip F03 `rule_applied` claim to true with only an authority hash | **May pass bootstrap** | Require real selected rule → output mutation → first reader and refusal |
| Make conditional seam predicate unconditional | **May pass bootstrap** | Compare all IF/MUST predicates and reverse reachability |
| Mark ZL-00 `ACTIVE_VERIFIED` in original `CONTROL/FLIGHT_BOARD.tsv` | Validator's all-18-`NOT_DISPATCHED` static rule will fail | Evolve validator to stage-aware `USER_DISPATCHED` + immutable session/return evidence, preserving old snapshot |
| Drop a record from the large SR-01 manifest while maintaining source count field | **May pass bootstrap** | ZL-01 exact composite-key source-to-return anti-join |
| Treat `fdda84750` or `76392135` as validated 40-hex immutable commits | **May pass bootstrap** | Expand/verify short RM14/RM15 locators or record UNRESOLVED_SHORT_SHA |

**No negative-control execution result is claimed.** The table states control-flow expectations from the actual script. The independent reviewer must run the exact checker and deliberately corrupted fixtures on a genuinely authorized S2 runner, capture exit codes/stdout/stderr and source SHA, and check that the stage-aware revised validator does not silently erase real worker dispatch. If no eligible runner is available, the gate remains `NOT_RUN`; documentary static readback is not an alternative PASS.

## Exact P0 acceptance blockers left for ZL-01 / #799

1. Retrieve the **actual** Pyat 2,416 and Sorok 1,314 JSONL bodies through an authorized readable surface; verify every composite source key, category, 1,310+4 Sorok override split, and no-drop against pinned source members. ZL-00 observed Git blob identities only.
2. Complete exact source-key inventory for historical 49 GAP, 11 sections, 35 R157 sources and full 30 RM underlying branch/currentness links, including short RM14/15 cuts.
3. Preserve #777 25 source-authority-unproved + 30 NOT_RUN, FIABC 144/3 red, R5C F14 D2 REPAIR, PR #786 draft/nonprotected, and paused-commission stops as typed negative evidence.
4. Have independent P0 receiving #799 test schema widths, alias collisions, status ceilings, actual branch leases, row-by-row source fidelity, conditional reachability and no-drop; **ZL-00 author may not self-accept**.
5. Version the bootstrap validator's pre-dispatch expectation before any claim of post-dispatch structural PASS.

**Return classification:** `P0_VALIDATOR_STATIC_INSPECTED__AUTH_RUNNER_UNVERIFIED__PYTHON_NOT_RUN__NEGATIVE_CONTROLS_NOT_RUN__NO_P0_GATE_PASS`.

## Independent P0R #799 D06 — stage-aware executable validation requirements (V1 contract; NOT EXECUTED)

The unchanged protected Python checker `validation/validate_vmestye.py@fb39e939ef4bdd21e52bce78d5a50825317acc6f` cannot serve as an executable P0 green for the current stage. Its 18 `NOT_DISPATCHED` test refers to the historical frozen pre-dispatch control board. Do not alter a protected snapshot to force a pass. The validated subject must be a **separate, versioned stage-aware current-flight return** pinned to each independently reviewed branch HEAD and underlying exact protected sourcecuts, not an invented update of the old snapshot.

A competent authorized validator author/runner (separate implementation and independently witnessed run, not granted to ZL-00 here) must implement and record:

1. **Frozen historical regression:** verify the original seed/status snapshot at its original source SHA with the original test, preserving 18 historical NOT_DISPATCHED and nine NOT_RUN gates; distinguish this from live execution. Baseline test result and byte-identical pinned inputs must be in runner receipt.
2. **Live stage machine:** parse actual ZL-00/ZL-01/P0R branch/head/issue evidence as `PREPARED → DISPATCHED_BY_USER → ACTIVE_VERIFIED → RETURNED_AT_SHA → INDEPENDENT_REVIEWED → ACCEPTED_TO_VMESTYE`; reject undocumented leap, branch-head drift, self-acceptance and stale review against a prior HEAD; do not require live worker status to equal old NOT_DISPATCHED.
3. **Exact census/header/foreign-key:** validate current 25-column `P0_RETURN_AND_BRANCH_CENSUS.tsv` (independent reviewer observed 6,120 rows), exact composite source tuple and collision checks, all 110 ZL-01 anti-join checks and 110 receipts, and both 2,416 and 1,314 original SR-01 manifests using exact source-grain ID set equality. No equal counts/digests alone can substitute for exact per-key anti-joins; external source bytes must be verified or be `SOURCE_UNAVAILABLE` HOLD. Reject D02–D07 per-file pointer that cannot dereference grouped estate plus source_path; reject RM negative pointer whose census estate is not `RECENT_CAMPAIGN30` plus `source_exact_id`.
4. **RM check aliases:** load `P0_ANTI_JOIN_REQUIREMENTS.tsv` canonical 30 `AJ-RMxx` and exact `P0_RM_CHECK_ID_BIJECTION_V1.tsv` 30 old/new links. Validate uniqueness, bijection and actual ZL-01 versioned use; any missing/extra/collision/unregistered replacement is failure, not 30 genuinely absent RM source rows.
5. **G4 seam predicate fidelity:** read original 82-row source JSONL at exact cut/blob and the 82-row ZL-00 predicate sidecar. Re-extract `edge_id`, `original_requiredness`, `original_predicate`, `original_G2.edge_condition`; assert 82 distinct keys, exact per-field equality and 26 IF + 2 functional IF without DAG promotion. Then match all 82 to ZL-01's independently versioned predicate-bearing receipt; absence of that receipt is `HOLD`, not PASS. Do not conflate conditional G4 seam records with 13 roadmap conditional dependency links.
6. **P1 preflight:** validate all 13 prong owners' path leases and header exactly against `VMESTYE_P1_PRONG_TABLES_V1` in `P0_SCHEMA_AND_LEASES.md`; enforce primary/foreign/source tuple keys, negatives, explicit UNJOINS and no unapproved schema migration. Executable validation is a P1 dispatch prerequisite, not a declaration that P1 writers are active.
7. **Result grammar:** `PASS|FAIL|HOLD|NOT_RUN` separately per check and sourcecut; explicit error ID, original input SHA, branch head, script SHA, runner/authorization evidence, invocation/environment, row/key/mutation counts, console transcript/artifact hash, and independent reviewer determination. `PASS` at identity is never a current scientific/functional/native PASS.

**Required deliberate negative fixtures** (only in a disposable copy, NEVER corrupt protected or active worker data): (a) omit one SR-01 composite key while retaining claimed count; (b) duplicate an RM alias/point to nonexistent estate; (c) change one `ASTRA:IF:N0:N4:0` original predicate without changing edge_id or row count; (d) flip another IF requiredness to MUST; (e) leave D02 grouped-estate file selector impossible; (f) leave RM negative selector unresolved; (g) forge live ACCEPTED_TO_VMESTYE without independent review at the same SHA; (h) change one prong table header or unresolved FK. Each must produce an exact assertion failure in qualified execution; no dry-run/static expected failure is a runtime receipt.

**Runner/actual status at this ZL-00 author correction:** independently authorized S2 implementation/run **NOT VERIFIED**; Python baseline `NOT_RUN`; stage-aware validation `NOT_RUN`; eight negative mutations `NOT_RUN`; original native S3 `NOT_RUN`. P0R D06 and P1 dispatch remain **HOLD**. Source-authoritative 6,120-row raw census body is not available to this ZL-00 connector path; do not infer 6,120 independent field-valid rows from a reviewer’s separate count.
