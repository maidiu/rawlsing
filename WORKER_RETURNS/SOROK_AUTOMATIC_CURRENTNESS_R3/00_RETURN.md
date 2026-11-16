# SOROK automatic currentness R3 — material-event authority correction

**Engineering:** `AUTHOR_CANDIDATE_FOR_FOCUSED_INDEPENDENT_RERECEIVING`
**Scientific:** `HELD` | **Authority:** `HOLD_SOURCE_AUTHORITY`
**Author session:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Job:** `sorok-programma-automatic-currentness-material-auth-repair-20261116-r3`
**Branch:** `codex/sorok-automatic-currentness-material-auth-20261116-r3`
**Base:** `d2883f60b1f8b0d83221051844eca7e11b72dc01` (actual R2 lifecycle banked)
**Rejected R2 source:** `ea5e48cf3240e72e39cd19be3120ad727902eee2`
**R2 review:** `53fad99fd8da86e4ab1cd12fdcfcd93fc8b2942f`, evidence
`f8006235266aa618963b186e5c357bf92be830b3`, verdict `REVISE_EXACT_DEFECT`
**Exact source commit / artifact SHA:** `WORKER_RETURN.json` and the HQ notification.
**Terminal:** one corrected frozen candidate for the same focused nonauthor
`ses_e2186e745ffecK1Ilg4cw26pVu`; no self-review and no protected merge.

## Received RED and exact reproduction

The entire reviewer package at `53fad99` was read and preserved: receiving,
`VERDICT.json`, handoff, `REVIEW_RECEIPT.json`, unchanged
`material_auth_probe.py`, and its report. The probe was rerun on the rejected
source `ea5e48` with only its own scratch path adapted. Result:
`3 fixed, 4 gaps, REVISE_EXACT_DEFECT` — untrusted `REJECTION`,
untrusted `PROTECTED_INTEGRATION`, unauthenticated `GITHUB_OBSERVATION`, and a
self-consistent fake worker run were accepted. The corrected source now returns
`7 fixed, 0 gaps, PASS` on the same probe. A separate fake-reviewer probe returns
`PASS` by refusing `UNTRUSTED_CONTROLLER_RUN`.

## One admission boundary implemented

1. **Trusted launch registry.** A private local HMAC capability under
   `state/runtime_capability.json` (mode `0600`, never logged or committed)
   signs `state/trusted_launches.json`. Attestation covers job/binding/launch/
   process/argv/session/grant/worktree/return path. The active R3 run was
   enrolled as an already-running launch with explicit migration provenance and
   the HQ operator authorization
   `hq-legacy-infra-resolution-20261115-r2`; launch ID
   `launch-fe3962d5863908ef9a580557b488ec0e`. Self-consistent fake runs with no
   real live process, no controller process tree, an untrusted root, a tampered
   registry, or no enrollment are refused. `migrate` now requires operator
   authorization; `control-event` accepts only control kinds.
2. **Rejection.** `REJECTION` is accepted only from a trusted `REJECTOR` run
   with matching task/session/expected source, a committed rejection artifact
   with predecessor, exact source hash and reason. The public CLI refuses
   `UNTRUSTED_REJECTION_SOURCE`. A real rejection sets B01 `REJECTED`,
   `claim_ready=false`, and the bounded repair/receiving action; B01 can no
   longer remain `READY_FOR_SCOPED_ENGINEERING`.
3. **Protected integration.** `PROTECTED_INTEGRATION` is accepted only from a
   trusted `PROTECTED_INTEGRATOR` run. The merge must exist, have exactly the
   asserted source as its second parent, and match the task source or a known
   protected foundation. `ci_state=PASS` alone cannot mint
   `PROTECTED_SOURCEFREE`: a fresh internal live observation must contain the
   merge check success and the matching observation digest. Otherwise the result
   is `PENDING_PROTECTED_CI_AND_ADOPTION` with an explicit hold. Known protected
   foundations are never downgraded. A fabricated `ffff…` merge is refused
   `PROTECTED_MERGE_LINEAGE_INVALID`.
