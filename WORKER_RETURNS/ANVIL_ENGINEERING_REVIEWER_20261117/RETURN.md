# ANVIL CUT1 — independent G5 return

## Verdict

**`ACCEPT_SCOPED_PREPARED_SAVED_BATCH_CUT1`**

Sourcefree TEST_ONLY engineering acceptance of the exact prepared saved Batch
cut.

- Baseline: `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`
- Code/test: `a13d69cf5636de5541660cd60115f8b61d66261b`
- Combined candidate: `347baec696c8b395d750ac3b9e74417a6490c223`
- Owner ACK: `a744a5a4e4bb31ba9e93a650c7200c064d4d2e11`
- Integration: **UNMERGED**

The implementation adds only the owner-authorized exact prepared dispatch in
`pre553_saved_workload_integration.py`, the exact prepared class guard in
`pre553_batch_runner.py`, and the new focused test. Prepared, base admission,
writer, schema, native evaluator, issuer, normal/resume and prior tests remain
read-only.

## Actual execution evidence

- New focused 5: **5 passed in 5.56 s**
- Author 70-node scoped boundary: **70 passed in 31.34 s**
- Four distinct selected/F2/F4/raw operations through prepared Batch:
  **4 COMPLETED receipts, one DirectEstateI03Session._build**
- Actual prepared Batch I05: **1 discovery receipt, one build, exact one-shot refs**
- Prepared vs plain saved receipt material and summary: **equal**
- Actual receipt-boundary revocation: after first completed receipt, observed
  `COMPLETED, FAILED, FAILED, FAILED`; `execute_saved_batch` raised a CURRENT
  refusal; no positive return and the context closed
- Evil prepared subclass refused; wrong release and changed manifest refused
- Actual source-builder and `C11Repository.__init__` counter: **0/0** across the
  four-operation prepared Batch

## Resource observation

Small sourcefree fixture: 8 respondents, 3 questions, 4 operations.

- 4 COMPLETED Batch receipts; 1 prepared index build; 4 output refs
- Wall `0.164410677 s`
- Parent max RSS `110,874,624 B`
- Estate/root `783,936 B`
- Single process; no subprocess
- CPU, peak staging and process-tree increment were **not measured**
- 100k/6 GiB **NOT_RUN**

The author probe's `source_reads=0/full_c11_builds=0` fields are hardcoded; our
independent counter confirms 0/0 for the actual prepared path. The small parent
RSS includes fixture construction and is not an economic claim.

## Accuracy notes

- Author parent RSS was `104,222,720 B`; our independent rerun observed
  `110,874,624 B`. This is a run/fixture-parent variation, not a code delta.
- The implementer return contains a historical "stops before implementation"
  section followed by an appended implementation section. The immutable
  receipt/ACK/code/test/candidate pins control; this is a documentation-phase
  residue, not a product change.
- No full 202 matrix, original35 source, native 100k, production CURRENT,
  protected merge or #998/#1009 integration is claimed.

## Grades

- Code/engineering: **ACCEPT_SCOPED** at sourcefree TEST_ONLY cut1.
- Science: **NO_ORIGINAL35_SCIENTIFIC_ACCEPTANCE**.
- Authority: **NO_NEW_SOURCE_CURRENT_ISSUER_HOST_OR_MERGE_GRANT**.
- Protected: untouched / **UNMERGED**.
- K3/29 mappings, 26 NOT_ADOPTED, 14 HELD, F26 exact-caller holds are preserved
  and not silently re-adjudicated.

## Artifact

- `REVIEW_VERDICT.json`
- `evidence/anvil_new_5.txt`
- `evidence/anvil_70.txt`
- `evidence/prepared_i05_witness.json/.out`
- `evidence/prepared_batch_receipt_parity.json/.out`
- `evidence/receipt_boundary_witness.json/.out`
- `evidence/counter_witness.json/.out`
- `evidence/anvil_resource_probe_recheck.out`
- `evidence/SOURCE_CHECKS.tsv`
- `evidence/commands.txt`
- `MANIFEST.sha256`

**STOP: cut1 sourcefree code acceptance; no author repair/self-extension.**

## Additional preservation

- S2-A/C semantic selector and direct reader preservation: **57 passed in 5.90 s**
- S2-D saved-reader preservation: **31 passed in 13.79 s**

These cover the retained repeated/ranked/UNKNOWN/zero/None/empty, changed/
restore and saved-reader boundaries relevant to the cut1 Batch change. No full
202-matrix claim is made.

## Remote verification

Review content commit `d9818f81670cec898391a76b8ac60d8a811eb2fd` was pushed to
`origin/agent/anvil-engineering-cut1-g5-20261117-r1`. Direct remote verification
found the product tree unchanged from candidate `347baec6` and the remote verdict
valid. See `evidence/remote_verification.txt`.
