Verified HEAD and a clean tree at **`812e34cd7da7ff334f8a082a3cbc94b75050766d`**, including the final code and tests. **Two blocking findings remain.**

- **[P1] Discovery measure substitution.** The measure check applies only to QUERY units at [line 108](/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq282-p01-secondary/rawlsing_next/pre553_v2_durable_consumer_integration_candidate.py:108). Changing the frozen discovery declaration from `RAW` to `GOVERNED_WEIGHTED` still returns `ok=True`, no failures, and three consumed products from actual RAW owner results. Bind discovery expectations to the executed query/fact measure; reject unsupported measures and add a regression.
- **[P1] Frozen authority is not bound to execution.** The [manifest validation](/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq282-p01-secondary/rawlsing_next/pre553_v2_durable_consumer_integration_candidate.py:92) never resolves or compares the declaration’s `authority_ref`. Replacing a query’s frozen authority with `UNRELATED-NONEXISTENT-AUTHORITY` still returns `ok=True`, no failures, and three actual owner calls under the original authority. Require the frozen authority to resolve and match the actual dispatch and owner authority closure, with a regression.

Both reproductions used unchanged owner code with in-memory substitutes for storage, journals and locks. They establish semantic defects, not durability.

The prior predicate finding is corrected: frozen/query/fact predicates are compared, fact release provenance must equal the durable unit’s exact release set, and exported evidence uses the observed predicate. All three new predicate/release regression cases passed with in-memory storage. I found no additional issue in the previously cleared locking, replan, multiplicity and typed-result safeguards.

Verification:

- Recorded logs and exit files show **164 passed, 6 explicit skips**, including **20 integrated tests**; fresh collection found 170 cases.
- Read-only pytest checks passed: **6 passed, 38 deselected**, using `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider -s`.
- Exact-object court passed: **17 pinned imports, 328 unchanged startup files**. A05’s **18 cases** passed.
- Saved frozen E, source inventory, three actual Field Forge products and replay matched fresh source-free owner recomputation.
- The durable pytest rerun could not start because the sandbox has no writable temporary directory. Its recorded passes were not independently rerun here.

Imported baseline objects remain exact pinned sources with documented direct-call limitations. External custody, source-use, scientific/model authority, REAL_EXECUTION and publication holds remain intact. **This candidate is not cleared; no scientific acceptance is claimed.**

No files were edited, committed or pushed. No real survey data was accessed.