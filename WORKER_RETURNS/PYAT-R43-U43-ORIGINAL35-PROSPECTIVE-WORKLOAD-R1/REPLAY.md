# Qualified replay

Use a new checkout of the returned branch, Python3.11 and pytest9.1.1. All original-source rights remain separate. Commands below read only committed code/metadata and literal sourcefree test fixtures. Run from the checkout root; `LOCAL_COURTS/` is ignored. Existing stages are deliberately never overwritten.

```sh
python3 -m venv LOCAL_COURTS/u43-venv
LOCAL_COURTS/u43-venv/bin/python -m pip install pytest==9.1.1 pyyaml==6.0.3
LOCAL_COURTS/u43-venv/bin/python -B WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/prepare_replay.py baseline
LOCAL_COURTS/u43-venv/bin/python -B WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/prepare_replay.py repaired
LOCAL_COURTS/u43-venv/bin/python -B WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/prepare_replay.py current-p10
LOCAL_COURTS/u43-venv/bin/python -B WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/build_frontier.py
LOCAL_COURTS/u43-venv/bin/python -B WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/handback.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 LOCAL_COURTS/u43-venv/bin/python -B -m pytest WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/tests -q
LOCAL_COURTS/u43-venv/bin/python -B WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/run_native.py
LOCAL_COURTS/u43-venv/bin/python -B WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/repro/execute_permitted.py --output current_native_manifests.json
```

For the unchanged independent65 battery, set `PYTHONPATH=repro`, `WG0L_PHASE_B_ADAPTER=u43_reviewer_transport` and `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, run pytest on `tests/test_precommitted_phase_b.py` **with working directory `LOCAL_COURTS/u43-repaired`**, using the absolute qualified interpreter path. Add the absolute U43 `tests/test_descriptor_refusal.py` path for the9 explicit early-refusal controls. The `current-p10` stage runs identically; its control transport records native physical imports and hashes. The old baseline's exact `tests/phase_b/test_additional_descriptor_binding_red.py` must produce three assertion failures. Do not relabel its intentional RED as a passing repair test.

The frozen65 assertions and original programs are byte-identical. The new reviewer transport changes only the proof of the second-frontier precommit from ambient Git HEAD to the exact frozen-file hash, enabling relocation without Git. `prepare_replay.py` shows that single transport change and the complete descriptor repair. No assertion is weakened.

For original author programs, in the repaired stage's `runtime_phase_b/candidate` directory run `repro/run_suites.py prepare_native prepare_historical_j historical_p2 historical_p3 historical_k_on_p3 historical_j ported_j ported_k wg0p4`. Inspect each actual `observations/*.terminal.json` and XML: this launcher deliberately retains old J/K REDs against old implementations. Its shell exit alone is not an all-green result.

The shared gate command is `python CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1/tests/test_issued_workload.py.proof.json --root . --receipt <new-receipt.json>` in the qualified environment. It executes positive → exact implementation mutation → named assertion RED and restores source.

`repro/cold_relocate.py` stages sourcefree code/metadata in `LOCAL_COURTS/u43-cold` without `.git`, warm owner keys or checkpoints. Run the same courts from that actual relocated root and its reviewer subdirectory, not from the original checkout. Rebuild the frontier and run native execution there; compare exact SHA256 preimages in `evidence/cold_identity_comparison.json`. The final retained metadata extension includes the frozen WG0R repaired flags. `verify_return.py` verifies retained artifacts and actual JUnit outcomes without rerunning science.
