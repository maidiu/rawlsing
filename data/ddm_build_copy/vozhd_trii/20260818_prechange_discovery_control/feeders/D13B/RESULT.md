# VOZHD TRII D13B — EXACT REPLAY PROOF OBLIGATIONS & HOSTILE FIXTURE COURT

**Repository:** `maidiu/rawlsing`  
**Exact base SHA:** `b92d3f3db9faaa962f59d55e61122701df9e53aa`  
**Branch:** `agent/vozhd-trii-d13b-replay-proof-protocol`  
**Status:** `NON-DISPOSITIVE D13 FEEDER`  
**Write domain:** `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/feeders/D13B/` only.  
**Production semantics changed:** `NO`  
**Retained substrate selected:** `NO`

## FINITE FEEDER VERDICT

```text
PROOF_PROTOCOL_COMPLETE
STATIC_PROOF_EXECUTABLE
SYNTHETIC_FIXTURE_PROOF_COMPLETE
POPULATED_PRODUCTION_PROOF_BLOCKED
SOURCE_EQUIVALENCE_UNPROVEN
```

Combined disposition:

`PROOF_PROTOCOL_COMPLETE__STATIC_PROOF_EXECUTABLE__SYNTHETIC_FIXTURE_PROOF_COMPLETE__POPULATED_PRODUCTION_PROOF_BLOCKED__SOURCE_EQUIVALENCE_UNPROVEN`

D13B awards **neither** `EXACTLY_REPLAY_EQUIVALENT` nor
`INFORMATION_EQUIVALENT_FOR_THE_RETAINED_CAPABILITY_FRONTIER` to any current or
proposed substrate. This feeder defines the burden a candidate must satisfy.
It does not choose the candidate.

## 1. Central theorem

Replay equivalence is not a property of a file, schema, table name, row count,
or hash.

It is a typed relation among:

```text
SOURCE OBJECT
× REPLAY OBJECT
× EXACT EMPIRICAL SCOPE
× AUTHORITY SNAPSHOT
× RETAINED CAPABILITY FRONTIER
× PROOF-PROTOCOL VERSION
```

For every proof-relevant dimension the court must know:

1. source object;
2. replay object;
3. comparison key;
4. expected equality;
5. allowed normalization;
6. forbidden normalization;
7. failure state;
8. typed blocked state.

Those obligations are normative and machine-readable in
`REPLAY_PROOF_CONTRACT.json`.

A candidate cannot pass because its numbers look right. The question is whether
the exact empirical fact remains reconstructible with the same respondent
binder, topology, predicate, risk set, typed state, measure basis, scope,
authority and provenance required by the retained query.

## 2. Two equivalence tokens, two different burdens

### `EXACTLY_REPLAY_EQUIVALENT`

This token requires all mandatory D13B dimensions to pass for the governed
source object. No mandatory dimension may be `FAIL`, `BLOCKED` or `UNKNOWN`.

Physical storage may differ only under an explicitly declared
semantics-preserving normalization. A finite whitelist of current queries
cannot be used to claim global exact replay when the source object and governing
future-query law are broader.

### `INFORMATION_EQUIVALENT_FOR_THE_RETAINED_CAPABILITY_FRONTIER`

This token is narrower and therefore requires a second object: an explicit,
versioned, closed `RETAINED_CAPABILITY_FRONTIER`.

The frontier must name:

- its authority snapshot;
- exact scope policy;
- allowed query classes;
- whether respondent incidence is required;
- any formally permitted information-equivalent substitution;
- explicit exclusions;
- future-extension policy;
- a deterministic frontier hash.

Every frontier-required query and proof dimension must pass. A dimension may be
`NOT_APPLICABLE` only because the frontier explicitly makes it inapplicable,
never because a candidate happens not to contain the necessary information.

Expanding the frontier invalidates the old proof until the candidate is tested
again.

This distinction is important. A complete fixed contingency table may be
information-equivalent for one finite closed query family. It is not thereby
information-equivalent for arbitrary future conjunctions, new predicates,
branch reconstruction, outside-variable reconditioning or k-way incidence.

## 3. Binding inherited law

D13B read the current feeder inputs by their actual branch-carried result rather
than treating their absence from the exact base's `courts/` directory as absence
of a ruling.

### D05

D05 remains:

`BLOCKED_MISSING_POPULATED_DATA_ACCESS`

with audit apparatus:

`CLOSED_EXECUTABLE_FIXED_SEMANTICS`

D13B therefore makes no live-population claim.

