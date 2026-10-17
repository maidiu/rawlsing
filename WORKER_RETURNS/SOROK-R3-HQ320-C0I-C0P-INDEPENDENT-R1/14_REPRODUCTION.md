# Reproduction

Run from the repository root in an independent worktree with the exact source Git objects available. Set `R=WORKER_RETURNS/SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1`.

1. `PYTHONDONTWRITEBYTECODE=1 python3 "$R/repro/stage.py"` reconstructs32 exact target files,19 frozen SC0/E06/GF1 sources and29 native modules. Staging refuses to overwrite an existing target runtime. Empty namespace scaffolding is disclosed and not counted as native source.
2. `python3 "$R/repro/run.py" author49` — expected49 PASS.
3. `python3 "$R/repro/run.py" hostile` — expected47 PASS/3 literal RED. The outer runner saves the actual child exit code and returns after packaging; it does not declare all tests passed. Freeze hashes are checked before collection. No pytest conftest/plugins/cache is loaded, and importlib mode/explicit root is used.
4. `PYTHONDONTWRITEBYTECODE=1 python3 "$R/repro/observe.py"` — exact original nonparent/mother receipt hashes, source-native traces and three independent AS_OF clock contrasts.
5. `PYTHONDONTWRITEBYTECODE=1 python3 "$R/repro/pyat_audit.py"` — source/API discrepancy plus current R22 primary evidence. This does not rerun Pyat's E06I/GF1I/XSP missions; external JUnit is labeled external. E06's C0P-only import failure and the missing GF1 consumer-name probe are actual subprocesses, with full stdout/stderr.
6. `PYTHONDONTWRITEBYTECODE=1 python3 "$R/repro/audit.py"` — independently reverify all29 actual imports and Git preimages, unchanged49/frozen50/candidate bytes, full case counts and completion evidence.

The candidate facade has a hardcoded `/tmp/c0p-runtime`. Its default path binding is tested separately and fails. For other facade tests the harness loads the exact source after importing the fresh native modules, then sets only its `RUNTIME` variable to the verified runtime for producer hash reads. No older `/tmp` files are used, no candidate bytes are edited, and this does not cure the default-path RED. Both contract/envelope tests still fail after relocation.

Portable logs/JUnit normalize only the absolute worktree prefix and host name. Full failure text, counts and timings remain; raw originals are locally retained in ignored staging, with raw/portable digests in11_EVIDENCE_PORTABILITY.json. Imported module paths are return-relative aliases of actual `module.__file__` values. No personal home paths or credentials belong in the passport.

Do not insert a second world estimator, fabricate GF1's absent consumer, supply original data, issue a grant, or count oracle-JSON inspections as full K9/K10. Full K9 and the original28 upstream mutations remain NOT_RUN. The prospective freeze is72cc80eb93b4ddf55bb473db40aa3640ceb1e5b4; keep its three REDs rather than editing them to green.
