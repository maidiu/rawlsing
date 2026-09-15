# RABOCHII — OBL063 CONSUMER AUTHORITY TRACE R1

Repository:
`maidiu/rawlsing`

Worker branch:
`agent/rabochii-obl063-consumer-authority-trace-r1`

Starting HEAD:
`b71784d48f5a64844586cd6b8844cc3f3db71892`

Authorized grain:
`OBL063_EMPIRICAL_CONSUMER_AUTHORITY_TRACE_ONLY`

Purpose:

Determine, from the actual current Rawlsing code and governed PRE553/C05/GSR07 seams, the minimum empirical authority required by each real downstream consumer. This is a bounded dependency trace, not a new audit campaign and not a source-document recovery campaign.

Trace only:

`raw/source-backed empirical objects -> PRE553/C05/GSR07 query/discovery/structural admission -> component/driver/vector-facing consumer seams`

For each actual consumer operation, classify the minimum authority ceiling as one of:

- `SOURCE_IDENTITY_ONLY`
- `SOURCE_LOCAL_CERTIFIED`
- `POPULATION_CERTIFIED`
- `POPULATION_PLUS_RELATION_COMPARABILITY`
- `OPERATION_SPECIFIC_AUTHORITY_REQUIRED`

The worker must distinguish:
- respondent/source-local descriptive structure;
- weighted or estimand-specific population claims;
- cross-country/cross-wave comparisons;
- relation/backfill/harmonization;
- routing/person-position semantics;
- mere provenance/object identity.

Required questions:

1. Is a fully materialized `EmpiricalUniverse@1.0.0` with target+frame+design actually required for every WVS datum to reach downstream runtime?
2. Which exact operations truly require target/frame/design?
3. Which operations can lawfully consume exact source-local respondent distributions without population generalization?
4. Where, if anywhere, does current code conflate object existence with population authority?
5. What is the smallest gate correction needed so documentary incompleteness does not block lawful source-local runtime evidence?
6. Does the existing OBL063 generic runtime contract suffice, or is one additional admission type/seam required?

Hard stops:

- no country-by-country documentary recovery;
- no weakening or rewriting of source facts;
- no HB01/HB05/HB06/HB07/C09 execution;
- no V3/PFF redesign;
- no production driver priors;
- no broad project audit;
- no inference from desired architecture: classify only what actual consumers require.

Required return:

- `RESULT.md`
- `RESULT.json`
- `CONSUMER_AUTHORITY_MATRIX.csv`
- `GATE_CORRECTION.md`
- `CHANGED_FILES.txt`

PASS target:

`OBL063_CONSUMER_AUTHORITY_TRACE_COMPLETE__MINIMUM_AUTHORITY_PER_REAL_CONSUMER_PROVED__D11_GATE_CORRECTION_READY`

Blocker target:

`OBL063_CONSUMER_AUTHORITY_TRACE__EXACT_CONSUMER_SEAM_BLOCKER_PROVED`
