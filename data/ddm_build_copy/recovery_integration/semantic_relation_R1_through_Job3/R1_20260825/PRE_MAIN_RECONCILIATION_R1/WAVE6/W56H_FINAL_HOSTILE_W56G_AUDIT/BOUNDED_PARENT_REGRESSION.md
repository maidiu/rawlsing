# BOUNDED-PARENT REGRESSION

W56G does not modify the ordinary governance-packet validator relative to the audited W56E baseline.

The current ordinary validator still makes bounded parent validity depend explicitly on:

`(parent or {}).get("decision_domain") == domain`

before parent deep-grounding and child relevant-state/relevant-obligation subset checks.

Thus `PHYSICAL_ARCHITECTURE -> PHYSICAL_PERSISTENCE` fails regardless of subset overlap, while lawful same-domain narrowing remains expressible subject to the already-existing deep-parent and non-escalation predicates.

Classification: `PASS`.