# PYAT HQ246 — F7 STAGE B FROZEN NATIVE P07 INDEPENDENT HOSTILE REVIEW — R1

**STATUS:** NEW — NEEDS LAUNCH
**AGENT:** DeepSeek-Harness / OpenCode INDEPENDENT governed-runtime hostile native reviewer (not author Space Bunny)
**MODEL / INTELLIGENCE:** DeepSeek V4.1 Flash, verify installed provider/model ID and variant before launch
**MACHINE:** governed Mac CPython 3.11.3 x86_64, dedicated NEW isolated sparse worktree from shared single Git object store
**REPOSITORY:** `maidiu/rawlsing`
**BRANCH:** `agent/reviewer-pyat-hq246-f7-native-stage-b-independent-hostile-r1`
**FROZEN EXACT CANDIDATE AND BASE:** `agent/space-bunny-pyat-hq245-f7-native-stage-b-full-p07-parity-r1 @ 0dd0a503882ef777141092d7678285462214a600`
**MODEL REVIEW MODE:** Frozen author Stage B source only. No reviewer repair or adoption. No production mutation, no user raw survey, actor/V3/F8, no control writes, no compiled binary Git commit.

## Binding source evidence

Read COMPLETE `WORKER_RETURNS/PYAT-HQ245-F7-NATIVE-STAGE-B-FULL-P07-ADJUDICATOR-PARITY-R1/`; actual `rawlsing_next/_p07_native_owner_stage_b.c` blob `2d8ffc686fcdb3f7108f0c8bafe7f60273fcf304` at 1802 lines and Stage B test file; independent prior Stage A review `WORKER_RETURNS/PYAT-HQ245-F7-NATIVE-STAGE-A-INDEPENDENT-HOSTILE-RUNTIME-REVIEW-R1/` at `14432c2b21eaf87a8e92ecb75a6765cf3763ddc1`, especially HQ245-D1–D9 and real runnable reproduction under `reproduction/`. Baseline A at `85144216e9ceb58f306d5624620ee42df34d1718`. HQ242 T1 bounded producer-grain architecture and HQ241 alias census, original four HQ234–HQ236 forgeries and five HQD216 lawful positives.

A **separate** Space Bunny repair is being engineered at `agent/space-bunny-pyat-hq246-f7-native-ab-memory-boundary-repair-r1` on a separate worktree from the SAME frozen Stage B tip. Do NOT read/merge that repair into this immutable review or certify the future candidate. Your findings determine the minimum fresh independent review of repaired SHA.

## HIGH-PRIORITY exact Stage B constructor unsafe pattern (HQ verified static)

In original Stage B source lines 827–829 `PyList_Check`/`PyTuple_Check` admits subclasses; lines 850–851 obtain `n`/`m` via overridable `PySequence_Size(relations/snaps)`; lines 863–876 enumerate `PySequence_Fast_GET_ITEM(fast,i)` up to those counts **without verifying `GET_SIZE`**. Stage A same pattern was ASAN-proven to SIGSEGV via `class EvilList(list): def __len__(self): return 5` wrapping 1 real element. Stage B has TWO dimensions, relations and authority snapshots. Independently produce original subprocess-contained reproductions for over-report, under-report, error-raise, negative/huge length, tuple subclass as feasible; note state and exit code/ASAN. Do NOT assume identical crash merely from static source: **measure**. No executing raw surveys. If subprocess crashes preserve receipt but avoid uncontrolled repeated crash loops.

## Additional independent hostile review goals

