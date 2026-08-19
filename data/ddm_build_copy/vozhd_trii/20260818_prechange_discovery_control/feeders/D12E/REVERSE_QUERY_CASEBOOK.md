# D12E — REVERSE QUERY CASEBOOK

**Cell:** `D12E`  
**Status:** `NON_DISPOSITIVE_D12_FEEDER`  
**Purpose:** synthetic information-theoretic fixtures for the declared reverse positioned-subject empirical possibility-field capability  
**Populated-data claims:** `NONE`

## 1. Query semantics used by every case

D12E tests the target capability:

```text
P(Q1, Q2, ... Qk
  | exact lawfully comparable generated-subject empirical properties,
    historical/source scope)
```

The generated-subject side may enter the empirical query only after an exact comparability seam maps generated actor demographic/biographical facts to survey-comparable empirical predicates. D12E does not assume D12D's result. Every such actor-conditioned fixture is therefore marked:

`REQUIRES_D12D_SEAM`.

For one authorized bounded query define:

```text
S  = exact source / source-family / wave / canonical-wave / geography / historical scope
C  = exact governed empirical conditioner predicate
R  = exact target risk-set / routing / applicability predicate
T  = ordered or otherwise topology-governed target vector (Q1,...,Qk)
ΩT = exact lawful target configuration space under each question's response topology
μ  = raw respondent measure and, where governed, a separately identified weighted measure
```

For each `z ∈ ΩT`, the possibility field must be able to distinguish at least:

```text
raw_support(z,C,R,S)
weighted_support(z,C,R,S) where governed
raw_denominator(C,R,S)
weighted_denominator(C,R,S) where governed
probability/mass under the declared measure when denominator > 0
typed support/uncertainty state
source/scope/provenance/risk-set/topology identity
```

The field is a population empirical possibility geometry selected for a comparable generated subject. It is not an actor state.

---

# A — One comparable property

## Query

```text
P(Q1 | age = 35)
```

## Fixture

Generated actor A has exact age 35 at query time.

Survey source S may expose either:

1. exact respondent age; or
2. only an age bin such as `35-44`.

The shared number `35` is not enough to authorize the mapping.

## Information requirement

If D12D lawfully maps the generated age fact to the exact survey predicate, target arity is one. A complete unary conditional distribution is sufficient for this bounded query, provided it carries:

- exact age predicate identity;
- exact risk set for Q1;
- Q1 response topology;
- raw support/denominator;
- governed weighted support/denominator where applicable;
- typed missing/routing states;
- source/wave/time/geography/provenance.

Respondent incidence is not additionally necessary once that exact bounded contingency is already authoritative. It remains necessary, or must have an information-equivalent substitute, if the age predicate or target is to be selected/redefined later.

## Failure modes

- exact actor age `35` silently mapped to survey bin `35-44`;
- age omitted and population marginal used;
- low support hidden behind a percentage;
- survey age field assumed current merely because the generated actor is currently 35.

## Ruling

`TARGET_REQUIRED`  
`EXACT_FIXED_CONTINGENCY_SUFFICIENT_FOR_BOUNDED_QUERY`  
`REQUIRES_D12D_SEAM`

---

# B — Several comparable properties

## Query

```text
P(Q1 | age=35 AND education=high AND locality=Beirut)
```

## Fixture

Suppose three one-property conditionals are known:

```text
P(Q1 | age=35)
P(Q1 | education=high)
P(Q1 | locality=Beirut)
```

No exact three-way intersection contingency is known.

World 1 and World 2 may share all three one-property conditionals while differing arbitrarily inside the intersection:

```text
age=35 AND education=high AND locality=Beirut
```

## Information requirement

The reverse query requires the exact conjunction predicate. Separate marginal conditionals are not sufficient. The machine needs either:

- respondent-bound incidence from which the intersection can be selected; or
- an exact information-equivalent contingency already indexed by the full conjunction.

## Failure modes

- multiplying or averaging the three one-property conditionals;
- treating the narrowest available single conditioner as a substitute;
- dropping locality because its support is inconvenient;
- treating Beirut geography as a nine-stratum structural-position binding.

