# SYN02-RF0 — independent hostile review of F0 alternate return

**Reviewer:** fresh RF0 I3 independent reviewer; not F0/RP0/RM40/S/S-R author, Sorok/Pyat HQ, production editor, original CAN/ADP/SCI05 issuer, or self-reviewer.
**Immutable subject:** `9903a30d8d9cd4594f58c46bec80e538610a1851` on `agent/sorok-syn02-f0-source-portability-r1`.
**Original F0 subject:** `agent/sorok-syn02-f0-portable-sourcefree-build-r1` remains at source seal `c821b488b3a9a3f0fa01b1981989cc17af637dc1`.
**Review branch/startup:** `agent/sorok-syn02-review-rf0-code-r1` at `4fc21d74d5c585ba6c83b3de2e6ace2d5127b392`.
**Evidence date:** 2026-10-27.
**Evidence grade:** `SOURCEFREE_TEST_ONLY`; 58/58 from repository root, 57/58 from `/tmp`; no provider/paid call, no native C8/C9/C12/C11/A5, no raw survey, no production edit.
**Final reviewer remote SHA:** reported in the delivery message and remote readback; not embedded here because self-embedding changes the commit.

## 0. Verdict

**ENGINEERING: `REVISE_PRECISE` — not `ACCEPT_SCOPED`; bounded F0-R2 required.**
Normal source resolution, the two accepted G18 file hashes, missing-CLI refusal, and the targeted cold-open refusal are real. The delivery is nevertheless not the commissioned complete F0: explicit user-selected provider/model/CLI is unimplemented, full source custody/containment is absent, dependency verification occurs after imports, the portable-cwd test fails, cold fork/parent-error behavior is untested, and 8 of 11 changed files are outside the narrow write list.

**SCIENCE: `NO_CHANGE / ACCEPT_SCOPED_ENGINEERING_ONLY`.**
F0 changes no psychological, developmental, care, memory, typology, Rule A/T, SCI05, or B/world semantics. It is not scientific evidence and creates no native person.

**AUTHORITY: `HOLD / NO_NATIVE_GRANT`.**
The alternate branch and extra-file write scope are a material protocol deviation, not an authorized substitution. Reviewer does not adopt the branch swap. No C8/C9/C11/C12, CAN/ADP/Pyat, source, human, provider-account, or production authority is issued. F1.1 remains blocked on independently reviewed RP0 plus competent C9/C12 storage-owner approval, neither of which F0 supplies.

## 1. Subject, identity, and branch/write-scope discrepancy

F0 is one commit by Maidiu `<matthewdavidsmith86@gmail.com>` with parent `c821b488b3a9a3f0fa01b1981989cc17af637dc1`; the diff is 11 files, 616 insertions and 68 deletions. The ten source/test SHA-256 values in `SYN02/RETURNS/F0/00_RETURN.md` were independently recomputed and all match; the return file hash is `ad2a5607be946a2b8f204e1bf5a59969097049a9c17c8da515abe857da600f75`. There are no C9/C12, CAN/ADP/Pyat, PRE-MAIN, central-atlas, or production edits in the changed set.

The originally commissioned branch is still at `c821b488...`, zero ahead. The author used a different branch at `9903a30d...`, one commit ahead of the same seal. The intake correctly records this as a material protocol deviation; no owner authorization for the branch substitution or the extra files appears in the F0 commit or return. The review therefore assesses the alternate branch faithfully, as instructed, but does not adopt the swap.

| Path | F0 status | Narrow F0 write list | Assessment |
|---|---|---|---|
| `S52/.../s52/bootstrap.py` | M | allowed | in scope |
| `S52/.../s52/session.py` | M | allowed | in scope |
| `S48/.../s48/product.py` | M | allowed | in scope, but incomplete provider selection |
| `S51/.../s51/bootstrap.py` | M | **not allowed** | technically required to remove S51's own hardcoded G18; named exception missing |
| `S51/.../s51/source_binding.py` | A | **not allowed** | new resolver outside the new F0 directory; exception missing |
| `S52/.../s52/source_registry.py` | A | **not allowed** | new verifier outside the new F0 directory; exception missing |
| `S52/.../run_s52_evidence.py` | M | **not allowed** | evidence-portability edit; exception missing |
| `S52/.../tests/test_f0_source_portability.py` | A | **not allowed** | should be under the new F0-owned test directory |
| `S52/.../tests/test_s52.py` | M | **not allowed** | existing test edited |
| `S48/.../tests/test_f0_product_portability.py` | A | **not allowed** | under S48 tests, not the new F0-owned test directory |
| `SYN02/RETURNS/F0/00_RETURN.md` | A | **not allowed** | return outside the named F0-owned directory |

