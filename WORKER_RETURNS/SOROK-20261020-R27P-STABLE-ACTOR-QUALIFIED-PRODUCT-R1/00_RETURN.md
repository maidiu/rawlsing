# SOROK R27P — stable historical actor to verified C12/A0 product

## Identity / custody

- Repository: private `maidiu/rawlsing`.
- Branch: `agent/rabochii-sorok-20261020-r27p-stable-historical-actor-c12-a0-product-r1`.
- Exact sealed startup: **`8a71fdab2f46adccb33843824b42ba3d2f9e7a8d`**; no R27P branch/session existed.
- Write scope: only `WORKER_RETURNS/SOROK-20261020-R27P-STABLE-ACTOR-QUALIFIED-PRODUCT-R1/**`.
- Pinned inputs: R26V `fd32e0b28349aa54a01d46a2116c7a401fde0a60` (actor code/tests), BP2P4J `5b3e6577400ea1d88971ae6b48e41a118b8059ae` (150-file origin manifest), R26E `eb0a2b90eb1bfc1f1020cc854ed8ae1243deceb6` (NOT staged/run; see NOT_RUN), BP2 `5065e2e…`, BP4 `d868e82…`.
- Model/harness: DeepSeek V4.1-Flash MAX local Git/Python/pytest/SQLite; no model/provider/subagent switch.

## FINDING / INTERPRETATION / ACTION / OWNER

| Finding | Interpretation / alternatives | ACTION | COMPETENT OWNER |
|---|---|---|---|
| R26V’s global `build_two_actor_life` monkeypatch is removed. `StableJoinedProducer` subclasses the real BP2 producer and overrides only `stage_world` with an explicitly injected `historical_life`; `bp2_joined.producer.build_two_actor_life` is unchanged before/after A→B→A runs. | The stable boundary is an owned narrow adapter because the immutable BP2 producer has no constructor hook for a life. This is not a global patch and is process/branch isolated. Alternative: upstream BP2 owner adds a constructor-injection hook. | Keep adapter; ask BP2 owner for native hook if upstream is revised. | R27P implementation + BP2 owner. |
| New R26V A/B histories (material/cash/time/birth/seed, independent B refusal, A omission) feed real BP2 C8/E1/CAN008/CAN011/C9/E2 and BP4 C12/A0/A2. Observed `ARRIVAL`, practice/tool, clock 40, `OFFSCREEN_REPAIR`, other `completed_units=5`, C12 state. | One source→user consequence, not adjacent green engines. H0 no-development remains possible; role/fixture practice is not psychology. | `ROLE_DERIVED_PRACTICE_FIXTURE_HOLD`; keep TEST_ONLY. | Sorok science/HQ. |
| Seven actor-source fault trials all PASS→RED→restored PASS under `stable_actor_binding.seven_actor_source_faults`: actor genesis/source, A omission, B independent refusal, ADP010 encounter, C8/E1 proof, A/T target/grant, independent E2. | **Only three** (A omission, B refusal, E2) turn the same A0/A2 assertion RED; actor-source, encounter, C8/E1 and A/T cuts are RED at product construction/refusal. They do not all meet the strict “same A0/A2 observation” requirement. | Extend the four construction cuts into post-construction same-assertion faults. | R27P + BP2/BP4 owners. |
| Stable A→B→A same-interpreter branch isolation works; cold subprocess stable replay works for C8/source/A0/A2/other. C12 world hash is path-bound and differs between cold roots. | C12 state is produced, but **true cold C12 reopen** and R26E corrected verifier integration were not executed. | R26E verifier/C12 reopen edge HOLD. | R26E/BP4/C12 owner. |

## Executed results

| Check | Result |
|---|---:|
| R27P stable injection/faults/cold court | **7/7 PASS** |
| Seven actor-source fault trials | **7/7 `proves=true`** (3 same-assertion, 4 construction/refusal RED) |
| Inherited R26V actor court | **10/10 PASS** |
| R26E inherited 129 | **NOT_RUN** (not staged) |
| Native ports | **10/10 fail closed** |
| Stable positive | target `f0bc4a08…`, A0 `ARRIVAL`, A2 40, other 5 |

No global actor builder mutation (`P.build_two_actor_life is original` before/after). Faults restore on a fresh good root. See `03_SEVEN_FAULTS.md`, `evidence/seven_faults_receipt.json`.

## What is not complete

- **Same-assertion seven-edge contract is not fully met.** Four cuts fail before A0/A2 construction, not at the final observation.
- **R26E corrected C12 verifier is not integrated/run.** R26E 129 tests are NOT_RUN; BP4 C12 is the real product store, but the repaired R26E verifier is not exercised.
- **True cold C12 reopen/fork** is not tested; cold is a fresh-process stable reproduction.
- **Actor-limited M6 perception/privacy** is inherited BP4 but not independently asserted here.
- Positive/NO_CHANGE/H0/refusal are present; **DENY/contradiction** are not separately implemented.
- Role-derived BP1/G18 practices/attitudes are fixture evidence, not empirical psychology.
- Native ADP007/010/015/016/017/019, CAN008 A, CAN011 T/grant, C8 D1/D2/D3, Pyat N11/N12, C11, original source, native C12: **HOLD**.

## Three courts

**ENGINEERING — REVISE.** Stable non-global injection, real BP2→BP4 product, seven faults and inherited R26V 10 execute. Full acceptance fails because four faults are construction/refusal RED rather than the same A0/A2 assertion, R26E 129/C12 verifier is not integrated, and true C12 cold reopen/fork is not proved.

**SCIENTIFIC — ACCEPT_SCOPED_TEST_ONLY.** Sourcefree historically situated activity only; H0 remains; no acquired personality from role/class/country/Enneagram/fixture. N1 eligibility is not a rule/psyche issuer.

**AUTHORITY — HOLD.** All native actor/ADP/E1/E2/CAN/C8/Pyat/C11/source/C12 authority remains unissued. No production claim.

## Artifacts

`01_STABLE_BOUNDARY.md`, `02_INHERITED_AND_NEW_COURTS.md`, `03_SEVEN_FAULTS.md`, `04_C12_N1_RECEIPTS.md`, `05_NATIVE_AUTHORITY_AND_NOT_RUN.md`, `EVIDENCE_MANIFEST.json`, `environment_passport_delta.json`, JUnit/cold logs, `evidence/seven_faults_receipt.json`, `evidence/stable_positive.json`.

Exact pushed SHA is bound in the final response after ordinary push and `git ls-remote`; no force/reset.
