# PYAT999 S2-A — native canonical body truth repair (J1)

## Decision

**`S2A_PUBLIC_NATIVE_BODY_TRUTH_REPAIRED__G5_PENDING`**

The public selector and the native I03 first reader now both refuse the exact
coherent projected-column + locator poison when canonical `body_json`/ref
remains unchanged. Native I03 no longer silently returns a changed fact.

This is an author return. It is **not** independent G5 acceptance and does not
claim production source, scientific issuance, CURRENT, original35, 100k/6 GiB
or protected merge.

## Exact artifact

- Branch: `agent/pyat999-s2a-body-truth-r2`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat999-s2a-body-truth-r2`
- Startup: `a59c6a5a85451330500bd6a939c3faee6dbc94ad`
- **Code/test cut: `ce7704253f6a2381310c3eb2c7412a2d85c5596c`**
- Native file before/after:
  - `8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e`
  - `1dc82ab5658051f35dc1d81cbac30688e84a1623`
- S2-A regression blob: `84db13b94888065a99dbdb77b1aa73eab3653bd8`
- Public selector unchanged: `e8622ac6bf59c4d1ec052e21410e63aab7dd9aa1`
- Owner grant: `https://github.com/maidiu/rawlsing/issues/999#issuecomment-6890211780`

Changed paths only:

- `rawlsing_next/pre553_direct_estate_i03.py`
- `rawlsing_next/tests/test_pre553_s2a_public_selector_h26.py`
- `WORKER_RETURNS/PYAT999_NATIVE_BODY_TRUTH_20261115/`

No writer/schema/manifest/I02, native evaluator, `_selected_events`, public
selector, S2-D, #1006 or accepted prior-return file was edited.

## Exact G5 RED reproduced before edit

The exact attack from the independent delivery
`f88a6c61b89f6c18157f2f789de1b7873bc9e747` was run on pristine `a59c6a5a8`
before touching the native file. It keeps canonical `body_json`/ref and external
I02 fixed while coherently changing projected `RespondentEvent.native` and the
matching locator, then re-pins the physical manifest.

Observed:

| Measure | RED |
|---|---:|
| Body/ref digest | `3070d589d6c7255063ed8ac26d90c06e61ed4db4881523266e5918095b895f6c` |
| Body/ref digest changed | No |
| Public select | `0` vs native `1` |
| Public refusal | No |
| Native I03 refusal | No |
| Native oracle fact | `8867cb069c...` |
| Native observed fact | **`e8b3842a3a...`** |
| Native silently changed | **Yes** |

## Native repair

`DirectEstateI03Session._validate_event_body_truth` is called from `_build` for
every event row before SQLite insertion or native fact construction. It:

- reconstructs canonical `body_json` through the existing `_object_from_row`
  codec;
- requires exact `RespondentEvent` type and exact canonical ref/kind/object_id/
  content_hash/family identity;
- derives respondent, native, canonical, component, state, universe and
  occurrence fields from canonical body truth and checks projected body columns;
- checks locator group/offset/ref and selector fields against the canonical
  body;
- raises typed `DirectEstateError` before the index can serve a fact.

The existing public selector body-truth check is unchanged. All native
evaluator, selected-event, writer/schema/manifest/I02 and S2-D code remains
frozen.

## GREEN evidence

Same exact attack after repair:

- Public: `DirectEstateError: physical event posting disagrees with exact native body`
- Native: `DirectEstateError: cold I03 event posting disagrees with exact canonical native body`
- `actual_native_i03_fact_ref`: `null`
- `actual_native_i03_silently_changed`: `false`
- Body/ref digest unchanged
- Untampered public/native selection and native facts restore exactly.

Regression also covers:

- paired native/respondent/canonical/component/state/occurrence poison;
- invalid `body_json`, ref, object_id, content_hash and kind;
- public and native refusal before any fact;
- repeated/ranked occurrences, native-only precedence, empty states,
  routing `UNKNOWN` versus zero, valid source/current/root;
- changed legitimate input → changed fact → exact restore.

## Tests actually run

| Suite | Darwin | Linux Lima s2b |
|---|---:|---:|
| New S2-A 7 | **7 passed in 3.66s** | included in 64 |
| S2-A focused | **64 passed in 8.92s** | **64 passed in 24.38s** |
| S2-C focused | **31 passed in 4.76s** | **31 passed in 7.80s** |
| S2-C inherited `/proc` | not claimed | **86 passed in 39.79s** |
| S2-D focused | **31 passed in 13.18s** | **31 passed in 26.38s** |

The Linux runner is the existing qualified Lima `s2b` and existing venv; no new
VM/config/environment. Full accepted 202 court and 100k/6 GiB were not run.

## Resource evidence

Own probe: `WORKER_RETURNS/PYAT999_NATIVE_BODY_TRUTH_20261115/resource_probe.py`

Synthetic 256 respondents / 256 events, sourcefree, not 100k:

| Measure | Value |
|---|---:|
| Retained bytes | `9,758,503` |
| Peak selected index | `16,384 B` |
| Public select body reconstructions | `257` |
| Public select family / row-group | `3 / 257` |
| Native I03 body reconstructions | `1025` |
| Native I03 family / row-group | `10 / 1021` |
| Cold / repeat public select | `0.2076 s / 0.2038 s` |
| Cold / repeat native I03 | `0.7013 s / 0.6811 s` |
| Parent / child peak RSS | `153,772,032 B / 59,977,728 B` |
| Fresh-child cold select | `0.2167 s` |
| Source-extension opens | `[]` |
| Full C11 builds | `0` |
| `pq.read_table` fallbacks | `0` |
| 6 GiB cap | PASS at material local fixture |
| Integrated 100k/6 GiB | **NOT_RUN** |

Native body reconstruction count includes canonical body-truth validation plus
ordinary native reconstruction. Parent and child are single processes; no
multi-process tree claim.

## G1–G5

- **G1 PASS:** owner grant, exact branch/startup/native/public/test blobs, frozen
  inputs and allowed symbols verified before write.
- **G2 PASS:** native positive/fact/ref/risk/denom/replay, repeats/ranked,
  routing-UNKNOWN/zero, None/empty, changed/restore and inherited tests.
- **G3 PASS:** exact coherent public+native poison, all paired selectors and
  invalid body/ref refuse with typed `DirectEstateError` before facts.
- **G4 PASS_SCOPED_FIXTURE:** material 256-respondent probe; bounded body truth
  cost; no 100k.
- **G5 NOT_RUN:** same independent reviewer `ses_e30c25800ffeT8XbyTuHekRCme`
  receives exact code/test SHA `ce7704253...` after HQ intake. Author cannot
  self-accept.

## Courts

- **Scientific:** sourcefree TEST_ONLY; no original35/source/science acceptance.
- **Authority:** no new source/CURRENT/issuer/host/merge grant.
- **Integration:** UNMERGED.
- **Overall S2-A:** ready for independent G5, not accepted.

## Self-critique

Native `_build` now reconstructs every event body, adding cost at the material
fixture; 100k is unproved. Public and native body-truth checks remain separate
implementations. The expanded S2-A test file is still an unaccepted test file
until G5. Linux 86 is the scoped inherited set, not a full 91/202 claim. No
independent G5 has occurred.

## Next

HQ intake, then same distinct reviewer receives exact SHA
`ce7704253f6a2381310c3eb2c7412a2d85c5596c` for one coherent public+native G5.
No self-acceptance, no new A/B campaign.
