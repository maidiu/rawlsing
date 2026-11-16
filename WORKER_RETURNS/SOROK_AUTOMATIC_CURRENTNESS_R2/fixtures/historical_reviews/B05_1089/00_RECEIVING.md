# SOROK #1037 B05 R3 independent G5 — final focused receiving

**Engineering verdict:** `ACCEPT_SCOPED_SOURCEFREE`
**Accepted source:** `cab1f2d6cdab6f6b653ed20e5b41afb90d9facbc`
**Branch:** `codex/sorok1037-b05-zero-status-repair-20261115-r3` (review branch `codex/sorok1037-b05-r3-independent-g5-20261115-r3`)
**Base / prior reviewed code:** `270eb29cd4487b6865b61adc9d671952554d425d`
**Reviewer:** `ses_e21caf5dfffeSywXGrQ6qw65oe` (same independent nonauthor)
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Scientific verdict:** `HELD`
**Authority verdict:** `HELD`
**Grade:** `SOURCEFREE_S2_ONLY`
**Protected PRE-MAIN:** declared cut `6a5c12f04323d74001f9632063ec907f4fc4468e`; read-only/untouched, no protected write or merge.
**Terminal:** STOP. No R4 or additional repair round.

## 1. Scope and source custody

Inherited merged capital is acknowledged, not rebuilt: P5 #775, P6 #779, MIII #891, MII #905 and MI #907 are merged historical implementations; this focused B05 receiving neither calls them absent nor modifies them.

This is one focused independent receiving after the fresh-user-authorized R3 correction. The original adverse reviews remain historical and unchanged:

- `5b65a35b1f54cd13da0a340eed1c9b92783a0ce1` — original positive sole-receipt RED.
- `6dc921841a748ee7121887c0484068249a526b17` — R2 zero-rent ADMITTED RED.

R3 changes exactly one product file, read side only:

| Path | Before R3 | Candidate R3 | Result |
|---|---|---|---|
| `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py` | `a193fb5bfb6a1955209bedf0e66be974dcfa8e1b` | `9de3b5a295431fac2b0f9833ed520262df04b363` | +10/-6 read-side status validation |
| `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py` | `3c1d326bfa2f8a78c92a84e5cc5e039e04376441` | `3c1d326bfa2f8a78c92a84e5cc5e039e04376441` | unchanged |
| author R3 test `tests/test_b05_zero_status_semantics.py` | absent | `0576b17433737f0f8831d81940848c7762d87d64` | 4 tests |

B05 candidate sha256 `bb67d3e03baf28943076cf5902e308c26ccbb7678672a297817a358a6296c774`. The diff is only the `ADMITTED` strict-debit guard in `_rent_chain` and `read_household_obligation`; the accepted R2 checkpoint/unique-transition proof is retained. No writer, receipt schema, store, lock, ledger, registry, key, currency, B04, C03/C04, P6 or D03 change. Full pins: `evidence/BLOB_PINS.json`; source delta: `evidence/source_delta_name_status.txt`; diff: `evidence/source_diff_b05.patch`.

Exact prior probe assets were copied from the immutable git tree into this reviewer root at normal depth and executed unmodified:

```text
own zero probe        blob d5d41240d32170ab0f2bed292afa747662283287
                       sha256 0300e8ddc694a85260589a92a9632c3661835a3a096c9294e09287bbf8acd4d8
own positive probe    blob 3e98929dbb526edf6fab60f74132cafe03d63239
#1027 witness         blob 7cd5a23044426961d6f33e13b1ccf44f54916f81
#1027 cold probe      blob 6fc86dc5ca7ca8cc52baa8ad71ad33349d846cab
own R3 negative probe blob d9f70c60620667f9940e5df884c45dcf070855c9
```

No author probe was executed in place or overwritten. The immutable R2 RED report is preserved at `evidence/immutable_r2_red_report.json` (sha256 `f941df6986a5ea4378abbd730d2828d6ceb3a562323e0041adbe130b92797588`; 17 checks, 16 pass, residual true). The author R3 RED report is separately at `evidence/red_g5_r2_focused_probe_report.json` in the author return.

## 2. Environment and executed commands

