# PYAT HQ280 PV3 C02E — Authentic Issuer and Rehydration Trust Contract

**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`

## The Mandatory Authority Act

The smallest competent owner jurisdiction that makes **every** operative publication and restore path go through one mandatory producer-authentic/permission-scoped gate is the **accepted B5 owner (`LearnedProductLifecycleExecutor`)** and the **accepted M2 owner (`register_producer_subject`, `constitute_release`)**.

No new trust root, issuer, key registry, or signature scheme is created. The enforcement binds the existing M2 content-addressing to a producer-issued credential, and binds the B5 owner to a mandatory perimeter ticket.

## Exact Requirements

### 1. B5 Owner — Mandatory Perimeter Ticket

Every public method of `LearnedProductLifecycleExecutor` MUST require a valid `PerimeterTicket`:

- `__init__(perimeter_ticket)` — constructor requires ticket
- `stage_release(subject)` — requires valid ticket matching subject slot
- `register_product(...)` — requires valid ticket
- `publish_product(...)` — requires valid ticket
- `select_current(...)` — requires valid ticket
- `declare_no_current(...)` — requires valid ticket
- `from_checkpoint(checkpoint, checkpoint_authority)` — requires independent authority

**Refusal:** `PerimeterTicketError("PERIMETER_TICKET_REQUIRED")` raised BEFORE any B5 logic executes.

### 2. M2 Owner — Mandatory Producer Credential

`register_producer_subject` and `constitute_release` MUST require a `ProducerCredential`:

- `register_producer_subject(repository, ..., producer_credential)` — requires valid credential covering the subject
- `constitute_release(repository, ..., producer_credential)` — requires valid credential covering the release subject

**Refusal:** `ProducerCredentialError("PRODUCER_CREDENTIAL_REQUIRED")`

### 3. Rehydration — Independent Checkpoint Authority

`from_checkpoint` MUST require an independent `CheckpointAuthority`:

- The checkpoint hash must be verified against an independent authority's verification hash
- The caller's self-computed hash (`checkpoint_hash == semantic_hash(payload)`) is NOT authentication

**Refusal:** `CheckpointAuthorityError("CHECKPOINT_AUTHORITY_REQUIRED")` or `("CHECKPOINT_HASH_INDEPENDENT_VERIFICATION_FAILED")`

### 4. Frozen Expectation Type Gate

`EXPECTATION_KEY_TYPES` in the C02 candidate MUST be frozen as `MappingProxyType` to prevent runtime type-gate weakening (C02R F4).

## What Is NOT Required

- No new trust root, issuer, or key registry
- No cryptographic signing without a threat-model/issuer assessment
- No G0b, G1, CURRENT, or actor/V3 grants
- No self-adoption, no canonical mutation
- The C02 optional facade remains available but is superseded

## Residual Holds (Not Granted)

| Hold | Description |
|------|-------------|
| PRODUCER-ISSUER HOLD | No accepted issuer/credential exists; M2 registration is unauthenticated |
| ENFORCEMENT-SURFACE HOLD | Perimeter not yet mandatory in adopted owners (test-only patch) |
| REPLAY HOLD | `REPLAY_COMPLETE` remains owner-held claim |
| AUTHORITY HOLD | Semantic AuthoritySnapshot refs remain owner-held |
| G0b/CURRENT HOLD | No operative grants |

## Patch Overlay Specification

The exact minimal changes to make enforcement mandatory at the adopted owners are recorded in `PATCH_OVERLAY_SPEC` in `pre553_b5_mandatory_boundary_candidate.py`. The test-only overlay `repro/b5_mandatory_patch.py` demonstrates these changes at runtime.

**No accepted source file is modified.** The patch is applied only at test runtime.