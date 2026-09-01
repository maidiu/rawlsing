# FINAL RULING

`BLOCKED__BOUNDED_PARENT_SHALLOW_GROUNDING`

First failed gate: `W56D-G4`.

The candidate does **not** satisfy the commanded requirement that a bounded child fail when its parent packet belongs to a different decision domain. The contract says the parent must be adoptive in the same registered decision domain; the implementation validates the parent's own domain and child relevant-ID subsets but never compares parent domain to child domain. `PHYSICAL_ARCHITECTURE` can therefore act as parent for `PHYSICAL_PERSISTENCE` while satisfying the explicit subset predicates. Governance enforcement is not yet fail-closed enough for PRE-MAIN.

Independent additional blocker: `W56D-G9/G10`. The canonical-predecessor meta-validator protects its own blob identity but does not authenticate independent hostile-audit provenance and treats any ruling containing `READY` as pass-like. A descendant self-authored JSON audit can therefore counterfeit the separation the change protocol says is the enduring security boundary.

Other commanded attack families are statically closed at their specified machine grain: generic/custom domain adoption, closed authority-effect vocabulary, successor-parent openness, typed terminal evidence, unknown/blocked terminal normalization, immutable-ref form, CLI adoptive failure, self-application, machine-overreach, and jurisdiction diff.

PRE-MAIN remains `8b13b67df8f055761b432191eca564c1840250ec`.
main remains `0777a34e50221bde6801dbaca26c058a7350c9e8`.

Terminal token:

`W56D_FINAL_HOSTILE_W56C_AUDIT_BLOCKED__W56D-G4__NO_PREMAIN_INTEGRATION`

Do not integrate W56C.