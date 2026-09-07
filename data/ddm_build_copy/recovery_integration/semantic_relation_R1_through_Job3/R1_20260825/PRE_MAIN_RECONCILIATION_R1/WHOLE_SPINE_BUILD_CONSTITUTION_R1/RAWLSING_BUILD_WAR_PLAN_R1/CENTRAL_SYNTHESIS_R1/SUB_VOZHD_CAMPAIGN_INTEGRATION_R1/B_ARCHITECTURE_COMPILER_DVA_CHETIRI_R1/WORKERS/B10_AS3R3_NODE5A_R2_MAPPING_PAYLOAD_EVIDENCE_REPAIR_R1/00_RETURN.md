# B10 — AS3R3 Node5A-R2 mapping-payload evidence repair R1

Terminal:

`AS3R3_NODE5A_R2_MAPPING_PAYLOAD_EVIDENCE_REPAIR__IRRECOVERABLE_PROTOCOL_BLOCKER`

HQ return:

`READY_FOR_VOZHD_HQ_ADJUDICATION__NODE5A_R2_MAPPING_REPLAY_PROTOCOL_IRRECOVERABLE`

## Holding

The bounded forensic search did **not** recover either lawful PASS path:

- Outcome A — the actual historical byte preimage of the accepted Node5A-R2 mapping-payload digest: **NOT RECOVERED**.
- Outcome B — the actual historically used deterministic serialization law that generated those bytes: **NOT RECOVERED**.

The blocked historical digest remains:

`081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`

This return does not dispute that Node5A-R2 recorded that digest or that three historical replay runs reported it. The defect is narrower: the evidence chain retained the **digest and material 19-row mapping**, but did not retain the byte payload or the byte-producing protocol needed for a future independent process to reproduce that historical digest.

## No target fitting

B10 did not enumerate, hash, or compare candidate JSON/CSV/JSONL/newline/field-order/whitespace/encoding variants.

Candidate serializations tested against the target digest: **0**.

No putative serialization law was selected because it matched the target. No retrospective law is supplied.

The target digest was treated only as the identity of the historical proof obligation under investigation. Because no independently grounded preimage or law was recovered, there was no lawful candidate on which to perform final digest verification.

## Provenance search result

The commissioned search order was completed:

1. **Node5A-R2 immutable commit sequence** — inspected from command-only tip `127fda6e...` through terminal `a208b910...`. Nine additive evidence commits exist; none contains a helper, mapping-payload byte carrier, or serialization law.
2. **Original fail-closed Node5A** at `34caf24...` — its command and replay receipt establish deterministic 19-row mapping reproduction and the A000/A1RAPP collision, but contain no mapping-payload serialization/preimage protocol.
3. **Identity/cardinality court** at `dc597c5...` — establishes the lawful 19-role / 19-mapping / 18-object cardinality and sole alias, not a mapping-payload byte law.
4. **Frozen Node4A / producer surfaces** — establish exact inputs, constructor identity, canonical predicate identity law, and runtime semantics; they do not specify how Node5A-R2 wrapped its 19 role mappings into the separate historical payload whose digest is blocked here.
5. **PR #243** — exact Node5A-R2 banking PR. No comments contain execution code or preimage material; its diff is the same committed evidence set.
6. **Workflow run 34090165952** — no artifacts. The governed-court job failed at generic protocol self-test before bounded-court execution; no mapping helper/output was uploaded.
7. **Retained Library/conversation execution evidence** — searched using the Node5A-R2 branch/task name and rare replay-receipt field names, not the target digest. Only exported result artifacts were recovered; no bash/Python execution transcript or scratch helper containing the mapping-payload construction survived.
8. **Explicitly referenced helper/output** — none is referenced by the Node5A-R2 receipt/ledger as the producer of the mapping payload.
9. **Earlier reused replay implementation** — original Node5A records fresh mapping determinism but does not retain or define a byte serialization protocol that Node5A-R2 can be shown to have reused.

## Material mapping remains intact

This evidence failure does not reopen semantic identity:

- material role/source rows: **19**;
- distinct canonical successor predicates: **18**;
- sole alias class: **{A000,A1RAPP}**;
- A000 and A1RAPP remain separate role rows;
- both resolve to canonical predicate content hash `ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0`;
- material crosswalk Git blob remains `26a7c35df2e6454c5e270a03b3571599bdf152fd`.

No row, ExactRef, producer input, canonical predicate, count law, or semantic terrain was modified.

## Why retrospective repair is unlawful at B10 authority

A deterministic convention can certainly be specified **now** for serializing the 19 committed rows. That would create a prospective protocol. It would not prove that the convention was the one historically used to generate `081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`.

Selecting a present convention by trying plausible byte layouts until the historical digest matches would be exactly the target fitting prohibited by the B10 commission.

Therefore B10 cannot lawfully convert evidence incompleteness into historical proof.

## HQ question

The remaining issue is an evidence/protocol authority question, not a semantic/runtime question:

> How should Node7 treat a historical digest whose asserted historical replay is preserved, but whose byte preimage and generating serialization protocol are irrecoverable?

B10 does not decide that question.

HQ may adjudicate the proof contract prospectively without changing the 19 mapping rows or successor identities. What B10 cannot authorize is a false claim that a newly chosen serialization convention is the recovered historical law.

## Boundary audit

B10 did not:
- modify Node5A-R2 or original Node5A;
- modify Node4A, producer/contract/schema, Node4B, Node5B, Node6, or B9;
- execute Node7;
- create DiscoveryAuthority/frontier/replay identities;
- execute AS4I0, hostile validation, LiTS-I/I05/C05R2B, C08/G1, OBL037, or V3;
- modify central state, PRE-MAIN, main, or sibling campaigns.

Node7 remains frozen.

Return to:
`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`.
