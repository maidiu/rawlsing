# PYAT991 S2-D Phase1 — DISTINCT NONAUTHOR G5 / REVISE

## 1. Exact artifact and commission

- Packet / old obligation: **S2-D / P2-05** (original #919, successor #991)
- Contract: `S2-D_PHASE1_USER_20261113.md@d7eaaf2363312af96e9bea02f6d85ae69a8cc47f`
- Contract SHA256: `37d4b7e22035f97ec39bf72c57fbe944be215b3a7273a284a30fbafdf6a87da5`
- Protected base: `6a5c12f04323d74001f9632063ec907f4fc4468e`
- Accepted S2-C executable/tree: `b7b697b69f0acea12174937ee824c19ac34ac284` / `dc416d1f23100d4d52b19bc2120226964bc0be43`
- A prior delivery/implementation: `e399c48d576f5b2ae501dac569fb729e95bd968e` / `55af65cc1a2df1d3eb82906a80434353735c5d50`
- B delivery/code cut: `b23d85428e4cd0180231fd7e35727c771de18cab` / `75e1521878ee1e4d4d661d8fdae6b80944d07f6c`
- Tested frozen cut: **`2b1f8d878e455b1f6ecb48683895b8a40dcbad72`** (code and author returns at this cut)
- Branch / worktree: `agent/pyat991-s2d-g5-r1` / `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat991-s2d-g5`
- Reviewer session: `ses_e30c25800ffeT8XbyTuHekRCme`
- Model: `opencode-go/deepseek-v4.1-flash#max`
- Write allowlist: `WORKER_RETURNS/PYAT991_S2D_G5/` only. Product, tests, source, author returns, controller and other worktrees are read-only; no reviewer patch.

Code blobs at this cut:

- `pre553_saved_c11_admission.py`: `7d1807be4e25cad18a6d0890b9a563ee04204ea9`
- `pre553_saved_workload_integration.py`: `fd3fa4378d2c15f85ee1fa0f68714307bc1de54c`
- `test_pyat991_s2d_a_counter.py`: `dc24827df6e50b4cb65c8a5d0eb18cffb7c271bd`

## 2. Closed decision

**`REVISE_EXACT_DEFECT`** at the implemented `S2_SOURCEFREE_SAVED_I03_I05_ACTUAL` boundary.

- Only **I03** and **I05** are actual; **Batch, NORMAL, COMPLETED, PARTIAL, ABSENT remain BLOCKED_OWNERSHIP** with the exact shared-owner ACK gaps.
- The independent G5 found a material **scope false refusal** in the actual saved I03 boundary: a valid native I03 request carrying the **exact admitted source artifact scope** is accepted by the native owner and by the native saved-estate executor, but the `SavedC11Admission` wrapper rejects it as a “foreign scope reference”.
- Therefore no all-seven `ACCEPT_SCOPED` and no full original S2-D acceptance. Full original remains open; integration **UNMERGED**.
- G1–G4 are not complete for the original packet; the two actual readers' base/change/restore subresult is independently proved, but the I03 scope defect and five owner holds remain.
- Scientific grade `NONE_VERIFIED`; authority grade `HOLD` (production current/issuer and shared owner ACKs absent). Q2/Q3 goal not complete.

## 3. Decisive independent scope witness

The exact accepted S2-C estate exposes the source artifact root in `receipt.i02.source`. I constructed a native `EmpiricalQuerySpec` and `EmpiricalPredicate` whose exact `scope_refs` include that **admitted** source artifact, while retaining the admitted estate universe. This is not a foreign source: it is the exact source identity of the accepted estate.

Observed with the actual native and saved first readers:

- Native full-repository I03 owner: **`SUPPORTED`**, denominator 2, fact `c2105164ca700da1e205185f5a27723c556c797ce7be5945350f3694f3fef3e8`.
- Native `CarrierNeutralResearchExecutor.execute_i03` directly over the accepted saved estate: **`SUPPORTED`**, same fact and denominator.
- Saved base I03 control: **`SUPPORTED`**, fact `064b866d646f7b7b9076842a3e26ee19df6262a1bd07a5e2e8ac87cd60955278`.
- `SavedC11Admission.execute_i03` with the exact admitted source scope: **`REFUSED`** with `SavedC11AdmissionError: saved consumer scope contains a foreign scope reference`.

Exact admitted scope:

- `SOURCE_ARTIFACT`
- object `SOURCE-G5-ADMITTED-SOURCE-SCOPE`
- content hash `ab4de5365b5eb12a8592d54898ddde47b0c0c5c542378767e2f5f7d8f0a3e0cf`

Reproduction:

```bash
PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 TMPDIR=<private-proofroot> \
python3 WORKER_RETURNS/PYAT991_S2D_G5/scope_false_refusal.py <private-proofroot>
```

Output: `defect=true`; the evidence file records native/oracle and saved-estate native SUPPORTED versus saved admission REFUSED.

### Original contract basis and minimal repair

- `EmpiricalQuerySpec.scope_refs` and `EmpiricalPredicate.scope_refs` are required **set-like exact scope references**; the schema does not impose a universe/release-only kind whitelist.
- The accepted native I03 owner accepts the exact admitted source artifact as scope metadata. The saved admission’s docstring itself says a source-scope descriptor is lawful, but `_require_exact_scope_refs` only allows `{universe, release}` and rejects the exact admitted source.
- The S2-D G1 requirement is exact trust/permitted scope; the exact admitted source artifact is permitted, while a **foreign** source/universe/release/authority must still refuse.
- Code location: `rawlsing_next/pre553_saved_c11_admission.py::SavedC11Admission._require_exact_scope_refs` (lines 296–327), `allowed = {universe, release}`.
- Minimal repair: allow the exact admitted `SOURCE_ARTIFACT` ref derived from `estate.i02.source` (and exact universe/release); reject any other source/universe/release/authority scope; add a focused regression. This is local to the new S2-D adapter and does not require a native/shared owner edit.

This is a **SEV-1 actual native first-reader false refusal**, not theoretical universal hardening. The A counter’s exact-release scope repair was correct but incomplete for source-scope descriptors; B’s foreign-universe/release refusals remain necessary.

## 4. What actually passed

- Focused existing suite at `2b1f8d`:
  `test_pre553_direct_estate_i03.py`, `test_pyat991_s2d_saved_admission.py`, `test_pyat991_s2d_b_adversarial.py`, `test_pyat991_s2d_a_counter.py`
  → **26 passed in 6.86 s** (7 accepted S2-C + 8 A + 9 B + 2 A counter).
- The 26 tests include actual cold/native I03/I05, fresh process, changed/restore I03/I05, I05 zero/valid-empty/mixed frontier, current revocation, wrong root/missing body, B-D1 immutable binding, B-D2 mixed foreign-universe I03, B-D3 mixed-universe I05, B-D4 resource/negative evidence, and A-C01 receipt-fact conservation.
- Actual base I03/I05 native facts/receipts/replay and fresh-process execution reproduce; no `C11Repository` graph or whole-table `pq.read_table` fallback is allowed during the saved consumers.
- The actual Batch guard still refuses a saved admission; NORMAL/COMPLETED/PARTIAL/ABSENT raise exact typed `SavedWorkloadOwnerHandoffRequired` holds. No stub is presented as a reader success.
- A’s exact-release scope test and B’s repairs are preserved; the new scope witness is a distinct legitimate input, not a replay of a happy path.

## 5. Resources / host limits

Independent resource probe adapted from B’s probe and run at the current cut (synthetic 2 respondents/2 events; not 100k):

- retained `193,570 B`; peak root tree `193,570 B`; peak staging `28,672 B`
- bounded object materializations `24`
- source-extension opens parent `0`, child `0`
- full C11 builds `0`; whole-table fallbacks `0`
- cold I03 `0.0158 s`, repeat `0.0138 s`
- cold I05 `0.0261 s`, repeat `0.0265 s`
- child cold I03 `0.0203 s`, I05 `0.0297 s`
- parent peak RSS `112,869,376 B`; child peak RSS `52,043,776 B`
- I03 `SUPPORTED`, denominator `2`; I05 `1/1` candidates, `2` facts, `1` receipt
- 6 GiB cap PASS at fixture grade; integrated 100k/6 GiB **NOT_RUN**
- host: Darwin/macOS Python 3.11.3; **new S2-D modules were not executed on Linux**. Accepted S2-C Linux producer evidence is prior and is not a new-module Linux claim. This is an explicit proof limit, not a made-up requirement.
- No second corpus/new physical writer/whole-table corpus archive; the accepted S2-C estate reader is reused.

## 6. Seven-reader matrix

| Reader | Actual first reader | Status |
|---|---|---|
| I03 | `SavedC11Admission.execute_i03` → `CarrierNeutralResearchExecutor.execute_i03` → `execute_empirical_query` | **ACTUAL COLD / CHANGE / RESTORE PASS; SCOPE FALSE REFUSAL** |
| I05 | `SavedC11Admission.execute_i05` → `execute_exact_bounded_discovery` | **ACTUAL COLD / CHANGE / RESTORE PASS** |
| Batch | `BatchExecutionRunner.__init__` | **BLOCKED_OWNERSHIP** |
| NORMAL | `execute_issued_workload` | **BLOCKED_OWNERSHIP** |
| COMPLETED | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |
| PARTIAL | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |
| ABSENT | `resume_joined_workloads` / checkpoint | **BLOCKED_OWNERSHIP** |

Exact five-reader holds:

- Batch: `pre553_batch_runner.py::BatchExecutionRunner.__init__` — accept exact `SavedC11Admission`/narrow saved repository and resolve exact `SavedReleaseIdentity`; no full C11 graph.
- NORMAL: `pre553_issued_workload.py::execute_issued_workload` — optional exact `saved_admission`, skip source factory/full C11 build, preserve current/fates.
- COMPLETED/PARTIAL/ABSENT: `pre553_issued_workload.py::resume_joined_workloads` / `JoinedWorkloadCheckpoint` / `capture_joined_checkpoint` — bind saved estate identity to entries and use the saved path for partial/absent while preserving receipts/current.
- Additional: S1-D native I03 mixed-scope owner hold; S1-D production current/revocation; Q2/S1-E body-sink→S2-C and postconsumer native fate join.

No guard was monkeypatched, no fake `C11Repository` constructed, and no shared owner file edited.

## 7. Prior evidence, concessions and strongest self-critique

- B-D1 immutable/private binding, B-D2 mixed foreign-universe I03 refusal, B-D3 mixed-universe I05 refusal, B-D4 changed/restore/zero/frontier/current/resource evidence, and A-C01 receipt-fact conservation are accepted and preserved.
- A’s exact admitted-release scope repair is correct where it goes; it was incomplete because a lawful exact **source-scope descriptor** is still rejected.
- The strongest counterargument to my finding would be that `scope_refs` should only contain universe/release refs; the original schema has no such whitelist, the native owner accepts the exact admitted source, and the A code docstring calls a source-scope descriptor lawful. The saved base path remains exact; the defect is the arbitrary whitelist, not the accepted source.
- The saved admission is a Python-level binding; external manifest/I02/current pins remain the trust anchor. Production current/issuer and shared owner authority are absent.
- No Linux run of the new modules; no 100k/6 GiB; no all-seven.

## 8. Return and next actor

- Return: `WORKER_RETURNS/PYAT991_S2D_G5/{receipt.json,00_HANDOFF.md,scope_false_refusal.py,resource_probe.py,resource.json,resource_run.out,evidence/}`.
- Independent decision: **`REVISE_EXACT_DEFECT`**; integration `UNMERGED`; full original S2-D remains open; five reader holds preserved.
- Exact finding goes to HQ/original owner: one bounded repair of the exact admitted-source scope in the new adapter plus focused regression, or HQ adjudication; no broad A/B round, no optional hardening, no reviewer patch. The five shared-owner ACKs remain the only path to all-seven, and cannot be inferred from branch ancestry.
- Stop finite. No protected merge, original35/science, production CURRENT or 100k/6 GiB claim.