## Ruling

`UNARY_INSUFFICIENT`  
`RESPONDENT_INCIDENCE_OR_INFORMATION_EQUIVALENT_REQUIRED`  
`REQUIRES_D12D_SEAM`

---

# C — Joint attitudes

## Query

```text
P(Q1,Q2 | properties)
```

## Fixture

Within one exact comparator cohort, let both unaries be balanced:

```text
P(Q1=0)=P(Q1=1)=0.5
P(Q2=0)=P(Q2=1)=0.5
```

World A joint support:

```text
00 = 0.5
11 = 0.5
01 = 0
10 = 0
```

World B joint support:

```text
01 = 0.5
10 = 0.5
00 = 0
11 = 0
```

The unary distributions are identical. Their plausible joint configurations are disjoint.

## Information requirement

For target arity two, the complete `Q1 × Q2` conditional contingency is sufficient for this fixed query. Scalar Cramér's V, NMI, lift, or two independent unary tables are not substitutes for the contingency.

## Independent-sampling attack

Independent unary sampling in either world yields all four combinations with probability `0.25`.

It therefore fabricates half the configuration space in each world and suppresses the actual dependence.

## Ruling

`UNARY_INSUFFICIENT`  
`EXACT_FIXED_CONTINGENCY_SUFFICIENT_FOR_BOUNDED_QUERY`  
`DIRECT_ACTOR_ASSIGNMENT_FORBIDDEN`

---

# D — Higher-order joint configuration

## Query

```text
P(Q1,Q2,Q3,Q4 | properties)
```

## Fixture

The target asks for four responses as one configuration. The empirical field must preserve the distribution over the lawful four-question topology, not four independent marginals and not merely six pairwise scores.

A dense `2^4=16` table is one mathematical representation, but D12E does not require dense materialization. An exhaustive sparse support representation with exact denominator and zero semantics is information-equivalent for the fixed query.

## Information requirement

One of the following is sufficient in information terms:

- exact 4-way contingency;
- exhaustive nonzero 4-way pattern support + exact denominator + explicit zero-state semantics;
- exact factorization that can reconstruct the same 4-way joint without approximation.

Pairwise data alone are not generally sufficient.

## Ruling

`TARGET_REQUIRED`  
`PAIRWISE_INSUFFICIENT`  
`EXACT_FIXED_CONTINGENCY_SUFFICIENT_FOR_BOUNDED_QUERY`

---

# E — Same unary marginals, different joint structure

This is the binary two-variable fixture from C generalized as a theorem.

Two empirical universes can have identical:

```text
P(Q1)
P(Q2)
...
P(Qk)
```

while having different support over `(Q1,...,Qk)`.

Therefore unary equality does not establish possibility-field equality.

### Ruling

`UNARY_INSUFFICIENT`

---

# F — XOR / parity attack

## Query

```text
P(Q1,Q2,Q3,Q4 | properties)
```

Each Qi is binary.

## World EVEN

Uniform probability over the eight bit strings with even parity:

```text
0000
0011
0101
0110
1001
1010
1100
1111
```

Each has probability `1/8`.

## World ODD

Uniform probability over the eight bit strings with odd parity:

```text
0001
0010
0100
0111
1000
1011
1101
1110
```

Each has probability `1/8`.

## Key theorem

For the 4-bit parity construction:

- every unary marginal is identical and balanced;
- every pairwise marginal is identical and uniform;
- every three-variable marginal is also identical and uniform;
- the full four-way supports are disjoint.

Thus even preserving **all lower-order marginals through arity 3** does not reconstruct the 4-way possibility geometry.

## Consequence

No universal rule of the form

```text
all pairwise cotravel known
=> full joint possibility field known
```

is lawful.

Nor is

```text
all lower-order marginals known
=> arbitrary k-way joint known
```

lawful.

## Ruling

`PAIRWISE_INSUFFICIENT`  
`RESPONDENT_INCIDENCE_OR_INFORMATION_EQUIVALENT_REQUIRED`