The S51 bootstrap edit is technically difficult to avoid: `S52.install()` calls `s51_install()`, and the pre-F0 S51 bootstrap owns the hardcoded G18 constant, so a pure S52 change cannot remove that path. The S52 registry and evidence-helper edits are also technically motivated. Technical necessity is not a waiver. The correct authority path is either a named, owner-approved exception limited to these exact files or a rebase/reassignment onto the commissioned branch. The reviewer makes no branch adoption decision.

**First real consumers:** `S52.bootstrap.roots()`/`S52Session` consume the resolver; the S48 `run_turn` one-call transport consumes the provider selection; Sorok HQ/F0 owner consume the branch/exception decision.

## 2. Per-claim adjudication

| Claim | Verdict | Independent basis |
|---|---|---|
| G18 normal resolution no longer embeds `/Users/` in S51/S52 bootstrap | **ACCEPT_SCOPED** | `S51/bootstrap.py:7-21,42-51`, `S52/bootstrap.py:7-51`; normal 58-test root run. |
| Exact SHA-256 for the five named dependency files is correct | **ACCEPT_SCOPED** | Ten changed source/test hashes and both G18 hashes independently match the return and actual files. |
| Missing or hash-mismatched named files fail closed | **ACCEPT_SCOPED** | `S51/source_binding.py:115-131`, `S52/source_registry.py:28-42`; tampered/substituted tests pass. |
| Full source custody: exact path, owner, role, scope, origin/effective time, whole manifest | **RED** | Two G18 files and three S49/S51 files only; no owner/role/clock; no containment; symlink escape demonstrated; unhashed G18 package files execute. |
| Verification occurs before importing/running accepted dependencies | **RED** | `S52/bootstrap.py:31-32` calls `s51_install()` **before** `verify_dependencies(...)`; `S51/bootstrap.py:36-38` imports `s49` and `lab_sgi1.history`. The return's "before importing/running" at `00_RETURN.md:77-84` is false for S49/S51. |
| Duplicate env names reject conflict | **REVISE_PRECISE** | `S51/source_binding.py:38,93-103`: first of `S52_G18_SOURCE`, `S51_G18_SOURCE`, `G18_SOURCE`, `M35_G18_SOURCE` silently wins; no conflict error. |
| Import cache and mutable `sys.path` preserve one verified source | **REVISE_PRECISE** | `S51/bootstrap.py:25-39` mutates global `sys.path` and imports; `sys.modules` is never purged. Probe below shows a verified new root while `lab_sgi1.history` remains the old module. |
| S52 verifies only five files, not complete S49/S51/G18 ancestry | **RED for full-custody claim; ACCEPT_SCOPED for five named files** | `S52/source_registry.py:12-42`; `s52/session.py:13` imports `r30a.first_session`, absent from the registry; `S51/source_binding.py:33-36` hashes only two of the G18 package files; actual G18 also has `__init__.py`, `core.py`, and `proposal.py`. |
| S51 bootstrap edit shadows S49 or changes effective path order | **ACCEPT_SCOPED / NO_REGRESSION OBSERVED** | Static order is equivalent; `S51/bootstrap.py:30-33` inserts `RETURN,S49,G18`; `S52/bootstrap.py:24-32` then `s51_install()` yields the same effective precedence. No S49 shadowing found; no order test exists. |
| S52 cold open no longer overwrites its own errors | **ACCEPT_SCOPED for tested rehashed self-candidate** | `s52/session.py:33-56,266-328`; old `_OPENING`/`ok=True` removed; clean cold and rehashed cold tests pass. |
| Cold fork, parent error, no double failure, no session leak, verification non-mutation | **REVISE_PRECISE / NOT_RUN** | No fork test; no explicit `base_ok=True` assertion; no mutation/leak test. `S52Session.open` catches only base `S37_VERIFY_FAILED` and rethrows other refusals. |
| S48 fails typed when no CLI is available | **ACCEPT_SCOPED for the empty-CLI branch** | `s48/product.py:227-231`; `test_f0_product_portability.py:12-22` passes and creates no directories. |
| S48 user selection is explicit; no automatic provider/model/account fallback | **RED** | `s48/product.py:20-32` uses `shutil.which("opencode")` and fixed model/variant defaults; `PRODUCT_CONFIG` at 46-50 statically enables only `opencode-go`. A fake `opencode` on `PATH` with no env probe yields the fallback CLI plus `opencode-go/deepseek-v4.1-flash`/`max`. |
| S48 static `enabled_providers` matches injected model/provider | **REVISE_PRECISE** | `s48/product.py:25-32,46-50`; model/variant can be injected while `enabled_providers` stays `["opencode-go"]`; no provider/account validation. |
| 58 sourcefree tests pass | **ACCEPT_SCOPED from repository root only** | Own fresh root replay: S52 18, S48 14, S51 13, S49 13 = 58 passed. Root-only; alternate cwd is 57/58. |
| Claim is portable from another working directory | **REVISE_PRECISE** | From `/tmp`, S52 is 17/18; `tests/test_f0_source_portability.py:36` reads relative `WORKER_RETURNS/...` paths from cwd and fails. S48/S51/S49 pass from `/tmp`. |
| S52 evidence helper is portable | **ACCEPT_SCOPED for `run_s52_evidence.py`; INCOMPLETE for the source family** | `run_s52_evidence.py:5,16-18` derives `REPO` and seams correctly; its `FILES` list omits the new F0 test and S51 new files. `run_s51_evidence.py:21` and `run_s48_evidence.py:23` still contain `/Users/` paths. |
| No paid/provider call by F0 tests | **ACCEPT_SCOPED** | S48 tests use a fake product runner and the missing-CLI branch raises before subprocess; no provider invocation run by reviewer. The code path nevertheless permits an implicit paid CLI. |
| No C9/C12 native or semantic change | **ACCEPT_SCOPED** | Diff is confined to S48/S51/S52 sourcefree code, tests, evidence helper, and F0 return; `S52.verify()` reports `native=False`. |
| F0 outcome `F0_IMPLEMENTED_SCOPED` / engineering `ACCEPT_SCOPED` | **REVISE_PRECISE / OVERCLAIM** | `00_RETURN.md:10,144`; provider selection, full custody, verification order, cwd replay, cold fork/parent, and branch/exception are not satisfied. |

