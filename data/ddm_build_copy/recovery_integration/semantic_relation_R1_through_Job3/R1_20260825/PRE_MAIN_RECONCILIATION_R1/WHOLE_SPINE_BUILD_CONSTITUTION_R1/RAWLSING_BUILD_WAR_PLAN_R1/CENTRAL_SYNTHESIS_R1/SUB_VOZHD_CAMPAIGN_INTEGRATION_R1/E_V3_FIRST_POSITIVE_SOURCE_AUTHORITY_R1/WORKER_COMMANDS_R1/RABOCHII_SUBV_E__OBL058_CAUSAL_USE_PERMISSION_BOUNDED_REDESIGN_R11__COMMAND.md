# RABOCHII SUB-VOZHD E — OBL058 CAUSAL_USE_PERMISSION — BOUNDED DISPATCH-CAPABILITY REDESIGN R11 — COMMAND R1

ROLE: `RABOCHII SUBORDINATE`

REPORTS TO: `SUB-VOZHD E`

LANE: `E1 / OBL058 — FIRST-POSITIVE OEE CAUSAL-USE PERMISSION SOURCE AUTHORITY`

WORKER BRANCH:
`agent/rabochii-subv-e-obl058-causal-use-permission-bounded-redesign-r11`

EXACT WORKING-ANCESTRY START:
`61b3731b0b20ed4ebdbe5918a076674c05cf403d`

FAILED FROZEN R10 TARGET — RETAIN UNCHANGED:
`0d23b02c75783033a4c8087b00721cb73a0924b4`

R10 REVIEW TERMINAL BLOCKER:
`BLOCKER__OBL058_R10_DISPATCH_VERIFIER_READS_MODULE_DICT_BUT_PUBLIC_VALIDATOR_BINDING_USES_CALLER_MUTABLE_MODULE_ATTRIBUTE_LOOKUP`

## Commission

Produce a NEW OBL058 R11 frozen candidate by redesigning the dispatch/binding boundary at the smallest abstraction level that closes the recurring family.

This is not a commission to patch one more attribute lookup.

The governing property is:

> the exact validation capability that is authenticated/verified must be the exact capability retained and later invoked. After that capability is established, no later caller-mutable ordinary Python lookup surface may substitute a different validation decision path.

The mechanism may be chosen by the worker, but verification and invocation must converge on one retained identity/capability boundary.

## Required closure properties

At minimum, the new candidate must establish all of the following:

1. The verifier does not validate one object/surface and then later invoke a capability obtained through an independent Python module attribute lookup.
2. The exact verified callable/capability identity is retained for subsequent public validation use.
3. Rebinding or customizing the dispatch module's ordinary attribute access after establishment cannot substitute `bind_contract`, `public_validate`, or an equivalent decision entry.
4. Replacing relevant entries in `sys.modules`, adding module aliases, changing module `__class__`, customizing module `__getattribute__`, or rebinding ordinary exported names after establishment cannot redirect the accepted decision path.
5. Python class/instance/descriptor/metaclass lookup cannot re-enter as a substitute path for the already-closed R9 receipt-class seam.
6. If the verified dispatch bundle/capability cannot be established from the authenticated source boundary, fail closed rather than using an ordinary Python fallback.
7. Do not merely add a second verification step immediately before an ordinary mutable lookup. The property is retained identity, not repeated expectation of equivalence.

## Preserve all independently closed properties

Do not reopen the properties that survived earlier producer and independent courts, including:

- R9 native-core source-origin/import-cache binding closure;
- R8 native transport and peer/source decision path;
- requester process generation and fork separation;
- explicit close and bounded lifecycle cleanup;
- endpoint/broker death handling;
- exact actor/world/subject/time/transition scope;
- genuine source-basis and current/stale controls;
- fabrication/copy/reconstruction rejection;
- concurrency behavior;
- no project-current effects;
- no weakref/finalizer authority dependency;
- no caller-mutable Python socket-constructor dependency;
- no receipt-class method-dispatch dependency.

## Producer court requirements

Build a bounded producer court that includes, at minimum:

- the exact R10 independent-review reproduction involving divergence between module-dictionary verification and module-attribute binding;
- module `__class__` / `__getattribute__` customization before and after capability establishment;
- exported-name rebinding before and after issuance/validation establishment;
- `sys.modules` replacement and alias-module cases;
- relevant import/spec/loader/cache surfaces sufficient to show the redesign did not merely move the lookup seam;
- class/instance/descriptor rebinding controls covering the closed R9 family;
- genuine PERMIT and DENY controls;
- unregistered control remains DENY;
- lifecycle/fork/close/scope/source-basis/reconstruction/concurrency controls;
- no-current-effect assertions.

The court should test the invariant as a family, not only one concrete module-class reproduction.

## Frozen candidate discipline

Freeze a NEW R11 candidate commit.

Record exact executable/native source blobs and the new mechanism/revision identity.

The failed R10 candidate remains immutable historical evidence.

## Review separation

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R11_REDESIGN_WORKER = NO`

Do not commission or perform the fresh independent review yourself.

If the producer court is green, return the new candidate to SUB-VOZHD E for exactly one fresh distinct independent review.

## Current-effect exclusions

Do not create or consume project-current positive effects.

No current actor, current ADP-008 transition, current ADP-019 occurrence, current-positive OBL056 entry, OBL055 execution, ENCOUNTER, project-current OEE, OBL061 execution, comparator/PSEPF/OBL032 work, architecture/topology selection, or sibling-campaign work is authorized.

`OBL061 = HARD_BLOCKED`

`POSITIVE_V3_EXECUTION = NOT_AUTHORIZED`

`PROJECT_CURRENT_FIRST_CANARY_OEE = NOT_AUTHORIZED`

## Return Beacon

The terminal Return commit must contain `.rabochii/return_manifest.json` and the durable return packet together, truthfully recording PASS/FAIL/BLOCKED, CLOSURE_ONLY, required outputs, governed evidence, no uncommissioned review, and no required/background work remaining.

The final commit headline must contain `Return`.

## Return

Return exact branch, start, frozen candidate, final tip, mechanism identity, governed evidence execution, run/job, court counts, artifact identity/hash, execution-only PR disposition, self-review flags, and recommendation.

On producer-green:

`PASS__OBL058_R11_BOUNDED_REDESIGN__READY_FOR_EXACTLY_ONE_FRESH_DISTINCT_INDEPENDENT_REVIEW`

Terminal form:

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_BOUNDED_REDESIGN_R11__RETURN_TO_SUB_VOZHD_E`
