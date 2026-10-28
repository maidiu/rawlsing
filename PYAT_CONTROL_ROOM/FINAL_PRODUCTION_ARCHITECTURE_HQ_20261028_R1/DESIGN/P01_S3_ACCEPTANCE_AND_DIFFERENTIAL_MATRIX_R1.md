# P01-S3 — Differential acceptance matrix: old vs new, negative, restoration and original-use boundaries

**Executable acceptance contract, not test results.** Current base: `maidiu/rawlsing@299f41e97a43c67be9cc76a79fa49b48f4e12e54`. Test outputs from the existing I02 baseline may be verified; no new journal/view code has been run. Every Codex builder/reviewer must record exact changed SHA, commands, exit status and independent oracle.

## Gate distinction

- **GOLDEN_BASELINE:** old accepted I02 fixture yields a fixed hash, native object identity and refusal taxonomy.
- **OLD/NEW_SOURCEFREE_PARITY:** new journal/view implementation and old path produce exact same results, including negative distinctions; independent expected oracle.
- **INTEGRATION_PARITY:** query, recursive handoff, old audits, source-equivalence consumer, repository and provenance all function unchanged.
- **ORIGINAL_DATA_ACCEPTANCE:** permitted source owner actually reads original source with exact grant, records source-byte custody, independent review and downstream consumer; no fixture is promoted.
- **HOST_ECONOMICS:** measured cold, warm, cache miss/restore, memory/disk/scratch/whole native query time; not a physical-route bakeoff.

## Complete sourcefree and later authorized cases

