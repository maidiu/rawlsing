# PYAT R56 R00V — independent gate review

**VERDICT:** `REVISE__DO_NOT_ACCEPT_AS_GENERIC_POLICY_CLAIM_GATE`.
**ROLE:** independent R00V reviewer; not R00E author, not R00P policy owner, not native/R09/ original issuer.
**SESSION:** DeepSeek V4.1-Flash, MAX, OpenCode local, mainMac; new independent review worktree/branch. No subagents, zero external model calls.
**STARTUP / CANDIDATE:** `efd12b1d46f1ccf90de14b292f600078f11ec7e0`.
**BRANCH:** `agent/rabochii-pyat-r56-r00v-independent-gate-review-r1`.
**REMOTE SHA:** `__REMOTE_SHA__` (replaced after non-force push and readback).

## Four-column return

| FINDING | INTERPRETATION AND RIVALS | HQ ACTION | COMPETENT OWNER |
|---|---|---|---|
| **F1. All 36 frozen cases reproduce independently.** Exact decisions, ceilings, reasons, counts, diffs and materialized renamed variant pass through the public evaluator against a separately recomputed policy pin. | This proves the author’s 36-case fixture behavior, not broad claim-gate security. | Accept the replay evidence only at that grain. | R00V |
| **F2. The gate has 8 material laundering/identity defects outside the 36 cases.** An `EXECUTED_NATIVE` claim without evidence is allowed locally; completed `SUPPORTED` status edits are allowed locally; a PROHIBITED operation can be completed as `OBSERVED_ZERO`; a semantic mutation is hidden by a status edit; unknown claim grades allow; duplicate `occurrence_objects` are ignored; a handle contract mismatch allows; an ELIGIBLE operation can be disposition-edited to HELD. | The gate does not enforce the frozen separation of eligibility/execution/result, exact operation identity, status authority and untrusted claims. The 36-case oracle is insufficient; `REFUSE`/`HOLD` paths are bypassable. | **REVISE**. Return exact failing inputs to the same R00E implementer; no replacement gate architecture. | R00E implementer |
| **F3. Candidate evidence packaging has custody defects.** Author `manifest.json` is absent. Author `SHA256SUMS.txt` has a stale `00_RETURN.md` hash. The author `proof_witness.json` is a policy identity record, not evidence that a repository mechanical witness ran. | Custody can be reconstructed from Git + author sums, but the author’s own manifest is incomplete/stale. | Require normalized manifest and fresh mechanical witness in the R00E revise. | R00E implementer |
| **F4. Shared execution contract was unavailable.** `REVIEW_SHARED_START_AND_RETURN.md` and `NATIVE_SHARED_EXECUTION_CONTRACT.md` are absent at candidate/startup; no launch URL/exact external ref was supplied; local/remote/code-search attempts found nothing. | The R2 policy was reviewed, but additional shared-contract material obligations cannot be certified. | Supply exact shared contract ref or record the missing-obligation frontier explicitly. | Director / R00E |
| **F5. Native/original/R09 remain unproven.** No native facility, R09 runner, actual consumer or original35 grant is present. | A gate-only policy review cannot become native/survey certification. | Keep all native/generic/original holds. | R09/native/original owners |

## Reproduction

- Independent policy pin: five R2 files at `6d95a78bf6b7bcf70022e303a151255e65edc38a`; freeze blobs recomputed independently.
- 36/36 cases pass: `evidence/reviewer_replay.json`.
- Author tests preserved; reviewer tests added under `tests/universal_execution_oracle/`.
- JUnit: `evidence/junit/r00v.xml` — 19 tests, 11 passed, 8 xfailed defect probes, 0 failures/errors.
- Defect probes: `evidence/defect_probes.json` — **8 defects**.
- Typed identity: bool/int/null/order distinctions verified.

## Exact defect examples

| Probe | Actual | Required secure result |
|---|---|---|
| `claim_kind=EXECUTED_NATIVE`, full 18, no evidence | `ALLOW_LOCAL_POLICY_CONSISTENT` | HOLD_TRUSTED_NATIVE / REFUSE |
| COMPLETED `SUPPORTED` status edit, no native evidence | `ALLOW_LOCAL_POLICY_CONSISTENT` | HOLD/REFUSE |
| PROHIBITED op promoted ELIGIBLE + COMPLETED + OBSERVED_ZERO | `ALLOW_LOCAL_POLICY_CONSISTENT` | REFUSE_STATUS |
| Semantic mutation + status edit on same operation | `ALLOW_LOCAL_POLICY_CONSISTENT` | REFUSE_FRONTIER |
| Unknown `claim_grade` | `ALLOW_LOCAL_POLICY_CONSISTENT` | REFUSE |
| Duplicate `occurrence_objects` | `ALLOW_LOCAL_POLICY_CONSISTENT` | REFUSE_FRONTIER |
| Constructor handle contract mismatch | `ALLOW_LOCAL_POLICY_CONSISTENT` | REFUSE_PIN/IDENTITY |
| ELIGIBLE disposition-edited to HELD | `ALLOW_LOCAL_POLICY_CONSISTENT` | REFUSE_STATUS |

The same-process handle defect is bounded by the stated trusted-operator assumption; the other seven are candidate-input paths.

## Three courts

| Court | Verdict | Ceiling |
|---|---|---|
| **ENGINEERING** | `REVISE__36_CASES_PASS_BUT_CLAIM_GATE_BYPASSABLE` | Not accepted as generic claim gate. |
| **SCIENTIFIC** | `NO_SCIENTIFIC_CLAIM` | Policy fixtures only; no survey/decoder/native evidence. |
| **AUTHORITY** | `HOLD` | R09, native, generic and original35 remain unissued. |

## Not run / limits

- No R09 native runner, native event, actual consumer, original35 data or survey/decoder qualification.
- No new science rule; no replacement gate architecture.
- No HQ technical seal; review performed on direct Vozhd instruction.
- Shared execution contract unavailable; exact external ref missing.
- Author manifest absent; author SHA256SUMS stale for `00_RETURN.md`.
- Same-process `PinnedPolicyHandle` trust is an explicit boundary assumption, not resistance to arbitrary supervisor-process control.

## Handoff

Return the eight exact failing inputs to the **same R00E implementer**. R02/R04.byte may proceed only under their own separate seals and must not treat this gate as native acceptance. Stop after the finite R00V verdict; no self-adoption.
