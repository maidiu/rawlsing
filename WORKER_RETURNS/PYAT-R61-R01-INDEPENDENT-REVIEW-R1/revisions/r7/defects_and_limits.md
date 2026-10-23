# R61-R01V R7 defects and limits — REVISE

Verdict: **REVISE**. R7 is a substantial and mostly successful whole-function
repair: create now resolves releases/source/query/authority; chronology is
independent of generation; multiple generation-1 batches count; stopped/no-work
records advance the head; completed-prefix restore activates without rerunning
discovery; fixed-pin restore and full record closure work; and the changed-data
D3/hidden-75/25/exploration/cold positives pass. Four remaining validation
defects prevent `ACCEPT_SCOPED_LOCAL` at the exact generic facade. Candidate
files were not edited.

Repro commands (revision-relative):

```sh
/usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r7/independent_probes/test_r01v_r7_hostile.py \
  -q -o addopts=''
/usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r7/independent_probes/defect_demonstration.py
```

## D1 — Target label is not validated against the query target (blocking)

**Contract:** R61AF section 3: Create must validate "target/query
compatibility". The root record carries both `target_label` and `query_ref`.

**Observed:** `_native_campaign_context` (`native_map.py:1792`) validates the
query's target refs against the repository, query/root predicate equality,
target arity, J and authority fitness, but never checks that `target_label`
identifies the query's actual target. `_create_campaign_from_catalog` stores
`target_label` and `query_ref` independently.

**Repro (H1):** create with `target_label="wrong-label"` and the unchanged
`query` targeting `t`. Creation, issue and execution all succeed; the retained
plan is labeled `wrong-label` while its query ref is the `t` query
(`evidence/defect_demonstrations.json`, `H1_target_label_mismatch`).

**Repro (H2):** create with `target_label="t"` and a query targeting `s3`.
Creation, issue and execution succeed; the plan claims target `t` while the
query target is `s3` (`H2_query_target_mismatch`). This is not merely a display
label: the target label is part of rule/operation identity and the plan
metadata presented to R03.

**Required:** at Create (and through the shared restore context validator),
derive the target identity from the pinned source/query inventory and require
`target_label` to identify exactly that target; typed-refuse any mismatch
before native work.

## D2 — Condition catalog key/value is not validated against the predicate semantics (blocking)

**Contract:** R61AF section 3: Create must resolve "every ... catalog
predicate" and validate the "complete typed condition inventory"; R61V A pins
the admitted predicate inventory. Predicates must affect real facts, not
labels.

**Observed:** `create_campaign` (`native_map.py:2710`) checks the typed
`(key, value)` key and duplicates, and `_native_campaign_context` validates the
predicate's source scope, risk set and authority. It does **not** check that the
predicate actually represents the keyed question/value (for example by matching
the response leaf question/value refs). `_condition_predicate` later returns
whatever predicate was stored for the key.

**Repro (H3):** create with catalog entry `(OccurrenceKey("s1"), 0)` bound to
the predicate for `s1=1`. Creation, issue and execution all succeed. The plan
records condition key `s1`, value `0`, but its bound predicate content hash is
the `s1=1` predicate, not the `s1=0` predicate
(`evidence/defect_demonstrations.json`, `H3_catalog_key_predicate_mismatch`).
The execution therefore conditions on `s1=1` under the label `s1=0`.

**Required:** at Create, validate each catalog `(key, value, predicate)` against
the pinned source's actual response semantics for that typed key/value (exact
leaf/question/value refs or an equivalent canonical inventory lookup), and
typed-refuse mismatches. Restore must reuse the same validator, which it already
does for the other frozen-context checks.

## D3 — Malformed public condition key crashes instead of typed refusal (blocking for public API)

**Contract:** Ordinary callers may propose governed operation selections; an
invalid proposal makes no accepted record. Product refusals must be typed, not
raw Python attribute errors.

**Observed:** `RetainedRecurrenceCampaign.issue` does not validate the type of
each condition key. `_condition_predicate` (`native_map.py:2117`) assumes
`key.key` and raises `AttributeError` for a string key.

