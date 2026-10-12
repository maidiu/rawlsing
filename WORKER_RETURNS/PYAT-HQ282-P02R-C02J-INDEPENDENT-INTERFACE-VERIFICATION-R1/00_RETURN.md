# P02R independent C02J interface review

Disposition: source-free review complete; additional owner work and independent authority sources are required. This review does not adopt the candidate or approve production use.

Reviewed exact candidate `895980397cc0533043c7ca0e493ebbb455666c1e`. The accepted owners and frozen candidate were unchanged. Tests used Git-exported source in a temporary directory, not the different source on the commission branch. The user confirmed this session is on the secondary Mac/account and authorized worktree setup from the repository.

Existing owner tests: **83 PASS, 0 FAIL, 0 SKIP**. Original court: exit 0, 24 emitted records counted by its script, including control and descriptive records; this is not 24 asserted tests. Independent requirement checks: **41 PASS, 14 FAIL, 0 SKIP, 3 UNTESTED**, exit 1. Counts are separate populations, not additive proof of overall coverage. Full observations and reasons are in `01_TEST_RESULTS.md` and `repro/review.jsonl`.

Normal use succeeds through both interfaces. The verifier returns publication event identities with `authorizing=false` and `current_selection_performed=false`. Fixed expected identities reject mismatched release/product/permission/authority references and post-freeze repository mutation. Recorded release, semantic-authority, consumed-authority and replay-closure revocations reject publication. Obsolete replay grades and incomplete replay material are refused. The accepted owner rejects selection of a withdrawn release.

Failures and remaining requirements:
- A replacement repository with matching replacement expectation passes. Matching self-declared permission also passes. Separate expectation custody and permission authority remain necessary.
- Direct event authority/rule references are not authenticated. Registered recertification ignores revocation. NO_CURRENT can run with no verifier when subject_release_ref is omitted.
- Valid published and selected-current checkpoints fail under the overlay because the verifier looks up a release reference in the M2 producer-subject table. Its rejection of truncated checkpoints therefore does not establish replay completeness.
- Without the overlay, truncated event history and changed publication state with recalculated self-hashes restore. Structural hash and registered-set checks do work.
- Several B5 and M2 state-changing entrypoints are unwrapped. No expiry clock or time-scoped revocation ledger exists. Historical event resolution and historical checkpoint resolution differ under present revocation.

Eight concurrent facade calls over stable material completed with identical publication-event identities. Concurrent mutation was not exercised; this result does not establish synchronization or durable publication idempotence.

Independent permission, expected-identity, event-provenance and current revocation sources remain unresolved. REPLAY_COMPLETE is a claim checked for consistency, not independently re-executed. No live publisher, G0b, whole-project acceptance, new scientific authority or actor/world activation is established.
