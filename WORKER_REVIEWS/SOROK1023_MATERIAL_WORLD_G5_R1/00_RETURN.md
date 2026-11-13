# SOROK #1023 — independent nonauthor G5 return, B01–B05 material world

**Verdict:** `REVISE_EXACT_DEFECT`
**Scope:** B01–B05 sourcefree material/temporal tranche at composed code cut
`c724d1a89626f3e177acd004c0be20029dc7ade4`.
**Reviewer:** fresh session `ses_e28ef72f9ffelBx7qet6BAina3`, branch
`codex/sorok1023-material-g5-20261113-r1`, host `oldMac.lan`.
**Model/effort:** `opencode-go/deepseek-v4.1-flash`, variant `max`.
**Product code:** READONLY. No patch, no repair loop, no Browser contact.

## 1. Independence and immutable inputs

I did not reuse a B-author or J1-author conversation. The commission names the
authors as `ses_e3129596bffes0LaqGfkjAwEuQ`,
`ses_e312958e8ffeVzjGxpyNpsMatM` (B) and
`ses_e2bcd8b7bfferVT3C26nF0Mw7C` (J1); this review session is distinct. I did
not edit any B, C, D, P2/P3/P6 or J1 product or test file.

Read in full: the current #1023 commission and the #998/#999/#1006/#1002/#997
coordination snapshots (their observed SHA-256 values are in
`CONTRACT_READBACK.json`). Read the original B01–B05 packets at
`227ce149fc7864c83c179a7d3ecaef2b92c5bdab`, `SOROK_PRODUCT_CONTROL_ROOM` read
order, PROGRAMMA SOROK 00, MCR-lite, and the available UM-SOROK R1/R2
source-graded overlay objects at
`f5c43c80675f2556e1287bf55d25052d11e8746e`. The overlay files are present as
Git objects even though not all are in the assigned worktree; no missing
overlay content is invented. The sourcefree constraints used are: material
conditions are not psychological motives; sourcefree evidence is not native
person science; there is no new finance/world engine; parent funds and
household funds are not interchangeable; affordability does not determine
desire.

Exact pins and blob identities are in `BLOB_PINS.json`; selected values:

| Item | Value |
|---|---|
| B source head | `1161e5f74081888bd813825b3df4afab3e2f5ca7` |
| Composed code | `c724d1a89626f3e177acd004c0be20029dc7ade4` |
| Documentary head | `fb061dec16c8386b9caa1b5ea75ec7645aff88a7` |
| `house.py` | `b4591b4b924d0f1d364a41757f77d7fb207f3270` |
| `p2_owner.py` | `a6b289558898d16a58056df36dd647a0a28ec547` |
| `historical_period.py` | `2da7d126774be3bcf5bd2b392ae0589c85861c23` |
| `material_operations.py` | `7901b4fe80248c8ecb731440464454c799fa73b8` |
| `rolling_reproduction.py` | `9500d80e85fba969f8e5fb8f3d233fc11f39c9d0` |
| `parent_decision.py` code-cut SHA-256 | `0fa40ee88f4f32e12a05fb687b7da4ff75b27717782797557239741356c034d4` |
| B packets file at 227ce149 | blob `17cfae53f9ca16640d5d3d500aa7dcb3b31cc89c` |

Verified: each B product and B test worktree blob equals the B source head;
the B files are byte-identical in the composed cut; the only composed
production delta from C is the documented parent-decision HOLD label
correction; the documentary cut has the same product/test blobs as the code
cut; no non-review path differs from `fb061dec` (`BLOB_PINS.json`).

## 2. G1–G5 matrix

| Gate | Status | Exact evidence |
|---|---|---|
| G1 material/temporal/owner/source/grade | **PASS scoped sourcefree** | B blobs verified; household owner/resource bindings; separate parent/household funds; separate market stock/ownership; explicit currency equality; dated periods/as-of/midperiod split; tenancy/space/acoustics/costs; typed purchase/refusal/rent. No external rights or native science. |
| G2 actual first consumers | **PASS on the normal path; forged provenance failure in G3** | `house.read_household/read_dwelling/material_feasibility`; `historical_period.read_material_period/period_progress/materialize_to`; `material_operations.read_market_inventory/read_owned_objects/read_purchase`; `rolling_reproduction.read_household_obligation`; C03 `parent_decision` actual PURCHASE path; fresh-process cold reopen. No parent-desire or Nadia-choice claim. |
| G3 independent hostile | **FAIL — REVISE_EXACT_DEFECT** | Two forged `ADMITTED` receipt attacks accepted by public readers. All other 61 checks pass. See section 4. |
| G4 preservation/change/restore/cold/measure | **PASS with limits** | Original 43: 43 passed in 534.18s (exit 0). Changed space/feasibility restored exactly; changed stock/ownership/cold restored exact receipt/source identity; fresh process with two purchases and one rent had no duplicate. |
| G5 nonauthor verdict | **REVISE_EXACT_DEFECT** | Fresh distinct reviewer; no acceptance, no protected merge, no native/source grant. |

Machine matrix: `G1_G5_MATRIX.json`.

## 3. Commands, logs and true exits

All runs used the existing accepted Python
`/private/tmp/rawlsing-oct28-p1r1/venv/bin/python` (Python 3.11.3, pytest
9.1.1). Commands were run sequentially, one workload child at a time, from the
review worktree. No GitHub Actions were used.