1. C-API **memory ownership** across all 1802 lines: parse borrowed references; `canonicalize` may return input unchanged; trusted hash/authority callbacks, temporary material ownership, PySequence_Fast, exception handles, `Py_BuildValue` formats, module init PyModule_AddObject failures, partially initialised owners, NULL/failed pointers, GC cycles, normal dealloc/cancel. Check Stage A D2/D3 analogous memory leaks in B. Test 2,000/20,000 failing init iterations, custom list subclasses/callback reentry, defensive GC and callable-refcount; record true memory growth/false positive.
2. **Native custody/authenticity**: exact owned real relation-object key, accepted custody hash and semantic_projection rehash, source vs independent empty victim, registry replacement immunity, malicious changed underlying projection with ref.key/content_hash fixed, substituted snapshots, wrong class/identity, counterfeit exact ref with equal payload, enumerable dynamic Python instances. Pinning callable references from a caller **does not itself prove they are trusted code**: audit actual trusted-callable provenance and how a forger can supply its own positive `require_positive_authority`, canonicalize or semantic_hash to Stage B construction. The intended full T1 owner must not accept attacker-chosen trusted function identities; qualify it as a TCB-assumed test seam only where appropriate, and name future production-owned sealed construction gate.
3. **Parity rather than counts**: independently reconstruct P07 exact accepted original decision ladder, matrix defaults, forbidden backfill, typed positivity, 17 reported reachable state strings vs 6 precedence steps and original commission 12-state phrase. Compare owner-produced state, exact negative type/message, replay identity and custody hash on independent cases; especially **multi-positive CONFLICTING_AUTHORITY** and precedence ties, which the Stage B author itself says are untested. Do not count unexercised branches as PASS. Also source-free legitimate positive paths and exact snapshot verification.
4. **Evidence discrimination**: independently rebuild .so from committed C under governed CPython 3.11.3, check exact ABI/source/normal binary hash and no fault macro; rerun Stage B 41 and Stage A 39 (if Stage A crashes under targeted probes, do separate subprocesses), accepted P07 24/F7 163. Repeat `-DSTAGE_B_FAULT_INJECT_RESOLVE` red control; no production import. Baseline: stage author broad reports 2691 pass/45 fail/**16 errors** and normalized `72d0a5ca347d71f207a77bca3609dfa5931a3c6f29224a2f3f860ebc3ab09ffe`. Stage A reviewer independently reproduced nine-exclusion **54-item** digest `278854ee94fadfd57284a572441522fb56105081f89af431b17ec2e556ace6a9`; author's `72d0a5...` was NOT reproducible under reviewer's normalizations, so compare the **same** command and precise normalized failure lines.
5. **Scope**: Candidate is quarantined, may have AUTHORIZED in test harness only, never actually trusted by `pre553_source_relations.py` or F7 production `pre553_temporal_comparability.py`. No accepted `from_c11` cutover, no migrated introspection coupled tests, no actual F7 four-forgery or full five positive qualification. HQ242 T1 explicitly excludes arbitrary rewriting trusted F7 executable alias (HQ227/HQ231 red controls still required), no claimed T2 or external positive sink.

## Verdict and return

The existing Stage A hostile finding is an inherited BLOCKER until directly repaired; **do not rate unqualified Stage B green just because 41 tests pass**. Evaluate frozen B for actual exploitability and incremental findings independent from separate repair. If unable to test local ABI, report that rather than inventing pass.

Return `WORKER_RETURNS/PYAT-HQ246-F7-NATIVE-STAGE-B-INDEPENDENT-HOSTILE-REVIEW-R1/`:
- `00_REVIEW.md`
- `01_FROZEN_NATIVE_SOURCE_ABI_AND_MEMSAFETY_HOSTILITIES.json`
- `02_TRUSTED_CALLBACK_ORIGIN_CUSTODY_AND_FORGERY_ATTACKS.json`
- `03_PARITY_CONFLICT_CASES_AND_POSITIVE_CEILING.json`
- `04_FAIL_CAPABILITY_REGRESSION_AND_HQ242_HQ244_DIGEST.json`
- `05_NAMED_REPAIR_OBLIGATIONS_AND_STAGE_C_HOLDS.json`
- `06_FINAL_DISPOSITION.json`
- `reproduction/` original minimal synthetic scripts, no binary or raw survey.

Allowed dispositions:
- `F7_NATIVE_STAGE_B_FROZEN_HOSTILE_BLOCKED__NAMED_MEMORY_OR_TRUST_DEFECT`
- `F7_NATIVE_STAGE_B_FROZEN_HOSTILE_PARTIAL__NAMED_PARITY_OR_CUSTODY_DEFECT`
- `F7_NATIVE_STAGE_B_FROZEN_HOSTILE_ACCEPTABLE__STILL_QUARANTINED` (only if evidence truly supports it; doesn't adopt).

Commit only reviewer returns and proof scripts. Push reviewed branch, re-fetch exact GitHub remote return HEAD and report. No self-repair, no merge, no production/security adoption.
