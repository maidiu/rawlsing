# PYAT HQ200 — seven-source unsigned warrant/accounting successor — R1

Repository: maidiu/rawlsing

Role: documentary instrument worker — Space Bunny

Branch:
agent/rabochii-pyat-hq200-r2

Base technical-value successor:
ea51c409462b3bfe0a88a4b7e7326e117b76877e

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ200-R9-SEVEN-SOURCE-WARRANT-SUCCESSOR-R1/
- /WORKER_RETURNS/PYAT-HQ200-R9-SEVEN-SOURCE-WARRANT-SUCCESSOR-R1/

Read by exact Git object:
- HQ200 adjudication e7ce39dade6b169ab068f5f786b7a0dea06846dd
- seven-source plan 09e1325da6ee880374a4065ae748cc03de93c421
- HQ198 successor ea51c409462b3bfe0a88a4b7e7326e117b76877e
- accepted repaired broker 4b6335ca5fc485108b0ffb1d682a29a02e1eee51
- HQ199 session candidate 90ccbd54c549f67358d0c02ad18ff90b843cf3ee

Do not clone or create a full checkout.

The exact startup SHA is the commission-tip SHA after this file is committed.

## Mission

Produce the next unsigned, unissued, non-authorizing warrant/accounting successor that carries the exact seven-source operation plans and HQ200's corrected authority/policy distinctions.

This is documentary binding only.
Do not issue anything.
Do not fill locators.
Do not invent source-dependent numeric byte budgets.

## Required plan fields

For each of SRC02, SRC06, SRC08, SRC12, SRC14, SRC26, SRC27 carry a machine-readable operation plan containing:

- source_key;
- format;
- reader lane/config;
- row_data_mode;
- selected variable names/ordinals where frozen;
- header_prefix_bytes or explicit NONE;
- retry ceiling;
- full_route_pass expected/min/max fields;
- all O1-C07 access accounts;
- expected / floor / maximum / observed kept distinct;
- authority status for every numeric/policy field:
  - FROZEN_AUTHORITY
  - IMPLEMENTATION_POLICY
  - PENDING_TECHNICAL_ACCEPTANCE
  - UNBOUND_SOURCE_DEPENDENT

## Exact source-plan binding

Carry the documentary determination from 09e1325... and HQ200:

SRC02:
- SELECTED Q10B ordinal 58;
- full_reads exact 0;
- selected_reads exact 1;
- no header prefix.

SRC06:
- SELECTED Q101/Q2061B ordinals 20/19;
- full_reads exact 0;
- selected_reads exact 1;
- no header prefix.

SRC08:
- METADATA_ONLY;
- declared Big5 config;
- metadata_reads exact 1 where frozen;
- selected/full row-data reads exact 0;
- no header prefix.

SRC12:
- METADATA_ONLY;
- declared Windows-1252 config;
- metadata_reads exact 1 where frozen;
- selected/full row-data reads exact 0;
- no header prefix.

SRC14:
- SELECTED v372 ordinal 466;
- selected_reads exact 1;
- full_reads exact 0;
- no header prefix.

SRC26:
- METADATA_ONLY plus admitted 176-byte header prefix;
- selected_reads 0;
- full_reads 0;
- header_prefix_bytes exact 176;
- do not invent a DTA-style 512 prefix.

SRC27:
- FULL declared latin1 compatibility lane;
- outer full_route_passes expected 1 and max 1 — FROZEN_AUTHORITY;
- full_reads FLOOR 1, historical ceiling UNBOUND;
- path_opens historical numeric value UNBOUND;
- decoder_invocations historical expected value UNBOUND;
- retries max 0;
- no header prefix;
- selected_reads remains UNBOUND unless exact governing authority supplies a value.

## SRC27 correction

Do NOT encode:
- path_opens >=2;
- full_reads exact 1 as historical authority;
- decoder_invocations exact 1 as historical authority.

The phrase "will involve multiple path-level opens" is descriptive, not a numeric floor.

The generic runtime may later bind:
- decoder_invocations MAX 1 as IMPLEMENTATION_POLICY;
- path_opens MAX 1 as IMPLEMENTATION_POLICY;
- full_reads MAX 1 as IMPLEMENTATION_POLICY if independently accepted.

Such maxima must live in policy/authorization fields, never historical expected fields.

Until the HQ200 runtime/session reviews accept the relevant mechanisms, mark these candidate maxima:
`PENDING_HQ200_RUNTIME_ACCEPTANCE`.

## Route-pass account

Add an explicit outer full-route-pass account separate from every lower layer.

For SRC27:
- expected = 1, FROZEN_AUTHORITY
- maximum = 1, FROZEN_AUTHORITY
- observed = null until execution
- second pass stop law = new HQ-bound authority required

For every other source:
- no full-route pass is admitted; represent this exact zero where the source plan authority supports it.

Never use route-pass count as the value for decoder/full/chunk/reader/path-open accounts.

## Operation-plan mismatch blockers

The successor should state that warrant issuance requires the accepted runtime to prove:
- declared encoding does not imply row-data mode;
- header-prefix access follows the bound plan;
- decoder_invocations is separately measured;
- bound plan cannot be swapped after issuance;
- outer full-route-pass maximum is enforced;
- the source-session owner is deterministic.

These are technical acceptance fields, not locator fields.

## Byte accounts

Reader-byte measurement/enforcement exists.

Numeric real-source byte ceilings remain:
`UNBOUND_SOURCE_DEPENDENT__MUST_BE_BOUND_BEFORE_LAUNCH`

Do not use synthetic totals.
Do not silently turn measurability into a budget.

If a lawful derivation rule exists in frozen authority, cite it exactly. Otherwise preserve the requirement as issuance-blocking.

## Historical PRQ-07

PRQ-07 is DISCHARGED and MUST NOT reappear as an open blocker.

## Instrument status

Must remain exactly:
- signed=false
- issued=false
- authorizes_access=false
- execution_authorized=false
- approvals unset
- all seven locator placeholders unfilled

## Required outputs

At minimum:
- 00_RETURN.md
- 01_SEVEN_SOURCE_PLAN_BINDING.json
- 02_AUTHORITY_POLICY_OBSERVED_MATRIX.json
- 03_SRC27_OUTER_AND_LOWER_ACCOUNTING.json
- 04_TECHNICAL_ACCEPTANCE_DEPENDENCIES.json
- 05_ISSUANCE_BLOCKER_MATRIX.json
- 06_UNSIGNED_SEVEN_SOURCE_WARRANT_SUCCESSOR.json
- 07_FINAL_DISPOSITION.json

Allowed dispositions:
- SEVEN_SOURCE_WARRANT_SUCCESSOR_READY__RUNTIME_ACCEPTANCE_AND_SOURCE_DEPENDENT_VALUES_PENDING
- WARRANT_SUCCESSOR_PARTIAL__SPECIFIC_STRUCTURE_GAP
- MATERIAL_AUTHORITY_CONFLICT_FOUND
- SOURCE_DEPENDENT_VALUES_PREVENT_SOURCE_FREE_COMPLETION

Do not claim R9 closed.

Commit, push, re-fetch, verify.

Terminal:
HQ200_R9_SEVEN_SOURCE_WARRANT_SUCCESSOR_RETURNED__HQ_REVIEW_REQUIRED

No source access, locator discovery, warrant issuance, live C4, production mutation, C7 or actor/person work.
