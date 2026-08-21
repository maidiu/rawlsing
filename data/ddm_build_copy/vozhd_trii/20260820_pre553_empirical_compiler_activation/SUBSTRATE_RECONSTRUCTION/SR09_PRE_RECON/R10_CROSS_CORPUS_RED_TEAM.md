# SR09-PRE R10 — CROSS-CORPUS RED TEAM

Status: `AUTHORIZED__NON_DISPOSITIVE__ADVERSARIAL`
Branch: `agent/vozhd-trii-sr09pre-r10-cross-corpus-red-team`
Write only: `SR09_PRE_RECON/RETURNS/R10/`

Read `00_COMMON_WORKER_CONTRACT.md` first and obey it exactly.

## Scope

All CLOSED_35 sources as represented by:

- accepted SR03 physical manifests / summary / receipt;
- `SOURCE_BYTE_INVENTORY.csv`;
- the frozen source constitution and decoder contract;
- targeted raw-source probes only where the existing census leaves a named cross-corpus ambiguity.

Do not duplicate nine full family scans.

## Mission

Act as an adversarial cross-corpus taxonomy court. Look for rare or novel source behaviors that could surprise G-SR09 even after WVS7/LiTS-I and the nine family reconnaissance orders.

Determine at minimum:

- every physical hazard class actually observed across CLOSED_35 and how many sources exercise it;
- rare classes exercised by only one/few sources;
- multiple-response/topology classes and which exact sources carry them;
- compatibility-encoding sources and whether any non-allowlisted source shows a materially different text/reader risk in accepted evidence;
- source families with unusual native-ID, country-coordinate, weight/design, missingness, or topology patterns;
- source-specific combinations of otherwise-known hazards that merit compound hostile fixtures;
- gaps in the common worker taxonomy or output schema;
- likely false assumptions that a family worker could make by overgeneralizing from a later/earlier wave;
- a prioritized exception queue for later HQ review.

## Required additional outputs

In addition to the common seven files, also write:

### `CROSS_CORPUS_HAZARD_MATRIX.csv`
Columns exactly:

`hazard_class,subclass,source_file,source_sha256,evidence_locator,rarity_count,known_contract_coverage,needs_family_fixture,needs_hq_adjudication,notes`

### `SR09_EXCEPTION_QUEUE.csv`
Columns exactly:

`priority,source_file,source_sha256,hazard_or_gap,reason,required_future_action,can_batch_with_family,notes`

## Red-team disposition law

R10 may say that a class is already covered by frozen generic law or that it appears novel. It may not certify the source or decide semantic authority.

If the accepted SR03 census is insufficient to tell whether something is a new hazard class, record `RECONNAISSANCE_INCOMPLETE` or `DOCUMENTARY_AUTHORITY_GAP`; do not guess.

Required success token in `RESULT.json`:

`PRE553_SR09PRE_R10_CROSS_CORPUS_RED_TEAM_COMPLETE`
