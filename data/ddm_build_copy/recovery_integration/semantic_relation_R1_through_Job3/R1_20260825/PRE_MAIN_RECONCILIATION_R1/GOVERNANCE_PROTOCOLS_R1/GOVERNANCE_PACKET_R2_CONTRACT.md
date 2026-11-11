# RAWLSING GOVERNANCE PACKET R2.1 CONTRACT

R2.1 hardens the R2 machine wrapper after the W56B hostile audit. It changes enforcement, not Rawlsing semantic/runtime/architectural authority.

## Positive authorization, never deny-list default allow

Adoptive packets must use an explicitly registered `decision_domain` whose `allowed_requested_effects` includes the requested effect. `GENERAL_PROJECT_DECISION` and `CUSTOM` are non-adoptive. A new adoptive subject therefore requires an explicit governance-scope change before it can be adopted; relabeling specialized work as "general" cannot lower its grounding burden.

Protected authority targets use a closed `requested_effect` vocabulary and an explicit per-target `allowed_promotion_classes` list. Unknown/typo effects fail schema. At this version protected targets permit only `PRESERVE_CURRENT_STATUS`; a future positive promotion requires an explicit, separately audited enforcement-map change.

## Bounded execution

A bounded executor inherits only from one exact immutable **parent governance packet**, not a free-standing receipt. The parent packet must be a schema-valid `GROUNDED_PROJECT_DECISION`, current to the live canonical head/Ground, adoptive in the same registered decision domain, and fully satisfy that domain's machine grounding requirements. Child state/obligation scope must be a subset of the parent. Bounded execution never inherits the parent's authority.

## Successor-parent openness

Every successor-return edge carries `successor_id`, `parent_obligation_id`, and `return_to`. Every parent obligation must be touched and disposed `SPAWNED_SUCCESSOR_RETURN_REQUIRED`; the work return must itself remain in that reintegration status. Outstanding successors and terminal parent dispositions cannot coexist.

## Terminal disposition evidence

`CLOSED` and `ABANDONED_BY_EXPLICIT_DECISION` are terminal dispositions. Each requires an immutable `<40hex>:<repo-path>` closure-evidence packet validating against `CLOSURE_EVIDENCE_SCHEMA_R1.json`. The evidence packet is bound to the exact obligation, canonical closure condition, competent closure authority, authorizing Grounding Receipt ID, and immutable evidence refs. Bare paths, branches, tags, mutable working-tree files, and arbitrary prose do not satisfy terminal disposition.

The machine verifies identity/binding, not intellectual sufficiency.

## Governance self-modification

The paths in `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv` are meta-governance. The validator compares the executing working-copy blobs against the same paths at the live canonical PRE-MAIN SHA. If they differ, `GOVERNANCE_SELF_INTEGRITY = false` and **no adoptive effect is machine-eligible**.

This is intentional: a candidate enforcement implementation cannot validate its own adoption. Enforcement changes must be candidate-local, independently hostile-audited, and then adopted by competent external canonical-ref succession. Once integrated, the new canonical copy becomes the validator allowed to govern later ordinary packets.

A worker may never weaken governance and use the weakened candidate validator as proof of its own adoption.
