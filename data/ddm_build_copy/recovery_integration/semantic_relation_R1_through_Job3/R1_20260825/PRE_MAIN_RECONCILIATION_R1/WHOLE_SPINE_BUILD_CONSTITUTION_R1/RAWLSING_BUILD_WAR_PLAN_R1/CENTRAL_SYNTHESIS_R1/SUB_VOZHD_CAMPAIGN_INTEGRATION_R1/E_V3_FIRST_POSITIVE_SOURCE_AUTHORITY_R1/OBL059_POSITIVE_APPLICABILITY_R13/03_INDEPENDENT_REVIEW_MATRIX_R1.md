# OBL059 POSITIVE_APPLICABILITY — R13 FRESH DISTINCT INDEPENDENT REVIEW MATRIX R1

Status: `FROZEN_BEFORE_GOVERNED_EXECUTION`

Reviewer branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r13-independent-review-r1`

Exact review start:
`cfd6d3b8971063c73178e819b9ec28acaa134a79`

Prospective SUB-VOZHD E authority:
`54f02a19198c5d4fe7939fb14f0d3a8077929a5a`

HQ zoom-out/adoption:
`31dbfc741b945ed46c831cba90d59f3370c376e7`

Current PRE-MAIN authority:
`0fd958c2840b0f7029a545e60a0ce75764b8d66d`

Frozen R13 target:
`9e255ff2a49dda900080e06affb084a9cae02dc3`

Candidate executable blob:
`1dc206afcd25315f406fade7f8a3b72c378dfcd0`

Primary proposition:

`R13_DECISION_LAYER_ACCEPTS_ONLY_VALIDATED_CANONICAL_BUILTIN_PACKET__ARBITRARY_OR_EFFECTFUL_SOURCE_CARRIER_BEHAVIOR_CANNOT_BECOME_AUTHORITY_BEARING_AFTER_CANONICALIZATION`

The review is review-only. The frozen candidate is not to be modified. No repair, second reviewer, R12 rereview, R14 commission, OBL058 reopening, OBL060 reopening, or OBL061 runtime action is authorized.

## Matrix

| ID | Independent review family | Frozen expected property |
|---|---|---|
| M01 | arbitrary custom `Mapping` direct input | deterministic negative result without protocol traversal |
| M02 | effectful `Mapping` direct input | effects/calls remain zero inside decision layer |
| M03 | cache-warming mapping | no cache-warming method invoked by direct decision |
| M04 | layered mapping | no layer traversal by direct decision |
| M05 | aliased mapping | aliasing cannot become authority-bearing |
| M06 | path-mutating mapping | path mutation cannot affect decision input |
| M07 | lookup mutates nested state | mutation cannot occur inside decision layer |
| M08 | inconsistent nested views | inconsistent carrier views cannot affect direct decision |
| M09 | old R12 arbitrary-effectful-parent/path-rewrite family | once canonical packet is built, later carrier behavior cannot rewrite authority-bearing nested input |
| M10 | canonical packet outer immutability | exact tuple-only public boundary |
| M11 | nested canonical immutability | no mutable/custom Mapping object survives inside canonical token tree |
| M12 | canonical producer exact-type validation | raw/custom/non-exact semantic packet is not silently canonicalized |
| M13 | canonical schema/tag validation | wrong schema/tag rejected totally |
| M14 | canonical tuple shape validation | wrong arity/container shape rejected totally |
| M15 | canonical dictionary token validation | duplicate keys/non-string keys/bad entries rejected totally |
| M16 | canonical scalar token validation | malformed bool/int/float/bytes/string tokens rejected totally |
| M17 | traversal order boundary | nested authority-relevant traversal occurs only after exact canonical schema/payload checks and thaw to exact built-ins |
| M18 | source-specific adapter remains upstream | decision function never calls adapter |
| M19 | adapter semantics not absorbed | adapter behavior can affect only pre-boundary representation materialization, not post-boundary authority traversal |
| M20 | genuine positive applicability | exact lawful NONCURRENT_SYNTHETIC fixture yields positive decision |
| M21 | genuine negative applicability | exact in-grain semantic mismatches yield negative decision |
| M22 | actor binding | changed actor is rejected/distinguished |
| M23 | subject binding | changed subject is rejected/distinguished |
| M24 | world binding | changed world is rejected/distinguished |
| M25 | time binding | changed time is rejected/distinguished |
| M26 | opportunity/applicability scope binding | changed opportunity/scope is rejected/distinguished |
| M27 | source identity | expected source/owner identities remain exact |
| M28 | wrong source | wrong source/semantic owner rejected where applicable |
| M29 | wrong authority | wrong authority identity rejected where applicable |
| M30 | malformed/noncanonical totality | malformed public-boundary values return governed negative/malformed receipt rather than uncontrolled traversal |
| M31 | oversized integers | supported runtime settings remain total at canonical encode/decode and semantic evaluation |
| M32 | equal-input proof determinism | equal authority-relevant inputs produce equal proof/results |
| M33 | unequal-input proof distinction | authority-relevant unequal inputs produce distinguishable proofs/results |
| M34 | repeated evaluation | stable repeated results from same canonical packet |
| M35 | concurrent evaluation | stable concurrent results from same canonical packet |
| M36 | `NONCURRENT_SYNTHETIC` boundary | lawful synthetic fixture remains allowed as candidate mechanics only |
| M37 | `CURRENT` / `PROJECT_CURRENT` exclusion | current/project-current shapes do not create positive applicability |
| M38 | no project-current positive applicability fact | all receipt/effect flags remain false |
| M39 | no positive OBL056 installation | no registry/current installation effect |
| M40 | no actor/current transition | no actor creation/activation or current phase transition effect |
| M41 | no OBL055/ENCOUNTER/OEE/OBL032 | no downstream runtime execution/effect |
| M42 | no authority-index/current-runtime side effect | all declared no-current-effect fields remain false and no extra mutation surface is invoked |

## Independent constructions beyond producer court

The review test surface will not simply invoke the producer `CourtR13` class. It will independently load the frozen executable and construct its own fixtures and carrier classes. It will emphasize cases not identical to producer methods, including:

1. a `Mapping` whose `__class__`/iteration/lookup counters and nested payload change on every access, proving zero access for direct decision input;
2. a parent carrier whose first nested lookup returns a wrong-authority child and whose second returns a repaired child, reproducing the R12 path-rewrite family while proving a prebuilt canonical packet is unaffected;
3. canonical token trees containing duplicate dictionary entries, tuple subclasses, malformed integer hex/sign combinations, float-width errors, and non-exact nested containers;
4. monkeypatch sentinels on the upstream adapter to prove `evaluate_direct_positive_applicability` never invokes adapter behavior;
5. a canonical snapshot followed by aggressive mutation/replacement of every source-side authority-relevant node, proving the snapshot result is unchanged;
6. exact five-position semantic mutations with proof distinction checks;
7. concurrent mixed positive/negative canonical packets rather than only one positive packet;
8. runtime integer string-digit settings at supported extremes while canonical integer encoding remains byte/hex based and total.

## Disposition law

A PASS requires all commissioned properties above to hold under fresh governed evidence.

If a failure shows arbitrary/effectful carrier behavior can still affect authority-bearing nested input after canonicalization, classify:
`SAME_CANONICAL_INPUT_BOUNDARY_FAMILY`.

If a failure is a different semantic defect wholly inside the commissioned OBL059 grain, classify:
`GENUINELY_NEW_IN_GRAIN_DEFECT`.

No failure will be repaired by this reviewer.

Required separation at terminal:

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R13_CANDIDATE = 1`

`FROZEN_R13_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`R12_REVIEW_REPEATED = NO`
