# SOROK O-LIVE R2 — dynamic gaps, blocked chain and next-flight readback

## What changed

R1 used a module-level `WORK_NOW` constant and a BFS-to-first-L5
`_critical_path`. R2 derives gaps and candidates from the persisted graph:

- node axes: source, science, engineering, authority, review, consumer, human,
  operational;
- source rows and exact Git source identity;
- typed edges: required/causal, consumer, governance, epistemic and
  hypothetical/index;
- imported O-SCIENCE workstream evidence, 14 missing-function rows and 226
  candidate links;
- explicit source-cut staleness and unreviewed-evidence holds.

No scalar priority is produced. Each candidate has relative impact, exact
blockers, owner, science/authority state, consumer and a next legitimate flight.

## Gap counts

| State | Nodes | Edges | Gaps | Work-now candidates |
|---|---:|---:|---:|---:|
| R1 baseline | 198 | 423 | 22 | 22 |
| After O-SCIENCE import | 212 | 649 | 37 | 37 |
| After S5 source fault | 212 | 649 | 41 | 41 |
| After exact S5 repair | 212 | 649 | 37 | 37 |
| After new requirement intake | 212 | 649 | 38 | 38 |
| Final persisted reference | 212 | 649 | 38 | 38 |

Fault gap delta:

- added `GAP_INVALIDATED_L3_S5_NORMATIVE_MODEL`,
  `GAP_INVALIDATED_L4_S5_FLOURISHING_OWNER`,
  `GAP_INVALIDATED_L5_S5_HARMFUL_ATTACHMENT_COUNTEREXAMPLE` and
  `GAP_INVALIDATED_S5`;
- repair removed exactly those four and restored the three dependent nodes to
  `CANDIDATE_READY`;
- the new requirement added `GAP_SOROK_R2_NEW_REQUIREMENT`.

The final gap classes are:

| Class | Count |
|---|---:|
| `WORKSTREAM_OUTPUT_OR_CONSUMER` | 17 |
| `MISSING_FUNCTION` | 14 |
| `NATIVE_OR_OWNER_BLOCKER` | 4 |
| `UNREVIEWED_CANDIDATE_EVIDENCE` | 1 |
| `EXTERNAL_BOUNDARY` | 1 |
| `UNREPRESENTED_REQUIREMENT` | 1 |

The 17S workstreams are all represented; the six original product gaps are
specific (`GAP_S5_NORMATIVE_OUTPUT`, `GAP_S7_PRAXIS_OUTPUT`,
`GAP_S11_HUMAN_UX`, `GAP_S13_REVENUE_MODEL`, `GAP_S14_SOCIAL_SAFETY`,
`GAP_S15_HUMAN_ALPHA`) and the other eleven are explicit
`GAP_WORKSTREAM_Sx` gaps. Source identity alone does not remove a gap: every
S workstream remains consumer-missing until an actual consumer/owner is proven.

## Work-now routes

The final work-now has 38 candidates in 8 parallel groups:

| Group | Candidates | Parallel |
|---|---:|---|
| `C12_A5_FUNCTION` | 14 | yes |
| `PRODUCT_WORKSTREAM` | 17 | yes |
| `NATIVE_PERSON` | 2 | yes |
| `SCIENCE_OWNER` | 1 | no |
| `HUMAN_ALPHA` | 1 | no |
| `REVIEW` | 1 | no |
| `EXTERNAL_BOUNDARY` | 1 | no |
| `DISCOVERED_REQUISITE` | 1 | no |

Relative impact is evidence-backed, not a priority decree. Examples:

| Gap | Relative impact | Evidence |
|---|---:|---|
| `GAP_MISSING_FUNCTION_01` | 7 | seven original workstreams: S0/S5/S7/S11/S13/S14/S15 |
| `GAP_MISSING_FUNCTION_05` | 5 | S7/S8/S9/S11/S14 |
| `GAP_MISSING_FUNCTION_02` | 4 | S1/S3/S12/S15 |
| `GAP_SOROK_R2_NEW_REQUIREMENT` | 0 | newly discovered; owner/consumer not assigned |

