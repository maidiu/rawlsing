# SOROK O-INDEX R3-IR — independent source-object and six-product-path acceptance

**Lane:** existing sealed R2-IR reviewer lane, not a new author/HQ/adopter
**Branch:** `review/sorok-oindex-r3-independent-source-and-map-acceptance-20261031`
**Review base (commission):** `06f40a3eabb4acfc57f433144224695c2427c25f`
**Remote commission clarification incorporated by fast-forward:** `e17ce303652efe8e4628f42387ab9d9a80c71c28`
**R3 base:** `96af4f15c993c7a4f32da4cc31ef3175903a0d5c`
**Immutable subject:** `e50d32eb6816578145d17dcd637a0b90b3a1ef40`
**Controlling R2-IR review:** `3f3d9ec2fddc36bd4047bc6c730382c65a5e692a`
**Proposed living-reference first consumer / PR #559 head:** `93d44ddb51cbabf89e52e1e8c553c46205bad68d` remains PROPOSED, untouched
**Model/host:** OpenCode 1.18.34, `opencode-go/deepseek-v4.1-flash`, variant `max`, agent `build`; host `mainMac.lan` (macOS 13.2.1, x86_64)
**Session verification:** process argv has `--model opencode-go/deepseek-v4.1-flash --variant max --agent build`; session DB row `ses_e6c922f35ffet6XtlGF0v43LIw` records provider `opencode-go`, model `deepseek-v4.1-flash`, variant `max`, agent `build`, version `1.18.34`. No silent model/provider/effort/host switch.
**Final SHA:** reported in the terminal push readback after commit/push. A file cannot contain the SHA of the commit that contains it.

## Decision

**`REVISE_EXACT_DEFECTS`**

R3 genuinely repairs the specific R2-IR source path/blob/tree defects and adds a real Git refresh verifier and six specific forward L0-L5 product paths. It does not yet close the R2-IR requirement to prove the actual first-consumer/edge, and the six product workstreams still have only generic backward navigation through `L1_GOVERNANCE`. The remaining defects are finite, exact and repairable without a new source census or a new framework.