| Test | Ticket | Grounded test and falsifier | Required behavior | Current proof level |
|---|---|---|---|---|
| T01 | B00 | Existing I02 accepted canonical fixture full section coverage | Same release/ref, manifest/ref, all M01–M18, public/internal ref list | SOURCEFREE baseline rechecked; new path NOT RUN |
| T02 | B01 | Candidate section ref order reversed | Exact _candidate_projection_semantic_hash unchanged, duplicate refs retained | SOURCEFREE old baseline proof; new path NOT RUN |
| T03 | B01 | Unicode, escape, typed absence, Fraction/Decimal, float refusal | Canonical bytes and exact constructor types equal; no binary float semantic identity | SOME BASELINE PROVED; extended parity NOT RUN |
| T04 | B02 | Replay closure global multiset source+retention included | Full ordered tuple and ReplayManifest.ref exactly equal old accepted output | SOURCEFREE old hash baseline; new path NOT RUN |
| T05 | B02 | Declared count mismatch including optional omitted/explicit zero | Old failure order and IngestDisposition equal; no inferred absence | BASELINE mixed cases; new path NOT RUN |
| T06 | B02 | Mandatory coordinate, respondent, question, event, routing, universe, authority missing | Same old rejection class; no true empty means missing | SOURCEFREE old baseline rechecked |
| T07 | B02 | Duplicate respondent key within same universe with corrected manifest/replay | Reject duplicate namespace at same stage, not fake success | SOURCEFREE old baseline rechecked |
| T08 | B02 | Same respondent key across two exact universes | Remain two separate exact records, no join | ADDITIONAL fixture needed |
| T09 | B02 | Duplicate event occurrence with corrected counts/replay | REJECTED_EVENT_IDENTITY_COLLAPSE and no view | SOURCEFREE old baseline rechecked |
| T10 | B02 | Two multiselect events with same raw value but distinct event ids | Both preserved, no value dedup | SOURCEFREE baseline accepted |
| T11 | B02 | Event lacks native question binding after refreshed replay | REJECTED_TOPOLOGY_LOSS | SOURCEFREE old baseline rechecked |
| T12 | B02 | Wrong exact respondent/universe binding | REJECTED_SOURCE_UNIVERSE_COLLAPSE | SOURCEFREE old baseline rechecked |
| T13 | B02 | Unknown public/internal authority with resealed candidate | Rejected; no authority-by-presence | SOURCEFREE old baseline rechecked |
| T14 | B02 | Unauthorized canonical mapping or coordinate crosswalk | Reject, never auto-authorize canonical values | Existing tests present; new path NOT RUN |
| T15 | B02 | Routing unknown, not asked, inapplicable, eligible states | Every state exact, do not infer eligibility from observed event | Extended fixture needed |
| T16 | B02 | Weight missing or unauthorized | No default weight=1; native estimand permissions intact | Existing tests present; new path NOT RUN |
| T17 | B02 | Distinct-by-default relations vs authorized relation scope | No cross-source pool/same-person join inferred | Existing tests present; new path NOT RUN |
| T18 | B02 | Authoritative replay malformed closure, permuted or duplicate refs | Exact full multiset comparison rejects, stable manifest hash | SOURCEFREE old negative rechecked |
| T19 | B02 | Two simultaneous independent faults | Match legacy check priority and negative class | NEW dual-engine oracle needed |
| T20 | B03 | I02-resealed manifest with wrong snapshot retention SHA | New source-view admission FAIL despite old I02 logical acceptance | SOURCEFREE old boundary rechecked; new gate NOT RUN |
| T21 | B03 | Forged source_sha256 string/transport identity | Cannot mint qualified original-source byte-attested view | NEW negative test needed |
| T22 | B03 | Changed governed slot owner/projection/authority | Cache invalidated; original source admission and version binding re-evaluated | NEW negative test needed |
| T23 | B01 | Duplicate or missing physical row/slot in projected source cells | Source-backed projection refuses, not silently converted to missing response | Existing tests present; new path NOT RUN |
| T24 | B01 | Ranked/ordered/repeated events from one source cell | Same occurrence, order, rank, component and exact native event identity | Existing tests present; new path NOT RUN |
| T25 | B04 | Mixed materialized and source-backed exact same release | Same logical inventory, correct allowed idempotence, no duplicate ref ghost | NEW mixed-repo test needed |
| T26 | B04 | Same release_id different semantic hash, old/view both orderings | Atomic reject; prior snapshot_identity and lookups unchanged | NEW mixed-repo test needed |
| T27 | B04 | Native object ExactRef conflict, bad stored proof or tampered physical frame | Atomic reject, no object shadow or cache authority | NEW mixed-repo test needed |
| T28 | B04 | Interrupt before final durable commit and during reopening | No release_refs or object ghosts, stale stage deleted or quarantined | NEW crash test needed |
| T29 | B05 | Old materialized exact object resolution and new lazy ref lookup | Typed native objects and full semantic projection/content_hash/ref match | NEW old/new test needed |
| T30 | B05 | Rebuild complete C11LogicalRelease and full ReplayManifest with budget | Old type, exact replay, all sections, source-equivalence and audit satisfy unmodified tests | NEW old/new test needed |
| T31 | B05 | Budget intentionally insufficient; source/cache unavailable | Fail cleanly, do not represent incomplete proof as valid empty | NEW negative test needed |
| T32 | B06 | I03 native unary and supported-zero denominator cases | Identical complete-domain EmpiricalFact and execution replay/provenance refs | NEW old/new sourcefree test needed |
| T33 | B06 | I03 two conditional directions, unequal-risk conditional, J2 and J3 | Exact values/denominators, no estimator or topology change | NEW old/new sourcefree test needed |
| T34 | B06 | I03 missing, special, routing, weights and unauthorized measure | Same typed negative/positive scientific facts and no invented weight | NEW old/new sourcefree test needed |
| T35 | B07 | I05 recursive N+1 child branch replay cold | Same exact respondent membership, exact source scope and branch ancestry | NEW old/new sourcefree test needed |
| T36 | B07 | Batch runner exact scope and real consumer readiness | No accidental all-pairs predecessor or cells=[] resume | P05 companion, new test needed |
| T37 | B08 | Existing ParquetC11Carrier/replay audit/source equivalence | Legacy path unchanged and old tests pass | NEW regression in future code checkout |
| T38 | B08 | Optional cache miss/delete/corrupt/stale; cold fresh process | Same logical refs, refuse invalid state, no cache-derived grant | NEW negative/rebuild test needed |
| T39 | B08 | Resource profile under original host capacity | Measure full lifecycle wall time, RSS, swap, scratch, persistent bytes, native fact cost | NOT MEASURED |
| T40 | B08 | Qualified original source scope & all35 family diversity | Only permit and claim actual original outcomes at current grant scope; all35 full acceptance separate | NOT EXECUTED, separate source authority |
| T41 | B03 | Source file mutation between _decode SHA and iter_batches pathname reopen | Approved immutable snapshot lease binds read cells to verified bytes; altered synthetic path never qualifies an original-source view | NEW negative/positive sourcefree test needed |


## Execution evidence ledger requirements

For every Txx, report: actual fixture source/path and expected reference SHA; old baseline command/exit/output; new sourcefree command/exit/output; independent reviewer check; source/authority/physical cache state; positive vs negative/held state; cold reopen; resource measurement and permitted original-source status. A result is never simply 'PASS' without the exact comparison and scope.

**Do not cross the authority boundary:** source SHA/retention wrong (T20/T21) is tested as a DIFFERENT gate from self-consistent old I02 logical validation; false-original release construction must fail. A journal checksum or Parquet file by itself never confers I02 validation or source permission. Test T40 is not a Codex authorization for an original-data run.

**Minimum P01 code acceptance:** all T01–T38 positive or exact documented held with fail-closed behavior, no changed logical root/fact schema, independent hostile reviewer, measured local memory/resource limits T39. Any unpassed target-semantic test blocks affected view deployment; a scope-held original source only blocks its own original execution. Other source-free engineering can proceed.

**Risk priority:** T04 replay multiset, T09 occurrence, T13 authority, T20/T21 source admission, T26/T27 atomicity, T30 legacy full compatibility, T32–T35 native I03/I05 parity. Each is a hard positive proof gate before declaring sourcefree production-equivalent.
