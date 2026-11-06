# Sorok developmental recursion engine — independent exact-cut review

**Reviewer:** distinct independent engineering reviewer, OpenCode DeepSeek V4.1-Flash `#max` (effective model verified from the OpenCode session record; quota **UNKNOWN**).
**Exact subject:** `41863919210021eced174ad5abdf49cb2df2042a` (parent `bffd5c2414111d923bfde0d849c050c3fac72196`).
**Protected baseline:** `33c40a315d3c231cb2021bd8e60f3261547efa62`.
**Review branch:** `review/sorok-developmental-recursion-engine-20261106-r1`.
**Write scope:** this return root only. Subject code/tests, scientific rules, protected baseline and PROGRAMMA files were not edited by this review.
**Exact-cut replay:** performed from a `git archive` copy of the subject, with the inherited P2 bootstrap's `.git` marker only. The later lead branch was inspected separately; it is not accepted here.

## Verdict

**ENGINEERING — REVISE at the integrated exact-subject scope.** The valid-path generic `BatchEngine`/`RecursionCycle` execution and the actual P2 multi-batch path are independently demonstrated, but the pre-effect negative/grounding/chronology contract is incomplete (R2/R3) and the exact subject's accessible projection is the portal user's view (R1). No integrated acceptance is issued.

**SCIENCE — HOLD.** No concrete CAN/ADP formation/coupling, original actor/human validity, or independently owned B is issued. No native psychology claim was accepted; no laundering of `MISSING_RULE` into `NO_CHANGE` was found.

**AUTHORITY — HOLD.** No protected CAS merge, Pyat/native/source grant, or human receiving is issued. No evidence of an unauthorized source-rights crossing was found. The only non-return change is the lead's append-only candidate status note in `PROGRAMMA_SOROK/10_RECONCILIATION_QUEUE...`, which does not rewrite accepted PROGRAMMA text; whether that logging action is within the lead's own scope is for the lead/receiving authority, not this reviewer to grant.

This is **REVISE, not RED**: the defects are bounded engineering/custody defects with direct repairs; the core sourcefree machinery works and the scientific/authority holds are honest. The exact subject's claim that the provider receives "actor-accessible" history is false for the P2 adapter (finding R1), which is a false-preservation defect.

## Independently demonstrated (PASS at stated scope)

- **66/66 subject tests pass** in an exact-subject scratch copy: `66 passed in 254.90s (0:04:14)`.
- **Baseline P2 suite 7/7 passes**: `7 passed in 61.22s`, confirming the unchanged #697 product behavior.
- **Cold three-process witness passes**: `BOOTSTRAP/ORDINARY/TERMINAL` exactly once each, two 3-event batches, two retrospectives, same root, clock `222 -> 258`, `provider_calls_between_events=0`, `MISSING_RULE`.
- **Hard crash/custody**: child exit 17, batch `RUNNING`, event 0 `RESERVED`/null result; recovery realizes `e1,e2,e3` through the same operation, `MISSING_RULE` preserved, `verify` true.
- **Cross-process exclusion**: shared journal/owner serializes to `a1,a2,a3,b1,b2,b3`, zero duplicate effects, `verify` true.
- **Sequential actual state**: valid two-batch P2 run carries `before == previous after`; event 2 reads the state event 1 left; cold reopen reproduces the same root/history.
- **Material cause reaches native C9**: independently severing `s.produce_interval(domain)` makes the ACTUAL/SCHEDULED contrast fail (`ACTUAL` becomes `[True,True,True]`); exact restoration makes the targeted test pass. This is a real producer→C9 consumer edge, not a narrative fixture.
- **Prior retrospective completion**: independently removing the persisted pre-next-batch retrospective block makes the targeted assertion fail (`len(retrospectives) == 0`); exact restoration passes.
- **Privacy walker**: the accepted P2 `privacy_hits` walker returns `[]` for all three realized accessible payloads; no forbidden private keys/markers found.
- **Source closure**: all 11 subject file hashes match `SOURCE_PINS.json`; the P2 product tree is byte-identical to protected baseline; #697 source `4b2fed81...` and #699 source `ab59af29...` are untouched. The architecture blob hash matches `38876f6e...`; the task hash matches `c8f91bda...`.
- **MISSING_RULE / controlled B**: P2 consequences keep `durable_psychological_transition=MISSING_RULE`; `independent_B` is explicitly `CONTROLLED_SOURCEFREE_PARTICIPANT_ONLY`. No evaluated `NO_CHANGE` laundering was found.

## Findings requiring repair

### R1 — Exact subject uses the portal user's view as "actor-accessible" experience (REVISE)

