# 04 — Stage 4: from repeat queries to a reusable scientific computation substrate

**Status:** detailed candidate semantics, not implemented/received as a whole. Current native I03 remains the **correctness baseline for its authorized supported operations**, not the ceiling on all future scientific functions.

## A. The actual present execution

Read: [`_pre553_query_eval.py`](https://github.com/maidiu/rawlsing/blob/cea2d4d3009e9087d2267e9d1f53bec28b730dc7/rawlsing_next/_pre553_query_eval.py) (`_evaluate_index_group`, `_evaluate_index_group_core`, `_build_fact`), [`pre553_empirical_query.py`](https://github.com/maidiu/rawlsing/blob/cea2d4d3009e9087d2267e9d1f53bec28b730dc7/rawlsing_next/pre553_empirical_query.py), [`pre553_direct_estate_i03.py`](https://github.com/maidiu/rawlsing/blob/cea2d4d3009e9087d2267e9d1f53bec28b730dc7/rawlsing_next/pre553_direct_estate_i03.py), [new prepared session](https://github.com/maidiu/rawlsing/blob/cea2d4d3009e9087d2267e9d1f53bec28b730dc7/rawlsing_next/pre553_prepared_saved_i03.py).

Present basic operation: resolve exact authorized query/predicate/target plan/source; obtain native release index; visit full respondent scope; for each respondent fetch routing for every target, determine risk-set membership, evaluate predicate/conditions, append denominator, retrieve target response configuration, check weight basis if selected, accumulate exact raw/weighted cells and provenance; then build full result/replay. Typed negative and unresolvable cases are meaningful outputs, not empty fast paths.

- `I03GroupedExecutionScope` caches compatible **measure-independent whole-core** and can reuse it across RAW versus governed weighted regimes under exact key, authority and size guard. It keys target plan + predicate + risk identity, so it does **not** generally share independent predicate leaves across unrelated target plans.
- Native `execute_empirical_query` explicitly refuses grouped execution on `DirectEstateI03Session`. The new prepared session keeps `group_scope=None`; it fixes posting-index reuse, not cross-query scientific work reuse.
- Native predicate `AND/OR` evaluates all child branches, recording used objects and authorities, not Python short-circuit logical evaluation. Replacing this with boolean-only short-circuiting can lose provenance/typed failures while preserving apparent truth values.

## B. Design target, stated in user terms

The hundredth distinct question should be cheaper **when** the prior 99 established legitimately shared source/question, eligibility, predicate, branch, joint or weight preparation. No promise every query is cheaper; genuinely new inputs, complete output ref lists and large full-domain joint combinations impose real lower bounds.

The terminal substrate must support not only current I03 query semantics but future authorized recursive, minority, conditional, shared-country/wave, cross-survey, temporal, signed/diagnostic and Field Forge operations. It must preserve semantics even for those **not implemented yet**, with extensible *computational* primitives rather than inventing scientific laws.

## C. Proposed derived object classes (DESIGN CANDIDATES)

| Derived concept | Plain-language meaning | Critical witness/identity |
|---|---|---|
| `VerifiedReleaseView` | One current-authenticated immutable C11 release in scope | source/custody/member hash, semantic I02 root, release/manifest SHA, CURRENT snapshot checked on use |
| `RespondentOrdinalTable` | Dense internal address ↔ canonical respondent ref | exact universe and source; immutable one-to-one reversible map; no accidental cross-wave linkage |
| `EventAccessSpine` | Question→person and person→event/occurrence physical locators | actual full body/typed-state and row-group address, multiplicity/order/rank |
| `RoutingEligibilityView` | Who was eligible, asked, not asked, inapplicable, unknown for a target and risk contract | source questionnaire/routing authority, exact target/risk, different typed states |
| `PredicateEvidenceView` | Which respondents satisfy a qualified atomic condition and which evidence/authorities were consulted | exact predicate AST/grammar/source/role, negative states and evidence closure |
| `PopulationExpression` | Explicit AND/OR/NOT, child ancestry and exact population operations | grammar semantics, evaluated/all-children provenance, unknown/error rules |
| `TargetResponseProjection` | Respondent-aligned responses to a selected question or component | native/canonical ref, topology, typed states, multiplicity, domain and authority |
| `JointPatternView` | Genuine same-person k-target joint, not product of marginals | ordered components; eligible/answered/overlap bases; full domain/cells/coverage |
| `AnalyticIntermediate` | Reusable conditional/joint counts, entropy/MI inputs, branch gain, minority candidate support | exact estimator, source population, weights, numerator/denominator, status and ancestry |
| `PopulationWitness` | Versioned, independently verifiable exact membership without duplicating long lists | canonical membership, expansion proof, content identity; **prospective v2**, no v1 substitution |
| `IssuedEmpiricalFact` | Separate authorized output and replay | existing immutable I03/F1–F4 owner and fact ABI; authority/negative semantics preserved |

These are logical roles, **not twelve mandatory new classes or databases**. A good implementation may represent several in a single compact read-only structure, with scientific owners retaining their present interfaces.

## D. How an actual multi-operation batch should work

1. **Admit only authorized operations** (including I05-generated), preserve actual query/predicate/catalog identities and scope. Never mint an issuer because it would improve batching.
2. **Inspect demands across the issued workload:** which sources/universes/countries/waves; which source variables/occurrences; which target domains and eligibility; which scalar/3-way patterns and exact predicate leaves recur.
3. **Load/verify one bounded source access view**, not every canonical Python object. Provide both directions to one event store. If whole-file cold authentication is required, account for it once per admitted cold release and preserve CURRENT checks at operation boundaries.
4. **Prepare reusable atomic information** (subject to exact scientific authority), e.g. “Lebanon, age 30–40”, “unemployed”, “Q17 asked”, “Q17 observed state”, “branch descendant of parent P”. No assumption these share denominator/weight.
5. **Compose only demanded subexpressions**: `A ∩ B`, `A ∩ B ∩ C`; preserve typed unknown/refusal and complete relevant provenance. Never materialize exponential powersets of possible predicates or every possible joint cell before actual demand.
6. **Compute actual targets and measures:** eligible denominator vs observed support; raw and authorized weighted cells; ordered/repeated/multiselect actual joint; precise F2 direction; branch gain etc under proper scientific owner. Emit separate facts for separate operations.
7. **Construct exact v1 provenance/replay** even if source access was accelerated. If output is too large, record output-contract cost; do not silently omit member refs or weaken original hashes.
8. **Keep required reusable results** under explicit bound, eviction and invalidation. New operation may add nodes; source/authority/current changes invalidate or refuse; a crash never becomes falsely accepted retained science.

## E. One walk-through: shared cohort, different scientific results

Let A = Lebanese respondents age 30–40, B = unemployed, C = financially insecure; R17 = eligible/asked population for government trust Q17. Then:

- `A ∩ R17`: government-trust distribution in age/country group.
- `A ∩ B ∩ R17`: distribution among unemployed.
- `A ∩ B ∩ C ∩ R17`: financially insecure unemployed.
- Same membership but different governed weight design: **new weighted calculation**, not reuse of raw numerator/denominator.
- Reverse F2: “probability of unemployment given trust” needs **different denominator**, not a copy of “trust given unemployment”.
- Joint F4: answer configuration across Q17, Q24 and Q51 must come from **the same respondents** with appropriate common eligible/answered overlap; pairwise marginals cannot be multiplied.
- F3 recursive branch: child set must remember selected parent, scientific selection/stop rules and minority path; storing only persons in the child loses the discovery history.

**Important:** A can be valid while R17 is unavailable; a false/unknown eligibility state cannot be coerced to no members. A population is defined relative to a scope, not simply a string label.

## F. Memory and algorithmic economics

For 100,000 release-local respondents, one dense membership bitset costs 100,000 bits ≈ 12.5KB **only for the bits**, not respondent refs, state exclusions, index, provenance, proof, or permissions. Sparse/chunked bitmaps may be better if most are out; dense bitmaps may be best for full-country cohorts. No universal choice without understanding actual expected access distributions.

An incremental computational graph amortizes work. Schematic (NOT exact profiling):

- Per-query independent prepare: `T ~ T_save(N)+Q×[T_access(N)+T_condition(N)+T_eval+T_output]`.
- Shared preparation: `T ~ T_save(N)+T_access(N)+Σ unique_condition T_cond +Σ required_relation T_relation+Σ query T_output`.

The `Σ query T_output` lower bound remains; special single queries may cost the same or more because planner overhead is not free. Never promise a numeric speedup from these symbols.

Plan resource bounds: release-local identity mapping; bounded row-group cache; bounded predicate core cache; no all-responses resident default; cap materialized joint cells; deliberate memory pressure fallback that preserves semantics; cold-process and crash restoration distinct from warm in-process reuse.

## G. Cache identity and invalidation court

A candidate reuse key must account for the exact determinants of its computation. At minimum, depending on node type: physical release member roots; semantic source/I02 root; source universe, wave, country/frame, respondent ordering map; question native+semantic+component identities; response topology/missingness/routing policy; predicate AST and grammar authority; risk contract; full response state and target domain; relevant role/scale/source rule; measure/weight/estimand for weighted nodes; active authorization and source relationship; as-of time; scientific rule/estimator version; parent/branch ancestry. **Do not cram all fields into every key**—derive the minimal sufficient determinants per node by proof.

Invalidate/refuse on source corruption, changed source edition, wrong wave/Universe, changed authority/CURRENT, new routing policy, revised scale meaning, different sampling/weight basis, changed index codec, incompatible temporal ordering or noncomparable source relationship. Cached outputs are never independent permission grants.

**Cross-release caching** requires proved comparability/identity, not same question labels. Cross-country/cross-wave source preparation may be reused *within* an authorized multi-universe operation without pooling or linking respondents.

## H. Provenance and negative semantics are computational inputs

The evaluator accumulates used objects/authorities even when an `OR` ultimately evaluates true; it has exact positive and negative result types. Bitset algebra must either preserve all required evidence in the same semantic operations or change the result contract under separately qualified new version. “Optimization” that short-circuits and drops evidence can silently change the fact hash and its trust meaning.

A target can be **zero observed**, **not asked**, **inapplicable**, **missing**, **routing unknown**, **rule unavailable**, **unauthorized**, **noncomparable**, **valid empty**, **partial**, or **supported**. These cannot all be coded as false or zero. A prepared view needs typed outcome and proof for refusing, not merely membership.

## I. Deepest unresolved ABI pressure

Current `_make_execution_replay_ref` and `_build_fact` serialize full risk/denominator member refs and source object closures. That imposes a potentially huge repeated output cost. A compatible optimized engine will still pay it when issuing v1 facts.

**Prospective** versioned shared membership/provenance witness could preserve exact reconstructed refs and evidence once across many outputs. It would require independent authority/consumer adoption, canonical hash/replay migration, exact typed negative and no fake counts. Do not make it a hidden prerequisite to getting a useful sourcefree first consumer.

## J. Required demonstration, not a bakeoff

One **actual integrated set** of distinct authorized operations, including different target plans and shared leaves, with known same-person 3-way joint, reverse F2, recursive/minority branch, relevant weights, empty/unknown/negative, CURRENT revocation, corrupt locator, changed source restore, and qualified FF first consumer. Compare **against the accepted native semantic oracle for supported functions**, and separately test newly restored historical operations against valid corrected estimands—not the old buggy numerics.

Measure exact access count, repeated predicate work, memory/scratch, full facts/replay, cold index preparation and cost per actual consumer. Stop once existing-contract acceptance is met, do not launch rival engines. A single concrete RED justifies a bounded repair, not another indefinite architectural tour.
