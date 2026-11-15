# CASE — ZAK04S F6M / F6P / current receiver boundary

**Case ID:** `ZAK04S:SEAM:R1:F6M_F6P_CURRENT_RECEIVER`. **Primary historical aliases:** `G1A-FUNC-026`, `R5:SEAM:07_F6M_NUMERICAL_MIX`, `R5:SEAM:08_F6P_EVIDENCE_CONSUMER`, `R5:SEAM:35_F6_N9_POLICY_RECEIVER` (cross-references, not reminted T). **Source cut:** `1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa`; producer blob `2df811d76db258d98d89ffb43c830cb221ff9a7d`. **Consumer cut:** `016870e86913e6f7a811a51db6aba2d741bcfe58`; blob `8fa992899293f454d7abded36831a4b4a362df8e`. **Current cut:** protected `6a5c12f04323d74001f9632063ec907f4fc4468e`; guard blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5`.

## 1. Identity and reason

The capability is not “a file named synthesis.” It is a knowledge-producing operation: given independently sampled surveys that each observed a joint distribution over the same constructs, produce a target-population joint **without** pretending the surveys share respondents. When coverage is incomplete, the operation must retain the uncovered mass instead of inventing a point. That is why the old machine’s output is valuable: it turns an impossible “just pool them” request into a bounded partial-identification result.

## 2. Old inbound data

`synthesize(target, sources, policy)` receives:

- a target with `target_id`, geography/boundary, population, unit, year, and target strata shares summing to one;
- sources, each with source identity, product/sample/risk-set/design/weight/routing/missingness/permission refs, survey lineage, explicit test-origin, date scope, axes with reviewed category maps and construct/item/scale/polarity/instrument/response-semantics refs, `MEASURED_SAME_SURVEY_JOINT` dependence, coadministration and joint-frontier refs, and complete declared joint cells with eligible/excluded counts and masses;
- a policy naming exact source weights, reviewed conditional invariance, overlap-review refs, mapping hashes, minimum raw support, joint-domain budget, and bias radii.

Illustrative shape only (not an executed observation): one source stratum may have eligible_n=150, excluded_n=0, with cells covering the full declared cross-product; a second present source may have a table but fail the aggregate support threshold for that stratum. The latter is where the predecessor/repaired difference bites.

## 3. Historical transformation

**Repaired candidate at `1f1c72f8...`** (`synthesize` L186):

1. Validate target shares, source identities, complete native joint domains, raw/mass conservation, reviewed mapping/scale/polarity, and exact policy/source weights.
2. Preserve each source’s native summary and mapped joint baseline.
3. For each target stratum, set `planned` = sources with a table for that stratum; compute `denom` = planned weights; compute `eligible` = sources passing support and mass; compute `eligible_weight`; compute `missing_share = share * (1 - eligible_weight/denom)` and `covered_share = share - missing_share` (L307-L312).
4. Accumulate the covered joint only from eligible contributions; add `missing_share` to uncovered; widen upper bounds by missing mass; compute lower/upper disagreement bounds and bias-sensitivity envelopes.
5. Emit `covered_subprobability` and `uncovered_target_mass` (L364); emit a full distribution only when uncovered is zero; otherwise `decision=PARTIAL_IDENTIFICATION_ONLY` (L380).

**Predecessor at `1428c2e9...`** (`synthesize` L181):

In the predecessor, `denom` is the sum of weights of *eligible* sources and `uncovered += share` sits inside `if not denom` (L284-L287), so the whole target-stratum share reaches `uncovered` only when **no source is eligible** for that stratum. When some planned sources are ineligible but at least one is eligible, it renormalizes `alpha = weight/denom` onto the eligible survivors (L295-L303), assigns no uncovered mass to the excluded present source, and may emit a complete distribution with zero uncovered mass (L327). This is a genuinely different uncovered-mass rule. It is pinned as an alternative producer cut; its historical operational status is not proved here.

**Refusals:** unknown overlap or duplicate samples trigger `SOURCE_INDEXED_BACKOFF` before the candidate is produced; mapping/scale/polarity defects enter diagnostics; in the repaired candidate an ineligible planned source contributes its proportional `missing_share` to uncovered, while in the predecessor partial ineligibility instead renormalizes onto eligible survivors and can emit a complete distribution with zero uncovered mass; real source without an external admission callback raises an error. `conditional` refuses a non-complete joint, a category outside support, or `REAL_USE` without owner admission.

## 4. Old output and consumption

Producer output fields include `covered_subprobability`, `uncovered_target_mass`, `support`, `uncertainty.source_disagreement_and_uncovered_bounds`, `uncertainty.bias_sensitivity_bounds`, `decision`, and `target_joint_status`.

**Actual first reader:** `f6p_partial_bound_evidence_consumer.consume_f6m_evidence` at L189. It imports `pre553_heterogeneous_synthesis as f6m`, verifies the bundle hash and prohibited fields, then:

- requires `covered_sum + uncovered == 1` (L235);
- rejects a complete distribution with uncovered mass and a null distribution with zero uncovered;
- rejects excluded source with zero uncovered as `FALSE_FULL_COVERAGE` (L245);
- maps scope/time/domain/transport refusals to typed states;
- refuses real/self-declared model use as `PROHIBITED_MODEL_USE`;
- returns `PARTIAL_IDENTIFICATION` with bounds and exclusions, never a point when uncovered is positive.

This is a real static importing reader. It is not a selected-world receiver and it issues no source, transport or actor right.

## 5. Intermediate history

- **R29 repair:** the predecessor/repaired difference above is the R29 “native decision and admission repair” line. The earlier R28/R35 receipts and A/A0 variants are identified in the git log but not read end to end in this round.
- **R39 F6P:** actual static consumer created at a separate worker cut.
- **R35 F6C:** a native A/B/C comparative and WP2 consumer delta exists at `c1ebe091f`; only commit metadata and its `02_EXACT_F6_OWNER_BLOB_IMPORTS_AND_CUSTODY.json` disclosure line were inspected. Its full receipt is HELD.
- **pre-Vozhd/Vozhd/Verkhovod/Dva/Trii/Chetiri/Long Memory:** not searched this round; no disposition claimed.

## 6. Modern reality

**Protected current at HEAD `69804f88...`:**

- `pre553_source_relations.py#guard_estimand_composition` L794-L834 returns an `OperationGuardReceipt`. It requires exact semantic-equivalence, overlap and composition authority refs; on failure it raises `OUT_OF_SCOPE`. It has no mixture, covered mass or uncovered mass output. This is the I07 composition **permission guard**, not the numeric producer. Its material schema does name `weight_or_mixture_rule_ref` (L90), but that is an authority reference, not a calculation.
- `rawlsing_next/pre553_analytical_composition.py` uses `coverage_state` at L382/L440/L1105/L1119/L1141, but those values (`RECURSIVE_DEPTH_CONTINUATION`, `DISCOVERY_EXACT_FRONTIER`, `DIRECT_EXACT_SINGLE_QUERY`) are query-frontier reachability states, not target-population uncovered mass. This is a name-collision caution, not an F6M receiver.
- Full enumeration of HEAD (9954 paths) and protected 6a (9709 paths) confirms no `rawlsing_next/pre553_heterogeneous_synthesis.py` under that exact basename; the primary candidate is recovered at `1f1c72f8...` under the worker-return path. `git grep` for `covered_subprobability`, `partial_identification`, `native_bundle`, `f6_sidecars` finds no executable F6M producer/consumer. This is a bounded F6-symbol/path negative, not global absence.
- The same full enumeration finds the protected N9 candidate `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` (blob `84d404...`) plus five N10E test/proof paths. The earlier wildcard lookup that returned empty is preserved as EV020, a false-negative lookup, not absence evidence. Reading the N9 file shows a synthetic 58-respondent A/B/C/Y chain over N10E/C1/F8 with no F6M import; immediate owner modules also contain no F6 token. Therefore this file is not an F6 numeric reader; deeper transitive paths remain NOT_PROVED.

