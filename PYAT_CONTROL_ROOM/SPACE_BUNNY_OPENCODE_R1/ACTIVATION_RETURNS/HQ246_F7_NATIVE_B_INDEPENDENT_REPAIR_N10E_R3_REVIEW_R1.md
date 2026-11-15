# VOZHD PYAT HQ246 — THREE RETURNS, F7 NATIVE BLOCKING BOUNDARY, N10E R3 READY FOR INDEPENDENT REVIEW

**DECISION:** `HQD-2026-10-08-246`  
**DATE:** 2026-10-08 (America/New_York)  
**STATUS:** RATIFIED RETURN INTAKE & THREE BOUNDED SUCCESSOR COMMISSIONS. **NO F7 SECURITY / RUNTIME / N10E ISSUER / MODEL AUTHORITY ADOPTION.**

## I. Exact verified inputs

### A. Space Bunny / OpenCode F7 Stage B native complete adjudicator candidate

**BRANCH:** `agent/space-bunny-pyat-hq245-f7-native-stage-b-full-p07-parity-r1`  
**GITHUB RETURN HEAD:** `0dd0a503882ef777141092d7678285462214a600`  
**WORKER DISPOSITION:** `F7_NATIVE_STAGE_B_FULL_P07_ADJUDICATOR_PARITY_READY__QUARANTINED_FOR_INDEPENDENT_REVIEW`.  
**STATUS:** candidate only; NOT independently accepted.

Stage B built `rawlsing_next/_p07_native_owner_stage_b.c` **1802 lines** (Git blob `2d8ffc686fcdb3f7108f0c8bafe7f60273fcf304`), full native decide/require/replay and guarded exact lookup, accepted P07 custody hash and relation-object-key in place of Stage A FNV-1a and ref-key stand-ins. Captures trusted Python canonicalize/semantic_hash/require_positive_authority into C references. Reports **41 Stage B + 39 Stage A + 24 P07 +163 F7 PASS**. No production P07/F7 code or accepted tests changed, compiled binary not shipped, `PRODUCTION_INTEGRATED=0`; native `AUTHORIZED` only inside quarantined differential harness. Worker independently caught and repaired multiple native C reference bugs including EXC_BAD_ACCESS; implementation is not proof of memory safety.

**Known coverage holes:** multi-positive `CONFLICTING_AUTHORITY` and tie order unexercised, `from_c11` absent. The accepted P07 appears to have **17 reachable typed strings across categories**, six precedence ladder outcomes, not necessarily the historical commission phrase "12 decision states"; this must be settled by independent oracle census rather than forcing counts. Stage B self-reported broad digest `72d0a5ca...` but Stage A independent reviewer could not reproduce that digest; independent reviewer did reproduce accepted 54-item baseline `278854ee94fadfd57284a572441522fb56105081f89af431b17ec2e556ace6a9` with nine environmental exclusions.

### B. DeepSeek-Harness / OpenCode Stage A independent review — **BLOCKED**

**BRANCH:** `agent/reviewer-pyat-hq245-f7-native-stage-a-independent-runtime-r1`  
**GITHUB RETURN HEAD:** `14432c2b21eaf87a8e92ecb75a6765cf3763ddc1`  
**REVIEW DISPOSITION:** `F7_NATIVE_STAGE_A_INDEPENDENT_HOSTILE_RUNTIME_BLOCKED__MEMORY_SAFETY_OR_CUSTODY_INVALID`.

