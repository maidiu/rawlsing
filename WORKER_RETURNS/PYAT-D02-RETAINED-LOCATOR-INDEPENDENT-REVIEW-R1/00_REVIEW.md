# PYAT D02 — CORRECTED RETAINED LOCATOR INDEPENDENT REVIEW — R1

Disposition:

`APPROVE_AT_DECLARED_GRAIN`

Reviewed corrected archaeology head:

`bb4db6c5131be50fded8d91961ee81683459e22e`

Reviewed blocker:

`C2-02-BLOCK-D02-LOCATOR-001`

Source:

- `SRC14`
- `EVS 2008.sav`
- SHA-256 `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`

No raw SAV was opened, materialized, downloaded, decoded or inspected. C4 was not executed. The user's Mac was not used.

## Review holding

The corrected archaeology return is competent to close the D02 locator blocker at the exact declared grain.

The decisive August PREP71 fixture independently freezes, before the current C4 proving-workload preparation and before the D02 archaeology:

- source SHA `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`;
- physical variable `v372`;
- source variable ordinal `466`;
- fixture `EVS08_DATE_MISSING_V372`;
- fixture kind `VARIABLE_MISSING_DECLARATION`;
- physical class `TYPED_DATE_USER_MISSING_SENTINEL`;
- rendered physical witness `1582-10-13`;
- `1917` user-missing records;
- `64363` ordinary-present records;
- `0` system-missing records;
- `66280` total rows;
- authority basis `SOURCE_PHYSICAL_OR_READER_METADATA_AUTHORITY__NON_SEMANTIC`.

The immutable PREP71 fixture is at:

- branch `agent/vozhd-trii-srcprep71-r04-evs`;
- tip `3bc063aa7bf461caf5baf581ff32a434ba9e09a3`;
- commit time `2026-08-22T10:03:56Z`;
- path `data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SOURCE_CERT_PREP71/RETURNS/R04/HOSTILE_FIXTURES.csv`;
- blob `12f6adb77ef5692511055c8f0520e42c454f3867`.

The exact row itself was read and matches the corrected archaeology claim.

## A. Correction scope

PASS.

Comparing provisional archaeology head:

`e8d43c4769371b2d68ea73429fe595732ef6ef60`

to corrected head:

`bb4db6c5131be50fded8d91961ee81683459e22e`

shows exactly five modified files, all inside:

`WORKER_RETURNS/PYAT-D02-EVS2008-LOCATOR-ARCHAEOLOGY-R1/`

and exactly the five commissioned return artifacts:

- `00_RETURN.md`
- `01_SEARCH_AND_CUSTODY_AUDIT.json`
- `02_LOCATOR_OR_TRAVERSAL_EVIDENCE.json`
- `03_C4_BINDING_EFFECT.json`
- `04_FINAL_DISPOSITION.json`

No unrelated repository file changed in the correction.

## B. Exact decisive fixture

PASS.

The immutable CSV row at the exact historical tip directly contains the claimed source SHA, fixture identity, `v372`, ordinal `466`, physical class, rendered sentinel, and all four count facts.

The fetched file's Git blob is exactly:

`12f6adb77ef5692511055c8f0520e42c454f3867`

matching the corrected archaeology claim.

The row's authority is explicitly nonsemantic:

`SOURCE_PHYSICAL_OR_READER_METADATA_AUTHORITY__NON_SEMANTIC`

and its assertion scope is:

`PHYSICAL_MISSINGNESS_ONLY`.

Its documentary field says only:

`semantic_reason_for_1582_10_13 = UNKNOWN_PENDING_DOCUMENTARY_AUTHORITY`.

That is a strong negative guard against silently converting the retained sentinel into survey meaning.

## C. Chronological independence

PASS.

The decisive PREP71 fixture tip was sealed on:

`2026-08-22T10:03:56Z`.

The current C2-02 C4 proving-workload commission was issued only on:

`2026-09-30T04:04:23Z`

at `440e0a600f66103aad6076979cb23209f0a0ae4a`.

Its worker return followed at:

`2026-09-30T04:26:59Z`

at `6f6ab9dfe5ad8f9359630dd05abf43c3fd11a1b5`.

The D02 archaeology commission itself was issued later still, on:

`2026-09-30T07:47:09Z`.

The corrected archaeology head was sealed at:

`2026-09-30T14:47:47Z`.

