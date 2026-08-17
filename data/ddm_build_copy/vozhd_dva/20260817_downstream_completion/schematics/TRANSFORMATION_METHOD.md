# Boundary Transformation Method

For every current stage `B` with downstream consumer `C`, reason over the **cumulative upstream material available to the system**, not a fictional strictly serial handoff.

Rawlsing's downstream architecture is a governed dependency DAG. Earlier outputs do not become unusable merely because another stage has since transformed related material.

The governing sequence is:

`CUMULATIVE UPSTREAM MAP → C DOWNSTREAM NEED → C LAWFUL REUSE OF EXISTING MATERIAL → RESIDUAL NEED REQUIRING B → B LAWFUL INTAKE → B-SPECIFIC TRANSFORMATION → B REACHABLE NEW OUTPUTS → C COMPOSED INTAKE → UPDATED CUMULATIVE MAP`

The central question is:

> Given everything already available upstream, what can the downstream stage use directly, what new meaning does the current stage uniquely need to create, and does the union of reusable upstream material plus current-stage outputs satisfy the downstream stage's actual need?

## 0. Cumulative upstream map inheritance

Every schematic session inherits the accepted cumulative map from all prior adjudicated seams.

The map is additive. It retains:
- upstream producer/stage and object identity;
- semantic/authority material available at each point;
- how later stages transformed, preserved, aggregated, or conditioned it;
- stable provenance/lineage links;
- epistemic, permission, absence, uncertainty, and noncomparability states;
- named downstream uses and restrictions.

When a stage is adjudicated, its accepted outputs are added to the same map:

`pre-V553 map + accepted V553 outputs = S01 inherited map`

`S01 inherited map + accepted V554 outputs = S02 inherited map`

and so on through the chain.

The cumulative map is not merely archival lineage. It is the inventory from which later stages may select useful earlier outputs when that use is semantically lawful.

A later stage is **not** prohibited from reaching back simply because an intermediate stage exists.

Direct reuse of an earlier object is lawful when:
- the earlier producer remains authoritative for the meaning being consumed;
- the object is useful to the current stage's assigned operation;
- a later transformation has not explicitly replaced that object for this particular semantic purpose;
- the consumer preserves the earlier object's epistemic/permission state and lineage;
- the consumer does not silently reinterpret an earlier object as meaning something its producer did not establish.

Direct reuse becomes a defect only when it:
- bypasses a transformation whose derived meaning is actually required;
- creates two competing authorities for the same semantic claim without precedence rules;
- consumes a superseded representation for a use that requires the transformed representation;
- strips provenance, uncertainty, absence, noncomparability, or permission state;
- re-derives or overwrites meaning owned by another stage without authority.

For each active stage, therefore, construct a `SELECTED_INPUT_SET` from **any adjudicated upstream outputs that are useful and lawful**, not only the immediate predecessor.

## 1. Upstream availability envelope

Starting from the inherited cumulative map, inventory the richest lawful objects, authorities, and contexts available anywhere upstream that B or C could potentially use.

For every available surface record:
- producer/stage;
- artifact/object/field;
- object grain and stable IDs;
- structural/temporal/scope identities;
- values, relations, directionality, conditions;
- provenance/lineage;
- epistemic class;
- uncertainty/confidence;
- absence, noncomparability, blockers, permissions, negative authority;
- whether B currently consumes it;
- whether C could lawfully consume it directly;
- whether a later stage has transformed the same underlying material and for what semantic purpose.

Useful classifications include:
- `DIRECT_REUSE_AVAILABLE`;
- `AUTHORITY_CONTEXT`;
- `PROVENANCE_CONTEXT`;
- `VALIDATION_CONTEXT`;
- `TRANSFORMED_VARIANT_AVAILABLE`;
- `SUPERSEDED_FOR_SPECIFIC_USE`;
- `NOT_LAWFUL_FOR_THIS_USE`;
- `UNRESOLVED`.

The existence of a current read path does not prove correctness, and the existence of an intermediate stage does not prove illegitimacy.

## 2. Downstream demand envelope

Before defining B's output, work backward from C.

Determine:
- what operation C is actually responsible for performing;
- every information class C needs to perform it;
- which needs can already be satisfied by lawful direct use of cumulative upstream objects;
- which needs require B-derived meaning because no earlier object contains that meaning;
- which needs are truly required versus convenient;
- what must explicitly remain unresolved, absent, noncomparable, blocked, or uncertain;
- which requested meanings actually belong to C or a later stage and therefore must not be pre-resolved by B.

Partition C's need into:

`C_NEED = REUSABLE_UPSTREAM_INPUTS + RESIDUAL_NEED_FOR_B_DERIVATION + C_OWN_DERIVATION`

This partition is central. Do not make B duplicate upstream information merely to create a self-contained serial packet if C can lawfully use the authoritative upstream object directly.

## 3. Residual obligation of B

After mapping C's direct upstream reuse, identify the residual information that B must create.

Ask:
- what meaning needed by C does not yet exist anywhere upstream?
- what meaning exists upstream but requires B's assigned transformation before C can use it for its intended purpose?
- which upstream materials must B combine to create that meaning?
- what meaning should B leave untouched because an upstream producer already owns it adequately?

This yields B's actual obligation rather than a maximal repackaging obligation.

## 4. Lawful intake selection for B

Now select the upstream objects B itself needs in order to perform the residual transformation.

