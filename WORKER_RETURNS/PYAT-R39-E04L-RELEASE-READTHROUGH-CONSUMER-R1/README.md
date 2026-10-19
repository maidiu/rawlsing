# E04L sourcefree read-through reproduction

Start with `00_RETURN.md` and the frozen `evidence/preregistration.json`. No production install is required or authorized.

Using Python 3.11 and pytest 9.1.1 from an authorized environment, run at the repository root:

```sh
python -B WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1/rehydrate_original.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 python -B WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1/run_evidence.py
PYTHONDONTWRITEBYTECODE=1 python -B WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1/capture_native.py
```

The original seven-case test is staged locally under ignored `.runtime/` from its exact Git pin. Retained E03/E04 sources under `vendor/` are exact byte preimages, not modified owner code. The new integration test has two exact code-fault witnesses in its sibling `.proof.json`. Witness faults must remain RED by the named assertions; restoring the implementation must return green.

The PRE-MAIN gate can also be run with `changed --base 2e6c189fd54b818556a44419b19691938ea76d5a --head <committed-return-sha> --root .`. It checks the changed test and executes the witnesses. No other original historical tests are retroactively claimed qualified by that gate.
