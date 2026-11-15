# SOROK C05 — independent nonauthor G5 receiving

**Verdict:** `REVISE_EXACT_DEFECT` (not `ACCEPT_SCOPED_SOURCEFREE_C05`)
**Issue:** C05 — continuing relations and variable-depth supporting actors
**Reviewer session:** `ses_e2186e745ffecK1Ilg4cw26pVu` — fresh nonauthor, not
author `ses_e21b02ab1ffemxs6mpCCk6TCs1`.
**Independence:** separate idle checkout and branch; no author conversation
reused; no product patch, self-review, nested agent, provider, account, global
permission, protected merge or fleet action.
**Checkout:** `/Users/matthewsmith/.codex/worktrees/sorok1038-custody-g5/Rawlsing`
**Branch:** `codex/sorok-c05-independent-g5-20261115-r1`
**Report commit:** `bc45f699a22708aae3df7e34b1ba3b272a362565`
**Frozen implementation/tests:** `9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`
**Frozen start:** `ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9`
**Prerequisite receipt:** `8bdfbdd22c19d865b5049bde8213eb3bcaea973b`
(PR 1062), scoped C04 child-facing custody + C03 material readset only; C04
parent metadata and D03 caller-receipt residuals remain held.
**Grade:** `SOURCEFREE_S2_ONLY` / `SOURCEFREE_S2_C05` scoped sourcefree receiving
only. No native ADP-015/C4, G2, J1, D04/D05, human/scientific/source-rights or
protected-merge acceptance.

## 1. Exact defect (one, in scope)

The candidate's own finite depth-1 → depth-2 promotion state machine is
inconsistent between the write path and verification. A second
`promote_relation(..., depth=2, ...)` with a **new** operation ID on an already
promoted scope is accepted by the pre-write check, appended, and only then
rejected by `_verify_scope`. The change+head write commits before the refusal,
so a normal public call permanently turns a `QUALIFIED` relation scope into
`HOLD_CUSTODY_SEVERED`.

- Pre-write check: `continuing_relations.py:1041` selects only
  `RELATION_STATE_CHANGES` (`ENTER`/`LEAVE`/`CHANGE`), so prior `PROMOTE`
  episodes are invisible and `machine["depth"]` is always 1. The
  `depth <= machine["depth"]` guard at `continuing_relations.py:1048` therefore
  does not refuse depth 2.
- Append: `_append_change` (`continuing_relations.py:839-886`) commits the
  second `PROMOTE` change and head in its own `_StoreWrite` transaction.
- Verification: `_state_machine` rejects `promoted_depth <= depth`
  (`continuing_relations.py:189-192`) and `_verify_scope` returns
  `HOLD_CUSTODY_SEVERED`; `_record_result` raises
  `RELATION_CUSTODY_SEVERED` after the commit (`continuing_relations.py:889-893`,
  called at `1071-1073` in the promotion path).
- The author's five tests only retry the **same** promotion operation
  (`test_c05_continuing_relations.py:309-318`), which returns `UNCHANGED`; no
  test uses a second promotion operation ID.

**Shortest runnable witness (independent, product read-only):**

```text
TMPDIR=$PWD/.local-logs/sorok-c05-independent-g5/tmp \
PYTHONDONTWRITEBYTECODE=1 \
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
WORKER_REVIEWS/SOROK_C05_CONTINUING_RELATIONS_G5_R1/newprobes/c05_defect_probe.py
```

Observed (`evidence/c05_defect_report.json`, exit 0):

```text
before: relation_status QUALIFIED, changes 2, heads 2, episodes 49,
        world_events 14, perceptions 42, checkpoints 33, C12 verify ok
second call: raise RELATION_CUSTODY_SEVERED (not RELATION_PROMOTION_NOT_DEEPER)
after:  relation_status HOLD_CUSTODY_SEVERED, changes 3, heads 3, episodes 51,
        world_events 14, perceptions 42, checkpoints 33, C12 verify ok
second PROMOTE: operation defect:promote:2, sequence 3, promoted_depth 2
exact retry of defect:promote:1 after the write: RELATION_CUSTODY_SEVERED
```

