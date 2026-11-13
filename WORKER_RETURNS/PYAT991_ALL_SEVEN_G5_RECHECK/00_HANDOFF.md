# PYAT991 S2-D — ALL-SEVEN G5 RECHECK / SCOPED ACCEPTANCE

## 1. Verdict

**`ACCEPT_SCOPED@S2_SOURCEFREE_SAVED_NATIVE_ALL_READERS`**

at **`S2_SOURCEFREE_SAVED_FIXTURE`** grade, on the exact repair cut
**`9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`**.

The prior G5 finding is closed:

- Before (`5df0bbd`): forged PARTIAL binding restored **2** protected outputs
  before `JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH`.
- After (`9d96a9c`): forged PARTIAL and COMPLETED controls both refuse with **0**
  protected entry/output/receipt work.
- Legitimate PARTIAL still resumes its exact prefix and final native outputs.

The seven actual saved native readers and the bounded G4 observations are accepted
at the TEST_ONLY sourcefree fixture grade. No production CURRENT, original35,
source science, 100k/6 GiB, Linux new-module, or protected-merge claim is made.
Integration remains **UNMERGED**.

## 2. Exact artifact and authority

- Tested cut: **`9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`**
- Prior G5 return/base: `f5b9c2acdb79b0bc9fabcf8eabcffe580611b34f`
- Prior reviewed cut: `5df0bbdf3ec4c479724e74651a80d4861ab700a1`
- Owner ACK delivery: `b32f215660def205762f0e9d0eafa2c3dfaa0c36`
- Owner ACK blob: `dae76ff13b096efe67df9ec526b9d8b99ce28b25`, status `ACK`
- Accepted S2-C: `b7b697b69f0acea12174937ee824c19ac34ac284` / tree `dc416d1f23100d4d52b19bc2120226964bc0be43`
- Contract SHA-256: `37d4b7e22035f97ec39bf72c57fbe944be215b3a7273a284a30fbafdf6a87da5`
- Branch/worktree: `agent/pyat991-s2d-g5-r1` / `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-g5`
- Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme`; `opencode-go/deepseek-v4.1-flash#max`
- Write allowlist: `WORKER_RETURNS/PYAT991_ALL_SEVEN_G5_RECHECK/` only.

**Owner ACK is actual and still in force.** The Batch and issued-workload leases are
exact; the ACK distinguishes the parent/HQ functional allocation from personal R16
Batch authorship. The five old ownership holds are resolved and are not carried
forward. No new owner permission was manufactured. The repair delta is only the
issued-workload PARTIAL ordering plus the new test; Batch, saved admission,
integration wrappers and accepted S2-C remain unchanged.

Source pins at the tested cut:

- `pre553_issued_workload.py`: `b02810677ae66231e5e59b09aefe9bd63a31aaa3`
- `test_pyat991_s2d_partial_binding_order.py`: `4591e6300624b1e80c7f4e8e92c91ddb2155fca9`
- `pre553_batch_runner.py`: `49e3974c658d66a270815d9faa3798b40d4488b1`
- `pre553_saved_c11_admission.py`: `22749addc1fca5f0b90e12728847c390aafa7a84`
- `pre553_saved_workload_integration.py`: `cc8aa32512378261406d765f0b049c748cb3e11f`
- `test_pyat991_s2d_five_readers.py`: `38e339b70eb1ca8f607b75a8a259523504ede731`

## 3. Exact repair

In `resume_joined_workloads` PARTIAL, the order is now:

```text
fresh CURRENT require_unchanged
exact saved admission factory
  exact type
  exact checkpoint saved_binding
  exact current source hash
fresh CURRENT require_unchanged after the saved binding
_validate_entry_material
_validate_entry_outputs
_restore_receipt
_restore_output_material
```

The COMPLETED branch was already correct. Legacy source-factory behavior, ABSENT,
Batch, the checkpoint schema/hash, issuer/current semantics and scientific owners
are unchanged.

