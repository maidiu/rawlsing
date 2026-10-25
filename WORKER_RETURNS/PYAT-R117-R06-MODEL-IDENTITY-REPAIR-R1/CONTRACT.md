# R117 pre-code contract — shared prefix model identity

Status: frozen before the R117 code commit. Same R112 branch/startup
`73b7d62c391f444a0dd4cd60532ac071543ac14d`. Only the two R06 code paths are
written; the R112 native successor owner/test and all earlier returns remain
read-only.

## Repair

`_progressive_prefix_identity` must compare an exact model identity derived from
each prefix's existing `PositionedSubjectPossibilityModelRule`: its
`rule_hash` plus the canonical existing `material()` (model/walkback authority
refs, source universe refs, walkback steps, proxy authority refs, rule and
algorithm ids). All prefixes in one progressive chain must share this identity
and the same source universe/release/risk/repository. A mismatch registers a
typed invalid context; `progressive_world_view` refuses
`PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH` before serving. No invented
model merging/issuance; a consistent shared alternate model remains valid.

## Preserved

R112 native per-prefix `product.nonparent.consume` (world routes + exact source
support + N10E hashes), R115 owner-derived rows identity, mandatory source
repository, mixed-prefix repository guard, R110 empirical/world revocation and
N10E binding, condition/value/world mutation, unlike shapes, cold replay,
minority/zero/actor firewall, and R109/R111/R116 probes. Sourcefree finite-shape
only; no original/source/science/actor/R09/CI/prod/N11/N12/Sorok/J52/W52.