**Repro (H4):** `campaign.issue(parent_lineage_refs=(root_ref,),
condition_refs=(("s1", 0),))` raises
`AttributeError: 'str' object has no attribute 'key'`
(`evidence/defect_demonstrations.json`, `H4_malformed_condition_key`). No
record is accepted, but the caller gets a setup/attribute crash rather than a
product refusal.

**Required:** validate each `condition_refs` entry is `(OccurrenceKey, typed
value)` before lookup and raise `RecurrenceRefusal` with an exact reason (the
Create path already has `CAMPAIGN_TYPED_OCCURRENCE_KEY_REQUIRED`).

## D4 — Duplicate condition refs raise raw ValueError rather than RecurrenceRefusal (secondary)

`build_recurrence_issue_plan` raises bare `ValueError(
"RECURRENCE_DUPLICATE_CONDITION_PREDICATE")` for duplicate condition predicate
refs. The message is explicit, but it is not the `RecurrenceRefusal` class used
by the owner API. Repro H5
(`evidence/defect_demonstrations.json`,
`H5_duplicate_condition_refs`). Convert to `RecurrenceRefusal` for a consistent
typed public refusal.

## R61AF fixed-pin correction and forged-both-inputs

R61AF reclassifies the R6 forged-snapshot-plus-forged-pin case as host-trust
replacement, outside the in-scope refusal gate. We did **not** use that case as
a defect. The fixed original pin correctly refuses an altered/rehashed snapshot
and a missing pin; genuine snapshots restore. In addition, R7's internal
closure refused the forged-lineage mutation even when the snapshot and pin were
both forged (`RESTORE_FULL_RECORD_CLOSURE_MISMATCH`), which is stronger than
required. The host-trust demonstration is recorded in
`evidence/defect_demonstrations.json` with that note and is not counted as a
blocker.

## Positive findings retained (not acceptance)

- Author suite independently replayed: 31 passed, 0 failed/error/skip.
- R3 A1–A3 controls independently replayed: 10 passed.
- Reviewer changed-data D=3 owner positive: 2 passed. Independent expected
  operation sets matched content/multiplicity; independent root/parent typed
  states matched; neutral 50/50 exploratory parent contained 75/25 opposite
  subgroups; nonwinning exploration was retained; in-process and fresh-process
  cold restore ran real next-batch execution.
- Reviewer controls: 15 passed, including multi-batch generation-1 chronology
  (4 then 8), stopped/no-work predecessor advancement, pre-activation restore
  without rerun, post-activation existing activation, zero-cap no-native-call,
  retry/no-second-native-call, concurrent serialization, deep-detached inspect,
  fixed-pin refusal, wrong query/catalog refusal, duplicate catalog/missing
  release refusal, typed receipt states and inflight typed HOLD.
- Missing receipt, missing handoff, altered lineage ancestry, altered cumulative
  count and duplicate execution records all refused with self-consistent
  recomputed pins (internal closure), demonstrating R7 repaired the R6 D2/D5
  classes.
- The author manifest's 8 report hashes and four code blobs were independently
  reproduced; manifest self-exclusion is explicit.

## Minimal missing function / owning seam

`rawlsing_next/universal_grammar/native_map.py`:

1. In the shared Create/restore native-context validator, bind `target_label`
   to the pinned query target identity and reject mismatch.
2. Validate each catalog `(key, value, predicate)` against the pinned source's
   exact typed response leaf/predicate semantics, not only scope/risk/authority.
3. Validate `issue(condition_refs)` key type and duplicate refs and raise
   `RecurrenceRefusal` before planning.
4. Reuse the same validator on restore (already structurally shared).

No new engine, pin service, native-owner edit or scientific authority is
required.

## Preserved limitations

Reference caps/rows are TEST_ONLY synthetic engineering, not original science.
The owner is a local trusted-runtime campaign, not a protected issuer, signing
service, global durable uniqueness, R04 joined custody or R09 capture. R04/R09
durable custody/fork prevention is NOT_REACHED. R03 remains NOT_STARTED. No
original 35/1890, global F6/F7/F8, N11/N12, Sorok, production/CI or J52/W52
claim follows. R08/R61Q is a separate lane and was not reviewed or repaired.
