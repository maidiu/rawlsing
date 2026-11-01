# PROGRAMMA SOROK — P0/P1 Living Reference Engineering R1 — Return

**Status:** `P0_P1_FIRST_VERTICAL_SLICE_IMPLEMENTED__AUTHOR_TESTED__NOT_INDEPENDENTLY_ACCEPTED`
**Whole scope:** `WHOLE_SCOPE_NOT_YET_PROVEN`
**Operating state:** `WORKING_CANDIDATE_NOT_HQ_ADJUDICATED`

## Baseline and final identity

| Item | Exact value |
|---|---|
| Engineering branch | `codex/programma-sorok-p0-p1-engineering-20261101` |
| Verified initial HEAD | `a89e5ccbe67400168aaea8367f7aa00ca0de7625` |
| Verified remote initial HEAD | same; branch was not advanced |
| Implementation commit | `93945e4b4539fd5d5e39805d7d1f35d2325a2cbd` |
| Final remote SHA | reported by terminal push readback; a file cannot contain the SHA of the commit that contains it |

No force-push, reset of another checkout or PRE-MAIN mutation occurred. Other
worktrees/sessions were preserved. The original O-LIVE branch was not occupied.

## Model / harness / effort observed

- Harness: OpenCode CLI, local S2 filesystem/Python/pytest/subprocess execution.
- Model selected by the session runtime: `opencode-go/deepseek-v4.1-flash`.
- Provider/account: user's existing configured OpenCode account; not changed by
  this worker.
- Effort request: MAX from the launch. The harness did not expose a separate
  independent effort telemetry field; this return does not claim a verified
  runtime effort beyond the session configuration.
- No worker/reviewer/controller/model call was launched by this implementation.

## Changed paths (scoped)

Under `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1/`:

- `living_reference.py` — trust boundary, journal replay, CAS/recovery, typed
  dependency classification, prerequisite restoration, P1 views, maturity,
  Whole-Program Gaps, HTML generation, new CLI commands.
- `evidence_store.py` — append-only hash-chained journal, idempotent event IDs,
  truncation/tamper detection.
- `programma_p1_seed.py` — source-backed P1 objects, typed edges, maturity and
  gap records.
- `r2_live_transaction.py` — disposable demo; temp-only writes; operating-file
  byte comparison; synthetic-review and synthetic-return probes.
- `initialize_r3.py` — clean R3 reconstruction and quarantine manifest.
- `probe_faults.py` — real subprocess stale-CAS/concurrent-append/interrupted-
  write/cold-reload probes.
- `test_living_reference.py` — corrected synthetic-intake expectation and
  baseline counts.
- `test_living_reference_r2.py` — baseline counts, restoration expectation,
  current-ref check correction.
- `test_p0_trust_repair.py` — 16 focused P0 tests.
- `test_p1_whole_program.py` — 12 P1 traversal/maturity/gap tests.
- `00_START_HERE.md` — R3 status, commands, trust boundary and limits.
- `HISTORICAL_DEMO_QUARANTINE.md` — quarantine pointer.
- `state.json`, `SNAPSHOT.json` — derived clean operating state.
- `evidence/journal.jsonl` — canonical append-only stream (4 events).
- `quarantine/historical_demo_contamination/` — exact contaminated R2 state,
  snapshot and receipt bytes plus manifest/README.
- `r2_live_transaction.json` — left byte-identical as historical receipt; exact
  copy and SHA-256 are in quarantine.

Under `WORKER_RETURNS/PROGRAMMA_SOROK_P0_P1_LIVING_REFERENCE_ENGINEERING_R1/`:

- `00_RETURN.md` and `PUSH_RECEIPT.json`.
- `evidence/` actual outputs: pytest, manifest verifier, home, Whole-Program Gaps,
  focus/maturity, source verification, journal, HTML, disposable demo, fault
  probe, CLI trust probes, real-return intake and `QUERY_OUTPUTS.md`.

## What was repaired (P0)

1. **Disposable demo.** `r2_live_transaction.py` now writes only a temp state,
   snapshot and receipt. It hashes operating state, snapshot, journal and the
   historical root receipt before/after and observes them byte-identical.
2. **Quarantine and clean rebuild.** The contaminated R2 state/snapshot/receipt
   bytes are preserved under quarantine with exact SHA-256. The clean state is
   deterministically rebuilt from frozen seeds plus the append-only journal.
   Excluded events are inventoried with reasons:
   `R2_DEMO_H0003` synthetic S5 withdrawal, `R2_DEMO_H0004`/`H0005` self-declared
   review/engineering acceptance, `R2_DEMO_H0006` repair after the synthetic
   chain, `R2_DEMO_H0007` synthetic requirement/repeated-a SHA, `R2_DEMO_H0008`
   unverified owner grant. None are relabelled as acceptance.