The governing C4 dossier remains `DRAFT__NOT_DISPATCHED__ISSUANCE_REQUIRES_EXACT_SCOPE`; no C4 execution output exists from which the August locator could have been selected.

The competent independence claim is therefore exact: the August physical witness predates the current C2-02 C4 proving-workload preparation, the blocker discovery, the archaeology, and any C4 execution. This review does not need to claim that it predates every earlier abstract mention of a future C4 phase.

## D. Provenance competence

PASS.

The PREP71 source-certification packet explicitly anchors EVS 2008 to:

`accepted SR03 physical manifest`

and records the exact source as `66280 x 477` under the exact SHA and governed reader boundary.

The PREP71 common packet contract required:

`source SHA -> decoder/config -> hostile physical fixtures -> metadata/topology fixtures -> documentary semantic assertions -> ...`

and required physical facts to be separated from documentary semantics.

The accepted SR03 adjudication states that all 35 manifests were produced from exact frozen SHA-256 source bytes, that no source was substituted, that row/cell conservation passed, and that SR03 is a physical source census rather than semantic certification.

PREP71 also records that its browser environment lacked pyreadstat and therefore used the accepted SR03 manifests rather than introducing a substitute SAV reader. This strengthens, rather than weakens, the custody chain for the retained fixture.

Later CLOSED35-L2/L2R/R2 EVS2008 artifacts corroborate the same locator/count geometry, but they are not needed as the origin of the locator.

## E. Physical-versus-semantic boundary

PASS.

The locator is competent without knowing what `v372` means.

The decisive physical fixture already names `v372` and ordinal `466` and classifies the state as `TYPED_DATE_USER_MISSING_SENTINEL` while explicitly leaving the semantic reason unknown.

Therefore:

- `1582-10-13` is a retained physical typed-date rendering, not a substantive interview-date claim;
- no `-1` through `-5` missing-reason code is recoverable from this retained rendering alone;
- no semantic interpretation of `v372` is needed to choose the locator;
- later producer documentation may constrain meaning but is not the source of the physical locator.

## F. C3 binding

PASS.

Accepted C3 integration:

`30686b185d4ceb2c94f61815ef70d8c8e76255d6`

contains the source-free D02 owner:

- exact built-in naive `datetime.datetime` -> opaque `python.datetime.datetime@1`;
- exact built-in `datetime.date` -> opaque `python.datetime.date@1`;
- exact built-in naive `datetime.time` -> opaque `python.datetime.time@1`;
- timezone-aware datetime/time -> fail closed.

The accepted physical decoder additionally unwraps `.item()` and routes an exact supported built-in date/time object through the same normalization.

Independent C3 integration review at:

`462e6bf1ed514056f9316dad761054e690a7755d`

approved `D02_opaque_decoder_native_datetime_law` at declared grain with zero raw survey access.

Historical retained evidence does **not** prove whether the current native object is specifically `datetime.date` or `datetime.datetime`. That is not a defect in the locator oracle because the pre-C4 expected class can be frozen as:

`TYPED_DATE_USER_MISSING_SENTINEL + accepted C3 naive date/time carrier domain`.

Future C4 must record the actually observed exact current subclass and fail closed if it is not one of the accepted C3 classes or if the frozen witness otherwise mismatches.

## G. AT20 / C2 blocker effect

PASS.

AT20 requires the source/authority/workload to be frozen before oracle materialization, oracle identity to be frozen before execution, and candidate output not to define expected truth.

The independently approved C2-02 review made the D02 wake law explicit:

1. recover/freeze from competent retained evidence an exact immutable physical locator plus expected native-type/carrier witness; or
2. independently freeze a deterministic whole-source traversal oracle before C4 source execution.

The August PREP71 fixture satisfies path 1.

It freezes the exact source, exact column, exact ordinal, sufficient physical typed-date witness class, exact rendered sentinel and exact expected occurrence cardinality independently of future C4 output. C3 separately freezes the only accepted current decoder-native carrier domain.

Accordingly:

`C2-02-BLOCK-D02-LOCATOR-001 = CLOSED_AT_DECLARED_GRAIN`.

The traversal-oracle route is unnecessary.

No new D02 source scan is needed merely to establish the expected witness.

This approval does **not** authorize raw source access, C4 execution, production mutation, semantic expansion, or any other independent C4 prerequisite.

## Final disposition

`APPROVE_AT_DECLARED_GRAIN`

`D02_RETAINED_LOCATOR_INDEPENDENT_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
