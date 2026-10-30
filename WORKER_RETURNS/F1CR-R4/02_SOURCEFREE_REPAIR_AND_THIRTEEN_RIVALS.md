# Sourcefree repair and thirteen rivals

## 1. Exact cut

- F1C author return: `bcea367e7dc0f2e069de71b0fe5e481de094dad5`.
- F1C executable blob `104f5bd7826c8676192eac96753d980e35d8a80a`, SHA-256 `7e3492a267acbc0fa11d8792158bdaa2acc9dfb6053f16141ed637dc1cd2881b`.
- F1CI3 reviewer: `0a884fd5af7ebb97f4cc0ef8c1251386641732f0`.
- R31J: `64fec28c374d8f77fb0b412d0c934d798ede03e8`; JOIN-E: `7bf2da302996491ddf34b9a039fea47ac982d135`; QF2: `a93db6bce4832270cf29727233dbfbc5f0312395`.
- Unchanged p01 blob: `f53ad1bffb4dcd7fc0edc27ccbd3362d64ca1aa8`.
- Frozen root: `30fc98b9babdbb089573eccb4790baf7886bee44b56314eb4cac932ba1aeee5d`.
- Prior roots: A `c71024e9…`, B `f94ea0c4…`, shared `e7f9bb7d…`.
- All 27 source pins are in `01_LIVE_HISTORY_MUTATION_NEGATIVES.json`.

The 13 original outcomes are the F1C executable’s own cases, not 13 pytest passes:
SHARE, REFUSE, SILENCE, UNOBSERVED_SHARE, UNOBSERVED_REFUSE, B_SOURCE_SEVERED, B_SOURCE_RESTORED, E2_OMITTED, NO_B_RESOURCE, ENCUMBERED_B_TOOL, DUPLICATE_TOOL, NATIVE_SOURCE_SMUGGLED, RETROACTIVE_A.

## 2. Minimal repair

Only the F1C executable is changed, in the temp candidate. The patch adds:

```python
def live_prior(life):
    return {
        "A": {"snapshot": life.a_snapshot,
              "events": [dataclasses.asdict(e) for e in life.a_ledger.events]},
        "B": {"snapshot": life.b_snapshot,
              "events": [dataclasses.asdict(e) for e in life.b_ledger.events]},
        "shared": {"material": life.material, "witness": life.witness,
                   "objective": life.objective},
    }
```

and, at the start of `same_receiver_assertion`, before `intervene`/C8:

```python
    live = live_prior(life)
    require(digest(live["A"]) == digest(frozen["prior"]["A"]),
            "LIVE_A_HISTORY_CHANGED")
    require(digest(live["B"]) == digest(frozen["prior"]["B"]),
            "LIVE_B_HISTORY_CHANGED")
    require(digest(live["shared"]) == digest(frozen["prior"]["shared"]),
            "LIVE_SHARED_HISTORY_CHANGED")
```

No original test, assertion, p01 case, source-severance case, material ledger or targetless case is changed. Patched program SHA-256 `18c96f97…`; patched Git blob `bf7e625e…`.

The F1CI3 negative test is preserved and now passes:

```python
@pytest.mark.parametrize("changed_input", ["A", "B", "shared_witness"])
def test_changed_live_prior_is_refused(tmp_path, changed_input):
    life, frozen, expected = F.freeze()
    if changed_input in {"A", "B"}:
        ledger = life.a_ledger if changed_input == "A" else life.b_ledger
        event = next(e for e in ledger.events if e.kind == "RELATION_VIEW")
        event.payload["perceived_state"] = "F1CI3_POST_FREEZE_DRIFT"
        assert ledger.verify()[0] is False
    else:
        life.witness["status"] = "F1CI3_POST_FREEZE_NOT_WITNESSED"
    assert F.digest(frozen) == expected
    with pytest.raises(F.Hold):
        F.same_receiver_assertion(tmp_path, life, frozen, expected)
```

## 3. Actual results

| Court | Actual |
|---|---|
| Original F1C 13 | **13/13 expected outcomes**, exit 0 |
| Original F1CI3 mutation test | **3 failed**, `DID NOT RAISE Hold` |
| Patched F1C 13 | **13/13 same outcomes**, exit 0 |
| Patched F1C 13, second process | **13/13**, same p01/hold/terminal/access fields |
| Patched F1CI3 mutation test | **3 passed**, distinct live A/B/shared codes |
| JOIN targetless REFUSE regression | **1/1 passed**, read-only source |