B may draw from any useful adjudicated upstream output when the use is lawful.

For every selected object state:
- why B needs it;
- which producer owns its meaning;
- whether B consumes it as semantic payload, authority context, provenance context, or validation context;
- whether B is preserving, combining, comparing, conditioning, or transforming it;
- what B is explicitly forbidden from inferring from it.

If multiple upstream objects supply related meaning, define their roles rather than forcing everything through one predecessor merely for pipeline neatness.

## 5. B-specific transformation obligation

Only after upstream availability, C demand, direct upstream reuse, and B residual obligation are known, state exactly what new class of meaning B creates.

Use:

`SELECTED LAWFUL INPUT GRAINS → B-AUTHORIZED OPERATION → B-DERIVED OBJECT GRAINS`

Every B-derived field/object must have:
- lawful source basis;
- explicit transformation rule or governed derivation class;
- retained lineage to its basis;
- epistemic/permission state;
- a clear reason B owns this derivation.

## 6. Reachable new-output envelope

Determine everything B can lawfully create from its selected inputs without invention.

Separate:
- genuinely B-derived meaning;
- lossless reformats useful for downstream consumption;
- aggregates with retained lineage;
- unresolved/negative states generated by B's transformation;
- upstream meaning B merely references rather than reproduces;
- meanings B cannot lawfully create.

The purpose is to understand B's capacity, not to maximize B's packet size.

## 7. C composed intake and sufficiency test

C's lawful input is the union of:

`SELECTED REUSABLE UPSTREAM OBJECTS + ACCEPTED B OUTPUTS`

Test whether that composed intake satisfies C's downstream demand.

For every C requirement, classify its source as:
- `EARLIER_UPSTREAM_DIRECT`;
- `B_DERIVED`;
- `EARLIER_UPSTREAM_PLUS_B_DERIVATION`;
- `C_OWN_DERIVATION`;
- `MISSING_AUTHORITY`;
- `UNRESOLVED`.

B's required output contract is therefore only the minimum set of new/reshaped objects B must contribute to this composed intake.

B does **not** need to carry forward every useful earlier object merely so C can access it, unless doing so is itself useful for integrity, performance, portability, or a named downstream constraint.

## 8. Preservation / transformation ledger

For every important input or inherited distinction classify:
- `DIRECT_REUSE` — later stage may consume the original governed object;
- `REFERENCE` — later stage uses lineage/reference while consuming a transformed object for semantics;
- `PRESERVE_IN_B_OUTPUT` — B must carry the distinction into its own object because B's new meaning depends on it;
- `DERIVE` — B computes governed new meaning while retaining lineage;
- `REFORMAT` — representation changes losslessly;
- `AGGREGATE_WITH_LINEAGE` — compression permitted with auditable source linkage;
- `SUPERSEDED_FOR_SPECIFIC_USE` — original remains available but a transformed object is authoritative for a named use;
- `DROP_EXPLICITLY` — information may be omitted from B output because downstream can lawfully reuse the original or no named capability needs it;
- `FORBIDDEN_TO_INFER` — current stage may not manufacture the value;
- `UNRESOLVED` — authority is insufficient and the unknown survives.

Silent loss remains forbidden. Omission from B's packet is not loss when the authoritative upstream object remains deliberately available to downstream consumers.

## 9. Reconciliation outcomes

For every downstream requirement classify:
- `MEETS_BY_UPSTREAM_REUSE`;
- `MEETS_BY_B_DERIVATION`;
- `MEETS_BY_COMPOSITION`;
- `UPSTREAM_INFORMATION_LOSS`;
- `MISSING_AUTHORITY`;
- `MISPLACED_RESPONSIBILITY`;
- `CONTRACT_GAP`;
- `REPRESENTATION_GAP`;
- `AMBIGUOUS_AUTHORITY`;
- `ILLICIT_BYPASS` — direct reuse skips a transformation required for the intended semantic use;
- `UNNECESSARY_DUPLICATION` — B republishes upstream meaning with no semantic or operational reason.

Do not use `reach-back` itself as a defect category. Cross-stage reuse is normal when governed.

## 10. Worked transformations

At least two concrete examples should travel through:

`cumulative upstream map → C need → direct upstream reuse → residual B obligation → B selected inputs → B transformation → B outputs → C composed intake → updated cumulative map`

Prefer one ordinary and one adversarial/ambiguous case.

## 11. Hostile cases

Test at least:
- contradiction/competing evidence;
- absence versus observed zero;
- unknown versus low confidence;
- noncomparability;
- temporal drift/rupture uncertainty where relevant;
- duplicate/competing authorities;
- legitimate long-range reuse of an earlier-stage object;
- illicit bypass of a transformation that changes the meaning required by the consumer;
- direct structure-to-person/personality inference pressure.

## 12. Session termination

A session ends with:
1. inherited cumulative upstream map confirmed/corrected;
2. downstream demand map;
3. direct-reuse map for the downstream consumer;
4. residual current-stage obligation;
5. current-stage selected input set;
6. accepted transformation equation;
7. reachable new-output envelope;
8. downstream composed-intake sufficiency result;
9. required current-stage output contract;
10. updated cumulative map including accepted stage outputs;
11. preserve/reuse/derive/supersede/drop/forbid/unresolved ledger;
12. concrete dependency/authority defects;
13. implementable obligations;
14. unresolved questions for Vozhd adjudication.

No production implementation begins merely because a breakout worker proposes a schema.
