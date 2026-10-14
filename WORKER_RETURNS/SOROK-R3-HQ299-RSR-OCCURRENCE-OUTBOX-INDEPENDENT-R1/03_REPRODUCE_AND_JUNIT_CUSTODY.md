# HQ299 RSR — exact source-free independent reproduction

## Pinned executable closure (all in this folder)

The test-only prototype and original suite are *unmodified, byte-identical* copies from HQ298 SR `8da45605c267ea60b664d00fc8444d8c9b007628`.

| File | Git blob SHA-1 |
|---|---|
| `outbox_prototype.py` | `fe429516e48f63035457bcff5431d2da4f26f8d3` |
| `test_sr_28_falsifier_court.py` | `a6263f8903f22da2b1cde3999d950328d19c9e21` |
| `FROZEN_S01_S28_ORACLES.json` | `782ba75ee94f24908100b1f3464e7035497d546c` (original SR `99f2e7128a8417dfeaa39468c45ba65f6958c061`) |
| `test_rsr_independent.py` | `044b9cb48c2e4e3d825e7a2cbb52bb412d1366d7` |
| `rsr_cold_replay.py` | `0c8676aaa3ff6605f3fb7a987e29f88d26fafb03` |
| `test_rsr_cold_replay.py` | `ad132e7e852d3873597276b51afda86b8296f891` |

In a fresh eligible Python3/pytest runtime, *from this directory*, without a full repository checkout:

```bash
python -m pytest -q test_sr_28_falsifier_court.py::test_s27_material_move_needs_world_owner --junitxml=first_s27.xml
python -m pytest -q test_sr_28_falsifier_court.py --junitxml=original_28_junit.xml
python -m pytest test_rsr_independent.py -q --junitxml=independent_raw_junit.xml
python -m pytest -q test_rsr_cold_replay.py --junitxml=cold_junit.xml
```

**Actual separate independent S1 run results:**

```text
S27 first discriminating test:   1 passed in 0.09s           exit 0
HQ298 original test file:       28 passed in 0.06s          exit 0
HQ299 independent strict test:  12 failed, 5 passed in 0.65s exit 1
HQ299 subprocess cold replay:   2 passed in 6.74s           exit 0
```

These numbers were obtained from actual local pytest commands, and are NOT claimed from GitHub or an unexecuted static trace. The 12 real independent failures are deliberate **RED acceptance findings**, not `xfail`, skipped, or discarded. Full test names, causes and exact JUnit hashes are in `01_EXECUTED_REVIEW_MATRIX.json`.

## Raw executed JUnit integrity

| Artifact | SHA256 |
|---|---|
| `first_s27.xml` | `081496859004776ee27a8e4c0bf7a51913acd4f8fc849b495c9e23851f268248` |
| `original_28_junit.xml` | `6f3fe907e53fc8aa86895e3eb55fa214396fd89088c9f0d07743d69fa2b73ced` |
| `independent_raw_junit.xml` | `5b4bb8c219c1741b0371fce0121540064ac2db610f935382bd0f346c5fe0a648` |
| `cold_junit.xml` | `9153d855fe0caa3d6b7e956f9de388841fcad8de7f24a069fca2a406ea3b28e7` |
| Raw executed-JUnit/stdout archive `rsr_hq299_run_evidence.tar.gz` | `6be368ac0ba6abc172ee20ec6bdd8e54800bc5bda5190af6fece8a5a07d33744` |
| Exact executed-source/JUnit/stdout archive `rsr_hq299_executed_sourcefree_bundle.tar.gz` | `528fcb1e9f9323d4015b695c7e664a98f8f8e14cbed265c8eb7738c23f261350` |

The two archives are **ephemeral conversation attachments** supplied with the final chat response, **not GitHub files**. This GitHub return includes all executable source and the complete machine-readable outcome/failure custody, but GitHub does not carry the raw JUnit text. Do **not** claim that a raw JUnit file exists in the remote branch. Verify any transferred archive against these SHA256 values. Re-running tests is the authoritative method for a new host.

## Cold crash/restart harness limits

`test_rsr_cold_replay.py` invokes **fresh Python subprocesses**. The helper `rsr_cold_replay.py` makes exact source-free state records with a JSON temp file and `os.replace` *outside* the SR prototype. On a simulated crash (`os._exit(79)`) **after the harness has saved** one event+emission, the next process reloads one event with unchanged identity and can deliver+ACK without promoting human perception.

A separate crash **after an in-memory admit and before an explicit save** restores zero events from the last persisted baseline: the current prototype has no durable commit coupling at all. In other words, the positive is a test of externally supplied snapshot persistence, **not** proof of an atomic ADP019 event/outbox transaction. Neither case proves cross-process locking, parent-directory fsync, client/transport exactly once, human actually seeing the artifact, or a real V3 actor/event.

## Raw code-source vs actual frozen oracle

The unmodified original 28 tests check only their written assertions; several do not exercise their frozen oracle's full meaning. Specifically S27's positive `mug_position='hand'` is contrary to the frozen oracle's missing-world-owner `HOLD`; S28 commits and then intentionally restores *before*-commit state instead of checking a missing causal-time DEFER; S17 never persists or crashes. In this exact sourcefree scope, `28_PYTEST_PASS` != `28_SEMANTIC_ORACLE_PASS`.

**Stop boundary:** no paid model call, original surveys, generated V3 actor, live renderer, accepted CAN/ADP modules, real physical object, or product user was operated in these tests.
