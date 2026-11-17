# GATE_DESIGN — D3A: precise executable gates for false-S1-blockage **and** false-S3/C acceptance

**Pair question:** *Which precise executable gates and production artifacts prevent false S1 blockage AND false S3/C no-loss acceptance with the least nonceremonial machinery?*

**Answer in one line.** Replace the *artifact* S1 test (an already-finished R5/R6 SPINE) with a *byte-locator* S1 test over the same 118 identities; require S3 to reconcile all 118 identities (not nine domain headings) against those locators; and require C to prove per-boundary positive/negative/restore, one typed authority/time graph, and the six deterministic projections by bytes. Nothing else is added.

---

## 0. What was actually wrong (three defects, one cause)

**Cause:** the active gate tested *the presence of a downstream artifact* instead of *the provenance of the upstream fact*.

| # | Defect | Exact location in supplied `tools/r7_integrated.py` | Consequence |
|---|---|---|---|
| D1 | **S1 circularity.** `check_frame` requires `historical_source_spine` with schema `ANVIL_SPINE_R5|R6` and `original.coverage == history.coverage`; `r7_transfer_conservation.transfer()` only accepts such a spine. | lines 112–122; `r7_transfer_conservation.py` 13–22 | The only way to pass S1 is to already possess the *output* of the campaign (`SPINE.json`), which R5 never produced (`20_RECOVERY_AND_TEST_PROVENANCE.md`: `NOT DISPATCHED`). Honest source-only work is **blocked**, and a fabricated spine is **accepted**. |
| D2 | **S3 under-coverage.** `check_decision` reconciles only `frame.requirements` — the nine mission domains. There is no 118-identity crosswalk at all. | lines 177–201 | A decision can be "complete" with 53 rows or 0 rows of the historical universe; a single missing historical functional decision is invisible. |
| D3 | **C structural emptiness.** `check_C` checks prose fields, two builder cards, and a reviewer-relationship string. It never checks the seven T contracts, never checks a typed graph, never checks builder bytes. | lines 211–242 | "No loss" can be asserted without any positive/negative/restore, any authority typing, or any produced artifact. |

The correction is deliberately *not* a new tribunal. It moves three checks from "a document says so" to "a byte says so".

---

## 1. S1 — `FRAME`: source-qualified identity inventory

### 1.1 Object: `ANVIL_SOURCE_QUALIFIED_INVENTORY`

```jsonc
{
  "schema": "ANVIL_SOURCE_QUALIFIED_INVENTORY",
  "inventory_grade": "SOURCE_QUALIFIED_DOCUMENTARY_NOT_SCIENCE",
  "source_authentication": "BYTE_VERIFIED_AGAINST_SUPPLIED_SOURCE_ROOT_BY_LOCAL_CHECK",
  "source_cut": "<40-hex live protected commit>",
  "rows": [
    {
      "group": "K1_CAP | PYAT_PC | P4R | SEAM_B | SEAM_S | ANVIL_L | BOUNDARY | TERMINAL",
      "id": "K1-CAP-01 | PYAT-PC-R9-01 | P4R-R01 | B-01 | S-01 | L-01 | T1 | F1 | N9 | PRE-V3 | …",
      "necessity": "BUILD_NOW | MUST_PRESERVE_NOW | MUST_ALLOW_FUTURE | EXTERNAL_OWNER_HELD | HISTORICAL_NOT_ADOPTED | HISTORICAL_PROOF_HELD",
      "adopted": false,            // required false on PYAT_PC
      "closed": false,             // required false on P4R
      "source_anchor":   "≤ verbatim locator text",
      "source_semantics":"≤ verbatim source text (must be grounded in origin row)",
      "consumer_or_hold":"≤ first consumer or named hold",
      "negative_meaning":"≤ the original negative / non-claim",
      "architecture_effect":"≤ the requirement this places on any candidate",
      "why":             "≤ why it survives",
      "evidence_ids":    ["K3_K1_CAP"],
      "origin": {
        "kind": "K3_TSV_ROW | DOC_ROW | JSON_MEMBER | TERMINAL_TABLE",
        "container": "GIT | ZIP",       // authority is the container, never a local file
        // --- container = GIT ---
        "commit": "<40-hex>",           // must resolve via git rev-parse in --git-repo
        "path": "<original repository-relative path>",
        "git_blob": "<40-hex>",         // must equal `git rev-parse <commit>:<path>`
        "file_sha256": "<64-hex>",      // sha256 of `git cat-file blob <git_blob>`
        // --- container = ZIP ---
        "member": "ANVIL_R7/02_BOUNDARY_CONTRACTS.json",
        "zip_sha256": "<64-hex>",       // must equal sha256 of the real archive
        "member_sha256": "<64-hex>",
        // --- row ---
        "row_selector": "K1-CAP-01",    // TSV / terminal
        "exact_excerpt": "≤ exact bytes present in the container member",
        "row_sha256": "<64-hex>"        // sha256 of the exact located row bytes
      }
    }
  ]
}
```

