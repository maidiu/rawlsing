# EE-P2F1 — FINAL CHETIRI P2 WVS7 PRE553 AUTHORITY REQUIREMENTS / POSSESSION / TRANSLATION AUDIT

Status: `COMMISSIONED__AUTHORITY_REQUIREMENTS_AND_POSSESSION_AUDIT_ONLY__NO_OBJECT_MINTING_YET`

Repository: `maidiu/rawlsing`

Exact branch:

`agent/rabochii-prev3-ee-p2f1-wvs7-authority-requirements-possession-audit-r1`

## Mission

Determine **exactly what authority the frozen WVS7 P2 program requires, whether Rawlsing already possesses that authority in another accepted form, and what the smallest lawful next action is for every requirement**.

This is not a semantic rediscovery exercise and not an object-construction task.

Read current canonical HQ from `HQ_HANDOFF/LATEST.json`, then read:

- `HQ_HANDOFF/CHETIRI_CARRIER_DECISION_CLOSURE_PLAN_R2.md`;
- `HQ_HANDOFF/CHETIRI_FINAL_P2_COURT_MANIFEST_R1.md`;
- `HQ_HANDOFF/CHETIRI_FINAL_P2_COURT_MANIFEST_R1.json`;
- `HQ_HANDOFF/EE_P2F0_BLOCKER_ADJUDICATION_20260917.md`;
- EE-P2F0 governed return at `520231f0b86ab93ae396a2e89ceb900ba54c6407`.

## Core question

For every exact PRE553 object/authority required to materialize and execute the frozen WVS7 46-candidate court:

1. What exact public object family / authority kind / operation / scope is required by current code?
2. What semantic proposition does that formal requirement actually assert?
3. Which accepted current Rawlsing artifact(s), if any, already assert that proposition?
4. Is the missing step only mechanical PRE553 issuance/current binding?
5. If the proposition is not yet adopted, does already-authorized exact source evidence suffice for a competent owner to adopt it without inspecting empirical outcomes?
6. If not, what genuinely new authority/evidence is missing?

## Required classification

Every requirement must terminate in exactly one class:

- `A__SATISFIED_AS_IS_PRE553_READY`
- `B__SEMANTIC_AUTHORITY_EXISTS__PRE553_ISSUANCE_OR_BINDING_ONLY`
- `C__SOURCE_EVIDENCE_SUFFICIENT__NEW_ADOPTED_AUTHORITY_REQUIRED`
- `D__GENUINELY_MISSING_SEMANTIC_OR_ROUTING_AUTHORITY`
- `E__NOT_REQUIRED_FOR_FROZEN_P2_WVS_PROGRAM`

Do not collapse B/C/D.

## Authority surfaces that MUST be inspected

At minimum:

### PRE553 formal requirements

- `rawlsing_next/pre553_empirical_objects.py`
- `rawlsing_next/pre553_empirical_authority.py`
- `rawlsing_next/pre553_empirical_query.py`
- current exact-bounded I05/discovery implementation and validators actually used by the accepted LiTS path;
- accepted LiTS PRE553 authority/object precedent, including the exact discovery-frontier authority snapshot consumed by HB04/AS4.

### WVS accepted source/semantic/routing surfaces

- EE-R6A at `4b141b8b5748175e34c9286eba36f53d8df1e9d5`, especially:
  - `WORKER_RETURNS/EE-R6A/02_QID_BOUND_RESPONSE_SEMANTICS.json`
  - `WORKER_RETURNS/EE-R6A/03_SELECTED_PROVING_PAIR.json`
  - `WORKER_RETURNS/EE-R6A/04_OP003_OP006_WVS7_PREMISE_ORACLE_PACKAGE.json`
- PSC03-A04 at `7321ed3e7faf43deb8c71bad69df8103a7a7755e`;
- L05-R2 at `1f56349c3fd1a99b8ae83d07da2aac81e01699fb`;
- EE-R3D at `fbd151af338c6b56c5d8072015425ab6cb05bbc3` and the exact reason its objectizer-ready subset is empty;
- exact accepted WVS R14/B03/current-qid/source-native authority named by those artifacts;
- exact WVS7 source/universe identity and current binding authority already banked in repo;
- current HQ decisions relevant to cross-survey source-state / source-local semantic / risk-set separation.

Do not treat `EE-R3D positive_or_known_count=0` as globally dispositive without proving that its exact authority question is the same question PRE553 now needs.

## Library access

Library mode: `EXACT_ONLY`.

Library may be used only to verify already-named evidence chains when the repo artifact is insufficient to classify B vs C vs D. No discovery search.

Permitted WVS documentary carriers include only exact files already named by accepted repo authority, including:

- WVS Wave 7 codebook: `file_00000000e41c722f8d67a0fc93343951`, accepted SHA-256 `d13c892099ac6a4681acdad344b81f99d086a5694be94cf5e7a578a62bf02ad3`;
- WVS Wave 7 questionnaire: `file_00000000da80722f98a132205b69d244`, accepted SHA-256 `5b6b06cb79681c0f5013fcfb93720951a033674b657985944bfcabc9f6a2735b`;
- WVS deep catalog: `file_000000007cfc81f9a595a3de1e57fa15`, accepted SHA-256 `cc538e7208e96f2a3333082e3ffdc88faf1bba0eee273664fe2ff213c3821ec0`;
- exact R14/R5 evidence carriers already named by L05-R2, only if needed to verify an already-named chain.

