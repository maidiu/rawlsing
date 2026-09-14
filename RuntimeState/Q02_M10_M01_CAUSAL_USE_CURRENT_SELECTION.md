# Q02 — M10-M01 CAUSAL-USE / CURRENT-SELECTION AUTHORITY R1

- repository: `maidiu/rawlsing`
- worker: `agent/rabochii-prev3-w15-q02-m10-causal-use-current-selection-r1`
- branch commission tip: `be693c5c948c020ee7867457516e41b866af7ad0`
- commission HQ authority: `4c2a0e9b0423be77a51284b34e87a3f8ae59a321`
- exact grain: `SDTF_M10_M01_CAUSAL_USE_AND_CURRENT_SELECTION_AUTHORITY_R1_ONLY`
- Library: `NO`

## Required candidate identity

- P03 return tip: `903079c179abca4eabd163c99b19efdef1855ce9`
- source worker tip: `0ebca9ff111bea63838f9b68c8e5c3cb93d9d128`
- source-ledger blob: `606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7`
- source ledger: `.../STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1/M10_WRIGHT_FULL_SOURCE_LEDGER_R1.md`
- bounded candidate: `M10-M01 — PROPERTY SEPARATION / WAGE DEPENDENCY`
- mechanism-class ceiling: `P1 MATERIAL_ACCESS DEPENDENCY`

Candidate documentary kernel retained from P03:

```text
insufficient independent productive assets
+ active wage position
+ contract/employer binding
-> dependence on labour-market sale for income/subsistence
+ employer relation
+ bounded exit set
```

The source ledger is competent extraction/adjudication evidence for this bounded mechanism candidate, but it explicitly states that source claims are not automatic architecture authority.

## Exact repo-bound binding authority consumed

The project-current SDTF R4 runtime package was adopted at `73f33a8a4c185c46faec5ac47332153ca079ca5f` from exact assembled candidate `de7f7dc9f34e1d0e1ebb1486ed3d960a4a82ffa8`.

Its R1 authority/currentness implementation is:

- contract: `SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0`
- production path: `rawlsing_next/sdtf_r4_mechanism_rule_authority_binding.py`
- exact blob: `c94997f5c7f2bbee9cd99c570554fd48c0f47556`

For a `CAUSAL_USE` role, that contract requires an `AuthorityCeilingBinding` with:

1. role exactly `CAUSAL_USE`;
2. disposition `BOUND`;
3. an exact `scope_or_na_ref`;
4. an exact competent `AuthorityRef`;
5. nonempty explicit `current_selection_evidence_refs`.

The enclosing mechanism-rule binding rejects any causal-use disposition other than `BOUND`. The same contract records `source_citation_does_not_imply_causal_use = True`, forbids mutable/latest/default/fuzzy authority selection, and does not create or resolve an authority registry. The adopted runtime package additionally states that the infrastructure mints no authorities.

The commission HQ authority `4c2a0e9b0423be77a51284b34e87a3f8ae59a321` adopts P03's exact deficit for this candidate: no exact external `CAUSAL_USE` authority + scope + current-selection evidence is project-current.

## Terminal

`Q02_BLOCK__NO_EXACT_PROJECT_CURRENT_EXTERNAL_CAUSAL_USE_AUTHORITY_PLUS_CURRENT_SELECTION_EVIDENCE_FOR_M10_M01`

## Adjudication

Q02 cannot lawfully emit the requested immutable `CAUSAL_USE` binding.

No exact project-current competent external `AuthorityRef` scoped to `M10-M01 — PROPERTY SEPARATION / WAGE DEPENDENCY` is supplied by the adopted P03 return or HQ fan-in, and no nonempty authority-current-selection evidence exists there for such a binding. The Wright source extraction cannot fill that role because `SOURCE_CITATION != CAUSAL_USE_AUTHORITY`. The `P1 MATERIAL_ACCESS DEPENDENCY` class ceiling likewise classifies the mechanism family but does not issue claim-specific causal-use permission.

Creating an `AuthorityRef`, scope/current-selection proof, or permitted-use statement from the source wording, mechanism plausibility, P1 membership, or the binding infrastructure itself would invent the missing authority layer. That is outside this commission and would violate the binding contract's fail-closed law.

## Smallest exact blocker

```text
NO EXACT PROJECT-CURRENT EXTERNAL CAUSAL_USE AuthorityRef
+ NO EXACT M10-M01-SCOPED CAUSAL_USE BINDING
+ NO NONEMPTY EXPLICIT CAUSAL_USE AUTHORITY-CURRENT-SELECTION EVIDENCE
FOR M10-M01 — PROPERTY SEPARATION / WAGE DEPENDENCY
UNDER SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0
```

This is narrower than P03's combined blocker: Q02 does not adjudicate or issue `RULE_OWNER`; that deficit belongs to its independent authority lane.

## PASS replay condition

Q02 may be replayed at this exact candidate once a competent project-current causal-use owner supplies an immutable, M10-M01-scoped authority binding with explicit current-selection evidence and an exact statement of permitted and prohibited causal/mechanism use. That binding must preserve provenance to source worker `0ebca9ff111bea63838f9b68c8e5c3cb93d9d128`, source-ledger blob `606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7`, the P03 return, and contract blob `c94997f5c7f2bbee9cd99c570554fd48c0f47556`, while retaining the negative ceilings above. Only then can deterministic binding identity/replay be computed without fabrication.

## Preserved boundaries

- no `RULE_OWNER` authority was issued or inferred;
- no concrete mechanism rule was minted;
- no Q01 or Q03 provisional output was consumed;
- no source or receiving structural position was bound into topology;
- no causal authority was inferred from Wright's wording;
- no V555/M2, V3/person-state, or OBL063 semantics were used;
- no Library search was performed;
- no MAIN or PRE-MAIN state was mutated.

This artifact supersedes the branch-local draft at `822c34ed7e6625d3dbe091888448e176eaf93e78`, whose source-worker identity did not match the committed Q02 commission. History is not rewritten.