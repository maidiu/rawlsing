# Sociological product and seam contract

This is a proposed adapter contract, not a new semantic authority or a replacement for current owner schemas. Preserve existing owner types and references; the envelope below makes their sociological use inspectable. V3 is a read-only consumer specification in this commission and must not run.

## What PRE-V3 must supply

A consumer requests a geographically and historically situated population, structural position and sequence of conditions. PRE-V3 supplies actor-independent social possibilities, with observed support and modeled extensions separately traceable. It does not select an actual person, invent childhood, assign personality or narrate a biography.

| Product component | Required content and identity | Scientific boundary |
|---|---|---|
| World scope | Geography and historical boundary version; reference/fieldwork dates; population, cohort/age definitions, units, coverage/exclusions; release and as-of identity | Country, sampled population and future simulated person are different units; geography and cohort labels alone do not license transport |
| Material/social conditions | Distributions of resources, work, education, housing, household configurations, social stratification and other demanded conditions where supported; explicit missing channels | A question about deprivation is material experience at its measured unit; an attitude about government is not government capacity |
| Institutions and positions | Qualified institutional facts, rules, implementation/enforcement distinctions, social positions, opportunities/constraints, contextual exposure and objective occurrences/standing conditions | Legal ratification does not establish enforcement; structural opportunity does not imply actor uptake or causal effect |
| Survey distributions | Source-native categories, item/construct mapping, weighted/unweighted estimand, routing/asked/eligible risk set, numerator, denominator, design/weight identity and missingness | Not-asked is not a substantive response; unsupported design uncertainty remains unknown |
| Dependence | Same-person configurations, directional conditional queries, higher-order interactions, component order/roles, minority and recursive alternatives, frontier/coverage | Preserve measured joints. Cross-survey respondents are not linked. Unvisited higher-order work is unfinished, not zero |
| Heterogeneous synthesis | Target-population specification, source contribution graph, compatible/complementary constructs, support diagnostics, harmonization/transport/pooling policy and comparison baseline | Model-based dependence is inferred, even when all marginal inputs are measured. Unsupported overlap requires backoff, not fabricated linkage |
| Time/history | Anchor dates and scopes, measured comparison when qualified, modeled interpolation/drift/gaps/breaks, horizons and contextual historical evidence | Repeated cross-sections do not yield individual trajectories; interpolated years are not observed waves |
| Conditional possibilities | Cumulative ordered conditions, explicit joint predicate, alternatives and support after every step, contextual applicability and uncertainty | Conditioning restricts/updates a social distribution; it does not instantiate parents, children or a life history |
| Provenance and uncertainty | Exact producer/source/method/authority refs, transformations, inference assumptions, uncertainty components, negative states and replay determinants | Digest integrity is not independent custody or scientific calibration; no fake interval precision |

The demanded dimensions are a coverage register, not a claim that every survey measures them. Retain unavailable and weakly supported dimensions alongside permitted fallback policies. Full completion requires all source-supported mandatory obligations, plus explicitly adjudicated global world/service obligations. Unknown work cannot become N/A merely because a first product omits it.

## Minimum versioned envelope

- `contract_version`, `bundle_id`, `content_hash`, `canonical_preimage_ref`, `producer_code_refs` and runtime/dependency identity.
- `world_scope`: geography/boundaries, time range, fielding dates, target population, eligibility, unit, structural-position definition and exclusions.
- `selection`: producer/release refs, exact resolution/selection receipts, use permissions, current/as-of/frozen mode, authority epoch and policy. Frozen mode never bypasses a protected operation's required checks.
- `channels[]`: kind, semantic object ref and dereferenceable value/distribution, support, units/category meanings, item→construct→condition mapping and source scope. An ID-only channel is insufficient.
- `evidence_graph[]`: each node has `evidence_mode` in `MEASURED`, `TRANSFORMED`, `INFERRED`, `PRIOR`; parent refs, exact method/version, parameter/assumption refs, authority/use ceiling and typed uncertainty. Synthetic origin is a separate `test_origin` flag, never a fifth empirical class masquerading as source evidence. A transformed measurement still carries the measured parent; a modeled pooled estimate is inferred.
- `dependence`: observed joint refs and coadministration/risk identities; modeled dependencies with assumptions; issued K/J/depth frontier and outstanding frontier. No bare normalized score can stand for an empirical probability.
- `temporal_model`: qualified anchor refs, interpolation/backoff/break policy, supported horizon, model uncertainty and noncomparability decisions. Direct-comparison issuance remains separate from authority to use an explicit historical prior/model.
- `conditions[]` and `steps[]`: query/predicate refs and order, result alternatives/probabilities or bounds, numerator/denominator/support, missing/negative states and updated uncertainty. Reuse rich C1/N10E/N10W semantics.
- `replay`: all input preimages, seeds where stochastic, exact code/config/environment refs, selected dependencies, invalidation/currentness rules and durable checkpoint refs where invoked.
- `consumer_receipt`: consumer code/schema ref, requested scope/use, input bundle and per-field/value hashes, actual queries and values read, output result hash, refused fields/reasons, replay digest and test evidence scope. Acceptance requires semantic effects, not merely a changed digest.

No `actor_state`, `personality`, `biography`, `childhood_history`, generated `parent`/`coparent` object, person ID or developmental transition belongs in the output. A cohort distribution or household-composition prior is lawful sociology. Sampling a named household and developing its children crosses the seam.

## Consumer contract and discriminating cases

A contract-only consumer dereferences a selected world, asks for progressive conditional possibilities, verifies permissible use and records actual values used. It may compute scenario distributions and inspect possibility sets. It must not invoke V3, V2, actor constructors or a narrative renderer.

| Case | Expected sociological effect | Failure detected |
|---|---|---|
| Same marginals, opposite same-person joints | Conditional result changes under the identical condition; unconditional result stays fixed | Independent-marginal substitution |
| Added cumulative condition | Correct nested risk set and denominator; rare supported alternative remains | Resetting the predicate or losing minority branches |
| Qualified source contribution changes | Appropriate synthesized distribution changes; source graph and uncertainty update | Decorative two-source metadata or ignored input |
| Source support/estimand mismatch | Typed refusal or explicit source-indexed fallback at the affected operation | Silent pooling, fabricated joint or invented permission |
| Changed qualified historical anchor | Only dependent temporal/world channels change, with inferred dates labeled | Unread payload or interpolation labeled observed |
| Break, long gap or outside horizon | Declared backoff/uncertainty/refusal; no unbounded interpolation | False temporal precision |
| Material/institutional context changes | Relevant applicability/world values change while unrelated empirical tables remain stable | Opinion inflated to institution; whole-world overinvalidation |
| Irrelevant context or reordered equivalent input | Semantically equivalent result; deterministic replay, subject to declared order semantics | Hidden coupling or unstable serialization |
| Revoked/stale selected dependency | Current use blocked; permitted historical explanation and siblings retained | As-of/current conflation, stale cache or false root |
| Entirely unsupported condition | Native typed zero-support/unavailable/refusal; no invented actor or arbitrary confident prior | Conflation of sampling zero, missing authority and uncertainty |

For synthetic cases freeze expected values independently of future production output. Source-free examples test interface behavior only. Real-source qualification must bind the exact admitted producer products, original source/design and operation permission, and independent review. The local `repro/seam_contract_probe.py` is a deliberately small, partial executable acceptance oracle, not a complete schema implementation, the existing production service or an empirical qualification.
