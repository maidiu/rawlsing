# SRC04 R4 release fingerprint — aggregate receiving

## Verdict

**R4 is a scoped 177-response construction witness, not the historical accepted
release.**

The reader reopened the saved estate successfully and its event/coordinate
counts match. The remaining `SRC04_ACCEPTED_RELEASE_HASH_DIFFER` is explained by
a **missing q217 `QuestionVariableBinding` in the scoped R4 candidate projection**,
not by a reader count failure.

- R4 reconstructed `C11LogicalRelease`:
  `8444fcb5701db32ca00de37d4f67b8af73cb3cd95ce76e270637b1741240f611`
- Historical accepted release:
  `9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1`
- R4 replay:
  `1ea8528c8745fc0e1f905a54459780f69add5d42f6d4167d8a64cdcc139a0c85`
- Historical accepted replay:
  `893f24ae10b297cd21422d154ec1649d522da4add006d1d3ac3da9a3da111a49`
- R4 `QuestionVariableBinding` count: **177**
- R4 Parquet contains **no q217 native-question binding**
  (`question_impl.phase0.6cbd4e206f21e147fd21` absent)
- Historical release source accounting records **178 configured response slots**,
  with **q217 held** and **177 selected responses**.

The historical release therefore retained the q217 question binding in the
candidate projection while holding its response events. The R4 scoped config
removed q217 before construction, so the candidate projection lacks that QVB.
The downstream release/replay hashes differ accordingly. The reader's
`differences_from_accepted: {}` is only a count comparison and cannot detect
this missing binding.

## Exact R4 inputs

From the actual R4 launch record:

- candidate tree:
  `MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree`
- candidate patch:
  `OWNER/WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_ONLY_CANDIDATE_20261118/candidate.patch`
- base config:
  `IMPLEMENTER/WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/inputs/SRC04/source.config.repaired.v2.json`
  file `5e107de4…`, canonical `28630f26…`
- runtime overlay:
  `MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/SRC04.post_alignment.runtime.config.json`
  file `dd5cf699…`, canonical `ba886d87…`
- binding directory:
  `MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118`
- work root:
  `evidence/anvil-src04-candidate-31rqm9z_/private-runs-aligned`
- source:
  SRC04, SHA `2a48ba4b…`, 7,337 rows, 181 columns
- saved manifest:
  `5297493c6626a178029cb15d36ccdd1693c9a977ca126d93c43b289432df2cb2`
- retained estate:
  `…/SRC04_WITNESS_b860363f87c69684/private/releases/a10f329f09e2223c08803cca5113b68f772b45540a3a384e8f1b2f339767385e`

## Exact historical pins

- Release receipt: `303a57851785557fff8229e29a5554717168cbd1`
- Acceptance commit: `ba41253681212be14a0cde009afb99d77e14935e`
- Accepted release: `9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1`
- Accepted replay: `893f24ae10b297cd21422d154ec1649d522da4add006d1d3ac3da9a3da111a49`
- Historical config: repaired-v2 base `5e107de4…` with accepted runtime overlay
  `ba886d87…`; source accounting `configured_response_slots=178`,
  `held_response_slots=[27]`, `selected_response_slots=177`
- Local accepted bundle id: `SRC04-9ddec98561a0fc54`

## Bounded read-only evidence

No source read, decode, rebuild, full-estate re-verification, or estate mutation
was performed.

Read-only checks:

1. R4 `QuestionVariableBinding.parquet` footer/body:
   - 177 rows;
   - q217 native-question ref absent.
2. R4 producer/reader/supervisor aggregate receipts:
   - reader exit `2`;
   - `historical_reference_verified=false`;
   - `release_ref_equal_to_accepted=false`;
   - counts equal accepted counts, so `differences_from_accepted={}`.
3. Historical release receipt:
   - configured 178 responses, q217 held, selected 177;
   - accepted release/replay pins above.

The exact hashed field is the **QuestionVariableBinding family in the
candidate projection**, specifically the q217 native-question binding. The
release hash and replay hash are downstream consequences of that omitted
binding; no reader ordering or count defect is indicated.

## Disposition and smallest repair

**Do not promote R4.** It is a valid scoped 177-response construction witness,
not the historical accepted release.

No reader-only repair is warranted: the saved R4 estate does not contain the
q217 QVB, so a reader cannot reconstruct it from counts. A certificate-only
repair also cannot add a missing family member to the saved estate.

The smallest legitimate repair, if historical release equivalence is required,
is to construct a successor estate with the q217 **question binding retained**
while q217 response events remain held, then cold-reopen and compare the exact
release/replay identities. That is a construction change, not a reader fix.

If the scoped 177-response witness is the intended product, the correct
disposition is `R4_SCOPED_177_WITNESS__Q217_BINDING_OMITTED__NOT_ACCEPTED_HISTORICAL`
and the historical release gate must remain failed.

## Evidence

- `reader_receipt.json`
- `producer_receipt.json`
- `supervisor_receipt.json`
- `private/releases/.../QuestionVariableBinding.parquet` metadata/body pins
- historical `RELEASE_RECEIPT.json` at `303a57851`
- actual R4 `job.json` at the local automation state root

No file was written to the saved estate, checkpoint, product, or protected
receiving.
