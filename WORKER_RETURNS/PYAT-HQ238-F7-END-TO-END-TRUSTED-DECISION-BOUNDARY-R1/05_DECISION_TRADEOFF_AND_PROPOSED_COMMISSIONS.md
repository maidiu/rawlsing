# 05 — Decision tradeoff and two proposed successor commissions

**Status for every instruction below: `PROPOSED_NOT_AUTHORIZED`.** This worker does not commission, adopt, schedule, merge, or instruct production mutation by force of this file. HQ must separately adopt the desired TCB and issue actual branch/commission authority.

## A. Options at an executable interface grain

| Dimension | Design I: T1 native P07 owner, trusted Python F7 | Design II: T2 protected P07/F7/effect gate |
| --- | --- | --- |
| Actual protected asset | Exact owner-instance constructor custody **and actual P07 decision**, not just a storage capsule | Accepted P07 decision, F7 comparison, receipt replay, and **relying consumer's acceptance action** |
| Attacker | Named T0/T1 same-interpreter reflection; trusted F7 executable and terminal consumer unchanged | Arbitrary same-interpreter Python code/result/alias/verifier substitution; protected server/consumer unchanged |
| Owner identity | Exact static native `SourceRelationResolver` object with private one-shot C state keyed to that very object; no transplantable `_handle` | Trusted provisioner-bound `job_ref + resolver_owner_id` stored server-side; client locator not authority |
| False-positive gate | Native P07 refuses empty victim; trusted F7 consumes exact native decision | Trusted server refuses empty victim **and** no untrusted client result can write trusted acceptance journal |
| Code relocation | P07 algorithm migrates **as one owner** to native; F7 semantic implementation retained in trusted Python | P07/F7 accepted implementations run in server; Python client is non-authoritative |
| Build cost | C type safety, exact P07 port, CPython 3.11.3/macOS x86_64 ABI, Python compatibility/differential court | Separate process/service account, trusted source bootstrap, IPC protocol, replay/correlation, journal, trusted effect recipient, deployment |
| Reliability | In-process call; native crash is process crash; no transport/service liveness failure | Service transport/liveness, daemon lifecycle, secret/ACL isolation, replay journal, crash recovery |
| Portability | Requires compiled native extension per ABI/OS; exact macOS x86_64 build qualification not pre-proven | Existing Python P07/F7 semantics can run in protected separate interpreter, but OS privilege/IPC varies by platform; build/runtime provenance still mandatory |
| Existing consumers | Existing F7 receipt and trusted local consumer semantics remain unchanged under explicit T1 assumption | Every *real* relying consumer must be located and moved/gated. F7 receipt is presently module-local, not an adopted F8/V3 product; no hidden consumer may be invented |
| Same-UIP Python code change | **Not protected** if it reaches final F7/consumer callable; declare T2 out of scope | Protected accept/journal is unchanged even if client callable/verifier/result changes |
| Authority mutation | No new semantic kind, operation, comparison rule, source relation or actor power; owner **representation and ABI architecture** changes require HQ warrant | No new domain authority, but **new process/provisioner/relying-consumer architecture authority** required; cannot rely on an arbitrary privileged service label |
| Five lawful positives | Proven by independent source-free parity on trusted F7 producer and consumer | Proven through server **and trusted accepting journal**; no refusal-only green |
| Main risk | Hidden shared mutable alias, exposed native sealer, native P07 semantic drift, dynamic Python F7 dispatch seam misclassified as trusted | Untrusted Python still acting as terminal consumer, weak OS separation, self-issued server owner ids, wrong replay/nonce/job binding |
| Candidate status | Design sufficient *conditional on exact T1 TCB and proven native implementation*; not an implemented PASS | Design sufficient *conditional on real independent service/consumer boundary*; not an implemented PASS |

**Recommendation:** HQ should prefer **T1** at the present accepted F7 feature grain, explicitly excluding arbitrary rewrite of trusted F7 executable, module-global native owner alias, and trusted terminal consumer. It is a bounded provenance requirement driven by actual witnessed attacker powers and preserves the current F7 semantic receipt without inventing an F8/actor consumer. HQ must not disguise a scope change: named HQ227/HQ231/HQ234/HQ235 reflection and monkeypatch probes **still belong in T1 acceptance**, and must be tested.

