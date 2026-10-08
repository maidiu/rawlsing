# PYAT HQ246 — F7 NATIVE A/B MEMORY-BOUNDARY + TRUSTED-SEAM REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Space Bunny / OpenCode governed native engineering worker  
**MODEL / INTELLIGENCE:** Space Bunny Max preferred, confirm actual configured provider/model/variant before launch. **Not Browser/Sol.**  
**MACHINE:** User's governed macOS 13.7.8 x86_64, CPython 3.11.3, independent isolated sparse worktree using the ONE shared Git object store; no separate clone or shared concurrent checkout.  
**REPOSITORY:** `maidiu/rawlsing`  
**BRANCH:** `agent/space-bunny-pyat-hq246-f7-native-ab-memory-boundary-repair-r1`  
**BASE / IMMUTABLE STAGE B CANDIDATE:** `0dd0a503882ef777141092d7678285462214a600`  
**EXACT COMMISSION TIP:** verify the tip of THIS commission's commit on origin before work.  
**PERMITTED MUTATION:** only the quarantined `rawlsing_next/_p07_native_owner_stage_a.c`, `_p07_native_owner_stage_b.c`, directly corresponding new A/B synthetic unit/hostile tests/build recipes, and this commission's return directory.  
**FORBIDDEN:** production P07/F7 mutation or imports, accepted test weakening, work outside branch, root/issuer/model authority, real surveys, actor/V3/F8, production adoption/merge, self-certification, binary commits.

## Triggering facts — three HQ245 returns

1. **Independent DeepSeek Stage A HOSTILE REVIEW BLOCKED:** `agent/reviewer-pyat-hq245-f7-native-stage-a-independent-runtime-r1 @ 14432c2b21eaf87a8e92ecb75a6765cf3763ddc1`, disposition `F7_NATIVE_STAGE_A_INDEPENDENT_HOSTILE_RUNTIME_BLOCKED__MEMORY_SAFETY_OR_CUSTODY_INVALID`. Read `WORKER_RETURNS/PYAT-HQ245-F7-NATIVE-STAGE-A-INDEPENDENT-HOSTILE-RUNTIME-REVIEW-R1/` including runnable *original* reproducible evil-list constructor and ASAN probe. Its D1-D9 findings are binding hostile leads; they do not silently become Stage B passes.
2. **Space Bunny Stage B author return** `agent/space-bunny-pyat-hq245-f7-native-stage-b-full-p07-parity-r1 @ 0dd0a503882ef777141092d7678285462214a600`, disposition `F7_NATIVE_STAGE_B_FULL_P07_ADJUDICATOR_PARITY_READY__QUARANTINED_FOR_INDEPENDENT_REVIEW`. Quarantined 1802-line native adjudicator, 41 B +39 A +24 P07 +163 F7 reported green, byte-exact differential **tested corpus only**; conflict tie with two valid relation candidates untested; no `from_c11`, no production cutover.
3. **Independent HQ static-source verification of Stage B source at exact B tip:** `rawlsing_next/_p07_native_owner_stage_b.c` Git blob `2d8ffc686fcdb3f7108f0c8bafe7f60273fcf304`. Lines **827/829** use `PyList_Check/PyTuple_Check` (not Exact). Lines **850–851** call `PySequence_Size(relations/snaps)` invoking overridden subclass `__len__`. Lines **863–876** call `PySequence_Fast` and iterate `PySequence_Fast_GET_ITEM(fast,i)` for `i<n` or `i<m` **without deriving bound from `PySequence_Fast_GET_SIZE`**. This is the same unsafe length-to-array indexing pattern that DeepSeek ASAN-confirmed crashes Stage A. **Treat B as UNSAFE until actually reproduced/fixed independently**; do not claim author's 41 tests or past stress absolve it. Also Stage B lines 840–848 INCREF/pin trusted refs BEFORE fallible work, and 1785–1793 ignore `PyModule_AddObject` returns; audit repeated failed init, module init OOM, borrowed/stolen refs, GC cycles.

