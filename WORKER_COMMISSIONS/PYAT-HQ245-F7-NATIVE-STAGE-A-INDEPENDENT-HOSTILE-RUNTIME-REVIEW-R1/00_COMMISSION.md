# PYAT HQ245 — F7 NATIVE STAGE A INDEPENDENT HOSTILE RUNTIME AND MEMORY-SAFETY REVIEW — R1

**STATUS:** NEW — NEEDS LAUNCH
**AGENT:** DeepSeek-Harness / OpenCode independent local hostile code and runtime reviewer
**MODEL / INTELLIGENCE:** **DeepSeek V4.1 Flash** (verify actual provider/model ID + variant on host)
**MACHINE:** user's governed Mac, ISOLATED new sparse shared-store worktree; **NOT Browser/Sol**; distinct from simultaneous Space Bunny Stage B worktree/branch
**REPOSITORY:** `maidiu/rawlsing`
**BRANCH:** `agent/reviewer-pyat-hq245-f7-native-stage-a-independent-runtime-r1`
**EXACT BASE:** `85144216e9ceb58f306d5624620ee42df34d1718`
**PRODUCTION / STAGE A SOURCE MUTATION:** FORBIDDEN; build compiled binaries only in disposable local worktree (no binary commits).
**SELF-ADOPTION, SOURCE WORK, INTEGRATION, SEMANTIC/TCB Warrant CHANGES:** FORBIDDEN.

## Subject and context

Independent review of immutable Space Bunny Stage A candidate `agent/space-bunny-pyat-hq244-f7-native-owner-stage-a-custody-resolve-r1 @ 85144216e9ceb58f306d5624620ee42df34d1718`, with source `rawlsing_next/_p07_native_owner_stage_a.c` and `rawlsing_next/tests/test_p07_native_stage_a_custody.py`, plus Stage A receipts under `WORKER_RETURNS/PYAT-HQ244-F7-NATIVE-OWNER-STAGE-A-CUSTODY-RESOLVE-R1/`.

Worker disposition `F7_NATIVE_STAGE_A_CUSTODY_AND_RESOLVE_READY__NONAUTHORIZING_FOR_STAGE_B` with source 719 lines, normal native binary reported SHA256 `94683dd76cfa9c4d76958ef14f006f97616e0b082b4510cbea38768a8047fd04`, ABI CPython 3.11.3 on macOS 13.7.8 x86_64; 39/39 Stage A tests, 24 P07 + 163 F7 accepted baseline. A test-only build with `-DSTAGE_A_FAULT_INJECT` reportedly makes 2/39 red. Two actual segfault defects (NULL key read and malformed `Py_BuildValue`) fixed. These are claims until YOU independently check.

**Stage B Space Bunny engineering is separately running** on `agent/space-bunny-pyat-hq245-f7-native-stage-b-full-p07-parity-r1` from same Stage A candidate. Do not edit Stage B or auto-approve it. Your verdict may block Stage B later adoption and require integration correction; no concurrent code overwrite.

## Startup proof

`git fetch origin`; verify exact own branch commission HEAD, immutable reviewed SHA and ancestry; isolated worktree, no new clone. Check actual governed interpreter SHA256 `11d6f541a870a141249ce98d45834a6789e29c07031e85ce17f3e67f24c535f6`, headers and compiler provenance, exact native source and test blob SHAs against returned Git source tree. Rebuild from scratch **without relying on author's locally retained .so**, verify normal build SHA/determinism; preserve physical source estate. Do not use raw survey carriers or unrelated directories.

## Hostile review requirements

