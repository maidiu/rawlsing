# C02H — Unadopted Owner Diff and Competent Adoption Packet

## Required changes (UNADOPTED petition)
1. Adopt a producer issuer with RSA (or stronger) keypair, separate from producer and caller
2. Modify M2.register_producer_subject / constitute_release to require issuer credential
3. Modify B5.LearnedProductLifecycleExecutor to require PerimeterTicket + issuer credential verification
4. Modify C02 expectation to be issuer-held (break R3 tautology)
5. Establish a trust root held by separate-principal verifier

## Holds
- OWNER_ISSUER_HOLD: no competent issuer exists
- DEMO_ONLY: RSA demo is not production crypto
- ENFORCEMENT-SURFACE HOLD: boundary is test-only overlay
- G0b/CURRENT HOLD: no operative grants
