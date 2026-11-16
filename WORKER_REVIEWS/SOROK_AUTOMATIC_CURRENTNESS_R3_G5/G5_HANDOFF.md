# SOROK automatic currentness R3 — G5 handoff (not accepted)

**Verdict:** `REVISE_EXACT_DEFECT`
**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu`
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Corrected source:** `0b2664a8353f5957e1dad4bb5678be66fa9470ef`
**Final artifact/report:** `cb299a2f2a0fcd55826486c7a0a38108ba21bfab`
**Runtime blob:** `fc322b1ea3b3769bae699aeea8c1d31c053fd042`
**Test blob:** `d9e0f81ee6578ecf1fb9e6838ba0e6fa82d94651`
**Focused R3 test blob:** `fc8f18260127ca039453d2100c69602fef126e7b`
**Evidence commit:** this frozen review commit
**Receipt:** `WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R3_G5/REVIEW_RECEIPT.json`
**Full original claim:** `NOT_ESTABLISHED`
**Protected CI:** `UNAVAILABLE_BILLING`
**Adoption:** `PENDING_PROTECTED_CI_AND_ADOPTION`

## What passed

The R2 material probe was run unchanged apart from scratch path and returns
**7 fixed / 0 gaps / PASS** on this source. The public unenrolled fake REVIEWER
probe returns `UNTRUSTED_CONTROLLER_RUN`. The 28-test suite passes (17 original
+ 11 R3) with reviewer TMPDIR. Trusted rejection, fake/real protected merge
handling, exact verdict equality, registry/run-path tamper, public material
event refusal, trusted reviewer acceptance, revocation/restoration and
post-REVISE resubmission are covered. Live startup/status shows 16 refs, PR
reads 200, issue reads 403, and the four expected source items. The actual R3
author job completed; the author pair generation 51 records
`RETURNED_REVIEW_PENDING`; the review job is enrolled as REVIEWER with expected
source `0b2664a8`.

## Why it is still RED

The public `attest-launch` boundary can be spoofed:

1. A reviewer sandbox created a self-authored executable named `launch.py`
   with caller arguments `--binding fake --job fake`.
2. It spawned its own live supervisor/observer/child process tree with the
   parent relationships expected by `_require_launcher_process_tree`.
3. `attest-launch --run-dir ...` returned exit 0 and
   `TRUSTED_LAUNCH_ATTESTED` for fake REVIEWER launch
   `launch-aada117a2f29fc0b2459c69caa1d1912`.
4. The fake self-consistent REVIEWER run was accepted by `intake-review` using
   the real R2 receipt; `mechanism_review` recorded a verdict for a run whose
   job session was `ses_FAKE_ATTEST`, while the receipt expected this reviewer.

The implementation checks a command string (`launch.py`, `--binding`,
`--job`) and live PID relationships, but not the installed launcher path/hash
or an operator-issued/launcher-issued nonce. A caller-provided process tree is
not a supervised controller boundary. The run’s actual session is also not
compared to the receipt expected session; the expected field is.

**Raw:** `evidence/fake_attest_report.json`,
`evidence/raw/fake_attest/attest.out`,
`evidence/raw/fake_attest/review.out`,
`evidence/raw/fake_attest/review.exit`.

## Exact correction

- Make `attest-launch` internal to the actual installed patched launcher, or
  require competent operator authorization/enrollment. Verify the installed
  launcher exact path/hash or a launcher-issued nonce; do not accept
  caller-authored `launch.py`/command strings or caller-owned PIDs.
- Bind the actual run job session/role/source to the receipt and registry, not
  only `expected_session` / `expected_source_commit` fields.
- Keep the successful material-event routes, exact verdict equality,
  revocation/restoration, and source HOLD logic.
- After correction, run one focused rereceiving of the exact fixed source.
  No new author cycle, no #1095 G5 rerun, no protected merge.

## Local evidence (macOS, not Actions)

- 28 tests: `28 passed`, exit 0, 16.49s.
- Frozen verifier self-test/plain/no-git: 0 each.
- MCR py_compile/self-test: 0 each.
- Canonical PROGRAMMA: 0.
- Pyat plain/self-test: 0 each.
- Changed WORKER_COMMISSIONS: 0; selector not applicable.
- Live cold startup/status/what-next: exit 2 with the four source items;
  `what-next` recommends B01 `RECEIVE`; issue/comment `403` is a source HOLD;
  no full currentness claim.

## HQ post-review

After this reviewer exits, the installed hook should intake
`REVIEW_RECEIPT.json` and HQ should run a fresh-process `startup`/`status`.
Because this verdict is `REVISE_EXACT_DEFECT`, do not adopt protected/native/
full currentness. Send one bounded code correction for the attest-launch
boundary, then one focused rereceiving. **STOP.**
