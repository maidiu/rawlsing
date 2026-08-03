# Exact implementation sequence

Execute in this order. Do not parallelize contract changes before the preceding gate passes.

## 1. Baseline capture

- Checkout the packaged commit.
- Record `git status`, commit, Python, Pandas, PyArrow, PostgreSQL client versions.
- Run parent package and Section 85 verification.
- Copy test returns into Section 86 logs.

## 2. Storage path additions

Modify `ddm_v550_storage.V550ShardPaths` additively:

```text
respondent_substrate
```

pointing to:

```text
<shard>/checkpoints/respondent_substrate
```

Ensure `ensure()` creates it. Do not alter existing checkpoint paths.

## 3. Neutral schema/helper module

Create the neutral shared-substrate module and tests before touching the shard runner.

Gate:

- canonicalization deterministic;
- logical hash order-independent;
- multiplicity-sensitive;
- atomic writer refuses incomplete validation;
- loader refuses missing `COMPLETE`.

## 4. Registry requirement resolver

Implement a pure function that accepts:

```text
base question rows
governed registry
source/wave/country
optional selected configuration IDs
```

and returns:

```text
base rows
joint requirement rows
union extraction rows
selection audit
```

The resolver must not access PostgreSQL.

Gate it using all nine Section 85 registries.

## 5. Response authority union

Refactor response-option-map filtering and matching so it covers the union extraction set while retaining separate base and joint audit counts.

No joint-required item may enter the substrate without exact response authority or an explicit governed missingness-only rule.

## 6. Shard-runner integration

Integrate in the order:

1. parse new CLI;
2. resolve selection surfaces;
3. check for exact reusable substrate;
4. only then connect/query if necessary;
5. prepare cache once;
6. persist substrate;
7. run ordinary base loop;
8. optionally invoke V550J.

Add structured progress labels; do not log respondent values.

## 7. V550J explicit substrate path

Implement explicit path and no-DB gates. Add tests that monkeypatch all database connection functions to raise if touched; the no-DB path must still pass.

## 8. Orchestrator propagation

Add argument forwarding and plan metadata to shard launcher and smoke runner. Plan-only tests must prove exact command construction.

## 9. Resume and recovery refactor

Implement cache-first resolution in shard runner and recovery scripts. Add query-counter assertions.

## 10. Synthetic integration fixture

Create a tiny deterministic fixture. Do not use the nine-source archive's aggregate tables as respondent rows.

## 11. Full test matrix

Run unit, integration, mutation, legacy regression, Section 85 reproduction, and package portability tests.

## 12. Freeze

Commit, bundle, package, fresh-extract, clone, and rerun all static/synthetic gates from the package alone.
