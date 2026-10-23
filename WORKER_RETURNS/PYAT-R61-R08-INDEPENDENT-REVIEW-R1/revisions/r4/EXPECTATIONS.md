# R61-R08V R4 independent review — frozen EXPECTATIONS

Frozen and committed before reading R4 candidate code, candidate test code, or
author R4 conclusions. UTC freeze: 2026-10-23T17:18:54Z.

Reviewer: NEW distinct native reviewer session, not author
ses_e98c8dfe6ffewNYOqJpvqK21a6. Model/account unchanged:
opencode-go/deepseek-v4.1-flash, variant max, existing user-selected account.
Same-account role/session/worktree separation is not institutional independence
or proven OS isolation. No subagents, no additional sessions, no provider/model/
account change. Python /usr/local/bin/python3.

## Custody pins for this review

- Director/commission tree: 9307abc2a9a4177fc8964496334e74694f8ba711.
- Commission blob f393439a3535fd032384cac11d56557c445d9202
  (R08V/r4/00_COMMISSION.md).
- Binding engineering decision 99222514afbac4fc1671dbc90f02b210e6c1f6ce;
  decision blobs 9bd5d27634bc9afdbd0e4bde03ff0a2ca87a51dc and
  1ae5ebe1eb61635a7867a1fba659dfb5ef6ab93e.
- Author repair commission 5fce75ffd2690261b637e0d88bde8e8adb91eb5a; blob
  b0668688e00b54c0dcf75d760a092aa8f2254b50.
- Frozen precode trust contract 07d94592af4773afb7fa01cdde1f605d820b44f4;
  blob 1576d615b8d3a8353df13070a5413c73cd5333a9.
- Prior terminal R3 review 5b7e338086cd86a9a011c1e911a2b85b9170239f; return
  blob e2d191ca1ac720d3268c20d29276b3b23a8b4282.
- Candidate/startup: 48a2eaf6d3c653e2efe40643c427f28c47cd744b.
- Candidate code commit: 3c69a13e64dd2bca65858906a367347e895f9d82.
- Candidate code blob: c3b039fd908c20b6494a2bcf37b89d878dfaf6c6
  (rawlsing_next/pre553_universal_evidence_binding.py).
- Candidate test blob: 1f72a428283eb35d7bcedf5391528dbcbd22a489
  (rawlsing_next/tests/test_universal_evidence_binding.py).
- Native owner pins to reverify, not edit: provider
  23167aa25291fb148b1e3cf210ac33fe7769b783, composition
  604c8d591d4cc2b646e9b149cdb233fc9d69cf6b, positioned evaluator
  62e5eced47b64512f47b004e3e13a6ef3fe21de7, empirical objects
  a61365b994e5c3c50de0f598fcf40e90abf757b6, AT07 fixture
  0e384f72fa615dc72a0dcb08a36472a64b7b1e4a.
- Reviewer branch: agent/opencode-pyat-r61-r08v-r4-independent-review-r1;
  worktree /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4.
- The only legitimate candidate delta from 84704f4a7 is 3c69a13e6 touching
  the two R08 allowlist paths, plus 48a2eaf6d adding author r4 artifacts.
  Reviewer writes only WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/
  revisions/r4/; .r61/r4/ is reviewer scratch evidence only.

## Inherited position and independent obligations

R3 was REVISE because the default resolver used a source-visible public
admission authority whose public issue_producer/issue_evidence factories could
mint a forged full context and re-sign forged evidence accepted by the actual
consumer. R4 claims a trusted host configuration, trusted execution envelope,
and verification-only ingress. These are claims to test, not assumptions.

The review question is the configured trusted-host callable grain: can an
untrusted subject, with full source visibility and all public constructors/
methods/factories, obtain admitted support through the SAME preconfigured real
consumer for material it chose or mutated? R4 passes only if the SAME consumer
both serves a genuine independently pinned native positive and refuses every
in-scope subject-controlled substitution at the public interface.

## Trust scope fixed before attack

