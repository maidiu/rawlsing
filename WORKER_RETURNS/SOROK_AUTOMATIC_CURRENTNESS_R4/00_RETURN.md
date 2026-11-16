# SOROK automatic currentness R4 — launch enrollment and session authority

**Engineering:** `AUTHOR_CANDIDATE_FOR_FOCUSED_INDEPENDENT_RERECEIVING`
**Scientific:** `HELD` | **Authority:** `HOLD_SOURCE_AUTHORITY`
**Author session:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Job:** `sorok-programma-automatic-currentness-launch-auth-repair-20261116-r4`
**Branch:** `codex/sorok-automatic-currentness-launch-auth-20261116-r4`
**Base:** `a60bffc293cf8805cd80fc2a95e4e0369be916c3` (real R3 review intake, generation 52)
**Rejected R3 source:** `0b2664a8353f5957e1dad4bb5678be66fa9470ef`
**R3 review:** `b83438438dcb82eec43d23f170cf5672269edf54`, evidence
`a49be6e8bf728262dad62753f3066e99351b7af9`, path
`WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R3_G5/`, verdict
`REVISE_EXACT_DEFECT`.
**Exact source commit / artifact:** `WORKER_RETURN.json` and the HQ notification.
**Terminal:** one corrected frozen candidate for the same focused nonauthor
`ses_e2186e745ffecK1Ilg4cw26pVu`; no self-review and no protected merge.

## Exact residual RED corrected

The R3 reviewer package and its hostile launcher were read at `a49be6e8` and
preserved. The exact `evidence/raw/fake_attest/launch.py` witness was run
against the rejected source `0b2664a8` and reproduced the bypass: a
caller-authored `launch.py` with `--binding/--job` strings, its own live
supervisor/observer/child tree, and a self-consistent REVIEWER run received
`TRUSTED_LAUNCH_ATTESTED`; the fake REVIEWER run was then accepted by
`intake-review` even though its `job.session` was `ses_FAKE_ATTEST` and the
receipt expected this reviewer. The old author R4 run's actual attestation was
also made by that pre-fix R3 launcher; it is preserved and was migrated under
an explicit HQ operator enrollment, not retroactively called an R4 proof.

## Root fix

1. **Installed-launcher proof, not a command string or PID tree.** The runtime
   now requires a launcher proof consisting of:
   - the exact installed controller launcher path and reviewed SHA-256 from a
     fixed local identity file outside mutable config;
   - an HMAC token over the exact launch spec (`run_dir`, job, session, grant,
     argv digest, worktree, role, task, expected session, expected source)
     using a fixed local launcher key; and
   - the existing live-process sanity checks.
   The installed `launch.py` computes the proof from its own resolved path/hash
   and the spec and passes it via the child environment. The key and identity
   are local `0600` files outside the repo; neither key nor token is logged,
   committed or printed.
2. **No public self-attestation.** A caller-authored `launch.py` at another
   path, a byte-copy, a wrong hash, a wrong token, an own live PID tree, or a
   mismatched session/job/source/role is refused. Exact fake witness:
   old `TRUSTED_LAUNCH_ATTESTED` and fake review `EVENT_RECORDED`; corrected
   exact fake refuses `TRUSTED_LAUNCH_ACTUAL_SESSION_MISMATCH`, matching-session
   fake refuses `LAUNCHER_PROOF_REQUIRED`, and corrected fake review refuses
   `UNTRUSTED_CONTROLLER_RUN`.
3. **Actual-session binding.** Enrollment and intake require
   `job.session == binding.session == binding.expected_session` and the trusted
   registry's actual session. Review additionally requires
   `job.session == receipt.reviewer_session`, a distinct author session, and
   `receipt.implementation_commit == binding.expected_source_commit` with exact
   verdict equality. The fake R3 run with `ses_FAKE_ATTEST` can no longer pass
   on the expected-session field alone.
4. **Operator authorization cannot be self-issued.** High-risk operator
   purposes (`TRUSTED_LAUNCH_ENROLLMENT`, `STATE_MAINTENANCE`) require an
   operator authorization signed by the fixed local launcher key. Ordinary
   signed operator controls remain supported; unsigned enrollment fails
   `OPERATOR_AUTHORIZATION_SIGNATURE_REQUIRED`.
5. **Migration, not fake prior authority.** The real R4 run was launched by the
   old R3 launcher and has its old `attestation.json`. Its registry entry is
   explicitly migrated to `HQ_EXPLICIT_ACTIVE_RUN_ENROLLMENT` with the HQ
   authorization `hq-legacy-infra-resolution-20261115-r2`; the old
   `TRUSTED_LAUNCHER_ATTESTATION` is preserved under `legacy_attestation` and
   remains visible. No job/binding/launch/process/completion record was edited.
6. **Positive installed launcher.** The actual installed `launch.py`
   (`cfd180ac…`) launched a sandbox qualification job and auto-attested it with
   `TRUSTED_LAUNCHER_ATTESTATION`, exit `0`. A future real review run launched
   by this controller will attest without arbitrary caller privilege.

## Proof

- Exact hostile witness, old cut: attest exit `0`, fake review exit `0`.
- Corrected exact hostile witness: attest exit `1`,
  `TRUSTED_LAUNCH_ACTUAL_SESSION_MISMATCH`; fake review exit `1`,
  `UNTRUSTED_CONTROLLER_RUN`.
- Corrected matching-session hostile launcher: attest exit `1`,
  `LAUNCHER_PROOF_REQUIRED`.
- Launcher-proof variants: exact positive accepted; same basename/different
  path and byte-copy `LAUNCHER_PATH_MISMATCH`; wrong hash
  `LAUNCHER_HASH_MISMATCH`; wrong token and mismatched job/session/source/role
  `LAUNCHER_TOKEN_MISMATCH`.
- Runtime tests: `34 passed` (28 prior + 6 R4) covering proof tamper, unsigned
  enrollment, actual-session enrollment/review mismatch, expected-source
  mismatch, replay, registry/run-path tamper, and the retained R1/R2/R3 reds.
- Reviewer R2 material probe: `7 fixed / 0 gaps / PASS`; fake reviewer probe:
  `UNTRUSTED_CONTROLLER_RUN`.
- Local macOS workflow: frozen #1095 self-test/plain/no-git, MCR py_compile and
  self-test, canonical PROGRAMMA, Pyat visibility plain/self-test all exit `0`;
  changed `WORKER_COMMISSIONS` zero. Not GitHub Actions PASS.

## Current state and holds

The pair is pre-exit generation `52`, checkpoint
`476fc4fb24bba99a7b5a24fba0d6aafe0641eacb5e02e3d5a9f9b3a5eb2703b1`, with the
actual R3 `REVISE_EXACT_DEFECT` review at `0b2664a8`/`b8343843` preserved as
history. The R4 hook is expected to record
`mechanism_worker_return=RETURNED_REVIEW_PENDING` after the real process exits.
The 27 tasks, 21 decision nodes, seven protected foundations, scoped B05/C04/C05
pins, #939 STOP, Browser #1008/#1010 terminal bounds and #1012 unlaunched remain
unchanged.

Remaining holds: issue/comment GitHub reads are HTTP `403` source-authority
holds (#939/#1008/#1010); PR #1095 status advance remains unreconciled; actual
independent review of R4 is pending; protected CI is `UNAVAILABLE_BILLING`;
native science/actor/human authority and full original claim remain `HELD`.
No #1095 G5 rerun, protected merge, fleet, Browser, PYAT, SEAM, new provider or
automatic dispatch was used.

**STOP** at this frozen corrected candidate for the same focused nonauthor.
