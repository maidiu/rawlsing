# PYAT HQ199 — governed source-session/accounting owner — R1

Repository: maidiu/rawlsing

Role: source-free implementation worker — Space Bunny

Branch:
agent/rabochii-pyat-hq199-r1

Implementation base / accepted repaired broker candidate:
4b6335ca5fc485108b0ffb1d682a29a02e1eee51

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ199-R9-GOVERNED-SOURCE-SESSION-OWNER-R1/
- /WORKER_RETURNS/PYAT-HQ199-R9-GOVERNED-SOURCE-SESSION-OWNER-R1/
- /rawlsing_next/
- /WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/
- /WORKER_RETURNS/EE-P2R6S/
- /WORKER_RETURNS/FIABC-LM2/

Do not clone the repository. Do not create a full checkout.

The exact startup SHA is the commission-tip SHA after this file is committed.

## Mission

Implement the generic execution owner needed by HQ199 without hardcoding the seven source-specific plans.

Current accepted broker scope is one _decode() call. R9 needs an explicit per-source execution owner whose lifecycle and aggregate accounts exist above individual reader calls.

Close the mechanism gaps:

- GOV-SCOPE-001 — no per-source execution/session owner;
- GOV-DEC-003 — no decoder_invocations account;
- generic mechanism needed for GOV-HDR-002 — operation plan must explicitly admit or forbid header-prefix access.

Do NOT decide the frozen SRC27 "multiple path opens" interpretation in this lane.
Do NOT hardcode source-specific budgets or plans that the documentary lanes have not adjudicated.

## Required generic owner

Introduce the smallest explicit source-execution/session abstraction, naming may vary but the semantics must be exact.

It must own:

- source entry key supplied by caller;
- path;
- expected SHA-256;
- source format;
- reader encoding/config;
- one SourceAccessBroker lifecycle;
- one operation plan;
- aggregate source-access receipt;
- decoder_invocations account;
- deterministic close lifecycle.

The owner must be created once for a caller-bound source entry and reused for every admitted operation in that scope.

A second decoder entry must be rejectable PRE-OPERATION when decoder_invocations is capped at 1.

reader_invocations and decoder_invocations remain separate accounts.

## Generic operation plan

Implement a typed generic plan. Do not embed SRC02/SRC06/etc constants.

It must be able to express at minimum:

- METADATA_ONLY
- SELECTED
- FULL
- CHUNKED_FULL / streaming full-row mode if needed by existing compatibility behavior
- selected variable names + bound ordinals where applicable
- header_prefix_bytes = integer or NONE
- encoding independent of row-data mode
- retry ceiling
- full-route/pass token only as a separately typed outer account if represented

Key correction:
encoding being non-null must NOT by itself force a full row-data read.

A METADATA_ONLY plan with a declared encoding must perform metadata admission and zero full/selected row-data reads.

A SELECTED plan must perform metadata binding + exactly the selected reader invocation and may perform zero header-prefix reads when the plan does not admit one.

A FULL plan may perform a full reader invocation without being confused with CHUNKED_FULL.

Header-prefix access must occur only when the plan explicitly admits a prefix size.

## Decoder integration

Refactor the decoder narrowly so the governed-session path uses the session-owned broker rather than constructing a new broker inside each decode.

Preserve the accepted one-open broker properties.

Legacy decoder APIs may remain for existing source-free compatibility, but:
- the governed-session path must be explicit;
- there must be no hidden raw-path fallback;
- the session-owned broker must be the account owner on the governed path.

PhysicalSourceIncidence.source_access_receipt must remain live/complete.

close_source_access() should close the session/broker safely.

Prefer context-manager support and deterministic cleanup on success and exception paths.

## New accounting

Add decoder_invocations to:
- SourceAccessAccount;
- SourceAccessBudget;
- receipt measurement basis;
- pre-operation budget checks.

Increment it once at the decoder/session entry boundary, not once per reader call.

Second decode with max decoder_invocations=1 must refuse before metadata/hash/row operations of the second decode.

Do not rename reader_invocations.

## Source-free courts

Add focused courts proving:

1. one session owns one physical open across all operations in one decode;
2. decoder_invocations=1 after one decode;
3. max1 rejects second decode before any second source operation;
4. METADATA_ONLY + non-null encoding => metadata read 1, selected 0, full 0;
5. SELECTED => selected 1, full 0;
6. FULL => full 1 and is distinct from chunk_reads;
7. CHUNKED_FULL remains separately accounted if supported;
8. header_prefix_bytes=None => zero prefix reads;
9. explicit prefix 176 => one prefix operation / 176 bytes on a suitable synthetic SAV;
10. deterministic close on normal and exceptional paths;
11. reader_bytes limiter remains intact;
12. no raw path reaches pyreadstat.

Do not assert source-specific plan truth in this lane.

## Exact requalification

Because production blobs change, rerun the fixture-complete exact R7 court:

Interpreter:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

Environment:
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<worktree root>

pytest:
-p no:cacheprovider

Exact six files:
- rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py
- rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py
- rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py
- rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py
- rawlsing_next/tests/test_r35_i01_physical_metadata.py
- rawlsing_next/tests/test_pre553_source_backed_c11_facade.py

Collect exactly 55; run twice; target 55/55 twice.

Also rerun the broker/session courts.

## Write terrain

Only:
- rawlsing_next/pre553_source_access_broker.py
- rawlsing_next/pre553_physical_decoder.py
- one narrowly scoped new rawlsing_next/pre553_*source_session*.py module if needed
- rawlsing_next/tests/**
- WORKER_RETURNS/PYAT-HQ199-R9-GOVERNED-SOURCE-SESSION-OWNER-R1/**

No other production files without STOP/HQ recommission.

## Allowed dispositions

Exactly one:
- GOVERNED_SOURCE_SESSION_CANDIDATE_READY_FOR_INDEPENDENT_REVIEW
- SESSION_OWNER_MECHANISM_PARTIAL
- R7_REQUALIFICATION_FAILURE
- MATERIAL_NEW_COUNTEREXAMPLE
- CHECKOUT_MODE_INSUFFICIENT__HQ_RECOMMISSION_REQUIRED

No self-adoption.

Commit, push, re-fetch, verify.

Terminal:
HQ199_R9_GOVERNED_SOURCE_SESSION_RETURNED__HQ_REVIEW_REQUIRED

No real survey-source access, locator discovery, warrant issuance, live C4, C7, or actor/person work.
