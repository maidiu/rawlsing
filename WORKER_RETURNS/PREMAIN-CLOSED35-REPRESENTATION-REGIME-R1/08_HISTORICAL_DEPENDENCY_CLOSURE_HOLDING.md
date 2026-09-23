# Historical Dependency Closure Holding

## Census-qualified dependency graph

The authoritative census dependency receipt is PASS and reports:

`ambient_current_dependency_leaks = []`

Classification:

### EXPLICIT_CURRENT_SUCCESSOR_DEPENDENCY

- current R5 codec — blob `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`;
- current physical binding-key owner — blob `8a761119e4a8d68eb291fc4edfadb52e027f8284`;
- current physical decoder — blob `86109c4a0b7ebd9b66e3b531b6334bfb48f03f78`;
- WVS7 representation authority — blob `220c646df5b85eb927af70961c5d05be97edfb73`;
- pinned pyreadstat/readstat representation evidence referenced by that authority.

### HERMETIC_HISTORICAL_DEPENDENCY — key-law scope

For the LiTS accepted historical physical-key comparison the census pins exact commit/path/blob for:

- legacy facade: `0b96b8de...:rawlsing_next/pre553_source_backed_c11_facade.py` blob `7c509c2098d0030f253344eb3f682471378812a8`;
- historical canonicalize/semantic-hash owner: blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`;
- historical missing-state enum owner: blob `13aa733b511dc23e00bfcdf288c5b920e3f09983`.

This holding is deliberately limited to the key-law dependencies actually proven by the census receipt.

### BYTE_IDENTICAL_AMBIENT_DEPENDENCY

None is required by the census-qualified representation comparison. If a future replay relies on one, byte identity must be proved explicitly before it may be so classified.

### ACCIDENTAL_CURRENT_DEPENDENCY_LEAK

Count: **0** in the authoritative census dependency receipt.

## Controlling warning from cloud preflight

Earlier cloud archaeology proved that deploying one historical file and loading it with `importlib.util.spec_from_file_location` does **not** isolate its absolute imports. Historical code can silently consume current `rawlsing_next` dependencies.

Therefore this HQ fan-in freezes a hostile requirement:

> every future historical replay that participates in physical-key or hash identity must capture import/dependency provenance and fail closed when a changed current key/hash dependency enters without an explicit successor authority.

No claim of whole-runtime hermeticity is made merely from the key-law closure above.
