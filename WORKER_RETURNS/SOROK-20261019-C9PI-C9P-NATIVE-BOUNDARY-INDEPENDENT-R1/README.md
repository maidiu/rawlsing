# C9PI review packet

Read `00_RETURN.md` for the **REVISE / native HOLD** verdict. The executed new courts retain 29 substantive assertion REDs. Passing this packet's reproduction driver means it reproduces those REDs and scoped positives; it does not turn the candidate green or accept native actor science.

From the repository root:

```sh
python3 WORKER_RETURNS/SOROK-20261019-C9PI-C9P-NATIVE-BOUNDARY-INDEPENDENT-R1/run_review.py
```

Requires Python 3.11+ and pytest (observed 3.11.3 / 9.1.1), standard-library SQLite/subprocess, and Git for the original native custody helper. No package installation, network fetch, model API, source survey or production database is required by the replay. The frozen exact source closure is included. `stage_review.py` and `collect_authorities.py` document original Git-object acquisition; replay uses frozen preimages and does not regenerate the commission or authority artifacts.

The driver creates only `runs/` and generated evidence inside this packet. `runs/` is disposable and ignored. `prepare_runtime.py` restores exact C9P sources into a repository-shaped runtime with the original relative test/proof paths, three native namespace-package modules, and separate reviewer tests. It does not alter owner terrain. `probe_closure.py` verifies all runtime candidate/native bytes and original test/evidence identities against the frozen source. Runtime `__file__` values are verified under the dedicated runtime; portable receipts retain relative paths and a digest of the observed absolute path. Personal host prefixes in generated logs are normalized to `<RETURN_ROOT>`/`<REPO_ROOT>`; frozen source bytes are never normalized.

For raw independent assertions, run inside the created `runs/runtime`:

```sh
python3 -B -m pytest -q -p no:cacheprovider review/test_hostile.py
python3 -B -m pytest -q -p no:cacheprovider review/test_record_custody.py
python3 -B -m pytest -q -p no:cacheprovider review/test_edges.py
```

The first two commands return **1** because the retained boundary requirements fail (26 and 3 assertion failures). The last returns **0** for six narrowly technical controls. The unchanged author suite is at `WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1/tests` inside that runtime and returns 0 for 90 authored checks. Do not run the author's nonportable `/tmp/proof_integrity_gate_r1.py` wrapper; this packet carries the exact shared checker blob and runs its unchanged contracts with the qualified local path.

`run_faults.py` runs the original six plus five reviewer faults, retaining positive/fault/restored JUnit and hashes; `--extra-consumer` appends the other two original proof claims. `run_shared_gate.py` executes the exact shared checker over all original eight and reviewer five claims. Mutations are sequential, exact-text, confined to disposable source copies and restored in `finally`. Run the full driver in a dedicated runtime, not concurrently with another process mutating these copies. Original signature/import paths remain intact.

`cold_replay.py` builds and cold-inspects two TEST_ONLY SQLite databases in four fresh interpreters, comparing full table snapshots and read receipts. It establishes deterministic logical replay, not source truth, schema-wide concurrency protection, native action or power-loss durability.

Key receipts: `evidence/court_summary.json`; `evidence/fault_trials.json`; `evidence/actual_imports.json`; `evidence/shared_*.json`; `evidence/cold_replay.json`; `custody/source_preimages.json`; `custody/native_sources.json`; `custody/authority_preimages.json`; preregistration hashes and reviewer test preimages. `evidence/fault_setup_attempt*` preserves an uncredited reviewer temporary-directory setup mistake. Those errors must not be counted as candidate REDs or successful fault witnesses.

Native holds, LIFE1 native deferrals, accepted B3AS scope, no-repair/no-issuance and reviewer separation are recorded in the return. This packet does not commission a repair or further reviewer.
