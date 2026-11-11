# MII final checkpoint independent receiving — 49720bf

**Checkpoint verdict:** `REVISE_EXACT_DEFECT` — sourcefree implementation is substantially repaired and the author suite passes, but duplicate `look` requests still double-count adaptive evidence. Full sourcefree engineering is not accepted.

**Tested author SHA:** `49720bf5e532cfd0588d7ae8255ee103cd6ced76`
**Prior checkpoint:** `eb2e53d89d2acef556da6b6fb7ceb6622c9604dc`
**Prior adverse findings preserved:** `319a2060d`, `d33e58d5b4b8b841227f7e2356a970d44171508d`, `99f428fc1`.
**Commission:** replacement complete-construction commission in the review workspace.

## Executed evidence

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_mii.py

# 17 passed in 532.88s
```

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_REVIEWS/SOROK-MII-49720BF-FINAL-R3/test_final_adverse.py

# 1 passed, 1 failed
# FAILED test_duplicate_look_does_not_double_count_adaptive_evidence
# second weight 3 != first weight 2
```

The passing independent test confirms the R2 correction: exposure records now retain the full `candidates` map separately from the actually `offered`/`selected` detail. The failing test is a real P6 consumer reproducer, not a helper-only assertion.

A proportionate local timing probe of three warm turns from one state produced:

```text
init 7.726092 / 3.020328 / 3.044629 s
availability 3.69e-05 / 3.55e-05 / 3.55e-05 s
ledger 8.56e-04 / 1.18e-03 / 1.19e-03 s
recognition/update 4.30e-03 / 1.01e-04 / 1.02e-04 s
composition 6.19e-04 / 9.64e-04 / 1.16e-03 s
total 7.731916 / 3.022620 / 3.047126 s
```

The committed `measurements.json` reports cold CLI n=13, p50 6.340 s, p95 9.688 s, max 12.873 s; warm import n=5, p50 3.101 s, p95 3.106 s; zero provider calls/tokens; child RSS 50.730 MiB; state 1,600,669 bytes; gallery hinge identity present. I did not invent a performance threshold and did not independently rerun the full 13-command measurement harness.

## Repaired findings verified

- Foreign `observer=B` is denied optional/close detail for user `U`.
- Forged persisted `recognized` data is discarded; committed inspection is required for earned recognition.
- A previously selected detail gets adaptive weight 1; a previously omitted available target gets independent weight 2.
- Committed house-source denial/restore, per-object qualification, gallery and symbolic fixtures, P2 fork profile isolation, corrupt/tampered profile reset, and interrupted exposure save all pass the changed author suite.
- `test_user_derivative_does_not_enter_actor_packet_or_action` confirms user labels do not enter the actor packet or alter the authorized Nadia movement.

## Concrete defect: duplicate look still increments adaptive evidence

`run_p6.py:151-155` calls `mii.update_attention` whenever the latest action target matches and the command is `look`. `mii.record_exposure` deduplicates the duplicate request at `mii.py:263-270`, but `update_attention` is called independently and increments the hypothesis again at `mii.py:278-300`.

Reproducer: `test_duplicate_look_does_not_double_count_adaptive_evidence` in `test_final_adverse.py`.

Observed:
- first `look sandals` with `request_id="same-look"`: weight `2`;
- identical duplicate request: weight `3`;
- the P4 ledger remains unchanged, so this is not a new world action.

This violates the duplicate-request/idempotence and adaptive-evidence requirements. The smallest correction is to return a “newly created” flag from `mii.record_exposure` (or compare exposure sequence/count before and after) and call `update_attention` only for the first, non-replayed exposure.

## E1–E10 and original 44 assessment

- **E1:** committed source denial/restore and exact speech are exercised; no unresolved defect found here.
- **E2:** observer and per-object qualification now work in the changed suite; fixture qualification remains sourcefree-only.
- **E3:** the R2 missing-candidates defect is repaired; duplicate look still corrupts adaptive evidence.
- **E4:** committed recognition and taught/corrected labels are separated; forged persisted recognition is rejected.
- **E5:** competing hypotheses and simple decay are present, but the duplicate-look defect invalidates the claimed evidence accounting; `test_stale_evidence_decay_and_correction_change_selection` is primarily helper-level rather than a full P6 consumer proof.
- **E6:** surface budget/mandatory/optional separation passes.
- **E7:** existing P4/P6 ingress remains the action path.
- **E8:** corrupt/missing/tampered profile and actual P2 fork reset pass; interrupted save passes the focused test.
- **E9:** measurements are present and internally consistent with the provider/storage fields; independent full re-measurement is NOT_RUN.
- **E10:** README, measurement artifact and 17-test MII suite exist. The 44-ID table is still largely a cross-suite mapping, not 44 independently executed current-head assertions; the author's stated sourcefree scope therefore cannot be accepted as fully executed without correcting the duplicate defect and making the 44 mapping execution evidence explicit.

## Finite remaining work

- Fix duplicate-request adaptive update idempotence and add a regression that asserts unchanged hypothesis weight.
- Convert helper-only E5/G03/G08 evidence into real P6 consumer tests where the claim is made.
- Provide per-ID current-head execution evidence for the 44 mapping; existing alternate-suite evidence may be reused only where source behavior is unchanged.
- Independent full performance rerun remains optional/not run; no invented threshold is required.
- Native science, human validity, live provider, production privacy approval and protected merge remain excluded.

No implementation or existing tracked source was modified. Only this reviewer test/report is owned in `WORKER_REVIEWS/SOROK-MII-49720BF-FINAL-R3`.
