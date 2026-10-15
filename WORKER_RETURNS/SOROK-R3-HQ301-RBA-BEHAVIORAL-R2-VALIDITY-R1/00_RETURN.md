# HQ301 RBA — independent R2 behavioral assay validity review

**Recommendation: `REVIEW_PASS_SCOPED_MOCK_PROTOCOL`.** Never `BEHAVIORAL_PASS`. No model-use permission, actor authority, semantic adoption, or production authority is issued by this review.

**Terminal:** `RBA_R2_MOCK_PROTOCOL_VALIDATED__53PLUS4_SCOPES__ZERO_LEAKS__ZERO_BYPASS__ZERO_LIVE_CALLS__NO_ADOPTION`.

## 1. Custody and identity

- Repository: private `maidiu/rawlsing`. Review branch
  `agent/reviewer-sorok-r3-hq301-rba-behavioral-r2-validity-r1`, created at sealed
  startup `f035191192ed709b09209a7e2e629f7ac6ec54a7` (direct remote read matched
  before any work). No reset or force-push at any point.
- Role: independent I2 reviewer. Not candidate author, Sorok HQ, model-use
  issuer, actor, or adopter. This review does not self-adopt anything.
- Candidate: HQ300 BEH R2 `a7d2be9894bf92f81356adf14141136666e63bd1`
  (`WORKER_RETURNS/SOROK-R3-HQ300-BEHAVIORAL-ASSAY-R2-RECONSTRUCTION-R1/`).
  Baselines: LAB1 `d7cc7ebf0c06303ffe5637aa4d14c3c1fc228e09`, LAB2
  `bf5fda102f4bced41a0f18f71c4c380d5d099462`, R1 RMB
  `bf7518cff877ce108ef9c07f2e2eeaf990171d08`.
- **Executing agent disclosure (00D honesty):** the dispatch names Codex /
  GPT-6.1 High. The agent actually performing this review is Muse Spark in the
  present local session (OpenCode-style harness, macOS darwin, Python 3.11.3).
  No model switch was available or performed mid-task; no GPT-6.1/Codex identity
  is claimed. All deterministic evidence below (reruns, hashes, JUnit) is
  model-independent by construction; the I2 interpretation is the reviewer's own.
- Write terrain: this return directory only. No candidate, commission, owner,
  CURRENT, or PRE-MAIN file was modified.
- ZERO real behavioral model calls, ZERO actor runs, ZERO original-survey reads
  in this review. Socket connect is denied by test fixture in every suite run.

## 2. What was independently reproduced (commands + receipts)

All runs use blob-verified staged copies under `staging/` (manifest
`staging/staging_manifest.json`, 48 objects) executed from `exec/` mirrors.
Frozen v6 sha256 reproduced: `9a05efd9cc4060a7ae9b496f6fe71a5193912b228ac0d2e04577f80902384823`.
R1 prereg sha256 reproduced: `880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330`.

| Suite | Command (from return root) | Result | Receipt |
|---|---|---|---|
| R2 entrypoint 51 | `pytest exec/r2/test_r2.py -q --junitxml=repro/r2_review_run.xml` | **51 PASS** | `repro/r2_review_run.xml` |
| LAB1 unit 20 | `pytest exec/lab1/lab/test_lab.py -q --junitxml=../../repro/lab1_review.xml` | **20 PASS** | `repro/lab1_review.xml` |
| LAB1 machine 576 | `python3 exec/lab1/lab/run_lab.py` | **576 trials; scores/integrity/null_controls/opacity/comparison all equal** to original | `exec/lab1/outputs/primary_results.json` |
| LAB2 suite 25 | `pytest exec/lab2/lab2/test_lab2.py -q --junitxml=../../repro/lab2_review.xml` | **25 PASS** | `repro/lab2_review.xml` |
| RMB original 36 | `pytest exec/rmb/test_independent.py -q --junitxml=../../repro/rmb_review.xml` | **13 PASS / 23 RED, exact original failing set** | `repro/rmb_review.xml` |
| RBA hostile 19 | `pytest hostile/test_hostile_rba.py -q --junitxml=repro/hostile_review.xml` | **19 PASS** | `repro/hostile_review.xml` |
| Full mock sweep | `python3 exec/r2/run_experiments.py rba_review_run1` + `audit_outputs.py` | 10,800 lawful + 21,600 total captures; all six phases verified | `exec/r2/receipts/rba_review_run1/` |

