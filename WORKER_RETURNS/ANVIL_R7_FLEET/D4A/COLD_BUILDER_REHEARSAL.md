# D4A — COLD BUILDER REHEARSAL

**Scope:** instrument/build-readiness rehearsal only. No native survey run, no owner/science/actor/H1 receiving. The product base is exact `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`; the cold archive was extracted with `git archive` and did not use any author worktree path.

## 1. Current consumer (present-hard)

**Exact ABI.** `rawlsing_next/pre553_empirical_query.py::execute_empirical_query` is keyword-only:

```python
execute_empirical_query(
    *, repository: C11Repository, query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate, authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
    group_scope: I03GroupedExecutionScope | None = None,
) -> QueryExecutionResult
```

The accepted repository is `C11Repository` or the exact verified `DirectEstateI03Session`; grouped sessions are presently refused for the cold sourcefree estate. It raises typed errors on identity/hash tampering and returns typed `EmpiricalFact`/negative results for lawful nonpositive outcomes.

**Cold command actually run:**

```bash
TMP=$(mktemp -d)
git archive cea2d4d3009e9087d2267e9d1f53bec28b730dc7 rawlsing_next | tar -x -C "$TMP"
PYTHONPATH="$TMP" python3 - <<'PY'
from rawlsing_next.pre553_empirical_query import execute_empirical_query
try:
    execute_empirical_query(repository=None, query=None, predicate=None,
                            authority_registry=None, release_refs=())
except Exception as e:
    print(type(e).__name__ + ':', e)
PY
```

**Actual result:**

```text
EmpiricalQueryExecutionError: repository must be accepted I02 C11Repository or exact verified S2-C I03 session
```

**First fail.** The cold import succeeds from exact product bytes (`import ok`, 178 package entries). The first actual first-reader call fails closed because no accepted `C11Repository`/verified `DirectEstateI03Session`, exact release refs, or authority registry is present in this bounded return. This is `SPECIFICATION_CONSTRUCTION_READY` at best; it is **not** `EXECUTED_FIRST_READER_PROOF`.

**Rights/ABI conditions.** Native survey source rights are not granted; the product base is sourcefree code. An actual first-reader receipt would need an executable `python3 ...`/unittest argv, a raw log with SHA-256, a stdout hash, a runner code head, and the exact source/fixture SHA. A JSON receipt without those is rejected by the guarded gate (attack A11).

## 2. Future owner-held consumer

**Exact ABI.** `rawlsing_next/sorok_history/admission.py::evaluate(packet: dict, candidate: dict) -> dict` returns `SOROK_HISTORY_ADMISSION_RESULT@1` with `status`, accepted/held/rejected groups and `result_digest`. Its owner is SOROK actor/consent/development; it is not PYAT evidence and not a C11 writer.

**Cold command actually run:**

```bash
TMP=$(mktemp -d)
git archive cea2d4d3009e9087d2267e9d1f53bec28b730dc7 rawlsing_next | tar -x -C "$TMP"
PYTHONPATH="$TMP" python3 - <<'PY'
from rawlsing_next.sorok_history.admission import evaluate
print(evaluate({}, {}))
PY
```

**Actual result (abridged):**

```text
{'schema': 'SOROK_HISTORY_ADMISSION_RESULT@1', 'request_id': None, 'status': 'REJECTED',
 'rejected': [{'status': 'REJECTED', 'reason': 'INVALID_REQUEST_ID', ...}],
 'result_digest': '9bcebe2ece02ce9f494195d92369c7b16448eb98474f756df6c98c1970b96290'}
```

**First fail.** `INVALID_REQUEST_ID`: there is no owner-held, admitted actor/world request packet. The future card is `EXACT_BUILDER_HOLD`, not a claim that SOROK can already receive. No actor access, perception, knowledge, motive or world mutation is granted.

## 3. Builder-card acceptance rule used by the private repair

A `CURRENT_FIRST_CONSUMER` or `FUTURE_NONPRECLUSION` card must:

- name an executable `path::symbol` first consumer (a filename alone is rejected);
- pin producer/consumer symbols to exact source bytes and a Git head;
- provide a permitted `python3 -m unittest ...` or `python3 tools/...` test command;
- for `EXECUTED_FIRST_READER_PROOF`, provide an `ANVIL_R7_EXECUTION_TEST_RECEIPT` with argv, exit code, raw log path/SHA, stdout SHA, host/time and runner head.

Both cards in this return are deliberately `EXACT_BUILDER_HOLD`. That is honest but **cannot** support a `C_CONDITIONALLY_ADMIT_DESIGN` verdict with a current-card hold.
