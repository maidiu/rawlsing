# SOROK #1008 — Agent B counterbuild, C03/C04, same lineage

**Grade:** `SOURCEFREE_C04_CAUSAL_CUSTODY_REPAIR_CANDIDATE__LOCAL_ISOLATED_PROBE_PASS__FULL_S2_NOT_RUN__G2_MOTHER_VOLITION_HELD__G5_NOT_STARTED`.
**Agent position:** B follow-upper, subsequent A counter authorized independently by user. No self-acceptance, no protected merge, no #939 fleet restart.

## 1. Original target reconstructed without Agent A's framing

Original issue [#1008](https://github.com/maidiu/rawlsing/issues/1008), frozen programme and C03/C04 packets at `227ce149fc7864c83c179a7d3ecaef2b92c5bdab`, adopted MCR-lite at PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e`, and candidate UM-SOROK R1/R2 `f5c43c80675f2556e1287bf55d25052d11e8746e` govern. The missing `SOROK_PRODUCT_CONTROL_ROOM/READ_FIRST.md` path is not the guide; actual entry is `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_PROGRAMMA_SOROK.md` plus `00_READ_ME_FIRST.md`.

**C03:** A historically constituted registered mother, with existing C01/C02 identity, work/care/social and material history and qualified B02/B03/B04/B05 world constraints, must condition prospective alternatives, then actually select/attempt/refuse via an existing competent actor and P2 world owner. Financial feasibility must NOT determine maternal intent. Both parent and household funds/currency/clock/locks remain distinct.

**C04:** A distinct actually committed public speech occurrence with exact speaker/clock/root must pass actual C12/P6 Nadia perception without giving her private maternal motive, decision basis, or retrospective narrative. D03 responds under Nadia's own prior organization; prospective alternatives and D03 eligible modes are not performed actions. A different later performed child event remains a separate E01/D04/D05 held edge.

**No scientific promotion:** Native CAN/ADP Rule A/T, NO_CHANGE, memory/transfer, human actor rights and authentic independent mother-language-generation authority are unissued. Sourcefree C03/C04 engineering may still be completed to its actual demonstrated grade.

## 2. Frozen parent/provenance and what A genuinely achieved

- Parent immutable A HEAD: `0ba01215936df0b28027afe6f1596e6e610dacf7` (draft PR #1015); initial #996 J1 return `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`, earlier composition code `c724d1a89626f3e177acd004c0be20029dc7ade4`.
- A code/test cut `b70aeb1b937d937c118e150ea9a6cb73247e0013` was **not** executed in A's Browser session. The 221 PASS / 1 SKIP belong to #996 author's earlier report, not A/B.
- A's C03 `read_parent_material_prospectives` is a read-only five-possibility material/history bridge that *correctly* says no chosen/performed act and leaves real maternal selection held. It did not turn cash into a native motive.
- A's C04 repair rechecks actual event ID/hash, speaker/source, clock, stored receipt, parent own-speech and admission-time child perception on replay/self-read. That is a meaningful improvement over the earlier receipt-only replay. Preserve it.
- A correctly leaves caller-supplied `text` and `hidden_reason` labeled `CALLER_SUPPLIED_NOT_GENERATED`, never native actor language/knowledge. A's `as_actor=parent_id` is a requested self-reader label, NOT an authenticated principal.

## 3. New consequential attack: stale-hash event substitution at actual child surface

**A-world source:** `developmental_recursion/parent_speech.py` blob `9a1f602b90cb87191aca69c044ece69339b1947c`, including `_verify_utterance_custody`, `read_child_experience`, `read_child_uptake`.
**Actual event maker:** existing vendored `bp4/world.py` blob `5c4a309d376ce2bedce6a8a7e4f09768131f4d46`, `make_event`: `event_id = "TEST_ONLY_BP4_WORLD_EVT_" + digest(base)`; `event["hash"] = digest(event_without_hash)`.
**Actual outward first consumer:** `s45_projection.projection.project_event`, directly projects `location`, `summary`, and `body_public.observable` from the returned event; P6 `run_p6.child_speech_experience` calls `read_child_experience`.

A compared returned event `event_id/hash/kind/actor/clock/text/source` with persisted episode values. It never recomputed the event seal. A source-preserving attacker can return the same ID/hash, same utterance text, same source, same C12 receipts, but change `location`, `summary`, `body.observable`, or `sequence` of the object returned by `session.event`. Those are public or custody-relevant world attributes. The A-era gate accepts them by its actual field comparisons, and `project_event` trusts the altered location/summary/observable. This is a specific **cross-boundary forged world → child public projection** problem, not merely an aesthetic test.

**Executed bounded probe:** `evidence/ISOLATED_BP4_HASH_PROBE_LOCAL_20261113.txt`; source-equivalent stdlib proof passes original event and rejects four stale-hash altered-world fields plus event hash-only recompute with stale ID. This is *not* an executed integrated RED→GREEN. Real J1/P6 pytest tests have been committed but remain NOT_RUN in this host.

## 4. Implemented causal correction — minimal existing-owner repair

On isolated branch `agent/sorok-c03-c04-counterbuild-b-20261113-r1`, descended directly from A immutable HEAD:
- `parent_speech.py`: add `_verify_world_event_seal` which checks original BP4 event schema/grade/non-native identity, exact hash of all event fields except hash, and exact content-derived event ID of remaining base. Invoke after A's existing detail-specific checks on parent replay/self-read and on normal `read_child_experience` and `read_child_uptake`. Invalid event **refuses**, never mutates state to mend it.
- `WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py`: four parametrized actual-J1 / normal-P6 attacks with same stale ID/hash and changed summary, location, observable, sequence. Require refusals from replay, parent self-read, ordinary P6, and child uptake; then restore genuine event getter and require ordinary replay and child perception. Original A tests are retained verbatim.
- New bounded probe and raw isolated local execution record under `WORKER_RETURNS/SOROK-C03-C04-COUNTERBUILD-B-R1/` document the exact proof ceiling.

**No edits** to C03 code, B02/B04/B05 world/material/locks, D02/D03/P3, J1 composer, protected PRE-MAIN or live controller. Existing function and source identities stay in place.

## 5. Proof, conservation, and hostile self-attack

- GitHub exact commit compare from A HEAD to the B two source/test commits: fast-forward `ahead_by=2`, `behind_by=0`, only `parent_speech.py` (+34 lines, zero removals) and inherited `test_c04_custody.py` (+76 lines, zero removals). Later B commits add evidence/docs only.
- **Actually executed outside repo:** `python /mnt/data/c04_event_hash_probe.py` (stdlib), exit 0: A compared fields still match for 4 altered objects; new full-content/ID check rejects all 4; untouched event passes; a rehashed but stale-ID forged event refuses. Observed `/usr/bin/time`: 0.67 s, max RSS 95632 KB for that isolated Python process, not J1 economics. No provider tokens/cost observed.
- **NOT_EXECUTED at real repo:** inherited A C03 tests, A/B C04 actual-J1 tests, J1 221 suite, complete P6/D03 first consumers, cold fork/root, B05 rent/currency locking and independent G5. The private repository is reachable through GitHub connector but is not mounted as a runnable full checkout in this agent container. GitHub file writes are not substitute execution. Commands are in evidence receipt.
- **Own repair attack:** Old A actor/text/source tampering must keep its earlier precise refusal codes, so new full-event seal is placed *after* their prior checks. An unmodified event remains hash-valid. The new read-only check adds no receipt writer and preserves original historical admission-time hearing. But a legitimate future BP4 event-ID/schema migration may now fail closed unless the competent world owner versions a lawful replacement verifier; test cold/forks before treating this as accepted integration.
- **Limits:** Authentic event/episode *coordinated rewriting by a privileged store writer* is not defeated by self-hashing; source rights and durable append/commit custody remain competent owners. `session.event` monkeypatch is a hostile injected return, not proof a production attacker can remotely edit private SQLite. The vulnerability is data-integrity acceptance at the module contract, not a claimed remote exploit.
- **No fabricated alternatives:** I examined connecting `RecursionCycle` 3–5 proposals but found its current owner/validation is the focal sourcefree P3 event owner; that alone does not authorize independent C01 mother's actor-owned choice. There is no demonstrated lawful parent performer selected merely by having this module. Rather than smuggle another chooser, preserve A's honest G2 hold.

## 6. Refuted or conceded accusations

- **Concede A right:** A's admission-time child perception is the right temporal fact; current position must not rewrite the past. Preserve A's original checks and tests.
- **Concede A right:** A's five options must not be presented as autonomous parent activity; there is no legitimate reason to delete the useful reader in anger.
- **Refute attempted claim:** Matching a stored event hash to an unchanged caller-provided hash is enough to prove BP4 public event integrity. False under BP4 content-addressed maker and public projection contract.
- **Do not claim:** That the alternative chooser is solved, that C04 language is actor-generated, or that the executed isolated probe proves native S2.

## 7. Remaining exact work / G1–G5

| Gate | B evidence-bounded disposition |
|---|---|
| G1 original identity/contract/source | `PARTIAL_SOURCE_GROUNDED` — existing mother/material/history owner preserved; actual independent plural organizations/volition not proved |
| G2 actor-conditioned chosen/performed act→speech→P6/D03 | `HOLD_REAL_PARENT_ACTOR_SELECTOR` — inherited sourcefree demonstration and child reader exist, but caller purchase selector, text, motive remain externally supplied |
| G3 adversarial causal falsification | `ISOLATED_BP4_HASH_NEGATIVE_PASS; FULL_J1_TESTS_NOT_RUN` — 4 hostile actual-J1 tests committed; no real whole-host pass |
| G4 conservation/recovery/economics | `SOURCE_DIFF_CONSERVED; COLD_FULL_RUNTIME_NOT_RUN`; local isolated Python timing only |
| G5 nonauthor receiving | `NOT_STARTED`; neither A nor B can issue |
| Engineering | `SOURCEFREE_C04_CANDIDATE_REPAIR_NOT_INTEGRATION_ACCEPTED` |
| Scientific | `NATIVE_RULE_A_T_NOCHANGE_MEMORY_AND_MOTHER_VOLITION_HELD` |
| Authority | `NO_ACTOR_SCIENCE_HUMAN_RIGHTS_OR_PROTECTED_MERGE` |

## 8. Strongest challenge to Agent A

**Run the actual inherited and new tests on a real source-closed J1/P6 checkout.** Find whether a normal BP4 cold or forked event returned by `session.event` does not preserve the original maker's event-ID/hash format: if so, show exact authentic event, root, clock and legitimate source migration and repair with competent owner-specific versioning, not weakened acceptance of forged public content. Also prove no earlier A error codes regressed; self-generated synthetic tamper now must be rejected all the way through P6 and D03.

**Then attack the more consequential G2:** identify a lawful source-owned mother actor prospective/outcome performer using distinct C01/C02 prior organizations under *unchanged* objective affordances, and demonstrate an actual performed nonpurchase or purchase followed by her separately sourced public utterance. If it does not exist, return the exact functional seam; don't claim A/B C04 hash custody solves mother's independence.

**STOP for A counter; one follow-up only if an actually reproduced material break.**
