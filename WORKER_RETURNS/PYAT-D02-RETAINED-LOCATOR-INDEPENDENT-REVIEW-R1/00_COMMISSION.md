# PYAT D02 — CORRECTED RETAINED LOCATOR INDEPENDENT REVIEW — R1

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Independent Browser/GitHub documentary reviewer, GPT-5.6 Sol High

Branch:
`agent/reviewer-pyat-hq134-d02-retained-locator-r1`

Exact base / corrected archaeology return:
`bb4db6c5131be50fded8d91961ee81683459e22e`

Original archaeology commission:
`57d7ee585f7364383394d067c6aeb871470edda4`

Do not access raw survey files.
Do not use the user's Mac.
Review only.

## Corrected worker disposition

`EXACT_RETAINED_D02_LOCATOR_RECOVERED`

Claimed resolved blocker:

`C2-02-BLOCK-D02-LOCATOR-001`

Source:

- SRC14
- `EVS 2008.sav`
- SHA-256 `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`

## Mission

Independently verify whether the corrected archaeology return is competent to close the D02 locator blocker for later C4 preparation.

The decisive claimed retained witness is:

- branch/tip: `agent/vozhd-trii-srcprep71-r04-evs` @
  `3bc063aa7bf461caf5baf581ff32a434ba9e09a3`
- commit time: `2026-08-22T10:03:56Z`
- path:
  `data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SOURCE_CERT_PREP71/RETURNS/R04/HOSTILE_FIXTURES.csv`
- blob:
  `12f6adb77ef5692511055c8f0520e42c454f3867`

Claimed exact row:

- fixture id: `EVS08_DATE_MISSING_V372`
- physical variable: `v372`
- source variable ordinal: `466`
- fixture kind: `VARIABLE_MISSING_DECLARATION`
- witness class: `TYPED_DATE_USER_MISSING_SENTINEL`
- rendered witness: `1582-10-13`
- rows: `66280`
- ordinary present: `64363`
- system missing: `0`
- user missing: `1917`
- exact source SHA:
  `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`
- authority basis:
  `SOURCE_PHYSICAL_OR_READER_METADATA_AUTHORITY__NON_SEMANTIC`

## Required checks

### A. Correction scope

Compare provisional archaeology head:

`e8d43c4769371b2d68ea73429fe595732ef6ef60`

to corrected head:

`bb4db6c5131be50fded8d91961ee81683459e22e`

Require that only the five commissioned archaeology return artifacts changed.

### B. Exact decisive fixture

Read the immutable PREP71 fixture at the exact historical tip.

Verify the exact row itself—not merely the corrected worker's paraphrase—binds:

- exact source SHA;
- `v372`;
- ordinal `466`;
- `TYPED_DATE_USER_MISSING_SENTINEL`;
- rendered `1582-10-13`;
- 1917 user-missing;
- 64363 ordinary-present;
- 0 system-missing;
- 66280 rows;
- nonsemantic physical/reader-metadata authority.

Verify exact blob identity.

### C. Chronological independence

Verify the decisive fixture commit predates C4 preparation and the current D02 archaeology.

The purpose is to establish that the locator was retained independently and was not selected after consulting future C4 candidate output.

### D. Provenance competence

Review whether PREP71's fixture is competently derived from accepted SR03 physical/source-native work.

Where helpful, independently inspect corroborating pre-C4 artifacts:

- CLOSED35-L2-EVS2008 tip
  `dd17c06606709bad5e56189a21db729cdd6ca859`
- CLOSED35-L2R-EVS2008 tip
  `3201d94156742870562c6f98c239673a1a6ef2ba`
- CLOSED35-R2-EVS2008 tip
  `6f9dbb1f3cdc0fc2ec92d5705a43b353b7b56594`

Do not treat later corroboration as the origin of the locator if the August fixture already suffices.

### E. Physical-versus-semantic boundary

Verify that the locator does not depend on interpreting what `v372` means.

The review must preserve:

- rendered `1582-10-13` is a physical typed-date sentinel, not a substantive date claim;
- no negative missing-reason code may be invented;
- historical evidence does not prove whether the current Python object is specifically `datetime.date` versus `datetime.datetime`;
- later C4 may only require the frozen `v372` witness to enter one of the accepted C3 D02 naive date/time carrier paths and must record/fail closed on mismatch.

### F. C3 binding

Verify accepted C3 integration:

`30686b185d4ceb2c94f61815ef70d8c8e76255d6`

supplies the generic source-free D02 behavior needed to consume the recovered source-bound witness without adding new semantic authority.

### G. AT20 / C2 blocker effect

Determine whether this retained pre-C4 locator is sufficient to close:

`C2-02-BLOCK-D02-LOCATOR-001`

under the independently approved C2-02 rule allowing either:

1. exact immutable retained locator + sufficient physical/native witness class; or
2. deterministic traversal oracle.

If the locator path is competent, explicitly state that the traversal-oracle route is unnecessary and that no new D02 source scan is needed merely to establish the expected witness.

Approval still does NOT authorize raw source execution or C4 execution.

## Return terrain

Write only:

`WORKER_RETURNS/PYAT-D02-RETAINED-LOCATOR-INDEPENDENT-REVIEW-R1/**`

Required:

- `00_REVIEW.md`
- `01_EXACT_FIXTURE_AUDIT.json`
- `02_PROVENANCE_AND_INDEPENDENCE_AUDIT.json`
- `03_AUTHORITY_BOUNDARY_AND_C4_EFFECT.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:

- `APPROVE_AT_DECLARED_GRAIN`
- `CHANGES_REQUIRED`
- `TYPED_RESIDUAL`
- `ESCALATE_WITH_COUNTEREXAMPLE`

Terminal:

`D02_RETAINED_LOCATOR_INDEPENDENT_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
