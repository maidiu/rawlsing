# PYAT HQ199 — R9 scope and operation-plan independent review — R1

Repository: maidiu/rawlsing

Role: independent documentary/source-free reviewer
Preferred model: DeepSeek V4.1 Flash

Branch:
agent/reviewer-pyat-hq199-r1

Documentary base:
dbf3287084b547226a401fd0bde2da46610f2b9b

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ199-R9-SCOPE-AND-OPERATION-PLAN-INDEPENDENT-REVIEW-R1/
- /WORKER_RETURNS/PYAT-HQ199-R9-SCOPE-AND-OPERATION-PLAN-INDEPENDENT-REVIEW-R1/
- /PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ199_R9_SCOPE_OWNER_ADJUDICATION_R1.md

Read code/authority through exact Git objects. Do not clone or create a full checkout.

The exact startup SHA is the commission-tip SHA after this file is committed.

## Independence

Do not inspect the parallel HQ199 Space Bunny returns before your own conclusions are fixed.

## Mission

Independently review the remaining R9 accounting/ownership frontier after HQ198 broker acceptance.

Review these questions:

1. Does R9 genuinely need a per-source execution/session owner above one _decode() call, or can the current decoder-level broker itself lawfully own the warrant source scope?
2. What lifecycle boundary makes path opens, existence checks, metadata reads and decoder invocations exact per source entry?
3. Is decoder_invocations a separate mandatory account requiring a new counter?
4. Which of the seven frozen source operation classes admit a header-prefix read?
5. Do SRC08/SRC12 metadata-only declared-encoding operations forbid a compatibility full read?
6. What exactly does SRC27's 'will involve multiple path-level opens' mean — binding lower-layer minimum or historical/descriptive expectation?
7. Does SRC27's EXACTLY_ONE_GOVERNED_FRESH_FULL_ROUTE_PASS require one full reader invocation, one decoder entry, or both? Keep all layers separate.
8. Can MAX 1 decoder invocation be introduced as a conservative execution-policy ceiling without fabricating historical expected-count authority?

## Exact authorities

Use at minimum:
- c2af4f61d68e9803af83f8e26f633acfe31062fa — C4B workload/warrant freeze
- 8ff40d37de69db2d8a6053a7c2242f481677f1a4 — exact C4 accounting law + warrant candidate
- ea51c409462b3bfe0a88a4b7e7326e117b76877e — technical-value analysis
- 9a07441a6296d7cf2a9aa11dd70e728db5fa9f1a — independent broker acceptance
- 4b6335ca5fc485108b0ffb1d682a29a02e1eee51 — accepted repaired broker code
- dbf3287084b547226a401fd0bde2da46610f2b9b — HQ199 adjudication

## Current-code attack

Inspect exact repaired code and verify/falsify:
- SourceAccessBroker is instantiated inside _decode and therefore naturally scopes to one decode call;
- decoder_invocations has no account/budget field;
- header_prefix() is called unconditionally for every format/source;
- encoding != None currently routes to full_read when no selected set is present;
- selected route is metadata + selected read;
- SRC27 compatibility lane currently performs metadata + full read;
- PhysicalSourceIncidence keeps the broker alive for later iteration;
- caller-owned close lifecycle is not itself a warrant source-session owner.

## SRC27

Build the strongest case that 'multiple path-level opens' is normative.
Build the strongest case that it is descriptive of the then-current implementation.
State which reading wins and why.

Also distinguish:
- outer full Route-B pass
- decoder invocation
- metadata read
- full read
- chunk read
- reader invocation
- physical source-path open

Do not collapse any pair.

## Session-owner sufficiency test

If you conclude a new per-source session owner is required, specify the minimum properties that would make it sufficient:
- once per bound source entry;
- one broker lifecycle;
- exact operation plan;
- decoder-entry counter;
- deterministic close;
- aggregate receipt;
- second-session/second-decode refusal where budgets require it;
- no silent legacy-path fallback.

State what such an owner still would NOT solve, including source-size-dependent byte ceilings.

## Allowed dispositions

Exactly one:
- PER_SOURCE_SESSION_OWNER_REQUIRED__SEVEN_SOURCE_PLAN_DETERMINATE
- CURRENT_BROKER_SCOPE_ALREADY_SUFFICIENT__NO_NEW_SESSION_OWNER_REQUIRED
- SRC27_ONE_OPEN_BROKER_CONFLICT__ARCHITECTURE_DECISION_REQUIRED
- SPECIFIC_AUTHORITY_AMBIGUITY__ASTRA_DECISION_REQUIRED
- MATERIAL_CONTRACT_CONFLICT_FOUND

## Return packet

At minimum:
- 00_REVIEW.md
- 01_GOVERNED_SCOPE_ANALYSIS.json
- 02_SEVEN_SOURCE_OPERATION_MATRIX.json
- 03_SRC27_MULTIPLE_OPENS_REVIEW.json
- 04_DECODER_INVOCATION_ACCOUNT_REVIEW.json
- 05_SESSION_OWNER_MINIMUM_CONTRACT.json
- 06_FINAL_DISPOSITION.json

Commit, push, re-fetch, verify.

Terminal:
HQ199_R9_SCOPE_PLAN_INDEPENDENT_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED

No real survey-source access, locator discovery, warrant issuance, live C4, production mutation, C7, or actor/person work.