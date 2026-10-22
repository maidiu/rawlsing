# Same-person join — JOIN-E repair checkpoint

**Branch:** `codex/sorok-join-e-20261022`
**Exact startup:** `3fe8444b4a0374d95fa9f7e60dd295049a5d3172`
**Continuation seal:** `141b5fe1e393621862791281e980c450715bbb9a`
**Prior candidate:** `c367777f83367240352c267a2d3750abb7f09397`
**Authority:** independent ruling `3de081023406a52ec23e1ae43ade77aea485a3f8`; human HQ appointment; effective owner `6456fc57cbe05cdf69e63ef51fa6ca6198401c60`.
**Grade:** `TEST_ONLY_SOURCEFREE__NOT_NATIVE`.

## Implemented in this repair

- `joined/imports.py`: one explicit, idempotent J-first/E-second closure. E-first imports are cleared and replayed from J before E; actual module origins are audited.
- `joined/provenance.py`: sidecar/meta source is compared with the C12 `GM01_SOURCE` episode, the keyed C8 payload source, and the C8/E1/target readsets. Exact R31J-to-BP1 actor map is checked.
- Canonical root/lineage guards: `product_root` must be `<state_root>/product`; `state_root` must match; foreign/R29P roots, orphan roots and moved roots are typed refusals. Legitimate `fork_alt` writes a parent/branch/clock/root receipt and reopens.
- Nonmutating cold open retained via `joined/readonly.py`.
- `joined/refusal.py`: derived targetless C12/world session for B `REFUSE_TOOL`/`NO_CHANGE`. It carries the real refusal source, C8/E1 and no C9/C10 target; E refuses help because the tool is absent. No target or grant is fabricated.
- B source-edge proof: share vs refusal uses the same `_help_observable` assertion (`True/1/SHARE_TOOL` vs `False/0/REFUSE_TOOL`); a real source-derived material mutation makes the refusal test fail by assertion and restore to pass. The original A omission→inspection witness is retained.
- Full encounter/cold/fork/privacy/contact/no-contact regressions retained.

## Executed

- Owned suites: **15 join + 8 J + 15 E + 10 R30A = 48 entries**, all pass.
- JOIN-V frozen suite on repaired candidate: **10 positive + 7 hostile = 17 pass**.
- Proof witness: two claims (`A omission→inspection` and `B refusal→targetless session`), both `TARGET_ASSERTION_FAILED`, `BOUNDED_MUTATION_DETECTED`.
- Closure: 444/444 source-manifest blobs verified; fresh-process loaded origins all J/E/LIVE correct.
- Cold root hashes unchanged; targetless refusal C12 verifies.
- `evidence/test_results.json`, `evidence/positive_receipt.json`, `evidence/targetless_refusal.json`, `evidence/refusal_owner_contract.json`, `evidence/proof_witness.json`, `evidence/junit/**`.

## Remaining / NOT_RUN

- Independent JOIN-V final verdict on exact final SHA.
- Native CAN008/CAN011/ADP019/C8/C11/C12/Pyat N11/N12: `NOT_RUN`/`HOLD`.
- External actor LLM/two-call, production, human A5: `NOT_RUN`.
- Full inherited R29P 155/202/30 denominators: not rerun; counts are executed entries, not a clean union.
- C10 target semantics for refusal remain absent by design; owner contract records the remaining decision.

## Next safe stop

Commit coherent units, push ordinary non-force, read back exact remote HEAD, and hand to JOIN-V/HQ. No self-adoption.

**Model selector:** OpenCode implementation worker, `DeepSeek V4.1-Flash` requested at `MAX`; actual metered effort/quota `UNKNOWN`. No model switch, provider call or subagent.
