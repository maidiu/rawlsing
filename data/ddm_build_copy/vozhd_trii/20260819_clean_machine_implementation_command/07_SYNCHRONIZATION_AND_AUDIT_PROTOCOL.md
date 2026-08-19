# 07 — SYNCHRONIZATION & AUDIT PROTOCOL

## 1. Principle

Synchronization is a command duty and an explicit technical process.

The purpose is to prevent local correctness from becoming global incompatibility.

## 2. Synchronization events

A synchronization event is mandatory when any unit:

- changes or requests change to a shared schema/interface;
- changes object identity/hash material;
- adds/removes a field used across a boundary;
- changes typed negative/absence behavior;
- changes authority/version binding;
- adds/removes a DAG edge;
- changes temporal/effective-time semantics;
- changes source-universe relationship or composition behavior;
- changes replay/reference material;
- adds an adapter/shim;
- discovers sibling incompatibility;
- completes a wave-scoped tranche.

## 3. Immediate synchronization procedure

1. Worker freezes work at the affected shared seam.
2. Worker emits exact `DEPENDENCY_IMPACT` and contract-change request if needed.
3. Domain Vozhd classifies local versus shared impact.
4. G6 enumerates impacted workers/consumers.
5. Owning Staff authority adjudicates the shared contract.
6. G5 identifies fixture/test updates.
7. Inspectorate reviews for drift/hidden scope increase.
8. G6 marks affected workers `STALE_CONTRACT`.
9. Updated contract/version/hash is published.
10. Affected workers acknowledge and refresh/rebase.
11. Domain Vozhds re-audit sibling compatibility.
12. Work resumes.

## 4. Wave reconciliation

Before opening a dependent wave, Campaign Vozhd requires a reconciliation packet covering:

- current integration SHA;
- current substrate/schema contract;
- current object/interface/DAG registries;
- all integrated semantic diffs since prior wave;
- unresolved authority requests;
- Inspectorate findings;
- current golden-fixture state;
- terminal-capability coverage;
- replay/reconstruction state;
- known implementation debt and whether it is dependency-blocking.

Result must be one:

- `WAVE_RECONCILED__NEXT_DEPENDENCIES_MAY_OPEN`
- `WAVE_RECONCILED_WITH_BOUNDED_NONBLOCKING_DEBT`
- `WAVE_BLOCKED_HARMONIZATION_REQUIRED`
- `WAVE_BLOCKED_AUTHORITY_REQUIRED`

## 5. Domain synchronization audit

Each domain Vozhd regularly compares all subordinate outputs pairwise where they share a contract.

Audit questions:

- Do both sides reference the same contract ID/version/hash?
- Do they agree on object grain?
- Do they agree on identity/hash fields?
- Do they agree on cardinality/order/role?
- Do they agree on typed negative states?
- Do they agree on time semantics?
- Does consumer interpret only legal producer fields?
- Is provenance still nonsemantic where required?
- Are source-universe distinctions identical?
- Are fallbacks/defaults identical to authority (normally none unless governed)?

## 6. Cross-domain seam audit

At every cross-domain edge, both domain Vozhds plus G4 must sign a seam receipt.

Minimum receipt:

- producer object/contract;
- consumer contract;
- exact legal edge;
- negative states;
- references required;
- replay obligations;
- forbidden reinterpretations;
- fixture IDs;
- producer head/tranche;
- consumer head/tranche;
- Inspectorate disposition.

## 7. Drift signatures

Any of the following trigger immediate audit even if tests pass:

- two names for apparently same concept;
- same name with different field sets;
- duplicated upstream fields carried locally without explicit reason;
- `None`/`null` used without typed semantic meaning;
- an ID built from display labels;
- a join on text labels;
- a default to most recent/nearest/majority;
- copied authority content without authority hash;
- stage-local re-ID of producer object;
- source identity omitted from a semantically source-sensitive key;
- consumer loading raw producer directories rather than canonical interface;
- worker referring to a floating branch or `latest` contract;
- test fixture privately invented by one worker for shared behavior.

## 8. Whole-machine checksum

Campaign Vozhd runs a whole-DAG semantic checksum after every major wave:

For every terminal capability, trace:

- authoritative inputs;
- semantic transforms;
- governance boundaries;
- repository/reference boundaries;
- negative authority;
- actor-development boundary where applicable;
- terminal consumer.

Then trace backward from terminal output to exact source/authority/replay material.

Any unowned transform, ambiguous reference, or unverifiable authority stops dependent integration.

## 9. Time compression rule

Audits are not scheduled for leisurely intervals. They occur at the earliest event that could create divergence.

The campaign optimizes elapsed time by detecting incompatibility before dependent workers build on it.
