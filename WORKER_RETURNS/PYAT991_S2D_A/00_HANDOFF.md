# PYAT991 S2-D Phase1 — A implementation handoff

## Decision

**`IMPLEMENTED_I03_I05__HOLD_SHARED_OWNER_ACK`**

This is not a completed all-seven-reader packet. The accepted S2-C estate is now cold-readable through the existing native **I03** and **I05** owners, with actual fresh-process I03/I05 execution, changed/restore I03, current/root/body refusals and measured fixture resources.

The original **Batch, NORMAL, COMPLETED, PARTIAL and ABSENT** readers remain **BLOCKED_OWNERSHIP** because their shared owner files did not receive the requested narrow acknowledgement. No guard was monkeypatched, no fake `C11Repository` subclass was introduced, and no fake all-seven PASS is claimed.

## Exact artifact

- Branch: `agent/pyat991-s2d-a-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-a`
- Startup / accepted S2-C: `b7b697b69f0acea12174937ee824c19ac34ac284`
- S2-C accepted tree: `dc416d1f23100d4d52b19bc2120226964bc0be43`
- S2-C G5: `ACCEPT_SCOPED__S2C_TERMINAL_CLOSED@b7b697b69f0acea12174937ee824c19ac34ac284`
- S2-C local G5 evidence:
  - `LOCAL_S2C_G5_TERMINAL_RESULTS.json` SHA-256 `b331632f…`
  - `LOCAL_S2C_G5_TERMINAL_RETURN.md` SHA-256 `1744c7d5…`
- Contract: `S2-D_PHASE1_USER_20261113.md@d7eaaf2363312af96e9bea02f6d85ae69a8cc47f`, SHA-256 `37d4b7e22035f97ec39bf72c57fbe944be215b3a7273a284a30fbafdf6a87da5`
- Lease: `WORKER_COMMISSIONS/PYAT_SUCCESSOR_960/S2D_PHASE1_LEASE.json`
- Shared owner ACK: **PENDING** at `https://github.com/maidiu/rawlsing/issues/919#issuecomment-6848800312`

New files only:

- `rawlsing_next/pre553_saved_c11_admission.py`
- `rawlsing_next/pre553_saved_workload_integration.py`
- `rawlsing_next/tests/test_pyat991_s2d_saved_admission.py`
- `WORKER_RETURNS/PYAT991_S2D_A/`

No existing product/test/source/other-return file was changed.

## What actually works

### Accepted S2-C estate

The accepted S2-C reader remains unchanged:

- `VerifiedDirectEstate` with independent manifest/I02 roots, exact path and live current callback.
- `DirectEstateI03Session` with positional/selector/body coverage and temporary metadata-only SQLite.
- Historical `C11LogicalRelease` identity reconstructed from the direct certificate.
- No full `C11Repository` graph, `C11LogicalRelease` graph or whole-table `pq.read_table` on the observed I03/I05 paths.

### New saved admission

`SavedC11Admission`:

- accepts only the exact `VerifiedDirectEstate`;
- requires the exact reconstructed v1 release;
- binds the existing `RuntimeObjectCatalog`;
- exposes an exact binding receipt with manifest/I02/release and `source_opens=0`, `full_c11_repository_builds=0`;
- implements I03 through the existing `CarrierNeutralResearchExecutor.execute_i03` / `execute_empirical_query`;
- implements I05 through the existing `execute_exact_bounded_discovery` using the accepted `DirectEstateI03Session`;
- rechecks the live current callback before and after serving;
- exposes identity-only `SavedReleaseIdentity` for a future owner-approved Batch adapter.

`SavedWorkloadIntegration`:

- `execute_saved_i03` and `execute_saved_i05` are actual;
- `execute_saved_batch`, normal, completed, partial and absent raise typed `SavedWorkloadOwnerHandoffRequired` with exact owner/path/function/minimum edit.

## Actual evidence

Focused command:

```text
python3 -m pytest \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pyat991_s2d_saved_admission.py -q -o addopts=''
```

Result: **15 passed in 4.06s** (7 accepted S2-C tests + 8 new S2-D tests).

New tests cover:

- cold I03 exact native fact refs/projections/release refs with `C11Repository.__init__` and `pq.read_table` forbidden;
- cold I05 exact native candidate/covered counts, fact refs and `DiscoveryResultReceipt` refs, same forbidden fallbacks;
- fresh-process I03 and fresh-process I05 with only external pins and public preimages;
- changed native I03 fact and exact original restore;
- revoked current, wrong independently held manifest, missing event body;
- the actual Batch guard refusal (`repository must be accepted I02 C11Repository`);
- typed owner holds for the remaining five readers.

