# HQ200 — R9 session/plan adjudication

Status:
`SEVEN_SOURCE_PLAN_ACCEPTED__SRC27_ONE_OPEN_COMPATIBLE__SESSION_CANDIDATE_PENDING_INDEPENDENT_ACCEPTANCE__ROUTE_PASS_BINDING_NEXT`

Inputs:
- seven-source authority return: `09e1325da6ee880374a4065ae748cc03de93c421`
- governed source-session candidate: `76970cfdfc8968e975595ea288cf44b448205e30`
- code-bearing session candidate: `90ccbd54c549f67358d0c02ad18ff90b843cf3ee`
- independent scope/plan review: `302d4a5da513381e26066cea70bf3ec5be7d3636`

## Seven-source plan

HQ accepts:
`SEVEN_SOURCE_PLAN_DETERMINATE__ONE_OPEN_BROKER_COMPATIBLE`

Accepted source-plan consequences:
- SRC02: SELECTED Q10B / full_reads 0 / no header prefix.
- SRC06: SELECTED Q101,Q2061B / full_reads 0 / no header prefix.
- SRC08: METADATA_ONLY with declared Big5 / selected 0 / full 0 / no header prefix.
- SRC12: METADATA_ONLY with declared Windows-1252 / selected 0 / full 0 / no header prefix.
- SRC14: SELECTED v372 / full_reads 0 / no header prefix.
- SRC26: METADATA_ONLY + exactly the admitted 176-byte prefix operation / selected 0 / full 0.
- SRC27: FULL compatibility lane with latin1, full Route-B pass outer account, no admitted header-prefix operation.

Reader encoding/configuration is independent of row-data mode.

The pre-session implementation violated the frozen plan for SRC08/SRC12 by letting non-null encoding trigger full row-data reads, and violated six sources by unconditionally reading a header prefix. The generic HQ199 session candidate contains the mechanism needed to correct both.

## SRC27 "multiple path-level opens"

HQ accepts the descriptive reading.

The phrase:
`the pass will involve multiple path-level opens`
does NOT freeze a numeric path-open minimum.

Decisive evidence:
- dedicated HQ190-C per-access grading gave SRC27 path_opens no floor and no ceiling;
- the hardened minimum names existence/access, full SHA, metadata read and full compatibility read, but no path-open floor;
- the phrase is absent from the operative C4 warrant candidate;
- its binding clause is that each layer must be accounted separately.

Therefore the accepted one-open broker is compatible with SRC27.

SRC27 path_opens remains historically UNBOUND. A one-open implementation-policy ceiling may be proposed by the runtime mechanism, but must not be relabelled as frozen historical authority.

## SRC27 account semantics — correction to independent review

HQ does NOT adopt the independent review's stronger statement that one Route-B pass itself freezes exactly one full reader invocation and exactly one decoder entry.

Frozen authority is:

- `full_route_passes`: EXACT 1 / MAX 1.
- `full_reads`: FLOOR >=1; ceiling UNBOUND.
- `decoder_invocations`: mandatory separate account; historical expected value UNBOUND.
- `path_opens`: mandatory separate account; historical numeric value UNBOUND.
- `retries`: MAX 0.

Therefore:

- MAX 1 decoder_invocations is permissible as an **IMPLEMENTATION_POLICY_CANDIDATE** authorization ceiling, not as a historical expected count.
- A runtime may choose exactly one full read as a stricter execution policy, but frozen authority itself supplies only the floor.
- chunk_reads cannot silently satisfy the frozen full-read floor; they are a different lower-layer account.
- the outer full Route-B pass remains separate from decoder/full/chunk/reader/open accounts.

## Session owner

HQ accepts the shared architectural conclusion:
`PER_SOURCE_SESSION_OWNER_REQUIRED`

The HQ199 implementation candidate adds:
- GovernedSourceSession;
- SourceOperationPlan;
- independent row-data modes;
- plan-controlled header-prefix access;
- separate decoder_invocations account/budget;
- one broker/physical-open lifecycle;
- live aggregate session receipt;
- deterministic close;
- pre-operation second-decoder refusal.

Its source-free evidence is strong:
- exact R7 court 55/55 twice;
- 15 session courts;
- 20 broker courts;
- zero new full-suite failures;
- no hard-coded SRCxx policy.

However the session candidate remains:
`CANDIDATE_READY_FOR_INDEPENDENT_ACCEPTANCE`

It is not yet adopted.

## Missing route-pass owner

The generic plan currently carries an `outer_account_token` field, but the session/broker account model does not yet own or enforce:
`full_route_passes`.

For SRC27 this is a frozen workload account:
- expected 1;
- max 1;
- second pass requires new authority.

The next runtime layer must add a separately typed outer route-pass account/ceiling without collapsing it into decoder_invocations or full_reads.

## Warrant-plan binding

Source-specific plans must NOT be hard-coded into the generic session module.

The unsigned warrant/accounting successor must carry the seven exact plans.

A generic binding layer should:
- validate a bound source-entry plan;
- construct one GovernedSourceSession;
- bind the exact operation plan;
- bind source-independent policy ceilings separately from frozen expected values;
- execute at most the admitted outer route-pass count;
- preserve unknown/source-dependent numeric fields as issuance-blocking.

## Remaining byte budgets

Reader-byte measurement and enforcement are technically accepted.

No numeric real-source reader-byte ceiling is source-free established.

That is not grounds to invent a number. The final instrument must preserve a source-dependent issuance-time requirement or exact later derivation rule.

## Next wave

1. independent acceptance review of the HQ199 session candidate;
2. generic warrant-plan binding + outer route-pass accounting implementation;
3. documentary unsigned warrant successor carrying the seven exact operation plans and corrected authority/policy distinctions.

All SPARSE_REQUIRED.

R9 remains open.
Host disk policy/capacity remains the separate live-run blocker.
HQ182 C4 non-adoption hold remains pending reserved Astra.
All source/warrant/live/C7/actor holds remain.
