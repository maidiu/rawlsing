# SRC17 exact SQLite-free normal operator

Runnable isolated operator for GSS 1973/SRC17 under the exact existing construction-only grant. It reuses the accepted streaming writer/reader; no SQLite proof in the normal path.

## Exact pins

- config: `SRC17.d2_runtime.config.json` file `ef461a36…`, canonical `b865e4ba…`
- grant: `d6272ba6…`; authentication `f7fb429b…`; current `CURRENT_GRANTED`, revocation `NONE_RECORDED`
- source SHA: `59e65801…`
- key slot: ordinal 3, `id`; row-native keys from the same admitted transport using `row_native_keys_from_transport`
- selection: 258 response slots, 21 held response slots, 2 coordinates; 51 continuous and 5 administrative fields are documented exclusions, not new categories/gates

## Commands

```bash
python3 src17_operator.py --mode preflight
python3 src17_operator.py --mode sourcefree --root <fresh-private-root>
python3 src17_operator.py --mode run --work-root <fresh-private-root>
```

`run` performs exact grant admission, one decode, slice/keys, streaming writer and fresh native reader; the controller must execute it, not this metadata-only author.

## Evidence

Sourcefree fixture: 90 identities/events/routing/coordinates, 7 authority snapshots, 0 weights; no `.sqlite` files; progress phases and fresh open recorded. Expanded source/purpose request is refused.
