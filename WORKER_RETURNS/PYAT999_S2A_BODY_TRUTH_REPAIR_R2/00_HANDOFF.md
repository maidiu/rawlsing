# PYAT999 S2-A — public canonical body-truth repair R2

## Decision

**Public half: `GREEN__CANONICAL_BODY_TRUTH`**  
**Overall S2-A: `HOLD_NATIVE_OWNER__PAIRED_PROJECTION_POISON_REMAINS`**  
**G5: `NOT_DISPATCHED__NATIVE_OWNER_HOLD`**

The public selector now refuses the exact G5 coherent projected-column +
locator poison after reconstructing and checking every event's canonical
`body_json`/ref. The frozen native I03 file was not edited and still returns the
changed fact for the same paired poison. S2-A overall is therefore not accepted.

## Artifact

- Branch: `agent/pyat999-s2a-body-truth-r2`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat999-s2a-body-truth-r2`
- Startup: `c29972ce99cae9672eae20dc7030d4eafe66ada6`
- Previous rejected public repair: `1cb7977b78022f8def26b769714b4c7ac519ece0`
- **Public code/test cut: `5727db0ebecab2c9ae393a49e9bce1be3076a589`**
- Target file before/after:
  - `dca76c98f6c097bb8d79316087eaf548b1b45594`
  - `e8622ac6bf59c4d1ec052e21410e63aab7dd9aa1`
- New S2-A test blob: `40faf558fdd13da063e7c58177e3d7c3d9fce343`
- Frozen native I03 blob at `b7b697`, `9d96`, `1cb`, `c299` and this R2:
  `8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e` — **unchanged**

Changed code/test paths only:

- `rawlsing_next/pre553_source_direct_parquet_estate.py`
- `rawlsing_next/tests/test_pre553_s2a_public_selector_h26.py`

No writer/schema/manifest/layout, native I03/I05, S2-D, science, current,
issuer, accepted test or prior-return file was edited.

## G5 delivery read

- Review delivery: `f88a6c61b89f6c18157f2f789de1b7873bc9e747`
- Review content: `8e788f7e622781a0950ff07a382d3f651d4e4462`
- Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme`
- Receipt/handoff/attack script read directly from the review commit.
- Exact attack script preserved under
  `WORKER_RETURNS/PYAT999_S2A_BODY_TRUTH_REPAIR_R2/baseline/` and run on the
  pristine startup before any source edit.

## Original G5 RED reproduced

The attack changes one projected `RespondentEvent.native` column and the
matching `event_locator.native`; it leaves canonical `body_json`/ref and the
external direct-I02 roots fixed, then coherently re-pins both physical member
hashes and the manifest.

Observed on pristine `c299` (which includes rejected public repair `1cb`):

| Measure | Red |
|---|---:|
| Canonical body_json/ref digest before | `3070d589d6c7255063ed8ac26d90c06e61ed4db4881523266e5918095b895f6c` |
| Canonical body_json/ref digest after | `3070d589d6c7255063ed8ac26d90c06e61ed4db4881523266e5918095b895f6c` |
| Body/ref corpus changed | **No** |
| Projected native changed | Yes |
| Locator native changed | Yes |
| Manifest coherently re-pinned | Yes |
| Public select count | **`0`** (native expected `1`) |
| Public refusal | **No** |
| Native I03 error | **No** |
| Native oracle fact | `8867cb069cbeb3c01a21413a8a4cdb80daf528aae03bce031e69e9aa41aba380` |
| Native observed fact | **`e8b3842a3a0866082d64b4cef994c2e8787dbd7a4f3df8c599e898282002059b`** |
| Native silently changed | **Yes** |

This reproduces the G5 finding exactly. The public selector undercounted; the
native first reader returned a changed fact without refusal.

## Public repair

`VerifiedDirectEstate._stage_validated_public_selector` now, for every event
row before any respondent/target/state filter or first yield:

1. Reads the canonical `body_json` together with projected body metadata.
2. Reconstructs the event through the existing `_object_from_row` codec.
3. Requires exact `RespondentEvent` type and exact canonical ref/object_id/
   content_hash/kind/family identity.
4. Derives the full selector projection from the canonical event and checks
   projected body columns for respondent, native, canonical, component, state,
   universe and occurrence.
5. Checks locator group/offset/ref and projected selector columns against that
   canonical body truth.
6. Retains the earlier complete coverage, duplicate-ref `seen` check, global
   census, bounded selected-ref index and native canonical `ORDER BY ref`.

This is exhaustive per event, not a comparison of projected columns to a
locator or only selected bodies. It uses the existing object codec, not a new
codec. It remains row-group bounded and does not construct a C11 graph or a
persistent second body corpus. `states=frozenset()` still validates every row
before returning empty.

## Public GREEN

Same G5 attack after the public repair:

- Public refusal: **`DirectEstateError: physical event posting disagrees with exact native body`**
- Public silent undercount: **false**
- Body/ref digest still unchanged
- Canonical projected/body truth mismatch detected
- Native paired poison: **still silently changed** (`e8b384...` vs oracle
  `8867cb...`) because native I03 remains frozen.

New public regression covers:

- Paired projected + locator poison for native, respondent, canonical,
  component, state and occurrence.
