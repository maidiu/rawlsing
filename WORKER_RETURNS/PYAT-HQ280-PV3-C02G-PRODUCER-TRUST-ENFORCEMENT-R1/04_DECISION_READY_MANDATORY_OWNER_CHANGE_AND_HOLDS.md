# C02G — Decision-Ready Mandatory Owner Change and Holds

## Required changes (UNADOPTED petition)
1. Adopt a producer issuer (separate principal, trust root, signed credentials)
2. Modify M2 registration to require issuer credential
3. Modify B5 to require PerimeterTicket + issuer credential verification
4. Modify C02 expectation to be issuer-held (break R3 tautology)
5. Establish a trust root held by separate-principal verifier

## Holds
- OWNER_ISSUER_HOLD: no competent issuer exists
- ENFORCEMENT-SURFACE HOLD: boundary is test-only overlay
- DEMO-FIXTURE TICKET ≠ AUTHENTICATION
- REPLAY HOLD: REPLAY_COMPLETE is owner-held claim
- AUTHORITY HOLD: AuthoritySnapshot refs are owner-held
- G0b/CURRENT HOLD: no operative grants
