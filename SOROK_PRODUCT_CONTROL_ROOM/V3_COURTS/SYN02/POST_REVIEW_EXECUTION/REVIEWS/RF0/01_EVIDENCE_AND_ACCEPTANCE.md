# SYN02-RF0 — evidence, replay, and acceptance record

**Reviewer:** fresh independent RF0; not F0/RP0/RM40/S/S-R author, HQ, production editor, original issuer, or self-reviewer.
**Immutable subject:** `9903a30d8d9cd4594f58c46bec80e538610a1851`.
**Original F0 branch:** `agent/sorok-syn02-f0-portable-sourcefree-build-r1` at `c821b488b3a9a3f0fa01b1981989cc17af637dc1`.
**Review branch/startup:** `agent/sorok-syn02-review-rf0-code-r1` at `4fc21d74d5c585ba6c83b3de2e6ace2d5127b392`.
**Host:** Darwin 22.6.0 x86_64; Python 3.11.3; pytest 9.1.1.
**Execution grade:** sourcefree local Python/pytest; no paid CLI/provider invocation, no native C8/C9/C12/C11/A5, no raw survey, no production edit, no author-branch edit.
**Review writes:** only this file and `00_REVIEW.md`.

## A. Custody, branch, and file identity

### A.1 Branch reality

```text
origin refs/heads/agent/sorok-syn02-f0-portable-sourcefree-build-r1  c821b488b3a9a3f0fa01b1981989cc17af637dc1
origin refs/heads/agent/sorok-syn02-f0-source-portability-r1       9903a30d8d9cd4594f58c46bec80e538610a1851
origin refs/heads/agent/sorok-syn02-review-rf0-code-r1             4fc21d74d5c585ba6c83b3de2e6ace2d5127b392
```

The F0 commit is:

```text
9903a30d8d9cd4594f58c46bec80e538610a1851
parent c821b488b3a9a3f0fa01b1981989cc17af637dc1
author Maidiu <matthewdavidsmith86@gmail.com>
subject F0 portable source binding, dependency hashes and cold-open refusal
```

The commissioned branch remains at the source seal and is not the returned branch. The return is one commit ahead of the same parent on a separately named branch. The intake at `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_REVIEW_EXECUTION/01_THREE_RETURN_EVIDENCE_INTAKE_R1.md:9,11` records this as a material protocol deviation and notes the extra files. No owner authorization for the branch substitution or extra-file scope was found in the reviewed commit/return; this review does not adopt the swap.

### A.2 Exact changed set and hashes

`git diff --name-status c821b488... 9903a30d...`:

```text
A  SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/RETURNS/F0/00_RETURN.md
M  WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48/product.py
A  WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests/test_f0_product_portability.py
M  WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py
A  WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/source_binding.py
M  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/run_s52_evidence.py
M  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/bootstrap.py
M  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/session.py
A  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py
A  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests/test_f0_source_portability.py
M  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests/test_s52.py
```

`git diff --stat c821... 9903...`: **11 files changed, 616 insertions(+), 68 deletions(-)**.

Independently computed SHA-256 (all ten source/test values match `RETURNS/F0/00_RETURN.md`; the return hash is additional):

