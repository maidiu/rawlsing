# S40 generated native speech — independent REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `1d6f89b2ef60f4713741c9432c63940737248984`.
- Branch: `codex/sorok-s40-generated-native-speech`.
- Base: accepted S39 `e41513fa65601a37e7b3b430d26c626ae0217d90`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`,
  language `8d2920d…`, JOIN-E `7bf2da3…`.
- Reviewed in a disposable clone. No product edits, provider/model calls,
  controller-attachment changes, or native/science action.

## Executed checks

```text
PYTHONPATH=<S40 return> M35_JOIN_E_RETURN=<warm JOIN-E> \
  python3 -B -m pytest -q <S40 return>/tests -p no:cacheprovider
7 passed in 2.09s
```

The entrypoint also exits 0 and produces the four expected chains: share request
uses Spanish native speech and labeled English, generated refusal does the same,
denied refusal has no speech and valid-empty C9, nonverbal inspection has no
speech. All preserve `NO_CHANGE/NO_PROPOSAL` and zero target rows, with cold
verification.

Targeted plan-binding falsifier:

```text
SOROK_REVIEW/S40/oracles/s40_e1_plan_binding.py
```

Result: **0 PASS / 1 FAIL**. The actual admitted E1 is
`TEST_ONLY_BP2_E1_OCC-0001`; the authorized plan's public
`ADMITTED_E1` fact instead has `event_id` equal to the E1 hash:
`8efc87075cf70bdd6b9dc73dc4bcb0942dff094a6fb627d476d87bd280b26aad`.
The plan therefore does not bind the actual E1 event ID.

## Blocking defect

`s40/language.py` `make_plan` constructs the public E1 fact as:

```python
"kind": "ADMITTED_E1",
"event_id": generation_receipt.get("event_ref", ""),
"event_hash": generation_receipt.get("event_ref", ""),
```

`generation_receipt.event_ref` is the E1 hash, not the E1 event ID. The actual
E1 ID is available in the C8/session binding. `read_s40` does not validate the
plan's public E1 fact, so warm and cold reads accept an authorized plan whose
E1 event_id is wrong. This violates the required exact source/event binding of
the plan before wording/commit.

## Required repair

Use the actual E1 event ID and E1 event hash separately in the plan's
`ADMITTED_E1` public fact (or remove the fact and bind the E1 identity through
the existing exact C8/session source). Add a focused assertion for the plan's E1
event ID in the warm/cold reader. Re-run the seven focused tests and this
oracle; keep the existing share/refusal/nonverbal/denial/no-target behavior.

## Receipt

- 7-test output: `evidence/s40-tests-7.out` SHA-256 `7d887e80…`.
- Entrypoint output: `evidence/s40-entrypoint.json` SHA-256 `db40eae6…`.
- E1 plan-binding oracle output: `evidence/s40-e1-plan-binding.json` SHA-256
  `37fb742c…`; FAIL.
- Oracle: `oracles/s40_e1_plan_binding.py` SHA-256 `c38ed92f…`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
