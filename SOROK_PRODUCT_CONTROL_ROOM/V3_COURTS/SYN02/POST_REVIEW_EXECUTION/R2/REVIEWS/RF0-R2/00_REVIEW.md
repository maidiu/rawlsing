# SYN02-RF0-R2 — independent hostile review of F0-R2 source-custody repair

**Reviewer:** RF0-R2 code reviewer on a distinct sealed review branch; not the R2 author, Sorok/Pyat HQ, native source/science issuer, production editor, or self-reviewer.
**Immutable subject:** `60797302652e7d7877443f6e9d0becde5afb8382` on `agent/sorok-syn02-f0-r2-source-custody-repair-r1`.
**Subject parent:** `9903a30d8d9cd4594f58c46bec80e538610a1851` on `agent/sorok-syn02-f0-source-portability-r1`; `9903` is the unadopted F0 alternate source and its parent is the original F0 branch seal `c821b488b3a9a3f0fa01b1981989cc17af637dc1`.
**Original F0 branch:** `agent/sorok-syn02-f0-portable-sourcefree-build-r1` remains at `c821b488...` on the remote; the R2 return's parent line and original-branch line are consistent with the source lineage, while the R2 commit itself is one commit ahead of `9903`.
**Review branch/startup:** `agent/sorok-syn02-review-rf0-r2-code-r1` at `a7a6c781e158cd1317c0ecd0d6e1e542a4fd633d`.
**Evidence date:** 2026-10-28.
**Evidence grade:** `SOURCEFREE_TEST_ONLY`; 58 base tests plus 21 R2 tests from repository root and from `/tmp`; no paid model/provider call, no native C8/C9/C11/C12/A5, no survey/source execution, no production edit, no author-branch edit.
**Final reviewer remote SHA:** reported after the three-file commit and remote readback; not embedded here because self-embedding changes the commit.

## 0. Verdict

**ENGINEERING: `REVISE_PRECISE` — not `ACCEPT_SCOPED`; bounded F0-R2 repair required.**
The explicit S48 selection, removal of the PATH/model fallback, listed-source verification order, root/symlink/traversal checks, cold-open repairs, and dual-cwd test replay are real. A preloaded `s51.source_binding` module without `__file__` bypasses the verifier, the 31-file manifest is smaller than the executed R30A/S39 closure it claims to protect, an empty manifest is accepted as zero verified sources, and an external `log_dir` raises after a completed subprocess. These are finite, sourcefree repairs, not a reason to discard the useful R2 work.

**SCIENCE: `NO_CHANGE / ACCEPT_SCOPED_ENGINEERING_ONLY`.**
F0-R2 changes no psychological, developmental, care, memory, typology, Rule A/T, SCI05, actor, or world semantics. The sourcefree tests are not scientific evidence and create no native person. The RP0-R2 C12 fork perception-loss defect remains a real inherited C12 issue.

**AUTHORITY: `HOLD / NO_NATIVE_GRANT`.**
The `01_OWNER_SCOPE.md` statement that the user chose “Approve enumerated R2 source scope” is worker-captured prospective approval, not independently evidenced original S48/S51/S52 owner adoption. It does not retroactively approve the old F0 alternate delivery at `9903`, merge the old 11-file set, or grant source, account, C8/C9/C11/C12, CAN/ADP/Pyat, SCI05, human, or production authority. F1.1 remains gated by independently reviewed RP0-R2 plus competent C9/C12 storage-owner approval.

## 1. Subject, branch, and write scope