| Status | Path | SHA-256 |
|---|---|---|
| A | `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/RETURNS/F0/00_RETURN.md` | `ad2a5607be946a2b8f204e1bf5a59969097049a9c17c8da515abe857da600f75` |
| M | `S48/s48/product.py` | `e8d66c5ce76221f6debb68f5a4e0bb712c707defda70ebf67a431218ce69298f` |
| A | `S48/tests/test_f0_product_portability.py` | `16c498f4b6919acc2888717b6515bf65cd4ad0373d2ea3d9946490bf882beeb5` |
| M | `S51/s51/bootstrap.py` | `5e519b28d9e32946d9e1a2ffd908805d124ddada94979f2d9dad486c0a18a313` |
| A | `S51/s51/source_binding.py` | `ebe2164230b33fdb852936da4a49fbfc2c0e8b57874e8f9c9366b57f99eb0314` |
| M | `S52/run_s52_evidence.py` | `196c3e0727e6fdb1b8f946f87df640349ba24cdfe861e4b62dedea566fbab76e` |
| M | `S52/s52/bootstrap.py` | `68aa762683200a6494c612c738b2efed56f5cec78ae21d5642266a1ef7dcc0cc` |
| M | `S52/s52/session.py` | `2aa2737bea395cdc78c19dfca791b9107cd54ea600f0e19f1243df9ebce5cebe` |
| A | `S52/s52/source_registry.py` | `f292ec98fda1d025674700c025813491e29769042441f0836add92c557217cc3` |
| A | `S52/tests/test_f0_source_portability.py` | `6190fabbc315cdea1dcb5e884b126796bd20f2c2a09e2f16f51a8ff70eb012b7` |
| M | `S52/tests/test_s52.py` | `87580ffac8fcc9e930fb381e67c3c7d73cf625327c88260892522b4fd4c2f904` |

The short paths above are under `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/`, `SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/`, and `SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/` respectively. Full paths are in the diff list.

**Source hash correctness:** the five dependency hashes independently read from the accepted files are:

```text
S49/s49/actor.py       c2a889c825807c174cdc91ce4ec08cde07c2e6e0575fadf9ee97185324c5eb95
S49/s49/session.py     9932029c529a399ffedb24545ea5d0f6884a5fe8719ffc39c8af9fe1db0f3625
S51/s51/session.py     6ef8e92eb3ea2d83cfdb5aba1121ed42f1706a0df9bc3f36aff2b91a47596a82
G18/lab_sgi1/joint.py  755820d7d703cd459aec8271a784c39a69e9374aae501da1cd9f37bbccc21ee9
G18/lab_sgi1/history.py 2d861d7a820168d443e23efb2403b7ed9c3e899a8a79aaa72fd859c46f47c1c1
```

They match `S51/source_binding.py:33-36`, `S52/source_registry.py:12-25`, and the return. This is dependency identity only, not a source grant.

### A.3 Original commission and scope

The original F0 commission at `07ebb10eac214ebc909b92f24b459caf2d37d730` is `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_REVIEW_EXECUTION/COMMISSIONS/F0/00_COMMISSION.md`. Its code-write list at line 8 allows S52 `bootstrap.py`/`session.py`, S48 `product.py` (and S48 `bootstrap.py` only if necessary), and a new unique `WORKER_RETURNS/SOROK-SYN02-F0-PORTABILITY-R1/` for source resolver, tests, and `00_RETURN`.

Actual out-of-scope paths: S51 `bootstrap.py`, new S51 `source_binding.py`, new S52 `source_registry.py`, S52 `run_s52_evidence.py`, S52 `tests/test_f0_source_portability.py`, S52 `tests/test_s52.py`, S48 `tests/test_f0_product_portability.py`, and `SYN02/RETURNS/F0/00_RETURN.md`. Three changed existing files are in the narrow list (`S52/bootstrap.py`, `S52/session.py`, `S48/product.py`).

**Technical-necessity finding:** S51 bootstrap is genuinely involved because `S52/bootstrap.py:28-32` delegates to `s51_install`, and the old S51 bootstrap owned the hardcoded G18 constant. A pure S52 edit cannot remove S51's own path. S52 registry and evidence-helper changes are also motivated. That explains the edits; it does not supply the named owner exception, and it does not authorize the branch substitution.

## B. Independent test replay

### B.1 Environment and commands

```text
W=/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/f0-wt
L=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rf0-logs
cd "$W"
unset S52_G18_SOURCE S51_G18_SOURCE G18_SOURCE M35_G18_SOURCE
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" \
  python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests

PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" \
  python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests

PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" \
  python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/tests

PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" \
  python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/tests
```