The exact subject's `P2Owner._realize` sets `accessible=self.fanin.public_opportunity(observation)` (`p2_owner.py:192`). `public_opportunity` returns `"view": self.view()` (`p2_product_fanin/integration.py:153`); `LifecycleEncounter.view()` calls `S45Projection.view()`, which calls `project_view`; `project_view` filters `session.user_perceived_ids()` (`s45_projection/projection.py:316`), and `user_perceived_ids` returns the perceptions of `USER_ACTOR` (`r30a/first_session.py:212-214`). That is the portal user U's view, not developing actor A's perception receipts.

The independent reproduction (`logs/actor-access.log`) starts the actual P2 root, realizes three events, and shows:

- root actors `('TEST_ONLY_BP1_R26V_ACTOR_A','TEST_ONLY_BP1_R26V_ACTOR_B')`, portal user `U`, action alias `A`;
- exact-subject accessible keys have **no `actor_ref` and no actor perception receipts**;
- the accessible `view` is `SOROK_WP19_ENCOUNTER_VIEW@1` with `perceived_by_user=true` on every visible event;
- actor A has 18 perception receipts, portal user U has 17, and the accessible view exposes only the 15 user-visible events.

This misses the commission's actor-limited/actor-specific requirement and makes the exact subject's 00_RETURN claim ("only actor-accessible projections") false. The later lead head `99e79810f` adds `P2Owner.actor_experience`, binds the E1/action hash, reads the developing actor's receipt alias, and refuses a missing actor receipt; its focused P2 tests pass `3 passed in 16.26s` and the integration tests pass `2 passed in 243.67s`. That repair is **outside the exact subject** and is not accepted by this review. The exact subject is REVISE; the later repaired cut needs its own exact-cut review.

**Repair:** re-review the repaired actor-experience cut; require actor receipt binding, explicit HELD when actor receipts are absent, no user-view fallback, and default CLI output that does not publish actor-private experience. Do not inherit this review's result for the later head.

### R2 — Invalid native grounding mutates interval state before refusal and poisons the batch (REVISE)

`P2Owner.validate_proposal` only checks that `circumstances` keys are in `{"history_refs","language_context"}` (`p2_owner.py:86`); it never inspects the refs. `_realize` then applies the interval first (`p2_owner.py:147-152`) and only afterwards calls `s.admit_event(..., history_event_refs=refs, ...)` (`p2_owner.py:159-161`). A nonexistent ref is rejected by native `S42_HISTORY_REF_MISSING` after the interval has changed state. The engine has a durable reservation but no completed record; the batch cannot be retried without the adapter's ambiguous-operation hold.

Independent reproduction (`logs/invalid-grounding.log`):

```
batch exception: RecursionRefusal OWNER_REALIZE_FAILED:S41EventRefusal:S42_HISTORY_REF_MISSING: does-not-exist
before clock/state 222 ...
after  clock/state 226 ...
state changed: True
history records: 0
verify: True
journal rows: [(0, 'RESERVED', None, 'S41EventRefusal:S42_HISTORY_REF_MISSING: does-not-exist')]
retry exception: RecursionRefusal P2_AMBIGUOUS_PRIOR_OPERATION_HOLD
```

The same reproduction at later lead head `99e79810f` gives the same clock `222 -> 226`, zero records, `verify=True`, and ambiguous retry (`logs/later-head-invalid-grounding.log`). This is a missed "inadequate event grounding" explicit failure and an untracked relevant state change; the exact subject's claim that the interval effect is recorded with the event result is false in this failure path.

**Repair:** validate `history_refs` (type, existence, branch/actor, ordering, no future refs) and other native-only grounding before applying the interval or committing the operation reservation; add a negative test proving state/clock unchanged, zero history records, no stuck `RESERVED`, and a clean typed refusal. If native prevalidation cannot cover a case, provide an owner-level reconciliation that records or compensates the interval result rather than leaving it untracked.

### R3 — Out-of-order batch event times are accepted before effects; the batch then sticks (REVISE)

`BatchEngine._normalize_batch` accepts any 3–5 proposals and only checks duplicate event IDs (`engine.py:229-241`). `_validate_all` calls `owner.validate_proposal` on each proposal against the *starting* state (`engine.py:617-631`). `RecursionCycle._parse_proposals` likewise only checks that `event_time` is an integer (`model_cycle.py:534-536`). None enforces nondecreasing batch chronology. In the reproduction, times `240, 230, 250` all pass the initial `> 222` check; event 1 realizes at 240, event 2 is then rejected as not future, and the batch is permanently stuck.

Independent reproduction (`logs/time-inversion.log`):

```
exception: RecursionRefusal P2_EVENT_CLOCK_NOT_FUTURE
before 222 after 240 changed True
records ['t1']
rows [(0, 'COMPLETE', 1, None), (1, 'RESERVED', 0, 'RecursionRefusal:P2_EVENT_CLOCK_NOT_FUTURE')]
retry: RecursionRefusal P2_EVENT_CLOCK_NOT_FUTURE
```

The same reproduction at later lead head `99e79810f` behaves identically (`logs/later-head-time-inversion.log`). This is a malformed batch that produces a real partial effect and a stuck `RUNNING` batch instead of a pre-effect refusal.