JUnit SHA-256: original mutation `5f854fea…` (3 RED), patched mutation `02f59236…` (3 PASS), JOIN targetless `a37aaeab…` (1 PASS). F1C result JSON is retained by hash in `01`; the 13-case program is not a JUnit suite.

### Mutation evidence

| Mutation | Original | Patched |
|---|---|---|
| A `RELATION_VIEW.payload.perceived_state` | accepted; p01 true | `LIVE_A_HISTORY_CHANGED` |
| B `RELATION_VIEW.payload.perceived_state` | accepted; p01 true | `LIVE_B_HISTORY_CHANGED` |
| shared witness `status` | accepted; p01 true | `LIVE_SHARED_HISTORY_CHANGED` |

The check is before any `intervene`, `Receiver`, C8 or C9 construction. The mutation test’s own `ledger.verify()` remains false in the A/B cases; the repair does not repair or hide the changed ledger.

## 4. Physical and negative invariants

- SHARE, B_SOURCE_SEVERED and B_SOURCE_RESTORED: terminal tool **A=0, B=0, spent=1**; material **A=3, B=0, spent=1**; B free hours **11**; source-severed `B_source_admitted=False` with the physical transfer retained.
- E2_OMITTED: terminal tool **A=1, B=0, spent=0**; material **A=4, B=0, spent=0**.
- UNOBSERVED_SHARE: `A_tool=True`, `A_B_act=False`; B motive remains `UNKNOWN`.
- REFUSE: `TEST_ONLY_INTERVENTION`, performer `B`, `A_event_access=True`, `A_tool_access=False`.
- SILENCE: `NON_EVENT_CONDITION`, performer `None`, `A_event_access=False`, `A_tool_access=False`.
- REFUSE/SILENCE/UNOBSERVED_REFUSE: exact `C9_RECEIVER_HOLD:later_e2:NO_PROPOSAL`; p01 NOT_RUN.
- RETROACTIVE_A remains `A_B_OR_SHARED_PREHISTORY_CHANGED`; no fake acceptance.
- B evidence remains `TEST_ONLY_COUNTERFACTUAL_INTERVENTION_NOT_NATIVE_B`; no independent B or motive is manufactured.

## 5. Targetless receiver

Existing JOIN source `joined/refusal.py` blob `9a8726fe…` provides `RefusalProduct`, `RefusalSession.start/open` and `validate_targetless`. Its original targetless provenance/lineage/fork regression passes 1/1. It is **read-only evidence**, not an F1C adapter:

- `RefusalSession.start` hardcodes an original R31J evaluated input and original actor/source identities; it does not accept F1C frozen roots or a SILENCE packet.
- F1C REFUSE/SILENCE still stop at `later_e2:NO_PROPOSAL`.
- Original C10 still has no targetless read path; no zero/empty target or CREATE action is synthesized.
- The F1C material handoff is not a durable C9 store; no cross-cut acceptance is borrowed.

The targetless continuation is therefore `HOLD_OWNER_SEMANTICS_UNISSUED`, not a repair, a fake REFUSE, an evaluated NO_CHANGE or a new C10 target.

## 6. FINDING / INTERPRETATION / ACTION / OWNER

**FINDING:** Three live-history mutations survived the original consumer because it bound only the detached frozen value and snapshots. The added live A/B/shared digest binding refuses all three before C8 while preserving the 13 outcomes and physical/negative invariants.

**INTERPRETATION:** The F1C SHARE receiver now enforces the complete consumed projection against the accepted frozen roots. The targetless continuation remains a separate owner-semantic problem; existing JOIN REFUSE machinery is useful evidence, not an F1C adapter.

**ACTION:** Original F1C adapter/C8/R31J owner replays the patched cut; JOIN/BP2P4/C9/C10/C12 owners decide REFUSE/SILENCE/C10 continuation. No merge or adoption.

**OWNER:** Original F1C adapter owner; R31J/C8 owner; JOIN/BP2P4/C9/C10/C12 owners; incumbent HQ; distinct reviewer.

## 7. RUN / NOT_RUN

- **RUN:** original 13, patched 13 (two processes), original/patched 3-mutation test, JOIN targetless 1/1.
- **NOT_RUN:** JOIN whole suite, native B/world, C10 native contract, F1C SILENCE targetless cold product, acquisition/transfer, A4/A5 human, production, QF2.
- **NOT CLAIMED:** independent B, Rule A/T, evaluated NOCHANGE, acquired practice, durable C9/C12, adoption.
