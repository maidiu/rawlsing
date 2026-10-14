# HQ298 S-M-LAB2 — precise MODEL_BEHAVIORAL_HOLD

**Hold ID:** `MODEL_BEHAVIORAL_HOLD`
**Missing authority class:** `MISSING_ACTOR_OR_MODEL_USE_AUTHORITY`
**Model calls issued by this commission:** **0**
**Hosts affected:** ALL (per commission `OBJECTIVE_FALLBACK / STOP`: "No model API grant => MODEL_BEHAVIORAL_HOLD on ALL hosts; continue authorized sourcefree tests locally")

## Why the hold is exact, not generic

The commission's model-call gate is explicit:

> "Model-call gate: prior LAB1 having used OpenCode does NOT license model-actor trials. Confirm named provider, exact model/version, privacy permission, use grant and explicit monetary cap BEFORE any paid, actor or external model call. If missing, execute only sourcefree heldout/negative invariants and return MODEL_BEHAVIORAL_HOLD with exact missing grant; do not submit extra calls by inference."

The launch adds: "Make ZERO new paid or actor/model calls without exact provider, model, privacy, cost-cap and experiment-use authorization" and "Specialized model access requires a separate explicit grant."

**No such grant exists in the commission, the launch message, or any binding authority read for this job.** Therefore zero behavioral model calls were issued — by me or by any tool I ran — and none may be issued by inference from local credentials or from the predecessor's authoring-environment use.

## Exact missing grant fields (all 8 required; all 8 absent)

| Required field | Status |
|---|---|
| `named_provider_exact_endpoint` | **MISSING** — no provider named in commission/launch/authority |
| `exact_model_and_version_pin` | **MISSING** — no model/version named for behavioral actor trials |
| `privacy_permission_for_synthetic_lab_packets` | **MISSING** — no permission to transmit lab packets to any external model |
| `experiment_use_grant_behavioral_actor_trials` | **MISSING** — no behavioral/actor trial use grant |
| `explicit_monetary_cap` | **MISSING** — no monetary cap issued |
| `price_class_and_quota_observed` | **MISSING** — no price class or quota bound |
| `raw_request_response_retention_permission` | **MISSING** — no permission to retain raw call captures |
| `per_trial_call_budget` | **MISSING** — no per-trial call budget |

Machine-readable: `outputs/model_gate_decision.json`, `outputs/behavioral_run_result.json` (mode `HOLD`, `model_calls_issued: 0`).

## What a grant must contain to lift the hold

A competent owner must issue, in writing and bound to exact identities:
1. named provider + exact API endpoint;
2. exact model AND version pin (a mutable alias like "latest" is not a pin);
3. explicit privacy permission covering synthetic lab packets (world/history/actor-info packets are synthetic lab fixtures; confirm they may leave the host);
4. experiment-use grant for **behavioral actor trials** (distinct from authoring/tooling use);
5. explicit monetary cap and price class; observed quota or explicit UNKNOWN;
6. raw request/response retention permission (needed for the auditable capture the commission requires);
7. per-trial call budget and total trial budget (the frozen plan needs `n_trials` matched calls + declared retries).

After issuance: re-verify the gate immediately before the first call (`lab2/model_gate.require_call_permission`), then run `BehavioralRunner.run_granted()` — the single sanctioned call site (intentionally unwired in this return because no grant exists).

## What this hold does NOT mean

- **Not** an unexecutability claim: the behavioral question remains open and the protocol is finished and executable (see `01_PREREGISTRATION_FROZEN.json`, `lab2/`).
- **Not** a negative behavioral result: no behavioral evidence exists either way; the question is UNTESTED, not refuted.
- **Not** a reason to relabel the machine-level synthetic results as behavioral proof — LAB1's 576 trials and this commission's independent replication remain `SYNTHETIC MACHINE-LEVEL` and are explicitly not model/actor evidence.
- **Not** a license to use any locally available credential informally: credentials that happen to exist on a host are not an experiment grant.

## Termination condition

`MODEL_BEHAVIORAL_HOLD` lifts exactly when the 8 fields are filled by a competent grant. Until then the honest terminal for the behavioral question is this hold, and the completed deliverable is the frozen protocol + source-free replication.
