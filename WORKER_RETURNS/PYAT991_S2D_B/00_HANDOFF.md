# PYAT991 S2-D Phase 1 — Role B hostile corrective handoff

## Decision

**`IMPLEMENTED_I03_I05_REPAIRED__HOLD_SHARED_OWNER_ACK`**

This is a corrective B turn on A's same S2-D descendant. The accepted S2-C estate is still cold-readable through the existing native **I03** and **I05** owners. A's actual two-reader implementation is preserved and strengthened. The other five original readers — **Batch, NORMAL, COMPLETED, PARTIAL, ABSENT** — remain **BLOCKED_OWNERSHIP** pending the shared owner acknowledgement. There is no all-seven pass and no full S2-D completion claim.

B is the corrective author, not an independent G5.

## Exact artifact

- Branch: `agent/pyat991-s2d-b-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-b`
- Base / A delivery: `e399c48d576f5b2ae501dac569fb729e95bd968e`
- A implementation: `55af65cc1a2df1d3eb82906a80434353735c5d50`
- Accepted S2-C executable: `b7b697b69f0acea12174937ee824c19ac34ac284`
- Accepted S2-C tree: `dc416d1f23100d4d52b19bc2120226964bc0be43`
- Contract: `S2-D_PHASE1_USER_20261113.md@d7eaaf2363312af96e9bea02f6d85ae69a8cc47f`, SHA-256 `37d4b7e22035f97ec39bf72c57fbe944be215b3a7273a284a30fbafdf6a87da5`
- B code/test cut: `75e1521878ee1e4d4d661d8fdae6b80944d07f6c`
- Git blobs:
  - A admission: `2f2f53639f61c0ef0feacd8775d0d383e9db5e03`
  - B repaired admission: `721029ca35c389885423719c3b17345565257f1a`
  - B adversarial test: `25cefde8310c5d4754090b755e9af28679213703`
  - A saved integration: `fd3fa4378d2c15f85ee1fa0f68714307bc1de54c` (unchanged)
- Changed code/test files:
  - `rawlsing_next/pre553_saved_c11_admission.py`
  - `rawlsing_next/tests/test_pyat991_s2d_b_adversarial.py`
- A's `pre553_saved_workload_integration.py` remains unchanged; A's tests and A return files remain unchanged.
- All accepted S2-C/native/shared owner files remain read-only.

## Independently verified A strengths

A's core claim survives examination:

- Actual cold I03 reads the accepted `VerifiedDirectEstate` through `CarrierNeutralResearchExecutor.execute_i03` and the existing `execute_empirical_query` semantics.
- Actual cold I05 uses the existing `execute_exact_bounded_discovery` owner over the accepted `DirectEstateI03Session`.
- Fresh-process I03/I05 reconstruct the native facts, receipts and replay material without source or a `C11Repository` graph.
- A's supported fact, changed/restored I03, revoked-current/wrong-root/missing-body and Batch-guard tests pass unchanged.
- A honestly disclosed the five owner holds and the TEST_ONLY current boundary.

A's artifact was capable. It was not terminal.

## Established defects and repairs

### B-D1 — Mutable admission could retarget the served estate (SEV-1)

At A's cut, `SavedC11Admission` exposed mutable `estate`, `release_ref`, `runtime_catalog` and `_executor`. Assigning them after construction let the same admission serve a different exact estate/release. The A-cut RED accepted the retarget:

- base fact: `311b0d12d70d9ed9cd0e825ae227607775f2a791fe542d6215be9ce5c32e4dea`
- retargeted fact: `20827d0ed6585f758b1dd48a57dfa43809f208036c0fd341c9f6099e41dc4e91`

Repair:

- `SavedC11Admission` now uses private slots, freezes after initialization and rejects normal field reassignment with `SavedC11AdmissionError("saved admission binding is immutable")`.
- A direct-constructor estate is re-verified into a private reader, so mutating the caller-held estate or its authorizer after construction cannot retarget the admission.
- The runtime catalog is copied into a private immutable binding; `open()` uses the just-verified private estate fast path.
- GREEN: B refuses the retarget and the base fact is restored exactly to `311b0d12...`.

### B-D2 — Mixed-scope I03 query/predicate returned a positive (SEV-1)

At A's cut, I03 checked the query's `empirical_universe_refs` but not exact `scope_refs`. A query named the estate universe plus a foreign universe in scope and still returned **SUPPORTED**. A predicate with an extra foreign scope had the same class of gap.

This is a real mixed-source positive at the saved first reader. The native full-repository I03 also accepts that query; that separate native-owner gap is recorded below and was not edited.

Repair:

- I03 and I05 now require query and predicate scopes to equal exactly the admitted estate universe.
- GREEN: mixed-scope I03 refuses with `saved consumer query scope is not the exact admitted estate universe`; the predicate variant refuses similarly. Valid base I03 remains exact.

