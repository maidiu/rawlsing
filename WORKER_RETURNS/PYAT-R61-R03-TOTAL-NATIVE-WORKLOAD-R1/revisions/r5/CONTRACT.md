# R61 R03 R5 shared capture/restore structural validator contract

Status: frozen before the R5 code commit. Implements R61AZ/R61AV. Sourcefree
TEST_ONLY local trusted host. Native owners/U43 unchanged.

## One shared pin-free validator

`_validate_governed_ledger_material(material)` is the single structural/
expected-mapping/native receipt-fact closure/multiplicity validator. It checks
the exact compilation hash, expected jobs against issued jobs, expected
candidate/operation mapping, row/candidate uniqueness, native receipt/fact
object identity and duplicate rejection, receipt-to-row/state/coverage/fact
associations, fact coverage (shared facts allowed) and true candidate/operation
anti-joins. No anti-join boolean or self-reported ref is trusted as a substitute.

- Live `freeze_restore_checkpoint()` builds `self.ledger()`, removes only the
  self hash, runs the shared validator, and only then returns the canonical
  checkpoint. Empty/invalid operation rows, missing expected jobs/candidates,
  duplicate facts/refs, closure breaks and failed flags refuse capture.
- Cold `restore_governed_frontier_ledger(ledger, *, expected_checkpoint_ref)`
  first checks submitted self-hash and the separately provisioned original pin,
  then calls the same validator. No unpinned fallback.

## Preserved

Genuine original-pin restore, fact/job deletion/duplication/substitution
refusals under the original pin, fresh-process no-rerun restore, governed
joint/conditional/D3/minority/pending/source-value/held-unknown positives.
Legitimately shared facts across receipts remain lawful.

## Holds

No R04 durable custody/cryptographic issuer, R05+, original source/science,
CI/prod/N11/N12/Sorok/J52/W52. Trusted-host replacement of both pin and
candidate remains excluded.