**HQ RULING:** This is a bounded *pre-adoption repair*, not another security architecture ruling. F7-RR-04G remains OPEN; HQ242 bounded T1 trusted-executable producer-grain warrant only. Stage A cannot be adopted as capsule-only final shape; Stage B has complete adjudicator candidate but none of it authorizes production until independent proof.

## Mandatory repair work

### A. Close memory-safety defects on *both* A and B

- `HQ245-D1`: no untrusted `PySequence_Size`/subclass `__len__` may supply a larger or smaller iteration/allocation bound than converted actual PySequence_Fast length. Either **exact builtins only** (`PyList_CheckExact/PyTuple_CheckExact`) plus C-API exact count, or defensive fully consistent lengths based on actual fast sequence after conversion. For list and tuple subclasses supply adversarial `__len__` returning greater, less, negative, huge, raising, reentrant and side-effecting; **relations and authority snapshots**; ensure every path refuses or processes actual safe length with no OOB/underflow/truncation.
- `HQ245-D2`: `custody_diagnostic` missing owned `Py_DECREF(rows)`, 20,000 calls leaked +20,000 tracked lists. Fix A; assess B's comparable diagnostics and refcount ownership. Check CAPI `Py_BuildValue` O vs N semantics, including source documentation.
- `HQ245-D3`: repeated failing `__init__` loses pinned `trusted_semantic_hash` and relations array. Fix A/B owner lifecycle, use transactional initialisation/cleanup, refuse reentry to dirty partly initialised owners or fully clean before retry, including `PySequence_Fast`, `admit_relation`, `admit_snapshot`, `compute_custody_hash` failures; prove callback refcounts remain bounded after 2k/20k retries.
- `HQ245-D4`: fix potential second `PyModule_AddObject` failure double-DECREF/dangling static exception, check **every** AddObject return, clear correct owned refs. Test or source-justify reliable OOM injection.
- `HQ245-D5`: fix/strictly bound cycles under native owner strong PyObject refs via GC traversal/clear OR prove truly impossible in allowed admission shape under hostile inputs. Do not assert impossible without a discriminating cycle and refcount test.
- `HQ245-D6`: Stage A's authority_registry=42 accepted/only tp_name retained; Stage A is NONAUTHORIZING but must represent its limited custody honestly or validate exact acceptable type and deep snapshot binding. B must validate and immutably pin snapshots actually used, not synthetic labels only. 
- `HQ245-D7`: Stage A `trusted_semantic_hash` stored but never called: either label Stage A as merely non-authorizing provenance and leave known-deficient but **do not put incomplete Stage A on any future authority path**, OR make exact Stage A trust seam meaningful without expanding positive authority. B must prove actual native-owned accepted semantic_hash/canonicalize/authority calls (no caller-rebindable aliases) and defend callbacks.
- `HQ245-D8`: Stage A only verifies ref.key/content_hash strings, not mutable semantic payload; no Stage A authority. Stage B's semantic_projection rehash is claimed fixed — verify with unchanged exact strings but mutated payload tests that deny, with typed, immutable production analogues too.
- `HQ245-D9`: broad normalized digest conflict: independent Stage A reviewer reproduced **accepted HQ242 54-item digest `278854ee94fadfd57284a572441522fb56105081f89af431b17ec2e556ace6a9`** with exactly nine environmental exclusions. Stage A author `72d0a5ca...` was not reproducible by reviewer (`52e07035...` for unexcluded case); Stage B author also claims `72d0a5ca...`. Run **the same accepted nine-exclusion command** and record canonical failing/error case set, and with/without A/B synthetic tests. Do not compare differently normalized/invoked runs or manufacture a digest match; explain author mismatch as needed.

### B. Preserve & upgrade full Stage B native P07 adjudicator parity

