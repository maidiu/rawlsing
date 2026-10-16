# HQ314 OUT9 — reviewer independence declaration and hostile acceptance matrix

## Independence

- This review was produced by a **fresh reviewer agent distinct from every
  author chain**: not the OUT8 author (repair), not the OUT6 author, not the
  OUT7 independent author, not HQ.
- No self-adoption: this return ranks and reproduces evidence; it adopts no
  CAN/ADP rule, no policy, and no production state.
- No helper agent, no model switching, no human-perception assertion, no
  semantic adoption, no V3 operation.
- One agent completed staging, reproduction, hostile court, cold-crash evidence,
  documentation and push.

## What was re-verified vs relied upon

| Item | Method | Result |
|---|---|---|
| 247 closure identity | git blob SHA-1 (NUL header) + sha256 + byte count vs pinned ancestors and author pins | 16/16 pinned verified; source lineage reconstructed from patches |
| 247 results | literal unchanged run of the exact command form | 245 PASS / 2 historical RED (matches author frozen counts per module) |
| two historical REDs | read their failing assertions directly | S27 material move (no world owner); two-writer stale journal race — both preserved, neither xfailed/skipped/edited |
| cold journal | real child-process `os._exit` at both boundaries + tamper+recompute | atomic and typed-refusing |
| imports/cold realness | `module.__file__` probe + real subprocess cold tests | resolves into isolated staging dir |

## Hostile acceptance matrix (this court)

| Requirement (commission) | Case(s) | Result |
|---|---|---|
| aggregate ACK↔client ACK congruence, ACTIVE viewer | N02, N23 | VALID_LEGITIMATE validates |
| aggregate ACK↔client ACK congruence, formerly-authorized REVOKED viewer | N01, N09 | VALID_LEGITIMATE validates (history survives) |
| forged aggregate ACK / only-failed client receipt | N22 | REFUSED `FORGED_AGGREGATE_ACK_WITHOUT_CLIENT_RECEIPT` |
| zero-ACK / too-many ACK counts | N04, N05 | REFUSED `BAD_DELIVERY_IDENTITY` / `BAD_AGGREGATE_DELIVERY_COUNTS` |
| zero-attempt masquerade | N03, N06 | REFUSED `INCONSISTENT_DELIVERY_STATE` / `BAD_AGGREGATE_DELIVERY_COUNTS` |
| revoked `NOT_SENT`/attempts-0 tombstone | N08, N25 | REFUSED `FORGED_ZERO_ATTEMPT_CLIENT_HISTORY` |
| valid ACTIVE `NOT_SENT` placeholder | N07 | VALID |
| detached restore / failure atomicity | N10–N13 | REFUSED with typed codes + live snapshot byte-unchanged |
| real cold `Journal.recover` after unkeyed checksum recompute | N14 (valid → recovers), N15 (tamper → refused), N25 | as expected; digest recompute is never authorization |
| `os._exit` crash before/after rename | N16, N17 + `cold_crash_evidence.py` | atomic at both boundaries (before: prior bytes identical; after: newest state durable+valid) |
| legitimate multi-viewer behavior + remaining-authorized retry | N02, N18 | VALID |
| ACK terminal immutability | N19 | ACK survives failure callback + cold reload |
| revoked-viewer new emission refused | N20 | `None`, no new attempt |
| ghost opportunity / projection leakage | N21 | REFUSED |
| duplicate event identity | N24 | single deterministic ledger entry |
| no human perception asserted | all | none; `projection.perceive` never asserted OK |

## Acceptance statement (bounded)

At the **source-free single-writer grain**, OUT8's repaired closure satisfies
the commissioned custody invariants and reproduces exactly with the two frozen
historical REDs preserved. **REVIEW_PASS_SCOPED_SINGLE_WRITER_SOURCEFREE.**

Anything beyond that grain (real client ACK, human perception, multiwriter
safety, ADP-019 event authority, OUTP policy, population claims) remains
unproved and is not claimed by this review.
