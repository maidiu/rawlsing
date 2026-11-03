# PDEV-01 N10W identity repair — independent review

**Candidate:** `877f974a0e70ea591118fd94f558d73f426202dc`  
**Review branch:** `review/pyat-pdev01-n10w-identity-r1`  
**Scope:** TEST_ONLY sourcefree W41/E41/P41 J42 and synthetic E04 only.  
**Write root:** `WORKER_RETURNS/PDEV01-N10W-INDEPENDENT-REVIEW/`

## Verdict

**`REVISE__ACTUAL_J42_84_AND_COLD_POSITIVE__FIVE_REHASHED_MUTATIONS_AND_MISSING_STALE_CONTROLS_REJECTED__SELECTED_CLOCK_STILL_CALLER_SELF_CONSISTENT`**

Engineering positive scope is real: the actual J42 build produces **84/84**
positive guarded views, both cold builds are byte-equal, and the isolated guard
rejects the five recorded rehashed provider/currentness mutations, missing
parents, stale P41 hash, R05 substitution, wrong rows and wrong as-of.

The repair is not accepted because its selected-clock check is self-consistent
inside the caller-supplied receipt rather than bound to the trusted W41 input.
Changing both `n9_world.selection` and `j42_bindings.w41_clock` to `2099-01-01`
and recomputing the P41 `content_hash` still produces a positive selected view.
The guard never compares either field to the pinned W41 artifact clock
(`09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7`).

Science and authority are **HOLD**: TEST_ONLY sourcefree values, no operative
N9/CURRENT, no original source, no N9/N11/N12, no production edit, no new trust
issuer or adoption.

## Independently measured

- Actual J42 commit: `f53cb0d2bce52640268c844c398bbd8007d28edc`
- Actual build 1 and build 2 receipts:
  `c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`
  (byte-equal; 2,596,100 bytes each)
- Actual views: **84 positive / 84**, no first refusal
- Cold view hashes: all **84** equal
- Positive guard view: `062c4c5fc59c5618582d43f9e4c917ab97a32ecfd7249d5bfba2824fe0767287`
- N9: `W41_READONLY_SOURCE_QUALIFIED_WORLD@1`
- N10E: `E41_N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0`
- N10W: `P41_GENERIC_POSSIBILITY_SERVICE@1`
- N9 currentness: `CURRENT_TEST_ONLY_SELECTION`
- Three N10E steps `EXACT_SUPPORTED`; N10W `EXACT_PROGRESSIVE_CHAIN` /
  three live consumptions.
- Source rows: `4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02`

## Five rehashed mutations

All five were refused after recomputing the P41 hash:

| Mutation | Guard result |
|---|---|
| wrong N9 provider version | `JOINED_PROVIDER_IDENTITY_MISMATCH` |
| wrong N10E provider version | `JOINED_PROVIDER_IDENTITY_MISMATCH` |
| wrong N10W provider version | `JOINED_PROVIDER_IDENTITY_MISMATCH` |
| revoked N9 currentness | `JOINED_N9_CURRENTNESS_INVALID` |
| mutated N9 selected clock | `JOINED_N9_SELECTION_MISMATCH` |

The unchanged public receiver still accepts these same mutations (recorded in
`base` fields of `evidence/review_evidence.json`); the guard is an isolated
overlay, not production enforcement.

## Remaining defect: trusted clock

The guard compares:

```text
n9_world.selection  ==  j42_bindings.w41_clock
```

Both are caller-supplied receipt fields. It does not compare either to the
trusted W41 artifact `worlds[base/TEST_CURRENT/budget5].clock`, whose pinned
artifact is:

`b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2:WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/current_historical_asof_world_consumer_receipts.json`
SHA-256 `09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7`.

Simultaneous mutation test:

1. Set both `n9_world.selection` and `j42_bindings.w41_clock` to
   `{mode: AS_OF, published_asof: 2099-01-01, valid_at: 2099-01-01}`.
2. Recompute P41 `content_hash`.
3. Guard returns `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER`,
   `WORLD_SELECTED_VIEW`, view hash
   `42885d9d078a4a8341d42f404ff0a37b5f43b86748314091e155931fab19490c`.

Selection-only mutation with rehash is refused (`JOINED_N9_SELECTION_MISMATCH`),
which confirms the comparison is only between the two caller fields. The
trusted W41 artifact clock remains `TEST_CURRENT / 2027-09-01`.

## Other controls

All independently executed and refused:

- stale P41 hash → `JOINED_RECEIPT_CONTENT_HASH_MISMATCH`
- missing N9 provider → `JOINED_PROVIDER_IDENTITY_MISMATCH`
- missing N10E steps → `JOINED_CONSUMER_NOT_PRODUCTIVE`
- missing P41 or joined receipt → `JOINED_VIEW_NOT_FOUND`
- missing second field → `WORLD_REQUIRES_AT_LEAST_TWO_FIELDS`
- wrong source rows → `JOINED_SOURCE_ROWS_MISMATCH`
- wrong as-of → `JOINED_AS_OF_MISMATCH`
- R05 provider substitution → `JOINED_PROVIDER_IDENTITY_MISMATCH`

## Exact command

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review
PYTHONHASHSEED=0 python3 WORKER_RETURNS/PDEV01-N10W-INDEPENDENT-REVIEW/run_review.py
```

`run_review.py` extracts and runs actual J42 twice from pinned commit
`f53cb0d2...`, then runs the guard and all controls. Evidence:
`evidence/review_evidence.json`, `evidence/J42_RECEIPTS_actual_{1,2}.json`,
`logs/`, `SOURCE_PINS.json`.

## Required repair

Bind the selected clock to a trusted input, not only two fields of the same
receipt. The existing W41 artifact/clock and its exact snapshot/view hash are
available; no new trust authority is needed. Any repair must reject both
fields being changed together, including after P41 rehash, and must preserve
the actual 84 positive/cold results and all current refusal codes.

## Limits

No original SAV/DTA/source/respondent read. No production code edit, merge,
CI, N9/OC05 installation, N11/N12, actor/Sorok, new trust authority, or new
scientific rule. Candidate remains readonly; only this review root was written.
