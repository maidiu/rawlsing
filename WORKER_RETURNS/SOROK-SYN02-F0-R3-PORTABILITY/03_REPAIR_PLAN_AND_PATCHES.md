# SYN02-F0-R3 — repair plan, isolated patch and owner gate

**Status:** `SOURCE_EDITS_HELD__ISOLATED_PATCH_READY__R3_TESTS_RED_ON_R2_GREEN_ON_PATCHED_COPY__NO_NATIVE_GRANT`.

## 1. Source-specific findings

### R3-F01 — Preloaded fake `s51.source_binding` bypass

Actual source:

- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py:20-23` returns any `sys.modules.get("s51.source_binding")` before verifying its path/hash.
- `s51/source_binding.py:368-374` skips a managed module with no `__file__`.
- A fake no-`__file__` binding can return `verify_sources() == True`; S49/G18/R30A are then reached.

**Patch:** load only the canonical `BINDING`; if a preloaded module exists, require its resolved `__file__` to equal `BINDING` and reject a foreign/no-file module. Do not silently trust an arbitrary preloaded object. Tests: `test_preloaded_fake_binding_is_refused_before_managed_imports`.

**Owner:** S52/S51 source engineer. **First consumer:** `s52.bootstrap.install()` / `S52Session`; no native consumer.

### R3-F02 — No-`__file__` managed cache module accepted

Actual source `s51/source_binding.py:368-374`: `if not filename: continue`, so a poisoned `s52`/managed module is invisible to cache verification.

**Patch:** raise `SOURCE_IMPORT_CACHE_UNBOUND` for every managed-prefix module without a canonical file path. Test: `test_managed_no_file_cache_is_refused`.

**Owner:** S51/S52 source engineer. **First consumer:** `S52.bootstrap.install()`.

### R3-F03 — Empty/truncated manifest verifies zero files

Actual `s51/source_binding.py:437-458` iterates `manifest["sources"]` with no minimum count or required root/path set. A provenance-valid empty manifest returns `verified: 0`.

**Patch:** enforce `_MIN_SOURCES = 31` and an externally defined 31-path `REQUIRED_SOURCE_PATHS` set; reject empty/truncated/missing-required-path manifests with `SOURCE_MANIFEST_TRUNCATED`/`SOURCE_MANIFEST_REQUIRED_PATH_MISSING`. Tests: `test_empty_manifest_is_refused`, `test_truncated_manifest_missing_required_path_is_refused`.

**Owner:** S51/S52 source engineer. **First consumer:** `S52.bootstrap.install()`.

### R3-F04 — R30A vendor/r29p and S39 outside the 31-file manifest

The 31-file manifest covers `r30a/r30a/*.py` only. Actual `r30a/first_session.py:24-37` imports `r29p.product`/`r29p.runner`; `r29p/runner.py:11` imports `stable_actor_binding`; `s52/session.py:11` imports S39. These execute but are not listed.

**Patch/choice:** keep the 31-entry **core** manifest and add a separate **external trust registry**:

```text
WORKER_RETURNS/SOROK-SYN02-F0-R3-PORTABILITY/external_source_trust.json
141 entries:
  133 R30A vendor/r29p files
  8 S39 package files
```

Each entry carries root, exact path, SHA-256, bytes, owner, role, scope and effective date. The patched binding verifies this registry before imports and returns `external_verified=141`; no false “full R30A closure” inside the 31-file count. Test: `test_external_trust_covers_r30a_vendor_and_s39`.

**Owner:** S52/R30A source engineering. **First consumer:** `s52.session` / `r30a.first_session`; no native C12.

### R3-F05 — External `log_dir` raises after completed subprocess

Actual `s48/product.py:340-341` calls `stdout_path.relative_to(RETURN)` and `stderr_path.relative_to(RETURN)` after `subprocess.run` and log writes. An external path raises `ValueError` after a real/fake call.

**Patch:** resolve `RETURN` and `log_dir` before `work.mkdir`/`logs.mkdir`/subprocess; refuse an external/relative-escaping log root with typed `S48_PRODUCT_LOG_DIR_OUTSIDE`. Test: `test_external_log_dir_refused_before_fake_subprocess`; fake call marker must be absent.

**Owner:** S48 engineering. **First consumer:** `S48Session.run` / one-call transport.

### R3-F06 — Account/actual-provider receipt overclaim

Actual `s48/product.py:70-74,331` hashes an account alias; account is absent from argv (`:296-306`) and `OPENCODE_CONFIG_CONTENT` (`:289-290`); `actual_provider_call` is hard-coded `True` at `:326` for a fake CLI.

**Patch:** keep the account as an explicit alias (`account_transport: ALIAS_ONLY`), set `actual_provider_call: False`, add `subprocess_completed: True`, `provider_step_observed` from observed event types, and a clear `provider_call_evidence` label. Do not infer account entitlement or a real provider call. Test: `test_fake_cli_receipt_does_not_claim_actual_provider_call`.

**Owner:** S48 engineering + user’s actual provider/account choice. **First consumer:** `S48Session` one-call transport; real entitlement remains `NOT_RUN`.

## 2. Isolated patch

`patches/F0-R3-source-custody.patch` is a unified diff against the exact R2 source startup `60797302652e7d7877443f6e9d0becde5afb8382`.

Patch SHA-256: `40b98b7b6f08016ffe69e4c7054bc7277944a5d06931c9dfa29864f9c80ffea9`.

It changes:

- `S48/s48/product.py` — early log-root validation; truthful receipt fields.
- `S51/s51/source_binding.py` — no-file cache refusal, minimum manifest count, external trust verification.
- `S52/s52/source_registry.py` — canonical/foreign binding check.
- `R2/source_manifest.json` — updated hashes for the patched S48/S51/S52 files.

It does **not** change S39/R30A vendor or any evidence script. The external trust registry is a separate R3-owned artifact.

`git apply --check` against the unmodified source returned `0`. The patch has **not** been applied to the accepted source because no R3 owner scope exists.

## 3. Test levels

| Test | Unpatched R2 | Isolated patched copy | Grade |
|---|---|---|---|
| Existing 58 base tests | 58 passed root; 58 passed `/tmp` | 58 passed root; 58 passed `/tmp` | `EXECUTED` |
| Existing 21 R2 adversarial | 21 passed root; 21 passed `/tmp` | 21 passed root; 21 passed `/tmp` | `EXECUTED` |
| R3 seven adversarial tests | **7 failed** | **7 passed** | `DIFFERENTIAL_EXECUTED` |
| Real provider/account | **NOT_RUN** | **NOT_RUN** | no entitlement |
| Native C8/C9/C11/C12/A5 | **NOT_RUN** | **NOT_RUN** | no grant |

The R3 failures are the expected pre-repair findings; they are not accepted as a passing sourcefree repair. The isolated patched-copy passes are not applied-source acceptance.

## 4. Owner / authority gate

The source-edit hold is explicit in `01_OWNER_SCOPE_AND_HOLD.md`:

- F0-R2 `01_OWNER_SCOPE.md` approves only the **R2** enumerated scope.
- No R3-specific prospective owner record was found.
- Therefore the accepted source is unchanged; only the isolated patch/tests are supplied.
- The historical F0 branch `c821...` and unadopted `9903...` alternate are not adopted or merged.

A competent original **S48/S51/S52 source owner** must approve the exact R3 patch files/scope before application. A separate independent reviewer must inspect the applied patch and replay the tests. No reviewer or R3 implementer can self-approve.

## 5. Downstream consumer and boundaries

First future sourcefree consumer: `s52.bootstrap.install()` and `S48Session.run` (source custody and one-call transport). No C12/A0–A5, native C9, Rule A/T, SCI05, independent B, actor, or production consumer is reached.

- The external trust registry is bounded source custody, not a signed owner grant.
- S39/R30A vendor are covered by exact hashes/owners/roles, not a native dependency release.
- `actual_provider_call: False` is deliberate: a fake/local subprocess is not provider evidence.
- C12 fork perception loss remains an independent RED; this patch does not repair it.
- S48/S51/S52 evidence scripts and `run_s52_evidence.py` remain `NOT_RUN` / residual.

## 6. Science and authority

**SCIENCE: `NO_CHANGE`.** This is sourcefree infrastructure and test semantics; no developmental, psychological, care, memory, Rule A/T, SCI05, independent-B or no-change science is changed or validated.

**AUTHORITY: `HOLD / NO_NATIVE_GRANT`.** No source-owner adoption, provider/account entitlement, C8/C9/C11/C12, CAN/ADP/Pyat, SCI05, human, or production authority is issued. C12 fork repair and F1.1 remain separately gated.

**ENGINEERING: `REVISE_PRECISE / PATCH_READY_FOR_OWNER_APPLICATION / UNPATCHED_SOURCE_HOLDS_REJECT`.** The proposed isolated patch is executable and tested in a copy, but the accepted source intentionally remains unmodified and the R3 owner gate remains open.
