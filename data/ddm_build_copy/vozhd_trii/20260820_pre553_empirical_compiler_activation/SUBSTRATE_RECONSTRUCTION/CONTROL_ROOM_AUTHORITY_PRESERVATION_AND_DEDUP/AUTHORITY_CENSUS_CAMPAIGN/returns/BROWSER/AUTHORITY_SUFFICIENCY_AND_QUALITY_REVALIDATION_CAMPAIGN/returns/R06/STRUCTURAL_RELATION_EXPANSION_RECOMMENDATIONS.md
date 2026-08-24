# R06 — Structural / Relation Expansion Recommendations

These are **non-dispositive preservation recommendations**. They do not create new relation authority, source semantics, or runtime objects. [TIR-003, TIR-019, TIR-020, TIR-024, TIR-025, TIR-026–TIR-043, TIR-045]

## 1. Preserve direct implementation and source-structure identity separately

Relation members should continue to reference exact P2 implementation identity and named source-structure objects directly. QSR row identity, normalized/casefold coordinate, display name, or helper parent key must not substitute for implementation identity. [TIR-003, TIR-024, TIR-025]

For LiTS III, every bridge that touches the seven case-collision groups must retain exact case-sensitive identity. [TIR-003, TIR-024]

## 2. Preserve relation roles, applicability, evidence ceilings, and blockers

A structural/relation object is not sufficiently explained by a member list alone. Downstream relation authority should retain or exact-reference, as governed:
- member implementation IDs;
- source-structure / battery / parent-child identity;
- member roles and direction where actually authorized;
- applicability/routing conditions;
- respondent composability / anti-join state;
- evidence ceiling and prohibited inference;
- explicit block/noncomparability state;
- provenance to the O03/O04/FQRA/QSMv2 authority that licensed the assertion. [TIR-007, TIR-019, TIR-020, TIR-024, TIR-025, TIR-026–TIR-043, TIR-045]

This preserves the distinction between **implementation identity** and **structural/relation authority**. [TIR-003, TIR-025]

## 3. Do not expand FQRA merely to eliminate target absence

The 26 P2 implementations outside FQRA remain valid P2/source implementations. Add them to a relation target only if a governed relation requirement proves they belong there. “P2 exists” is not a relation predicate. [TIR-003, TIR-025]

Likewise, do not resolve the nine FQRA blocked joins through guessed aliases. [TIR-003, TIR-020, TIR-025]

## 4. Treat QSR-only rows as residue until exact semantic binding exists

The 518 unique QSR-only keys may remain useful as structural/access evidence, source locators, or documentary residues. They should not become new semantic implementations or relation members merely because they are structurally convenient. [TIR-003, TIR-024, TIR-025]

## 5. Keep QSM retirement gated by information-class succession, not file replacement

R06 confirms that source-structure membership and relation-topology classes have active successor surfaces. It does not prove that every same-grain QSM information class—especially evidence ceiling, forbidden inference, review/block history, and full joint composability—has passed quality revalidation. Global QSM retirement therefore remains outside R06's authority. [TIR-019, TIR-020, TIR-024, TIR-025, TIR-026–TIR-043, TIR-045]

## 6. Preserve typed Joint Evidence states

The R00 595-row requirement-by-source-wave audit is not a binary relation inventory. `PARTIALLY_OBSERVABLE`, `ROUTING_BLOCKED`, `SEMANTIC_ONLY_NONCOMPOSABLE`, and `NOT_OBSERVED` are semantically material source/capability states. Future structural relation products must not upgrade these states into positive respondent composability or silently discard them as missing. [TIR-020, TIR-026–TIR-043, TIR-045]

## 7. TIR-014: separate topology authority from occurrence-identity proof

Source-native first/second ranks, repeated blocks, checklist children, multiselect groups, and battery membership are real structure when source-certified. But the existence of those structures does not by itself prove that every identity-bearing C11 semantic occurrence field is a deterministic function of retained source determinants. [TIR-013, TIR-014, TIR-024]

HQ should run `BLE-R06-014-A` before making any persistence or derivability claim from TIR-014. A positive exact FD certificate may reduce the information that must persist; a nonderivability result may establish independent occurrence information. R06 chooses neither outcome in advance. [TIR-014, TIR-064]

## 8. Expansion after the first local court must be hazard-driven

If `BLE-R06-014-A` finds a nonempty exception class or a determinant not represented in source-native coordinates, expand only to exact R14-certified source objects sharing that hazard. Candidate documentary domains already known to contain occurrence-sensitive topology include WVS Wave 4 ranking pairs, EVS 1981/1990/1999 ranking or multiselect structures, and LiTS I/2006 Q3.14 checklist children. Their existence alone is not sufficient to launch a second court. [TIR-013, TIR-014, TIR-024]

## 9. Do not let later bridge incompleteness retroactively erase valid upstream authority

Where later structural/composability bridge surfaces are incomplete, repair the missing downstream role/composability/evidence-ceiling link. Do not reinterpret that incompleteness as proof that current source-backed R10F O03/O04 is invalid. Upstream authority and downstream completeness are distinct propositions. [TIR-024, TIR-025]

## Proposed expansion posture

- new semantic implementation population from QSR residue: `NO`
- automatic FQRA target widening for 26 absences: `NO`
- guessed repair of nine FQRA blocks: `NO`
- broad raw-source occurrence crawl: `NO`
- exact bounded WVS7 TIR-014 FD court: `YES__BLE-R06-014-A`
- later occurrence-domain expansion: `CONDITIONAL_ON_EXACT_HAZARD_FROM_FIRST_COURT`