---

# G — Multimodal population

## Fixture

Within one comparator cohort:

```text
configuration 0000 = 40%
configuration 1111 = 35%
configuration 0011 = 25%
```

Assume all other configurations are observed zero in the exact target/risk set.

## Attack

A modal-only cloud retains `0000` and erases 60% of the population's supported configuration geometry.

A top-2 view retains `0000` and `1111` but converts a substantial 25% third mode into silence.

## Information requirement

The possibility field must preserve all supported configurations needed by the authorized target. Sparse representation is permitted only when it is exhaustive, not thresholded.

## Ruling

`TARGET_REQUIRED`  
`INFORMATION_REQUIREMENT_ESTABLISHED`

---

# H — Contradictory but supported configuration

## Fixture

Suppose a conventional one-axis ideology model expects Q1 and Q2 to align, yet the exact respondent contingency contains a supported configuration:

```text
Q1 = A
Q2 = not-A-like neighboring position
Q3 = C
```

with substantial positive support.

The labels are intentionally abstract. D12E does not infer psychological contradiction or latent ideology. It tests only empirical coexistence.

## Requirement

The configuration must remain a supported empirical possibility even if a model designer regards it as inconsistent.

The field may lawfully say:

> respondents in this exact comparator population exhibited this joint configuration.

It may not say:

> the generated actor is internally contradictory in this way.

## Ruling

`TARGET_REQUIRED`  
`DIRECT_ACTOR_ASSIGNMENT_FORBIDDEN`

---

# I — Minority configuration with low support

## Fixture

Exact comparator denominator:

```text
N = 200
```

Configuration C raw support:

```text
n = 3
```

Weighted support may differ if governed weights exist.

## Requirement

The field must retain at least:

- positive raw support `3`;
- denominator `200`;
- weighted support/denominator if governed;
- low-support/uncertainty status;
- exact scope/provenance.

It must not convert low support to:

```text
IMPOSSIBLE
ABSENT
INVALID
```

merely because the support is beneath a ranking threshold.

## Strongest lawful statement

> Configuration C is observed with positive but low support in this comparator population; its population probability is uncertain/weakly supported according to the available design basis.

Not:

> Actor A is unlikely to believe C in the psychological sense.

## Ruling

`TARGET_REQUIRED`  
`ACTOR_METABOLISM_REQUIRED`

---

# J — Zero-support conditioner

## Query

```text
P(Q1,Q2 | C)
```

but:

```text
N(C,R,S) = 0
```

## Requirement

The conditional distribution is undefined because no eligible observed comparator respondents support the conditioner.

The result must be a typed no-empirical-basis state such as the semantic equivalent of:

```text
ZERO_SUPPORT_CONDITIONER
OUT_OF_EMPIRICAL_SUPPORT
```

D12E does not freeze the eventual enum name.

## Forbidden fallbacks

- population marginal;
- nearest demographic bucket;
- broader geography without authority;
- uniform distribution;
- all configurations assigned probability zero;
- random configuration;
- synthetic interpolation.

## Important distinction

```text
conditioner denominator = 0
```

is not the same as:

```text
conditioner denominator > 0
and one target configuration has observed count 0
```

The first has no conditional empirical basis. The second is an observed-zero cell inside a supported empirical field.

## Ruling

`TARGET_REQUIRED__CURRENT_AUTHORITY_MISSING` where actor comparator cannot resolve  
`DIRECT_ACTOR_ASSIGNMENT_FORBIDDEN`

---

# K — Sparse support

## Fixture

Suppose the target topology has 10,000 theoretically enumerable configurations but only 37 are observed with positive support.

## Sufficient sparse representation

For this **fixed query**, a sparse table is information-equivalent to a dense table if it proves:

1. the exact configuration universe/topology;
2. every positive-support configuration is present;
3. no positive cell was suppressed by top-k, threshold, privacy transform, cardinality cap, or file truncation unless that transform is itself the declared empirical semantics;
4. the exact denominator/risk set is known;
5. omitted lawful configurations are explicitly interpretable as `OBSERVED_ZERO_IN_THIS_RISK_SET`, not generic missing;
6. weights/support/provenance are exact where governed.