Resource probe:

```text
python3 WORKER_RETURNS/PYAT991_S2D_A/resource_probe.py
```

Actual fixture (2 respondents/2 events):

| Measure | Value |
|---|---:|
| Retained disk | `193,222` B |
| Files | `17` |
| Peak root tree | `193,222` B |
| Peak staging | not separately measured |
| Cold I03 | `0.016766` s |
| Repeat I03 | `0.014585` s |
| Fresh-child peak RSS | `54,771,712` B |
| Fresh-child elapsed | `0.019359` s |
| Source opens in child | `0` |
| Full C11 builds | `0` |
| I03 fact | `SUPPORTED`, denominator `2` |
| I05 frontier | `1` candidate, `1` covered, `2` facts, `1` receipt |
| 100k/6GiB | `NOT_RUN` |

The child was a separate process; it was not passed the source, original C11 repository or event bodies. The resource probe forbade `C11Repository.__init__` and `pq.read_table` during the saved consumers.

## Why five readers are blocked

The lease permits only the two new modules and new tests; shared files remain READONLY without an explicit owner ACK. The actual startup barriers are:

- `pre553_batch_runner.py::BatchExecutionRunner.__init__` line 402 requires `C11Repository`.
- `pre553_issued_workload.py::execute_issued_workload` line 327 rebuilds source/full C11.
- `resume_joined_workloads` line 1283 and `JoinedWorkloadCheckpoint` v2 have no saved-estate binding.
- `pre553_empirical_query.py` / `pre553_carrier_execution.py` current saved-I03 admission is accepted through S2-C, but production S1-D current composition is not included.

Minimum owner edits are recorded in `pre553_saved_workload_integration.py` and `receipt.json`.

I did not edit those files, monkeypatch their guards, or construct a fake C11 graph to claim the five readers. The actual Batch guard test proves the refusal is still in force.

## Joint S1-E / Q2 handoff

- Q2/S1-E accepted compatibility: `8b51dc8f…`, G5 `41f47931…`, grade `SOURCEFREE_PROVISIONAL_TEST_ONLY_COMPATIBILITY`.
- The accepted S2-C tree at `b7b697` does **not** contain `pre553_source_i02_handoff.py` or `pre553_source_i02_streams.py`. Q2 remains an external handoff; no merge was performed.
- Q2 `operation_fates` remain pre-consumer with `issued_receipt_refs=()` and native HOLD. No postconsumer native receipt→operation/fate join exists in the startup tree.
- This A turn used the accepted S2-C/native test candidate producer for the actual saved estate; it did not claim production Q2 source composition.

## Self-critique

- The implementation is genuinely partial: only I03/I05 are actual.
- The current callback is TEST_ONLY; production S1-D current/revocation remains a HOLD.
- No Linux execution of the new modules was performed. The accepted S2-C G5 is Linux evidence for the producer, not for these new modules; the new tests ran on Darwin.
- The I05 path bypasses the accepted S2-C carrier’s explicit saved-I05 refusal by calling the existing discovery owner directly; this is lawful reuse of the existing I05 engine, but it needs hostile B review for session/current/catalog attacks.
- No peak staging/orphan disk or process-tree measurement beyond a single child; no all-seven resource claim.
- No Q2 body-sink→S2-C writer integration was available in the accepted tree.

## Strongest next falsifier

A hostile B should try to:

- cause a forged caller current callback or a non-exact saved admission to reach a native I03/I05 fact;
- reuse a `DirectEstateI03Session` across boundaries or replace its catalog/preimages;
- attack the I05 session/frontier path with mixed universe or partial discovery;
- construct a fake saved release/identity that bypasses `SavedC11Admission` type/identity checks;
- inspect whether the partial integration holds can be mistaken for accepted Batch/normal/resume.

## Grades and stop

- Engineering: `S2_SOURCEFREE_SAVED_I03_I05_ACTUAL__FIVE_OWNER_BLOCKS` — partial, not full G1–G4.
- Scientific: `NONE_VERIFIED`; sourcefree TEST_ONLY only.
- Authority: `HOLD`; S1-D production current and shared owner ACK absent.
- Integration: `UNMERGED`.
- G5: `NOT_RUN`.
- Disposition: `BLOCKED_OWNERSHIP` for the five shared-reader integrations.

The next actor is B on this same descendant, then A's one bounded counter, then a distinct nonauthor G5. No additional shared file may be edited without the missing owner ACK.