### 1.2 Checks (all hard RED)

| Code | Meaning |
|---|---|
| `HISTORY:NOT_SOURCE_QUALIFIED_INVENTORY` | a bare `ANVIL_SPINE_R5/R6` was offered as origin — **the exact D1 hole** |
| `HISTORY:LEGACY_TRANSFER_WITHOUT_SOURCE_QUALIFIED_ORIGIN` | a legacy transfer without an `origin_inventory` pointer |
| `HISTORY:TRANSFER_NOT_VERBATIM_TO_SOURCE` | legacy `coverage` text ≠ located source text |
| `…:SOURCE_FILE_ABSENT` / `GIT_BLOB_ID_DISAGREES` / `SOURCE_FILE_BYTES_CHANGED` | container identity wrong |
| `…:ROW_NOT_IN_SOURCE` / `EXCERPT_NOT_IN_SOURCE` / `ROW_BYTES_CHANGED` | row identity wrong |
| `…:SEMANTICS_NOT_GROUNDED_IN_ORIGIN` | row text rewritten while keeping an honest locator |
| `HISTORY:ID_SET_DRIFT:<group>` / `HISTORY:COUNT_DRIFT` | missing/extra identity (B-10, a K1 row, etc.) |
| `…:FALSE_PROSPECTIVE_ADOPTION` / `FALSE_PROOF_CLOSURE` / `WRONG_NOT_ADOPTED_GRADE` / `WRONG_PROOF_HELD_GRADE` | 26 adopted or 14 closed |
| `FRAME:SOURCE_SPINE_NOT_THE_118_UNIVERSE` | a SPINE is still supplied but is not the 118 universe |

### 1.2b HQ defect D4 — a claimed commit was never resolved (fixed)

`verify_origin` originally checked only the *shape* of `commit` and recomputed `git_blob` from the **caller's own file bytes**. A caller could set `commit = 'a'*40` and keep everything else, and the gate returned **PASS**. Reproduced verbatim before the fix (see `TEST_TRANSCRIPT.json` → `before_fix`).

The repair binds each row to an **independently pinned container**:
- `GIT` — `git rev-parse --verify <commit>^{commit}` (the commit must exist and be a commit), an optional allow-list of pinned cuts, `git rev-parse <commit>:<path>` (must equal `git_blob`), then `git cat-file blob` is the only byte source. The caller's working copy is never consulted.
- `ZIP` — sha256 of the real archive must equal the declared `zip_sha256` and the externally supplied anchor, and the member bytes must hash to `member_sha256`.
- **No anchor ⇒ `NO_EXTERNAL_TRUST_ANCHOR` ⇒ RED.** There is no silent degradation to a local-shape PASS.

New refusal codes: `ORIGIN_COMMIT_NOT_IN_REPOSITORY`, `ORIGIN_COMMIT_OUTSIDE_PINNED_CUTS`, `ORIGIN_PATH_NOT_IN_COMMIT`, `ORIGIN_PATH_BLOB_MISMATCH`, `ORIGIN_FILE_SHA_MISMATCH`, `ZIP_CONTAINER_SHA_MISMATCH`, `ZIP_ANCHOR_SHA_MISMATCH`, `ZIP_MEMBER_SHA_MISMATCH`, `NO_GIT_ANCHOR`, `NO_ZIP_ANCHOR`. No blacklist of `a*40` is used.

**What the gate still does not decide.** It does not decide whether a row's *semantic content* is scientifically right, whether the K3 owner decision was sound, or whether a terminal identity is implementable. Those stay with their owners.

### 1.3 Legacy path

`ANVIL_R7_INHERITED_CONSERVATION` survives — it is useful for carrying a genuine historical spine — but only as a **transfer**, never as origin:

```jsonc
{ "schema":"ANVIL_R7_INHERITED_CONSERVATION",
  "source_authentication":"NOT_AUTHENTICATED_BY_LOCAL_CHECK",
  "transfer_method":"VERBATIM_R5_R6_SEMANTIC_COVERAGE_NO_RECLASSIFICATION",
  "source_spine_sha256":"<64-hex>",
  "origin_inventory":{"path":"inventory.json","sha256":"<64-hex>"},
  "coverage":{ …118… } }
```

