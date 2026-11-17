# D3B COMPLETE RETURN — active gates, source proof, 118→decision, builder outputs

**Return root:** `WORKER_RETURNS/ANVIL_R7_FLEET/D3B/` on `agent/anvil-d3b-rabochii-20261117-r1`,
base `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`.
**Role:** independent corrective rabochiy / D3 Role B. **Not HQ, not final C, not architecture selector.**
**Pair question answered:** which precise executable gates and production artifacts prevent false S1 blockage and false S3/C no-loss acceptance with the least nonceremonial machinery.

## 1. Source/currentness cut and GROK

- Protected PRE-MAIN `31291d08179890852246c8742700e055168e9933`; paired PYAT progress rev10.
- K3 protected `7fc00289dd801d2d0a8ce159986c7595fc27a4d9`; exact 29/26/14 TSVs reconstructed via `git show`.
- SEAM/25 `596f1230…`; SEAM/26 `796452b8…`; ANVIL/15 `3cc09bba…`.
- Supplied ZIP SHA-256 `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332`; 280 files.
- Full curriculum and sources read independently; `GROK_PROOF.md` answers all ten probes with exact evidence and a falsifier each.
- Scope-sensitive grounding receipt: `GROUNDING_RECEIPT.md` / embedded in `GROK_PROOF.md`.
- No sibling worker draft/worktree/branch was inspected. No worker was dispatched. The trailing controller launch snippet was **not executed** because it conflicts with the explicit D1/D2 prohibition and controller/lease law.
- No `ANVIL_118_FORENSIC_AUDIT.md` was supplied; bounded local search found none. It is treated as an untested allegation, not source authority.

## 2. Confirmed observations (source-static / code / local tests)

1. **S1 false blockage is real.** `tools/r7_integrated.py` required `historical_source_spine.schema` in `{ANVIL_SPINE_R5,ANVIL_SPINE_R6}` and equality to a transfer file. R5 provenance (`20_RECOVERY_AND_TEST_PROVENANCE.md`) says `PREPARED / LOCALLY STRUCTURALLY TESTED / NOT DISPATCHED`; a completed P2 SPINE was an expected output. The old test fixture `r6_fixture()` fabricates a spine, demonstrating the circularity.
2. **The transfer does not authenticate.** `r7_transfer_conservation.py` copies `coverage` and hashes the same bytes; equality proves internal consistency only.
3. **S3 was silent on 118.** `check_decision` reconciled only `frame.requirements` (nine domains in the fixture), never all 118 mixed identities. Local `PASS` was possible while most of the historical/prospective universe had no candidate-specific disposition.
4. **C checked packet prose/cards but not T1–T7 positive/negative/restore, not a typed producer/authority/time/consumer graph, and not an actual builder handoff.**
5. **The supplied R5 `anvil.py` already had exact row/blob validation and six deterministic projections** (`DESIGN_DECISION.md`, `COVERAGE_TO_DECISION.tsv`, `DOWNSTREAM_BUILD_HANDOFF.jsonl`, `EVIDENCE_AND_FALSIFIER_INDEX.jsonl`, `GLOBAL_ARCHITECTURE.json`, `BOUNDARY_TRACE.json`). The correction restores equivalent mechanics for the active instrument without importing a SPINE.

## 3. What was implemented (private package copy only)

- **`tools/r7_inventory.py`** (new): builds/verifies the `ANVIL_R7_SOURCE_IDENTITY_INVENTORY` from exact bytes:
  - 118 entries, exact counts 29/26/14/10/8/8/7/16;
  - K3 row SHA-256 + file/blob/commit verification (`git cat-file`/`rev-parse`/`show` when `--repo` supplied);
  - SEAM/ANVIL exact excerpts; T1–T7 and terminal IDs from the supplied ZIP contracts;
  - `PYAT_PC.adopted=false`, `P4R.closed=false`; no adoption/closure claim.
- **`tools/r7_integrated.py`** (corrected):
  - S1 now requires `source_inventory`; a legacy R5/R6 SPINE is optional historical evidence only and **cannot** satisfy S1.
  - S3 now requires 118 candidate-specific `identity_dispositions`, origin-hash binding, 26/14 status enforcement, no silent retirement, no blocking loss at author grade, and a typed whole-machine graph.
  - C now requires T1–T7 positive/negative/restore, graph audit with no holes, builder-handoff review, no self-certified independence, no local H1/protected claim.
- **`tools/r7_build.py`** (new): deterministic six projections + manifest; `verify` re-derives and byte-compares, with refusal/restore.
- **`tools/r7_transfer_conservation.py`**: now explicitly `sufficient_for_s1: false`; transfer is not identity truth.
- **`tools/test_r7_integrated.py`**: replaced with a source-authenticated 24-test suite covering the required positive/negative/restore matrix and preserving the old A/B/optional-duel/no-fake-source intents.
- **`GATES_CHANGESET.patch`**: applies cleanly to a fresh original `ANVIL_R7/tools` tree (`git apply --check` exit 0).
- **`EVIDENCE/SOURCE_IDENTITY_INVENTORY.json`**: the actual built inventory, verified with the shared Git object store; status `PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY`, `GIT_OBJECT_BLOB_AND_BYTES_VERIFIED`.

## 4. What was actually run

