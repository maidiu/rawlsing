# Custody, manifest and supersession

- Repair parent/candidate: `efd12b1d…`.
- Original R00E author return/evidence remain untouched at their original commit.
- Original R00V reviewer return/tests remain untouched at `140c41d6…`.
- Original author `manifest.json`: ABSENT.
- Original author `SHA256SUMS.txt`: stale `00_RETURN.md` entry; preserved as historical.
- Successor `manifest.json`: exact hashes for gate, tests, successor docs/receipts; self-excluded.
- Successor `evidence/normalized_manifest.json`: normalized file list.
- Successor `evidence/SHA256SUMS.txt`: refreshed sums; excludes itself.
- `evidence/manifest_supersession.json`: old absent/stale entries and new identities.
- No policy file, original return/evidence, reviewer return, production module or foreign branch was edited.

Manifest/sums self-reference is avoided by explicit self-exclusion; no stale self-hash is presented as current.
