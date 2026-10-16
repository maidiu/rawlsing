# Reproduce MS3

Use a new authorized isolated sparse worktree over the existing authenticated Git store. Delivered environment: Python3.11.3, pytest9.1.1, Git2.39.1. Preserve existing `staging/` before reconstruction; the stager refuses to overwrite it. All paths below are repository-relative and all writes remain in this return.

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1/repro/stage.py
python3 WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1/repro/run_courts.py before
python3 WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1/repro/install_candidate.py
python3 WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1/repro/run_courts.py after
python3 WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1/repro/run_courts.py author
python3 WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1/repro/run_courts.py extension_after
python3 WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1/repro/package_audit.py
```

The actual initial run used a Git-only95-file MS2 packet extraction, then MS2's unchanged stager to reconstruct MS1's34-file closure and nine native CAN2 files plus guard. The delivered own stager encapsulates those same steps; it was not retroactively described as the first launcher. Accepted law is staged separately; missing historical CAN2 law maps remain missing. Earlier worker runtime files are never copied.

The before run completed171 original cases and separate literal P3b before candidate implementation. New47 predictions/test bytes were then Git-frozen at650a46593fd19be2642a025c1e03bbe09583d337. The candidate wrapper/helper were installed at the original MS1 import location and exact171/P3b rerun; author47 ran in a separate fresh process. Initial target171 and author47 met their expectations first run. A later source audit found an explicitNone selector gap. Supplemental12 expectations were prospectively frozen; two v1 invocations failed in logging before assertions (12TypeErrors each). The frozen logging-only v2 keeps every assertion/expected outcome unchanged. It yielded11PASS/1scientificRED on initial source79dba9af, and12PASS after the selector fix. Final171,47 and12 were then actually run on source96b568b0. See evidence/SELECTOR_EXTENSION_HISTORY.json. Original171 and47 source/expectations never changed. The final installer was also run afterward to verify that delivered candidate bytes match the installed bytes; no differing source change or scientific rerun was introduced.

The runner records real pytest exits: before original120 child exits1 with2 failures, MS251 exits1 with8, literal P3b exits1 with1. After original120 still exits1 with2; MS251 exits0; P3b still exits1. Author47 and final supplemental12 exit0. The v2 supplemental run on initial candidate79dba9af exits1 with one scientific failure; the preserved v1 logging invocations each exit1 with12 failures before assertions. The outer orchestration saves all outcomes and finishes successfully without reclassifying failures as passes. The auditor checks the exact expected counts, source preimages, case identities and eight-RED transition ledger independently of that orchestration status. `MS3_AUDIT_OK` means consistency, not independent acceptance.

Original test files are checked directly against their pinned Git bytes before each execution. New author controls verify frozen SHA-256 before execution; after-the-fact audit also matches them to the prospective Git commit. For the optional historical supplemental probe, materialize both candidate source files from Git commit79dba9afe30844c05fa840e7b36c0d5f27765e0c into the staged import directory and run `run_courts.py extension_before`; then reinstall final candidate bytes before final courts. Original supplemental v1 remains frozen and preserved; the current runner executes logging-only v2. No inference is drawn from v1 logging failures.

Source/import receipts capture actual Python module files and Git blob hashes, separating original-before bytes from candidate-after bytes at the same staged import path. Native owners, production guard and original scientific assertions are untouched.

The original MS2 tests serialize native state/events/read/counterfactuals; each phase's observations are copied before later execution overwrites their original harness output path. Five author exception tests use temporary raising wrappers **after real native operations**, with verification shadows excluded from live-call accounting; they never supply fake productive outputs. Shadow replay source functions remain the pinned native APIs.

Raw first-run outputs are retained under ignored `staging/raw_execution/` before portable packaging. Published JUnit/stdout redacts personal path/hostname presentation only, with raw/portable digests. Original assertions, exact source bytes, synthetic native data, outcomes and scientific falsification are unchanged. The response receipt is uncommitted, both hypothetical rules UNISSUED, and sourcefree actor/model experiments remain prohibited.

Commit and push only the owned return. Verify the direct content remote SHA, then a receipt-only child and its final remote SHA outside its own tree. Do not merge into canonical code or self-accept; HQ owns the separate future MS4 review.
