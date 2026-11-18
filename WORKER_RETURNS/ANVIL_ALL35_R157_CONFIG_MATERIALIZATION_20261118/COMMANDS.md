# Commands

From `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER`:

```bash
export PYTHONPATH=/tmp/anvil_all35_aee
python3 -B WORKER_RETURNS/ANVIL_ALL35_R157_CONFIG_MATERIALIZATION_20261118/materialize_validate_all35.py
```

The script reads exact config blobs with `git show <immutable-ref>:<path>` into a
private temporary directory, loads them through `load_source_config`, compares
the all-35 metadata pins, and removes the staging directory. It does not read
respondent/source files and writes only `CONFIG_INDEX.json`, `VALIDATION.json`,
and `NEGATIVE_EVIDENCE.json` to this owned return.
