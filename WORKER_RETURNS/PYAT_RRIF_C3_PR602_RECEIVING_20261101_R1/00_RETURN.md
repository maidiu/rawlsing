# PYAT RRIF C3 PR602 — FINAL OWNER-CAS RECEIVING RETURN R1

**Status:** `EXACT_HOLD__ENGINEERING_RECEIVING_PASS__GOVERNED_COURT_PROOF_INTEGRITY_RED__NO_MERGE__PR602_READY_FOR_OWNER_CAS`

**One-line result:** At exact PR #602 head `273565d84dd61458254db5b1e3f7c53741b185ef`, all mandated sourcefree suites reproduce green (45/45, selected 194 pass/1 skip, hostile matrix, SAV/DTA opaque, PR526 custody, G01 same two baseline RED), and the six payload blobs exactly match the frozen allowlist. PR #602 was marked **ready** but **NOT merged**: canonical PRE-MAIN's mandatory governed-court proof-integrity gate is RED because two new integration-claim tests lack sibling `.proof.json` executable severance witnesses, and the frozen seven-path payload forbid adding them. No source, scientific, actor, G01, R9 or Sorok authority is issued.

## 1. Identity, role and execution envelope

- Role: independent PRE-MAIN receiving integrator and sourcefree regression/CAS verifier. Not E1 author, not E4F author, not E4FR reviewer, not Pyat HQ, not a scientific/actor/issuer court.
- Host: `mainMac.lan`, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Harness/model actually used: OpenCode `1.18.34`, agent `build`, session `ses_e67a22151ffeL6zCfltQuYO90k`, `providerID=opencode-go`, `modelID=deepseek-v4.1-flash`, `variant=max`, `mode=primary`. No model/provider/host/effort switch occurred.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2. Same versions as the independent E4FR review.
- Execution surface: S2 local Git, one fresh clone, detached/sparse receiving and PRE-MAIN worktrees, sourcefree synthetic pyreadstat files, no raw survey or native source execution.
- Assigned documentary branch: `agent/pyat-rrif-c3-pr602-protected-receiving-20261101-r1`, started at PRE-MAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`.

## 2. Live Git state and exact PR scope

Live reads at start and immediately before the receiving decision:

- `integration/pre-main-reconciliation-r1` (PRE-MAIN) = `8e44ca9c751049d65e6def47600b5c073ee04b29` (unchanged).
- PR #602 base = same PRE-MAIN SHA; head = `273565d84dd61458254db5b1e3f7c53741b185ef`; `merge-base = 8e44ca9c751049d65e6def47600b5c073ee04b29`; seven linear commits.
- PR state at decision: OPEN, ready for review, `mergeable=MERGEABLE`, `mergeStateStatus=UNSTABLE` because of the failing governed-court check below.
- GitHub branch truth: `integration/pre-main-reconciliation-r1` reports `protected=false`, no rules. This return does **not** claim the branch is protected; "protected receiving" here is the governance/CAS concept, not a GitHub ruleset.

Exact diff `8e44ca9c..273565d8` — seven paths, nothing else:

| Path | Git blob | sha256 |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `4b89c4598f324834de064c1200c63698a20e3c5c` | `f9794976aef51c418e8152850a7b0143df6790d0596549ea7f0991fc1f4501e9` |
| `rawlsing_next/pre553_r5_codec.py` | `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7` | `fc3aaec95d1ea6b396afb7484e5b58a242a878f9a003b47a30d7f35d48eaa9ae` |
| `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py` | `625f1d8b1f3fa8c24501addcaff7d70209598596` | `54195599ba4428db26b41f49bb486588502115bd119c7dc6bdee6fe1b65873da` |
| `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | `ac5f331322a69dab224eeeda14b05681918b432e` | `18465ff974d8767fa2ed23197084ff787d2b3bdc19e88201d1fdd84b83121d0f` |
| `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py` | `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115` | `487e9c3aabd73ae24cbdfe11b9563ea77344e06ee0c2241df7049df15620df12` |
| `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` | `c07c2019455e6264b4297c1c1d782bd887b96bdd` | `1042789d92c94dd5ef983299f4cbc46b40bc55e2d556f055f6777ada11254737` |
| `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/RRIF_C3_E4F_SELECTIVE_RECEIVING_20261101.md` | `8f0ff3c00d9ea1361f201cf3daf3f06540c5942f` | documentary receiving record |

The two production blobs are exactly the E4F `f2c0af32...` blobs. The four test blobs are exactly the frozen E1/E4F blobs. The two production files are the only production deltas (`+53/−6` decoder, `+102/−0` codec); all four tests and the documentary record are additions.

## 3. Mandated receiving results