## Insufficient sparse representation

A list of the 37 largest patterns without proof that they are all positive patterns is not sufficient.

## Ruling

`EXACT_FIXED_CONTINGENCY_SUFFICIENT_FOR_BOUNDED_QUERY`

---

# L — Routed / not-asked question

## Fixture

Q2 is asked only when Q1 has one specific answer or when a routing condition is satisfied.

For some respondents:

```text
Q2 = NOT_ASKED
```

not:

```text
Q2 = substantive category x
```

## Attack

A naive complete-case join drops all routed-out respondents. A naive categorical encoder converts `NOT_ASKED` into an ordinary answer. Either move changes the possibility geometry.

## Requirement

The query must preserve separately:

- the conditioner C;
- the target risk set R;
- routing/applicability state;
- substantive response topology;
- DK/refusal/IAP/not-asked/inapplicable/missing distinctions where governed.

The eventual query authority may choose, for example, a risk set restricted to respondents eligible for all target questions. D12E does not choose that policy. It requires that the chosen policy be explicit and reconstructible.

## Ruling

`INFORMATION_REQUIREMENT_ESTABLISHED`

---

# M — Different respondent universes with no lawful join

## Fixture

Source S1 observes Q1 among respondents R1.

Source S2 observes Q2 among respondents R2.

There is no lawful respondent identity linking R1 to R2 and no exact higher-order contingency authority connecting them.

## Invalid construction

```text
P(Q1,Q2) := P_S1(Q1) × P_S2(Q2)
```

This creates a synthetic joint respondent universe.

Matching both sources on country, locality, year, age bucket, or another shared label does not create same-respondent cotravel.

## Requirement

D12E permits only:

- separate source-scoped empirical fields; or
- a typed unavailable/noncomparable joint result.

Cross-survey composition is a separate seam. D12E does not solve it.

## Ruling

`RESPONDENT_INCIDENCE_OR_INFORMATION_EQUIVALENT_REQUIRED`  
`DIRECT_ACTOR_ASSIGNMENT_FORBIDDEN`

---

# N — Actor property with no survey comparator

## Fixture

Generated actor A possesses a lawfully generated biographical fact `G` for which no exact survey coordinate/comparator rule exists.

## Requirement

Do not approximate `G` with:

- a semantically similar survey label;
- a nine-stratum structural position;
- geography;
- a nearby demographic bucket;
- an LLM-generated equivalence.

The reverse query must mark the conditioner unresolved or unavailable.

If other generated properties have lawful empirical comparators, a query using only those properties may be a separately authorized less-specific query. It may not silently pretend G was included.

## Ruling

`REQUIRES_D12D_SEAM`  
`TARGET_REQUIRED__CURRENT_AUTHORITY_MISSING`

---

# O — Historically distant survey / questionable temporal comparability

## Fixture

Generated actor query time is `t_actor`.

Candidate survey field is from historical time `t_survey` with a large gap, and the question wording/category system or social referent may have changed.

## Requirement

The field may still describe the historical survey universe exactly. What is not automatically lawful is applying that field as a comparator for the actor at `t_actor`.

Required identity includes:

- raw wave;
- canonical wave;
- empirical observation time;
- question/component semantic authority/version;
- category/topology identity;
- geography/source scope;
- any temporal-comparability authority.

If temporal comparability is unresolved, return a typed unresolved/noncomparable state rather than treating the source as timeless.

## Ruling

`TARGET_REQUIRED`  
`REQUIRES_D12D_SEAM`  
`UNPROVEN` for the actor-to-distant-source comparator until temporal comparability is governed.

---

# P — Same structural position, different comparable biographies

## Fixture

Actors A and B share an exact generated nine-stratum structural position P.

They differ in generated demographic/biographical facts, for example:

```text
A: age 35, education high, locality Beirut, household history HA
B: age 52, education secondary, locality Beirut, household history HB
```

Assume some subset of those facts receives exact empirical comparability under D12D.

