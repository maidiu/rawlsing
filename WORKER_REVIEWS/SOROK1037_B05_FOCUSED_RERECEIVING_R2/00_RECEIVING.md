# SOROK #1037 B05 focused R2 re-receiving — same nonauthor reviewer

**Verdict:** `REVISE_EXACT_DEFECT` (not `ACCEPT_SCOPED`)
**Issue:** #1037
**Reviewer session:** `ses_e21caf5dfffeSywXGrQ6qw65oe` (same independent nonauthor; not author `ses_e21a481bfffefyvpxaeFaAOFvQ`)
**Candidate:** `270eb29cd4487b6865b61adc9d671952554d425d`
**Branch:** `codex/sorok1037-b05-writer-proof-repair-20261115-r2`
**Base:** `c7018020f002bb7f509a83fba0bf2a6a5955cc00`
**Grade:** `SOURCEFREE_S2_ONLY`
**Terminal:** STOP. The one permitted post-G5 correction budget is used; no new repair loop dispatched.

## 1. Focused scope and source custody

This is the focused closure of the existing G5, not a new campaign. The original independent RED receiving `5b65a35b1f54cd13da0a340eed1c9b92783a0ce1` (published PR #1065) remains immutable and historical. R2 changes exactly one product read-side file and adds its own return/tests/evidence:

| Path | Before R2 | Candidate R2 | Result |
|---|---|---|---|
| `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py` | `b944b8f0b6e0d700e85141256df01cdaef8d59e2` | `a193fb5bfb6a1955209bedf0e66be974dcfa8e1b` | +85 read-side lines |
| `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py` | `3c1d326bfa2f8a78c92a84e5cc5e039e04376441` | `3c1d326bfa2f8a78c92a84e5cc5e039e04376441` | unchanged |
| author R2 test `tests/test_b05_actual_rent_transition.py` | absent | `e61dca9f81ddc3fcb5fcf33272934232c2ae16a2` | 5 tests |

The B05 candidate sha256 is `5ac75cb66c61fb120f56900e976a8cdcd4e153fd4b0d37d9a93a0c95ab578331`. The diff contains only the new checkpoint-proof helpers and the `ADMITTED` read call; no writer, schema, store, lock, currency, ledger, registry, key, B04, C03/C04, P6, D03 or protected PRE-MAIN change. B04 is byte-identical to the original reviewed candidate.

Exact frozen assets were copied byte-identically into this reviewer root and executed unmodified:

```text
review probe       blob 3e98929dbb526edf6fab60f74132cafe03d63239
                    sha256 fb42f9fd48d455bedf236d6f578e8aab94de449b4bf1e07adb315c99115a6c57
#1027 witness      blob 7cd5a23044426961d6f33e13b1ccf44f54916f81
                    sha256 da1d4389fdae9d092f3bb777777e5f5ea76a71fea943730ff6cf029e3414fa5a
#1027 cold probe   blob 6fc86dc5ca7ca8cc52baa8ad71ad33349d846cab
                    sha256 f9cc6e56cf6899bea1b09c820b4b3dc0ad52a97b5864bc9121a34229dc1820aa
own R2 probe       blob d5d41240d32170ab0f2bed292afa747662283287
                    sha256 0300e8ddc694a85260589a92a9632c3661835a3a096c9294e09287bbf8acd4d8
```

No author probe was executed in place or overwritten. Full pins: `evidence/BLOB_PINS.json`.

## 2. Environment and commands

Host `oldMac.lan`, Darwin 22.6.0 x86_64, macOS 13.7.8; actual Python `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python` 3.11.3; pytest 9.1.1. Every command used `TMPDIR=$PWD/.local-logs/sorok1037-b05-focused-r2/tmp`, `PYTHONDONTWRITEBYTECODE=1`, `pytest -p no:cacheprovider`. No `/tmp` redirect, dependency install, global permission change, hosted CI, provider/model/auth change or paid fallback. Model checkpoint/org/quota and token/USD cost are `UNOBSERVED`.

| Command | Exit | Result | Real / max RSS |
|---|---|---|---|
| unchanged review probe `g5_review_probe.py` | `0` | **34/34**, no residual; original sole positive rehash now `B05_RENT_OPERATION_UNPROVEN` | 37.76 s / 57,102,336 B |
| exact #1027 witness `g5_probe_1027.py` | `1` literal | **63/63** checks, both defects `accepted=false`; historical oracle quirk only | 15.89 s / 64,147,456 B |
| exact #1027 cold probe `g5_cold_probe_1027.py` | `0` | `ok=true`, `warm_ok=true`, `child_exit=0`; two purchases + one rent; head unchanged | 14.88 s / 55,865,344 B |
| author focused R2 tests | `0` | 5 passed | 35.01 s / 67,796,992 B |
| author legacy 6 tests | `0` | 6 passed | 43.02 s / 68,726,784 B |
| inherited original B01-B05 43 | `0` | 43 passed once on final R2 source | 438.62 s / 80,191,488 B |
| selected C03/C04 consumer | `0` | 3 passed; product read-only | 56.43 s / 72,790,016 B |
| own focused R2 probe `g5_r2_focused_probe.py` | `2` own oracle | **16/17**; one failure = new forged ADMITTED zero-rent false proof | 41.64 s / 60,432,384 B |

The exact #1027 witness literal exit `1` and its `verdict` field remain the unchanged historical oracle quirk; the semantic result is 63/63 checks with both defect rows `accepted=false`.

## 3. What R2 closes — original 5b65 positive case

The original focused RED was a sole, caller-rehashed **positive** `ADMITTED` rent receipt for a completed period with no actual rent debit. On R2, the unchanged reviewer probe now returns `B05_RENT_OPERATION_UNPROVEN`, 34/34 checks, exit `0`. The checkpoint sever/restore, sibling transition copy, genuine zero `UNCHANGED`, genuine held `REFUSED`, historical h1/h2, replay/retry and normal warm/cold paths all pass. The #1027 foreign-root cases still refuse. The exact original positive defect is closed at R2.

## 4. Remaining material RED — forged ADMITTED zero rent

The R2 proof requires an adjacent durable checkpoint pair at the receipt clock whose cash/material hashes match the receipt before/after. It does **not** require the pair to be a rent operation or a strict debit. That is exploitable with existing public owner actions, without any world rewrite:

1. Legitimately commit dwelling `monthly_rent = 0` via `house.commit_dwelling`; materialize `period:2026-h1` to `COMPLETE`.
2. Call the existing public product action `session.product.say(...)` twice at the same clock `429`. Both return `OK`; neither changes household cash.
3. The durable checkpoint list then contains four adjacent same-clock checkpoints at `429`, each with cash `55`, material hash `8ee0b853d3b34cec760f642cd3203719055613d298950b0203d7629a351888da`, source `acd91d4ef9b4b8f09814a8b476d861cfe3f2c4f360ae0acccc15f7ef08ddc88e`.
4. Append one sole forged `ADMITTED` `P2_HOUSEHOLD_RENT` receipt for operation `g5review:r2:zero-false-admitted`, period h1, rent `0`, cash before/after `55/55`, before/after hashes equal to the public checkpoint hash, using only `session.product.store.append_episode`.
5. The actual existing writer for zero rent produces `UNCHANGED`, not `ADMITTED`. Nevertheless `read_household_obligation` returns:

```json
{"status": "READ", "historical": false,
 "receipt_status": "ADMITTED", "household_cash": 55}
```

Cash before and after the append is unchanged (`55 -> 55`). This is a false `ADMITTED` evidence/currentness proof, not a duplicate debit. It directly violates the focused requirement that genuine zero remains `UNCHANGED` and that no false `ADMITTED` proof be accepted.

The control with a positive forged rent on the same non-rent checkpoint pair refuses `B05_RENT_OPERATION_UNPROVEN`; the zero case is accepted because the forged before/after values equal an unchanged public no-cash checkpoint pair.

### Why this is in scope and not privileged

- `session.product.say` is an existing public product action; the two checkpoints are legitimate durable state writes, not a fabricated world rewrite.
- The forged rent is append-only through the public C12 store API.
- The actual zero-rent writer is `UNCHANGED`; the reader accepts a different status. The proof authenticates a convenient same-clock state pair, not **this** rent operation.
- A fully privileged rewrite of checkpoints remains outside the observed append-only threat model and is not used here.

### Non-rent cash-delta check

The only public product writer that changes A household cash is `apply_household_rent` itself (`rolling_reproduction.py` line 423). The base product `repair` action only credits `+2`, which cannot satisfy a non-negative rent debit; no existing public owner API provides a non-rent A-household-cash debit. The zero false proof therefore uses a public **no-cash** checkpoint pair, not a privileged cash rewrite.

## 5. G1-G5 focused matrix

| Gate | Status | Basis |
|---|---|---|
| G1 source/owner/custody | `PASS_SCOPED_SOURCEFREE` | exact candidate/branch/parent; B04 unchanged; only B05 read-side changed; byte-identical assets; exclusive reviewer root; no hot imports; product read-only |
| G2 build/normal first consumers | `PASS_NORMAL_READERS_AND_COLD` | two purchases + one rent warm/cold; 5 focused, 6 legacy, 43 inherited, 3 consumer; no second debit; head unchanged |
| G3 falsification | `FAIL_REVISE_EXACT_DEFECT` | original positive sole-rehash closed; root/branch/actor/exchange/period/rent/second-receipt controls pass; checkpoint sever/restore and sibling copy pass; **forged ADMITTED zero rent accepted via public no-cash checkpoint pair** |
| G4 boundaries/preservation | `PARTIAL_PASS_PRESERVATION__ZERO_STATUS_BOUNDARY_FAILS` | no writer/schema/store/lock/ledger/currency change; B04, zero genuine, held, historical, retry, cold preserved; ADMITTED status semantics not preserved |
| G5 independent receiving | `REVISE_EXACT_DEFECT` | one remaining exact append-only/public-action false `ADMITTED` proof; no `ACCEPT_SCOPED` |

## 6. Minimal correction for the record — not dispatched

The smallest correction is status/transition semantics for `ADMITTED`: require a strict debit transition (`monthly_rent > 0`, `household_cash_after < household_cash_before`) backed by the actual checkpoint pair, and reject an `ADMITTED` receipt with `monthly_rent == 0` or `before == after`; zero rent must remain `UNCHANGED`, insufficient cash must remain `REFUSED`. This needs no new ledger, key or writer. The one permitted post-G5 correction budget is used, so this is recorded as the exact residual, not dispatched as another repair round.

## 7. Supersession

- Original independent RED `5b65a35b1f54cd13da0a340eed1c9b92783a0ce1` and its published report remain historical; they are not erased or regraded by this R2.
- R2 closes the original **positive sole-rehashed** B05 false accept and preserves the exact #1027, normal, cold, zero-genuine, held, historical and retry behavior.
- R2 does **not** earn `ACCEPT_SCOPED@B01_B05_SOURCEFREE_270eb29cd4487b6865b61adc9d671952554d425d`: a remaining zero-rent `ADMITTED` false proof is reproduced.

## 8. Limitations and nonclaims

- No native science, human/actor authority, J1/Nadia G2 acceptance, motive/volition inference, protected PRE-MAIN merge, new ledger, or psychological fact.
- The zero false proof is false evidence/status acceptance, not a second debit.
- Fully privileged checkpoint fabrication remains outside the observed append-only threat model.
- Timings/RSS are observations under host load, not isolated benchmarks. Provider token/USD and checkpoint/org/quota are `UNOBSERVED`.
- No further repair round, subagent, staging, fleet or protected merge is launched.

## 9. STOP

Focused re-receiving complete. R2 is not accepted; exact residual witness is committed in this reviewer root. STOP.
