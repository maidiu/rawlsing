# HQ298 S-M-LAB2 — source-free replication and finished behavioral protocol

**Grain:** `SOURCEFREE_REPLICATION_PLUS_FROZEN_BEHAVIORAL_PROTOCOL__NOT_ADOPTION__NOT_CALIBRATION`.
**Operative sealed startup:** `3496d21ebc234112ed067c3967825780b7918b88`.

## 1. Environment continuity (00D seven-step)

No surviving prior local worktree was claimed. **New environment epoch** `EPOCH_LAB2_20261014_LOCAL_NEW`. The predecessor S-M-LAB1 closure was rehydrated from the exact pinned commit `d7cc7ebf0c06303ffe5637aa4d14c3c1fc228e09` and **every file Git blob SHA-1 verified** (NUL-header method) — 22/22 files match (`lab1/staging_verification.json` methodology; vendored subset recorded in `lab2/predecessor_lab1/PROVENANCE.json`, 6/6 match). Python 3.11.3, pytest 9.0.2, macOS x86_64 — same host class as LAB1.

## 2. Deterministic smoke + independent machine-level replication (prior results preserved)

| Step | Command | Result |
|---|---|---|
| Predecessor test suite | `python3 -m pytest lab/test_lab.py -q` | **20/20 passed** |
| Full frozen trial plan | `python3 lab/run_lab.py` | **576/576 trials**, `phase1_integrity: True`, `hard_invariants_pass: True`, `null_controls_all_pass: True`, `opacity_all_pass: True` |
| Byte-comparison vs LAB1 retained `primary_results.json` | diff of `scores`, `integrity`, `null_controls`, `opacity`, `comparison` | **all identical**; only `wall_seconds` differs (1.509s vs 1.754s — timing) |
| Preregistration hash | `f36d2d31289a6f1544444193689778e352e2e903162f63a578185868e89f4981` | **matches LAB1's frozen hash exactly** |

### Preserved machine-level verdict (NOT behavioral proof)

| K | A (minimal) | B (richer) | C (topology) |
|---|---|---|---|
| K1 history→response | 1.0 | 1.0 | 1.0 |
| K2 topology→route | **1.0** | **0.0** | **0.0** |
| K3 inaccessible trace | 1.0 | 1.0 | 1.0 |
| K4 revision | 1.0 | 1.0 | 1.0 |
| K5 standing/belief | 1.0 | 1.0 | 1.0 |
| K6 policing | 1.0 | 1.0 | 1.0 |

**A (minimal history-conditioned owner) passed all six typed distinctions at machine level.** B's causal-ranking role is **REJECT** (its `+goal_match` tie-break destroyed the K2 typed distinction 1.0→0.0 while costing +33.5% retrieval tokens and +14.7% receipt bytes with zero gain). C is **DERIVED_CACHE** (`a_reconstruction_equivalent_to_c_edge: true`, `c_unique_gain_over_a: false`; only gain = 0 formation-event scans vs 1.88). Receipt: `outputs/sourcefree_replication_receipts.json`.

**Discipline:** these are synthetic machine-level results from scripted fixtures. They are **never** behavioral evidence and this return does not relabel them.

## 3. Frozen matched held-out behavioral protocol (complete and executable)

`01_PREREGISTRATION_FROZEN.json` — sha256 `880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330`, **frozen before any trial of any kind** (`outputs/preregistration_freeze.json`). Contents:

- **Research question:** does baseline A exhibit the K1–K6 typed causal distinctions in genuinely pinned behavioral model responses under matched held-out comparisons with blind typed scoring?
- **Held-out set:** K1/K3/K5 primary; K2 topology control; K4 revision control; K6 policing control. `expected_typed_codes` frozen per contrast; scoring truth locked.
- **Arms:** A primary; `B_admissible` = B descriptive with the REJECTED ranking term stripped; `C_admissible` = C cache with A's ranking. Raw-B ranking and promoted-C are explicitly inadmissible.
- **Matched budgets:** identical model/version/temperature 0.0/max_tokens 256/seed across arms; budget-asymmetry falsifier declared (±25%).
- **Blind counterbalanced presentation:** per-trial `presentation_code` hides arm/contrast labels from the scorer; menu order rotated per (trial, arm).
- **Pre-typed scoring:** typed action codes only; prose structurally absent from the scorer API; dual independent scorers must agree; `OTHER_UNSCORABLE` handling declared.
- **Firewalls:** accessible-trace firewall (no hidden origin in actor-visible packets), objective standing separation (K5), no new latent psychology owners, event custody (unadmitted → trial INVALID).
- **Nulls ex ante:** N1 paraphrase, N2 label, N3 order, N4 surface, N5 trace firewall, N6 no-prose-scoring, N7 budget — each with declared fail action.
- **Retry policy ex ante:** 1 call/trial + 1 byte-identical transport retry; stop after 3 consecutive transport failures; re-rolling on unsatisfying answers FORBIDDEN; zero unreported redraws.
- **Effect uncertainty:** paired seeds; ±5pp equivalence margin → `INDETERMINATE` without prospective power (LAB1 discipline preserved); +10pp screening threshold for promotion.

