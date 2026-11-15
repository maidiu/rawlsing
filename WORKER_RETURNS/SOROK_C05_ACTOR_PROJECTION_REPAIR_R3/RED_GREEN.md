# C05 R3 RED → corrected projection proof

**Base source / RED cut:** `5d771dd86767655534b23576075e5da2db4fba78`
**Base product blob:** `d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`
**Corrected product blob:** `8006440bd420ce8526bb2f333cd201ac077cbd22`
**Corrected source-256:** `a9e0595f92005fffb0c93720b7d63881994df71ed14fbbd140a723cd78f965d1`
**Hostile court:** `df4e51e75298bc1393c6f4b3640449e678bc44ff`

The three hostile probes and both helpers were copied byte-identically into
`newprobes/`; SHA-256 values equal the court’s `PROBE_PINS.json`.

| Probe/helper | SHA-256 |
|---|---|
| `c05_challenge1_leakage.py` | `b7c0a465e24e73fb1de4208264a76594932d61c8290cad5e4cdc93025da0e982` |
| `c05_challenge2_temporal.py` | `b47d0e4712c6eb8763626e801f9f1c7bb4185c403587070b68fb2c8dfc5f46f8` |
| `c05_challenge3_relation_perception.py` | `73ad97342e1a9db9bd1d9a0d0207aea62097ef62d9a0453dc74e269809a6947b` |
| `c05_r3_common.py` | `b251b3be4fa16a49d369f2596f1cdc19d1a2541ea64d06e373273304cfc92800` |
| `c05_r3_cold_child.py` | `02e89a0b265f2d152024b1bb1ed49906f19661401a55c88805278076bbe341a8` |

The probes hardcode
`.local-logs/sorok-c05-actor-view-temporal-challenge-20261115-r3` (including the
cold-child `TMPDIR`). A temporary symlink redirected it to the leased R3
scratch. Probe bytes and oracles were not edited.

## 1. Base RED (unchanged probes)

### Challenge 1 — hidden existence/cardinality

Literal exit `0`; actual RED observed:

- same event, same viewer Q, all compared actor fields equal,
- `withheld_relation_count` changes `0 → 1` in both
  `read_relation_history` and `read_actor_relative_context.relation_scope`.
- Report hash: `bfdd1d754fb253d69260a3711a7dc586fbde88d1213430bef6f75ff97ab1e0b1`.

### Challenge 2 — same-clock retrospective contamination

Literal exit `0`; witness reproduced:

- real event at clock 228; event doc/hash/access unchanged,
- ENTER and depth-2 PROMOTE appended after the event at clock 228 enter its
  relation context; later-clock CHANGE at 234 is excluded,
- no retrospective/event-time label.
- Report hash: `07d138e40d769e96d9cb5a1fd770dc77e21f99657d259503fb04be072b0c653d`.

### Challenge 3 — relation knowledge vs event perception

Literal exit `0`; actual RED observed:

- viewer P has two QUALIFIED relations and `NOT_PERCEIVED` event access;
- `context_effect.basis` nevertheless includes `C12_EVENT_PERCEPTION`;
- plural relations are present; summary is first sorted key.
- RED report hash: `cacca579a30879913b579cf38ff4eddaf94aff9bdfaaddfd4c90ba2c86e2edc3`.

Note: the first challenge-3 RED report was overwritten by the post-fix run. The
same byte-identical probe was re-executed against the base product blob to
preserve a raw RED report; the original RED stdout/time log is also retained.
This is disclosed, not concealed.

## 2. Correction

Product blob `8006440bd420ce8526bb2f333cd201ac077cbd22` changes only
`continuing_relations.py`:

1. Removed actor-facing `withheld_relation_count` from both readers and the
   nested relation scope. No controller-only count API was invented.
2. Unified absent and fully unexposed scopes to the same qualified
   `HOLD_NOT_EXPOSED` output. The new tests compare the documents exactly,
   including named queries and unexposed-relation severance.
