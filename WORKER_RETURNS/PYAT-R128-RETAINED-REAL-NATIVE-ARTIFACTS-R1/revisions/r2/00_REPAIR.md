# R129 — same-owner retained input catalog binding repair

**Status:** `M1_INPUT_COMPOSED__FAMILY_RULE_UNBOUND__NEXT_TYPED_REFUSAL_REACHED`

R129 repairs only the input-composition seam between R128's broad retained
custody and the existing M1 owner. It does not change M1, create or rename an
authority, weaken the duplicate guard, or consume a source/current grant.

## Preserved R128 evidence and defect

R128 recovered 234 exact native objects and replayed the existing M1 input owner
with **all 24 retained AuthoritySnapshot objects** from the broad custody store.
The owner correctly refused:

`M1IntegrityError: conflicting exact authority snapshot preimages`

The defect was the caller-supplied catalog: six `AuthorityRef`s each have two
different retained snapshot preimages. The native M1 duplicate guard was not
defective and was not changed.

R128's original return/runtime, private `.r61` exports, and full 234-object
custody remain preserved. R129 did not reread the 3.4GB checkpoint.

## Exact producer catalog binding

The exact producer source is:

- commit `6286c15bea78758a91686d60e036680bb26c6674`;
- `WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/source_retry_evidence/zero_source_resume_receipt.json`;
- `audit.common_execution_binding.runtime_catalog.catalog_identity`
  `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`.

Its `runtime_catalog.authorities` contains 12 exact
`AuthoritySnapshot@1.0.0` object refs, unique by `AuthorityRef`. For each of the
six duplicate-key groups, the producer catalog's exact object ref was selected:
no first/last/hash-sorted winner and no snapshot merge was used.

The selected receipt's evidence dependencies require one additional exact
snapshot absent from that 12-entry producer catalog:
`urn:rawlsing:pre553:as2b:lits1:authority:part_a_projection` (only one exact
preimage exists in full custody, object
`998d7e93b1d8424386f6f918c84f4fd3cb120fcb07127abf7ed3a73df9d90b5b`). It is
included only as a uniquely required full-custody support object.

The resulting invocation catalog has 13 exact snapshots: 12 unchanged producer
catalog refs + 1 uniquely required support ref. The other 11 full-custody
snapshot objects, including every unselected duplicate variant, remain in
private custody and are listed by exact ref in `CATALOG_BINDINGS.json`.

## Actual M1 call

The full R128 all-24 replay was repeated first and retained the same native
refusal.

The source-bound 13-snapshot input produced an actual
`M1AdjudicationInputBundle`:

- bundle:
  `urn:rawlsing:pre553:m1:M1AdjudicationInputBundle:sha256:e4683f0baf36848a1f26b228d793db642fd47a33802f7893ea91b75d61673d9a`;
- authority snapshots: 13;
- selected receipt:
  `urn:rawlsing:pre553:DiscoveryResultReceipt:sha256:006df79b240d7314d113a86d37ab28c02325af642681c40460977a69d70547b8`;
- claim family: `NOT_BOUND`; claim rule:
  `D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS`;
- family rule binding: absent;
- validator registry: empty.

The existing owner returned a typed disposition:

`BLOCKED / MISSING_FAMILY_VALIDATION_RULE_AUTHORITY`

Disposition:
`urn:rawlsing:pre553:m1:LearnedEmpiricalDisposition:sha256:50cc3a0b1a6f85fd3c824213208b4b54bd8c0697e5f01c5e1d71c960a61ff6dc`.

No positive M1, M2, B5, N10E, FF, or V553 result was created. No values were
read. The next binding is the exact existing family rule/validator; R129 does
not search broadly, register a permissive validator, or invent one.

## Sever/restore

- Removing one required producer-bound snapshot
  `urn:rawlsing:governance:authority-28:...` from the invocation catalog caused
  the native owner to return `BLOCKED / MISSING_AUTHORITY_CLOSURE`
  (disposition `6c76f8f8…193c`).
- Restoring the exact 13-snapshot input returned the original
  `MISSING_FAMILY_VALIDATION_RULE_AUTHORITY` disposition with the same reference
  `50cc3a0b…f6dc`.

## Resource and access

- Runtime: approximately 290.5 seconds, peak RSS `749748224` bytes; under 3GiB.
- Whole-checkpoint rereads: 0.
- Source/raw/decode/respondent-snapshot accesses: 0.
- Only R128's private exported objects and the exact producer receipt were read.

## Exact next step

1. If an already-issued exact family rule/validator binding exists in the
   selected native evidence, bind it faithfully to the resulting M1 bundle and
   replay the same call.
2. If none exists, bank the exact `MISSING_FAMILY_VALIDATION_RULE_AUTHORITY`
   disposition and the required family-rule fields for the competent scientific
   owner.
3. Do not add a substitute authority, family rule, validator, or M2/B5/FF
   positive.

The full learned/consumer milestone remains **NOT_REACHED**.

## Holds

R124 representative milestone, fullscope, parallel C5, source/current
measurement, CI/prod/R09, actor/dyad/V3, N11/N12, Sorok, J52/W52, and the
original big-scope endpoint remain unchanged.
