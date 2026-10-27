# SYN02 F0-R2 — source custody, provider selection and portability repair

**Branch:** `agent/sorok-syn02-f0-r2-source-custody-repair-r1`
**Exact source startup:** `9903a30d8d9cd4594f58c46bec80e538610a1851`
**Parent:** `c821b488b3a9a3f0fa01b1981989cc17af637dc1`
**Original F0 attempted branch:** `agent/sorok-syn02-f0-portable-sourcefree-build-r1` remains at `c821b488...` (unadopted; historical deviation unresolved).
**Role:** independent sourcefree engineering repair author; not source owner, HQ, original CAN/ADP/SCI05 issuer, production editor, RF0 reviewer or self-reviewer.
**Test grade:** `SOURCEFREE_TEST_ONLY`; no paid product/provider call, native C8/C9/C12/C11/A5, survey data or production change.
**Owner scope:** recorded in `01_OWNER_SCOPE.md`; user approved the enumerated R2 source scope prospectively. This does not retroactively approve the old F0 branch/extra-file delivery or merge it.

## 0. Outcome

`F0_R2_IMPLEMENTED_SCOPED_SOURCEFREE__PENDING_INDEPENDENT_REVIEW`.

The implementation now:
- requires explicit user-selected CLI, provider, model, variant and account; removes `shutil.which("opencode")` and fixed provider/model/variant defaults; validates provider/model coherence and fails typed before directory creation or subprocess;
- verifies a versioned, 31-file bounded source manifest before importing S49/S51/G18/R30A, with root containment, symlink/traversal refusal, conflicting-env refusal, declared owner/role/scope/effective-time provenance, full G18/R30A package hashes and import-cache checks;
- preserves the corrected S52 cold-open verifier and adds base-ok/rehashed, moved-fork, parent-exception, double-failure/cleanup and non-mutation tests;
- fixes the RF0 alternate-CWD failure; the original 58-test suite passes from both the repository root and `/tmp`.

No native or scientific authority is claimed. A distinct hostile code reviewer must still inspect and accept the R2 branch before integration.

## 1. Changed files

Source:

- `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48/product.py`
- `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py`
- `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/source_binding.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/bootstrap.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py`

Preexisting F0 tests adjusted only for the new explicit selection/cwd behavior:

- `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests/test_f0_product_portability.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests/test_f0_source_portability.py`

New R2-owned artifacts:

- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/build_source_manifest.py`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests/conftest.py`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests/test_provider_selection_r2.py`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests/test_source_custody_r2.py`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/tests/test_cold_open_r2.py`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/00_RETURN.md`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/01_OWNER_SCOPE.md`
- `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/02_TEST_RECEIPTS.md`

Not changed: `s52/session.py` (the F0 cold-open fix was preserved), S48/S51/S52 evidence scripts, S48 `bootstrap.py`, C9/C12, CAN/ADP/Pyat/SCI05, original V3/G18 data, production and the original commissioned branch.

## 2. Implementation

### 2.1 Explicit S48 product selection

`s48/product.py` now has a `ProductSelection` value and requires:

```text
S48_PRODUCT_CLI       absolute executable path
S48_PRODUCT_PROVIDER  nonempty provider token without "/"
S48_PRODUCT_MODEL     must be "<provider>/<model>"
S48_PRODUCT_VARIANT   explicit variant
S48_PRODUCT_ACCOUNT   explicit account/context alias
```

`select_product()` validates all fields before `work.mkdir()`/`log_dir.mkdir()` or `subprocess.run`. There is no PATH lookup and no fallback model/variant/provider. `product_config()` derives `enabled_providers` as exactly `[selected.provider]`; the receipt contains an account hash, not the raw account. The one-call dispatch/SCI05_HOLD/one-prospect behavior is unchanged.

### 2.2 Bounded source custody and verification order

`s51/source_binding.py` now loads the versioned registry:

```text
WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json
```

The bounded nonstdlib closure is 31 files:

- S48 `s48/*.py` (6)
- S49 `s49/*.py` (5)
- S51 `s51/*.py` (4)
- S52 `s52/*.py` (5)
- accepted G18 `lab_sgi1/*.py` (5: `__init__.py`, `core.py`, `proposal.py`, `joint.py`, `history.py`)
- accepted R30A `r30a/*.py` (6)

The manifest also declares exact root provenance (`owner`, `role`, `scope`, `origin`, `effective_from`) for the F0 repo tree, G18 and R30A. Root paths are resolved at runtime; only allowed canonical roots are accepted. Standard library, site-packages and prior accepted S36/S37/M35/language/JOIN-E roots are explicitly outside this bounded closure; those remain a separate pre-existing seam and are not newly certified here.

`verify_sources()` rejects missing/changed/unlisted files, root symlinks, file/directory symlink components, traversal/absolute relative paths, roots outside the allowed set, changed provenance, and duplicate conflicting G18 environment roots. It checks loaded managed modules: a module from a foreign root or an unlisted module fails before further imports. The pre-existing `sys.path` insertion remains only import resolution; it is not the custody proof.

Ordering:

- `s52/bootstrap.py` loads `.source_registry` (stdlib-only + standalone S51 binding), verifies the manifest, then inserts paths and calls `s51_install()`;
- `s51/bootstrap.py` verifies the manifest before importing S49/G18;
- `s52/source_registry.py` does not import the S51 package before verification.

The necessary S51/S52 entry modules are trust-entry code; S49, G18, R30A and their submodules are not imported before the manifest check. The corrected `s52/session.py` cold-open refusal is unchanged.

### 2.3 Cold open and cwd

The old `_OPENING`/`ok=True` override remains removed. New R2 tests explicitly prove:

- base S51 verification is `ok=True` while the malformed S52 candidate is refused;
- moved cold-fork root is refused and the original root remains clean;
- unexpected parent `SessionRefusal` is not masked;
- false verify and a verify exception both close the session;
- verification does not mutate the world and reports `native=False`.

`tests/test_f0_source_portability.py` now anchors its source reads in `REPO`, eliminating the RF0 `/tmp` 17/18 failure.

## 3. Test results

Root and alternate-CWD baseline (same four suites):

```text
S52 18 passed    S48 14 passed    S51 13 passed    S49 13 passed
TOTAL 58 passed from repository root
TOTAL 58 passed from /tmp
```

R2 adversarial suite:

```text
21 passed from repository root
21 passed from /tmp
```

The R2 suite covers PATH/CLI fallback, missing/wrong provider/model/account, relative/non-executable CLI, no subprocess before selection, full G18/R30A coverage, root symlink, file symlink, traversal/absolute paths, conflicting env roots, changed G18 `__init__`/`core`, wrong manifest role/owner metadata, poison preloaded G18, verification-before-S49-import ordering, base-ok cold refusal, moved cold fork, parent exception, double failure/close, and verify non-mutation.

No real CLI/provider was invoked. Exact commands, counts and logs are in `02_TEST_RECEIPTS.md`.

## 4. F0-R2 requirement mapping

| Requirement | Result |
|---|---|
| Remove PATH/opencode and model/provider/variant defaults; explicit user selection; fail before dirs/subprocess | **DONE** |
| SourceRef manifest with all F0-managed imported modules, G18 package, R30A, owner/role/effective time | **DONE for bounded F0 closure** |
| Allowed-root containment, symlink/traversal, conflicting env | **DONE** |
| Verify before S49/S51/G18/R30A import | **DONE** (entry modules are trust-entry) |
| Prevent stale cache/root switch bypass | **DONE** (foreign/unlisted managed modules refused) |
| Preserve S52 cold open; parent/fork/rehashed/cleanup/no-mutation | **DONE / sourcefree** |
| 58 tests from root and `/tmp` | **DONE (58/58 both)** |
| Evidence/source manifest and changed-file receipts under R2-owned directory | **DONE**; S48/S51 evidence scripts intentionally unchanged |
| Historical F0 branch/extra-file custody | **UNRESOLVED / no retroactive approval** |
| Native C11/C12, CAN/ADP/SCI05, actor/science, provider account | **HELD / NOT_RUN** |

## 5. Residual limitations

1. The manifest is a declared sourcefree trust root, not a cryptographically signed owner grant. Its provenance metadata is checked for exact declared values, but it does not confer source/native authority.
2. The bounded closure excludes prior S36/S37/M35/language/JOIN-E dependency roots installed by the existing S37 bootstrap. Those are outside the R2 write scope and are not newly certified.
3. The S48/S51 evidence scripts still contain historical `/Users/` paths; no evidence-script edit was included because the commission required exact necessity and an owner-approved exception. `run_s52_evidence.py` was not changed or executed.
4. The old F0 alternate branch and its historical extra files remain an unresolved branch/extra-file custody matter. This branch starts from the unadopted 9903 source as directed; it does not adopt that return or the original commissioned branch.
5. No scientific, native C11/C12, actor, provider-account or production acceptance follows. A distinct independent hostile reviewer is required.

## 6. Three courts

**ENGINEERING — `ACCEPT_SCOPED_SOURCEFREE` for the implemented R2 repair, pending independent review.** Provider fallback, verification order, root/cache hostility and cwd portability are repaired and tested. Residual bounded-closure/evidence-script limitations remain explicit.

**SCIENCE — `NO_CHANGE`.** No psychological, developmental, care, memory, Rule A/T, SCI05 or actor semantics were changed or tested.

**AUTHORITY — `HOLD / NO_NATIVE_GRANT`.** No C8/C9/C11/C12, CAN/ADP/Pyat, source, human, provider-account or production authority is issued. Historical F0 branch/extra-file custody remains subject to owner/HQ disposition. F1.1 still requires independently reviewed RP0 and competent C9/C12 storage-owner approval.

## 7. Handoff

The F0-R2 sourcefree repair is ready for a distinct hostile reviewer. The reviewer should inspect the exact source manifest, the five source edits, the two adjusted F0 tests and the R2 test suite; rerun root/`/tmp` 58 + 21; verify the remote SHA; and reject any unverified provider call, unbounded source claim or historical branch adoption.

**Final remote SHA:** verified after commit/push and reported in the delivery handoff; not embedded here because self-embedding changes the commit. No self-adoption.
