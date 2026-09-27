# PYAT HQ118 — I2 M2 LEARNED-PRODUCT RELEASE / RESOLUTION RUNTIME — R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-pyat-hq118-i2-m2-release-runtime-r1`

Exact sealed HQ118 base:

`6cd63ce6cd5bf697f76ff7e62c4681f16c062832`

**AGENT TYPE: SOURCE-FREE CODE IMPLEMENTATION / GITHUB**

## Governing authority

Read:

- `HQ_HANDOFF/LATEST.json`
- `PYAT_CONTROL_ROOM/17_HQD118_M01_AND_LEARNED_WORLD_OWNER_ADOPTION.md`
- `PYAT_HQ118_FANIN_R1/00_HQ_JOIN.md`
- `PYAT_HQ118_FANIN_R1/01_CROSS_EXAMINATION.md`
- M2 return at `35f3a34c63390c94aa361331b4506adfd4783b59`
  - `01_M2_CONSTITUTION.md`
  - `02_RELEASE_IDENTITY_AND_PREIMAGE.md`
  - `03_DEPENDENCY_REPLAY_EXPLANATION_CONTRACT.md`
  - `04_PUBLICATION_RESOLUTION_LAW.md`
  - `05_NEGATIVE_PRODUCT_PUBLICATION.tsv`
  - `06_IMPLEMENTATION_CONTRACT.md`
  - `07_HOSTILE_RELEASE_TEST_PLAN.md`

## HQ118 publication correction

Freeze:

`B5_LIFECYCLE_PUBLICATION_EVENT != M2_RELEASE_CORE != M2_PUBLICATION_BINDING`

M2 `PublicationBinding` is an immutable resolver/locator representation for one exact release.

It does NOT create lifecycle `PUBLISHED` state.

Only the current B5 OBL034 lifecycle owner may govern lifecycle publication/currentness.

## Mission

Implement:

- immutable content-addressed `ReleaseCore`;
- immutable `PublicationBinding`;
- exact `ResolutionReceipt`;
- exact closure objects/refs for authority/dependency/determinant/replay/explanation;
- exact release resolution;
- producer-preserving dereference;
- materialized/virtual representation parity.

Preferred write surface:

- `rawlsing_next/pre553_learned_product_release.py`
- `rawlsing_next/tests/test_pre553_learned_product_release.py`

## Required operations

Implement logical equivalents of:

- `constitute_release(...)`
- `publish_binding(...)` — representation binding only
- `resolve_release_exact(...)`
- `resolve_subject_exact(...)`
- `explain_release(...)`
- optionally exact graph-only `affected_release_refs(...)`

Do not implement lifecycle currentness.

## Required release identity

ReleaseCore must bind exact:

- release contract ref;
- release subject ref;
- subject kind;
- semantic producer contract ref;
- authority closure ref;
- dependency closure ref;
- determinant closure ref;
- replay/reconstruction ref;
- explanation-lineage ref.

Must exclude from release semantic identity:

- mutable path;
- mutable endpoint;
- current flag;
- latest/default selector;
- consumer permission;
- cache state;
- insertion/commit time.

## Required hostile tests

At minimum:

1. same exact preimage -> same release id;
2. constitutive closure change -> new release id;
3. physical relayout/path/endpoint change -> same release core, different publication binding;
4. exact subject required;
5. producer contract mismatch fails closed;
6. incomplete authority/dependency/determinant/replay/explanation closure fails closed;
7. no latest/default/fuzzy/nearest/semver fallback;
8. virtual rebuild parity where claimed;
9. materialized/virtual semantic parity;
10. VALID_EMPTY typed disposition publishes without invented positive object;
11. NONCOMPARABLE/BLOCKED/UNKNOWN/INTEGRITY_FAILURE preserved;
12. no negative-state laundering;
13. no B5 lifecycle PUBLISHED state minted;
14. no current-selection minted;
15. no consumer permission minted;
16. direct producer dereference preserves producer ownership;
17. publication binding cannot resolve a different release;
18. endpoint failover only among bindings to same release;
19. deterministic historical resolution;
20. M1 LearnedEmpiricalDisposition can be an exact release subject in synthetic source-free integration.

## Hard prohibitions

No raw source.
No real-source execution.
No Field Forge mutation.
No lifecycle current-selection implementation.
No semantic adjudication.
No source/carrier retirement.
No architecture/topology selection.

## Return

Own only:

`WORKER_RETURNS/PYAT-HQ118-I2-M2-RELEASE-RUNTIME-R1/`

Return:
- `00_RETURN.md`
- `01_CHANGED_FILES.tsv`
- `02_PUBLIC_API_AND_OWNER_RECEIPT.md`
- `03_HOSTILE_TEST_LEDGER.tsv`
- `04_M1_TO_M2_INTERFACE_RECEIPT.md`
- `05_VIRTUAL_MATERIALIZED_PARITY_RECEIPT.md`
- `06_PUBLICATION_BOUNDARY_RECEIPT.md`

Success:

`PYAT_HQ118_I2_PASS__M2_RELEASE_CORE_AND_RESOLUTION_RUNTIME_SOURCE_FREE_GREEN__NO_LIFECYCLE_PUBLICATION_COLLAPSE`

Block:

`PYAT_HQ118_I2_BLOCKED__M2_RUNTIME_CANNOT_SATISFY_RELEASE_IDENTITY_OR_B5_PUBLICATION_BOUNDARY`
