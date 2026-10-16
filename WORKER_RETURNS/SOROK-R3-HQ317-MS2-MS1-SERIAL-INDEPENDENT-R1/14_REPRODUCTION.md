# Reproduce MS2

Use an isolated sparse worktree of the assigned MS2 branch over the authenticated shared Git store. Delivered runner: Python3.11.3, pytest9.1.1, Git2.39.1. MS1 originally used pytest9.0.2; the exact case identities and results reproduced under the available reviewer version. No package installation or external provider is needed.

Run from repository root:

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1/repro/stage.py
python3 WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1/repro/run_original.py
python3 WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1/repro/run_review.py new
python3 WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1/repro/run_review.py literal_p3b
python3 WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1/repro/package_audit.py
```

Preserve any existing `staging/` before reconstruction; the stager refuses to overwrite it. The delivered initial materialization used the same Git-only34-file extraction later encapsulated by `stage.py`, followed by `stage.py verify`; it was not falsely claimed to have initially run the wrapper. The original packet includes native candidate source and published evidence. Nine native CAN2 preimages and the separate EMPTY guard match their authoritative commits exactly. Accepted-law blobs are materialized in a separate directory; the two missing original law maps are deliberately not filled in. `staging/` is ignored and all writes remain inside this return.

`run_original.py` executes the two unchanged original test files in a fresh process, records actual imports and checks EMPTY guard bytes. Its pytest child exits1 with118 PASS/2 FAIL; the wrapper exits0 after validating that exact result. The failures are not successes or xfails. It retains actual JUnit/stdout and missing-file errors.

Both reviewer files and predictions were Git-frozen at6a1e733cd92113b10ba85db4e93f13e9ef9861b5 before collection/import/execution. `run_review.py` verifies their bytes against that commit and executes fresh Python processes. The first-run new court exits1 with43 PASS/8 FAIL. The literal original P3b court exits1 with1 FAIL. These nonzero exits are the intended review evidence; do not combine commands with a shell `&&` that prevents subsequent evidence packaging. Do not repair, xfail or remove any failing assertion. No scientific rerun was needed for the delivered packet.

Each independent cell is reconstructed with actual native ADP016 formation/commit and canonical claim binding, then the original hypothetical mediator/native ADP017 operations and original consumer. Before/after owner and registry states, exact transitions and source events are serialized. Consumer reads are verified against the exact native owner hash. The auditor matches all eleven honest cell hashes/outcomes against MS1's publication and verifies original120 names/outcomes, source/test preimages, chronology, original P3b custody and native source/import hashes. `MS2_AUDIT_OK` means consistency of the evidence, including REDs; it is not an acceptance verdict.

The first-run raw execution outputs are retained in ignored host-local `staging/raw_execution/`, recovered byte-identically by reversing metadata redaction and matching recorded pre-redaction SHA-256 (see `evidence/RAW_CUSTODY_RECOVERY.json`); portable JUnit/stdout replaces personal paths/hostname metadata only. Original preregistration is copied byte-for-byte. Scientific source, assertions, observed synthetic state, decision/effect projections and failures remain unchanged. Full receipts differ with provenance even where the projected choice is equal.

Only the assigned MS2 return may be committed. Commit/push the evidence, verify the exact direct remote SHA, then publish the receipt-only child and directly verify its final SHA outside its own tree. No canonical merge, rule issuance, production registry update, model/actor call, private respondent data or V3 operation is authorized by this reproduction.