3. **Fixture-origin refusal.** Synthetic/demo or `fixture_origin` evidence cannot
   promote review, engineering, authority, science, human or consumer axes. In
   operating replay the event is refused before mutation.
4. **Acceptance gate.** Promotion requires a distinct reviewer principal/role,
   distinct author, exact subject SHA (real commit), assertion, scope, appointment
   or intake evidence in the immutable review record, and an immutable review
   record reference. Self-written `reviewer_role`/`PASS`, unrelated genuine SHAs,
   stale subjects, self-authored principals and fake/selfhashed record refs fail.
   A real JOIN-V record is verified at its exact `7bf2da3` scope without migrating
   acceptance to native C9/C12 or another root.
5. **Canonical journal and reducer.** One append-only hash-chained journal is the
   canonical evidence/change stream. `state.json`/`SNAPSHOT.json` are derived.
   Duplicate event IDs are idempotent; withdrawal events are recorded; truncation
   and payload tamper fail closed. Local hashes are explicitly not external
   custody.
6. **CAS and recovery.** Journal append is locked and retains stale-writer events
   without loss; state writes use revision compare-and-swap; interrupted/truncated
   state is recoverable from the journal. Cold replay is deterministic.
7. **Prerequisite recomputation.** Restoration re-evaluates all active required
   prerequisites. A second independent RED remains; unrelated valid paths remain.
   Only explicit `REQUIRED_CAUSAL` edges block. Hypothesis, alternative, mention,
   association, source-location and missing-edge relations do not.

## What was built (P1)

Same persisted reference, actual CLI/HTML outputs:

- `home`, `focus`, `zoom`, `lateral`, `alternatives`, `maturity`, `whole-gaps`,
  `owners`, `code`, `evidence`, `history`, `work-now`, `journal`,
  `verify-journal`, `verify-sources`, `html`.
- Home begins with the unchosen-neighbor purpose, independent Astra experience,
  100/101 constraints, terminal obligations, blocked/held frontiers, source
  freshness, `KERNEL_UNRESOLVED` and `WHOLE_SCOPE_NOT_YET_PROVEN`.
- Maturity lens I/T/A/E/C/V is attached to substantive objects and gaps, with
  MISSING, UNKNOWN, UNREAD, PROPOSED, REVIEWED_NEGATIVE, SUPERSEDED and
  NOT_REQUIRED_WITH_REASON statuses.
- Whole-Program Gaps group by purpose/domain and expose parent obligation, exact
  evidence/cut, missing stages, alternatives, dependencies, affected consumer,
  competent owner, smallest next action and falsifier.
- Generated static HTML from the same state: `evidence/html/programma_home.html`.

Twelve demonstrations are implemented and tested: unchosen neighbor/Astra/100/101/
P1-or-missing/A5; Q-GAME/Q-ACTION historical closure; Q-HEALTH/SPD-0003
flourishing vs attachment with S13/S14 and missing evaluator; historical V3
external consumers vs current M6/GT0 blocked; P1 same-B access/no-access and
distinct HELP_REFUSE causes; JOIN-V scoped acceptance with C9/C12 holds; RRIF F1
→ F2 → partial first consumer; withdrawal/restoration with second RED; disposable
demo attacks; real W1-A return intake at exact SHA; 101 occurrence vs perception
and call-count alternatives; queued High vs observed Low, READY vs RUNNING, dated
Library continuity and no automatic redispatch.

## Commands and observed results

```sh
cd SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1
python3 -m pytest -o addopts= -q -p no:cacheprovider \
  test_living_reference.py test_living_reference_r2.py \
  test_p0_trust_repair.py test_p1_whole_program.py
```

Observed: `51 passed in 70.80s` (exit 0). Inherited 23 cases remain included;
the corrected cases are explained below.

```sh
python3 verify_source_manifest.py
```

Observed: `PASS`, 144 Sorok rows, 3 references.

```sh
python3 living_reference.py verify-sources
```

Observed: `PASS`, 80 local refs verified, 3 external refs not re-read locally,
0 failures.

```sh
python3 living_reference.py verify-journal
```

Observed: `PASS`, 4 events, head
`22565fd2a79b1d40cb0d67a546edd4cd417b10ee33d8af366f0de1b147be8d84`.

```sh
python3 r2_live_transaction.py
```

Observed: operating files unchanged `true`; self-review
`PENDING_INDEPENDENT_ACCEPTANCE`; synthetic requirement
`QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE`; withdrawal/restoration preserves second
RED; cold digest equal; tamper `STATE_DIGEST_MISMATCH`.

```sh
python3 probe_faults.py
```

Observed: two concurrent subprocess appends retained 3 events with stale flags
`[false,true]`; interrupted state recovered from journal; cold digest equal.

Actual query artifacts are in `evidence/`; `QUERY_OUTPUTS.md` summarizes them.