Host `oldMac.lan`, Darwin 22.6.0 x86_64, macOS 13.7.8; actual Python `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python` 3.11.3; pytest 9.1.1. Every command used `TMPDIR=$PWD/.local-logs/sorok1037-b05-r3-independent-g5-20261115-r3/tmp`, `PYTHONDONTWRITEBYTECODE=1`, `pytest -p no:cacheprovider`. No product edit, `/tmp` redirect, dependency install, global permission change, CI, new agent/server/controller, model/provider/account change or paid fallback. Checkpoint/org/quota and token/USD cost are `UNOBSERVED`.

| Command | Exit | Result | Real / max RSS |
|---|---|---|---|
| unchanged zero probe `g5_r2_focused_probe.py` | `0` | **17/17**, zero forgery now `B05_RENT_RECEIPT_INVALID`; R2 positive-red cases also pass | 47.61 s / 58,920,960 B |
| original positive probe `g5_review_probe.py` | `0` | **34/34**; positive sole rehash `B05_RENT_OPERATION_UNPROVEN`; B04 controls pass | 43.84 s / 59,695,104 B |
| exact #1027 witness `g5_probe_1027.py` | `1` literal | **63/63** checks; both defects `accepted=false`; historical oracle quirk retained | 19.37 s / 61,104,128 B |
| exact #1027 cold probe `g5_cold_probe_1027.py` | `0` | `ok=true`, `warm_ok=true`, `child_exit=0`; two purchases + one rent; head unchanged | 16.60 s / 59,052,032 B |
| R3 focused tests | `0` | 4 passed | 32.67 s / 69,107,712 B |
| R2 focused regression | `0` | 5 passed | 41.09 s / 65,798,144 B |
| legacy B04/B05 tests | `0` | 6 passed | 50.81 s / 70,238,208 B |
| selected C03/C04 consumer | `0` | 3 passed; product read-only | 75.18 s / 67,919,872 B |
| inherited original B01-B05 43 | `0` | 43 passed once on final source | 495.37 s / 73,240,576 B |
| own R3 independent probe | `0` | **12/12** own negative/positive checks | 40.06 s / 54,599,680 B |

Base RED was verified from the immutable R2 report at `6dc9218` and the author R3 RED report: 17 checks, 16 pass, one failure, zero-rent forged receipt `READ` with cash 55. The immutable literal exit receipt is preserved at `evidence/immutable_r2_red_exit.txt` (`EXIT=2`). The same unchanged probe blob was executed on R3 and returned 17/17 with the zero forgery refused. Product was not mutated to re-run the base.

## 3. Independent negative witness (own construction)

`g5_r3_independent_probe.py` uses only existing public product actions and public `append_episode`, then the actual `read_household_obligation`:

1. **ADMITTED positive rent with no cash decrease** — rent 12, cash 55 -> 55, on public no-cash `say` checkpoints: refused `B05_RENT_RECEIPT_INVALID`.
2. **ADMITTED rent not equal to the cash decrease** — rent 12, cash 55 -> 50: refused `B05_RENT_RECEIPT_INVALID`.
3. **Well-formed ADMITTED debit with no actual checkpoint transition** — self-consistent before 67 / after 55 and matching material hashes, but no actual rent checkpoint pair: refused `B05_RENT_OPERATION_UNPROVEN`.
4. **Genuine zero** — writer `UNCHANGED`, reader `READ`, cash unchanged.
5. **Genuine held** — writer `REFUSED`, reader `READ`, cash unchanged.
6. **Genuine positive** — writer/reader `ADMITTED`, exact debit, h1 `historical=true` after h2, h2 `historical=false`, exactly two debits.
7. **Same-period replay boundary** — a copied ADMITTED receipt is refused `B05_RENT_OPERATION_NOT_UNIQUE`; the genuine receipt is fail-closed while the copy exists; no second debit.

All 12 checks passed. This distinguishes malformed ADMITTED status/debit from genuine zero, held and positive reads; it is not a blanket refusal. The forged ADMITTED cases use public `session.product.say` and public `append_episode`; the held `REFUSED` control uses the same local test-fixture cash setup (`world.actor_state["A"]["cash"]=5` plus the existing checkpoint) as the existing B05 writer tests. That is a disclosed fixture setup, not a product edit or a hidden privileged attack on the reader. No hidden product world write was made.