3. Added viewer-specific `event_perception` from the viewer’s own event access;
   `C12_EVENT_PERCEPTION` is added to `basis` only when that viewer status is
   `PERCEIVED`. `relation_aware`, plural relations and the mechanical
   first-sorted summary are retained and labeled.
4. Added explicit retrospective labels:
   `relation_scope.temporal_scope = RETROSPECTIVE_AS_OF_EVENT_CLOCK`,
   `relation_temporal.event_time_relation_knowledge = NOT_AVAILABLE`,
   `event_time_relation_status = HOLD_SOURCE_AUTHORITY`,
   `within_clock_cutoff = UNAVAILABLE`,
   `usable_as_prior_event_cause = false`.
   Same-clock later relation writes remain in the retrospective context; they
   are not relabeled as event-time prior knowledge.

No product change was made outside this module. `supporting_actor.py` is
unchanged at blob `98cb4ceb3e5e201815c0ac46ba93f773601d818c`.

## 3. Post-fix unchanged-probe outcomes

| Probe | Literal exit | Actual observation |
|---|---:|---|
| Challenge 1 | 1 | Obsolete oracle raises `KeyError: withheld_relation_count`; the intentionally removed field is gone. New R3 assertions prove desired noninterference. |
| Challenge 2 | 0 | Same-clock retrospective inclusion still observed; new context explicitly labels it and holds event-time knowledge. Event doc/access remain unchanged. |
| Challenge 3 | 2 | Only obsolete `basis_includes_c12_event_perception_without_own_perception` fails; new viewer-specific `event_perception`/`basis`, plural relations, cold and private checks pass. |

Post-fix reports:
`c05_challenge2_report_POST_FIX.json`
(`4044256df12401d832a635cd49104f85014820b4d50a6489d21213543a0e1c44`) and
`c05_challenge3_report_POST_FIX.json`
(`6868143a43d277c752aff57d03875a08dde20aad5a0e2487bc84b52298a18e6c`).
Challenge 1 produced no post-fix report because its old oracle crashed on the
intentionally removed key.

## 4. New meaningful GREEN assertions

`tests/test_c05_actor_projection_repair_r3.py` — **4 passed**, exit 0, 30.41 s,
max RSS 61,845,504 B.

It proves:

- A/B same event/viewer permitted actor outputs are byte-identical with and
  without a hidden unexposed relation; named absent/unexposed queries are equal;
  hidden severance is not disclosed; visible positive relation still works;
  sever/restore and fresh-process cold are exact.
- `event_perception` is viewer-specific; a `NOT_PERCEIVED` viewer with known
  relations has no `C12_EVENT_PERCEPTION` basis, while a `PERCEIVED` viewer does;
  both simultaneous relations remain present; the singular summary is labeled
  mechanical first-sorted, not salience/psychology.
- Event document/hash/access stay immutable while same-clock relation writes
  appear only under the explicit retrospective label; later-clock changes stay
  excluded; cold replay is exact.
- ENTER/CHANGE/LEAVE history, depth promotion, same-operation retry
  `UNCHANGED`, different-operation depth-2 refusal-before-write, real P2 event
  access and private-state boundaries remain intact under the new ABI.

## 5. Preserved suites and obsolete historical assertions

| Suite | Result |
|---|---|
| C05 R3 new projection/ordering tests | 4 passed |
| C05 R2 focused promotion repair | 1 passed |
| Original C05 author suite (bytes immutable) | 3 passed, 2 failed |
| C01 supporting actor | 6 passed |
| C04 first-consumer identity | 6 passed |
| C04 custody | 12 passed |
| P2 owner | 5 passed |

The two original C05 failures are exactly the intentionally corrected actor
ABI: the old `withheld_relation_count` assertion (`KeyError`) and the old
`HOLD_UNKNOWN_SCOPE` assertion (`HOLD_NOT_EXPOSED` now intentionally
indistinguishable). They are recorded unchanged, not skipped or rewritten. The
old challenge-3 oracle similarly fails only its obsolete
`C12_EVENT_PERCEPTION`-without-perception assertion.

Timings and RSS are observations under host load, not isolated benchmarks.
Provider/token/cost and checkpoint/org/quota are `UNOBSERVED`.
