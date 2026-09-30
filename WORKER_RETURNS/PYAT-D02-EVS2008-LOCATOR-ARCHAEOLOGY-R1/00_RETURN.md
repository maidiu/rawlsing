# PYAT D02 — EVS 2008 RETAINED LOCATOR ARCHAEOLOGY — R1

Disposition:

`EXACT_RETAINED_D02_LOCATOR_RECOVERED`

Blocker:

`C2-02-BLOCK-D02-LOCATOR-001`

Source:

- source id: `SRC14`
- file: `EVS 2008.sav`
- SHA-256: `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`

No raw EVS-2008 SAV bytes were opened, materialized, downloaded, decoded, inspected, or inferred from in this lane. The user's Mac was not used. The Library copy was observed only as a Library directory entry; it was not read.

## Holding

The blocker is resolved at the exact commissioned documentary grain.

The project already retained, before future C4, a competent exact physical D02 witness for EVS 2008:

- physical variable: `v372`;
- exact source variable ordinal: `466`;
- physical fixture id: `EVS08_DATE_MISSING_V372`;
- fixture kind: `VARIABLE_MISSING_DECLARATION`;
- exact sufficient D02 witness class: `TYPED_DATE_USER_MISSING_SENTINEL`;
- exact retained rendered witness: `1582-10-13`;
- accepted user-missing cardinality: `1917`;
- accepted ordinary-present cardinality: `64363`;
- accepted system-missing cardinality: `0`;
- accepted source rows: `66280`;
- exact source SHA-256: `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`.

This is not a locator inferred from questionnaire semantics. It is frozen in a source-physical hostile fixture whose authority basis is explicitly:

`SOURCE_PHYSICAL_OR_READER_METADATA_AUTHORITY__NON_SEMANTIC`.

The fixture predates C4 by more than a month.

## Decisive retained physical witness

Immutable worker branch:

`agent/vozhd-trii-srcprep71-r04-evs`

Immutable branch tip:

`3bc063aa7bf461caf5baf581ff32a434ba9e09a3`

Commit date:

`2026-08-22T10:03:56Z`

Retained file:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SOURCE_CERT_PREP71/RETURNS/R04/HOSTILE_FIXTURES.csv`

Git blob:

`12f6adb77ef5692511055c8f0520e42c454f3867`

The exact EVS-2008 row is:

- fixture id: `EVS08_DATE_MISSING_V372`;
- source SHA: exact commissioned SHA;
- fixture class: `VARIABLE_MISSING_DECLARATION`;
- ordinal: `466`;
- variable: `v372`;
- physical class: `TYPED_DATE_USER_MISSING_SENTINEL`;
- missing range: `lo=1582-10-13, hi=1582-10-13`;
- physical counts:
  - rows seen = `66280`;
  - ordinary present = `64363`;
  - system missing = `0`;
  - user missing = `1917`;
  - native rendered user-missing witness `1582-10-13` = `1917`;
- semantic interpretation at that physical court: explicitly unresolved;
- authority basis: source physical / reader metadata, nonsemantic.

That row was prepared from the already accepted SR03 source-physical manifest, not from future C4 output.

## Provenance chain

The physical witness is independently corroborated by later pre-C4 retained archaeology without changing its physical authority.

### CLOSED35-L2-EVS2008

Branch tip:

`dd17c06606709bad5e56189a21db729cdd6ca859`

Commit date:

`2026-09-20T18:13:31Z`

Its return states that accepted physical evidence has `v372` as a **typed user-missing date** rendered `1582-10-13`, affecting exactly `1917` records, under the same canonical source SHA.

### CLOSED35-L2R-EVS2008

Branch tip:

`3201d94156742870562c6f98c239673a1a6ef2ba`

Commit date:

`2026-09-20T18:47:18Z`

Its immutable V372 authority freezes:

- physical variable `v372`;
- source ordinal `466`;
- rendered physical user-missing witness `1582-10-13`;
- user-missing count `1917`;
- ordinary-present count `64363`;
- source rows `66280`;
- exact source SHA.

It additionally proves that the rendered date must not be promoted into an invented substantive date or a guessed missing-reason code.

### CLOSED35-R2-EVS2008

Branch tip:

`6f9dbb1f3cdc0fc2ec92d5705a43b353b7b56594`

Commit date:

`2026-09-20T19:20:07Z`

Its source-specific realization retains the same locator/count/ordinal and reader boundary. It explicitly did not open or execute the raw source.

## D02 type-law binding

Accepted C3 integration:

`30686b185d4ceb2c94f61815ef70d8c8e76255d6`

defines the generic source-free D02 carrier law for exact built-in naive:

- `datetime.datetime`;
- `datetime.date`;
- `datetime.time`;

with timezone-aware datetime/time failing closed.

The historical EVS witness does **not** retain a literal Python `type(value).__name__` that would justify choosing `datetime.date` versus `datetime.datetime` in advance. It instead retains the stronger-for-this-purpose source-bound physical class:

`TYPED_DATE_USER_MISSING_SENTINEL`

together with an exact column locator, exact rendered witness and exact cardinality.

Under the commission's competence law—"expected physical/native type or exact sufficient D02 witness class"—that is sufficient to predeclare the D02 real-source witness without inventing a Python subclass.

Future C4 must therefore **not** claim that historical evidence proves a particular built-in subclass. It must require the current decoder's value at the frozen `v372` witness to enter the accepted D02 date/time carrier path and fail closed if it does not.

## Library custody finding

The Project Library contains:

`/Rawlsing/EVS 2008.sav`

The SAV itself was not opened or materialized. Its Library presence was used only to confirm custody terrain and to search adjacent retained documentary artifacts. The decisive locator authority remains the immutable Git physical fixture above.

Library search also surfaced retained September EVS-2008 documentary commissions that pointed back to the already existing Git branches. Those branches were then read directly and immutably.

## Why this is not semantic inference

The decisive locator existed before the later documentary finding that `v372` means "date of interview."

The locator is therefore not being selected because of that meaning.

The chronological and authority chain is:

`SR03 exact-source physical census -> PREP71 source-physical hostile fixture EVS08_DATE_MISSING_V372 -> later L2/L2R documentary interpretation -> future C4`

Only the first two links are necessary to locate D02.

The later documentary work is corroboration and a negative semantic guard.

## C4 predeclaration now available

A future governed C4 D02 check may predeclare, before opening the source:

1. source SHA exactly `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`;
2. physical column `v372`, ordinal `466`;
3. expected physical class `TYPED_DATE_USER_MISSING_SENTINEL`;
4. exact retained rendered witness `1582-10-13`;
5. expected user-missing cardinality `1917`;
6. expected ordinary-present cardinality `64363`;
7. expected total rows `66280`;
8. expected D02 behavior: current decoder must preserve the located decoder-native date/time object through the accepted opaque D02 carrier law, without semantic stringification;
9. any source SHA, column identity/ordinal, physical class, cardinality, or carrier mismatch fails closed.

No whole-source traversal oracle is needed once this exact retained locator is admitted.

## Correction to the provisional archaeology return

The earlier provisional return on this branch reported no competent locator because the initial Git search had not yet traversed the older PREP71 EVS worker branch, and the Library path had not yet been supplied.

That conclusion is superseded by this corrected return.

`C2-02-BLOCK-D02-LOCATOR-001` is resolved by retained pre-C4 evidence.

`D02_EVS2008_LOCATOR_ARCHAEOLOGY_RETURNED__HQ_ADJUDICATION_REQUIRED`