Each candidate carries `blockers` such as:
`source_recovery=SOURCE_NOT_FOUND`, `science=CANDIDATE_EVIDENCE_NOT_ISSUED`,
`authority=NOT_ADOPTED`, `consumer=INVALIDATED_BY_UPSTREAM`,
`human=NOT_PROVEN`, or a required predecessor's exact edge ID.

## Blocked chain

`blocked-chain A5` is `TYPED_BLOCKED_CHAIN`, not a shortest path:

- required edges considered: **129**;
- hypothetical/candidate edges excluded: **268**;
- A5 blockers: science `NOT_ISSUED`, authority
  `OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION`, human `NOT_PROVEN`;
- the external Pyat boundary is not traversed and is not locally mutable.

`blocked-chain C12` likewise excludes the 226 O-SCIENCE hypothesis edges and
does not turn them into required causal dependencies.

## Source fault and repair readback

S5 source withdrawal:

- invalidated `L3_S5_NORMATIVE_MODEL`, `L4_S5_FLOURISHING_OWNER`,
  `L5_S5_HARMFUL_ATTACHMENT_COUNTEREXAMPLE` and S5's own consumer;
- untouched: `M01` consumer `NONE_PROVEN_AT_PREMAIN`, `V3CORE-R1` consumer
  `AUTHOR_TESTED_ONLY`, `S0` consumer `NOT_A_RUNTIME_MODULE`, Pyat status
  `EXTERNAL_OWNER_HELD`;
- work-now showed the invalidation gap and the blocked chain named the exact
  source and required predecessor.

Exact S5 source repair:

- `restored = [L3_S5_NORMATIVE_MODEL, L4_S5_FLOURISHING_OWNER,
  L5_S5_HARMFUL_ATTACHMENT_COUNTEREXAMPLE]`;
- all four invalidation gaps removed;
- S5's own consumer restored to its prior `NOT_A_RUNTIME_MODULE` state, not a
  false actual consumer;
- S5 product gap remains (`GAP_S5_NORMATIVE_OUTPUT`); repair restores only what
  the source evidence warrants.

## Product coverage readback

The final reference exposes:

| Surface | Status | Present nodes | Candidate evidence |
|---|---|---|---|
| user | `CANDIDATE_EVIDENCE` | S7/S8/S11/S15 | S7/S8/S11/S15 |
| UX | `CANDIDATE_EVIDENCE` | S11/S15/CP-A5-R2 | S11/S15 |
| safety | `CANDIDATE_EVIDENCE` | S14/C9C12-R2/E08 | S14 |
| economics | `CANDIDATE_EVIDENCE` | S13 | S13 |
| alpha | `CANDIDATE_EVIDENCE` | S15/A5/CP-A5-R2 | S15 |
| native person | `SOURCE_ONLY_OR_MISSING` | C4/C11/C12/A5 | none |
| science | `SOURCE_ONLY_OR_MISSING` | N10/N11/N12 | none |

The candidate evidence is not an implemented product. Missing consumers remain
explicit in every row.

## Next-flight candidates

The following are candidate routes, not a ranking:

1. **O-SCIENCE review** — one independent I3 review of the exact patch digest
   and the integrated 17/102/14/226 evidence; hypothesis links stay candidate.
2. **S-workstream product outputs** — owners produce S0–S16 outputs and name
   actual consumers; S5/S7/S11/S13/S14/S15 remain the first product-specific
   alternatives.
3. **C12→A5 missing functions** — 14 missing-function rows become actual typed
   functions with consumers; no sixth-workstream substitution.
4. **Native person/science** — original C4/C11/C12/A5 and CAN/ADP/SCI05 owners
   decide; no local string can promote them.
5. **External Pyat contract** — Pyat HQ supplies the qualified world/N11/N12/C11
   input or a typed HOLD; Sorok does not invent it.
6. **Recovery assets** — R6/R7 and the four returned assets remain unadopted
   until their owners and independent review act.

## HQ judgment

`HQ_JUDGMENT_REQUIRED`. The map now makes actual blockers, consumers, impacts and
parallel alternatives legible; it does not choose the substantive priority.
