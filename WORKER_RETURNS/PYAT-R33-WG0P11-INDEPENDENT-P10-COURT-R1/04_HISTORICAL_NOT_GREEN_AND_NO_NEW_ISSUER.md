# Historical NOT GREEN and authority ceiling

Both the Phase A P8 replay and the completed P10 replay ran the original tests
without edits. Fresh P10 JUnit lives under
`03_ALL_ACTUAL_FROZEN_NATIVE_AND_COLD_JUNIT/phase_b_remote/`.

- `historical_five_unconstructible.xml`: 5 failures during stimulus construction,
  15 unrelated tests deselected. C3 raises UNKNOWN_RELEASE_NO_REVOCATION for a
  source-artifact id; D3 refuses an empty content hash with Pre553IntegrityError;
  E1/E2/E3 raise TypeError for nonexistent issuer_id/issuer_epoch fields.
  These remain UNCONSTRUCTIBLE / NOT GREEN. They were not retargeted or xfailed.
- `historical_characterisation.xml`: 1 passed / 2 failed. The source_edition and
  native_item_ids cases still raise IdentityError:
  COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED. No frozen expectation was altered.
- P10 now includes the exact historical WG0N verdict from
  `6cd28b429504ad47e1bbc0fbcc6c4ef91db59ccd`, SHA-256
  `839adc7508fcd81bd0a59af8f0fc8793b8ea075c80661683b776124cb90a228b`.
  The reviewer's separately frozen copy was never overlaid into the candidate.

The five original historical construction limits do not become green because
new controls against the real authority API pass. Actual supported-cell and
signature checks concern the bounded synthetic fixture. Byte custody cannot
establish an independently signed institutional issuer. The source-artifact
revocation surface remains NOT_SUPPORTED; no new temporal-owner rule is granted.

No original-source U/E_pre, raw survey evidence, N11/N12/OC05, actor/V3 authority,
production grant, source/semantic adoption or HQ self-adoption follows from the
independent replay. The positive mechanical verdict preserves these ceilings.
