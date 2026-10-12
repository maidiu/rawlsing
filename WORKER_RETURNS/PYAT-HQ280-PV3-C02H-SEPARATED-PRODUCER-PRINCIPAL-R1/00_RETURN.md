# PYAT HQ280 PV3 C02H — Separate-Principal B5 Producer Authentication

**TERMINAL:** `HQ280_PV3_C02H_INDEPENDENT_PRODUCER_PRINCIPAL_DEMO_AND_OWNER_PETITION_OR_EXACT_HOLD__NONOPERATIVE__GITHUB_PUSHED`

**Disposition:** `SEPARATE_PRINCIPAL_DEMO__OWNER_ISSUER_HELD__NONOPERATIVE`

## What was done
Built the smallest genuinely testable separate-principal demonstration where an issuer controls a credential-verification root the caller cannot substitute, self-register or rewrite. Uses ephemeral RSA keypairs (DEMO_ONLY, not production crypto).

## Results (13 cases, all from real invocations)
- UNPATCHED: raw B5 publishes forged subject (PUBLISHED), B2b forged subject publishes
- SEPARATE_PRINCIPAL_DEMO:
  - Genuine issuer credential verifies (RSA signature against trusted root)
  - Forged credential refused (SIGNATURE_INVALID)
  - Root swap refused
  - Self-registered issuer refused
  - Revoked issuer credential refused (ISSUER_REVOKED)
  - B2b forged subject refused (SUBJECT_FORGERY_REFUSED)
  - C2 self-derived expectation refused (EXPECTATION_TAUTOLOGY_REFUSED)

## Key finding
The separate-principal demo proves the trust boundary is enforceable when an issuer holds a private key and a verifier holds the corresponding public root. The caller cannot forge credentials, swap the root or self-register. However, this is DEMO_ONLY with ephemeral RSA — no competent production principal exists. The real principal and signed authority are HELD.

## Residual holds
OWNER_ISSUER_HOLD. No G0b, G1, CURRENT or V3 grant. No self-adoption. No canonical mutation.