`PYTHONDONTWRITEBYTECODE=1`, pytest cache disabled, and `TMPDIR` outside the repository. No environment G18 override was used; the normal accepted-root resolution was exercised.

### B.2 Root replay

| Suite | Result | Own observed time | F0 return count |
|---|---:|---:|---:|
| S52 | 18 passed | 88.35s | 18 |
| S48 | 14 passed | 12.47s | 14 |
| S51 | 13 passed | 32.12s | 13 |
| S49 | 13 passed | 31.69s | 13 |
| **Total** | **58 passed, 0 failed** | ~164.63s | **58** |

The F0 return reports different durations (`S52 56.27s`, `S48 9.27s`, `S51 21.66s`, `S49 20.14s`); counts match, timing is host-dependent and is not acceptance evidence.

### B.3 Alternate-cwd replay

```text
cd /tmp
unset S52_G18_SOURCE S51_G18_SOURCE G18_SOURCE M35_G18_SOURCE
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$L/tmp" \
  python3 -B -m pytest -q -p no:cacheprovider \
  "$W/WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests"
# same for S48, S51, S49
```

| Suite | Result |
|---|---:|
| S52 | **17 passed, 1 failed in 91.04s** |
| S48 | 14 passed in 15.45s |
| S51 | 13 passed in 36.13s |
| S49 | 13 passed in 34.78s |
| **Total** | **57 passed, 1 failed** |

Exact failing test and error:

```text
FAILED WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests/
  test_f0_source_portability.py::test_source_roots_are_resolved_without_embedded_user_paths
FileNotFoundError: [Errno 2] No such file or directory:
  'WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py'
```

The failure is at `S52/tests/test_f0_source_portability.py:36`, which uses `Path(rel).read_text()` against cwd-relative paths. `roots()` itself worked from `/tmp`; the test is not portable. This is a test-artifact defect, not a runtime binding failure, but it invalidates an unconditional 58-test portability claim.

### B.4 Tests / grades not run

- `run_s52_evidence.py` was **not executed** because it writes `evidence/`, `junit/`, and `logs/` into the F0 source tree; it was statically reviewed. Its `FILES` list at line 11 includes `s52/source_registry.py` but omits `tests/test_f0_source_portability.py` and S51 new files.
- Real `run_product_cli`/provider/CLI invocation: **NOT_RUN**. No paid call.
- Native C8/C9/C12, C11/Pyat weld, A5 human, raw survey/source data, full original V3 suite: **NOT_RUN**.
- `S51/S48` evidence helpers: statically inspected; `run_s51_evidence.py:21` and `run_s48_evidence.py:23` still contain `/Users/` paths.

## C. Hostile probes

These are reviewer-owned, sourcefree probes outside the 58 tests. They did not modify the repository or invoke a provider.

### C.1 Symlink / root containment

Constructed a fake return root, an external `g18` directory containing the accepted `joint.py` and `history.py` bytes, and a symlink at the relative G18 path. `resolve_g18` returned the external target and `verify_g18` passed:

```text
resolved .../outside_g18
inside fake root? False
verify_g18 passed on external symlink target
```

This directly falsifies containment: the two-file hash check does not require the resolved root to be inside the injected/allowed root. The external target could also supply an unhashed `lab_sgi1/__init__.py`.

### C.2 Implicit provider fallback

A fake `opencode` executable was placed on `PATH`; all `S48_PRODUCT_*` environment variables were unset. Importing `s48.product` produced:

```text
PRODUCT_CLI /tmp/rf0-provider.../opencode
PRODUCT_MODEL opencode-go/deepseek-v4.1-flash
PRODUCT_VARIANT max
enabled_providers ['opencode-go']
```

The fake executable was not invoked. This demonstrates that `shutil.which("opencode")` supplies a CLI with fixed model/variant defaults and a static provider list without user selection. `s48/product.py:220-258` would pass those to `subprocess.run` if called.

### C.3 Import cache / root switch