Per-suite verdict ledger: `02_verdict_matrix.json`.

## 3. Independent hostile findings

**H1–H4 packet custody (all PASS).** Full serialized provider packets for all 126
cases × 3 arms carry no K/contrast/arm/expected labels, no hidden-origin bytes,
no origin-bearing event IDs, no grant/issuer/signature objects. All case, event
and trial IDs are 32-hex random, not `K__contrast__seed` lookup keys. (One probe
iteration initially flagged the English substring inside the lawful fixture value
`"specific_authority"`; structural key/object inspection confirms no grant or
issuer object — recorded as a probe-calibration note, not a leak.)

**H5–H6 arm liveness (all PASS).** A/B/C representations differ on all 126
matched cells by implemented intervention (owner scan vs descriptive streams vs
evidence index), while the lawful fact sets are byte-identical across arms.

**H7–H9 K3/K5/K6 semantics (all PASS).** K3: current trace effect visible,
origin content absent, evaluator `mistaken`/`confident_mistaken` labels never
reach actor testimony (mapped to claim + LOW/HIGH confidence). K5: public
notice, private prior and belief/standing reports are distinct slots. K6: actual
position/capacity facts present with True/False contrast; NO_SANCTION retained
in K6 menus.

**H10–H11 oracle attack (all PASS).** A lawful-structure, content-corrupted key
is refused by the frozen-key channel; the separately implemented
rejection-rule channel independently refuses the same forgery. The two channels
are distinct code paths (`proposed_key` vs `check_key` + adjudicator), but they
share one author — agreement is cross-validation, **not** independent custody
(see §5).

**H12–H14 schedule/menu/pairing (all PASS).** 10,800 unique trial IDs; 3,600
cells each with one shared menu and all three arms; all six arm-order
permutations present; every row carries OTHER_UNSCORABLE. Observation (not a
failure): permutation counts are unbalanced (1440 vs 432) and rows-per-case are
78/96; pairing is exact within-cell so point estimates are unaffected, but a
position-sensitive responder could interact with order — the first-option
control is the guard.

**H15–H16 grant gate and ledger (all PASS).** Untrusted issuer class, tampered
signature, LIVE mode, unregistered transports all denied at construction.
Ledger relocation/removal after binding denied; truncation → LEDGER_ROLLBACK;
partial-line journal fails closed; completed-trial redraw refused.

**H17 intervals (PASS).** Paired-interval code contains the bounded-mean
machinery; recompute (below) confirms the math.

**H18–H19 transport surface (PASS).** No network/provider/subprocess imports in
`assay/`; unregistered policies denied at construction.

**Independent paired recompute** (`hostile/recompute_paired.py`, own join/score
code): 3,600 matched blocks, exact joins, B−A = 0.0 and C−A = 0.0 on all six
families, interval [-1,1] (vacuous at n=6). First-option control independently
verified: B−A deltas zero on 2,592 blocks at 0.361 overall correctness.

**Adversarial counterexample (required): the mock responder is arm-blind.**
`respond()` reads only `facts`, `menu`, `response_id` — never the arm-produced
`representation`. Paired B−A/C−A = 0.0 is therefore **guaranteed by
construction**, and the intervals cannot discriminate treatments. The candidate
discloses exactly this ("correctness_fraction_plumbing_only", MOCK_ONLY,
INDETERMINATE equivalence) — confirmed, not contradicted. Consequence: this
protocol validates plumbing, fail-closed transport and hostile robustness; it
is structurally incapable of validating the treatment-effect claim. Any future
live assay must have the responder actually consume arm representations.

