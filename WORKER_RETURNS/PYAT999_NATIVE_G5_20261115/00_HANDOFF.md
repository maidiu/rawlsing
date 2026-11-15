# PYAT999 J1 — native body-truth independent G5

## Verdict

**`ACCEPT_SCOPED@S2A_NATIVE_AUTHENTICATED_SEMANTIC_RANGES`**

at sourcefree TEST_ONLY grade on the combined return
`b3075129fa6aef08de900b79e50bd5d47de5143a`, exact code/test
`ce7704253f6a2381310c3eb2c7412a2d85c5596c`.

Integration: **UNMERGED**. Full original35/source science, production CURRENT,
100k/6 GiB, #998 integration and protected merge remain external holds.

## Exact artifact

- Review branch/worktree: `review/pyat999-native-g5-20261115` /
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat999-native-g5-20261115`
- Startup: `a59c6a5a85451330500bd6a939c3faee6dbc94ad`
- Code/test: `ce7704253f6a2381310c3eb2c7412a2d85c5596c`
- Combined return: `b3075129fa6aef08de900b79e50bd5d47de5143a`
- Native before/after blobs: `8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e` /
  `1dc82ab5658051f35dc1d81cbac30688e84a1623`
- New test blob: `84db13b94888065a99dbdb77b1aa73eab3653bd8`
- Public selector blob: `e8622ac6bf59c4d1ec052e21410e63aab7dd9aa1` (unchanged)
- Prior public body-truth repair: `5727db0ebecab2c9ae393a49e9bce1be3076a589`
- Owner grant: `USER_QUEUE_20261115/sources/999_OWNER_GRANT.md`
- Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme`, not author/fixer.

The author delta is only `pre553_direct_estate_i03.py::DirectEstateI03Session._build`
plus the same-file `_validate_event_body_truth` helper, and the S2-A regression.
Public selector, physical writer/schema/manifest/layout, native evaluator,
`_selected_events` science, S2-D and prior returns are unchanged.

## Exact attack

Independent coherent projection+locator poisoning was run against the actual
native `CarrierNeutralResearchExecutor.execute_i03`:

- changed projected `RespondentEvent.native` and matching locator `native`;
- kept canonical `body_json`/ref corpus digest
  `3070d589d6c7255063ed8ac26d90c06e61ed4db4881523266e5918095b895f6c`;
- kept external direct-I02 roots unchanged;
- coherently re-pinned the physical member/manifest.

Current b307/ce770 result:

```text
public select_events:
  DirectEstateError: physical event posting disagrees with exact native body

actual native execute_i03:
  DirectEstateError: cold I03 event posting disagrees with exact canonical native body

native fact created: false
native silently changed: false
```

This closes the exact SEV-0 from f88 (`e8b384...` vs oracle `8867cb...`).

## Tests actually run

- New S2-A seven-test file: **7 passed in 3.91 s**
- S2-A focused (57 old + 7 new): **64 passed in 8.72 s**
- S2-C focused: **31 passed in 4.53 s**
- S2-D focused: **31 passed in 13.12 s**
- Existing Linux Lima `s2b`, 86 inherited S2-C/proc tests:
  **86 passed in 35.25 s**
- New seven were independently run on Darwin; Linux 64/new-7 author evidence
  was not independently rerun in this recheck.

The seven tests cover coherent native/respondent/canonical/component/state/
occurrence poison, invalid body_json/ref/object_id/content_hash/kind,
repeated/ranked occurrence, native-only precedence, states=None vs empty,
routing UNKNOWN vs true empty, changed/restore and current/wrong root.

## Assertion correction

The prior test asserted the known broken native inequality as a HOLD. It now
asserts typed `DirectEstateError` refusal. That is the required repair
regression, not a weakened valid negative.

## Baseline provenance correction

This is an evidence correction, not a product failure:

- **f88**: public `select_events` returned **0** without refusal; native I03
  returned the changed fact `e8b384...` instead of `8867cb...`.
- **a59** (pristine startup): public `select_events` **already refuses** with
  `DirectEstateError: physical event posting disagrees with exact native body`;
  native I03 still returned the changed fact.
- **b307/ce770**: both public and native refuse; no fact is created.

The author’s baseline claim that pristine a59 public silently undercounts is
therefore **not reproduced**. That old public behavior belongs to f88/1cb; a59
already contains the 5727 public body-truth repair (public blob `e862`). The
native RED at a59 is real and is repaired at ce770. The current product result
passes; only the author baseline provenance needs correction.

## Resource impact

Independent current 256 synthetic respondent/event probe:

| Measure | Observed |
|---|---:|
| Retained estate | `9,758,503 B` |
| Peak selected index | `16,384 B` |
| Public body reconstructions | `257` |
| Native body reconstructions | `1,025` |
| Public family opens / row-group reads | `3 / 257` |
| Native family opens / row-group reads | `10 / 1,021` |
| Cold / repeat public select | `0.1986 / 0.1977 s` |
| Cold / repeat native I03 | `0.6199 / 0.6025 s` |
| Parent RSS | `152,604,672 B` |
| Child RSS | `61,644,800 B` |
| Source-extension opens | none |
| Full C11 builds | `0` |
| Whole-table `pq.read_table` fallbacks | `0` |
| 100k / 6 GiB | **NOT_RUN** |

Only parent/child snapshots were measured; no process-tree peak is claimed.
The added per-event canonical body reconstruction is bounded at this fixture but
unproved at 100k.

## G1–G5

- **G1 PASS:** exact owner grant/file/symbol, source/test blobs, startup and
  combined return verified; all production deltas inside the granted native
  class/helper. Baseline provenance corrected.
- **G2 PASS:** actual native/public positive, repeated/ranked/None/empty/routing,
  changed/restore and exact fact/ref/release parity.
- **G3 PASS:** coherent body-truth attack and invalid field/ref/body poisons
  refuse before facts in both public and native paths; no false EMPTY.
- **G4 PASS_SCOPED_FIXTURE:** bounded 256-respondent resource impact; no
  100k/process-tree claim.
- **G5 PASS:** same distinct nonauthor reviewer; scoped acceptance.

## Limits

Sourcefree TEST_ONLY only. Original35 source/science/rights, production
CURRENT/host/actor issuer, integrated 100k/6 GiB, #998 and protected merge are
external HOLDs. Integration UNMERGED. S1-A 6286/c900 accepted 34+136 is closed
and not reopened.

Return: `WORKER_RETURNS/PYAT999_NATIVE_G5_20261115/`.

## Remote verification

Review content commit `ed9786d4eefb2ebb59374cfb559201da7d044cbe` was pushed to
`origin/review/pyat999-native-g5-20261115`. Direct remote verification found the
product tree unchanged from combined return `b3075129f` and the remote receipt
valid. See `evidence/remote_verification.txt`.
