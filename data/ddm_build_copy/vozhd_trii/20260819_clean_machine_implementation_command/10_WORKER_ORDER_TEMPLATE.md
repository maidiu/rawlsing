# 10 — STANDARD RABOCHII ORDER TEMPLATE

Use this template for implementation workers after campaign activation.

```text
VOZHD TRII CLEAN MACHINE — <UNIT ID / MISSION TITLE>

You are Rabochii <ID> under <DOMAIN/SUB-VOZHD>.

Repository:
maidiu/rawlsing

EXACT BASE SHA:
<issued integration or command SHA>

COMMAND DEPENDENCY EPOCH:
<epoch id>

Work ONLY on branch:
<branch>

Write ONLY under / modify ONLY:
<explicit paths>

SHARED WRITE LEASES:
- <resource/lease id or NONE>

COMMAND PARENT:
<domain/sub-Vozhd>

MISSION:
<one bounded implementation mission>

BINDING AUTHORITY PACK:
Manifest: <authority-pack id/version/content-hash>
- <governing spirit / terminal law document id/hash>
- <whole-machine architecture closure ID/hash>
- <stage/seam authority IDs/hashes>
- <negative-authority IDs/hashes>

FROZEN SUBSTRATE:
- Incoming Data Reality Receipt: <id/version/hash>
- Incoming Data Contract: <id/version/hash>
- Physical Schema: <id/version/hash>
- Database Snapshot/Profile Authority: <id/hash or governed external locator>
- Golden Fixture: <id/hash>

FROZEN INTERFACES:
Consumes:
- <interface id/version/hash>

Produces:
- <interface id/version/hash>

LEGAL DAG EDGES:
- <exact registered edges>

FORBIDDEN EDGES / SEMANTIC MOVES:
- <exact negatives>

SIBLING DEPENDENCIES:
- <units/contracts actually depended upon>

LOCAL ENGINEERING FREEDOM:
You may choose ordinary implementation details inside this contract where they do not alter shared schema, object grain, identity, authority, negative states, DAG edges, replay meaning, sibling interfaces, substrate grain, transaction semantics, or source-universe law.

SHARED-CONTRACT RULE:
If implementation requires any shared contract/schema/identity/interface/authority/substrate change, STOP at that seam and return a formal change request. Do not invent a local convention.

STALE-DEPENDENCY RULE:
If G6 marks any frozen dependency stale, do not cross the affected interface or claim completion until a DEPENDENCY_REFRESH_RECEIPT is accepted.

LEGACY REUSE:
No legacy surface may be reused without a registered salvage classification. Historical stage naming creates no authority.

REQUIRED TESTS:
- <unit tests>
- <producer or consumer contract vectors>
- <cross-worker seam vectors if applicable>
- <canonical golden fixture cases>
- <hostile negatives>
- <replay/identity tests if applicable>
- <database key/cardinality/transaction tests if applicable>

REQUIRED OUTPUT PACKET:
1. RESULT.md
2. RESULT.json
3. SEMANTIC_DIFF.json
4. CONTRACT_CONFORMANCE.json
5. TEST_AND_FIXTURE_RECEIPT.json
6. DEPENDENCY_IMPACT.json
7. OPEN_AUTHORITY_REQUESTS.json
8. DEPENDENCY_REFRESH_RECEIPT.json or NOT_APPLICABLE
9. SHARED_WRITE_LEASE_RELEASE.json or NOT_APPLICABLE

SEMANTIC_DIFF must explicitly report:
- object changes
- schema changes
- authority changes
- DAG changes
- ID/hash changes
- negative-state changes
- replay/reference changes
- source-universe behavior
- transaction/storage behavior where applicable
- affected consumers
- migration effects

ALLOWED RESULT STATES:
COMPLETE_CONFORMANT
COMPLETE_WITH_NONBLOCKING_DEBT
BLOCKED_SHARED_CONTRACT
BLOCKED_AUTHORITY_CONFLICT
BLOCKED_SUBSTRATE_AMBIGUITY
BLOCKED_SIBLING_DEPENDENCY
STALE_DEPENDENCY__NO_CROSS_INTERFACE_PROGRESS
FAILED_CONFORMANCE

You do NOT have integration authority.
You do NOT have architecture-selection authority.
You do NOT have authority to modify sibling-owned contracts.
You do NOT have authority to mutate shared canonical resources without a recorded write lease.
```

## Worker-order quality gate

A worker may not be launched if any of these are unknown:

- exact base SHA;
- command dependency epoch;
- content-hashed authority pack;
- populated Incoming Data Reality receipt where substrate-dependent;
- substrate version;
- consumed interface version;
- produced interface version;
- legal DAG edge;
- write surface;
- shared-write lease state;
- command parent.

If the mission genuinely does not touch one category, state `NOT_APPLICABLE` rather than omitting it.
