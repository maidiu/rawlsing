# SOROK R35 M35 — first-class B material source into BP2 → C12/E

**Disposition:** `TEST_ONLY_SOURCEFREE_AUTHOR_EVIDENCE__FIRSTCLASS_B_SOURCE_PRE_C8__SHARE_CREATE_REFUSAL_NO_CHANGE__SAME_E_CONSUMER_COLD__AUTHORITY_HOLD`

**Branch:** `agent/rabochii-sorok-20261024-m35-firstclass-b-source-bp2-c12-r1`
**Exact sealed startup:** `89b703e8d775b8ecd0efb2a9c1cbfa6616bc7889`
**Role:** one bounded sourcefree implementation engineer; not Sorok HQ, original CAN/ADP/science issuer, protected C8/C11/C12/native owner, production editor or independent reviewer.
**Editor/model:** OpenCode + DeepSeek V4.1-Flash, REASONING MAX requested; actual metered effort and provider quota `UNKNOWN`.
**Runtime:** macOS; Python 3.11.3; pytest 9.1.1; SQLite (local, sourcefree). No Codex, no subagent, no external provider call.

## 1. FINDING | INTERPRETATION AND RIVALS | HQ ACTION | COMPETENT OWNER

| FINDING | INTERPRETATION AND RIVALS | HQ ACTION | COMPETENT OWNER |
|---|---|---|---|
| **F1 — The B source is now a first-class BP2 input, not a producer subclass.** `bp2_joined.material_source` types B's owner, performed operation, quantity, A recipient, clock and event identity. `JoinedProducer(material_source=...)` validates it in `stage_world`, before `build_world_occurrence` and before C8. The source envelope is sealed into the C8 payload as `gm01_pre_c9_source`; `world.material_ref` and `world.material_receipt_id` are the B event ref/hash. R31J's `PreC9Producer` is not used by this path. | The original BP2 `stage_world` accepted only the BP1 life and R31J wrapped it in a subclass. The candidate instead changes the BP2 producer input itself. Alternative: a post-C8 payload append or a boolean would not make A's tool state source-owned; both are rejected by the targeted tests. | Accept scoped sourcefree engineering; keep the upstream BP2 owner contract visible. | M35 engineering + BP2 semantic owner |
| **F2 — A's material tool state is derived from B's performed operation and quantity.** `firstclass.prepare_life` sets A `tools_remaining` from `SHARE_TOOL`/positive quantity versus `REFUSE_TOOL`/zero quantity. A deliberately supplied false `gm01.material_feasible_after` does not change that state: share still gives tools 1 and C9 `CREATE`. | The stale boolean is not the source. Alternative: A's tools could come from the caller or a post-C9 overlay; the boolean-false test falsifies both for this path. | Preserve; no caller boolean in the new path. | M35 engineering |
| **F3 — Share and refusal reach the same R31E first-neighbor `do_help` consumer with different lawful outcomes.** Share+omit: C8 source share, C8 digest `e472d9…`, tools 1, `HELP_ACCEPT`. Refusal: C8 source refuse, C8 digest `5e92ae…`, tools 0, C9 `NO_CHANGE`/`NO_PROPOSAL`, no target, targetless C12, `HELP_REFUSE`. Both cold reopen and verify. | The E surface is not a B-perception claim. Refusal may lawfully refuse help; it does not imply acceptance, acquired practice or A knowledge of B's private act. The targetless refusal consumer is JOIN-E's existing derived C12 path, not a fabricated target. | Accept scoped; do not infer psychology or native C10 semantics. | M35 engineering + JOIN-E/C12 owner |
| **F4 — A performed inspection is independent of B performed share.** Share+E2 adds one admitted `material_inspect` DO, tools 0, `HELP_REFUSE`; share+omit has no admitted inspection, tools 1, `HELP_ACCEPT`. The B envelope stays `b_performed=True` share in both cases. Refusal has `b_performed=True` for the B refusal operation but zero admitted A material inspections. | Opportunity is not action; B performed is not A performed. Alternative: E refusal in share+E2 could be read as B refusing; the source/action witnesses show the A tool depletion instead. | Preserve exactly; no learned trait or ghost A inspection. | M35 engineering + ADP/action owner |
| **F5 — The source fault/restore stays on the same E consumer.** Share → valid B refusal → restored share gives `HELP_ACCEPT` → `HELP_REFUSE` → `HELP_ACCEPT`; refusal's named assertion is zero admitted `material_inspect`, and cold reopen is green. | The changed edge is before C8, with A initial state, E1, project, clock and schema held fixed. Alternative: a missing-target crash or digest-only change is not the behavioral negative; this path asserts the consumer witness. | Accept scoped fault/restore; retain the native C10 targetless contract as an owner question. | M35 engineering + JOIN-V reviewer later |

