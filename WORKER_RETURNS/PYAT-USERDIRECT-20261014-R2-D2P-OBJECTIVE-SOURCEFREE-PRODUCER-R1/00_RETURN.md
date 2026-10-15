# R2 D2P — objective field producer and numeric consumer — implementation return

**Terminal:** `D2P_OBJECTIVE_SOURCEFREE_PRODUCER_COMPLETE__TWO_VALUES_DEREFERENCED__116_TESTS_PASS__REAL_OWNER_HANDOFF__NO_ISSUANCE__NO_ADOPTION`

**Authority:** user-direct bounded implementation candidate. No Pyat HQ accession,
no N5/N6/N7/N9 source/use signature, no self-adoption. NOT independent reviewer
for own code.

## Identity and sealed startup

- Repository: `maidiu/rawlsing` private.
- Branch: `agent/userdirect-pyat-20261014-r2-d2p-objective-sourcefree-producer-r1`.
- Exact sealed startup `77e549036002fa97b9af6e5c23208d8440942db0`, direct remote
  verified before edits. Parent canonical `0d551d36ff19dc9806e0ad490ff33a1e4c25e381`.
- Commission `WORKER_COMMISSIONS/PYAT-USERDIRECT-20261014-R2-D2P-OBJECTIVE-SOURCEFREE-PRODUCER-R1/00_COMMISSION.md` read in full.
- Mandatory priors read: D2I `2653fff57ac59fe2eaeffd24a0611c45f16f3b54` 00–07 +
  40-test code; N9C `9ab4a0192b7c951bb0b387637e6c74333246766c` 47-test reader +
  `04_FIELD_EE13_OC05_POSITIVE_GATE.md`; pinned `compose_direct_producer` blob
  `4a8e27a226a9c06606f5ba493d2cc7356d491a7b` and OC05 blob
  `f30fca20e7b56e00348e82765d95f974b4b6a195` (both == current tree).

## Adapter recovery (mission 1): no accepted field producer exists — so reuse, then add the one missing piece

A versioned accepted external-original-published-aggregate source/field adapter
and issuer was searched for and **is absent**: `compose_direct_producer` is a
transport that records explicitly authorized direct routes (not an original-PDF
adapter); OC05 is `NOT_YET_APPLICABLE` with `seam=None`; the N9C reader is a
candidate file, not an installed owner; no accepted N5/N6 field product exists
anywhere the commission names. Consistent with D2I, **no competing issuer is
created.** The one missing piece is written as a minimal test-only candidate:

- `repro/d2p/external_fields.py` — `ExternalPublishedAggregateField`: binds
  versioned GSS (`GH_GSS_PHC_2021_V3K_TABLE5P10@TESTONLY1`) vs NCA
  (`GH_NCA_Q4_2021_BULLETIN_TABLE10@TESTONLY1`) native units, values,
  denominators, observation/publication clocks, and typed source authority
  requirements (`fixture_only`, `issued=False`, `TEST_ONLY_NO_EXTERNAL_USE_GRANT`,
  NULL binary custody, NULL issuer). Both fields independently content-addressed.
- `repro/d2p/n9c_reader.py` — N9C reader byte copy, attributed; blob
  `03eb46efccadd6880cb34b2e2ac609ffc9b16c59` verified identical.
- `repro/d2p/direct_transport.py` — handoff into the REAL accepted
  `compose_direct_producer` (imported from
  `rawlsing_next.pre553_learned_world_composition`, blob-verified, actual
  `module.__file__` recorded) with an explicit TEST_ONLY DIRECT_PRODUCER
  contract; call trace + receipt terminal state recorded.
- `repro/d2p/counterfactual.py` — executable no-actor 2021 Ghana counterfactual.

## Positive (mission 2): two values actually dereferenced