**Repair:** enforce nondecreasing (or strictly increasing) `event_time` for the ordered batch before any reservation/effect, either in the generic engine/coordinator or through an owner `validate_batch` hook that can preflight future events against projected state. Add a negative test proving zero owner effects, zero completed records and no `RUNNING` batch for inverted times.

## Replay receipts

| Replay | Result | Log |
|---|---|---|
| Exact-subject combined suite | `66 passed in 254.90s` | `logs/full-suite.log` |
| Unchanged P2 baseline suite | `7 passed in 61.22s` | `logs/p2-baseline-suite.log` |
| Cold three-process 3+3 CLI | same root, clock 222→258, 2 retrospectives, 0 between-event provider calls | `logs/cold-cli.json` |
| Hard crash / recovery | exit 17, RUNNING/RESERVED, 3 realized, MISSING_RULE | `logs/hard-crash.log` |
| Cross-process exclusion | a1..b3, 0 duplicate effects | `logs/cross-process.log` |
| Boundary sever | targeted assertion RED (`retrospectives` 0) | `logs/boundary-sever.log` |
| Boundary restore | targeted assertion PASS; hash `af83f8f1...` | `logs/boundary-restore.log` |
| Material sever | ACTUAL outcomes `[True,True,True]` RED | `logs/material-sever.log` |
| Material restore | targeted assertion PASS; hash `c9566d18...` | `logs/material-restore.log` |
| Invalid grounding | clock 222→226, 0 records, verify true, ambiguous retry | `logs/invalid-grounding.log` |
| Time inversion | event 1 COMPLETE at 240, event 2 RESERVED, retry fails | `logs/time-inversion.log` |
| Actor-access source | portal user U view, no actor_ref/receipts; A receipts 18 vs U 17 | `logs/actor-access.log` |
| Privacy walker | `privacy_hits=[]` ×3 | `logs/privacy-probe.log` |
| Later head invalid grounding | same defect | `logs/later-head-invalid-grounding.log` |
| Later head time inversion | same defect | `logs/later-head-time-inversion.log` |

Reproduction scripts are in `reproductions/`. The exact-subject replay was performed in a `git archive` copy so no subject file was edited. Sever/restore was performed only in that scratch copy; exact source hashes were restored and are recorded in `logs/*restore.log`.

## Source and branch closure

- Exact subject `41863919210021eced174ad5abdf49cb2df2042a`; protected baseline `33c40a...` is an ancestor.
- All 11 subject code/test hashes match `SOURCE_PINS.json`; see `SOURCE_CLOSURE.json`.
- `engine.py` and `test_engine.py` are byte-identical to batch return `68a1299f6`; `model_cycle.py` is cycle return `0d60caf` plus the lead's persisted-retrospective repair; exact restore hash `af83...`.
- P2 product/lifecycle/interval/later/projection/import-closure trees have **no diff** from protected baseline. #697 source `4b2fed81...` and #699 source `ab59af29...` are untouched.
- The only non-return change from baseline is an append-only candidate status note in `PROGRAMMA_SOROK/10_RECONCILIATION_QUEUE...`; accepted PROGRAMMA text was not rewritten. This is the lead's logging action, not a subject-code edit.
- Architecture pin `fbfc529...` is not an ancestor of the subject, but the exact blob is present and its sha256 (`38876f6e...`) matches. The task file sha256 (`c8f91bda...`) matches.
- The remote agent branch has advanced beyond the exact subject to `99e79810f` (actor-access repair plus receiving preparation). That head is outside this exact-cut verdict; its two custody defects reproduce as noted above.

## Explicit limits

- P2 is a **controlled sourcefree fixture**; no independently owned B, native CAN/ADP formation/coupling, original actor/human validity, or native psychology is accepted. The `independent_B` consequence remains `CONTROLLED_SOURCEFREE_PARTICIPANT_ONLY`.
- The retrospective provider is a file/mock transport. Proposed impressions are render proposals, not canonical memory; the exact subject has no real memory-formation consumer. This is an acknowledged science/source hold, not a green claim.
- The later lead head's actor-access repair is spot-checked only (`3` P2 tests, `2` integration tests); it is not independently accepted here.
- The inherited Pyat receiving-court RED reported by the lead at `99e79810f` was not recensused; it is unrelated to this exact subject and remains the lead's custody evidence.
- Quota was not measured: **UNKNOWN**. No UI automation, model/account/provider change, or protected/PROGRAMMA edit was performed by this review.

## Disposition

**REVISE** the exact subject. The lead should repair R2 and R3, obtain an exact-cut re-review that includes the actor-access repair at the later head (R1), and then decide protected receiving. The valid-path core machinery works; the blockers are the missing pre-effect grounding/chronology validation and the exact subject's actor-access projection.

Reviewer proposes; the Codex High lead receives at demonstrated scope. Science and authority remain HOLD.
