# E04S independent court

Use Python 3.11, pytest, and private `maidiu/rawlsing` exact-object access. Run from this return directory:

```
python3 repro/import_evidence.py
python3 repro/stage.py
python3 repro/run.py baseline51
python3 repro/run_inherited.py
python3 repro/run.py new_hostiles
python3 repro/run.py scientific_probe
python3 repro/run.py authority_probe
python3 repro/run.py f1_f2_probe
python3 repro/run.py ceiling_probe
python3 repro/run.py cold first
python3 repro/run.py cold replay
python3 repro/verify.py
```

The baseline51 and new_hostiles commands intentionally exit 1 when they reproduce the recorded REDs. Run commands individually or use orchestration that retains all declared exits rather than stopping at the first expected RED. `stage.py` refuses an existing runtime. The preexecution oracle and digest were committed before the first original/candidate Python execution. `freeze_oracle.py` records how it was authored; do not rewrite the historical freeze during reproduction.

Exact sources come from sealed Git objects. The original E04N selector supplies 94 original source/report/fixture files (including all 51 native dependencies); six E04R product files are staged separately. Ignored `inputs/` and `runtime_root/` are fully reconstructible from the two manifests. `reviewed_candidate/` retains the exact candidate source for review, not a product modification. Five product files remain byte-identical to original E04; `empirical.py` is the sole product repair.

`pytest_entry.py` explicitly selects original E04 only for baseline51, otherwise E04R, and preimports the six exact `product.*` modules. The original author37 test prepends its historical product location; preloading prevents that path operation from silently switching the candidate. No native callable, estimator, evidence object, repository, client, hash function or expected oracle is replaced. `common.py` and all 51 original test bodies are exact E04N bytes. The native231 selection and original author37 file are exact staged originals. `author_hostiles37` reruns the author's exact additional tests; they are labeled inherited implementer tests, separate from the new independent court.

`observer.py` records actual call/return frames and imported file hashes without wrapping owner functions. The dedicated scientific probe independently reconstructs 58 respondents and 232 native C11 events and checks the same concrete C1 evidence objects entering F8. Normal attempted mutation of actual retained I03 facts and source carriers is distinguished from a later served result. No arbitrary `object.__setattr__`, private-attestation replacement or monkeypatch attack is used.

A RED new native-authority lifecycle witness is deliberately preserved. New query-registry withdrawal fixtures remove the exact query grant while leaving the request/source/release refs, sealed source object and public projection intact. Cached clients return productive material; after removing cache projections, actual native production returns typed UNAVAILABLE without cells/support. Fresh fixture reconstruction and bit-identical replay do not imply durable real permission renewal.
