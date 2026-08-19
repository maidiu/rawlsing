# S554D — HOSTILE DUPLICATE-EQUIVALENCE / PRECEDENCE FIXTURES

**Status:** `NON_DISPOSITIVE_FIXTURE_PROPOSAL`  
**Parent:** `SCR554`  
**Purpose:** force any candidate V554 duplicate-equivalence/precedence contract to prove no-double-support while preserving source plurality, temporal negatives, exact authority, epistemic states, and replay invariance.

These fixtures are test specifications only. They do not authorize production implementation or select the final SCR554 schema.

## 1. Common fixture oracle

Each fixture should record, at minimum:

- candidate A exact basis envelope;
- candidate B exact basis envelope where pairwise;
- canonical `SUPPORT_EQUIVALENCE_KEY` projection or an explicit `EQUIVALENCE_UNKNOWN` reason;
- exact `AUTHORITY_SNAPSHOT_FINGERPRINT` for every candidate;
- exact `BASIS_PROVENANCE_FINGERPRINT` for every candidate;
- pairwise semantic classification;
- authority-snapshot relation classification;
- applicable ADP-001 precedence state;
- canonical semantic carrier, if one exists;
- emitted F1 count;
- retained duplicate provenance refs;
- retained negative/missing/conflict refs;
- deterministic replay fingerprint.

Global assertions for every fixture:

```text
physical_path_count != semantic_support_count
provenance_count != support_weight
same_label != semantic_equivalence
same_payload_bytes != source_equivalence
newer_artifact != authority_precedence
unknown_equivalence != permission_to_choose
```

## HF-D01 — same labels, different source universes

**Construct**

Two exact bases share:

- canonical proposition display text;
- target use;
- stable V554 rule ID;
- native calendar year;
- apparent geography label.

But:

- A binds `EmpiricalUniverse=UA`;
- B binds `EmpiricalUniverse=UB`;
- no source-equivalence/composition authority relates UA and UB.

**Expected**

`DISTINCT_SEMANTIC_SUPPORT`.

Both candidate decisions remain separate. No merged F1, average, winner, or stronger-source selection is created by the dedup court.

**Kill condition**

Any implementation that returns equal duplicate keys because proposition/use/rule labels are equal fails.

## HF-D02 — same proposition, different estimand

**Construct**

A and B share universe, measure family, target use, and proposition label.

- A estimand: population mean.
- B estimand: conditional mean over an exact governed risk set.

**Expected**

`DISTINCT_SEMANTIC_SUPPORT`.

Risk-set and estimand refs are identity-bearing.

## HF-D03 — same proposition, different weight basis

**Construct**

- A: exact governed `UNWEIGHTED` basis.
- B: exact survey-weight authority `W1`.

Everything else appears equal.

**Expected**

`DISTINCT_SEMANTIC_SUPPORT` unless an explicit authority creates a semantic equivalence for the exact use.

The explicit unweighted state must not be serialized as missing/null.

## HF-D04 — direct + V553 compatibility no-op

**Construct**

- direct admission A is already temporally complete for the exact static/point V554 use;
- V553 object T is derived from A only for compatibility transport;
- T proves `temporal_effect_for_target_use = NONE`;
- T resolves to the exact same target temporal semantics;
- no temporal relation, derived interval, limit, comparability result, negative state, or source relation is added.

**Expected**

`SAME_SEMANTIC_SUPPORT`.

`DIRECT_CANONICAL__V553_DUPLICATE_PROVENANCE_ONLY`.

Exactly one F1 maximum. T remains replay/audit provenance and must add zero weight, score, multiplicity, confidence, or route count.

**Metamorphic control**

Delete the compatibility V553 artifact. F1 semantics must remain identical.

## HF-D05 — V553 creates genuinely required temporal meaning

**Construct**

Direct A has one exact point observation. Target rule requires persistence/change across an interval. V553 T creates the exact governed temporal relation.

**Expected**

Direct A is ineligible for that temporal invocation. T is not a duplicate no-op.

`V553_REQUIRED__DIRECT_INELIGIBLE_FOR_INVOCATION`.

No weaker signature fallback.

## HF-D06 — temporal NONCOMPARABLE versus direct-positive appearance

**Construct**

- direct basis is physically present and superficially complete;
- exact invocation requires a temporal relational comparison;
- V553 supplies exact `NONCOMPARABLE` authority for the required support.

**Expected**

No F1. K08/hard temporal negative wins for that invocation.

Direct presence cannot bypass the negative and cannot trigger a non-temporal downgrade.