## Theorem

Shared structural position does not require a shared empirical possibility field.

If D12D maps the two actor property sets to different empirical predicates:

```text
C_A != C_B
```

then:

```text
P(Q1,...,Qk | C_A,S)
```

and

```text
P(Q1,...,Qk | C_B,S)
```

may lawfully differ even though the actors share structural position P.

Conversely, the structural position P itself is not automatically a survey coordinate or conditioner.

## What this protects

- D10's structural-position noncollapse;
- D12D's separate actor-property comparability seam;
- biography-sensitive empirical differentiation where lawful;
- V3's ability to metabolize the same empirical prior differently through distinct generated histories.

## Ruling

`REQUIRES_D12D_SEAM`  
`ACTOR_METABOLISM_REQUIRED`

---

# 17. Independence attack — exact lossless boundary

Assume an implementation proposes:

```text
for each i:
    sample Qi independently from P(Qi | C)
```

D12E rules this **not generally information-equivalent** to the target possibility field.

Independent unary factorization is lossless only if an exact authority/proof establishes **mutual conditional independence** under the same complete query identity:

```text
P(Q1=q1,...,Qk=qk | C,R,S,μ)
=
Π_i P(Qi=qi | C,R,S,μ)
```

for **every** lawful target configuration `(q1,...,qk)`.

The proof must bind at least:

- the same exact conditioner C;
- the same source/historical scope S;
- the same risk-set semantics R or an exact governed decomposition proving equivalence;
- the same raw/weighted measure semantics μ;
- compatible response topology and routing semantics;
- exact support/structural-zero semantics;
- mutual independence, not merely pairwise zero association.

### Pairwise independence is insufficient

The parity case F proves that all pairs can be independent while the full joint is maximally constrained.

### Different risk sets are fatal to naive factorization

If Q1 is observed among R1 and Q2 among R2, then

```text
P(Q1 | C,R1) × P(Q2 | C,R2)
```

is not an exact statement about one common respondent joint merely because both factors are well estimated.

### Weighting matters

An unweighted factorization does not prove a governed weighted factorization. The measure basis is part of the empirical fact identity.

### Ruling

`UNARY_INSUFFICIENT` by default.  
Independent unary sampling is `UNPROVEN` unless exact mutual conditional-independence authority/proof exists for the full query.

---

# 18. Pairwise attack — exact lossless boundary

Assume the implementation retains every pairwise contingency among target questions.

For k=2, the complete pairwise contingency **is** the full joint for that target and is sufficient when conditioned on the exact C/R/S/measure identity.

For k>2, pairwise contingencies are not generally information-equivalent to the k-way joint.

Parity fixture F proves something stronger:

> Even every marginal of order `< k` can fail to reconstruct a k-way distribution.

Therefore D12E rejects:

```text
pairwise empirical association = full joint possibility geometry
```

and also rejects scalar association summaries as substitutes even at k=2, because a scalar functional cannot reconstruct the full contingency.

### Ruling

`PAIRWISE_INSUFFICIENT` for general k-way reverse inference.

---

# 19. Graphical / factorized representation attack

D12E does not require a dense table as the semantic representation.

A graphical/factorized representation is information-equivalent **only if** it can reconstruct the exact authorized joint distribution and support/typed-state geometry without approximation.

Examples of potentially sufficient exact representations include, in pure information terms:

- exact chain-rule factors covering all target variables;
- an exact junction-tree/factor representation;
- an exact Bayesian-network factorization whose conditional-independence claims are themselves governed/proven;
- another exact algebraic representation.

Insufficient evidence includes:

- a fitted model with nonzero approximation error;
- pairwise graph edges only;
- low NMI edges omitted;
- regularization-induced zeros;
- top-k pattern projection;
- a latent embedding from which exact support/probabilities cannot be recovered;
- independence assumed because no significant association was detected.

### Ruling

`UNPROVEN` unless exact information equivalence is demonstrated.

D12E chooses no model family or physical implementation.

---

# 20. Support and epistemic-state case law

