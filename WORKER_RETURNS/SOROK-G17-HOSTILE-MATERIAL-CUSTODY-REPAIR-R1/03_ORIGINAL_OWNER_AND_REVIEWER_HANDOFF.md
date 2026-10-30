# G17 — original owner and independent reviewer handoff

Observed FINDING: the candidate overlay closes the three original reviewer REDs under their unchanged assertions and preserves the author’s positive court. Causal INTERPRETATION: the missing capability was owner-canonical material authentication and recursive embargo partitioning, not a new psychological or C9 rule. Proposed HQ ACTION: hand the three candidate blobs to the original G17/C9 owners, then to a separate source-qualified reviewer for replay; no merge or adoption here. Accountable OWNER: original G17 author, C9 owner and incumbent HQ intake.

## Exact apply instructions

Base: original G17 return at `90d0eb7925de54635559a879ee76fc1b97b9ff61`. Candidate overlay:

- `candidate/lab_sgi1/continuation.py` → author `candidate/lab_sgi1/continuation.py`
  - original blob `c9318dcf33d041a673cfae15aff8fc51712f53e7`
  - candidate blob `705ef1a4568ec84020638b3cf32d348066945e86`, SHA-256 `80823bde776f09a2ae7bf02dd7458982625a318fb9248228a5df2401e88d9426`
- `candidate/lab_sgi1/pipeline.py` → author `candidate/lab_sgi1/pipeline.py`
  - original blob `fc954993ef966d20d1915546e04a122daa93538f`
  - candidate blob `d07bb06c7a44cd337a43c387f55a17906c5307e3`, SHA-256 `b5d19758da9b8115642e832efff17343cebfab1987fb37cf5afbfc59b362376c`
- `candidate/c9_handoff_consumer.py` → author root `c9_handoff_consumer.py`
  - original blob `47e59c12b79c04b05c18e73ad76078a29d0d7b3c`
  - candidate blob `bd7a179e846e4067e324360fc3411806b2a537d4`, SHA-256 `2c0430340512b7c2447c73de019227481f43f7156ba3d1b19d1fd8e16f7f4c6d`

Replay against the original reviewer test `83f17006…`/JUnit baseline `0dec3faf…`:

```sh
cd <g17-reviewer-return>
cp <candidate>/lab_sgi1/continuation.py target_candidate/lab_sgi1/continuation.py
cp <candidate>/lab_sgi1/pipeline.py target_candidate/lab_sgi1/pipeline.py
cp <candidate>/c9_handoff_consumer.py target_candidate/c9_handoff_consumer.py
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_g17i_independent.py -q
```

Expected: original baseline 11/3; patched 14/14. The author positive replay uses the same three files in author `candidate/` plus the root C9 file and `tests/test_g17_material_history_consumer.py`; expected 13/13.

## What the patch actually enforces

1. `continue_person` reconstructs the owner-canonical material event (`material_joint_opportunity(effective_index, permit, material_units)`) and requires exact equality before using payment/task hours/units. It also checks the participation event preimage and that the material event is an explicit causal parent. A forged +100000 payment cannot supply cash 100058.
2. `FutureChildPartitionGuard` recursively traverses nested dict/list/string fields. The nested `metadata.future_child_personality` alias is refused as `FUTURE_CHILD_INFORMATION_LEAK` before any proposal, selection, construction or COMMITTED output.
3. `c9_handoff_consumer.receive_handoff` authenticates the material source against the owner-canonical event and requires the handoff payload to match before accepting the after-state. Forged cash 100055 is refused with `MATERIAL_SOURCE_NOT_AUTHENTIC`.

No assertion was weakened: the original tests remain byte-identical and still assert `None`, `status != COMMITTED`, and `pytest.raises(C9Refusal)`. The candidate does not turn a failure into a success by changing the oracle.

## Preserved holds / do not overread

- SCIENTIFIC: test-only sourcefree material/current-state method. No native person, child, biology, calibrated psychology, original survey, CAN/ADP/SCI05, Rule A/T or C11/C12 authority.
- AUTHORITY: no merge, adoption, production, PR514/516/519 or PRE-MAIN change. The original G17/C9 owners retain decision rights.
- C9: the bounded material handoff is exercised; full C9 E1/RULE_A/RULE_T/E2 remains `HOLD_UNISSUED`. No durable C9 store reopen is claimed.
- M2/MP: typed coverage HOLDs remain; no fabricated archive grammar or F_EXISTING history.
- The first actual consumers in this slice are `continue_person`/`forward_continuation` for the material action, `run_pipeline` for the future-child guard, and `receive_handoff` for the C9 material handoff. No native/live consumer is claimed.

## Reviewer requirements and questions

The reviewer must be separate from this author and the original G17 author/C9 owner, source-qualified, and appointed by incumbent HQ. Reviewer should:

1. Verify the three original and three candidate blobs byte-for-byte.
2. Replay the original 11/3 RED and patched 14/14 with the same test file.
3. Replay the author 13/13 positive suite and cold-process reruns.
4. Attack the candidate: forged material with altered units/hours/permit/effective index; nested keys in lists/values; altered handoff payload; severed parent; wrong owner/permission; C9 same-consumer path.
5. Decide whether exact canonical material equality is the correct owner law or whether an owner-issued alternative material schema is required.
6. Confirm all M2/MP/Rule A/T/C9 E2 holds remain; do not promote the test-only material positive to native science.

DONE: exact patch mapping, replay commands, original REDs, preserved holds, reviewer questions. REMAINING: original owner replay and independent review. CRITICAL BLOCKERS: C9 E1/E2, M2/MP and native authority; none block the bounded engineering candidate. LARGEST PRODUCTIVE MOVE: original G17 author applies the three blobs and replays; C9 owner reviews the receive boundary. FLIGHT: sourcefree local Git/Python; no original branch, PRE-MAIN or PR mutation. DELTA: owner/source authentication and recursive embargo containment are restored under unchanged assertions, with all prior negatives preserved.
