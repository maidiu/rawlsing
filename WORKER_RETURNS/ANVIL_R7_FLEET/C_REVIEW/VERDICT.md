# ANVIL DISTINCT C — REVIEW VERDICT

**Verdict:** `REVISE_EXACT_DEFECT`  
**Grade ceiling:** prepared/local instrument review only. **Protected H1, native science, source rights and actor consent are NOT_GRANTED. No physical C11 architecture is selected.** An honest `C_HOLD_EXACT` remains the correct packet grade until the defects below are repaired.

## 1. Exact target and custody

| Item | Exact value |
|---|---|
| Integrated commit | `0f0c673f99978aff6c11f7bd0e6fe1840fbdc799` |
| Branch | `agent/anvil-integrated-instrument-20261117-r1` |
| Candidate ZIP | `REPAIRED_PACKAGE.zip`, 1,561,148 bytes, SHA-256 `7569fb21a577aff06d48ce7759cf692c8f2ba3e475b8eba1e71c36d4e5abc689` |
| Original ZIP | `ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip`, 280 entries, SHA-256 `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332` |
| Candidate manifest | 657 files; independently re-hashed: **657/657 match**, 0 missing, 0 bad |
| Protected currentness | `31291d08179890852246c8742700e055168e9933`; first-position HQ OATH present; paired PYAT progress revision 10 |
| K3 source | `7fc00289dd801d2d0a8ce159986c7595fc27a4d9`; 29/26/14 exact rows |
| Source bank | `8523007613d411390a76683fa464002c0f25df83`; 297/299 hash-match and 278/279 ZIP-text-match caveats preserved; original ZIP remains byte authority |

I reconstructed the exact ZIP into a fresh directory under this review root. I did not execute the handoff's literal `rm -rf /tmp/...` and did not use an author worktree or hidden checkout. The shared Git object store `/Users/matthewsmith/s2b-work/rawlsing` and the declared original ZIP were the only external pins.

## 2. What independently passed

- **Source identity (S1) is real.** `W0_SOURCE_REPLAY/source_replay.json`: 118 unique IDs, exact counts 29/26/14/10/8/8/7/16, all 118 excerpts match exact Git rows/ZIP members, 69 K3 rows exact, 26 NOT_ADOPTED and 14 HELD preserved, B-10/S-08/L-08 present. 95 Git rows + 23 ZIP objects/scalars.
- **Package custody is coherent.** 657/657 manifest hashes, ZIP SHA/size, source inventory SHA, raw-log hashes and the six built files match. No candidate product file was modified.
- **The local structural suites can run.** `test_r7_integrated.py -q` = 29/29 OK; package `FRAME`, `DECISION`, `C_INTEGRATED` all PASS; `r7_build.py verify` = `PASS_SIX_PROJECTIONS_BYTE_IDENTICAL`. These are local structural/source-byte results, not C, H1, native science or actor proof.
- **Several hostile controls work.** Missing B-10/S-08/L-08, synthetic SPINE replacement, K3 row mutation, prospective adoption, missing T4 negative, revoked release, fabricated H1, missing identity and zip-member forgery are refused in the candidate's own tests or my controls (`W8`).

## 3. Consequential defects found (reproducible)

### D1. The 16 requirement headings are not 16 encoded requirements — a pairwise-only science loss passes

`W1_REQ_AND_F6_HOLLOW` replaces `REQ-MULTIWAY-JOINT` with an explicit "pairwise marginals are sufficient; no three-way joint need be preserved" obligation, and replaces the matching requirement disposition; it also erases the K1-CAP-17 F6 "numeric bounds do not follow from the I07 guard" distinction. All IDs, domains, bindings, source excerpts, hashes and 118/16 counts remain valid. The candidate gate nevertheless returns:

- `FRAME: PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED`
- `DECISION: PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`

Why: `W6_PROJECTION_NO_LOSS` shows all 16 requirement rows have only one distinct `why_needed`, `loss_if_missing`, `first_consumer`, `architectural_consequence` and `proof_or_owner_hold` value; only the ID-bearing `substantive_requirement` differs. All 118 identity rows have exactly one distinct `design_effect`, one `first_consumer_path` and one `conservation_or_refusal_witness`. The machine packet is a roster of names, not candidate-specific dispositions. The human-readable `FULL_118...SPEC.md` contains more detail, but the gate accepts the machine packet, not the markdown.