- The R2 commit is one commit by `Maidiu <matthewdavidsmith86@gmail.com>` with parent `9903`; `git diff --stat` reports **16 files changed, 1,639 insertions, 126 deletions**.
- Remote readback verified all three relevant refs: the original F0 branch at `c821`, the unadopted F0 alternate at `9903`, and the R2 subject at `607973`. The R2 return's “Exact source startup” is `9903`; its “Parent” is the parent of that source startup (`c821`), not the R2 commit's immediate parent. That distinction is material for custody, but it is not a hash mismatch.
- The 16 changed paths are the five source edits, two adjusted F0 tests, and nine R2-owned return/manifest/builder/test artifacts:
  - `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48/product.py`
  - `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests/test_f0_product_portability.py`
  - `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py`
  - `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/source_binding.py`
  - `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/bootstrap.py`
  - `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py`
  - `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/tests/test_f0_source_portability.py`
  - `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/{00_RETURN.md,01_OWNER_SCOPE.md,02_TEST_RECEIPTS.md,build_source_manifest.py,source_manifest.json,tests/conftest.py,tests/test_cold_open_r2.py,tests/test_provider_selection_r2.py,tests/test_source_custody_r2.py}`
- The R2 edits are within the commission's enumerated source/test scope except that the historical F0 branch and its extra-file delivery remain a separate custody matter. The prospective scope record authorizes the enumerated R2 paths and tests; it does not authorize an original-branch merge or production integration.
- The unchanged `s52/session.py` preserves the F0 cold-open repair. The R2 suite's “fork” case is a moved-root refusal test, not an actual C12/BP4 fork or a native continuity proof.

## 2. Claim adjudication

| Claim | Verdict | Independent basis |
|---|---|---|
| S48 requires explicit CLI, provider, model, variant, and account; no PATH lookup/default model | **ACCEPT_SCOPED** | `s48/product.py:58-101`; `test_provider_selection_r2.py:38-68`; no provider invoked. |
| S48 fails before work/log directories or subprocess on invalid selection | **ACCEPT_SCOPED** | `s48/product.py:68-101,281-285`; tests `:38-49,71-86`; invalid selection raises before `mkdir`. |
| `enabled_providers` matches the selected provider | **ACCEPT_SCOPED** | `s48/product.py:104-113`; test `:52-68`. |
| 31-file manifest has exact hashes/roles/owners/scopes/effective time for its listed entries | **ACCEPT_SCOPED for the listed 31** | `source_manifest.json`; `test_source_custody_r2.py:36-41`; independent hash audit and test logs. |
| Root containment, symlink/file traversal, duplicate env, wrong role, changed G18 `__init__`/`core` | **ACCEPT_SCOPED for tested paths** | `s51/source_binding.py:106-269,338-347`; tests `:44-83,87-95,190-216`. |
| Verification occurs before listed S49/G18/R30A imports | **ACCEPT_SCOPED for listed entries, with the preloaded-binding exception below** | `s52/bootstrap.py:20-34`; `s51/bootstrap.py:25-42`; subprocess tests `:98-173`. |
| Stale cache/root switch cannot bypass verification | **REVISE_PRECISE / FALSE** | `s52/source_registry.py:20-23` trusts any preloaded `s51.source_binding`; `s51/source_binding.py:368-374` skips modules without `__file__`; probes below. |
| Manifest covers the complete executed R30A package and actual closure | **REVISE_PRECISE / OVERCLAIM** | Manifest has only six `r30a/r30a/*.py`; `r30a/first_session.py:24-37` imports `r29p.product`, `r29p.runner`; `r29p/runner.py:11` imports `stable_actor_binding`; module audit finds unlisted R30A vendor and S39 modules. |
| Manifest rejects an empty or truncated but provenance-valid source list | **REVISE_PRECISE / NO** | `verify_sources` has no minimum count/required-path check; probe returns `verified: 0`. |
| Cold open, base-ok, moved fork, parent exception, false verify, cleanup, non-mutation | **ACCEPT_SCOPED at the sourcefree tested grain** | `s52/session.py:33-56,325-328`; `test_cold_open_r2.py:49-138`; no native C12 fork. |
| 58 base tests and 21 R2 tests pass from root and `/tmp` | **ACCEPT_SCOPED — independently replayed** | Logs `root_*`, `tmp_*`; exact counts in `01_EVIDENCE_AND_TEST_REPLAY.md`. |
| S48 account is explicit and bound to the invocation | **REVISE_PRECISE / PARTIAL** | Account is required and hashed (`product.py:70-74,331`), but absent from argv and `OPENCODE_CONFIG_CONTENT`; fake CLI can return `STATUS OK` with `actual_provider_call: true`; no entitlement. |
| S48 external `log_dir` is safe | **REVISE_PRECISE / FALSE** | `s48/product.py:340-341` calls `relative_to(RETURN)` after the subprocess; external path raises `ValueError` after logs and possible paid call. |
| S48/S51/S52 evidence scripts are portable and complete | **RESIDUAL / NOT_RUN** | S48 and S51 retain `/Users/` paths; `run_s52_evidence.py` was not executed; return discloses these residuals. |
| Historical F0 branch/extra-file custody is resolved | **HOLD** | Original branch remains at `c821`; R2 starts at `9903`; prospective scope does not adopt the old delivery. |
| Native/science authority | **NO_CHANGE / HOLD** | No native execution; C12 fork perception-loss remains RED; no CAN/ADP/SCI05/Pyat grant. |

