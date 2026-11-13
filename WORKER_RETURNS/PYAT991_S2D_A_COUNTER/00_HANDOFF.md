# PYAT991 S2-D Phase1 — A bounded final counter

## Decision

**`BLOCKED_OWNERSHIP` / `IMPLEMENTED_I03_I05_REPAIRED__HOLD_SHARED_OWNER_ACK`**

B’s corrective repair is preserved. The actual cold **I03** and **I05** saved readers remain green, and B’s mixed-foreign-universe/release refusals remain in force. A new counterexample found one over-narrow B rule: B required the entire query/predicate `scope_refs` set to equal `{admitted universe}`, rejecting a lawful **admitted-release** scope reference that the actual native I03 first reader accepts. I repaired that only in the S2-D saved-admission module.

The five remaining readers — **Batch, NORMAL, COMPLETED, PARTIAL, ABSENT** — remain **BLOCKED_OWNERSHIP**. There is no all-seven pass and no full S2-D completion claim.

## Exact artifact

- Branch: `agent/pyat991-s2d-a-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-a`
- Startup / B delivery: `b23d85428e4cd0180231fd7e35727c771de18cab`
- B code cut: `75e1521878ee1e4d4d661d8fdae6b80944d07f6c`
- A prior delivery: `e399c48d576f5b2ae501dac569fb729e95bd968e`
- A prior implementation: `55af65cc1a2df1d3eb82906a80434353735c5d50`
- Accepted S2-C executable: `b7b697b69f0acea12174937ee824c19ac34ac284`
- Accepted S2-C tree: `dc416d1f23100d4d52b19bc2120226964bc0be43`
- Contract: `S2-D_PHASE1_USER_20261113.md@d7eaaf2363312af96e9bea02f6d85ae69a8cc47f`, SHA-256 `37d4b7e22035f97ec39bf72c57fbe944be215b3a7273a284a30fbafdf6a87da5`
- Shared owner ACK: **absent at intake** (`#919/comment-6848800312`).

Code/test changed by this counter:

- `rawlsing_next/pre553_saved_c11_admission.py` (B repair preserved; one scope refinement)
- `rawlsing_next/tests/test_pyat991_s2d_a_counter.py` (new bounded counter tests)
- `WORKER_RETURNS/PYAT991_S2D_A_COUNTER/`

B’s `pre553_saved_workload_integration.py` and all B/A tests remain unchanged. No shared Batch/issued/checkpoint/current/carrier/query/science/fate owner was edited.

## B repairs accepted

- **B-D1:** immutable/private saved admission binding, private estate re-verification, frozen catalog/executor. Preserved.
- **B-D2:** mixed foreign-universe I03 query/predicate refusal. Preserved.
- **B-D3:** mixed/foreign-universe I05 hard refusal and discovery-scope preflight. Preserved.
- **B-D4:** changed I03/I05 and exact restore, zero/valid-empty, mixed supported+valid-empty frontier, current revocation, fresh-process tripwires, measured resource evidence. Accepted and reproduced.
- B’s 9 adversarial tests remain in place; none was removed or weakened.

B’s `repro_a_defects.py` currently exits 0 and reproduces the A RED/B GREEN restoration for the mutable binding and mixed-scope/mixed-universe attacks.

## Counterexample A-COUNTER-SCOPE

At B cut `b23d854` / code `75e1521`, the actual native I03 owner returned **SUPPORTED** for a query whose `scope_refs` contained:

- the admitted empirical universe, and
- the exact admitted `C11LogicalRelease`.

This is not a foreign source: the extra scope is the same admitted release. B’s `SavedC11Admission` rejected it solely because the complete set did not equal `{universe}`:

```text
SavedC11AdmissionError:
saved consumer query scope is not the exact admitted estate universe
```

### Repair

`_require_exact_scope_refs` now:

- requires every `EmpiricalUniverse@1.0.0` scope ref to be exactly the admitted universe;
- requires every `C11LogicalRelease` scope ref to be exactly the admitted release;
- permits the exact admitted release as additional scope metadata;
- rejects any other foreign scope reference.

