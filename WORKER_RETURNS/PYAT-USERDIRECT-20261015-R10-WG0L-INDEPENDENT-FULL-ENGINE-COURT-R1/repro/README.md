Phase A replay from a fresh checkout of the assigned branch:

1. `python3 <return>/repro/stage_phase_a.py` (refuses existing runtime_root; stages only exact historical commits, never WG0P4 candidate).
2. `python3 <return>/repro/run_phase_a.py author29`
3. `python3 <return>/repro/run_phase_a.py author36`
4. `python3 <return>/repro/run_phase_a.py phase_a`
5. `python3 <return>/repro/run_phase_a.py wg0k_full_historical` (expected exit1,1PASS/10FAIL on historical WG0P3).
6. Run capture_environment.py with PYTHONPATH containing runtime_root, runtime_root/WG0P2/repro and runtime_root/WG0P3/repro. This captures exact imported files/hashes, actual historical owner calls and canonical fact projections.

`freeze_expectations.py` documents independent derivation but refuses overwriting the original frozen oracle. Do not rerun it over the precommitted oracle. Original WG0J and WG0K copies and their hashes must remain unchanged.

`tests/test_precommitted_phase_b.py` collects65 candidate-neutral acceptance cases. No candidate adapter is selected by default, so executing that suite before a published candidate deliberately errors rather than fabricating results or skipping acceptance. Phase B must provide an explicitly versioned adapter via WG0L_PHASE_B_ADAPTER, with pinned candidate SHA, actual source files/calls and raw outcome evidence. The adapter transports APIs/evidence only; scientific assertions remain in the frozen contract and oracle. Source-specific stimulus choices and any interface mapping must be recorded alongside it. All original44 WG0J cases and original tests remain immutable and separately accountable.

The owner_cold_rehearsal script uses real accepted UnitExecutionReceipt and original manifest in fresh processes. Its own JSON fact restoration is labelled REVIEWER HARNESS, not WG0P4 candidate code, independent grant verification or semantic adoption. Actual candidate recovery/currentness is still Phase B.
