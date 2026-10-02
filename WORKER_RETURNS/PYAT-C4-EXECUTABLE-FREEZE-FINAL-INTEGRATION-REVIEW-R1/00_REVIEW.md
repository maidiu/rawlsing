# PYAT C4 — EXECUTABLE FREEZE FINAL INDEPENDENT INTEGRATION REVIEW — R1

## Disposition

`APPROVE_AT_DECLARED_GRAIN`

Terminal:

`C4_EXECUTABLE_FREEZE_FINAL_INTEGRATION_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

This approves only the exact source-free executable-freeze grain represented by:

- executable-freeze result: `8ff40d37de69db2d8a6053a7c2242f481677f1a4`
- combined execution tree: `8f7efe690a161902e79358eb31650c238a4c0be8`
- C4B freeze: `c2af4f61d68e9803af83f8e26f633acfe31062fa`
- accepted D2P: `41bd7a7c056de9d45b905efc0f926b4ab6a097ad`
- C4C3 runtime qualification: `1df64cc596b5602c952518c87b1c71cc1fcfb35f`

It does **not** authorize raw-source access, C4 execution, warrant issuance, source-locator discovery, production mutation, C7, PRE-V3→V3, actor/person work, or self-adoption.

The warrant remains exactly:

`CANDIDATE_ONLY__NOT_ISSUED__NO_RAW_ACCESS_AUTHORIZED`

## Independent findings

### Commit graph

The apparent “3 commits versus 5 reachable commits” discrepancy is benign and exactly explained.

There are three first-parent fan-in commits after commissioned fan-in tip `012569770c551aca60c16eb20482c3435399c5d1`:

1. `39015a90aec3596b87c0e9b0a664c025e919c137` — merge C4C3;
2. `f8c8e2e4ebc407bc419d2908a78f06addb21031c` — exact-path/blob import of C4B and D2P;
3. `8ff40d37de69db2d8a6053a7c2242f481677f1a4` — final freeze packet.

GitHub correctly reports five commits reachable from the fan-in commission tip because the merged C4C3 side contributes its two commits (`eba2f424...` commission + `1df64cc5...` return). No hidden fourth or fifth fan-in mutation exists.

### Zero production movement and blob conservation

The `rawlsing_next` tree SHA is independently identical at C4A and final:

`b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0`

All required C1/C3/facade/consumer blobs are exact, and the fan-in-observed Route-B producer is also exact:

`rawlsing_next/pre553_route_b_production.py @ 2385cd327dced3c5b887b59085aa0d21b04d78c3`

The 34 non-commission imported evidence blobs independently compare exact: C4B 9/9, D2P 16/16, C4C3 9/9.

### O1-C01 / Route-B owner

The Route-B binding is correct, not incidental. HQD-118 explicitly adopts `rawlsing_next/pre553_route_b_production.py` as the current M01 selected-B execution compositor, and the module declares `PYAT_M01_ROUTE_B_PRODUCTION_COMPOSITOR@1.0.0` with public `execute_route_b_production`.

The current AT07 successor identities are also independently present in the adopted successor-spine evidence:

- forward: `01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd`
- reverse: `a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca`

### Court continuity

C4A's C1 court is exactly 454/454 and belongs to this lineage. The authoritative C3 court is exactly six files and 55 tests; C4C3 ran it twice on the exact combined tree / Darwin x86_64 anchor and obtained 55/55 both times. Supplementary compatibility failures remain explicitly outside the authoritative denominator and are not relabelled.

### Workload / oracle / D02

The eight-source set, SHAs, variables/ordinals, operation classes and read economy match C4B exactly:

`SRC02, SRC06, SRC08, SRC12, SRC14, SRC26, SRC27, SRC35`

Only SRC27 is fresh full Route-B; six are bounded physical-only; SRC35 is retained-only; excluded fresh reads remain zero.

LiTS remains bound by document SHA `2704fd3f...` plus the accepted D2P packet. B001/B002/B003 are accepted at their declared retained-preimage grain. The 3.4 GB checkpoint SHA was not recomputed on StarriyMac, the 120 deferred-member digests were not recomputed there, and extraction was not byte-replayed there; those limits remain explicit and are not converted into independent verification.

For SRC14, the PREP71 fixture blob resolves exactly to `12f6adb77ef5692511055c8f0520e42c454f3867` at its named historical tip. The retained rendering does not determine the runtime subclass. C4C3's `datetime.date` observation is synthetic source-free evidence only; real SRC14 subclass remains a warrant-time observation.

### Runtime reviewer correction

One fan-in wording claim is too broad and is corrected here.

C4C3's recorded 21-module “actual C4 path” starts at decoder/facade/provider/composition/consumer and therefore does not include the now-confirmed M01 entrypoint. Once the current Route-B producer is included, the static production closure gains:

- `rawlsing_next/pre553_route_b_production.py`
- `rawlsing_next/pre553_carrier_execution.py`

So the producer-inclusive static closure is at least 23 repository modules, not 21.

This is **not** a P2X/runtime blocker. Independent import inspection shows those two modules add no `ee_p2x_*`, `duckdb`, subprocess, `importlib` dynamic-loader, or builder-exec edge; their repository imports terminate inside modules already in the C4C3 closure. Therefore `P2X_DARWIN_GATES_NOT_ON_C4_PATH` remains correct.

This review also does not falsely claim a Darwin-specific M01 rerun. M01 has a governed 61/61 Python-3.11 court, and its 11 compositor tests pass on the exact combined C4A tree; C4C3's exact Darwin run did not separately rerun M01. At the commissioned source-free freeze grain, this does not defeat O1-C05 because the platform-sensitive reader/codec/facade surface is the part qualified on the exact Darwin anchor, and the added M01/carrier modules introduce no new platform/runtime gate. HQ should carry the corrected closure wording forward.

### Accounting / retry / all-35

Zero retry is lawful. C4B froze immediate stop on hash/config/authority/oracle mismatch and required any retry to be separately counted; it did not require a positive retry. The fan-in's zero maximum is a stricter predeclared budget and does not widen C4B law. A corrected rerun requires new HQ authority.

The all-35 ledger independently recomputes to:
- 35 distinct source identities;
- 8 selected;
- 27 excluded;
- 280 cells = 35 × F1–F8;
- exactly eight cells per source;
- all nine claim ceilings preserved;
- three carried residuals preserved.

### Warrant candidate

The candidate independently parses, has exactly seven fresh-read sources, excludes SRC35, leaves every locator unfilled, leaves both approvals unset, and preserves all no-access booleans.

Its SHA-256 was independently recomputed from the exact GitHub bytes:

`d57420f8016bf49cc0353f39dcd2271e6f370c3bd9b7e81f08466c0a1f574e0a`

This exactly matches the freeze binding.

The seven locator slots block warrant issuance only. They do not block acceptance of this source-free freeze because the review was explicitly forbidden to discover them and no raw storage was searched.

## Open-item adjudication

- Seven source locators: **blocks warrant issuance/live access only**.
- Route-B producer binding: **resolved by this review; correct current M01 owner**.
- No repository dependency lock: **advisory/nonblocking**; exact C4C3 environment freeze remains the qualified surface.
- Zero-byte framework `python3.11` launcher: **advisory/nonblocking**; C4C3 used an actually executing uv-managed CPython 3.11.3 and future checks must do the same.
- 3.4 GB checkpoint absent on StarriyMac: **nonblocking at declared retained-custody grain**; no stronger verification claimed.
- 120 deferred-member digests not recomputed on StarriyMac: **nonblocking at declared D2P grain; claim ceiling retained**.
- D2P extraction not byte-replayed on StarriyMac: **nonblocking at declared D2P grain; no reproducibility claim granted**.
- `checkpoint_identity 3fab15f3...` and `canonical_closure_identity f264dd8f...`: **recorded-but-not-independently-verified labels only**.
- Producer-inclusive closure count correction (21→23): **reviewer correction, advisory/nonblocking; P2X-off-path conclusion independently survives**.
- `C2-EPCLASS-PAYLOAD-001`: **carried unresolved; blocks class-sensitive epistemic-origin claims, not C4 freeze**.
- single fresh-process provider→consumer→lifecycle bridge: **carried OPEN__NONBLOCKING**.
- C7 comparable-wave gate: **HELD; C4 does not unlock it**.

## Final

No counterexample requires production repair or freeze rejection. The exact executable C4 freeze is accepted at its declared source-free grain, subject to HQ adjudication and the unchanged O1-C06 issuance gates.

`C4_EXECUTABLE_FREEZE_FINAL_INTEGRATION_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
