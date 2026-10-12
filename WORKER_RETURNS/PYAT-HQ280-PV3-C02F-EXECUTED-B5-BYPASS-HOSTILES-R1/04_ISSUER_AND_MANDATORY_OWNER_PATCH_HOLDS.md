# C02F — Issuer and Mandatory Owner Patch Holds

## What a mandatory adopted owner change would need
1. **Trust principal** — an issuer that signs/attests PerimeterTicket and ProducerCredential so callers cannot forge them
2. **Independent checkpoint validator** — verifies checkpoint hashes without trusting caller's self-computed hash
3. **Owner adoption** — accepted B5/M2 owners modified to require these credentials (currently UNADOPTED)
4. **Tautology closure** — C02 expectation authored independently of construction it authenticates

## Holds (nonissuing)
- PRODUCER-ISSUER HOLD: no accepted issuer exists
- ENFORCEMENT-SURFACE HOLD: boundary is test-only overlay
- DEMO-FIXTURE TICKET ≠ AUTHENTICATION: caller-supplied dataclass satisfies type requirement but is not issuer authentication
- REPLAY HOLD: REPLAY_COMPLETE is owner-held claim
- AUTHORITY HOLD: AuthoritySnapshot refs are owner-held
- G0b/CURRENT HOLD: no operative grants
