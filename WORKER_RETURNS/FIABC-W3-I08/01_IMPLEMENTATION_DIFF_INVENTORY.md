# FIABC-W3-I08 — Implementation / Diff Inventory

Base: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`

## Production delta

### `rawlsing_next/fiabc_p2_terminal_verifier.py`

Adds one verification-only current contract for IMP13.

Key behavior:

- exact admitted cell closure;
- explicit succession-preflight PASS receipt consumption;
- explicit independent-oracle PASS/independence/freeze receipt consumption;
- source-local expected C11, I03 and I05 identities supplied by the oracle;
- mandatory C11 and I03 intermediate checks;
- mandatory full I05 learned empirical product terminal;
- complete declared-frontier coverage check;
- exact constituent-I03 fact closure;
- exact semantic/replay/output and source/workload/authority/frontier/product identities;
- typed-state noncollapse;
- exact lifecycle terminal-identity reproduction;
- deterministic PASS/BLOCK receipt with stable verification identity.

No existing semantic owner, authority producer, empirical query/discovery producer, candidate implementation, measurement implementation, HQ handoff or decision ledger is modified.

## Test delta

### `rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py`

Adds 12 focused deterministic unit tests covering:

1. full two-source/six-cell PASS;
2. C11-only false terminal rejection;
3. I03-only false terminal rejection;
4. partial I05 coverage rejection;
5. admitted-cell omission rejection;
6. succession-preflight non-PASS rejection;
7. independent-oracle causal/neutrality rejection;
8. pairwise-agreement-without-complete-oracle-match rejection;
9. constituent-I03 closure rejection;
10. semantic/replay/output identity drift rejection;
11. typed-state collapse rejection;
12. lifecycle terminal identity drift and typed nonqualification rejection (separate tests; total test functions: 13).

## Return package

- `WORKER_RETURNS/FIABC-W3-I08/00_RETURN.md`
- `WORKER_RETURNS/FIABC-W3-I08/01_IMPLEMENTATION_DIFF_INVENTORY.md`
- `WORKER_RETURNS/FIABC-W3-I08/02_TESTS_AND_COMMANDS.md`
- `WORKER_RETURNS/FIABC-W3-I08/03_TERMINAL_VERIFIER_CONTRACT.md`
- `WORKER_RETURNS/FIABC-W3-I08/RETURN.json`
