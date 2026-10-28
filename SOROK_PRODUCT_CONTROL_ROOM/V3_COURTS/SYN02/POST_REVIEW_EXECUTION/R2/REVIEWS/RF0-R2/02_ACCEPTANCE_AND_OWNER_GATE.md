# SYN02-RF0-R2 — acceptance and owner gate

**Reviewer:** RF0-R2 code reviewer; not the R2 author, Sorok/Pyat HQ, native source/science issuer, production editor, or self-reviewer.
**Immutable subject:** `60797302652e7d7877443f6e9d0becde5afb8382`.
**Parent / original F0:** R2 parent `9903a30d...`; original F0 branch `agent/sorok-syn02-f0-portable-sourcefree-build-r1` at `c821b488...`; the original branch remains unadopted.
**Review branch/startup:** `agent/sorok-syn02-review-rf0-r2-code-r1` at `a7a6c781...`.
**Disposition:** `RF0_R2_REVISE_PRECISE__SOURCEFREE_PARTIAL__NOT_ADOPTED__AUTHORITY_HOLD`.

## 1. Engineering gate

**ENGINEERING: `REVISE_PRECISE`, not `ACCEPT_SCOPED`.**

The following positive claims are independently accepted at their stated sourcefree grain:

- S48 explicitly requires CLI, provider, model, variant, and account; PATH discovery and fixed model/provider defaults are removed; selection fails before work/log directories or subprocess (`s48/product.py:58-113,274-285`; R2 provider tests).
- The listed 31-file manifest verifies exact hashes and exact root provenance; normal G18/R30A paths resolve; listed symlink/traversal/conflicting-env/wrong-role cases refuse (`s51/source_binding.py`; custody tests).
- Verification of the listed entries occurs before the S49/G18 imports; the preloaded G18 poison test and subprocess ordering test pass.
- The S52 cold-open verifier preserves the F0 repair and adds tested base-ok, moved-fork, parent-refusal, double-failure, cleanup, and non-mutation cases.
- The 58 base tests and 21 R2 tests pass from both repository root and `/tmp`; the RF0 alternate-cwd failure is repaired.

`ACCEPT_SCOPED` is nevertheless unsupported because three sourcefree claims are false or incomplete:

1. **The stale-cache/root-switch bypass is not closed.** A preloaded `s51.source_binding` with no `__file__` is trusted by `s52/source_registry.py:20-23`; `_check_import_cache` skips it at `s51/source_binding.py:372-374`. A fake module returned `verify_dependencies() == True` without reading the manifest. The same fake can supply arbitrary roots to `s51.bootstrap.install()`.
2. **The 31-file manifest is not the executed closure.** `r30a/first_session.py:24-37` imports `r29p.product`/`r29p.runner`; `r30a/vendor/r29p/r29p/runner.py:11` imports `stable_actor_binding`; the manifest contains only six `r30a/r30a/*.py`. S39 is imported by `s52/session.py:11` and is not in the manifest or the named exclusions. The “full G18/R30A package hashes” and “complete bounded closure” claims need narrowing or repair.
3. **An empty provenance-valid manifest is accepted** with `verified: 0`; there is no minimum count or required-path check.

Two additional sourcefree defects require repair before a later acceptance:

4. External `log_dir` raises `ValueError` at `s48/product.py:340-341` after the subprocess and after both log files are written. `S48Session` exposes `product_log_dir`; a completed paid call could be lost.
5. Account selection is not passed to the CLI/config; the receipt sets `actual_provider_call: True` for a fake executable. This is not proof of a provider call or entitlement. It must be documented as an alias-only selection or bound through a supported transport, and the receipt must not overclaim.

The evidence and exact probe outputs are in `01_EVIDENCE_AND_TEST_REPLAY.md`; the detailed claim table and finding chains are in `00_REVIEW.md`.

## 2. Required finite repairs

