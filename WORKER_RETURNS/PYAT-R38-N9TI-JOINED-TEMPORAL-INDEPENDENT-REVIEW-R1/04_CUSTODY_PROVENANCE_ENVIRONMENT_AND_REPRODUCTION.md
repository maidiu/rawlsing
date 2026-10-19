# Custody, Provenance, Environment and Reproduction Commands

## Pins

| Item | Commit | Blob |
|---|---|---|
| N9J target (pin worktree `R38-N9TI-N9J-pin-7628840c4`) | `7628840c4c8e95b320cadc672743355afbe2958a` | — |
| N9J tested head (CI `39173649313`) | `aa6eb4c96…` | — |
| N9J freeze precommit | `8c49333a7` | — |
| T35 target (pin worktree `R38-N9TI-T35-pin-8bfb145f7`) | `8bfb145f7da8a2d5e6c0913919721ad4085b5d85` | — |
| T35 sealed startup | `5064d76b3c58a8225693055a8ec6bb07e216d9b1` | — |
| Review base | `68873526efe5a39a0849aa401666ac997870f156` | — |
| E04 product (R10) | `9c96f201f3530d2dae321201e9a913bb7a61800f` | `06a74caeb…,facf1c869…,2181b832…,b7e568166…,475feb9f9…` |
| N9J adapter (R11) | `257dfaf41be7d2a88c11741851e9dc89363b5386` | `642381bc033aaeef878624bdce71f9f94708043d` |
| T35 adapter (R13 E05R) | `84485d32c0088995f8dc664dc0517b2d27f2563d` | `690790e81854cde363643edc64946ddc63c58dbf` |
| N9C reader (HQ297) | `9ab4a0192b7c951bb0b387637e6c74333246766c` | `03eb46efccadd6880cb34b2e2ac609ffc9b16c59` |
| E03 progressive candidate | `0e0ed50dbce2dd1434d3a3c84b937b9a956adba9` | `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` |
| HQ297 fixture | `9ab4a0192…` | `1a1bec6e2…` |
| T35 product identity | — | sha256 `c4697da7e08a6920d2208e46274a0bab122ecdd334249f6268875625ea2f857b`, 1,099,273 bytes |

Verification method for all blobs: `git ls-tree <commit> <path>` and byte
comparison against the staged copies (reproduced in adversarial t09; the
reader blob `03eb46ef…` is additionally confirmed **absent** at sealed
`5064d76b3`, justifying staged loading). All staged native modules were
independently preimage-checked against the claimed upstream commits before the
courts were run.

## Reproduction commands (neutral environment mandatory)

Ambient `/Users/matthewsmith/Desktop/Rawlsing/pytest.ini` poisons any
pytest run in this workstation; every run used a clean config and no-cache
mode:

```
python3 -m pytest -c <neutral.ini> -p no:cacheprovider -q <suite> \
  --junitxml=<out.xml>
```

with `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1`, cwd at the pinned T35
runtime for Court B driver/subprocess tests.

* Court A repro: 20 passed in 15.981 s (`evidence/n9j-repro-i2.xml`).
* Court A adversarial: 14 tests → 13 passed / 1 failed in 11.635 s
  (`evidence/n9j-adversarial-i2.xml`).
* Court B repro: 41 + 30 + 75 + 37 = 183 passed (cold JUnit files in
  `evidence/`), driver product byte-identical to the pinned artifact.
* Court B adversarial: 13 passed in 87.698 s
  (`evidence/t35-adversarial-i2.xml`).

Run isolation: cold runners and the T35 driver never wrote into the pinned
trees (bytecode disabled, cache disabled, driver output directed to scratch);
pins remained byte-untouched.

## Environment (sanitized)

See `05_ENVIRONMENT_PASSPORT.json`. No network access was needed or used by
any suite; CI artifact retrieval for the N9J run/artifact identity check is the
only external fetch and is recorded as such.
