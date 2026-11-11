# Preserved old baseline worker receipts

`old_baseline_worker_json.tar.zst` is a lossless zstd-compressed tar of the six
nonempty worker JSON files left by the stopped `NATIVE_W03_W04_FULLSCALE`
baseline run. The uncompressed bytes were verified file-by-file against
`old_baseline_worker_manifest.json`; the archive itself is published atomically.

The archive is **not** committed to Git because its compressed size is about
249 MiB, above the normal single-file Git host limit. The manifest is committed;
the archive and all originals remain in this worktree/state. No zero/incomplete
file is counted as completed proof.

These worker JSONs are complete worker payloads but do not carry parent-level
`cap_enforced`/method/source-head provenance. They are preserved as raw history,
not used as the fully qualified first-pair baseline.
