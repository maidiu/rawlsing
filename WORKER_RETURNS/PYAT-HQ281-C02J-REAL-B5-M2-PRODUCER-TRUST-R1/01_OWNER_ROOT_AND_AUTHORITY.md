# C02J — Owner root and authority: the verifier-held principal

## The principal

The verifier is an `OwnerHeldB5Verifier` instance constructed once, in the
trusted harness, holding:

1. **The exact M2Repository object** (`held_repository()`, identity via `id()`).
   Never passed by any caller; never addressable from any request field.
2. **A frozen per-slot expected product identity** (21-key closed map,
   `MappingProxyType`, derived from the held repository at construction).
3. **A frozen replay/authority scope**: accepted M2 grade vocabulary, per-slot
   required grade, revocation ledger (all frozen at construction).

## The anchors (owner-authentic, not toy)

1. **M2 content-addressing** (accepted owner): `resolve_release_exact` refuses
   refs whose `content_hash` does not match stored content. A caller cannot
   present content for a hash it does not hold. Every expectation key that is
   a content hash (`release_content_hash`, `semantic_projection_hash`,
   `determinant_set_hash`, `m2_release_projection_hash`) inherits this.
2. **Constructor-held references**: the repository object and frozen maps are
   bound at construction. The data-only caller (one slot string) has no field
   through which to substitute them.
3. **Frozen type map**: `EXPECTATION_KEY_TYPES` is a module-level
   `MappingProxyType`. There is no mutable map to weaken.
4. **Re-resolution at every check**: observed identity is rebuilt from the held
   repository immediately before comparison, so post-authoring M2 mutation is
   detected (demonstrated: mutated-repo publish refused).

## Jurisdiction

- **Verifier holds**: repository identity, frozen expectation, replay scope,
  revocation sets, event authority/rule refs used on the verifier path.
- **Accepted B5 owner holds**: well-formedness gates (replay closure presence,
  semantic authority presence, determinant presence), event ordinals and
  append-only ledgers, checkpoint structural checks.
- **Accepted M2 owner holds**: content binding, closure completeness, grade
  declaration.
- **Nobody holds (HELD)**: producer issuance, ceiling validation, independent
  expectation authorship, replay re-execution, current selection, G0b/G1/V3.

## What the overlay guards (all mutating entrypoints)

`stage_release`, `stage_protocol`, `register_product`, `publish_product`,
`record_recertification`, `select_current`, `declare_no_current`,
`from_checkpoint` (B5) and `register_producer_subject`, `constitute_release`
(M2). Read-only resolution (`selection_key`, `resolve_selection_exact`,
`lifecycle_state`, `export_checkpoint`) is intentionally unwrapped: it
publishes nothing. Cutover order: build material, construct verifiers, register
them, then activate. Post-cutover, unknown releases, foreign repositories and
foreign checkpoints are refused before any accepted owner is invoked.
