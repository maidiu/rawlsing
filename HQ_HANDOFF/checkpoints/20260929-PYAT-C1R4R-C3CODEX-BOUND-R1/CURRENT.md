# RAWLSING HQ CHECKPOINT — C1 FINAL REREVIEW + C3 CODEX EXECUTION FALLBACK BOUND

Checkpoint: `20260929-PYAT-C1R4R-C3CODEX-BOUND-R1`

Decision:
`HQD-2026-09-29-128`

Status:
`C1_R4_RETURNED_REVIEW_READY__C1_R4_INDEPENDENT_REREVIEW_BOUND__C3_03_STATIC_PASS_EXECUTION_BLOCKED__CODEX_FALLBACK_BOUND`

## C1

R4 return:
`233a91d7cb7789a8e338405abdfef15a5a8ee764`

HQ accepts R4 as internally synchronized and ready for the final independent rereview.

Current owner-native UNKNOWN_CURRENTNESS SelectionKey:
`53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`

Former contradictory ref:
`a0c54c568eee1351a67ecfee43c297e82aba509daf4bce6932b5ae7331ca03cd`

is retained only as explicitly stale/wrong history in the current packet.

Independent rereview issued:
- branch `agent/reviewer-pyat-hq126-c1-00-r4-rereview-r1`
- commission `bcaa43885dafaa9391a4466620eb41a0e570eebb`
- exact base `233a91d7cb7789a8e338405abdfef15a5a8ee764`

C1-01 remains blocked. Even an approving rereview does not auto-authorize C1-01; HQ must separately freeze the exact implementation contract, oracle and write allowlist.

## C3

Independent C3-03 review:
`1b92286cc1f8e40f73b8a3bcf61e11d36aabe2a0`

Static repair disposition:
`PASS_AT_DECLARED_GRAIN`

Execution qualification:
`BLOCKED_EXECUTION_CAPABILITY`

Overall:
`STATIC_PASS__EXECUTION_CAPABILITY_PENDING`

Exact semantic candidate:
`901e3e77f905847d3ef8d86b458280d8fe422dd0`

Exact execution commit:
`283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`

GitHub run `36627731035` failed before runner assignment on attempts 1–4. Attempt 4 job:
`109643559497`

with `runner_id=0`, empty steps, no pytest, no environment evidence and no artifacts.

The Omega capability-routing law authorizes a bounded Codex fallback once a runtime capability blocker is proven rather than spending repeated browser attempts.

Codex fallback issued:
- branch `agent/codex-pyat-hq126-c3-03-source-free-execution-r1`
- commission `01d393e94b185f9cbb7f8aa85d25b7ee8f79a64a`
- branch base `1b92286cc1f8e40f73b8a3bcf61e11d36aabe2a0`
- exact tested commit must remain `283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`
- no code/test/workflow mutation permitted;
- source-free execution only;
- raw survey access forbidden.

C3 adoption remains blocked until exact source-free execution qualification passes.

## Held gates

- C1-01: wait final independent C1 rereview + HQ exact implementation freeze.
- C2-02: wait accepted C1 contract + exact HQ proving workload.
- C3 adoption: wait Codex source-free execution PASS.
- JOIN-01: wait applicable independently reviewed/qualified outputs.
- OMEGA-1: wait scoped source-free join.

No Astra trigger. No raw-source execution. No new semantic/comparability authority. PRE-V3→V3 remains deferred.
