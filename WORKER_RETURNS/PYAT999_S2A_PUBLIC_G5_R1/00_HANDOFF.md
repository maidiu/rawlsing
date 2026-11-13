# PYAT999 S2-A — public selector repair G5 recheck

## Verdict

**`REVISE_EXACT_DEFECT`** at code/test cut
`1cb7977b78022f8def26b769714b4c7ac519ece0`.

The author repair correctly fixes the original **locator-only** H26 RED and adds
canonical ordering, but it does **not** authenticate the projected
`RespondentEvent` selector columns against canonical `body_json`/exact event
refs. A coherent attack that changes both the projected semantic column and the
matching locator, while leaving body_json/ref and external I02 roots intact and
re-pinning the physical manifest, still passes.

The result is stronger than the original defect:

- original 9d96 locator-only RED: public `select_events` 0 vs native 1, no
  refusal; actual native I03 refused;
- coherent projected+locator attack on 1cb: public `select_events` 0 vs native 1,
  no refusal; **actual native `execute_i03` returned a different fact with no
  refusal** (oracle `8867cb...`, observed `e8b384...`).

The body/ref digest was unchanged; projected `native` and locator `native` were
both changed; the manifest was coherently re-pinned. This directly violates the
original H26 body-truth requirement and the S2-A actual native first-reader
contract.

## Exact artifact

- Code/test cut: `1cb7977b78022f8def26b769714b4c7ac519ece0`
- Baseline: `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`
- Author return content: `17e1471550c7e77228a40607d9eaaeef4b3fc971`
- Target file: `rawlsing_next/pre553_source_direct_parquet_estate.py`
- Baseline blob: `0e4b34ce4973bb4d23b6105faea55b9056ecf373`
- Repaired blob: `dca76c98f6c097bb8d79316087eaf548b1b45594`
- New test blob: `cdadb84531659a0dc9264b740e12d9f084e5380b`
- Owner grant: `owner_comment_6866766494.md@66c9dd38fa31d075b99b1bdbf90ca03a56f29b08`
- S2-C accepted: `b7b697b69f0acea12174937ee824c19ac34ac284`
- Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme`; not author/fixer.

The author delta is confined to the granted public selector file plus the new
S2-A test. Accepted S2-C writer/schema/manifest/layout/tests, native I03,
S2-D, science, current, issuer and prior returns were not edited.

## Original RED reproduced

The prior independent witness was run unchanged against pristine `9d96`:

- native selected 1; normal public 1; poisoned public **0** with no refusal;
- native I03 refused the locator-only poison;
- body/ref corpus unchanged; exit 0.

## Author green evidence

- New S2-A test file: **5 passed in 2.40 s**.
- S2-A focused four files: **62 passed in 11.65 s**.
- S2-C focused: **31 passed in 10.87 s**.
- S2-D focused: **31 passed in 22.47 s**.
- The five tests check locator-only poisons, aliases/order, empty/routing,
  changed/restore and current/root. They do **not** change both projected
  columns and locator.

## Independent coherent body-truth attack

Script:
`WORKER_RETURNS/PYAT999_S2A_PUBLIC_G5_R1/s2a_coherent_body_attack.py`

Raw:
`evidence/s2a_coherent_attack.json`

Actual observed:

```text
canonical body_json/ref digest before == after
projected RespondentEvent.native changed
event_locator.native changed
physical manifest coherently re-pinned
public select_events: 0 (native expected 1), no error
actual execute_i03: changed fact e8b384..., no error
native oracle fact: 8867cb...
```

Root cause: `_stage_validated_public_selector` reads projected selector columns
and the matching locator, then compares them to each other. It never reads the
canonical `body_json`/event ref for every row. `DirectEstateI03Session._build`
follows the same projected-column trust for the native path; coherent changes to
both projected columns and locators therefore change the actual native fact.

## Required next owner path

1. Within the existing public-selector grant, validate every canonical
   `body_json`/event ref against the projected respondent/native/canonical/
   component/state/occurrence fields and the locator before filtering. Add the
   coherent projected+locator regression; assert public refusal and exact
   restored selection.
2. A separate narrow S2-C/native-I03 owner decision is required for the native
   `DirectEstateI03Session` body-truth gap, because the current owner grant
   explicitly freezes native I03. The native path must refuse the same coherent
   poison before returning a fact, not only the locator-only poison.
3. Freeze the corrected SHA and return to this same G5. No adapter is authorized
   by the current grant; no product patch was made by this reviewer.

## G1–G5

- **G1 PASS:** exact owner grant, original H26–H30, code/test blobs and allowed
  public-selector symbols pinned.
- **G2 PASS_SCOPED:** normal public/native positive, changed/restore, ordering
  and existing tests pass.
- **G3 FAIL:** coherent projected+locator attack yields public undercount and a
  changed actual native fact with no refusal; body_json/ref was never validated.
- **G4 PASS_SCOPED_FIXTURE:** material 256-respondent probe rerun; retained
  `9,758,503 B`, selected index `16,384 B`, source opens none, 3 family opens /
  257 row-group reads / 1 body reconstruction per public select, cold/repeat
  select `0.5385/0.1247 s`, parent `152,174,592 B`, child `60,084,224 B`,
  process-tree wrapper sampled peak `213,860,352 B` (286 samples), C11 builds 0,
  `pq.read_table` 0; 100k/6 GiB NOT_RUN.
- **G5 FAIL / REVISE_EXACT_DEFECT:** one runnable actual native first-reader
  breach and a precise owner path.

The author's Linux 91/proc evidence was read but not independently rerun; the
decisive Darwin SEV-0 already refuses acceptance and Linux cannot cure it.

## Limits

Sourcefree TEST_ONLY only. No original35/source science, production CURRENT,
full 100k/6 GiB, Linux new-module or protected merge claim. Integration
**UNMERGED**. The 256-respondent resource probe is not an integrated benchmark.

## Linux preservation

Existing qualified Lima `s2b` was used without new VM/config changes. The
inherited S2-C/proc suite (four files) passed **86/86 in 38.68s**; the new S2-A
five-test file passed **5/5 in 3.38s**. These are separate counts, not an
invented 91/91 sum. The decisive coherent body-truth attack remains a Darwin
SEV-0; Linux cannot cure it.

## Remote verification

Review content commit `8e788f7e622781a0950ff07a382d3f651d4e4462` was pushed to
`origin/review/pyat999-s2a-public-g5-r1`. Direct remote verification found the
product tree unchanged from `1cb7977b` and the remote receipt valid. See
`evidence/remote_verification.txt`.
