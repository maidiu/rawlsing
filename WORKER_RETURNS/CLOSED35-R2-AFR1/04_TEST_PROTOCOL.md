# CLOSED35-R2-AFR1 — Synthetic / Source-Independent Test Protocol

Status:

`TESTS_AUTHORED__NOT_EXECUTED`

This browser/GitHub worker did not open the canonical SAV, run source decoding, execute source processing, run Candidate A/B/C, run I05, run whole-source physical equivalence, or run measured P2X.

The tests below define the mandatory rejection and positive behavior for later qualification of the exact source-specific owner:

`AFROBAROMETER_R1_SEMANTIC_OWNER_V1`

## Qualification invariant

All Candidates A/B/C consume one frozen source-specific semantic owner.

Candidate-local physical implementation may vary.

Candidate-local source semantics may not.

A candidate fails if it changes identity, country-coordinate scope, SUPDEM physical/documentary state, weight role, bounded-UNKNOWN behavior, or national-instrument interpretation even when a particular downstream numeric output happens to match.

## Required rejection tests

### T01 — CASENUMB / documentary RESPNUMB alias invention

**Mutation**

Set:

`CASENUMB == RESPNUMB`

or use documentary `RESPNUMB` as an alias/name for exact source `CASENUMB`.

**Required result**

`REJECT__UNAUTHORIZED_IDENTITY_ALIAS`

**Reason**

Authority71 R1-G01 explicitly leaves the exact source/documentary join unresolved.

### T02 — cross-country or hard replay identity from survey IDs

**Mutation**

Use any of:

- `CASENUMB`;
- `COUNTRY + CASENUMB`;
- `REFNUMB`;
- documentary `RESPNUMB`;

as the hard Rawlsing replay key, cross-country person identity, cross-round identity, or longitudinal identity.

**Required result**

`REJECT__NATIVE_SURVEY_ID_PROMOTED_TO_REPLAY_OR_PERSON_IDENTITY`

**Reason**

Hard replay is exact source SHA + physical row ordinal. Accepted preparation evidence also records CASENUMB collisions after COUNTRY composition.

### T03 — weight-role or default-weight invention

**Mutation**

Select an analytical default because:

- a field is named `WITHINWT`;
- a field is composite;
- a field is non-null;
- a field has a particular magnitude;
- a later Afrobarometer round uses a similarly named field.

Or assign a carrier an undocumented role.

**Required result**

`REJECT__UNAUTHORIZED_WEIGHT_SELECTION`

**Reason**

The realization preserves documented R1 roles but authorizes no universal analytical default or estimand.

### T04 — SUPDEM special-code coercion into physical missingness

**Mutation**

Convert any documentary special code to system/user missing solely from semantic label, including:

- `4 = DONT_KNOW`;
- `97 = NOT_APPLICABLE`;
- `98 = REFUSED`;
- `99 = MISSING_DATA`.

Canonical negative control:

`SUPDEM=99` -> generic physical null.

**Required result**

`REJECT__DOCUMENTARY_SPECIAL_CODE_COERCED_TO_PHYSICAL_MISSING`

**Reason**

The accepted R1 packet treats the codes as ordinary physical storage with separately authorized documentary meaning.

### T05 — semantic generalization across national instruments

**Mutation**

From one merged source variable, assert identical question wording, response options, routing, or semantic meaning across all 12 national instruments without exact per-variable documentary authority.

**Required result**

`REJECT__UNAUTHORIZED_NATIONAL_INSTRUMENT_EQUIVALENCE`

**Reason**

The accepted Round-1 codebook explicitly documents nonstandardized national instruments and source-level merging of identical/similar/conceptually equivalent questions.

### T06 — Candidate A/B/C semantic divergence

**Mutation**

Candidate A returns `BOUNDED_UNKNOWN` for CASENUMB↔RESPNUMB while Candidate B aliases them, or any candidate selects a different SUPDEM/weight/country/national-instrument law.

**Required result**

`REJECT__CANDIDATE_SEMANTIC_DIVERGENCE`

### T07 — canonical source SHA drift

**Mutation**

Bind the realization to any SHA other than:

`6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2`

**Required result**

`BLOCKED__CANONICAL_SOURCE_ROOT_UNPROVED`

### T08 — later-round country map leakage

**Mutation**

Interpret a Round-1 numeric `COUNTRY` code using the R5 or R9 coordinate system.

**Required result**

`REJECT__CROSS_RELEASE_COORDINATE_IMPORT`

### T09 — discard one of the five R1 weight carriers

