# SYN02-RF0-R2 — evidence, replay, and probe record

**Reviewer:** RF0-R2 code reviewer; not the R2 author, Sorok/Pyat HQ, native source/science issuer, production editor, or self-reviewer.
**Immutable subject:** `60797302652e7d7877443f6e9d0becde5afb8382`.
**Subject parent:** `9903a30d8d9cd4594f58c46bec80e538610a1851`; source-startup parent: `c821b488b3a9a3f0fa01b1981989cc17af637dc1`.
**Review branch/startup:** `agent/sorok-syn02-review-rf0-r2-code-r1` at `a7a6c781e158cd1317c0ecd0d6e1e542a4fd633d`.
**Host:** Darwin 22.6.0 x86_64; Python 3.11.3; pytest 9.1.1.
**Execution grade:** `SOURCEFREE_TEST_ONLY`; no paid CLI/provider invocation, no native C8/C9/C11/C12/A5, no raw survey/source execution, no production edit, no author-branch edit.
**Review writes:** only the three RF0-R2 review documents in this directory.

## A. Custody, branch, and changed-file identity

### A.1 Remote refs

`git ls-remote origin` returned:

```text
c821b488b3a9a3f0fa01b1981989cc17af637dc1  refs/heads/agent/sorok-syn02-f0-portable-sourcefree-build-r1
60797302652e7d7877443f6e9d0becde5afb8382  refs/heads/agent/sorok-syn02-f0-r2-source-custody-repair-r1
9903a30d8d9cd4594f58c46bec80e538610a1851  refs/heads/agent/sorok-syn02-f0-source-portability-r1
```

The original F0 branch is still at the seal and is not the R2 branch. The R2 subject is one commit ahead of the unadopted `9903` alternate; `9903` is one commit ahead of `c821`. The R2 return's “Exact source startup” is `9903` and its “Parent” is `c821` (the parent of that startup), not the R2 commit's immediate parent. The reviewer treats the R2 commit's parent as `9903` and does not adopt either historical branch.

### A.2 Changed set

`git diff --name-status 9903a30d... 607973...`:

```text
M  WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48/product.py
M  WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests/test_f0_product_portability.py
M  WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py
M  WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/source_binding.py
M  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/bootstrap.py
M  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py
M  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests/test_f0_source_portability.py
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/00_RETURN.md
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/01_OWNER_SCOPE.md
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/02_TEST_RECEIPTS.md
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/build_source_manifest.py
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests/conftest.py
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests/test_cold_open_r2.py
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests/test_provider_selection_r2.py
A  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests/test_source_custody_r2.py
```

`git diff --stat 9903... 607973...`: **16 files changed, 1,639 insertions(+), 126 deletions(-)**. No `s52/session.py` change, no evidence-script change, no S48 `__init__.py` or `bootstrap.py` change.

### A.3 Independent file hashes

The following SHA-256 values were computed by the reviewer from the immutable target tree. They match the R2-owned receipt hashes where stated, but the receipt claim remains `WORKER_REPORTED`; the values below are `EXECUTED` file reads.

