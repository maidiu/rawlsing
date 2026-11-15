# Manifest scope

`FILE_MANIFEST_SHA256.csv` covers every file supplied in `R1_20260825/` except:
- the manifest file itself;
- the future post-install `provenance/INSTALL_RECEIPT.json`, which Codex creates only after Git commit/validation metadata are known.

No supplied payload file may be silently omitted, regenerated, reformatted, or normalized during installation.
