# Independent negative witnesses

Executed with the F0R3 candidate validator at blob `2fc1c3c7…` against the exact PR #519 current 32-event / 32-flight corpus at `59c9a7a4…`.

## Preserved old 13

The original validator's 13 frozen witnesses remain present and fail closed in both the original and candidate:

| ID | Mutation | Expected/observed rejection |
|---|---|---|
| W1 | duplicate event | `DUPLICATE_ID` |
| W2 | fake full adoption | `ADOPTION_REQUIRES_EXTERNAL` |
| W3 | self-review | `SELF_REVIEW` |
| W4 | flight SHA mismatch | `FLIGHT_LOG_EXACT_SOURCE_MISMATCH` |
| W5 | illegal science grade | `COURT_INVALID` |
| B1 | fake adopted worker status | `FAKE_ADOPTED_STATUS` |
| B2 | owner rewrite | `INITIAL_WORKERS_REWRITTEN` |
| B3 | known-RED removal | `INITIAL_EVENTS_REWRITTEN` |
| B4 | science promotion in frozen seed | `INITIAL_EVENTS_REWRITTEN` |
| B5 | unbound reviewer target | `REVIEW_TARGET_NOT_BOUND` |
| B6 | fully filled fake adoption | `ADOPTION_REQUIRES_EXTERNAL` |
| B7 | historical event finding rewrite | `INITIAL_EVENTS_REWRITTEN` |
| B8 | fake merged PR status | `INITIAL_PRS_REWRITTEN` |

The original validator passes with 13 witnesses. The candidate preserves all 13 and passes with 20.

## New N1–N7 at current head

| Witness | Exact mutation | Original | Candidate error |
|---|---|---|---|
| N1 | Post-seed flight `source_authority=NATIVE_CAN_ADP_PYAT_FULL_GRANT` | **ADMITTED** | `FLIGHT_13_UNVERIFIED_SOURCE_AUTHORITY` |
| N2 | `F2-RETURN` scientific grade `ACCEPT_SCOPED` by nonissuer | **ADMITTED** | `EVENT_14_SCIENCE_NONISSUER` |
| N3 | Independent review targets a merely commissioned F1 event | **ADMITTED** | `EVENT_32_REVIEWER_TARGET_RETURNED_ONLY` |
| N4 | PR 519 status `OWNER_REVIEWED_NO_REMOTE_PROOF` | **ADMITTED** | `PR_REMOTE_STATE_UNVERIFIED_519` |
| N5 | Post-seed event reuses an earlier immutable SHA | rejected via flight/log mismatch | `EVENT_12_APPEND_REUSES_PRIOR_IMMUTABLE_SHA` plus the same flight/log mismatch |
| N6 | Backfill PR 513 after seed max | **ADMITTED** | `PR_APPEND_ORDER_513` |
| N7 | Authority grade `ACCEPT_SCOPED` by nonissuer | **ADMITTED** | `EVENT_14_AUTHORITY_NONISSUER` |

N5 is the one case the original also rejects, but for a different reason; the candidate adds the dedicated append-reuse witness. The candidate cannot create a false negative by treating the original's incidental log mismatch as sufficient.

## Legal nonadopted candidate

The candidate accepts an appended event with state `OWNER_ADOPTION_CANDIDATE`, `adoption=false`, matching flight state and owner. Both original and candidate return no errors. This proves the guard does not ban lawful nonadoption while refusing fabricated adoption.

## Import of the result

The candidate's 20-witness PASS is an offline structural/custody result. It does not prove:

- reviewer identity or signature;
- source-owner or science-issuer permission;
- the real merged target SHA;
- a real importing first consumer;
- paired Sorok/Pyat progress;
- repository protection or required checks.

Those remain external owner/admin/privileged-verifier gates.
