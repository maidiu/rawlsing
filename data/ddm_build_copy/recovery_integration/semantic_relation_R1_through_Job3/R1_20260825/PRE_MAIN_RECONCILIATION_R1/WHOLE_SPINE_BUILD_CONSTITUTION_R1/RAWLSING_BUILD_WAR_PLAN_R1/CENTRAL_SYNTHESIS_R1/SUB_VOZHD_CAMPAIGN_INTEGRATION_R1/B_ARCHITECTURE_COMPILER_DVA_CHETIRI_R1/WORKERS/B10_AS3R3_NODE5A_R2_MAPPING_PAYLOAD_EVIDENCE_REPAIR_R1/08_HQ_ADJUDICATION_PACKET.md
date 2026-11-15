# B10 — Vozhd HQ adjudication packet

Packet:

`READY_FOR_VOZHD_HQ_ADJUDICATION__NODE5A_R2_MAPPING_REPLAY_PROTOCOL_IRRECOVERABLE`

Worker terminal:

`AS3R3_NODE5A_R2_MAPPING_PAYLOAD_EVIDENCE_REPAIR__IRRECOVERABLE_PROTOCOL_BLOCKER`

## Exact defect

Node5A-R2 preserved:
- the material 19 role/source mapping rows;
- the historical mapping payload digest `081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`;
- receipts asserting three fresh historical runs reproduced that digest.

It did **not** preserve:
- the exact byte payload hashed to produce that digest; or
- the exact deterministic serialization protocol that produced those bytes.

B10 exhausted the commissioned independently grounded provenance surfaces without finding either.

## Why B10 cannot repair it retrospectively

There are many deterministic ways one could serialize the same 19 material mappings today. Choosing one now establishes a new prospective convention.

It does not establish historical identity with the lost Node5A-R2 protocol.

Choosing among possible conventions by seeing which one matches `081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e` is explicitly forbidden target fitting. B10 performed no such search.

Therefore the missing historical replay protocol is irrecoverable at worker/campaign evidence-repair authority.

## What is not in dispute

Do not reopen or mutate:
- 19 source/role rows;
- 19 role-to-ref mappings;
- 18 distinct canonical successor predicates;
- sole alias `{A000,A1RAPP}`;
- exact successor refs;
- Node4A mappings;
- producer/schema;
- Node4B/Node5B;
- Node6 semantic/runtime aggregate identities merely to cure this evidence defect;
- frozen 82-candidate terrain or A/B/C fairness.

This is an evidence-contract defect.

## Exact HQ question

HQ must decide the status of the **historical mapping-payload digest as a Node7 replay obligation** when the historical byte protocol is no longer recoverable.

B10 does not select a disposition.

At evidence/protocol grain, the logically available classes are:

- preserve the historical digest as immutable provenance but declare it non-replayable, then prospectively define a new explicit mapping-payload serialization law for future fresh replay without claiming that new payload is the historical `081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e` preimage; or
- retain exact historical-digest reproduction as mandatory, in which case Node7 remains permanently blocked unless an independently grounded historical preimage/law is later discovered.

Any HQ action must explicitly distinguish **prospective proof protocol** from **historical preimage recovery**.

No semantic identity change is required or justified by B10.

## Downstream gate

Until HQ adjudicates:
- Node7 frozen;
- no successor DiscoveryAuthority/frontier/replay seal;
- no AS4I0;
- no C05R2B;
- no C08/G1;
- OBL037 remains gated;
- no V3.
