# S554D — HOSTILE V554 DUPLICATE-EQUIVALENCE / PRECEDENCE FEEDER

**Campaign:** `VOZHD TRII — STAGE CLOSE READ`  
**Cell:** `SCR554 / feeder S554D`  
**Repository:** `maidiu/rawlsing`  
**Exact base SHA:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Branch:** `agent/vozhd-trii-dr-r03-spec-v554-dedup`  
**Authority:** `NON_DISPOSITIVE_FEEDER`  
**Write scope:** `data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/STAGE_CLOSE/SCR554/feeders/S554D/` only  
**Production code modified:** `NO`  
**R03 broad DAG amended:** `NO`  
**SCR554 legislated:** `NO`

## Result

`S554D_FEEDER_COMPLETE`

No broad-topology counterexample was found. No parent-authority conflict prevents a bounded exact duplicate-equivalence/precedence proposal.

The hostile finding is that a single flat V554 dedup hash cannot safely do both jobs that the close-read needs:

1. decide whether two physically different basis paths represent the **same semantic support**; and
2. preserve whether their **authority snapshots, temporal effects, negative states, and provenance roles** differ.

Putting basis kind, receipt ID, or raw lineage into the sole equivalence key makes a direct admission and a no-op V553 restatement look distinct and permits double support. Omitting source-universe, estimand, measure/weight, temporal semantics, epistemic state, or identity-bearing provenance makes genuinely distinct supports look equal and erases plurality/disagreement. Putting authority version directly into the support-equivalence key makes conflicting versions look like independent support. Omitting authority version hides a conflict.

The smallest safe pattern is therefore a **two-level semantic/authority court plus a provenance record**:

- `SUPPORT_EQUIVALENCE_KEY` — source-sensitive semantic support identity, route-independent;
- `AUTHORITY_SNAPSHOT_FINGERPRINT` — exact rule/admission/temporal/use/negative authority versions and hashes used to decide the candidate;
- `BASIS_PROVENANCE_FINGERPRINT` — basis kind, physical producer refs, lineage/replay refs and exact provenance-role assignments; provenance does not become additional support merely because there are two paths.

The proposal is specified in `PROPOSED_EQUIVALENCE_KEY.md`. SCR554 remains the only authority that may accept, amend, or reject it.

## Binding law consumed

S554D consumed the commanded authority/evidence chain, including:

- accepted R03 `RESULT.md`, `FINAL_BROAD_DAG.md`, `WHOLE_MACHINE_CLOSURE_GATE.md`, `STAGE_CLOSE_READ_CAMPAIGN.md` from the accepted synthesis branch;
- parent authority `24_DR_R03_SYNTHESIS_RETURN_ADJUDICATION_AND_STAGE_CLOSE_GATE.md`;
- parent authority `25_STAGE_CLOSE_READ_PARALLEL_COMMAND_AND_LAUNCH_AUTHORITY.md`;
- EP554 exact head `6ebb7c5ca1e007f3677706da19db9e83f451bff0`, including `RESULT.md`, `RESULT.json`, `V554_AUTHORITY_DATAFLOW_MATRIX.csv`, `V554_FIELD_ROLE_MATRIX.csv`, and `V554_BYPASS_TEST_MATRIX.csv`;
- R03A exact head `3d96c1213b46d3e6a908c83c2525f1ef20282f88`;
- R03F exact head `9f661931d51e03f137601b27eeaecf77ab11ad2f`;
- accepted `V554_AFFORDANCE_RULE_REGISTRY@1.0.0` / ADP-001;
- accepted `V554_APPLICABILITY_PREDICATE_CONTRACT@1.0.0` / CAN-001;
- accepted R02 V554 direct-admission minimality/routing law as subsequently qualified and frozen by R03.

Current V554 code was treated only as implementation evidence. The accepted evidence already records that the legacy seed identity (`run_id + seed_type + seed_scope`), scores/readiness, interpolation, and V553-only wiring are not target semantic authority.

## Frozen constraints this feeder does not reopen

