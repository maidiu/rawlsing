# PYAT S7-FIX — six S6 boundary-function-family repairs — independent return

**Schema:** `PYAT_S7FIX_BOUNDARY_REPAIR_RETURN@1`  
**Branch:** `agent/pyat-s7-six-boundary-function-family-repair-20261031-r1`  
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-s7-six-boundary-function-family-repair-20261031-r1`  
**Role:** independent PYAT S7-FIX source-lineage and function-identity repair engineer at I2. Not the S6 author, S7 reviewer, semantic issuer, original reviewer, or own reviewer.  
**Device/harness/model:** mainMac; OpenCode 1.18.34, agent `build`; `opencode-go/deepseek-v4.1-flash`, variant `max`.  
**Independent session:** `ses_e6f7c46f8ffeJ808JJfoBH3866`, title `PYAT S7-FIX six boundary family repairs`, directory is this worktree. This is a fresh S7-FIX session, not S7 `ses_e700ee99affet8V64XRG9BwxGt`, not S1/H1/H03 `ses_e7285576bffeqo0lE8N0HYK6gc`, and not an S6 author session. MAX was verified from process argv (`--variant max`) and the OpenCode session DB row (model `{"providerID":"opencode-go","id":"deepseek-v4.1-flash","variant":"max"}`, agent `build`).

## 1. Exact inputs and current PRE-MAIN

| Item | Exact value |
|---|---|
| STARTUP | `87755f02ec5c37499b09e80db6fbdcc9316a6b15` |
| PRE-MAIN at dispatch | `d0342290b257f85c3e8931f9962e0aecabc84ed3` |
| PRE-MAIN actual recheck | `d0342290b257f85c3e8931f9962e0aecabc84ed3` (`origin/integration/pre-main-reconciliation-r1`) |
| PRE-MAIN delta vs STARTUP | three audit/workflow files only; `rawlsing_next` tree at both cuts `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`; no production delta |
| S6 return | `2c5cf86beb12b7dbeda5532614784737ad30d89d` |
| S7 return | `026ca72c24d564d4dc203f68385df8c75b4bd3a7` |
| S1 corrected | `6a658ad347ad0a714f40cbce04b5cd6d1f5b5ab5` |
| S2 corrected | `3042fca8a2165e07871d408118e1741686020cdc` |
| S3 corrected | `ebdb51a5c79209b2e552cfce648f7847b19386c2` |
| S4 corrected | `d93e8c2441dfa394e56fc1f5bcf43a0b4388adcb` |
| S5 corrected | `32dac59b3741dcc54f507321c7826e65174af372` |
| Evidence law | `f50651a2bb0758e9fe6d6a2852441dcc782344be` |

S6 and S7 files were read from exact Git objects, not checkout copies. S4 `function_id` was independently re-proved as `sha1(ast.dump(node, include_attributes=False))` against the exact module blob. All 12 S4 boundary IDs matched their exact AST dump hash; all five S5 outer IDs and the S5 join representation resolved to exact AST qualnames; the four S5 emit variant blobs all resolve to the same AST hash `4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445`.

## 2. Verdicts

- **Engineering ACCEPT (bounded static/sourcefree reconciliation):** every original function ID appears exactly once; five outer/nested merges are split; the one emitted-function split is joined; exact AST ownership and lineage are recorded; sourcefree validator passes.
- **Scientific ACCEPT (preservation only):** original method assumptions and adverse scientific findings remain attached to the correct outer/nested/function owners. Structural code identity is **not** promoted to behavioral or scientific equivalence.
- **Scientific HOLD (issuance):** no original source/science issuance was available to this lane and none is claimed.
- **Authority ACCEPT:** bounded static/sourcefree reconciliation only. No merge, adoption, production mutation, source/actor/world/N11/N12 grant, or self-review. **Authority HOLD:** separate original owner/adoption remains required.

## 3. Six actual boundary defects repaired

The defect set is exactly the six S7-discovered defects, not a new or larger set.

| Old S6 group | Correction | Corrected family | Actual qualname | Members |
|---|---|---|---|---|
| `FAM_b8e8a1c5bac3370d` | SPLIT outer | `S7FAM-0869c56ad5e0c899` | `SourceRelationResolver.__init__` | `828fbc7fea7fdcaf419a79ea78c63c574e473f2d`, `rawlsing_next/pre553_source_relations.py::SourceRelationResolver.__init__` |
| `FAM_b8e8a1c5bac3370d` | SPLIT nested | `S7FAM-3ced5b9ab5b98431` | `_make_sealed_source_relation_owner.SourceRelationResolver.__init__` | `d8a2f70fc0de05bfe0f0db6d42e207d8d915ee64`, `733bdba8281c6cdf1fe5ce22cadd060627bd1b6c` |
| `FAM_1427a684892de839` | SPLIT outer | `S7FAM-82686a98a4281425` | `SourceRelationResolver.require` | `1d789a2f1ade746a79847ff1a8f6bf3a9eea97ee`, `rawlsing_next/pre553_source_relations.py::SourceRelationResolver.require` |
| `FAM_1427a684892de839` | SPLIT nested | `S7FAM-0808b82fba697141` | `_make_sealed_source_relation_owner.SourceRelationResolver.require` | `0d719b06e1689c10095dfd9da701dbb02f28bb36` |
| `FAM_214c6eaf1fe2a42d` | SPLIT outer | `S7FAM-5823124c837704c1` | `SourceRelationResolver._validate_positive` | `52bf494350f4abe5c16149241da8506a82401345`, `rawlsing_next/pre553_source_relations.py::SourceRelationResolver._validate_positive` |
| `FAM_214c6eaf1fe2a42d` | SPLIT nested | `S7FAM-739724b429c79765` | `_make_sealed_source_relation_owner.SourceRelationResolver._validate_positive` | `8fcb028899610f219a6b85dc09ef67d429834376` |
| `FAM_6813a575a7ce67c0` | SPLIT outer | `S7FAM-6054813ba02c8e44` | `SourceRelationResolver.decide` | `8dd873c436acfb407ad330294a910e2b082b197a`, `rawlsing_next/pre553_source_relations.py::SourceRelationResolver.decide` |
| `FAM_6813a575a7ce67c0` | SPLIT nested | `S7FAM-dabfb5ad4dc9f0a4` | `_make_sealed_source_relation_owner.SourceRelationResolver.decide` | `920b54cd009151c9c9b9fd7913201d14ce739511` |
| `FAM_c0d48f7daa8cc28d` | SPLIT outer | `S7FAM-a7fe27d3f45643c3` | `SourceRelationResolver.resolve_exact` | `7473e1e908d78e3a3f5bc9537dc922deaae81a6f`, `rawlsing_next/pre553_source_relations.py::SourceRelationResolver.resolve_exact` |
| `FAM_c0d48f7daa8cc28d` | SPLIT nested | `S7FAM-c7246db42c0322e0` | `_make_sealed_source_relation_owner.SourceRelationResolver.resolve_exact` | `1e88e2680b5d88f8115575c5b382dc9c0658dbb2` |
| `FAM_bd6118ca46930519` + `S6FAM-23dd9c27fe2a7c60` | JOIN | `S7FAM-41da3f505673271b` | `PhysicalSourceIncidence.iter_batches.emit` | `4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445`, `rawlsing_next/pre553_physical_decoder.py::PhysicalSourceIncidence.iter_batches.emit` |

**Counts:** 1,881 old S6 groups + 5 splits - 1 join = **1,885 corrected families**.

### Exact lineage facts for the repaired boundaries

- Outer `SourceRelationResolver` lineage origin: `ce4edcc83dbf99c6c6edc856288bdcfd60ce29dd` (file add; no nested owner).
- Nested `_make_sealed_source_relation_owner.SourceRelationResolver` qualname lineage origin: `fbb735f695ec0753085f11d2d4b7c521a4749874` (HQ231 lexical sealing).
- Exact outer blob introduction: `61acee605d618ed4a0db11d893f6139593ae5780` (blob `00f50ea547dd224221ed232f68cd84c1e4b7a463`).
- Exact nested blob introductions: `d5e6d6baa67ddf25a9864be6bb2564b535e0868f` (blob `d9fb2c48ff6f2b68b2b8b06a47402c65cf6b7737`) and `c86ae335eaf70e82b5764c46754b16ca7e1587ce` (blob `8053d30d306a3654ebf563043088311ff390bb2b`).
- `PhysicalSourceIncidence.iter_batches.emit` qualname lineage origin: `fc74879bdc3a1d987e3f19022116ac551da582e6`; exact S4 blob introduction `901e3e77f905847d3ef8d86b458280d8fe422dd0` (blob `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf`); earliest S5 variant origin `42ddc284f7a959797d864e6f8e656fbd94d82348` (blob `5a21bdbf314f240a8718fe64b6db734e839a8581`).

## 4. Complete custody and preservation

- **3,135/3,135 function IDs** occur exactly once: S1 1,279 + S2 218 + S3 398 + S4 897 + S5 343. Ordered-ID SHA-256 `5917b3bd58bb56f101d0daa35a0259761234a58a6c4bf9adaf6f0586d3593a68`; per-shard digests match S7 exactly.
- **1,881 old groups** are mapped in original order; no old group is dropped. `OLD_TO_NEW_S6_S7_FAMILY_MAP.jsonl` records old record SHA-256 and, for the seven repaired old groups, the full old S6/S7 records.
- **845 branch names**, 838 distinct tips, per-shard 175/175/174/161/160, are carried in the corrected receiver artifact with ordered-name/tip digests. All 225 S6 inherited branch names are a subset of the 845 roster.
- **Both external zero-member priority cases** `S6EXT-P41-SERVICE` and `S6EXT-R61-R09-NEGATIVE` remain zero-member families and are not counted in the 3,135 row set.
- Reviewer negatives are preserved per member where S6 alignment exists and at group scope where alignment does not exist. The five S5 outer rows contain review prose that names the sealed nested owner; those records are marked `CONTEXTUAL_ONLY__NESTED_SEALED_OWNER__NOT_OUTER_DEFECT` and are not attributed as outer-family defects. Nested defects remain under nested families.
- Variants, permissions, current source ownership, test status, successor candidates, first-consumer evidence, and integration recommendations are retained under the corrected family keys. First-consumer records carry source-field provenance; no consumer was invented.
- Body/source presence is E1 evidence only. Every family is explicitly `behavioral_equivalence: NOT_CLAIMED` and `science_acceptance: NOT_CLAIMED`.

## 5. Validator and test receipts

- `SOURCEFREE_MEMBERSHIP_VALIDATOR.py` reads only the seven S7-FIX artifacts. Baseline: **PASS**, 11 checks, 3,135 function IDs, 1,881 old groups, 1,885 corrected families, 845 branches.
- Self-test: **PASS**, baseline plus 8 fail-capability mutations detected (missing ID, duplicate ID, outer/nested mis-nesting, false join identity, lost adverse review, invented first consumer, branch roster drift, old-group map drift).
- Exact-object AST check: **PASS**, 12/12 S4 boundary IDs match exact AST dump SHA-1; 5/5 S5 outer IDs and the S5 join representation resolve to exact qualnames; 4/4 S5 emit variant blobs resolve to AST SHA-1 `4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445`.
- Full commands, exits, pass/fail counts, output hashes, and ABI limits are in `TEST_RECEIPTS_AND_ABI_LIMITS.md`.

## 6. Explicit UNKNOWN / NOT_RUN

- **UNKNOWN:** introducing commits for non-defect S1-S4 rows were not re-derived by a full object-history walk; branch-tip/presence evidence is retained and introduction remains explicitly unknown where not exact.
- **NOT_RUN:** historical branch code, the C3 55-test court, F7/P07 hostile attacks, and current production consumers were not executed by S7-FIX.
- **NOT_APPLICABLE:** 104 S5 native C/JS rows are not Python-AST-applicable; they retain explicit source identity and are marked `NON_PYTHON__AST_NOT_APPLICABLE`.
- **NOT_CLAIMED:** behavioral equivalence, ABI acceptance, production integration, scientific issuance, source/actor/world/N11/N12 authority, merge, or adoption.

## 7. Independent I3 review handoff

I3 must be a distinct hostile reviewer, not the S7-FIX author, S6/S7/S1/H1 author, or an own reviewer. I3 should independently:
1. Recompute the S1-S5 ordered ID digests and confirm 3,135 exact-once IDs.
2. Re-read the exact AST blobs for the 19 boundary members and confirm the outer/nested actual qualnames.
3. Confirm exactly five splits and one join, with no extra boundary changes.
4. Confirm nested defect reviews are under nested families and the S5 outer contextual prose is not counted as an outer defect.
5. Confirm the 845-branch roster, both external zero-member cases, and that no first consumer was invented.
6. Rerun `SOURCEFREE_MEMBERSHIP_VALIDATOR.py` and `--self-test`.
7. Keep scientific issuance and authority adoption on HOLD unless a separate original owner issues them.

Final S7-FIX commit SHA is reported externally because a commit cannot contain its own hash. No merge, adoption, self-issuance, or protected PRE-MAIN mutation was performed.
