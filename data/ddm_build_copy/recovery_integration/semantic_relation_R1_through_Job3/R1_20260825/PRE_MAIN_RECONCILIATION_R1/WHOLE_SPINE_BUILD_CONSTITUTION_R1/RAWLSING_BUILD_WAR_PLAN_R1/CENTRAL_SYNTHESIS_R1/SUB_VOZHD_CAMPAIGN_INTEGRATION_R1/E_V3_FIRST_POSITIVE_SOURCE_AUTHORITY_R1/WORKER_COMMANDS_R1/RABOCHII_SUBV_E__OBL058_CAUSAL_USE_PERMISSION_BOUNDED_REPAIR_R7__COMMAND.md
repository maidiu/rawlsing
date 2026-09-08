# RABOCHII SUB-VOZHD E — OBL058 CAUSAL_USE_PERMISSION — BOUNDED REPAIR R7 COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E1 / OBL058 — CAUSAL_USE_PERMISSION R7 OBJECT-GENERATION RETIREMENT REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r7`

EXACT STARTING HEAD:
`6ba1dccef96d4de93c66b48c267d46d9e40920e6`

FAILED FROZEN R6 CANDIDATE:
`92418a9e13f55464a91c1c9f1deb96977bc294ef`

R6 REVIEW RECOMMENDATION:
`FAIL__OBL058_R6_INDEPENDENT_REVIEW__STALE_OBJECT_RECORD_RETIREMENT_NOT_INVARIANT`

SMALLEST BLOCKER:
`BLOCKER__OBL058_R6_OBJECT_RECORD_RETIREMENT_DEPENDS_ON_CALLER_DETACHABLE_WEAKREF_FINALIZER`

This is a repair-only continuation. Do not modify the frozen R6 candidate in place. Produce a new frozen R7 candidate.

## Read first

Read and obey the SUB-VOZHD E campaign charter, inter-campaign orchestration law, all OBL058 R1–R6 candidate/court/review/repair returns needed to understand the lane, the R6 independent review return at `6ba1dccef96d4de93c66b48c267d46d9e40920e6`, and the current SUB-VOZHD E adjudication from its immutable campaign ref supplied prospectively with this command.

## Exact repair objective

Close only the remaining object-generation retirement defect.

R6 correctly binds broker authority to requester PID/UID/process-start generation and rejects forked process-local copies. Its remaining weakness is that retirement of the broker record after object release depends on an ordinary `weakref.finalize` registration that can be detached from the inspectable Python surface.

R7 must ensure that a source-issued object ID cannot become a stale authoritative record after the source-issued object generation has ceased.

At minimum:

1. detaching or clearing ordinary weak-reference finalizer registrations must not leave a stale authoritative broker record usable by a later object generation;
2. if the design prevents the issued object generation from ceasing while broker authority is live, that lifetime reservation must not itself be caller-removable through the declared ordinary Python inspection surface;
3. explicit `close()` may retire broker authority, but after close the object identity must not become a path to positive validation even if the Python object remains alive for address-reservation purposes;
4. a later same-process object generation must not inherit authority from an earlier receipt merely because CPython reuses an integer address;
5. R6 fork/process-generation rejection must remain exact;
6. ordinary same-process repeated and concurrent validation of a live issued receipt must remain functional.

Architecture selection remains with the worker. Do not rely on leading underscores, hidden naming, caller-cooperative cleanup, or ordinary mutable callback registries as authority boundaries.

## Preservation law

Preserve the R6 controls independently confirmed correct:

- genuine broker endpoint/PID/UID/start-time verification;
- requester process-generation enforcement derived from OS-observed peer state;
- unrelated same-user endpoint replacement rejection;
- broker-death and authority-child-death fail-closed behavior;
- one-shot source-owned scope/basis/fixture decision;
- no caller-built authoritative-body injection;
- exact actor/world/subject/time/transition binding;
- field-specific `NONCURRENT_SYNTHETIC` namespace enforcement;
- exact current first-canary and project-current-shaped identity rejection;
- one frozen source-owned positive basis and unregistered-basis `DENY`;
- exact authority/schema/fixture/scope/basis-proof/authority-instance/content-integrity checks;
- constructor, `object.__new__`, subclass, Mapping/proxy, JSON reconstruction, copy/deepcopy and serialization rejection on ordinary paths;
- cross-scope and cross-receipt reuse rejection;
- stable repeated/concurrent validation;
- denial of classification/routing/occurrence/proximity/narrative-like surrogate permission;
- no public source-basis registration surface;
- no project-current effect.

Do not widen source-owner jurisdiction or enter OBL059/OBL060, comparator, PSEPF, OBL032, architecture/topology, sibling-campaign, or project-current semantics.

## Governed R7 court requirements

Freeze the new R7 candidate before governed evidence execution. The producer court must include direct regressions for the R6 review blocker and preservation controls, including at minimum:

- detachment/clearing of any ordinary `weakref.finalize` registration must not create a stale authoritative record;
- release of caller references followed by forced collection must either retire authority or prove the exact issued object generation remains source-owned/live and non-reusable;
- explicit close followed by validation must fail closed;
- duplicate close must be idempotent or fail closed without re-authorizing;
- forked copies of genuine `PERMIT` and `DENY` remain rejected;
- child-process close cannot retire the parent record;
- parent remains valid after child rejection;
- caller-supplied requester identity fields remain rejected;
- same-process repeated and concurrent validation remains stable;
- multiple receipts with equal semantic content remain distinct by authority-instance identity;
- cross-receipt, cross-scope and cross-module reuse remain rejected;
- exact-type fabrication, copy/proxy/reconstruction/serialization remain rejected;
- broker endpoint replacement, broker death and authority-child death remain fail closed;
- valid synthetic `PERMIT` and `DENY` controls remain functional;
- all basis/scope/fixture/current-boundary controls remain exact;
- no project-current permission, current-positive OBL056, OBL055 execution, ENCOUNTER, or OEE path exists.

Record exact candidate, tests, governed evidence execution, run, job, artifact, ZIP SHA-256, and court terminal.

## Separation of duties

`INDEPENDENT_REVIEW_PERFORMED_BY_R7_REPAIR_WORKER = NO`

Do not commission, perform, or claim the fresh independent review of the R7 candidate. If the producer court is green, return to SUB-VOZHD E. SUB-VOZHD E alone will commission exactly one fresh distinct reviewer against the new frozen R7 candidate.

## Hard prohibitions

Do NOT create project-current positive causal-use permission, actor state, positive applicability, occurrence, witness independence, ENCOUNTER, OEE, current-positive OBL056 entries, or execute OBL055.

Do NOT claim SUB-VOZHD E adoption or HQ adoption.

## Required return

Return a durable repository packet containing the new frozen R7 candidate identity, exact repair description, governed court identities/results, direct regression coverage for the R6 lifecycle blocker, no-self-review attestation, no-current-effect attestation, and recommendation to SUB-VOZHD E.

Terminal:

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_BOUNDED_REPAIR_R7__RETURN_TO_SUB_VOZHD_E`
