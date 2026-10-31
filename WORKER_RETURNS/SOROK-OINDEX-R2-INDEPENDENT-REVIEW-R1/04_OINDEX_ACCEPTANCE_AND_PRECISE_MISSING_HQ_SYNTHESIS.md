# O-INDEX acceptance and precise missing HQ synthesis

## Decision

**`REVISE_PRECISE_DEFICIENCIES`**

The primary-source correction is verified. The candidate is not yet a qualified
source-exact, whole-program navigation substrate. The deficiencies below are
specific and finite; this is not a request for another global recovery campaign.

## What is accepted at source grade

- Both `05_PROGRAM_MAP.md` versions are exact Git objects with 17/17 S0–S16
  headings, questions and outputs; both are `ACTIVE_EXPLORATORY_PROGRAM_R1`.
- The corrected S rows carry the exact current and earlier commit/path/blob.
- The source correction successfully overturns R7’s S0–S16 source-absence
  conclusion while preserving R7’s other findings.
- The intact corrected validator passes its 9 tests and reports 144 Sorok rows,
  23 Pyat rows, 4 assets, 189 nodes, 431 edges, 3 traversals and 40 slots.
- R6’s 39/94/133/26/9 grain and the four assets’ candidate-only status are
  represented without pooling or native promotion.
- No permission, native science, PRE-MAIN adoption or priority decision was
  fabricated.

## Defects that prevent acceptance

### 1. The validator does not bind source evidence to Git

`validate_index.py` checks non-S rows only for a 40-hex commit, a non-empty path,
and a metadata timestamp. It does not require a blob, does not resolve the path,
and does not compare the blob to Git. Demonstrated:

- `A5` with real commit `5fc1d43e…`, `path=FORGED/NOT_A_SOURCE.py`,
  `blob=1*40`, and a fabricated `first_consumer` returned **PASS**.
- Non-empty forged `source_cut_metadata.timestamp` returned **PASS**.
- `PYAT_N11` path/blob forgery under a real commit returned **PASS**.
- A forged metadata path returned **PASS**.

This violates the claimed source-exactness and fails the required
“source-to-consumer path without actual source evidence” negative.

**Required correction:** for every Sorok and Pyat row, resolve
`commit:path`, verify its object type and blob/tree identity, verify the
metadata timestamp against Git, and require evidence for the actual
`first_consumer`/edge. Add tests for all eight required mutations, including
metadata and claimed-consumer paths.

### 2. Source evidence contains three unresolved paths and five null blobs

- `B3A` path `candidate/integration.py` is absent; actual candidate path at
  `8bd4d6b…` is under `WORKER_RETURNS/SOROK-20261018-B3-X3-ATOMIC-ADMISSION-REPAIR-R1/`.
- `B3AS` path `candidate/integration.py` is absent; actual path at `16f15a12…`
  is under `WORKER_RETURNS/SOROK-20261018-B3A-SCHEMA-READSET-REPAIR-R1/`.
- `S39_S52` path `s52/session.py` is absent; actual path at `c821b488…` is
  `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/session.py`.
- `B1`, `B2`, `B3`, `BP2P4J` have null blobs; actual blobs are known and must be
  filled.
- `R15_V2` points to a directory/tree, not a file blob; the record must state
  tree identity explicitly or point to the actual file preimage.

**Required correction:** use exact repository paths and object identities, or
mark the row `SOURCE_IDENTITY_INCOMPLETE` with a typed hold. Do not let a source
claim pass on a title or citation document alone.

### 3. S5, S7, S11, S13, S14, S15 are not product-traversable

The exact source questions/outputs are present, but the graph collapses them
into generic `L1_GOVERNANCE`:

- S5 flourishing: governance + person, no flourishing/health/normative node.
- S7 player praxis: governance + person, no feedback/privacy node.
- S11 UX/UI: governance + person, no UX/accessibility node.
- S13 monetization: governance only, no revenue/incentive node.
- S14 safety/privacy/abuse: governance only, no safety/abuse/privacy node.
- S15 alpha/evaluation: governance + person, no alpha/evaluation/human-evidence
  node.

All six are `L1_GOVERNANCE.member_ids`; none has a specific L0 outcome, L4
consumer, traversal, or per-workstream owner slot. The only relevant HQ slot is
the aggregate `S0_S16_SOURCE` adoption question.

**Required correction:** add the specific product/consumer/owner mapping needed
for HQ to deliberate these workstreams, or explicitly declare them
`SOURCE_DEFINED_UNMAPPED` and exclude the index from claiming a complete
whole-product traversal. Do not leave them as generic governance links.

### 4. Stale counts and proof epochs

- `00_START_HERE.md` says 188 nodes/414 edges; actual 189/431.
- `03...md` says 188/414 and “17 S0–S16 holds”; actual 189/431 and 17
  source-defined workstreams.
- `05_VALIDATOR_AND_READBACK.md` says 188/414, seven tests, six mutations, and
  points to old `VALIDATION_RESULTS.json`; actual 189/431, 9 tests, 8 negative
  mutations, fresh run.
- `claim_epochs.s0_s16` is `R7_EXACT_HOLD` while corrected S rows are
  `POST_SOURCE_CORRECTION`.

**Required correction:** update all counts, test/mutation counts, proof epoch,
and stale “holds” language to the corrected candidate. Do not cite old
`VALIDATION_RESULTS.json` as proof.

### 5. Current PRE-MAIN is one intake ahead

The candidate records `5fc1d43e…` as current PRE-MAIN. At review, the refreshed
remote is `87755f02…`, three Pyat S6/H1/PE intake files ahead. The S0–S16 map is
unchanged, but the index’s currentness label is stale.

**Required correction:** record the candidate build cut separately from the
refreshed current PRE-MAIN and state the exact equivalence/non-equivalence; do
not automatically rebase or mutate.

## What is not a defect

- The 17 S0–S16 source definitions are not missing.
- R6’s 39/94/133/26/9 source close and nine unwired material families are
  retained at their actual grain.
- R7’s F1CR missing-bytes, reconstruction, ZIP-container and historical
  negative findings remain valid; only its S0–S16 absence conclusion is
  superseded.
- CP-A5-R2, C9C12-R2, B-F1CR-R2 and V3CORE-R1 remain author-tested, unadopted
  sourcefree candidates; their test counts are not native/person acceptance.
- No scientific issuance or priority selection is required to fix the index.

## Finite HQ synthesis gate

After the five corrections, HQ can use the index as a source-exact overview
substrate. Until then:

- Use the primary Program Map for S0–S16 obligations.
- Use R6/R7 and the four asset returns for their declared sourcefree evidence.
- Do **not** rely on the current graph as a complete S0–S16/product traversal.
- Do **not** treat validator PASS as proof of source path/blob identity.
- Do **not** use the index to rank priorities or adopt any asset.

This remains `HQ_JUDGMENT_REQUIRED`; it is not a new implementation roadmap.
