# RAWLSING GOVERNANCE PACKET R2 CONTRACT

R2 is a machine-only cross-field enforcement wrapper over the unchanged R1 Grounding Receipt, Work Return, and Central State Update schemas. It does not alter semantic, architectural, runtime, or authority law.

`PACKET_VALID` answers whether the packet is structurally honest and internally/live-state consistent. `ADOPTION_ELIGIBLE` answers whether the requested effect can acquire adoption/banking authority. `PROJECT_CLOSURE_ELIGIBLE` answers whether closure claims are structurally admissible. These are distinct.

The validator MUST load every R1 schema and `GOVERNANCE_PACKET_SCHEMA_R2.json`; resolve the canonical PRE-MAIN ref from Git rather than packet data; parse the live Ground version; load canonical authority levels, open obligations, scope requirements, anti-resurrection gates and protected-target map; and fail closed on missing/unknown/contradictory data.

Bounded execution inherits evidence context from one exact verified grounded project-decision receipt but never inherits the parent's authority. It may only return bounded execution, obtain no new authority, make no closure claim, and preserve all forbidden reinterpretation tokens.

Scope exclusions are explicit non-closure declarations: excluded obligations remain open. Domain-required obligations cannot be excluded.

A successor must have one explicit return edge per successor. A touched obligation must have exactly one typed disposition in both return and central-state update. `all([])` is never proof of accounting.

Anti-resurrection enforcement is two-layered: gate IDs must be real, and structured authority effects are checked against protected targets. Acknowledgement alone cannot legalize a forbidden promotion.