**If HQ requires T2 today**, Design II is the correct class of solution, but needs a separate full protected consumer/authority bootstrap warrant. A native capsule or isolated P07 IPC endpoint **alone** is insufficient. If neither T1 TCB nor T2 isolated accepting consumer can be honestly established, HQ must hold F7 nonforgeability adoption rather than declare success.

## B. Exact present evidence anchoring future work

- Commissioned HQ238 exact startup/base: `ae5e140a378406888c94d099b7dd8e98dfeb1459`; launch tip `16ee0054622077c84f815c71c04468bc39411d61`.
- P07 accepted/current working blob: `rawlsing_next/pre553_source_relations.py @ 8053d30d306a3654ebf563043088311ff390bb2b`.
- F7 accepted/current working blob: `rawlsing_next/pre553_temporal_comparability.py @ 6f6b462b1cdef54d7989f15452473383c1661594`.
- F7 hostile court: `rawlsing_next/tests/test_pre553_temporal_comparability.py @ 8a82bd5905d266c1d500b1bf2bdcb01ea948efd6`.
- P07 court and relevant M1 files retain their current exact base blobs; verify them at successor startup, do not silently update.
- HQ236 governed independent review evidence: `WORKER_RETURNS/PYAT-HQ236-F7-COORDINATED-HOSTILE-EVIDENCE-R1/02_EXACT_ATTACK_AND_CONTROL_RECEIPTS.json`, `reproduction/hq236_independent_attack.py`, `reproduction/hq236_attack3_focus.py`, and their outputs.
- Prior independent architecture review at **separate** branch `agent/reviewer-pyat-hq236-f7-owner-boundary-architecture-r1 @ 7a9a0a5917b888c15b3ead051fb116b7549b37c9` is evidence only; do not assume ancestry or merge.
- HQD-216 adopted productive adequacy: exact Git object `e0e7ce0e596e4e5ea7ec96c265ec949b9fe801a2:PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`.
- Governed local runtime evidence: CPython 3.11.3 macOS x86_64 executable SHA-256 `11d6f541a870a141249ce98d45834a6789e29c07031e85ce17f3e67f24c535f6`; current 228 targeted green tests; broad 2691 passed / 45 failed / 7 errors, normalized 54-item fail/error digest `278854ee94fadfd57284a572441522fb56105081f89af431b17ec2e556ace6a9`, no differential from baseline. **Neither suite certified provenance closure.**
- The exact native extension/service binary, compiler version, supported CI runner, future branch and review candidate commit do **not** yet exist. No fictitious SHA, test execution or qualifier is supplied.

## C. Deterministic HQ decision → implementation → independent review sequence