If `origin_inventory` is absent, S1 is RED. This is what makes a synthetic SPINE "fake original" impossible: the transfer is now a *view* of a verified inventory, not a substitute for it.

---

## 2. S3 — `DECISION`: 118→candidate conservation, not nine headings

### 2.1 Additional required fields on the decision

```jsonc
{
  "inventory_sha256": "<sha256 of the canonical inventory object>",
  "identity_dispositions": [
    {
      "identity_id": "K1-CAP-01",
      "disposition": "PRESENT_PRESERVED | FUTURE_NONPRECLUDED | EXACT_OWNER_HOLD | BLOCKING_LOSS",
      "candidate_specific_effect": "≤ what THIS candidate does to the located semantics",
      "first_consumer_consequence": "≤ what changes at the named first reader / refusal",
      "conservation_or_refusal_witness": "≤ the positive or refusal witness",
      "origin_row_sha256": "<must equal the inventory row's origin.row_sha256>",
      "evidence_grade": "CODE_STATIC | DOCUMENTARY | EXECUTED_SOURCEFREE | EXECUTED_NATIVE | UNVERIFIED_HELD",
      "owner": "≤ required when disposition == EXACT_OWNER_HOLD",
      "adopted": false,   // required false on PYAT_PC
      "closed":  false    // required false on P4R
    }
  ]
}
```

### 2.2 Checks

| Code | Meaning |
|---|---|
| `DECISION:IDENTITY_UNIVERSE_INCOMPLETE:<group>:<ids>` | a distinct historical functional decision is missing — **the D2 hole** |
| `DECISION:IDENTITY_UNIVERSE_HAS_EXTRA` / `DUPLICATE_IDENTITY_DISPOSITION` | invented or duplicated identity |
| `DECISION:INVENTORY_NOT_PINNED` | dispositions not bound to the verified inventory object |
| `DECISION:IDENTITY_ORIGIN_NOT_VERIFIED` | `origin_row_sha256` does not match the byte-verified row |
| `DECISION:IDENTITY_EFFECT_NOT_GROUNDED_IN_ORIGIN` | the effect text shares <2 distinctive tokens with the located source semantics |
| `DECISION:UNAUTHORIZED_PROPOSAL_ADOPTION` | a PYAT_PC row is `PRESENT_PRESERVED` or `adopted:true` |
| `DECISION:FALSE_PROOF_CLOSURE` | a P4R row is `PRESENT_PRESERVED` or `closed:true` |
| `DECISION:IDENTITY_HOLD_WITHOUT_OWNER` | `EXACT_OWNER_HOLD` without a named owner |
| `DECISION:READY_WHILE_LOSING_REQUIRED_FUNCTION` | (retained) an `AUTHOR_PROPOSED_PENDING_C` grade with any `BLOCKING_LOSS` |
| `DECISION:READY_WITH_PRESENT_HARD_HOLD` | (retained) a present-hard requirement held at author grade |

**Why the grounding-token rule exists.** Set equality alone proves *count*; it does not prove the row is about the identity. Requiring ≥2 distinctive token overlap between the proposed effect and the byte-located source semantics is a cheap floor that defeats copy-paste boilerplate. It is a floor, **not semantic review** — a deciding author can still write a wrong-but-topical sentence, and only independent C can catch that.

---

## 3. C — `C_INTEGRATED`: boundary court, typed graph, builder bytes

### 3.1 Boundary court (per T1–T7)

```jsonc
{
  "boundary_contract_sha256": "<sha256 of 02_BOUNDARY_CONTRACTS.json>",
  "boundary_court": [
    { "boundary":"T4", "contract_name":"<must equal the frozen name>",
      "must_preserve_witness":"<≥3 token overlap with the frozen must_preserve>",
      "status":"ACTUAL_PROVED_AT_SCOPE | SOURCE_STATIC_CONSERVED | EXACT_OWNER_HOLD",
      "positive":{"case":"…","expected":"…","evidence_grade":"…"},
      "negative":{"case":"…","expected":"…","evidence_grade":"…"},
      "restore":{"case":"…","expected":"…","evidence_grade":"…"},
      "graph_edge_ids":["E4"] }
  ]
}
```

Checks: exactly T1–T7; frozen contract name preserved; contract file hash pinned (`C:BOUNDARY_CONTRACT_NOT_PINNED`); each of positive/negative/restore present and non-vacuous (`C:BOUNDARY_MISSING_RESTORE:T4`, …); an `EXACT_OWNER_HOLD` must name an owner and an exact hold; otherwise the cited graph edges must exist and carry that boundary (`C:BOUNDARY_NOT_GRAPHLY_CONNECTED`).

