# CLOSED35-R1-GSS1973 — Future A/B/C Qualification Test Protocol

This protocol is specified now and executed only in a later exact-carrier qualification court.

No raw carrier was opened and no test in this file was run by this worker.

## Qualification invariant

Every candidate must consume the same frozen `GSS1973_SEMANTIC_OWNER_V1`.

A candidate fails if it changes source-semantic ownership even when its final numeric output appears equal on a particular fixture.

## Required rejection tests

### T01 — X/Y form collapse

**Mutation:** map FORM 1 and FORM 2 into one undifferentiated form coordinate.

**Required result:** REJECT.

**Reason:** 1973 has producer-authorized X/Y experimental forms with form-specific membership and distinct denominators.

### T02 — CLASS / CLASSY aliasing

**Mutation:** alias, coalesce, rename, or share one source response dictionary between `CLASS` and `CLASSY`.

**Required result:** REJECT.

**Reason:** Q56 X has four categories; Q56 Y has five and includes upper-middle.

### T03 — INCOME72 / INCOME equivalence

**Mutation:** declare `GSS1972.INCOME72 == GSS1973.INCOME` or transfer raw response codes/dictionary identity across the release boundary.

**Required result:** REJECT.

**Reason:** producer documentation treats 1972 and 1973 groupings as separate questions/variables after category revision.

### T04 — WTSSNRPS use in 1973

**Mutation:** bind `WTSSNRPS` as a 1973 analytical weight.

**Required result:** REJECT.

**Reason:** accepted documentary authority starts WTSSNRPS in 2004.

### T05 — Q105 Card / questionnaire FORM conflation

**Mutation:** set `Q105_CARD_XY = FORM`, derive card assignment from FORM, or derive FORM from the Q105 card coordinate.

**Required result:** REJECT.

**Reason:** no accepted producer authority proves the join.

### T06 — routing inferred from raw missingness

**Mutation:** convert a raw/system/user missing state into `ROUTED_SKIP` or `FORM_NOT_ADMINISTERED` without documentary form/route authority.

**Required result:** REJECT.

**Reason:** missingness is not eligibility authority.

## Additional required rejection tests

### T07 — 1973 form-weight invention

**Mutation:** apply `FORMWT`, `BALLOTFORMWT`, or an equal-form normalization synthesized from realized form counts.

**Required result:** REJECT.

### T08 — common-item denominator split by FORM

**Mutation:** for an exact variable absent from the 1973 Appendix P form-difference registry and with no independent route, restrict the denominator to one form.

**Required result:** REJECT.

### T09 — source-variable membership by suffix heuristic

**Mutation:** infer Y membership because a variable ends in `Y`, or X membership because it lacks the suffix.

**Required result:** REJECT.

**Reason:** exact Appendix P documentary membership owns the decision.

### T10 — later design import

**Mutation:** apply later `VPSU`/`VSTRAT` strata-cluster survey-estimation semantics to 1973.

**Required result:** REJECT.

### T11 — missing WTSSPS synthesis

**Mutation:** if the exact carrier does not expose `WTSSPS`, create it from another weight or external formula without a separately authorized materialization.

**Required result:** REJECT.

### T12 — physical form-count assumption

**Mutation:** hard-code expected X/Y counts from cumulative aggregates or assume exact half-sample realization.

**Required result:** REJECT.

**Reason:** exact realized counts are later physical observations.

## Required positive fixtures

### P01 — CLASS form eligibility

Given owner FORM=1 and exact variable `CLASS`, owner state must be eligible for the form dimension.

Given owner FORM=2 and exact variable `CLASS`, owner state must be `FORM_NOT_ADMINISTERED` before any response missingness interpretation.

### P02 — CLASSY form eligibility

Given owner FORM=2 and exact variable `CLASSY`, owner state must be eligible for the form dimension.

Given owner FORM=1 and exact variable `CLASSY`, owner state must be `FORM_NOT_ADMINISTERED`.

### P03 — distinct response dictionaries

`dictionary(CLASS) != dictionary(CLASSY)`.

### P04 — common item survives both forms

An exact source variable absent from the 1973 Appendix P registry is `BOTH_FORMS` unless an explicit independent route says otherwise.

### P05 — unclassified physical missingness survives

When no form exclusion, questionnaire route, or substantive response-state authority is proven, a physical missing cell remains `PHYSICAL_MISSING_UNCLASSIFIED`.

### P06 — general weight after eligibility

For a form-specific variable, form eligibility is resolved first. If the exact carrier exposes authorized `WTSSPS`, weight application follows; it cannot expand the risk set.

## Qualification order

```text
1. verify source filename + SHA
2. freeze GSS1973_SEMANTIC_OWNER_V1
3. observe exact physical FORM/variable/weight/missing carriers
4. bind physical facts to owner without semantic inference
5. run all negative and positive fixtures candidate-neutrally
6. start A/B/C only after identical owner receipt
7. require common terminal semantic/replay identity
```

Any candidate-local semantic repair before step 6 is disqualifying.