This is the exact failure the commission warns about: one missing choice-changing scientific distinction is not repaired because 118 IDs and 16 headings remain.

### D2. Terminal16 names are absent from the actual typed graph — role prose, not producer/consumer graph

`W5_TERMINAL_GRAPH` reads the actual `whole_machine_graph`: **6 nodes / 7 edges**, node IDs `N_SRC, N_C11, N_CALC, N_FIELD, N_WORLD, N_ACTOR`. **Zero** of the 16 terminal IDs (`F1..F8, N9, N10E, N10W, N11, N12, PRE-V3, SEAM, SOROK`) appear anywhere in the graph. The gate still passes DECISION/C, and the C graph audit says `holes=[]`, `producer_authority_time_consumer_checked=true`, all T1–T7 boundary edges checked. The final graph is a six-role cartoon, not the source→terminal producer/authority/time/consumer graph the integrator says D2A completeness preserved. The terminal-identity rows exist only in the 118 inventory and one generic `REQ-TERMINAL...` heading.

### D3. The C court accepts false actor/world science

`W2_C_BOUNDARY_FALSE_SCIENCE` changes the C packet's T4/T6/T7 positive/negative/restore and C prose to assert exactly the forbidden claims: survey opinion = institutional power; survey answers give actor private knowledge without encounter; fictional action overwrites observed source; no independent structural producer. The candidate gate returns `PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED` with no errors. The decision-level actor flags are correct; the C boundary court only checks string length and a local excerpt, not the boundary's scientific semantics. The actor/world firewall is not enforced where the C packet states its boundary results.

### D4. The builder receipt path refuses a real command and admits a non-executed fake

`W3_BUILDER_RECEIPT` constructs a normal `python3 tools/test_r7_integrated.py -q` card with a structurally valid receipt:

- Fresh cwd, no file named `python3`: **RED** with `C:BUILDER_NONEXISTENT_TEST_COMMAND:python3` (the gate treats the interpreter token as a filesystem path).
- Same non-executed receipt, only a dummy file named `python3` in cwd: **PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED** and the packet is `C_CONDITIONALLY_ADMIT_DESIGN`.

This is a false C admission path. The candidate's acknowledged limit says a malicious evidence-root author can forge a local raw log; but the gate should not promote that local receipt to conditional C admission without an external runner/independence check. The raw-log parser also expects JSON, not a text stdout log, so an actual text log is refused as malformed.

### D5. The six projections are shallow, not R5-equivalent

`W6_PROJECTION_NO_LOSS`:

- `BOUNDARY_CONTRACT_MAP.json`: each T has only `name`; producer, receiver, must-preserve, first effect, veto, time class and owner are absent.
- `IDENTITY_DISPOSITIONS.tsv`: 118 rows, one identical `design_effect`, one identical `first_consumer_path`, one identical `conservation_or_refusal_witness`; missing the R5 `source_semantics`, `negative_meaning`, `decision_ids`, `architecture_effect`, `evidence_ids`, `why` fields.
- `EVIDENCE_INDEX.jsonl`: 236 lines with only `id`, `kind`, `origin_sha256`, `disposition`; no source excerpt, negative, falsifier, consumer or evidence grade.
- `BUILDER_HANDOFF.json`: one generic object; not the R5 JSONL handoff with producer/consumer symbols, input/output ABI, transformation, negative, restore, test command, expected effect, authority, status and dependencies.
- `TYPED_GRAPH.json`: the same 6 nodes/7 edges; no terminal/FF/SEAM/SOROK graph.
- `DESIGN_DECISION.md`: a short authored summary, not a source→consumer/negative rationale with actual first readers.

Byte-identical rebuild is real, but it proves determinism, not R5 no-loss. Renamed shallow views are not automatically equivalent.

### D6. The documented cold reconstruction is not runnable from the exact package

In a clean extraction of `REPAIRED_PACKAGE.zip`, the literal handoff command fails:

`python3 r7_inventory.py verify ... --inventory ../tests/fixtures/source_118/SOURCE_IDENTITY_INVENTORY.json` → `FileNotFoundError`; the inventory is under `../EVIDENCE/SOURCE_IDENTITY_INVENTORY.json`.

