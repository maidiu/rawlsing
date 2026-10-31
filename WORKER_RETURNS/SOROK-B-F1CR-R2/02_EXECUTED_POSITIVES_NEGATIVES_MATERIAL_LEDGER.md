# Executed positives, negatives and material ledger

## Environment

- macOS `oldMac` local Git/Python; Python 3.11.3; pytest 9.1.1.
- Local OpenCode / `opencode-go/deepseek-v4.1-flash`; MAX effort not independently observable.
- Test runtime: R5 `f1cr-recon` under the output worktree; detached I1 runtime at `7d44e300…`.
- No native source, SAV, respondent corpus or unreviewed branch script was run.

## R5 F1C replay

Runtime: `.tmp-f1cr-recon` inside the output worktree. The R5 reconstructed candidate was copied to `f1c.py`; the frozen test was copied unchanged.

```sh
# reconstructed candidate
shasum -a 256 f1c.py test_full_history_binding.py
# 12f183a3… f1c.py; 271e6aa1… test_full_history_binding.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest test_full_history_binding.py -q
# 3 passed
PYTHONDONTWRITEBYTECODE=1 python3 f1c.py > reconstructed_13.json
# exit 0; 13 cases; result sha256 87fa57f6…

# exact original
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest test_full_history_binding.py -q
# 3 failed (DID NOT RAISE Hold for A, B, shared_witness)
PYTHONDONTWRITEBYTECODE=1 python3 f1c.py > original_13.json
# exit 0; 13 cases; result sha256 830b2dc9…
```

The three original failing mutations are preserved as historical evidence. The reconstructed candidate passes the same three named tests with `LIVE_A_HISTORY_CHANGED`, `LIVE_B_HISTORY_CHANGED`, `LIVE_SHARED_HISTORY_CHANGED`. The 13 case names are `SHARE`, `REFUSE`, `SILENCE`, `UNOBSERVED_SHARE`, `UNOBSERVED_REFUSE`, `B_SOURCE_SEVERED`, `B_SOURCE_RESTORED`, `E2_OMITTED`, `NO_B_RESOURCE`, `ENCUMBERED_B_TOOL`, `DUPLICATE_TOOL`, `NATIVE_SOURCE_SMUGGLED`, `RETROACTIVE_A`. Case set, expected and observed outcomes are preserved; the local result hashes differ from R5's historical hashes because this is a different replayed runtime (`87fa57f6…` vs `4de846b2…`; `830b2dc9…` vs `5c3b91dd…`).

## Targetless C10 court

```sh
cd .tmp-f1cr-recon
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest test_targetless_c10.py -q
# 14 passed in 2.62s
```

Positives:

- `test_refuse_silence_and_no_proposal_are_distinct_targetless_states` — REFUSE performer B; SILENCE performer None; NO_PROPOSAL no performer; three distinct receipt hashes; no C9 proposal/target/E2/practice/utterance; tick advances.
- `test_observed_vs_unobserved_access_differs` — observed SHARE `B_SHARED_TOOL`; unobserved SHARE no B event but tool access 1.
- `test_refuse_observed_vs_unobserved_differs` — observed REFUSE readable; unobserved REFUSE not readable; tool access 0 in both.
- `test_no_change_requires_competent_receipt` — no receipt -> `HELD_MISSING_RULE`; valid receipt -> `EVALUATED_NO_CHANGE`.
- `test_market_work_ledger_attached_to_targetless_refuse` — material ledger on the targetless receipt; `clamped=False`.

Negatives:

- `test_negative_sever_b_live_prehistory` -> `LIVE_B_HISTORY_CHANGED`.
- `test_negative_forged_shared_and_b_digests` -> `SHARED_HISTORY_CHANGED` / `B_HISTORY_CHANGED`.
- `test_negative_remove_b_resource_or_time` -> `B_HAS_NO_TRANSFERABLE_TOOL` / `B_TOOL_TRANSFER_RIGHT_DENIED`.
- `test_negative_refuse_without_performed_event` -> `REFUSE_REQUIRES_PERFORMER`.
- `test_negative_no_change_without_receipt_is_held_not_no_change` -> `HELD_MISSING_RULE`; malformed receipt -> `NO_CHANGE_RECEIPT`.
- `test_negative_unobserved_event_in_a_memory_is_refused` -> `UNOBSERVED_EVENT_IN_MEMORY`.
- `test_restore_preimages_reproduces_intended_state` — fresh preimages reproduce the same ledger, B/shared roots and durable history.
- `test_cold_replay_in_two_fresh_processes` — two separate processes return equal outputs and the same ledger hash.

## I1 same-person consumer

Detached I1 runtime at `7d44e300…`, with the output candidate copied into its `candidate/` and test under `tests/`.

```sh
BP4R_C9_DIR=$PWD PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -o addopts='' -q tests/test_i1_guarded_consumer.py
# 8 passed (baseline unchanged)

BP4R_C9_DIR=$PWD PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -o addopts='' -q tests/test_targetless_i1_consumer.py
# 5 passed
```

`TargetlessGuardedJoinedProduct` is the same I1 `GuardedJoinedProduct` with a durable `targetless_c10.json` under the same product root. Tests:

- `test_targetless_refuse_is_consumed_by_same_i1_person` — same product, `GuardedJoinedProduct`, B owner material readout remains `material_remaining=0` with inherited `material_delta=-1`; targetless ledger records `replenished=1`, `consumed=1`, `stock_after=0`, `clamped=False`; A public state unchanged; C12 still verifies.
- `test_silence_is_distinct_and_not_a_refuse` — SILENCE state, no B event, no tool.
- `test_observed_and_unobserved_share_differ_for_same_i1_person` — observable B event vs tool-only access.
- `test_cold_reopen_reads_same_targetless_history` — same targetless hashes after `reopen`, C12 verifies.
- `test_targetless_does_not_fabricate_c9_or_e2` — no C9 target/E2; A public state unchanged.

## Material ledger — I1 `material_delta=-1` with stock 0

The inherited I1 offscreen market event is preserved: B position `market`, cash `+2`, completed units `+1`, `material_delta=-1`, `material_remaining=0`. The adapter does not accept a negative delta without a source of stock.

- No prior stock/replenishment -> `MATERIAL_EXHAUSTED`; no event.
- Source-visible test-only replenishment `1` at tick 39, then one unit consumed at tick 40: `stock_before=0`, `replenished=1`, `consumed=1`, `stock_after=0`, `clamped=False`.
- Explicit refusal: `REFUSED_MATERIAL_EXHAUSTED`, `consumed=0`, stock unchanged.
- Non-stock tool action: `consumed=0`, stock unchanged.

The I1 event is not rewritten; the targetless continuity ledger carries the missing prior-stock receipt (or the refusal). This is the material reconciliation, not a silent clamp.

## Not run

- Native B/world, original CAN/ADP/SCI05/Pyat/C11/C12 execution.
- Original F1CR patched source (`SOURCE_NOT_FOUND`); no claimed recovery.
- Full V3/V2 historical suite, original survey/respondent data, LLM/provider calls.
- No PRE-MAIN/PR/CI mutation, no worker disturbance, no self-adoption.