The proof contract inherits D05's hostile rules:

- exact respondent-ID sets outrank matching counts;
- raw respondent/question multiplicity is counted, not silently collapsed;
- zero-overlap pairs are real evidence and must remain representable;
- typed missingness is not inferred from blank values;
- response topology is not inferred from observed cardinality;
- source-equivalence requires more than database-internal parity.

### D06

D06 R2 establishes a real V550/V550J shared respondent-grain co-execution
surface and strong declared-column hashing/integrity checks.

It also establishes exactly what it does **not** prove:

- unary replay completeness;
- pairwise replay completeness;
- arbitrary-joint replay completeness;
- repeated/multiselect preservation;
- identical semantic preparation for all `JOINT_ONLY` variables.

Its scalar duplicate policy is therefore a direct hostile target here rather
than a replay theorem.

### D07

D07's controlling future-query law is:

`RECONSTRUCTIBLE_ON_DEMAND`

at the future-authorized empirical query frontier.

That law is not a command to pre-materialize every permitted calculation. It is
a no-information-loss obligation: a later authorized query must be exactly
answerable or must fail with a typed unavailable state.

### D08

D08 supplies the fact algebra that makes exact replay meaningful.

An empirical fact may require:

- exact scope;
- same-respondent binder;
- typed predicate;
- separate denominator/risk set;
- response topology;
- routing/applicability;
- raw and governed weighted measures;
- branch/cohort provenance;
- joint configuration identity;
- authority/provenance.

A repeated, ranked or multiselect response cannot be silently forced into one
scalar respondent×question row. A branch ID without its membership semantics is
not branch replay. Unary marginals do not determine joint incidence.

### D09

The current D09 result makes the numerical-equality trap explicit:

> the same displayed answer under a different lawful predicate, risk set,
> topology, joint configuration or provenance is a different empirical fact.

D13B therefore treats predicate and risk-set identity as proof dimensions in
their own right.

### D10

D10's ontology barrier is preserved in the replay protocol.

An empirical coordinate may be replayed as an empirical coordinate. It may not
be normalized into a generated V3 structural-position predicate merely because
the labels resemble one another.

Accordingly this is forbidden normalization:

```text
income_level = low
    =>
generated actor class position
```

unless a later accepted authority explicitly licenses the transformation.

### D11

D11 shows why downstream provenance cannot substitute for replay proof.

Exact V550J respondent membership is present at the V550J membership surface,
but canonical V551J does not consume respondent membership. Later packet/fact/
join provenance is useful provenance; it is not the same thing as retaining the
respondent-bound empirical incidence needed to reconstruct new conditionals.

## 4. Twenty mandatory proof dimensions

`REPLAY_PROOF_CONTRACT.json` defines 20 dimensions with complete source/replay
contracts and fail/blocked states:

1. respondent incidence;
2. response-event multiplicity;
3. response topology;
4. risk-set identity;
5. routing/applicability;
6. typed missingness;
7. raw support;
8. weighted support;
9. weight basis;
10. scope;
11. predicate identity;
12. condition AST/hash;
13. target identity;
14. branch membership/provenance;
15. k-way joint topology;
16. authority identity;
17. logical content hash;
18. deterministic replay;
19. duplicate semantics;
20. order independence where appropriate.

The key distinction is that these dimensions are not all reducible to a
numerical distribution.

For example:

```text
same denominator count
!= same denominator respondents

same branch N
!= same branch members

same unary marginals
!= same pair incidence

same weighted total
!= same weight basis

same displayed answer distribution
!= same empirical fact

same schema
!= same populated relation

same Parquet hash
!= semantic equivalence
```

## 5. Hash law

D13B gives three kinds of hash deliberately different legal status.

### Serialized-file hash

`PROVENANCE ONLY`

It proves byte identity of one serialization. It cannot prove that a different
serialization is semantically unequal, nor that an equal file captures all
source meaning.

### Schema hash

`PROVENANCE ONLY`

It proves declared shape/version, not populated equality.

### Logical semantic hash

`REDUNDANT_SEMANTIC_INTEGRITY_SEAL_AFTER_DIMENSIONAL_PROOF`

A logical hash is useful only when its projection is itself already proven to
contain every proof-relevant field for the declared claim/frontier. It cannot
replace the dimensional comparison that establishes that fact.

This matters directly to the current shared-substrate implementation:
`logical_shared_substrate_hash()` is meaningful integrity for its declared
logical columns. D13B does not treat that as a universal replay certificate.

## 6. Duplicate law