```text
d95fe621314b86615b5a83dee3655f2fb40a35543ed61ec7da56c2667bfe4b75  R2/00_RETURN.md
d5b95eca0eac96d9b9e40109f16f2e90d33994d3a62472e2ac0cb0ffb4357d84  R2/01_OWNER_SCOPE.md
5cb9db65071c5495d3257f47793acfbbf3993fd66bd4311ec8c6e35d1730b294  R2/02_TEST_RECEIPTS.md
8bae025cd2cabedeba239a77cc940781fb85b984f4b10eeee0239895c3a82efa  R2/build_source_manifest.py
7120d3077a6687957c02d0eba880a11329a4a4fcc29ad9fe17ef92a92600b84d  R2/source_manifest.json
4359dc1a62021886c02007bc257ac01ce9e65b25dfb4151f7540f0719ef33c02  R2/tests/conftest.py
26522e2f28cad9678e7577572cf62c85e7b0bdb56b82bc3dc603b3d90824e11e  R2/tests/test_cold_open_r2.py
5f06c3adaad3a338dc021732b21215ef9ce6a254989197c62074637fb4ec21cc  R2/tests/test_provider_selection_r2.py
73cc40ef2702adee612dc2c2b1e9f781b0c352ed4b5568d249c9b0fe7672a56d  R2/tests/test_source_custody_r2.py
29fe4f70e9f3190e0f989ab9d3075b9a1d10138cf250b45964d712c234cf6d1d  S48/s48/product.py
d879438b48c7c31d78fa5b914ffd01702ec6a0b91918693c677344009c297244  S48/tests/test_f0_product_portability.py
b180c81c145fd2d16b13b4067058a02681e6007689ee4573e87a3a7af81d6531  S51/s51/bootstrap.py
a5ecf0c60efd6aaa9dee279b4176cd72789b4573d4939186d361be3e4d6997cb  S51/s51/source_binding.py
e6461605dc96fbb8957da8eaec1d769b699d3fab58f0596c88152b6cf29b3373  S52/s52/bootstrap.py
8881d97b83ef8bfd59c2cb9796881f58e39066a479a6d90a8158218a0692863d  S52/s52/source_registry.py
f75b0c70b4844537b4ae2b0613820b855fe30c6886ce65781e299024750060f6  S52/tests/test_f0_source_portability.py
```

## B. Manifest and source-closure audit

### B.1 Counts

`source_manifest.json` has schema `SOROK_F0_R2_SOURCE_MANIFEST@1` and **31** sources:

| Root | Count | Contents |
|---|---:|---|
| `repo` | 20 | S48 `s48/*.py` 6; S49 `s49/*.py` 5; S51 `s51/*.py` 4; S52 `s52/*.py` 5 |
| `g18` | 5 | `lab_sgi1/{__init__.py,core.py,proposal.py,joint.py,history.py}` |
| `r30a` | 6 | `r30a/{__init__.py,bootstrap.py,cli.py,faults.py,first_session.py,phenomenal.py}` |

The manifest records exact `owner`, `role`, `scope`, `origin`, and `effective_from` values for `repo`, `g18`, and `r30a`. `verification` checks those exact values; this is provenance metadata, not a signed owner grant.

### B.2 Listed-source verification

The reviewer independently rehashed the listed source files and the manifest’s digest values matched. The normal `verify_sources()` result was `verified: 31`. The tests cover normal G18 resolution, a changed `lab_sgi1/__init__.py`, changed `core.py`, a symlinked G18 file/root, traversal/absolute paths, a conflicting G18 environment, wrong provenance, and a poison-preloaded `lab_sgi1` module.

The builder (`build_source_manifest.py:47-57`) builds repo entries from four package directories, G18 from `lab_sgi1`, and R30A only from `r30a/*.py`. It does not include `r30a/vendor/r29p`, `r30a/vendor/r29p/candidate/stable_actor_binding.py`, or S39.

### B.3 Manifest limitations confirmed

| Limitation | Reviewer result |
|---|---|
| Excludes S36/S37/M35/language/JOIN-E | Declared in `00_RETURN.md` residual 5.2; actual S52 imports `candidate` (S36), `s37` test support, and JOIN-E/vendor modules. |
| Excludes signed provenance | No signature; exact metadata only. |
| Includes complete R30A package | **No.** Only six `r30a/r30a/*.py`; `r30a/first_session.py:24-37` imports `r29p`/`bp1`/`bp4`; `r30a/vendor/r29p/r29p/runner.py:11` imports `stable_actor_binding`. |
| Includes actual S52 import closure | **No.** `s52/session.py:11` imports `s39.sources`; the module audit found unlisted S39 and vendor modules. |
| Cannot claim full current dependency custody/native grant | Correct; the reviewer does not upgrade the bounded claim. |

## C. Test replay

### C.1 Environment and commands