### B-D3 — Mixed-universe I05 authority was not hard-refused (SEV-1)

At A's cut, an I05 discovery authority from a foreign universe returned a `COVERAGE_LIMITED` receipt with `UNAVAILABLE` facts. It was not a positive, but it was a typed fallback where exact source-scope refusal is required. The A-cut RED is recorded as `COVERAGE_LIMITED` / `UNAVAILABLE`.

Repair:

- I05 now preflights every discovery atom predicate, every query template and the authority source-universe scope against the admitted estate before executing.
- GREEN: the foreign authority raises `SavedC11AdmissionError`; valid base I05 receipts remain exact.

### B-D4 — I05 changed/negative/frontier and measurement evidence were missing (SEV-2)

A did not independently execute I05 changed/restore, zero/valid-empty I05, mixed supported/valid-empty frontier, I03 zero support, or measured source-open/materialization counters. The binding receipt's zero counters were declared constants, not measurements.

Repair/evidence:

- Added B tests for changed I03/I05 and exact restore, I03 zero support, I05 negative/valid-empty, I05 mixed supported+valid-empty frontier, I05 current revocation and restore, and fresh-process I03/I05 with `C11Repository.__init__` / `pq.read_table` tripwires.
- Added `counter_status = "DECLARED_ZERO__NOT_A_MEASUREMENT"` to the binding receipt, while separately measuring source opens, materializations, C11 builds and whole-table fallbacks.
- GREEN: 24 focused S2-D tests pass; 153 S2-G and 19 S2-F regressions pass; the resource probe reports 0 source-extension opens, 0 C11 builds, 0 whole-table fallbacks, 24 bounded materializations.

## RED at A → GREEN at B → restoration

Script: `WORKER_RETURNS/PYAT991_S2D_B/repro_a_defects.py`  
Machine JSON: `WORKER_RETURNS/PYAT991_S2D_B/a_red_b_green.json`

A's original module is loaded unchanged from `e399c48...` via `git show`, not edited.

| Case | A cut | B cut |
|---|---|---|
| Mixed-scope I03 | accepted `SUPPORTED` | refuses exact query scope |
| Mutable admission I03 | retarget accepted, changed fact served | refuses immutable binding; base fact restored |
| Mixed-universe I05 | `COVERAGE_LIMITED` / `UNAVAILABLE` | refuses exact predicate/source scope; base I05 exact |

Native full-repository I03 still returns `SUPPORTED` for the mixed-scope query. That is an exact **S1-D/native I03 owner** hold; B's saved adapter refuses it but does not edit the native owner.

## Proof of improvement

### Focused S2-D

Command:

```text
python3 -m pytest \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pyat991_s2d_saved_admission.py \
  rawlsing_next/tests/test_pyat991_s2d_b_adversarial.py \
  -q -o addopts=''
```

Result: **24 passed in 6.40s** (15 A + 9 B).

### Inherited regressions

- S2-G: **153 passed in 45.46s**
- S2-F: **19 passed in 8.01s**

Logs are in `WORKER_RETURNS/PYAT991_S2D_B/`.

### Actual fixture resources

Measured by `WORKER_RETURNS/PYAT991_S2D_B/resource_probe.py` on the synthetic 2-respondent/2-event fixture, not 100k:

| Measure | Value |
|---|---:|
| Retained estate disk | `193,570` B |
| Peak estate root | `193,570` B |
| Peak temporary staging | `28,672` B |
| Bounded object materializations | `24` |
| Source-extension opens, parent | `0` |
| Source-extension opens, fresh child | `0` |
| Full C11 repository builds | `0` |
| `pq.read_table` whole-table fallbacks | `0` |
| Cold I03 / repeat | `0.0151` s / `0.0135` s |
| Cold I05 / repeat | `0.0255` s / `0.0273` s |
| Parent peak RSS | `107,683,840` B |
| Fresh-child peak RSS | `54,824,960` B |
| 6 GiB cap | PASS at fixture grade |
| Integrated 100k/6 GiB | **NOT_RUN** |

The fresh child receives only external manifest/I02/release pins and public preimages; it exits successfully with exact I03/I05 facts, receipts and replay refs. Estate Parquet reads are expected; “source opens” counts original-source extensions only. `C11Repository.__init__` and `pq.read_table` are forbidden during both parent and child saved consumers.

## Seven-reader status

| Reader | Actual first reader | Status |
|---|---|---|
| I03 | `SavedC11Admission.execute_i03` → `CarrierNeutralResearchExecutor.execute_i03` → `execute_empirical_query` | **PASS_SCOPED_ACTUAL_COLD** |
| I05 | `SavedC11Admission.execute_i05` → `execute_exact_bounded_discovery` | **PASS_SCOPED_ACTUAL_COLD** |
| Batch | `BatchExecutionRunner.__init__` | **BLOCKED_OWNERSHIP** |
| NORMAL | `execute_issued_workload` | **BLOCKED_OWNERSHIP** |
| COMPLETED | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |
| PARTIAL | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |
| ABSENT | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |

