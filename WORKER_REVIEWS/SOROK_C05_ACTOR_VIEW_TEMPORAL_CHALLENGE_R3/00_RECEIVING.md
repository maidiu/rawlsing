# SOROK C05 — independent hostile actor-view/temporal court (R3)

**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu` — same independent C05
nonauthor; did not write the product.
**Source:** `5d771dd86767655534b23576075e5da2db4fba78`
**Final author report:** `1cf1a37113cb7a48137734648b523a0a6deccd92`
**Prior independent review preserved:** `c0cbe82f62a4e9516bf466575de3692c5c3081df`
**Checkout:** `/Users/matthewsmith/.codex/worktrees/sorok1038-custody-g5/Rawlsing`
**Branch:** `codex/sorok-c05-actor-view-temporal-challenge-20261115-r3`
**Protected PRE-MAIN:** `6a5c12f04323d74001f9632063ec907f4fc4468e` (read only)

This is a hostile TESTS-ONLY court, not a product correction, self-review,
architecture replacement or native/actor-knowledge issuance. The accepted
mechanical custody/promotion result remains intact at its prior boundary; the
new findings are contrary witnesses at the actor-facing projection and temporal
boundaries that prior review did not establish.

## 1. Actual RED / PASS / static risk / owner decision

### Challenge 1 — hidden relation existence/cardinality

Controlled fixture: one real P2 event at clock 228, same event ID/hash/access.
A = no relation; B = P/O relation exposed only to P/O; C = additionally a P/R
relation genuinely exposed to Q. Viewer Q is not a participant.

- **Actual RED:** adding the unexposed P/O relation changes Q's actor-facing
  `withheld_relation_count` from `0` to `1` in both `read_relation_history` and
  `read_actor_relative_context.relation_scope`. Every other compared actor-facing
  field is equal: status `HOLD_NOT_EXPOSED`, `relations=[]`, `context_effect`
  `{relation_aware:false, basis:["QUALIFIED_HOLD"]}`, event access
  `NOT_PERCEIVED`, same event, same viewer. Q learns hidden existence/cardinality
  from the public actor-facing reader.
- **Actual PASS:** C exposes a genuine P/R relation to Q (QUALIFIED, entry
  visible, `viewer_is_party=false`); Q still does not perceive the event; the
  hidden P/O relation stays withheld; change/head sever gives custody HOLD only
  to the exposed viewer; unexposed viewer gets no custody disclosure; restore is
  exact; fresh-process cold is exact and the hidden count persists.
- **Static risk:** the ABI previously described the count as a qualified-HOLD
  diagnostic, but there is no controller-only API/capability in the module. The
  count is in the actor-facing document.
- **Owner decision:** C05 read/projection owner. Smallest correction: remove
  `withheld_relation_count` from actor-facing documents, or expose it only
  through an explicit controller-only diagnostic. Keep status/custody/relations.
  No new psychology or ledger.

Evidence: `evidence/c05_challenge1_report.json` (checks all true; A/B equal
except the count; positive/sever/restore/cold pass).

### Challenge 2 — later same-clock relation knowledge in an earlier event

Real owner event E1 at clock 228 was read first with no relation, then after an
ENTER and depth-2 PROMOTE appended **after** E1 at the same logical clock 228,
then after a real event at 234 and a relation CHANGE at 234.

- **Actual RED:** E1's relation context changes from `HOLD_NOT_EXPOSED` to
  `QUALIFIED` (depth 2 after promotion). The event document/hash/clock and
  `PERCEIVED` access are unchanged. This is not a past rewrite, but the same
  event's actor-facing context is not event-time stable and there is no explicit
  retrospective/within-clock boundary.
- **Actual PASS:** event document/access unchanged; later-clock CHANGE at 234 is
  excluded from E1; cold replay of E1 is exact; C12 world-event seq (`14`) and
  relation episode seq (`54/56`) are separate sequence spaces; owner operations
  contain the real events but not the relation writes. The relation writes are
  caller-appended C12 self-hash change/head episodes.
- **Static risk:** `read_actor_relative_context` uses `event.clock` only
  (`continuing_relations.py:714-717`); `_representation` filters
  `body.clock <= as_of_clock` (`:459-462`); no operation/seq cutoff is consulted.
  The relation episode sequence is after the event in its own table but cannot
  supply a cross-owner ordering. The output is not labeled retrospective vs
  event-time.
- **Owner decision:** bounded projection fix: label the relation context
  `RETROSPECTIVE_AS_OF_EVENT_CLOCK` / event-time relation knowledge
  `NOT_AVAILABLE`, and do not use it as prior event cause. A true within-clock
  event-time cutoff needs a source-qualified ordering/receipt rule; that is
  `HOLD_SOURCE_AUTHORITY` for the original C05/CAN/ADP issuer. Do not ban
  retrospective understanding or rewrite E1.

Evidence: `evidence/c05_challenge2_report.json` (witness reproduced; pass
controls true; cold exact) and `evidence/c12_order_trace.txt`.

### Challenge 3 — known relation versus perceived event; plural relations

P has two qualified prior relations (P/O and P/R) and does not perceive the
current event (focal/O).

- **Actual PASS:** event access `NOT_PERCEIVED` is distinct from relation
  `QUALIFIED`; known relationship is preserved; both simultaneous relations are
  present in the plural output; the singular summary is the first relation key
  sorted, not a salience/psychology rule; cold and private-state boundaries are
  exact.
- **Static projection risk:** `context_effect.basis` includes
  `C12_EVENT_PERCEPTION` while the same document's `event_access.status` is
  `NOT_PERCEIVED` and `both_parties_event_access` is false. `relation_aware` is
  true for known relations, but the actor-facing basis is not viewer-specific
  and can be read as event-perception provenance. No product downstream consumer
  of `C12_EVENT_PERCEPTION`, `relation_aware` or `context_effect` was found
  outside the C05 module and its tests/probes; this is a projection ambiguity,
  not an executed downstream misinference.
- **Owner decision:** bounded projection fix: make `context_effect`
  viewer-specific, e.g. add `event_perception` from the viewer's own access and
  include `C12_EVENT_PERCEPTION` only when that status is `PERCEIVED`; keep
  `relation_aware` distinct. No salience selector is invented. The plural
  `relations` output remains authoritative.

Evidence: `evidence/c05_challenge3_report.json` (all checks true; cold exact).

## 2. Independent commands and raw results

Every command used the authorized Python:
`/private/tmp/rawlsing-oct28-p1r1/venv/bin/python` with
`TMPDIR=$PWD/.local-logs/sorok-c05-actor-view-temporal-challenge-20261115-r3/tmp`,
`PYTHONDONTWRITEBYTECODE=1`, `-B`. No product file was written.

| Command | Exit | Real s | Max RSS B | Result |
|---|---:|---:|---:|---|
| `newprobes/c05_challenge1_leakage.py` | 0 | 13.24 | 50,917,376 | A/B same event, only withheld 0→1; C positive; sever/restore/cold pass |
| `newprobes/c05_challenge2_temporal.py` | 0 | 11.86 | 45,944,832 | same-clock ENTER/PROMOTE enter E1 context; event unchanged; later-clock excluded; cold exact |
| `newprobes/c05_challenge3_relation_perception.py` | 0 | 5.36 | 45,039,616 | NOT_PERCEIVED vs QUALIFIED separated; basis C12_EVENT_PERCEPTION; plural present; cold exact |

Raw stdout/time logs are `evidence/c05_challenge*_stdout.log` and
`evidence/c05_challenge*_time.log`; reports and hashes are in
`evidence/challenge_summary.json`, `RECEIPTS.json`, and `PROBE_PINS.json`.

The initial Challenge-1 independent-start fixture produced different P2
admission receipts, and a copied state root was refused `SESSION_ROOT_MOVED`.
The harness was corrected to one real event/state with sequential relation
writes; no product code or oracle was changed. A Challenge-3 local KeyError was
corrected to the actual document field. Disclosed in
`evidence/HARNESS_CORRECTIONS.md`.

## 3. Exact source and boundary

Product blob `d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`, SHA-256
`72e213220ed2855a5bd303985a7a584cb14b1a3b2e704b26aa4b8161fef068d2`;
`supporting_actor.py` unchanged `98cb4ceb3e5e201815c0ac46ba93f773601d818c`.
The accepted mechanical relation write/custody and repeat-promotion
refusal-before-write fix from `c0cbe82f` remain unmodified and are not reopened.
The private-state and exposure boundaries remain caller-supplied sourcefree
fixture inputs; no owner receipt proves relation knowledge; coherent append is
not an owner signature or perception proof.

**Original full C05 actor-qualified knowledge remains `UNPROVED`.** This court
only tests the actor-facing projection/temporal behavior at the sourcefree
fixture boundary. It does not establish native C4/ADP-015, CAN/V3 science,
actor perceptions, generated language, G2 selection, J1/J2, D04/D05, human,
source-rights or protected authority.

## 4. Three separate verdicts

| Court | Verdict | Basis |
|---|---|---|
| **Engineering** | `REVISE_EXACT_DEFECT` | Actual actor-facing hidden-cardinality supply; unlabeled retrospective/event-time relation context under same-clock later writes; plus a static actor-facing `C12_EVENT_PERCEPTION` basis ambiguity for a `NOT_PERCEIVED` viewer. A bounded read-side/projection correction exists; accepted mechanical custody/promotion fix remains intact. |
| **Scientific** | `HELD` | No native actor relationship knowledge, event-time perception science, CAN/ADP/V3 rule or psychology issued. Sourcefree fixture behavior only; actor-qualified knowledge unproved. |
| **Authority** | `PASS_SCOPED_SOURCEFREE_TEST_ONLY` for this review; `HELD` for native/protected | This hostile test review is within the user lease. No protected merge, native actor/source right, human grant or source-rights issuance. |

## 5. Smallest admissible correction and next route

One bounded C05 read/projection correction in `continuing_relations.py` can
separate controller diagnostics from actor-facing output and correct the
provenance labels:

1. Remove/segregate `withheld_relation_count` from actor-facing
   `read_relation_history` / `read_actor_relative_context`.
2. Make `context_effect` viewer-specific: expose the viewer's own
   `event_perception`; include `C12_EVENT_PERCEPTION` only when that status is
   `PERCEIVED`; keep `relation_aware` as relation knowledge.
3. Label the relation context as retrospective as-of event clock (or equivalent)
   and do not use it as prior event cause. If event-time actor knowledge is
   required, the original C05/CAN/ADP source owner must issue the within-clock
   ordering/receipt decision; this is `HOLD_SOURCE_AUTHORITY`, not a new
   psychology or ledger.

Preserve the accepted mechanical custody, repeated-promotion refusal, normal
later consumer, sever/restore, cold and C01/C04/P2 results. No new salience
engine, model replacement, native knowledge grant or unbounded campaign.

## 6. STOP

One final hostile-court verdict: engineering `REVISE_EXACT_DEFECT`, science
`HELD`, authority scoped test-only/native-protected `HELD`. The original full
C05 actor qualification is not complete. HQ may route one bounded correction to
the original author and return the frozen candidate to this nonauthor; no
ongoing duel or automatic next job.