## 4. Canonical independent witness

My prior canonical `forged_partial_binding.py` was run unchanged at the fixed cut
from the prior return; only the proofroot/output location changed.

```text
current canonical exit 2 (expected defect=false signal)
COMPLETED forged control: protected output restores = 0
PARTIAL forged witness:   protected output restores = 0
error: JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH
defect_reproduced: false
```

The historical `5df0` bytes remain untouched and still record the original
2-restore defect.

### Independent PARTIAL-order witness

`independent_partial_order.py` additionally measured every protected-work stage:

- coherent forged PARTIAL binding: factory 1; material validation 0; output
  validation 0; receipt restore 0; output restore 0; binding-mismatch refusal;
- wrong admission type: factory 1; all protected work 0;
  `EXACT_SAVED_C11_ADMISSION_REQUIRED`;
- revoked CURRENT: factory 0; all protected work 0;
  `CURRENT_COMPETENT_SOURCE_AND_SCIENCE_DECISION_REQUIRED`;
- CURRENT flip after the saved binding checks: factory 1; all protected work 0;
  `ISSUER_SNAPSHOT_CHANGED_AFTER_SAVED_BINDING`;
- legitimate PARTIAL: material/output validation 1/1, receipt/output restores
  3/2, exact full output-ref parity, no error.

This covers the requested “0 protected entry/output/receipt work” more strongly
than the new test’s output-restore spy alone.

## 5. Tests

```text
focused 38 (prior 36 + 2 new partial-order tests): 38 passed in 18.09 s
native 69 (Batch/S1-D current/checkpoint):          69 passed in 66.88 s
```

The prior all-seven positive evidence (I03/I05, Batch, NORMAL, COMPLETED,
PARTIAL, ABSENT, fresh child, integrated I05 discovery final parity, full object
parity, test-only capsule qualification, source-scope closure) is inherited from
the exact `5df0` source with current-delta conservation only. The repair is a
PARTIAL ordering/second-current change and does not alter those positive paths.

## 6. G4 bounded observations

`independent_g4_probe.py` on the S1-D/S3 sourcefree 4-respondent/2-occasion
fixture; **not 100k**:

| Observable | Independent result |
|---|---:|
| Retained disk | `320,500` B |
| Peak root tree | `320,500` B |
| Observed stage peak | `555,503` B |
| Stage sampler | 1 ms, 66 samples |
| Parent max RSS | `121,630,720` B |
| Fresh normal tree peak | `184,864,768` B |
| Fresh completed tree peak | `184,221,696` B |
| Fresh partial tree peak | `185,520,128` B |
| Fresh absent tree peak | `182,910,976` B |
| Main tree sampler | 2 ms `ps` parent-root tree including live descendants; 22–24 samples per mode |
| Separate fresh-Batch nested tree peak | `297,783,296` B (includes the independent driver and its Batch child; not the same parent+one-child comparator) |
| Normal / repeat | `0.1302` / `0.1015` s |
| Partial / repeat | `0.0653` / `0.0703` s |
| Completed / partial / absent resume | `0.0369` / `0.1041` / `0.1570` s |
| Family objects yielded | `15` |
| Counter coverage | parent normal+partial only |
| Source-factory calls | `0` |
| Full C11 builds | `0` |
| Whole-table `pq.read_table` calls | `0` |
| Scratch leftovers | none |
| Orphan child PIDs | none |
| 100k / 6 GiB | NOT_RUN |
| New modules on Linux | NOT_RUN; Darwin only |

The process-tree values are **sampled peaks**, not exact hardware maxima. The
15-object count covers only parent normal+partial; fresh children and the separate
Batch driver were not included in that counter. This is a bounded fixture proof,
not an all-reader object-materialization census and not a 6 GiB claim.

### Native crash boundary witness

