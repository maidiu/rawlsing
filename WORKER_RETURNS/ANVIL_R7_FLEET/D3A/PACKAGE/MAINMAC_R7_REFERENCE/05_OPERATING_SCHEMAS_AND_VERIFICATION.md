# 05 — One executable vocabulary, evidence content and honest receiving

## Source of exact literals

`contracts/policy.json` governs claim, graph, scope, measurement, source and stage enums and exact physical floor. `contracts/source_registry.json` holds the 118 distinct historical/SEAM/boundary/terminal IDs and K3 source-pinned references; source snapshot `7fc00289dd801d2d0a8ce159986c7595fc27a4d9` is historical, not a permanently current HEAD. `contracts/boundaries.json` holds seven explicit boundary contracts. `reference/ANVIL_R5_IMMUTABLE.zip` is full exact 45-entry R5 archive with 44 hashed listed payloads and manifest, **not an R7 runtime rule**. OldMac's stronger case×metric floor and raw-bytes approach are integrated in R7 policy and code; my R6's source-value typing and clean launch roles are likewise integrated. No R4/R5/R6 amendments may override R7 launch semantics.

All runtime artifacts use `ANVIL_R7_*_1` schema names. Original R5 executable interfaces may be consulted for historical diagnosis but are not alternative launch validators. R7's unique executing contract is `tools/r7.py`, Python 3 stdlib only. `tools/test_r7.py` creates fake receipt bytes **on purpose** to ensure invalid data are rejected. `tools/preflight.py` verifies package structure, original R5 manifest/payloads, compiled code, runnable tests, and launch vocabulary. `tools/package.py` creates and re-reads every archive payload and manifest digest. If a required file is absent, the quality gate returns RED; do not handwave a partially repaired copy as the shipped artifact.

## The CLI, starting from the ZIP root

```sh
python3 tools/test_r7.py -q
python3 tools/preflight.py
python3 tools/fixtures.py fixtures
python3 tools/r7.py check-plan fixtures/SYNTHETIC_PLAN.json
python3 tools/r7.py compare fixtures/SYNTHETIC_PLAN.json fixtures/SYNTHETIC_MEASUREMENTS.json --evidence-root fixtures
python3 tools/r7.py check-spine fixtures/SYNTHETIC_SPINE.json fixtures/SYNTHETIC_PLAN.json fixtures/SYNTHETIC_MEASUREMENTS.json --evidence-root fixtures
python3 tools/r7.py check-claim path/to/real_selected_source_claim.json
python3 tools/r7.py check-graph path/to/proposed_global_SPINE.json
python3 tools/r7.py check-handoff path/to/first_consumer_card.json
python3 tools/r7.py amend path/to/previous_frozen_plan.json path/to/amended_pre_result_plan.json
python3 tools/r7.py check-stage C path/to/C_review.json --evidence-root path/to/evidence
python3 tools/r7.py check-stage H1 path/to/H1_owner_receipt.json --evidence-root path/to/evidence
python3 tools/r7.py render path/to/SPINE.json output/derived
python3 tools/r7.py check-render output/derived
```

**Amended plans** must supply their immutable original frozen plan via `--parent path/to/parent_plan.json` to `compare` and `check-spine`. A run without a parent for `version>1` is RED. No `--phase final`, no `A_PROVED_AT_SCOPE`, `B_PROVED_AT_SCOPE` or contradictory alias: only `P15_DECISIVE_SCOPED`, `P15_CONDITIONAL`, `P15_EXACT_HOLD`.

## Required receipt content and source proof grades

A raw measurement receipt under `--evidence-root` must parse as JSON `ANVIL_R7_MEASUREMENT_RECEIPT_1` and give `candidate` A/B, `cell_id`, `metric`, exact `fixture_hash`, `runner_identity`, code `code_head`, `grade`, interval `low`/`high`, `sample_count`, source ref, methodology/host, and actual described positive, denied and restored behavior, `design_frozen_head` matching the distinct A0/B0 identity, `mechanism_signature` and typed `unit=BYTES|SECONDS`. RSS above the 6 GiB selected cap contradicts a PASS veto regardless of other measured wins. Evidence map points at its **relative local path and exact SHA-256**. A rehashed arbitrary text or rehashed JSON claiming the wrong candidate/metric/interval is RED. The checker demands both sides on each frozen cell for a positive numerical verdict. It cannot verify physical origin from bytes alone; C checks the real runner and source host.

A nonnumeric veto document `ANVIL_R7_VETO_WITNESS_1` must identify **its candidate A or B**, veto ID, exact selected scope, qualified source/owner/evidence grade, `PASS_AT_STATED_SCOPE` and negative/restoration/limitation; all **14** candidate×veto witness documents are required for a fully compared scope. An unexecuted rights/actor/science veto remains held; do not invent a PASS by filling the fields. A ready R7 spine also demands exact source semantic evidence `ANVIL_R7_SEMANTIC_WITNESS_1` for routing, k-way/denominators and cold negative/restoration, including correct scope and witness ID.

