# FIABC-T4 — Lifecycle Binding Contract

Required order:

`T3/I06A isolation receipt`
→ `exact lifecycle request`
→ `actual candidate-state action`
→ `I06C action validation`
→ `I06B telemetry admission`
→ `governed lifecycle/accounting receipt`.

A metric attached to a lifecycle action is not admitted before the action validates.

## Live action map

| Live stage | I06C action | Required physical fact |
|---|---|---|
| S01 | COLD_FIRST_REALIZATION | T3 absent-state receipt + actual first realization |
| S06 | AUDIT_REVALIDATION | executed audit primitive |
| S08 | WARM_RETAINED_STATE_USE | retained candidate-owned session exists before action |
| S09 A | AUDIT_REVALIDATION | actual persistence information audit; no fake rebuild |
| S09 B/C | DELETION_REGENERATION | actual session deletion + regeneration + lineage |
| S10 | SOURCE_INVALIDATION | actual invalidated unit(s) + actual recomputed unit(s) |
| S11 | AUTHORITY_SEMANTIC_INVALIDATION | actual invalidated unit(s) + actual recomputed unit(s) |
| S12 A/C where applicable | STALE_STATE_RECOVERY | changed governed determinant + detection + recovery |
| S13 A/C where applicable | CORRUPT_STATE_RECOVERY | actual corruption injection + detection + recovery |
| S14 | INTERRUPTION_RECOVERY | governed replay process actually interrupted, then recovered |
| S15 | FRESH_PROCESS_REPLAY | new Python process executes C11/I03/I05 and reproduces expected terminal identity |

Candidate-B cache stages and WVS-C zero-accelerator cache stages remain frozen skips where the T2 manifest says they are not applicable.

## Reject rules

The accepted I06C validator rejects:

- formula-derived lifecycle evidence;
- law-hash-only evidence;
- generic temp-file evidence;
- declarative-only evidence;
- warm state owned by another candidate or absent before use;
- deletion without actual deleted/regenerated object identities and lineage;
- invalidation without actual invalidated/recomputed units;
- stale exercise without a changed determinant;
- corrupt exercise without injected corruption;
- interruption that does not target/recover the governed operation;
- replay in the parent process;
- replay with the wrong terminal identity;
- lifecycle telemetry bound to the wrong action or binding.

## Source access remains governed

T4 does not widen a stage's empirical-source access bit merely to make a lifecycle action pass.

If a source-backed candidate cannot lawfully replay from the state/source made available by the governing T2/T3 stage tuple, the lifecycle action fails closed. There is no source substitution or synthetic fallback.

## Preserved stages

A preserved historical stage is not re-executed merely to obtain telemetry.

LiTS-A and LiTS-B preserved evidence is classified separately under the preserved-work law in `04_PRESERVED_WORK_LIVE_LEDGER.csv`.