**Mutation**

A physical realization omits any one of:

- `WITHINWT`;
- `ACROSSWT`;
- `COMBINWT`;
- `AFRICAWT`;
- `AFCOMBWT`;

because the current analytical workload does not use it.

**Required result**

`REJECT__SOURCE_WEIGHT_CARRIER_LOSS`

**Reason**

EC12 requires source-native weight candidates to survive independently of later analytical use.

### T10 — routing inferred from missingness or label alone

**Mutation**

Treat `SUPDEM=97` as proof of a routing/applicability path without the exact accepted country/question documentary rule, or infer eligibility from absent/present values.

**Required result**

`REJECT__ROUTING_INFERRED_WITHOUT_DOCUMENTARY_AUTHORITY`

**Reason**

Physical state and documentary applicability are separate authority layers.

## Required positive synthetic fixtures

These fixtures are source-independent. They test the realization law, not the raw survey.

### P01 — common owner identity

Given candidate labels `A`, `B`, and `C`, every candidate binding returns exactly:

`AFROBAROMETER_R1_SEMANTIC_OWNER_V1`

with the same canonical SHA and bounded-UNKNOWN law.

### P02 — REFNUMB remains a useful source-local attribute without replacing replay

Given a synthetic row:

- source SHA = canonical AFR1 SHA;
- row ordinal = 42;
- REFNUMB = 9001.

Expected:

- replay identity = `(canonical SHA, 42)`;
- REFNUMB owner state = `DOCUMENTED_UNIQUE_CASE_REFERENCE__SOURCE_LOCAL_ATTRIBUTE`.

### P03 — CASENUMB / RESPNUMB remains bounded unknown

Given:

- source carrier `CASENUMB=123`;
- documentary concept `RESPNUMB=123`.

Expected relation:

`BOUNDED_UNKNOWN__CASENUMB_TO_RESPNUMB_RELATION`

Numeric equality does not create an alias.

### P04 — documentary MISSING_DATA remains physically ordinary

Given a synthetic physical cell:

- variable = `SUPDEM`;
- raw value = `99`;
- physical missing state = ordinary;
- accepted documentary semantic state = `MISSING_DATA`.

Expected owner output contains both:

- `physical_class = ORDINARY_STORED_VALUE`;
- `documentary_state = MISSING_DATA`.

No dimension overwrites the other.

### P05 — five weights survive with no default

Given all five exact R1 weight-carrier names, expected owner output:

- preserves all five;
- attaches the accepted source-local role to each;
- returns `DEFAULT_WEIGHT = NONE_AUTHORIZED_BY_SOURCE_SPECIFIC_REALIZATION`.

### P06 — unresolved national equivalence stays typed UNKNOWN

Given a merged source variable and no exact per-country documentary variant for the requested semantic claim, expected state:

`BOUNDED_UNKNOWN__NATIONAL_INSTRUMENT_EQUIVALENCE_NOT_PROVEN`

No candidate may substitute a family analogy.

## Later physical qualification order

The later court must preserve this ordering:

```text
1. VERIFY EXACT AFR1 SOURCE FILENAME + SHA
2. FREEZE AFROBAROMETER_R1_SEMANTIC_OWNER_V1
3. BIND R35-I01 PHYSICAL METADATA RECEIPT
4. IF NON-DIRECT REALIZATION, VERIFY R35-I02 DERIVATIVE PARENTAGE
5. FREEZE R35-I03 CANONICAL PHYSICAL EXPECTATION FOR EC01/05/07/12/13
6. MATERIALIZE EACH CANDIDATE PHYSICAL REALIZATION
7. RUN SOURCE-INDEPENDENT OWNER REJECTION/POSITIVE TESTS
8. VERIFY A/B/C SHARE ONE OWNER AND ONE BOUNDED-UNKNOWN LAW
9. ISSUE R35-I03 WHOLE-SOURCE PHYSICAL-EQUIVALENCE RECEIPTS IF THE REAL SOURCE COURT PASSES
10. PROCEED TO LATER SEMANTIC/I05/TERMINAL COURTS UNDER THEIR OWN AUTHORITY
```

This commission completed only the contract-authoring portion. It did not execute steps 1-10 against raw source bytes.

## Claim boundary

A future synthetic test PASS would prove only that the source-specific realization law rejects the named semantic mutations.

It would not prove:

- real-source execution;
- whole-source physical equivalence;
- A/B/C source execution;
- I05;
- source certification;
- measured P2X.

Current status remains:

`TESTS_AUTHORED__NOT_EXECUTED`
