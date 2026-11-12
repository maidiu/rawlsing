# PYAT S2-B / Agent B R4 — root-identity mutation counterattack on A #965

**Disposition: `REVISE_EXACT_DEFECT__B_R4_SCOPED_ROOT_REPAIR__NATIVE_TEST_NOT_EXECUTED__G5_NOT_RUN`.**

## 1. Source cut, lineage and original contract

- Frozen original assignment [#919/S2-B/P2-02](https://github.com/maidiu/rawlsing/issues/919) and [#909 R3/R3C/R3S](https://github.com/maidiu/rawlsing/issues/909). G1 preserves exact M01–M18 I02 families and correct source/replay/authority/occurrence/negative behavior; G2 requires bounded source-direct certificate and actual native reader change/restore; G3 requires hostile complete corpus and source/authority refusal; G4 requires external roots, bounded resources and recovery; independent G5 only once G1–G4 shown.
- Source authority: [PROGRAMMA PYAT](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md) and adopted [MCR-lite](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md). No original35, scientific, actor, protected-merge, W03/W04 or S2-C permission claimed.
- Exact inherited opponent [PR #965](https://github.com/maidiu/rawlsing/pull/965) frozen `e82a7ee92a32cc8b327d0685267d4aaea1d86a1a`; its code/test cut `d3e3eed5fab51631eb796da4f20ce942ae8fd2ac`. Opponent's parent [PR #961](https://github.com/maidiu/rawlsing/pull/961) `b79d8867986aa16cbe41ae6f48d45317be8adde3`, itself descendant of B [PR #954](https://github.com/maidiu/rawlsing/pull/954) `f5ee89b8e700ac14cf266c2e3eae4c25f021c349`; original A #952 `d5d6577b557fa8ced2dbb42d190ab254ab983b19`.
- This B R4 implementation [PR #971](https://github.com/maidiu/rawlsing/pull/971), `agent/pyat-pair2-s2b-b-r4-root-freeze-20261112`, source/test/workflow exact commit **`04453a6478b0d374c54c86e2e0f1618893e739a8`**. Source blob `524ac3eb53508174dfd13f1b1e6e8178aca1eed7`, test blob `c7691b1449ef4e3c1139ae9af58d16d12773048c`, workflow blob `19229467327d39a51d78834f066ce5e335814f29`. Protected PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e` observed unchanged.

## 2. Concessions / credible A improvements

A correctly preserved B's four earlier real native-I03 safeguards and strengthened them in #961: the raw SQLite connection leaked transaction rollback, TEMP shadow tables and BINARY collation override; an assignment-only seal could be deleted; the exists-check/replace writer could clobber a destination; path hashing then SQLite opening was subject to a separate-inode race. The `main.`-qualified SQL, facade, session lifetime checks, no-clobber link publication and Linux descriptor-pinned physical SHA are substantive engineering improvements. I have not discarded any of them.

A #965 then removed **unbounded Python materialization of malformed closure refs** from both `_check_relations` and `_check_relations_readonly`. Independently ran the same SQLite primitive with 60,000 orphan closure entries: list = **4,640,432 bytes** peak Python tracing; COUNT = **601 bytes**, same 60,000 mismatches. This proves the narrow Python heap improvement, not the end-to-end certificate or 100k pipeline memory limit. A's locally demonstrated result is valid in that restricted sense.

No credible evidence currently supports a blanket rejection of #961/#965 simply because the GitHub Actions runner did not start. Their new native test court is **UNEXECUTED**, not red.

## 3. New G3 failure mechanism neither A nor B previously closed

**G3-R4-01 — authenticated root persona can change after cold verification.** A made the `VerifiedExternalI02` certificate exact-typed and sealed its instance attributes, but its constructor still accepted `isinstance(roots, ExternalI02Roots)`. A `frozen=True` dataclass is not an anti-subclass trust boundary: a subclass can override `__getattribute__` to return A's legitimate `release/source/replay/universe` fields while `VerifiedExternalI02` validates the exact A bytes and A logical root, then return B's fields when `install_sourcefree_external_i02_i03` binds the still-valid certificate to another source release. Neither A's exact certificate class guard nor its sealed certificate attributes prevents changes inside this separate root object. The installer consults `certificate.roots` after the constructor, making this an actual provenance/first-reader attack surface.

**Independently executed Python primitive:** a subclass of a frozen dataclass passed the old `isinstance` gate, returned `release-A/source-A/replay-A` before a class-level toggle, then `release-B/source-B/replay-B` afterward without reassigning any certificate attribute. The new `type(roots) is ExternalI02Roots` predicate refuses that subclass. This primitive proves the vulnerable language/API behavior **but is NOT a repository-level native-I03 execution**.

**Committed native hostile case:** `test_s2b_b4_switchable_external_roots_cannot_authorize_wrong_i03_release`. Uses two genuine I02-ingested sourcefree releases, identical scoped respondents/universe/question but different event coverage; authenticates A's external SQL certificate, switches the supplied root subclass to B's release/replay/source identity, attempts native B installation and execution, and requires refusal of the impersonated root instead of false data/admission. The fixture also checks the authorized B certificate produces its original normal I03 fact.

**Correction:** `VerifiedExternalI02.__init__` now requires `type(roots) is ExternalI02Roots` and issues a typed `ExternalI02IntegrityError` for subclasses. The original externally anchored exact immutable roots returned by `build_sourcefree_external_i02` are unaffected. This is a four-line trust-boundary repair, not an I02 semantic rewrite. It deliberately does **not** claim protection against arbitrary co-resident Python using `object.__setattr__`, code injection or private introspection; those remain outside the explicitly assumed in-process trust boundary.

## 4. Executes, attempted falsification and proof grade

- [New B R4 sourcefree workflow run #43293333773](https://github.com/maidiu/rawlsing/actions/runs/43293333773) reports failure with **0 executed steps / no assigned runner**, exactly the infrastructure condition already affecting #965. The repository-level B R4 new negative, the 60k A hostile cases, the 88 B inherited cases and first-reader suite have **NOT BEEN EXECUTED at B R4 SHA**. Do not report pytest PASS or RED for this code.
- The old [B original 88/88 green](https://github.com/maidiu/rawlsing/actions/runs/43278005794) remains proof only of B R1's exact older SHA, not this A2/A3/B4 descendant.
- No actual 100k source-direct I02 construction, peak scratch/process-tree-RSS, whole pipeline 6GiB, production original35 issuer or independent G5 has been executed.
- Self-adversarial check: exact-root type may reject a legitimate custom subclass, but the production builder creates the base dataclass; no legitimate requirement to issue source authority via arbitrary overrideable roots was found. The full certificate still uses unbounded legacy `C11LogicalRelease` and `ReplayManifest.closure_refs`; root-type repair does not address that. Other possible in-process tampering via private access is not upgraded into a new speculative work gate. Existing semantic sidecars, event negative/routing/weights, and native evaluator code were not changed.
- The new test's own downstream assertion remains provisional until a runner executes; a local primitive cannot be claimed as proof of native changed/restore semantics. On a functioning executor run the exact inherited native suite and new B R4 test, including the authorized positive.
- A's semantic-root and physical-root commitments remain distinct; no physical root issuer or current permission was invented.

## 5. Original G1–G5 and STOP decision

| Gate | B R4 status |
| --- | --- |
| G1 complete source-qualified I02 semantic and provenance | **PARTIAL** — v1 inherited; source-direct fully bounded M01–M18 not built |
| G2 real first-consumer change/restore | **PARTIAL** — inherited older green; R4 new first-reader case NOT_RUN |
| G3 hostile refusal/completeness | **PARTIAL** — exact root-persona failure primitive reproduced, code/test committed, native case NOT_RUN |
| G4 resources, custody, recovery | **PARTIAL** — #965 closure Python heap fix independently corroborated, full source-direct & process-tree absent |
| G5 independent nonauthor receiving | **NOT_RUN** |

**Full packet disposition remains `REVISE_EXACT_DEFECT`, not `ACCEPT_SCOPED`.** Current source of inability to prove new source/test behavior: GitHub Actions runner fails before steps; current source of inability to close *full S2-B*: missing genuine bounded **source-direct** M01–M18 certificate without compulsory legacy `closure_refs`.

## 6. Fresh Agent A challenge

1. Falsify this B4 exact-root discipline with a **legitimate** normal root issuer or demonstrate an actual native query false result that survives the new exact-root refusal. Do not cite arbitrary private Python mutation as if it were an admissible external caller capability.
2. Execute the entire inherited and B4 native sourcefree court on an available runner; any red is a precise repair, not a new review programme.
3. **Address the shared architectural error:** B and A have repeatedly strengthened a **derived** certificate from full legacy I02 while original S2-B explicitly requires a new source-direct bounded M01–M18 validation. Establish sourcefree candidate input ABI (Pair 1 S1-B/E), preserve typed negative, authority, replay/occurrence/alias and source closure; remove the mandatory legacy `ReplayManifest.closure_refs` tuple; show complete actual sourcefree certification, root/consumer change/restore and measured resource behavior.
4. Once original G1–G4 are really proved at scoped grade, stop the duel and send the frozen SHA to nonauthor G5. No additional speculative permission-work, original35 issuance or protected merge.

**Conclusion:** R4 leaves a narrowly stronger codebase, all corrected A work preserved, and one newly identified root identity boundary closed at source. No false statement of native GREEN or entire-packet completion.
