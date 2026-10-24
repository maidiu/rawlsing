# R06 addendum — actual J42/P41 N9/N10W/E04 integration

This addendum extends the frozen CONTRACT after the first N10E-only candidate.
It does not alter the prior contract commit; it records the later actual-joined
consumer adapter and its proof.

## Pinned actual consumer

- J42 packet commit: `f53cb0d2bce52640268c844c398bbd8007d28edc`
- Packet: `WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1`
- Actual providers observed in the returned receipt:
  - `W41_READONLY_SOURCE_QUALIFIED_WORLD@1`
  - `E41_N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0`
  - `P41_GENERIC_POSSIBILITY_SERVICE@1`
  - unchanged E04 `J42_JOINED_E41_W41_P41_PREV3_CONSUMER@1`
- The test materializes the packet from the pinned Git commit in a temporary
  in-worktree directory, runs its frozen build in a fresh subprocess, and loads
  the returned 84-view receipt. It never edits the packet or substitutes a
  dictionary-only evaluator.

## Added API

`JoinedWorldField`, `JoinedWorldSelectionRequest`,
`JoinedWorldSelectedView`, `select_joined_world_view`.

The adapter validates the actual P41/E04 service and provider identities, E41
rows hash, P41/J42 view binding, N9 rules consumed by the E04 structural
dependencies, exact field values, currentness/as-of, unit pooling/transport,
context-vs-structural role, and clocks. It returns a canonical assertion over
actual N9 routes, N10E steps, N10W positioned consumptions and consumer receipt
hashes. It does not create a selected world or re-run a replacement consumer.

## Positive and hostile evidence

Two actual fields, `training_access` and `civil_sanction`, change the same
joined view's E04 structural assertion (`training` / `civil`), and the canonical
view hash changes. A permitted actual clock-mode mutation (`base/TEST_CURRENT`
to `base/HISTORICAL`, `valid_at` 2027-09-01 to 2026-06-01) also changes the
receipt/view hash. Cold replay uses a second fresh build process and reproduces
the exact view, N10E steps and N10W payload.

Hostile controls refuse wrong source rows, fewer than two fields, a context
field promoted to structural, person/household pooling without transport,
unobserved clocks, and revoked currentness; the original then restores.

## Remaining limits

- This is a **permitted clock-mode/as-of temporal mutation**, not an actually
  observed F7 comparison pair of measured waves. The observed-pair positive
  remains NOT COMPLETE and must not be claimed as original F7.
- The accepted R05 candidate learned product is still not the learned input to
  this joined packet. J42 carries its own pinned E04L learned-release
  readthrough. No unrelated R05 evidence is silently joined into J42.
- N9/N10W/E04 are now actually joined and qualified at the pinned historical
  sourcefree packet. Original 35x54/F6/F7/F8, CI/prod, N11/N12, Sorok, J52/W52
  remain not reached. No self-adoption; distinct reviewer required.