1. One V554 proposition/use/rule may not count equivalent direct + V553 support twice.
2. `EQUIVALENCE_UNKNOWN -> FAIL_CLOSED`.
3. Direct `StructuralEmpiricalAdmission -> V554` is lawful for the exact target use only when temporally complete and positively rule-eligible.
4. If the exact use requires new V553-owned temporal/comparability meaning, direct fallback is not a substitute.
5. V553 cannot manufacture source-universe equivalence, pooling, sample linkage, estimand compatibility, or composition authority.
6. Exact negative/noncomparability/gap/denial authority dominates a superficially positive path when it applies to that same use/signature.
7. Observed numeric zero is a measurement, not missing authority.
8. `VALID_EMPTY`, `DENIED`, `NONCOMPARABLE`, `MISSING`, `UNKNOWN/CONFLICTING`, observed zero, and zero-support are not one state.
9. No score, readiness, recency, `latest`, majority, specificity, filename, row order, artifact presence, or compatibility-path presence may break a tie.
10. Provenance reachability does not grant source composition authority.

## Hostile conclusions

### H1 — Labels can never be the duplicate key

Two candidates may share normalized proposition text, geography labels, time labels, and target use while belonging to different `EmpiricalUniverse` identities, risk sets, estimands, measure definitions, or weight bases. These are `DISTINCT_SEMANTIC_SUPPORT` unless a separate governing authority explicitly says those identity-bearing semantics are equivalent for the exact use.

A source-insensitive hash such as:

`hash(normalized_proposition + target_use + rule_id)`

is unsafe and must fail the proposed fixture suite.

### H2 — Basis kind and receipt lineage can never be the sole semantic key

For a temporally complete direct admission, a compatibility V553 object that adds no required temporal meaning may be a second physical representation of the same support. `basis_kind` and raw receipt IDs therefore belong in provenance, not automatically in semantic distinctness.

Conversely, lineage is not always disposable. The governing upstream structural/admission authority may explicitly make source/evidence lineage identity-bearing. The contract must carry a machine role:

`lineage_semantic_role = PROVENANCE_ONLY | IDENTITY_BEARING`.

Unknown role means equivalence is unknown and fails closed.

### H3 — Authority version cannot be either blindly ignored or blindly put into semantic equivalence

Two candidates may project to the same semantic support but be evaluated under conflicting rule/admission/temporal authority versions.

- If version/hash is ignored, the conflict disappears.
- If version/hash is part of the semantic support key, the two versions appear to be independent support and can double count.

Therefore authority version/hash must live in a separate exact `AUTHORITY_SNAPSHOT_FINGERPRINT`. Same-support candidates with different snapshots require explicit producer-governed compatibility/supersession/precedence. Without it: `AUTHORITY_CONFLICT -> NO_F1` for the affected invocation.

No `latest` rule is implied by a larger version, newer commit, file mtime, or enumeration order.

### H4 — Temporal meaning must be compared semantically, not by V553 object presence

For the exact target use, each candidate must expose a governed temporal semantic projection.

A V553 object may be duplicate-only when it proves `temporal_effect = NONE_FOR_TARGET_USE` and resolves to the same exact target-time/effective-interval semantics already governed in the direct admission.

If V553 creates a required temporal relation, derived interval, persistence/change semantic, temporal limit, or exact noncomparability/gap state, it is not a no-op. For a rule that requires that meaning, the direct basis cannot win by being simpler or earlier.

### H5 — Negative/epistemic states must not be normalized into zero

At minimum, the equivalence court must keep separate:

- observed numeric `0` under a valid measurement state;
- zero empirical support / support-count state when producer-owned;
- positive assertion of absence when producer-owned;
- `DENIED` target-use authority;
- `NONCOMPARABLE` temporal authority;
- `MISSING_AUTHORITY`;
- `UNKNOWN_OR_CONFLICTING_AUTHORITY`;
- `VALID_EMPTY` run/collection state.

`VALID_EMPTY` has no candidate support key at all. It is not a zero-valued candidate. A denial is not an observed zero. A typed gap/absence is not an observed zero.

### H6 — Exact duplicate handling must not create extra weight

If two candidates are `SAME_SEMANTIC_SUPPORT` and their authority snapshots are compatible, the output is at most one F1 semantic support. The non-canonical path may be preserved only as provenance/audit evidence tagged as duplicate representation. The existence of two physical paths must not increase strength, confidence, support count, rank, or downstream multiplicity.

