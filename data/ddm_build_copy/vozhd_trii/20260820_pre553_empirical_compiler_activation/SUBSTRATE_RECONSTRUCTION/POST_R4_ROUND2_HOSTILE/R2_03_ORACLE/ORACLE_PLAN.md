# ORACLE PLAN — COURT_MINREF@2

Status: `IMPLEMENTATION_BLUEPRINT_ONLY__NO_RUNTIME_MUTATION`

## Objective

Build the **smallest independent evaluator** that can make a later carrier implementation court dispositive without becoming a second Rawlsing.

The evaluator has four modules and one common typed interchange.

## Module A — `court_freeze`

Responsibilities:

- validate exact Authority 54/55 and frozen contract/source identities;
- bind exact candidate commit;
- bind exact built artifact/physical root;
- bind compiler/configuration/profile/cache policy;
- canonicalize and hash complete tuning-workload disclosure;
- record evaluator/test corpus version;
- after all candidate commitments, generate explicit oracle nonce;
- derive and seal blind-frontier identity.

Forbidden:

- default branch / latest release lookup;
- wall-clock data in identity;
- hidden randomness after receipt;
- candidate changes after nonce without restarting.

Suggested artifact:

`ORACLE_RUN_MANIFEST.json`.

## Module B — `passive_reader_<carrier>`

One parser may be required per physical carrier schema, but every parser emits the same interchange.

Responsibilities:

- open the exact immutable root path/object supplied by the court;
- independently recompute physical hashes necessary to establish byte identity;
- enumerate canonical members as *observed*, not as expected;
- decode physical lanes/direct relations;
- emit `PRIMITIVE_WITNESS@2`.

Forbidden imports/dependencies:

- candidate semantic object constructors;
- candidate virtual-event materializer;
- candidate query/discovery/admission engine;
- candidate caches/indexes for correctness;
- R4 physical reconstruction;
- production C11/I03/I05/I04 semantic functions.

A candidate-specific parser is not a semantic waiver. If the physical schema is so opaque that an independent parser cannot be implemented from a frozen specification, the carrier remains blocked.

## `PRIMITIVE_WITNESS@2`

Recommended record envelope:

```text
surface
source_snapshot_id
record_kind
identity_tuple
typed_payload
authority_refs
semantic_order_fields_if_any
```

Canonical tuple serialization must distinguish:

- integer/bool/type tags;
- exact float-bit identity where the frozen source frontier exposes it;
- string byte/code-point sequence including empty/NUL;
- physical no-payload/system/user/extended missing;
- semantic response/absence state;
- routing state;
- ordered versus set-like fields.

Large releases should compare by bounded external sort/merge on canonical key + payload digest, while retaining an exact mismatch witness.

## Module C — `minref_semantics`

This module contains no physical planner.

### C11 acceptance projection

For the fields/surfaces required by M01-M18:

- construct canonical acceptance tuples from source/authority primitives;
- construct the same tuples from candidate primitives;
- independently serialize/hash them;
- compare exact expected/observed refs and completeness.

It does not need to instantiate production objects.

### I03 set evaluator

Required operations:

- scoped respondent universe;
- primitive predicate membership;
- AND/OR/NOT with NOT relative to governed risk universe;
- target event selection;
- routing/applicability/risk-set membership;
- source scope;
- raw numerator/denominator;
- exact authorized weighted support where authority closes;
- typed positive/zero/empty/unavailable/noncomparable states.

Use straightforward sets/sorted IDs/Fraction-or-Decimal style arithmetic as required by frozen exactness. Performance is secondary.

### I05 bounded evaluator

Required:

- deterministic candidate generation from frozen grammar/templates;
- exact pair and bounded k-way combinations;
- conditional/reversal;
- recursive subgroup;
- branch-conditioned;
- co-signature/joint inputs;
- full candidate-count == covered-candidate-count proof;
- no diagnostic-driven pruning.

### I04 minimal evaluator

Encode only the frozen decision-state precedence and positive-projection permission exercised by the acceptance corpus.

If a semantic surface cannot be encoded independently without importing production implementation, the court is not yet independent enough for dispositive acceptance.

## Module D — `oracle_controls`

Runs before any candidate evaluation.

Control catalog is content-addressed and versioned.

### Required destructive families

1. identity permutation with unchanged marginals;
2. drop/duplicate compensation;
3. zero-incidence declaration deletion;
4. dictionary/variable identity collapse;
5. physical/semantic state collapse;
6. negative-result flattening;
7. topology permutation/dedup;
8. routing authority mutation;
9. weight/design authority mutation;
10. source relation mutation;
11. semantic projection mutation with stale ExactRef;
12. semantic deletion + recomputed candidate-format digests;
13. intentional evaluator-field omission canary.

### Required invariant families

1. physical record reorder;
2. legal shard/block regroup;
3. cache deletion;
4. lawful worker-count variation;
5. incidental filesystem enumeration variation.

Each control has an exact expected court outcome.

`ORACLE_CONTROL_PASS` requires all controls to match expected outcomes.

## Independence test for the evaluator codebase

Before use, statically inspect/import-audit the evaluator.

Disallowed semantic dependencies:

- production `rawlsing_next` semantic modules;
- candidate semantic/materialization/query modules;
- candidate cache/index implementations.

Allowed:

- standard library;
- frozen low-level file-format libraries required to parse bytes;
- cryptographic/hash libraries;
- a separately versioned declarative contract table copied from frozen authority and reviewed as data.

The import audit itself is not proof of semantic correctness; mutation adequacy remains mandatory.

## Source execution

For real implementation certification:

- exact source bytes are verified against governed identities;
- expected source primitives are produced through the frozen source-native decoder/accepted source witness whose lineage resolves to those bytes;
- the independent candidate reader never uses candidate source decoding to define expectation.

R2-03 performs no new raw-source probe.

## Run outputs

A dispositive run should emit at minimum:

- `ORACLE_RUN_MANIFEST.json`;
- `ORACLE_CONTROL_RECEIPT.json`;
- source primitive expectation digest + counts by kind;
- candidate passive primitive digest + counts by kind;
- exact mismatch witnesses, if any;
- C11/ExactRef receipt;
- I03 receipt including set digests;
- I05 frontier/coverage receipt;
- I04 admission receipt;
- integrity/cache/replay/authorization receipt;
- final atomic acceptance state.

No pass percentage is emitted as an acceptance metric.

## Complexity limit

Reject the evaluator design if it accumulates:

- a persistent semantic database;
- a second optimizer/planner;
- source-family semantic special cases;
- a general harmonization layer;
- production caching;
- candidate-specific semantic expectations.

Carrier-specific physical parsing is the only intended specialization.