## 3. Material findings

### F1 — RED: explicit user-selected provider/model/CLI is not implemented

`WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48/product.py:20-32` resolves the CLI as `S48_PRODUCT_CLI` **or `shutil.which("opencode")`** and fills model/variant with `opencode-go/deepseek-v4.1-flash`/`max` when unset. `PRODUCT_CONFIG` at lines 46-50 always enables only `opencode-go`. `run_product_cli` at lines 220-258 then launches that CLI with those defaults.

Consequence: a host with `opencode` on `PATH` can be invoked with no user-selected CLI, model, variant, account, or provider. The F0 return itself documents the PATH fallback at `00_RETURN.md:62-66`. The commission required explicit selection and no automatic fallback (`F0/00_COMMISSION.md:13`); the intake already flagged this defect (`01_THREE_RETURN_EVIDENCE_INTAKE_R1.md:11`). The missing-CLI test only covers the empty-string branch; it does not test PATH discovery, missing model/variant, or provider mismatch (`tests/test_f0_product_portability.py:12-28`).

**Alternative cause:** `shutil.which` was intended as portability, not provider choice. That does not supply user consent or provider/model coherence.

**Finite repair:** require explicit `S48_PRODUCT_CLI`, `S48_PRODUCT_MODEL`, `S48_PRODUCT_VARIANT`, and provider/account selection; validate model prefix against an injected `enabled_providers`; fail typed before directory creation or subprocess; add fake-PATH, missing-model, missing-variant, and provider-mismatch tests; never invoke a real model in tests.

**Owner / first consumer:** S48 engineering implements; the user alone selects the actual provider/model/account; first consumer is the S48 one-call `run_turn` transport.

### F2 — RED: source custody lacks containment and complete identity

