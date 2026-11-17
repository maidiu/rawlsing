# RAW COMMANDS AND EXITS — C review

All paths are under `/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW` unless absolute. Logs are in `WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/LOGS/`; witness results are under `WITNESS/`.

## 0. Identity and target

```text
$ git branch --show-current
agent/anvil-instrument-independent-c-20261117-r1
$ git rev-parse HEAD
0f0c673f99978aff6c11f7bd0e6fe1840fbdc799
$ git log --oneline -2
0f0c673f9 ANVIL: integrated source-authenticated 118 decision instrument (PENDING_DISTINCT_C)
cea2d4d30 PYAT P0: reuse one authenticated cold saved C11 session across many operations
```

`shasum -a 256 REPAIRED_PACKAGE.zip` = `7569fb21a577aff06d48ce7759cf692c8f2ba3e475b8eba1e71c36d4e5abc689`; `stat -f '%z'` = `1561148`.
`shasum -a 256 /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip` = `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332`; original ZIP has 280 entries.

## 1. Candidate manifest verification (657/657)

```text
python3 - <<'PY'
import json,hashlib,os
m=json.load(open('WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/MANIFEST.json'))
missing=[];bad=[];ok=0
for f in m['files']:
    p=f['path']
    if not os.path.exists(p): missing.append(p); continue
    h=hashlib.sha256(open(p,'rb').read()).hexdigest()
    if h!=f['sha256'] or os.path.getsize(p)!=f['bytes']: bad.append((p,h,f['sha256']))
    else: ok+=1
print('total',m['total_files'],'ok',ok,'missing',len(missing),'bad',len(bad))
PY
```

Result: `total 657 ok 657 missing 0 bad 0`. `SOURCE_AUTHENTICATION.json` inventory hash `5e06b95f...` and raw log hash `3aa43804...` match; all 23 `TEST_TRANSCRIPT.json` raw-log hashes match.

## 2. Exact source replay (W0)

```text
python3 WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/WITNESS/w0_source_replay.py
```

Exit `0`; `WITNESS/W0_SOURCE_REPLAY/source_replay.json`:
`sets_equal=true`, `unique_ids=118`, `exact_rows_ok=118`, counts 29/26/14/10/8/8/7/16, 26 PC NOT_ADOPTED, B-10/S-08/L-08 present. The exact Git files/blobs/SHA are recorded there.

## 3. Cold extraction and candidate tests

```text
unzip -q WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/REPAIRED_PACKAGE.zip -d WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/TEMP/COLD_<stamp>
cd .../TEMP/COLD_<stamp>/ANVIL_R7/tools
```

- `python3 r7_inventory.py verify --source-root ../tests/fixtures/source_118 --repo ... --zip ... --inventory ../tests/fixtures/source_118/SOURCE_IDENTITY_INVENTORY.json` → exit **1**, `FileNotFoundError` (the literal handoff path is wrong).
- Corrected path `--source-root ../EVIDENCE/SOURCE_118 ... --inventory ../EVIDENCE/SOURCE_IDENTITY_INVENTORY.json` → exit **0**, `PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY`, 118, zero errors (`LOGS/cold_inventory_correctpath.log`).
- `python3 test_r7_integrated.py -q` → exit **0**, `Ran 29 tests ... OK` (`LOGS/cold_inherited29.log`).
- `python3 test_integrated_strict.py` from the literal clean extraction → exit **1**, 13 errors, missing `.../TEMP/EVIDENCE` (`LOGS/handoff_clean_13.log`).
- After manually copying `ANVIL_R7/EVIDENCE` to `.../TEMP/EVIDENCE` (undocumented layout), `python3 test_integrated_strict.py` → exit **0**, `Ran 13 tests ... OK` (`LOGS/cold_integrated13_temp_evidence.log`).
- `python3 r7_integrated.py FRAME ../EVIDENCE/FRAME.json ...` → exit 0, `PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED`.
- `python3 r7_integrated.py DECISION ../EVIDENCE/DECISION.json ...` → exit 0, `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`.
- `python3 r7_integrated.py C_INTEGRATED ../EVIDENCE/C.json ...` → exit 0, `PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED`.
- `python3 r7_build.py verify ... --out .../INTEGRATION/BUILT` → exit 0, `PASS_SIX_PROJECTIONS_BYTE_IDENTICAL`.