This preserves B’s foreign-universe and foreign-release refusals. The counter test proves the actual native I03 fact/projection/ref parity on the saved estate after the repair.

The native full-repository **foreign-universe** mixed-scope positive remains an external **S1-D/native I03 owner HOLD**. The saved adapter refuses it; I did not edit the native owner.

## Actual tests

```text
python3 -m pytest \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pyat991_s2d_saved_admission.py \
  rawlsing_next/tests/test_pyat991_s2d_b_adversarial.py \
  rawlsing_next/tests/test_pyat991_s2d_a_counter.py \
  -q -o addopts=''
```

**26 passed in 7.25s** (7 accepted S2-C + 8 A + 9 B + 2 A counter).

Regression:

```text
python3 -m pytest [S2-G/owner suite + 17 S2-D tests + 2 counter tests] -q -o addopts=''
# 172 passed in 49.94s

python3 -m pytest [four S2-F regression files] -q -o addopts=''
# 19 passed in 8.09s
```

The focused 26-test log is `focused-26.txt`; regression logs are `regression-172.txt` and `regression-19.txt`. The B-cut RED and repaired GREEN are `red_b_cut.txt` and `green_counter.txt`.

## Seven-reader status

| Reader | Actual first reader | Status |
|---|---|---|
| I03 | `SavedC11Admission.execute_i03` → existing native I03 | **PASS_SCOPED_ACTUAL_COLD__SCOPE_COUNTER_REPAIRED** |
| I05 | `SavedC11Admission.execute_i05` → existing bounded discovery | **PASS_SCOPED_ACTUAL_COLD** |
| Batch | `BatchExecutionRunner.__init__` | **BLOCKED_OWNERSHIP** |
| NORMAL | `execute_issued_workload` | **BLOCKED_OWNERSHIP** |
| COMPLETED | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |
| PARTIAL | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |
| ABSENT | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |

The five owner holds and exact minimum edits are unchanged:

- `pre553_batch_runner.py::BatchExecutionRunner.__init__`
- `pre553_issued_workload.py::execute_issued_workload`
- `pre553_issued_workload.py::resume_joined_workloads` / `JoinedWorkloadCheckpoint`
- S1-D current/revocation
- Q2/S1-E body-sink and postconsumer fate join

No guard was monkeypatched and no fake C11 repository was constructed.

## Resource evidence

Current A counter fixture (2 respondents / 2 events):

| Measure | Value |
|---|---:|
| Retained disk | `193,222` B |
| Peak root tree | `193,222` B |
| Peak staging | not separately measured |
| Cold I03 | `0.015308` s |
| Repeat I03 | `0.013368` s |
| Fresh-child RSS | `58,384,384` B |
| Fresh-child elapsed | `0.017366` s |
| Source-extension opens in child | `0` |
| Full C11 builds | `0` |
| Whole-table fallbacks | `0` |
| I03 | `SUPPORTED`, denominator `2` |
| I05 | `1` candidate / `1` covered / `2` facts / `1` receipt |
| 100k / 6 GiB | `NOT_RUN` |

B’s independently reported fixture resources (retained `193,570` B, staging `28,672` B, 24 materializations, parent/child RSS) are preserved as B evidence; they are not a 100k claim.

## Self-critique and next attack surface

- Only I03/I05 are actual. The five readers remain blocked by ownership, not passed.
- The scope repair allows only the exact admitted universe and exact admitted release; other scope metadata is conservatively refused. A foreign source hidden in a non-universe scope kind should be tested, but no lawful native example was established.
- The native full-repository I03 still accepts a foreign-universe scope positive. That is an exact owner hold; the saved adapter refuses it.
- Current is TEST_ONLY; the Python admission freeze is not hostile process isolation. External manifest/I02/current pins remain the trust anchor.
- No Linux run of the new modules; no full 100k/6 GiB; no distinct nonauthor G5.

## Stop

A/B sequence is complete at this bounded counter. The next actor is a **distinct nonauthor S2-D G5**. Because five readers remain blocked by missing shared-owner ACKs, G5 cannot honestly issue an all-seven `ACCEPT_SCOPED`; the expected terminal is `HOLD_EXTERNAL` with the exact ownership witnesses recorded above.