## Test corrections (not defect preservation)

- `test_intake_new_requirement_is_visible_and_old_history_preserved` encoded the
  unsafe synthetic-return promotion. It is replaced by
  `test_synthetic_intake_is_quarantined_and_cannot_create_operating_gap`.
- `test_source_withdrawal...` expected blind `CANDIDATE_READY`. It now expects
  the recorded preregistered baseline and verifies no invalidated consumer.
- Exact 198/423 and 212/649 counts were generalized to constants because the same
  reference now includes the P1 whole-program slice; the original counts remain
  the pre-P1 baseline.
- The current-ref test no longer requires an old R3 review branch head; it
  verifies the old negative is not used and the observed ref is real.

## Excluded historical demo evidence

Exact bytes and SHA-256 are in
`quarantine/historical_demo_contamination/MANIFEST.json`. The contaminated root
receipt remains byte-identical and is pointed to by
`HISTORICAL_DEMO_QUARANTINE.md`. No synthetic review is treated as independent
acceptance.

## Source-read depth

- Full text read by this worker: the existing commission, Step2 commission,
  W1 joint synthesis, W1-A/B/C/D/E substantive 00 and 02 returns, O-LIVE code and
  tests, 01 charter, 05 Program Map, Astra STRATA_MAP, P1 plain-English product,
  JOIN-V return, RRIF F2 return, exact Q/SPD rows, selected D002/24/100/101/CAN011/
  M6/GT0/PRE-MAIN sections, local external V3 call-chain files, controller R63
  records via authenticated GitHub API read.
- Partial/selected: original 03, 24, 100, 101, CAN008, original V3 modules beyond
  the call-chain files, W1 atomic records beyond locator checks.
- NOT read: entire 00–103 estate, every Q/D/R row, full original V3 archive,
  full books/theory corpus, fresh native Library state, all other active branches.
- The local external V3 copy hashes differ from W1-C's recorded member hashes;
  this is represented as `V3_EXTERNAL_MEMBER_HASH_MISMATCH`, not conflated.
- Dated Library continuity is `REPORTED_NOT_ACCESSED_NOW` at
  `2026.10.31.17.40`; no fresh native Library read was substituted.

## Remaining gaps and owners (representative)

- S5/Q-HEALTH-001 flourishing measurement and harmful-attachment evaluator:
  `SOROK_ORIGINAL_SCIENCE_OWNER` / `SOROK_ALPHA_OWNER`.
- CAN011 positive practice-acquisition Rule T vs `MIDDLE_STATE_UPDATE_RULE_MISSING`:
  `CAN011_OWNER` / `ADP_OWNER` / `C9_C12_OWNER`.
- Original V3 yearly/persona migration and current consumer: `ORIGINAL_V3_SOURCE_OWNER`
  / `C11_OWNER`.
- S13 non-extractive revenue, S14 privacy/abuse, S11 accessible encounter UX:
  respective product/business/safety/UX owners.
- Human A5: `SOROK_ALPHA_OWNER`; blocked by native C11/C9/C12 and ethics.
- Sorok 101 two-call actor/phenomenal implementation: `C11_OWNER` / `V2_OWNER`.
- RRIF F2 native same-root consumer and C9/C12 anchor: `C9_C12_OWNER` /
  `PREMAIN_RECEIVING_OWNER`.
- Controller observed effort/lease truth: `CONTROLLER_OWNER` / `SOROK_HQ`.
- Full estate population and source breadth: `SOROK_HQ`; whole-scope not proven.

## Three separate verdicts

**ENGINEERING — author-tested behavior; no independent self-acceptance.**
P0 trust repairs and P1 views are implemented and pass the inherited plus focused
author suites, including subprocess/cold/CAS/interrupted-write probes. This is
author evidence only. No independent reviewer accepted this exact returned code.

**SCIENTIFIC — represented evidence/alternatives; no new psychological law.**
The reference preserves source-backed competing accounts (Leontiev, Lahire,
Archer, Sève, CAN008/CAN011, Court 10, P1 TEST_ONLY) and labels missing theory,
evaluators and human evidence. It issues no new developmental rule, CAN/ADP/SCI05
grant or native psychological claim.

**AUTHORITY — candidate reference scope; no native/human/PRE-MAIN adoption.**
The reference is a candidate operating instrument. JOIN-V acceptance remains at
its exact `7bf2da3` scope; P1/RRIF remain TEST_ONLY/PARTIAL; C9/C12/C11/Pyat/human
A5/native science remain HELD or MISSING. No controller activation, pre-main merge,
production deployment or owner adoption is claimed.

## Stop condition

`WHOLE_SCOPE_NOT_YET_PROVEN` remains explicit while the broader estate remains
unpopulated. This return completes the P0/P1 first vertical slice, not the whole
Programma and not the Sorok developmental person.
