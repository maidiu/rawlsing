# PYAT R3 — PE reversed-issuer and V2K original-identity sourcefree recovery

**Role:** independent source-code forensic and scientific-contract repair engineer. Not PRE-MAIN integrator, source/semantic issuer, original reviewer or own hostile reviewer.

**Repository:** `maidiu/rawlsing` (private). **Branch:** `agent/pyat-r3-pe-v2k-stranded-scope-repair-20261031-r1`. **Startup:** `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3`. **Current PRE-MAIN at audit close:** `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`; PE/V2K relevant paths unchanged between the two cuts, while `pre553_issued_workload.py` is the same blob `31e84f49...`.

**Executor/capability:** OpenCode / `opencode-go/deepseek-v4.1-flash` (DeepSeek V4.1-Flash). MAX requested; actual effort not independently observable. Isolated worktree; no existing PE/V2K worktree displaced. No model/harness switch.

**Write scope:** only `WORKER_RETURNS/PYAT-R3-PE-V2K-SCOPED-RECOVERY/`. No PRE-MAIN, production source, actor/science permission or merge was modified.

## FINDING

### 1. PE `_auth` reversed-issuer defect is repaired at candidate scope

Original PE `e61a26ce...`, blob `58484f4c3d9aae148d4116dcf00420c432aefcbd`. The defect was that role-reversal acceptance checked only non-null caller authority shape. The candidate adds exact issuer-registry dereference of a `TARGET_USE_PERMISSION` snapshot, requiring the reverse operation, target use and denominator/risk scope. `_auth` remains shape normalization only.

**Actual receipts:**
- Original author suite: **21 passed**.
- Original independent strict: **4 passed / 9 failed**, including reversed issuer-scope forgery.
- Repaired candidate author suite: **21 passed** (with exact reversal authority snapshot registered in the sourcefree fixture).
- Repaired candidate independent strict: **5 passed / 8 failed** (only the module blob pin changed to repaired candidate; all assertions unchanged). The reversed-issuer forgery now refuses.
- Candidate-specific competence test: **2 passed**.

The remaining eight strict failures are SC0 value-bearing/schema requirements (`clocks`, `scoped_status_rows`, `structural_publication_refresh_receipt`, `n9_values_read_receipt`, `generic_consumers`, N9/F2/AH strata). They are preserved. The whole PE contract remains **DEFECTIVE_BLOCK / HOLD**, not READY.

### 2. V2K dependency lineage is restored only in isolation; current ABI is not compatible

Original V2K `694fb450...`, source `e3ef9a2469966b8ecfbcd178b971f54c687aef22`. Exact historical dependency blobs restored in the isolated test tree:

- contract `08bb75c431d3352cb0d17e9a65f7d855b4d35e59`
- binder `7d8b3902c3f8f257637b7c07ad9feb5e096d48e5`
- durable consumer `dc146e920909c8577b5c3c316cd9a8631e96ffd8`
- verifier `996c8e907f2befde93af09b60154b610c1ffeb63`
- checkpoint `719c8d878bcfb3b6c61c844c9bf974ada8365929`
- dependency test helpers `0b9f1add...`, `3218f280...`

Current `rawlsing_next/pre553_issued_workload.py` at `5fc1d43e...` blob `31e84f49...` is a **different native workload admission/execution interface** (`NativeWorkload`, `IssuedWorkloadRecord`, `CurrentDecisionResolver`, `admit`, `execute_issued_workload`). It has no `V2ExpectedWorkDeclaration`, `v2_bind_semantic_to_dispatch` or `V2_SCHEMA_VERSION`. It is not a drop-in V2K successor and was not transplanted.

**Actual receipts:**
- Four V2K suites with exact dependency restored: **63 passed**.
- 24-test candidate suite: **24 passed**.
- Exact dependency/owner suites: **50 passed / 1 failed**; the failure is the source-cut check `test_no_accepted_owner_modifications` comparing current tree to historical commit, not a V2K semantic failure.
- Without exact dependency: **collection error**, not green.
- The 111-test owner aggregate is **not available as one exact suite** at this cut; no 111/111 claim.
- Negative dependency-severance tests: **2 passed**.

V2K remains `SCIENCE_HOLD` / `INSUFFICIENT_EVIDENCE`; foreign issuer and removed-held-row acceptance remain unadopted. No current consumer or native source authority.

### 3. Current first consumers

- PE repaired candidate: branch-local `tests/test_pe_reversed_issuer_repair.py`; original PE author/independent suites. No PRE-MAIN consumer.
- PE whole contract: branch-local PE courts only; blocked by 8 strict SC0 gaps.
- V2K: branch-local V2K four suites only; exact historical dependency restored only in isolation. No current consumer.
- Current issued workload: a distinct current native API, not a V2K consumer.

