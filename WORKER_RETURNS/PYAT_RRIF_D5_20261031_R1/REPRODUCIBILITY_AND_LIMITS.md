# Reproducibility and limits — RRIF-D5

## 1. Identity

| Item | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Assigned branch | `agent/pyat-rrif-d5-world-service-fates-20261031-r1` |
| Startup SHA | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| Remote startup readback | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d5-world-service-fates-20261031-r1` |
| Return directory | `WORKER_RETURNS/PYAT_RRIF_D5_20261031_R1/` |
| Final commit SHA | reported in terminal after push/readback; not embeddable in this file |
| Final GitHub readback | reported in terminal after non-force push |

Current PRE-MAIN source was rechecked at the startup SHA before writing. The branch remote ref was at the same SHA before the first write. No PRE-MAIN/main mutation was performed.

## 2. Environment

| Item | Value |
|---|---|
| OS | macOS Darwin |
| Python | `3.11.3` |
| pytest | `9.0.2` |
| Harness | local OpenCode |
| Configured model ID | `opencode-go/deepseek-v4.1-flash` |
| Actual provider | UNKNOWN |
| Variant / effort | UNVERIFIED; MAX is not claimed |
| Browser | not used |
| Source-native execution | none |
| Raw survey / PDF / native P07 | none |
| Network | GitHub Git/API reads only; no source download |

## 3. Worktree, lease and active-worker check

Before creating the D5 worktree:

- `git worktree list` showed the canonical repository plus existing D1/D2/D3 worktrees at `8e44ca9c75` and several older worktrees.
- `~/Desktop/Rawlsing_Worktrees/pyat-rrif-d5-world-service-fates-20261031-r1` did not exist (`FREE`).
- The remote D5 ref existed at `8e44ca9c75`.
- D1 was clean and an active OpenCode D1 worker process was observed; it was not touched.
- D2 and D3 were clean at their startup refs; they were not touched.
- No local D5 worktree existed.
- `git worktree add -b agent/pyat-rrif-d5-world-service-fates-20261031-r1 <d5-path> 8e44ca9c75` created the exclusive worktree.

No repository lease file or worker-lease artifact exists in `maidiu/rawlsing`. The user launch did not grant a verifiable account/quota lease. Lease, account, quota and host rights remain `UNKNOWN`; no right was inferred. The sibling D4 remote ref moved during the task (`57e22a5c...` at readback); D4 was not inspected as current, not consumed, and not touched.

The linked sparse world-binding worktree at `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_worldwt` was used only for R117 tests and removed after the run. Historical test archives were extracted under `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_hist/`; they are disposable and not part of the return.

## 4. Source cuts read

- Current PRE-MAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- RRIF-C: `b75addf621c3a6c1a3b196bd92a810fad77ae3ae`.
- RRIF-V hostile: `bec050449f0b38606718e4e9691caa1721fcd94f`.
- A: `84182f9fa7044d67689ea4f80eabf7e9337f15c2`.
- B: `59e6e62600814d82cfefd1a2137b7aa63316bc95`.
- A×B: `f5a9facd189af6756c2b15c8daebe680016f658a`.
- E8: `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`.

Historical lineage cuts read include:

- `5eb51c68`, `a1dc5941` (I01).
- `0e0ed50d`, `c98e8881`, `208bca30`, `849a76de` (N9/N10W progressive and world binding).
- `9ab4a019` (N9C), plus D2P `af128002d`, D2R independent verdict, D2P2 `d19bd3cbe`.
- `b497f857`, `b94f0f981` (PE and PE2).
- `54f14553`, `ac75c6fc`, `5e6e802f`, `aba2f6a6` (R3 seam).
- `79309093`, `22280a3f`, `359ffcef` (world binding source cuts).
- PYATWORLD-R3 documentary decision `a9d84389d`.

## 5. Reproducing the tests

The exact commands and observed counts are in `FIRST_CONSUMER_AND_TESTS.md`. Summary:

```bash
# current
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d5-world-service-fates-20261031-r1
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py -q -o addopts=''
# 18 passed

