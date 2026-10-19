# P41 positioned possibility service contract (VERSIONED)

**Contract:** `P41_VERSIONED_CONSUMER_CONTRACT@1` (nonauthoritative until a competent
consumer owner approves; no actor, no personhood, no route probability).
**Service:** `P41_GENERIC_POSSIBILITY_SERVICE@1` at branch
`agent/rabochii-pyat-r41-p41-generic-progressive-n10w-service-r1` from sealed
startup `c4934fd71120d37a4d06f7c830891e6e97fe4ecf`.
**Grade:** SOURCEFREE TEST_ONLY capability, bounded; NOT an N10W global
installation and NOT original-source occupancy.

## Provider interfaces (versioned; E41/W41 attach later without redesign)

| Channel | Version binding now | Future attachment |
|---|---|---|
| `n9_world` | `E04_TEST_ONLY_SELECTED_WORLD_M4_M5@1` (sealed M4/M5 + E04 catalog through `GenericSelectedWorldService.select`) | W41 `world_snapshot_and_dependency_graph.json` / `current_historical_asof_world_consumer_receipts.json` bind at the same field |
| `n10e_empirical` | `N10E_PUBLIC_SINGLE|C1_PUBLIC_MULTI_BINDING` (actual `provide_empirical_possibility_slice` / `compose_positioned_subject_possibility`) | E41 `empirical_slice_provider_contract.md` / `computed_slice_evidence.json` / `slice_consumer_receipt.json` |
| `n10w_progressive` | `E03_PROGRESSIVE_CHAIN@1` (`run_progressive_chain`, separate F8 per step) | unchanged |
| `learned_release` | `E04L_M1_M2_B5_READTHROUGH@1` (exact selected-release fact values) | unchanged |
| `n9_structural_consumer` | `NONPARENT_OPTIONS@1` (original E04 client) | unchanged |

No E41/W41 product is claimed as consumed; the version fields are explicit
binding points. A future producer replaces a bound provider only by exact
receipt reference.

## Query surface

* `progressive(target, conditions, consumer, snapshot, world_part)` — target
  `Y` (forward) or `A` (authorized reverse) only; any other target/condition
  orientation raises `TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE`. Conditioners
  are ordered exact native value bindings; re-supplying an additional
  conditioner changes the query identity and recomputes slices.
* Receipt fields: `schema`, `service`, `providers`, `query`
  (`role_class` ∈ {FORWARD_AUTHORIZED, REVERSE_AUTHORIZED}, authority refs,
  identity hash), `n9_world` (selection clocks, rules with
  revision/publication/effective dates, permission root), `n10e_steps`
  (per-depth route `N10E_PUBLIC_SINGLE`/`C1_PUBLIC_MULTI_BINDING`, state,
  denominator, cells, uncertainty, exact refs), `n10w` (chain state,
  positioned consumptions, progressive update identities), `minorities`
  (all alternatives preserved, smallest cell), `unknown` (zero-support steps,
  `NO_SUPPORTED_EVIDENCE` vs `EXACT_SUPPORT_ON_CONDITIONED_RISK_SET`),
  `structural` (routes, `route_probability = null` +
  `NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL`, actor/model call counts),
  `consumer`, `firewall`, `dependencies`, `replay_grade`, `content_hash`.
* Every value carries the TEST_ONLY source/risk/permission identity; unknowns
  are typed states with reasons, never fabricated zero.

## Consumer permission matrix

| Consumer | State |
|---|---|
| `NONPARENT_OPTIONS` (original E04 client) | ADMITTED_TEST_ONLY |
| `GENERIC_POSITIONED_SUBJECT` (native generic receiver) | ADMITTED_TEST_ONLY |
| `CONCEPTION_SCENARIO_PROPOSALS` | `CONSUMER_PERMISSION_UNISSUED` + this versioned contract |
| `SOROK_ACTOR`, `HOUSEHOLD_DYAD` | typed refusal (actor firewall / sampling-unit firewall) |

## Clocks, currentness and invalidation

Four distinct times are preserved: rule effective date, rule publication date,
requested as-of selection, and release currentness (selected / no-current).
A future-published rule cannot enter an earlier as-of selection; a declared
no-current selection refuses fresh serve while archival receipts remain
available (`archival_only = true`, `fresh_use_authorized = false`). Structural
revocation is selective (civil revocation leaves training/empirical intact);
empirical source revocation affects the consumer channel while the producer
channel state is reported separately.

## Explicit exclusions

No parent/mother/father/partner generation; no actor state; no encounter,
behavioral-route or partner-choice probability; no cross-source person
binding; no invented estimator; no supplied fixture probabilities (the
provider rejects caller probability geometry by construction).
