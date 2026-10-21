# SOROK R30A — first neighbor session, binding actor surface and lawful return

**STATUS:** `COMPLETE_TECHNICAL_ALPHA_RETURN__RUNNABLE_LOCAL_CLI__ACTUAL_R29P_C12_M6__NO_EXTERNAL_MODEL__NO_HUMAN_A5`.
**ROLE:** independent accountable first-session technical product engineer; not Sorok HQ, R29P author, source-scientific issuer, Pyat owner, native C11/C12 authority or human A5 adopter.
**MODEL / HARNESS:** DeepSeek V4.1-Flash, reasoning MAX, I2+, user-selected OpenCode local session; one agent; no model/harness switch; no subagent dispatch. Actual external provider usage/cost: **UNKNOWN / NOT_RUN**.
**SEALED STARTUP:** `ec7b651052e6e2f0b819b0e59e07d35ced8237f2`.
**BRANCH:** `agent/rabochii-sorok-20261021-r30a-first-neighbor-binding-first-session-r1`.
**R29P SOURCE:** `agent/rabochii-sorok-20261021-r29p-actor-history-cold-c12-user-product-r1@001b506fa26ae879ff5b6e57138fc2696e12b538`.
**REMOTE SHA:** `638188fe823dde8fd74dde06690a61eeb81a89bd` — substantive publication commit; the later receipt commit is the final branch head, verified by `git ls-remote`.

## Four-column return

| FINDING | INTERPRETATION AND ALTERNATIVES | HQ ACTION | COMPETENT OWNER |
|---|---|---|---|
| **F1. Runnable first-session product exists.** `python3 -m r30a.cli` starts an already-ongoing workshop scene over actual R29P A/B material state, supports SAY/DO/ATTEND/TRAVEL/WAIT/LEAVE/RETURN, natural or user exit, outside-portal state, later message/no-message and reentry. | This is product wiring over immutable R29P, not a new native person or a canned transcript. Alternative: a browser UI or richer front-end is unnecessary for this technical gate. | Accept/reject at scoped technical grade; do not infer native or human A5. | Sorok HQ (acceptance); R30A product engineer |
| **F2. Binding occurrence precedes phenomenal presentation.** Every actor speech/gesture/material action is a C12/world event with exact text, hash and owner receipt before the user surface is composed. The user surface uses only actual U perceptions; actor/private fields are absent. | This proves the local membrane at this scope. Alternative: an external renderer would need the same typed event binding; none is claimed. | Retain as technical pattern; require the same discipline for any later renderer. | R30A + eventual renderer owner |
| **F3. Actor/world outcomes are not user commands.** Available session: A accepts help, grants contact, ends the scene, B independently repairs offscreen, A sends a late message. Pressed session: A refuses help, refuses contact, scene ends, no message. Both use the same actual R29P owner. | The difference is actual material availability (`free_hours=0` in the pressed branch), not a hidden mood or a “correct response” script. Alternative: richer actor policy is future fidelity, not this gate. | Accept scoped; do not turn template utterances into a personality claim. | Sorok HQ; R30A |
| **F4. Cold continuity and branch distinction pass.** The same SQLite C12 DB closes/reopens in new processes; same target/consumed custody; both `root` and `first_session` verify with R26E qualified preimage. A fork test shares the past and diverges post-fork. | This is genuine local logical custody, not production KMS or power-loss trust. Alternative: external witness/checkpoint archive for trailing-row deletion is future custody work. | Accept scoped cold continuity. | R29P/C12 implementation + C12 owner |
| **F5. Fault/privacy boundary responds.** 8/8 fault trials pass: committed-utterance tamper and recomputation, B offscreen removal, user-DO removal, retroactive time, hidden-state scan, ATTEND-before-access, message-without-channel. Attention focus/distraction changes surface but not event IDs/hashes. | Interior tamper/refusal is real. Trailing-row deletion remains a local-custody residual unless externally witnessed. | Retain fault matrix; schedule external witness if production custody is pursued. | R30A + C12/C8 owners |
| **F6. External LLM not run.** Deterministic local actor occurrence and phenomenal compositor only. Zero external calls, zero provider credentials, zero external charges. | Valid SOURCEFREE baseline; not a claim of generative fidelity or two-call live rendering. Alternative: future provider-authorized actor realization behind the same typed event contract. | No provider action; keep `LIVE_MODEL_NOT_RUN`. | Sorok HQ + provider authority |
| **F7. Scientific/authority ceiling.** Simulated material/relational life only; no acquired human trait, attachment, subjective awareness or A5 human evidence. Native ADP/CAN/C8/C11/C12/Pyat remains HOLD. | The scene is a technical product artifact, not psychogenesis evidence. Alternative: consented human study later, separately owned. | Do not promote; preserve H0 live. | Sorok HQ science + native owners |