- Trusted host/supervisor: a separate privileged setup operation, performed
  before and independent of subject traffic, pins one immutable trust domain:
  verifier root/configuration, accepted owner/context recipe, admitted native
  producer callable/identity, and the signing/attestation capability.
- Trusted execution authority: may issue admissions only for the exact admitted
  owner/context and may attest only a result it actually produced by invoking
  the admitted provider and unchanged evaluator. Its issuance entry points must
  not be reachable from subject-facing request/binding/result/cache APIs.
- Subject-facing resolver/consumer: accepts untrusted request, binding, result,
  and cache bytes. It exposes verification only: no accepted signing secret,
  no key export, no root/configuration mutation, no arbitrary-payload signing
  oracle. A verification-only object must not expose accepted-root signing or
  key-export methods usable from the resolver/reader path.
- Canonical owner recipe/inputs and the actual native producer/evaluator come
  from the pinned source-free AT07/n10e fixture authority and the unchanged
  native owner modules, not from the author test helper as sole oracle.
  Independently calculate the expected positive values from that fixture and
  the unchanged evaluator. The canonical forward case expectation is yes=54,
  no=6, denominator=60; a genuinely changed valid native case must be computed
  independently and must serve its own values, not merely reuse 54/6/60.
- Out of scope and excluded, not used to excuse a public defect: private-state
  reflection, monkeypatching trusted host code, deliberate trusted-root
  replacement by the host, ptrace/root, same-UID secret/key inspection, a
  dishonest competent issuer, and an attacker-owned resolver/reader configured
  with its own root. Such an attacker-owned resolver does not prove or disprove
  the behavior of the preconfigured real consumer; isolate that distinction
  explicitly.
- In scope: source reading, all public data types and constructors, legitimate
  exported cache/producer entries, caller-created issuers with matching ids,
  self-consistent forged owner/context/K, mutation/re-seal/re-sign of public
  input/result/cache objects, callable substitution proposals, and any publicly
  exposed accepted-key issuance/signing factory.

## E1 — Custody, scope, manifest, and remote identity

- Candidate/startup, code commit, code/test blobs, and native owner blobs must
  equal the pins above; branch must be the reviewer branch at 48a2eaf6d.
- The candidate delta must be exactly the two allowlisted code/test paths in
  3c69a13e6 plus author r4 report artifacts in 48a2eaf6d. No native-owner,
  evaluator, archived-return, HQ, workflow, config, lockfile, old-return or
  source/science file may be edited.
- Author manifest must be independently recomputed for every listed artifact,
  explicitly exclude itself, and match byte-for-byte. Any mismatch, omission,
  self-inclusion, or unreproducible claim is a defect.
- Final reviewer commit must be non-force-pushed on the reviewer branch and the
  exact final SHA must be directly read back from origin.
Falsifiers: wrong startup/branch/blob, out-of-scope candidate diff, false or
self-including manifest, unreachable final remote SHA.

## E2 — D1 no implicit admitted authority

- `EvidenceResolver()` / default/implicit construction with no host
  configuration must not accept an admission root, produce SUPPORTED, or serve
  admitted values. Request/bind/resolve must yield a typed UNKNOWN/unresolved
  or explicit configuration refusal; cache import must fail closed with a
  typed integrity/configuration refusal.
- There must be no fallback public key, module singleton authority, shared test
  authority, source-derived secret, request/cache-selected verifier, or
  data-supplied root. Missing configuration is a refusal, not an empty success.
- A no-op import or an import that only checks its own self-seal is not
  productive support.
Falsifiers: unconfigured/default route returns SUPPORTED or authenticates cache;
request/cache chooses verifier/root/key; fallback source-visible authority.

## E3 — D2 owner/recipe pin, producer identity, permission != measurement

- At trusted setup, the canonical owner context and admitted recipe are pinned
  from independent fixture authority. Bind/resolve must check full K and exact
  owner/context: source, dataset, wave, edition, byte digest, instrument,
  units, estimand, weight, design, uncertainty, direction, role, consumer use,
  grammar, custody, observation/reference/as-of/publication clocks, permission,
  query/predicate, risk, currentness, consumer/model identity.
