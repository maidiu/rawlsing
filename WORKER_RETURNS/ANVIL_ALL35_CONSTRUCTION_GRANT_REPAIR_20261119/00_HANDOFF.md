# ALL35 construction grant repair

## Outcome

**Existing active bindings: 2 (SRC04, SRC17).**  
**New materialized grants: 0.**  
**Authorization-pending drafts: 33.**  
**Total sources: 35.**

The 33 held waves now have fully populated construction-only grant-record drafts
in the existing `PYAT_FULL_SOURCE_READ_GRANT@1.0.0` format. They contain exact
source SHA, row/column/byte extent, host, construction-only purpose/consumer,
local retention and no Q2/science scope.

The drafts are deliberately **nonoperative**:

- `draft: true`, `operative: false`
- `currentness: DRAFT_NONOPERATIVE_AWAITING_COMPETENT_DECISION`
- `issuer: NOT_SIGNED`
- `authorization: DRAFT_ONLY__NOT_ISSUED__NO_SOURCE_ACCESS`

The existing accepted resolver check authorizes the existing SRC04 binding and
refuses the nonoperative draft with `GRANT_NOT_CURRENT`. No source was opened,
statted, hashed, or decoded.

## Private/public boundary

Full drafts contain `source_path` and remain **outside Git** under:

`/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil_all35_construction_grant_drafts_20261119`

The public return contains only permissible metadata, hashes, filenames and the
decision packet. The public index does not contain `source_path`.

## Files

- `DRAFT_INDEX.json` — 33 public draft records with exact source identity/hash,
  shape, purpose, consumer, scope, retention and draft SHA; no source paths.
- `DRAFT_VALIDATION.json` — all 33 private drafts mechanically validated.
- `DECISION_PACKET.json` — one concise exact batch decision covering the 33.
- `RESOLVER_CHECK.json` — actual existing resolver authorize/refuse exercise.
- `SUMMARY.json` — counts.
- `assemble_drafts.py` — reproducible builder.
- `MANIFEST.json` — public artifact hashes and source-input pins.

## Existing active record reuse

- **SRC04**: existing exact full-source C11 binding; not reissued, not duplicated.
- **SRC17**: existing exact C11-only binding; I03/I05 excluded; not reissued.

No permission was inferred from custody, filesystem presence, TEST_ONLY
fixtures, stale/superseded material, or another source's consent. No new grant
was signed or issued.

## Shortest remaining consequential decision

**One competent-user decision in the existing Pyat HQ** authorizing the 33
construction-only local C11 records as a batch, with exceptions only if the
competent user names them. The existing historical scheme uses a competent user
decision, not an assumed third-party signer. The decision would authorize no
Q2, analysis, science, export, respondent-row publication or source access
during this commissioning.

No source was read or run; no product, protected, science or new administrative
system was changed.
