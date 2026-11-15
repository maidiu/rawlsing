# V553-P1 — Admission and Authority Hardening

**Launch status:** `BLOCKED_UNTIL_FINAL_UPSTREAM_IDENTITY_BASE`

## Mission

Implement the first dependency layer of the accepted V553 completion architecture: fail-closed upstream admission plus exact governed comparability authority intake, on top of the finalized source/wave identity contract.

## Read first

1. `integration/V553_COMPLETION_IMPLEMENTATION_RULING.md`
2. `schematics/recalibration/TD_R00_V553/RESULT.md` + `RESULT.json`
3. `schematics/sessions/S00_5_V553_ARCHITECTURE/RESULT.md`
4. `schematics/synthesis/S00_V552J_TO_V553_RULING.md`
5. finalized source/wave identity campaign terminal report/ruling once merged
6. current V553 admission/harmonization/identity code and focused tests

## Authorized production terrain

Primary:
- `data/ddm_build_copy/ddm_v553_canonical_harmonization.py`
- `data/ddm_build_copy/ddm_v553_harmonization.py`
- `data/ddm_build_copy/ddm_v553_repo_discovery.py`
- `data/ddm_build_copy/ddm_v553_temporal_identity.py`
- V553-focused admission/authority tests

Do not edit V550–V552J producer semantics. If an upstream defect is discovered, report a cross-hook rather than repairing upstream silently.

## Required outcomes

- Preserve the accepted fail-closed V552J publication verifier and valid-empty distinction.
- Bind all V553 scope/identity handling to finalized governed `source_family_uid` / `wave_uid` identity where applicable, while preserving required legacy identity/provenance.
- Make repository discovery authority-neutral: locating an overlay/file cannot certify it.
- Remove comparability certification fallbacks based on confidence, reviewability, shared-column presence, row presence, or thin/readiness state.
- Define and enforce the exact predicate by which semantic/directionality/position authority is governed/certified for V553 use.
- Keep thin/readiness as validation/orchestration context only.
- Fail closed on ambiguous/multi-family/multi-country/duplicate temporal-anchor scope.
- **TD-R00 amendment:** retain exact producer-owned object IDs/refs for every governed semantic, directionality, position/use and relation authority admitted; booleans or labels are not substitutes for reference identity.
- **TD-R00 amendment:** preserve multi-valued governed finite-stratum refs, Horizon-related refs, explicit Absolute-Horizon designation refs, and inherited incompatibility/coexistence refs exactly as supplied, without synthesis, singularization or inference.
- **TD-R00 amendment:** admission must preserve enough authority identity for P2 to construct `GOVERNED_STRUCTURAL_REFERENCE_SET`; P1 does not itself create a new semantic family.

## Proof required

At minimum add/extend tests proving:
- untyped overlay cannot certify comparability;
- high-confidence or review-only overlay cannot certify comparability;
- file/shared-column presence cannot certify comparability;
- valid-empty differs from missing/corrupt/schema-invalid/integrity-invalid;
- source/wave UID coherence survives admission;
- conflicting redundant identity fails closed;
- multi-family/multi-country/duplicate-anchor inputs fail;
- admitted governed authority refs remain exact and multiplicity-preserving;
- absence of explicit stratum or Absolute-Horizon authority stays absence rather than inferred classification.

## Prohibited

- no sparse key/observation redesign yet;
- no aggregate/publication cleanup yet;
- no V554 changes;
- no new persistence/drift/rupture thresholds;
- no persona/runtime semantics;
- no stratum/Horizon/conflict synthesis from labels, topic names, religiosity, ideology or temporal delta sign.

## Return

Write:
- `integration/V553_COMPLETION/P1_ADMISSION_AUTHORITY/RESULT.md`
- `integration/V553_COMPLETION/P1_ADMISSION_AUTHORITY/RESULT.json`

Commit to the assigned P1 branch and open a draft PR to `agent/vozhd-dva-v553-completion-integration`.

Return head SHA, PR number, files changed, tests/results, any upstream cross-hook, and whether P1 is safe to integrate.