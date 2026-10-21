# R26V downstream join and severance

## Positive

`run_joined` patches the BP2 builder seam, runs real `JoinedProducer`, assembles `BP2Artifacts`, then `JoinedProduct`:
C8 occurrence/proof → E1 → CAN008 A → separate CAN011 T/grant → C9 target → performed E2 → C12/A0/A2. Observed A0 `ARRIVAL`, practice/tool, A2 clock 40 and `OFFSCREEN_REPAIR`, other `completed_units=5` for the new variant; native claims all false.

## Cuts

| Cut | Physical change | Result |
|---|---|---|
| B independent refusal | `B_NO_REFUSAL` ledger lacks B `NO_CHANGE` | target changes; same expected-target assertion RED; restore on fresh good root PASS |
| A independent omission | `A_NO_OMISSION` ledger lacks A `NO_CHANGE` | target changes; same assertion RED; restore PASS |
| A performed material | `A_NO_MATERIAL` genesis | `ACTOR_G18_HISTORY_NOT_RESOLVED` typed refusal; good actor restores |
| Source target mismatch | named assertion bound to another target | `R26V_TARGET_NOT_BOUND_TO_ACTOR_HISTORY`; good target restores |
| H0 | no performed action | `practice_established=False`; no fabricated development |

The BP2 target identity is path/key-bound; the same-assertion test uses the **same process/root expectation** and a fresh restored root. C8 state digest, A0/A2 and cold fields are the path-independent comparison.

## Not cut here

E1, CAN008 Rule A, CAN011 T/grant, C8 protected trust, native encounter/opportunity and E2 independence are inherited from BP2P4J but were **not each independently severed in this campaign**. That is the main engineering REVISE edge.
