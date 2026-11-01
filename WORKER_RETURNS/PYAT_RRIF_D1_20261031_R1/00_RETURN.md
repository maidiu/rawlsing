# PYAT RRIF-D1 — ACCEPTED CODE / RECEIVER FATES — RETURN R1

**Status:** independent I3 accepted-integration and consumer comparison. Not HQ, not a native/scientific issuer, not a PREMAIN integrator, not an author of the six lineages, not own reviewer. No merge, adoption, permission, source science, actor/model-use issuance or PREMAIN mutation.

**Branch:** `agent/pyat-rrif-d1-accepted-receiver-fates-20261031-r1`
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d1-accepted-receiver-fates-20261031-r1`
**PREMAIN at start and end:** `8e44ca9c751049d65e6def47600b5c073ee04b29` (remote `refs/heads/integration/pre-main-reconciliation-r1` read back unchanged).
**Exact cuts read:** RRIF-C `b75addf621c3a6c1a3b196bd92a810fad77ae3ae`; RRIF-V hostile `bec050449f0b38606718e4e9691caa1721fcd94f`; A `84182f9fa7044d67689ea4f80eabf7e9337f15c2`; B `59e6e62600814d82cfefd1a2137b7aa63316bc95`; A×B `f5a9facd189af6756c2b15c8daebe680016f658a`; E8 `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`.

**Harness/model verification:** process argv contains `opencode run --model opencode-go/deepseek-v4.1-flash --variant max --agent build`. Session DB row `ses_e6af3a6cbffeVfRfHa85tHy2c6` records `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`. No model/provider/host/account/editor/effort switch occurred.

**Write scope:** only `WORKER_RETURNS/PYAT_RRIF_D1_20261031_R1/**`. No PREMAIN, main, Sorok, native/protected source, pending reviewer or other worktree mutation. No force push. #580–#584 untouched.

## 1. Six dispositions

| Lineage | Disposition | Engineering | Science | Authority |
|---|---|---|---|---|
| `LIN-C1_ANALYTICAL_COMPOSITION` | `CURRENT_RETAINED` (C1-02 successor exact current; C1-01 blobs superseded inside the lineage) | `ACCEPT` (C1-02 source identity/test; no production call site found) | `HOLD` | `ACCEPT` (only historical HQD-139/HQD-145 scoped decisions; no new adoption) |
| `LIN-C1_M2_RELEASE_BINDING` | `HOLD_UNPROVED` | `HOLD` (development candidate, absent current, no importer) | `HOLD` | `HOLD` (nonissuing, no issuer/grant, no HQ adoption) |
| `LIN-C3_PHYSICAL_DECODER_R5_G01` | `ADAPT_REPAIR_CANDIDATE` | `RED` (D01/D02 current loss; PR526 custody passes; G01 binding present, authority absent) | `HOLD` | `HOLD` (production repair needs decoder/codec owner plus source authority) |
| `LIN-C3_R9_SOURCE_BROKER` | `HOLD_UNPROVED` | `HOLD` (absent current, no importer, conflicts with PR526 custody) | `HOLD` | `HOLD` (no real current issuer/role owner; historical HQD-199 not current adoption) |
| `LIN-C5_N5_STRUCTURAL_CONTEXT` | `SUPERSEDED_PROVED` | `ACCEPT` (capability; wrapper absent, current owners reproduce exact retained floor and refuse denominator drift) | `HOLD` | `HOLD` (any new wrapper adoption; historical HQD-151 only) |
| `LIN-N10E_EMPIRICAL_POSSIBILITY` | `CURRENT_RETAINED` (provider core exact current) | `ACCEPT` (provider/source-identity only; AT17 lifecycle and source-context authenticity remain HOLD) | `HOLD` | `HOLD` (context/source authenticity; historical HQD-147 only) |

The six IDs appear exactly once in `SIX_LINEAGE_DISPOSITIONS.jsonl`.

## 2. Exact accepted decisions and current state

### C1 analytical composition

- **C1-01:** HQD-2026-09-30-139; accepted integration tip `5fafb499d53dddadaf8a7b4fd46506e91a09d270`; independent review `98825f710e5238e794c78bf0acbb43faaea355e4` (`APPROVE_AT_DECLARED_GRAIN`). Composition blob `26f3380cb83c`; test blob `68631fb1a18f`.
- **C1-02:** HQD-2026-10-01-145; accepted integration tip `bc661188b51e995d9f5d74e55c4e37d2ba358a17`; independent review `59d69ba31b8de2d028bd44048e8d7b75f2d82538` (`APPROVE_AT_DECLARED_GRAIN`, blocker `C1-02-REVIEW-BLOCK-WITNESS-PAIR-001` closed). Composition blob `604c8d591d4c`; test blob `2210fc1b4cb9`; higher-order test `c8a83d3deffa`; fixture `0393cc8c17a3`.
- **Current:** all three C1-02 code/test blobs are exact at PREMAIN. C1-01 blobs are not exact; its legacy AT07 path survives inside the C1-02 composition.
- **Negative history:** R6 `458f839845` found incomplete preimage authority and a CLOSED-16-key extra-field counterexample; the current `_verify_witness` enforces exact key-set equality (`pre553_analytical_composition.py:494-500` legacy, `:586-589` multi-binding). C1-02's reachable pairing-ground-truth repair is current.
- **Consumer:** `pre553_empirical_possibility_provider.py:35`, `pre553_analytical_state_and_route.py:939` and `pre553_n9_n10w_progressive_candidate.py:59` import the composition; no production call site exists. Runtime evidence is test-hosted through the N10E provider/progressive tests.
- **Tests:** 48 passed (`test_pre553_analytical_composition.py` 13 + higher-order 35). Targeted R6/R7 witness tests 2 passed; pairing/ordering tests 4 passed.

### C1-M2 release binding

- **Source:** F8D `69bb0fc69175b2f6048b00cfa47dc852593798c0` (module `2f6ab22c`), F8E `2a4a90ec76d3400f98ba6fd3fd306f6ff977d042` (module `36563ddee5b6`, tests `1e972bf91992`).
- **Decision status:** HQD-2026-10-10-280 authorizes a development candidate, not operative C1 issuance/adoption. F8D is nonissuing: `grant=None`, `external_issuer=None`, `G0B_HELD`.
- **Negative:** F8F independent review `aecc32736` reproduced 280/280 and recorded the B5 caller-supplied provenance boundary open. The candidate itself states it does not authenticate a caller-supplied C1 result against G1 owner-held source.
- **Current:** module absent; no importer. Current M2 release owner `pre553_learned_product_release.py` blob `f76c390665f0` is imported by `pre553_learned_world_composition.py:40` (blob `4a8e27a226a9`), but that composition has no production importer.
- **Disposition:** `HOLD_UNPROVED`. No real current C1→M2 receiver and no competent producer issuer. Do not adopt.

### C3 physical decoder / R5 / G01

- **Decision:** HQD-2026-09-30-131; accepted integration `30686b185d4ceb2c94f61815ef70d8c8e76255d6`; independent integration review `462e6bf1ed514056f9316dad761054e690a7755d`/`4ded1143` (`APPROVE_AT_DECLARED_GRAIN`).
- **Accepted blobs:** decoder `d3d828c171ea`, R5 codec `6000a1704d71`, G01 `31a9afd7d91e`, tests `fb7b090809a6`, `8fc059653860`, `3901f10a4878`.
- **Current:** decoder `8732e34d0ea3` (PR526 `_SourceSnapshot`, commit `30f9e42ed`), R5 codec `72f8f3c03ed0`; G01 and all three tests absent.
- **Negative history:** C3-02 required changes for item-unwrapped timezone-aware date/time handling and import-time dependency installation; C3-03 was static-pass/execution-pending. C3/R9 recovery (`4da445880`) proved D01/D02 are genuine current losses and R9 transplant is unsafe.
- **Current fault evidence:** `ac0b8bc1…+BIG5` refused (`encoding override is not in the frozen exact SHA/config allowlist`); `DECLARED_ENCODING_ALLOWLIST` and `SOURCE_DECLARED_ENCODING_ONLY` absent; `_jsonable(date(2020,1,2))` returns `"2020-01-02"`; `_jsonable(datetime(..., tzinfo=UTC))` returns a string instead of refusing; `opaque_decoder_value`/`normalize_decoder_physical_value` absent; naked date encode refused. G01 binding behavior is present at the C11 key/facade layer (`physical_value_binding_key(1.0)` = `47f141e4…`; int key differs); the C3/R9 recovery return records the current SAV float lane as the source. The exact nine-surface G01 authority module is absent.
- **Source custody:** PR526 snapshot positive/fault tests passed: O_RDONLY fd, `/dev/fd` reader path, snapshot survives original-file tamper, wrong expected SHA refused, unlink/close idempotent.
- **Consumer:** `ee_p2x_darwin_stage_backend.py:713` is the actual production call to `decode_dta`/`decode_sav`; `pre553_source_native_preimage_adapter.py:30` is a static importer. No current consumer of D01/D02/G01.
- **Disposition:** `ADAPT_REPAIR_CANDIDATE` — bounded production repair on top of current decoder/codec, not a historical transplant. No patch was written because the write scope is returns-only and the production decoder owner/source authority is separate.

### C3/R9 source broker

- **Decisions:** HQD-2026-10-03-199 is the primary `HQ_ACCEPT` for the broker/refinement tip `4b6335ca5fc485108b0ffb1d682a29a02e1eee51`; HQD-2026-10-03-198 is the same-tip contextual/`HQ_OTHER` blocker and must not be dropped. Final independent review `0deb64784829661780ee3957f8070ccc2c241722` accepted the hardened execution binding at binding grain.
- **Accepted blobs:** broker `090d978bbd63`, session `ac1390b861f6`, execution binding `0e11af2205a0`; courts `c1bc82732984`, `8b45e3f9ac14`, `67492110a148`; accepted runtime placement `dfdf5659fd78e9bc996b07383349094059a5553d`.
- **Current:** all three modules and courts absent; no importer. `IssuedWorkloadRecord` has no role field (`pre553_issued_workload.py:78`); `TestOnlyDecisionResolver` is explicitly a test double (`pre553_native_workload_binding.py:403`).
- **Negative history:** HQ196 confirmed broker route but found raise-inside-read hang, seek/tell requirement, fresh-broker-per-call requirement, `usecols` post-read projection, and the selected-read operation itself missing. HQ204 recorded incomplete dependency closure; HQ207 resolved the SR06 seam but the governed environment failed. The C3/R9 recovery measured six current SAV representation failures if the historical R9 decoder is transplanted.
- **Disposition:** `HOLD_UNPROVED`. Historical HQ acceptance is not current retention. Any successor must be built on PR526 snapshot custody, with a real issuer/role record and a real current consumer.

### C5/N5 structural context

- **Decision:** HQD-2026-10-01-151; accepted integration `151d39260a803635f622323b14e42d96c7976d25`; independent review `294d8935ccab6f0f3c0d462a0f6f78e2e5f4a4ae` (`APPROVE_AT_DECLARED_GRAIN`). Service blob `35c0a3768d07`; test `3342c2017154`.
- **Current:** service/test absent; no importer. The same six owners remain current.
- **Reconstitution:** loading the accepted service module from Git into a temporary sourcefree path and calling it against current PREMAIN owners returned exactly: query `e4ec3998…d0d0`, fact `540236d5…1f46`, denominator `19,210`, relation `1ffdfe53…d19`, admission `a445e43d…b08d`, M1 `ELIGIBLE`, V557 `ALLOW_CONTEXT_ONLY`, resolved uses `CONTEXT`, producer `V554`, family `F1`.
- **Denominator drift negative:** mutating the loaded fact denominator to `19,211` in memory is refused by the service contract (`current GT2 denominator is 19211, not 19210`).
- **Negative history:** HQ221 positive realization accepted at GT2 grain with corrections; HQ222 review confirmed 36-cell geometry and the V555 contract gap. C5 review observations were nonblocking.
- **Disposition:** `SUPERSEDED_PROVED`. The accepted wrapper's behavior survives exactly in current owners; no current consumer requires the wrapper. No import/re-adoption without a named consumer.

### N10E empirical possibility

- **Decision:** HQD-2026-10-01-147; accepted integration `52e41a41e8bc3b77390016a049095b5aea1721d0`; independent review `43cdc1a8d1077be78a879ef06232a454736084d9` (`APPROVE_AT_DECLARED_GRAIN`).
- **Current:** provider blob `23167aa25291` is exact current. Accepted test `82adfac870f6` is superseded by current test `f776cc2b26be`; fixture `0e384f72fa61` exact. Current C1 composition is the C1-02 blob `604c8d591d4c`.
- **Consumer:** `pre553_n9_n10w_progressive_candidate.py:55` imports the provider and `:327` calls `provide_empirical_possibility_slice`; that progressive module is only imported by tests. No production call site found.
- **Negative history:** HQ222 proved the local positive provider/replay path but recorded `HQ222-N10E-DEFECT-001__EXACT_DETERMINANT_LIFECYCLE_REACHABILITY_NOT_PROVED` (current `AnalyticalDependencyRegistry.build_graph` still ignores `determinant_exact_refs` at `pre553_analytical_replay_dependency.py:432-462`) and `HQ222-N10E-DEFECT-002` (unchanged-identity-after-recomputation branch). Cache presence never restores currentness; that part passed. HQ237 found the fixture-context issuer and C1/N10E trusted-entrypoint custody unproved; the current request has no `fixture_use_context_ref`.
- **Tests:** 43 passed for the current provider court; 8 targeted replay/fresh-process/successor tests passed.
- **Disposition:** `CURRENT_RETAINED` at provider/source-identity scope. Lifecycle reachability and source-context authenticity remain HOLD and are not laundered into retention.

## 3. V hostile corrections used, not reopened

- A's `2,269` is not a current-code subtraction. `1,333` are branch-only exact implementations, `291` are exact-other-path copies requiring owner/ABI proof, `199` are same-path current exact, and `62` are modified non-code. Only the `199` are current source-identity evidence.
- B's `155` are branch rows, not `155` unique decisions: `122` distinct primary IDs, `135` decision records, `151` fate-classified rows, `4` unclassified `HQ_OTHER`, `5` `HQ_OTHER` class rows. Multi-subject decisions and same-tip aliases are not extra decisions.
- `CKPT-20261009-PYAT-HQ274…` is documentary candidate intake with `NOT_A_FORMAL_HQ_LEDGER_DECISION`, `CANDIDATE_BUNDLE_NOT_ADOPTED`, `code_adoption:false`. It is not code adoption.
- Nine accepted integration branches; none is a PREMAIN ancestor. Acceptance is not merge or retention. C1-02, C1-03R, C1-03A and C1-03 join are exact-current; C1-01, C3 and C5 are not; N10E is partial; AT07 is identity-only.
- The C3/R5 exact assets survive in the historical C3/R9 return `24847592…`, but current D01/D02/G01/R9 paths are absent. No transplant was performed.
- #565 returned a real S7-FIX boundary/source-ABI review and was consumed: the six historical boundary identities and negative custody pass, current ownership mapping is RED, current PR526 decoder tests pass at test scope, source relations has no production consumer, and no merge is recommended. It does not change the six D1 dispositions. The #564/#569–571/#575–579 refs present at read time are commission/control tips, not returned review packets. #577 remote unchanged does not mean the worker is idle. #580–#584 were not touched.

## 4. Test evidence

| Test | Result |
|---|---|
| `pytest test_pre553_analytical_composition.py test_pre553_analytical_composition_higher_order.py` | 48 passed in 11.07s |
| Targeted C1 R6/R7 witness tests | 2 passed |
| Targeted C1 pairing/ordering tests | 4 passed |
| `pytest test_pre553_empirical_possibility_provider.py` | 43 passed in 23.52s |
| Targeted N10E replay/fresh-process/successor tests | 8 passed |
| `pytest test_fiabc_lm2_r1j_sav_representation_authority.py test_fiabc_lm1_r1e_n1_physical_boundary.py` | 16 passed in 69.82s |
| Accepted D01 court against current code | 2 failed, 6 passed (declared allowlist/status absent) |
| Accepted D02 court against current code | collection ImportError (`normalize_decoder_physical_value` absent) |
| C3 sourcefree fault script | D01 BIG5 refused; dates stringified; helpers absent; G01 float key present/authority absent |
| PR526 snapshot positive/fault script | O_RDONLY, `/dev/fd`, tamper survival, wrong-SHA refusal, unlink/close all pass |
| C5 reconstitution against current owners | exact 19,210 denominator and all frozen identities; 19,211 mutation refused |
| R9/C1-M2/C5/G01 import probes | all absent (no importers) |
| #565 returned S7-FIX boundary review (consumed, not re-run) | current PR526 byte custody 26 passed, projection 31 passed, carrier 16 passed/1 skipped; current ownership mapping RED; source relations test-only |

No raw survey, native P07, original U/E_pre, FF, CAN/ADP, N11/N12, Sorok actor or model-use issuance was executed.

## 5. Separate verdicts

### ENGINEERING

- **ACCEPT:** C1-02 composition/test exact current and green; N10E provider exact current and green; C5 capability reproduces exactly against current owners; PR526 source custody passes positive and fault probes.
- **RED:** C3 D01 declared-encoding admission and D02 opaque date/time carriage are genuinely lost in current PREMAIN; timezone-aware date/time is stringified rather than refused; G01 exact authority wrapper absent.
- **HOLD:** C1-M2 release binding absent, no importer, caller-supplied C1 provenance unauthenticated; R9 source broker absent, no importer, no issuer/role; N10E exact determinant lifecycle edges still not built and no production consumer.

### SCIENCE

**HOLD at every lineage.** No survey meaning, comparability, model authority, structural-world claim, actor/person state, U/E_pre, causal or mechanism semantics is issued. C1/N10E/C5 are sourcefree fixtures/owners; C3 D01/D02 are physical representation only; R9 is source-access control only.

### AUTHORITY

**HOLD except the historical scoped decisions already recorded.** This return does not adopt, merge, re-issue or widen HQD-139/145/131/147/151/199/202 or HQD-280. No source owner, native issuer, G1/G0b, publication or model-use authority is created. The C1-M2, R9 and N10E lifecycle/context residuals require their named external owners.

## 6. Limits

- No production patch was written. The write scope is returns-only; C3 D01/D02 production repair belongs to the PREMAIN decoder/codec owner and needs exact source authority.
- No raw source SHA or native source meaning was verified. C3 D01/D02 negative behavior is observed on current code with synthetic values only.
- No raw survey, SAV/DTA source, actor, model-use or native P07 execution occurred.
- C5 reconstitution used the accepted service module read from Git and committed GT2 transport materialized to a temporary directory; it is sourcefree behavioral evidence, not production adoption. The worktree is sparse and `data/` is not checked out.
- Static imports are not behavioral proof. Where no production call site was found, the consumer is reported as `UNKNOWN`/`TEST_ONLY`.
- No whole-estate recount; RRIF-V counts are used as corrections, not re-derived.
- #565 returned and was consumed at S7-FIX boundary scope; #564/#569–571/#575–579 reviews were not returned in the read cut; #577 remote unchanged is not worker idleness. #580–#584 remain held.

## 7. GitHub readback

Commit and push are non-force. The final 40-hex remote SHA is read back with `git ls-remote origin refs/heads/agent/pyat-rrif-d1-accepted-receiver-fates-20261031-r1` after the final commit and is reported in the session terminal. A file cannot contain the SHA of the commit that contains it; no self-referential SHA is asserted here.
