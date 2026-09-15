# GT34 OBL055 R3 — EXACT REPLAY-REPRESENTATION SUCCESSOR COMMISSION

## Jurisdiction

`OBL055_ONLY`

`WHOLLY_IN_GRAIN_OBL055_REPLAY_RECONSTRUCTION_REPRESENTATION_DEFECT`

No new semantic authority, cross-campaign authority, or trajectory decision is commissioned.

## Immutable ancestry and authority

- campaign authority branch remains `agent/sub-vozhd-gt34-trii-first-canary-r1`; no rebase is required merely to consume HQ authority.
- HQ OBL056 adoption ref: `9ecae8c4a499dddb364c633b581e9e4d68ad3540`
- HQ authority: `GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY@1.0.0`
- HQ authority hash: `6c9ab99a7d89835e7fdf405511abd7d6d66ced54b6e2fd8ef1863be842f39123`
- HQ OBL056 implementation blob: `49538b9c36e58e19a6dc293ecac5bc2dff58eebe`
- installed registry: `ZERO_POSITIVE`
- frozen W2 candidate: `39e4efc35cec5f1bbb7aafbf165698e6f6cc72ea`
- frozen W2 executor blob: `54d9acba40f0eb1db8bb03aec3c1bb900f849588`
- first acceptance-bound repair blob: `fa169dbb525475c17b2495a5b35aa300aa809881`
- failed R2 replay-reconstruction implementation blob: `eb9c91b705a01868d99d3e3a564b611749e028f8`
- failed R2 court seal: `14a74f3dd59515cb095db2a03bfc4d2743a98a16`
- failed R2 governed run: `34158705781`
- failed R2 governed job: `101855817978`
- failed R2 result: `12 failed, 87 passed`
- failed R2 receipt artifact: `10031848302`
- failed R2 artifact ZIP SHA-256: `85f0fdb75cb59289c7ed4a8878a2d2c7b3c0647dacd5c93434deb2af641b7bf1`

## Exact defect

R2 reconstructs the source evidence objects and reruns the W2 validators, but `_assert_base_binding` compares the JSON-decoded stored OBL056 receipt body directly with `asdict(reconstructed_receipt)`.

The frozen acceptance receipt contract contains tuple-valued fields. Canonical JSON replay turns those tuples into JSON arrays. Therefore the lawful record cannot match its own exact receipt after replay even though the canonical wire content is identical. All twelve R2 court failures collapse to that first causal-use binding mismatch.

## Smallest authorized repair

Create a distinct R3 successor that:

1. preserves W2, R1, R2, and the R2 source-bundle format unchanged;
2. compares the stored and reconstructed receipt at canonical JSON wire grain, so tuple/list round-trip representation is normalized but added, removed, renamed, or mutated content still fails;
3. reruns the same W2 source validators and exact R1 OBL056 acceptance validation;
4. retains distinct contact occurrence/independence roles, authorities, and receipts;
5. retains exact subject, ADP-008 phase, applicability, contact, provenance, candidate, record, and event replay bindings;
6. retains the zero-positive current boundary and all prior authority ceilings.

No positive fact may be invented. No current-positive acceptance may be issued here.

## Governed repair court

The R3 court must include the exact R2/H1 replay attack surface redirected to the R3 successor plus the inherited W2/T3/W4 closure and OBL056 provenance courts.

On PASS: commission exactly one fresh independent hostile review.

On wholly in-grain FAIL: commission only the smallest exact successor repair.

On new authority/cross-campaign/trajectory defect: freeze only that lane and return the smallest HQ packet.

## Hard gates

- `OBL055 = NOT_ADOPTED`
- `POSITIVE_V3_EXECUTION = NOT_AUTHORIZED`
- project-current first-canary OEE = `NOT_AUTHORIZED`
- OBL031 = `BLOCKED_ON_OBL055_HQ_ADOPTION`
- OBL032 = `BLOCKED_ON_OBL031_CENTRAL_CLOSURE`
