# P3 compression native-binding repair — bounded return

**Worker:** `sorok-p3-compression-native-binding-repair-r1`  
**Branch:** `agent/sorok-p3-compression-native-binding-repair-20261106-r1`  
**Startup / protected:** `501f646199bc28197d5dbb3966d016669b51c44b` / `c852d7516e23fcb6cf2215e9be7c5fa268503516`  
**Scope:** sourcefree TEST_ONLY metadata binding repair only.

## Result

**PASS_SCOPED__ACTUAL_P2_E1_ACTION_PERCEPTION_BINDING_REPAIRED**

The demonstrated defect was repaired. `bind` now follows the accepted
P2Owner relationship:

```text
native objective event
  e1_event_id / e1_event_hash              (E1 occurrence)
  action_event_id / action_event_hash      (actual action event)
  -> developing actor's accessible perception event_id == action_event_id
  -> perception clock/channel
```

It no longer compares the actor's accessible event ID to `e1_event_id`.
The E1 occurrence ref/hash and the action event ref/hash are retained as
distinct fields:

- `actual_event_ref` / `actual_event_hash` = E1 occurrence
- `actual_action_ref` / `actual_action_hash` = action event
- `perception_refs[].event_id` = actual action event ID

There is no E1/action-ID equalization, aliasing, substitution or rewriting.

## Actual producer-consumer receipt

One actual sourcefree P2 owner event was executed through the original
`load_p2()` factory, `case_for`/`source_for`, and actual participants, with an
`ACTUAL` interval. The compression layer made no owner call and issued no
world event. The actual realized document bound successfully.

Actual receipt:

- E1 occurrence: `TEST_ONLY_BP2_E1_OCC-0002`
- E1 hash: `a81f7b77e6b3dd962a0368e10f5eeeb6404cfc3ca994b145e606874131421bb2`
- Action event: `TEST_ONLY_BP4_WORLD_EVT_7f30b86812802bff54dbfb77f81ac06481d5aae255d5e0a2703cd5598ef4a416`
- Action hash: `39689960a200953c5b99edcb23efcb08d14b8e62820bad83e75cb126e13cea23`
- Actor access: `OBSERVED`, actor `TEST_ONLY_BP1_R26V_ACTOR_A`
- Perception: `co_present` at clock `228`
- Actual interval: `PARTIAL`, receipt
  `5438e358b9ee26d4e4e718600a694384337ac0142e1e4d91fc8f39478c64676c`
- Realized document SHA-256:
  `5353a21349f31d3ff75ccab0fee28c8b567d8b164bb50095d24d8f22c6021493`
- Bound envelope hash:
  `eb8e6676b30d1e52e2d72418c61f69143b2bc14fe7b32b0ebb036e287b994d9b`

The exact compact producer-consumer receipt is
`evidence/compression-native-binding-repair/actual_p2_receipt.json`.

### Negative/restore checks on the actual output

- Remove actor perception: **HELD**
  `ACTOR_PERCEPTION_UNAVAILABLE_FOR_PRESENT_EVENT`
- Substitute the accessible action ID: **HELD**
  `ACTOR_PERCEPTION_UNAVAILABLE_FOR_PRESENT_EVENT`
- Remove the E1 action binding: **HELD**
  `ACTUAL_ACTION_BINDING_UNAVAILABLE`
- Restore the exact original producer output: **BOUND**, equal to the original envelope.

The actual interval `PARTIAL` schema is preserved; no replacement interval
owner or positivity requirement was invented for `SINGULAR_OCCURRENCE`.

## Changed scope

Only:

- `p3/compression.py`
- `tests/test_compression.py`
- new `evidence/compression-native-binding-repair/`

Original `evidence/compression/` and `evidence/compression_intake_actual.json`
remain unchanged. No accepted P2/704, contracts, engine, rules, projections,
stores, sourcepack, production registry or PROGRAMMA changes.

## Tests

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
PYTHONPATH=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1 \
python3 -m pytest \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_compression.py \
  -q -o addopts="" -p no:cacheprovider
```

Observed: **23 passed in 4.89s**.

The 22 prior mechanical tests remain covered with distinct realistic E1/action
IDs and no equalization; the added regression runs one actual sourcefree P2
owner event and binds its actual RealizedEvent. The four representation forms,
empty psychological effects and all prior source/identity/clock/interval
negative cases remain meaningful.

## Source pins

- P2Owner: `fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0`
- Contracts: `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d`
- Integration contract: `0c728671db1c8271e27be48872678adef89de7eea9e92e6c59d3ad7c5c0806af`
- Compression implementation: `49df70d60cbc3b37ec3e484c5a7c64e14ac174faafe8fcaa02e5428c583be4f4`
- Tests: `80e1f5b850255f879d186cfc5442d2d6cacad62425a0b228c7886bc980dba6bc`
- Actual P2 receipt: `1f8975c0c98f3c39c2917e5c8a5c90224a4452a78eadf1dce80995906e9ac885`
- E1 candidate: `ee1ff298fe7e57277c34a5af16df33165743d84f` — candidate only
- S1 candidate: `5a505a911509073eb38102f0022f445e7ec602e5` — candidate only

## Runtime / passport

- Assigned model: `opencode-go/deepseek-v4.1-flash#max`
- Runtime observed: `opencode v2.0.22`, Python `3.11.3`, Darwin `22.3.0 x86_64`
- Quota: **UNKNOWN_UNOBSERVED**
- Sourcefree execution only; one actual P2 event, zero P2 batches, no compression-layer
  owner calls or world events.

## Known limits / remaining work

- This is one actual P2 binding regression, not the integrated A–H P3 product.
- No psychological writer, memory/claim issuance, ADP-016/017 authority, native
  science, source issuance or human validity is claimed.
- Actual P2 wrapper integration and full integrated acceptance remain HQ work.
- The compression layer remains metadata only and emits empty
  `psychological_effects` with `no_state_mutation=true`.
- An actual native event whose actor access is unavailable, whose action
  binding is absent, or whose accessible event does not match the actual action
  remains HELD/refused even if a portal-user view exists.

## Evidence / commit

- `evidence/compression-native-binding-repair/00_RETURN.md`
- `evidence/compression-native-binding-repair/TEST_RESULTS.json`
- `evidence/compression-native-binding-repair/SOURCE_PINS.json`
- `evidence/compression-native-binding-repair/PASSPORT.json`
- `evidence/compression-native-binding-repair/RECEIPTS.json`
- `evidence/compression-native-binding-repair/actual_p2_receipt.json`
- `evidence/compression-native-binding-repair/pytest.log`
- `evidence/compression-native-binding-repair/MANIFEST.json`

**Commit:** `PENDING_ARTIFACT_COMMIT`  
After commit, push and verify this exact branch, then stop. This author pass is
not independent final-runtime acceptance.