## Executed evidence

- **10/10 R30A tests passed** (`evidence/junit/r30a.xml`): available/contact/natural exit/offscreen/return/cold reopen; pressed refusal/no contact/no message; attention occurrence invariance; private-state isolation; ATTEND without access; tampered utterance refusal; B-activity and user-DO removal refusal; retroactive time; fork; actor-initiated question.
- **4/4 selected R29P inherited integration tests passed** (`evidence/junit/r29p_subset.xml`): baseline/cold, M6, fork, no global builder mutation. **Full 155 inherited suite NOT_RUN**; no double count.
- **Available C12:** 21 episodes / 11 world events / 16 checkpoints / 27 perceptions; qualified verifier OK; SHA-256 `e9e05473…`.
- **Pressed C12:** 19 / 10 / 14 / 24; qualified verifier OK; SHA-256 `59a41d3f…`.
- **Cold reopen:** same target and consumed-state hash before/after; both verifies OK (`evidence/cold_reopen.json`).
- **Faults:** 8/8 (`evidence/faults.json`); attention contrast same event hashes, different surface (`evidence/attention_contrast.json`).
- **Exact source custody:** `vendor/r29p/` (178 files) + `evidence/source_manifest.json`; R29P ref `001b506f…`; live M6 blob `74d9701c…`; live guard blob `e0528d65…`.

## Commands actually run

```bash
cd WORKER_RETURNS/SOROK-20261021-R30A-FIRST-NEIGHBOR-SESSION-R1
export PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1
python3 -m pytest tests -q --junitxml=evidence/junit/r30a.xml
python3 tools/run_evidence.py
python3 -m r30a.cli --state /tmp/r30a-cli-available start --scenario available
python3 -m r30a.cli --state /tmp/r30a-cli-available say "Hello. I just moved in."
python3 -m r30a.cli --state /tmp/r30a-cli-available do help
python3 -m r30a.cli --state /tmp/r30a-cli-available ask-contact
python3 -m r30a.cli --state /tmp/r30a-cli-available wait 30
python3 -m r30a.cli --state /tmp/r30a-cli-available offscreen 30
python3 -m r30a.cli --state /tmp/r30a-cli-available messages
python3 -m r30a.cli --state /tmp/r30a-cli-available return
python3 -m r30a.cli --state /tmp/r30a-cli-available verify
```

CLI cold-process transcripts: `evidence/cli_available.txt`, `evidence/cli_pressed.txt`.

## Three courts

| Court | Verdict | Ceiling |
|---|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED` | Runnable actual R29P C12/M6 first session, binding occurrence, refusal/contact alternatives, offscreen B, cold reopen, faults. Deterministic actor realization; full 155 NOT_RUN. |
| **SCIENTIFIC** | `ACCEPT_SCOPED_TEST_ONLY__H0_LIVE` | Simulated sourcefree actor/world only; no human acquisition, attachment, awareness, health or empirical equivalence; A5 NOT_RUN. |
| **AUTHORITY** | `HOLD` | Native ADP actor/other/E1/E2, CAN008/CAN011, C8, native C11/C12, Pyat N11/N12/R53, production renderer and real human study remain unissued. |

## NOT_RUN / limits

- External LLM/provider call and two-call live architecture: `LIVE_MODEL_NOT_RUN`.
- Full 155 inherited R29P tests: NOT_RUN (4-test subset passed).
- Human A4/A5 study: NOT_RUN, no recruitment; see `05_HUMAN_VALIDATION_PLAN.md`.
- Real contact/message delivery, production deployment, native C12/C11/C8, ADP/CAN science, Pyat world: HOLD.
- Deterministic actor utterances, one workshop/market ecology, one B offscreen event, local TEST_ONLY channel.
- Local C12 custody residual (same-user DB/witness; trailing-row deletion needs external witness).
- No production code outside this return subtree, no R30G consumption, no raw respondents, no real user data.

## Readback

`evidence/github_api_readback.json`: **PASS 6/6** at `638188fe8…`; returned bytes equal local `00_RETURN.md`, `01_PRODUCT_README.md`, `evidence/c12_available.sqlite`, `evidence/cli_available.txt`, `evidence/faults.json` and `evidence/junit/r30a.xml`.

## Publication

`638188fe823dde8fd74dde06690a61eeb81a89bd` — exact ordinary non-force push tip for the substantive return, verified by `git ls-remote` and GitHub API readback (6/6 files byte-equal). The final branch head adds the readback receipt and is reported in the worker response.
