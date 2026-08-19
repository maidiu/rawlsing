# SCRV3 — Hostile Test Oracle

A conforming implementation MUST pass every fixture below. Any fixture marked `REJECT` or `ZERO_EFFECT` is fail-closed.

| ID | Hostile case | Required verdict |
|---|---|---|
| HV3-001 | PSEPF supplied but metabolism-authority ref missing | `ZERO_EFFECT__METABOLISM_AUTHORITY_MISSING` |
| HV3-002 | Authority present but matrix denies transition | `ZERO_EFFECT__INPUT_USE_DENIED` |
| HV3-003 | Matrix allows surface but owning V3 rule has no empirical-use binding | `ZERO_EFFECT__RULE_BINDING_MISSING` |
| HV3-004 | Thin input embeds joint mass/configuration/support/J-way geometry | `REJECT__THIN_INPUT_COPIED_GEOMETRY` |
| HV3-005 | PSEPF ref/hash cannot dereference exact source-indexed J-way/minority/multimodal geometry | `INTEGRITY_FAILURE__ZERO_EFFECT` |
| HV3-006 | Two source negatives `DECLARED_NONE` and `UNSPECIFIED` are collapsed to null | `REJECT__NEGATIVE_STATE_COLLAPSE` |
| HV3-007 | Mixed sources disagree and implementation chooses modal/majority source as actor state | `REJECT__SOURCE_DISAGREEMENT_TO_ACTOR_STATE` |
| HV3-008 | `field.mass` assigned directly to belief probability/state scalar | `REJECT__DIRECT_EMPIRICAL_ASSIGNMENT` |
| HV3-009 | Modal response selected as actor response without owning V3 rule | `REJECT__MODAL_CELL_SHORTCUT` |
| HV3-010 | PSEPF used as encounter/exposure/route/interaction/rupture witness | `REJECT__NONCAUSAL_PRIOR_AS_CAUSAL_PARENT` |
| HV3-011 | `ActorComparatorReceipt` added to actor priors or mutation inputs | `REJECT__COMPARATOR_RECEIPT_SEMANTIC_UPGRADE` |
| HV3-012 | `ReplayReceipt` grants read/mutation authority | `REJECT__REPLAY_RECEIPT_AUTHORITY_UPGRADE` |
| HV3-013 | Objective comparator-relevant actor fact changes; V3 silently retargets old field | `REJECT__UPSTREAM_REQUERY_REQUIRED` |
| HV3-014 | Same field remains valid; only new V3 decision binding/causal-parent receipt required | `PASS__V3_REBIND_NEW_ENVELOPE` |
| HV3-015 | Source interval no longer comparable to decision time; implementation uses latest field anyway | `ZERO_EFFECT__TEMPORAL_NONCOMPARABLE` |
| HV3-016 | Future proxy is backdated into earlier actor history | `REJECT__RETROACTIVE_REWRITE` |
| HV3-017 | Lifecycle `STALE/REFRESH_REQUIRED/INVALIDATED/UNAVAILABLE` but PSEPF changes transition | `ZERO_EFFECT__NONCURRENT_INPUT` |
| HV3-018 | PSEPF creates candidates before CAN-008/010/011/012 owner establishes lawful candidate set | `REJECT__EMPIRICAL_CANDIDATE_CREATION` |
| HV3-019 | Owner uses PSEPF weight without exact versioned formula/content hash | `REJECT__UNGOVERNED_EMPIRICAL_NUMERIC_MAP` |
| HV3-020 | ADP-020 reads PSEPF directly or invents candidates/weights | `REJECT__RNG_SEMANTIC_OWNERSHIP_THEFT` |
| HV3-021 | `ResolvedStructuralContext` copied inside `V3EmpiricalPossibilityInput` | `REJECT__PEER_PRIOR_COLLAPSE` |
| HV3-022 | Generic merged prior erases structural-vs-empirical authority provenance | `REJECT__PEER_PRIOR_COLLAPSE` |
| HV3-023 | Same PSEPF + same structural prior, different lawful causal histories -> different outcomes | `PASS__LAWFUL_DIVERGENT_LIVES` |
| HV3-024 | Exact same priors + ordered history + rule hashes + scheduler + RNG + intake/replay receipts produce different result | `REJECT__NONDETERMINISTIC_REPLAY` |
| HV3-025 | Exact replay uses mutable latest, wall clock, filesystem/container order or unrecorded RNG | `REJECT__HIDDEN_AMBIENT_STATE` |
| HV3-026 | Structural-context final function signature guessed before SCR5578 closes | `REJECT__PREMATURE_FINAL_SEAM` |
| HV3-027 | All local burdens pass and only SCR5578 signature is absent | `SCRV3_WAITING_ONLY_FOR_EXACT_FINAL_SEAM` |

## Oracle invariant

The oracle distinguishes **availability of empirical evidence** from **authority to use it** and from **authority to mutate actor state**. Those three gates may never collapse.