## 3. Material findings

### F1 — P0: a preloaded `s51.source_binding` bypasses source custody

`s52/source_registry.py:20-23` returns `sys.modules.get("s51.source_binding")` before loading the canonical file. It does not compare that module's path, hash, or contents. `verify_dependencies()` then calls the preloaded module's `verify_sources()`, so an attacker or contaminated process can supply a module that returns `True` without checking the manifest. `s51/source_binding.py:368-374` also skips every managed module without `__file__`, so the cache check cannot see the fake.

The reviewer probe injected a no-`__file__` fake and observed:

```text
VERIFY_RETURN True
CALLS ['source_roots', 'verify_sources']
FAKE_FILE None
```

A second probe with a fake `s52` module lacking `__file__` returned `CACHE_RESULT 31`, proving the cache check silently skips it. A preloaded binding can also direct `s51.bootstrap.install()` to an arbitrary `g18` value because the fake `verify_sources()` result supplies the roots. The target's requirement mapping says “Prevent stale cache/root switch bypass — DONE”; that is false.

**Rival explanation:** the binding is a trust-entry module, and an attacker already controlling `sys.modules` has process control. That does not satisfy the commission's explicit prior-module contamination check: the existing poison-G18 test (`test_source_custody_r2.py:144-173`) proves the authors intended to reject preloaded managed modules, while `_binding()` exempts the most privileged one. A contaminated namespace can also arise from an earlier accepted import, not only an attacker.

**Finite repair:** load the binding only from the canonical `BINDING` path with `importlib.util.spec_from_file_location`, reject any preexisting `s51.source_binding` whose resolved path/hash differs, and reject managed modules without `__file__` (or require a canonical name/path). Add a subprocess test with a fake binding and a poison G18 that asserts no S49/G18 execution and no marker.

**Owner / first consumer:** S51/S52 source engineering; first consumer is `S52.bootstrap.install()` and `S52Session`. No C12/A0–A5 consumer is reached by this sourcefree bypass until a source-owner repair.

### F2 — P1: the manifest does not cover the executed R30A vendor/S39 closure

The 31-file manifest contains 20 repo files (S48 6, S49 5, S51 4, S52 5), 5 G18 files, and 6 `r30a/r30a/*.py` files. It does not contain `r30a/vendor/r29p` or the other R30A vendor modules. `r30a/first_session.py:24-37` imports `bp1`, `bp4`, `r29p.product`, and `r29p.runner`; `r30a/vendor/r29p/r29p/runner.py:11` imports `stable_actor_binding`, and that module imports `historical_actor_producer`, `bp2_joined`, and `bp2p4`. The reviewer module audit observed `stable_actor_binding` at `r30a/vendor/r29p/candidate/stable_actor_binding.py` as unlisted, together with unlisted S39 (`s39.sources` from `s52/session.py:11`) and the declared S36/S37/vendor roots.