**Branch-only PDEV01 test port at `aa18b6b85...`:**

- `stage/wp2/wp2.py` imports F6M, calls `synthesize` and `conditional` (L45/L49), and builds a read-only envelope at L94 with `native_bundle` hash plus `conditional` sidecars.
- It sets `join_state='NO_AUTHORIZED_COMMON_WORLD_OR_RESPONDENT_JOIN'`, `installation=False`, terminal `OWNER_CHAIN_PARTIAL_WITH_EXACT_HOLD`, model/actor executions zero (L94-L95).
- The protected N9 candidate is present at HEAD and 6a but is a synthetic 58-respondent A/B/C/Y progressive chain over N10E/C1/F8; it has no F6M or partial-bound import in the file or its immediate owner modules. PDEV01 also reports that substituting the F6P schema into the port’s `native_bundle` expectation yields `KeyError: 'native_bundle'`.

**Finding:** F6M/F6P are a preserved sourcefree test-grade chain. The current protected I07 operation preserves permission semantics only. No selected current N9/SOROK numeric reader is proved.

## 7. Mechanism-by-mechanism comparison

- **Predecessor no-eligible-source whole-share uncovered / partial-ineligibility renormalization → repaired proportional missing-share:** changed; the predecessor can emit a complete distribution with excluded sources, while the repaired candidate emits a complete distribution only when uncovered mass is zero. Lost/unproved: which rule was historically accepted. Falsifier: one partial-ineligibility source-exclusion world under both variants.
- **Repaired numeric producer → current I07 guard:** split; authority intent retained, numeric calculation not present. Comparison `NOT_PROVED`, not `SUPERSEDED`.
- **Numeric output → F6P:** preserved at static consumer level (hash, conservation, typed refusal). This is the strongest positive edge in the tract.
- **F6P typed refusals → current:** no equivalent proved at I07.
- **WP2 sidecar:** test-only carrier, no common-world join.

