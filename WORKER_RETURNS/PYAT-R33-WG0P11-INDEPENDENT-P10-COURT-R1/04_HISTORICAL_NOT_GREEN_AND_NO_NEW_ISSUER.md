# Historical NOT GREEN and authority ceiling

The exact historical WG0N verdict is frozen at `frozen_WG0N_historical_verdict.md`.
It is evidence of historical status and was never inserted into the candidate.

Actual unmodified tests in the isolated P8 clone reconfirmed:

- C3 source-artifact revocation: `RevocationError: UNKNOWN_RELEASE_NO_REVOCATION`
  during fixture construction. The owner accepts release tags; independent
  source-artifact revocation remains unrepresented and NOT_SUPPORTED.
- D3 empty snapshot: `Pre553IntegrityError` rejects an empty content hash during
  construction. The original frozen oracle does not count that as its required
  refusal; it remains historically UNCONSTRUCTIBLE / NOT GREEN.
- E1/E2/E3 issuer controls: `TypeError` on nonexistent `issuer_id` or
  `issuer_epoch` constructor fields. These three controls remain
  UNCONSTRUCTIBLE / NOT GREEN. They have not been silently retargeted to a
  different authority surface.
- The two original `test_bound_descriptor_cannot_change_served_provenance`
  cases for `source_edition` and `native_item_ids` still fail with
  `IdentityError: COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED`. Their assertions
  have not been edited. The third case in the same file passes.

JUnit and command/stdout/stderr receipts are under
`03_ALL_ACTUAL_FROZEN_NATIVE_AND_COLD_JUNIT/`. Five construction failures are
reported as five failures in XML, not skipped, xfailed or newly green.

Hash identity establishes byte custody, never an independent signed issuer.
No source-artifact revocation support, new temporal-owner rule, U/E_pre,
N11/N12/OC05, actor/V3 authority, source/semantic adoption or HQ self-adoption
is granted. Future genuine authority tests do not retroactively regrade these
historical cases.
