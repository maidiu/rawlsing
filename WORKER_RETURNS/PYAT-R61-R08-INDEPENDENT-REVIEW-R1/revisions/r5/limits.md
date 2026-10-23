# R61-R08V R5 independent review — limits and retained assumptions

- Scope is the configured trusted-host callable grain only. This is not
  institutional independence, OS isolation or protected capture.
- Full live J42 `E41ProviderAdapter.step`, live P41 progressive and repaired
  live E04 terminal integration remain NOT_REACHED; not waived.
- No original source/science, original-35/1890, global F6/F7/F8, production/CI,
  N11/N12, Sorok, J52/W52, actor or R03/R09 authority is claimed or changed.
- The excluded set fixed before attack remains: private-state reflection,
  monkeypatching trusted host code, deliberate trusted-root replacement by the
  host, ptrace/root, same-UID secret/key inspection, a dishonest competent
  issuer, and an attacker-owned resolver/reader with its own root. Both
  remaining findings use only public candidate APIs/objects and the
  preconfigured verifier; neither is in the excluded set.
- The reviewer did not use author tests as the sole oracle. Positive values were
  recomputed from the pinned AT07 response table and the actual unchanged
  provider; author suite replay is regression evidence only.
- The author's R4 probe failures are not blanket-dismissed: the two failures are
  `EvidenceAssociationError` from the repaired reader (the old probes expected
  the former unsigned 999 service). The two probes were preserved unchanged and
  replayed from blob `80b89a714da02a670c96a69f40706dd8d80df0b5`; no skip or
  TypeError/import/setup failure is counted as safety.
- The verifier-only re-export refusal is recorded as a partial functional
  obligation, not as a served-value bypass.
- No candidate code/test, native owner, archived return, HQ, workflow or config
  file was edited. The reviewer wrote only this r5 ownroot; the sealed log is
  `logs/stdout.jsonl`. The harness's `.r61/r5/stdout.jsonl` is outside the
  reviewer edit root and was not written by this session.
- Same-UID host/key compromise, a dishonest competent issuer and protected
  native capture remain separate future work.
