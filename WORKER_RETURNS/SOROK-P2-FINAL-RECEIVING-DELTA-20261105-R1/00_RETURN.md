# SOROK P2 FINAL RECEIVING DELTA R1

## RESULT

`FINAL_P2_RECEIVING_DELTA__PRODUCT_4B2FED81_OVER_ACCEPTED_25D40806__PRIOR_COMPOSITE_3894541E__CURRENT_GUIDE_B6D3F8D2__FINAL_COMPOSITE_F5DEBB10__COLD_CLI_PASS__ENGINEERING_RECEIVING_EVIDENCE_NOT_ACCEPTANCE`.

This is the actual final imported-source first-consumer proof for receiving the current product head. It is not independent review, self-acceptance, or permission to merge.

## EXACT INPUTS

- Live protected base: `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`; tree `ba895ff69255f35c8fec58c0d0b28e339def57f6`.
- Independently accepted product: `25d40806d15516b7f7ffa04f47bc651022c6f2b0`; tree `57dbdca8efdbb6bcda7b64df0ac60e8fe75ddc3a`; review `332e00cb3da51b859a408a31f820b1afd7fe8fc0` (`ACCEPT_SCOPED_TEST_ONLY`).
- Final product head: `4b2fed81c3f513eb4262ad5de277ce519c74c614`; tree `07f3226184803362cc26e680730866d2a3faf930`.
- Current guide PR699 source head after moving-ref verification: `b6d3f8d2b946a38f6336361c2b625c1260699100`; tree `36b5341fb36618ca8d6f816eb8d9aaaf4d07b2bc`.
- Prior protected receiving: `bf574e5a1c5b46bfd92d272fb9616ac697fbbe6a`; composite `3894541eeac3e2133a3823252c65f04252e21e93`.
- Merge base: `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`.

## SELECTIVE DELTA AND COMPATIBILITY

- Product delta `25d40806..4b2fed81`: 73 files, confined to the interval, later-event and fanin returns. Paths: `evidence/product_delta_25d_to_final.txt`.
- Final product allowlist versus protected base: 665 files, all under the seven intended product returns plus the S45-S47 receiving commission. Paths: `evidence/product_allowlist.txt`.
- Current guide allowlist: exactly the 9 existing `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/` files changed by PR699 head `b6d3f8d2`. Paths: `evidence/guide_allowlist.txt`.
- Final composite: protected base + 665 product files + 9 guide files = tree `f5debb10c53b8e9a735f6fe1e1696bfbf46412fc`, exactly 674 changes vs base (665 additions, 9 guide modifications).
- Delta versus prior protected receiving composite `3894541e`: 80 files = 73 product delta + 7 changed guide files. Paths/diff: `evidence/delta_vs_prior_receiving.txt`.
- Merge-tree diagnostics, no conflicts:
  - product `8ffec40 + 4b2fed81` → `07f3226184803362cc26e680730866d2a3faf930`
  - guide `8ffec40 + b6d3f8d2` → `36b5341fb36618ca8d6f816eb8d9aaaf4d07b2bc`
  - combined `4b2fed81 + b6d3f8d2` → `1e1bc686f079beca3512c8b124e16dc11b835da3` (full merge includes 4 excluded guide-return files)
- No product/guide path overlap, no product file collision in protected base, no schema/root/import incompatibility observed.

## ACTUAL FINAL FIRST-CONSUMER CHAIN

Executed once from the final receiving snapshot with `python3 -I -B`, fresh processes:

`new -> interval ACTUAL -> later-event -> opportunity -> verify (zero encounters) -> explicit do-help -> exit -> cold blocked say -> local return -> say UNKNOWN -> verify`.

Observed:

