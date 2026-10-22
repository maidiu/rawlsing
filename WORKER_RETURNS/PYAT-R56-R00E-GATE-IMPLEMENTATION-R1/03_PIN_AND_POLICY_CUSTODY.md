# Pinned policy and custody

## Exact pin

- Commit: `6d95a78bf6b7bcf70022e303a151255e65edc38a`
- Policy root: `CROSS_HQ_CONTROL_ROOM/universal_execution_policy/r56_sourcefree_v1/revisions/r2/`
- Contract: `R56-R00P-CLAIM-TRANSITION-GATE@1.1.0`

## Verified Git blobs

| File | Git blob SHA-1 |
|---|---|
| `CONTRACT.md` | `01ccb46475ba09fe868a59c8810a12de1190dc22` |
| `policy.json` | `5f5d0253cfc8e1eef2e452e54bae631c23da378f` |
| `synthetic_universes.json` | `66fdf81f3cb440c36df4cd03dcff8613d1b4928d` |
| `decision_cases.json` | `5608e9c3435042e92d846644aad5404b47d6b2f0` |
| `freeze.json` | `dfc1c375b4a4a7b962156c1ddb46b56b9cb8ee10` |

`load_pinned_policy` recomputes these Git blob SHA-1 values and compares them to `freeze.successor_content_blobs`. The handle is `verified=True` only on exact equality. The policy files were not edited.

## What Git custody is not

Git blob identity proves content custody at a commit. It is **not** a protected signature, KMS attestation, R09 runner or native event proof. A same-user process able to construct a Python object can bypass the class boundary; the candidate JSON boundary is separate. Production/native deployment needs the independent facility and R09 trust owner.

## Expected material

- 18 expected operation objects from `CANONICAL_V1` or `ARC1_BIJECTIVE_Q301_LOCAL`.
- Eligibility distribution: 13 ELIGIBLE, 1 PROHIBITED, 2 HELD, 1 INAPPLICABLE_PROVED, 1 UNKNOWN.
- Original obligations preserved: 35 sources × 54 = 1,890 cells plus global F6/F7/F8, all U/Epre null/unissued.
- `ARC1_BIJECTIVE_Q301_LOCAL` contains the complete full 18 renamed operation objects and the exact label/occurrence/operation bijections; the gate does not infer them from candidate output.

## Readback

Evidence: `evidence/proof_witness.json`, `evidence/imports.json`, `evidence/SHA256SUMS.txt`.
