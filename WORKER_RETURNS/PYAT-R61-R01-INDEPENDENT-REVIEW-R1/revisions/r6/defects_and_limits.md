# R61-R01V R6 defects and limits — REVISE

Verdict: **REVISE**. The retained campaign owner is a substantial improvement
over R5: public lineage refs, retained plans and issuance records defeat the
old caller plan/parent injection attacks; R3 A1–A3, D=3 changed-data arithmetic,
hidden 75/25 minority, nonwinning exploration and post-activation cold restore
all pass. But creation does not validate source/release compatibility, restore
does not validate the supplied query/condition context, self-consistent forged
snapshots are admitted with a forged pin, and generation-1 multiple batches are
refused. A4 therefore remains unqualified. Candidate files were not edited.

Repro commands (revision-relative):

```sh
/usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r6/independent_probes/test_r01v_r6_hostile.py \
  -q -o addopts=''
/usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r6/independent_probes/defect_demonstration.py
```

## D1 — Create accepts a source release absent from the repository; execution silently succeeds (blocking)

**Contract:** R61V A/root record and C.1 Create must validate
root/source/release/authority compatibility. F1/F5 require exact source/release
binding and wrong source/release to be a typed limit.

**Observed:** `create_campaign` (`native_map.py:2438`) checks only that the
policy is a `RecurrencePolicy` and the release tuple is non-empty. It does not
resolve the releases in `repository`, compare them with the root predicate's
scope/universe/source authority, or validate the query/root relation.

**Repro (H2):** create a campaign whose `source_release_refs` is a fabricated
`C11_SOURCE_RELEASE@1` ref with a `'f'*64` hash. Creation succeeds, generation-1
issuance succeeds, and execution succeeds with `no_drop_ok: true`. The four
native receipts carry the fabricated release ref
(`evidence/defect_demonstrations.json`, `H2_bogus_release`). The facts are still
evaluated from the root predicate's source, so the campaign claims a source
release it never checked.

**Required:** at Create, resolve every release in the pinned repository and
validate root predicate authority/scope, target/query and owner context against
those releases; otherwise typed-refuse. At Execute, re-resolve the retained
release/authority and refuse before the native call if any identity is missing,
mismatched or unresolvable.

## D2 — Restore accepts a wrong query context and an incomplete condition catalog (blocking)

**Contract:** F5 requires restore to check source/root/policy and the full
frozen context; missing/wrong source/root/policy must be a typed limit. C.6
snapshot restore must preserve the same records and authority boundary.

**Observed:** `RetainedRecurrenceCampaign.restore` (`native_map.py:2256`)
reconstructs the root from snapshot bytes but accepts caller-supplied
`repository`, `authority_registry`, `authority_factory`, `condition_catalog`
and `query_object` without comparing them with the snapshot's
`root.query_ref`, frozen `condition_catalog` or native configuration. The
snapshot's own `condition_catalog` is not compared with the supplied catalog.

**Repro (H3):** restore a valid snapshot with a query object targeting `s3`
instead of the original `t` query. Restore succeeds; a subsequent issue and
execute succeed, and the new plan's `query_ref` differs from the retained
`root.query_ref` (`evidence/defect_demonstrations.json`,
`H3_wrong_restore_query`). The restored campaign now holds inconsistent root
and plan context.

**Repro (H8):** restore with only the generation-1 condition predicates from a
snapshot whose frozen catalog contains six entries. Restore succeeds; a later
issue with a missing condition fails only then with
`CONDITION_NOT_IN_CAMPAIGN_CATALOG` (`H8_incomplete_restore_catalog`).

**Required:** at restore, compare supplied `query_object.ref` with
`root.query_ref`, supplied condition catalog with the snapshot's frozen
catalog, and supplied repository/registry/authority factory identity with the
pinned native configuration; typed-refuse on any mismatch before accepting the
snapshot.

## D3 — Self-consistent forged snapshot is admitted with a supplied forged pin (blocking under F5)

**Contract:** F5: "A self-consistent forged checkpoint supplied as subject data
cannot replace the original configuration." D: the coordinator supplies the
expected checkpoint ref/hash separately from untrusted snapshot bytes.

