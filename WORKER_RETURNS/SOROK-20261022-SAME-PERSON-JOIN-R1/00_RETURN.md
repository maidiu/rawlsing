# SOROK JOIN-E — coherent same-person sourcefree completion

**STATUS:** `COMPLETE_SOURCEFREE_CANDIDATE__AWAITING_INDEPENDENT_JOIN_V_REVIEW__NOT_NATIVE__NOT_SELF_ADOPTED`
**BRANCH:** `codex/sorok-join-e-20261022`
**EXACT STARTUP:** `3fe8444b4a0374d95fa9f7e60dd295049a5d3172`
**ROLE:** OpenCode implementation worker; not Sorok HQ, not JOIN-V, not a native CAN/ADP/C8/C12/Pyat/C11 issuer, not a human A5 evaluator.
**MODEL / HARNESS:** OpenCode, `DeepSeek V4.1-Flash`, `REASONING=MAX` requested; actual metered effort/provider quota `UNKNOWN`; one agent; no subagent, external provider call or model switch.
**RUNTIME:** macOS 13.7.8 x86_64; Python 3.11.3; pytest 9.x.
**WRITE SCOPE:** `WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/**` only. Vendored J/E files remain byte-identical; the closure audit confirms all 444 manifest files.
**GRADE:** `TEST_ONLY_SOURCEFREE`.

## 1. FINDING | INTERPRETATION AND RIVALS | HQ ACTION REQUESTED | COMPETENT OWNER

| FINDING | INTERPRETATION AND RIVALS | HQ ACTION REQUESTED | COMPETENT OWNER |
|---|---|---|---|
| **F1. The join now imports one explicit closure.** `r31j.build/product/pre_c9/scenarios`, `historical_actor_producer`, `bp2p4`, `bp2_joined`, `bp4`, `r29p`, and `r26e` resolve under `vendor/j`; `r30a` and `r31e` resolve under `vendor/e`; the M6 module resolves from live `rawlsing_next`. The 444 vendored files match their recorded Git blobs. | The two vendored trees share module names; path presence alone is not proof. The rival explanation — accidental cache contamination — is falsified by actual `__file__` audit in a fresh process. | Accept the closure audit at scoped engineering grade; retain it as a precondition for any later join. | JOIN-E implementation + JOIN-V independent review |
| **F2. The full sourcefree encounter now runs from one persisted J root.** Start with `omit`; J material state leaves A's tool available; E admits help, contact, attention, departure, offscreen message and return; cold reopen preserves source, target and C12. | A second R29P root or a pressed/free-hours patch would be an invalid substitute. The rival — “the E session is still running on its original R29P root” — is falsified by the exact source/target meta and same-root C12 checks. | Accept scoped engineering after JOIN-V; keep `SCIENCE TEST_ONLY` and `AUTHORITY HOLD`. | JOIN-E + JOIN-V + Sorok HQ |
| **F3. E2 vs omission changes E help admission through actual material state.** `e2` exhausts the tool and yields `HELP_REFUSE`; `omit` preserves it and yields `HELP_ACCEPT`. The B operation remains `SHARE_TOOL` in both; the distinction is the performed/omitted A action. | A `SHARE_TOOL` label alone is not the cause; the rival — a test-only boolean overlay — is rejected by the source and tool-state checks. The proof witness severs the implementation path and the named test fails by assertion. | Retain as the frozen material/expression assertion; do not infer acquired practice or psyche. | JOIN-E + JOIN-V |
| **F4. B refusal is a lawful typed no-target boundary, not a fabricated C9 target.** `REFUSE_TOOL` yields C8 `661e95...`, `NO_CHANGE`/`NO_PROPOSAL`, `RESPONSE_EFFECTS_VALID_EMPTY`, and `target_id=""`. | The original BP2P4 consumer requires a committed target; the E session requires a product. The rival — mint a target to keep the UI green — is forbidden. | `HOLD` this exact no-target edge and request the owner's lawful no-target C10/C12 representation; unaffected share/E2, share/omit and expression paths are complete. | BP2P4/C9 consumer owner with C10/C12 owner |
| **F5. Attention is excluded from actor choice; only user perception changes.** Same-session contract hashes are identical under focused/distracted attention; admitted event IDs are unchanged; the surface differs. Private actor fields do not cross the surface; unobserved B yields `UNKNOWN_B`. | The rival — attention retroactively changes the actor's occurrence — is falsified by the identical contract and event identities. | Retain; do not claim native V2 or human phenomenology. | JOIN-E + JOIN-V |
| **F6. Fork and cold reopen work.** Cold reopen leaves all product-root file hashes unchanged; root and `first_session` verify; fork shares the past and diverges on the alternate branch. | The rival — cold reopen rewrites `bp2_join.json` and therefore mutates the root — was observed in the inherited candidate and is now suppressed by the read-only wrapper. | Accept the cold/fork behavior at scoped engineering grade. | JOIN-E + JOIN-V |

## 2. ENGINEERING / SCIENTIFIC / AUTHORITY COURTS

