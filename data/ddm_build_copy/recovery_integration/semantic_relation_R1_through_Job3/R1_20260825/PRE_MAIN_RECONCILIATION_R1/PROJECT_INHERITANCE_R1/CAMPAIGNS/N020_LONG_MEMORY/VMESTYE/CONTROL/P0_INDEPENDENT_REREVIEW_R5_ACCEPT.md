# VMESTYE ZL-P0R R5 — independent Phase 0 schema-and-estate receiving

**Formal independent verdict: `ACCEPT_P0_SCHEMA_AND_ESTATE`.**
This is a *scoped S0–S2 documentary schema/source-estate receiving verdict*, not VMESTYE/Omega HQ's P0 closure decision, an authorization to dispatch ZL-02–ZL-14, a protected merge, or current functional/scientific/actor/native proof. R1–R4 findings remain preserved as prior historical verdicts; R5 resolves the three R4 S2 defects on the later immutable head.

## Exact immutable receiving subjects

| Role | Object / HEAD | State |
| --- | --- | --- |
| Protected PRE-MAIN base | `integration/pre-main-reconciliation-r1@2162d85db5e6822707e5cdff7aac2656ebef4761` | protected, untouched |
| ZL-00 schema/lease candidate | PR #819 `11047708a6e4b4050da351f4b6cc35f03cb8269b` | draft/unmerged |
| ZL-01 corrected estate candidate | PR #820 `353adc216a832a6c41ccc99f77cb3b53651af64e` | draft/unmerged |
| S2 validator/runner return | PR #826 `a9a477066d5cd0a0811278edc09cc42644bf4dc3` | draft/unmerged |
| Independent P0R reviewer | PR #821, isolated `review/vmestye-p0-independent-currentness-no-drop-r1`; R4 HEAD `a1f8b70b9db6081ed682a37f908274bb7bd5c7b9` | R5 append-only on same branch |
| Historical D05 source | commit `b7dd1bce667651c88ddd71c17c065f2b33ec38ec`, ledger blob `bf77b70f1858697ce663f2eeec2e91e25aa6ac94` | immutable historical input |

Review surface: independent ChatGPT authenticated GitHub S0–S1 direct-source and S2-receipt examination, including independent digest readback; **reviewer did not rerun S2 locally on mainMac**. Worker reports user-dispatched structural S2 on `mainMac.lan`, macOS 13.2.1, Python 3.11.3, OpenCode `opencode-go/deepseek-v4.1-flash`, unexposed effort. This is *not* an I3+/HIGH attestation or S3/native execution.

## Source identity and semantic boundary carried forward

R4 independently read ZL-01 census Git blob `65c1bbe4a602341c5caacca2d58dced31a23f382`, compared it with the predecessor 6,120-row census, and established:

- **6,125** census identities (25 columns), no duplicate composite source identity; prior 6,120 identities retained, exactly five restored D05-F07 through D05-F11 entries.
- D02–D07: **23 per-file selectors / 369 source rows**; D05 grouping **29**; D05 authority-maintenance ledger **11 source identities** at historical source rows 2–12. ZL-01 110 anti-join and 111 coverage receipts are internally consistent; 82 G4 predicate receipt entries including 26 `IF` scopes remain preserved.
- All **11/11** `P0_D05_RAW_SOURCE_QUALIFICATION.tsv` raw physical-line SHA256 records independently matched immutable source bytes (including newline) in R4. D05 F06 and F11 malformed-CSV *field meanings remain explicit historical holds*. They have exact raw-line identity, not qualified eight-field interpretation.
- No current functional zero-loss, authority application, first consumer, actor or scientific promotion is inferred from census presence. Source-key equality is a deliberately narrower proposition.

Same ZL-01 exact HEAD in R5: these checks carry forward; no new unreviewed sourcecut is silently admitted.

## R5 executable receiving: all three R4 defects repaired

At exact S2 PR #826 HEAD `a9a477066d5cd0a0811278edc09cc42644bf4dc3`:

