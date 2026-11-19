# SRC16 declared-missing overlay and residual observed cells

## Census received

The authorized aggregate census completed:

- 126 response slots;
- 58,697 unmapped cells;
- 40,592 `FORMAT_USER_MISSING_RANGE`;
- 18,105 `OBSERVED_STORAGE_VALUE`;
- zero missing or duplicate mapped positions.

No new native source scan was performed by this worker.  No raw token or
respondent record was printed, committed, or included in this handoff.

## Declared-missing repair

`common/declared_missing_mapping.py` deterministically reads the completed
private census and the pinned config.  It materializes **only**
`FORMAT_USER_MISSING_RANGE` cells, preserving:

- the exact source missing declaration (`kind=range`, exact `lo`/`hi`); and
- the existing `FORMAT_USER_MISSING_RANGE` physical state.

Each rule uses the existing typed `MISSING` response state, retains the raw
source token, keeps `canonical_value: null`, and copies the exact scalar
occurrence topology.  No authority is added.

Private aggregate coverage replay:

- declared-missing range cells covered: **40,592 / 40,592**;
- exact range rules: **243** across **121** slots;
- observed storage cells left explicitly unresolved: **18,105**;
- remaining unresolved cells: **18,105**;
- other mapped cells touched: **0**;
- coverage replay: **PASS**;
- overlay SHA-256: `3e107fb0fcec7c94a4e50be7b614a6351ced3cca3cd8f836e1e6886fc0f5ce42`.

The overlay itself is private and is not in Git.  The only published values are
counts and digests.

## Observed-value class requiring a decision

Exact class: `PhysicalMissingState.OBSERVED_STORAGE_VALUE`, **18,105 cells** in
126 response slots.  These were not made substantive merely because a raw value
exists.  No rule was added for them; the overlay leaves them unresolved.  This
is the exact remaining mapping decision class.

No source token values were emitted to logs, model context, or Git.

## Synthetic positive/refusal

`synthetic_declared_missing_witness.py` uses synthetic cells only:

- declared range token -> `MISSING` rule: **YES**;
- observed token not made substantive: **YES**;
- observed token not dropped: **YES**;
- no authority expansion: **YES**;
- provenance pinned: **YES**;
- one synthetic positive and one refusal path: **PASS**.

Output: `synthetic_declared_missing_witness.out`.

## Metadata admission and provenance

Base pinned metadata admission still passes through the actual source adapter:

- config file `1106de3e…`, canonical `c26e8e71…`;
- source SHA `e368fc0f…`;
- 1,613 rows / 216 physical / 157 response / 2 coordinates / 0 weights;
- `CURRENT_GRANTED`, no revocation;
- exact source-scope negative cases refused;
- source read: false.

The private overlay records the base config file/canonical hashes, census hash,
source SHA, `authority_expansion: false`, and `source_reopened: false`.
A private candidate config built by appending these 243 rules loads through
`load_source_config` with 157 response slots.  Candidate admission passes; its
file digest is private and is not published.  No source was opened for this
test.

## Remaining state

- 40,592 declared source-missing cells now have exact typed overlay rules.
- 18,105 observed-storage cells remain explicitly unresolved and need an exact
  decision; they are not substantive by existence.
- The private overlay is not yet applied to the public pinned config because it
  is data-derived and must remain outside Git.
- Native SRC16 was not launched or rerun.  No new grant, scope, wave, Q2/science,
  protected write, or DHIKR was added.

## Files

- `common/declared_missing_mapping.py`
- `common/synthetic_declared_missing_witness.py`
- `declared_missing_replay.out`
- `declared_missing_overlay_admission.out`
- `synthetic_declared_missing_witness.out`
- `src16_metadata_declared_missing.out`
- `src16_age_refusal.out`
- `receipt.json`