The reviewer reconstructed exact original macOS native binary SHA256 `94683dd76cfa9c4d76958ef14f006f97616e0b082b4510cbea38768a8047fd04` from committed A source and reproduced the Stage A C native `__init__` **out-of-bounds read / deterministic SIGSEGV exit 139, 3/3**, with ASAN READ on null pointer. `PyList_Check` admits subclass with overridable `__len__`; `PySequence_Size` used for element bound while `PySequence_Fast` underlying array can be shorter, and `PySequence_Fast_GET_ITEM` blindly indexes. Under-report likewise silently truncates. **`HQ245-D1` BLOCKING.** Additional named D2 custody_diagnostic unbounded list leak (+20k lists/20k calls); D3 failed repeated `__init__` trusted callable/rel-array leak (+2000 refs /2000 failures); D4 module-init OOM double DECREF; D5 GC cycles; D6 nominal registry binding; D7 dead hash seam in Stage A; D8 string identity check only, not payload; D9 author broad digest not reproducible as reported.

Reviewer independently reproduced A 39 and P07 24/F7 163 PASS and real red `-DSTAGE_A_FAULT_INJECT` control (2 RED). Native crashes invalidate security despite green counts. It reproduced **54-item historical digest** `278854ee94...` with same nine accepted environmental exclusions; 16 vs 7 error discrepancy stems from nine additional unexcluded collection errors and Stage A added ZERO. No source correction or adoption occurred on review branch.

### C. HQ independent STATIC SOURCE CHECK proves Stage B retains exact D1 class

At immutable Stage B blob `2d8ffc686fcdb3f7108f0c8bafe7f60273fcf304`, source lines **827–829** use `PyList_Check/PyTuple_Check` which admit malicious subclasses; **850–851** set `n,m = PySequence_Size(relations,snaps)` via attacker-overridable `__len__`; **863–876** call `PySequence_Fast_GET_ITEM` with `i<n`/`i<m` and no `PySequence_Fast_GET_SIZE` bounds. The same defect pattern independently caused A SIGSEGV. **Do not claim Stage B itself separately reproduced a crash yet**; instead BLOCK any Stage B acceptance as unsafe on static grounds pending B hostile runtime court.

Additional B trust boundary to adjudicate: constructible `StageBOwner` expects caller-passed trusted hash/positive callables; C pinning identity after construction is NOT independently competent provenance unless a future trusted owner-only construction ingress prevents caller injection. Stage B catches C callback and borrowed-ref issues itself but this seam requires independent hostility before authorizing production.

**HQ RULING F7:** Stage A review BLOCKED and exact B source continues unsafe pattern, so Stage B **NOT ACCEPTABLE FOR ADOPTION/INTEGRATION** and may not proceed as if Stage A green. Preserve Stage B substantive adjudicator code as candidate for repair. Commission independent original B hostile review AND separate Stage A/B bounded memory/refcount/custody repair on their own branches; fresh independent review of repaired candidate later. No production P07/F7 migration/Stage C automatic cutover. F7-RR-04G remains **OPEN**; original four HQ234–HQ236 forging attacks and five HQD216 lawful positive paths still demand later actual F7 path gates. HQ242 producer T1 trusted executable warrant unchanged; no T2/external receiver.

### D. Browser/Sol N10E AT07 R3 documentary correction candidate

**BRANCH:** `agent/rabochii-pyat-hq245-n10e-at07-warrant-r3-reference-correction-r1`  
**GITHUB RETURN HEAD:** `338aa789dd20d04c83175a6593172fee4b61c078`  
**WORKER DISPOSITION:** `C1_AT07_ISSUER_WARRANT_R3_DOCUMENTARY_CANDIDATE_COMPLETE__READY_FOR_INDEPENDENT_REVIEW` (NOT ADOPTED).