| Priority | Repair | Owner | First real consumer | Re-review evidence |
|---|---|---|---|---|
| P0 | Load `s51.source_binding` only from the canonical path; reject a preexisting module with a different resolved path/hash; reject managed modules without `__file__`; add a fake-binding subprocess poison test that proves no S49/G18 import or marker | S51/S52 source engineering | `S52.bootstrap.install()`, `S52Session` | New test plus a negative probe; no provider |
| P0 | Add R30A vendor/r29p and S39 to the manifest, or explicitly declare each as an out-of-closure trust-entry and prevent its execution before a separate trust decision; add an unlisted R30A vendor marker/tamper test | S52/R30A source engineering | `r30a.first_session` via `S52Session` | Manifest/test proof; no claim of full closure unless actually covered |
| P1 | Require the expected 31-file count/root set (or an exact required-path set); reject empty/truncated manifests; add an empty-manifest refusal test | S51/S52 source engineering | `S52.bootstrap.install()` | Test expects typed/source-binding refusal |
| P1 | Validate external `log_dir` before selection/subprocess, or store a portable path label without `relative_to`; add an external-log test and ensure no completed call is discarded | S48 engineering | `S48Session.run` / one-call transport | Test with fake CLI; no paid call |
| P2 | Bind the selected account through a supported CLI/env transport, or document it as an alias-only receipt marker; derive call evidence from observed step events; rename/qualify `actual_provider_call` | S48 engineering + user provider choice | `S48Session` one-call transport | Fake-CLI receipt test; real entitlement remains `NOT_RUN` |
| P2 | Keep S48/S51/S52 evidence-script host paths and `run_s52_evidence.py` `NOT_RUN` as explicit residuals; do not claim general portability | S48/S51/S52 evidence owners | Evidence manifests | Static inspection plus declared residuals |
| P3 | Decide historical F0 branch/extra-file custody separately; do not merge or adopt `9903` by this review | F0 original owner + Sorok HQ/user | Source integration gate | Separate owner record |

The repairs are bounded and sourcefree. No real provider, account, native C12/C9, raw source/survey, or production execution is required to test them.

## 3. Science gate

**SCIENCE: `NO_CHANGE / ACCEPT_SCOPED_ENGINEERING_ONLY`.**

F0-R2 does not change or test a psychological, developmental, care, memory, typology, Rule A/T, SCI05, actor, or world semantics. The sourcefree tests do not constitute scientific evidence, a person, a native session, or an independent-B result. The R2 manifest’s `repo` provenance owner is the implementer, not a scientific owner; no learned graph or rule is created.

The RP0-R2 C12 fork perception-loss finding remains a real source-level issue inherited from the C12/BP4 seam. R2 does not repair it. The scientific disposition therefore remains unchanged and no F1.1 release is opened.

## 4. Authority gate

**AUTHORITY: `HOLD / NO_NATIVE_GRANT`.**

- The R2 owner-scope record says the user selected “Approve enumerated R2 source scope.” This is documented prospective sourcefree write scope. It is not an independently witnessed original S48/S51/S52 owner adoption, not retroactive approval of the old F0 alternate delivery at `9903`, and not a source/native grant.
- The original F0 branch remains at `c821`; the R2 branch starts from the unadopted `9903` alternate. The reviewer does not adopt, merge, rebase, or legitimize the historical extra-file set. A separate original-owner/HQ disposition remains required.
- The reviewer issues no C8/C9/C11/C12, CAN/ADP/Pyat, SCI05, Rule A/T, provider-account, human, or production authority. No account entitlement is inferred from the S48 selection.
- C12 fork perception-loss remains `RED`/held pending the C12 source owner’s Option A patch, Option B hard guard, or Option C hold decision. The R2 sourcefree tests do not discharge that gate.
- F1.1 remains blocked on independently reviewed RP0-R2, competent C9/C12 storage-owner schema/readset/fork approval, and the separate source/owner decisions. F0-R2 acceptance for sourcefree code does not start F1.1.

## 5. Re-review criteria

A later F0-R2 code re-review can move from `REVISE_PRECISE` to `ACCEPT_SCOPED` only after:

1. The canonical binding loader rejects a preloaded/different-path/no-`__file__` binding before any S49/G18 execution, with a fresh subprocess marker test.
2. The R30A vendor/S39 execution is either covered by the manifest or explicitly declared and prevented/handled as a trust-entry seam; no remaining “full R30A” claim is unsupported.
3. Empty/truncated manifests refuse with an expected-count/required-path check.
4. External `log_dir` cannot raise after a completed subprocess; no paid call is required to test it.
5. Account transport/receipt semantics are truthful; real provider/entitlement remains `NOT_RUN`.
6. Root and `/tmp` 58 + 21 still pass; hash receipts remain exact; no paid/native execution is introduced.
7. Historical branch/extra-file custody and C12 owner gates remain explicitly separate and unresolved.

The correct next action is a bounded sourcefree repair by the R2 author, followed by a distinct independent re-review. The reviewer does not merge, adopt, issue native rights, or run a paid model.

**Final reviewer remote SHA:** reported after the three-file commit and remote readback; this file does not self-embed the commit SHA.