## 8. Cross-references and evidence

- `ZAK04S:EV:R1:001`–`003` producer.
- `ZAK04S:EV:R1:004`–`005` predecessor.
- `ZAK04S:EV:R1:006`–`008` F6P.
- `ZAK04S:EV:R1:009`–`010` I07 guard.
- `ZAK04S:EV:R1:011`–`014` PDEV01 WP2; `015`–`017` full enumeration and N9 correction; `020`–`024` failed lookup, N9 read, importer search, protected 6a identity, ZAK00 matrix.
- `ZAK04S:EV:R1:015`–`017` bounded current search.
- Prior: `ZAK04:EV:G1A_026:OLD`, `R5:EV:07:BEFORE`, `R5:EV:08:BEFORE`, `R5:EV:35:BEFORE`; `ZAK04:SEARCH:G1A_026`; `R5:SEAM:07/08/33/35`.

## 9. Dispositions and future utility

- **F6M numeric producer:** `STRANDED_CANDIDATE` / `SOURCE_LOCATED_NOT_NATIVE_EXECUTION_CONFIRMED`; reusable only as a sourcefree oracle until an owner-qualified diff and first reader exist.
- **F6P consumer:** `STATIC_READER_PROVED` at sourcefree test grade; not an adopted selected reader.
- **I07 guard:** `PARTIAL_RELATED_GUARD`; no numerical equivalence.
- **Current N9 source:** present at HEAD and 6a; its F6 numeric role is `NOT_PROVED` at the read file and immediate owner modules. Not global loss.
- **Next discriminating check:** identify whether any protected N9/N10W producer is *expected* to consume partial-identification bounds; if yes, name its exact input shape and owner. If no, the documented gap is a conscious retirement/absence decision, not a lost implementation.

## 10. Plain English

Old F6M received independent survey joint tables and a target population. It built only what the sources could support: a covered subprobability, an explicit uncovered mass and sensitivity bounds, refusing a full point when coverage failed. F6P really read that product and checked its conservation and refusals. The earlier producer variant added the whole stratum share to uncovered only when no source was eligible; with partial ineligibility it renormalized onto survivors and could report complete coverage despite excluded sources. The repaired variant proportioned the missing mass by planned eligible weight, so partial ineligibility leaves positive uncovered mass. Today the protected code contains an I07 permission guard that asks whether composition is authorized but never computes the mixture. A branch-only WP2 test port carries the F6M bundle as an unjoined sidecar. The protected N9 candidate exists, but it is a synthetic A/B/C/Y chain over N10E/C1/F8 and does not read F6M. Therefore the numerical knowledge is documented and statically consumable at F6P, but current selected-world conservation is not proved; that remains an owner decision, not a build order.