The return's `00_RETURN.md:2.2` says “full G18/R30A package hashes” and the requirement table says “complete bounded closure”; only G18 is complete at package level. The declared residual names S36/S37/M35/language/JOIN-E but not S39 or R30A vendor. Bounded closure may intentionally exclude prior accepted roots, but then the claim must be narrowed and the executed unlisted R30A vendor must be declared as a trust-entry seam, not silently omitted.

**Rival explanation:** the R30A “package” may mean only `r30a/*.py`; the vendor is a separately accepted JOIN-E dependency. That explains the omission but not the unqualified “full R30A package” or “all F0-managed imported modules” wording. The actual first session imports those vendor modules, so a changed `stable_actor_binding` is still source that executes under the S52 path.

**Finite repair:** either add the R30A vendor/r29p closure and S39 to the manifest, or explicitly declare those roots outside the bounded closure and prevent their execution before a separately reviewed trust decision. Add an R30A vendor marker/tamper test; keep the existing G18 test. Do not claim complete R30A custody while the vendor is unlisted.

**Owner / first consumer:** S52/R30A source engineering; first consumer is `r30a.first_session` through `S52Session`, not a native C12 consumer.

### F3 — P2: an empty provenance-valid manifest verifies zero files

`verify_sources()` validates schema and root provenance, then iterates `manifest["sources"]` without a minimum count, required labels, or root-relative expected set. A manifest with `sources: []` and intact provenance returns `verified: 0`; the reviewer probe observed:

```text
EMPTY_RESULT {'schema': ..., 'verified': 0, ...}
```

This weakens the “31-file bounded closure” acceptance: a regenerated or truncated manifest can be accepted as a successful custody proof. The manifest is an authored trust root, so this is not an attacker-controlled signal by itself, but the target claims deterministic bounded verification and the builder (`build_source_manifest.py:47-57`) would happily regenerate a partial list.

**Rival explanation:** an owner-authored manifest is trusted, and an empty list is an owner mistake rather than a bypass. The target's acceptance claim still needs a fail-closed count/required-set check; a missing source should fail, not silently verify nothing.

**Finite repair:** require the expected count (31) and root counts, or a constant expected path set, and reject zero/missing roots; add an empty-manifest test that expects refusal. Keep provenance validation separate.

**Owner / first consumer:** S51/S52 source engineering; first consumer `S52.bootstrap.install()`.

### F4 — P1/P2: external `log_dir` raises after a completed subprocess

`s48/product.py:274-341` accepts arbitrary `log_dir`, creates it, runs the selected CLI, writes stdout/stderr, then computes `stdout_path.relative_to(RETURN)` at line 340 and `stderr_path.relative_to(RETURN)` at line 341. An external `log_dir` raised:

```text
ValueError: '.../external-logs/product_2cf24dba5fb0a30e.stdout.jsonl'
is not in the subpath of '.../return' ...
```

The reviewer probe confirmed both log files were written and the subprocess had completed before the exception. The public `S48Session` path accepts `product_log_dir` (`s48/session.py:209,254-272`), so this is an API path, not only a test helper. If the CLI is a paid provider, the call can be lost after being made.

**Rival explanation:** production callers normally use the default `RETURN/logs`, and the function may intentionally require internal logs. That constraint is not validated before the subprocess, and no test covers an external path.

**Finite repair:** validate `log_dir` under `RETURN` before selection/subprocess, or store a portable path label without `relative_to`, and add an external-log test with no real provider. Do not perform the call before refusing an invalid log location.

**Owner / first consumer:** S48 engineering; first consumer is `S48Session.run` / the one-call transport.

### F5 — P2: account selection is metadata, and the receipt overstates the call

