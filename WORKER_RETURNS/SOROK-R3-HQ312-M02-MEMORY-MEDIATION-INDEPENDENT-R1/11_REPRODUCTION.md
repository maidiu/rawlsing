# Reproduction and evidence handling

Requirements: authorized local private repository Git object store, Python 3.11 and pytest. No survey file, real actor, external model or V3 execution is required. The original source closure is reconstructed from exact Git objects inside this return's ignored `runtime/`; no owner or original test file is edited.

From the repository root, let `R=WORKER_RETURNS/SOROK-R3-HQ312-M02-MEMORY-MEDIATION-INDEPENDENT-R1`.

1. In a fresh return/runtime, run `python3 "$R/repro/stage.py"`. It refuses an existing runtime, verifies original M01/predecessor sources and the unchanged earlier preregistration, and uses the original CAN3/CAN2 staging chain. Required pinned objects must already be present or fetched from their specified private source commits/branches.
2. Run `python3 "$R/repro/run_original.py"`. The unchanged M01 runner executes 94+97+89+133 tests. Expected exit 0, 413 PASS. Portable copies of exact run outputs, imports and JUnit are written under `evidence/original_413/`.
3. Run `python3 "$R/repro/run_independent.py"`. Expected exit 1: 98 PASS / 2 RED out of 100, no errors/skips. All 36 actual arm states/receipts and independent contrast records are retained. The observer uses `sys.setprofile`, not replacement response functions.
4. Run `python3 "$R/repro/run_independent.py" corroboration`. Expected exit 1: the same two REDs in another interpreter. It does not replace or suppress their assertions.
5. With `PYTHONPATH="$R/repro"`, run `python3 "$R/repro/isolate_selector.py"`. This post-RED paired experiment proves identical owner state/history with differing selected-claim response. It records observations, not a green provenance acceptance claim.
6. With that same PYTHONPATH, run `python3 "$R/repro/run_historical_nine.py"`, saving its stdout into `runtime/historical_nine_raw.log`. Expected exit 1 and all nine literal original REDs. This selects the unchanged original node IDs and does not run CAN3's entire 585. Do not call the 413 reproduction a new execution of that historical total.
7. Run `python3 "$R/repro/audit.py"`. It verifies actual suite counts, native source/import blobs, original/new freeze custody, real function traces, factorial values, complete owner-state history invariance, all-six-component epistemic-state-fixed contrasts, empty guard and scope. Audit exit 0 means the evidence matches the reported mixed PASS/RED verdict; it does not mean the candidate passed.

Use `PYTHONDONTWRITEBYTECODE=1` and `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` as the recorded commands do. The runtime marker/passport identifies a live reviewer epoch; a Git return is not itself a live process guarantee.

`evidence/initial_99/` preserves the first 96 PASS / 3 FAIL run and its exact test source. Two failures were a reviewer setup error involving provenance-derived stance IDs; the corrected native-order intervention holds the actual epistemic store fixed. The genuine future-state RED is retained. A further claim-selector falsifier and paired isolation are explicitly labelled post-result follow-ups. Neither the original independent freeze nor any M01/inherited test is rewritten.

Portable outputs normalize absolute local prefixes and remove JUnit hostname metadata. `PORTABILITY_SANITIZATION.json` records raw hashes; original raw files remain local under ignored `runtime/raw_portable/`. Numeric outcomes, test identities and failure expectations are preserved. No username, personal home path, hostname, secret or original survey data belongs in the committed packet. Literal captured traceback whitespace is retained as evidence.