## 2. Exact evidence

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1/tests -p no:cacheprovider`
Result: **6 passed in 1.79s, exit 0** (`evidence/test_run.txt`).

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -B WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1/tools/capture_evidence.py`
Result: exit 0 (`evidence/chain.json`).

| Observation | Share | Refusal |
|---|---|---|
| B source hash | `16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486` | `3e00199d533b793897cd8b9bdc0639830252c60588de732b46dfcec3cc3b9421` |
| B operation / quantity / owner | `SHARE_TOOL` / 1 / `TEST_ONLY_OWNER_share` | `REFUSE_TOOL` / 0 / `TEST_ONLY_OWNER_refuse` |
| A recipient / B clock / A E1 | `TEST_ONLY_R31J_A` / 5 / `dac4aeb0…` | `TEST_ONLY_R31J_A` / 5 / `dac4aeb0…` |
| C8 state digest | `e472d9f9331cd827e70902232419eb0cc8dc590c9503e2f3040501eec84bb6fb` | `5e92ae09f1e97fe5d3c94234d9ce228011bf08e21bf022804ee34369e0e453c4` |
| C8 payload source equals product source | true | true |
| C8 world material ref / receipt equals B event | true / true | true / true |
| C9 | target `abd2efe9…`, `CREATE` on this fresh key | `NO_CHANGE` / `NO_PROPOSAL`, target `""` |
| C9 response / material | — | `RESPONSE_EFFECTS_VALID_EMPTY` / `NO_ELIGIBLE_MATERIAL_SOURCE` |
| A tools before E | 1 | 0 |
| E `do_help` | accepted true, `HELP_ACCEPT` | accepted false, `HELP_REFUSE` |
| Admitted A material inspection | 0 (omit) | 0 |
| Cold reopen verify | true | true |

Share+E2 independently: one admitted `material_inspect`, tools 0, `HELP_REFUSE`; B source remains share. Restored share after refusal: `HELP_ACCEPT`. Fresh local C9 IDs vary with the keyed run; they are TEST_ONLY, not historical R31J IDs.

The `gm01.material_feasible_after=False` / share-source test produced `material_access=granted`, A tools 1, C9 `CREATE` target `1567ffa4…`. This is the direct falsifier of a boolean overlay.

Source/custody hashes (`evidence/chain.json`):

```text
candidate/vendor/bp2/bp2_joined/material_source.py  8101eb3529989ddad9b9a18a5c2149b34b921a816997d1093d3d14041e8e10ba
candidate/vendor/bp2/bp2_joined/binding.py          e8ec62177e38f5946b7f493922c44b4bcbf77b2accbe89d49e378681f4a8a7bf
candidate/vendor/bp2/bp2_joined/producer.py         38a492e96eecbbeb06de7b352d7bd138a84cb3388c8441437127e6c348875970
candidate/vendor/bp2/bp2_joined/__init__.py         09b803a5add78012012281c9bf92dbb2422b408752809fce77e4eb626bd8b1f6
candidate/vendor/bp2/bp2_joined/bootstrap.py        268c3be5c6f5193246c60f2672327d359fed840ec28ddca9338dd158dfe24c6a
firstclass.py                                       29d47d30dac65e04f4bb369371a1e32a5867fd7429888337ed65d1a9a686a0d7
install.py                                          359491275da6452b392fdec7b7dfcf5a39c618d9ca2b6447150b946feb7fab88
tests/test_firstclass_b_source.py                   e9d69ed6055ef51409c34a42f213698dc144f9f052c897c686bafd4789769daa
```