1. **Exact C-API safety**: inspect/refcount all constructor/exception/reinit/dealloc/partial-failure paths, GC cycles, PyObject* lifetimes and parse conversions; malformed `Py_BuildValue` and NULL-key prior defects independently exercise corrected paths and pathological synthetic invalid inputs. Read 719 lines, avoid superficial checklists. Run repeated long/invalid/randomized synthetic constructor/resolve stress with interpreter crash/ASAN/valgrind if available and permitted, report unavailable tools. No unsafe native memory injection claim required; actual segfault/repro reported explicitly.
2. **Security invariants**: inspect exact PyTypeObject flags (non-subclassable), one-shot state, mutable Python input deep-copy, C immutable sealed relation/authority refs, absence of writable Python capsule/resealer/wrapper positive bypass, exact by-ref lookup and ownership per native instance. Attack copy/pickle/reduce/reinit, object mutation, input callback/reentry, hostile registry reassignment, different owner same-key/source→empty victim. Check live per-lookup ref.key/content_hash and misdirection before rehash. Does the candidate *really* hold its needed immutable material in C, or only borrowed mutable Python objects? Distinguish nominal `deep custody` from actually copied semantic_projection bytes/authority snapshot — Stage A has an explicit incomplete scope.
3. **Quarantine**: source is Stage A only, `decide/require` unconditional `NOT_IMPLEMENTED_NONAUTHORIZING_STAGE_A`, no `RelationDecision` positive authority, no production P07/F7 imports or semantic/test mutation. Preserve the exact negative ceiling and F7-RR-04G OPEN. Stage A source **cannot** be adopted as final storage-only capsule. Check stage builder/rebuild doesn't load malicious wrong `.so` by path or leave fault-injection binary in standard import position.
4. **Positive + fail-capability**: independent 39-test rerun and new adversarial tests, independently rebuild normal binary and deliberately faulty **test-only** binary and verify at least two genuine negative test flips, then restore standard binary and show 39 pass again. Check `#ifdef STAGE_A_FAULT_INJECT` cannot be selected by normal recipe. A test that passes without actual runtime assertions fails. No claim of native F7 forged-owner security because no adjudicator exists.
5. **Parity / future blockers**: assess exact scope of `resolve_exact` parity, stage A fake FNV-1a custody provenance hash, ref-key-derived `by_key` vs actual object key, absent semantic_projection rehash and accepted P07 replay. Are these openly signposted future Stage B requirements, or do they invalidate even Stage A's claimed exact resolve under a material edge case? Give specific counterexample/court, avoid allowing a too-weak Stage A into Stage B as silently good.
6. **Broad regression**: HQ242 normalized digest `278854ee94fadfd57284a572441522fb56105081f89af431b17ec2e556ace6a9` vs Stage A `72d0a5ca347d71f207a77bca3609dfa5931a3c6f29224a2f3f860ebc3ab09ffe`; Stage A 2691 passed/45 failed/16 errors vs earlier 2691/45/7. Independently run exact same command and with/without Stage A test file, inventory 9 missing `pandas`, `pyarrow`, D07 harness collection errors, show whether Stage A adds any new errors. No installing optional dependencies or silently excluding tests to manufacture match; name true evidence ceiling.

**AUTHOR INDEPENDENCE:** write your own tiny hostile reproduction(s) and probes; do not just source author's attack helpers. Preserve source-only attack semantics; do not claim native T2 or all four F7 attacks are qualified.

## Disposition

- `F7_NATIVE_STAGE_A_INDEPENDENT_HOSTILE_RUNTIME_ACCEPTABLE__STAGE_B_MAY_CONTINUE_CANDIDACY`
- `F7_NATIVE_STAGE_A_INDEPENDENT_HOSTILE_RUNTIME_PARTIAL__NAMED_DEFECT`
- `F7_NATIVE_STAGE_A_INDEPENDENT_HOSTILE_RUNTIME_BLOCKED__MEMORY_SAFETY_OR_CUSTODY_INVALID`

Return ONLY under `WORKER_RETURNS/PYAT-HQ245-F7-NATIVE-STAGE-A-INDEPENDENT-HOSTILE-RUNTIME-REVIEW-R1/`:
- `00_REVIEW.md`
- `01_NATIVE_BUILD_ABI_SOURCE_BLOB_AND_MEMORY_SAFETY_AUDIT.json`
- `02_INDEPENDENT_HOSTILE_CUSTODY_AND_CRASH_REPRODUCTIONS.json`
- `03_FAIL_CAPABILITY_QUARANTINE_AND_BASELINE_DISCRIMINATION.json`
- `04_STAGE_B_SCOPE_DEFECTS_AND_BOUNDED_READINESS.json`
- `05_FINAL_DISPOSITION.json`

Commit/return only reviewed evidence, test scripts inside return directory if appropriate. Push and verify exact remote SHA. Never approve/merge production, never demand absent Stage B adjudicator as if Stage A claimed it, never count empty victim checks as completed F7-RR-04G.
