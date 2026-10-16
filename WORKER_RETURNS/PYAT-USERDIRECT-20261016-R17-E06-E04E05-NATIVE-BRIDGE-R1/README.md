# Reproduce E06 candidate

Start with `00_RETURN.md`. All commands below run from this commissioned return inside the private shared repository's returned branch:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 repro/stage_sources.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/execute_products.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/run_tests.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/build_report.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/verify_return.py
```

Staging reads and verifies exact Git objects into ignored `runtime/`. It refuses to overwrite changed source bytes. It does not fetch original sources or alter accepted owners. The preserved 401-object E05S closure is unchanged; E04T is an extra separately imported owner module, not a shadow replacement of `product.empirical`. Source manifests make the entire physical closure reproducible from exact private Git objects.

The public Python API is `NativeBridge(rows, enabled=True, **fixture_options)`, `prepare(request_binding)`, `read(prepared, scalar_only=False)` and `archive(output)`. `execute` composes prepare/read. Without literal enabled=True, construction refuses before producing native source evidence. Original E05R acceptance and serving remain explicit. Reverse queries use their own scalar request, because the two original clients have a narrower forward readset. Passing supplied consumer material is only a checked transport surface; E05R authenticates it against actual original client reexecution.

`02_ACTUAL_NATIVE_TO_TWO_CONSUMER_PRODUCTS.json` carries actual values and binds the separate exact raw native trace by SHA256. The observer only reads actual Python call/return frames; it never wraps owners. Native module `__file__` aliases, exact Git preimages and original callee lines are retained. Four cold-process outputs and terminals, two comparisons, current fixture grant ledgers, final and initial JUnit/stdout/exits are under `observations/`.

The independent numerical/source contract is immutable at the first E06 freeze commit and precedes bridge implementation/owner execution. New author checks use that contract and actual C11 events; this is not the distinct independent E06 acceptance court. Original 494/403 accepted suites are referenced at their exact pins, not relabeled as fresh bridge tests. Full reruns were unnecessary; new joint-boundary cases directly exercise the materially changed constructor and authority path.

All products are synthetic sourcefree evidence. No actual N9/OC05 installation, original source issue, new grant principal, EE13/EE14, N11/N12 or actor/V3 action occurs. The final publication receipt binds a directly verified evidence commit; final containing SHA is reported separately after remote readback to avoid recursive self-hashing.