1. **HQ architecture choice (new explicit authority):** adopt exact T0/T1/T2 definitions, declare whether F7's final Python owner alias and terminal consumer are inside T1 trusted code, select Design I (recommended) or II, and freeze exclusions. Do not begin repair if the TCB is ambiguous.
2. **HQ bootstrap:** issue a separate actual commission with branch, exact base, worktree, mutation limit, native/OS qualification environment, binary provenance and no self-adoption. Use the current base above only if verified identical at dispatch.
3. **Implementation source-free:** perform only the selected design; eliminate parallel positive P07 implementations, publish exact API/types and constructor/owner material, runtime acceptance gates, semantics preservation and new hostile tests. Do not mutate V554/V557/V558/F8/actor, relation states, authority kinds, numerical thresholds or temporal comparison semantics.
4. **Worker-local tests:** run exact old F7+P07+M1 courts, four attack variants, private payload-anchor fail-capability, HQ227 monkeypatch and registry-immunity attacks, five positive F7 paths, and deterministic replay. Record tested binary/environment and no-test-greenwashing.
5. **Independent DeepSeek-Harness hostile and runtime lane:** receive exact implementation SHA on a separate branch; independently recreate attacks rather than import worker attack helpers; test actual accepted entrypoint/native module provenance (or server's actual trusted journal if T2), exact source/empty-victim controls and all five positive paths; rerun targeted and broad regressions, compare baseline failure set.
6. **HQ review and adoption:** require source-level review, independent runtime and positive end-to-end gate. Reject semantically drifting ports, forged owner, service self-issued handles, or preserved Python bypass. Only HQ issues the integration/adoption decision; do not auto-promote a green local court to authority.

## D. Proposed successor commission 1 — implementation (paste-ready, but NOT issued)

```text
PROPOSED_NOT_AUTHORIZED — PYAT [HQ ASSIGNS] F7 T1 NATIVE P07 OWNER-INSTANCE / END-TO-END T1 PROVENANCE IMPLEMENTATION R1

AGENT: Space Bunny / governed macOS isolated sparse worktree worker
REPOSITORY: maidiu/rawlsing
MODEL: HQ selects implementation intelligence
BRANCH: PROPOSED_HQ_MUST_CREATE_AND_ASSIGN
EXACT CANDIDATE SOURCE BASE: ae5e140a378406888c94d099b7dd8e98dfeb1459
EXACT BASE BLOBS:
  rawlsing_next/pre553_source_relations.py = 8053d30d306a3654ebf563043088311ff390bb2b
  rawlsing_next/pre553_temporal_comparability.py = 6f6b462b1cdef54d7989f15452473383c1661594
  rawlsing_next/tests/test_pre553_temporal_comparability.py = 8a82bd5905d266c1d500b1bf2bdcb01ea948efd6
UPSTREAM DESIGN: WORKER_RETURNS/PYAT-HQ238-F7-END-TO-END-TRUSTED-DECISION-BOUNDARY-R1/
ARCHITECTURE/T1 TCB: MUST BE EXPLICITLY HQ ADOPTED FIRST; do not infer adoption from this skeleton
STARTUP: verify new HQ-authorized branch SHA equals assigned exact base, shared-store worktree, and clean status; no clone, no branch switching/merge/rebase

MISSION:
  Replace caller-reflectable P07 owner custody and actual authenticated P07 adjudication with an exact
  one-shot native CPython SourceRelationResolver owner whose constructor-sealed private payload cannot
  be read/assigned/rebound by admitted T1 reflection; no exposed sealer/loader/handle transplant.
  The exact native owner instance is the provenance key; copying visible data cannot change its contents.
  Preserve 12-state F7, P07 exact relation/authority semantics, full source/use/operation/scope/time binding,
  existing registry replacement immunity, F7 receipt field set, and replay; preserve C11/direct P07 API or
  report explicit compatibility issue. Trusted Python F7 code and terminal consumer remain T1 TCB.
  No separately viable Python P07 positive path is left in production.

MINIMUM ACCEPTANCE:
  Four HQ234/HQ235/HQ236 attack variants must now be refused for the original EMPTY victim.
  Every court asserts !victim_positive, not assert(forgery_succeeded).
  Distinct independent payload-vs-anchor consistency check must show the SOURCE relation cannot enter
  empty victim native owner, even with victim live anchors left untouched and by_key left empty.
  A test-only fault injection must reopen same victim, make the security court fail, and never ship.
  Preserve all five lawful positives, exact P07/F7 replay and registry/snapshot immunity.
  Avoid vacuous all-refusal solutions; preserve HQD216 productive semantics.
  Qualify native ABI under the actual governed 3.11.3 x86_64 environment and record source/binary/toolchain hashes.
  Compare F7 163 + P07 24 + M1 14/27 targeted courts and broad baseline with documented exclusions.
  Do not silently modify accepted tests only to remove their hostile capabilities.

MUTATION TERRAIN:
  P07 owner representation/native package + narrow F7 callsite/native binding adapter + exact related tests
  and explicitly HQ-authorized build manifests only; no semantics/authority adoption or unrelated file writes.
  Do not touch actor/V3/F8/V554/V557/V558 or create new authority kinds.

RETURN:
  Exact native design/API, C object registration/custody proof, diff and blob hashes,
  four negative attack receipts with old vulnerable control, five positive products,
  fail-capability, runtime provenance, regression, security claims/limits,
  exact pushed branch SHA and truthful COMPLETE/PARTIAL/BLOCKED disposition.

NO SELF-ADOPTION, NO CONTROL MERGE, NO PRODUCTION IMPLEMENTATION WITHOUT THE HQ WARRANT.
```

## E. Proposed successor commission 2 — independent hostile review and runtime qualification (paste-ready, NOT issued)

```text
PROPOSED_NOT_AUTHORIZED — PYAT [HQ ASSIGNS] F7 T1 NATIVE OWNER INDEPENDENT HOSTILE / GOVERNED RUNTIME REVIEW R1

AGENT: DeepSeek-Harness/OpenCode independent hostile reviewer on separate HQ-authorized sparse worktree
REPOSITORY: maidiu/rawlsing
BRANCH: PROPOSED_HQ_MUST_CREATE_AND_ASSIGN
EXACT HISTORICAL SOURCE BASE: ae5e140a378406888c94d099b7dd8e98dfeb1459
EXACT IMPLEMENTATION CANDIDATE HEAD: HQ_MUST_FILL_FROM_VERIFIED_PUSH_AFTER_IMPLEMENTATION
ORIGINAL CODE BLOBS: P07 8053d30d306a3654ebf563043088311ff390bb2b;
  F7 6f6b462b1cdef54d7989f15452473383c1661594;
  F7 court 8a82bd5905d266c1d500b1bf2bdcb01ea948efd6
REQUIRED EVIDENCE:
  HQ236 source-local and governed reproduction outputs/scripts, HQ236 independent browser architecture review,
  HQ238 design and explicit later HQ T1/TCB decision, candidate native source/binary/ABI manifest.
STARTUP:
  Verify candidate exact Git SHA, new review branch start, environment, no mutation or merge.

MISSION:
  Reconstruct original source/empty victim independently under real native F7/P07 path.
  Execute four precise hostile variants: original source anchors/one cell; HQ235 coordinated visible
  _by_ref/_by_key replacement and ledger; HQ236 one-cell only with victim anchors/unchanged fields;
  HQ236 source by_ref-only payload with victim by_key/anchors intact.
  Assert source P07/F7 legitimate positive, victim P07/F7 nonpositive before/during/after each variant.
  If ledger seam is absent, prove native empty-victim custody still cannot be minted via arbitrary
  callable recovery, constructor reinvocation, exposed handle, owner swap or legacy Python path.
  Independently attack private payload-vs-anchor provenance invariant, nested snapshot/replay,
  exact wrong-kind/pair/use/scope, client-side monkeypatch routes within adopted T1 powers,
  public diagnostics and registration. Require fail-capability on actual new load-bearing seal.
  Run five lawful positive F7 paths, exact zero/increase/decrease and cross-universe owner productivity.
  Run governed CPython 3.11.3 actual compiled extension, binary integrity, relevant courts,
  full normalized baseline set, platform ABI and independent differential source parity.
  Determine any required downstream trusted consumer (do not invent F8/V3 consumer).
  T2 arbitrary code/alias/consumer substitution is explicitly OUT OF SCOPE if HQ adopted T1.

RETURN:
  Independent hostilities with raw scripts/output and receipts,
  proof of no false positive / non-vacuous legal positives,
  exact semantic conservation and ABI/runtime/fail-capability audit,
  risk/TCB boundary, exact reviewed and pushed branch SHAs, honest disposition.

NO REPAIR, SELF-ADOPTION, PRODUCTION MUTATION, OR MERGE.
HQ EXPLICIT ADOPTION AND SEPARATE INTEGRATION COMMISSION REQUIRED EVEN IF GREEN.
```

**If HQ selects T2 instead:** the above templates are NOT silently repurposed. HQ must issue separate T2-specific implementation/qualification commissions grounded in `03_T2_END_TO_END_TRUSTED_GATE_DESIGN.json`, naming the actual protected source/authority bootstrap issuer, service binary/OS isolation, trusted job/owner issuance, receiving/committing consumer and full untrusted-client code-rewrite court. Reusing a T1 acceptance statement for T2 would invalidate the security claim.

## F. Unresolved pre-implementation gates (not permission to invent)

1. Explicit HQ determination of T1/T2 powers and what module-level mutation is inside the T1 admitted surface; if final F7 global alias is mutable by attacker, T1 trusted Python cannot be claimed protected.
2. Exact native extension ABI, object layout, constructor one-shot behavior, source hash equivalence, and whether existing subclass/monkeypatch courts need nonsemantic test harness adaptation.
3. Repo-wide **actual** F7 receipt relying-consumer census. Inspected current F7 tests are consumers at test grain; HQ210 authorized no F8 consumption. Do not create actor/F8/terminal use in order to make T2 plausible.
4. Mac/CI runner, compiler, privilege/account and native binary validation feasibility are untested in this documentary lane. A design is not a runtime certificate.

**This file does not adopt a TCB, issue a commission or allow production changes.**