Batch still actually refuses the admission at the existing `C11Repository` guard. The five integration functions still raise exact typed owner holds. No guard was monkeypatched, no fake repository was substituted and no shared file was edited.

## G1–G5 at this cut

- **G1:** PARTIAL. Exact I03/I05 estate/release/catalog binding and source scope; five readers blocked.
- **G2:** PARTIAL. Actual cold I03/I05, changed/restored native facts, negative/mixed frontier and fresh process; five readers blocked.
- **G3:** PARTIAL. I03/I05 hostiles include mutable binding, mixed source scope/universe, revoked current, wrong roots, missing body; five-reader negatives blocked.
- **G4:** PARTIAL. Actual fixture I03/I05 resources measured; Batch/resume resources and integrated 100k/6 GiB NOT_RUN.
- **G5:** NOT_RUN. B is not G5; a distinct nonauthor reviewer is required after A's bounded counter.

## Challenges tested and rejected

- **Claim: A's moved I03/I05 outputs are just a mock or in-memory substitute.** False. The tests use the accepted S2-C physical estate and fresh processes; C11 graph and whole-table fallbacks are tripwired.
- **Claim: The saved I05 path is only a replay of a precomputed fact.** False. Changed native rows produce changed I05 receipts/replay/facts; exact restore reproduces the base identities.
- **Claim: The five typed refusals are hidden all-seven passes.** False. They remain `BLOCKED_OWNERSHIP`; the Batch guard and typed owner holds are executed.
- **Claim: A's supported parity is invalid because negatives differ.** A's supported/zero/negative lawful paths match. The mixed-universe input is now hard-refused before the S2-C session can emit a divergent fallback.

## New attack surfaces created or exposed

- The saved adapter is stricter than the native full-repository I03 for a mixed-scope query. That aligns with the S2-D source-scope requirement, but the native owner still needs its own exact scope check.
- The admission freeze is a Python-level binding guard. `object.__setattr__` or constructing a new admission with different external pins can still bypass it; the external independent pin/current callback remains the trust anchor.
- The private-estate re-verification is performed on direct construction; `open()` uses the estate it has just constructed and verified. A hostile host that mutates estate files after open remains bounded by the accepted S2-C row/body checks, not by a per-call whole-estate rehash.
- The new exact-scope preflight rejects mixed-scope inputs but does not repair the native owner's acceptance; that remains a shared-file HOLD.

## Surviving disagreements and external holds

1. **Five shared readers:** exact owner ACK for `pre553_batch_runner.py` and `pre553_issued_workload.py` is absent. This is a real `BLOCKED_OWNERSHIP`, not a solved capability.
2. **Native I03 mixed-scope positive:** `execute_empirical_query` still accepts a query whose `empirical_universe_refs` name the estate but whose `scope_refs` also name a foreign universe. B's saved adapter refuses it; the native owner edit is outside this grant.
3. **Production current/as-of/revocation issuer:** absent; only the TEST_ONLY callback is used.
4. **Q2/S1-E body-sink and postconsumer fate join:** not present in the accepted S2-C tree.
5. **S2-B G5-R1 independent recheck:** outstanding; not claimed.
6. **Original35/source science/rights:** not read or claimed.
7. **Integrated 100k respondents / 6 GiB:** NOT_RUN.
8. **Distinct S2-D G5:** NOT_RUN. A's bounded counter must precede it.

## Challenge to Agent A

Preserve the two actual readers and the five honest holds. Do not accept the native mixed-scope positive as solved because B's adapter refuses it; either obtain the exact S1-D/native owner edit or record the precise HOLD. Then perform one bounded counterattack on this exact code cut:

- Attack the private/frozen admission through a caller-held estate/release/catalog/preimage swap; try to make the admission serve a different exact estate after construction.
- Attack the exact-scope preflight with a query/predicate whose `empirical_universe_refs` match the estate but whose dependency or scope provenance names a foreign universe or release.
- Attack I05 with a multi-candidate frontier where one candidate is supported and another is zero/valid-empty, and with current revocation between the first and last candidate.
- Keep the five reader holds; a typed refusal is not an all-seven pass.
- If a shared-owner ACK arrives, integrate only the exact granted files and preserve the accepted S2-C reader/session and existing native I03/I05 owners.

## Bounds

- sourcefree TEST_ONLY engineering only.
- No original35, source science, production CURRENT, issuer, rights, full source-to-C11 join or protected merge.
- No Batch/NORMAL/COMPLETED/PARTIAL/ABSENT claimed.
- No 100k/6 GiB integrated claim.
- No independent G5 claim.
- Integration: UNMERGED.
- Known session cost: UNKNOWN.
- Stop: terminal. No poll/sleep/autowake.