The author’s probe crash path JSON-loads an already durable PARTIAL capsule and
SIGKILLs before native resume. I did **not** treat that as interrupted-native
execution. My own witness instead kills the child **after the second actual
`BatchExecutionRunner.record_receipt` inside native PARTIAL resume**:

```text
checkpoint state: PARTIAL; prior receipts: 1
crash point: after second actual receipt in native resume
crashed child returncode: -9
fresh resume returncode: 0
fresh resume output refs exactly match full normal refs: true
```

This proves caller-owned immutable checkpoint survival plus fresh native recovery
at a real native receipt boundary. It does **not** claim atomic creation of a new
checkpoint, a production journal, or a universal failpoint matrix. No new
checkpoint store or engine was added.

## 7. Seven-reader matrix

| Reader | Status |
|---|---|
| I03 | **PASS_SCOPED_ACTUAL_COLD** |
| I05 | **PASS_SCOPED_ACTUAL_COLD** |
| Batch | **PASS_SCOPED_ACTUAL_NATIVE_SCHEDULER** |
| NORMAL | **PASS_SCOPED_ACTUAL_NATIVE_ISSUED_PATH** |
| COMPLETED | **PASS_SCOPED_ACTUAL_RESUME__FORGED_REFUSAL_0_PROTECTED_WORK** |
| PARTIAL | **PASS_SCOPED_ACTUAL_RESUME__ORDERING_REPAIRED__0_PROTECTED_WORK** |
| ABSENT | **PASS_SCOPED_ACTUAL_RESUME** |

## 8. G1–G5

- **G1 PASS_SCOPED:** all seven actual owner paths, exact accepted S2-C estate/
  release/source/catalog/workload binding, exact owner ACK, legacy C11/source path
  preserved.
- **G2 PASS_SCOPED:** actual cold/completed/partial/absent, fresh child, exact
  prefix/final outputs, changed/restore and prior full parity preserved.
- **G3 PASS_SCOPED:** exact forged PARTIAL ordering defect repaired; zero protected
  work for forged binding, wrong type, revoked CURRENT and post-binding CURRENT
  change; COMPLETED control zero; legitimate PARTIAL conserved.
- **G4 PASS_SCOPED_BOUNDED:** bounded independent fixture observations above,
  explicit sampling/counter limits, no 100k/6 GiB or production claim.
- **G5 PASS:** same distinct nonauthor reviewer accepts at the stated scoped grade.

## 9. Limits / self-critique

- Process-tree RSS and stage peak are sampled, not exact instantaneous maxima.
- Object/materialization counter covers parent normal+partial only.
- The crash witness is one controlled SIGKILL at a real native receipt boundary,
  not a universal failpoint matrix and not atomic new-checkpoint publication.
- Caller-owned immutable checkpoint material is the API boundary; no production
  durability service is claimed.
- The fresh-process capsule remains TEST_ONLY public workload-envelope transport;
  it is bound by exact envelope/record and exact estate roots, not an unbound duck
  projection source authority.
- New modules are Darwin-only; no Linux proof is inherited from S2-C.
- Production CURRENT/issuer, original35/source science/rights, Q2/S1-E body-sink/
  fate join, S2-B G5-R1, 100k/6 GiB and protected merge remain external.
- Integration is **UNMERGED**.

## 10. Decision

**Scoped packet accepted; full original mission remains open only for the listed
external holds.** No new A/B round, reviewer patch, optional hardening, production
source/current, protected merge, or universal crash architecture.

Return: `WORKER_RETURNS/PYAT991_ALL_SEVEN_G5_RECHECK/`.

## 11. Remote verification

Review content commit **`c0d266403a7f2929557403cbd70025444583734b`** was pushed to
`origin/agent/pyat991-s2d-g5-r1`. Direct remote verification found the tested product
tree unchanged (`git diff --stat 9d96a9c..c0d2664 -- rawlsing_next` empty), the remote
receipt valid and the handoff present. A branch `9d96a9c`; B branch `b23d85428`.
See `evidence/remote_verification.txt`.
