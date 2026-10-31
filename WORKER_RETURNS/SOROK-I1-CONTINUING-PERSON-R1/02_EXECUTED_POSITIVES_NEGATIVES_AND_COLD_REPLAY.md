# Executed positives, negatives, and cold replay

All commands ran from
`WORKER_RETURNS/SOROK-I1-CONTINUING-PERSON-R1/candidate/` with:

```text
Python 3.11.3
pytest 9.1.1
SQLite 3.40.1
macOS 13.7.8 x86_64 (oldMac)
PYTHONDONTWRITEBYTECODE=1
```

The environment has no external C12 anchor, no CAN/ADP issuer, no Pyat
structural source, and no native A0-A5 participant.

## 1. Unchanged BP2P4J positives

```sh
cd candidate
PYTHONPATH="$PWD" python3 -m pytest -o addopts='' -q \
  tests/test_joined_product.py \
  tests/test_joined_security.py \
  tests/test_joined_severance.py \
  tests/test_source_closure.py
```

Exit `0`; result `33 passed in 10.30s`.

Breakdown:

| Test file | Passed | Scope |
|---|---:|---|
| `tests/test_joined_product.py` | 10 | joined source, practice/E2, fork, cold process, literal origin |
| `tests/test_joined_security.py` | 12 | source/identity/perception forgery and private-state checks |
| `tests/test_joined_severance.py` | 7 | ten same-assertion source cuts and restorations |
| `tests/test_source_closure.py` | 4 | staged BP1/BP2/BP4/C9 byte closure |

The only source edits in these files are additive `product_cls` defaults in
`bp2p4/assertion.py` and `bp2p4/severance.py`; no original test expectation was
changed. The default remains `JoinedProduct`.

## 2. BP4R guard positives

```sh
BP4R_C9_DIR="$PWD" PYTHONPATH="$PWD" python3 -m pytest -o addopts='' -q \
  tests/test_bp4r_candidate.py
```

Exit `0`; result `9 passed in 0.66s`.

The nine tests cover:

- legitimate episode-bearing fork and cold reopen;
- immutable episode origin versus current storage location;
- forged branch transplant refusal;
- unsupported C9/C12 writer version `@2` refusal;
- actual C9 consumer writer-schema gate and restoration;
- supported writer ready/mirror handshake;
- cold schema mismatch fail-closed;
- mixed writer-domain refusal;
- two diagnostic REDs: global writer chronology and anchor actor/clock coverage
  remain separate HOLDs.

## 3. I1 guarded-consumer positives

```sh
PYTHONPATH="$PWD" python3 -m pytest -o addopts='' -q \
  tests/test_i1_guarded_consumer.py
```

Exit `0`; result `8 passed in 5.16s`.

Tests and observed claims:

1. `test_guarded_product_verifies_episode_fork_and_cold_branch`
   - root and child episode origins resolve correctly after cold branch reopen.
2. `test_guarded_consumer_uses_the_named_assertion_and_all_severances`
   - `joined_downstream_a0_a2_assertion(..., product_cls=GuardedJoinedProduct)`
     returns `PASS`;
   - all 7 primary and 3 supplementary severance trials are baseline PASS ->
     edge-specific RED -> restored PASS.
3. `test_b_offscreen_market_work_adds_cash_but_stays_material_exhausted`
   - B position `workshop -> market`;
   - B completed `3 -> 4`;
   - B cash `54 -> 56`;
   - B material `0 -> 0` (stock exhausted; event body still records
     `material_delta: -1` under the existing floor rule);
   - B free hours `13 -> 13`;
   - public `other()` shows completed `4`, position `market`, and the public
     work event; cash/material/free-hours remain hidden;
   - cold reopen returns identical material readout.
4. `test_material_stock_cannot_be_spent_twice`
   - A material `2 -> 1 -> 0`;
   - A completed `4 -> 6`;
   - A cash `55 -> 59`;
   - A free hours `12 -> 10`;
   - third repair returns `DENY / MATERIAL_EXHAUSTED`.
