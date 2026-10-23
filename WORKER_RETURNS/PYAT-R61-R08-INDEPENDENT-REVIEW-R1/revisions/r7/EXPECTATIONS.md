# R61-R08V R7 independent review — frozen EXPECTATIONS

Frozen and committed **before** reading R7 candidate code, candidate test code,
or author R7 conclusions. UTC freeze: 2026-10-23T22:29:36Z.

Reviewer: existing DISTINCT session `ses_e962f7b5effeIc4B6gtfbZNHvh` (not author
`ses_e98c8dfe6ffewNYOqJpvqK21a6`), OpenCode DeepSeek V4.1-Flash MAX/Global,
same user-selected account. No new sessions, Codex workers, subagents, provider,
model or account. Same-account role/session/worktree separation is not
credential, institutional or OS independence. Python `/usr/local/bin/python3`.

Stable worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`
(folder suffix historical). Successor branch:
`agent/opencode-pyat-r61-r08v-r7-independent-review-r1`.

## Custody pins for this review

- Sealed R7 commission: `747656253811b1915b994a1fb316dff214655ef5`;
  blob `04e03acc63fdd6a270c11acfb1873f7be2b5b007`.
- Binding R61AF decision:
  `e349da0d886d8e365648afccf40a2e6b8e105ff7`;
  `R61AF_R08_CANONICAL_CACHE_DESCRIPTOR_DECISION.md` blob
  `0efd5777ed6cc81374b741d15a91a8551ad08f39`.
- Binding R61Q decision: `99222514afbac4fc1671dbc90f02b210e6c1f6ce`;
  decision blobs `9bd5d27634bc9afdbd0e4bde03ff0a2ca87a51dc` and
  `1ae5ebe1eb61635a7867a1fba659dfb5ef6ab93e`.
- Frozen precode R7 contract: `c6c6a2e5c...`;
  `revisions/r7/CONTRACT.md` blob
  `92e2f2d226a2676c9d110ccc379504242f337008`.
- Candidate/startup: `ea39bd324d297a93bb9e87ede9b9da75dfa8750a`.
- Candidate code commit: `992236d245e165dcf5842411ad0a4733433fd7de`.
- Candidate module blob: `00312f84afa5677c94193cefd94cdfd951f05222`
  (`rawlsing_next/pre553_universal_evidence_binding.py`).
- Candidate test blob: `0dae12308157735f188bc11163a224229563d8a4`
  (`rawlsing_next/tests/test_universal_evidence_binding.py`).
- Fixture identities blob: `ae96c7a37051d8715e1e93cedac889243c300c8a`;
  harness sitecustomize blob `4a90fc79230232a59443902ee92b3668626dda99`.
- Prior R6 review: `c42b4abee4e54340659ec6b1f8f6760dfbef9411` — primary
  regression/oracle; R5 review `4a5d9a9f8...` and R4 review `d1baa92...`
  remain preserved. R6 oracle and artifacts unchanged.
- Native owner pins to reverify, not edit: provider
  `23167aa25291fb148b1e3cf210ac33fe7769b783`, composition
  `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`, positioned evaluator
  `62e5eced47b64512f47b004e3e13a6ef3fe21de7`, empirical objects
  `a61365b994e5c3c50de0f598fcf40e90abf757b6`, AT07/n10e fixture
  `0e384f72fa615dc72a0dcb08a36472a64b7b1e4a`.
- Reviewer writes only
  `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r7/`.
  Candidate/native/archived oracle/HQ/other node/original data/CI/prod edits are
  forbidden; probes/mutants/evidence stay in this ownroot.

## Fixture/harness custody verified before freeze

The author return contains extracted fixture copies because the sparse originals
are absent. I independently verified, against candidate startup `ea39bd...`:

- all five extracted fixture files match their declared SHA256, byte size and Git
  blob, and each Git blob equals the original repository blob:
  - R2 `02_VALUE_RELATION_ORACLE.json`: `c6acafae...`, 14199 bytes,
    SHA256 `b8a29223...`;
  - R2 `03_SYNTHETIC_AUTHORITY_FREEZE.json`: `333989fa...`, 16335 bytes,
    SHA256 `ae159afe...`;
  - R2 `04_SLICE_PROJECTION.json`: `8e5bd3d2...`, 7195 bytes,
    SHA256 `bab72ceb...`;
  - R3 `02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json`: `5d1583dc...`, 12394
    bytes, SHA256 `838c76dd...`;
  - R8 `04_CURRENT_AT07_IDENTITY_SPINE.json`: `462bb282...`, 5683 bytes,
    SHA256 `a4416c48...`.
- `harness/sitecustomize.py` only rebinds `R2_RELATION`, `R2_AUTHORITIES`,
  `R2_SLICE`, `R3_AUTHORITY`, `R8_SPINE` on the native fixture modules to the
  extracted fixture root. It does not patch implementation, evaluator, provider,
  native semantics or expected oracle values.
- The same native code and inherited fixture bytes must be used; the initial
  setup failure is facility evidence, not product qualification.

## Inherited position and review question

R6 was REVISE because a parallel serialized `producer_binding` record could
contradict the signed owner identity and propagate a forged admission token
through import/re-export. R61AF settles one canonical read-only transport
descriptor, no live admission in cache, and a shared checked projection. R7
claims cache schema @5 / descriptor @1. These are claims to test, not
assumptions.

The review question is the configured trusted-host callable grain: can an
untrusted subject, with full source visibility, all public constructors/methods/
factories, a legitimate cache, and the SAME configured verifier/reader/exporter,
obtain admitted support, a forged ownership/capability record, or a wrong served
value through the canonical descriptor? R7 passes only if the SAME consumers
serve a genuine independently pinned native positive and every in-scope owner
field mutation/removal/duplicate/type-alias/order/unknown/admission attack
refuses or serves only the original authenticated normal form.

## Frozen normal form

- Cache schema `R61_AUTHENTICATED_EVIDENCE_CACHE@5`.
- Owner descriptor schema `R61_CACHE_OWNER_DESCRIPTOR@1`, top-level entry key
  `cache_owner_descriptor`.
- Exactly six descriptor fields: `schema`, `request_key`,
  `owner_identity_material`, `owner_identity_hash`, `validated_conditions`,
  `descriptor_hash`. `descriptor_hash` covers the preceding five fields,
  excluding itself; it is an integrity/canonicalization aid, never a signature
  or live binding hash.
- Thirteen owner classes, exactly:
  1. `context_ref`
  2. `context`
  3. `actual_conditions`
  4. `producer_query_ref`
  5. `predicate_ref`
  6. `predicate_hash`
  7. `release_refs`
  8. `consumer_query_ref`
  9. `consumer_binding_fingerprint`
  10. `model_rule_hash`
  11. `source_universe_ref`
  12. `risk_set_ref`
  13. `target_ref`
- No duplicated top-level owner fields; no admission field/token in the
  descriptor or new-format cache. Compatibility views, if any, must be derived
  from the one canonical owner projection at each use; never stored/imported as
  independent authority. Unknown fields/schema ambiguity refuse at cache/entry/
  descriptor/envelope owner boundaries. Diagnostic metadata may exist only in a
  separately named nonauthoritative area excluded from ownership/capability
  decisions and export promotion.
- `request_key` equals the fully verified request K; `validated_conditions`
  equals its exact ordered typed conditions; owner material/hash equal the
  signature-verified envelope; native query/conditions/consumer/rule semantics
  remain exact. A signed owner hash does not excuse inconsistent duplicated
  envelope fields.
- Legacy @4 and prior caches explicitly typed-refuse; no automatic migration.
  Nonempty legacy `trusted_binding_hashes` explicitly typed-refuses cache
  operations (`LEGACY_BINDING_PINS_REQUIRE_MIGRATION`), never silently ignored
  or reinterpreted. A separately named `trusted_descriptor_hashes` may restrict
  @1 read-only descriptors on export/import/replay; existing live binding_hash
  meaning is unchanged.
- No live producer admission token travels in the new descriptor. Import/
  re-export must not mint, resurrect or propagate a live admission, issuer,
  configured callable or trusted root. Replay of an already signed execution
  works under the configured verifier without a live admission.

## E1 — Custody, scope, manifest, remote

- Candidate/startup, code commit, module/test blobs, fixture identities, harness
  and native owner blobs must equal the pins; branch must be the R7 reviewer
  branch at candidate `ea39bd...`; working tree clean at freeze.
- Candidate delta must be exactly the two R08 code/test paths plus the author R7
  return root; the precode contract/fixtures/harness are part of the author
  return and may exist there. No native owner/evaluator/archived oracle/HQ/
  other-node/config/source/science edit.
- Author R7 manifest independently recomputed for every listed artifact,
  explicitly self-excluding; any mismatch/omission/self-inclusion is a defect.
- Author 126 tests are regression evidence, not independent proof. Independently
  recompute code/test/import pins and actual exits/skips.
- Final reviewer commit non-force-pushed on the successor branch; exact final
  SHA directly read back from origin.
Falsifiers: wrong startup/branch/blob/fixture/harness, out-of-scope delta, false
manifest, unreachable remote SHA.

## E2 — D1 no implicit admitted authority

- `EvidenceResolver()` / default construction with no host configuration must
  not accept an admission root, produce SUPPORTED, authenticate cache or serve
  admitted values. Request/bind/resolve/import/read must yield typed
  UNKNOWN/unresolved or explicit configuration/integrity refusal.
- No fallback public key, module singleton, shared test authority, source-derived
  secret, request/cache-selected verifier or data-supplied root. Empty/no-op
  import is not support.
Falsifiers: unconfigured/default route returns SUPPORTED or authenticates cache;
request/cache chooses verifier/root/key; fallback source-visible authority.

## E3 — D2 live producer permission versus read-only record

- Trusted setup pins the canonical owner context/recipe from independent fixture
  authority and the actual admitted producer callable. Bind/resolve checks exact
  owner/context, typed conditions, source/release, query/predicate, risk,
  role/direction/design/currentness, consumer/model identity and actual
  conditions.
- Live execution requires a non-null configured admitted producer callable
  identity. Missing pin must not execute a substituted callable (counter 0);
  copied legacy admission cannot authorize live work.
- New-format cache carries no admission token. A corrupted/inserted admission
  field/token must typed-refuse, not be ignored or resurrected. Import/re-export
  cannot choose/rotate root, producer, issuer or configured callable; no new
  signing capability.
- A verifier-only resolver may replay/re-export retained authenticated
  descriptor/objects but cannot execute a new producer.
- Unknown/copied-to-another-context/mutated/wrong-scope/wrong-root/wrong-key/
  retired admission material refuses. A producer permission is not a
  measurement and not a cache-transport credential.
Falsifiers: forged context plus matching request yields SUPPORTED; substituted
callable executes with pin omitted; new-format cache carries live admission;
import grants live execution/root; default lazily admits subject input.

## E4 — D3 complete signed result and canonical owner descriptor

- A SUPPORTED/authenticated result carries the versioned signed envelope binding
  full K; context/owner/recipe; source/release; provider receipt/fact refs and
  states; evidence complete content/ref; consumer query/model identities;
  evaluator result/hash; eligibility/execution/result axes; uncertainty;
  denominator/cells/values; trust domain/version/grade. Original execution
  provenance/mode remain signed; no unsigned result provenance is used as a
  trusted current-execution label.
- One checked owner projection returns a deeply detached canonical descriptor
  after signature/K/object/association validation. Export/import/read/replay
  share it; no forked whitelist.
- Descriptor hash and all associations must be recomputed and verified;
  descriptor hash is not a signature. Envelope-owner duplicate disagreement,
  swapped signed envelope/owner/K/source/query/rule, post-construction deep
  mutation and extra unknown duplicate owner fields refuse.
- No raw `_binding_materials` copy is transport truth; no parallel authoritative
  duplicate owner fields.
Falsifiers: descriptor omits/duplicates/mis-associates an owner class; unknown
fields accepted; raw binding propagated; signed metadata does not match served
object; descriptor hash trusted as signature; unsigned provenance becomes a
trusted execution label.

## E5 — D4 real consumer pin, qualified reader and local delivery

- The actual productive consumer verifies the envelope/descriptor against the
  SAME pinned trust domain. A caller-created result with self-consistent
  evidence/evaluator hash must not acquire admitted provenance.
- Qualified result-only reader without trusted delivery context reports
  UNKNOWN/unspecified local transport; it must not report fresh live execution
  merely because a public result field says so. Either omit the unsigned
  `local_delivery_context_unsigned` from qualified output or derive a separately
  named label from trusted resolver/reader execution context.
- Original execution provenance/mode remain signed and authoritative; local
  delivery must not overwrite them or claim a new original execution.
- Attacker-owned resolver/reader with its own root is a separate case; do not
  count it as compromise or positive.
Falsifiers: direct fabricated result passes; local label falsely live; unsigned
result provenance treated as trust; association-only read presented as qualified;
attacker-owned resolver conflated with real one.

## E6 — D5 cache, verifier-only chains, cold, legacy and pins

- Full chain: actual live pin/producer -> signed values -> export -> verifier A
  import/read -> re-export -> verifier B import/read, plus fresh-process cold,
  preserving original envelope/signature/signed provenance and 54/6/60, with no
  new producer permission, signature or grade.
- Import/read/re-export stores only detached authenticated descriptor/objects
  and signed execution; no live admission/issuer/root/callable propagation.
- Same/cross-source corruption, omitted provenance, status edits, K/source/
  edition/clock/design changes, evidence re-signing with attacker key,
  query/model substitution, swapped/copied envelopes, re-sealed aliases and
  deep nested mutations refuse generically.
- Wrong root/no verifier/missing config; legacy @4/older schema; admission-
  bearing new format; nonempty legacy trusted_binding_hashes; optional
  trusted_descriptor_hashes mismatch all typed-refuse honestly. No silent ignore
  of configured pins.
- Cache cannot reinstall selected root, choose/rotate producer/issuer, widen
  scope or upgrade an association grade. Key/config delivered separately via a
  recorded trusted fixture channel, never committed/logged/argv/cache.
Falsifiers: chain/cold not 60; signature/provenance not preserved; import grants
live capability/root/issuer; legacy silently upgrades; configured pins ignored;
wrong root accepted; key leaks.

## E7 — D6 compatibility and unchanged meaning

- Legacy duplicated transport/admission format is explicitly incompatible; no
  silent acceptance as canonical. Version changed cache/descriptor; preserve
  historical artifacts/readback. Descriptor hash must not reuse live
  binding_hash meaning; trusted_binding_hashes not silently reinterpreted.
- Preserve actual provider/evaluator 54/6/60 and changed 54/16/70; VALID_NULL,
  DIFFUSE, VALID_EMPTY, OBSERVED_ZERO, ZERO_SUPPORT, UNKNOWN, Z UNRESOLVED16;
  typed bool/int/null; condition/order/currentness; eligibility/execution/result
  separation; zero-zero vs missing.
- All-refuse is not completion. No scientific estimand, source permission,
  minority-discovery intent or F6/F7 method change.
Falsifiers: legacy silently upgrades; descriptor hash confused with binding
hash; status/typed/Z semantics change; all-refuse success; positives not exact.

## E8 — Mandatory thirteen-class descriptor mutation inventory

Build a table-driven independent mutation inventory from the declared 13 owner
classes, not only `producer_query_ref`. For every class independently:
mutate; remove; add a duplicate/compatibility field; type-alias (e.g. string vs
int/bool/null where applicable); reorder where semantically ordered
(`actual_conditions`, multi-entry `release_refs`). Recompute the public
descriptor hash and entry seal, submit through import -> read -> re-export ->
second import; the SAME configured verifier/reader/exporter must refuse or serve
only the original authenticated normal form. Each attack gets a pristine cache.
Also test:
- unknown descriptor/cache/envelope owner fields and forbidden admission;
- diagnostic metadata not promoted;
- descriptor hash self-exclusion/canonicalization;
- request_key/validated_conditions exactness;
- envelope-owner duplicate disagreement, swapped signed envelope/owner/K/source/
  query/rule;
- deep post-construction nested evidence/query/rule mutation with individual
  isolation and original restoration values (cell 6, not 60);
- optional descriptor pins and legacy pin migration;
- no live producer/root/issuer from import;
- local delivery label honesty.
Every attack must be assertion-level mutant -> refusal/failure -> restored
positive. No exception/setup error counted as integrity proof; no blanket
all-refuse.

## E9 — Native actual consumer and semantic preservation

Independently count forward 54/6/60 and changed 54/16/70 from the pinned
source-free fixture rows and actual unchanged provider/evaluator. Use the SAME
configured consumer and exercise source/receipt-dependent output. Preserve
typed/status/currentness/observed-zero/ZERO_SUPPORT/all-missing Z UNRESOLVED16.
Baseline -> meaningful mutant refusal/failure -> restore PASS at assertion level.
Restore evidence cell to its original 6, not 60. Isolate query/rule attacks.

## E10 — Prior review probes and accounting

Re-run R6/R5/R4 probes through ownroot semantic adapters preserving the same
invariants. The removed duplicated transport field cannot be counted as lawful
refusal unless the SAME assertion is adapted to the new canonical descriptor.
Account for every outcome/skip/setup failure; preserve initial setup failure as
facility evidence, not product qualification. Author 126 tests are not
independent proof. No TypeError/import/setup failure as safety.

## E11 — Verdict and artifacts

Return `ACCEPT_SCOPED_LOCAL_TRUSTED_HOST_ADMISSION_AND_CONSUMER_BINDING` only if
E1-E10 are fully justified at this exact callable grain. Otherwise return
`REVISE` with the exact minimal missing function and all partial/unrun
obligations honestly preserved. Full live J42/P41/E04 integration remains
NOT_REACHED. No source/science/prod/CI/N11/N12/Sorok/J52/W52/R03/R09 or
adoption/author wake. All original35/1890/globalF6F7F8 holds preserved.

Required artifacts in the new r7 ownroot: `EXPECTATIONS.md`, `00_RETURN.md`,
`defects.md`/`limits.md`, independent probes under `probes/`, assertion-level
outcomes under `outcomes/`, JUnit XML under `junit/`, exact commands/exits/skips,
`proof_witness.json`, explicit self-excluded `SHA256manifest.json`, `RESUME.md`,
and logs.
