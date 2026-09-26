# RAWLSING HQ CURRENT — BOUNDED AUTONOMOUS CONTROL-PLANE REMEDIATION

Decision: `HQD-2026-09-26-108`

Status: `MEASURED_SOURCE_RUNS_ACTIVE__BOUNDED_AUTONOMOUS_CONTROL_REMEDIATION_AUTHORIZED__NO_USER_ROUNDTRIP_FOR_MECHANICAL_BLOCKERS`

The prior fail-fast law is superseded for **proven source-neutral control-plane defects**.

Agents may autonomously diagnose, patch local control surfaces, source-free test, reseal local bindings, create a fresh work root, and retry without asking the user.

They may NOT change:
- protected execution bytes at `16f5e7d5f691e908d85dc1dd26b8a59a29f668f4`;
- Candidate A/B/C owner/algorithm bytes;
- survey source semantics;
- source identity;
- P2/S17/architecture-selection authority.

Every failed root remains immutable and every retry uses a fresh root.

## Known shared control-chain defects

LiTS has already exposed:
- stale branch-name assertions: `prev3` vs exact 10C-bound `cache-neutral-joined-successor`;
- readiness/pair/control identity fallout from local source-neutral override;
- S00 source-free preflight receipt misclassified as forbidden candidate state;
- same misclassification in preprovision;
- evidence closure rejecting the actual local override branch label.

WVS must audit and repair these **before** its first measured entry rather than rediscovering them serially.

## Stop condition

Return to HQ/user only for:
1. successful source-local A->B->C terminal; or
2. a proven substantive candidate/source blocker that cannot be solved without changing protected candidate/source semantics.

Mechanical bookkeeping drift is not a terminal.

No P2.