| Command | Result |
|---|---|
| `python3 tools/r7_inventory.py build …` | exit 0, 118 entries, exact counts |
| `python3 tools/r7_inventory.py verify … --repo /Users/matthewsmith/s2b-work/rawlsing` | exit 0, `PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY`, `GIT_OBJECT_BLOB_AND_BYTES_VERIFIED` |
| `python3 -m unittest -v test_r7_integrated` | exit 0, **24 tests OK** |
| `python3 tools/run_r7_quality.py` | exit 0, `PASS_LOCAL_SYNTHETIC_AND_FORMAT_ONLY`, 12 commands all exit 0 |
| `python3 -m unittest test_r7_integrated` | exit 0 |
| `git apply --check` of `GATES_CHANGESET.patch` on fresh original tools | exit 0 |

Exact stdout/return codes/input hashes: `TEST_TRANSCRIPT.json`. **Not run:** native original SAV/DTA decode, 100k/6 GiB production benchmark, independent C, protected H1, CI. Those remain `NOT_RUN` and are not claimed.

Required negative cases observed RED, then restore PASS where applicable: synthetic SPINE-as-original; missing K3 row; source-byte mutation; missing B-10; 26 adopted/14 closed; one missing identity after a 53-row complete crosswalk; blocking loss; silent historical retirement; missing T negative/restore; typed graph hole; local fake H1; six-projection byte mutation.

## 5. Strongest alternative / counterexample

**Alternative considered:** keep the legacy SPINE path and add an inventory cross-check.
**Rejected:** the synthetic path remains sufficient whenever the cross-check is absent or bypassed; the minimal safe rule is “legacy SPINE is never identity truth.” **Counterexample:** two rows with identical ID text but different meanings; ID-only coverage passes, exact row hash + excerpt + origin fails. **Second:** a 118-row decision with a copied `PRESENT_PRESERVED` row but drifted origin/first-consumer path; the gate fails on origin drift/vacuity. **Third:** a C packet with all seven T labels but generic identical positive/negative/restore text; the local gate rejects short/vacuous fields, but only an external C can judge semantic adequacy — local PASS is deliberately not H1.

## 6. Exact file hashes (this return)

```
3854e0bdcf6faa017a03e43db8817fa11cb25a08164898f300a75910a8bdffca  EVIDENCE/SOURCE_IDENTITY_INVENTORY.json
544d8822bd9f5b4fc6f771f4cb4578449348a32baa6a6db429f581f333b470ff  EVIDENCE/SOURCE_118/PIN_MANIFEST.json
01c5da0df1ba0db71383fbfeec6bcd7cec8d49bcf4dff4ebae75a15a76d873f6  PACKAGE/ANVIL_R7/tools/r7_integrated.py
536f7fd9bdff388beb1482f0660a3758b6e5b2656d4b0fc6779f54da64848062  PACKAGE/ANVIL_R7/tools/r7_inventory.py
9e90183219f755f1310df1d37515fb1ddc774ca4e9a36addd7671f33f05f4779  PACKAGE/ANVIL_R7/tools/r7_build.py
ec3af115b1b8d7f6625c1d4434c6c661a01eeb362f9787007cf2afaccfb450bc  PACKAGE/ANVIL_R7/tools/test_r7_integrated.py
0aa12c27b764ab7f4d7c25579d1da0f7a820721e0b79e6346d9878c01219747c  PACKAGE/ANVIL_R7/tools/r7_transfer_conservation.py
19dd88cc5ba818cb46f98cde28bd652552042b23148903c005a863a97f4c8208  GATES_CHANGESET.patch
001be65335a02affebb42338b14338e7e85b6ae6db1b918e336363f9f0306007  GROK_PROOF.md
cac323497ea64a193c316e823e40d406ef1c7c4d90b1547a5b6a77f6a5bbc7e1  GATE_DESIGN.md
bc7e3e976b71e1c59fd6f647a7151079b78442e53b0702f3daf736eba0024231  COLD_BUILDER_OUTPUT_SPEC.md
c633257288a3bc45a4b0d20efcc1a5f4e776c277f6da6b5df3f0175a3cb7ad11  TEST_TRANSCRIPT.json
cf7ebd61eda6ca0989a47fb37fafd558121a3a6d5ea678aa7a81238fe8c61895  GROUNDING_RECEIPT.md
```

Published commit is the final branch HEAD reported to HQ; this file is included in that commit. The commit cannot truthfully embed its own SHA.

## 7. Confirmed vs interpretation vs owner holds

- **Confirmed source/code facts:** the old S1 spine dependency, transfer circularity, missing 118 crosswalk, missing C boundary/graph checks; exact K3/SEAM/ANVIL bytes and 118 counts; local test behavior.
- **Interpretation:** the minimal safe correction is an inventory-first S1, 118-row decision reconciliation, C boundary court and deterministic builder. This is an instrument argument, not architecture selection.
- **Owner holds:** physical C11 architecture; all K3 26/14 dispositions; native original-source rights; FF02/N9/N10W/SOROK science; independent C; protected H1. No local PASS converts any of these.

## 8. Explicit non-claims

No final C, no HQ accreditation, no protected H1, no architecture selection, no source/science/actor permission, no 118 accepted functions, no 26 new adoptions, no 14 proof closures, no full A/B mandate, no K4, no CI-green claim. The test suite is bounded authored sourcefree evidence; the missing integrated candidate’s attacks are `NOT_RUN`.