- Invalid canonical `body_json`, ref, object_id, content_hash and kind.
- Public refusal before any yield; exact untampered restore.
- Old locator-only H26/H27/H28/H29 tests, canonical order, repeated occurrences,
  authorized aliases, `native_only`, empty states, routing UNKNOWN,
  current/root and changed/restore remain green.
- Native paired poison is explicitly asserted as a still-changed known owner
  hold; it is **not** changed to an expected green refusal.

## Tests actually run

| Suite | Darwin | Linux Lima s2b |
|---|---:|---:|
| New S2-A body-truth + old 5 | **7 passed in 3.81s** | (included in 64) |
| S2-A focused public | **64 passed in 8.43s** | **64 passed in 12.61s** |
| S2-C focused | **31 passed in 4.78s** | **31 passed in 4.57s** |
| S2-C inherited/proc | not claimed | **86 passed in 37.10s** |
| S2-D focused | **31 passed in 13.19s** | **31 passed in 19.73s** |

Logs under `WORKER_RETURNS/PYAT999_S2A_BODY_TRUTH_REPAIR_R2/evidence/`.
The Linux runner is the existing qualified Lima `s2b` and existing venv; no new
VM/config/environment. Full accepted 202 court and 100k/6 GiB were not run.

## Resource evidence

Own probe copied into this return; no old author/G5 directory was written.

`WORKER_RETURNS/PYAT999_S2A_BODY_TRUTH_REPAIR_R2/resource_probe.py`  
`WORKER_RETURNS/PYAT999_S2A_BODY_TRUTH_REPAIR_R2/resource.json`

Synthetic **256 respondents / 256 events**, sourcefree, not 100k:

| Measure | Value |
|---|---:|
| Retained estate bytes | `9,758,503` |
| Peak disposable selected-index bytes | `16,384` |
| Public select body reconstructions | `257` |
| Public select family opens | `3` |
| Public select row-group reads | `257` |
| Cold public select | `0.2011 s` |
| Repeat public select | `0.2032 s` |
| Cold native I03 | `0.5399 s` |
| Repeat native I03 | `0.5162 s` |
| Selected count | `1` |
| Selected refs equal repeat | `true` |
| Native I03 fact | `SUPPORTED`, repeat equal |
| Parent peak RSS | `150,343,680 B` |
| Fresh-child peak RSS | `63,893,504 B` |
| Fresh-child cold select | `0.2179 s` |
| Fresh-child source opens | `[]` |
| Source-extension opens | `[]` |
| Full C11 builds | `0` |
| `pq.read_table` fallbacks | `0` |
| 6 GiB cap | PASS at material local fixture |
| Integrated 100k/6 GiB | **NOT_RUN** |

The 257 body reconstructions are 256 validation bodies plus the selected body.
Parent and child are single processes; no multi-process tree claim.

## Courts / status

- **G1 PASS:** owner grant, original H26–H30, G5 delivery f88a, exact startup,
  target/test and native blobs pinned.
- **G2 PASS_SCOPED_PUBLIC:** public positive, change/restore, order and all
  public regressions pass; overall S2-A positive held by native red.
- **G3 PUBLIC_PASS / NATIVE_OWNER_HOLD:** public paired projection+locator
  refuses before subset; native paired projection still changes fact and was not
  altered.
- **G4 PASS_SCOPED_FIXTURE:** 256-respondent own resource proof; no 100k.
- **G5 NOT_DISPATCHED:** defer until the Browser owner grants and the same
  author implements the native-file exception; then same reviewer gets one
  coherent final delta.
- **Scientific:** `NO_ORIGINAL35_SCIENTIFIC_ACCEPTANCE`; sourcefree TEST_ONLY.
- **Authority:** no new source/current/issuer/host/merge grant; native exception
  pending existing Browser owner.
- **Integration:** `UNMERGED`.
- **Overall S2-A:** `HOLD_NATIVE_OWNER`, not accepted.

## Native remaining RED

`rawlsing_next/pre553_direct_estate_i03.py::DirectEstateI03Session._build`
remains at frozen blob `8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e`. It reads the
projected selector columns and does not reconstruct canonical `body_json` for
all rows. The exact coherent attack still returns `e8b384...` with no error.
A narrow native-file exception has been requested from the existing Browser
owner; **no native edit was made here**. The public half cannot discharge that
owner breach.

## Self-critique

- Public selector now parses every event body on every call; at 256 events it
  costs about 0.20 s and 257 reconstructions. 100k behavior is unproved.
- The test suite intentionally includes a passing native-known-RED observation;
  this documents the owner hold, not acceptance.
- The legacy private `_locators` helper remains unused; `select_events` is the
  repaired public path.
- Native I03 and public selector now implement body truth in separate code; the
  native half remains unsafe until the owner grant.
- No independent G5 has occurred; the reviewer is not dispatched early.

## Next

Browser owner decides the exact native-file exception. If granted, the same
author applies the canonical body truth check to the frozen native session,
reruns the same coherent attack, and only then the same distinct reviewer
receives one coherent final delta. No additional A/B campaign, adapter,
architecture, science/current/issuer promotion or 100k claim is offered.