Review logs are under `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rf0-r2-logs`; the target checkout is `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rf0-r2-target-wt` (`W` below). `TMPDIR` was outside the checkout. The relevant source-root variables were unset before replay:

```text
S52_G18_SOURCE S51_G18_SOURCE G18_SOURCE M35_G18_SOURCE
S52_ALLOWED_ROOTS S52_R30A_SOURCE S37_JOIN_E_RETURN S52_JOIN_E_SOURCE
```

Root replay:

```text
cd "$W"
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/tests
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/tests
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests
```

Alternate-cwd replay used `cd /tmp` and absolute paths to the same test directories. No repository file or provider was written.

### C.2 Results

| Suite | Root | `/tmp` | Reviewer grade |
|---|---:|---:|---|
| S52 F0 regression | 18 passed | 18 passed | `EXECUTED` |
| S48 F0 regression | 14 passed | 14 passed | `EXECUTED` |
| S51 F0 regression | 13 passed | 13 passed | `EXECUTED` |
| S49 F0 regression | 13 passed | 13 passed | `EXECUTED` |
| **Base total** | **58 passed** | **58 passed** | `EXECUTED` |
| R2 adversarial | 21 passed | 21 passed | `EXECUTED` |

Root log names and observed times: `root_S52...log` 18 passed 55.65s; `root_S48...log` 14 passed 8.50s; `root_S51...log` 13 passed 21.38s; `root_S49...log` 13 passed 19.63s; `root_r2.log` 21 passed 13.50s. Alternate-cwd logs: S52 18/54.52s, S48 14/8.50s, S51 13/20.63s, S49 13/20.49s, R2 21/14.74s.

The worker return reports the same 58 + 21 counts. The reviewer does not treat worker-reported timing or counts as evidence; the reviewer logs above are the evidence.

### C.3 Tests not run

- `run_s52_evidence.py`: **NOT_RUN**; it writes `evidence/`, `junit/`, and `logs/` into the author tree and the target says it was not changed or executed. Static inspection only.
- `run_s48_evidence.py`, `run_s51_evidence.py`: **NOT_RUN**; static inspection found remaining host paths.
- Real `run_product_cli` with a real CLI/provider/account: **NOT_RUN**; no paid call, no entitlement inference.
- Native C8/C9/C11/C12/A5, raw survey/source execution, production merge: **NOT_RUN**.

## D. Hostile probes

All probes are reviewer-owned, sourcefree, outside the target repository, and used temporary directories. They did not call a provider or modify the author branch.

### D.1 Preloaded fake `s51.source_binding`

`probe_fake_binding.py` installed a `types.ModuleType("s51.source_binding")` with no `__file__` and fake `source_roots`/`verify_sources`; then called `s52.source_registry.verify_dependencies()`:

```text
VERIFY_RETURN True
CALLS ['source_roots', 'verify_sources']
FAKE_FILE None
```

This directly contradicts `00_RETURN.md` requirement mapping “Prevent stale cache/root switch bypass — DONE” and `s51/source_binding.py:8-9` (“A preloaded managed module ... fails closed”).

### D.2 No-`__file__` managed cache

`probe_no_file_cache.py` loaded the real resolver, injected a no-`__file__` `s52` module, and called `verify_sources(check_cache=True)`:

```text
CACHE_RESULT 31
```

`_check_import_cache` at `s51/source_binding.py:368-374` skips `filename`-less modules, so the claimed cache contamination check is not complete.

### D.3 Empty manifest

`probe_empty_manifest.py` used the actual resolver and a provenance-valid manifest with `sources: []`:

```text
EMPTY_RESULT {'schema': 'SOROK_F0_R2_SOURCE_VERIFICATION@1',
 'manifest': '.../empty.json', 'verified': 0, ...}
```

No minimum count or required-path check rejected it.

### D.4 Module closure

`probe_module_closure3.py` imported `s52.session` through the target tree and compared `sys.modules` paths with the manifest. Representative unlisted modules:

```text
UNLISTED stable_actor_binding r30a vendor/r29p/candidate/stable_actor_binding.py
UNLISTED s39 repo WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/s39/__init__.py
UNLISTED s39.sources repo .../s39/sources.py
UNLISTED candidate repo WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1/candidate/__init__.py
UNLISTED s37 repo WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1/s37/__init__.py
UNLISTED bp1 /Users/.../rawlsing-r31j/.../candidate/vendor/bp2/vendor/bp1/bp1/__init__.py
UNLISTED bp2p4 /Users/.../rawlsing-join-e/.../vendor/j/candidate/bp2p4/__init__.py
UNLISTED bp4 /Users/.../rawlsing-join-e/.../vendor/j/candidate/vendor/bp4/bp4/__init__.py
```

The S36/S37/vendor roots are declared exclusions; `s39.sources` is not named in the return's residual list, and `stable_actor_binding` is inside the R30A vendor tree that the return calls part of the “full R30A package.” The target's `test_manifest_covers_all_g18_package_files` covers G18 only.

### D.5 Account and receipt

`probe_account_receipt.py` used a fake executable that recorded argv and config, then emitted one `step_start`, one valid text envelope, and one `step_finish`. Result:

```text
STATUS OK
ACCOUNT_HASH d4ce5b2a0021cfd31c0b43609066b0ca0fa39e650a5ff7ba6e613ecb22df640d
ACTUAL_PROVIDER_CALL True
ARGS ['run', '--model', 'provider-x/model-y', '--variant', 'variant-z', '--format', 'json',
      '--pure', '--dir', '.../work', '--title', 'S48_PRODUCT_TURN', 'hello']
CONFIG {'model': 'provider-x/model-y', 'small_model': 'provider-x/model-y',
        'enabled_providers': ['provider-x'], 'autoupdate': False, 'permission': {...}}
ACCOUNT_IN_ARGS False
ACCOUNT_IN_CONFIG False
```

The account is a selected/hashed alias, not a transport binding; `actual_provider_call` is fixed `True` at `s48/product.py:326` even for the fake executable. This is sourcefree evidence only; no real provider call or entitlement was tested.

### D.6 External `log_dir`

`probe_external_log.py` used a fake CLI and `log_dir` outside the patched `RETURN`:

```text
ERROR ValueError '.../external-logs/product_2cf24dba5fb0a30e.stdout.jsonl'
is not in the subpath of '.../return' OR one path is relative and the other is absolute.
LOG_FILES ['external-logs/product_2cf24dba5fb0a30e.stderr.log',
           'external-logs/product_2cf24dba5fb0a30e.stdout.jsonl']
```

The subprocess completed and both files were written before the exception. The failing code is `s48/product.py:340-341`; the public `S48Session` exposes `product_log_dir` at `s48/session.py:209,254-272`.

### D.7 Evidence-script paths

Static inspection found `run_s48_evidence.py:23` and `run_s51_evidence.py` host-specific `/Users/matthewsmith/...` paths. `run_s52_evidence.py` was not executed and has no executed receipt in this review. These are declared residuals, not a pass for general portability.

## E. Evidence-grade summary

| Evidence | Grade |
|---|---|
| 58 base + 21 R2 tests, root and `/tmp` | `EXECUTED` by reviewer |
| 16 changed-file identity and hashes | `EXECUTED` |
| 31 listed manifest entries and normal verification | `EXECUTED` |
| Preloaded fake binding, no-`__file__` cache, empty manifest, module closure, fake account, external log | `EXECUTED` by reviewer |
| Worker root/`/tmp` receipts and timings in `02_TEST_RECEIPTS.md` | `WORKER_REPORTED`; independently matched counts |
| `run_s52_evidence.py`, S48/S51 evidence scripts, real provider/account, native C12/A5 | `NOT_RUN` |
| C12 fork perception-loss | `INHERITED` from RP0-R2/owner docket; not repaired here |