## Four-column findings

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| All 167 Sorok+Pyat manifest rows and 3 reference sources resolve to actual Git objects; 166 blobs + 1 tree, 21 commits, exact object ids and commit timestamps; R15 tree file list matches Git. | R3's exact source-object binding and the eight named path/blob/tree repairs are real. This is substantially stronger than the R2-IR passing-but-forgeable validator. | Retain the source manifest, Git refresh verifier and source fixes. Do not redo the source census. | R3 author / original source owners / independent reviewer |
| The required "first ACTUAL consumer provenance" fault is not rejected. A fabricated `ACTUAL` consumer with either a fake Git object or a real-but-unrelated Git object passes both `validate_index.py` and `verify_source_manifest.py` after a joint manifest+registry change with a recomputed digest. | R2-IR required evidence for the actual `first_consumer`/edge. R3 only checks that `actual_consumer_evidence` is a non-empty field and that registry and manifest agree. With zero `ACTUAL` rows in the returned artifact, the check is vacuous and the 135 `NONE_PROVEN_AT_PREMAIN` count is not protected. This is the precise remaining source-to-consumer gap. | Add Git resolution for every non-null `actual_consumer_evidence` (Sorok and Pyat); require it in a consumer manifest; or forbid `ACTUAL` at this cut and hard-check `NONE_PROVEN_AT_PREMAIN == 135` / `ACTUAL == 0`. Add fake-object, real-unrelated-object and joint-tamper negative tests. | Validator / O-INDEX author |
| `source_kind`, `required_consumer` and `first_consumer` are consistency-checked, not Git-derived. A joint relabel passes both tools; a different real Git blob can be substituted as the A5 source and passes both. | The manifest proves object existence at a commit, not source-type semantics, required-consumer semantics or historical/owner authenticity. The self-digest is integrity, not an external signature. | Derive `source_kind` from object type/path or declare it authored metadata; add an owner-signed per-row source anchor if provenance substitution must fail; add joint-tamper tests. | O-INDEX author / original source owners |
| S5, S7, S11, S13, S14, S15 now have specific forward L0-L5 chains, alternatives, owner slots and falsifiers, and no longer collapse only to `L1_GOVERNANCE` on the forward path. Their declared `backward_paths` still read `S# -> L1_GOVERNANCE -> L5_S_WORKSTREAM_PRIMARY_SOURCE` for all six. | The R2-IR generic-governance forward defect is repaired; the commission's "backward link" requirement is not. There is no product-specific reverse edge from L5 to L0 and no backward path through the specific L1/L3/L4 nodes. | Add product-specific backward paths or reverse edges for the six and a validator negative that removes the specific backward link. Do not replace the forward chains. | O-INDEX author / Sorok HQ |
| R6 39/94/9, R41 133/26, R7 102 definitions, F1CR original-patch absence, V3 ZIP container mismatch and the historical RED register are preserved; the four assets remain `CANDIDATE_ONLY`, author-tested and unadopted. | The recovery history is not pooled or promoted into native/scientific acceptance. | Keep the exact grain and separate test counts; no native/A5/priority inference. | R6/R7/asset owners |
| 135 rows are typed `NONE_PROVEN_AT_PREMAIN` (112 Sorok + 23 Pyat), 0 are `ACTUAL`. Seven `NONE_PROVEN` rows nevertheless have prose `first_consumer` strings containing "actual" (C4, C9, O15, E02, E11, E12, E14). | The typed state controls the claim, but the prose labels can be misread as current importers. This is a documentation risk, not a second count of current importers. | Prefix such labels with `REQUIRED_ONLY:` or carry `current_importer: NONE_PROVEN` in the same row. | O-INDEX author |
| Stale text remains: `s0_s16_primary_source_correction.note` says `L5_SOURCE_HOLD` is the generic terminal and `backward_paths["*_limits"]` says S0-S16 end at a source hold, while the data now end at `L5_S_WORKSTREAM_PRIMARY_SOURCE`; `05_VALIDATOR_AND_READBACK.md` says `ACTUAL` requires callable/source evidence but only non-empty fields are checked. | Minor overhang that can overstate the validator and understate the repaired source terminal. | Update the three notes to the current terminal and the exact consumer-evidence check. | O-INDEX author |
| The review branch remote advanced from `06f40a3` to `e17ce303` (commission clarity only, two added lines). The subject `e50d32` and all candidate blobs are unchanged. | The lane remains the same sealed reviewer; no candidate rewrite or force push occurred. | Fast-forward to the existing remote, commit the six outputs on top, push without force, read back the final 40-hex SHA. | This reviewer |

## Three courts

### ENGINEERING

**`REVISE_EXACT_DEFECTS`.** Source-object identity, the eight named path/blob/tree repairs, the 21-test + 4-subtest suite, the 167+3 Git refresh and six forward product-path negatives pass. The required actual-consumer provenance negative and the six product backward links do not. Joint manifest+registry tampering with a recomputed digest still passes for consumer evidence, source-kind/consumer labels and a different real source object.

### SCIENTIFIC

**`HOLD`.** All 17 original S0-S16 questions/outputs are exact at the historical Sorok HQ Program Map. The six product obligations are source-defined and now have specific candidate forward paths, alternatives, owner slots and falsifiers. No workstream output exists, no falsifier has been run, no human alpha or native person is evidenced, and no scientific issuance is made. The index is navigation substrate, not a scientific decision.

### AUTHORITY

**`HOLD`.** No CAN/ADP/SCI05, Pyat N11/N12/C0, C9/C12, native B/A5, owner adoption, PRE-MAIN merge, PR #559 edit or self-adoption is issued. The four assets remain author-tested, unadopted candidates. R3 remains `RETURNED_UNADOPTED` candidate material.