## HF-D07 — temporal ABSENT/GAPPED versus observed zero

**Construct**

Pair A contains exact temporal point measurement `value=0` with valid observed state. Pair B contains exact required temporal support state `ABSENT_OR_GAPPED`.

**Expected**

A and B are not semantically interchangeable.

A may remain eligible if all other authority passes. B causes the accepted K09 hard block for the affected temporal invocation.

## HF-D08 — same semantic support, conflicting authority versions

**Construct**

A and B project to the same source-sensitive support identity.

- A evaluated under stable rule R version/hash V1/H1.
- B evaluated under stable rule R version/hash V2/H2.
- no explicit producer-governed compatibility/supersession relation exists.

**Expected**

`SAME_SEMANTIC_SUPPORT` plus `AUTHORITY_CONFLICT_UNRESOLVED`.

No F1 for the affected competition until exact authority relation is supplied.

**Kill controls**

- If rule version in support key causes two independent supports: fail.
- If version is ignored and one is chosen: fail.
- If largest semver/newest commit wins: fail.

## HF-D09 — explicit authority supersession

**Construct**

Same as D08, but supply exact producer-governed authority object stating V2/H2 supersedes V1/H1 for the exact rule/use.

**Expected**

One semantic support. V2/H2 is authority winner because the explicit relation says so, not because it is newer. V1/H1 remains historical provenance.

Remove the supersession object: result must revert to unresolved conflict.

## HF-D10 — unknown equivalence leaf

**Construct**

A and B appear equal by labels and proposition ID, but B's exact estimand or universe manifest cannot be resolved.

**Expected**

`EQUIVALENCE_UNKNOWN -> FAIL_CLOSED`.

The system may not assume equal, assume distinct, union, or choose one by convenience.

## HF-D11 — observed numeric zero

**Construct**

One exact candidate has measurement value `0` with complete positive authority.

**Expected**

Zero remains an observed measurement. No magnitude/truthiness filter converts it to missing, denied, zero-support, or valid-empty.

If all other requirements pass, F1 remains eligible.

## HF-D12 — zero-support state

**Construct**

Same labels as D11, but producer-owned epistemic/support state is exact `ZERO_SUPPORT` or terminal equivalent, not an observed measured zero.

**Expected**

It remains a distinct producer state. Its V554 disposition follows its exact producer/admission/use authority; it cannot be equated to D11 by numeric encoding.

## HF-D13 — VALID_EMPTY

**Construct**

Coherent V554 invocation/run with zero candidates satisfying the rule.

**Expected**

`VALID_EMPTY`, zero F1, zero candidate support keys, no dummy seed, no synthesized numeric-zero candidate.

## HF-D14 — explicit denial against positive-looking duplicate path

**Construct**

A direct/V553 candidate pair otherwise appears support-equivalent. An exact applicable K05 target-use denial governs the invocation. Legacy scores/readiness are maximal.

**Expected**

No F1. Denial is retained by exact ref. Dedup selection cannot erase the denial.

## HF-D15 — row/file enumeration permutation

**Construct**

Replay the identical candidate/authority set under at least these permutations:

- A then B;
- B then A;
- different input filenames;
- different directory enumeration order;
- different packet row ordering.

**Expected**

Identical semantic classification, authority result, canonical F1 identity/multiplicity, provenance set, and authority-bundle fingerprint.

Any first-row/last-row/file-order behavior fails.

## HF-D16 — wall-clock/latest mutation

**Construct**

Hold all semantic and authority objects fixed. Change only:

- file mtime;
- artifact publication timestamp;
- commit observation order;
- wall-clock time at replay.

**Expected**

No change whatsoever to equivalence or precedence.

## HF-D17 — legacy score/readiness mutation

**Construct**

Hold canonical refs and authority fixed. Swap direct and V553 legacy values for:

- seed strength;
- readiness;
- confidence;
- specificity;
- certifiability.

**Expected**

Canonical equivalence, precedence, and F1 result are unchanged.

## HF-D18 — source-insensitive payload hash collision

**Construct**

A and B contain byte-identical measured payloads but are governed by different exact universe manifests UA and UB.

**Expected**

`DISTINCT_SEMANTIC_SUPPORT` absent explicit equivalence authority.

A digest of payload bytes alone must collide intentionally in the fixture and must not be accepted as the support-equivalence key.

## HF-D19 — alias/reissue with provenance-only lineage

**Construct**

Admissions A1 and A2 have different receipt/admission IDs but exact equal support semantics. Producer authority explicitly marks the reissue lineage `PROVENANCE_ONLY`.