- The actual producer callable must be selected from trusted configuration or
  an admitted registry; a callable stuffed into an otherwise matching untrusted
  binding must not be invoked or authorized. A module/name/hash label alone is
  not code-load proof.
- Admission issuance must validate the exact producer authority/token/owner
  relation and configured admitted recipe. Unknown, copied-to-another-context,
  mutated, wrong-scope, wrong-root, wrong-key, retired/unadmitted material must
  refuse. A legitimate producer permission must not permit arbitrary new
  measurement issuance or certify a caller-supplied result.
- The public subject-facing resolver/verifier/reader/export APIs must not expose
  accepted-root signing, arbitrary signing, or key export. A public issuance
  factory reachable by the subject is a defect even if named TEST_ONLY.
Falsifiers: forged context plus matching request yields SUPPORTED through the
real consumer; untrusted callable substitution executes; copied producer
permission certifies altered evidence/result; accepted-key signing/key-export
reachable from subject API; default setup lazily admits whatever subject offers.

## E4 — D3 complete executed envelope and D4 real-consumer pin

- A SUPPORTED/authenticated result must carry a versioned canonical completed-
  execution envelope whose signature covers at least: full K/material hash or
  identity; context and actual owner/recipe identity; source/release; provider
  receipt and fact refs and applicable states; complete evidence content/digest
  ref; consumer query and model-rule identities; evaluator result/hash; separate
  eligibility/execution/result axes; uncertainty; denominator/cells/values read;
  trust-domain/version/grade. Internal identities must agree with the envelope,
  not merely verify a different retained envelope.
- Only the trusted execution path, after actual provider and unchanged evaluator
  completion/validation, may produce/sign this envelope. There must be no
  arbitrary input-after-permission signing, no producer/evidence re-issuance
  from untrusted imported records, and no export re-certification of caller-
  forged results.
- The actual productive consumer must obtain its result from the configured
  resolver/executor or verify the envelope against the same pinned trust domain.
  A caller-created EvidenceResult with self-consistent evidence and evaluator
  hash must not acquire admitted provenance; the direct reader route must
  refuse. An association-only helper, if retained, must carry an explicit lower
  grade and must not be the qualified productive path.
- A newly attacker-configured resolver/reader with its own root is not the
  preconfigured real consumer and must be tested as a separate case, not counted
  as either compromise or positive proof.
Falsifiers: envelope omits any required identity/axis; signed metadata does not
match the consumed object; result fields mutate after signing; direct fabricated
result/evidence plus matching hash passes the real consumer; export re-signs
caller data; reader authenticates association only.

## E5 — Genuine independent positive and meaning preservation

- Through the SAME configured real resolver/consumer, using the unchanged
  native provider and unchanged evaluator and independent fixture authority:
  canonical forward positive must be yes=54, no=6, denominator=60, with the
  actual evaluator values read and the same consumer result hash. Independently
  recompute arithmetic from the pinned fixture, not from an author helper.
- A genuinely changed valid native case must execute and serve its own
  independently computed values, proving the consumer is not hard-wired to one
  fixture.
- Cold original positive must reproduce the same value result and same-consumer
  hash in a fresh process.
- Preserve VALID_NULL, DIFFUSE, VALID_EMPTY, OBSERVED_ZERO, ZERO_SUPPORT,
  UNKNOWN, Z UNRESOLVED at denominator 16/all-missing, typed bool/int/null,
  condition/order/currentness, eligibility/execution/result separation, and
  zero-zero versus missing semantics. All-refuse is not completion.
Falsifiers: only hash/marker without evaluator values-read; 54/6/60 not
reproduced; changed case silently reuses canonical values; status/typed/Z
semantics changed; all-refuse presented as success.

## E6 — Hostile controls at the SAME configured consumer

