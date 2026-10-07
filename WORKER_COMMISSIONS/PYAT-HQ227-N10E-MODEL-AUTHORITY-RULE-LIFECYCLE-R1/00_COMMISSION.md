# PYAT HQ227 — N10E MODEL-AUTHORITY / MODEL-RULE LIFECYCLE REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** authority-sensitive replay/dependency implementation worker  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**BRANCH:** `agent/rabochii-pyat-hq227-n10e-model-authority-rule-lifecycle-r1`  
**EXACT STARTUP TIP:** `b5ba9ebfc7bc8e6c07aa8799ce9c76d64d5ca03d`  
**PRIOR REVIEW:** `agent/reviewer-pyat-hq226-n10e-owner-authentic-lifecycle-final-rereview-r1 @ 41cfff87a9ff659ec452a49fe5b4dacab455d2e2`  
**PRIOR DISPOSITION:** `N10E_OWNER_AUTHENTIC_LIFECYCLE_AUTHORITY_OVERREACH`

Read HQD-216 and AT17/AT18/AT19.

## Exact remaining defects

1. **MODEL AUTHORITY BASELINE BODY/REF MISMATCH**  
   Actual runner constructs a model AuthoritySnapshot whose semantic body differs from the authority-content hash it reuses.

2. **MODEL RULE SEMANTIC IDENTITY NOT LIFECYCLE-BOUND**  
   Provider/result consume `model_rule_hash`, but graph closure does not independently bind the exact rule determinant or prove the entire rule material is cryptographically owned by the authority refs.

3. **ACTUAL RUNNER DOES NOT CONSUME SEALED MODEL SUCCESSOR SNAPSHOT**  
   Recomposition receives a bare successor AuthorityRef rather than exact sealed/selected successor snapshot material.

## Mission

Close these three defects without weakening the repaired query/predicate ownership path.

### Baseline model authority
The baseline model authority used by the fresh runner must be owner-authentic:
- exact body;
- exact authority ref/hash;
- content hash recomputed/verified from the constitutive body where owner law requires it;
- no old-body/new-hash or changed-body/reused-hash construction.

If installed fixture material cannot produce a truthful snapshot, fail closed and return the exact upstream authority-material blocker.

### Model rule identity
Represent the exact consumed model-rule semantics truthfully.

Either:
- register an exact model-rule determinant with determinant-specific owner evidence and graph reachability; or
- prove the full model-rule material is cryptographically identity-bearing inside an already-consumed exact authority object so no separate determinant exists.

Do not merely bind a free-floating `model_rule_hash` string.

Mandatory hostile:
change rule material while holding existing authority refs fixed. This must either:
- move/refuse the authority identity as required; or
- be detected as unowned/unbound and fail lifecycle-coverage claims.

### Model successor
Use the actual successor snapshot sealed and selected by `AuthorityMaintenanceExecutor`, not a proposed/bare AuthorityRef.

Recomposition must verify exact snapshot body/ref/hash and consume that snapshot’s model rule semantics.

## Preserve prior repairs

Sustain:
- total exact-determinant classification;
- source-universe and EmpiricalFact dependency paths;
- determinant-specific owner evidence;
- real sealed query successor;
- family-safe query/predicate replacement;
- edge-deletion hostiles;
- positive provider→composition→slice→consumer path.

## Residual owner limits

Do not fake:
- C11LogicalRelease ownership;
- unstaged comparability/walkback authority material;
- affected-but-identical recomputation if accepted owner forbids same-ref replacement.

## Runtime

Execute targeted N10E + directly dependent owner/provider courts on a lawful runtime surface. No adoption-ready claim without actual court evidence.

## Write terrain

Production:
- `rawlsing_next/pre553_analytical_replay_dependency.py`

Court/runner:
- `rawlsing_next/tests/test_pre553_n10e_provider_replay_lifecycle_court.py`
- `rawlsing_next/tests/n10e_provider_replay_lifecycle_runner.py`

Do not mutate authority-maintenance, provider, analytical composition, learned lifecycle/release, or positioned-subject consumer owners.

## Required return

Write only:
`WORKER_RETURNS/PYAT-HQ227-N10E-MODEL-AUTHORITY-RULE-LIFECYCLE-R1/`

Required:
- `00_RETURN.md`
- `01_BASELINE_MODEL_AUTHORITY_AUTHENTICATION.json`
- `02_MODEL_RULE_IDENTITY_AND_GRAPH_BINDING.json`
- `03_SEALED_SUCCESSOR_RECOMPOSITION.json`
- `04_RUNTIME_COURT_PRODUCTIVE_PATH_AND_RESIDUALS.json`
- `05_FINAL_DISPOSITION.json`

Allowed:
- `N10E_MODEL_AUTHORITY_RULE_LIFECYCLE_COMPLETE__READY_FOR_FINAL_REREVIEW`
- `N10E_MODEL_AUTHORITY_RULE_LIFECYCLE_PARTIAL__NAMED_DEFECT`
- `N10E_MODEL_AUTHORITY_RULE_LIFECYCLE_BLOCKED_BY_AUTHORITY_MATERIAL`
- `N10E_MODEL_AUTHORITY_RULE_LIFECYCLE_REVEALS_ARCHITECTURE_CONFLICT`

Push only this branch; report exact SHA.
