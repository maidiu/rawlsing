# PYAT HQ199 — seven-source operation-plan authority reconstruction — R1

Repository: maidiu/rawlsing

Role: documentary authority-forensics worker — Space Bunny

Branch:
agent/rabochii-pyat-hq199-r2

Documentary base:
dbf3287084b547226a401fd0bde2da46610f2b9b

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ199-R9-SEVEN-SOURCE-OPERATION-PLAN-R1/
- /WORKER_RETURNS/PYAT-HQ199-R9-SEVEN-SOURCE-OPERATION-PLAN-R1/
- /PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ199_R9_SCOPE_OWNER_ADJUDICATION_R1.md

Read historical authorities through exact Git objects. Do not clone or create a full checkout.

The exact startup SHA is the commission-tip SHA after this file is committed.

## Mission

Reconstruct the exact seven-source execution plan that the governed source-session owner must eventually implement.

Do not write production code.
Do not invent numeric budgets.
Do not weaken existing frozen operation classes.

Central questions:
1. What operations are admitted for each of SRC02, SRC06, SRC08, SRC12, SRC14, SRC26, SRC27?
2. Which operations must be zero?
3. Is SRC27 phrase 'will involve multiple path-level opens' a normative frozen minimum or a descriptive statement about the then-current implementation?
4. How do the outer governed full Route-B pass and lower-layer full_reads, chunk_reads, reader invocations, decoder invocations, hash/metadata/open accounts relate without collapsing them?
5. Can decoder_invocations = MAX 1 be lawfully frozen as an execution-policy ceiling at the per-source session scope?
6. Which values are FROZEN_AUTHORITY versus IMPLEMENTATION_POLICY_CANDIDATE versus UNBOUND?

## Exact authority set

Read at minimum:
- c2af4f61d68e9803af83f8e26f633acfe31062fa — C4B workload freeze, authority/API freeze, unsigned warrant template
- 8ff40d37de69db2d8a6053a7c2242f481677f1a4 — exact C4 accounting law and warrant candidate
- ea51c409462b3bfe0a88a4b7e7326e117b76877e — HQ198 technical-value return
- 4b6335ca5fc485108b0ffb1d682a29a02e1eee51 — accepted repaired broker candidate
- dbf3287084b547226a401fd0bde2da46610f2b9b — HQ199 adjudication

## Required per-source matrix

For each source emit:
- source_key
- operation_class
- source format
- reader encoding/config lane
- selected variable names and ordinals
- row_data_mode: METADATA_ONLY / SELECTED / FULL / CHUNKED_FULL / NONE / another exact type if required
- metadata_reads expectation
- selected_reads expectation
- full_reads expectation
- full_route_passes expectation
- header_prefix admitted yes/no
- header_prefix bytes if frozen
- hash pass expectation/status
- existence/access expectation/status
- path-open expectation/status
- decoder-invocation expectation/status
- retry ceiling
- byte-count status
- exact authority provenance
- authority status: FROZEN_AUTHORITY / IMPLEMENTATION_POLICY_CANDIDATE / UNBOUND

Do not turn descriptive prose into numeric authority without proving that the prose is normative.

## SRC08/SRC12

The frozen class is metadata-only with declared encoding.
Determine explicitly whether any row-data/full read is admitted.
If none is admitted, record that encoding configuration is independent of row-data mode.

## SRC26

Determine exactly whether the 176-byte header-prefix operation is unique to SRC26.
Do not infer DTA 512-byte prefix authority from implementation behavior.

## SRC27 deep review

The exact law says one governed full Route-B pass is not one OS-level file open, and says the pass will involve multiple path-level opens, a hash pass, a metadata pass and a full read.

Determine from origin/context:
- whether 'multiple path-level opens' freezes a normative minimum >=2;
- whether it describes the pre-broker implementation expected at the time;
- whether the one-open broker may lawfully reduce that lower-layer count while preserving the pass and separate accounting;
- whether exactly one pass implies MAX 1 decoder entry/session;
- whether one full reader invocation is frozen;
- whether chunked full reading could substitute for that full read.

Do not choose by convenience.

## Decoder invocation budget

O1-C07 requires decoder invocations as a separate account but supplies no explicit count in the seven per-source entries.
Determine whether MAX 1 per source session may be introduced as a conservative implementation-policy ceiling, whether that requires higher authority, or whether another structure is required.
Keep expected / maximum / observed distinct.

## Current candidate mismatch crosswalk

Against 4b6335ca5fc485108b0ffb1d682a29a02e1eee51, verify rather than assume:
- selected sources perform unwanted header-prefix reads;
- metadata-only encoded sources may fall into compatibility full-read behavior;
- SRC27 may carry an unwanted DTA prefix read;
- outer full-route pass has no explicit owner/account;
- decoder_invocations has no owner.

## Output

At minimum:
- 00_RETURN.md
- 01_SEVEN_SOURCE_OPERATION_PLAN.json
- 02_SRC27_MULTIPLE_OPENS_ADJUDICATION.json
- 03_DECODER_INVOCATION_POLICY.json
- 04_CURRENT_CANDIDATE_MISMATCHES.json
- 05_IMPLEMENTATION_CONTRACT_FOR_SESSION_OWNER.json
- 06_AUTHORITY_VS_POLICY_VS_UNBOUND.json
- 07_FINAL_DISPOSITION.json

Allowed dispositions:
- SEVEN_SOURCE_PLAN_DETERMINATE__ONE_OPEN_BROKER_COMPATIBLE
- SEVEN_SOURCE_PLAN_DETERMINATE__SRC27_ONE_OPEN_BROKER_CONFLICT
- PLAN_PARTIAL__SPECIFIC_AUTHORITY_GAPS_REMAIN
- MATERIAL_AUTHORITY_CONFLICT_FOUND
- ASTRA_DECISION_REQUIRED

Commit, push, re-fetch, verify.

Terminal:
HQ199_R9_SEVEN_SOURCE_PLAN_RETURNED__HQ_ADJUDICATION_REQUIRED

No real survey-source access, locator discovery, warrant issuance, live C4, production mutation, C7, or actor/person work.