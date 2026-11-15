# OBL063 — EMPIRICAL CONSUMER AUTHORITY TRACE R1

Status: `PASS`

Terminal:

`OBL063_CONSUMER_AUTHORITY_TRACE_COMPLETE__MINIMUM_AUTHORITY_PER_REAL_CONSUMER_PROVED__D11_GATE_CORRECTION_READY`

## Commission

Worker branch:

`agent/rabochii-obl063-consumer-authority-trace-r1`

Starting HEAD:

`b71784d48f5a64844586cd6b8844cc3f3db71892`

Commission handoff:

`3aea24efa787d263319ddefe9a03be6668352337`

Authorized grain:

`OBL063_EMPIRICAL_CONSUMER_AUTHORITY_TRACE_ONLY`

No country documentary recovery, HB execution, V3/PFF redesign, or source-authority weakening was performed.

## Answer to the six commissioned questions

### 1. Is fully documentary-certified target+frame+design required for every WVS datum to reach downstream runtime?

**No.**

Current code requires an exact `EmpiricalUniverse@1.0.0` object as the source-scope identity used by C11/I03, but RAW single-universe execution does not inspect the universe's target/frame/design fields.

The blanket D11 rule that withheld the EmpiricalUniverse object unless all three documentary claims were positive therefore over-gates source-local RAW use.

### 2. Which operations truly require target/frame/design strength?

Population-generalizing operations, especially where the exact use depends on representative sampling.

The current code separately proves stronger operation-specific requirements:

- `GOVERNED_WEIGHTED` -> exact positive `WEIGHT_DESIGN_ESTIMAND` authority;
- `AUTHORIZED_COMPOSITE` -> exact pooling + nonduplication/source-relation + estimand-composition authority;
- I04 structural use -> exact named structural-admission and target-use authority, plus temporal/weight/estimand/relation authority where that rule requires them.

Target/frame/design documentary certification therefore belongs to the population-use authority lane, not to universal source-scope existence.

### 3. Which operations can lawfully consume source-local respondent distributions?

At least:

- I03 `RAW + SINGLE_UNIVERSE`;
- I03 `RAW + SOURCE_INDEXED_MULTI_UNIVERSE` when facts remain source-indexed rather than pooled;
- exact bounded discovery over RAW facts;
- Field Forge GT2 conditional-support projection, which explicitly requires `SINGLE_UNIVERSE` and `RAW` and explicitly rejects weighted numerator/denominator;
- positioned-subject empirical possibility slices at exact same source/release grain, subject to their conditioner/model/proxy authorities;
- source-local DDM analytical queries whose claim remains source-local.

These consumers still require exact question/response/routing/predicate/target-use authority at their own grain.

### 4. Where does current code conflate object existence with population authority?

The conflation is upstream in D11/HB01 policy, not in the RAW query evaluator.

`EmpiricalUniverse@1.0.0` requires the target/frame/design field names to be present, but has no family-specific validator that requires those fields to be positive documentary facts.

C11 integrity requires the universe's respondent namespace.

I03 then uses the exact universe ref as the source-scope key and validates its authority closure, but RAW execution counts respondents/events/routing and never reads target/frame/design.

Thus:

`D11 documentary fullness -> universe object existence`

is stronger than the actual RAW consumer contract.

### 5. What is the smallest gate correction?

Add one bounded PRE553 materialization/admission profile:

`SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1`

No new public ontology family is required.

It permits an exact EmpiricalUniverse source scope to exist when exact source identity + respondent namespace/replay are established, while target/frame/design unknowns remain explicit typed unknown/not-certified material and the authority carries hard negative limits against population generalization, unauthorized weighting, and cross-universe pooling.

Population-certified use remains a separate positive overlay/permission and continues to consume documentary recovery.

### 6. Does generic OBL063 suffice?

It suffices at the final driver/runtime claim ceiling, but **one PRE553 upstream seam is still required**.

Generic OBL063 correctly prevents:

- source-local -> population laundering;
- missing -> zero;
- implicit coefficient renormalization;
- model prior -> empirical camouflage.

But without a source-local EmpiricalUniverse materialization/admission profile, the PRE553/C11 path can still be starved before OBL063 ever sees the evidence.

Therefore OBL063 needs this one bounded upstream bridge, not a whole audit campaign.

## Key code evidence

- `pre553_empirical_objects.EmpiricalUniverse` requires target/frame/design field names but has no family-specific semantic completeness validator.
- `pre553_c11_integrity` requires EmpiricalUniverse respondent namespace.
- `_pre553_query_predicate._build_release_index` resolves exactly one EmpiricalUniverse and then indexes respondents/events/coordinates/routing/weights by its exact ref.
- `_pre553_query_eval._weight_for` returns exact 1 for RAW; design/estimand authority is consulted only for `GOVERNED_WEIGHTED`.
- `field_forge_conditional_support._validate_common_closure` requires one exact SINGLE_UNIVERSE RAW fact and rejects weighted numerator/denominator.
- `pre553_empirical_query._authorized_composite_refs` requires exact pooling, nonduplication and estimand-composition authority for composite multi-universe use.
- `pre553_structural_admission.evaluate_structural_empirical_admission` binds exact target-use/structural/temporal/measure/relation authority according to the named rule.
- inherited accepted C01 terminal-consumption work found ordinary generated-person V3 runtime consumes compiled V558 structural products and has no lawful ordinary respondent/event-grain empirical runtime dependency.

## WVS7 implication

The present documentary fraction (3/66 materialized in the old D11 court; 5/66 documentary-full prerequisite frontier after separate recovery work) should be interpreted as:

`POPULATION-CERTIFICATION COVERAGE`

not:

`ONLY THESE SOURCES MAY CONTRIBUTE ANY EMPIRICAL EVIDENCE`.

D12's 66/66 exact respondent/source-row identity is sufficient to support source-local universe materialization at the source-scope level once the bounded admission profile exists.

Individual queries remain fail-closed wherever routing, question semantics, response semantics, predicate authority, or other exact query requirements are unresolved.

## Required next action

Implement and hostile-test:

`SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1`

Then recompose WVS7 D11 into:

1. source-local universe materialization;
2. population-certification overlay.

Do not start a 60-country methodology hunt as a runtime prerequisite.

Documentary recovery may continue as authority maximization for the population lane.