- new: WP19 view schema.
- ACTUAL interval: `PARTIAL`, coverage `[[222,223]]`, material `0`.
- Later event/opportunity: `event_status=OK`, C9 material `false`, S43 `ACCEPTED`, `do_help_executed=false`, `user_attempt=false`.
- Verify before attempt: encounters `0`, events `2`, `ok=true`.
- Explicit DO_HELP: `REFUSED`, `attempted=true`, `performed=false`, `refusal=true`.
- Exit: `LOCAL_EXIT_ONLY`, `OUTSIDE`; cold SAY blocked `LOCAL_OUTSIDE_MODE_BLOCKED` with no actor response/world/clock change.
- Local return: `LOCAL_RETURN_ONLY`, `PORTAL`, no world/clock mutation.
- Typed UNKNOWN preserved; final verify `ok=true`.

Evidence: `evidence/cli/` (11 command receipts plus `summary.json`), `evidence/receiving_rehearsal.json`.

## IMPORT ORIGIN AND PRIVACY

- All load-bearing modules loaded from the final receiving snapshot: `sorok_s45_s47.bootstrap`, `s45.session`, `s47.session`, `s45_projection.adapter`, lifecycle, repaired interval, repaired later-event and fanin. `all_under_snapshot=true`. Evidence: `evidence/import_origin_check.json`.
- Public `new`, later-event, opportunity and final verify outputs have no `root_hash`, `root_id`, private projection keys or forbidden markers. Evidence: `evidence/privacy_check.json`.

## REUSED CUSTODY

- Prior protected rehearsal/manifests reused: protected base, product25d allowlist, prior composite tree and prior selected manifest. `evidence/prior_protected_receiving_manifest.json`.
- Existing focused test evidence reused: 7 fanin, 8 later-event author, 6 interval author; only one cold CLI chain was executed here. No 7+8+6 or inherited 55-test suite rerun.
- Current guide selected files changed, so the existing canonical verifier was rerun against the final snapshot: `PASS` (Pyat 782/892/62/82, FF 26/16, cross 18/16, Sorok 144/38, no prototype). Log: `logs/guide_canonical_verify.log`.

## REVIEW STATUS AND LIMIT

- Final head `4b2fed81` is **not independently accepted**.
- Accepted `25d40806` at `332e00cb` is preserved exactly; this delta is not its acceptance extension.
- Interval secondary public-key/census repair and later-event public-boundary repair component closures remain pending.
- Later-event historical `76fdb624` remains original `REVISE`; its public-CLI limits are preserved.
- No protected merge, PR697 edit, native/science/human/B grant, new event handle, absence flow, lifecycle behavior or interval behavior is claimed.

## SMALLEST REMAINING RECEIVING STEP

HQ can consolidate this final product delta into the existing product PR/receiving line rather than opening a duplicate protected PR. Required remaining step is independent closure of the final head (and pending component repairs) followed by the competent PRE-MAIN owner's selective receiving decision. This rehearsal does not authorize merge.

## EVIDENCE

- `evidence/selected_manifest.json` — exact base/product/guide/prior/final trees, allowlists, merge-tree results, collision disposition.
- `evidence/receiving_rehearsal.json` — cold chain, import origin, privacy, canonical verify, checks.
- `evidence/product_allowlist.txt`, `evidence/product_delta_25d_to_final.txt`, `evidence/guide_allowlist.txt`
- `evidence/composite_diff_vs_base.txt`, `evidence/delta_vs_prior_receiving.txt`, `evidence/composite_tree.txt`
- `evidence/merge-tree-final-product.txt`, `evidence/merge-tree-final-guide.txt`, `evidence/merge-tree-final-combined.txt`
- `evidence/import_origin_check.json`, `evidence/privacy_check.json`, `evidence/cli/`
- `logs/guide_canonical_verify.log`
- `PR_READY_RECEIVING_TEXT.md`
- `PROGRAMMA_DELTA.md` / `.json`

## PUBLICATION

Branch: `codex/sorok-p2-final-receiving-delta-20261105-r1`. Only this return directory was written/committed. Final commit SHA is returned in the final chat readback.
