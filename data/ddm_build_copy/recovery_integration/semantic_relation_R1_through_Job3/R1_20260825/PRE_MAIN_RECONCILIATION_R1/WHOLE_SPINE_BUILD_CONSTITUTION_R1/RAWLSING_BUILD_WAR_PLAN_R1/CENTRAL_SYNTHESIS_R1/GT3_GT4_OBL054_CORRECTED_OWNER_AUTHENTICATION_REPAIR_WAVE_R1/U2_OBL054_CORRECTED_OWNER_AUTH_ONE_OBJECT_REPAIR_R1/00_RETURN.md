# GT3/GT4 U2 — OBL054 CORRECTED OWNER-AUTHENTICATION + ONE-OBJECT PERMIT REPAIR R1

## Terminal

`PASS__GT34_U2_OBL054_CORRECTED_OWNER_AUTH_AND_ONE_OBJECT_PERMIT_REPAIRED__NO_ADOPTION`

## Exact boundary

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-u2-obl054-s2-corrected-owner-auth-one-object-scope-repair-r1`
- starting / instruction ref: `2a797a6421b9c280b96a6742e7db83ae0890d1c0`
- historical S2 semantic candidate: `38257e57bd5e2d862edfcd1efb610c4d15774b37`
- fresh corrected OBL053 adoption blob: `f561765bad4fdad2bbf4591f35fe7f81f8486428`
- semantic candidate: `15002c7f87656d57eb0c56d68942f4b24765d55f`
- evidence execution: `09cc0da92eb047686aecbb68f25d6fed91c9aa37`
- governed court run/job: `34046703322 / 101522919696`
- protocol self-test: `20 passed in 0.07s`
- bounded repair tests: `20 passed in 0.08s`
- court receipt artifact ID: `9993314929`
- artifact zip SHA-256: `27778dbbe751ed644d86cb3e7126db9ca05b64430a2628141d99036f7847cecc`
- OBL054 adoption: NONE
- real first-canary subject_ref materialized: NO
- OBL052 closed: NO
- OBL055 touched: NO
- PRE-MAIN moved by worker: NO
- main moved: NO

## Successor implementation

New bounded successor:

`rawlsing_next/gt34_u2_v3p1_authenticated_subject_materializer.py`

Blob:

`b0cb39a9a975381f3f3b4a03e7e435b2932e89b9`

Materializer:

`GT34_V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_MATERIALIZER@2.0.0`

Historical S2 remains intact in-tree as failed-candidate history.

## Exact accepted root

The successor production path terminates only in the fresh corrected OBL053 adoption:

- adoption artifact blob:
  `f561765bad4fdad2bbf4591f35fe7f81f8486428`
- accepted-root hash:
  `1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8`
- authority hash:
  `867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29`
- semantic object hash:
  `9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547`
- objective-evidence receipt hash:
  `153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c`

Historical adoption blob `286ff7...` fails current-root validation.

Historical invalid authority/object/receipt identities fail current-root validation.

## One-object permit

Exact permit hash:

`3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc`

Permit ID:

`urn:rawlsing:gt34:obl054:one-object-materialization-permit:sha256:3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc`

Scope:

`EXACT_ONE_ADOPTED_OBL053_SEMANTIC_OBJECT_ONLY`

Cardinality:

`1`

The permit binds the fresh adoption root, exact corrected owner, exact corrected object, exact OBL053 objective-evidence receipt, and exact seed/authority provenance refs.

## T2-D01 closure

Historical defect:

`OWNER AUTHENTICATION FAIL OPEN`

is closed.

A caller may still compute the mechanical owner-binding checksum, but that checksum is explicitly transport integrity only.

Production materialization separately requires the exact current permit.

Hostile tests prove:

- unregistered owner + self-consistent owner binding -> rejected;
- caller-created hostile root + internally valid permit checksum -> structurally coherent but rejected as noncurrent;
- historical adoption root -> rejected;
- historical invalid owner/object/receipt identities -> rejected.

Thus:

`SELF_CONSISTENT_CALLER_CHECKSUM != ACCEPTED_OWNER_AUTHENTICATION`.

## T2-D02 closure

Historical defect:

`ONE OBJECT SCOPE ESCAPE`

is closed at the successor adoption grain.

Every production materialization path requires an explicit current permit.

The permit itself names exactly one semantic object.

Therefore:

- direct materialization without permit -> impossible;
- same permit + distinct object -> rejected before subject-ref emission;
- fresh registry instance + distinct object -> rejected;
- alternate permit + distinct object -> rejected as noncurrent;
- registry memory is no longer the cardinality authority.

The registry remains only an idempotent local cache/slot over the stronger permit-level invariant.

## Semantic opacity and identity behavior

Preserved:

- semantic object bytes are treated as opaque bytes;
- no semantic object field is parsed;
- no classifier is emitted;
- no actor/contact/use/encounter/exposure truth is emitted;
- `semantic_owner_transfer = false`;
- `semantic_fields_interpreted = false`;
- no UUID, wall-clock, display-label, filesystem-order or environment input participates;
- deterministic subject-ref identity direction remains:
  `owner + exact object + exact evidence/provenance -> subject_ref`.

The stronger adoption-root/permit authentication is bound into the successor materialization receipt.

## Real subject non-materialization

The governed court did **not** materialize the real first-canary subject.

Successful mechanics/idempotence tests used a private, explicitly:

`NONCURRENT_SYNTHETIC_TEST_ONLY`

shadow root/receipt path.

That private shadow path is excluded from `__all__` and cannot validate as the production current root.

No production receipt or current real subject_ref was persisted.

## Candidate status

U2 is a repaired OBL054 candidate only.

`OBL054 != ADOPTED`

Required next sequence:

1. bank U2 candidate;
2. independent hostile review against T2-D01/T2-D02 and the fresh OBL053 root;
3. only hostile PASS permits HQ adoption of the successor materializer;
4. only after adoption may the exact real OBL053 object be materialized to close OBL052.

## Final

`PASS__GT34_U2_OBL054_CORRECTED_OWNER_AUTH_AND_ONE_OBJECT_PERMIT_REPAIRED__NO_ADOPTION`
