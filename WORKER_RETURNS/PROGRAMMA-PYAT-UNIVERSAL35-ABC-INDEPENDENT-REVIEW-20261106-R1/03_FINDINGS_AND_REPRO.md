# Findings and exact reproductions

## 1. B F2/F3/F4 plan operations are not bound to the governed-frontier consumer — REVISE

`rawlsing_next/pre553_original35_operations.py:545-568` compiles the supplied frontier, then compares:

```python
requested = {
    code for op in plan.operations
    if op.kind in {OPERATION_F2, OPERATION_F3H, OPERATION_F4}
    for code in op.source_variable_codes
}
present = {
    target.item_id for operation in frontier.operations
    for target in operation.targets
} | {
    key.item_id for operation in frontier.operations
    for key, _ in operation.conditions
}
```

The plan also carries `item_ids`, `conditioner_values`, response/conditioner values, joint arity and operation identity, but none of those are passed to `compile_governed_frontier`. The check only verifies that some source variable code string appears as some frontier target/condition item ID. The test `test_terminal_current_governed_frontier_joint_consumer` (`rawlsing_next/tests/test_pre553_original35_operations.py:221-237`) builds the frontier independently with `_frontier_fixture(bundle)` and happens to use the same short codes (`A`, `B`, `Y`) as the synthetic config. It does not exercise a plan item ID or actual plan F2/F3/F4 operation payload.

Reproduction against a real pinned source pack (SRC31):

```text
f2_count 6 item_ids ('question_impl.phase0.09c8e496e3bfd3bad25a', 'question_impl.phase0.091f9a2b2e90afe75950') codes ('c13a', 'd18c')
BIND_REFUSED Original35OperationError GOVERNED_FRONTIER_PLAN_ITEMS_MISSING:b8,c10ai,c13a,d18c
```

The frontier was keyed by the plan's actual F2 `item_ids`; `bind_governed_frontier` still demanded the source variable codes. This is a disconnected consumer for F2/F3/F4. The F1 path is separately consumed and accepted in this review; the non-F1 claim is not.

**Owner:** B code owner + HQ. **Action:** either make B pass the plan's exact operation/item/conditioner identities into the governed frontier compilation, or explicitly limit the accepted scope to F1 and do not claim F2/F3/F4 current consumption. Re-run with a frontier keyed by plan item IDs, not only by matching short codes.

## 2. A/B `select` ABI is advertised but not consumable — REVISE joined seam

`rawlsing_next/source_configuration/ABI.json:31-36` lists `SourceConfigLibrary.select(source_id, source_root=...)` as an operation-adapter input. `SourceConfigLibrary.select` (`rawlsing_next/source_configuration/library.py:737-776`) returns a compact selection record (`schema`, source identity, counts, held, reader, resolution) and does not include `identity`/`binding`/`items`/`physical_slots`/`response_slots`.

B `_documents`/`_source_plan` (`rawlsing_next/pre553_original35_operations.py:59-70,217-233`) requires full source configuration fields. Reproduction:

```text
REFUSED Original35OperationError SOURCE_ID_REQUIRED
```

when all 35 `SourceConfigLibrary.select` records are passed to `build_original35_operation_plan`. The working integration path is `SourceConfigLibrary.load_original(sid).document`; that produced the full 35-row plan and matching `plan_ref`:

```text
{"counts":{"ABSTAIN":0,"DEFERRED":51,"EXECUTABLE_RAW":5630,"HELD":4655,"INAPPLICABLE":8131,"NOT_REQUESTED":0}, "items":18276, "joints":[20,742250526], "no_drop":true, "operations":18467, "pairs":[120,1862592], "plan_ref":"3e3a604a78c377030bffa39eb62cf065d111746f9bc1588f7dbf33bac0373b9c", "rows":35, "slots":18413}
```

**Owner:** A + B + HQ. **Action:** either add the full config document to the advertised select ABI (or explicitly name `load_original` as the B input), or make B accept the compact selection and resolve the exact artifact itself. Do not claim the advertised A/B ABI is frozen until the actual caller path is demonstrated.

## 3. B return status counts disagree with its own evidence — REVISE return

B `00_RETURN.md:73-74` reports:

```text
EXECUTABLE_RAW 5,630; HELD 1,595; ABSTAIN 0;
INAPPLICABLE 11,191; DEFERRED 51; NOT_REQUESTED 0
```

B `evidence/all35_plan.json` `whole_plan.counts` and the independent A/B rebuild report:

```text
EXECUTABLE_RAW 5,630; HELD 4,655; ABSTAIN 0;
INAPPLICABLE 8,131; DEFERRED 51; NOT_REQUESTED 0
```

Both sum to 18,467, but the held/inapplicable split is wrong in the return. The plan_ref, item/slot totals and pair/joint counts are consistent. This is a reporting defect, not a plan-ref mismatch.

**Owner:** B author/HQ. **Action:** correct the return text or explicitly label the 1,595/11,191 figures as a superseded run. Keep the evidence file as the authoritative machine receipt.

## 4. C exact donor identity and current-base tests — ACCEPT_SCOPED_SOURCEFREE

`rawlsing_next/_pre553_c11_execution_view.py` is byte-identical to the accepted donor view `02c1200b82b8397e551817e8e4cf2c6763413189:rawlsing_next/_pre553_c11_execution_view.py` (blob `986f327aa18053edc61bd837cdded02bbf8388d9`). The selected test file differs from the donor test only by author-added cross-shape coverage (blob `e6c002334724aefff7d61e0165577a30d8dc3a8d`).

Independent runs:

- `test_pre553_c11_execution_view.py`: 10 passed in 6.09s.
- `test_pre553_carrier_execution.py` + `test_pre553_i03_grouping.py`: 19 passed in 5.92s.
- Covered cache poison/rehashed-key rebuild, delete/rebuild, stale/torn publication, revoked-workload no-cache, old-cache read, compressed chunk bounds, five cross-shape exact facts, and ordered/ranked/repeated/weighted/routed states.

C does not claim real-source cold/warm performance or all35 native execution. Those remain NOT_RUN.

## 5. Positive A checks

- `test_source_configuration_current_port.py` + `test_source_configuration_library.py` + `test_source_configuration_foundation.py`: 33 passed in 81.12s.
- `test_pre553_source_read_admission.py`: 5 passed in 1.16s.
- 35/35 `validate_source` passed in 52.96s.
- 35/35 `build_fixture_release` matched recorded native fixture content hashes in 124.87s.
- Index counts: 18,276 items / 18,413 slots / 18,250 exact joins / 26 unmatched.
- 35 relative locator bindings match the custody observation; no source-root absolute path is in the production locator file.
- 119-path ledger has 119 unique expected paths and no missing/extra path.

A remains sourcefree and does not prove original decode, native all35, source rights or science.

## 6. Non-blocking observation

A's committed proof `evidence_source_root_override.json` contains author-workspace absolute probe paths even though the production `source_locator_bindings.json` is relative and no absolute path is in product code. This is not a code defect, but any publication/privacy policy that treats return evidence as public should redact those probe paths.