`test_integrated_strict.py` → 13 errors, because it expects `EVIDENCE` two levels above the package, not the package's `ANVIL_R7/EVIDENCE`. The 13 tests pass only after I manually copied `ANVIL_R7/EVIDENCE` to the undocumented parent location. The 29 inherited tests pass from the package. The package content is largely correct, but the handoff/cold-test layout is not self-contained.

### D7. Source semantic summaries/negatives are identity-authenticated, not machine-authenticated

`W4_SOURCE_NEGATIVE_TAMPER` inverts K1-CAP-11's source semantics/negative to "pairwise marginals are sufficient" and K1-CAP-17's to "the I07 guard determines all F6 numeric bounds," while preserving the exact source excerpt, row hash, 118 IDs and counts. Both FRAME and DECISION PASS. This is the D2B `D2B_R2_RESIDUAL_BLINDSPOT` residual: a source row hash authenticates bytes, not the authored semantic summary. The candidate's HOLDS acknowledge human-summary/source-owner limits; the verdict grades this as identity-only S1, not full source-semantic authentication.

## 4. Minimum corrective action (exact; not a new campaign)

1. **Encode the real 16 obligations, not names.** Replace the generic requirement/disposition fields with the specific obligations in `FULL_118_TO_DECISION_REQUIREMENTS_SPEC.md` (multiway joint, F6 numeric vs guard, denominators/missing/routing, signed/neutral and review/coverage lanes, time vs fictive time, Other recruitment/access, independent actor life, 1/10/100, revocation, terminal holds). Make them individually testable, not length floors.
2. **Make per-identity dispositions per-identity.** `PRESENT_PRESERVED` must carry the identity-specific source meaning/negative, actual first-consumer path or exact owner hold, and positive/refusal/restore witness, as the spec already states. Do not accept one repeated sentence for 118 rows.
3. **Publish a real whole-machine graph.** Add the 16 terminal/FF/SEAM/SOROK nodes and their producer/authority/time/consumer/negative/restore edges, or mark them exact holds. Make the C graph audit require them. A six-node role graph is not terminal completeness.
4. **Enforce the C actor/world firewall.** Apply the decision firewall checks and a semantic negative check to C boundary positive/negative/restore and C prose; add T4/T6/T7 false-science tests that must be RED.
5. **Fix builder receipts.** Resolve argv/script paths after the interpreter, accept actual text stdout logs, require external runner identity/independence and exact execution evidence before `C_CONDITIONALLY_ADMIT_DESIGN`; add a real-command positive and a fake-local-receipt negative.
6. **Make the package cold-handoff self-contained.** Put `SOURCE_IDENTITY_INVENTORY.json` at the documented path or fix the handoff and test path to `ANVIL_R7/EVIDENCE`; run the literal commands from a clean extraction. Keep only the declared external Git/original-ZIP pins.
7. **Rebuild the six projections with the R5 fields/roles** (full coverage row, boundary trace fields, JSONL handoff, evidence/falsifier index, full architecture graph) and compare them against source→consumer/negative/builder/graph functions, not just hashes.

Source-semantic summary authentication and F26 caller/invalidation remain external C/source-owner holds; they are not to be invented. The 26 NOT_ADOPTED and 14 HELD remain unchanged.

## 5. Authority and limits

- **NOT_GRANTED:** protected H1/CAS, native/original35 science, source rights, actor consent, human/product acceptance, physical C11 winner.
- **NOT_RUN:** native SAV/DTA source read, dense 100k 600–1,300 slots, process-tree ≤6 GiB, cold 1/10/100 distinct operations, actual F1–F8/N9/N10W/SOROK first reader, real economic benchmark.
- **HOLD:** F26 exact caller/invalidation at the existing K3 `K1-CAP-24` / `P4R-R02` / `PYAT-PC-R11-21` owner route. This does not block the source-qualified S1 identity review, but it blocks any invented F26 body or native claim.
- **Independence:** this is a distinct nonauthor assertion; external verification of reviewer independence is still required and is not self-certified.
- **Currentness:** protected cut `31291d…` and paired revision 10 were read; any later protected movement requires re-grounding.

## 6. Disposition

`REVISE_EXACT_DEFECT` — the source-identity S1 layer is genuinely source-authenticated and worth preserving, but the candidate instrument's DECISION/C/projection layer is not yet a truthful whole-machine decision instrument. It overfits the known 13 mutations and accepts coherent semantic losses. Repair the seven exact items above and submit the same branch/package to HQ intake; do not claim protected H1 or native science from this review.
