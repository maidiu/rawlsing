# SELF-MODIFICATION ATTACK

## Candidate-side ordinary validator

Static ruling: **SAFE for direct self-adoption**.

The protected-path manifest includes the schemas, scope registry, anti-resurrection map, contracts, helper library, ordinary validator, and meta-validator. `enforcement_integrity(live_sha)` compares the candidate working-copy blob for every protected path against the same path at live canonical PRE-MAIN. Because W56C changes/adds protected files relative to `8b13b67d...`, candidate-side `GOVERNANCE_SELF_INTEGRITY` is false and ordinary `ADOPTION_ELIGIBLE` is false.

## Canonical-predecessor meta-validator

Static ruling: **BYPASS REMAINS**.

The script correctly refuses to run authoritatively unless its own working blob equals the live canonical predecessor blob. This closes the narrow attack in which a future candidate modifies the meta-validator and executes the modified copy as proof.

But the next boundary—independent hostile audit—is not authenticated:

- audit evidence need only be immutable JSON;
- its Git commit must descend from the candidate;
- candidate binding is a self-declared JSON field/token;
- the ruling is treated as pass if it starts with `PASS`, contains `_PASS`, **or contains `READY`**;
- there is no hostile-audit schema, authorized auditor identity, branch/ref separation, or external attestation predicate.

Therefore a future enforcement candidate can leave the canonical predecessor meta-validator untouched, add a self-authored descendant JSON object that names the candidate and uses a pass-like/`READY` ruling string, and obtain `EXTERNAL_INTEGRATION_ELIGIBLE=true` from the predecessor gate. The meta-validator is canonical, but the supposed independent hostile evidence is counterfeit.

Classification: `GOVERNANCE_SELF_MODIFICATION = BYPASS`.

This is an independent blocker even though the overall W56D ruling is keyed to the earlier `W56D-G4` bounded-parent failure.