## 4. G1-G5 matrix

| Gate | Status | Basis |
|---|---|---|
| G1 source/owner/custody | `PASS_SCOPED_SOURCEFREE` | exact candidate/base/branch; only B05 read-side changed; B04 unchanged; no writer/schema/store/lock/ledger/key; exact assets byte-identical; product read-only |
| G2 build/normal first consumers | `PASS` | 17/17 zero, 34/34 positive, #1027 63/63, cold two purchases + one rent, 4+5+6+3+43 tests; B04 purchase/controls preserved |
| G3 falsification | `PASS` | own malformed ADMITTED/no-debit/replay negative witness passes; original positive forgery remains refused; zero forgery refused; checkpoint sever/restore and sibling copy preserved; no new false ADMITTED found |
| G4 boundaries/preservation | `PASS_WITH_LIMITS` | no writer/ledger/schema/lock/currency/psychology change; historical h1 true/h2 false, replay/retry, changed/restored, B04 and cold preserved; fully privileged checkpoint fabrication remains outside observed public-action/append threat model; UNCHANGED/REFUSED no-debit statuses remain by design |
| G5 independent receiving | `ACCEPT_SCOPED_SOURCEFREE` | exact source `cab1f2d6cdab6f6b653ed20e5b41afb90d9facbc`; no remaining in-scope false ADMITTED proof found |

## 5. Why the checkpoint evidence now suffices at this boundary

The R2 proof required an adjacent same-clock checkpoint pair matching the receipt's before/after cash and material hashes, plus exactly one rent episode with that transition tuple. R3 adds the missing status/debit truth: an `ADMITTED` receipt must have positive rent, a strict cash decrease, and exact debit arithmetic at both the public reader and `_rent_chain`. This closes the zero-rent public no-cash pair exploit.

For positive rent, the only public product operation that changes A-household cash is `apply_household_rent` itself; the base product `repair` action only credits `+2` and cannot satisfy a non-negative rent debit. No public non-rent A-household-cash debit exists. A forged positive receipt therefore either has no matching checkpoint transition (`B05_RENT_OPERATION_UNPROVEN`) or copies a genuine rent transition, in which case the genuine rent episode shares the tuple and both refuse. The fully privileged fabrication of a matching checkpoint pair remains outside the observed public-action/`append_episode` threat model, as previously scoped for B04.

## 6. Supersession and preserved history

- `5b65a35b1f54cd13da0a340eed1c9b92783a0ce1` remains the immutable original RED; its positive sole-receipt false accept is closed at R2.
- `6dc921841a748ee7121887c0484068249a526b17` remains the immutable R2 RED; its zero-rent ADMITTED false proof is closed by R3.
- This receiving accepts only the sourcefree B05 reader at `cab1f2d6`. It does not erase or regrade either historical report, and does not promote native science, actor knowledge, J1, human or protected rights.

## 7. Limitations and nonclaims

- Sourcefree engineering only; no native science, actor knowledge, human authority, J1/Nadia G2 acceptance, motive/volition inference or protected PRE-MAIN merge.
- No new ledger, currency engine, writer, schema, store, lock or scheduler.
- `UNCHANGED` zero and `REFUSED` held receipts remain readable without a debit checkpoint by the authorized R3 scope; this receipt does not claim operation authenticity for those no-debit statuses.
- Fully privileged checkpoint fabrication is outside the observed public-action/append threat model.
- Timings/RSS are observations under concurrent host load, not isolated benchmarks. Provider cost and checkpoint/org/quota are `UNOBSERVED`.
- No R4, new agent, fleet, staging, CI or protected merge was launched.

## 8. Verdict and STOP

**Engineering:** `ACCEPT_SCOPED_SOURCEFREE` at `cab1f2d6cdab6f6b653ed20e5b41afb90d9facbc`.
**Scientific:** `HELD`.
**Authority:** `HELD`.

One focused receiving complete. Evidence is in this reviewer root; commit only this root, do not push. STOP.