Corrected R3 canonical warrant path `PYAT_CONTROL_ROOM/C1_AT07_FIXTURE_ISSUER_WARRANT_HQ245_R3/01_BOUNDED_WARRANT_CANDIDATE_PREIMAGE.json` blob `d1c835119a08bb27124c87b15485d6b83b91659f`. The sole root and handoff normative contract pointers now target **existing** R2 return files with exact Git blobs `f0e05df99cc7ec8c3445b37e461fad86948f140e` and `a8c31625fcfb7bd65007e30ee2dda579d3b85e3e`, at frozen `cdef72ddc805e3ed943bac9f9241467454df8030`. R3 adoption-gates blob `af777fe3a6fda08d0b96a31d20ca91443fcb61d4` records HQ240 superseded→HQ241 PARTIAL→HQ242 R2 proposal→HQ244 PARTIAL→HQ245 R3 proposal→future independent review→only then separate HQ adoption. No self-hash in R3 commit. Preserves previous substantive root authority/mandatory handoff and 43 hostile / 10 positive **PROPOSED, NOT RUN** courts, source-free R8 100 only; no 19th I01 kind, issuer/root/credential/R4 activation or code changes.

**HQ RULING N10E:** R3 can be submitted to an **independent exact-SHA documentary hostile review**; positive adoption is forbidden until reviewer green and fresh explicit HQ decision. The two HQ244 documentary defects are author-claimed corrected and require independent verification.

## II. Three parallel successors

1. **F7 native A/B repair — Space Bunny/OpenCode Max, local Mac**: `agent/space-bunny-pyat-hq246-f7-native-ab-memory-boundary-repair-r1 @ c718020ffbcbfb047977e33d6fcc8bd6a241e4f0`. Exact commission `WORKER_COMMISSIONS/PYAT-HQ246-F7-NATIVE-AB-MEMORY-BOUNDARY-REPAIR-R1/00_COMMISSION.md`. Repair D1–D5 in both A+B, address D6–D9/evidence, true two-candidate parity and trusted constructor boundary; no production cutover; independent hostile re-review required.
2. **F7 frozen B independent hostile runtime — DeepSeek-Harness/OpenCode V4.1 Flash, distinct local Mac worktree**: `agent/reviewer-pyat-hq246-f7-native-stage-b-independent-hostile-r1 @ aca358d62e657c6d55369b86aadf85884b2402b6`. Exact commission `WORKER_COMMISSIONS/PYAT-HQ246-F7-NATIVE-STAGE-B-INDEPENDENT-HOSTILE-REVIEW-R1/00_COMMISSION.md`. Attack immutable original B native constructor and trusted-callable provenance, refcount/GC and parity; no author repair/review candidate mixing.
3. **N10E/C1 R3 independent issuer warrant review — Browser/GitHub Sol High**: `agent/reviewer-pyat-hq246-n10e-at07-warrant-r3-r1 @ 35c3cb14fe807fd0a21c41c859dfc252952ca9fc`. Exact commission `WORKER_COMMISSIONS/PYAT-HQ246-N10E-AT07-WARRANT-R3-INDEPENDENT-HOSTILE-REVIEW-R1/00_COMMISSION.md`. Verify SHA referents, adoption order and R2 conservation; no issuer/adoption.

## III. Holds

- **F7 Stage A hostile reviewer BLOCKED; B is not accepted, direct unsafe pattern remains.** No production P07/F7 adoption, no F7-RR-04G closure; no certified four forged negatives/five positives. Stage A and B branch source/test artifacts are evidence and candidates, not production.
- **N10E issuer R3 PROPOSED NOT ADOPTED.** No HQ-created issuer/root/credential or model rule R4, no new I01 authority kind. R3 documentation corrections do not grant operations.
- C1-01 R8 synthetic 100 source-free, Z08/A05 six states and actual-null effective context preserved; no real survey, downstream F8/actor/V3, N6 beyond local CONTEXT or OC05 currentness.

**NEXT:** `RUN_HQ246_F7_NATIVE_AB_REPAIR_AND_FROZEN_B_INDEPENDENT_HOSTILE_REVIEW_AND_N10E_R3_INDEPENDENT_REVIEW_IN_PARALLEL__INTAKE_ANY_RETURN`

**TERMINAL:** `PYAT_HQ246_A_BLOCKED__B_UNSAFE_PENDING_REPAIR_AND_HOSTILE_COURT__N10E_R3_UNADOPTED_READY_FOR_REVIEW`
