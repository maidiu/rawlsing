# 10 — STANDARD RABOCHII ORDER TEMPLATE

Use this template for implementation workers after campaign activation.

```text
VOZHD TRII CLEAN MACHINE — <UNIT ID / MISSION TITLE>

You are Rabochii <ID> under <DOMAIN/SUB-VOZHD>.

Repository:
maidiu/rawlsing

EXACT BASE SHA:
<issued integration or command SHA>

Work ONLY on branch:
<branch>

Write ONLY under / modify ONLY:
<explicit paths>

COMMAND PARENT:
<domain/sub-Vozhd>

MISSION:
<one bounded implementation mission>

BINDING AUTHORITY PACK:
- <governing spirit / terminal law bundle hash>
- <whole-machine architecture closure ID/hash>
- <stage/seam authority IDs/hashes>
- <negative-authority IDs/hashes>

FROZEN SUBSTRATE:
- Incoming Data Contract: <id/version/hash>
- Physical Schema: <id/version/hash>
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
You may choose ordinary implementation details inside this contract where they do not alter shared schema, object grain, identity, authority, negative states, DAG edges, replay meaning, or sibling interfaces.

SHARED-CONTRACT RULE:
If implementation requires any shared contract/schema/identity/interface/authority change, STOP at that seam and return a formal change request. Do not invent a local convention.

LEGACY REUSE:
No legacy surface may be reused without a registered salvage classification. Historical stage naming creates no authority.

REQUIRED TESTS:
- <unit tests>
- <canonical golden fixture cases>
- <hostile negatives>
- <replay/identity tests if applicable>

REQUIRED OUTPUT PACKET:
1. RESULT.md
2. RESULT.json
3. SEMANTIC_DIFF.json
4. CONTRACT_CONFORMANCE.json
5. TEST_AND_FIXTURE_RECEIPT.json
6. DEPENDENCY_IMPACT.json
7. OPEN_AUTHORITY_REQUESTS.json

SEMANTIC_DIFF must explicitly report:
- object changes
- schema changes
- authority changes
- DAG changes
- ID/hash changes
- negative-state changes
- replay/reference changes
- affected consumers
- migration effects

ALLOWED RESULT STATES:
COMPLETE_CONFORMANT
COMPLETE_WITH_NONBLOCKING_DEBT
BLOCKED_SHARED_CONTRACT
BLOCKED_AUTHORITY_CONFLICT
BLOCKED_SUBSTRATE_AMBIGUITY
BLOCKED_SIBLING_DEPENDENCY
FAILED_CONFORMANCE

You do NOT have integration authority.
You do NOT have architecture-selection authority.
You do NOT have authority to modify sibling-owned contracts.
```

## Worker-order quality gate

A worker may not be launched if any of these are unknown:

- exact base SHA;
- authority pack;
- substrate version;
- consumed interface version;
- produced interface version;
- legal DAG edge;
- write surface;
- command parent.

If the mission genuinely does not touch one category, state `NOT_APPLICABLE` rather than omitting it.