1. **R4-D01 — contradictory exit receipt: RESOLVED.** `P0_S2_EXECUTION_RECEIPT.tsv` baseline exit_code `0` agrees with `logs/P0_S2_BASELINE_EXIT.txt` actual bytes `0\\n`, stdout, and `P0_S2_BASELINE_RESULT.json`: exactly **50 PASS / 0 FAIL / 0 HOLD**. Historical prior contradictory R4 state remains recorded, not rewritten.
2. **R4-D02 — conditional 364-row bypass: RESOLVED.** Current `validation/validate_vmestye_p0_s2.py` emits named `C_D02_D07_SELECTORS` independently of a stale literal, tied to source-derived row totals. Its logged check reads **`23 file selectors resolved 369 grouped census rows; source rows 369`** and is `PASS`. Also `C_D02_D07_ROWS` is `PASS`; no quiet disappearance on 369.
3. **R4-D03 — regex-only hash: RESOLVED.** Validator loads historical source with Git `commit:path`, preserves physical newlines, resolves `csv-record:N` and compares `hashlib.sha256(source_lines[N-1]).hexdigest()` to each D05 qualification record. The new **N09_D05_RAW_HASH_TAMPER** supplies a syntactically valid but wrong 64-hex SHA for D05-F01; the run exits nonzero and includes exact `C_D05_QUALIFICATION_HASH:D05-F01`. This tests source-content binding, not merely SHA-shaped syntax.

## Independent receipt checks and bounded confidence

- Baseline JSON programmatically counted: **50 PASS, 0 FAIL, 0 HOLD**; exit file literal `0`; execution receipt exit `0`.
- Negative-control TSV and nine individual committed negative logs individually examined: N01–N08 original eight **all PASS** with their named intended errors; N09 newly added **PASS**, intended hash error present. All nine mutate the now-clean baseline, all nine exit `1`; no inherited D05 no-drop baseline failure taints the negatives.
- Historical bootstrap exit `0`: protected **18 NOT_DISPATCHED / 9 NOT_RUN** preserved; no false protected execution. Five validator unit tests reported passing. GitHub CI status is separate from these scoped S2 results; inherited unrelated protected-base pin failures cannot be erased by this review.
- Candidate assembly manifest lists **18 pinned files, nine ZL-00 + nine ZL-01, no path overlap**. Reviewer independently recalculated content SHA256 matching S2 manifest for validator `c35c2fad896ecf2f78dd0340d46b27276101d111d9f0830dc1082feebc338801`, negative harness `b1e97b7eb5712c173071d69b7bc4f6d1fa553ce1c8fc1eb1cd34d8555ab08ae2`, assembly `a2c4bc45f9341147ef8312bd4291f1bbaafb7c083caba96e0d0569c8ac1db667`, and qualification `467e0ea1cf86113baec6f1ed0c496d3eb0d740e8495c1daab4cd062fd250075f`.
- This reviewer read GitHub source, manifests, hashes, and produced logs; **not an independent same-host S2 re-execution**, not independent code-signing or runner-identity attestation.

## Receiving disposition and mandated next gate

`ACCEPT_P0_SCHEMA_AND_ESTATE` means the two exact P0 candidate sourcecuts plus corrected stage-aware S2 evidence are received for the bounded schema/source-identity/estate no-drop gate. F06/F11's qualified *field-semantic* holds stay open under historical source stewardship; they do not falsify exact raw-key preservation and must not be washed into current functional evidence.

**Only VMESTYE/Omega HQ / qualified PRE-MAIN owner now adjudicates Phase 0 closure, adoption path, and whether to release P1 ZL-02..14.** This reviewer neither self-adopts into protected PRE-MAIN nor dispatches or merges. Pending HQ: `P1_RELEASE=NO`, `PROTECTED_WRITE=NO`, `MERGE=NO`, `NATIVE_S3=NO`, `SCIENTIFIC_ACTOR_FUNCTIONAL_PROMOTION=NO`.

Independent receiving terminal:
`ACCEPT_P0_SCHEMA_AND_ESTATE__CORRECTED_ZL00_ZL01_S2_EXACT_HEADS__50_PASS_ZERO_FAIL_ZERO_HOLD__NINE_NEGATIVES_PASS__FIELD_SEMANTICS_HOLDS_PRESERVED__HQ_ADJUDICATION_PENDING__NO_P1_RELEASE`
