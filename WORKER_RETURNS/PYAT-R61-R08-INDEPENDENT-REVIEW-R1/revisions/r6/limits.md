# R61-R08V R6 independent review — limits and retained assumptions

- Scope is the configured trusted-host callable grain only. This is not
  institutional independence, OS isolation or protected capture.
- Full live J42 `E41ProviderAdapter.step`, live P41 progressive and repaired
  live E04 terminal integration remain NOT_REACHED; not waived.
- R01 High adjudication is separate and was neither inspected nor decided.
- No original source/science, original-35/1890, global F6/F7/F8, production/CI,
  N11/N12, Sorok, J52/W52, actor or R03/R09 authority is claimed or changed.
- The excluded set fixed before attack remains: private-state reflection,
  monkeypatching trusted host code, deliberate trusted-root replacement by the
  host, ptrace/root, same-UID secret/key inspection, a dishonest competent
  issuer, and an attacker-owned resolver/reader with its own root. The R6
  finding uses only public cache/import/export APIs, a self-rehashed public
  seal, and the configured verifier.
- Positive values were recomputed from the pinned AT07 response table and the
  actual unchanged provider; author tests are regression evidence only.
- The R4 probe replay 7/2 and R5 probe replay 6/2 are accounted for: the two R4
  failures are lawful `EvidenceAssociationError`; the two R5 failures are old
  expectations for the removed unsigned `cache_trust_grade` and for downstream
  import refusal after export already refused. No TypeError/import/setup failure
  is counted as safety.
- The local delivery label is explicitly unsigned and can be influenced by
  `EvidenceResult.provenance`; signed original provenance/mode and served
  values are unaffected. It was recorded but not scored as a separate defect.
- Verifier-only re-export without the original ephemeral cache issuer drops the
  optional `issuer_grade`/`issuer_seal` local label; signed envelope/signature
  and served values are preserved. Not a grade upgrade.
- Author 38/38 is not independent qualification; the author export-object test
  has a non-isolated evidence restoration (60 vs original 6), as recorded.
- No candidate code/test, native owner, archived return, HQ, workflow or config
  file was edited. The reviewer wrote only this r6 ownroot. The harness log path
  `.r61` is outside the permitted edit root; the sealed log is
  `logs/stdout.jsonl`.
- Same-UID host/key compromise, a dishonest competent issuer and protected
  native capture remain separate future work.
