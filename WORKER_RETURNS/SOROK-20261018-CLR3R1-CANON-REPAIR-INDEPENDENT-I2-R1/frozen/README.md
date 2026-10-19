# CLR3 independent I2 science review

Start with `00_RETURN.md`, the native-owner matrix, and `03_MINIMUM_LAWFUL_MIGRATION.md`.

**42 PASS / 8 RED across 50 cases**, zero errors/skips: unchanged CLR3 **38 PASS**, unchanged original **6 RED**, independent **4 PASS / 2 RED**. General research canon admission needs revision; native migration and whole-archive lineage remain HOLD. No adoption or semantic issuance.

From this directory, using Python 3.11:

```sh
python3 -m pip install --target .runtime -r reconstructed/clr3/requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 run_review.py
```

Expected runner exit: **1**. `run_review.py` keeps source/expectation checks, separate JUnit/logs, full-trajectory comparison and four cold-process hash-seed replays. It does not rewrite reconstructed author evidence or call native actors/models. Its final shape assertion describes observed RED evidence, not acceptance of the failing safety properties.

`reconstruct.py` re-materializes exact original Git blobs from an available shared repository object store. `acquire_authority.py` reads only exact pinned authority objects. These require authorized repository access; normal replay uses the included reconstructed closure without GitHub/network. `audit_sources.py <sourcefree-code-archive>` independently checks the 31 selected members and 65-file closure when the local archive is available. The container mismatch is an expected HOLD, never waived. Full source and import manifests plus per-suite commands/exit statuses are under `evidence/`.

The source archive itself and ignored `.runtime` packages are not published. Only selected source-code/doc members are included under `sources/`; they are audit inputs, not an alternative runtime. All original candidate files under `reconstructed/` are byte-identical to their exact Git preimages. Only the commissioned reviewer return subtree is changed.
