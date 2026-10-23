# R61-R08V R7 independent review — limits

- Scope is the configured trusted-host callable grain only; not credential,
  institutional or OS independence.
- The only scored defect is the lost explicit legacy-pin migration code on a
  cache-hit `resolve`; no support/measurement/ownership/admission/root/live-
  producer bypass was found.
- A wrong `trusted_descriptor_hashes` on a cache-hit `resolve` likewise reports
  generic `UNKNOWN`; import/export report `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`.
  The contract requires enforcement on replay (it is enforced, no support) but
  does not name a distinct replay code.
- Full live J42 `E41ProviderAdapter.step`, live P41 progressive and repaired
  live E04 terminal integration remain NOT_REACHED; future-owner work, not
  waived.
- Author 126/126 is regression evidence, not independent qualification. The
  independent R7 table covers all 13 owner classes and the API chain; the one
  failure is the legacy replay code.
- The extracted fixtures were verified byte-for-byte against original startup
  blobs; the harness only redirects fixture path constants and does not change
  implementation, evaluator, provider or expected oracle semantics.
- R6 immutable 9/2, R5 6/2 and R4 7/2 outcomes are accounted for. R6/R5
  failures are removed-transport/local-grade superseded expectations; semantic
  adapters preserving the same invariants pass 3/3. R4 failures are lawful
  `EvidenceAssociationError` from the repaired path.
- Original35/1890/global F6/F7/F8, source/science/CI/prod, N11/N12, Sorok,
  J52/W52, R03/R09 and original data holds remain unchanged. No adoption, author
  wake, candidate edit, new session or provider/account change.