| Court | Verdict requested | Basis |
|---|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED_CANDIDATE__AWAITING_JOIN_V` | One root, explicit J/E closure, source-bound C8/C9/E2, branch and root C12 verification, full encounter, cold/fork, behavioral mutation witness. No vendor edits. |
| **SCIENTIFIC** | `TEST_ONLY_SOURCEFREE_MATERIAL_ACTION_EXPRESSION__H0_LIVE` | Material aid affects the simulated actor's next admission; B remains an independent source; no psychogenesis, acquired practice, demographic inference or human claim. |
| **AUTHORITY** | `HOLD` | No native CAN008/CAN011/ADP/C8/Pyat/C11/C12, external model, production or human A5 grant is issued or implied. |

## 3. DONE / REMAINING / CRITICAL BLOCKER / LARGEST MOVE / FLIGHT / DELTA

**DONE:** one explicit sourcefree J→C8/C9/E2→persistent C12→E expression/admission→user encounter; explicit closure audit; nonmutating cold reopen; B-refusal typed boundary; attention/privacy/actor-ignorance tests; fork/cold; proof witness; runnable CLI.

**REMAINING:** JOIN-V independent review of the exact final SHA; BP2P4/C9 owner decision for a lawful no-target C10/C12 representation; external model/two-call only if separately authorized; native CAN/ADP/C8/Pyat/C11/C12; human A5.

**CRITICAL BLOCKER:** the no-target refusal path cannot produce an E user session without a target because the original BP2P4 consumer refuses `BP2_C9_TARGET_ABSENT`; fabricating a target is prohibited. Native permissions remain separate and do not block the completed sourcefree positive.

**LARGEST MOVE:** independent JOIN-V review of this exact candidate; if accepted, one competent no-target consumer decision plus the existing sourcefree encounter. No second implementation worker.

**FLIGHT:** JOIN-E complete and awaiting V; JOIN-V final verdict waits on exact E SHA; DEV-R independent; no external provider/human/native lane launched.

**DELTA:** `SOURCEFREE_SAME_PERSON_ENCOUNTER_EXECUTES__COLD_NONMUTATING__REFUSAL_TYPED_HOLD__NATIVE_C12_ZERO__C11_ZERO__HUMAN_A5_NOT_RUN`.

## 4. Exact commands and results

```text
python3 -B -m pytest -q WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests -p no:cacheprovider
10 passed

# isolated J frozen test
cd vendor/j; PYTHONPATH=... python3 -B -m pytest -q tests/test_r31j.py -p no:cacheprovider
8 passed

# isolated E frozen test
cd vendor/e; PYTHONPATH=... python3 -B -m pytest -q tests/test_r31e_expression.py -p no:cacheprovider
15 passed

# isolated R30A frozen baseline
cd vendor/e/vendor/r30a; PYTHONPATH=... python3 -B -m pytest -q tests/test_r30a_first_session.py -p no:cacheprovider
10 passed
```

JUnit receipts: `evidence/junit/join_new.xml`, `j_r31j.xml`, `e_expression.xml`, `e_r30a.xml`.

Proof integrity:

```text
python3 /tmp/proof_integrity_gate_r1.py witness \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_join.py.proof.json \
  --root . --receipt WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/evidence/proof_witness.json
baseline PASS; fault_probe TARGET_ASSERTION_FAILED; grade BOUNDED_MUTATION_DETECTED
```

Closure audit: `evidence/import_closure.json` — 444 files, `problems=[]`, loaded J/E/LIVE origins all correct.

CLI: `evidence/cli_demo.json` and `DEMO_AND_VERIFICATION.md`.

## 5. Source / authority hashes and changed-path allowlist

- J source: `64fec28c374d8f77fb0b412d0c934d798ede03e8`.
- E source: `a2760d3687b063513fe0a5b9589c56c998d4ccb5`.
- `SOURCE_MANIFEST.json` SHA-256: `evidence/import_closure.json` (`manifest_sha256`).
- Positive source/target identity: `evidence/positive_receipt.json`.
- Refusal contract: `evidence/refusal_owner_contract.json`.
- Changed paths only:
  - `joined/session.py`
  - `joined/closure.py`
  - `joined/readonly.py`
  - `joined/assertion.py`
  - `joined/cli.py`
  - `joined/__init__.py`
  - `tests/conftest.py`
  - `tests/test_join.py`
  - `tests/test_join.py.proof.json`
  - `DEMO_AND_VERIFICATION.md`
  - `RESUME_CHECKPOINT.md`
  - `00_RETURN.md`
  - `evidence/**`
- No `vendor/j` or `vendor/e` file was edited. No PRE-MAIN, incumbent HQ, other worker branch or candidate dossier was touched.

## 6. NOT_RUN / limits

- External actor LLM / two-call rendering: `NOT_RUN`; zero provider calls.
- Native CAN008/CAN011/ADP019/C8/C11/C12/Pyat N11/N12: `NOT_RUN`/`HOLD`.
- Human A5: `NOT_RUN`; no recruitment or real contact channel.
- Historical 202/30 inherited test claims: not rerun; local counts are 43 executed entries (10+8+15+10) and are not a clean unique union.
- No-target E session: `HOLD_BY_OWNER_CONTRACT`; no target was minted.
- Full inherited R29P 155: `NOT_RUN`.
- Production deployment, real messaging provider, real wall-clock scheduler: `NOT_RUN`.

## 7. Final status

`COMPLETE_SOURCEFREE_CANDIDATE__AWAITING_INDEPENDENT_JOIN_V_REVIEW__NOT_NATIVE__NOT_SELF_ADOPTED`.

The exact ordinary non-force remote commit/readback is recorded in `PUBLICATION_RECEIPT.json` and returned in the final response. No self-adoption, no native grant, no HQ mutation.