The write is committed (`changes +1`, `heads +1`, `episodes +2`), does not alter
world events, perceptions or checkpoints, and passes the raw C12 store
`verify()`; the relation state machine is what severs. The exact first-promotion
retry can no longer recover the scope through the public API.

**Minimum correction (owner):** compute the current depth from the full verified
change list including prior `PROMOTE` episodes (or call
`_state_machine(scope["changes"])`), and refuse
`RELATION_PROMOTION_NOT_DEEPER` **before** `_append_change`. As defense in
depth, perform the post-append verification inside the same `_StoreWrite` unit
so a verification failure rolls the write back instead of committing a
self-severing episode. Add one test: first depth-2 promotion succeeds; a second
depth-2 promotion with a new operation ID is refused with no new episode/head.

## 2. What was independently run

### Exact listed suites, once at the final frozen cut

Every command used `TMPDIR=$PWD/.local-logs/sorok-c05-independent-g5/tmp`,
`PYTHONDONTWRITEBYTECODE=1`, `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`,
`-B`, `-q`, `-p no:cacheprovider`, with `/usr/bin/time -l`; product was
read-only.

| Suite | Result | Exit | Real s | Max RSS bytes |
|---|---:|---:|---:|---:|
| `WORKER_RETURNS/SOROK_C05_CONTINUING_RELATIONS_R1/tests/test_c05_continuing_relations.py` | 5 passed | 0 | 45.14 | 63,811,584 |
| `WORKER_RETURNS/SOROK-DUEL-C01-R1/test_c01_supporting_actor.py` | 6 passed | 0 | 14.55 | 57,913,344 |
| `WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py` | 6 passed | 0 | 27.70 | 63,545,344 |
| `WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py` | 12 passed | 0 | 55.24 | 66,351,104 |
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py` | 5 passed | 0 | 14.65 | 62,291,968 |

Total 34 passed, all exit 0; literal stdout/time logs in `evidence/suite*.log`
and `evidence/suite_summary.json`.

### Independent normal/negative/cold probe

`newprobes/c05_probe.py`, exit 0, 89/89 checks pass, 179.35 s real,
54,431,744 B peak RSS, report `evidence/c05_probe_report.json`, logs
`evidence/c05_probe_stdout.log` / `evidence/c05_probe_time.log`.

It builds a real P2 world with focal root Nadia, registered parent `P`, neighbor
`O`, a live never-exposed observer `Q`, and a live never-exposed outsider `R`;
uses real `P2Owner` `ADMIT_EVENT` events at clocks 228, 234 and 240; and covers:

- `ENTER` at clock 222 exposed only to `P`/`O`; `P`/`O` `QUALIFIED`, Nadia `Q`
  and `R` `HOLD_NOT_EXPOSED` with no relation token, party ID or private value.
- Later real owner event at 228 with focal, `P`, `O`: all three `PERCEIVED`;
  `P`/`O` relation-qualified; Nadia present but relation `HOLD_NOT_EXPOSED`;
  `Q`/`R` absent from the event and relation-held.
- Later event at 234 with focal and `P` only: `O` `NOT_PERCEIVED` but still has
  its full dated relation context; relation access is not physical co-presence.
- `CHANGE` at 234 exposed to `P`/`O`/Nadia: Nadia sees only `CHANGE`,
  `history_complete=false`, `prior_exposure=HOLD_NOT_EXPOSED`; no retro-filled
  `ENTER`; `P`/`O` see both entries.
- Event at 240, then depth-2 promotion: representation depth is 1 before the
  promotion and 2 after at the same `as_of_clock` 240; the entries and
  `visible_history_hash` are byte-identical; the promotion document and
  `representation_depth` change; `as_of_clock` 239 remains depth 1; earlier
  event contexts are byte-exact; stored `ENTER`/`CHANGE` episode bytes and
  hashes are unchanged. This is a real reader difference beyond the integer
  label in the normal case.
- Late `CHANGE` exposed to `P`/`O`/`Q`: `Q` (never a participant) sees only the
  late `CHANGE`, no `ENTER`, no promotion, depth 1; Nadia does not gain the late
  entry. `LEAVE` then re-`ENTER` exposed only to `P`/`O`: `ACTIVE → LEFT →
  ACTIVE` for parties, with no retro-fill for Nadia or `Q`.
- Change primary sever and change head sever: exposed viewers become
  `HOLD_CUSTODY_SEVERED`; event access stays `PERCEIVED`/`NOT_PERCEIVED`;
  unexposed `R` is not disclosed; world snapshot, events, perceptions and
  checkpoints are unchanged; restore returns byte-exact contexts/histories.
- Fresh-process cold: exact root/clock/actors/registrations/dated
  histories/contexts/row counts; an exact cold retry of the original `ENTER`
  returns `UNCHANGED`; no registration/change/head/speech duplicates; private
  fixture values absent from cold stdout.
- C01 role extension: `SUPPORTING_ROLES = {parent, neighbor}`; parent and
  neighbor registrations; unleased `sibling` role refused; duplicate
  registration `UNCHANGED`; private state self-only; root actor list preserved;
  only the one allowlist line changed from start.
- Refusals without writes: operation reuse mismatch, missing party exposure,
  stranger exposure, future and backdated clocks, private-value leak, unknown
  actor; counts unchanged.
- Later-event seal: real owner result `REALIZED`, BP4 event hash and event-ID
  content-address verified, stored world-event hash match, owner/focal binding
  and prior event access separate.
- Private boundary: parent/neighbor/observer/outsider/relation fixture strings
  absent from actor-facing contexts, event and world; actor-facing private
  state is `NOT_READ`.

### Independent coherent append-only forgery probe

`newprobes/c05_probe.py` also constructs an `ENTER` change and its custody head
directly through the public `session.product.store.append_episode` API, without
`record_relation_change` and without any owner/source receipt for the relation.
The reader returns `QUALIFIED` and the later context is relation-aware. This is
recorded as an explicit boundary, not as an owner-authenticated relation fact:
C05 is caller-authorized sourcefree input and its `source`/head are self-hashes,
so the chain proves append-only internal custody, not who observed the relation.
It is **not** accepted as independent perception proof and does not establish
native ADP-015/C4 relation authority. See
`evidence/c05_probe_report.json` observation
`coherent_append_only_relation_accepted`.

## 3. Exposure qualification (scoped boundary)

`exposed_actor_ids` is caller-supplied and both relation parties are mandatory.
There is no owner/source receipt that qualifies relation knowledge. The reader
is explicit that relation visibility is `DATED_EXPOSURE_ONLY`; it does not label
relation knowledge as `PERCEIVED`. In the probe:

- a physically present but unexposed actor (Nadia at the first event) has
  `PERCEIVED` event access but a relation `HOLD_NOT_EXPOSED`;
- an absent/never-participant actor (`Q`) is `NOT_PERCEIVED` for the event but
  becomes relation-`QUALIFIED` only when the caller explicitly adds it to a
  later exposure; it receives no earlier entry or promotion;
- both parties are structurally in every exposure, so a party cannot be
  constructed as relation-unaware; that is an admitted caller-fixture choice,
  not a perception proof.

No owner/source receipt qualifies relation knowledge. If the original owner
reads the original contract as requiring one, that is an unmet qualification,
not a fact this candidate supplies; no new psychology or perception gate is
invented here. Accordingly, the received scope (if the depth defect were
corrected) would be
**operation/custody of caller-authorized illustrative relation facts**, not
actor perception, actor truth, native relation authority or psychology. The
caller-supplied exposure and the public append authority are boundaries, not
independent observation.

## 4. G1–G5

| Gate | Status | Basis |
|---|---|---|
| G1 source/owner/custody | `PASS_SCOPED_SOURCEFREE` | exact HEAD/branch/report/implementation/start; only `supporting_actor.py` one-line role allowlist and new `continuing_relations.py` product; test blob pinned; product unchanged between implementation and report commit; reviewer wrote only this review return and own scratch |
| G2 build/actual first consumer | `PASS_SOURCEFREE_NORMAL` | 34/34 listed tests; real P2Owner events at 228/234/240; separate parent/neighbor/Nadia contexts; 89/89 independent normal/negative/cold checks; cold exact |
| G3 falsification | `FAIL_REVISE_EXACT_DEFECT` | repeated depth-2 promotion appends a self-severing episode and permanently returns `HOLD_CUSTODY_SEVERED`; caller exposure and coherent append are disclosed boundaries; normal past-rewrite/collapse/omniscience checks pass |
| G4 boundaries/preservation | `PARTIAL_PASS_PRESERVATION__RELATION_DEPTH_STATE_MACHINE_FAILS` | C01/C04/P2 regressions pass; world/event/perception/checkpoint unchanged by relation sever and by the defect write; change/head sever restore exact; cold exact; but the claimed finite promotion state machine is not self-consistent |
| G5 independent receiving | `REVISE_EXACT_DEFECT` | one in-scope, reproducible public-writer defect; no `ACCEPT_SCOPED` |

## 5. Original C05 contract disposition

- Positive oracle — at least one other enters/leaves/changes a relationship over
  a dated period with actor-limited access: **normal path exercised** (`ENTER`,
  `CHANGE`, `LEAVE`, re-`ENTER` at actual world clocks; real later owner events;
  separate viewer contexts). Not accepted as a whole because the depth state
  machine is defective under a normal repeat promotion.
- Negative oracle — past rewritten on promotion, relationships collapse to
  child profile, or mutual omniscience: **not observed in the normal path**
  (entries unchanged, full/incomplete histories separated, Nadia partial/held,
  private state not read). The repeat-promotion defect is a new relation-custody
  failure, not a past rewrite.
- Restoration/replay — cold lineage reads the same separate actor states and
  relationship history: **passes** for the intact candidate state (exact
  snapshot, `UNCHANGED` cold retry, no duplicates). It does not recover a scope
  already severed by the defect through the public API.
- C01/C04 dependency: C01 6 passed, C04 identity 6 passed, C04 custody 12
  passed, P2 owner 5 passed. C04 scoped prerequisite receipt `8bdfbdd...` is not
  extended; parent metadata/D03 residuals remain held.
- `#1037` B05 repair remains a separate unaccepted line: not imported, not
  tested, not repaired, not generalized to C05. Its lesson (self-hash/receipt
  consistency is not proof of an actual owner operation) is reflected only in
  the explicitly scoped append-authority boundary above.

## 6. Held / not claimed

Native ADP-015/C4 relation authority, household/genealogy issuance, maternal
psychology, independent volition/autonomy, generated language, G2 mother-owned
selection, complete J1/Nadia response, D04/D05, durable acquisition, human/
scientific/source-rights receiving, protected merge, #939 restart, PYAT/Browser
actions, concurrent same-operation uniqueness and branch-fork replay remain
`HELD`/`UNOBSERVED`. Provider/checkpoint/organization/quota/cost is
`UNOBSERVED`. Timings are observations under host load, not isolated
benchmarks. No product repair or second review loop was launched.

## 7. STOP

The candidate does not earn
`ACCEPT_SCOPED_SOURCEFREE_C05@9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`.
One exact in-scope promotion/custody defect remains. Product is unchanged.
This receiving stops after the single independent pass.
