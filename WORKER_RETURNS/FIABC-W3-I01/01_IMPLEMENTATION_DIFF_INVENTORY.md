# FIABC-W3-I01 — Implementation / Diff Inventory

Base: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`

## Production delta

### `rawlsing_next/pre553_diagnostics.py`

New bounded current PRE553 diagnostic successor.

Primary public call surfaces:

- `produce_governed_diagnostics`
- `replay_governed_diagnostics`
- `assert_diagnostic_only_use`
- `GovernedDiagnosticProduct`

Implemented mechanics:

- exact contingency extraction from governed I03 joint facts;
- entropy reduction;
- mutual information;
- normalized mutual information;
- Cramér's V;
- per-cell uplift/lift;
- optional exact-component F018 joint-confidence diagnostic;
- exact fact/query/release/authority/provenance/replay determinant binding;
- content-addressed replay and product identities;
- recursive freezing of identity-bearing product material;
- fail-closed malformed-joint handling;
- typed negative-state propagation;
- explicit diagnostic-only use gate.

Semantic ownership change: **none**.

Existing production files modified: **none**.

Historical V550/V550J modules imported as runtime owners: **none**.

## Test delta

### `rawlsing_next/tests/test_pre553_diagnostics.py`

New focused hostile test module. Expected pytest cases after parameter expansion: **21**.

Coverage includes:

- exact perfect-association F012 calculations;
- deterministic replay identity;
- F018 joint-confidence exact determinant binding;
- refusal to default confidence determinants/effective-N inputs;
- changed confidence inputs changing replay/product identity;
- preservation of NONCOMPARABLE / UNAVAILABLE / UNRESOLVED / INTEGRITY_FAILURE / VALID_EMPTY;
- explicit UNDERPOWERED determinant requirement;
- UNCERTAINTY_UNQUANTIFIED preservation;
- positive unary -> NOT_APPLICABLE rather than zero association;
- malformed arity-2 contingency -> fail closed;
- exact release provenance requirement;
- missing exact authority -> fail closed;
- fact/query identity mismatch -> fail closed;
- diagnostic product immutability;
- attempted diagnostic -> EmpiricalFact promotion rejected;
- attempted diagnostic -> structural admission rejected by I04;
- computed NMI attempting to control I05 frontier rejected;
- semantic/source/structural authority-role attempts rejected.

## Scope proof

Diff is intentionally limited to:

1. one new production module implementing IMP01/IMP03;
2. one new focused test module;
3. this worker return package.

No HQ handoff, decision ledger, candidate binding, parity oracle, equal-work instrumentation, succession preflight, terminal verifier, source semantic authority, or measured execution surface is mutated.