5. `test_market_work_is_not_known_before_presence`
   - claims before travel are `["ARRIVAL"]`;
   - workshop attend adds no B market event;
   - after travel to market and attend, `OFFSCREEN_REPAIR` is claimed.
6. `test_fork_child_cannot_rewrite_parent_material_history`
   - child A repair changes child completed units;
   - root B material readout and root counts remain unchanged;
   - guarded fork equality and both branch verifications pass.
7. `test_guarded_reader_refuses_unsupported_writer_schema`
   - `meta.schema = BP4_C12_STORE@2` produces `schema_ok: false`;
   - fork raises `StoreRefusal("SCHEMA_UNSUPPORTED")`.
8. `test_cold_process_reopens_guarded_material_and_public_history`
   - four separate Python processes run `wait 30`, `verify`, `owner-material`,
     and `other` through `run_guarded.py`;
   - verify reports content/fork/schema OK and
     `authenticity.code = OWNER_ANCHOR_REQUIRED`;
   - owner material readout reports B cash `56`, material `0`, completed `4`;
   - public readout reports completed `4` and position `market`.

## 4. Combined suite

```sh
BP4R_C9_DIR="$PWD" PYTHONPATH="$PWD" python3 -m pytest -o addopts='' -q tests
```

Exit `0`; result `50 passed in 15.66s`.

## 5. Causal severance detail

The guarded consumer uses the same named assertion as BP2P4J. Each trial ran
baseline PASS, the physical source cut, then restoration:

| Edge | RED message observed |
|---|---|
| `BP2_C8_PROOF` | `BP2_C8_PROOF_INVALID` |
| `BP2_ACTOR_HISTORY` | `BP1_ACTOR_SOURCE_NOT_MATCHING_BP2_C8` |
| `BP2_RULE_A` | `BP2_RULE_A_RESPONSE_ABSENT` |
| `BP2_RULE_T` | `BP2_RULE_T_AUTHORIZATION_ABSENT` |
| `BP2_TARGET_HASH` | `BP2_C9_CONSUMED_HASH_MISMATCH` |
| `BP2_E2` | `BP2_E2_SELF_PERFORMED` |
| `BP4_C10_M6_ACCESS` | `A0_CLAIM_SET` |
| `BP2_OTHER_HISTORY_ALIASED` | `BP1_OTHER_SNAPSHOT_NOT_MATCHING_BP2_C8` |
| `BP2_E2_NOT_PERFORMED` | `A0_E2_ADMITTED` |
| `BP2_PRACTICE_NOT_MATERIALIZED` | `A0_PRACTICE_NOT_ESTABLISHED` |

The first seven are the load-bearing edges; the last three are supplementary.
No cut was proven by a generic exception. Restoration returned the baseline
receipt.

## 6. Cold-replay command shape

The ninth I1 test executes the equivalent of:

```sh
python3 run_guarded.py --root "$ROOT" wait 30
python3 run_guarded.py --root "$ROOT" verify
python3 run_guarded.py --root "$ROOT" owner-material
python3 run_guarded.py --root "$ROOT" other
```

Observed cold values: B cash `56`, B material `0`, B completed `4`, position
`market`; public completed `4`; guard content/fork/schema OK; authenticity
`OWNER_ANCHOR_REQUIRED`.

## 7. Negative / HOLD results

- No external C12 anchor exists; `OWNER_ANCHOR_REQUIRED` is a HOLD, not a pass.
- Unsupported writer schema `@2` is refused.
- Forged branch transplant is refused.
- Third A repair with zero material is refused.
- B market work is not claimed before A reaches the market.
- Child branch repair does not rewrite root material state.
- F1CR targetless REFUSE/SILENCE adapter is not present and not claimed.
- C9 R3B durable actor mirror and C12 durable cold reopen are not claimed.
- BP2P4J `c12_verify.py` self-referential residual is unchanged and bypassed by
  the new guard path; it is not an authorization source for I1.