- Preserve accepted native custody hash, **true object key** rather than ref key, `semantic_projection` rehash, replay identity, whole decision ladder, authority-positive guards, exact original P07 exception types, exact error messages, canonical preimage and all declared scope/ordering fields.
- Stage B author correctly reported **17 reachable state strings across categories**, **six** actual ladder precedence entries (not blindly commission's '12'); verify all states and typed subgroups against pinned Python P07, including authority conflict and forbidden backfill. A **two independently valid relation candidates** synthetic fixture is needed to exercise `CONFLICTING_AUTHORITY`, precedence tie/order; **do not forge positive authority** to generate it. If needs an exact fixture source, supply permitted source-free constructor material or return a named independent positive-coverage blocker, don't claim untested paths pass.
- Native trusted Python seam `semantic_hash`, `canonicalize`, `require_positive_authority` is within TCB only if captured exact callable identities and validated immutable owner material, no live registry Python-positive delegation, no caller supplied fake trusted hash/positive-authority function; the temporary harness must mark what is assumed trusted vs demonstrated. Test replacement of module names, defaults, `__globals__`, registry internals as bounded T1 attacker cases without substituting trusted executable alias itself.
- Keep Stage B candidate in quarantined namespace, though it may generate AUTHORIZED **only within the test oracle**. No F7/P07 production path, no `from_c11` production API cutover. `from_c11` and accepted introspection-coupled tests remain explicitly Stage C gates. No automatic Stage C/Stage D dispatch based solely on your self-report.

### C. Independent court/fail capability

- Preserve original A 39 and B 41 tests; add distinct hostile negative cases and memory stress with author/independent original reproducer scripts; require **independently reproducible SIGSEGV-before/clean-no-segfault-after**, but don't run deliberate known-crashing baseline in the same process as production. Capture exit codes, ASAN where available. Test no silent truncation from underreporting.
- Real fault-injection A and B red cases, no `STAGE_A_FAULT_INJECT` or `STAGE_B_FAULT_INJECT_RESOLVE` in normal binary; record C source SHA-256, governed ABI, compiler build log and local-only normal binary SHA-256 (no `.so` in Git).
- Stage A extra fields admitted only if valid type; Stage B memory invariants sustained across malformed/reentrant inputs. Prove test count and no changed accepted tests/production files.
- Preserve current **four HQ234–HQ236 attacks and five HQD216 lawful F7 positives as later Stage D actual native/P07→F7 interface review**, no claim this repair closes them.

## Return and disposition

Write `WORKER_RETURNS/PYAT-HQ246-F7-NATIVE-AB-MEMORY-BOUNDARY-REPAIR-R1/`:
`00_RETURN.md`, `01_D1_OOB_AND_D2_D5_REFCOUNT_GC_PROOF.json`, `02_D6_D9_TCB_CUSTODY_AND_BASELINE_DISCRIMINATION.json`, `03_STAGE_B_PARITY_CONFLICT_AND_SECOND_POSITIVE_COURTS.json`, `04_NATIVE_ABI_FAIL_CAPABILITY_AND_NEGATIVE_CEILING.json`, `05_INDEPENDENT_REVIEW_REQUIRED_AND_CUTOVER_HOLDS.json`, `06_FINAL_DISPOSITION.json`.

Allowed:
- `F7_NATIVE_AB_MEMORY_BOUNDARY_REPAIR_READY__AWAITING_INDEPENDENT_HOSTILE_REVIEW` (only if real D1-D5 repairs and demonstrations)
- `F7_NATIVE_AB_REPAIR_PARTIAL__NAMED_MEMORY_OR_PARITY_BLOCKER`
- `F7_NATIVE_AB_REPAIR_BLOCKED__GOVERNED_RUNTIME_OR_ARCHITECTURAL_CONFLICT`.

On unexpected tip change, stop and report. Push/verify same branch exact remote HEAD and return SHA. Do not mutate control, production, accepted tests, old reviewer/author branches; do not self-adopt.