### 4. Source/authority boundary

No source-native read, original U/E, scientific rule, model-use, N9/N10W operative world, N11/N12, Sorok actor or production permission is issued. Sourcefree tests are allowed and were run. No self-issued authority, self-review, PRE-MAIN mutation or merge.

## INTERPRETATION

The PE reversed-issuer defect is real and now closed at candidate scope; the whole PE contract is still incomplete because strict SC0 value-bearing fields are absent. V2K was never a current implementation: its exact dependencies are stranded, and current `pre553_issued_workload.py` is a different contract. Restoring the old dependency is valid only for sourcefree historical replay, not for current integration. Both remain sourcefree candidates/evidence, not production or native science.

## HQ ACTION

1. Preserve the PE candidate repair and 8 strict failures; do not merge PE.
2. Route PE `_auth`/SC0 gaps to the original PE/SC0 owner for a decision on full contract repair.
3. Preserve V2K exact dependency restoration as historical evidence; route current-ABI adaptation or retirement to the original U/E/V2K owner.
4. Require independent I3 hostile review at exact SHA before any canonical integration.
5. Do not claim 111/111 V2K or PE READY.

## OWNER

Original PE/SC0 source owner, original V2K/U/E/source owner, incumbent Pyat/HQ intake, and a distinct I3 reviewer. No self-review.

## Three courts

- **ENGINEERING:** `PE_AUTH_REPAIRED_AT_CANDIDATE_SCOPE__WHOLE_PE_RED_BY_8_SC0_GAPS__V2K_HISTORICAL_63_PASS_WITH_EXACT_DEPENDENCY__NO_CURRENT_ABI`.
- **SCIENCE:** `HOLD__NO_ORIGINAL_SOURCE_OR_SCIENTIFIC_ISSUANCE`.
- **AUTHORITY:** `HOLD__SOURCEFREE_CANDIDATE_ONLY__NO_ADOPTION__NO_MERGE`.

## Actual tests

Sourcefree isolated pytest only:

- PE original author 21 passed; PE original independent 4/9.
- PE repaired author 21 passed; repaired independent 5/8; candidate competence 2 passed.
- V2K four suites 63 passed; 24-test candidate suite 24 passed; dependency/owner 50 passed/1 source-cut failed; missing dependency collection error.
- Negative dependency-severance 2 passed.
- No full K9/K10, 111 aggregate, native source, actor/world, or PRE-MAIN integration test.

## DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

**DONE:** exact PE/V2K source and dependency lineages; PE reversed-issuer repair and receipts; V2K exact dependency restoration and receipts; negative dependency-severance; sourcefree candidate code/tests; current ABI comparison.

**REMAINING:** PE whole-contract SC0 gaps; V2K current ABI/consumer decision; original owner review; independent I3 review.

**BLOCKERS:** 8 strict PE failures; V2K no current compatible ABI/consumer; 111 aggregate unavailable; foreign issuer/held-row unadopted; no source/native/science/actor permission.

**LARGEST PRODUCTIVE MOVE:** PE owner repairs the 8 SC0 value-bearing fields or explicitly retires the whole contract; V2K owner chooses exact historical dependency preservation vs a new current ABI adapter. Then one independent I3 reviewer reruns exact assertions.

**FLIGHT:** `PE_AUTH_REPAIRED_SCOPED + WHOLE_PE_HOLD + V2K_HISTORICAL_RESTORED_ONLY + CURRENT_ABI_MISMATCH + NO_ADOPTION`.

**DELTA:** `+` exact PE `_auth` repair and actual receipts; `+` V2K dependency restoration and 63-pass receipt; `+` negative severance and current-ABI mismatch; `+` minimal sourcefree code/tests; `−` no whole PE/V2K production acceptance; `−` no source/science/actor grant; `−` no merge.

## Return artifacts

- `00_RETURN.md`
- `FUNCTION_ORIGIN_AND_SUCCESSOR_MAP.jsonl`
- `TEST_POSITIVE_AND_FAULT_NEGATIVE.md`
- `SCIENCE_AUTHORITY_AND_CONSUMER_MAP.md`
- `INTEGRATION_PLAN.md`
- `candidate/pre553_postastra_pe_generic_world_possibility.py`
- `candidate/PE_AUTH_REPAIR.diff`
- `candidate/PE_TEST_FIXTURE_AUTHORITY.patch` (sourcefree test fixture registration only)
- `candidate/V2K_DEPENDENCY_RESTORATION.json`
- `tests/test_pe_reversed_issuer_repair.py`
- `tests/test_v2k_dependency_severance.py`

**Exact immutable pushed remote SHA:** reported after push/readback; self-reference excluded. Post-return independent I3 hostile review required before canonical integration.
