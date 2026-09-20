# CLOSED35-R1-EVS1999 — Synthetic Test Protocol

## Boundary

This court is source-independent.

It does not open EVS 1999.sav, execute the source, decode real source bytes, materialize a real C11 release, or run measured P2X.

Test file:

rawlsing_next/tests/test_closed35_r1_evs1999_realization.py

Implementation under test:

rawlsing_next/closed35_evs1999_realization.py

## Test obligations

### T01 — malformed label cannot become semantic authority

Feed a readable compatibility-rendered string with no producer documentary entry.

Required result:

DOCUMENTARY_ALIGNMENT_UNKNOWN

The compatibility string must have no effect on semantic output.

### T02 — producer document overrides readable compatibility garbage

Supply:

- exact variable identifier v49_filt;
- a producer ZA3811 v3.0.0 documentary entry;
- an exact raw-value dictionary entry;
- contradictory/readable compatibility prose.

Required result:

semantic label and value meaning come from the producer documentary entry only.

### T03 — unresolved documentary label remains unknown

Supply an exact producer variable entry whose requested semantic label remains unresolved.

Required result:

DOCUMENTARY_ALIGNMENT_UNKNOWN

No compatibility fallback.

### T04 — exact identifier law

Supply documentary authority for v49_filt but request v49.

Required result:

DOCUMENTARY_ALIGNMENT_UNKNOWN

No fuzzy or neighboring-variable join.

### T05 — routing is documentary, not physical missingness

Give an undocumented variable a physical missing-state token.

Required result:

DOCUMENTARY_ALIGNMENT_UNKNOWN

Then resolve v49_filt with the admitted RT002 documentary rule while giving a nonmissing physical state.

Required result:

DOCUMENTARY_ROUTING_RESOLVED through ZA3811 v3.0.0 authority.

### T06 — release-specific routing precedence

Provide a Master default and a ZA3811 v3.0.0 release-specific rule for the same exact field.

Required result:

release-specific producer rule wins.

### T07 — compatibility execution cannot change the source root

Construct a synthetic incidence with:

- exact EVS1999 canonical SHA;
- pyreadstat 1.3.6;
- explicit latin1 compatibility;
- user_missing=True;
- apply_value_formats=False.

Required result:

admitted source SHA remains the exact canonical root and compatibility_semantic_authority=False.

Mutating the source SHA must fail closed.

### T08 — reader/config drift fails closed

Mutations tested:

- wrong pyreadstat version;
- UTF-8 execution substituted for accepted latin1 compatibility;
- apply_value_formats=True.

Each must fail source-specific physical admission.

### T09 — A/B/C share one semantic realization law

Create CandidateSemanticBinding objects for exact A, B and C.

Required result:

all share SOURCE_SPECIFIC_REALIZATION_IDENTITY.

Mutate C to a different realization identity.

Required result:

semantic realization divergence fails closed.

### T10 — exact physical edge/hook scope remains frozen

Required exact S35 edge set:

EC01; EC02; EC03; EC10; EC14

Required R35 seams:

- I01 physical metadata;
- I02 derivative parentage for non-direct-raw realizations;
- I03 candidate-neutral physical scope/equivalence.

All must remain semantic_authority=False.

## Qualification extensions

This synthetic court proves the source-specific law only.

Later ABC qualification must additionally execute, under the accepted R35 generic implementation line:

1. exact canonical raw SHA verification;
2. exact reader/config identity freeze;
3. R35-I01 physical metadata receipt;
4. R35-I02 derivative-parentage receipts for any non-direct-raw A/C path or other persisted derivative;
5. R35-I03 canonical expectation over EC01/02/03/10/14;
6. candidate A physical realization receipt;
7. candidate B physical realization receipt;
8. candidate C physical realization receipt;
9. common SOURCE_SPECIFIC_REALIZATION_IDENTITY across A/B/C;
10. downstream common PRE553 source-backed C11 semantic owner.

No semantic PASS may substitute for a failed physical receipt.

No physical PASS may promote compatibility text into semantics.

## Execution status

The source-independent tests were added but not executed by this browser/GitHub worker.

That is deliberate: this commission prohibits real-source execution and measured P2X, and the acceptance target here is implementation readiness for later ABC qualification rather than a claimed execution receipt.

A later source-independent CI/qualification lane may run:

pytest -q rawlsing_next/tests/test_closed35_r1_evs1999_realization.py

The real EVS 1999 source must not be introduced into this synthetic test file.
