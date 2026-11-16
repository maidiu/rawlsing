# SOROK automatic currentness R3 — focused independent receiving

**Engineering:** `REVISE_EXACT_DEFECT`
**Scientific:** `HELD`
**Authority:** `HOLD_SOURCE_AUTHORITY`
**Full original claim:** `NOT_ESTABLISHED`
**Accept scoped:** `false`

**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu` (same distinct nonauthor)
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Corrected source:** `0b2664a8353f5957e1dad4bb5678be66fa9470ef`
**Main corrected commit:** `a1fa15d47`
**Final artifact/report:** `cb299a2f2a0fcd55826486c7a0a38108ba21bfab`
**Runtime blob:** `fc322b1ea3b3769bae699aeea8c1d31c053fd042`
**Test blob:** `d9e0f81ee6578ecf1fb9e6838ba0e6fa82d94651`
**Focused R3 test blob:** `fc8f18260127ca039453d2100c69602fef126e7b`
**R1 RED:** `fc49662603c3dd8148c847cd6f35f2172184fd5a` (preserved)
**R2 RED:** `53fad99fd8da86e4ab1cd12fdcfcd93fc8b2942f` / evidence
`f8006235266aa618963b186e5c357bf92be830b3` (preserved)
**Review job:** `sorok-programma-automatic-currentness-r3-receiving-20261116-r1`
**Receipt bound path:** `WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R3_G5/REVIEW_RECEIPT.json`

This is one focused R3 receiving after the material-event correction. It is not
a #1095 G5 rerun, not a review-of-review, and not a new author cycle. Product
and frozen #1095 code/source were read-only. All mutations were in
reviewer-owned sandbox pair/config/state under the R3 lease. The author live
pair/config, private author capability, and registry secrets were not read,
copied, printed, or edited.

## 1. R2 material reds are fixed at the ordinary event routes

I executed the unchanged R2 `material_auth_probe.py` (original sha256
`973d9695f1e511bd3f7e29773806b043f13d8f04915a6edb4459dd7ab15a731c`);
only its own scratch path was adapted. On the rejected ea5 source the same probe reproduces **3 fixed / 4 gaps /
REVISE_EXACT_DEFECT**; on the corrected source it reports
**7 fixed / 0 gaps / PASS**:

- caller-only mechanism review refused;
- arbitrary STOP refused;
- arbitrary resolution refused;
- untrusted `REJECTION` refused;
- untrusted `PROTECTED_INTEGRATION` refused;
- unauthenticated public `GITHUB_OBSERVATION` refused;
- self-consistent fake `WORKER_RETURN` refused.

I also ran the R3 fake-reviewer probe unchanged apart from its scratch path.
It refuses the unenrolled fake reviewer run with
`UNTRUSTED_CONTROLLER_RUN`, as required. The 28-test suite (17 original + 11
focused R3) passes with the reviewer TMPDIR under this checkout. It covers
trusted rejection, fake/real protected merge handling, exact verdict equality,
registry/run-path tamper, public material-event refusal, trusted reviewer
acceptance, revocation/restoration, and resubmission after `REVISE`.

The 28 tests are useful but not sufficient: they do not exercise a
caller-authored `launch.py` that satisfies the launcher string/process-tree
check and then self-attests its own run.

## 2. Remaining RED: public `attest-launch` bypass

The corrected admission boundary is still forgeable at the public CLI:

- I created a reviewer-owned sandbox, a self-authored executable named
  `launch.py` with caller arguments `--binding fake --job fake`, and a
  self-consistent controller run.
- The fake launcher spawned its own live supervisor, observer and child PIDs
  with the expected parent relationships. It then invoked
  `attest-launch --run-dir ...`.
- `attest-launch` returned exit `0` and
  `state = TRUSTED_LAUNCH_ATTESTED` for a fake `REVIEWER` launch
  (`launch-aada117a2f29fc0b2459c69caa1d1912`), because
  `_require_launcher_process_tree` only checks that the parent command string
  contains `launch.py`, `--binding` and `--job`, and that the live PID tree
  has the expected relationships.
- The fake run was then accepted by `intake-review` with the valid R2
  reviewer receipt at the real evidence commit; `mechanism_review` was
  recorded as `REVISE_EXACT_DEFECT` for the fake run. The run was not an
  installed controller launch, not the actual patched launcher, and its job
  session was `ses_FAKE_ATTEST`, while the receipt’s expected session was
  accepted.

This is an ordinary public CLI authority bypass, not root-level secret/key
fabrication. No author capability was used: the sandbox created its own
capability under its own state. A caller-authored process named `launch.py`
plus own live PIDs must not be sufficient. The shortest fix is to restrict
`attest-launch` to the actual installed launcher (verified exact path/hash or a
launcher-issued nonce) or require competent operator authorization/enrollment;
a process-command string and caller-provided PID tree are not supervision.
The same boundary must bind the run’s actual session to the receipt expected
session, not only the `expected_session` field.

**Raw witness:** `evidence/fake_attest_report.json`,
`evidence/raw/fake_attest/attest.out`, `evidence/raw/fake_attest/review.out`,
`evidence/raw/fake_attest/review.exit`.

## 3. Live source and source-authority hold

Authenticated live GitHub refs/SHA and PR status were observed through the
existing credential helper in a reviewer sandbox: 16 refs, repo/PR reads
`200`, issue reads `939/1008/1010 = 403`, `REF_SHA_ONLY` coverage. The four
current items remain visible:

- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:939`
- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:1008`
- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:1010`
- `GITHUB_PR_STATUS_ADVANCED pr:1095`