## Proposed finite pairwise classification

For two candidates `A` and `B` presented to the same stable V554 rule family:

```text
1. PRESEMANTIC_VALIDATE(A, B)
   malformed/untrusted object -> reject that object before semantic court

2. BUILD_SUPPORT_PROJECTION(A), BUILD_SUPPORT_PROJECTION(B)
   any identity-bearing field missing/unresolvable -> EQUIVALENCE_UNKNOWN

3. if stable rule id / proposition / target use differ:
      NOT_DUPLICATE_SCOPE

4. if source-universe/risk-set/estimand/measure/weight/native-scope/
   producer epistemic-state/target-temporal-semantics differ:
      DISTINCT_SEMANTIC_SUPPORT

5. else:
      SAME_SEMANTIC_SUPPORT

6. if SAME_SEMANTIC_SUPPORT:
      compare AUTHORITY_SNAPSHOT_FINGERPRINT
      same snapshot -> exact duplicate court
      different snapshots + explicit governed relation -> obey that relation
      different snapshots + no explicit relation -> AUTHORITY_CONFLICT / NO_F1

7. if exact rule invocation requires no new V553 temporal effect and direct basis is complete:
      DIRECT is canonical semantic carrier;
      equivalent no-op V553 path is provenance-only

8. if exact rule invocation requires V553-owned temporal/comparability meaning:
      only a matching V553 semantic basis can satisfy that requirement;
      direct candidate is ineligible for that invocation

9. applicable explicit denial/hard temporal negative/unknown static authority
   is handled under accepted ADP-001 precedence before any positive F1 emission.
```

This classification intentionally separates **duplicate equivalence** from **basis precedence** and **authority precedence**. Conflating those three questions is the easiest path to silent double support.

## Minimum machine-readable requirements proposed to SCR554

A candidate basis entering the duplicate court should be able to expose or immutably dereference all of the following without label reconstruction:

- exact canonical structural proposition semantic ID;
- exact target-use ID;
- stable V554 rule ID plus separate rule version/hash;
- source `EmpiricalUniverse` identity/hash;
- risk-set/sample-frame/cohort semantic identity where identity-bearing;
- exact estimand identity/hash;
- exact measure identity/hash;
- exact weight-basis identity/hash, including an explicit governed unweighted sentinel when applicable;
- native scope/grain identity;
- exact producer epistemic/support-state class relevant to interpretation;
- exact target-use temporal semantic identity/effect;
- exact admission authority identity/version/hash;
- exact V553 temporal authority identity/version/hash where used;
- exact source-relation/comparability authority refs where required;
- exact permission/denial/negative/conflict refs and their semantic roles;
- exact lineage/provenance role assignment;
- basis kind and physical basis refs for replay.

These should be references/fingerprints, not copied producer payload.

## Precedence summary

The proposed ordering is intentionally conservative and consistent with accepted ADP-001:

`INTEGRITY -> PRODUCER-GOVERNED AUTHORITY PRECEDENCE -> APPLICABLE DENIAL/HARD NEGATIVE -> REQUIRED STATIC AUTHORITY COMPLETENESS -> SIGNATURE/TEMPORAL DEMAND -> SUPPORT EQUIVALENCE -> AUTHORITY-SNAPSHOT COMPATIBILITY -> BASIS CANONICALIZATION -> F1`

This ordering ensures dedup never overrides a denial or noncomparability state and never makes a direct path a fallback for an unmet temporal signature.

## Broad-topology assessment

The hostile cases are solvable entirely inside the already delegated SCR554 basis/dedup contract plus the M1 seam with SCR553. They require no new broad semantic owner, no new broad edge, no D15 reopen, and no source retirement.

`BROAD_TOPOLOGY_COUNTEREXAMPLE_CANDIDATE = NO`

`BLOCKED_AUTHORITY_CONFLICT = NO`

The only unresolved point is dispositive selection of the exact machine contract by SCR554, which is the intended parent jurisdiction.

## Feeder token

`S554D_FEEDER_COMPLETE`
