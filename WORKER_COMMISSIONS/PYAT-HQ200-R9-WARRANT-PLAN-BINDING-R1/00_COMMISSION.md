# PYAT HQ200 — generic warrant-plan binding + outer route-pass accounting — R1

Repository: maidiu/rawlsing

Role: source-free implementation worker — Space Bunny

Branch:
agent/rabochii-pyat-hq200-r1

Implementation base / HQ199 session candidate:
90ccbd54c549f67358d0c02ad18ff90b843cf3ee

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ200-R9-WARRANT-PLAN-BINDING-R1/
- /WORKER_RETURNS/PYAT-HQ200-R9-WARRANT-PLAN-BINDING-R1/
- /rawlsing_next/
- /WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/
- /WORKER_RETURNS/EE-P2R6S/
- /WORKER_RETURNS/FIABC-LM2/

Read these authorities by exact Git object:
- HQ200 adjudication e7ce39dade6b169ab068f5f786b7a0dea06846dd
- seven-source plan 09e1325da6ee880374a4065ae748cc03de93c421
- independent scope review 302d4a5da513381e26066cea70bf3ec5be7d3636

Do not clone. Do not create a full checkout.

The exact startup SHA is the commission-tip SHA after this file is committed.

## Mission

Build the generic binding layer that turns a caller-supplied warrant/source-entry specification into exactly one governed source execution.

Do NOT hard-code SRC02/SRC06/etc in production.

The generic GovernedSourceSession already exists. This lane adds the missing outer workload account and a typed bound execution wrapper above it.

## Required outer account

Add a separately typed FULL ROUTE PASS account.

It must NOT be stored or described as:
- decoder_invocations;
- full_reads;
- chunk_reads;
- reader_invocations;
- path_opens.

Recommended shape may vary, but the runtime/receipt must expose at minimum:
- full_route_passes_observed;
- full_route_passes_max;
- full_route_passes_expected or expected-status if supplied;
- whether the pass completed successfully;
- provenance/plan identity where appropriate.

For an execution bound with max 1:
- a second full-route pass attempt must be refused before any second source operation;
- lower-layer accounts must remain unchanged on refusal.

For a failed first pass:
- do not falsely report a completed pass;
- retries remain governed separately.

## Bound execution specification

Introduce the smallest generic immutable spec/wrapper needed to bind:

- source_entry_key;
- source path;
- expected SHA-256;
- source format;
- SourceOperationPlan;
- SourceAccessBudget;
- outer full-route-pass expected value if supplied;
- outer full-route-pass maximum if supplied;
- optional expected/min/max constraints for lower-layer accounts;
- authority/policy status labels sufficient to keep historical expectation distinct from implementation maximum.

Do not bake source keys or source-specific variable names into generic production code.

The caller supplies the exact plan.

## Count semantics from HQ200

Implement these semantics exactly:

- expected, minimum/floor, maximum, and observed are distinct.
- a policy MAX 1 decoder_invocations is not a frozen expected count.
- SRC27's full_reads historical authority is FLOOR >=1, not EXACT 1.
- SRC27's full_route_passes is EXACT 1 / MAX 1.
- path_opens historical expected count is UNBOUND.
- a one-open policy ceiling is allowed only as a clearly typed implementation policy if the caller supplies it.
- chunk_reads never substitute for full_reads.
- full_route_passes never substitute for decoder/full/chunk/reader/open accounts.

## Generic constraint checker

Add generic pre/post validation sufficient to support a bound warrant plan:

Pre-operation:
- maxima/zero ceilings refuse before the relevant operation;
- the outer full-route-pass max refuses before a second pass.

Post-operation:
- exact/floor expectations supplied by the bound spec are checked against observed receipt;
- missing required minima/exacts fail closed;
- a successful execution cannot silently return with a frozen exact/floor account unsatisfied.

Do not invent constraints the caller did not provide.

## Session ownership

The bound execution wrapper should create exactly one GovernedSourceSession and own its deterministic close.

The source session remains generic.

The wrapper must not permit:
- swapping the operation plan after binding;
- replacing the budget after binding;
- silently opening a second session for the same bound execution;
- raw-path fallback.

## Synthetic seven-plan conformance court

Using synthetic SAV/DTA only, instantiate seven caller-supplied specs that reproduce the documentary source-plan SHAPES without hardcoding them into production:

- selected single-variable SAV, no prefix;
- selected two-variable SAV, no prefix;
- metadata-only declared-encoding SAV, no prefix;
- second metadata-only declared-encoding SAV, no prefix;
- selected exact-variable SAV, no prefix;
- metadata-only SAV + 176-byte prefix;
- full declared-encoding DTA + outer full-route pass exact/max1.

For the SRC27-shaped synthetic plan demonstrate:
- one completed full_route_pass;
- metadata read >=1 according to supplied floor;
- full_read >=1 according to supplied floor;
- decoder max1 policy;
- path opens reported separately;
- second outer pass refused before any second source operation;
- chunk_reads do not satisfy the full-read floor.

The tests may name SRCxx; production code may not.

## R7 requalification

Because production code changes, rerun the fixture-complete exact six-file court:

Interpreter:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

Environment:
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<worktree root>

pytest:
-p no:cacheprovider

Collect exactly 55; run twice; target 55/55 twice.

Also run:
- session courts;
- broker courts;
- new bound-execution/route-pass courts.

## Write terrain

Only:
- rawlsing_next/pre553_source_session.py
- rawlsing_next/pre553_source_access_broker.py if strictly necessary
- one narrowly scoped new rawlsing_next/pre553_*execution_binding*.py module
- rawlsing_next/tests/**
- WORKER_RETURNS/PYAT-HQ200-R9-WARRANT-PLAN-BINDING-R1/**

No source-specific production constants.

## Allowed dispositions

Exactly one:
- WARRANT_PLAN_BINDING_CANDIDATE_READY_FOR_INDEPENDENT_REVIEW
- ROUTE_PASS_OWNER_PARTIAL
- CONSTRAINT_MODEL_INSUFFICIENT
- R7_REQUALIFICATION_FAILURE
- MATERIAL_NEW_COUNTEREXAMPLE

No self-adoption.

Commit, push, re-fetch, verify.

Terminal:
HQ200_R9_WARRANT_PLAN_BINDING_RETURNED__HQ_REVIEW_REQUIRED

No real source access, locator discovery, warrant issuance, live C4, C7 or actor/person work.
