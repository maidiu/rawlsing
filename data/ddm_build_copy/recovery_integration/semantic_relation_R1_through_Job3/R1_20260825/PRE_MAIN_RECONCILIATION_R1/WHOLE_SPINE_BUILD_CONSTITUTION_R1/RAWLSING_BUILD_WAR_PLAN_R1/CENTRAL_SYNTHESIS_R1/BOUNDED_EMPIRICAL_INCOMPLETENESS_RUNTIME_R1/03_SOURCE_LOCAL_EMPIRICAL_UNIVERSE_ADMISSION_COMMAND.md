# RABOCHII — SOURCE-LOCAL EMPIRICAL UNIVERSE ADMISSION R1

Repository:
`maidiu/rawlsing`

Worker branch:
`agent/rabochii-source-local-empirical-universe-admission-r1`

Starting HEAD:
`65de916d255958e3e858d4c426cc01552be8ebe4`

Authorized grain:
`SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1_ONLY`

Parent proof:
`WORKER_RETURNS/OBL063_CONSUMER_AUTHORITY_TRACE_R1/`

## Confirmed production-surface holding

A full current production-code trace found no downstream production consumer reading:

- `target_population_and_sample_frame`
- `sampling_design_regime`
- `sampling_geography`
- `country_geography`
- `field_or_reference_time`
- `canonical_wave_if_governed`
- `harmonization_authority_ref`

except the `EmpiricalUniverse` field declaration and source-local universe producers.

Existing Afrobarometer R5 producers already materialize:

`target_population_and_sample_frame = SOURCE_NATIVE_R5_SAMPLE_FRAME__NO_POPULATION_GENERALIZATION_BY_GT12`

and

`sampling_design_regime = SOURCE_NATIVE_R5__RAW_UNWEIGHTED_GT12_USE`.

Therefore source-local universe admission is an existing architectural pattern to generalize, not a new weakening of authority.

## Mission

Implement the smallest reusable PRE553 contract that can materialize an exact `EmpiricalUniverse@1.0.0` for source-local empirical use when source/replay/respondent identity is exact but population target/frame/design is not fully certified.

Do not create a new public ontology family.

Do not alter `EmpiricalUniverse@1.0.0` schema.

Do not erase known documentary content.

## Required claim ceilings

Every source-local admission must carry these exact negative limits:

- `NO_POPULATION_GENERALIZATION`
- `NO_WEIGHTED_POPULATION_ESTIMAND_UNLESS_SEPARATELY_AUTHORIZED`
- `NO_CROSS_UNIVERSE_POOLING_WITHOUT_RELATION_AUTHORITY`
- `NO_NEAREST_COUNTRY_OR_WAVE_BACKFILL`

The negative-limit refs must be deterministic exact refs and must be present in the source-local admission authority snapshot.

## Required source-local authority

The contract must require a positive exact admission `AuthoritySnapshot@1.0.0` whose:

- authority kind is `SOURCE_SEMANTICS_TOPOLOGY`;
- governed operation includes exactly `SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1`;
- governed object family includes `EmpiricalUniverse@1.0.0`;
- scope binds the exact source artifact ref and exact respondent/replay scope refs;
- negative-limit refs include all four required limits;
- dependency closure includes the exact source/replay/respondent determinants.

The contract may validate such an authority. It must not synthesize positive source authority from filenames, country labels, incidence, or observed values.

## Materialization law

The materializer may preserve positive documentary target/frame/design content if supplied as governed source material.

Where any population/documentary field is not certified, it must use explicit typed semantic material such as:

`{"state":"NOT_POPULATION_CERTIFIED","claim_ceiling":"SOURCE_LOCAL_ONLY",...}`

not an invented population description.

The resulting universe:

- is `UNIVERSE_IDENTIFIED`;
- has exact raw source identity;
- has exact respondent namespace/replay provenance;
- is valid for source-local admission only;
- does not thereby authorize weighted population estimation, population claims, source pooling, backfill, or harmonization.

## Required guards

Implement helpers sufficient to reject:

1. admission authority without exact source dependency;
2. admission authority without exact respondent/replay dependency;
3. missing required negative limit;
4. non-ALLOW authority;
5. wrong authority kind;
6. wrong governed operation;
7. wrong governed object family;
8. population-certified claim asserted from source-local authority alone;
9. weighted population use asserted from source-local authority alone;
10. cross-universe pooling asserted from source-local authority alone;
11. nearest-country/wave backfill asserted from source-local authority alone;
12. invented target/frame/design content supplied as if certified without exact documentary authority;
13. mutation of source/ref/negative limits without identity drift;
14. source-local universe reload/replay mismatch.

## Preservation law

Known population/documentary material is not deleted. The contract must allow it to be carried as documentary material with an explicit certification state.

A later population-certification overlay may positively authorize population use without requiring the source-local empirical evidence itself to be regenerated from raw source bytes.

## Required files

At minimum:

- `rawlsing_next/pre553_source_local_universe_admission.py`
- `rawlsing_next/tests/test_pre553_source_local_universe_admission.py`
- return `RESULT.md`
- return `RESULT.json`
- `CHANGED_FILES.txt`

PASS target:

`SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1_COMPLETE__SOURCE_LOCAL_RAW_SCOPE_MATERIALIZABLE__POPULATION_LIMITS_PRESERVED__READY_FOR_INDEPENDENT_HOSTILE_REVIEW`

Blocker target:

`SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1__EXACT_BLOCKER_PROVED`