## 4. Frozen-integrity findings

- v6 freeze `9a05efd9…` verified at every test entry (`Frozen.verify`); v6 `files`
  map (15 files) all present with matching bytes in the exec mirror.
- Corpus and oracle bytes **identical across archived v2–v5** (`corpus.json`
  `e96c730840de`, `oracle.json` `a43dbb2c57e`, schedule changed once v3→v4 as
  disclosed); current staged copies match. The "no corpus facts or expected
  outcome sets changed" claim is confirmed.
- Deviations v1–v5 each state freeze hash, execution outcome and repair with
  prior outputs preserved — matches the 00_RETURN account, including the two
  historical helper failures and two interrupted partial runs.
- RMB original 23 REDs preserved **byte-for-byte as the same failing cases**;
  R2 counterparts are separate new tests — no greenwashing detected.

## 5. Scope ceilings (what this review does NOT establish)

1. **No behavioral validity of arm effects.** See the arm-blind-responder
   finding above. MOCK_ONLY is confirmed as the correct ceiling.
2. **No independent oracle/scenario custody.** Dual channels, one author; R1 and
   23 REDs preserved rather than re-adjudicated; corpus authorship is the
   candidate's.
3. **No power.** Six convenience families; paired intervals vacuous; ±5pp
   equivalence correctly INDETERMINATE. No powered claim is licensed.
4. **No grant.** Model-use, provider, privacy, spend and retention authority
   remain ungranted; the mock issuer confers nothing.
5. **No adoption, production, actor, or wake authority** of any kind.
6. Permutation imbalance (1440 vs 432) and rows-per-case heterogeneity (78/96)
   are recorded observations for any future powered design.

## 6. Discrepancies and notes

- Executing-agent identity differs from the dispatched Codex/GPT-6.1 pair (§1).
  All evidence is deterministic and reproducible independent of model identity.
- pytest here is 9.1.1 vs the candidate's recorded 9.0.2/9.2 surface; no
  behavioral difference observed (51/51 green).
- One hostile probe initially used a tautological assertion and one flagged a
  benign English substring; both were corrected to strict checks before
  verdict (19/19 green after correction). The corrections are in the committed
  probe source.

## 7. Independent owner-action register

| # | Action | Owner | Status |
|---|---|---|---|
| O1 | Accept or revise this review's verdict | HQ / competent acceptance authority | PENDING (this return) |
| O2 | Independent scenario/oracle custody + lawful-set adjudication | Independent custodian + semantic owners | HOLD (unchanged) |
| O3 | Prospective sampling/power design before any equivalence/promotion claim | Experimental-design owner | HOLD (unchanged) |
| O4 | Competent eight-field model/use/privacy/spend grant | Grant issuer | NOT_GRANTED (unchanged) |
| O5 | Real-provider adapter + provider-level validation | Separately commissioned implementer + reviewer | NOT_IMPLEMENTED (unchanged) |
| O6 | Future live assay must consume arm representations in the responder | Future assay designer | REQUIRED before any treatment-effect claim |

No I3 accepted-authority collision was found; no escalation triggered.

## 8. Changed paths and verification

Changed paths (return terrain only): `00_RETURN.md`,
`01_reviewer_expectations.json`, `02_verdict_matrix.json`,
`environment_passport_delta.json`, `staging/` (script + manifest + 48 pinned
objects), `exec/` (byte-verified run mirrors), `hostile/` (19 probes +
recompute), `repro/` (5 JUnit + run logs), `outputs/` (provenance, paired
recompute, predicate ledger). Full list: `changed_paths.txt`.

Remote HEAD verified by direct `git ls-remote` readback after push; reported
below (a commit cannot self-reference its own future SHA). No self-adoption.
