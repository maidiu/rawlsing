# G1-G5 focused R2 matrix — SOROK #1037 B05

**Verdict:** `REVISE_EXACT_DEFECT`
**Candidate:** `270eb29cd4487b6865b61adc9d671952554d425d`
**Reviewer:** `ses_e21caf5dfffeSywXGrQ6qw65oe` (same nonauthor)

| Gate | Status | Evidence | Limit |
|---|---|---|---|
| G1 source/owner/custody | PASS_SCOPED_SOURCEFREE | exact candidate/base/branch; only B05 read-side changed; B04 unchanged; no writer/store/schema/lock/ledger/key; exact assets byte-identical; product read-only | fully privileged checkpoint fabrication outside append-only threat model |
| G2 build/first consumers | PASS_NORMAL_READERS_AND_COLD | original probe 34/34; #1027 63/63 semantic; cold two purchases + one rent; 5+6+43+3 tests; zero UNCHANGED, held REFUSED, historical/replay/retry | no full P6/MII/J1; timings under load |
| G3 falsification | FAIL_REVISE_EXACT_DEFECT | positive sole-rehash closed; sever/restore, sibling copy, positive forged rent, #1027, B04 controls pass | **forged ADMITTED zero-rent receipt accepted using public `say` no-cash checkpoints; actual zero writer is UNCHANGED** |
| G4 boundaries/preservation | PARTIAL_PASS_PRESERVATION__ZERO_STATUS_BOUNDARY_FAILS | no product/writer/schema/store/ledger change; normal, zero-genuine, held, historical, retry, cold preserved | ADMITTED status/actual-operation semantics not preserved for zero |
| G5 focused receiving | REVISE_EXACT_DEFECT | one exact remaining false ADMITTED proof; original 5b65 historical and positive case closed | not `ACCEPT_SCOPED`; no new repair loop |

## Exact zero residual

- Public `house.commit_dwelling` sets rent 0; materialize h1 `COMPLETE`; two public `session.product.say(...)` actions at clock 429.
- Four adjacent checkpoints at clock 429 all have cash `55`, material hash `8ee0b853d3b34cec760f642cd3203719055613d298950b0203d7629a351888da`, source `acd91d4ef9b4b8f09814a8b476d861cfe3f2c4f360ae0acccc15f7ef08ddc88e`.
- Sole appended `ADMITTED` rent receipt with rent 0, cash before/after 55/55, matching hashes.
- `read_household_obligation` returns `READ`, `historical=false`, `receipt_status=ADMITTED`, cash 55.
- Actual existing zero writer is `UNCHANGED`; no cash moved.

## Minimal correction for record (not dispatched)

ADMITTED must require a strict debit transition: rent > 0, after cash < before cash, actual checkpoint pair. Reject ADMITTED when rent == 0 or before == after; zero must remain UNCHANGED, insufficient cash REFUSED. No new ledger/key/writer.

## Nonclaims

No native/science/human/J1/protected acceptance, motive/volition inference, new ledger, or further repair round. Provider cost and checkpoint/org/quota `UNOBSERVED`.
