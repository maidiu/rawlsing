# PYAT HQ190-C — R9 warrant per-access-layer accounting binding — R1

Repository: `maidiu/rawlsing`

Role: **RABOCHII / DOCUMENTARY-FORENSIC IMPLEMENTER — SPACE BUNNY**

Branch:
`agent/rabochii-pyat-hq190-c-r9-warrant-accounting-binding-r1`

Exact implementation base:
`02309f4e708dd01cb0d64666acbe43d5c23b35e7`

The exact commissioned startup SHA is supplied by HQ in the launch directive after this commission commit is published.

Return directory:
`WORKER_RETURNS/PYAT-HQ190-C-R9-WARRANT-ACCOUNTING-BINDING-R1/`

## Mission

Produce the exact **unissued** warrant-accounting successor that closes, or precisely preserves, **R9**, the current sole warrant-instrument technical blocker.

This is source-free documentary/forensic work. It does not issue a warrant and does not discover locators.

Current governing C4 consolidation:
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/02_CURRENT_CONSOLIDATED_DECISION_CLAIMS.md`
- `.../03_CURRENT_CLAIM_EVIDENCE_MAP.json`

Exact subject freeze:
`8ff40d37de69db2d8a6053a7c2242f481677f1a4`

Read the exact historical warrant candidate and accounting/failure law at the freeze. Also read Omega-1 and C4B evidence by exact ref where needed.

## Startup law

Before work:
1. `git fetch origin`;
2. no blind `git pull`;
3. resolve this remote worker branch;
4. verify it equals the exact commissioned startup SHA supplied by HQ;
5. use an isolated worktree at that exact tip;
6. verify a clean tree;
7. stop on any identity mismatch.

## Governing facts to preserve unless exact evidence disproves them

- six of eight workload sources have explicit `expected_full_reads` / `expected_selected_reads` in the relevant accounting artifact;
- SRC27 uses a different law: exactly one governed full Route-B pass, maximum one, zero retries, and its existence/access check, full SHA-256 pass, metadata read and full compatibility read are **separate access accounts**;
- SRC35 is retained-only with `fresh_reads: 0` and is not a fresh-source warrant target;
- seven sources are authorized candidates for eventual fresh access;
- all seven currently have `max_retry_budget: 0`;
- the historical warrant candidate contains zero per-source expected full/selected read counters;
- the correction is an instrument/accounting binding task, not permission to re-derive semantics from sources.

Do not invent an exact per-layer limit where the governing artifacts do not establish one. If the evidence cannot support a lawful bound, return that exact insufficiency.

## Required output

Create a **new candidate**, preserving the historical candidate byte-for-byte.

At minimum create:
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/07_R9_WARRANT_ACCOUNTING_SUCCESSOR_CANDIDATE.json`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/08_R9_ACCOUNTING_BINDING_CROSSWALK.md`

The successor candidate must remain unmistakably:
- unsigned;
- unissued;
- non-authorizing;
- no raw access permitted;
- locator placeholders unfilled.

Do not overwrite the historical warrant candidate.

## Per-source/per-layer binding

For every eventual fresh-source target, bind the expected measurement basis and enforceable limit at the layer actually governed by the evidence.

Distinguish, where applicable:
- existence/access check;
- full-byte hash pass;
- metadata/header read;
- selected/bounded physical read;
- full compatibility/full-route read;
- retries;
- materialization/frame construction.

For SRC27, preserve the one-full-route-pass/max-one/zero-retry law while making the lower-layer access accounting explicit rather than collapsing it into "one open."

For the six sources with existing explicit counters, carry their exact established values and provenance.

For SRC35, preserve zero fresh access and explain why it is outside the fresh-source warrant target set.

Do not convert an operation-level pass budget into a fabricated OS-open count.

## Candidate safety invariants

The candidate must retain explicit fields equivalent to:
- `signed: false`
- `issued: false`
- `authorizes_access: false`
- `execution_authorized: false`

All locator slots remain explicit placeholders.

No field may imply that creating this candidate authorizes hashing, statting, metadata reads or file opens.

Compute and record the successor candidate's complete SHA-256.

## Warrant blocker inventory

Produce a machine-readable inventory distinguishing:
- technical R9 closure;
- locator prerequisites;
- user/resource-owner approval prerequisites;
- signature/issuance act;
- R7/live-runtime prerequisite;
- independent integration-review prerequisite.

For the historical "independent integration review not yet completed" item, collect the exact current evidence (Sol final review, ALT-B, R2 re-check, HQ187/HQ190 consolidation review), but **do not make the authority decision yourself** about whether that issuance prerequisite is discharged. Mark it `HQ_ADJUDICATION_REQUIRED`.

## No source operations

Zero locator discovery.
Zero raw source stat/hash/open/decode/materialization.
Do not inspect directories to find sources.
Do not execute C4.
Do not fill any placeholder from local knowledge.

## Allowed write terrain

- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/07_R9_WARRANT_ACCOUNTING_SUCCESSOR_CANDIDATE.json`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/08_R9_ACCOUNTING_BINDING_CROSSWALK.md`
- `WORKER_RETURNS/PYAT-HQ190-C-R9-WARRANT-ACCOUNTING-BINDING-R1/**`

Do not edit:
- historical warrant candidate;
- historical C4 returns;
- `rawlsing_next/**`;
- `HQ_HANDOFF/**`;
- source custody records.

## Required return packet

At minimum:
- `00_RETURN.md`
- `01_INPUT_IDENTITY_MAP.json`
- `02_PER_SOURCE_ACCESS_LAYER_LIMITS.json`
- `03_SUCCESSOR_CANDIDATE_VERIFICATION.json`
- `04_ISSUANCE_PREREQUISITE_INVENTORY.json`
- `05_LIMITATIONS_AND_UNRESOLVED.json`
- `06_FINAL_DISPOSITION.json`

Allowed dispositions:
- `R9_ACCOUNTING_BINDING_CANDIDATE_READY_FOR_INDEPENDENT_REVIEW`
- `R9_EVIDENCE_INSUFFICIENT__WARRANT_BLOCKER_REMAINS`
- `R9_MATERIAL_CONTRADICTION_FOUND`

If you claim R9 closed at the candidate grain, independent hostile review is mandatory before HQ removes the warrant-instrument blocker.

## Return-to-HQ law

Commit the substantive result and return packet to this worker branch; push to `origin`; re-fetch and verify local HEAD equals the remote branch tip.

Return artifacts bind the stable substantive candidate/result SHA. Do **not** chase a self-referential enclosing branch-tip SHA.

Report:
- branch;
- exact pushed remote tip SHA;
- substantive candidate/result SHA;
- disposition;
- terminal token.

Do not merge into control or self-adopt.

## Holds

Zero raw-source access.
Zero locator discovery.
Zero warrant issuance.
Zero live C4.
Zero C7.
Zero actor/person implementation.

Terminal:
`HQ190_C_R9_WARRANT_ACCOUNTING_RETURNED__HQ_REVIEW_REQUIRED`
