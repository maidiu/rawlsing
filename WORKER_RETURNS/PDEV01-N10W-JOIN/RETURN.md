# PDEV-01 — N10W two-input sourcefree qualification

**Status:** `CANDIDATE__TEST_ONLY__INDEPENDENT_REVIEW_REQUIRED`  
**Engineering:** `REVISE__ACTUAL_VALUES_POSITIVE__PROVIDER_VERSION_AND_N9_CURRENTNESS_NOT_ENFORCED`  
**Requested R05/P41 substitution:** `HOLD_NO_COMMON_N9_SCOPE`  
**Source science:** `HOLD`  
**Authority:** `HOLD`

Startup: `773bb412a820949f13a7178b6671327cd56a3bf1`  
Branch: `agent/pyat-pdev01-n10w-join-r1`  
Owned returnroot: `WORKER_RETURNS/PDEV01-N10W-JOIN/`

Session/provider/model verified: `ses_e98c8dfe6ffewNYOqJpvqK21a6`, `opencode-go`, `deepseek-v4.1-flash`, variant `max`.

## Finding

The actual J42 path does consume both inputs and produce an N10W view:

- N9 provider: `W41_READONLY_SOURCE_QUALIFIED_WORLD@1`
- N10E provider: `E41_N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0`
- N10W receiver: `P41_GENERIC_POSSIBILITY_SERVICE@1`
- Shared source rows: `4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02`
- N9 clock: `TEST_CURRENT` at `2027-09-01`
- N9 currentness: `CURRENT_TEST_ONLY_SELECTION`
- View: `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER` / `WORLD_SELECTED_VIEW`
- View hash: `062c4c5fc59c5618582d43f9e4c917ab97a32ecfd7249d5bfba2824fe0767287`
- P41 receipt hash: `339af8fd45d13f24604a22a579a8920d89ebe185ca7d26be421aa7cb248cdf00`
- Joined receipt hash: `bbe107189fd8be9c805668a4beb9263b7182ecd4c2d18ced9f6de02da3519825`
- Three N10E steps: all `EXACT_SUPPORTED`, denominators 32/16/8.
- Three N10W consumptions: all `EXACT_SUPPORTED`, `same_evidence_object=true`, `LIVE_TRACE`.

Two independent J42 builds produced byte-equal receipt files, identical view hashes, identical N10E steps, identical N10W consumptions, and identical N9 routes.

## Why the engineering verdict is REVISE

The public receiver does not enforce the requested provider-version/currentness identity. In the actual receipt:

| Hostile mutation | Actual result |
|---|---|
| N9 provider `W41_WRONG_VERSION@1` | positive `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER` |
| N10E provider `E41_WRONG_VERSION@1` | positive `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER` |
| N10W provider `P41_WRONG_VERSION@1` | positive `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER` |
| N9 currentness `REVOKED` | positive `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER` |
| N9 selection moved to `2099-01-01` | positive `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER` |

The same mutated receipts retain the old P41 `content_hash`; the receiver does not check it. The receiver therefore proves a caller-supplied shape, not compatible provider/version/currentness identity. This is a direct `REVISE` finding: the actual values are positive, but the public qualification path cannot reject a mismatched version or revoked N9 currentness.

Missing-parent controls do refuse:

| Control | Actual result |
|---|---|
| Missing N9 provider | `JOINED_PROVIDER_IDENTITY_MISMATCH` |
| Missing N10E steps | `JOINED_CONSUMER_NOT_PRODUCTIVE` |
| Missing second structural field | `WORLD_REQUIRES_AT_LEAST_TWO_FIELDS` |
| Wrong source rows | `JOINED_SOURCE_ROWS_MISMATCH` |
| R05 rows against J42 receiver | `JOINED_SOURCE_ROWS_MISMATCH` |
| Wrong requested as-of | `JOINED_AS_OF_MISMATCH` |

These controls are preserved in `J42_JOIN_WITNESS.json`; the version/currentness defects are in `VERSION_AND_IDENTITY_NEGATIVES.json`.

## R05/P41 boundary

The existing R05→P41 path also executes and returns `R05_WORLD_SELECTED_VIEW`, but its N9-labelled parent is:

`E04_TEST_ONLY_SELECTED_WORLD_M4_M5@1`

with `n9_world.currentness = CURRENT_TEST_ONLY_SELECTION`. It is not W41 N9. The R05 source rows are:

`a585bd130c1a935cdef7723095483ccf228da633f58b9110c8ca21a189595b54`

which are not the J42 W41/E41 rows. Passing those rows to the actual W41/E41 receiver produced `JOINED_SOURCE_ROWS_MISMATCH`.

R05/P41 therefore cannot be treated as a two-input N9+N10E join merely by renaming its E04 test-selected world. D2P3 was not used as N9 and was not relabelled; it remains the sourcefree GSS/NCA field reader accepted at candidate `cfe7dc6111afcb8eda26eb9a54f6cad43b6d1584` / review `830a9656cb65f00337d5bcd0f7373dbef11d50df`, with engineering `PASS_SCOPED_ENGINEERING` and N9/science/authority held.

The smallest next dependency for the R05-specific claim is an actual W41-style N9 selected world bound to the R05 source/release/rows, or an explicit scope switch to the already compatible J42 E41 N10E/W41 N9 pair. No new scientific rule, source, or parent object is authorized here.

## Exact commands and hashes

The exact replay is recorded in `COMMANDS.md`; `replay.sh` is executable and writes only under this returnroot plus one temp directory. The decisive J42 build was:

```sh
git archive f53cb0d2bce52640268c844c398bbd8007d28edc \
  WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1 \
  -o "$BASE/j42.tar"
tar -xf "$BASE/j42.tar" -C "$BASE"
ln -s "$ROOT/rawlsing_next" "$BASE/rawlsing_next"
printf 'gitdir: %s\n' "$(git -C "$ROOT" rev-parse --absolute-git-dir)" > "$BASE/.git"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" \
  python3 "$BASE/$J42_PACKET/runtime/j42_build.py" --outdir "$BASE/out"
```

The W41 artifact referenced by J42 is the accepted W41 return object, not a new parent:

- `b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2:WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/current_historical_asof_world_consumer_receipts.json`
- SHA-256 `09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7`

Evidence hashes:

- `J42_RECEIPTS.json` / `J42_RECEIPTS_2.json`: `c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf`
- `J42_JOIN_WITNESS.json`: `40a33060a7a8a146767c95edfd7342e9e83a913af48e73c9536e059609181798`
- `P41_RAW_TRACE.json`: `6e2b7c2ecd9a2b03e7b7cd7433bca64585d2d33a523bcdaa76ff3d653db583ee`
- `VERSION_AND_IDENTITY_NEGATIVES.json`: recorded in `PINS.json`
- `J42` build stdout: `2ccdeac00a06e09f410b180637b3dc1662ea7a71008967441c3e27adb1b5a796`
- `PINS.json`: source pins, commits, providers, and the exact D2P3 boundary.
- `W41_ARTIFACT_BOUND.json`: exact accepted W41 artifact identity.

## Limits

TEST_ONLY sourcefree W41/E41/P41 service and synthetic E04 rows only. N9 currentness is `CURRENT_TEST_ONLY_SELECTION`, not operative N9 or CURRENT. No original source/respondent read, original science, N5/N6/EE13, N9/OC05 installation, N11, N12, actor/Sorok, protected merge, CI/prod, new worker/model/provider, or production adoption. No N10W global-installation or full N9 claim.

**Next:** distinct nonauthor review of this return and the actual J42 replay; the author does not self-accept. The version/currentness gap must be repaired by its existing owner, not silently accepted.
