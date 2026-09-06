# GT3/GT4 W2 — OBL055 S3 ADP-010 AUTHENTICATION + REPLAY REPAIR R1

## Terminal

`PASS__GT34_W2_OBL055_S3_AUTHENTICATION_REPLAY_REPAIRED__NO_ADOPTION`

This is a bounded successor candidate repair only.

It does **not** adopt OBL055.

The final worker branch tip containing this return and its machine-readable evidence is reported in the worker handoff because a Git commit cannot contain its own SHA without circular self-reference.

## Exact execution boundary

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt34-w2-obl055-s3-authentication-replay-repair-r1`
- exact working-ancestry start: `8f2d13c4ab3c54a82f990fb9b7e384f546949c11`
- immutable instruction ref: `8f2d13c4ab3c54a82f990fb9b7e384f546949c11`
- executed only: `WORKER W2 — OBL055 S3 ADP-010 AUTHENTICATION + REPLAY REPAIR R1`
- W1 in-flight work/conclusions consumed: **NO**
- central moved: **NO**
- PRE-MAIN moved: **NO**
- main moved: **NO**
- self-adoption: **NO**

## Historical S3 preserved exactly

Historical S3 remains failed, noncurrent, and untouched:

- semantic candidate: `5bed04b83f0dc61e500da26130892e46ce9c86ff`
- evidence execution: `c70808c993b7e236e5535a03e22fe89cc3759d1e`
- historical module: `rawlsing_next/v3_adp010_oee_executor.py`
- historical module blob: `cd6e978eea25384482ef2ab75547b8d33bcc4fb7`
- historical original-test blob: `0d29a69e9f88beb72ebfb4ddb85bdb5c40fc74d5`

W2 did not silently convert historical S3 into current authority.

## Successor candidate

Distinct successor:

- semantic candidate SHA: `39e4efc35cec5f1bbb7aafbf165698e6f6cc72ea`
- implementation identity:
  `GT34_V3P5_ADP010_AUTHENTICATED_REPLAY_EXECUTOR@2.0.0`
- module:
  `rawlsing_next/v3_adp010_oee_executor_authenticated.py`
- module blob:
  `54d9acba40f0eb1db8bb03aec3c1bb900f849588`

Successor-specific courts:

- `rawlsing_next/tests/test_gt34_w2_adp010_successor_compatibility.py`
- `rawlsing_next/tests/test_gt34_w2_t3_hostile_closure.py`
- `rawlsing_next/tests/test_gt34_w2_adp010_repair_specific.py`

## Exact repair

The successor closes the T3 blockers at the executor authentication/replay seam only.

1. **Subject ingress authentication**
   - exact subject ref, semantic owner identity, semantic object identity, full materialization receipt wire identity, causal-use permission and provenance are mutually bound;
   - current ingress is accepted only under the exact adopted OBL054 contract:
     - adoption artifact blob `fc46d377dafa5b2c4e274d702e7f26268aa429cb`;
     - materializer `GT34_V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_MATERIALIZER@2.0.0`;
     - accepted-root hash `1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8`;
     - permit hash `3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc`;
   - materializer owner-binding, subject-ref, replay-input and receipt hashes are mechanically recomputed;
   - historical invalid OBL053 root `286ff7b851e920ff2760082d8b2fb194560ab127` cannot authenticate current ingress.

2. **ADP-008 phase authentication**
   - exact phase-state ref and exact phase-state receipt are authenticated;
   - exact accepted ADP-008 authority/registry identity is required;
   - phase authentication is persisted into replay provenance.

3. **Positive applicability authentication**
   - exact applicability authority ID/version/content hash, accepted-authority receipt, exact result receipt and provenance are authenticated;
   - the authentication binding enters candidate replay.

4. **Contact occurrence + independence authentication**
   - exact contact authority identity/acceptance, witness, actor/subject/time/semantic and basis are authenticated;
   - an independently authenticated authority/receipt/basis is required for witness independence;
   - both authentication bindings enter replay provenance.

5. **Anti-laundering**
   - co-location, co-presence, same geography/time, shared endpoint, structural target, institution category, simultaneous resolver selection and narrative plausibility remain insufficient when supplied directly **or wrapped inside purported contact/independence basis**.

6. **Accepted provenance**
   - each record requires exact ADP-010 authority, registry and rule-hash provenance;
   - exact ADP-008 authority/registry and ADP-020 authority provenance are also required.

7. **Source candidate identity**
   - `source_candidate_id` is derived from the exact candidate replay hash and validated.

8. **Reconstructible replay / record validation**
   - candidate material commits every mutable persisted record field other than values mechanically derived from that candidate/record identity;
   - `validate_record()` reconstructs candidate material and recomputes `source_candidate_replay_hash`, `source_candidate_id`, record hash/ID, and event ID/effect;
   - the T3 previously uncommitted-field tampering class now fails closed.

## Preserved S3 semantics

The successor preserves:

- `AVAILABLE -> OPPORTUNITY -> ENCOUNTER` sequencing;
- exact parent actor continuity;
- exact parent subject continuity;
- deterministic canonical identity;
- timezone normalization;
- canonical ref ordering;
- exact replay idempotence;
- ADP-020 core-v1 `ZERO_DRAW`;
- no hidden RNG;
- no `EXPOSURE` API;
- no broader actor mutation;
- direct insufficient-contact rejection.

The canonical `V3OEERealizationRecord` field contract remains unchanged.

## Synthetic/current boundary

All W2 successful fixtures are explicitly:

`NONCURRENT_SYNTHETIC_TEST_ONLY`

The public current executor requires:

`CURRENT_ACCEPTED`

A synthetic fixture cannot masquerade as current OBL054.

W2 did **not**:

- consume or persist W1's current first-canary subject;
- materialize a current first-canary subject;
- execute a current first-canary OEE record;
- claim any synthetic OEE record as current canary truth.

## Governed court

Semantic candidate was frozen before transient court configuration:

`39e4efc35cec5f1bbb7aafbf165698e6f6cc72ea`

Exact evidence execution / checkout:

`12dad53a3a18097de3ea0416f2741bb2bb4c68b6`

GitHub Actions:

- run: `34052025729`
- job: `101537227092`
- conclusion: `success`
- Python: `3.12.14`
- pytest: `9.1.1`
- protocol self-test: `20 passed`
- governed bounded court: `93 passed`
- determinism: `EXACT`
- exact court-spec SHA-256:
  `d18f11a7e14a5a031d2ac2e6da1a00120dc2e8e4f99fcdbd93e70e7857ac9a43`
- receipt artifact ID: `9994828958`
- receipt ZIP SHA-256:
  `78135a51cb51dc61fffdaa119003d83ec4aa97fa1329f82a09f8010e1283d18b`

The governed court contained:

- original S3 tests;
- original T3 hostile reproduction probes;
- successor S3-semantic compatibility tests;
- successor ports of every T3 hostile defect class;
- repair-specific OBL054/currentness/replay/anti-laundering tests.

The original historical T3 probes remain historical reproductions of why S3 failed; the W2 hostile-closure suite applies those defect classes to the successor and proves they now fail closed.

## Court cleanup

Transient court configuration was removed after successful execution.

Cleanup commit:

`cd06f1bccb003c1d83064552b5b379154d0d29fb`

Verified after cleanup:

- governed workflow blob restored exactly to:
  `a974469aa1d83514d896e3de591d7618310ca493`;
- transient `.rabochii/court_spec.json` absent;
- successor module blob unchanged:
  `54d9acba40f0eb1db8bb03aec3c1bb900f849588`;
- historical S3 module/test blobs unchanged;
- cleanup tree is byte-for-byte the semantic-candidate tree before this return/evidence is added.

## Authority ceiling

This PASS means only that the exact T3 authentication/replay defects are repaired in **candidate form** and the successor is ready for independent hostile review.

W2 does not:

- adopt or close OBL055;
- create EXPOSURE;
- create a current first-canary OEE fact;
- create comparator authority;
- create PSEPF authority;
- create metabolism authority;
- create CAN-008 authority;
- create V2 authority;
- create positive-V3 actor mutation authority.

## Disposition

`PASS__GT34_W2_OBL055_S3_AUTHENTICATION_REPLAY_REPAIRED__NO_ADOPTION`

Next lawful action is independent hostile review / HQ adjudication of this candidate.

Machine-readable evidence:

`01_REPAIR_EVIDENCE.json`

Exact governed court receipt:

`02_GOVERNED_COURT_RECEIPT.json`
