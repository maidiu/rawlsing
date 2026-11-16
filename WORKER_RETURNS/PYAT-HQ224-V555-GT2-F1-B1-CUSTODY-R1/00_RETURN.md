# PYAT HQ224 — V555 GT2 CURRENT-RULE F1/B1 CUSTODY RECOVERY — R1 RETURN

**DISPOSITION:** `V555_GT2_F1_B1_CUSTODY_PARTIAL__NAMED_GAP`
**BRANCH:** `agent/rabochii-pyat-hq224-v555-gt2-f1-b1-custody-r1`
**COMMISSION TIP:** `ab5278d1dde791b76ff698afd0c96bbf12303e06`
**EVIDENCE BASE:** `71f9f5593a9ebc59fe585a0d6ae9f1de100b1a74`
**IMPLEMENTATION MUTATION:** NONE
**AUTHORITY ADOPTION:** NONE · **SELF-ADOPTION:** NONE

---

## 1. Bottom line

The custody gap resolves **asymmetrically**, and that asymmetry is the finding.

| Family | Current-rule custody | Verdict |
|---|---|---|
| **F1** | exists, content-addressed, published, committed-corroborated | **RECOVERED** |
| **B1** | does **not** exist and may **not** be created | **NAMED AUTHORITY GAP** |

**F1** (current adopted rule):

```
object_id    urn:rawlsing:v554:f1:sha256:3530f08f43e704ad67e0fb74984b03b7ad0f068ea1de4bcf658f3b2d591bd56d
content_hash a008553dc94af138de44e73ade8ddbcc1e2bb3a5c40cec575aad694aae104cbb
```

**B1** is deterministically computed by the accepted M1 owner, but is **deliberately
not published**. This is not a gap awaiting a materialization step.

---

## 2. The decisive governance fact

The current adopted SIG-004 V554 rule — `GT12_V554_SIG004_ADMITTED_RELATION_CONTEXT_PUBLICATION_RULE@1.0.0`
(`da431544…`) — publishes **F1 only**:

- `publication_object_families_exact: ["F1"]`
- `forbidden: [… "F2", "B1" …]`
- publication authority `allowed_object_families: ["F1"]`, `authority_exclusions` include `"B1_PUBLICATION"`
- adoption authority ceiling: `publication_object_families_exact: ["F1"]`

Committed evidence states it in words: *"B1 may exist inside eligible M1; adopted law
forbids B1 PUBLICATION. Direct V557 handoff is F1-only."* and *"B1 must be None"*.

So B1's absence is **a publication-authority decision**, not a computation gap and not a
missing step. Answering required-work item 7 directly: **no materialization step can
close B1.** Supplying it would require an authority decision to widen publication
authority — out of scope here, and precisely the structural-route smuggling the
commission warns against.

---

## 3. F1 recovery, and how it was verified

Traced through the **current** binding/harness — `run_current_r1c_e2b_actual_objects`
under the no-argument adopted bundle — not HQ221's local fixture.

Four independent confirmations:

1. **Owner identity law.** `f1_id = _urn("v554:f1", f1_material)` and
   `content_hash = semantic_hash(f1)` recomputed independently → **exact match**.
2. **Publication.** Present in the direct V557 handoff, in the published V558 object
   payload (`f1_id`), and as `semantic_class == "F1"`.
3. **Committed corroboration.** The committed E2B terminal evidence's
   `f1_publication_roots` contains **exactly** this object_id and content_hash; 3
   committed files carry it.
4. **Determinism.** An independent re-run reproduces identical identities.

**The rule is inside the preimage.** `rule_id` / `rule_version` / `rule_hash` are fields
of `f1_material`, so a different rule *must* yield a different F1. HQ223 was right that
HQ221's fixture-rule F1 cannot be promoted — and substituting its hash demonstrably
changes the F1 id.

**Lineage bound:** relation ref `1ffdfe53…`, admission ref `a445e43d…`, basis
`06f95c1e…`, lineage-closure fingerprint `732ddd91…`, target use
`STRUCTURAL_MEDIATION_INPUT`, risk set `0484fa5c…`, producer query/fact/predicate/replay
hashes — all carried into the published object.

---

## 4. Required work item 6 — custody classes distinguished

| Class | Artifact |
|---|---|
| **CURRENT_ARTIFACT** | current-rule F1 (published, committed-corroborated) |
| **DETERMINISTIC_RECONSTRUCTION** | both F1 and B1 reproduce identically from retained R1C determinants + adopted bundle |
| **HISTORICAL_ONLY** | HQ221 fixture-rule F1/B1 (`V554-RULE-GT2-CONDITIONAL-SUPPORT`) — never promoted |
| **SYNTHETIC/TEST_ONLY** | HQ221 local fixture refs, same classification for custody purposes |
| **COMPUTED_BUT_NOT_PUBLISHED** | current-rule B1 — reproducible, not published, **not custody** |

---

## 5. Hostile checks — 8/8 fail-capable

| # | Attack | Result |
|---|---|---|
| H01 | F1/B1 from old/synthetic fixture | REJECTED — both differ from HQ221 refs |
| H02 | same object_id, wrong content hash | REJECTED — content hash is an independent hash over the whole object |
| H03 | stale V554 rule | REJECTED — rule hash is inside the preimage |
| H04 | wrong relation/admission lineage | REJECTED — lineage fingerprint moves; exact refs survive |
| H05 | wrong target use | REJECTED — target use is inside the preimage |
| H06 | manually relabeled M1 contract | REJECTED — contract version inside preimage; owner contract unchanged |
| H07 | test fixture refs as current custody | REJECTED — published payload carries only the current F1 |
| H08 | **manufacturing B1 custody from the internal computation** | REJECTED — B1 absent from handoff, published object and committed roots |

---

## 6. A correction I made to my own work

My first B1-absence check used a naive substring test for `"b1"` and **false-fired** on
the hex fragment `…a176cbb30a174faf4…`. I replaced it with a structural check (no B1
key, no B1 ref, no B1 family). The underlying conclusion was correct, but the original
check would have been wrong evidence. It is recorded in artifact 04 rather than
silently dropped.

---

## 7. Scope discipline

- **No implementation mutation** — `git diff` over `rawlsing_next/` is empty.
- **No authority adoption, no self-adoption.**
- **No structural-route authority inferred.** Source position, channel and receiver
  position authority are all recorded `NOT DERIVED`; that is the sibling archaeology lane.
- The `allowed_v555_structural_use: True` flag on the internal B1 is an *M1 computation
  result*, not structural-route authority. It is not promoted and not treated as custody.
- Source-free: the chain was re-executed from the retained R1C empirical product.

---

## 8. Named gap for HQ

`HQ224-GAP-001__B1_PUBLICATION_AUTHORITY_ABSENT_BY_ADOPTED_LAW`

No current-rule B1 custody exists or may be created. Closing it requires an **authority**
decision to widen publication authority — explicitly not a custody or materialization
task, and not this lane's to make.

---

## 9. Artifacts

Under `WORKER_RETURNS/PYAT-HQ224-V555-GT2-F1-B1-CUSTODY-R1/`: `00_RETURN.md`,
`01_CURRENT_SIG004_RULE_AND_BUNDLE.json`, `02_EXACT_F1_CUSTODY.json`,
`03_EXACT_B1_CUSTODY.json`, `04_RECONSTRUCTION_AND_CURRENTNESS_PROOF.json`,
`05_FINAL_DISPOSITION.json`.

`HQ224_V555_GT2_F1_B1_CUSTODY_RETURNED__F1_RECOVERED__B1_NAMED_AUTHORITY_GAP`