# Adoption Ceiling and Repair Target

**Ceiling:** `SOURCEFREE_INTERFACE_EVIDENCE_ONLY` — and only after REDs close.
Current grade: RED. No adoption of any kind.

**Repair target (minimal SC0F2):**
1. Replace import-trace with actual invocation of the three real functions
   under a qualified authority, or gate to `HELD_AUTHORITY` when unavailable.
   The tracer must record real args/result digests, never `sha256(b"imported")`.
2. Replace the attacker-writable module-global registry with an independent
   issuer-signed warrant store; `register_issuer_warrant` must not exist as a
   public unauthenticated mutation. Forged warrants refused unconditionally.
3. Strengthen `test_06` to assert actual 50/10 numerators, denominators, and
   propagation to both readsets.
4. Validate both receipts against the full frozen `oneOf` strict schema;
   remove the `selection_state` COMPLETE default; make `demand_closure`
   independently verified; scope the `fx:scope:town2008` allowlist;
   issuer-validate `earlier_knowledge_evidence_ref`.

**Not required for source-free grade:** real N9/N10W service, EE12, V3, C0 adoption.
**Reviewer independence:** this reviewer is not the SC0F author; a further
reviewer distinct from both SC0F and SC0I windows must adjudicate any SC0F2.
