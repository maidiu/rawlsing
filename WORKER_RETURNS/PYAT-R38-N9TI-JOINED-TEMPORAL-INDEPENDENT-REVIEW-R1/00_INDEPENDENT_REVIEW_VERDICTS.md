# PYAT R38 N9TI — Independent I2 Review Verdicts (Court A: N9J, Court B: T35)

Reviewer role: independent I2 scientific reviewer, arm's-length from both worker
returns. Base commit `68873526efe5a39a0849aa401666ac997870f156`; review branch
`agent/reviewer-pyat-r38-n9ti-joined-temporal-consumer-r1`.

Both courts were reproduced cold from their pinned immutable commits, and both
were then stressed by reviewer-authored adversarial suites that recompute the
frozen expectations from the publisher records, the hand-derived source counts,
the pinned closure preimages and the adapter/service sources themselves.

| Court | Target | Reproduction | Adversarial | Verdict |
|---|---|---|---|---|
| A (N9J) | `7628840c4c8e95b320cadc672743355afbe2958a` | 20/20 PASS (cold, 15.981 s) | 14 tests: 13 pass, 1 red (N9J-F1) | **REVISE** (bounded) |
| B (T35) | `8bfb145f7da8a2d5e6c0913919721ad4085b5d85` | 183/183 PASS (41+30+75+37) | 13 tests: 13 pass, 0 red | **ACCEPT** |

## Verdict A — N9J SELECTED-WORLD PROGRESSIVE CONSUMER: REVISE (bounded)

**Frozen-value grain: ACCEPT.** Every frozen numeric claim, count, fraction,
refusal code, revocation direction and cold-replay identity that I could
independently recompute was reproduced exactly:

* Base progressive chain recomputed from the synthetic world's cell counts:
  18/32 = 9/16 → 10/16 = 5/8 → 6/8 = 3/4; changed-source chain 19/32 → 11/16 →
  7/8; opposite-minority (A=0) chain 11/26 → 6/12 → 4/6; all match the frozen
  expectations and the served receipts.
* Zero/partial support is typed at the service layer
  (`PARTIAL_TYPED_EMPIRICAL_SUPPORT`, denominator 0, empty cells, uncertainty
  `NO_SUPPORTED_EVIDENCE`) — never a zero probability and never a fabricated
  positive completion.
* All three refusal classes reproduce: `UNREGISTERED_SELECTED_SNAPSHOT`,
  `ACCEPTANCE_BINDING_MISMATCH`, `ACCEPTED_SNAPSHOT_SUBSTITUTION`; revocation
  is directional (unrelated receipts stay servable, dependents become
  `TYPED_PARTIAL_SELECTED_WORLD`); structural-only revision leaves the
  empirical/native bytes untouched.

**Adapter-seam robustness grain: REVISE (N9J-F1, reproduced).** The delivered
R11 adapter (`642381bc033aaeef878624bdce71f9f94708043d`, staged from commit
`257dfaf41be7d2a88c11741851e9dc89363b5386`) raises an **untyped**
`KeyError('binding_order')` at `e05_n9_selected_world_adapter.py:462` when
`adapter.serve()` is asked to read a zero-support step produced by the service's
public `support_loss` mode. The service layer and the worker's own test
`test_05_zero_denominator_is_typed_not_fabricated` only exercise
`service.possibilities`; the adapter seam path is not covered by the worker's 20
green tests. This violates the adapter's own typed-refusal contract
(`N9SelectedWorldRefusal`/`SelectedWorldInconsistency` are `ValueError`s; a raw
`KeyError` is indistinguishable from a defect crash). It **fails closed** — no
zero probability and no positive completion is fabricated — so it is a bounded
robustness defect, not a falsification of any numeric claim.

The defect is already fixed upstream: the R13 adapter
(`690790e81854cde363643edc64946ddc63c58dbf` at
`84485d32c0088995f8dc664dc0517b2d27f2563d`) deep-copies the progressive steps and
types the partial receipt. Court B independently proves the R13 seam survives
the identical zero-support probe with a typed partial receipt (t12).

