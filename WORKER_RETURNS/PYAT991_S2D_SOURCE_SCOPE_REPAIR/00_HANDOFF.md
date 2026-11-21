# PYAT991 S2-D — exact source-scope G5 correction

## Result

**Local correction complete; same independent G5 delta recheck pending.**

- G5 finding: `G5-S2D-SCOPE-WHITELIST` — a valid native I03 request carrying the **exact admitted SOURCE_ARTIFACT** scope was falsely refused by `SavedC11Admission`.
- Fix: derive the exact admitted source artifact from the accepted estate’s `receipt.i02.source` and allow only that exact source, the exact admitted universe and the exact admitted release in scope.
- Foreign source, foreign universe, foreign release and foreign authority scope remain refused.
- Full original S2-D remains **OPEN**: only I03/I05 are actual; Batch, NORMAL, COMPLETED, PARTIAL, ABSENT remain **BLOCKED_OWNERSHIP**.
- The same distinct nonauthor G5 must receive this delta; A does not self-accept.

## Exact artifact

- Branch: `agent/pyat991-s2d-a-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-a`
- Startup / G5 delivery: `a59db5e36f5b8c1d0149a1eb0ee6815d6cc96569`
- G5 tested cut: `2b1f8d878e455b1f6ecb48683895b8a40dcbad72`
- B code cut: `75e1521878ee1e4d4d661d8fdae6b80944d07f6c`
- Accepted S2-C: `b7b697b69f0acea12174937ee824c19ac34ac284` / tree `dc416d1f23100d4d52b19bc2120226964bc0be43`
- Contract: `S2-D_PHASE1_USER_20261113.md@d7eaaf2363312af96e9bea02f6d85ae69a8cc47f`, SHA-256 `37d4b7e2…`

Changed paths only:

- `rawlsing_next/pre553_saved_c11_admission.py`
- `rawlsing_next/tests/test_pyat991_s2d_g5_source_scope.py`
- `WORKER_RETURNS/PYAT991_S2D_SOURCE_SCOPE_REPAIR/`

No shared Batch/issued/checkpoint/current/carrier/query/science/fate owner was edited. The prior A/B returns are untouched. The known dirty `WORKER_RETURNS/PYAT991_S2D_B/a_red_b_green.json` was preserved uncommitted and not staged or copied as canonical.

## Canonical G5 witness — before and after

The G5 witness was reproduced unchanged; only its proofroot/output location was changed. The admitted source scope is derived from the actual estate root, not hardcoded.

Canonical output before repair:

```text
defect = true
native I03:            SUPPORTED denominator 2
native saved-estate:   SUPPORTED same fact
saved admission:       REFUSED
error: saved consumer scope contains a foreign scope reference
fact: c2105164ca700da1e205185f5a27723c556c797ce7be5945350f3694f3fef3e8
```

Canonical output after repair:

```text
defect = false
native I03:            SUPPORTED denominator 2
native saved-estate:   SUPPORTED same fact
saved admission:       ACCEPTED same fact
base saved I03:        SUPPORTED fact 064b866d...
```

Exact admitted source scope from the witness:

- kind `SOURCE_ARTIFACT`
- object `SOURCE-G5-ADMITTED-SOURCE-SCOPE`
- hash `ab4de5365b5eb12a8592d54898ddde47b0c0c5c542378767e2f5f7d8f0a3e0cf`

Product derivation: `estate.i02.source` → exact `ExactRef` via the existing `_ref_from_key`; no fixture tag/hash whitelist in product code.

## Repair

`SavedC11Admission` now stores the exact admitted source artifact with the admitted universe and release. `_require_exact_scope_refs` permits exactly:

- every `EmpiricalUniverse@1.0.0` scope ref = admitted universe;
- every `C11LogicalRelease` scope ref = admitted release;
- the exact admitted `SOURCE_ARTIFACT` ref;
- no other scope ref.

