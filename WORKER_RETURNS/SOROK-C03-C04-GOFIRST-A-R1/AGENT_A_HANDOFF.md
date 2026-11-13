# SOROK #1008 C03/C04 — Agent A first-turn adversarial handoff

**Disposition:** `PARTIAL_C03_C04_SOURCEFREE_CANDIDATE__RUNTIME_NOT_RUN__G2_PARENT_VOLITION_HELD__G5_NOT_RUN`. This is a concrete code change, NOT a successful independent-parent completion. Agent B must inherit the SAME lineage and improve it; do not self-accept.

## 1. Exact artifact, lineage and commands

- Repo: `maidiu/rawlsing`.
- Issue: https://github.com/maidiu/rawlsing/issues/1008.
- Draft PR: https://github.com/maidiu/rawlsing/pull/1015.
- Branch: `agent/sorok-c03-c04-go-first-a-20261113-r1` (isolated GitHub branch; no local exclusive-worktree lease asserted).
- Immutable inherited parent: PR #996 return `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`; predecessor J1 tested-code cut `c724d1a89626f3e177acd004c0be20029dc7ade4`.
- **Frozen code + test source cut before documentary handoff:** `b70aeb1b937d937c118e150ea9a6cb73247e0013`. Exact final branch HEAD must be re-read after handoff docs. Both altered Python code files are committed at this cut.
- First changes: C04 event custody commit `f9e2a6a138fef02b0bd7c5f230f3bfb646f2e7d7`; C03 history alternatives commit `f8e2d2dadfb15391009a4e65d3f2d8ef0079cddb`.
- Changed existing owner files only:
  - `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_decision.py`
  - `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_speech.py`
- New tests/docs only under `WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/`.
- No B02/B04/B05, P3/D02/D03, J1 join, .github workflow, program constitution, or protected PRE-MAIN edits.

**Run in a real private-repository checkout with this branch's exact code, preserving existing test import roots:**

```bash
python -m pytest -q WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py
python -m pytest -q WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c03_prospectives.py
python -m pytest -q WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py
python -m pytest -q WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py
```

**Execution truth:** The four commands above were **NOT_RUN** in this session. GitHub read/write was available, but no executable private full checkout, exclusive host worktree, qualified S2 runner, or new CI workflow run was established. PR #1015's exact author-code SHA had **0 reported workflow runs and no combined status contexts** at readback. Therefore ZERO test PASS is claimed here; inherited PR #996's 221 PASS/1 SKIP are predecessor author-reported, not reproduced by Agent A. No resources/RSS/cold times/quota measurements observed.

## 2. Actual governing source contract

