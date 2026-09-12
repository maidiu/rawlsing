# REPLAY / CURRENTNESS / INVALIDATION + BOUNDED-INCOMPLETENESS + PROJECTION LAW R1

Status:

`HORIZONTAL_CONSTRAINTS_FORMALIZED__NO_PHYSICAL_WINNER__NO_CONSUMER_ONTOLOGY_PROMOTION`

## 1. Replay identity

A replayable resolution MUST pin:

- exact request ref;
- exact world/release/root ref;
- exact producer release refs;
- exact authority instances;
- exact valid/effective time basis;
- exact resolver semantic version;
- exact serializer/canonicalization version;
- exact dependency closure;
- exact ordered outputs including typed blockers/omissions.

No replay may dereference an unpinned mutable `latest` and then claim identity with an earlier receipt.

## 2. Currentness law

Currentness is multidimensional.

The constitution MUST preserve distinct currentness for, where applicable:

- producer release;
- proposition/fact;
- rule;
- rule application;
- witness;
- world/state/version;
- valid-time interval;
- root/replay horizon;
- permission/use authority.

`CURRENTNESS_ONE_DIMENSION != CURRENTNESS_ALL_DIMENSIONS`.

## 3. Invalidation law

Every result binding MUST expose the exact determinants on which it depends.

When a determinant changes or is superseded:

1. the old result/receipt remains historically addressable;
2. only dependent bindings/receipts become stale/invalidated;
3. unrelated producer objects remain valid;
4. redrive follows transitive dependency closure only;
5. successor receipt/root identities are new immutable identities.

`DETERMINANT_SCOPED_INVALIDATION -> DEPENDENT_ONLY_REDRIVE`.

Whole-world rematerialization may be chosen operationally but is not required semantically.

## 4. Succession / explanation law

Every superseded root, request-compatible receipt or result binding SHOULD carry explicit successor/supersession linkage where current project vocabulary supports it.

Historical explanation is append-only: the project must be able to state what was resolvable under the earlier authority horizon and why a later answer differs.

No overwrite may erase the prior replayable semantic state.

## 5. Generic bounded-incompleteness binding

For every requested proposition/component/context:

`MISSING_AUTHORITY != ZERO`

`TYPED_MISSING != ZERO`

`UNRESOLVED != FALSE`

`BLOCKED != FALSE`

`MISSING_POSITIVE != NEGATIVE`

`SOURCE_LOCAL != POPULATION_CERTIFIED`

`MODEL_PRIOR != EMPIRICAL_EVIDENCE`.

Forbidden absent exact competent transform/authority:

- availability-based renormalization;
- coefficient redistribution;
- nearest-source substitution;
- proxy substitution;
- temporal backfill;
- cross-population substitution;
- inferred negative from absent positive;
- numeric zero from nonnumeric/missing state.

Every omission or authorized substitution MUST remain visible in receipt coverage/provenance with the exact authority that permitted it.

## 6. Consumer-specific projection constitution

A downstream owner MAY derive:

- vector;
- score;
- coordinate;
- typology;
- classification;
- distribution;
- other compressed representation;

only if that owner separately freezes:

```text
semantic_target_ref
input_scope_and_source_ceiling
input_claim_ceiling
transform_ref
aggregation_or_fusion_rule_ref
missingness_policy_ref
calibration_ref
normalization_ref
replay/currentness_policy_ref
intended_consumer_ref
permission/use/causal-use ceiling
```

If any required transform authority is missing, the lawful result is typed incomplete/blocked/unresolved according to exact current law—not an invented completion.

A projection MAY be useful and even required for one consumer. That does not make it the seam ontology.

`CONSUMER_REQUIREMENT != UNIVERSAL_WORLD_REQUIREMENT`.

The quarantined OBL063 driver/Enneagram material remains optional-model evidence only under this constitution.

## 7. Physical neutrality

The exact same semantic constitution MUST be preservable under any later-chosen physical realization:

### Persistent canonical materialization

Lawful only if carrier/payload identity does not replace producer/authority identity.

### Source-backed virtual resolution

Lawful only if exact root/release/currentness/replay can be pinned and reconstructed deterministically.

### Hybrid

Lawful only if cache/materialization does not become authority and invalidation is determinant-scoped.

### Explicit publication boundary

Lawful if publication identity preserves producer ownership and exact ingress bindings.

### Continuous producer DAG

Lawful if direct producer refs remain reconstructible and semantic release/root identity survives without serial copying.

No winner is selected here.

## 8. Discriminator deferred

Performance, storage economics, latency and operational simplicity may discriminate physical architectures only after semantic/replay parity exists.

No starvation witness in this commission proves that a giant materialized world payload is semantically necessary.

Terminal:

`REPLAY_INCOMPLETENESS_PROJECTION_AND_PHYSICAL_NEUTRALITY_CANDIDATE_LAW_COMPLETE`
