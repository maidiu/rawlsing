# Custody, missing manifest and independent witness

## Candidate identity

- Candidate commit `efd12b1d…` against startup `6d95a78b…`.
- 20 candidate files reconstructed from exact Git; per-file Git blob SHA-1 and SHA-256 in `evidence/candidate_manifest_reconstruction.json`.
- Author `WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/manifest.json`: **ABSENT**.
- Author `evidence/SHA256SUMS.txt`: 25 entries, **stale** `00_RETURN.md` hash (`67a50277…` recorded vs `c03c7eb4…` actual at candidate).
- Author `evidence/proof_witness.json`: policy identity record, not a signed/mechanical run witness.

## Independent witness

`evidence/reviewer_proof_witness.json` binds:

- candidate gate SHA-256 `54c2c1e8…`;
- independently recomputed R2 policy blobs;
- reviewer replay SHA-256 and JUnit SHA-256;
- exact replay/test commands;
- 36/36 independent cases and 8 defects;
- `trusted_native_provenance=NOT_PRESENT`, `actual_consumer_values_read=null`, original grant UNISSUED.

The reviewer witness is a local mechanical test record, not a protected CI signature. Same-user filesystem custody remains a limit.

## Shared contract

`REVIEW_SHARED_START_AND_RETURN.md` and `NATIVE_SHARED_EXECUTION_CONTRACT.md` are absent at candidate/startup. No launch URL or exact external ref was supplied. Local filesystem, Git ref, and GitHub code-search attempts found no exact material. Their additional obligations remain **UNVERIFIED**, not satisfied.
