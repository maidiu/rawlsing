# PYAT991 S2-D — SAME G5 EXACT SOURCE-SCOPE DELTA RECHECK / HOLD_EXTERNAL

## 1. Exact artifact and delta

- Packet / old obligation: **S2-D / P2-05** (original #919, successor #991)
- Contract: `S2-D_PHASE1_USER_20261113.md@d7eaaf2363312af96e9bea02f6d85ae69a8cc47f`, SHA-256 `37d4b7e22035f97ec39bf72c57fbe944be215b3a7273a284a30fbafdf6a87da5`
- Protected base: `6a5c12f04323d74001f9632063ec907f4fc4468e`
- Accepted S2-C: `b7b697b69f0acea12174937ee824c19ac34ac284` / tree `dc416d1f23100d4d52b19bc2120226964bc0be43`
- Prior G5 return / cut: `a59db5e36f5b8c1d0149a1eb0ee6815d6cc96569` / `2b1f8d878e455b1f6ecb48683895b8a40dcbad72`
- Repair delivery / tested cut: **`5478210b7aeedf608a3e9754bf891d4d0262817f`**
- Branch / worktree: `agent/pyat991-s2d-g5-r1` / `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-g5`
- Reviewer session: `ses_e30c25800ffeT8XbyTuHekRCme`
- Model: `opencode-go/deepseek-v4.1-flash#max`
- Write allowlist: `WORKER_RETURNS/PYAT991_S2D_G5_RECHECK/` only. All product/tests/source/prior returns are read-only; no reviewer patch.

**Exact delta verified.** `2b1f8d..5478210` changes only:

- `pre553_saved_c11_admission.py` (+16/−1): private `_source_ref` derived from `estate.i02.source` via the existing `_ref_from_key`; exact source ref added to the allowed scope set alongside exact universe/release.
- new `test_pyat991_s2d_g5_source_scope.py` (+226, 3 tests).
- `WORKER_RETURNS/PYAT991_S2D_SOURCE_SCOPE_REPAIR/` return/evidence.

No shared Batch/issued/checkpoint/current/carrier/query/science/fate owner was edited. Exact blobs:

- repaired admission `10e1a13752f482406e47f3da45b83c10d7c5dd99`
- new source-scope test `ccad68294d9471d678ced5b43d68e623390654e0`
- prior admission `7d1807be4e25cad18a6d0890b9a563ee04204ea9`

## 2. Finding closure — G5-S2D-SCOPE-WHITELIST

The original G5 false refusal is **CLOSED_CORRECTED**.

**Before:** exact admitted `SOURCE_ARTIFACT` scope from `receipt.i02.source`:

- native owner I03: `SUPPORTED` denominator 2, fact `c2105164...`
- native saved-estate `CarrierNeutralResearchExecutor.execute_i03`: `SUPPORTED` same fact
- `SavedC11Admission.execute_i03`: **REFUSED** `saved consumer scope contains a foreign scope reference`

**After (same canonical G5 script, unchanged):**

- `defect=false`
- native owner I03: `SUPPORTED` denominator 2, fact `c2105164ca700da1e205185f5a27723c556c797ce7be5945350f3694f3fef3e8`
- native saved-estate I03: `SUPPORTED` same fact
- saved admission I03: **ACCEPTED** same fact/projection/ref
- base saved I03 control: `SUPPORTED` fact `064b866d646f7b7b9076842a3e26ee19df6262a1bd07a5e2e8ac87cd60955278`
- evidence: `evidence/recheck_scope.out`; historical before remains in `evidence/g5_scope_before_repair_historical.json`.

The repair derives the source ref from the **accepted estate’s exact I02 source root**, not a fixture tag or hash whitelist. No kind-wide permission was introduced.

**Foreign source split negatives** (independent `scope_foreign_split.py`):

- query-only foreign `SOURCE_ARTIFACT`: **REFUSED**
- predicate-only foreign `SOURCE_ARTIFACT`: **REFUSED**
- both `saved consumer scope contains a foreign scope reference`
- exact admitted source is accepted; a same-kind foreign source is not.

**I05 source scope:** the new test file covers exact admitted source scope on I05 atom predicates and query template with native candidate/fact/receipt parity; the full focused29 includes it and passes.

## 3. Tests

- Focused 29: **29 passed in 7.43 s** (prior 26 + 3 new source-scope tests).
- New source-scope file: **3 passed in 1.24 s**:
  - exact admitted source scope on I03 query+predicate;
  - foreign source refused;
  - exact admitted source scope on I05 discovery.
- Prior 26 and 172/19 author regressions are preserved historical evidence; no extra S2-F/S2-G/full matrix was rerun because the repair is a 16-line validation-only change.

The canonical G5 script was not edited. Only its proofroot/output location changed. Prior G5 historical bytes remain in the prior return.

## 4. Two-reader subresult and full packet

**Two-reader subresult qualified at `S2_SOURCEFREE_SAVED_I03_I05_ACTUAL`:**

- I03: actual cold `SavedC11Admission.execute_i03` → `CarrierNeutralResearchExecutor.execute_i03` → `execute_empirical_query`; base/change/restore/exact admitted source scope/refusals.
- I05: actual cold `SavedC11Admission.execute_i05` → `execute_exact_bounded_discovery`; base/change/restore/negative/valid-empty/mixed frontier/current/refusals.
- The source-scope false refusal is corrected. Foreign source/universe/release/authority, revoked current, wrong root and missing body remain refused.

**Full original S2-D remains HOLD_EXTERNAL.** Only two of seven real readers are actual:

| Reader | Status |
|---|---|
| I03 | **PASS_SCOPED_ACTUAL_COLD__EXACT_ADMITTED_SOURCE_SCOPE_CORRECTED** |
| I05 | **PASS_SCOPED_ACTUAL_COLD__EXACT_ADMITTED_SOURCE_SCOPE_PRESERVED** |
| Batch | **BLOCKED_OWNERSHIP** — `BatchExecutionRunner.__init__` |
| NORMAL | **BLOCKED_OWNERSHIP** — `execute_issued_workload` |
| COMPLETED | **BLOCKED_OWNERSHIP** — `resume_joined_workloads` / checkpoint |
| PARTIAL | **BLOCKED_OWNERSHIP** — `resume_joined_workloads` / checkpoint |
| ABSENT | **BLOCKED_OWNERSHIP** — `resume_joined_workloads` / checkpoint |

The five exact owner ACKs remain absent. The actual Batch guard and typed integration holds were already observed; they are not stubs presented as reader successes. No all-seven `ACCEPT_SCOPED` is available.

Additional holds: S1-D native I03 mixed-foreign-scope owner decision; S1-D production current/revocation; Q2/S1-E body-sink and postconsumer native fate join; S2-B G5-R1 recheck; original35/source science/rights; integrated 100k/6 GiB; new-module Linux run.

## 5. Resource / host qualification

The prior independent tiny-fixture resource evidence is inherited at exact source cut `2b1f8d`, with physical layout unchanged by this 16-line validation-only repair:

- retained `193,570 B`; peak root tree `193,570 B`; peak staging `28,672 B`
- 24 bounded object materializations
- source-extension opens parent/child `0`; full C11 builds `0`; whole-table fallbacks `0`
- parent RSS `112,869,376 B`; child RSS `52,043,776 B`
- cold I03/I05 `0.0158/0.0261 s`; repeat `0.0138/0.0265 s`
- 6 GiB cap PASS at fixture grade; integrated 100k/6 GiB **NOT_RUN**
- host: Darwin/macOS Python 3.11.3; new S2-D modules **not executed on Linux**. This is an explicit proof limit, not a new requirement. No process-tree benchmark or 100k claim.

## 6. Prior qualification correction

The prior G5 text’s “A-C01 receipt-fact conservation” phrase is **not** a current S2-D test or witness. It is removed from this delta qualification; the prior S2-G/S2-F A-C01 evidence remains historical and separate. No current S2-D test is cited for it.

## 7. Decision and next turn

**Overall verdict: `HOLD_EXTERNAL`.** The reported G5-S2D-SCOPE-WHITELIST is CLOSED_CORRECTED and the I03/I05 subresult is independently qualified; the full original S2-D packet cannot be accepted without the five exact shared-owner ACKs and actual readers. Integration `UNMERGED`; production current, original35/science, 100k/6 GiB and protected merge remain separate. Q2/Q3 goal not complete.

Return: `WORKER_RETURNS/PYAT991_S2D_G5_RECHECK/{receipt.json,00_HANDOFF.md,scope_foreign_split.py,evidence/}`.

HQ handles the next actual scope/owner ACK. No new A/B round, optional hardening, scope expansion, or reviewer patch. Stop finite.
