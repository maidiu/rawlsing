# C02J — Proposed mandatory patch: exact smallest line-level owner diff (UNADOPTED)

**Status: UNADOPTED test-only overlay. No accepted source file is modified in
this branch.** The overlay `repro/c02j_mandatory_overlay.py` applies the below
at runtime only. This document is the exact line-level change a competent
owner decision would need to adopt.

## 1. `pre553_learned_product_lifecycle.py` — `LearnedProductLifecycleExecutor`

For each of `stage_release`, `stage_protocol`, `register_product`,
`publish_product`, `record_recertification`, `select_current`,
`declare_no_current`: at method entry, resolve the presented release through
the verifier registry (`_RELEASE_REGISTRY[release_ref.key]`); refuse unknown
releases (`UNKNOWN_RELEASE`) before any owner logic; then verify the presented
subject's own fields plus the re-resolved held-repo identity against the
frozen per-slot expectation (`IDENTITY_AUTHENTICATION_FAILED` on mismatch).
`select_current`/`declare_no_current` additionally require the release to be
PUBLISHED (owner's existing check, unchanged).

For `from_checkpoint` (classmethod): after the accepted rehydration logic,
require every rehydrated subject's release to resolve through a registered
verifier and pass the frozen-expectation check (`CHECKPOINT_UNRESOLVED`
otherwise). Caller-authored checkpoints whose subjects live in no held
repository are refused even when their self-computed hash matches.

`__init__` is intentionally UNCHANGED: no constructor ticket, no credential
parameter. There is nothing for a caller to present.

## 2. `pre553_learned_product_release.py` — M2 registration

For `register_producer_subject` and `constitute_release`: at function entry,
require the supplied repository object to be held by a registered verifier
(identity via `id()`: `_REPO_REGISTRY[id(repository)]`); refuse foreign
repositories (`UNREGISTERED_REPOSITORY`) before any owner logic. No credential
parameter is added: there is no credential surface at all.

## 3. What is NOT changed

- No new parameters on any accepted method or function.
- No new modules imported by accepted owners.
- No change to event ordinals, ledgers, checkpoint schema, closure semantics,
  content hashing, replay grades, or selection state machines.
- Read-only paths (`selection_key`, `resolve_selection_exact`,
  `lifecycle_state`, `export_checkpoint`, `determinant_graph`) unchanged.

## 4. Adoption prerequisites (competent acts, none taken here)

1. A competent owner decision adopting verifier-held mediation as the sole
   operative ingress (cutover: build, construct, register, enforce).
2. A revocation-operating procedure (the ledger is currently harness-held).
3. A principal decision on the ceiling and tautology holds (see 04): either a
   competent issuer for the ceiling, or recorded acceptance of self-declared
   ceilings as out of scope; either an issuer-held expectation source, or
   recorded acceptance of the freeze-plus-re-resolution posture.
