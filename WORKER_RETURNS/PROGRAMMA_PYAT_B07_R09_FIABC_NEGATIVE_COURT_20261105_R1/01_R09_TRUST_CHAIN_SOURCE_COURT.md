# B07 / Court A — R09 parent/host-provenance and independently observed bytes

**Baseline:** protected `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`. **Investigated R2 implementation:** `4a10c82aa8ba2a31938d3d35e12dc42f4456264c` (verifier Git blob `7af149e9d0e9cb2bc85c31d370145a86abf078b8`, reported SHA256 `3cf9f5e7d07c110a47fff75c02d4169590060daf24518be95d46ddebf9103b8d`). **Independent review:** `25510c8d84f0ae5e452b301b017bdedf46f40b5c`; `REVISE`. **Facility preflight:** `2d30d98576ffad5da6156a2c03b0080916bf28d2`; `FACILITY_GAP`.

## Authority and threat model

The [original R09 node](https://github.com/maidiu/rawlsing/blob/4a10c82aa8ba2a31938d3d35e12dc42f4456264c/WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R09/NODE.json) names an independent CI engineer and repository administrator, exact candidate+externally pinned policy, sandboxed real owner execution, authenticated event/value artifacts, and independent promotion verification. The [sourcefree R09 commission](https://github.com/maidiu/rawlsing/blob/4a10c82aa8ba2a31938d3d35e12dc42f4456264c/WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R09/00_COMMISSION.md) permitted ONLY local candidate verifier/tests and explicitly excluded protected workflow/admin deployment. [R00P R2](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/PYAT_CONTROL_ROOM/R57_R00P_R2_POLICY_ADMISSION_CODEX_DELEGATED_TECHNICAL_SEAL_AND_PROOF_SIDECAR_R1.md) admitted frozen independent policy content at TEST_ONLY scope; it did not appoint R09 host administrator or issue native CI promotion. [R53 U53A](https://github.com/maidiu/rawlsing/blob/8ffec40a6924848a49f95950aa9ce28c27ee3ec1/PYAT_CONTROL_ROOM/R53_U53A_POST_PREPARATION_RESUME_INSTRUCTION_20261021.md) warns that self-claimed native flags do not prove trusted execution. Neither R00 nor U53A is a substitute for a host protection domain.

Threat model relevant to R09 is a *candidate allowed to run Python inside the observed child*. Such a candidate can mutate its interpreter, import machinery, JSON protocol and loaded-source dictionaries. It need not compromise the parent HMAC key to defeat an observation claim that was authored inside its process.

## Verified code path (read source, not author conclusion)

[Exact verifier source](https://github.com/maidiu/rawlsing/blob/4a10c82aa8ba2a31938d3d35e12dc42f4456264c/CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py):
- In `WRAPPER_SOURCE`, child installs `_CustodyFinder`, a `sys.meta_path` hook, traces frames, evaluates a tree-loaded entrypoint, constructs `payload` from local `execution_status/result/events/loaded_sources/import_events`, writes it via mutable child `json.dump`, and invokes `os._exit(0)`. The latter blocks an `atexit` overwrite, **not** prewrite source/process forgery.
- In `LocalNativeSupervisor.observe`, parent independently obtains candidate commit tree and entrypoint bytes, then **reads child `observation.json`**. It binds each `loaded_sha256` reported by the child against independently retrieved `git show commit:path` expected bytes; if child claims the same digest it marks `tree_bound=true`. It takes child `result` and `events` into a parent-assembled payload and HMAC seals that payload. HMAC protects the post-seal object, not the truth of the child-origin fields.
- `verify_observation` verifies HMAC, exact bindings, event/import expectations and result equality; those checks are real if observations originated from a trustworthy collector. They are insufficient to *create* such a collector.
- The TrustRoot constructor is caller-configurable; absent an externally pinned acceptable issuer identity, two colluding local participants can self-root. This is a separate provenance admission boundary, not proof of D1/D4 repair.

## Decisive hostile probes

| Probe | Attacker-controlled element | Independent observed outcome | Required |
| --- | --- | --- | --- |
| `P1_child_json_dump_forges_result` / D1 | Child support module replaces `json.dump`; real computation `double(add(20,1))=41`, protocol rewritten to 42 | `LOCAL_NATIVE_VERIFIED`, reasons empty, child marker independently shows 41 | Typed refusal; parent-origin actual result |
| `P2_child_forges_loaded_bytes_and_result` / D4 | Child replaces meta-path load from string and inserts benign expected digest into wrapper `loaded_sources` | `LOCAL_NATIVE_VERIFIED`, reports benign `5205ce76375a313ebf4f6235ad6105fa92070fb210f70762b07f85bbf60ff106`; actual executed code returns 41 | Refusal; independently captured executed bytes |
| `P10_non_serializable_expectation` / D7 | Authentic sealed observation + set-valued frozen expected result | `EXCEPTION:TypeError`, not typed refusal | `REFUSE_NATIVE_QUALIFICATION`; sourcefree bounded fix candidate exists |
| `P5_self_root_caller_accepted` | Caller creates its own matching `TrustRoot` | accepted under matching self-authored fingerprint | External issuer/trust-root admission before promotion |

Primary [reviewer defects](https://github.com/maidiu/rawlsing/blob/25510c8d84f0ae5e452b301b017bdedf46f40b5c/WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/defects.md) and [raw probe outcomes](https://github.com/maidiu/rawlsing/blob/25510c8d84f0ae5e452b301b017bdedf46f40b5c/WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/evidence/probes_r2.json). R2 reviewer had 15 cases, 12 reached the expected result, three exposed named defects. It did **not** modify the candidate and did not promote it.

## Sourcefree improvements already valuable; preserve, do not reopen indiscriminately

The [R2 author](https://github.com/maidiu/rawlsing/blob/4a10c82aa8ba2a31938d3d35e12dc42f4456264c/WORKER_RETURNS/PYAT-R61-R09-IMPLEMENTATION-R1/revisions/r2/00_RETURN.md) and later adversarial review corroborate **limited** functional improvements:
- Actual tree-bound entrypoint retrieval and refusal of straightforward worktree/target-outside-tree divergence.
- A valid existing C11 sourcefree positive: `ingest_c11_source_release` → `C11Repository.resolve_release_exact`, with accepted release `REL-R09`, two events and 18 M01–M18 records; a separate plain-process expected result matched, and wrong expected result refused.
- Rejection of bare/unsealed maps, mutated HMAC, fake issuer string in sealed record, missing/outside committed entrypoint, non-durable nonce ledger, and cold/concurrent nonce reuse; tests show one `CLAIMED` and one `REPLAYED`.
- Focused author tests 14 PASS and previously established 48-test oracle receipt: scope must not be inflated to adversarial parent-owned capture.
- D7 candidate branch [repair return](https://github.com/maidiu/rawlsing/blob/da101f1a70ed2ec3aaff80c201c007efe518bb1d/WORKER_RETURNS/PYAT-R09-D7-REPAIR-20261103/RETURN.json) replaces unguarded expected-result `typed_digest` with `safe_typed_digest`, creates `EXPECTED_RESULT_NOT_SERIALIZABLE` refusal, reports 15 tests PASS; still independent-review NOT_PERFORMED and neither D1 nor D4 changed.

## Existing-host capability is a typed owner hold

[Independent finite facility preflight](https://github.com/maidiu/rawlsing/blob/2d30d98576ffad5da6156a2c03b0080916bf28d2/WORKER_RETURNS/PYAT-R61-R09-FACILITY-PREFLIGHT-R1/00_RETURN.md) read permission metadata and code *on its commissioned mainMac*, did not change the host. It found only ordinary UID 501 with controller key files 0600 under that same UID, no separately protected broker principal, no pinned protected native-owner runtime, no broker-origin receipt, and no externally admitted issuer. Docker/Podman/Colima/Lima were not installed in that inspected environment; `sandbox-exec` was installed but not wired/qualified. External CI, remote VM and independent key services are **UNVERIFIED**, never globally `ABSENT`. The controller’s scheduling/grant/custody apparatus is real but cannot certify hostile-proof runtime independence under the same UID.

No privileged host observation was performed by B07. The correct remaining gate is `HOST_PLATFORM_ADMIN_AUTHORIZATION_REQUIRED` plus `R09_CI_ENGINEERING_OWNER_REQUIRED` plus `REPO_ADMIN_PROTECTED_CHECK_ADMISSION_REQUIRED`, not `ENGINE_FAILURE_NO_OWNER`.

## Smallest plausible upgrade and its exact claim

**Owner request (not B07 authorization):** permit a disposable macOS VM or a dedicated non-admin broker service UID and separate candidate UID/process protection; place approved C11 owner modules and **their imported dependencies** at non-candidate-writable pinned snapshot; create broker-only signing key and externally pinned verifier key. Admit only a schema-bounded declarative `R61_R09_BROKER_REQUEST@1`: operations `C11_INGEST_SOURCE_RELEASE`, `C11_RESOLVE_RELEASE_EXACT`; owner code SHA/tree; input and policy SHA; `K`; run/nonce/sequence; actual downstream consumer. Reject candidate-provided call names, source digests and result objects. Broker independently reads exact owner/input bytes, invokes owner in its **own protected interpreter**, captures resulting object itself, emits signed `R61_R09_BROKER_RECEIPT@1`; independent verifier checks issuer, exact bindings, cold replay and independently frozen expected return.

**Critical scope:** this can demonstrate “protected broker executed approved owner operation and returned value X.” It **cannot** simultaneously claim to observe arbitrary internal Python calls of an untrusted candidate running elsewhere. If that stronger observation is required, host-controlled tracing or another subject-inaccessible instrumentation primitive and different threat model are necessary. A container around the same compromised Python wrapper does not fix D1/D4. Parent HMAC over untrusted child JSON never suffices.

**Required falsifiers:** re-run exact P1/P2 against isolated broker so modified child `json.dump`, fabricated `loaded_sources`, wrong owner, wrong policy/input/`K`, issuer spoof, nonce replay and modified code all REFUSE; authentic positive accepted only if broker-protected result and independent expected result match; remove actual result assertion and confirm target positive test RED then restored PASS. Separate repo admin only after such an independently reviewed disposable qualification may consider CI required-check enforcement.

**Current grade:** `HOLD_HOST_OWNER` / `DEPLOYMENT_HOLD`, no new protected runner proof.
