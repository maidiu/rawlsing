# FIABC-T6 — Generic Parentage Live Binding

## Canonical owner

The canonical parentage law is now exclusively:

`rawlsing_next/fiabc_derivative_parentage.py`

with schemas:

- `FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`.

T4 no longer owns a parallel derivative-parentage schema.

## Governing chain

`CANONICAL RAW SOURCE OBSERVATION`
→ `IMMUTABLE SOURCE-VERIFICATION RECEIPT`
→ `GOVERNED PRODUCER / OPERATION / READER CONFIG`
→ `IMMUTABLE DERIVATIVE RECEIPT`
→ `EXTERNAL SEALED BUNDLE`
→ `EXACT DERIVATIVE IDENTITY`.

The reverse implication is forbidden:

`derivative asserts canonical source SHA`
-/→
`canonical ancestry proved`.

## T4 adaptation

The live accounting bridge exports `require_derivative_parentage(...)` for compatibility with accounting callers, but that function no longer validates a T4-specific receipt.

It:

1. requires a complete exact expected R35 live binding;
2. loads the external generic bundle;
3. calls `verify_parentage_bundle(...)`;
4. derives an accounting summary only after generic verification.

Without an exact expected binding it fails closed.

This preserves T4's safety behavior while removing competing parentage ownership.

## LiTS-I Candidate A

Required external inputs:

- `RAWLSING_EE_P2X_LITS_A_R5_ROOT`;
- `RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT`;
- `RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT_IDENTITY`.

The live backend verifies:

- canonical LiTS-I SHA;
- exact R5 physical-root identity;
- exact member-inventory SHA/byte length;
- logical-stream/root metadata;
- R5 builder identity/blob/version;
- Candidate-A owner blob;
- physical-only reader/config identity;
- derivation operation;
- current projection/runtime/binding/release;
- candidate/root ownership;
- independently pinned derivative-receipt identity.

An old copied carrier or plausible path cannot pass.

The browser implementation does not fabricate the missing historical first-build receipt from current contents.

## WVS7 structural preimage

When the canonical WVS SAV is lawfully available later, the accepted materializer creates the structural preimage only after the live path freezes:

- canonical raw-source verification;
- exact materializer producer/blob/version;
- exact producing operation;
- exact reader config;
- current projection/Lock2 determinants;
- source/candidate/root/process ownership.

The external bundle is persisted beside, but separate from, the structural JSON.

Source-free reopen requires:

- structural JSON;
- external bundle;
- previously frozen bundle/source/derivative/structural identities;
- exact generic verification;
- existing structural self-integrity checks.

A structural self-hash proves only contents, not ancestry.

## Preserved-work accounting

Parentage PASS is necessary but not sufficient for preserved-work numeric credit.

T4 still requires its independent field-by-field metric/workload/runtime/isolation compatibility law.

Thus T6 strengthens provenance without silently converting historical evidence into fresh numeric telemetry.

## Nonclaims

Generic parentage proves provenance only.

It does not authorize:

- semantic text;
- survey meaning;
- source certification;
- weight/default estimand;
- population inference;
- I05 semantic parity.