**WVS Wave 7 SAV empirical source bytes are forbidden.** No outcome access.

## Required authority rows

The audit must explicitly adjudicate at least:

1. `EmpiricalUniverse@1.0.0` identity/current source-universe binding.
2. Source semantics/topology authority for Q291G5 and Q291P5.
3. Substantive response-state atom authority for raw states `1..5` and typed handling of `-1,-2,-4,-5`.
4. Same-respondent / pair topology authority.
5. Country-conditioned applicability / routing / risk-set authority for the frozen 13-country set.
6. Exact source-universe/risk-set ExactRefs needed by predicates and queries.
7. `PREDICATE_GRAMMAR` authority required for `EmpiricalPredicate@1.0.0`, `EmpiricalQuerySpec@1.0.0`, and `EmpiricalFact@1.0.0`, including source scope and exact operations.
8. Required predicate atoms and compound predicate forms for the frozen 46-candidate grammar.
9. Required `EmpiricalQuerySpec` templates for unary, pair/cotravel, branch-conditioned and 5x5 joint-support roles.
10. Measure-basis / unweighted exact-count authority needed by this court; explicitly identify any weight/design authority that is **not** required.
11. `DISCOVERY_FRONTIER` authority and `DiscoveryAuthority@1.0.0` closure for the frozen exact-bounded 46-candidate program.
12. Support/validation rules and whether the current P2 manifest/HQ governing act is competent to freeze them.
13. Replay protocol authority/deterministic replay roots.
14. Any target-use permission actually required by the execution path; classify absent-but-unneeded target-use layers as E rather than inventing them.
15. Any source-release/C11 refs that must exist before candidate execution versus refs that are produced by A/B/C candidate work.

## Ownership analysis

For every B/C/D row identify the competent owner category, not merely a filename:

- source-semantic owner;
- routing/risk-set owner;
- source-universe/current-binding owner;
- generic PRE553 grammar owner;
- HQ/Verkhovod benchmark-frontier owner;
- replay-protocol owner;
- mechanical objectization/issuer.

If current HQ Lock 1 is sufficient governing authority for the **benchmark/search frontier**, say so explicitly while preserving the prohibition on HQ inventing WVS response/routing semantics.

## Required outputs

Write only under `WORKER_RETURNS/EE-P2F1/`:

1. `00_RETURN.md`
2. `01_REQUIRED_PRE553_AUTHORITY_MATRIX.json`
   - exact required object/authority rows from current code;
   - operation, family, scope, dependency and exact reason.
3. `02_EXISTING_WVS_AUTHORITY_INVENTORY.json`
   - accepted current authority/evidence surfaces;
   - adoption/currentness/authority ceiling;
   - exact refs/hashes/commits/paths.
4. `03_REQUIREMENT_TO_AUTHORITY_CROSSWALK.json`
   - one classification A/B/C/D/E per required row;
   - exact supporting authority/evidence;
   - no vague `missing semantics` labels.
5. `04_MINIMUM_PRE553_ISSUANCE_ENGINEERING_PLAN.md`
   - only B rows;
   - exact mechanical objects/snapshots/adapters needed;
   - must add zero new semantic propositions.
6. `05_MINIMUM_NEW_AUTHORITY_PLAN.md`
   - only C/D rows;
   - distinguish authority adoption from genuinely new evidence gathering;
   - identify competent owner and exact evidence needed.
7. `06_LOCK2_WAKE_DECISION.json`
   - whether Lock 2 can be closed by mechanical issuance alone;
   - or which exact authority-production precursor(s) are required first.
8. verifier and verification receipt sufficient to prove matrix completeness and classification exhaustiveness.

## PASS / blocker semantics

A successful audit need not find that all authority already exists. PASS means the authority problem is **fully decomposed and no requirement remains vaguely characterized**.

Preferred terminal forms:

- `EE_P2F1_PASS__ALL_WVS_P2_REQUIREMENTS_CLASSIFIED__MECHANICAL_PRE553_ISSUANCE_ONLY`
- `EE_P2F1_PASS__ALL_WVS_P2_REQUIREMENTS_CLASSIFIED__BOUNDED_AUTHORITY_ADOPTION_PRECURSORS_REQUIRED`
- `EE_P2F1_PASS__ALL_WVS_P2_REQUIREMENTS_CLASSIFIED__GENUINE_NEW_AUTHORITY_EVIDENCE_REQUIRED`

If current repo/authorized exact evidence cannot even determine the authority requirement itself, return the smallest exact meta-blocker.

## Hard prohibitions

- no WVS SAV/source outcome access;
- no A/B/C execution;
- no performance measurement;
- no candidate ranking;
- no Lock-1 workload/candidate/metric redesign;
- no PRE553 object minting or AuthoritySnapshot issuance in this worker;
- no new semantic proposition merely to satisfy a schema;
- no routing inference from observed values;
- no new WVS Candidate-C accelerator;
- no MAIN mutation;
- no semantic PRE-MAIN mutation;
- no replacement branch;
- no rebase.

Commit and push the governed return on the exact commissioned branch.
