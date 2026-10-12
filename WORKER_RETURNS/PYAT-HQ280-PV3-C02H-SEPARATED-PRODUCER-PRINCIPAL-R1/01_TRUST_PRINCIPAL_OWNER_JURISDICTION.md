# C02H — Trust Principal and Owner Jurisdiction

## Separate principals demonstrated
- ISSUER: holds RSA private key, signs credentials, revokes
- VERIFIER: holds RSA public root, verifies signatures, checks scope/revocation
- CALLER: presents subjects, cannot mint credentials or swap root
- ATTACKER: no access to private key or verifier root

## Jurisdiction
- Issuer jurisdiction: credential issuance and revocation
- Verifier jurisdiction: credential verification and scope checking
- Owner jurisdiction (B5/M2): must require verified credentials (UNADOPTED)

## What accepted owners must change
- M2 registration: require issuer credential with valid RSA signature
- B5 lifecycle: require PerimeterTicket whose issuer credential verifies
- C02 expectation: must be issuer-held, not derived from subject
