# REC-02 adjudication return

| # | Warrant | Result | Fragment | Blocked | Note |
|---:|---|---|---|---|---|
| 1 | U003 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | QSM/QSMv2 carriers located; same-grain accepted succession/retirement receipt not proved. |
| 2 | U004 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | Respondent source registries located; complete predecessor-preservation/retirement receipt not proved. |
| 3 | U005 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | Respondent semantics/response-contract surfaces located; complete same-grain succession receipt not proved. |
| 4 | U006 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | Overlay and exception surfaces located; complete family-scoped ownership receipts not proved. |
| 5 | U007 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | Discovery/frontier mechanism and replay surfaces located; accepted production provider receipt not proved. |
| 6 | U008 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | Branch/predicate mechanism surfaces located; exact governed membership replay provider not proved. |
| 7 | U009 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | Validation/admission surfaces located; general learned-product owner not proved. |
| 8 | U010 | `BOUNDED_SEARCH_BLOCKED__EXACT_ROOT_UNAVAILABLE` | no | yes | Required comparator-feeder step-zero root/list unavailable; downstream search was not performed. |
| 9 | U011 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | PSEPF guard/interface surfaces located; accepted positive V3 owner receipt not proved. |
| 10 | U012 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | Publication/lifecycle surfaces located; complete lifecycle-owner receipt not proved. |
| 11 | U013 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | C11/replay/source-cert surfaces located; one complete end-to-end closure chain not proved. |
| 12 | U014 | `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED` | yes | no | Publication/history surfaces located; complete cross-product succession/withdrawal history not proved. |
| 13 | EAD-V525B | `PAYLOAD_FRAGMENT_FOUND__HASH_NOT_PROVED` | yes | no | R03 summary and later semantic CSV fragment located; cited accepted V525b payload hashes not bound to readable accepted bytes. |
| 14 | EAD-D62-92 | `DELTA_FRAGMENT_FOUND__92_SET_NOT_PROVED` | yes | no | R03 d62 ledger fragment located; exact 92-row key/payload/provenance set not recovered. |

## Accounting

- `LOCATED_WITH_EXACT_RECEIPT`: none.
- `NOT_LOCATED_AFTER_BOUNDED_SEARCH`: none.
- `BOUNDED_SEARCH_BLOCKED__EXACT_ROOT_UNAVAILABLE`: U010 only.
- All other terminal results are recorded in the per-warrant ledgers and dedicated evidence receipts.
- HQ retains adjudication of provider sufficiency and any downstream opening.

## Pinned input access

- R08: `742fa99500f2f8ff82d65b4e0eb1339e7a56accb`.
- R03: `6d8cc6b4c918516c475e3c0bea1b8c9e50f60374`.
- Both were read by exact `git show` paths under the immutable sibling-input patch.