D13B separates two cases current scalar-key validation can otherwise make easy
to conflate.

### Conflicting scalar duplicate

Two incompatible `SCALAR` events for the same scoped respondent/question have
no authorized deterministic interpretation.

Required result:

`D13B_B_SOURCE_DUPLICATE_SEMANTICS_UNRESOLVED`

The verifier must block before choosing first, last, modal or arbitrary value.

### Legitimate repeated/multiselect/ranked event

Multiple events are lawful when topology says they are multiple events.

Required result:

- preserve event identity/multiplicity;
- preserve set semantics for multiselect;
- preserve explicit rank for ranked responses;
- preserve explicit sequence for repeated events.

Generic `drop_duplicates()` is forbidden replay logic.

## 7. Weight law

Raw and weighted support are separate proof dimensions.

A valid weighted replay requires the exact governed weight basis and exact
respondent weight values/status required by the query.

A missing or invalid weight yields:

`D13B_B_WEIGHT_BASIS_UNAVAILABLE`

It must **not** become `1.0` merely so a weighted calculation can proceed.

Synthetic fixture F16 proves that raw counts can remain equal while weighted
mass changes. F17 proves that replacing missing weight with `1.0` converts a
lawful blocked state into fabricated evidence.

## 8. Scope and identity law

D13B requires source-native and canonical identity to coexist where both carry
information.

Proof scope includes:

```text
source_raw
source_canonical
raw_wave
canonical_wave
country_code
```

and respondent identity is bound inside that scope.

The protocol therefore rejects:

- canonical-source alias collapse that erases source-native provenance;
- raw-wave collapse because two raw forms map to one canonical wave;
- country omission/defaulting;
- globally merging identical respondent IDs from different source scopes.

This is stricter than asking whether canonicalized aggregates happen to match.

## 9. Branch and k-way law

Branch replay requires either:

1. exact member identity; or
2. a deterministic branch reconstruction law with exact predicate AST,
   parent chain, algorithm/version, source semantics and proof that regeneration
   yields the exact same member set.

Same branch support is insufficient.

K-way joint replay requires exact configuration identity, component topology,
completion/routing law and exact joint incidence for every frontier use that can
recondition or relate the pattern to outside variables.

Pairwise marginals do not prove a three-way configuration.

## 10. Future-coordinate law

Current `ddm_v550_branching.py` has a fixed `INDICATOR_FIELDS` list of twelve
coordinates.

That list is current implementation geometry. It is not the definition of the
future empirical capability frontier.

F25 introduces `housing_tenure`, deliberately absent from today's fixed list.
A replay candidate that deletes the coordinate because the present brancher
does not use it fails if a future-authorized retained query is allowed to use
that empirical predicate.

This does not authorize `housing_tenure` as a structural-position predicate.
It remains an empirical coordinate under D10 law.

## 11. Hostile fixture suite

`HOSTILE_FIXTURE_MATRIX.csv` enumerates all 26 required fixtures and
`hostile_fixtures.py` constructs each source and hostile replay explicitly.

The suite includes:

- scalar;
- repeated;
- multiselect;
- ranked;
- routing/not-asked;
- DK/refusal/IAP;
- zero and sparse overlap;
- XOR;
- Simpson reversal;
- rare three-way conjunction;
- conflicting versus legitimate duplicate multiplicity;
- valid and unavailable weights;
- source/wave/country/respondent identity collisions;
- exact branch membership;
- k-way V550J configuration;
- equal marginals with different joint incidence;
- a future coordinate outside current fixed indicators;
- identical displayed answers under different predicates/risk sets.

Execution:

```bash
python run_hostile_fixtures.py
```

Result:

```text
executed_fixture_count = 26
passed_fixture_count   = 26
failed_fixture_count   = 0
SYNTHETIC_FIXTURE_PROOF_COMPLETE
```

The generated evidence is
`SYNTHETIC_FIXTURE_PROOF_REPORT.json`.

## 12. Metamorphic checks

The feeder also executes:

```bash
python -m unittest -v test_replay_proof_protocol.py
```

Six tests pass.

They prove in executable synthetic form that:

- all 26 expected pass/fail/block states occur;
- X and Y can retain the same unary marginals while joint incidence changes;
- XOR can retain every unary marginal while conjunction meaning changes;
- branch support can remain equal while membership changes;
- raw support can remain equal while weighted support changes;
- two source facts can display the same answer distribution while having
  different condition ASTs and risk-set members.

Those are precisely the cases aggregate-only replay tests tend to miss.

