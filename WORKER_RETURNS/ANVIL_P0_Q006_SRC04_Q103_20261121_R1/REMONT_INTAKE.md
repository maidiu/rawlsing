# REMONT intake draft — Q006 q103

**Status:** blocked before native I03.

**Exact q103 finding:** current `SRC04.post_alignment.runtime.config.json`
does not preserve 97/98/99 separately (`97`/`98` -> DK; `99` -> substantive)
and q103 routing is `ROUTING_UNKNOWN` with an unresolved risk set. The actual
SRC04 saved-stream q103 question binding is present.

**Code boundary:** #1084 public `compile_and_issue_governed_queries_v2` is
TEST_ONLY; #1205 asked-eligible RAW is policy/fixture code, not a real
saved-stream issuer; `execute_anvil_stream_i03` has no authentic catalog/query/
predicate to consume. This is code absence at the issuer seam, distinct from the
unsettled q103 source fact.

**Smallest next input:** one SRC04 q103 source/QSM/risk authority artifact and
one authentic saved-stream q103 catalog/query/predicate. Then run exact I03 and
replay on the unchanged SRC04 release.
