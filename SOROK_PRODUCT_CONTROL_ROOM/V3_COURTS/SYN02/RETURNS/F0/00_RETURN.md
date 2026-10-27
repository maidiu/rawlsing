# SYN02 F0 — source portability, dependency verification and S52 cold-open repair

**Source-code startup:** `c821b488b3a9a3f0fa01b1981989cc17af637dc1`.
**Branch:** `agent/sorok-syn02-f0-source-portability-r1`.
**Role:** actual source-free engineering implementation on the accepted S48/S52 source; not national/scientific issuer, production editor or self-reviewer.
**Test grade:** TEST_ONLY sourcefree; no provider call, native C8/C9/C12, C11 weld, survey data, production deployment or A5.

## 0. Outcome

`F0_IMPLEMENTED_SCOPED`: S51/S52 no longer embed a user-specific G18 path; S52 verifies the exact accepted S49/S51/G18 files before installation; S48 product transport is injected/portable and fails typed when no CLI is available; malformed S52 cold-open sessions are refused instead of returning `ok=True`.

No native or psychological authority is claimed.

## 1. Changed files

Source:

- `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/source_binding.py` (new)
- `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py` (new)
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/bootstrap.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/session.py`
- `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48/product.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/run_s52_evidence.py`

Tests:

- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests/test_f0_source_portability.py` (new)
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests/test_s52.py` (cold-open regression updated)
- `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests/test_f0_product_portability.py` (new)

No central atlas, PRE-MAIN, CAN/ADP/Pyat, current C9/C12 production, original V3 or other author branch was modified.

## 2. Source portability

### 2.1 S51/S52 G18 resolution

`S51` previously imported G18 from:

`/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/.../candidate/vendor/bp2/vendor/g18`

`S52` repeated the same absolute path. Both hardcodes are removed.

`s51/source_binding.py` now resolves the G18 checkout in this order:

1. explicit `S52_G18_SOURCE`, `S51_G18_SOURCE`, `G18_SOURCE` or `M35_G18_SOURCE`;
2. a `rawlsing-r31j/.../g18` path discovered from the Git common worktree root;
3. the same relative path under the repository/worktree roots.

An explicit environment path that is absent or points to the wrong source fails closed with `G18_SOURCE_ENV_INVALID`; no silent fallback. If no source is found, the error is `G18_SOURCE_UNRESOLVED` with the required environment variable named.

`S51Session` still receives the same G18 source and `lab_sgi1` imports; the change is path/identity resolution, not psychology or behaviour.

### 2.2 S48 product CLI/model

`s48/product.py` previously embedded:

`/Users/matthewsmith/.opencode/bin/opencode`

and fixed model/variant values. It now uses:

- `S48_PRODUCT_CLI` if set;
- otherwise `shutil.which("opencode")`;
- otherwise an empty value, causing a typed `ProductCallError("S48_PRODUCT_CLI_MISSING")` before any subprocess or filesystem work.

`S48_PRODUCT_MODEL` and `S48_PRODUCT_VARIANT` are also environment-injectable, with the prior model/variant as defaults. No paid/provider call is made by this return.

### 2.3 Evidence helper

`run_s52_evidence.py` no longer resolves seam files from
`/Users/matthewsmith/.codex/...`; it derives them from the repository root and
uses the portable `roots()` binding. The S52 source manifest includes
`s52/source_registry.py`.

## 3. Dependency verification

`S52` now verifies the exact accepted dependency files before importing/running:
- `S49/s49/actor.py`: `c2a889c825807c174cdc91ce4ec08cde07c2e6e0575fadf9ee97185324c5eb95`
- `S49/s49/session.py`: `9932029c529a399ffedb24545ea5d0f6884a5fe8719ffc39c8af9fe1db0f3625`
- `S51/s51/session.py`: `6ef8e92eb3ea2d83cfdb5aba1121ed42f1706a0df9bc3f36aff2b91a47596a82`
- `G18/lab_sgi1/joint.py`: `755820d7d703cd459aec8271a784c39a69e9374aae501da1cd9f37bbccc21ee9`
- `G18/lab_sgi1/history.py`: `2d861d7a820168d443e23efb2403b7ed9c3e899a8a79aaa72fd859c46f47c1c1`

`verify_dependencies(roots())` raises `SourceBindingError` on a missing file, a wrong root, or a hash mismatch. `roots()` reports `dependency_verified: true` and `g18_source_verified: true` only after the hashes pass. A changed source cannot silently execute.

The expected files are the accepted source identities; this is dependency integrity, not a native source grant.

## 4. S52 cold-open repair

`S52Session` previously had `_OPENING` and forced `verify()["ok"] = True` on a cold open when the base session was OK, even while S52 errors remained.

Removed:
- `_OPENING`;
- the `ok=True` override.

Added:
- `S52ColdOpenRefusal` (`S52_COLD_OPEN_INVALID`);
- `S52Session.open` now catches a base `S37_VERIFY_FAILED` and raises the typed S52 refusal, and also verifies the returned session before returning it;
- malformed cold history closes the session and raises, rather than exposing a session that can be mistaken for clean.

Clean cold reopen still verifies and returns normally.

## 5. Tests actually executed

Commands were local sourcefree, with `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` outside the repo and pytest cache disabled.

```text
S52 tests: 18 passed in 56.27s
S48 tests: 14 passed in 9.27s
S51 tests: 13 passed in 21.66s
S49 tests: 13 passed in 20.14s
TOTAL: 58 passed, 0 failed
```

New F0 adversarial/regression coverage:

- source binding resolves the accepted G18 without embedded `/Users/` paths;
- tampered `lab_sgi1/joint.py` is rejected by SHA-256;
- substituted G18 root is rejected;
- clean cold open remains valid;
- rehashed S52 candidate on cold open raises `S52_COLD_OPEN_INVALID` rather than returning a misleading session;
- S48 missing CLI raises typed `S48_PRODUCT_CLI_MISSING` before mkdir/subprocess;
- S48 source no longer contains a fixed `/Users/` CLI path.

**NOT_RUN:** provider/CLI invocation; native C8/C9/C12, C11/Pyat weld, A5 human, raw survey/source data, full original V3 suite. No positive native claim.

## 6. Source identities after change

| File | SHA-256 |
|---|---|
| `S48/s48/product.py` | `e8d66c5ce76221f6debb68f5a4e0bb712c707defda70ebf67a431218ce69298f` |
| `S48/tests/test_f0_product_portability.py` | `16c498f4b6919acc2888717b6515bf65cd4ad0373d2ea3d9946490bf882beeb5` |
| `S51/s51/bootstrap.py` | `5e519b28d9e32946d9e1a2ffd908805d124ddada94979f2d9dad486c0a18a313` |
| `S51/s51/source_binding.py` | `ebe2164230b33fdb852936da4a49fbfc2c0e8b57874e8f9c9366b57f99eb0314` |
| `S52/s52/bootstrap.py` | `68aa762683200a6494c612c738b2efed56f5cec78ae21d5642266a1ef7dcc0cc` |
| `S52/s52/session.py` | `2aa2737bea395cdc78c19dfca791b9107cd54ea600f0e19f1243df9ebce5cebe` |
| `S52/s52/source_registry.py` | `f292ec98fda1d025674700c025813491e29769042441f0836add92c557217cc3` |
| `S52/tests/test_f0_source_portability.py` | `6190fabbc315cdea1dcb5e884b126796bd20f2c2a09e2f16f51a8ff70eb012b7` |
| `S52/tests/test_s52.py` | `87580ffac8fcc9e930fb381e67c3c7d73cf625327c88260892522b4fd4c2f904` |
| `S52/run_s52_evidence.py` | `196c3e0727e6fdb1b8f946f87df640349ba24cdfe861e4b62dedea566fbab76e` |

## 7. Three courts

**ENGINEERING — `ACCEPT_SCOPED`.** Portability, hash verification, typed missing-CLI failure and cold-open fail-closed behavior are implemented and exercised. The changes are additive/scoped; no production edit.

**SCIENCE — `NO_CHANGE`.** No psychological, developmental, care, memory or typology claim is made or tested. This is source/session engineering only.

**AUTHORITY — `NO_NATIVE_GRANT`.** No C8/C9/C11/C12, CAN/ADP/Pyat, source, human or production authority is issued. The accepted G18 hashes are dependency identities, not actor/source permissions.

## 8. FINDING → INTERPRETATION → ACTION → OWNER

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| S52/S51 embedded absolute G18 path | Multi-host runs could silently use a stale source | Portable resolver with explicit env + Git common-root discovery; fail closed | S51/S52 engineering |
| S49/S51/G18 could drift | A replaced source could pass by name | Exact SHA-256 dependency verification before install | S52 engineering |
| S48 embedded user CLI path | Non-portable and untyped failure | Env/PATH injection and `S48_PRODUCT_CLI_MISSING` | S48 engineering |
| S52 cold open forced `ok=True` | Malformed cold history could be accepted | Remove `_OPENING`; `S52ColdOpenRefusal`; clean cold still passes | S52 engineering |
| Source paths in S52 evidence helper | Evidence was non-portable | Derive from repo/roots, include source registry | S52 evidence |

## 9. Handoff

The F0 implementation is ready for independent review at the exact branch commit. It is not a C9/C12 positive and does not alter the SYN02 architecture claims.

**Final remote SHA:** verified after commit/push and reported in the handoff; not embedded here because embedding it would change the commit. No self-adoption.
