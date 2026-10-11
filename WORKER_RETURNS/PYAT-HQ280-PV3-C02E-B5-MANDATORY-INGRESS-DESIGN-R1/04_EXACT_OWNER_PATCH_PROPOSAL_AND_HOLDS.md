# PYAT HQ280 PV3 C02E — Exact Owner Patch Proposal and Holds

**Status:** `UNADOPTED_OWNER_SEMANTIC_CHANGE` — test-only overlay, not committed to source branch.

## Minimal Patch to Make Enforcement Mandatory

The following exact changes to the adopted owners would make the mandatory boundary enforced at the owner level. This patch is **not applied to the source branch**; it exists only as the test-only runtime overlay in `repro/b5_mandatory_patch.py` and as the specification `PATCH_OVERLAY_SPEC` in the candidate module.

### 1. `pre553_learned_product_lifecycle.py` — `LearnedProductLifecycleExecutor`

```python
# ADD to __init__ signature:
def __init__(self, perimeter_ticket: "PerimeterTicket" = None) -> None:
    if perimeter_ticket is None:
        raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
            "mandatory boundary: every lifecycle executor requires a PerimeterTicket")
    self._perimeter_ticket = perimeter_ticket

# ADD to stage_release, register_product, publish_product, select_current, declare_no_current:
def stage_release(self, subject):
    if not hasattr(self, "_perimeter_ticket") or self._perimeter_ticket is None:
        raise PerimeterTicketError("PERIMETER_TICKET_REQUIRED",
            "stage_release requires valid PerimeterTicket")
    # ... existing logic

# ADD to from_checkpoint (classmethod):
@classmethod
def from_checkpoint(cls, checkpoint, checkpoint_authority=None):
    if checkpoint_authority is None:
        raise CheckpointAuthorityError("CHECKPOINT_AUTHORITY_REQUIRED",
            "from_checkpoint requires independent CheckpointAuthority; "
            "self-referential hash is not authentication")
    # verify authority's verification_hash independently
    # ... existing logic
```

### 2. `pre553_learned_product_release.py` — M2 registration

```python
# ADD to register_producer_subject:
def register_producer_subject(
    repository, *, producer_credential: "ProducerCredential" = None, **kwargs
):
    if producer_credential is None:
        raise ProducerCredentialError("PRODUCER_CREDENTIAL_REQUIRED",
            "register_producer_subject requires ProducerCredential under mandatory boundary")
    if producer_credential.subject_ref != kwargs.get('subject_ref'):
        raise ProducerCredentialError("PRODUCER_CREDENTIAL_INVALID",
            "credential subject_ref does not match registered subject")
    # ... existing logic

# ADD to constitute_release:
def constitute_release(
    repository, *, producer_credential: "ProducerCredential" = None, **kwargs
):
    if producer_credential is None:
        raise ProducerCredentialError("PRODUCER_CREDENTIAL_REQUIRED",
            "constitute_release requires ProducerCredential under mandatory boundary")
    # ... existing logic
```

### 3. `pre553_authenticated_b5_ingress_candidate.py` — Freeze type gate

```python
# REPLACE line 185:
EXPECTATION_KEY_TYPES = MappingProxyType({
    "release_key": str,
    # ... all 21 keys ...
})
```

## Exact Files to Modify (UNADOPTED)

| File | Change Type | Lines |
|------|-------------|-------|
| `pre553_learned_product_lifecycle.py` | Add `perimeter_ticket` param + checks | `__init__`, `stage_release`, `register_product`, `publish_product`, `select_current`, `declare_no_current`, `from_checkpoint` |
| `pre553_learned_product_release.py` | Add `producer_credential` param + checks | `register_producer_subject`, `constitute_release` |
| `pre553_authenticated_b5_ingress_candidate.py` | Freeze type gate | Line 185 (`EXPECTATION_KEY_TYPES`) |

## Holds (Nonissuing)

| Hold | Description |
|------|-------------|
| PRODUCER-ISSUER HOLD | No accepted issuer/credential exists; M2 registration is unauthenticated |
| ENFORCEMENT-SURFACE HOLD | Perimeter not yet mandatory in adopted owners (test-only patch) |
| REPLAY HOLD | `REPLAY_COMPLETE` remains owner-held claim |
| AUTHORITY HOLD | Semantic AuthoritySnapshot refs remain owner-held |
| G0b/CURRENT HOLD | No operative grants |

**No self-adoption. No canonical mutation. No G0b/CURRENT grant.**