# SOROK S47 — actual interval material/activity conditioning in C9

**RESULT:** `S47_INTERVAL_C9_CONDITIONING__SAME_S46_PERSON__ACTUAL_CONDITIONING_SOURCE_IN_C9_READSET__ACTUAL_MATERIAL_FALSE_SCHEDULED_TRUE__CONDITION_CUT_RESTORE_COLD__FORGERY_REFUSED__13_OF_13_FOCUSED_TESTS__NO_TARGET__NATIVE_HOLD`.

S47 composes the current independently issued S46 interval state into the existing S36/C9 conditioning path for the next real S42 admission on the same S45/S44/S46 person. The C9 readset and material eligibility now consume the actual interval source instead of treating the interval receipt as metadata only. The accepted targetless C9 response behavior is preserved.

## Scope and base

- Existing author/session/provider/model MAX; no new workers, provider/model calls, timeout, or broad test run.
- Branch `codex/sorok-s47-interval-c9-conditioning`; base accepted S46 `f0ef39b92ce2e4add5c0a699389e12f1d7ae434e`.
- Writes only `WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1/**` plus the minimal existing S42 `session.py` and S37 `producer.py` C9 call-site seams. S46 and S45 source files remain exact at their accepted cuts.
- S46 interval production, S45 encounters, S44 root generation and S43 language remain the same person/root/branch/store/C12 history. No new daily event, psychology state, target proposal, or native issuance is created.

## Implemented composition

- `s47/conditioning.py` builds one source from the current validated S46 state. It uses the existing material class `ResolvedStructuralContext` and existing `make_conditioning_source`; it does not add a source class or a new C9 rule.
- Source content is `S47_INTERVAL_MATERIAL_CONDITION@1` and binds: actor, branch, interval state ID/receipt hash, domain issuance ID/hash, domain ID/hash/mode, status, exact interval coverage, currentness, interval-end `as_of`, material-after-interval, and explicit non-native/non-psychological/non-actor-knowledge/non-private-B flags.
- `qualify_source` revalidates the source against the current validated interval state and actual world material. Forged or stale actor, branch, coverage, currentness, access, source ref, source class, and source hash are typed `S47Refusal`s.
- S42 exposes the minimal `_extra_conditioning_sources` hook. S37 uses supplied qualified sources at the actual `run_candidate_path` call site; absent supplied sources it uses the accepted B-source path unchanged.
- For an admitted interval event, the qualified interval source is the controlling material source. This prevents the stale accepted B material envelope from masking the actual interval material result. The B base path remains unchanged when no interval source exists.
- The same S42 event remains `NO_CHANGE`/`NO_PROPOSAL` with zero target proposals. C9 consumes `objective_material_eligible`; no existing finite response rule maps interval material presence to a different target/action, so S47 does not invent one or claim an action change.

## Evidence

- Focused S47 tests: **13 passed**, 0 failed/error/skipped; `junit/s47_full.xml`, `logs/s47_full.log`, `evidence/test_run.json`.
- Runnable entrypoint: `run_s47.py` exits **0**; `run_s47_evidence.py` exits **0**; `evidence/entrypoint.json`, `logs/entrypoint.log`, `logs/evidence_run.log`.
- ACTUAL interval: `PARTIAL`, coverage `[[222, 223]]`; material after interval `0`; C9 interval source is in the actual readset; `objective_material_eligible: false`; targetless `NO_CHANGE`/`NO_PROPOSAL`.
- SCHEDULED_ONLY control: `NOT_PERFORMED`, coverage `[]`; material after interval `1`; C9 interval source is in the actual readset; `objective_material_eligible: true`; same targetless response, same root `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`.
- C9 source identity/currentness/coverage is present in `evidence/actual.json` and `evidence/scheduled.json`: current interval receipt, exact one-unit coverage for ACTUAL, current source hash, and the S47 source ref in `readset_refs`.
- Same-person S45 encounters remain SAY OK, DO_HELP refused under ACTUAL / accepted under SCHEDULED_ONLY, ATTEND NO_CHANGE; root and other-actor B state unchanged.
- Condition cut/restore: revoking the S46 condition refuses the real S42 admission with `S46_INTERVAL_CONDITION_REVOKED`; restoring reconstructs the same source hash and admits with the interval source in C9. Cold reopen reconstructs the same source hash, receipt, coverage and targetless C9 evidence.
- Source faults refused: actor, branch, coverage, currentness, access, as_of, material-after, source ref and source hash (`evidence/source_faults.json`). Original current source remains readable after comparisons.
- No interval: accepted C9 path remains usable with no S47 source and no target (`evidence/no_interval.json`).
- `evidence/source_manifest.json` shows S46 and S45 reused sources exact at their accepted cuts, and only the two minimal S42/S37 seam files changed.

## Limits

- S47 uses the existing `ResolvedStructuralContext` material class because the accepted consumer already treats that class as an actual material opportunity. This is a TEST_ONLY objective interval-material condition; it is not an empirical probability, native CAN008/CAN011/C12/ADP issuance, OBL062 closure, developmental T, childhood biography, or human person.
- The interval source is deliberately scoped to the current workshop scene and interval end. A future event in another scene is not material-eligible from this source; the source is still an objective readset fact, but S47 does not generalize the domain.
- S47 does not create a new C9 response rule, coefficients, learning, demographic-to-psyche conversion, target proposal, actor knowledge, private B motive, or native authority. Material eligibility is real in the C9 receipt; the finite response remains the accepted targetless response.
- No broad regression run was performed in the final evidence pass; the focused S47 run is the requested validation. Prior compatibility checks were not folded into S47 evidence.

## Commands

```text
PYTHONPATH=$PWD/WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1 \
M35_JOIN_E_RETURN=/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
python3 WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1/run_s47_evidence.py \
> WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1/logs/evidence_run.log 2>&1
```

**Terminal:** `S47_INTERVAL_C9_CONDITIONING__SAME_S46_PERSON__QUALIFIED_INTERVAL_SOURCE__REAL_C9_READSET_AND_MATERIAL_ELIGIBILITY__CONDITION_RESTORE_COLD__FORGERY_REFUSED__13_OF_13__NO_TARGET__NATIVE_HOLD`. Final commit and remote SHA are verified after push.
