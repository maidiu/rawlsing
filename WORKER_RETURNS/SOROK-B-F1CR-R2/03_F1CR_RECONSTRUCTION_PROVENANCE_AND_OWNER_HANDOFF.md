# F1CR reconstruction provenance and owner handoff

## Exact source cuts

| Cut | SHA | Role |
|---|---|---|
| R5 recovery | `aebb2452b277bfc91fc78dec8d6001f8a844cc8c` | exact F1C recovery and reconstructed candidate |
| I1 | `7d44e30064f8e873e1a3ff9cb05fe75456756b88` | same I1/CP-A5 guarded consumer |
| Original F1C | `bcea367e7dc0f2e069de71b0fe5e481de094dad5` | original author source |
| F1CR historical | `03be5c225b8ec5832c1c648b9c1799419f0c4066` | historical F1CR return |
| BP2P4J | `5b3e6577400ea1d88971ae6b48e41a118b8059ae` | joined source |
| O1 | `501ea1f5bf07468b2c0437f452a81f3515cfdb6f` | source lineage |
| Launch PRE-MAIN / branch base | `750548ddbb9b4392a16ce93097b856f349e16182` | read-only reference |
| PRE-MAIN remote at return | `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3` | docs/CI-only #545; not merged into this worker branch |

## Exact F1C identities

- Original F1C program blob `104f5bd7826c8676192eac96753d980e35d8a80a`, SHA-256 `7e3492a267acbc0fa11d8792158bdaa2acc9dfb6053f16141ed637dc1cd2881b`.
- Frozen test blob `b012e65eb92c21e8733bdd92f46ca4a88aa709e5`, SHA-256 `271e6aa15af8b2c3217ed2fdb94f2514e70c0bf9a9fa3122e3fe4d7f0aebdc6b`.
- Claimed F1CR patched executable blob `bf7e625e1f208908e583ea72ebb73992ad7d19ae`, SHA-256 `18c96f97eca5480893c0f38a06f21c0d985fe0c6c997e63e0898001157351dfb`: **`SOURCE_NOT_FOUND`**. It is absent from the recovered objects, trees and surviving worktrees.
- R5 reconstructed candidate blob `c6e64b5874938045d80aae348de94930539d5cd2`, SHA-256 `12f183a379bd1fabf37433b0e3ac893221f78370cd73d2a7c173554a1db14871`: explicitly `RECONSTRUCTED_CANDIDATE`, not the missing F1CR bytes.

The reconstructed candidate adds `live_prior(life)` and A/B/shared digest checks after the frozen-hash check and before C8. It is not relabeled as the original patched source.

## Replay result

- Original F1C: 13/13 outcomes exit 0; the three live-history mutation tests fail as historical evidence (`A`, `B`, `shared_witness`).
- Reconstructed candidate: 13/13 outcomes exit 0; **3/3 live-history mutations pass** with `LIVE_A_HISTORY_CHANGED`, `LIVE_B_HISTORY_CHANGED`, `LIVE_SHARED_HISTORY_CHANGED`.
- The reconstructed candidate is required before use; it is still `TEST_ONLY`, not native B.

Local result hashes:
- reconstructed 13: `87fa57f6ec49234a5203bea3ec5182baa37768feed80d895800b02acd7b4b178`;
- original 13: `830b2dc9309bdf3fe7f23f86f0270a6fc58a2c6fb7843d7c0bbff46b2c84a291`;
- R5 historical values were `4de846b2…` and `5c3b91dd…`; the difference is the replayed runtime, not a changed case set.

## Targetless C10 boundary

The targetless adapter is separate from the original F1CR patched source:

- `REFUSE` is a performed TEST_ONLY B refusal, targetless, with B event access when observed.
- `SILENCE` is a non-event condition with `performer=None`.
- `NO_PROPOSAL` has no performer and no proposal.
- `HELD_MISSING_RULE` has no competent evaluation receipt.
- `UNOBSERVED` preserves the B action physically but does not insert it into A's memory.
- `EVALUATED_NO_CHANGE` requires a competent receipt.
- None creates a C9 target, C9 proposal, performed E2, learned practice or utterance.

The targetless ledger is an adjunct to I1's `GuardedJoinedProduct`; it is not a canonical C10 owner contract and not a replacement for the original C9/C10 semantics.

## Material ledger owner decision

The inherited I1 offscreen event reports `material_delta=-1` with stock 0. The adapter does not accept that as unexplained negative consumption:

- the positive option is a source-visible TEST_ONLY replenishment of one unit at tick 39, then the market work consumes it at tick 40 (`1 -> 0`, `clamped=False`);
- the negative option is an explicit `MATERIAL_WORK_REFUSED` with unchanged stock.

The I1 event is preserved. The incumbent I1/BP4 owner must decide whether the tick-39 replenishment is an admissible TEST_ONLY prior stock or whether the event must become a refusal. No native material grant is issued.

## Owner handoff

- **Original F1C/F1CR author:** confirm or reject the reconstruction; supply `bf7e625e…` if it ever becomes available. Do not accept the reconstruction as the missing bytes.
- **R31J/C8 owner:** review the live A/B/shared binding and the material/action fields.
- **I1/CP-A5 owner:** review `TargetlessGuardedJoinedProduct` and the same-person targetless read.
- **C9/C10/C12 owners:** decide whether the targetless receipt is a lawful C10 adjunct; no C9 target/proposal is supplied.
- **BP4/material owner:** decide the tick-39 prior-stock condition versus explicit refusal.
- **Incumbent HQ + distinct reviewer:** intake and independently review. No self-adoption.

## Preserved holds

- F1CR claimed patched source remains `SOURCE_NOT_FOUND`.
- Original F1C/F1CR author bytes are not replaced by reconstruction.
- Native B, original CAN/ADP/SCI05/Pyat/C11/C12, M35/S35 and A0–A5 remain HOLD.
- No PRE-MAIN merge, adoption, actor/person issuance or self-review.