4. **Live GitHub observation.** `GITHUB_OBSERVATION` is accepted only from
   `RUNTIME_INTERNAL_LIVE_FETCH` with a matching observation digest. Public
   caller flags/identity/digest/future expiry cannot promote an observation into
   `authenticated_checkpoint.live_github`. A fake `FAKE_SOURCE`/`evil` digest is
   refused `LIVE_GITHUB_OBSERVATION_UNTRUSTED_SOURCE`.
5. **Reviewer and verdict.** A non-replay review requires a trusted enrolled
   `REVIEWER` run with distinct role/session/task/expected source, the real
   return receipt, and an immutable `VERDICT.json`. The verdict comparison is
   exact equality, not `startswith`; a prefix or different grade is refused
   `REVIEW_VERDICT_ARTIFACT_MISMATCH`. A fully self-consistent fake reviewer run
   is refused `UNTRUSTED_CONTROLLER_RUN`. The actual R2 `REVISE` review remains
   historical, not acceptance.
6. **Controls and restoration.** STOP/RESUME/REVOCATION/RESTORATION and source
   holds require a competent, unexpired operator/source authorization bound to
   the exact kind/scope/event digest. Public event JSON cannot mint them.
   Authorized revocation and restoration were exercised: B03 became `REVOKED`,
   B05 `BLOCKED_BY_DEPENDENCY`, then restoration removed the revocation and
   restored their non-revoked readiness. Blanket RESUME is not accepted.

## Proof

- Reviewer probe, rejected source: `3 fixed / 4 gaps / REVISE_EXACT_DEFECT`.
- Reviewer probe, corrected source: `7 fixed / 0 gaps / PASS`.
- Fake reviewer probe: `PASS`, exact `UNTRUSTED_CONTROLLER_RUN`.
- Runtime tests: `27 passed` — the original 17 plus 10 focused R3 tests for
  public material-event refusal, trusted rejection, fake/real protected merge,
  fake reviewer, exact verdict, registry/run-path tamper, control CLI boundary,
  state-maintenance auth, trusted reviewer acceptance, and revocation/restoration.
- Local macOS workflow: frozen #1095 self-test/plain/no-git and all required
  canonical/Pyat/MCR checks exit `0`; changed `WORKER_COMMISSIONS` count `0`.
  These are local checks, not GitHub Actions PASS.
- Existing duplicate/out-of-order/crash/mixed-pair tests remain green; no new
  half-written pair path was introduced.

## Controller change

Only the narrowly leased installed `launch.py` was patched additively to invoke
`attest-launch` for bindings carrying `sorok_currentness`. Installed SHA-256
`4a7c243c0db89822ba8e51a1dd41ab6f63ad2929bef5508d64a78294aee8a370`; original
backup and exact diff are in `controller/`. `completion_events.py` is unchanged
`503f7b410343b1227cae9bf7cbbe130807e20a444915c12881030cdf19e02da2`;
`supervisor.py` is unchanged. Unaffected bindings keep their old behavior.

## Preserved current state

The pair is pre-exit generation `50`, checkpoint
`7e1fd6d057a4af6a3a3c2f97c976a0b6872e9a3d90ce76eaca703dfac72d3338`, retaining
the actual R2 worker return and `REVISE_EXACT_DEFECT` review at `ea5e`/`f800`.
The 27 tasks, 21 G/M/T decision nodes, gates, scoped holds, live GitHub source,
transactions and operator auth are unchanged. The installed R3 hook is expected
to record this R3 return as `mechanism_worker_return=RETURNED_REVIEW_PENDING`
after the real process exits; zero exit is not acceptance. HQ must cold-restart
and verify the new generation/checkpoint.

## Remaining holds

- Issue/comment status remains an honest `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE`
  hold for #939/#1008/#1010 (HTTP 403 through the existing connector).
- The real PR #1095 status advance remains a reconciliation item; no #1095 G5
  rerun.
- Actual independent review of this R3 source is pending; the author cannot
  self-review.
- Protected CI/adoption remains `UNAVAILABLE_BILLING`/pending; no protected
  merge, native science, actor/human authority or full original claim.
- No fleet, Browser, PYAT, SEAM, new provider, new scheduler or automatic
  dispatch was used.

**STOP** at this frozen corrected candidate for the same focused nonauthor.
