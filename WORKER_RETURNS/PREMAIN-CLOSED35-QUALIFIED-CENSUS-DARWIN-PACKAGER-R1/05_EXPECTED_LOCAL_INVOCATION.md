# Expected Local Invocation

Run from a **clean checkout** of:

`agent/rabochii-premain-closed35-qualified-representation-census-harness-r1`

at exact HEAD:

`efe8de2b032c93d1820fd3f8c82fe2f1acabbf87`

The wrapper verifies that condition itself and also verifies the qualified implementation ancestry, Darwin/x86_64, CPython 3.11.3, pyreadstat 1.3.6, and pyarrow 25.0.1 before staging any source bytes.

## One command

Replace only the three carrier paths:

```bash
git fetch --no-tags origin agent/rabochii-premain-closed35-qualified-census-darwin-packager-r1 && P="$(git rev-parse FETCH_HEAD)" && CLOSED35_PACKAGER_REF="$P" bash <(git show "$P":WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-CENSUS-DARWIN-PACKAGER-R1/01_RUN_CLOSED35_AUTHORITATIVE_CENSUS.sh) "/path/to/surveys.zip" "/path/to/LITS-2006-data.dta" "/path/to/WVS Wave 7.sav.zip"
```

That single invocation:

1. pins and materializes the packager helpers;
2. fetches the exact source-estate commit only if the local repository lacks that Git object;
3. verifies the three carrier roots;
4. stages exactly 35 canonical source files outside Git;
5. writes `CLOSED35_SOURCE_PATH_MANIFEST@1.0.0`;
6. invokes the frozen qualified census harness;
7. requires exactly 35 immutable per-source receipts plus all six aggregates;
8. prints the local post-run receipt-commit command.

The deterministic default work root is:

`$HOME/Library/Caches/Rawlsing/closed35-qualified-census-r1`

To place the work root elsewhere, set `RAWLSING_CLOSED35_RUN_ROOT` before invoking the same wrapper. Changing the work root does not relax any source/runtime/head gate.

## After the census

The wrapper prints a command equivalent to:

```bash
bash "$HOME/Library/Caches/Rawlsing/closed35-qualified-census-r1/package/03_POSTRUN_RECEIPT_COMMIT.sh" "$HOME/Library/Caches/Rawlsing/closed35-qualified-census-r1/census_output"
```

That helper creates/updates only the local branch:

`agent/rabochii-premain-closed35-qualified-representation-census-results-r1`

and commits only the 35 source receipts plus six aggregate outputs. It does **not** push.
