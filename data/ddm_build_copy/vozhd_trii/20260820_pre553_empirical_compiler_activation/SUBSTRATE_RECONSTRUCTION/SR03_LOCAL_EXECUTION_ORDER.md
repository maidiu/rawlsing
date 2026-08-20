# SR03 — 35-SOURCE NATIVE METADATA DUMB EXECUTOR — REVISION 2

Repository: `maidiu/rawlsing`
Frozen parent machine: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ in the launch command. Verify it before execution; do not substitute `latest` or another branch.

MISSION: Run the checked-in `SR03_SOURCE_NATIVE_METADATA_PROBE.py` over the exact 35-source byte inventory. Produce manifests only. Do not normalize, infer, repair, ingest, or write Postgres/C11.

REVISION-2 NOTE — EVS 1999:
The exact frozen `EVS 1999.sav` (`SHA-256 6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8`) fails default pyreadstat metadata decoding with an invalid-byte-sequence error but reads under explicit `latin1`. HQ has therefore frozen an explicit source-specific reader compatibility override in the checked-in probe. This is NOT a silent fallback and must not be changed by the executor. The override and its reason are emitted into the manifest and receipt for deterministic replay.

Inputs:
- checked-in `SOURCE_BYTE_INVENTORY.csv`;
- exact local raw-source directory containing all 35 hash-matched files;
- checked-in `SR03_SOURCE_NATIVE_METADATA_PROBE.py`.

Python requirements: `pyreadstat`, `pandas`.

The script deliberately uses `user_missing=True` for both SAV and DTA. Do not remove it. Do not apply value formats during physical extraction. Do not add additional encoding guesses or silent fallbacks. If another source fails decoding, return that failure to HQ unchanged.

Required preflight:
- `git rev-parse --show-toplevel`
- `git remote -v`
- `git status -sb`
- `git rev-parse HEAD`
- verify exact HQ launch HEAD.

Set:
`ORDER_ROOT=data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION`

Execute into a fresh R2 output directory; do not merge with or overwrite the partial R1 output:
`python "$ORDER_ROOT/SR03_SOURCE_NATIVE_METADATA_PROBE.py" --inventory "$ORDER_ROOT/SOURCE_BYTE_INVENTORY.csv" --source-root /Users/matthewsmith/Desktop/Rawlsing/data/Data --output-dir SR03_SOURCE_PHYSICAL_MANIFESTS_R2`

Return the complete `SR03_SOURCE_PHYSICAL_MANIFESTS_R2` directory plus:
- exact checkout HEAD;
- exact command;
- exit code;
- output byte size;
- SHA-256 of a deterministic ZIP/tar of returned manifests;
- `RECEIPT.json`;
- stdout/stderr;
- `git status -sb` after execution.

Success token:
`PRE553_SR03_35_SOURCE_NATIVE_METADATA_RECEIPT_COMPLETE`

Failure is returned verbatim. Do not troubleshoot semantics or change source files. Do not commit execution output unless HQ separately orders it.
