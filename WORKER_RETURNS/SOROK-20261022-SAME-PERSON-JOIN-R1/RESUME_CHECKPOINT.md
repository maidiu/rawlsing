# Same-person join — JOIN-E checkpoint

**Branch:** `codex/sorok-join-e-20261022`
**Exact startup:** `3fe8444b4a0374d95fa9f7e60dd295049a5d3172`
**Authority:** independent ruling `3de081023406a52ec23e1ae43ade77aea485a3f8`; human HQ appointment; effective owner `6456fc57cbe05cdf69e63ef51fa6ca6198401c60`.
**Grade:** `TEST_ONLY_SOURCEFREE__NOT_NATIVE`.

## Implemented

- Explicit J-first/E-second closure with `joined/closure.py`: 444 vendored files checked against `SOURCE_MANIFEST.json` Git blobs; actual `__file__` paths checked for `r31j`/`bp4`/`r29p` (J), `r30a`/`r31e` (E), and live `rawlsing_next`.
- `joined/readonly.py`: cold reopen suppresses the pinned product's constructor writes; root files remain byte-identical after `JoinedSession.open`.
- `joined/session.py`: one root, explicit source/target/C8/E1 metadata, root and branch C12 verification, source-identity check, typed no-target refusal probe, fork/branch switch, CLI-compatible status.
- `joined/assertion.py`: frozen positive/refusal assertions and cold positive.
- `joined/cli.py`: runnable start/say/help/contact/attend/wait/leave/offscreen/return/status/verify/messages/fork.
- `DEMO_AND_VERIFICATION.md`: exact commands.
- `tests/test_join.py.proof.json`: proof-integrity witness for material state → E help admission.

## Executed

- New join tests: **10 passed** (`evidence/junit/join_new.xml`).
- J frozen R31J: **8 passed** (`evidence/junit/j_r31j.xml`).
- E frozen expression: **15 passed** (`evidence/junit/e_expression.xml`).
- R30A frozen session: **10 passed** (`evidence/junit/e_r30a.xml`).
- Proof checker: baseline PASS; `TARGET_ASSERTION_FAILED`; `BOUNDED_MUTATION_DETECTED` (`evidence/proof_witness.json`).
- Cold reopen: source/target/root preserved; root file hashes unchanged.
- B refusal: `NO_CHANGE`, `NO_PROPOSAL`, no target, `RESPONSE_EFFECTS_VALID_EMPTY`; typed owner contract returned (`evidence/refusal_owner_contract.json`).

## Remaining / NOT_RUN

- Independent JOIN-V review of exact final SHA.
- No-target C10/C12 representation remains an owner-contract HOLD; no target was minted.
- External actor LLM/two-call, native CAN/ADP/C8/Pyat/C11/C12, production, human A5: `NOT_RUN`/`HOLD`.
- Historical 202/30 inherited counts were not rerun; the local counts above are executed entries, not a clean union.

## Next safe stop

Commit coherent units, push ordinary non-force, read back exact remote HEAD, then prepare the final return. No self-adoption.

**Model selector:** OpenCode implementation worker, `DeepSeek V4.1-Flash` requested at `MAX`; actual metered effort/quota `UNKNOWN`. No model switch, provider call or subagent.
