# R61-R08V R6 independent review — frozen EXPECTATIONS

Frozen and committed **before** reading R6 candidate code, candidate test code,
or author R6 conclusions. UTC freeze: 2026-10-23T20:28:41Z.

Reviewer: existing DISTINCT session `ses_e962f7b5effeIc4B6gtfbZNHvh` (not author
`ses_e98c8dfe6ffewNYOqJpvqK21a6`), same DeepSeek MAX/OpenCode/Global harness and
user-selected account. No new sessions, subagents, provider, model or account.
Same-account role/session/worktree separation is not institutional independence
or proven OS isolation. Python `/usr/local/bin/python3`.

Stable worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`
(folder suffix historical). Successor branch:
`agent/opencode-pyat-r61-r08v-r6-independent-review-r1`.

## Custody pins for this review

- Sealed R6 commission: `2ee413f6c86101a5cecabbc6d5b46fe7351fe68d`;
  `R08V/r6/00_COMMISSION.md` blob
  `69515af7696b1ccd5451c9a4bf61aa9bc72bdca3`.
- Binding decision: `99222514afbac4fc1671dbc90f02b210e6c1f6ce`;
  decision blobs `9bd5d27634bc9afdbd0e4bde03ff0a2ca87a51dc` and
  `1ae5ebe1eb61635a7867a1fba659dfb5ef6ab93e`.
- R6 author commission: `d737562873558ce01116f079815b00bdb06416fe`;
  blob `4b4f1086fc89659b231ee6741d617cb0eec6e50d`.
- Frozen precode R6 amendment: `b9076985ec3be2ead1c47a2f754a52f774dfca59`;
  `REPAIR_AMENDMENT.md` blob `93589a1d9c04bf87dddba5a8767a5c195fe1464e`.
- Candidate/startup: `d8a7b4005d23a1e39b35360ca96bf2aef5b9e591`.
- Candidate code commit: `7450b4f389e4a95a85066065dec7acafe83da84d`.
- Candidate module blob: `ad165eba9d04644f4b5ab34cd9e52ea1cf9b0ebe`
  (`rawlsing_next/pre553_universal_evidence_binding.py`).
- Candidate test blob: `576142c525e140fdfcd34af3949b5bf68ff2386f`
  (`rawlsing_next/tests/test_universal_evidence_binding.py`).
- Prior R5 review: `4a5d9a9f8d700cbc5e692401220623df1122e22b`; R5 frozen
  EXPECTATIONS `732404d1bdb53d6eb25618bf806aa9fd68800291`; R5 probes, defects,
  outcomes and witness are primary regression evidence, preserved unchanged.
- Prior R4 review: `d1baa92cb457c30bf6dffb91f23f8cee351de4f6`; R4 oracle
  `4cf30eee34891f269bed95294e3f31ef80c0b2d5` retained unchanged.
- Native owner pins to reverify, not edit: provider
  `23167aa25291fb148b1e3cf210ac33fe7769b783`, composition
  `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`, positioned evaluator
  `62e5eced47b64512f47b004e3e13a6ef3fe21de7`, empirical objects
  `a61365b994e5c3c50de0f598fcf40e90abf757b6`, AT07/n10e fixture
  `0e384f72fa615dc72a0dcb08a36472a64b7b1e4a`.
- Reviewer writes only
  `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/`.
  Candidate/native owners/old returns/HQ/workflows are immutable; probe copies,
  mutant cache/result files and evidence stay inside this ownroot.

## Inherited position and review question

R5 was REVISE because (1) `read()` derived `cache_trust_grade` from unsigned
`EvidenceResult.provenance` and (2) `export_cache()` emitted mutated evidence/
query/rule objects under a valid signed envelope; verifier-only re-export was
also incomplete. R6 claims signed execution provenance/mode, validated exported
objects, and verifier-only re-export from retained authenticated bindings. These
are claims to test, not assumptions.

The review question is the actual configured trusted-host callable grain: can an
untrusted subject, with full source visibility, all public constructors/methods/
factories, a legitimate exported admission/cache entry, and the SAME configured
consumer/verifier, obtain admitted support, a wrong served trust/provenance
label, or a wrong exported evidence/query/model object? R6 passes only if the
SAME consumer and the full cache round-trip serve a genuine independently pinned
native positive and every in-scope public mutation typed-refuses or serves the
authenticated canonical value/material.

## Trust scope fixed before attack

- Trusted host/supervisor pins one immutable domain before subject traffic:
  verifier root, accepted owner/recipe, admitted native producer callable, and
  signing/attestation capability. Configuration is not request/binding/result/
  cache data.
- Trusted execution authority may attest only the complete envelope after the
  actual provider and unchanged evaluator complete. Its issuance/signing entry
  points must not be reachable from subject request/binding/result/cache APIs.
- Subject-facing resolver/reader/verifier exposes verification only: no accepted
  signing secret, key export, arbitrary signing, root/configuration mutation, or
  live producer execution without the configured admitted pin. A verifier-only
  resolver may import/replay/re-export already-authenticated retained cache
  material but may not execute a new producer.
- Canonical owner recipe/inputs and the actual provider/evaluator come from the
  pinned source-free AT07/n10e fixture authority and unchanged native owner
  modules, not author helper definitions as sole oracle. Independently compute
  forward 54/6/60 and changed 54/16/70 from the fixture rows.
- Out of scope and excluded: private-state reflection, monkeypatching trusted
  host code, deliberate trusted-root replacement by the host, ptrace/root,
  same-UID secret inspection, a dishonest competent issuer, and an
  attacker-owned resolver/reader with its own root. Such a resolver is a separate
  case, not compromise or positive proof of the preconfigured real consumer.
- In scope: source reading, all public data classes/constructors/mappings,
  legitimate exported admissions/cache entries, caller-created issuers with the
  same human-readable id, forged owner/context/K, mutation/re-seal/re-sign of
  public input/result/cache/evidence/query/rule objects, alias/copy/mapping
  mutation, callable substitution, and any publicly exposed accepted-root
  signing/key-export/signing-oracle path.
- R01 High adjudication is separate: do not inspect, use, or decide it.

## E1 — Custody, scope, manifest, remote

- Candidate/startup, code commit, module/test blobs, amendment, commissions and
  native owner blobs must equal the pins above; branch must be the R6 reviewer
  branch at candidate `d8a7b400`; working tree clean at freeze.
- Candidate delta must be exactly the two R08 allowlist code/test paths plus the
  author R6 return artifacts under
  `WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r6/`; the amendment
  commit adds only its amendment file. No native owner/evaluator/archived
  return/HQ/workflow/config/source/science edit.
- R6 author manifest must be independently recomputed for every listed artifact,
  explicitly self-exclude itself, and match byte-for-byte. Any mismatch,
  omission, self-inclusion or unreproducible claim is a defect.
- Author 38-test claim is custody/regression evidence, not independent
  qualification. Independently recompute code/test/import pins and actual
  exits/skips.
- Final reviewer commit must be non-force-pushed on the successor branch and the
  exact final SHA directly read back from origin.
Falsifiers: wrong startup/branch/blob, out-of-scope delta, false/self-including
manifest, unreachable final remote SHA.

## E2 — D1 no implicit admitted authority

- `EvidenceResolver()` / default construction with no host configuration must
  not accept an admission root, produce `SUPPORTED`, authenticate cache, or serve
  admitted values. Request/bind/resolve/import/read must yield a typed
  UNKNOWN/unresolved or explicit configuration/integrity refusal.
- No fallback public key, module singleton, shared test authority, source-derived
  secret, request/cache-selected verifier, or data-supplied root. Empty/no-op
  import is not support.
Falsifiers: unconfigured/default route returns SUPPORTED or authenticates cache;
request/cache chooses verifier/root/key; fallback source-visible authority.

## E3 — D2 owner/recipe and live producer pin

- Trusted setup pins the canonical owner context/recipe from independent fixture
  authority, including all K-relevant meanings/clocks/permissions and actual
  native determinants. Bind/resolve checks exact owner/context, typed
  conditions, source/release, query/predicate, risk, role/direction/design/
  currentness, consumer/model identity and actual conditions.
- Live producer execution requires a non-null configured admitted callable
  identity. With the pin omitted, a copied legitimate owner admission plus a
  substituted callable must not execute (call counter 0) and bind/resolve must
  typed-refuse before invocation. A module/name/hash label alone is not code-load
  proof.
- A verifier-only cold/read-only resolver may replay and re-export retained
  authenticated cache but must not execute a new producer. Imported data cannot
  select/rotate root/producer/verifier, widen admission scope, or upgrade trust
  grade.
- Admission issuance validates the producer authority/token/owner/configured
  recipe; unknown/copied-to-another-context/mutated/wrong-scope/wrong-root/
  wrong-key/retired material refuses. A legitimate producer permission is not a
  measurement certificate and must not certify arbitrary caller results.
- Subject-facing resolver/verifier/reader/export must not expose accepted-root
  signing, arbitrary signing or key export. A public issuance factory reachable
  by the subject is a defect even if named TEST_ONLY.
Falsifiers: forged context plus matching request yields SUPPORTED; substituted
callable executes with the pin omitted; permission certifies altered evidence;
accepted-key signing/key-export reachable; default lazily admits subject input.

## E4 — D3 complete signed served-result projection and provenance

- A SUPPORTED/authenticated result carries a versioned signed envelope binding at
  least full K material/hash; context/owner/recipe; source/release; provider
  receipt/fact refs and states; evidence complete content/ref; consumer query and
  model-rule content identities; evaluator result/hash; separate eligibility/
  execution/result axes; uncertainty; denominator/cells/values read; trust
  domain/version/grade.
- **R6 mandatory:** the original execution provenance/mode must be authenticated
  in the signed envelope. The local cache-delivery context must be explicitly
  local/unsigned and must not claim fresh producer execution or overwrite the
  original evidence origin. Every served trust label and every exported
  evidence/query/model object must derive from signed/retained authenticated
  material or typed-refuse.
- Every field exposed by `read()`/`e04_step()` and every productive cache
  import/replay/export result must equal the authenticated canonical projection
  of the signed envelope (or typed-refuse). Supplied result
  `consumer_values_read`, producer receipt/fact/state, uncertainty, query/model/
  provenance/axes, K/context/source/clock/policy/grade/schema, evidence/query/
  rule objects and aliases must be compared by content/identity, not matching
  labels alone.
- Unsigned result fields must never leak through alternate methods, nested
  mappings, `dict` copies, `dataclasses.replace`, aliases or export. Unknown
  fields/schema ambiguity must refuse, not silently serve.
- Only the trusted execution path, after actual provider/evaluator completion,
  may produce/sign the envelope. No input-after-permission signing, no
  re-issuance from untrusted imported records, no export re-certification of
  caller-forged results.
Falsifiers: envelope omits a required identity/axis/provenance/mode; signed
metadata does not match served object; result values or provenance mutate after
signing and the real consumer serves them; direct fabricated result/evidence
passes; export emits altered nested objects; unsigned metadata leaks; old
envelope silently upgrades.

## E5 — D4 real-consumer pin and direct fabricated result

- The actual productive consumer obtains its result from the configured resolver
  or verifies the envelope against the same pinned trust domain. A caller-created
  `EvidenceResult` with self-consistent evidence/evaluator hash must not acquire
  admitted provenance or a qualified served assertion.
- An association-only helper, if retained, must carry an explicit lower grade
  and cannot be the qualified productive path.
- An attacker-owned resolver/reader with its own root is a separate case; test it
  explicitly and do not count it as either compromise or positive.
Falsifiers: direct fabricated result passes the real consumer; caller-created
issuer with matching id passes; attacker-owned resolver conflated with real one;
association-only read presented as qualified.

## E6 — D5 cache, verifier-only re-export, cold trust channel

- Cold replay reconstructs and verifies the complete request/owner/envelope/
  evidence/query/rule relation before the actual evaluator/consumer reads values.
  Pin root/configuration independently of cache bytes; transported cache contains
  no accepted key or root replacement instruction.
- Same-source/cross-source corruption, omitted provenance, status edits, K/
  source/edition/clock/design changes, evidence re-signing with attacker key,
  query/model substitution, old/new schema ambiguity, swapped/copied envelopes
  and re-sealed aliases refuse generically.
- **R6 mandatory round-trip:** live positive -> export -> verifier-only
  import/read -> re-export -> second verifier-only import/read, preserving the
  original envelope/signature and positive consumer result, with no live producer
  grant. Also a cold fresh process with the original envelope/signature and
  separate verifier channel.
- Wrong-root and missing-config cold refusal; trusted verifier/config delivered
  separately from cache via a recorded fixture channel (stdin permitted) with no
  key in committed artifacts/logs/argv/cache.
- Cache cannot reinstall selected root, choose/rotate configuration, widen
  admission scope, alter producer/measurement provenance or upgrade an
  association-only grade.
Falsifiers: cold/round-trip positive not reproduced; re-export requires live
producer authority or loses original signature; wrong root/missing config
accepted; cache chooses root/producer; key leaks; imported data upgrades grade;
cache replay serves unauthenticated values.

## E7 — D6 compatibility and unchanged meaning

- Legacy implicit-public-key/default caches and old envelope/result/cache
  versions are intentionally incompatible and must typed-refuse; no silent
  auto-upgrade into authenticated support. Version changed contracts; preserve
  historical evidence/readback.
- Preserve actual provider/evaluator computation and independent positives;
  VALID_NULL, DIFFUSE, VALID_EMPTY, OBSERVED_ZERO, ZERO_SUPPORT, UNKNOWN, Z
  UNRESOLVED denominator 16/all-missing; typed bool/int/null; condition/order/
  currentness; eligibility/execution/result separation; zero-zero vs missing.
- All-refuse is not completion. No scientific estimand, source permission,
  minority-discovery intent or F6/F7 method change.
Falsifiers: legacy/old envelope silently upgrades; status/typed/Z semantics
change; all-refuse presented as success; 54/6/60 or 54/16/70 not reproduced.

## E8 — R6 generic signed/served mutation matrix (all public paths)

For every exposed field category, use public dataclass/mapping/copy/alias
operations, including deep-nested `consumer_values_read` fields, producer
receipt/fact/state, uncertainty, query/model/provenance/axes, K/context/source/
clock/policy/grade/schema, evidence/query/rule objects, and recomputed unsigned
hashes. Mutate nested evidence/query/rule individually and in combinations. Test
the SAME configured `reader.read()`, `e04_step()`, resolver cache hit, replay,
import and export — not only named probe fields and not a helper. Mix a valid
signed envelope with a different result; swap/copy/re-seal records; mutate after
construction. Every exposed value must equal the authenticated canonical
projection or typed-refuse; no unsigned metadata or state may leak through an
alternate method/export. A meaningful positive -> mutated consumer failure/
refusal -> restored positive on the SAME consumer is required. Do not count
`TypeError`, import/setup failure or a signature crash as typed safety.

## E9 — R5/R4 regression evidence and author supersessions

R5 review `4a5d9a9f8` and its immutable probes/outcomes/defects are primary
regression evidence; R4 review/probes are historical. Reproduce or refute both
R5 defects with the SAME public reader/export/import: (1) unsigned provenance/
grade, (2) unsigned exported evidence/query/rule objects. Reproduce the former
R4 7-pass/2-lawful-failure and R5 probe outcomes; version successor probes inside
this ownroot with proper expected typed refusals/signed values; preserve the
original archived files unchanged and account for every old control, deselection
and skip. The author reports two R5 probe expectations superseded; verify the
actual semantic repaired result, not blanket dismissal. No TypeError/import/
setup failure as proof.

## E10 — Verification/no live producer authority and author claims

- Verifier-only resolver can import/read/re-export retained authenticated cache;
  it cannot execute a new producer. Missing admitted producer pin must be
  fail-closed, call counter 0.
- Independently recompute author 38 tests, manifest, code/test/import pins, and
  actual exits/skips. Author tests are regression evidence, not qualification.
- No new protected-service requirement; declared trusted-host/private-state/OS
  exclusions remain.

## E11 — Verdict and required artifacts

Return `ACCEPT_SCOPED_LOCAL_TRUSTED_HOST_ADMISSION_AND_CONSUMER_BINDING` only if
E1-E10 are fully justified at this exact callable grain. Otherwise return
`REVISE` with the exact minimal missing function and all partial/unrun
obligations honestly preserved. Full live J42/P41/E04 maintained integration
remains NOT_REACHED and is not waived. Original35/1890/global F6/F7/F8,
source/science/prod/CI, N11/N12, Sorok, J52/W52 and R03/R09 holds remain
unchanged. R01 High adjudication is separate and must not be inspected or
decided. No candidate repair, self-adoption or author wake.

Required reviewer artifacts in the new r6 ownroot: `EXPECTATIONS.md`,
`00_RETURN.md`, `defects.md`/`limits.md`, independent probes under `probes/`,
assertion-level outcomes under `outcomes/`, JUnit XML under `junit/`, exact
commands/exits/skips, `proof_witness.json`, explicit self-excluded
`SHA256manifest.json`, `RESUME.md`, and logs.