`S51/source_binding.py:33-38` hashes only `lab_sgi1/joint.py` and `lab_sgi1/history.py`. The resolved G18 directory also contains `lab_sgi1/__init__.py`, `core.py`, and `proposal.py`; those execute on import but are not in `G18_EXPECTED`. `S52/source_registry.py:12-42` adds only S49 `actor.py`/`session.py` and S51 `session.py`. There is no owner, role, scope, origin/ref, effective clock, or whole-content manifest.

`S51/source_binding.py:74-107` uses `.resolve()` on candidate roots and returns the first directory; `verify_expected` at 115-131 does not require the resolved root to be inside an injected allowed root, does not reject symlinks, and does not check duplicate env conflicts. A concrete probe created an external G18 target with the accepted joint/history bytes, symlinked it under a fake return root, and observed:

```text
resolved .../outside_g18
inside fake root? False
verify_g18 passed on external symlink target
```

This proves the two-file hash check can accept a path outside the claimed root. It also matters for the unhashed package files: `lab_sgi1/__init__.py` is imported before complete package provenance is established. The F0 return's claim that a changed source cannot silently execute (`00_RETURN.md:84`) is true only for the five named files, not the package/dependency closure.

**Alternative cause:** the accepted "vendor" may be trusted by convention. The commission explicitly required traversal/symlink/role checks; convention is not an injected boundary.

**Finite repair:** introduce a versioned `SourceRef` with content manifest, owner/role/scope/origin/effective time; inject allowed roots; reject `..`, symlink escape, duplicate conflicting env, wrong-role roots, and missing/unlisted imported files; verify the full imported closure before import; keep only one G18 manifest rather than duplicated constants in S51 and S52.

**Owner / first consumer:** S51/S52 source engineering; first consumer `S52.bootstrap.roots()` and `S52Session`.

### F3 — RED: dependency verification happens after imports

`S52/bootstrap.py:31-32` calls `s51_install()` and only then `verify_dependencies(s51_roots())`. `S51/bootstrap.py:36-38` imports `s49` and `lab_sgi1.history` inside `s51_install()`. Thus S49 and S51 dependency hashes are checked after the modules have already been imported. The F0 return says "S52 verifies the exact accepted dependency files before importing/running" (`00_RETURN.md:77-84`); that order is false for S49/S51.

This is a sourcefree code defect, not a style issue: a substituted S49/S51 module can execute before the hash failure. The existing `test_substituted_dependency_root_is_rejected` calls `verify_dependencies` directly after `roots()`; it does not assert bootstrap/import ordering.

**Finite repair:** resolve and verify all dependencies before any `s51_install`/`s49_install`/G18 import; add a subprocess test that injects a poison module and observes refusal before import side effects; assert call order.

**Owner / first consumer:** S51/S52 bootstrap engineering; first consumer `S52.install()`/`S52.roots()`.

### F4 — REVISE_PRECISE: alternate-cwd test failure contradicts the portability claim

Root replay is 58/58. From `/tmp`, S52 is **17 passed, 1 failed**; S48/S51/S49 pass. The failing test is `tests/test_f0_source_portability.py::test_source_roots_are_resolved_without_embedded_user_paths`, because line 36 executes `Path(rel).read_text()` with cwd-relative paths. Exact failure:

```text
FileNotFoundError: [Errno 2] No such file or directory:
'WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py'
1 failed, 17 passed in 91.04s
```

The runtime `roots()` call succeeded; the test artifact is cwd-sensitive. The F0 return's 58-test claim is therefore root-only, not the commission's "portable cwd" claim. The test should anchor reads to `REPO`/`Path(__file__).resolve().parents[...]` and add a `/tmp` replay.

**Owner / first consumer:** S52 test owner; first consumer is the F0 sourcefree acceptance suite/CI.

### F5 — REVISE_PRECISE: cold-open repair is real at tested grain, but fork/parent/no-leak coverage is absent

`S52/session.py:33-56` removes `_OPENING`, adds typed `S52ColdOpenRefusal`, catches base `S37_VERIFY_FAILED`, verifies the returned session, and closes on failure. `s52/session.py:327` is `r["ok"]=base_ok and not errors`; the old override is gone. Clean cold and rehashed-candidate cold tests pass in the 18-test suite. This is the original static risk now executed as a sourcefree regression, and it is accepted at that grain.