### Original 43 test command

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/time -l /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py \
  WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_period.py \
  WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_incremental.py \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_same_root_psyche.py \
  WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_operations.py \
  WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_composition.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rolling.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rollback.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_batch_cycle.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_cross_batch.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_zero_and_held.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_interleave_retry.py
```

| Run | Exit | Observed | Log |
|---|---:|---|---|
| original B01–B05 43 tests | 0 | **43 passed in 534.18s**; peak RSS 75,231,232 B | `evidence/b01_b05_original43.log` |
| novel hostile witness (`g5_probe.py`) | 1 | 63 checks, 61 pass, 2 defect failures | `evidence/g5_probe_run.log`, `evidence/hostile_report.json` |
| cold process (`g5_cold_probe.py`) | 0 | fresh process; 2 purchases + 1 rent; no duplicate; 22.285s | `evidence/g5_cold_probe.log`, `evidence/cold_report.json` |
| read-only C03/B04 lock order | 0 | `purchase_lock -> parent_lock`; purchase PERFORMED; 13.343s | `evidence/g5_c03_lock_probe.log`, `evidence/lock_report.json` |
| blob/provenance pins | 0 | B product/test blobs equal B head; product unmodified | `evidence/g5_pins.log`, `BLOB_PINS.json` |

## 4. Independent novel hostile witness and exact defects

`g5_probe.py` drives the actual public readers and writers; it is not a mock
suite. It covers wrong currency, wrong owner/parent, market branch tamper,
household-low/parent-adequate and household-adequate/parent-low, unknown
acoustics, prohibited tenancy, tight space, household root/actor tamper,
period boundaries/as-of/midperiod, duplicate purchase/rent and same-period
second rent, partial ownership removal, changed space and exact restore,
cold-after-failure, and the C03/B04 lock order. Those 61 checks pass.

The two failures are real provenance defects in public first readers:

1. **B04 `read_purchase`** (`material_operations.py:646-672`) accepts a forged
   `ADMITTED` `P2_PARENT_PURCHASE` receipt with `root = "f"*64` and
   `branch = "foreign-branch"` when a coherent ownership row is present. It
   checks acquisition fields but not the nested receipt root/branch/parent.
   C02 `parent_activity.py:363-364` already refuses the same mismatch.
2. **B05 `read_household_obligation`** (`rolling_reproduction.py:376-406`)
   accepts a forged `ADMITTED` `P2_HOUSEHOLD_RENT` receipt with
   `root = "e"*64` and `branch = "foreign-branch"`, and with before/after cash
   consistent with current household cash. No second debit occurs, but false
   rent evidence is accepted.

Runnable reproduction, exact input, expected/actual, source-level cause and
smallest suggested owner fix (not applied): `DEFECT_WITNESS.md`.
No product repair was attempted. This is an informational scoped owner
handoff for HQ/user decision.

## 5. Change/restore, cold, cost and contention

- Changed legitimate space input produced `REFUSED_SPACE`; restoring the
  original stored dwelling document restored the exact `material_hash`, and
  the feasibility document was exactly equal to baseline.
- A real purchase changed stock 2→1 and added one ownership row with exactly
  one 40-unit parent debit; household cash was unchanged. Replay did not debit
  again or add ownership.
- Cold process: purchase period `period:2026-h1`, later purchase
  `period:2026-h2`, one household rent 55→43. Fresh process read both purchase
  receipts and the rent; latest purchase replay was `REPLAY`, earlier purchase
  was a typed `PURCHASE_REPLAY_STALE` refusal, rent replay was `REPLAY`, and a
  second same-period rent was refused `B05_RENT_ALREADY_RECORDED`. Counts and
  P3 head were unchanged.
- Observed wall time: 43 tests 534.18s; hostile probe 32.58s; cold probe
  22.285s; lock probe 13.343s. Observed process peak RSS: pytest 75,231,232 B;
  hostile 58,798,080 B; cold 58,769,408 B; lock 53,338,112 B.
- Contention: #1006's `scale-50k` write workload (child PID 51945) and #1007
  were active during this review; load average was about 5.3 at start. The
  author's isolated 43-test reference was 442.42s; this contended run was
  534.18s. No simultaneous second reviewer or author was run.
- Host free disk observed about 15 GiB at start. Generated state was bounded
  under the review directory and removed after each probe. Provider
  token/USD cost is `UNOBSERVED`; no invoice claim is made.

## 6. Limits and holds

- Sourcefree S2 engineering only. No native CAN/ADP/Pyat science, no external
  source or respondent rights, no actor/human authority.
- No full J1/CG-D review; the J1 terminal performed child event remains held
  and is not claimed. No broader Nadia-choice or parent-desire claim.
- The original 43 B tests and the normal material first-consumer path pass.
  The verdict is `REVISE_EXACT_DEFECT` solely because the two public receipt
  readers accept forged foreign-root/branch provenance.
- Full original P6/MII suite and full J1 suite were not rerun for this
  B-tranche; they are outside the necessary evidence for this commission.
- No protected PRE-MAIN write/merge, no fleet resumption, no Browser session
  contact, no provider/server/config change, no `.env`/key access.

**STOP.** Evidence-only publication on this branch; defect reported to
HQ/user. User decides whether/how to relay or authorize an owner repair.