**Observed:** `restore` checks only
`snapshot.checkpoint_ref == hash(payload) == expected_checkpoint_ref`. There is
no independently retained original checkpoint inside the campaign or host
configuration. A caller who supplies both forged snapshot and forged pin gets a
restored campaign.

**Repro (H4):** alter a snapshot lineage `parent_id`, recompute every internal
hash and the checkpoint, and pass the recomputed pin. Restore succeeds, retains
the original `campaign_ref`, and exposes the forged lineage
(`evidence/defect_demonstrations.json`, `H4_forged_snapshot_forged_pin`). The
same altered snapshot with the original pin is correctly refused, so the
self-hash check works; what is missing is an independent pin anchor.

**Required:** bind restore admission to an independently retained original
checkpoint/ref (host configuration or campaign-held pin registry), not only to
the pin argument supplied by the same caller. If the declared trusted
coordinator is the sole holder of the pin, this must be made an explicit
trust-boundary limitation and the F5 "cannot replace" claim narrowed.

## D4 — Multiple explicit batches at generation 1 are refused (blocking)

**Contract:** C.2/E/F4: issue sequence and discovery generation are separate;
multiple explicit batches at a generation are allowed and all counted.

**Observed:** `_last_plan` is passed as `previous_plan` for every later issue,
but `build_recurrence_issue_plan` still rejects any `previous_plan` for
generation 1 (`ROOT_GENERATION_MUST_NOT_HAVE_PREDECESSOR`). Multiple generation-2
batches work and are counted (context evidence: cumulative 8 then 12), so this
is specifically a generation-1 restriction.

**Repro (H1):** issue generation 1 from the root, then issue a second explicit
generation-1 batch. The second is refused
(`evidence/defect_demonstrations.json`, `H1_multiple_gen1_batches`).

**Required:** allow a same-generation predecessor issuance for generation 1
while retaining the root-only parent rule; derive counts from the retained
issuance records and count both batches. Do not add a one-plan-per-generation
restriction.

## D5 — A restored completed execution cannot be activated (blocking for pre-activation snapshots)

**Contract:** F5: restore a full issuance/execution/lineage/activation prefix
and run the next generation from a fresh process; C.6 preserves the same
records and authority boundary.

**Observed:** `restore` stores execution records with `native_result=None`.
`execute` returns the retained execution ref for a completed issuance, so it
does not re-run native. `activate` refuses with
`RESTORED_EXECUTION_NATIVE_RESULT_NOT_REPLAYED` whenever no activation record
exists in the snapshot.

**Repro (H5):** snapshot after generation-1 execution but before activation;
restore, retry execute (returns the retained execution), then activate. The
activation is refused (`evidence/defect_demonstrations.json`,
`H5_restore_pre_activation`). The author's cold test works only because it
snapshots after activation.

**Required:** either reconstruct/replay the retained native execution from
canonical handoffs and actual receipts at restore (then allow activation), or
support activation from retained receipt/handoff records without inventing a
native result. If execution-only snapshots are intentionally unsupported,
return a typed missing-activation-prefix limit at restore and narrow the F5
claim.

## D6 — Stopped-budget issuance does not advance the issuance predecessor head (secondary)

`issue` updates `_last_issuance_ref` and `_last_plan` only for
`RECURRENCE_ISSUED` plans. A `STOPPED_BUDGET` issuance is appended to
`_issue_order` but the next issuance's `predecessor_issuance_ref` remains the
last work-bearing issuance (or `None`).

**Repro (H6):** with `per_generation_issued_cap=0`, issue twice. Both records
are `STOPPED_BUDGET`, cumulative 0, but the second record's
`predecessor_issuance_ref` is `None`, not the first stopped issuance
(`evidence/defect_demonstrations.json`, `H6_stopped_issuance_chain`). The full
issuance prefix/predecessor chain is therefore not retained for no-work
records.

**Required:** advance the issuance head and predecessor reference for every
committed issuance, including stopped/no-work, while leaving counts unchanged.

