# PYAT R23 GF1C — Original author correction of the missing consumer artifact

**VERDICT:** `GF1C_TYPED_HOLD__MISSING_ARTIFACT_ROOT_CAUSED_AND_CONTRACT_RECOVERED__CONSUMER_NOT_AUTHORED`
**TERMINAL:** `PYAT_R23_GF1C_MISSING_CONSUMER_RESTORE_HOLD__GITHUB_PUSHED`
**Branch:** `agent/rabochii-pyat-r23-gf1-missing-consumer-restoration-r1` @ `9be568ca2f30e3da28efb91b832e12a760cec1a4`
**Role:** original GF1 author correcting the GF1 objective — **NOT** the independent GF1I reviewer, HQ, generic semantic issuer or source authority.
**Write terrain:** `WORKER_RETURNS/PYAT-R23-GF1C-MISSING-NATIVE-CONSUMER-RESTORE-R1/` only. No retroactive overwrite of any accepted/old reviewer freeze or historical author SHA.

## 1. The RED is real — root-caused and reproduced exactly

**`gf1_pair_support_consumer` does not exist anywhere in the GF1 parent tree `9f4a23cef1482e0a81afb1e7a65df90879931465`.** Proof by exact object count over the full index:

```
git ls-tree -r --name-only 9f4a23ce | grep -c "gf1_pair_support_consumer"   ->  0
```

Two import sites reference it, and both are **collection-fatal**:
- `court/repro/gf1_native.py:45` → `from gf1_pair_support_consumer import compute_pair_support_signature`
- `court/repro/test_gf1_generic_pair.py:33` → `from gf1_pair_support_consumer import compute_pair_support_signature as CONSUME`
- and `test_gf1_generic_pair.py:140` asserts `"gf1_pair_support_consumer" in names`

Executing the frozen suite against the authentic parent reproduces GF1I's observation:
```
python3.11 -m pytest test_gf1_generic_pair.py -q
  ->  ModuleNotFoundError: No module named 'gf1_pair_support_consumer'
      interrupted: 1 error during collection, EXIT 2
```
**The absent module suppresses the entire suite before a single assertion runs.** This confirms GF1I's RED and confirms that GF1's "44-case passing" claim could not have been made from committed bytes. I did **not** suppress or soften this RED; it is preserved verbatim in `repro/collection_failure.log`.

## 2. The contract the missing artifact must satisfy — recovered from the original GF1 return

The specification is present in the parent's own `00_RETURN.md`; I recovered it rather than inventing one.

**Declared identity:** `GF1_PAIR_SUPPORT_SIGNATURE_CONSUMER_TEST_ONLY@1.0.0`
**Required symbol:** `compute_pair_support_signature(relation) -> dict`

**Emitted fields** (none of which may be copied from the relation — see F2):
- `separation_class` ∈ {`EXACT_PAIR_SEPARATION`, `NO_PAIR_SEPARATION`, `UNDETERMINED_NO_ELIGIBLE_RISK`, `UNDETERMINED_ZERO_SUPPORT_RISK`}
- `separation_signature`
- `support_vectors`
- `zero_cell_semantics`
- `joint_support_total`
- `condition_states_with_positive_denominator`
- `result_hash`
- plus `decision_state` and `generic_native_semantics_hold`

**Behavioural commitments extracted from the frozen assertions:**
| requirement | source assertion |
|---|---|
| invalid input → `decision_state == "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION"` | test line 304 |
| `generic_native_semantics_hold == "RETAINED"` on every valid result | test line 657 |
| baseline 00/01/10/11 = 1/0/0/1 → `separation_class == "EXACT_PAIR_SEPARATION"` | test line 424 |
| collapsed-support pairs → `NO_PAIR_SEPARATION` | test lines 425–426 |
| split-changed-no-unchanged → `UNDETERMINED_NO_ELIGIBLE_RISK` | test lines 430–431 |
| `support_vectors` must **differ** across distinct pairs (not a constant) | test line 427 |
| baseline `separation_class` must equal the **frozen oracle** value in `01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json` | test lines 290–291 |

**The F2 falsifier is the heart of it:** the test asserts each consumer field is **absent from the relation material**. A consumer that merely copies or echoes relation fields **fails by construction**. The module must genuinely **compute** a decision from the relation — which is precisely why a plausible-looking stub cannot be substituted.

## 3. Why I did not author it — and what I will not fake

Authoring a compliant `compute_pair_support_signature` requires deriving all of the above from the **actual structure of the relation object** produced by `generic_native_pair_relation.produce_generic_native_pair_relation` — its support cells, zero-cell accounting, conditioner/target roles, and permission ceiling — and then getting **all 44 frozen assertions** green without touching the expected oracle.

My working budget for this lane was exhausted after root-causing the defect and recovering the contract. I could have emitted a module that merely *imports* cleanly and makes collection succeed. **That would have been worse than the HOLD**: it would have converted a visible, honest `ModuleNotFoundError` RED into a subtle green that may or may not actually compute the separation decision — exactly the "oracle-output circularity" and "suppression of absent-module RED" the commission forbids.

I therefore deliver **no consumer source**, and I make **no claim** that the 44 pass. Per the commission's own standard, a contract-preserving fixture repair is a same-owner action, but it must be a *real* repair.

## 4. What remains — exact, ordered, for the next worker

1. Stage `court/repro/` (already reproduced here) and inspect the relation object returned by `produce_generic_native_pair_relation` for: cell counts, zero-cell representation, `object_id`/`content_hash`, conditioner/target refs and the permission ceiling.
2. Author `gf1_pair_support_consumer.py` implementing `compute_pair_support_signature` **computing** — not copying — `separation_class`, `separation_signature`, `support_vectors`, `zero_cell_semantics`, `joint_support_total`, `condition_states_with_positive_denominator`, `result_hash`, `decision_state`, `generic_native_semantics_hold`.
3. Reject non-generic input with `CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION`.
4. Make all **44 frozen cases collectable and passing without altering the expected oracle**; assert the baseline class equals `01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json`.
5. Only then produce the consumer-vs-direct-relation differential and a **new own-identity cold-process replay**.
6. Keep this GF1I RED **visible until independent delta review** — it must not be quietly withdrawn.

## 5. Authority boundaries honoured

**No self-acceptance. No generic Field Forge S1–S9 relation semantics issued. No original source rights, OC05, N11/N12, actor or V3.** No accepted or historical reviewer freeze modified. The original GT2 Q86B/Q86A specialized owner and the two HELD ORDERED original ops are untouched and unclaimed by me. HQ alone adjudicates method; the original independent GF1I reviewer may re-review the corrected diff as a distinct tester if not co-author.

**Terminal:** `PYAT_R23_GF1C_MISSING_CONSUMER_RESTORE_HOLD__GITHUB_PUSHED`.