| Check | Result | Exit |
|---|---|---|
| E1 original 33 + E4F new 12 = 45 | `45 passed in 2.32s` | 0 |
| Selected PR526/SAV/C11/EE-P2X 195 collected | `194 passed, 1 skipped in 144.21s` | 0 |
| G01 full pair at PR head | `2 failed, 7 passed in 278.03s`; same two baseline node IDs/values | 1 (preserved baseline RED) |
| G01 full pair at PRE-MAIN `8e44ca9c` | `2 failed, 7 passed in 277.07s`; identical node IDs/values | 1 (same baseline RED) |
| Hostile probe: real synthetic SAV/DTA, aware direct/one-level, SAV bits, PR526, range | exact expected outputs; see receipt doc | 0 |
| First decoder consumer `ee_p2x_darwin_stage_backend._decode` SAV branch | exercised by `test_actual_decoder_consumer_decode_regression` in the 45/45 suite | 0 |
| First decoder consumer DTA branch with synthetic SHA | refused by D01 exact encoding allowlist before decode (`DecoderError`), not a D02 failure | 1 (expected D01 law) |
| Governed-court proof-integrity CI | RED: two new integration-claim tests need sibling `.proof.json` witnesses | 1 |

The G01 REDs are exactly the pre-existing pair, not introduced or repaired by this packet:

- `test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation`: `47f141e43fb2...` vs `b9b720335f37...`.
- `test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak`: `StopIteration`.

The E4FR-discovered two-level `.item()` boundary is reproduced unchanged: `Wrapper(Wrapper(aware_datetime))` still stringifies through recursive `_jsonable`; direct and one-level aware values refuse with `R5CodecError`. This is recorded as **NONBLOCKING only** for the real current pyreadstat SAV/DTA cell route and is not a universal timezone-aware fail-closed claim. The historical R5 seam is loaded from pinned Git objects in the sourcefree tests; it is not an installed current production importer.

## 4. ENGINEERING / SCIENTIFIC / AUTHORITY

**ENGINEERING:** `PASS_RECEIVING_45_194_1_G01_2_BASELINE_RED__HOLD_GOVERNED_COURT_PROOF_JSON_WITNESSES_MISSING`.
The exact six blobs are correct and the mandated sourcefree receiver suites reproduce. The exact first consumer is unchanged (`rawlsing_next/ee_p2x_darwin_stage_backend.py:713`). The packet is not PRE-MAIN-mergeable as frozen because the governed-court proof-integrity gate is RED. The missing files are:
- `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py.proof.json`
- `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py.proof.json`

**SCIENTIFIC:** `HELD`. No raw survey/source decode, encoding text semantics, survey meaning, estimand, response state, G01 numeric bridge, N11/N12, actor or R9/Sorok authority is issued. The date/time carrier is physical representation only.

**AUTHORITY:** `OWNER_IDENTITY_VERIFIED__NO_MERGE_EXECUTED__EXACT_OWNER_DECISION_REQUIRED`.
The repository owner account `maidiu` issued the direct commission (issue #604) and the canonical 2026-10-30 direct user directive, which grants administrative permission to finish tested sourcefree work and says not to claim an unprotected branch is protected. The live branch is unprotected. No GitHub protection approval is missing. This is not source/scientific/actor authority, and E4FR engineering acceptance was not treated as one. The merge was nevertheless not executed because the mandatory proof-integrity gate is RED and the frozen seven-path allowlist forbids adding the two required witness files. The owner must now either authorize the two witness files plus a new exact head/allowlist, or explicitly waive the proof-integrity gate for this exact sourcefree receiving. A merge also requires the separate current owner progress MD/JSON paired revision CAS required by the fan-in law; the six-file PR does not carry that pair.

## 5. What was done, what was not, and exact next move

Done:
- Verified all six frozen input SHAs exist and the live PRE-MAIN matches.
- Recomputed the PR diff and all six blob identities; no whole-branch cherry-pick.
- Ran the mandated sourcefree suites and hostile probes on the exact PR head.
- Reproduced the same two G01 baseline REDs on PRE-MAIN and PR head.
- Marked PR #602 ready for owner CAS; did not merge, force-push or delete any branch.
- Updated the RRIF C3 terminal line on the ledger branch to EXACT_HOLD.

Not done:
- No PRE-MAIN merge; no MERGED SHA exists for this packet.
- No `.proof.json` files added; adding them would exceed the frozen seven-path allowlist.
- No source-native/raw survey execution; no PROGRAMMA activity; no R9/Sorok/actor/G01 authority.
- No own hostile review of E4FR; E4FR remains the independent reviewer.

Exact next move:
1. Owner decides: authorize the two proof-integrity witnesses (new exact head + allowlist) or explicitly waive that gate for this packet.
2. Owner performs/authorizes the separate progress MD/JSON paired revision CAS if adopting.
3. Then merge PR #602 and read back the actual merged PRE-MAIN SHA. Until then the terminal state is `EXACT_HOLD`, not `MERGED_SOURCEFREE`.

## 6. Return discipline and final SHA

Only these three documentary artifacts are committed on the assigned agent branch; the six payload files were not modified by this receiving agent and no source-native file was touched. The RRIF ledger update is a separate documentary commit on `research/pyat-rrif-hq-d1d5-intake-20261031-r1` (exact pushed SHA `b8994d2b2ff2aa556b4d9f2e8fda39a5cb574fff`).

The final 40-hex agent-branch commit is the pushed documentary commit read back from `origin`; it is reported in the terminal response and not embedded here because embedding it would change the commit it identifies.
