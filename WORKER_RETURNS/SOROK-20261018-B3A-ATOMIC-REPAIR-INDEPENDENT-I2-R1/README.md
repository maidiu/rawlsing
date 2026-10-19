# Independent B3A atomicity court

Read `00_RETURN.md` for the scoped verdict and `02_REQUIREMENTS_AND_LIMITATIONS.md` for owner boundaries. This return contains no candidate repairs. `inputs/b3a/` is an exact byte copy of the source and historical receipts at candidate commit `8bd4d6b01fd402e7e6a8d07903f2c3cada837f55`. Historical input receipts are not counted as independent execution. New executions are under `evidence/`.

`preregistration.json` freezes the 20-case reviewer court before its first execution. `preregistration_seeded.json` freezes four additional assertions, executed against original and repaired imports in separate processes. The early single-case schema trial is a subset of the 20, not another independent case. All failed assertions remain failures.

## Reproduction

Use a new checkout/worktree of this return with the existing authorized Git object store and Python 3.11+, pytest, Node, Git, SQLite, POSIX signals and fcntl. No package installation or model API is required. Keep new outputs separate from the returned evidence.

From this return directory in a new disposable checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 prepare_review.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_inputs.py
PYTHONDONTWRITEBYTECODE=1 python3 run_review.py --hostiles
PYTHONDONTWRITEBYTECODE=1 python3 run_review.py --seeded
PYTHONDONTWRITEBYTECODE=1 python3 run_review.py
```

The driver records and accepts expected nonzero pytest exits, preserving literal REDs. `prepare_review.py` refuses to overwrite an existing reviewer runtime. It rehydrates pinned source and fixtures, never an author database. Its transport materializer uses exact Git objects and the common store, so Git objects for every source pin must be available. It does not fetch new architecture revisions.

The exact individual commands and nested inherited commands used in this execution are in `evidence/commands.json`, `evidence/inherited/commands.json` and `evidence/inherited/b2_execution_receipt.json`. Portable path markers replace host paths. `run_review.py` gained its `--seeded` convenience option after the first supplemental execution; the actual initial supplemental command is equivalent and the frozen tests were not altered. The initial source audit had two bookkeeping errors (archive records have no commit field, and the two-file claim applies to Python files); both were corrected without changing any source or test expectation. The final privacy audit also initially matched its own regex literal as a home path; restricting the username grammar corrected that scanner false positive.

`verify_inputs.py` checks 228 Git/archive preimages and the two modified candidate Python files. The 509-file input transport manifest additionally binds every archived source/receipt byte. `evidence/loaded_modules.json` binds actual imported source paths and hashes. `artifact_manifest.json` inventories the review artifacts; `return_manifest.json` supplies the scoped return beacon. No root beacon or canonical control file is changed.