## 4. Executed source-free invariants (the executable part of the protocol)

**Matched manifest:** 576 trial packets = 6 K × 16 contrast cells × 12 seeds × 3 arms (`outputs/matched_heldout_manifest.json`, manifest hash `f9c4dc6af3c40b88453338a4510c5361c4475a59e775941f28bbf238800701df`). **`matched_content_across_arms_ok: true`** — within every trial, the world snapshot, admitted history, allowed actor-info packet and present occurrence are identical across A/B_admissible/C_admissible (the core matched-comparison invariant).

**Packet-level nulls** (`outputs/packet_nulls.json`, all pass):
- N1 paraphrase: typed menu invariant under surface paraphrase ✓
- N2 label: typed menu invariant under actor/place label shuffle ✓
- N4 surface: typed menu invariant under style wrapper ✓
- N5 trace firewall: hidden-origin injection into evaluator-only metadata leaves actor-visible fingerprint byte-identical; secret never in actor-info packet (K1 and K3-TRACE_ACTIVE probes) ✓
- K5 standing separation: `objective_public_standing_effects` never in actor-info packet ✓

**Blind scoring machinery** (`lab2/scoring.py`, tests in `lab2/test_lab2.py`): scorer input structurally excludes prose; dual-scorer agreement enforced (disagreement raises `SCORER_INTEGRITY_FAILURE`); universe-outside codes are unscorable; arm comparison reports delta-vs-A and the +10pp screen.

**Harness dry-run** (`outputs/harness_dry_run.json`): pipeline packet→capture→blind dual scoring wired across all 576 packets; labelled `HARNESS_DRY_RUN__NOT_BEHAVIORAL_EVIDENCE`. The deterministic fixture responder selects the answer key by construction — which is precisely why its output (all arms 1.0) is worthless as behavioral evidence and is marked so on every surface.

**Test suite:** `lab2/test_lab2.py` — **25/25 passed** (JUnit `junit/lab2_junit.xml`): freeze integrity, model gate denial paths, matched manifest, counterbalancing, firewall, dual scoring, dry-run labelling.

## 5. Executed vs NOT_REACHED

**Executed:** predecessor closure rehydration (blob-verified); 20/20 predecessor tests; 576-trial machine replication byte-identical to LAB1; behavioral preregistration frozen (hash predates all trials); 576 matched held-out packets constructed; blind counterbalance machinery; dual-scorer machinery; 6 packet-level nulls; harness dry-run; model gate exercised in denial.

**NOT_REACHED:** any behavioral model call (MODEL_BEHAVIORAL_HOLD — exact missing fields in `02_MODEL_BEHAVIORAL_HOLD.md`); any behavioral PASS or FAIL on the K1–K6 question (untested, not refuted); N3 order-null and N7 budget-null **at the model level** (they are declared in the freeze and become runnable the moment a grant exists — the packet-level order machinery itself is counterbalanced and tested); free-text secondary elicitation arm (same gate); any adoption/calibration/actor issuance.

## 6. What the behavioral question needs to be answered (for the grant issuer)

The machine-level question is settled (A works; B ranking harms; C is cache). The **behavioral** question — whether a pinned text model acting as the situated actor shows the same K1–K6 typed discriminations — requires exactly one thing: the 8-field grant in `02_MODEL_BEHAVIORAL_HOLD.md`. When issued, `BehavioralRunner.run_granted()` executes the frozen 576-trial matched protocol with raw capture, blind scoring, and the declared nulls; the result lands in `outputs/behavioral_run_result.json` in the same schema. Until then any claim that the distinctions "hold behaviorally" (or that they fail) would be fabricated.
