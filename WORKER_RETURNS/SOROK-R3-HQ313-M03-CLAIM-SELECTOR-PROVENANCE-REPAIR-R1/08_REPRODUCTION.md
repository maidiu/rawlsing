# Reproduce the bounded return

Use an authorized local Git worktree with the pinned commits available. Python and pytest are required; no source data, model/API call or production runtime is needed. All commands below run from the repository root and write only inside the assigned return. The supplied evidence records the completed executions; rerunning deliberately replaces those generated presentations.

On a clean runtime (the ignored `runtime/` directory must be absent), reconstruct authenticated sources:

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/stage.py
```

The optional sole argument to `stage.py` is an existing verified M02 return directory for warm static reuse. It verifies the prior runtime marker and every imported source blob, then verifies the M01 code against Git. It does not reuse mutable owner process state. Without that argument it runs the exact pinned inherited reconstruction. The original sources remain frozen in Git and in an ignored local snapshot before the candidate overlay.

Reproduce the unchanged baseline first:

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/run.py before original_413
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/run.py before independent_100
```

Expected baseline is 413 PASS, then 98 PASS / 2 FAIL. The second wrapper succeeds only if the real child pytest exits 1 with exactly those two failures and no errors/skips; it preserves the genuine child exit in `command.json`. Do not interpret its wrapper exit as 100 PASS.

Install the owned source patch and execute all final controls:

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/install_candidate.py
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/run.py after original_413
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/run.py after independent_100
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/run_author.py
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/run_historical.py
python3 WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/audit.py
```

Expected final counts are 413 PASS + 100 PASS + 74 author PASS, with nine separate historical FAILs. Historical wrapper success means its exact pytest child returned 1 with nine literal failures; raw exit/counts are recorded. Final audit reads actual JUnit case identities and saved native states, verifies literal test/expectation and import bytes, compares all 36 arms, sanitizes exported metadata and checks write scope. It issues no semantic or production acceptance.

The pinned original M02 `audit.py` must not be used as the M03 final auditor: it correctly describes the unchanged M02 baseline and expects 98/2 plus the original cell blob. M03's explicit candidate overlay intentionally changes that source. No frozen test, expectation or owner-law file is edited to accommodate it.

`runtime/` is excluded from Git. Source/grant hashes are content and Git-blob identities, not signed remote attestation. Portable XML/stdout copies change path and hostname presentation only; original experiment assertions and outcome counts remain intact. The final remote SHA is verified with direct `git ls-remote` against the assigned branch after pushing, and reported outside the hash's own tree.