## Stage contract

`H0`: `H0_FROZEN|H0_EXACT_HOLD`. `A0/B0`: blind frozen head or exact hold. `A1/B1`: reciprocal frozen opponent head or exact hold. `P15`: `P15_DECISIVE_SCOPED|P15_CONDITIONAL|P15_EXACT_HOLD`. `P2`: `P2_PROPOSED_READY|P2_PROPOSED_CONDITIONAL|P2_EXACT_HOLD`; author builder grade `PENDING_INDEPENDENT_C`. `C`: `C_ACCEPT_SCOPED|C_ACCEPT_DOCUMENTARY_HOLD|C_REVISE_EXACT_DEFECTS|C_DECISION_BLOCKED_EXACT`, qualified current/future builder cards. `H1`: `H1_RECEIVED_SCOPED|H1_RECEIVED_CONDITIONAL|HQ_CURRENTNESS_HOLD|H1_REJECT_EXACT_DEFECT` only under qualified owner plus live CAS and paired progress. Source rights, scientific, actor and engineering grades are separate flags, never inferred.

**C result must include:** frozen P2 HEAD, full frozen author `SPINE.json` byte-digest, exact frozen plan and actual A/B raw-receipt-based measurement object, recomputed comparator result, same selected candidate and first handoff, and the strongest surviving objection with real refuting frozen cells. C re-reads files through `reviewed_artifacts.{plan,measurements,comparison,spine}` each with relative path and SHA-256, **parses their contents and recomputes comparison + spine validation**. If version >1, include `parent_plan` exact bytes. An optional owner-predeclared tradeoff is not accepted until C supplies separate adjudication of objective, bounded losses and B's counterargument. If C has a still choice-reversing objection, `C_ACCEPT_SCOPED` is forbidden.

**H1 result must include:** actual parsed `ANVIL_R7_STAGE_1` C review from its exact file hash, same C head/verdict/P2/consumer grades, and parsed `ANVIL_R7_CAS_READBACK_1` receipt identifying the project-selected PRE-MAIN branch, expected parent, observed post-CAS SHA, paired progress MD/JSON hashes, authority and external live readback locator. The checker rejects arbitrary text, valid JSON of the wrong schema, content agreeing only in the filename, a contradictory C verdict or a fabricated held→buildable grade. H1 must independently verify source receipts and live GitHub origin, real reviewer distinctness, real owner jurisdiction and actual protected integration. A synthetically consistent local H1 JSON **cannot authenticate a real protected commit**. For `H1_RECEIVED_CONDITIONAL`, provide `authenticated_product_delta` pointing to parsed `ANVIL_R7_PRODUCT_DELTA_1` with distinct real before/after `ANVIL_R7_EFFECT_RECEIPT_1` files (hashes, source, same actual consumer and materially distinct effect digests). C receipt must identify the exact independently verified delta and same before/after hashes; otherwise conditional receiving is RED. A textual assertion of progress is not a delta. These tests only verify content consistency; an independent receiver checks real positive/negative/restore and product novelty against H0.

`H1_RECEIVED_SCOPED` without actual external confirmation is always a claim awaiting verification, never evidence that this ZIP merged anything.

## Generated author handoff

From one tested `SPINE.json`, `render` deterministically produces: `DESIGN_DECISION.md`, `GLOBAL_ARCHITECTURE.json`, `DOWNSTREAM_BUILD_HANDOFF.jsonl`, `REQUIREMENT_CONSERVATION.jsonl`, `EVIDENCE_AND_FALSIFIERS.tsv`, `OPERATIONAL_HANDOFF.md` and `RENDER_SHA256.json`. Every one of the 118 inherited IDs is exported **at its inherited status**, not rewritten as new implemented functionality. All architecture-changing source obligations must be linked to real selected decisions or held with exact first-consumer consequence; existence of 118 rows is *not* a substantive functional-conservation certificate. `check-render` rejects edited generated output. Before H1, C must demonstrate one source-selected historical function of actual product consequence, rather than merely IDs preserved.

## Scope of every green test

All positives in `fixtures/` are deliberately synthetic and arbitrary; the supplied small sourcefree fixtures never prove any live original35, external rights, real 100k CPU/RSS, economic superiority, real C independence, or protected currentness. A SHA/JSON **proves file identity within the supplied directory**, not true execution or authorization; `PASS_STRUCTURAL_ONLY_NOT_AUTHENTICATED` is the only local pass grade. This qualification must survive copying the package or relaying agent returns.
