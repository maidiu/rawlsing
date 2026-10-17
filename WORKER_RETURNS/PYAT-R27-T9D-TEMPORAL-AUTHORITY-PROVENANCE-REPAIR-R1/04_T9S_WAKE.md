# R27 T9D — independent T9S review wake

You are the independent T9S reviewer. This wake is a reproduction and attack
surface map, not an acceptance claim. Independent review and HQ acceptance are
separate acts; nothing here self-certifies.

## Identity under review

- Branch: `agent/rabochii-pyat-r27-t9d-native-authority-provenance-correction-r1`
- Sealed startup: `7603c47610c01937e48b07f7fc69531964182911`
- Return: `WORKER_RETURNS/PYAT-R27-T9D-TEMPORAL-AUTHORITY-PROVENANCE-REPAIR-R1/`
- The ONLY source change is `t9b_temporal.py` (real diff:
  `07_REAL_DIFF_T9C_TO_T9D.patch`). The staged native closure (22 files), the
  T9I court, the T9C suite + frozen contract, the author suite + oracle +
  ledger + stored artifact, and the T9R frozen delta/hostiles/vector files are
  byte-identical to their origin bytes (`06_EVIDENCE_FILE_HASHES.json`).
  `staging/phase_b_direct_bindings.py` is new T9D caller code: it performs
  actual candidate calls and rewrites nothing.

## Reproduce

```bash
cd WORKER_RETURNS/PYAT-R27-T9D-TEMPORAL-AUTHORITY-PROVENANCE-REPAIR-R1
python3 -B run_all_t9d.py
```

Each court runs in a fresh process under `guarded_runner_t9d.py` (per-import
git blob SHA-1 NUL-preimage checks, ambient path stripping, plugin autoload
disabled, bytecode writes disabled). Expected counts: T9I 47/1, T9C 52/0,
native 8/0, author 27/1, T9R delta 50/0, T9R hostiles 7/0, T9D own 22/0. The
two failures must be exactly the two historical compatibility nodes named in
`00_RESULT.md`; any other failure is a real defect.

## Attack surfaces worth your own fresh falsifiers

1. **Unused-future authority at other clocks.** The T9R hostile checks
   retrospective 1995. Please probe other clocks/methods: a held product's
   `temporal_key`/`authorized_opportunity`/`opportunity_ids` must not change
   when post-clock waves are added to the archive. Note the deliberate layer
   split: `evaluate(...).temporal_key` + `native_authorization` are the
   SOURCE-side native anchor-group verdict (T9C contract
   `01_SEVEN_DEFECT_CONTRACTS.json` is preserved green through them), while the
   CONSUMER product key in `read_selected_world` and the typed
   `product_observation_status` carry the used-basis/clock determination.
   Probe both layers and judge the split against the commission language
   ("determine permission per actually USED basis/clock, not all archive
   context"; "distinguish native temporal source-grant from actor opportunity
   entitlement").
2. **Entitlement gate.** Empty, whitespace-only or junk `access_grants` must
   never open a route. Check that a present grant on a held/interpolated
   product still opens nothing.
3. **Lag/rupture identity.** Construct lag + rupture + missing-support
   combinations and assert `set(pub_lag_of(x)) <= set(x.basis_wave_ids)` and
   that no qualifier string leaks into any wave-id list.
4. **Duplicate identity.** Duplicate ids across countries, across editions, at
   the same observation year, and duplicates where BOTH copies are admissible.
   All must refuse (`DUPLICATE_WAVE_ID_REFUSED`) before any filter; no
   last-wins rebinding may survive anywhere.
5. **Capability honesty.** Try `SourceGrant` claims with partial fields, empty
   strings, `grant_current` truthy non-bools, and `require_source_grant=True`
   without a claim. Every path must yield explicit UNAVAILABLE/HOLD — never a
   synthesized clearance. Try `archival_known_at_upper_year` below, at and
   above the publication year; the bound must be enforced in both clock modes.
6. **Preservation.** Re-verify the ten original T9I RED assertions are green,
   the .20/.40/.60 arithmetic, and that V553 bytes are untouched. Confirm the
   two historical failures were NOT "fixed" by reopening unsafe routes.

## Explicit non-grants

No original EE12 source pair, no real source bytes, no national inference, no
OC05, no N9, no N11, no N12, no Sorok actor, no V3, no method adoption, no
actor exposure or remembered-exposure claim, no production original issuer.
Boolean revoked/nonrenewed negatives remain boolean-only: effective/discovered
revocation timestamps, historical-entitlement-versus-present-use and dated
archive custody beyond `archival_known_at_upper_year` are still NOT expressible
and are disclosed as such in `02_ARCHIVAL_SOURCE_KNOWN_AT.json`.