## DONE

- Verified the immutable subject, the 17 subject paths and the base..subject 19-path delta.
- Independently resolved 167 manifest rows + 3 references against real Git: object type, object id, commit timestamp and R15 tree file list, with zero errors.
- Verified the eight named source-identity repairs: B1/B2/B3/BP2P4J blob fills, B3A/B3AS/S39_S52 exact paths and R15_V2 tree identity.
- Verified all 17 S0-S16 rows against the exact `05_PROGRAM_MAP.md` commit/path/blob, including question and output text.
- Verified 23 Pyat rows against the top-view and F-gate sources, and the 3 reference sources.
- Re-executed `validate_index.py`, `verify_source_manifest.py`, pytest and unittest on an isolated S2 copy with the real Git object database.
- Repeated the required source faults and the extra joint manifest+registry faults; documented exact pass/fail reasons.
- Reviewed the six product organs, their forward chains, owner slots, falsifiers, alternatives, sources and the missing backward link.
- Reviewed R6/R7, the four assets, F1CR patch absence, V3 ZIP scope and three graph edges that could be mistaken for current code imports.
- Restored the untouched candidate and proved GREEN; the candidate files were byte-identical before and after the test run.
- Verified the active model, variant, agent and host from process argv and the session DB.

## REMAINING

- Git-bind actual consumer provenance and the 135/0 consumer count.
- Decide whether source-kind/consumer labels and source provenance require an owner-signed anchor or only an explicit proof limit.
- Add product-specific backward links for S5/S7/S11/S13/S14/S15.
- Correct the three stale notes.
- Independent re-review of the repaired return and competent HQ/owner bounded adoption; none performed here.

## CRITICAL_BLOCKERS

- No Git-proven actual consumer edge exists; the current 135 `NONE_PROVEN` count is a typed data property, not a protected invariant.
- No external source-owner signature/anchor authenticates historical provenance beyond "this object exists at this commit."
- No scientific issuance, native person, human A5, Pyat N11/N12, C9/C12 release, owner adoption or priority decision.

## LARGEST_PRODUCTIVE_MOVE

Commission a bounded R4 repair of `verify_source_manifest.py` and `validate_index.py` for actual-consumer Git evidence, add the six product-specific backward links, and add the joint-tamper negatives. Do not run a new source census, do not rewrite the source manifest, and do not turn validator GREEN into native/science acceptance.

## FLIGHT

Local S2 sourcefree Git/Python/pytest on `mainMac`. No native survey, respondent, original Pyat/CAN/ADP/SCI05, model/provider call, native actor/world, production import or untrusted executable code was run. No candidate source, PRE-MAIN, PR #559, other worktree or commission file was modified. The only writes are the six files in this return directory; the review branch was fast-forwarded to the existing remote tip, never force-pushed.

## DELTA

R3 moves the candidate from a forgeable source-blind validator to an exact Git-object manifest with a real refresh verifier, corrected source paths/blobs/tree and six specific forward product paths. It does not yet move the actual-consumer provenance or the six backward links to the same standard. The remaining work is a bounded engineering correction, not a new recovery campaign.

## Priority neutrality

No priority, roadmap, ranking or sequencing decision is made. `PRIORITY` and `JOINT_TEST` remain `HQ_JUDGMENT_REQUIRED__NOT_MADE_BY_INDEX`; the index deliberately does not choose between recovery, science issuance, native-product work or another Sorok task.

## Final SHA readback

`FINAL_SHA: PENDING_TERMINAL_READBACK` — the exact 40-hex final branch tip is read with `git rev-parse HEAD` after the non-force push and reported in the terminal response. A commit cannot contain its own SHA. The source subject remains `e50d32eb6816578145d17dcd637a0b90b3a1ef40`; the review branch start was `06f40a3eabb4acfc57f433144224695c2427c25f`, and the incorporated remote commission tip was `e17ce303652efe8e4628f42387ab9d9a80c71c28`.
