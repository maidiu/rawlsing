# M35 source-preimage defect closure — ACCEPT_SCOPED

Decision: **ACCEPT_SCOPED**.

## Exact cut

- Corrected candidate branch:
  `agent/rabochii-sorok-20261024-m35-firstclass-b-source-bp2-c12-r1`
- Corrected commit: `4170fbf19a9d5a64bc728f5b22156bbffcec51e5`.
- Prior rejected cut: `55377b554ce49941665ae4080f70f2132ad963f5`.
- Original source commit: `2d11e32c2d5e7d44449e03c6af68aa75d4de1a60`.
- Base: `76961d2e58e7139ddd63f1758aea19a8026b375f`.
- Active startup/commission: `89b703e8d775b8ecd0efb2a9c1cbfa6616bc7889`.

Inspected the immutable diff in a disposable Git clone with the warm R31J/JOIN-E
closure. No writes to the author checkout or controller attachment worktree, no
product code changes, no provider/native action. Language closure and M35 prior
receipt were not re-reviewed or modified.

## Corrected behavior

`firstclass.validate_source` now builds the exact `case_preimage(case)` and
compares every field before C8:

`b_actor`, `b_owner`, `b_event_ref`, `b_event_hash`, `b_performed`,
`b_operation`, `b_quantity`, `b_to_actor`, `b_clock`, `a_e1_ref`,
`a_e1_hash`, `a_e1_clock`.

Any mismatch raises `MaterialSourceRefusal("MATERIAL_SOURCE_PREIMAGE_MISMATCH")`
before the producer/C8 directory is created. `source_from_case` projects the
same preimage, so lawful share/refusal case changes remain valid.

## Executed checks

```text
PYTHONDONTWRITEBYTECODE=1 M35_JOIN_E_RETURN=... \
python3 -B -m pytest -q \
  WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1/tests \
  -p no:cacheprovider
8 passed in 1.64s
```

The preserved 9-case reviewer oracle, run against `4170fbf`, returned
**9 PASS / 0 FAIL**: all wrong-owner, wrong-ref/hash, wrong-clock,
wrong-operation, wrong-quantity, wrong-E1-ref/hash/clock cases are rejected
with `MATERIAL_SOURCE_PREIMAGE_MISMATCH`.

The eight affected tests also retain lawful share and refusal planning,
targetless C12/refusal, the same `do_help` consumer, cold reopen, share→refusal→
share restoration, and the E2 independent-action distinction. No historical
suite was recensused.

## Receipt

- 8-test output: `evidence/m35-4170-tests8.out` SHA-256 `d6dafd7f…`;
  8 PASS / 0 FAIL.
- Preserved oracle output: `evidence/m35-4170-mutations.json` SHA-256
  `194a257a…`; 9 PASS / 0 FAIL (the oracle's static cut metadata still names
  the prior reviewed cut).
- Corrected `firstclass.py` SHA-256 `acfdc42d…`; tests SHA-256 `b4f5a58f…`.
- Preserved oracle SHA-256 `63b23257…`.
- No live provider/domain/native/production action was performed.
