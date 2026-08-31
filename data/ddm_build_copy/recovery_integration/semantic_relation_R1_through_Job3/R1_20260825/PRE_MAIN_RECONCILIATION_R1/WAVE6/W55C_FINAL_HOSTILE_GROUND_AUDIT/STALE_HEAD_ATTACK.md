# Stale-head grounding attack

Ruling: `BYPASS_FOUND`.

The validator does not read the live/canonical Git ref. It sets:

`canonical = packet.get('canonical_project_head', '564feddf...')`

and accepts when the receipt's head equals that packet value plus the self-asserted string `central_state_head_match == 'PASS'`.

Therefore an attacker can supply the same stale SHA in both packet fields and pass `CANONICAL_PROJECT_HEAD_MATCH`, even though the actual audited PRE-MAIN is `8b13b67df8f055761b432191eca564c1840250ec`.

Fixture F05 proves only that two packet fields disagreeing causes failure. It does not test a mutually consistent stale packet against the actual canonical ref.

Ground-version mismatch against the hardcoded current `RAWLSING_GROUND_R1` does fail, but the version is likewise not derived from the live Ground file.
