# HQ261 R01 — Owner diff, negatives and replay

## Owner diff

G03's entire code footprint versus the accepted HQ260 frozen base `788b2bf7…` is:

```
 rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py | 460 +++++++++++++++++++++
 1 file changed, 460 insertions(+)
```

**No production module changed.** Every owner blob is byte-identical to the accepted base
(table in `01_…json`). Consequently the G3 current/as-of lifecycle capability under review
was **already accepted at HQ260**; G03 adds only a new test over it.

Files G03 also touched are handoff/control documents and its own return directory:
`HQ_HANDOFF/DECISION_LEDGER.jsonl`, `HQ_HANDOFF/LATEST.json`, the HQ260 checkpoint
`CURRENT.json` / `CURRENT.md` / `MANIFEST.json`,
`PYAT_CONTROL_ROOM/EE14_SOURCE_FREE_SELECTED_USE_COMPETENCE_HQ260_R1.md`,
`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/…`,
`WORKER_COMMISSIONS/PYAT-HQ260-G3-CURRENT-ASOF-LIFECYCLE-COURT-R1/…`, and
`WORKER_RETURNS/PYAT-HQ260-G3-CURRENT-ASOF-LIFECYCLE-COURT-R1/…`.

**Note on control documents.** G03 modified `HQ_HANDOFF/LATEST.json` and a checkpoint
`CURRENT.json`. Per this commission, worker-local `LATEST.json` is branch-frozen at HQ260 and
is **not** a live checkpoint. I did not treat G03's `LATEST.json` as live control, and I did
not rely on it. This review resolved live control from origin independently. HQ should decide
separately whether those control-document edits are in-scope for a worker return; that is a
control question, not a code defect, and it did not affect any result above.

## Negative coverage

All eight commissioned attack classes are covered by real tests, not prose. The two most
load-bearing are:

- `g3_self_proclaimed_current_receipt_is_refused` — a self-declared currentness receipt is
  refused. This is the direct analogue of the HQ235 lesson that a self-declared owner
  reference is not proof of custody.
- `g3_unknown_selection_key_is_refused_not_guessed` and
  `g3_owner_unknown_analytical_dependent_is_never_current` — unknown selection keys and
  unknown analytical dependents resolve to UNKNOWN / never-current rather than being guessed.

Invalidation is covered on **both** axes by
`g3_affected_and_unaffected_dependency_transition` (affected versus unaffected dependencies
must transition differently) and `g3_invalidated_release_cannot_be_served_as_current`.

## Replay

Two distinct replay claims are covered and both passed:

1. **Historical as-of** — `g3_as_of_event_and_as_of_checkpoint_agree` and
   `g3_historical_as_of_still_resolves_the_prior_product`, i.e. an as-of event and the
   checkpoint agree, and the prior product is still correctly resolved.
2. **Fresh-process checkpoint reconstruction** —
   `g3_fresh_process_checkpoint_reconstruction`, which genuinely spawns a **separate
   interpreter** via `subprocess.run` (test file line 284). This is not an in-process
   simulation, so it actually exercises reconstruction from a cold start rather than reusing
   in-memory state.

## Stage-grade versus service-specific

All 97 cases are **stage-grade local owner capability over source-free material**. Explicitly
out of their scope, and therefore neither exercised nor granted:

- real service join; a real model; T1 model-use grant; T2 service use
- FF02 positive relation; EE12 pair authority; EE14 model-use competence
- actor/V3 authority

Two of G03's fifteen tests are themselves honesty guards — `g3_no_new_adapter_module_was_manufactured`
and `g3_court_claims_no_service_or_model_use_permission` — which is appropriate scope hygiene
for a court that must not imply permissions it does not hold.

No test here is expected to fail merely because a later service join arrives, and none would
*detect* a service-join fault. Both statements are about scope, not quality.

## Verdict basis

Acceptance rests on: exact final-SHA reproduction of 15/39/43/97 on clean committed source;
zero owner-code change against the accepted HQ260 base; a genuine separate-process replay
case; and real-owner imports with 32 assertions across 15 tests. The one weakness I found is
in **my own** probe methodology, recorded above — dependency was demonstrated, graded
sensitivity was not.
