# Executed, RED, and NOT_RUN

## Executed

| Check | Result | Evidence |
|---|---|---|
| New preflight tests | 22/22 PASS | `evidence/preflight_tests.xml` |
| Positive technical fixture | `TECHNICAL_PREFLIGHT_PASS__NATIVE_FALSE__PRODUCTION_EMPTY` | `evidence/preflight_positive_receipt.json` |
| Named negative preflight cases | 10/10 REFUSED with expected reason | `evidence/negative_preflight_receipts.json` |
| N1 source-neutral method rerun | 21/21 PASS | `evidence/n1_rerun.xml` |
| BP2P4J technical chain fresh rerun | 98/98 PASS, 0 failures/errors/skips, 150-file manifest | `evidence/existing_product_fresh_rerun.json` |
| Production registries at BP2P4J commit | 0 response rules, 0 target rules | `evidence/production_registry_receipt.json` |

The preflight positive is a technical fixture. Its receipt is `native=false`, `native_issued=false`, `production_registries=EMPTY`, `grant_written=false`.

## Not run

| Item | Status | Why |
|---|---|---|
| Real original A/B source ingestion | `NOT_RUN` | no current authorized original source or host/purpose grant exists |
| Real ADP010 encounter | `NOT_RUN` | no real contact witness |
| Real ADP019 E1 | `NOT_RUN` | no admission receipt |
| Concrete CAN008 RULE_A | `NOT_RUN` | registry empty; no issued rule |
| Separate CAN011 RULE_T/grant | `NOT_RUN` | registry empty; no issued grant |
| Native C8 protected writer | `NOT_RUN` | D1/D2/D3 held |
| Native C9→C12/A0/A2 positive | `NOT_RUN` | no native input and no native rules |
| Real later E2 | `NOT_RUN` | no independent performed action |
| Pyat N11/N12 or world use | `NOT_RUN` | R53 user STOP and N11_NOT_READY/N12 HOLD |
| C11 weld / native C12 | `NOT_RUN` | separate authorities held |
| Raw LiTS respondent rows | `NOT_READ` | no current permission; privacy/rights |
| R26E/R26V full suites | `NOT_RERUN` | author evidence read; not needed to establish source absence |

## RED / residuals

| Residual | Type | Consequence |
|---|---|---|
| No actual original A/B longitudinal source | source blocker | native practice test cannot start |
| Cross-sectional LiTS cannot supply A/B biography | scientific blocker | using it would be demographic psychogenesis |
| No concrete CAN008 RULE_A | issuer blocker | no lawful response transaction |
| No separate CAN011 RULE_T/grant | issuer blocker | no lawful durable practice target |
| C8 D1 old writer callable | security residual | acknowledged history can be erased by a legal legacy writer |
| C8 D2 unkeyed digests and format-only capability | security residual | forgery and rollback remain possible without a protected key and monotonic anchor |
| C8 D3 ADP019/E2 absent | occurrence residual | no authenticated native occurrence or performed action |
| R26E raw SQLite deletion and same-user witness | custody residual | append-only is not an OS completeness boundary |
| R26V global actor-builder patch | engineering residual | source histories can leak across runs; not a stable typed injection |
| H0 role/selection/fixture | scientific residual | not excluded by any current test-only positive |
| Preflight native verifier absent by design | authority residual | native pass cannot be produced without a real verifier |
| No distributed/production deployment | product residual | no A4/A5 human-experience claim |

## Falsifiers exercised

The preflight refuses at least the following, with the named reason preserved in `evidence/negative_preflight_receipts.json`:

- forged source content hash;
- self-signed CAN008 rule;
- unissued/missing rule;
- absent ADP019 E1 admission;
- stale source permission;
- malicious readset refs;
- backwards E2 clock;
- self-actuator E2;
- native candidate without verifier;
- nonempty production registry.

## Honest proof ceiling

`ASSERTION_EFFICACY_PROVED`: the preflight tests assert specific refusal codes on the exact mutated edge; the positive fixture asserts a pass with native false and empty production. `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED`: the named negative cases are the controls; the positive technical fixture survives. `NOT_PROVED`: that a real original A/B source or native rule exists, that a real person was generated, that C11/C12 was welded, or that A4/A5 human experience was demonstrated.