The test does not explicitly assert `base_ok is True` while a S52-only error exists, does not test cold fork, does not test a parent error other than `S37_VERIFY_FAILED`, and does not prove no state mutation/session leak. The code path for a non-`S37_VERIFY_FAILED` base refusal rethrows without a typed S52 wrapper; that may be correct, but it is untested.

**Finite repair:** add explicit base-ok/S52-only-error, cold-fork, parent-error, double-failure, and close/no-mutation tests; keep `native=False`; no native readiness promotion.

**Owner / first consumer:** S52 session engineering; first consumer `S52Session.open` and the C12 cold/fork consumer.

### F6 — HOLD: alternate branch and extra-file authority are unresolved

The branch substitution is a material protocol deviation. The original branch remains at the seal; the actual return is on a different branch. No owner authorization is present in the commit/return. Eight changed paths are outside the narrow write list. The reviewer cannot waive this by finding the code technically useful.

**Decision owner:** F0 original source/engineering owner plus Sorok HQ/user. Either approve a named retroactive exception for `9903a30d...` and exactly the extra paths, or require a rebase/rework on `agent/sorok-syn02-f0-portable-sourcefree-build-r1` with the extra-file exception. No integration before resolution.

### F7 — REVISE_PRECISE: evidence helper/source manifest is still incomplete

`run_s52_evidence.py:5,16-18` correctly derives `REPO` and seam paths, but its `FILES` list at line 11 omits the new `tests/test_f0_source_portability.py` and the new S51 source-binding/bootstrap files; `seams` still does not include `r30a.first_session`. `run_s51_evidence.py:21` and `run_s48_evidence.py:23` still contain `/Users/` paths. The F0 return only claims the S52 helper was repaired, so this is a scope/claim gap rather than a contradiction of the narrow S52 statement; it still blocks a claim of whole-family source portability.

**Owner / first consumer:** S51/S48 evidence owners; first consumer the S51/S48 evidence manifests.

### F8 — REVISE_PRECISE: import cache is not part of source custody

`S51/bootstrap.py:25-39` only removes/inserts `sys.path` entries and imports. It never removes cached `s51`, `s49`, `lab_sgi1`, or submodules from `sys.modules`. A probe resolved a new G18 root but `lab_sgi1.history.__file__` remained the original module:

```text
resolved_g18 .../tmp.../g18
imported_before .../real/.../lab_sgi1/history.py
imported_after .../real/.../lab_sgi1/history.py
cached_module_still_original True
```

Conversely, a module preloaded from a malicious source can survive a subsequent verified root. `G18` is also cached in a module global, and `_INSTALLED` makes later source changes no-ops. This is a real source-custody limitation, especially because the verifier is supposed to defend against substituted source.

**Finite repair:** isolate imports in a fresh subprocess/process boundary or explicitly purge the affected module closure before install; add a poison-cache test and a root-switch test.

**Owner / first consumer:** S51/S52 bootstrap engineering; first consumer the import path used by `S52Session`.

### F9 — ACCEPT_SCOPED: truthful positive fragments

The following are independently verified and should not be discarded:

- The two accepted G18 hashes and five named dependency hashes are correct at the frozen source.
- Normal G18 resolution works without `/Users/` in S51/S52 bootstrap.
- A tampered named file and an empty substituted G18 root are refused.
- Missing `S48_PRODUCT_CLI` (empty value) raises typed before directory creation.
- The targeted cold-open rehashed self-candidate is refused with `S52_COLD_OPEN_INVALID`.
- The 58 tests pass from the repository root; S48/S51/S49 also pass from `/tmp`.
- No paid/provider/native execution was performed by the tests or reviewer.

These fragments support a bounded F0-R2, not an unconditional F0 acceptance.

## 4. Test replay and hostile probes

**Root replay:** S52 18, S48 14, S51 13, S49 13 = **58 passed**. Exact command/config and timing are in `01_EVIDENCE_AND_ACCEPTANCE.md §B`. The F0 return's timing numbers differ (host variance); the counts match.

**Alternate cwd replay:** S52 **17 passed, 1 failed**; S48 14 passed; S51 13 passed; S49 13 passed = **57/58**. The one failure is the F0 portability test reading cwd-relative source paths; the runtime root resolution itself worked from `/tmp`.

**Probes not part of the 58 tests:**

