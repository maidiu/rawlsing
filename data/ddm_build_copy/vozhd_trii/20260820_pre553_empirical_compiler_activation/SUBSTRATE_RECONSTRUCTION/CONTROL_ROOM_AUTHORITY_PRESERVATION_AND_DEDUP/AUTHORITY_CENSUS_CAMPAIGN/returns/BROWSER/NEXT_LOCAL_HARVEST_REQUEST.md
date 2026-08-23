# HARVEST-004 — D62 DRIVER-MASTER PRODUCER AND DUPLICATE-SHADOWING PROVENANCE

Status: `ISSUED__AWAITING_LOCAL_PACKET`

## Exact authority question

What exact updater/merge/adjudication process created `questions_master_drivers.csv` SHA-256 `d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011`, especially the duplicate `(source,wave,var_name)` rows whose later structural/context entries become the effective semantic source for Register B; was that shadowing explicitly intended and accepted, or is it an incidental carrier/key collision; and what exact pre-`d62` driver-master state generated Register A?

This is provenance recovery. Do **not** repair, deduplicate, re-key, regenerate, or semantically adjudicate the master.

## Why this is now the smallest next request

HARVEST-003 established:

- V525b `53feb282...` / `6e76965c...` are accepted canonical structural authority;
- Register B's nine semantic/driver fields match the effective last-row-wins lookup of `d62accad...` exactly for every matched master key;
- Register A -> B is exactly 2,148 changed keys / 13,330 changed cells under that lookup;
- 2,056 changed keys have two `d62...` rows and 1,228 still retain the Register A state as the earlier duplicate;
- winning rows are predominantly `accepted_context_only` or `accepted_block_child` and cause large nonblank-to-blank semantic-field transitions;
- recovered facet-review files cover only 68/2,148 changed keys.

The unresolved object is therefore the **producer and acceptance lineage of `d62...`**, not the existence of historical semantic authority.

## Search roots

- `/Users/matthewsmith/Desktop/Rawlsing`
- `/Users/matthewsmith/Desktop/RawlsingsExcess`

## Exact primary identities / aliases

- `questions_master_drivers.csv`
  - target SHA-256 `d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011`
- earlier accepted driver master
  - SHA-256 `53feb28296705d2005f8c3d2548c136e2c15fabd62c103694f05caa555063711`
- later semantic master feeding the broader lineage
  - SHA-256 `171d399da7e0f2bbd66dcce08a6c353978e48b69fee8d32ac6b1720d10d70ca5`
- Register A SHA `f47c8adb65546b1c0a06dcd31dc0b827b59f8975a3806646f41a0742966c3d84`
- Register B SHA `15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b`

Search exact backup/version aliases:

- `questions_master_drivers.csv.bak_v5_schema`
- `questions_master_drivers*.bak*`
- `questions_master_drivers*pre*`
- `questions_master_drivers*backup*`
- other exact driver-master copies dated between 2026-05-19 17:29 EDT and 2026-05-20 13:51 EDT.

## Exact producer-content clues

Search source/text/config files for these literal strings:

- `accepted_context_only`
- `accepted_block_child`
- `context_not_applicable`
- `women_rights_representation`
- `p0_block_pattern`
- `semantic_deepening_pass`
- `prompt_shell_cleanup`
- `mapping_status`
- `evidence_kind`
- `question_block_id`
- `structural_domain_id`
- `driver_facet_id`
- `relation_axis_id`
- `target_entity_id`
- `missingness_code`
- `does_not_measure`
- `strata_relevance`
- `channel_affordances`
- `forbidden_inference`

Also recover, when directly linked to the producer lineage:

- `gss_p0_block_patterns.yaml`
- `lits_p0_block_patterns.yaml`
- `gss_lits_semantic_deepening_report.md`
- `arab_barometer_prompt_shell_cleanup_review.csv`
- source for any prompt-shell cleanup / semantic-deepening / block-pattern updater
- any script/notebook/SQL that reads and writes `questions_master_drivers.csv`, or concatenates/appends/merges structural mapping rows into it
- any receipt/README/manifest/commit note explicitly accepting this mutation or defining duplicate-row precedence.

Do not collect unrelated QSM/FQRA artifacts unless an exact producer/input/output reference points to them.

## Mechanical evidence requested

For every distinct pre-`d62` driver-master candidate:

- absolute path, SHA-256, bytes, mtime
- exact header and row count
- `(source,wave,var_name)` distinct/duplicate statistics
- whether its effective last-row-wins nine-field projection matches Register A for the 18,262 matched structure keys; report count only, no semantic interpretation.

For every producer/updater:

- exact input/output filenames
- whether rows are appended, concatenated, merged, replaced or updated in place
- exact ordering law before write
- exact key/join columns
- exact columns copied/blanked/assigned
- exact source of `mapping_status` and structural columns
- whether duplicate `(source,wave,var_name)` rows are knowingly permitted
- whether any explicit precedence law exists
- any explicit review/acceptance gate, reviewer, status or authority reference.

For any receipt/authority text:

- quote only the minimum exact lines that state acceptance, migration, supersession, preservation, duplicate precedence, or intentional semantic replacement.

## Required returned ZIP

One bounded ZIP containing:

- `README.md`
- `EVIDENCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `SEARCH_RECEIPT.md`
- `PRE_D62_MASTER_CENSUS.csv`
- `D62_PRODUCER_LINEAGE_RECEIPT.csv`
- `DUPLICATE_SHADOWING_MECHANICAL_RECEIPT.json`
- `ACCEPTANCE_AND_PRECEDENCE_RECEIPT.csv`
- `payload/` exact bytes of only responsive pre-master candidates, producer/updater/configs and explicit authority/receipt objects.

Do not include raw survey microdata.

## Forbidden

- no deletion/move/rename/edit/normalization;
- no builder/updater execution;
- no regeneration of any master/register;
- no deduplication or row reordering;
- no semantic interpretation;
- no declaration that `accepted_context_only` or `accepted_block_child` automatically supersedes semantic authority;
- no canonical selection from recency/path/row count;
- no repair proposal in the local packet.

Return the ZIP to Browser HQ for adjudication.

`AUTHORITY_CENSUS_LOCAL_HARVEST_REQUEST__HARVEST_004`
