# SR03 — 35-SOURCE NATIVE METADATA DUMB EXECUTOR — REVISION 3

Repository: `maidiu/rawlsing`
Frozen parent machine: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ in the launch command. Verify it before execution; do not substitute `latest` or another branch.

MISSION: Run the checked-in `SR03_SOURCE_NATIVE_METADATA_PROBE.py` over the exact 35-source byte inventory. Produce manifests only. Do not normalize, infer, repair, ingest, or write Postgres/C11.

## Revision-3 compatibility ruling

Earlier SR03 attempts exposed pyreadstat decoding/chunk-reader incompatibilities on a bounded legacy-source set. HQ has frozen an exact compatibility-execution allowlist in `10_FORMAT_DECODER_CONTRACT.md` and the checked-in probe.

The allowlist is exactly:

- `EVS 1999.sav`
- `EVS 2008.sav`
- `LiTS_I.dta`
- `LiTS_II.dta`
- `LiTS_III.dta`
- `LiTS_IV.dta`

Each is bound to its exact SHA-256 by `SOURCE_BYTE_INVENTORY.csv` and uses explicit `latin1` for this pyreadstat physical-census execution.

Every override has authority status:

`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

This means the override is lawful for deterministic physical extraction, but it is **not** permission to claim Latin-1 is the source's intended text encoding or to certify source semantics from compatibility-decoded labels alone. The override, reason, and authority status must be emitted into the manifest/receipt.

No source outside this exact allowlist may receive an encoding guess or fallback. If another source fails, stop and return the exact failure to HQ.

Inputs:
- checked-in `SOURCE_BYTE_INVENTORY.csv`;
- exact local raw-source directory containing all 35 hash-matched files;
- checked-in `SR03_SOURCE_NATIVE_METADATA_PROBE.py`;
- binding `10_FORMAT_DECODER_CONTRACT.md`.

Python requirements: `pyreadstat`, `pandas`.

The script deliberately uses `user_missing=True` for SAV and DTA. Do not remove it. Do not apply value formats during physical extraction. Do not add additional encoding guesses or silent fallbacks.

Required preflight:
- `git rev-parse --show-toplevel`
- `git remote -v`
- `git status -sb`
- `git rev-parse HEAD`
- verify exact HQ launch HEAD.

Set:
`ORDER_ROOT=data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION`

Execute into a fresh R3 output directory; do not resume, merge, or overwrite R1/R2 output:

`python "$ORDER_ROOT/SR03_SOURCE_NATIVE_METADATA_PROBE.py" --inventory "$ORDER_ROOT/SOURCE_BYTE_INVENTORY.csv" --source-root /Users/matthewsmith/Desktop/Rawlsing/data/Data --output-dir SR03_SOURCE_PHYSICAL_MANIFESTS_R3`

Return the complete `SR03_SOURCE_PHYSICAL_MANIFESTS_R3` directory plus:
- exact checkout HEAD;
- exact command;
- exit code;
- output byte size;
- SHA-256 of a deterministic ZIP/tar of returned manifests;
- `RECEIPT.json`;
- `SOURCE_PHYSICAL_MANIFEST_SUMMARY.csv`;
- stdout/stderr;
- `git status -sb` after execution.

Success token:
`PRE553_SR03_35_SOURCE_NATIVE_METADATA_RECEIPT_COMPLETE`

Failure is returned verbatim. Do not troubleshoot semantics or change source files. Do not commit execution output unless HQ separately orders it.