**Scope of REVISE:** adopt the R13 step-handling (or type the R11 seam), and add
an adapter-level zero-support regression test. No change to any frozen value,
count, fraction, refusal or clock semantics is required.

**Recorded deviation (not a defeat).** The N9J frozen hostile
`access_TRUE_fee_7_budget_5__nonparent_blocked__proposal_access_premise_only`
is not literally implementable (there is no fee-7 option; the base fee is 2). The
worker operationalized the same intent through the budget ladder (fee > budget
⇒ `BLOCKED_BY_MODELED_RULE` while `training_access` stays TRUE and the
institutional proposal stays `FEASIBLE_MODELED_PREMISE`); my Court A suite
independently reproduced that intent semantics (a13), and Court B reproduced the
same semantics independently at its own budget ladder (t03).

## Verdict B — T35 TWO-EPOCH TEMPORAL WORLD: ACCEPT

All frozen expectations were recomputed from first principles and matched, and
the complete product replays byte-identically:

* Rule identity recomputed from the publisher records: fee rev-1 = 2 published
  `2026-03-01` effective `2026-01-01`; rev-2 fee = 6 / exit = 8 published
  `2027-06-01` effective `2027-01-01`; no rev-2 for access/civil; both epochs
  select exactly the frozen revisions (t01).
* Empirical chain recomputed from the hand-derived 58-row cell counts:
  18/32, 10/16, 6/8 with source balance 4/4/4, identical across both epochs
  (t02); exact fractions cross-checked against their own numerator/denominator.
* Material affordability ladder recomputed: fee 6 blocks at budget ≤ 5 and is
  eligible at budget ≥ 6; exit 8 is resource-constrained below 8; formal
  eligibility (`training_access` TRUE) and both proposal feasibilities are
  preserved across epochs (t03).
* Clock matrix recomputed at both boundaries and the day before: fee 2/6 flips
  exactly at the effective boundary; publication boundary flips at
  `2027-06-01`; the explicit `AS_OF` control equals the `TEST_CURRENT` epoch
  (t04).
* Served receipts equal the pinned `epoch_receipts` byte-for-byte (t05), and
  the historical receipt is archival-only (`fresh_use_authorized = False`).
* Revocation matrix: civil revocation types the partial and leaves training
  eligible; fee revocation leaves the civil-only receipt servable and blocks
  training; GSS revocation leaves the typed partial native readset with NCA
  only (t06).
* All four mismatch refusals reproduce with their documented codes (t07);
  forbidden-token and authority-flag scans are clean, `actor_executions = 0`,
  `model_calls = 0` (t08).
* The full pinned closure (26 preimages) matches its own recorded blob+sha256,
  **and** every pin's blob is verified to exist at its claimed commit via
  `git ls-tree` (t09). The R13 adapter blob differs from the N9J R11 adapter
  blob, confirming the two courts exercise distinct capabilities.
* The driver redrives to a byte-identical product
  (`c4697da7e08a6920d2208e46274a0bab122ecdd334249f6268875625ea2f857b`,
  1,099,273 bytes), equal to the pinned product and to both worker cold files;
  `failed_assertions = []` (t10).
* The R13 seam survives the identical zero-support probe that reddens N9J-F1,
  producing a typed partial receipt instead (t12), and it refuses tampered
  consumer envelopes and trimmed consumer sets (t13, a capability the R11
  adapter does not have).
* Runtime transport modules contain no wall-clock/network/PID tokens (t11).

Documented limitations (not defects): the T35 freeze's
`frozen_before_executable_comparator_or_driver_code: true` is not verifiable
from Git history (freeze, runtime, tests and product all land in one commit
`71a4df6d5`); content-level consistency was verified instead. The worker JUnit
artifacts carry a sanitized hostname; counts/status are unchanged.

## Outstanding grants (unchanged, none conferred)

N5/N6 issuance; EE12; N9/OC05 installation or operative status; N10W
structural route model; Sorok C0 actor; Field Forge/actor construction; Ghana
N8E source custody; N11/N12; V3 weld. The Ghana EE12 record remains
`HOLD_SOURCE_RELEASE_METHOD_STATISTICS_AND_EE12_ISSUER` with all numerics null
and must not be read as a measured survey change.
