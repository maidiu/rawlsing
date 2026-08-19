# 14 — VOZHD AUDIT & RECONCILIATION TEMPLATE

Every domain/sub-Vozhd uses this after material subordinate work and before recommending integration.

```text
AUDIT ID:
<id>

COMMAND:
<Vozhd>

CANONICAL INTEGRATION SHA:
<sha>

SUBSTRATE:
<contract id/version/hash>

SHARED CONTRACT BUNDLE:
<object/interface/DAG/reference/negative authority versions>

UNITS AUDITED:
- <worker branch/head/base>

1. AUTHORITY SYNCHRONIZATION
For each unit:
- exact authority bundle matches? YES/NO
- worker invented local semantic authority? YES/NO
- legacy implementation contradicted accepted authority? details

2. SUBSTRATE SYNCHRONIZATION
For each shared input:
- grain identical?
- identity scope identical?
- routing/risk-set interpretation identical?
- weight/measure interpretation identical?
- time semantics identical?
- absence/negative states identical?

3. INTERFACE SYNCHRONIZATION
For every producer/consumer seam:
- same interface ID/version/hash?
- same object grain?
- same identity/hash tuple?
- same cardinality/order/role?
- same negative-state behavior?
- same reference semantics?
- same forbidden inputs?

4. DAG SYNCHRONIZATION
- every used edge registered?
- any numbered transit without unique semantics?
- any unauthorized direct bypass?
- any consumer starved?
- any duplicate semantic owner?

5. SOURCE-UNIVERSE SYNCHRONIZATION
- exact universe identity preserved?
- pooling/linkage/composition authority explicit?
- same labels accidentally treated as same source/respondent?

6. ACTOR/WORLD FIREWALL
- population fact promoted to actor fact?
- structural context promoted to actor psyche/persona?
- PSEPF/comparator/replay receipt promoted to developmental prior?
- V2/app direct/indirect upstream semantic dereference?

7. REFERENCE / REPLAY
- historical authority exact?
- required immutable references resolvable?
- broken reference fails closed?
- provenance fields copied/reowned unnecessarily?

8. SEMANTIC DIFF REVIEW
For each worker:
- declared semantic diff complete?
- observed undeclared semantic diff?

9. TEST / FIXTURE REVIEW
- required canonical fixture version used?
- hostile negatives pass?
- sibling seam tests pass?
- fixtures modified without G5 authority?

10. LEGACY REUSE
For every legacy import/reuse:
- salvage classification exists?
- retained/rejected semantics explicit?
- transitional shim has retirement condition?

11. OPEN CONFLICTS
<finite list>

12. REQUIRED HARDENING
<finite list with owner>

13. STALE WORKERS
<units requiring refresh/rebase>

RESULT:
VOZHD_RECONCILED__INTEGRATION_RECOMMENDED
VOZHD_RECONCILED_WITH_NONBLOCKING_DEBT__INTEGRATION_RECOMMENDED
RETURN_FOR_HARMONIZATION
BLOCKED_SHARED_CONTRACT
BLOCKED_AUTHORITY_CONFLICT
```

A Vozhd may not issue an integration recommendation with an unresolved mismatch in substrate grain, identity, shared interface, legal DAG edge, or constitutional negative authority.
