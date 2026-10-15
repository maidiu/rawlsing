# Reproduce E05R

Use private maidiu/rawlsing Git object access, Python 3.11 and pytest. Run from this return directory:

```
python3 repro/import_inputs.py
python3 repro/stage.py
python3 repro/activate_candidate.py
python3 repro/run_repair.py
```

`import_inputs.py` reconstructs the exact E05, E05I and E04N evidence from sealed Git objects with blob verification. `stage.py` is byte-identical to E05I's exact 401-object staging script, located at the normal return depth so its Git pathspecs resolve correctly. Nothing is copied from another worker's runtime or the Desktop data estate. All artifacts remain inside this E05R return. `inputs/` and `runtime/` are reconstructible and ignored.

`activate_candidate.py` copies only `candidate/e05r_selected_world_adapter.py` to the legacy module import path expected by the frozen E05/E05I tests. It preserves `original_source_manifest.json`, then replaces exactly one manifest row with the new candidate's explicitly labeled local version/hash. All 400 other staged objects, all six E04 product files, 271 original tests and 55 E05I tests retain their original bytes. The request/acceptance/receipt schemas are @2. No expectations, parametrizations, asserts, skips or xfails are changed. The profiler conftest and court_support.py remain original. The suite runner alone gains failure exit propagation.

The additional suite uses `--noconftest` with explicit original runtime/repro paths; the unchanged 55-case court retains its original profile and imported-file verification. Both cold interpreters reconstruct synthetic fixtures, not a durable real permission store. Optional consumers must be the exact two original clients under their default budget and validated finite proposal grammar; scalar reverse-target receipts can omit these fixed forward clients. With consumers supplied, the adapter recomputes original client material inside the serving boundary and requires full equality.

Baseline observations retain the exact 44 PASS / 11 FAIL reproduction and 271 PASS original result. Repaired observations are separate. Rerunning overwrites current repaired observations but never changes frozen tests. This is implementer execution evidence, not a distinct E05R independent adjudication or OC05 adoption.