Loaded closure: `bp2_joined.__file__` is under this return's `candidate/vendor/bp2`; `firstclass.JoinedProducer is bp2_joined.JoinedProducer` is true. The warm R31J BP2 staged vendor closure verifies 30/30 files (`bp2_joined.verify_sources()`; `source_manifest_sha256=1f624513d7f5591eb7418002871c9717ca430606e1205531e9f0d1d6025414da`), and no J/E/BP2 vendor file was edited or copied into this return.

## 3. What changed and what did not

Changed only under `WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1/**`:

- Added `bp2_joined/material_source.py`: typed envelope, owner/operation/quantity/recipient/clock validation, A tool derivation.
- Modified the candidate copy of `bp2_joined/binding.py` and `producer.py` to accept `material_source` in the BP2 producer and seal it before C8.
- Added `firstclass.py` (source projection, prepared A life, BP2 artifacts/product builder, C9-only builder) and `install.py` (loads the candidate BP2 before JOIN-E; reuses JOIN-E's `joined` package and patches only its source-builder names).
- Added targeted tests and `tools/capture_evidence.py`.
- Reused the warm R31J BP2 execution closure in place (`M35_BP2_VENDOR`; default path recorded in `evidence/chain.json`); no vendor bytes were copied into this return.

No production, original source, accepted authority, historical J/E/V/DEV-R branch, PRE-MAIN, HQ or Pyat edit. No original respondent data, native grant, external model, browser, listener or production activation.

## 4. Courts and disposition

| Court | Grade |
|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED_SOURCEFREE_FIRSTCLASS_B_PRE_C8__C8_C9_SAME_E_COLD__TARGETED_TESTS_PASS` — author evidence only, not independent adoption. |
| **SCIENTIFIC** | `TEST_ONLY_SYNTHETIC_MATERIAL_SOURCE__NO_PSYCHOGENESIS__NO_ACQUIRED_PRACTICE__B_ACTOR_ACCESS_UNKNOWN__H0_LIVE`. |
| **AUTHORITY** | `HOLD` — no native CAN008/CAN011/ADP/C8/C11/C12/Pyat, no production, no human A5. |

**DONE:** first-class typed B source before C8; A tool state derived from performed B operation/quantity; share → C9 CREATE and refusal → NO_CHANGE/no target; same R31E `do_help` consumer and targetless C12; cold reopen; source fault/restore; no ghost A inspection.

**REMAINING:** independent acceptance review of the exact pushed SHA; native C10 targetless semantics for refusal; protected C8/C12 custody; original CAN008/CAN011 science and accountable issuers.

**CRITICAL BLOCKER:** no native targetless C10 contract and no verified original A/T issuer. Neither is fabricated here.

**LARGEST MOVE:** one proportionate independent review of this exact sourcefree cut, with native/live remains held.

**FLIGHT:** sourcefree local only; no external provider, native lane or production.

**DELTA:** the B source is no longer a Renamed R31J subclass or a `material_feasible_after` boolean; it is a validated BP2 producer input with a source-owned C8/E consequence.

## 5. Limits / NOT_RUN

- Only the six targeted tests and the evidence capture were run. Inherited 7bf 30/30 and 5/5 independent results are history and were not recensused; the inherited R29P 155 and the 444-file corpus were not rebuilt or rerun.
- No native C8 writer/anchor, C10 target semantics, C11 weld, protected C12, CAN008/CAN011 issuance, ADP E1/E2, Pyat N11/N12, original respondent/source data, human A5, production or external model call.
- The share and refusal paths are sourcefree synthetic; no claim that B's act is perceived by A, that refusal implies help acceptance, or that any psychological/acquired-practice state exists.
- Fresh local C8/C9 IDs are keyed TEST_ONLY values; historical R31J fixed IDs are not reproduced by design.

## 6. Publication

Source commit `2d11e32c2d5e7d44449e03c6af68aa75d4de1a60` was pushed with an ordinary non-force push. `git ls-remote` read back the same SHA before the receipt-only commit; `PUBLICATION_RECEIPT.json` records that readback, and the final branch tip includes the receipt. No self-adoption, no force-push, no production or native claim.
