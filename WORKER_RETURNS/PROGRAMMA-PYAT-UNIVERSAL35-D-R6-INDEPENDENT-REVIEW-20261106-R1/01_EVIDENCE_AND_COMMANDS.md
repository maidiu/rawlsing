# D r6 evidence and commands

## D actual production-wrapper probe

Sourcefree TEST_ONLY_SOURCEFREE SAV/config, selected `A/B/Y`, coordinate `G`;
actual `execute_native_compiler_source`, current compiler/facts, no mocks.

- Positive resolver `A,A,A`: 30 facts / 15 expected ops / 18 candidates;
  anti and op-anti true; `native=false`.
- Old ABBA after extra-pre-call removal (`B,B,A`): refused
  `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`.
- Changed post-consumer decision `A,A,B`: refused.
- Revoked before: refused `SOURCE_READ_NOT_CURRENT: REVOKED`.
- Revoked after: refused `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`.
- Exact restore `A,A,A`: accepted with the same 30/15/18 result.

The R6 `_RecordingResolver` captures `dataclasses.asdict` at admission calls; the
first captured decision is the decode-approved decision; no extra wrapper pre-call.

## F local-read resolver probe (Git copy, not edited)

Extracted F `local_engineering_resolver.py` to own scratch; used only
metadata/config requests, no source bytes.

- Actual grant SHA `9e433cd95600c0634b38a08781eea851086fc8208739a6f29e6c83bbe58a88c7`;
  auth SHA `18b2b57188a91a4af25c53b67c0e1ff1c8b848ac823c2d3391a1a72e5517edb4`.
- Durable F commission and custody anchor bytes match the grant refs; user authorization bytes match. Valid decisions: 35/35. SRC09 decision retains host `oldMac.lan`, purpose
  `UNIVERSAL35_ORIGINAL_ENGINEERING_RAW`, consumer use, RAW scope, currentness,
  and retention/export/publication limits.
- Refused mismatches: host, purpose, consumer, scope, source SHA, source format,
  custody locator.
- Cached-instance live checks: after grant currentness/revocation change,
  existing instance still ACCEPTED; after auth file change, existing instance
  still ACCEPTED. `_current` only reads the cached interval.
- Fresh default resolver (expected hashes enabled): after grant revocation
  `SOURCE_READ_LOCAL_ENGINEERING_GRANT_CHANGED_OR_REVOKED`; after auth change
  `SOURCE_READ_USER_AUTHORIZATION_CHANGED`; missing auth
  `SOURCE_READ_USER_AUTHORIZATION_MISSING`; valid fresh input accepted.
- Fresh-load composed use therefore refuses changed/revoked/missing inputs
  before any source I/O; the cached instance is not accepted for the D run.

## Preserved floors

- Current route-qualified frontier 7 / 694 / 683 eligible / 11 held; 28
  no-explicit sources.
- Historical non-F1 scope 20 / 991 retained.
- Route 676 / 4,705 / 249; plan 18,276 items / 18,413 slots / 18,467 operations.
- Prior G held-Y positive and selected-missing refusal unchanged; no eligible
  operation dropped.

## Boundaries

No original source read, actual D original run, 600 s decode, full-estate floor,
E/native handshake, native facts, science, all35 or protected acceptance. No
product/test/guide/progress/controller edit or code repair.