- Actual adopted prospective MCR-lite: `CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md@6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `9412ed317f4fbf1686d55375a4a5c795b1fc7793`. Understand → Specify → Execute → Falsify → Independently receive → Integrate. Full native/source/human rights not issued.
- SOROK `00_PROGRAMMA_SOROK.md` and `PROGRAMMA_SOROK/READ_FIRST.md` at the same protected cut. The requested `SOROK_PRODUCT_CONTROL_ROOM/READ_FIRST.md` is not present at this cut; actual compatible first door is `SOROK_PRODUCT_CONTROL_ROOM/00_READ_ME_FIRST.md`.
- Frozen original task graph `SOROK_PRODUCT_CONTROL_ROOM/ADVERSARIAL_IMPLEMENTATION_20261112_R1/03_TASK_PACKETS_R1.json@227ce149fc7864c83c179a7d3ecaef2b92c5bdab`: C03 actual parent decision/P2 act, C04 separate utterance/Nadia read, C02 work/care history, B02/B03/B04/B05 objective machinery, E01 real subsequent consumer; original adversarial personas at the same cut.
- User corrected UM-SOROK R1 `00_UM_SOROK_GOVERNING_BRAIN_AND_GROKKING_R1.md@f5c43c80675f2556e1287bf55d25052d11e8746e`, plus corrected R2 semantics, interpretive candidates only.
- PR #996 `SOURCE_DERIVATION.json`, `J1_ABI.md`, `j1_join.py`, test. Existing C03 parent decision source, C04 event writer, C01 registration, C02 actual P2 history, `model_cycle.py`, P3 D02/D03 were inspected.
- Original source-code contract requires **mother's own historically conditioned prospective activity** → distinct objective/performed world action → distinct public speech → Nadia's actual perception/P6 and D03 under her own prior organization → later genuinely performed child event. A proposed or caller-provided choice is not a performed choice.

## 3. Actual bounded code changes

### C04 — specific cause/effect repair
The old `perform_parent_utterance` replay branch checked the episode's parameters but trusted stored `receipt`; `read_parent_utterance` checked only event presence and hash. A severed parent own-speech or child receipt could still pass the replay return. The new `_verify_utterance_custody` independently checks root/branch, speaker, event ID/hash/kind/time/body/source, stored receipt, parent `own_speech` receipt, and the **admission-time** child perception channel/receipt. Replay and parent self-reader both call it. Current child's location is not retroactively substituted for admission-time hearing. No additional world event, ledger, scheduler, or native rule is introduced.

**Hostile tests committed, not executed:** exact intact replay, severed actual event, severed parent perception, severed child perception, historically unheard speech, forged speaker, forged public text, forged utterance source. The expected failure is `RecursionRefusal`, not a silent `REPLAY`.

### C03 — no more feasibility-as-will on the new reader
New `read_parent_material_prospectives(session,parent_id,as_actor=parent_id)` uses actual C02 material/history, parent feasible-action reader, the existing B03/B04 evaluation, same root/branch/clock/source consistency, and **five alternatives**: junior purchase opportunity, paid work, dependent care, debt payment, quiet nonpurchase. It returns `ELIGIBLE_NOT_SELECTED`, `MATERIALLY_INELIGIBLE` or `MATERIAL_UNKNOWN_HELD`, never `CHOSEN` or `PERFORMED`; actor selection and speech generation explicitly HELD. The read is no-write. Historical source and material-state identities are hashed; same-cash / different parent-history and changed-source spoofing are new adversarial test cases.

**Critical limit:** A bounded junior drum-kit request is STILL an existing P6 sourcefree test opportunity; it is not the mother's independent wish. The old `admit_parent_decision` and `perform_parent_decision` experimental auto-purchase path remains byte-compatible for inherited J1 tests and remains **not** an independent mother-choice implementation. The new options reader is not yet consumed by an actor-owned choice/performance operator.

## 4. Strongest source-level findings, self-attacks and repairs

- **PROVED FROM CODE BEFORE PATCH:** old C04 replay trusted persisted receipt without revalidating source/event/perception. **REPAIR CODED** and attack tests committed; RED→GREEN runtime **NOT_EXECUTED**. Do NOT call this a scientifically or independently verified fix.
- **PROVED FROM CODE:** old C03 `DECISION_RULE` selects purchase when material premises pass. Thus financially feasible→selected purchase is an **experimental selector**, not maternal intent; `request_source=CALLER_SUPPLIED_OBJECTIVE_REQUEST`. **IMPROVED** by separate truly nonselecting parent-history read; full G2 still incomplete.
- **PROVED FROM CODE:** C04 `perform_parent_utterance` accepts supplied `text` and `hidden_reason`, labels `CALLER_SUPPLIED_NOT_GENERATED`. No language-generation owner, no verified actor-authored motive. Old private-only caller-reason storage remains in historical test-only ABI; it cannot be claimed as objective psychology.
- **SOURCE REVIEW:** existing `RecursionCycle` drives owner/provider history and `situated_context` reads focal actor; D03 only offers sourcefree immediate uptake and no performed child event. None of these inspected entry points positively established the registered supporting mother as a separately qualified parent-owned choice/utterance performer. This is a specific unimplemented interface, not a broad general theory problem.
- **SOURCE AUDIT NEGATIVE:** no protected main writer changed, no private reason newly exposed to Nadia, no B04 lock or currency rewrite; test-only reader uses the same parent material source/period.
- **UNRUN PROBES:** All new Python tests and cold cases need a qualified repo checkout to be meaningful.

## 5. G1–G5 and court status

| Gate | Honest state |
|---|---|
| G1 original mother/world, identities and boundaries | `PARTIAL_SOURCE_RECONSTRUCTED`: material/history sources inspected; C03 nonselecting read coded; true independent historical organizations and mother volition unproved |
| G2 actual independent parent selection → performed B04 → C04 → P6/D03 | `HOLD_EXACT_PARENT_ACTOR_OWNER`: inherited sourcefree explicit-rule path exists; autonomous parent choice and utterance generation not established. J1 later child event separately held |
| G3 hostile factual RED→GREEN | `NOT_RUN_RUNTIME`: falsifying tests committed, no actual failure/pass commands observed |
| G4 whole-source conservation/cold/economics | `SOURCE_DIFF_SCOPED; NOT_RUN_RUNTIME`: only two permitted source-owner Python files and new test/docs; resource, lock/cold positive unobserved |
| G5 independent nonauthor receiving | `NOT_STARTED` |
| Engineering | `CODE_CANDIDATE_UNVERIFIED_RUNTIME` |
| Scientific | `SOURCEFREE_ONLY; CAN008/CAN011/ADP_RULE_A_T_NOCHANGE_MEMORY_HELD` |
| Authority | `NO_REAL_PARENT_PERFORMER_ISSUANCE; NO_NATIVE/HUMAN/SOURCE_GRANT; NO_PROTECTED_MERGE` |

## 6. Most important attacks invited for Agent B

1. **Decisive:** trace an actually qualified parent-owned prospective selector/writer in current CAN/P3/P2 or demonstrate the precise absent source/owner; replace the old auto-purchase semantics *without losing the legitimate sourcefree B04/J1 first consumers*. A new menu alone does not win C03.
2. Execute the whole branch against the real J1 root. Find real failures, including my custody helper possibly relying on an event/perception projection that is not stable across cold or forks; repair, and publish the true failing SHA/command/trace.
3. Test when an originally perceived child receipt becomes inaccessible after branch/cold, whether custody must refuse replay or preserve historically accurate admission. Challenge this with actual store semantics, not a contrived new requirement.
4. Inspect stale market/current parent sources between C03 reads and within the B04→parent lock order, plus wrong currency, unknown noise, alternate household payer, B05 rent progression and event-clock mismatch.
5. Demand an actual two-history contrast with **same present objective affordances** but different independent historical organizations. My employment-status contrast changes the mother's present work fact and does **not** prove the stronger requirement.
6. Verify old and new C04 stored private text/reason cannot reach child/public P6/D03 projections, cold replay, diagnostics or error logs. `as_actor=parent_id` is an asserted parameter rather than authenticated actor principal.
7. Test scenario where purchase is feasible and mother refuses for real actor-state reasons, not automatically because a fixed request was supplied. If no competent performer exists, return precise HOLD rather than an invented chooser.

## 7. Rejected shortcuts and proof boundaries

- No new financial personality/ambivalence/mother psyche store or a fixed motive called "parent preference".
- No hand-coded `affordable→wanted`, static childhood-trauma result, or retrospective explanation deciding a previous act.
- No branch-local source of truth replacing B02 time, B04 purchase or P3 actor state.
- No editing immutable upstream tests merely to make this candidate green.
- No pretending the inherited 221 PASS ran here; no CI, S2, cold replay, RSS or independent G5 claimed.
- No protected merge or automatic dispatch of B/other users' Browser sessions.
- I did not inspect external Library books at a new exact source cut; no source-authored psychological science claimed.

**Stop:** One first-turn code/test/doc candidate on one branch. Agent B inherits this SHA (final HEAD reverify), tests and corrects within exactly the authorized mother C03/C04 + new test/adaptor scope. Do not fan out another programme or reviewer fleet.