1. Symlink/root containment: external G18 target with accepted bytes accepted through a symlink; `inside fake root? False`.
2. Provider fallback: fake `opencode` on `PATH`, no env, yields `PRODUCT_CLI=<fake>`, `PRODUCT_MODEL=opencode-go/deepseek-v4.1-flash`, `PRODUCT_VARIANT=max`, `enabled_providers=["opencode-go"]`.
3. Import cache: new verified root, old `lab_sgi1.history` module retained.
4. Env priority: missing explicit G18 source yields `G18_SOURCE_ENV_INVALID`; simultaneous `S52_G18_SOURCE` and `S51_G18_SOURCE` silently choose the former.

No real CLI/provider was invoked; no native A5/C11/C12 test was run.

## 5. Three courts and finite F0-R2

### ENGINEERING — `REVISE_PRECISE`

The normal portability path is a useful bounded start, but the return's `ACCEPT_SCOPED` is unsupported. Required repairs, in order:

| Priority | Repair | Owner | First consumer |
|---|---|---|---|
| P0 | S48 explicit CLI/model/variant/provider/account selection; remove `shutil.which` and fixed defaults; derive `enabled_providers`; fail before subprocess; fake-PATH/missing-model/provider-mismatch tests | S48 engineering + user provider choice | S48 `run_turn` |
| P0 | Resolve and verify the full dependency closure **before** any import; poison-module/order test | S51/S52 bootstrap engineering | `S52.install()`/`roots()` |
| P0 | `SourceRef` owner/role/scope/effective-time/manifest; allowed-root containment; reject symlink/traversal/duplicate env/wrong-role; hash unlisted G18/package modules; purge import cache | S51/S52 source engineering | `S52.bootstrap.roots()`/`S52Session` |
| P1 | Fix alternate-cwd test paths; run root and `/tmp` 58/58; add no-paid assertion | S52 test owner | F0 sourcefree suite |
| P1 | Add cold-fork/parent-error/base-ok/S52-only-error/no-mutation/no-leak tests | S52 session owner | `S52Session.open` |
| P1 | Complete S52/S51 source manifest and evidence helper coverage | S51/S52 evidence owners | Evidence manifests |
| P2 | Resolve branch/extra-file exception; no integration until owner decision | F0 owner + Sorok HQ/user | F0 acceptance gate |

**F0-R2 re-run criteria:** 58/58 from repository root **and** from `/tmp`; new F1-F3 tests; no provider call; source probes reject symlink/duplicate-env/import-cache; cold fork/parent tests pass; exact hashes; exact branch/exception receipt.

### SCIENCE — `NO_CHANGE / ACCEPT_SCOPED_ENGINEERING_ONLY`

F0 does not test or issue a psychological or developmental rule. S-R at `ac55c36...` already holds the architecture `REVISE_PRECISE` and C9/C12/SCI05 RED issues; F0 repairs none of them. The F0 sourcefree tests cannot support a human, care, memory, practice, Rule A/T, or SCI05 positive. `NO_CHANGE` is the correct scientific disposition.

### AUTHORITY — `HOLD / NO_NATIVE_GRANT`

No C8/C9/C11/C12, CAN/ADP/Pyat, original survey, actor, provider-account, or production authority is granted. CAN011 v1 registers only `V3MS_MEDIATOR`, `V3MS_TENSION`, and `V3MS_PRACTICE`, with zero concrete framework/wound/buffer/crack/practice IDs and no standalone V3/P7 release; it is not a source or C12 grant. The alternate branch and extra files require the owner/HQ decision above. F1.1 remains gated by independent RP0 review and competent C9/C12 storage-owner approval; F0 cannot open it. No self-adoption.

## 6. Handoff

**Disposition:** `RF0_REVISE_PRECISE__F0_PARTIAL_DELIVERY__NOT_ADOPTED__AUTHORITY_HOLD`.

The alternate branch is reviewed faithfully and not modified. The correct next action is an owner decision on the branch/extra-file exception, followed (if approved) by the bounded F0-R2 repairs above and a fresh independent re-review. If the exception is refused, the work must be reassigned/reworked onto the commissioned branch with the exact extra-file exception or a different lawful source-injection design. The reviewer does not merge, adopt, or issue native rights.

**Exact changed paths / test commands / logs:** `01_EVIDENCE_AND_ACCEPTANCE.md`.

**Reviewer remote SHA/readback:** reported in the delivery message after the two-file commit and push; this file does not self-embed it.
