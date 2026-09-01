# CODE AUDIT

Exact candidate: `1ec2dea4c418455aa28523eed57164a6bf5c756d`.

## Positive findings

- Top-level requested effects and nested authority-effect classes are closed vocabularies in schema and code.
- Generic/custom decision domains are non-adoptive; specialized domains constrain touched state/obligation IDs and allowed requested effects.
- Successor packets now bind every successor to a parent obligation, require the parent touched disposition `SPAWNED_SUCCESSOR_RETURN_REQUIRED`, require matching reintegration status, and forbid terminal parent disposition while successors remain.
- Terminal closure/abandonment requires a typed immutable JSON evidence packet bound to exact obligation, terminal status, canonical closure condition, competent closure-authority string, authorizing grounding receipt ID, and immutable evidence refs.
- Immutable refs are 40-hex Git object identities with optional exact tree path; bare paths, branches, tags, short SHAs, and mutable working-tree locators do not qualify.
- Ordinary validator CLI returns nonzero for adoptive requests unless `ADOPTION_ELIGIBLE` is true.
- Protected enforcement paths are enumerated and candidate-side self-integrity compares working-copy blobs to live canonical PRE-MAIN blobs.

## Blocking finding 1 — bounded-parent domain equivalence is not enforced

`GOVERNANCE_PACKET_R2_CONTRACT.md` states that the parent must be adoptive in the **same registered decision domain** and that child scope is a subset of that parent.

`parent_packet_grounding_ok(parent, ...)` validates the parent's own declared domain, scope registry, schemas, live head, Ground version, authority ceiling, active-obligation accounting, anti-resurrection IDs, and return destination. The caller then checks child `relevant_state_ids` and `relevant_obligation_ids` are subsets of the parent receipt.

But neither function receives/compares the child's `decision_domain` against the parent's. Thus:

- parent domain = `PHYSICAL_ARCHITECTURE`;
- child domain = `PHYSICAL_PERSISTENCE`;
- child required states `N006;N010;N012` are included in parent required states `N004;N006;N010;N012;S037`;
- child required obligations `OBL001;OBL037` equal the parent required obligations.

All explicit subset predicates can be true while the domains differ. The W56D command requires this case to fail. It is therefore a code-proved bypass.

The same seam means parent validation is not a full recursive validation of the exact invariants the ordinary validator applies to a grounded project decision; e.g. the helper does not re-run successor, terminal-evidence, authority-effect, touched-disposition, reintegration, and full return-path checks as one complete parent-packet judgment.

## Blocking finding 2 — hostile-audit authentication in meta-validator is fail-open

`validate_enforcement_candidate_from_canonical.py` correctly verifies that the executing meta-validator blob equals the live canonical predecessor copy, that the candidate descends from live canonical, and that the audit evidence is immutable JSON descended from the candidate.

However:

1. it does not authenticate auditor identity/independence or require a hostile-audit schema;
2. `AUDIT_RULING_PASS` is true when `ruling.startswith("PASS")`, contains `_PASS`, **or merely contains `READY`**;
3. exact-candidate binding is satisfied by a JSON field/token supplied by that audit object.

A candidate author can therefore add a descendant immutable JSON object such as a self-authored audit with exact candidate binding and a pass-like string containing `READY`, then invoke the canonical predecessor meta-validator. The modified candidate copy is not used, but the supposed independent hostile evidence can be counterfeit. The durable predecessor/auditor/ref-movement separation is therefore not machine-enforced.

## Overall

The enforcement is materially stronger than W56A, but it is not fail-closed enough for PRE-MAIN. First failure: `W56D-G4`; independent additional failures: `W56D-G9` and `W56D-G10`.