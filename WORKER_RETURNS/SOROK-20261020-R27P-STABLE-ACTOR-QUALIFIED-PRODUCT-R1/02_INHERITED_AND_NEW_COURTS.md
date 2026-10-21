# R27P inherited and new courts

| Suite | Source | Result |
|---|---|---:|
| R27P stable court | `tests/test_r27p_stable.py` | **7/7 PASS** |
| Seven faults | `stable_actor_binding.seven_actor_source_faults` | **7/7 proves** |
| Inherited R26V | `tests/test_inherited_r26v.py` (fd32e0b) | **10/10 PASS** |
| R26E 129 | not staged | **NOT_RUN** |
| Native ports | `native_ports.py` | **10/10 fail closed** |

Commands:

```bash
PYTHONPATH=candidate:../.. python3 -m pytest -q tests/test_r27p_stable.py
PYTHONPATH=candidate:../.. python3 -m pytest -q tests/test_inherited_r26v.py
```

The inherited R26V test file uses R26V’s `historical_actor_producer` and its original global seam. It is reproduced as an inherited test only; R27P’s new tests use `stable_actor_binding`.