Attack the preconfigured real consumer, not an attacker-owned replacement.
Every attempted attack must end in a typed refusal (not an import/signature/
setup crash counted as safety) or a genuinely changed legitimate result that is
still bound to the same execution.

1. No-config/default/missing-root request, bind, import, and direct reader.
2. Self-consistent forged full context/owner/K plus matching request labels;
   caller-created issuer with matching human id; attacker-selected root/key.
3. Callable substitution in binding/registry/context; a legitimately exported
   producer permission followed by arbitrary payload issuance or measurement
   certification.
4. Same-source and cross-source evidence mutation with re-seal/re-sign using
   subject-available capabilities, including denominator 999, values/cell
   forgery, copied producer admission to another context, wrong-K association.
5. Envelope mutation by each category: full K, owner/context, source/release,
   provider receipt, fact/refs, states, uncertainty, evidence content, query,
   model, evaluator hash, denominator, cells, values, trust grade, version.
   Use public dataclass replace/recomputed self-hash/copy methods and also
   mutate result fields after signature; the SAME consumer must refuse or yield
   a genuinely changed legitimate result, never silently retain the old
   assertion.
6. Direct fabricated EvidenceResult plus self-consistent evidence and matching
   evaluator hash, independent of cache import.
7. Cold/fresh-process: trusted verifier/config delivered separately from cache
   via a recorded trusted fixture channel (stdin permitted); positive replay;
   wrong root, missing config, legacy/schema substitution, cross-request,
   cross-source, same-source 999 must typed-refuse. Cache bytes must not carry
   or install the accepted root/key, choose/rotate configuration, widen
   admission scope, alter producer/measurement provenance, or upgrade an
   association-only grade.
8. Meaningful baseline -> upstream/context/evidence mutation (FAIL/refusal) ->
   restored PASS on the SAME actual consumer, with native call/import identity
   and cold evidence. Also challenge removed failing legacy defaults through
   successor semantic tests, preserve archived originals, and account for every
   omission/skip.
Falsifiers: any hostile route yields SUPPORTED/authenticated values through the
real consumer; refusal is only a crash; mutation leaves the same assertion;
restoration does not restore; cold channel leaks a key or is cache-selected;
legacy/default silently upgrades; skips/omissions unexplained.

## E7 — Cold replay and secret-channel discipline

- Fresh process, fresh native imports, separate trusted verifier/config channel.
- No accepted secret/key/root in committed artifacts, logs, argv, environment
  dumps, or cache bytes. The exact fixture channel and assumptions are recorded.
- Wrong-root cold refusal and missing-config cold refusal are mandatory. The
  cache cannot reinstall the selected root or certify arbitrary material.
- Trusted host authority to approve meaning is not scientific issuance; no
  production/source/science authority is claimed.

## E8 — Compatibility, reach, and verdict

- Legacy implicit-public-key/default caches are intentionally incompatible and
  must typed-refuse; no auto-upgrade into authenticated support. Version the
  changed contracts where needed. Preserve historical evidence/readback.
- Full live J42/P41/E04 maintained integration remains NOT_REACHED and is not
  waived; no archived return may be edited or treated as live. This review
  covers only the scoped local trusted-host admission and consumer binding.
- Original35/1890/global F6/F7/F8, Z UNRESOLVED16, source/science/CI/prod,
  N11/N12/Sorok, J52/W52 holds remain unchanged.
- Return ACCEPT_SCOPED_LOCAL_TRUSTED_HOST_ADMISSION_AND_CONSUMER_BINDING only
  if E1-E7 are fully justified at this exact callable grain. Otherwise return
  REVISE with the exact minimal missing function and honest partial/unverified
  obligations. No reviewer repair, no self-adoption, no author wake.

## Required reviewer artifacts

00_RETURN.md (bounded verdict), defects.md/limits, EXPECTATIONS.md (this file),
RESUME.md, SHA256manifest.json with explicit self-exclusion, proof_witness.json,
independent probes under probes/, assertion-level observations under outcomes/,
JUnit XML under junit/, and exact commands/exits/skips. Only the new r4 reviewer
root may be written.
