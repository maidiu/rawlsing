# D12F — AUTONOMY FAILURE CASEBOOK

**Status:** `NON_DISPOSITIVE_D12_FEEDER`  
**Repository:** `maidiu/rawlsing`  
**Exact base:** `6899e58e7ed509327fca3e0294b76bef378d0caf`  
**Branch:** `agent/vozhd-trii-d12f-autonomous-social-discovery`  
**Populated-data claims:** **NONE**. All examples below are synthetic information/search-geometry counterexamples.

This casebook tests two opposite failures:

1. authority so narrow that discovery can only confirm relationships individually named in advance; and
2. search so unconstrained that any combination may be mined without semantic, support, topology, validation, or source law.

The lawful target is between them: **authority predeclares the candidate grammar and admissibility frontier; the data select the discovered relationships.**

---

## Case A — Named-query prison: unexpected two-way conjunction

Let `I` be income (`low/high`), `E` education (`low/high`), and binary response `Y`.

Synthetic equal-size cells:

| income | education | Y=1 share |
|---|---|---:|
| low | low | 0% |
| low | high | 100% |
| high | low | 100% |
| high | high | 0% |

This is XOR.

Marginally:

- `P(Y=1 | income=low) = 50%`;
- `P(Y=1 | income=high) = 50%`;
- `P(Y=1 | education=low) = 50%`;
- `P(Y=1 | education=high) = 50%`.

A system authorized only for individually named unary queries can run:

`P(Y | income=low)`

and:

`P(Y | education=high)`

forever without discovering:

`P(Y | income=low AND education=high)`.

### Ruling

`PREDECLARED_QUERY_ONLY__TARGET_INSUFFICIENT`

The pair/conjunction itself must be allowed to be **data-selected** from an authority-bounded candidate universe.

---

## Case B — The opposite error: "search every conceivable combination"

Suppose there are `p` empirical coordinates, each with multiple categories, plus many response questions. A search over every subset, every category combination, every response topology, every source, and every time slice grows combinatorially.

Even before computational cost, the semantics fail:

- some coordinates are administrative rather than social evidence;
- some category labels are not comparable across sources/waves;
- routed questions do not share the same risk set;
- repeated/multiselect/ranked responses cannot be treated as scalar categories;
- tiny conjunction cells can be numerically extreme but unsupported;
- thousands of candidate tests can manufacture "discoveries" by multiplicity alone;
- absent/forbidden coordinates can be silently converted into false candidate atoms;
- cross-source respondents can be falsely joined;
- source-local and pooled answers can be double-counted;
- missingness can masquerade as an attitude.

### Ruling

`UNBOUNDED_SEARCH__UNLAWFUL`

Autonomy is not absence of authority. It is **data selection inside a governed search grammar**.

---

## Case C — V550 primary-star lockout

Current `secondary_indicator_summary_rows`:

1. scores unary candidates;
2. selects one `primary`;
3. evaluates only `primary + candidate` pairs;
4. requires joint `n >= 50`;
5. emits only positive secondary gain.

Construct three coordinates `A`, `B`, `C` where `A` has the strongest marginal relationship to `Y`, but the strongest interaction is `B×C`.

The current star search never evaluates `B×C`.

### Ruling

A greedy algorithm may be lawful for a declared **greedy diagnostic family**, but it cannot claim complete two-way interaction discovery.

`ALGORITHM_FAMILY_OPEN`

Any nonexhaustive implementation needs an explicit discoverability/coverage contract.

---

## Case D — Three-way parity with zero lower-order signal

Let three binary coordinates satisfy:

`Y = A XOR B XOR C`.

All unary and pairwise associations may be zero while the three-way relation is deterministic.

A search that requires:

- positive unary gain before expansion; or
- positive pair gain before testing triples

never reaches the true relation.

### Ruling

If higher-order joint discovery is in the target family, the authority/algorithm contract must preserve discoverability of lawful k-way effects that have no lower-order signal.

This does **not** require one particular algorithm.

---

## Case E — V548 deviation tunnel

Historical V548 selected a majority-carrying category and recursively followed only its `majority_position_deviation` child.

Construct two different nonselected categories with opposite subgroup patterns. They are aggregated outside the selected category and do not both receive independent recursive exploration.

### Ruling

Historical recursion proves that data-selected branch discovery is possible, but deviation-only recursion is not the target law.

A target recursive search must state its branch-coverage semantics and cannot silently equate "not followed" with "no structure."

---

## Case F — V550 top-two minority deletion

Current `branch_nodes_rows` follows only the two most frequent values of the chosen split variable.

Synthetic split:

- category A: 450 respondents;
- category B: 450;
- category C: 100.

Let C have a stable response distribution sharply different from A/B.

The tree can choose the split dimension yet omit C from recursion entirely.

### Ruling

`TARGET_DISCOVERY_CAPABILITY_REQUIRED`

Minority retention is semantic, not merely a display preference. A supported non-top category cannot become absence because it is not among the two largest categories.

---

## Case G — Simpson reversal hidden by scalar summaries

Construct a pooled association between `X` and `Y` that is positive, while within every lawful stratum `S` it is negative.

A scalar MI/Cramer's-V/top-pair row does not encode:

- the conditioned directions;
- the exact risk sets;
- which stratum creates the reversal.

If marginal and conditioned calculations use different routing/missingness denominators, an apparent reversal can also be manufactured.

### Ruling

Conditional reversal discovery requires exact marginal/conditional contingency identity under a governed risk-set/measure contract.

---

## Case H — Current attitude-cloud order dependence

D04 proved that current V550 cloud pair coverage depends on processing order: the current anchor compares only with already stored candidate frames.

Two permutations of the same lawful question set can emit different pair sets.

### Ruling

