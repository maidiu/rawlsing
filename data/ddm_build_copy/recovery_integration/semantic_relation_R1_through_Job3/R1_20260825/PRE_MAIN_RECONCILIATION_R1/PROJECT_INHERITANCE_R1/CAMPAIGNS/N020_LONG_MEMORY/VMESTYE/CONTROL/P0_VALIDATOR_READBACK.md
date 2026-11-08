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
