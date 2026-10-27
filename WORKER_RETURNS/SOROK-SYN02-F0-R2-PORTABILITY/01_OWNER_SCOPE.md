# SYN02 F0-R2 — prospective owner scope record

**Date:** 2026-10-27
**Branch:** `agent/sorok-syn02-f0-r2-source-custody-repair-r1`
**Startup:** `9903a30d8d9cd4594f58c46bec80e538610a1851`
**Commission:** `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_REVIEW_EXECUTION/R2/COMMISSIONS/F0-R2/00_COMMISSION.md` at documentary `2da83f77d820b327169673386d52c4acefbbdd46`.
**Independent review subject:** RF0 `fb8527fa8f182159c96ee95eb49644a649256c70`.

## 1. Approval record

The launch and commission both state that dispatch alone is only a prospective write-scope request and does not grant original S48/S51/S52 owner adoption. Before editing, the implementer searched the workspace and commit record for a separate approval and found none. The user was asked directly whether to approve the enumerated R2 source scope or produce an isolated-only HOLD. The user selected:

> **"Approve enumerated R2 source scope (Recommended)"**

That answer is the prospective owner approval for this bounded F0-R2 tranche. It authorizes only the files and purpose enumerated below. It is not a standing source-owner grant, not a retroactive F0 approval and not a native/production grant.

## 2. Approved prospective R2 scope

The approved scope is the commission's enumerated scope:

- `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48/product.py`
- `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/bootstrap.py`
- `WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/source_binding.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/bootstrap.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/source_registry.py`
- `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/session.py` (approved if needed; **not changed**, because the F0 cold-open repair was preserved)
- preexisting F0 test files under S48/S52 if needed:
  - `.../S48.../tests/test_f0_product_portability.py` (changed)
  - `.../S52.../tests/test_f0_source_portability.py` (changed)
- newly authored R2 tests, portable registry, manifest builder, replay receipts and return under `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/`
- S48/S51 evidence scripts only if exact necessity and a separate owner-approved exception existed. **No evidence script was changed** because no such exception was granted; this is recorded as residual in the return.

Actual source/test changes are enumerated in `00_RETURN.md` and hashed in `02_TEST_RECEIPTS.md`. S48 `__init__.py`, S52 `session.py`, S48 `bootstrap.py`, the evidence scripts, and all C9/C12/CAN/ADP/SCI05/Pyat/production files are unchanged.

## 3. Historical custody not waived

- The original commissioned branch `agent/sorok-syn02-f0-portable-sourcefree-build-r1` remains at `c821b488...`; this R2 branch starts from the separately returned/unadopted `9903a30d...` source as ordered by the commission.
- The old F0 alternate branch's 11-file delivery and its extra-file writes remain a historical branch/extra-file custody issue. This prospective R2 approval does not approve, merge, rebase or absolve that delivery.
- The R2 branch does not adopt the old F0 return. A separate owner/HQ disposition remains required for the historical branch substitution and any eventual integration of the old 11-file set.
- No original author branch, main/PRE-MAIN, source grant, C9/C12 production, CAN/ADP/Pyat/SCI05, provider account or native A5 is changed or authorized.

## 4. Limits of this approval

This approval permits sourcefree engineering and tests only. It does not permit:

- a paid CLI/provider/model call;
- a native C8/C9/C12/C11/A5 run;
- scientific Rule A/T or SCI05 issuance;
- actor/person positivity, source-data execution or production integration;
- self-review or self-adoption by the implementer.

A distinct independent hostile code reviewer must accept the R2 branch before any integration. F1.1 remains gated by independently reviewed RP0 plus competent C9/C12 storage-owner approval.
