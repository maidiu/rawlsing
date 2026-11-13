# SOROK CG-A — Agent B independent construction against Agent A relay

**Agent B / provisional sourcefree repair, not independent receiving.**
Original obligation: [#913](https://github.com/maidiu/rawlsing/issues/913) (4 original CG-A duties); independent receiving [#914](https://github.com/maidiu/rawlsing/issues/914). Original A relay [#928](https://github.com/maidiu/rawlsing/pull/928) exact frozen HEAD `37c5842e04892421c9ce74a39956c3cdcf57f0f5`, based on B [#924](https://github.com/maidiu/rawlsing/pull/924) `0213c844b26a8e69afeea6e499fea46e13444c69`. This branch was created from A's exact final HEAD, without rewriting A, B, or protected PRE-MAIN. **No new fleet launch or #939 STOP override**; this is the explicitly user-requested standalone adversarial turn.

## 1. Independently reconstructed source/mission

CG-A must select and demonstrate exact current P2/P3 world/actor/psyche owner reuse and future compatible interfaces without pretending to implement CG-B/C/D or issue CAN/ADP/psychological science. Four obligations remain `CGA-P3-ABI`, `CGA-POSITIVE-CAPITAL`, `CGA-COLD-LATER-READ`, `CGA-CGB-CD-CONTRACT`. P4's `new` creates the P3Owner from sourcebound `case.plans`, records a `ledger["scope"]` copied from the formation plan, and stores a foreground witness that binds world and P3 state but does not bind that scope. P6 passes the mutable ledger scope to `qualified_p3_read`, whose source and registry checks validate P3 records but do **not** establish that the caller-selected project/counterpart/role/relation was originally appointed.

This is a source-custody gap in an optional `--sourcefree-p3-bridge`; not evidence that native actor intention or P3 mediator relevance is issued.

## 2. Independently preserved victories

- Agent B #924 correctly barred stale near-term context as fresh current actor access.
- Agent A #928 correctly removed fabricated sensory cue laundering via a genuine world event, requiring current `outward_cue`, the exact performed event, rederived checkpoint sensory conditions, and a `P6_HOUSE_CONDUCT` parent. It separated world and P3 historical readsets and demonstrated fail-stop (not recovery) at P4 pending after committed speech.
- Existing `projections.activate` role/relation/contradiction treatment, `P3Owner`/PsycheStore and P6 first consumer are retained. No competing scheduler, world ledger, psyche engine or authorial source substitution is introduced.

## 3. Independently identified defect — unbound P4 scope

At A HEAD, `run_p6.experience` invokes `check_source(owner)` and `check_boundary(owner, ledger)` then creates `bridge_kwargs={"psyche_owner":owner, "psyche_scope":ledger["scope"]}`. The latter is later forwarded by `situated.reconsider` to `qualified_p3_read`. `check_boundary` compares the P3/world snapshot and witness, **not** `ledger["scope"]`. Changing `ledger["scope"]["project"]` or `counterpart` to a different well-formed string makes the otherwise authentic P3 query select an unrelated or empty sourcefree history without source-plan authority. Altering role/relation similarly changes activation eligibility. World and P3 store can be identical. This is a concrete source-level execution-path defect in the discretionary foreground scope, not a claim that an external untrusted actor can already edit private local files.

A model-provided `actor_context` is not this attack. The altered scope enters from mutable local P4 receipt data, bypassing the source-issued plan selection; the original Plan source and registry have not authorized that substitution.

## 4. Productive correction

- Add `qualified_p4_scope(owner, ledger)` in the existing P6 `sourcefree_p3_bridge.py` module. Validate **exact** four-field scope against the unique, `FORMATION` source-issued P3Owner plan: `project`, `counterpart`, `interlocutor_role`, and the single `relation_refs` element. Refuse ambiguous/malformed/mismatched plans with `P6_P3_SCOPE_NOT_SOURCE_BOUND`.
- Call it **before P4 pending persistence or outward world conduct** in `run_p6.experience` whenever the sourcefree P3 bridge is explicitly enabled. Preserve unmodified original P4 behavior when the optional bridge is off. The P3 source/config has already been checked on owner reopen.
- Add `test_scope_source.py`: real P3→P6 positive; four separate tamper cases (project, counterpart, role, relation) asserting **no provider call, no pending, no world change, no P3 change**; plus unknown extra scope field. Existing A and B tests remain.
- Add an exact-head CI workflow: 6 new tests (parametrization counted), 5 A relay, 6 B bridge, 2 P3 cold/replay, 1 P4 first reader, 3 P6 situated/outward = **23 planned executions**, not 23 established passes.

## 5. Proof status — do not inflate

**Source review and authored commits completed**; file blobs and invocation order have been independently re-fetched through GitHub at candidate branch. **No executable S2 promotion**: GitHub Actions candidate runs failed with job steps `null`, and the job log URL was unavailable. No test stdout, red/green assertion, or successful runner step was retrieved. The initial pre-fix test-commit run cannot honestly be called reproduced RED; the post-fix runs cannot honestly be called GREEN. A local checkout with dependencies and a functioning runner must execute the exact planned command and the tests must be independently evaluated at the final SHA. Existing Agent A #928 successful final-head 17/17 remains evidence only for A's older head.

Workflow: `.github/workflows/sorok-cga-agent-b-scope-custody-r1.yml`. Test: `WORKER_RETURNS/SOROK-CGA-AGENT-B-SCOPE-CHALLENGE-R1/test_scope_source.py`. No native CAN, ADP, PYAT, memory, rights, scientific relevance or protected integration claimed.

## 6. Investigated and rejected challenges

- A's sensory source custody and P4 pending fail-stop remain valid; changing those to fix scope would be unnecessary and dangerous.
- `qualified_p3_read` already source-checks P3 store/registry and exact actor root/branch/clock; do **not** duplicate these checks in a new owner.
- The historically selected original P4 single formation plan is an exact present fixture, **not** a general multi-actor source law. This check refuses future ambiguity rather than installing another universal actor-scope selector.
- Missing native stimulus→mediator relevance remains held, and so is the direct in-process `qualified_p3_read(actor_observed=True)` caller-trust seam. Those are not repaired by tamper-proofing the P4 scope.

## 7. New attack surfaces and limitations

1. The new preflight assumes current sourcefree P4 has exactly one formation plan with one relation. If a future qualified P4 supports multiple formations or differently indexed actor scopes, this deliberately refuses the opt-in bridge until a source-qualified selection is issued.
2. The P4 `say` path still uses ledger scope outside this optional P6 preflight. This PR does not harden P4 globally; an owner-directed follow-up could place the same source-plan verification at original P4 scope selection if actually required.
3. P4 foreground ledger is not cryptographically sealed; unauthorized edits to other receipt fields are outside this narrow bridge guard. The world/P3 snapshot witness does not certify every mutable foreground entry.
4. P6 internal Python callers with direct access to `qualified_p3_read` still can set `actor_observed=True`. This patch does not create a new actor-access authorization token.
5. No source-qualified mapping from an authenticated present observation to a particular historical P3 mediator has been scientifically issued.
6. Crash safety remains fail-stop, not reconciliation.
7. **Runner evidence missing:** no executable green on this new code. Do not accept pending tests as validated.

## 8. Exact conservation and handoff

- `CGA-P3-ABI`: P3Owner and P2 authority unchanged; only bounded read-scope preflight.
- `CGA-POSITIVE-CAPITAL`: original B1 TEST_ONLY, old 23-row source matrix unchanged.
- `CGA-COLD-LATER-READ`: prior A/B sourcefree cold first consumer retained; new positive and tamper negatives require execution.
- `CGA-CGB-CD-CONTRACT`: CG-B/C/D new owner composition not undertaken; no parent actor/world finance or scientific rule manufactured.
- Sourcefree engineering ceiling **DELIVERED_WITH_EXECUTION_HOLD**, not `ACCEPT_SCOPED_SOURCEFREE`. Independent #914 receiving still outstanding.

## 9. Challenge to Agent A

Prove the revised source-plan check allows the authentic current P3/P6 positive and rejects each scope-only substitution *before* P4 pending/world effects, under executable real P6 code. Then try a more surgical source attack: selectively alter a scope field while retaining an otherwise admissible plan or interfere with the timing of a committed actor speech. Demonstrate whether the unguarded P4 `say` path can be exploited without changing world/P3 state, and if so repair at the correct source owner rather than stacking bridge-specific gatekeepers. Finally, independently test whether direct `qualified_p3_read(actor_observed=True)` can be made safe without fabricating native psychological relevance or creating a second state authority.

**Do not merge or represent this candidate as accepted.** The strongest remaining blocker to asserting superiority is **the lack of executable new-head test evidence**, not a demonstrated correction failure.
