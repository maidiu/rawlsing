# R61 R03 R4 fixed external checkpoint contract

Status: frozen before the R4 code commit. Implements R61AV exactly. Sourcefree
TEST_ONLY, local trusted host. Native owners and exact U43 unchanged.

## Live capture

`GovernedFrontierResult.freeze_restore_checkpoint()` is the only accepted capture
path. It refuses unless the live result has candidate and operation no-drop,
eligible accounting, exact expected operations/jobs, and native receipt/fact
identity closure including duplicate-fact rejection. It returns the canonical
whole-result checkpoint (the existing ledger material hash). A failed/incomplete
live result cannot acquire an accepted checkpoint.

## Cold restore

`restore_governed_frontier_ledger(ledger, *, expected_checkpoint_ref)` requires
the separately provisioned original checkpoint string. Missing/malformed pin ->
typed refusal. The submitted self-hash and the independently supplied pin must
both equal the recomputed canonical material hash; only then does the existing
full structural/closure validation run. No compatibility fallback accepts an
unpinned ledger. No native rerun/new issuance/budget charge.

The trusted coordinator captures the pin from the original live result and
provisions it into the cold process. Subject ingress cannot select or recompute
it. Trusted-host replacement of both pin and candidate is excluded.

## Finite refusals

With the SAME original pin: fact deletion, fact duplication, expected
job/query/predicate substitution, receipt/fact/typed-row alterations and any
byte/content mutation with old refs fail pin equality. Genuine restore passes.
The prior governed D3/joint/conditional/minority/pending/value and HELD/UNKNOWN
positives remain.

## Holds

No R04 durable custody, cryptographic issuer, R05+, original science, CI/prod,
N11/N12, Sorok, J52/W52.
