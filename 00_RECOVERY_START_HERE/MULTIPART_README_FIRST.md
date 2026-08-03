# Rawlsing v41 Recovery — Three Independent ZIP Edition

This edition is distributed as three ordinary ZIP archives. Each archive is independently valid and openable.

## Assembly

1. Create one empty destination folder.
2. Extract ZIP 1, ZIP 2, and ZIP 3 into that same destination folder.
3. Allow identical shared control files to overwrite if prompted; their bytes are identical.
4. Open the combined package root `README_FIRST.md`.
5. Run `python verify_multipart_handoff.py` from the package root.

Do not concatenate the ZIP files.

The inherited `00_START_HERE/` controls are historical. The governing current controls are in `00_RECOVERY_START_HERE/`.

The original nested Linux runtime ZIP was replaced in this edition by its extracted contents under:

`90_RECOVERY_INPUTS/EXTRACTED_LINUX_RUNTIME_KIT/`

Original runtime-kit ZIP SHA-256:

`3949a948837c4ceeb989894f5b8e09dd0bd1fe535ce0bce8cd2ee3055e1a7c0d`

The root-level legacy `PACKAGE_INDEX.csv`, `SHA256SUMS.csv`, and `VALIDATION.json` describe the earlier single-ZIP recovery layout. The governing multipart controls are `MULTIPART_PACKAGE_INDEX.csv`, `MULTIPART_SHA256SUMS.csv`, `MULTIPART_VALIDATION.json`, and `verify_multipart_handoff.py`.
