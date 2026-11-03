# SOROK-LIVE-02 — scoped implementation return

> **Execution update (2026-11-03):** The `S2_NOT_RUN` boundary below records the original authoring session. Execution was later performed at content SHA `bbcc46bf3b7aadfc582e284daea61f99060e0fc3`; see `05_EXECUTED_TEST_RECEIPT.md`, `06_COLD_REPLAY_AND_SEVEN_VIEW_RECEIPT.md`, `07_ADVERSARIAL_FINDINGS_AND_REPAIRS.md`, and `08_FINAL_DISPOSITION_AND_HQ_HANDOFF.md`. Independent review and HQ adoption remain NOT ISSUED.

**Disposition: `IMPLEMENTED_ON_ISOLATED_BRANCH__SOURCE_INSPECTED__S2_NOT_RUN__INDEPENDENT_REVIEW_AND_HQ_ADOPTION_PENDING`.** This is not an execution-pass claim. A working Python runtime, secure Git worktree or authorized S2 runner was not available to this connected GitHub session; consequently code has been authored and committed, source identities have been checked, and adversarial pytest tests have been written, but the tests and cold CLI executions have **not** been performed.

## Exact boundaries

- Private repository: `maidiu/rawlsing`.
- Starting branch: `codex/programma-sorok-p0-p1-repair1-20261102`; its **observed** HEAD at launch was `fa8a2b1f75cd2ee2153a813215f51dea88e16a4b`, matching the commission's specified immutable base.
- Exclusive implementation branch: `agent/sorok-programma-live-update-adapter-20261103-r1`, created directly from that 40-hex SHA.
- Frozen W8-R guide: `a9ebf71e62d84e5dcc599662e976eca7fcd0e623` (`00/06–15` read-only; the adapter reads `14`/ `15` at this cut).
- Execution host: ChatGPT connected authenticated private GitHub source/API, **not** a verified Codex/mainMac Python S2 runtime. Model: GPT-6; requested High effort, actual selected effort and quota telemetry **not independently observable** here. No provider/model/editor switch or paid account action was initiated.
- This session previously examined PROGRAMMA/Sorok guide material, so cannot be the later **independent** reviewer of its own implementation. It is an implementation/source inspection return, not an independent acceptance report.

## The smallest extension

The existing P0/P1 engine is retained. `living_reference.py` still owns the canonical evidence store, derived state, gaps, source verification, work-now and original CLI; `evidence_store.py` remains unchanged.

**New `live_update_adapter.py`:** validates a typed `SOROK_PROGRAMMA_DELTA@1` against the actual Git object `commit:path:blob`, an exact source quote, known existing P1 node/owner, W8-R original guide ref, bounded sourcefree claim and exact code first-consumer symbol or explicit NONE. A returned candidate cannot be admitted against an unrelated real Git file. JOIN-E scoped positive review must bind the actual JOIN-V record and exact `7bf` subject/root using the pre-existing `_verify_acceptance_record`; S35 stays an authored test-only source with no native first consumer; RRIF-R2's `8090` independent `REVISE_MATERIAL_DEFECTS` remains a separate exact negative at `598d`.

**Minimal integration inside `living_reference.py`:** one `PROGRAMMA_DELTA` replay case, an opt-in strict expected journal head/CAS gate (legacy append behavior preserved for other commands), duplicate identity idempotency with mismatched-body refusal, and a derived `programma_live` section inside the same state/work-now response. Replaying the journal recomputes that section; the adapter does **not** create a new state database, copy original guide records, or claim a daemon. A caller-written withdrawal cannot silently erase a delta event from journal replay. Existing P0/P1 typed source withdrawal/restoration remains separate.

**Read views:** `whole`, `focus X@stage`, `source-to-product X@stage`, `goal X@stage`, `work-now`, `changes-since <SHA|event|transition>`, `freshness`, and `candidate-patch`. They read the pre-existing purpose/gaps/code-consumer functions and the pinned guide's exact 83 phase gates/127 leaves/38 seams, then show exact receipts, owner/negative/first consumer/next evidence and conditional reverse targets without treating a syntactic prerequisite as an issued target. `living_reference.py work-now` also includes the new section once a qualified delta is ingested.

**No silent guide mutation.** The only generated guide effect is a proposed `candidate-patch` data readback for HQ; W8-R `00/06–15` is untouched. Original science, Pyat, human product and privacy operations remain owner/issuer-held.

## Files changed on the exclusive branch

Within `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1/`:

- `living_reference.py`: narrow integration and strict CAS, replay/withdrawal guards.
- `live_update_adapter.py`: typed validation, source-scoped intake, phase/edge/work-now projection and entering-agent query CLI.
- `test_live_update_adapter.py`: source-cut-real adversarial tests written, not run.
- `fixtures/join_e_scoped_review.json`, `fixtures/s35_authored_sourcefree.json`, `fixtures/rrif_r2_negative.json`: exact source/owner/consumer/scope receipts.
- `00_START_HERE.md`: provisional usage, immutable source preflight and isolated journal-backed GENESIS.

Under this sole worker return directory: `00_IMPLEMENTATION.md`, `01_ACTUAL_SOURCE_AND_REUSE_LEDGER.md`, `02_TEST_MATRIX_AND_COMMANDS.md`, `03_ENTERING_AGENT_READBACKS.md`, and `04_HQ_INTEGRATION_PATCH_CONTRACT.md`.

**Unmodified:** `evidence_store.py`, `initialize_r3.py`, source/seed registry, `state.json`, `SNAPSHOT.json`, actual `evidence/journal.jsonl`, all W8-R guide files, HQ/PRE-MAIN and original Sorok/Pyat science.

## Evidence grade and stop

**Performed:** authenticated GitHub branch/source/ref checks, actual selected code-body reading, immutable source blob observations, static comparison of changed paths and JSON fixtures, and creation of code/test/doc artifacts. **Not performed:** Python syntax import, pytest, subprocess S2, file-lock/concurrent writer execution, clean detached worktree, native source grant/actor, real participant, independent review.

Do **not** claim the commissioned “working scoped adapter and cold proof” acceptance condition from this report alone. The code is ready **for** one S2 cold court to test and minimally repair if needed, not self-accepted. The remaining S2 test commands and precise acceptance requirements are in `02`. If S2 passes at the exact source cut, a different reviewer judges and HQ decides adoption. No new graph, scheduler, agent dispatch, daemon, product runtime or broad reconnaissance is authorized.