## D7 — Duplicate condition catalog silently collapses (secondary)

`create_campaign` builds a dict keyed by `(key, typed_value_key(value))`.
Duplicate catalog entries silently overwrite, so the frozen admitted inventory
is mutated rather than rejected.

**Repro (H7):** create with `list(s1) + list(s1)`; creation succeeds and the
catalog size is 2 (`evidence/defect_demonstrations.json`,
`H7_duplicate_catalog`).

**Required:** reject duplicate catalog keys or differing predicates for the
same key/value with a typed refusal.

## D8 — Execute revalidates only part of the retained parent identity (defense-in-depth gap)

**Contract:** C.3 says Execute resolves the retained plan and parent lineage
again, including full ancestry/root/policy/source and
handoff/receipt/predicate/replay equality; direct execution cannot trust an
earlier planning check.

**Observed:** `RetainedRecurrenceCampaign.execute`
(`native_map.py:2066-2075`) checks only parent id, predicate ref, kind and
producer generation against a parent-by-id map. It does not compare the plan
parent's ancestry conditions/predicates, source releases, receipt/replay refs
or handoff content with the retained lineage. Under the live public API there
is no plan/parent injection path, so no independent live exploit was found;
the gap becomes relevant only through the forged-pin restore path or a future
compatibility argument that accepts public plan/parent views. It is recorded
because the authored claim is broader than the code.

**Required:** compare every identity-bearing parent field (ancestry, source
releases, receipt/replay/handoff, canonical parent ref) between the retained
plan and the retained lineage before the native call.

## Positive findings retained (not acceptance)

- Author suite independently replayed: 28 passed, 0 failed/error/skip.
- R3 A1–A3 controls independently replayed: 10 passed.
- Reviewer changed-data D=3 owner positive: 2 passed. Independent expected
  operation sets matched content/multiplicity; independent root/parent typed
  states matched; neutral 50/50 parent contained 75/25 opposite subgroups;
  nonwinning exploration was retained; in-process and fresh-process
  post-activation restore ran real next-batch execution.
- Reviewer controls: 8 passed, including retry idempotency/no second native
  call, zero-cap no-native-call, forged lineage/requested generation/predecessor
  rollback/activation label/unknown refs, cross-campaign lineage, deep-detached
  inspect, altered snapshot with original pin, multiple generation-2 batches,
  and run-local concurrent execute.
- The public campaign facade does defeat the R5 live plan/parent injection
  attacks: forged lineage refs, caller parent relabel, caller handoff swap and
  caller predecessor undercount have no public registration path.
- The author manifest's 7 report hashes and four code blobs were independently
  reproduced; manifest self-exclusion is explicit.

## Minimal missing function / owning seam

`rawlsing_next/universal_grammar/native_map.py`:

1. At Create, resolve releases/root/authority/query/target and reject
   incompatible or nonexistent source context.
2. At Execute, revalidate retained release/root/policy/authority plus full
   parent ancestry/receipt/replay/handoff equality before the native call.
3. At Restore, compare supplied query/condition/repository/authority context
   with the snapshot's frozen context and typed-refuse on mismatch.
4. Bind restore admission to an independently retained original checkpoint/pin,
   not only the caller argument.
5. Allow multiple explicit generation-1 batches with retained count/predecessor
   accounting.
6. Replay or reconstruct retained native execution so a pre-activation snapshot
   can activate, or type- limit that snapshot state explicitly.
7. Advance the issuance predecessor/head for stopped/no-work issuances.
8. Reject duplicate condition-catalog entries.

## Preserved limitations

Reference caps/rows are TEST_ONLY synthetic engineering, not original science.
The owner is a local trusted-runtime campaign, not a protected issuer, signing
service, global durable uniqueness, R04 joined custody or R09 capture. R04/R09
durable custody/fork prevention is NOT_REACHED. R03 remains NOT_STARTED. No
original 35/1890, global F6/F7/F8, N11/N12, Sorok, production/CI or J52/W52
claim follows. R08/R61Q projection/export is a separate author lane and was not
reviewed or repaired here.