At `2022-07-08` `HISTORICAL_PUBLICATION_AWARE` the reader dereferences both
numbers, not URLs/hashes: **GSS 2,388,192/3,288,063 = 72.6%** rural occupied
dwelling-unit main lighting with all five subtypes summing exactly, and **NCA
23,414,527 = 23,237,338 prepaid + 177,189 postpaid** national active
subscriptions, not unique persons. Units, geographies, denominators and clocks
stay distinct; relation is `NONPOOLED_CONTEXTUAL_CO_PRESENCE_ONLY`.

## Directed mutation (mission 3)

- GSS numerator −1 (and mains −1): only the GSS slot and snapshot change; NCA
  byte-identical. Inverse NCA +1/+1: only NCA changes; GSS identical.
- Cutoffs: 2021-12-31 both refused; 2022-03-01 GSS-only partial (nonpositive);
  2022-07-07 NCA still unpublished; 2022-07-08 both. Before 2022 publication, no
  retrospective 2021 knowledge.
- Hostiles executed: forged binary SHA/source root/issuer signature, stale
  version/ref, wrong scope, revoked use, mislabeled 'rural phone people' / person
  units, fake correlation/causal/model-use, ref-only-hash vs dereferenced values,
  missing field, cold replay identical, targeted invalidation.
- No fictitious pooled individual inference anywhere; person-exposure requests
  refused with typed codes.

## Owner/call trace (mission 4)

`compose_direct_producer` executed with a TEST_ONLY contract: receipt
`terminal_state=SOURCEFREE_TEST_ONLY_TWO_FIELDS_BOUND`,
`reason_code=DIRECT_PRODUCER_ROUTE_EXACTLY_AUTHORIZED`, determinant count 2.
Recorded actual module path, function name, timestamp. Where a real source grant
would be needed, the edge is receipted (not greenwashed): sourcefree typed
grant is not N7 issuance or actual N9/OC05.

## Counterfactual (mission 5)

A 2021 Ghana person-context counterfactual shows the aggregates condition
structural context only: rural lighting shares and national subscription
markets cannot fix any person's dwelling, handset, access, awareness or
development. `counterfactual_holds` (8 executable checks) all hold.

## Deliverables

| File | Content |
|---|---|
| [00_RETURN.md](00_RETURN.md) | this return |
| [01_EXISTING_OWNER_AND_EXTERNAL_FIELD_ADAPTER.md](01_EXISTING_OWNER_AND_EXTERNAL_FIELD_ADAPTER.md) | reuse/recovery decision + boundary |
| [02_COMPUTED_FIELD_AND_READER_RECEIPTS.json](02_COMPUTED_FIELD_AND_READER_RECEIPTS.json) | field refs, dereferenced values, mutation slots, transport receipt, cutoff notes |
| [03_REGRESSION_HOSTILES_AND_RUN_LOGS.md](03_REGRESSION_HOSTILES_AND_RUN_LOGS.md) | 116 cases, hostile ledger |
| [04_SOURCE_AUTHORITY_AND_ENDPERSON_CEILING.md](04_SOURCE_AUTHORITY_AND_ENDPERSON_CEILING.md) | issuance chain holds + end-person ceiling |
| [repro/](repro/) | isolated code/tests/logs; owners untouched |

## Executed evidence (116 cases, 0 failures)

- D2P new suite: **29 passed** (JUnit `repro/logs/d2p_junit.xml`).
- N9C 47-test reader reproduced read-only: **47 passed**.
- D2I 40-test suite reproduced read-only: **40 passed**.
- Model calls 0; actor runs 0; SAV/DTA 0; binary custody 0; paid ops 0.

## First missing producer/permission/use

Secure actual GSS/NCA PDF bytes + SHA/size + revision chain + method validation
+ reuse grants (D2C parallel), then the field issuer authorizes two separate
N5/N6 products, then EE13/N7 nonpooled coexistence for this pair, then N9/OC05
consumer authorization. Sourcefree execution constitutes none of these.

## Invariants

Original respondent rows 0; V3 0; owner/canonical/CURRENT writes 0; SC0 port
under RED not depended upon; D2C custody untouched; no LLM calls; distinct
independent reviewer still required. Final remote SHA reported in push
verification, not embedded recursively here.