**Why this is not "seven new stages".** The court is an *interrogation record*, exactly matching `02_BOUNDARY_CONTRACTS.json`'s own `meaning` field. A direct branch may bypass an intermediate product, so the court does **not** require a linear T1→T7 path; it requires each boundary to have an answer.

### 3.2 Typed whole-machine graph

```jsonc
{ "typed_graph": {
    "nodes":[{"id":"SRC","kind":"…","owner":"…","authority":"OBSERVED",
              "time_class":"OBSERVATION_TIME","payload_types":["event"]}],
    "edges":[{"id":"E1","from":"SRC","to":"C11","payload_type":"event","boundary":"T1",
              "authority_from":"OBSERVED","authority_to":"OBSERVED","time_class":"OBSERVATION_TIME",
              "evidence_grade":"DOCUMENTARY","negative":"…","restore":"…",
              "first_consumer":"…","external_source_warrant":"… (only where an authority upgrade is claimed)"}] } }
```

Authorities: `EXTERNAL_OBSERVED, OBSERVED, DESCRIPTIVE_MODELED, STRUCTURAL_QUALIFIED, FICTIONAL_WORLD, ACTOR_STATE, HISTORY_EVENT, RIGHTS_METADATA`.

Checks: `GRAPH_TYPE_HOLE` (payload not declared on both ends), `GRAPH_AUTHORITY_HOLE` (edge authority ≠ node authority), `GRAPH_TIME_HOLE` (clock mismatch), `GRAPH_NO_CONSUMER`, `GRAPH_NO_NEGATIVE`, `GRAPH_NO_RESTORE`, `GRAPH_ORPHAN_EDGE`, `GRAPH_BOUNDARY_UNROUTED`, `GRAPH_SOURCE_TO_ACTOR_DISCONNECTED`, and the escalation firewall:

```
forbidden without external_source_warrant:
  DESCRIPTIVE_MODELED → STRUCTURAL_QUALIFIED
  DESCRIPTIVE_MODELED → OBSERVED
  FICTIONAL_WORLD     → OBSERVED | STRUCTURAL_QUALIFIED
  ACTOR_STATE         → OBSERVED | STRUCTURAL_QUALIFIED
  HISTORY_EVENT       → OBSERVED
```

This is the precise executable form of the T4/T6/T7 vetoes: a survey/prevalence node cannot *become* institutional power, a fictional branch cannot become observation, and an actor's state cannot become evidence about the world.

### 3.3 Builder handoff

```jsonc
{ "projection_manifest": {
    "files": { "DESIGN_DECISION.md":"<sha256>", "COVERAGE_TO_DECISION.tsv":"…",
               "DOWNSTREAM_BUILD_HANDOFF.jsonl":"…", "EVIDENCE_AND_FALSIFIER_INDEX.jsonl":"…",
               "GLOBAL_ARCHITECTURE.json":"…", "BOUNDARY_TRACE.json":"…" },
    "digest": "<sha256 of the canonical file map>",
    "schema": "ANVIL_R7_BUILDER_PROJECTIONS",
    "scope": "DETERMINISTIC_CONSTRUCTION_ONLY__NO_SCIENCE__NO_RECEIVING" } }
```

Checks: `C:NO_BUILDER_PROJECTIONS`, `C:PROJECTION_SET_INCOMPLETE`, `C:PROJECTION_MANIFEST_NOT_SELF_CONSISTENT`, `C:PROJECTION_MISSING:<name>`, `C:PROJECTION_BYTES_CHANGED:<name>`. See `COLD_BUILDER_OUTPUT_SPEC.md` for the ABI.

### 3.4 Retained honest ceilings

`PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED` is the strongest string C can emit. Added hard RED: `C:FALSE_PROTECTED_H1` when a packet claims protected receiving. Retained: `C:FALSE_AUTHORITY`, `C:SELF_CERTIFIED_INDEPENDENCE`, `C:ADMIT_WITHOUT_CURRENT_BUILDER`.

---

## 4. Positive / negative / restoration contract — actually executed

Command: `python3 -m unittest test_r7_integrated_d3a -v` in `PACKAGE/tools` (see `TEST_TRANSCRIPT.json`).

