# FFIF007 — OBJECT IDENTITY AND GRAIN

## 1. Four-level hierarchy

### `OBJECT_FAMILY`

A broad design lineage sharing a primitive representational commitment: exact joint-state objects, conditional objects, order/neighborhood objects, incidence/topology objects, metric geometry, latent mixture/model objects, motifs/signatures, or transport objects.

Family is discovery and registry vocabulary. It is too coarse to enter a closure court by itself.

### `ADMISSIBLE_OBJECT_SPECIFICATION` (`AOS`)

The finite-universe member. It freezes a claim-relevant empirical interface and all constitutive commitments required to construct and query it.

Minimum identity tuple:

```text
AOS_IDENTITY = hash(
  comparison_claim_hash,
  object_family,
  primitive_relation_and_equivalence,
  normalized_assertion_interface,
  invariant_and_loss_profile,
  semantic_and_representation_commitments,
  authority_dependencies,
  input/output domain,
  inferential_ceiling,
  stronger_view_query_dependency,
  validity_and_split_rules
)
```

### `METHOD_VARIANT`

An algorithm, estimator, hyperparameter region, optimization strategy, implementation, or nuisance setting operating inside one AOS without changing its frozen identity tuple.

Variants require sensitivity/hostile testing where registered. They are not independent votes and do not inflate `|U|`.

### `EXECUTION_INSTANCE`

One run under exact code/version, seed, partition, data hash, and numerical environment. It produces evidence about an AOS; it is not a new object member.

## 2. Mandatory split rule

Two candidates must be separate AOS members before results when any difference changes:

- a constitutive assertion slot or whether it is primitive/derived/undefined;
- state, category, order, metric, adjacency, neighborhood, mixture, motif, or transport semantics;
- the equivalence relation over inputs or outputs;
- claim-required invariant coverage or loss classification;
- hard-zero versus approximate preservation;
- authority dependencies or source-native ancestry ceiling;
- inferential class or ceiling;
- whether a stronger representation is consulted at query time;
- a claim-relevant commitment coordinate used in weaker/dominance adjudication.

Example: ordinal neighbor order and cardinal metric distance are distinct AOS objects even if both are called geometry.

## 3. Non-split rule

Keep candidates as method variants when they preserve the same exact interface and commitments and differ only in:

- optimizer or solver;
- seed;
- computational layout/index;
- equivalent estimator implementation;
- tuning within a preregistered nuisance region that does not change object semantics;
- display rotation that does not change admitted relations;
- storage/compression implementation preserving the same lawful object.

PCA, MCA, UMAP, factor analysis, k-means, LCA, and random forest are not automatic AOS names. Their status depends on the object they lawfully produce for the claim.

## 4. Result-bearing variation

Material output variation inside one frozen AOS has three possible dispositions:

1. `METHOD_SENSITIVITY_WITHIN_SPEC`: identity tuple holds; the AOS becomes unstable or fails its nuisance contract.
2. `PREEXISTING_HIDDEN_SPEC_DIFFERENCE_DISCOVERED`: the variant changed a constitutive commitment that should have been frozen; the comparison is invalid and must restart with split specifications.
3. `NUMERICAL_NONREPLAY`: implementation failure or unresolved numerical tolerance.

It is forbidden to split a coarse AOS after outputs merely to quarantine an inconvenient variant while retaining the original closure hash.

## 5. Composite objects

A set of AOS members is not automatically another AOS. If querying the set merely unions independently authorized assertion interfaces, it is a `SUFFICIENT_SET` candidate. If fusion creates a new primitive relation, learned bridge, semantic equivalence, or cross-object interaction, the fusion is a separate AOS and must be admitted before freeze.

This prevents minimal-set search from smuggling a new representation through the word “combination.”
