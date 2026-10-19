# Native M1 authority binding — correction of the previous diagnosis

The previous goal turn made material progress by recovering the exact checkpoint
and P1 Fact preimages and executing the real native M1 boundary. It also made a
diagnostic error: it treated failures from `AuthorityRegistry.require` with an
object-family constraint as though M1 imposed those constraints on every
provenance authority ref. That interpretation was wrong.

## Actual contract and bounded repair

The unchanged native `_verify_bundle` calls
`validate_object_authority_closure`, which resolves every exact authority ref
through `resolve_exact`. That closure function does **not** call
`require(object_family=...)`. The earlier 36 strict family observations remain
reproducible, but they are not 36 unmet M1 obligations and do not justify asking
an issuer to expand historical permissions. The earlier assertion of a
family-scope compatibility defect is retracted at this exact seam.

The actual resolution audit finds four unresolved object/ref occurrences
(three Facts and their receipt), all referencing one exact projection authority:

`urn:rawlsing:pre553:as2b:lits1:authority:part_a_projection`
at `AS2A-BANKED-1.0.0`, authority-content hash
`9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06`.

The retained archive already contains its unique full public snapshot,
`998d7e93b1d8424386f6f918c84f4fd3cb120fcb07127abf7ed3a73df9d90b5b`.
It matches the unchanged native
`historical_projection_authority_snapshot()` owner. The return-only adapter
appends that exact snapshot to the original scoped 13, giving 14. No archived
envelope, family, authority triple, original Fact, query, predicate, receipt or
native owner is changed. The full 24-snapshot union still has its six preserved
conflicting-envelope REDs; this repair does not flatten that union.

`P1_AUTHORITY_BINDING_CORRECTION_FREEZE.json` records this interpretation and
repair before relying on the repaired consumer output. The original
`CONTINUATION_P1_FREEZE.json`, its digest, test assertions and joint-Fact deletion
contract are unchanged. `audit_p1_exact_authority_resolution.py` records all
selected refs before and after the append. This is a mechanical binding repair
using an existing owner, not an authority issuance.

## Consumer and direct dependency proof

The original named consumer test passed against the repaired adapter:
**1 passed in 273.42 seconds**, with its expected oracle and assertions unchanged.
Its preregistered expected terminal remains
`BLOCKED__MISSING_FAMILY_VALIDATION_RULE_AUTHORITY`, after actual native
authority and receipt/query/Fact verification. No family-validation binding or
validator is supplied. A pass at that terminal establishes retained-object
integrity to the typed rule hold, not a qualified learned relation.

The existing claim-specific fault removes the original JOINT Fact from the
actual catalog supplied to native `build_m1_adjudication_input_bundle`. That
must make this same named test fail by assertion; an error, skip or failure of
a different test is insufficient. The adapter must then be restored byte for
byte and the positive rerun green.

The full retained Fact path takes more than the shared runner's fixed
180-second subprocess budget on this host. `run_p1_exact_witness.py` imports
the exact sealed shared checker and runs its unchanged witness algorithm with
only a transparent return-local timeout adjustment, 180 to 600 seconds. It
retains baseline and fault JUnit/stdout, checks exact source restoration, and
runs a third fresh restored positive. No shared checker/native-owner file or
assertion is edited. This is not a claim that the unadjusted 180-second CLI or
CI gate passed. The actual proof terminal in
`evidence/p1_native_severance_witness.json` is
`MECHANICAL_WITNESS_PASS_NOT_SEMANTIC_ADOPTION`: baseline GREEN, exact JOINT
deletion causes the named assertion RED (zero errors/skips), and the byte-exact
restored adapter passes in a third fresh native process. Baseline and restored
semantic result summaries are identical, including disposition
`fccdea7d53c85db158dd5b4c67774b8aac1ea781f18e661bd2acdf0086f7a22a`.

The first timeout-wrapper startup failed before any native test or mutation
because its subprocess proxy omitted PIPE/STDOUT constants. That author harness
error is retained separately in `p1_native_severance_setup_failure.txt` and is
not counted as a scientific RED. The corrected wrapper then ran the complete
sequence above. Native owners, the shared checker and the frozen test/oracle
remain unchanged.

From the dedicated worktree, after permitted exact P1 recovery, reproduce with:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -B WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/audit_p1_exact_authority_resolution.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -B WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/run_p1_exact_witness.py
```

The proof phases took 243.440 seconds GREEN, 22.382 seconds assertion RED,
and 250.748 seconds restored GREEN. There are zero errors or skips. These are
three executions of the same test, not three independent acceptance tests.
The 27 predecessor audit/catalog tests passed in the preceding continuation;
the 93 unchanged owner tests remain retained predecessor evidence and were not
rerun here. No broader suite count is invented.

## Full objective remains incomplete

Recovering three original P1 Facts and repairing their M1 binding advances a
real consumer edge; it does not execute a new original-source I03/Batch plan.
The exact validated LiTS C11 input repository remains unidentified in the
bounded retained custody inventory. Its ref and custodian/reconstruction
prerequisites remain in the owner packet. A metadata release, fabricated
validation token or new raw survey read is not substituted.

The original native execution-plan omission test remains NOT_RUN. The selected
P1 Fact-to-M1 witness, if successful, proves that separately declared narrower
edge only. Full35 scientific/source/operation bindings remain held, including
the 26-plus-nine frontier, six/twenty split, inactive 259, P10's 76 holds and
current original35 PERMITTED=0. No FF/model, actor, N11/N12, V3 or scientific
adoption is issued.

For a persona/world product, the change makes the retained q301_2 × q301_7
result verifiable through the current native M1 input path while conserving its
missing-rule hold. It does not turn that survey association into a new learned
or causal relation. The next competent decisions concern the exact validated
C11 repository/current reconstruction warrant and, for a positive learned
claim, a specifically qualified existing family-validation binding. The
retracted family-envelope expansion request is removed from the current motion.