`select_product()` requires `S48_PRODUCT_ACCOUNT` and the receipt hashes it (`s48/product.py:70-74,331`), but the account is not passed in argv (`:296-306`) or in `OPENCODE_CONFIG_CONTENT` (`:289-290,104-113`). A fake executable returned a valid event stream and produced `STATUS OK`, `actual_provider_call True`, `ACCOUNT_IN_ARGS False`, and `ACCOUNT_IN_CONFIG False`. The receipt's `actual_provider_call` is a fixed `True` at `:326`, before validating `step_start`, `step_finish`, or text.

This does not prove a provider call occurred or that the user's selected account was authorized. It also means the fake-CLI tests can produce a receipt that looks like an actual call. The target correctly does not claim a paid acceptance, but the evidence semantics are too strong for the sourcefree test.

**Rival explanation:** OpenCode may resolve the account from ambient configuration and has no supported account CLI flag. That makes the selection a policy marker, not a transport binding; the receipt should say `subprocess_completed` or record the observed provider events separately, and the claim should remain `NOT_RUN` for entitlement.

**Finite repair:** pass the account through a supported CLI/env mechanism when one exists, or explicitly document that account is an alias only; derive call evidence from actual step events and name the field accordingly. Add a fake-CLI test that asserts the receipt does not claim a verified provider call; never invoke a real provider.

**Owner / first consumer:** S48 engineering plus the user's provider/account choice; first consumer is `S48Session` one-call transport. No account authority is granted.

### F6 — Residual: evidence scripts and test coverage remain bounded

`run_s48_evidence.py:23` still embeds `/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/`; `run_s51_evidence.py` embeds multiple `/Users/matthewsmith/...` S39/S49 hashes. The return discloses both and says `run_s52_evidence.py` was not changed or executed; its exception remains `NOT_RUN`. This is consistent with the declared scope restriction, but it blocks a whole-family evidence-portability claim. The R2 test `test_manifest_covers_all_g18_package_files` checks G18 only; it does not prove R30A vendor coverage, empty-manifest refusal, preloaded-binding refusal, external `log_dir`, or account transport binding.

The source manifest and tests are acceptable as a bounded sourcefree artifact only after the P0/P1 repairs above; they are not a general portability proof.

## 4. Test and probe summary

Independent replay from repository root and `/tmp`: S52 18, S48 14, S51 13, S49 13 = **58 passed**, plus R2 **21 passed**, from each cwd. Exact commands, environment, log names, file hashes, worker-reported values, and probe outputs are in `01_EVIDENCE_AND_TEST_REPLAY.md`.

The key hostile results are:

- Fake preloaded binding accepted: `VERIFY_RETURN True`; `FAKE_FILE None`.
- No-`__file__` managed cache accepted: `CACHE_RESULT 31`.
- Empty manifest accepted: `verified: 0`.
- Module audit found unlisted `stable_actor_binding` under R30A vendor and unlisted S39/S36/S37/vendor modules.
- Fake CLI returned `STATUS OK` with `actual_provider_call True`; account absent from argv/config.
- External `log_dir` raised after the subprocess and after both log files were written.

No paid CLI/provider, native C8/C9/C11/C12/A5, survey/source data, or production mutation was used. `run_s52_evidence.py`, the S48/S51 evidence scripts, and real provider/account entitlement remain `NOT_RUN`.

## 5. Handoff

**Disposition:** `RF0_R2_REVISE_PRECISE__SOURCEFREE_PARTIAL__NOT_ADOPTED__AUTHORITY_HOLD`.

The code is a useful bounded R2 repair, but `ACCEPT_SCOPED` is not supported while a preloaded binding can return a successful verification and the 31-file manifest omits executed R30A vendor/S39 source. The finite repairs in `02_ACCEPTANCE_AND_OWNER_GATE.md` should be implemented and re-reviewed without paid or native execution. The reviewer does not merge, adopt, or grant source/provider/native rights.
