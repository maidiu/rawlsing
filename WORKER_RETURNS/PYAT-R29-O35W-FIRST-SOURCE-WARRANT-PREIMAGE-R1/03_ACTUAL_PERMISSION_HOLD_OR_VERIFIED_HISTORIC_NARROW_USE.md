# Actual permission: historical narrow use vs new-processing HOLD

## Decision

**`VERIFIED_HISTORIC_NARROW_USE` — SRC02 / Afrobarometer R5 / GT2 Q86B→Q86A
CONTEXT only.**

**`ACTUAL_PERMISSION_HOLD` — every new original-source processing operation,
including any new R5 native I03/I05/Batch, any raw SAV/DTA read, and all 34 other
waves.**

These are not the same permission. The historical use is real and proven; it
does not authorize new processing.

## 1. Verified historical narrow use

The following is supported by retained, exact evidence:

- WGE first retained E2B CONTEXT execution: exit 0, terminal SHA-256
  `269573bf9c69fd0ca2c6d0c018d67dde817132bdc2298c85d9e4304161a759d7`,
  36 cells = 13 observed positive + 23 measured zero, raw numerator sum 19,210.
- WGE-R second independent run: HQ-received receipt records exit 0, 20.43 s,
  the **same** typed terminal `269573bf…`, same 36/23/19,210 geometry.
- Source identity `Data/Afro Barometer Round 5.sav` SHA
  `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`; C11 release
  `R5_GT12_Q86A_Q86B_FROZEN` `8315b104…`; risk set `0484fa5c…`, 19,210.
- Permission ceiling: RAW, SINGLE_UNIVERSE, F1 only, V557
  `ALLOW_CONTEXT_ONLY`, V558 `CONTEXT`, V3 `DENY_ZERO_EFFECT`, no weights, no
  causal/actor/world/person promotion.
- The exact `2ee898…` prospective preimage has been recovered and independently
  recomputed; it is a proposed candidate, **not adopted**.

This verifies **technical operability and historical source-context permission**
at a narrow retained-product grain. It does not verify a new original microdata
operation.

## 2. Actual permission HOLD for new original processing

No currently applicable signed original-source warrant exists in recovered
custody. The 35-wave matrix has **0 verified current signed warrants** and
**0 new original-processing authorizations**.

The exact missing permission objects are:

1. **Named source-data owner/custodian authorization** for the exact source
   family/wave/release/edition/SHA, permitted host, executor, purpose, read and
   output scope, and raw-byte handling. No name, signature, delegation or DUA
   is recorded in Git/retained evidence.
2. **Named GT12-A source-semantics / routing / target-use owner delegation**
   for any extension beyond the existing historical CONTEXT scope.
3. **Named GT12-B/I03 operation-owner delegation** if a new native I03/I05/Batch
   obligation is created. Functional authority refs do not sign new work.
4. **Named E2B publication/consumer owner concurrence** for the exact consumer
   and no-widening ceiling.
5. **Independent prior-to-run expectation custodian** with a named signing
   identity, custody method and pre-run seal.
6. **Competent HQ adoption decision** for the exact `2ee898…` preimage if a
   retained replay is to be expectation-bound.

No Git author identity, repository ownership, or SHA-256 equality substitutes
for any of these.

## 3. Evidence that genuinely does not exist vs merely was not located

| Question | Finding |
|---|---|
| Valid pre-historical original E_pre | **Does not exist** in recovered evidence. WGD `ecb7411003…` is result-derived and retired. |
| Exact `2ee898…` material | **Exists and recovered** from retained WGE ZIP; not tracked in Git. |
| Named source-data signatory | **Not located** in Git/retained archives. Externally may exist; not proven absent. |
| Signed current warrant | **Not located**. C4B has an unsigned template only. |
| Full R5 administered U | **Partial only**; narrow Q86A/B retired universe proven. |
| R5 source SHA | **Historical identity present**; no fresh raw-byte hash or edition check. |
| Raw source files | Not searched/opened. Presence on host is not permission. |
| All-35 U/E_pre | **Missing**; 1 historical narrow root, 34 open. |

## 4. What may be done now

- Cite, audit and hash the retained historical evidence.
- Adopt/reject the exact `2ee898…` preimage by a competent HQ/owner act.
- If adopted, perform **one** retained R5 GT2 CONTEXT replay with the existing
  consumer, no raw source read, no new I03/I05/Batch, and an independent
  pre-run custodian.
- Do **not** open raw SAV/DTA, create a new original native operation, extend
  to other countries/items/waves, or claim new science from the replay.

## 5. Typed hold

`O35W_TYPED_HOLD__NO_SIGNED_CURRENT_ORIGINAL_SOURCE_WARRANT__HISTORICAL_R5_CONTEXT_USE_ONLY__EPRE_2EE898_RECOVERED_PROPOSED_NOT_ADOPTED`