| # | Required behaviour | Test | Result |
|---|---|---|---|
| 1 | valid source-only 118 inventory S1 **PASS** at documentary grade | `S1.test_source_only_inventory_passes_at_documentary_grade` | PASS → PASS |
| 2 | synthetic SPINE as fake original **RED** | `S1.test_synthetic_spine_cannot_be_the_origin` | RED as asserted |
| 3 | missing row / blob / **B-10** **RED** | `S1.test_missing_row_blob_or_B10_is_red`, `test_source_file_absent_is_red` | RED as asserted |
| 4 | 26 newly adopted or 14 magically closed **RED** | `S1.test_26_adopted_or_14_closed_in_inventory_is_red`, `Decision.test_decision_cannot_adopt_26_or_close_14` | RED as asserted |
| 5 | 53 rows complete + one distinct historical decision missing ⇒ **DECISION RED** | `Decision.test_one_missing_historical_decision_in_complete_53_is_red` | RED as asserted |
| 6 | seven T contract negative/restore missing ⇒ **C RED** | `IndependentC.test_each_T_contract_needs_positive_negative_and_restore` (T1/T4/T7) | RED as asserted |
| 7 | typed graph producer/authority/time/consumer hole ⇒ **C RED** | `IndependentC.test_typed_graph_type_authority_time_and_consumer_holes_are_red` | RED as asserted |
| 8 | no full-rival A/B required | `Decision.test_no_full_rival_ab_required` + baseline PASS | PASS with `requires_full_A_B_comparison:false` |
| 9 | local fake H1 accepted ⇒ **RED** | `IndependentC.test_local_fake_h1_is_red` | RED as asserted |
| + | weakened boundary contract ⇒ RED | `test_weakened_boundary_contract_is_red` | RED |
| + | authority upgrade without warrant ⇒ RED | `test_authority_upgrade_needs_an_external_warrant` | RED then allowed with warrant |
| + | six projections byte-mismatch/missing ⇒ RED | `test_six_builder_projections_must_match_bytes` | RED |
| + | builder determinism | `test_builder_is_deterministic` | identical manifest twice |

Totals: **24 new tests** (`test_r7_integrated_d3a.py`) + **18 retained** (`test_r7_integrated.py`, corrected fixture) + **12 command groups** in `run_r7_quality.py` — all exit 0.

### 4.1 Two retained tests whose premise was the defect (declared, not silenced)

| Old test | Old expectation | Correction |
|---|---|---|
| `test_existing_historical_spine_transfers_without_new_census` | a bare R5/R6 fixture is sufficient to construct S1 history | still tests `transfer()`'s verbatim-copy behaviour; the **gate** now additionally requires `origin_inventory` (`test_legacy_transfer_without_source_origin_is_red`) |
| `test_good_uncontested_integrated_decision_without_a_b` | PASS from a synthetic SPINE fixture | same *intent* (a good uncontested decision passes) but the fixture is now the byte-verified inventory, and the decision carries 118 dispositions |

This is a visible correction of an obsolete premise, not a weakening: the new suite is strictly stronger (42 tests vs 18, and the two replaced assertions now require real bytes).

---

## 5. What was deliberately NOT added

- No new tribunal, register, board, or approval. The three gates are the three existing stages.
- No mandatory rival architecture, no A/B bakeoff, no numeric comparator.
- No K3 recensus, no new K4, no promotion of the 26 or closure of the 14.
- No semantic verdict machine. The gates authenticate **location and shape**, and leave **meaning** to independent C and to the owners.
- No native 100k claim, no science, no actor right, no protected H1.

## 6. Residual weaknesses (honest)

1. **Boilerplate floor, not semantics.** The 2-token grounding rule defeats copy-paste but not a fluent wrong sentence.
2. **Terminal-16 binding is thin.** My instrument binds F1–F8/N9–N12/PRE-V3/SEAM/SOROK to documentary excerpts (`D3A_TERMINAL_ORIGINS.json`); a real decision needs their operative definitions from their owners.
3. **`DOC_ROW` excerpt matching is substring-based.** A row could quote a real but irrelevant sentence; the token-grounding rule plus C review is the only brake.
4. **The C boundary court can be filled with `SOURCE_STATIC_CONSERVED`.** That is honest but weaker than `ACTUAL_PROVED_AT_SCOPE`; the schema distinguishes them and `C_CONDITIONALLY_ADMIT_DESIGN` still requires an executed current builder card.
5. **`check_builder` is inherited and only partially re-verified here.** I did not widen it beyond the R7 original behaviour.
6. **Strongest alternative** — a pure "manifest-only" S1 (one hash per source file, no per-row locator) would be ~40 lines smaller. It is rejected because it cannot detect a missing B-10 row inside an otherwise unchanged file, which is exactly negative test #3. See `ALTERNATIVE_AND_COUNTEREXAMPLE.md`.