# historical archives (sourcefree)
TMP=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_d5_hist
mkdir -p "$TMP/n9c" "$TMP/pe" "$TMP/seam" "$TMP/i01"
cd /Users/matthewsmith/Desktop/rawlsing_r02v_r2_canonical
git archive 9ab4a019 rawlsing_next tests WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1 | tar -x -C "$TMP/n9c"
git archive b497f857 rawlsing_next tests | tar -x -C "$TMP/pe"
git archive aba2f6a6 rawlsing_next tests WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1 | tar -x -C "$TMP/seam"
git archive a1dc5941 rawlsing_next tests | tar -x -C "$TMP/i01"

# world binding: sparse linked worktree at exact R117 cut
git worktree add --detach --no-checkout "$TMP/worldwt" 849a76de18ef627c3c403b426ebe70f0951a7e7b
cd "$TMP/worldwt"
git sparse-checkout init --cone
git sparse-checkout set rawlsing_next
git checkout 849a76de18ef627c3c403b426ebe70f0951a7e7b -- rawlsing_next
```

Exact historical test commands:

```bash
cd "$TMP/n9c" && PYTHONPATH=. python3 -m pytest -q tests/test_hq297_n9c_two_field_reader.py -o addopts=''
cd "$TMP/pe" && PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py rawlsing_next/tests/test_postastra_pe_fixture.py -o addopts=''
cd "$TMP/seam" && PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_r3_s02_seam_witness.py rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py -o addopts=''
cd "$TMP/i01" && PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_hq287_i01_sourcefree_world_lifecycle.py rawlsing_next/tests/test_hq292_i01k_typed_selection_restore.py -o addopts=''
cd "$TMP/worldwt" && PYTHONPATH=. python3 -m pytest -q rawlsing_next/tests/test_universal_world_binding.py rawlsing_next/tests/test_world_conditioned_progressive_service.py -o addopts=''
```

Expected counts:

| Court | Count |
|---|---|
| Current E03 | 18 passed |
| Current owner baseline | 151 passed |
| I01 author | 17 passed |
| N9C local | 47 passed; 11 targeted passed |
| PE | 21 passed; 7 targeted passed |
| R3 seam | 50 passed, 1 stale-positive failed |
| R117 world binding | 30 passed, 4 J42 environment errors; 27 + 3 split; 7 targeted passed |

The 4 R117 errors are `test_r06_actual_j42_*` and `test_r06r4_context_authority...`, caused by the sparse checkout lacking the full J42 return/fixture terrain. They are not counted as candidate failures. The R3 failure is preserved, not waived.

## 6. I01 current-compatibility probe

The probe copies current `rawlsing_next` to a temp directory and overlays only the exact historical I01/selected/seam/durable files from `a1dc5941`. It does not modify the current worktree.

```python
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
import tempfile
I.build_product(tempfile.mkdtemp())
# AttributeError: 'LearnedProductLifecycleExecutor' object has no attribute
# 'verify_m2_release_subject_exact'
```

This is the exact current dependency-severance finding. It is not repaired here.

## 7. Limits

- No lease, account, quota or host-right verification was possible. These remain UNKNOWN.
- The actual provider and effort/variant are not independently verified. MAX is not claimed; no model switch was made.
- No browser was used.
- No original source, raw survey, publisher PDF, native P07, U/E_pre, Field Forge, CAN/ADP, N11 objective acceptance, Sorok N12 actor wake or model-use issuance was read, executed or issued.
- No current production consumer exists for I01, N9C, PE, R3 seam or world binding. The only current receiver is the E03 test/CI.
- The R117 tests are sourcefree and test-only; the 4 J42 errors are environment terrain. No full J42 acceptance is claimed.
- Exact blob identity is not behavioral equivalence.
- No returned code/review artifact was found for #564, #565, #569, #570, #571, #575, #576, #577, #578 or #579. Only issue states and correction comments were present. #577 remote unchanged is not worker-idle proof. #580–#584 remain held.
- No PRE-MAIN/main, Sorok, protected source, pending reviewer, other worktree or active worker was mutated.
- The final commit SHA is reported in the terminal after non-force push and GitHub readback. It cannot be embedded in the commit it identifies.

**STOP maintained:** no merge, no force push, no worker relaunch, no self-review, no inferred host rights.
