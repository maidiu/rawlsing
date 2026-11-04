# 04 — False-READY, false-block and first-reader contract tests

**Independent execution mode:** authenticated GitHub direct source/blob inspection plus a **16-case JavaScript static check** over the actual `14` and `15` JSONL, and read of LIVE-02 Python source and committed view output. **Not a Python S2 run, not independent journal replay and not native Sorok testing.** No human/owner adoption is assumed.

## Static gate and conservation result — 16/16 PASS

| Case | Actual observed source result | Disposition |
|---|---|---|
| 1 | 83 distinct `GATE` IDs in 14 | PASS |
| 2 | 38 distinct `VERSIONED_SEAM` IDs in 15 | PASS |
| 3 | 127 evidence leaves | PASS |
| 4 | 268 relations | PASS |
| 5 | 38/38 `w8r_source_qualified_disposition.whole_gate_status` still `JOIN_PENDING` | PASS |
| 6 | `C9@INTEGRATE` has both `G-C9-NATIVE-INTEGRATE` ALL and `G-C9-T-ANY` ANY | PASS |
| 7 | Rule T `ANY` requires explicit selected mode; currently `MODE_UNSELECTED_OWNER_HELD` | PASS |
| 8 | Positive Rule T conditional has actual predicate `C9.claim_mode == POSITIVE_ACQUISITION` | PASS |
| 9 | Native C12 ALL still includes C11, C10, C9, selected reader root and external anchor | PASS |
| 10 | Native C11 separate actual source/weld gate is not qualified | PASS |
| 11 | Gate5 readiness includes generated Gate4 plus operated S14; Gate4 not Gate5 | PASS |
| 12 | S14 operation VERIFY includes access, delete/export, revocation, research separation, abuse | PASS |
| 13 | `S10@SPECIFY` explicitly READY without old E021 review | PASS |
| 14 | `S14@SPECIFY` predecessors met at selected specification scope | PASS |
| 15 | Original D002 MPC-1..7 named full-cell test **not present** in current 06 spine (negative coverage test) | PASS — material omission established |
| 16 | Historical 579-function callable census **not present** in current 06 spine (negative coverage test; 144 isn't a code census) | PASS — material omission established |

These are independent source-backed *assertions*, not 16 passing adapter pytest cases. An exact selected 7bf fork review cannot complete the 598d/root-specific C12 gate, and an isolated C9 positive does not qualify its same-target Rule T ANY, original owner, or E2 member.

## Material LIVE-02 first-consumer defect — exact smallest reproducer

**Code subject:** `bbcc46bf3b7aadfc582e284daea61f99060e0fc3`, `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1/live_update_adapter.py`. **Guide subject:** `2aec26709fe1d28480de1109c0a52b460d9ed8b3`.

- At Python **lines 447–449**, `focus` normalizes a local guide target to its component ID using `target.split("@", 1)[0].split(":", 1)[0]`.
- At **lines 454–459**, `source-to-product` instead computes `comp = target.split("@", 1)[0]`. A legitimate target `C9:LOCAL_GUIDE:C9R_ACCESS_BRIDGE@BUILD` therefore asks the P0/P1 node map for `C9:LOCAL_GUIDE:C9R_ACCESS_BRIDGE` rather than `C9` and can return `NONE_VERIFIED` despite an existing C9 code-consumer map.
- A second concrete source identity issue is **E021**. The [committed actual view 3](https://github.com/maidiu/rawlsing/blob/6a63d19e73ecc814661ffaec6410a2dce711665d/WORKER_RETURNS/SOROK_PROGRAMMA_LIVE_UPDATE_ADAPTER_20261103_R1/cold_replay/view_3_source_to_product_e021.json) returns `existing_code_consumer: {id: "E021", current_importer: "NONE_VERIFIED"}`. The actual `15` **E021** row separately pins `JoinedSession.start/open/fork_alt` as a **scoped sourcefree first reader**, 7bf code cut `joined/session.py` blob `dc0894289e8b6a5e66148189e41d7efb563f25af`. A new agent relying on the top-level output will falsely think the code consumer is entirely unknown. This does not imply a native importer.
- The committed `test_seven_views_share_one_cold_reconstructed_state` tests source-to-product using `E021@VERIFY`, not a local guide-qualified `C9:LOCAL_GUIDE:...@BUILD` route. It checks coherent state/readbacks, **not the exact guide 15 first-reader-to-output parity**.

**Minimal owner repair and test, without new architecture:**
```python
# component-prefix normalization (source-to-product)
comp = target.split("@", 1)[0].split(":", 1)[0]
# Additionally resolve original E/child seam IDs through the immutable
# existing guide_index()['seams'] / source-qualified guide 15 first_reader,
# preserving exact scope and showing native importer separately.
```
1. Add regression `source-to-product C9:LOCAL_GUIDE:C9R_ACCESS_BRIDGE@BUILD`: actual P0/P1 C9 code-consumer mapping must be consulted (or a typed explicit reason if the selected node genuinely has no reader).
2. Add regression `source-to-product E021@VERIFY`: report `7bf` `JoinedSession.start/open/fork_alt` as **scoped historical sourcefree first reader**, and **native importer = NONE_VERIFIED** separately. The top-level first reader must not contradict `15` or the nested receipt.
3. Run actual pytest and cold replay on repaired exact code cut, then new independent source/consumer review; old executable receipt at `bbcc` does not attach to the repaired code root.

**Disposition:** `REVISE_EXACT_MATERIAL_DEFECT` for the adapter's source-to-product truthfulness and its tested first-reader contract. Existing 35/35 LIVE-02, 62/62 P0/P1 receipts are real **executor-reported** evidence and remain source-scoped; they cannot prove an assertion those tests did not exercise.

## Further negative tests still to run in real Python S2

Use existing signed/qualified local Git checkout and disposable P0/P1 journal; independently run: false source commit / source path / reviewer path / node transfer; source-withdrawal with cold rebuild; duplicate transition id conflicting body; concurrent stale CAS; three-event order permutation; old 7bf reviewer copied to 598d; negative withheld without phantom scoped acceptance; source-to-product nested ID and E021 first-reader parity; newly selected tuple under all active same-target ALL/ANY/IF gates. No such execution was performed by this review session. Report `NOT_RUN`, rather than guessing PASS.

## Currentness observation

The adapter `GUIDE_SHA` at line 22 is the frozen W8-R `a9ebf71e...`, and its `freshness` output explicitly warns there is no background fetch. That is honest for a sourcefree candidate **but not a self-updating post-COVER/post-LIVE-02 guide**. The HQ's existing `2aec...` guide is a legitimate current documentary patch; whether it contains the later inputs is a separate fact, not an excuse to refuse to review that patch. The observed absence of COVER source material in 06 and LIVE-02 final in current 00 is a bounded freshness limitation, not a fictitious second guide.
