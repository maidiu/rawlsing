# PRE-V3 Ninth-Wave Final Registry R1

Status: `W9_K01_K06_COMMISSIONED__PARALLEL_RELEASE_ACTIVE`

HQ eighth-wave fan-in authority: `a93e3717d9bea1857937a3fa278a933283948acc`

| ID | Branch | Commission tip | Exact grain | Library |
|---|---|---|---|---|
| K01 | `agent/rabochii-prev3-w9-k01-world-time-contract-reconcile-r1` | `34461439f274ea1630f76c9b9bfec803e73a6b46` | `PREV3_WORLD_TIME_NONTEMPORAL_RELEASE_STATUS_CONTRACT_RECONCILIATION_AND_RECEIPT_RERUN_R1_ONLY` | NO |
| K02 | `agent/rabochii-prev3-w9-k02-source-state-target-production-integration-r1` | `d2e025a4199cd631521b815705de02ec89d9adf3` | `PREV3_SOURCE_AGNOSTIC_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_PRODUCTION_INTEGRATION_R1_ONLY` | NO |
| K03 | `agent/rabochii-prev3-w9-k03-lits-q301-target-risk-authority-r1` | `549d0c3e8474ed7d2429d8ca34042578bfcb2e10` | `LITS_I_Q301_PRODUCT_TARGET_AND_PREQUERY_RISK_SET_AUTHORITY_RECONCILIATION_R1_ONLY` | NO by default; may inspect already-bound exact LiTS authority only |
| K04 | `agent/rabochii-prev3-w9-k04-position-publication-implementation-r1` | `e20028326cdf4fa653a54f25b5cf40692799cd90` | `PREV3_OBJECTIVE_POSITION_FACT_OWNER_PRESERVING_V557_V558_PUBLICATION_IMPLEMENTATION_R1_ONLY` | NO |
| K05 | `agent/rabochii-prev3-w9-k05-c09-rerun-r1` | `5ee80843b26382f39298c63c269afad15a5c361b` | `C09_FINAL_CANDIDATE_NEUTRAL_PHYSICAL_COMPARISON_RERUN_R1_ONLY` | YES — exact WVS7 package + exact LiTS-I carrier only |
| K06 | `agent/rabochii-prev3-w9-k06-sig004-structural-owner-adjudication-r1` | `d8f55b07910ba93b04a8cf7f8f34897a5cdcf2f5` | `V555_SIG004_OBJECTIVE_STRUCTURAL_PARTICIPANT_CHANNEL_OWNER_AUTHORITY_ADJUDICATION_R1_ONLY` | NO by default |

Parallelism:
- K01-K06 may all begin immediately.
- K02 and K03 are deliberately parallel; HQ reconciles them before learned-world re-execution.
- K02 candidate production integration requires fresh independent qualification before central integration.
- K03 does not execute the learned workload.
- K04 implementation requires fresh independent hostile qualification before central integration.
- K05 is the actual C09 rerun, not a readiness audit.
- K06 does not compose M2.
- K01 receipt PASS wakes separate world-validity + first real world-root construction.

Preserved law:
- PRE-V3 objective-world only.
- No raw source token has universal semantics by identity alone.
- Missing/typed-missing/not-applicable does not silently alter denominator membership.
- No post-outcome denominator mutation.
- No OBL063 driver/type/person-terminal semantics.
- No all-lanes barrier.

PRE-V3 remains `NOT_PROJECT_COMPLETE`.

Terminal: `PREV3_NINTH_WAVE_K01_K06__COMMISSIONED__PARALLEL_RELEASE_ACTIVE`