For an unordered candidate universe, input/column/processing order may stabilize serialization but may not create semantic candidate precedence.

Permutation/order independence is required **where the search semantics are unordered**.

Directional `A→B` versus `B→A` is a different issue: direction can be semantic and must be typed explicitly.

---

## Case I — Modal-cell cloud erases real nonmodal configuration

Current V550 cloud persists one globally modal joint response cell plus pairwise summaries.

Construct a pairwise contingency with one large ordinary cell and one smaller but well-supported politically/socially distinctive cell.

The distinctive cell can affect the full association score but disappears as an individually addressable empirical fact.

### Ruling

A diagnostic modal projection may be cached; it cannot be the sole authority for discovery that claims minority or contradictory-configuration coverage.

---

## Case J — Branch label without membership

Two branch artifacts both say `branch_7`, and both have `n=100`, but contain different respondents.

Their branch-conditioned response distributions differ.

A branch label/count/tree summary cannot recover which world is real.

### Ruling

Branch-conditioned discovery requires:

- exact predicate + provenance sufficient to deterministically recreate membership; or
- explicit immutable member incidence.

`RECONSTRUCTIBILITY_REQUIRED`

---

## Case K — Repeated/multiselect topology collapsed as scalar duplicate

One respondent lawfully selects `{A,B}` for a multiselect question. Another source encodes repeated observations of scalar `A`.

If both become multiple rows under one scalar respondent×question key, a duplicate validator can either reject lawful data or collapse distinct event topologies.

### Ruling

Response topology/event multiplicity is part of candidate and risk-set authority. Scalar deduplication cannot define generic discovery semantics.

---

## Case L — Weight-sensitive rank reversal

Construct a sample where unweighted counts favor coordinate `A`, while governed survey weights make coordinate `B` the stronger social fork.

Historical V547 was unweighted; current V550 mixes weighted entropy-style ranking with unweighted NMI/Cramer's V in adjacent outputs.

### Ruling

Discovery authority must name the measure basis and validation rule. Raw and weighted results are not interchangeable merely because both are available.

---

## Case M — Multiple-testing mirage

Assume 1,000 genuinely null candidate coordinates/conjunctions. With an unguided significance screen, some will look extreme by chance.

Autonomy that ignores the candidate family size can manufacture social "forks."

### Ruling

Where statistical inference is used, authority must bind a multiplicity/validation regime or explicitly declare why it is not applicable.

D12F does not select one statistical method. Lawful possibilities include exact/randomization tests, design-based uncertainty, resampling/stability, held-out replay, multiplicity control, or another governed validator appropriate to the data-generating/sampling contract.

---

## Case N — Typed missingness becomes social meaning

Suppose `99 = refused` and `98 = not asked`. If these nonblank codes enter the response content as ordinary categories, a strong "association" may merely measure questionnaire routing/refusal.

D04 proved current cloud preparation can admit nonblank special states.

### Ruling

Typed absence/routing semantics are part of discovery identity. Missing/refusal/IAP/not-asked may be analyzed **as missingness phenomena only under separate authority**, not silently as substantive attitudes.

---

## Case O — Temporal coding drift masquerades as fork change

Wave 1 codes education as three levels; wave 2 codes five levels. A literal label comparison can show a changed income×education fork even if the population relation is unchanged.

### Ruling

Temporal fork discovery requires governed cross-wave comparability/harmonization. Noncomparability is a valid result.

---

## Case P — Cross-source false respondent join

Lebanon-local survey respondents and WVS respondents both have respondent ID `123`.

Joining by raw respondent ID would fabricate a person who answered both surveys.

### Ruling

Cross-source disagreement discovery compares **separately scoped empirical facts** unless exact cross-source respondent identity authority exists.

No such join can be inferred from ID collision.

---

## Case Q — Naive pooling erases source disagreement

Source A shows a strong low-income fork; Source B shows none. Naively pooling the samples produces a moderate average and hides the disagreement.

### Ruling

Cross-source disagreement can itself be a discovered result. Source identity, weighting, sampling universe, and comparability must remain explicit.

---

## Case R — Materialization fallacy

A lawful pair or conjunction is discovered on demand and exactly reproducible from retained respondent incidence plus authority.

Nothing in its semantics requires a permanently stored pair/conjunction table.

Conversely, a precomputed table can be semantically inadequate if it omitted topology, risk-set identity, minority cells, or provenance.

### Ruling

`DISCOVERY AUTHORITY != DISCOVERY RESULT != MATERIALIZATION AUTHORITY != CACHE POLICY`

`MATERIALIZATION_NOT_REQUIRED`

`RECONSTRUCTIBILITY_REQUIRED`

---

## Case S — Demographic fork becomes actor psyche

Population fact:

`P(Y | income=low, education=high) = 0.72`

Illicit conclusion:

"a generated low-income/high-education actor has a 72% belief propensity toward Y" or "therefore this actor believes Y."

### Ruling

Forbidden.

Autonomous social discovery is population empirical discovery. D10 and the target corrective preserve the separation from generated nine-stratum position and from finished actor psyche/belief.

The target capability may later feed separately governed empirical possibility or structural lanes, but D12F creates neither downstream promotion authority nor actor state.

---

# Casebook conclusion

The failures divide cleanly:

- **too little authority:** only named hypotheses can be confirmed;
- **too much freedom:** semantically invalid, unsupported, multiplicity-inflated, topology-breaking combinations are mined;
- **algorithmic shortcut mistaken for semantics:** greedy/top-k/order-dependent procedures hide lawful candidates;
- **storage mistaken for capability:** precomputation is treated as necessary or sufficient;
- **population discovery mistaken for actor causality:** social evidence is copied into psyche.

The target authority shape is therefore a **bounded candidate-and-validation grammar** whose individual positive relationships are determined by the data and remain exactly replayable.