## 13. Current shared-substrate pressure points — no substrate ruling

D13B does **not** adjudicate the current shared substrate as retained
architecture. It records only what a later D13 proof may not skip.

### Declared logical hash is not enough

The current shared-substrate hash is a strong integrity check over its declared
logical columns. D13 still must prove that those columns are sufficient for the
chosen frontier.

### Default-filled fields are not source proof

Current shared/prepared canonicalization can fill missing columns with defaults
such as boolean false/unknown values and a default numeric weight.

That may be operationally convenient. D13B does not permit the existence of
such a default to count as evidence that the source meaning was false/unknown
or that the source weight was one. Source semantic equality must be proved.

### Scalar duplicate policy is topology-sensitive

A respondent×variable duplicate rejection rule is safe only after the source is
proven scalar at that grain. Otherwise it can reject lawful repeated,
multiselect or ranked events.

### `JOINT_ONLY` rows require their own proof

D06 established that joint-only extraction may extend beyond base QSM
membership, while identical semantic preparation for every joint-only row was
not demonstrated. D13 may not infer semantic parity from shared column names.

### Fixed current indicators do not close future queryability

Current workload inventory cannot define away a later authorized empirical
predicate.

These are proof obligations, not findings of populated loss.

## 14. What would block a D13 equivalence claim

Any of the following is sufficient to deny the token:

- source respondent identity unresolved;
- ambiguous scalar duplicates;
- topology unknown where multiplicity exists;
- source routing/not-asked semantics unavailable for a frontier query;
- exact risk-set member identity unreconstructible;
- typed missingness collapsed;
- raw support mismatch;
- weighted basis unavailable or changed;
- source/raw-wave/country identity collapse;
- predicate or target authority unresolved;
- branch membership/provenance unreconstructible;
- k-way topology reduced to insufficient marginals;
- required authority snapshot unavailable;
- nondeterministic semantic replay;
- proof depending only on schema/row count/serialized hash;
- candidate unable to replay a frontier query without guessing.

A typed `BLOCKED` state is a lawful result. It is not permission to guess.

## 15. No-DB closure

The protocol and synthetic verifier are complete without populated production
data.

That does **not** make the populated proof complete.

Current state:

```text
PROOF_PROTOCOL_COMPLETE
STATIC_PROOF_EXECUTABLE
SYNTHETIC_FIXTURE_PROOF_COMPLETE
POPULATED_PRODUCTION_PROOF_BLOCKED
SOURCE_EQUIVALENCE_UNPROVEN
```

The first three say the test law is closed and executable.

The final two say D13 still may not claim that a concrete populated candidate
actually preserves production incidence or source-native empirical meaning
until the required populated/source evidence exists.

## 16. Binding input provenance

D13B binds its feeder law to these inspected result blobs:

- D05 `RESULT.md` — `3b8948a8583c76859b4ab003c10ef12ff25ebb9c`
- D05 `D05_AUDIT_CONTRACT.json` — `7285ae94e319d08c57f44bd89f290b55ac9eddb5`
- D06 R2 `RESULT.md` — `5afcbc03c51578725dfeb1f58baa3352e51ce4c0`
- D06 `AUTHORITY_TO_EXECUTION_GRAPH.csv` — `3c4ce74fc21e23f63ef64b3b343638261932b912`
- D07 `RESULT.md` — `d7d99dc768848c0e672fe912e54e40896ed457e5`
- D08 `RESULT.md` — `c766f4b0d6ade72a56e921e6d03aa3dc20fba68c`
- D08 `EMPIRICAL_FACT_ALGEBRA.csv` — `e01c43d20b1e0b17541501683845d4ed62ddb1b7`
- D09 `RESULT.md` — `354f0269ed0654f6f2f4dc4ad100df5d4a9a9a86`
- D10 `RESULT.md` — `e867e7a597be546d91d4cecae568c75f6ccfe57f`
- D11 `RESULT.md` — `06a46105705d8beb159b16336eb671ee0381e726`

The exact commanded D13B base remains
`b92d3f3db9faaa962f59d55e61122701df9e53aa`.

## 17. D13 handoff

D13 may use this feeder to test any candidate substrate.

D13B does not tell D13 which substrate to retain.

The lawful handoff is only:

> Do not call a candidate exactly replay-equivalent because its aggregates,
> schema or file hash match. Prove the typed empirical identities and all
> frontier-required query results. If a required source semantic is unavailable,
> return the typed blocked state. Do not repair uncertainty by choosing a
> convenient representation.

No architecture has been selected.