A temporary G18 copy with the accepted joint/history bytes was selected via `S52_G18_SOURCE`; a real `lab_sgi1.history` was imported first. After `s51.bootstrap.install()`:

```text
resolved_g18 .../tmp.../g18
imported_before .../real/.../lab_sgi1/history.py
imported_after .../real/.../lab_sgi1/history.py
cached_module_still_original True
```

The newly resolved root was reported as verified, but the cached module remained the old source. `S51/bootstrap.py:25-39` does not purge `sys.modules`. This is a source-custody limitation and a test gap.

### C.4 Duplicate environment priority

```text
missing explicit G18 source -> G18_SOURCE_ENV_INVALID
S52_G18_SOURCE and S51_G18_SOURCE both set -> "one" (S52 wins)
```

The code documents priority but silently accepts conflicting values; no duplicate-conflict refusal. `S51/source_binding.py:38,93-103`.

### C.5 Five-file verifier

`S52/source_registry.py:12-42` checks only S49 `actor.py`/`session.py`, S51 `session.py`, and G18 `joint.py`/`history.py`. The actual G18 directory also contains `__init__.py`, `core.py`, and `proposal.py`; `s52/session.py:13` imports `r30a.first_session`, which is not in the registry. `S52/bootstrap.py:31-32` verifies **after** `s51_install()` imports S49 and G18 history. The F0 return's "before importing/running" claim at `00_RETURN.md:77-84` is false for S49/S51.

## D. F0 requirement acceptance matrix

| Original F0 requirement (`COMMISSIONS/F0/00_COMMISSION.md:11-15`) | Returned proof | Own check | Status |
|---|---|---|---|
| 1. Versioned `SourceRef`: exact hash/manifest, owner, role, scope, origin/effective time; injectable allowed root; traversal/symlink/hash fail closed | New S51 resolver + two-file hashes | Hashes correct; no owner/role/scope/time; symlink outside accepted; no containment | **RED for full requirement; ACCEPT_SCOPED only for normal two-file hash** |
| 2. S52 portable injected G18/S51/S49 roots; qualified cold import from other cwd; refuse missing root/role/hash | S52 bootstrap/registry; root tests pass | Normal root pass; `/tmp` 17/18; test reads cwd-relative; no role check | **REVISE_PRECISE** |
| 3. S48 separate trusted transport/CLI/model/variant; explicit user selection; no auto fallback; fake runner; no paid test | Env fields + PATH fallback + fixed defaults | Implicit PATH/model/variant/provider; no fake-PATH test; no real call by tests | **RED** |
| 4. S52 cold `_OPENING` must not overwrite own errors; base_ok true + S52-only error false; no mutation; cold/fork | Typed refusal + rehashed cold test | Rehashed cold passes; no explicit base_ok assert; no fork/parent/no-leak test | **ACCEPT_SCOPED tested path / REVISE_PRECISE coverage** |
| 5. Adversarial tests: valid pinned source/portable cwd; bad role/hash/missing/traversal/symlink; fake transport; missing model/CLI; cold base_ok; no stale readiness; existing S48/S52 | 5 new tests + 58 root | No traversal/symlink/wrong-role/duplicate-env/import-cache/cold-fork/alternate-cwd tests; cwd fails | **REVISE_PRECISE** |
| 6. Sourcegrade remains TEST_ONLY/SOURCEFREE; no native C11/C12/B/Rule/SCI05/3–5; no fake success | Return says TEST_ONLY | Tests sourcefree; no provider/native; `S52.verify` native=False | **ACCEPT_SCOPED** |

**Overall F0 commission acceptance:** `PARTIAL_DELIVERY`, not `F0_IMPLEMENTED_SCOPED`. The return's engineering `ACCEPT_SCOPED` at `00_RETURN.md:144` is unsupported by requirements 1, 3, and 5 and the cwd/coverage gaps.

## E. F0-R2 acceptance and re-run criteria