B’s immutable/private binding, exact-release repair, mixed foreign-universe I03 refusal, mixed-universe I05 refusal, current revocation, changed/restore, zero/valid-empty/mixed frontier and fresh-process tests are preserved.

## New focused tests

`rawlsing_next/tests/test_pyat991_s2d_g5_source_scope.py`:

1. exact admitted source scope on I03 query **and predicate** → exact native fact/projection/ref parity;
2. foreign source scope on I03 → refused;
3. exact admitted source scope on I05 atom predicates and query template → exact native discovery/fact/receipt parity.

Command:

```text
python3 -m pytest \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pyat991_s2d_saved_admission.py \
  rawlsing_next/tests/test_pyat991_s2d_b_adversarial.py \
  rawlsing_next/tests/test_pyat991_s2d_a_counter.py \
  rawlsing_next/tests/test_pyat991_s2d_g5_source_scope.py \
  -q -o addopts=''
```

**29 passed in 7.82s** (prior 26 + 3 new source-scope tests).

Prior evidence remains valid: 172 focused/owner regression and 19 S2-F passed at the prior cut; the local scope-only correction did not require a complete S2-G/S2-F rerun. No 100k benchmark was run.

## Resource boundary

The independent G5 fixture resource evidence remains the current honest grade:

- retained `193,570` B, peak staging `28,672` B, 24 bounded materializations;
- source opens parent/child `0`, full C11 builds `0`, whole-table fallbacks `0`;
- parent RSS `112,869,376` B, child RSS `52,043,776` B;
- integrated 100k / 6 GiB **NOT_RUN**.

The source-scope repair changes only exact-ref validation in the new adapter; it does not change physical layout or resource behavior.

## Seven-reader status

| Reader | Status |
|---|---|
| I03 | **PASS_SCOPED_ACTUAL_COLD__EXACT_ADMITTED_SOURCE_SCOPE_REPAIRED** |
| I05 | **PASS_SCOPED_ACTUAL_COLD__EXACT_ADMITTED_SOURCE_SCOPE_PRESERVED** |
| Batch | **BLOCKED_OWNERSHIP** — `BatchExecutionRunner.__init__` |
| NORMAL | **BLOCKED_OWNERSHIP** — `execute_issued_workload` |
| COMPLETED | **BLOCKED_OWNERSHIP** — `resume_joined_workloads` / checkpoint |
| PARTIAL | **BLOCKED_OWNERSHIP** — `resume_joined_workloads` / checkpoint |
| ABSENT | **BLOCKED_OWNERSHIP** — `resume_joined_workloads` / checkpoint |

The five exact shared-owner ACKs remain absent. No guard was monkeypatched, no fake C11 repository was constructed, and no all-seven claim is made.

Additional holds remain: S1-D production current/revocation; S1-D/native I03 foreign-universe scope decision; Q2/S1-E body-sink and postconsumer fate join; S2-B G5-R1 recheck; original35/source science/rights; integrated 100k/6 GiB; distinct S2-D G5 acceptance.

## Self-critique

- Only I03/I05 are actual; the correction is not full S2-D.
- The scope allowance is deliberately limited to the exact admitted source/universe/release; other exact scope metadata remains conservatively refused. A foreign source hidden in an unrecognized scope kind should be tested by the same G5.
- The native full-repository I03 still accepts a foreign-universe scope positive; that is an external native owner hold, not solved by this adapter fix.
- Current remains TEST_ONLY; the Python binding freeze is not hostile process isolation.
- New modules were not executed on Linux; resource evidence is the prior independent fixture, not 100k.
- The reviewer’s stray A-C01 receipt-fact phrase was not treated as current S2-D evidence and no task was invented from it.

## Next actor

Same independent G5 `ses_e30c25800ffeT8XbyTuHekRCme` should perform a bounded delta recheck of the exact source-scope repair, then issue the appropriate scoped/HOLD decision. Full all-seven acceptance remains unavailable while the five ownership holds remain. No new A/B round or self-acceptance.
