# PROGRAMMA_DELTA — SOROK P2 explicit interval continuation R1 second narrow repair

**Delta ID:** `SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1`
**Primary repair base:** `7a256ed4873155dfad86faf2464110ee6f1e2ad4`
**Independent closure:** `89b33453eff13d8a3638a97cf516438c42e7af4f` (primary no-auto-help PASSED; two secondary defects REVISE)
**Historical base:** `bdadbc57c2664d3155a97853422e74b6128261f8` (immutable)
**Product base:** `41bf45813fd0adeffd9b54e1306c2022abe96514`

## Delta

- Preserved the independently verified no-auto-help repair: observation remains observation-only, encounters unchanged, and only explicit `do-help` executes a user attempt.
- Renamed public result keys `admission`/`c9` to `admission_status`/`c9_public`; values are unchanged redacted summaries and the accepted projection privacy boundary is respected.
- Fixed `evidence/result.json` census: excluded `__pycache__`/`.pyc`, excluded the result receipt itself, and recomputed deterministic hashes for actual committed files.
- Updated focused tests, README/API wording, CLI receipts and ordinary return consistently.

## Not changed

- No product, vendor, projection, fan-in, later-event, lifecycle, PROGRAMMA working file, global config or protected branch edit.
- Historical `bdadbc57c...` and prior `REVISE` closure `89b33453...` remain immutable.
- Primary repair is independently verified; the new key/census fix is author-tested only. No acceptance promotion, native/human/B/Pyat grant or protected merge.