Direct path uses A2. V553 no-op derives from A1.

**Expected**

`SAME_SEMANTIC_SUPPORT`; one F1 maximum. Both lineages remain in provenance.

## HF-D20 — identity-bearing lineage

**Construct**

Same apparent proposition/source tuple, but governing upstream authority explicitly states that the two evidence/source lineages are part of structural proposition identity.

**Expected**

`DISTINCT_SEMANTIC_SUPPORT` when those exact identity-bearing lineage refs differ.

## HF-D21 — lineage role unknown

**Construct**

A and A2 appear to be aliases, but no authority establishes whether lineage is provenance-only or identity-bearing.

**Expected**

`EQUIVALENCE_UNKNOWN -> FAIL_CLOSED`.

Receipt equality/inequality cannot substitute for the missing role authority.

## HF-D22 — same universe, different risk sets

**Construct**

Same universe manifest U, proposition and measure. Exact governed risk set R1 differs from R2.

**Expected**

`DISTINCT_SEMANTIC_SUPPORT` when risk set is identity-bearing for the estimand.

## HF-D23 — same measure label, changed semantic measure definition

**Construct**

Measure display label is unchanged. Exact measure semantic ref/hash changes under a producer-governed definition revision that changes the estimand/measurement semantics.

**Expected**

Distinct support semantics. Label equality cannot hide the change.

## HF-D24 — same measure semantics, authority-package revision only

**Construct**

Exact measure semantic identity remains the same, but its authority package snapshot changes. No compatibility/supersession relation is supplied.

**Expected**

Support remains same; authority relation is unknown/conflicting. Do not manufacture two supports merely because package versions differ.

## HF-D25 — distinct target uses from one admission

**Construct**

One admission A is used for:

- U1 static bounded affordance;
- U2 persistence-conditioned affordance through V553.

**Expected**

Not one duplicate court: target-use identities differ. Both governed invocations may exist. U2 still requires V553 semantics if its rule demands them.

## HF-D26 — source disagreement must survive dedup

**Construct**

UA and UB produce same proposition label but conflicting exact values/states under their own estimand/measure/weight authorities.

**Expected**

Separate source-sensitive candidates. No majority, stronger-source, higher-support, pooled, or averaged synthesis by the dedup court.

Provenance reachability does not grant composition authority.

## 2. Required metamorphic replay suite

A candidate contract should pass all of these transformations without changing semantic output unless the transformed item is explicitly identity-bearing:

1. permute row order;
2. permute file order;
3. rename files;
4. alter wall-clock/mtime;
5. alter legacy scores/readiness/confidence;
6. add/remove a proven no-op duplicate V553 provenance path;
7. replace a provenance-only admission receipt with a producer-governed exact alias;
8. reorder nonsemantic ref arrays before canonical serialization.

Expected invariant:

```text
support classification unchanged
+ authority result unchanged
+ F1 count unchanged
+ canonical semantic carrier unchanged
+ replay fingerprint unchanged after canonicalization
```

Expected non-invariants, where the exact changed item is semantic/authority-bearing:

- change universe manifest -> support identity changes;
- change estimand -> support identity changes;
- change measure semantics -> support identity changes;
- change weight basis -> support identity changes;
- change required temporal meaning -> support identity/invocation eligibility changes;
- introduce K05/K08/K09 -> positive eligibility blocks as governed;
- change authority snapshot without relation -> authority conflict;
- add explicit governed supersession -> authority winner changes exactly as authorized.

## 3. Minimum acceptance oracle proposed to SCR554

A parent-selected contract should not pass its local barrier unless it can demonstrate all of the following:

- all D01-D26 outcomes are machine-decidable without label reconstruction;
- any unresolved identity-bearing comparison returns `EQUIVALENCE_UNKNOWN` and fails closed;
- direct+no-op-V553 yields one F1 maximum;
- a meaning-bearing or negative V553 basis cannot be bypassed by direct precedence;
- distinct source/estimand/measure/weight/risk-set semantics remain distinct;
- authority-version conflict does not become either silent reuse or false independent support;
- observed zero, zero-support, valid-empty, denied, missing, unknown/conflicting and noncomparable states remain distinguishable;
- replay is invariant to latest/score/order/mtime/filename mutations;
- source-insensitive payload hashing cannot define support equivalence;
- duplicate provenance never increases downstream multiplicity or evidentiary weight.

If any of these fails, S554D recommends that SCR554 classify the exact key/precedence contract as not closed rather than weaken the frozen no-double-entry law.
