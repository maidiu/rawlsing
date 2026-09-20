# CLOSED35-R2-EVS2008 — Synthetic Test Protocol

## Boundary

Implementation under test:

`rawlsing_next/closed35_evs2008_realization.py`

Synthetic test file:

`rawlsing_next/tests/test_closed35_r2_evs2008_realization.py`

This is a source-independent rejection court. It does not open `EVS 2008.sav`, decode real survey bytes, execute A/B/C, materialize a real whole-source physical-equivalence receipt, run I05, or run measured P2X.

Execution status:

`TESTS_AUTHORED__NOT_EXECUTED`

No browser-side test PASS is claimed.

## T01 — Compatibility-rendered text cannot become semantic authority

Supply readable latin1-rendered text with no admitted producer-documentary entry.

Required:

- result remains `UNKNOWN_PRODUCER_TEXT`;
- compatibility prose cannot become a semantic label.

Then supply an exact ZA4800 v5 documentary entry plus contradictory compatibility prose.

Required:

- producer documentary label/value meaning wins;
- compatibility prose remains irrelevant.

Reject:

`COMPATIBILITY_RENDERED_TEXT_AS_SEMANTIC_AUTHORITY`

## T02 — All thirteen native MR identities must survive

Supply the exact 13-set topology.

Required:

- exact set-name universe;
- exact ordered member lists;
- exact MR-topology digest.

Reject deletion of any native alias identity even when another set has identical members.

Reject:

`MR_FLATTENING`

## T03 — MR overlap cannot collapse native identities

Mutate `vv25` to the full `q5a` membership or `vv43` to full `q5b`.

Required:

- topology validation fails closed.

Mutate `evs_q107` by absorbing a b-side count variable.

Required:

- topology validation fails closed.

Reject:

`MR_OVERLAP_COLLAPSE`

and:

`MR_NONMEMBER_ROLE_ABSORPTION`

## T04 — Rank/order law cannot be invented

Verify:

- Q52 preserves selection cap 5;
- Q52 does not acquire rank significance;
- other MR batteries preserve category order only.

The court must not convert source order into preference rank.

Reject:

`MR_CATEGORY_ORDER_PROMOTED_TO_RANK`

## T05 — MR missing states remain typed and distinct

Verify producer-authorized integrated item states:

- 1 -> mentioned/yes;
- 0 -> not-mentioned/no;
- -1 -> don't know;
- -2 -> no answer;
- -3 -> not applicable;
- -4 -> question not asked/not provided;
- -5 -> other missing.

Required:

- 0 is not collapsed into missing;
- negative missing classes remain distinct;
- undocumented codes remain bounded unknown rather than inferred by analogy.

## T06 — Routing comes from documentary authority, not missingness

Provide physical missingness for a country/set combination with no exact admitted route.

Required:

`BOUNDED_UNKNOWN`

Then resolve a closed producer route while supplying a contradictory nonmissing physical state.

Required:

the documentary route still resolves.

Covered positive documentary examples:

- Q5b Denmark;
- Q6 named non-implementing countries;
- Q6 Finland;
- Q107 Finland;
- Q108 Finland.

Reject:

`ROUTING_INFERRED_FROM_MISSINGNESS`

## T07 — V372 rendered sentinel cannot mint a negative subreason

Supply:

`1582-10-13`

Required exact realization:

`EVS_STANDARDIZED_MISSING__NEGATIVE_SUBCODE_NOT_RECOVERABLE_FROM_DATE_RENDERING`

with:

`UNKNOWN_WITHIN_PRODUCER_NEGATIVE_MISSING_DOMAIN`

Attempt to claim `-4`, or any member of `{-1,-2,-3,-4,-5}`, from the rendered date.

Required:

fail closed.

Reject:

`INVENTED_V372_SUBREASON`

The test does not deny that a later authorized numeric-storage witness could refine the state. It only proves that the inherited date rendering cannot.

## T08 — Documentary release alignment cannot mint a producer checksum

Supply the canonical Rawlsing SHA as a claimed producer-published checksum.

Required:

fail closed.

The admitted law is:

- ZA4800 v5.0.0 = producer documentary release identity;
- Rawlsing SHA = exact internal source-byte identity;
- no public producer file digest was admitted.

Reject:

`PRODUCER_CHECKSUM_CLAIM_FROM_DOCUMENTARY_ALIGNMENT`

## T09 — Exact canonical source root is mandatory

Construct a synthetic incidence with the canonical SHA and accepted physical compatibility configuration.

Required:

admission succeeds at source-specific contract grain.

Mutate source SHA.

Required:

fail closed.

This is not a real-source physical-equivalence test.

## T10 — Reader/config drift fails closed

Synthetic mutations include:

- reader version not 1.3.6;
- UTF-8 execution substituted for the accepted exact-SHA latin1 compatibility path;
- `apply_value_formats=True`;
- semantic authority asserted for the compatibility reader.

Required:

each mutation fails source-specific physical admission.

## T11 — Closed producer flag relations remain scoped

Verify at minimum:

- `f201` scopes to `v201/v202`;
- f201 0 = consistent;
- f201 1 = inconsistent;
- `f180` scopes to `v170-v180`.

Compatibility-rendered misleading text must not override producer documentary relations.

## T12 — Candidate A/B/C semantic divergence fails closed

Create A, B and C bindings to the exact same:

`SOURCE_SPECIFIC_REALIZATION_IDENTITY`

Required:

common identity accepted.

Mutate candidate C to another identity.

Required:

fail closed.

Reject:

`CANDIDATE_SPECIFIC_SEMANTIC_DIVERGENCE`

## T13 — S35/R35 scope is frozen without semantic promotion

Required S35 edge classes:

`EC01; EC02; EC03; EC08; EC14`

Required R35 seams:

- I01 physical metadata;
- I02 derivative parentage where applicable;
- I03 source-scoped whole-source physical equivalence.

Required:

all R35 hooks remain `semantic_authority=false`.

No future physical receipt may substitute for documentary semantic authority, and no browser semantic implementation may substitute for a future physical receipt.

## Later ABC qualification obligations

A later qualified execution line must separately prove:

1. exact canonical source SHA;
2. exact accepted reader/configuration;
3. I01 physical metadata receipt;
4. I02 parentage for any non-direct-raw/persisted derivative;
5. candidate-neutral I03 physical expectation over EC01/02/03/08/14;
6. candidate A physical realization receipt;
7. candidate B physical realization receipt;
8. candidate C physical realization receipt;
9. exact native 13-set MR topology survives each candidate;
10. common `SOURCE_SPECIFIC_REALIZATION_IDENTITY` across A/B/C;
11. later semantic parity/I05 under its own authority.

An I03 PASS, if later obtained, remains:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

## Nonclaims

This authored test court does not establish:

- real source-byte execution;
- whole-source physical equivalence;
- A/B/C execution;
- I05 PASS;
- source certification beyond accepted documentary authority;
- measured P2X.