## 4. Independent adversarial witnesses

| Command | Exit | Result |
|---|---:|---|
| `python3 WITNESS/w1_req_f6_hollow.py` | 0 | FRAME + DECISION PASS after pairwise-only requirement/F6 negative erasure (`WITNESS/W1_REQ_AND_F6_HOLLOW/w1_result.json`) |
| `python3 WITNESS/w2_c_boundary_false_science.py` | 0 | C_INTEGRATED PASS with false T4/T6/T7 actor/world science (`WITNESS/W2_C_BOUNDARY_FALSE_SCIENCE/w2_result.json`) |
| `python3 WITNESS/w3_builder_receipt.py` | 0 | Real command RED as `NONEXISTENT:python3`; fake receipt PASS with dummy `python3` (`WITNESS/W3_BUILDER_RECEIPT/w3_result.json`) |
| `python3 WITNESS/w4_source_negative_tamper.py` | 0 | FRAME + DECISION PASS after inverting K1-CAP-11/17 semantics/negatives while preserving exact excerpts (`WITNESS/W4_SOURCE_NEGATIVE_TAMPER/w4_result.json`) |
| `python3 WITNESS/w5_terminal_graph.py` | 0 | 6-node/7-edge graph, 0 of 16 terminal IDs; DECISION/C PASS (`WITNESS/W5_TERMINAL_GRAPH/w5_result.json`) |
| `python3 WITNESS/w6_projection_no_loss.py` | 0 | 1 distinct identity/requirement disposition string; shallow projections (`WITNESS/W6_PROJECTION_NO_LOSS/w6_result.json`) |
| `python3 WITNESS/w7_joint_denominator.py` | 0 | even/odd `P(111)=0` vs `1/4`; forward denominator 4, reverse 5 (`LOGS/w7_joint_denominator.log`) |
| `python3 WITNESS/w8_omission_controls.py` | 0 | B-10/S-08/L-08 omission and inventory omission RED; control works (`WITNESS/W8_OMISSION_CONTROLS/w8_result.json`) |

## 5. Source/authority reads

```text
git -C /Users/matthewsmith/s2b-work/rawlsing cat-file -t 31291d08179890852246c8742700e055168e9933
# commit
git -C ... show 31291d...:PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md | head
# first bytes: "# HQ OATH — PROGRAMMA FIRST CONTACT"
```

`CURRENT_PROGRESS.json` revision = `10`; `CURRENT_PROGRESS.md` title = `REVISION 10`. K3 blobs/row SHA, SEAM/25, SEAM/26 and ANVIL/15 were read via `git show` at the exact commits/blobs recorded in `WITNESS/W0_SOURCE_REPLAY/source_replay.json`. No protected write or merge occurred.

## 6. Key source excerpts inspected for the pre-grok

- V549 `build_branch_co_signature_summary_v549.py`: `build_branch_mask` (line 449), `aggfunc="first"` (line 555) — branch conditioning survives; lossy first-value collapse does not.
- V550 `build_determinicity_repository_v550.py`: `is_missing`, `is_refusal`, `is_iap`, `is_not_asked`, `is_inapplicable` typed semantics.
- V550J `ddm_v550j_joint_patterns.py`: same-person joint pattern helper; `build_v550j_prepared_substrate.py`: prepared substrate/cache signature and `is_valid_substantive_response`.
- F26 exact original per-query caller/invalidation: **not found**; preserve the existing K3/P4R owner hold.

## 7. Verdict artifacts

- `GROK_PROOF.md`
- `VERDICT.md`
- `REVIEW_VERDICT.json` (`verdict = REVISE_EXACT_DEFECT`)
- `EXACT_SHA256.json` (generated after the final verdict; includes witness/log hashes)
- `LOGS/` raw stdout/stderr and exits
