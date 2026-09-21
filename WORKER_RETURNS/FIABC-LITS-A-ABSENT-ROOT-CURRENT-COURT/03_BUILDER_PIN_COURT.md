# Builder Pin Court

## Holding

`92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55` is a stale/malformed live pointer, not an accepted builder object and not a builder succession.

The authoritative qualified builder remains:

- symbol: `R5CompactLongShardedBuilder`
- path: `rawlsing_next/pre553_r5_compact_carrier.py`
- owner: `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`
- Git blob: `92e364b31eaf27be1bca2081eff65f6ffb779c3d`

The owner tree resolves that exact path to `92e364b31eaf27be1bca2081eff65f6ffb779c3d`. Direct Git-object lookup for `92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55` returns 404. No accepted `92e364b31eaf27be1bca2081eff65f6ffb779c3d` → `92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55` succession exists.

## Exact five-pin defect

R35-I02 introduced a malformed runtime pointer set that T6 inherited. Live `_ensure_r5` validates all five files, so all five exact pins must close to the named owner tree.

| Runtime file | malformed live pin | exact owner-tree blob |
|---|---|---|
| `pre553_r5_codec.py` | `72f8e8a2b6b2330332030e3978077c11e38ec8db` | `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540` |
| `pre553_r5_compact_carrier.py` | `92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55` | `92e364b31eaf27be1bca2081eff65f6ffb779c3d` |
| `pre553_r5_model.py` | `62cea85788eb160796642ba09d9f0d41f987a3d43` | `62ce608829c3d9c2fb7c999aefe40188637edf80` |
| `pre553_r5_seam.py` | `cef346fca029fa920db16e83db908d466018f39e` | `cef326ebbc40468428378f7fdbe76e4756179f39` |
| `pre553_r5_single_pass_audit69.py` | `ffb07a9d0bafbf685d27aa1161ce830bcfc810fc` | `ffb063b93c86e215604eecb29a9545c7efdff399` |

The malformed model pin is not even a valid 40-character Git SHA-1. The other malformed pins do not resolve as repository Git objects in the browser court. The exact replacements above are the actual blobs at owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`.

## Repair applied

Source-free branch repair:

- live five-pin map corrected to exact owner-tree blobs;
- top-level LiTS builder pin corrected to `92e364b31eaf27be1bca2081eff65f6ffb779c3d`;
- mirrored derivative-parentage test fixture corrected to the independently qualified builder blob.

No builder code was edited.

No Candidate-A semantic object, source SHA, R5 carrier schema, query/workload, or generic R35 parentage schema changed.

## Hostile/static proof

The source-free hostile court proves:

- none of the five malformed strings remains in the live backend;
- all five exact owner-tree strings are present;
- the current manifest requires measured S01 rather than preserved S01;
- reintroducing `NO_REPEAT_COMPLETED_LITS_A_FIRST_BUILD` fails validation;
- marking LiTS/A S01 `DONE__PRESERVE` fails validation;
- skipping S01 by restoring first-unfinished S02 fails validation;
- relabeling the absent root as present fails validation.

GitHub Actions run `35629679569`, job `106432556473`: **23 passed in 0.21s**.