The possibility field must distinguish at least these semantic conditions, without D12E freezing final enum names:

### Positive supported

`N(C,R,S) > 0` and `n(z,C,R,S) > 0`.

Lawful statement: configuration z was observed with positive support under the exact comparator field.

### Low supported

Positive support exists but is weak according to a governed support/uncertainty policy, or simply numerically small where no threshold authority exists.

Lawful statement: supported but weak/uncertain.

Forbidden: impossible.

### Observed zero cell

`N(C,R,S) > 0`, but `n(z,C,R,S)=0`, with exhaustive target enumeration.

Lawful statement: not observed in this sampled empirical field.

Forbidden: metaphysically impossible for a generated actor.

### Zero-support conditioner

`N(C,R,S)=0`.

Lawful statement: no empirical conditional basis exists for the query in this scope.

Forbidden: normalize, broaden, interpolate, or borrow a fallback without separate authority.

### Routed/not asked/inapplicable

Typed eligibility state, not a substantive target value unless exact question-topology authority says otherwise.

### Source disagreement

Two source-specific fields may remain different. D12E requires preservation of the disagreement and source identity, not a winner.

### Unresolved comparability

Actor property cannot be lawfully bound to the survey predicate or historical temporal comparator.

Lawful result: typed unresolved / `REQUIRES_D12D_SEAM`.

### No common respondent universe

Joint target is unavailable without a lawful respondent binder or exact information-equivalent contingency.

### Out-of-support actor

The actor-property predicate is well formed/comparable but lies outside observed survey support.

Lawful result: no empirical basis in that source field, not nearest-neighbor persona assignment.

---

# 21. Actor metabolism boundary

The strongest direct statement D12E authorizes from the empirical field is of this form:

> Under empirical comparator predicate C and historical/source scope S, configuration z has the stated observed support/mass and uncertainty status in the exact target/risk-set topology.

After a lawful generated-subject comparator binding, one may additionally say:

> This positioned subject is associated with empirical possibility field F as an upstream historical population prior/constraint because the exact generated-subject properties were lawfully mapped to C.

One may **not** say:

- the actor believes z;
- the actor has probability p of believing z as present psyche;
- the actor's persona is z;
- the actor will respond z;
- the actor remembers z;
- the actor identifies with z;
- the actor's biography is represented by the respondent cohort.

For the field to affect generated life, V3 would later need a separately governed actor-side rule that admits the possibility field as one input/constraint while preserving generated history, mediation, opportunity, encounter, exposure, relationship, response, memory, and path dependence as separate causal parents/stages.

D12E does not design that rule.

### Ruling

`ACTOR_METABOLISM_REQUIRED`  
`DIRECT_ACTOR_ASSIGNMENT_FORBIDDEN`  
`TARGET_REQUIRED__CURRENT_CONSUMER_MISSING`

---

# 22. Historical profile genealogy case law

D03 establishes that historical V526e/V549/V549b profile language mixed a valid empirical cotravel concern with an intended profile-generation direction that was never fully realized as a profile posterior.

D12E separates two propositions.

## A. Direct survey covariance -> finished persona / psyche

```text
respondent covariance/profile cluster
-> actor persona/belief/identity
```

Ruling:

`DIRECT_ACTOR_ASSIGNMENT_FORBIDDEN`

Historical naming does not revive it.

## B. Respondent-bound conditional/joint geometry -> upstream empirical possibility field

```text
exact empirical comparator
+ respondent-bound conditional/joint response geometry
-> uncertainty-bearing positioned-subject empirical possibility field
-> later separately governed V3 metabolism
```

Ruling under the steering corrective:

`TARGET_REQUIRED`

with:

- actor comparator binding: `REQUIRES_D12D_SEAM`;
- possibility-field information requirement: `INFORMATION_REQUIREMENT_ESTABLISHED`;
- current actor-side consumer/metabolism seam: `TARGET_REQUIRED__CURRENT_CONSUMER_MISSING`;
- direct actor assignment: forbidden.

The target obligation is justified by current owner-declared target ontology, not by the historical word `profile`.