The issue/comment `403` is a genuine existing connector-scope source HOLD, not
a code success and not a reason to claim full issue/comment currentness. The
PR #1095 status advance remains unreconciled by design. Required CI remains
`UNAVAILABLE_BILLING` / `PENDING_PROTECTED_CI_AND_ADOPTION`; no local check is
reported as GitHub Actions PASS.

A public `GITHUB_OBSERVATION` bearing `source.trust=RUNTIME_INTERNAL_LIVE_FETCH`
and a matching `observation_digest` was also refused
`LIVE_GITHUB_OBSERVATION_UNTRUSTED_SOURCE`; this specific label/digest bypass
is closed.

## 4. Actual R3 lifecycle custody

The actual author R3 job
`sorok-programma-automatic-currentness-material-auth-repair-20261116-r3`
(session `ses_e21a481bfffefyvpxaeFaAOFvQ`, PID 81644) completed and the
installed hook recorded `REAL_MECHANISM_WORKER_RETURN_INTAKEN`. The author live
pair generation 51, checkpoint
`42c533215ffdd623e45a9016d14a81210813e93228bcb240c5983fa3b3c7d16b`, has
`mechanism_worker_return.execution_state = RETURNED_REVIEW_PENDING` with exact
`0b2664a8` source, runtime/test blobs and return SHA
`4fc9476f…`. The prebound review job has role `REVIEWER`, expected session
this reviewer, expected source `0b2664a8`, and the receipt path above; the
actual R3 review launch is enrolled in the live trusted-launch registry. This
is not a fixture. The prior R2 `REVISE` remains historical; it is not
acceptance of R3.

## 5. Historical, dependency and whole-claim boundaries

The reviewed state preserves 27 `B01–G04` tasks, 21 G/M/T decision nodes,
original 144/38/83/304/100 scope, seven protected P3/P4/P5/P6/MI/MII/MIII
foundations, B05 #1089 / C04 #1062 / C05 #1091 scoped pins, G03-I0 scoped
accepted with full G03 held, CG-A #1066 outside the 27 DAG, Browser
#1008/#1010 terminal bounded and #1012 not launched, and #939
`USER_STOP_AFTER_ORIGINAL_ASSIGNMENTS` with no dispatch. B05/C04/C05 retain
their own full-claim decision blockers. No scoped → whole-original, sourcefree
→ native, candidate → protected, or merge → complete inference is made. A
reviewer acceptance without progress/decision update remains visibly held.

## 6. Checks performed (macOS, existing Python; not Actions)

- 28 tests: **28 passed**, exit `0`, 16.49 s with reviewer TMPDIR.
- Frozen #1095 verifier `--self-test --status`, plain, `--no-git --status`:
  exit `0` each.
- MCR py_compile and `--self-test`: exit `0` each.
- Canonical PROGRAMMA verifier: exit `0`.
- Pyat product visibility plain and `--self-test`: exit `0` each.
- Changed `WORKER_COMMISSIONS`: zero; selector not applicable.
- R2 material probe: `7 fixed / 0 gaps / PASS`.
- R3 fake reviewer probe: unenrolled fake refused `UNTRUSTED_CONTROLLER_RUN`.
- Public `attest-launch` fake launcher: accepted `TRUSTED_LAUNCH_ATTESTED`
  (the residual RED above).
- Live sandbox startup/status/what-next: exit `2` while the four source items
  remain; `what-next` returns B01 `RECEIVE` with owner and prerequisites; live
  observation time/digest persists across the follow-up status.

## 7. Verdict and STOP

Engineering is **REVISE_EXACT_DEFECT** because the public attestation boundary
can still be minted by a caller-authored launcher and live process tree. The
rest of the R3 material-event correction is a real improvement: the original
public `REJECTION`, `PROTECTED_INTEGRATION`, `GITHUB_OBSERVATION` and fake
worker/reviewer routes are refused when not trusted, and the trusted positive
tests and exact verdict equality pass.

Scientific authority remains HELD. Authority remains
`HOLD_SOURCE_AUTHORITY` for issue/comment connector scope. Full original
currentness is not established. This is one finite code correction, not a new
campaign. After correction, one focused rereceiving of the exact fixed source
is required. **STOP.**
