# SOROK automatic currentness R2 — G5 handoff (not accepted)

**Verdict:** `REVISE_EXACT_DEFECT`
**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu`
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Corrected source:** `ea5e48cf3240e72e39cd19be3120ad727902eee2`
**Worker artifact:** `20ae27f802a863370d215d9f4b7ed44e76c54da3`
**Final report:** `d71d52a5cf0c604a0738c0928bcf2b7e7ea8eb12`
**Runtime blob:** `d06cd8a9a736fac728ea6b5ea2c098aa4986cfa0`
**Test blob:** `202e81d85d78e4d158a43bfcfa55a818149bf8fd`
**Evidence commit:** this frozen review commit
**Receipt:** `WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R2_G5/REVIEW_RECEIPT.json`
**Full original claim:** `NOT_ESTABLISHED`
**Protected CI:** `UNAVAILABLE_BILLING`
**Adoption:** `PENDING_PROTECTED_CI_AND_ADOPTION`

## What is genuinely fixed

The five R1 reds are repaired in the corrected source:

1. The local baseline is only expected refs. Authenticated live GitHub
   observation fetched 16 refs, repo/PR reads `200`, issue reads `403`, with
   own `fetched_at_utc`, `expires_at_utc` and `evidence_digest`.
2. Mechanism review no longer returns `TASK_UNKNOWN`; caller-only receipt
   returns `REVIEW_SUPERVISED_RUN_REQUIRED`.
3. A fabricated ordinary task review without a supervised run is refused.
4. Arbitrary STOP/RESUME is refused; authorized stop and superseding resume
   work.
5. Arbitrary resolution text is refused; a fresh live digest resolves the
   exact item.

The real author lifecycle is also present: job
`sorok-programma-automatic-currentness-repair-20261115-r2`, PID 69246, hook
`REAL_MECHANISM_WORKER_RETURN_INTAKEN`, author pair generation 49,
`mechanism_worker_return = RETURNED_REVIEW_PENDING`, return SHA
`7403e06e…`.

## Why it is still REVISE

The corrected runtime does not authenticate all material event kinds:

- `REJECTION` is an unauthenticated public `intake-event`; a fabricated event
  set B01 to `REJECTED` while B01 still advertised
  `READY_FOR_SCOPED_ENGINEERING`.
- `PROTECTED_INTEGRATION` is an unauthenticated public event; a fabricated
  `ci_state=PASS` and fake merge SHA set B05
  `protected_integration=PROTECTED_SOURCEFREE`, `protected_ci=PASS`.
- `GITHUB_OBSERVATION` is accepted from public CLI with arbitrary
  `source_identity=FAKE_SOURCE` and `evidence_digest=evil`.
- A self-consistent fabricated controller run/PID 99999 and
  `WORKER_RETURN.json` was accepted as `mechanism_worker_return`.
- A self-consistent fabricated REVIEWER run and fake `VERDICT.json` was
  accepted as `ACCEPT_SCOPED_PENDING_HQ_ADOPTION` for a fake commit.
- `_verify_verdict_artifact` uses `startswith`, not exact verdict equality.

Exact raw witnesses are under `evidence/raw/materials/`,
`evidence/raw/fake_review/`, `evidence/fake_worker_return_intake.out`,
`evidence/fake_supervised_review_intake.out`, `evidence/material_auth_probe_report.json`,
and the unchanged R1 probe report.

## Required correction

1. Authenticate `REJECTION` and `PROTECTED_INTEGRATION` through a trusted
   supervised controller/competent role/source/CI/merge boundary. Arbitrary
   public JSON must refuse; valid staged integration must remain typed pending
   CI.
2. Do not accept public `GITHUB_OBSERVATION` payloads as live truth. Only use
   the runtime's authenticated fetch or a wired, expiring authenticated
   connector; validate source identity/time/expiry/digest; no arbitrary
   ref/digest can mint authority.
3. Bind `WORKER_RETURN` and REVIEWER runs to a trusted controller root, actual
   launch/process/argv/completion, exact role/session/source, and an immutable
   `VERDICT.json`. Self-consistent caller-created JSON/worktree is not
   supervision.
4. Require exact receipt/verdict equality and reject unknown/changed task
   source/scope. No public rejection/protected promotion.
5. Keep issue/comment `403` as an explicit source-authority HOLD; do not
   certify full currentness of unavailable fields. Keep
   `UNAVAILABLE_BILLING` / `PENDING_PROTECTED_CI_AND_ADOPTION`.

## Checks performed

- 17 runtime tests pass with reviewer `TMPDIR` under the checkout; default
  macOS TMPDIR yields 3 fixture-git failures (documented compatibility limit).
- Frozen #1095 verifier `--self-test --status`, plain, `--no-git --status`:
  exit 0.
- MCR py_compile/self-test: exit 0.
- Canonical verifier: exit 0.
- PYAT plain/self-test: exit 0.
- Author R2 correctness probe: PASS 8/8 but does not cover the material-event
  defects.
- Old R1 probe raw exit 0 with hardcoded historical REVISE; raw outcomes show
  fake review/STOP/resolve refusals and live tokens present. It is not a green
  product test.
- Cold live `startup`/`what-next`/`status` exit 2 with four visible items;
  recommended next is B01 `RECEIVE` with owner/prerequisites; live time/digest
  did not reset from the baseline file.

## HQ post-review

After this reviewer process exits, the installed hook must validate and intake
`REVIEW_RECEIPT.json` from the prebound `CURRENTNESS_R2_G5` REVIEWER run and
then HQ must run a fresh-process `startup`/`status` against the author live
pair. Do not manually fabricate this receipt or the completion. Because this
verdict is `REVISE_EXACT_DEFECT`, HQ may close the review as RED but must not
adopt protected/native/full currentness. Fix the event/run boundary, then run
one focused rereceiving of the exact corrected source. No automatic author
cycle, #1095 G5 rerun, protected merge or fleet/Browser/PYAT operation. STOP.