1. **S48 explicit selection:** no `shutil.which`; require explicit CLI/model/variant/provider/account; derive `enabled_providers`; fail typed before subprocess; add fake-PATH, missing-model, missing-variant, provider-mismatch tests; no real model call. Acceptance: all new tests pass; no directory/subprocess before selection.
2. **Source custody:** canonical `SourceRef` with owner/role/scope/effective time and full content manifest; allowed-root containment; reject symlink/traversal/duplicate env/wrong-role; hash the complete imported G18/S49/S51 closure; verify before any import; purge/isolate cached modules; add poison-module and root-switch tests. Acceptance: symlink/root-switch probes refuse before import; no unlisted package file executes.
3. **Verification order:** resolve+verify before `s51_install`/`s49_install`/G18 import; test call order. Acceptance: injected changed S49/S51/G18 is refused with no import side effect.
4. **Portable tests:** anchor `S52/tests/test_f0_source_portability.py:36` source reads to repository/test root; add `/tmp` replay. Acceptance: 58/58 from repository root and 58/58 from `/tmp`.
5. **Cold open:** assert base_ok true + S52-only error; test cold fork, parent error, no double failure, no session leak, no mutation; keep native=False. Acceptance: all new negatives pass.
6. **Evidence/source manifest:** include s51 bootstrap/source_binding, s52 new test, r30a import, and complete seam list; fix or explicitly scope S51/S48 evidence helpers. Acceptance: manifest lists every imported dependency and no unresolved `/Users/` path in claimed-portable helpers.
7. **Branch/authority:** owner/HQ decision on alternate branch and extra files; if approved, named exception; if refused, rebase/rework on the commissioned branch with lawful source injection. No integration until resolved.
8. **No native claim:** F0 remains `TEST_ONLY_SOURCEFREE`. F1.1 still requires independently reviewed RP0 plus competent C9/C12 storage-owner approval; no F0 test opens it.

## F. Authority and handoff record

- **CAN011 v1** at `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/CAN_011_V3_MIDDLE_STATE/AUTHORITY.md` (§0, §3) registers only `V3MS_MEDIATOR`, `V3MS_TENSION`, and `V3MS_PRACTICE`, with zero concrete framework/wound/buffer/crack/practice IDs and no standalone V3/P7 release. It is not a C12, source, actor, or A5 grant.
- **S-R** at `ac55c36e42ded82957176896cbc5953db62f7209` remains `ENGINEERING=REVISE_PRECISE`, `SCIENCE=ACCEPT_SCOPED_RESEARCH_PROGRAM`, `AUTHORITY=HOLD`; its F0 row in `RETURNS/S-R/02_REPAIR_AND_IMPLEMENTATION_GATE_DOCKET.md §5` requires exact source identity/role, injectable transport, no paid inference, and the `_OPENING`/base_ok regression. F0 repairs only part of that bounded row and none of S-R's P0 actor/world/SCI05 gaps.
- **Original F0 commission** is the documentary authority at `07ebb10eac214ebc909b92f24b459caf2d37d730`; its line 8 write scope and line 13 explicit-selection requirement are not met by the alternate branch.
- **RF0 commission** at `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_REVIEW_EXECUTION/REVIEW_COMMISSIONS/RF0/00_COMMISSION.md:13-21` supplies the branch/custody/provider/cold-open/test mandates; this review responds to each.
- **Intake** at `.../01_THREE_RETURN_EVIDENCE_INTAKE_R1.md:9,11` already noted the alternate branch, 11-file set, provider fallback, and five-file custody; this review independently reproduces and extends those findings.

**Reviewer disposition:** `RF0_REVISE_PRECISE__F0_PARTIAL_DELIVERY__NOT_ADOPTED__AUTHORITY_HOLD`. No self-adoption, no merge, no source/production change, no native grant. The two reviewer artifacts are the complete write output. The reviewer's own remote SHA/readback is reported in the delivery message after commit/push because a file cannot contain its own commit SHA.
