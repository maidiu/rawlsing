# SR09-PRE — LIBRARY RAW-SOURCE INPUT LAW

Status: `FROZEN_LIBRARY_FIRST_RAW_INPUT_AUTHORITY`

Parent authority: `../29_SR09_PREPARATORY_RAW_SOURCE_RECONNAISSANCE_AUTHORITY.md`

## Canonical Library transport bundles

Workers must use the user's ChatGPT Library copies as their raw-source transport input for SR09-PRE reconnaissance.

### Shared 33-source bundle

Library filename: `surveys.zip`

Observed Library size: `158180333` bytes

Observed ZIP SHA-256:

`f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`

The bundle contains exactly the 33 CLOSED_35 raw sources other than WVS Wave 7 and LiTS I, plus non-substantive macOS packaging entries under `__MACOSX/`.

HQ independently streamed every one of the 33 substantive archive members and verified its SHA-256 against `SOURCE_BYTE_INVENTORY.csv` with zero mismatches.

Workers must ignore `__MACOSX/**` and AppleDouble `._*` entries as packaging metadata, not survey sources.

### WVS Wave 7 proving-source bundle

Library filename: `WVS Wave 7.sav.zip`

ZIP size: `26200230` bytes

ZIP SHA-256:

`ce92993a022edbe39823f4a95d3f33522179ce4f388e2de2c1778c4ae6f1059a`

Substantive member:

`WVS Wave 7.sav`

Required member SHA-256:

`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

### LiTS I proving-source bundle

Library filename: `LiTS_I.dta.zip`

ZIP size: `7686379` bytes

ZIP SHA-256:

`b2e90ee7ceefc230572e89687de28186544308949f8fd33c32b1d0ffb14b8feb`

Substantive member:

`LiTS_I.dta`

Required member SHA-256:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

## Worker input procedure

For each family worker:

1. locate the named Library bundle(s) by exact filename;
2. materialize the bundle into worker-private scratch space;
3. verify the bundle byte size and SHA-256 above before extraction;
4. extract only the worker's assigned substantive source members;
5. verify every extracted source member against the exact SHA-256 in the worker order / `SOURCE_BYTE_INVENTORY.csv`;
6. STOP on any mismatch;
7. probe only the verified extracted copy;
8. never write back into, rename, replace, or mutate the Library artifact;
9. record Library bundle filename, bundle SHA-256, extracted member, member SHA-256, and scratch path in `PROBE_RECEIPT.json`.

R01-R06 and R08 use only `surveys.zip`.

R07 uses `surveys.zip` for LiTS II/III/IV and `LiTS_I.dta.zip` for LiTS I.

R09 uses `surveys.zip` for WVS Wave 1/Wave 4 and `WVS Wave 7.sav.zip` for WVS Wave 7.

R10 starts from the accepted SR03 census and the family returns; if a targeted raw probe is required it must obtain the relevant source from these same Library bundles under the same verification law.

## Isolation

Materialization/extraction is transport only. A Library filename or ZIP container is never source identity. The exact extracted member SHA-256 remains the source snapshot identity.

Do not require or assume `/Users/matthewsmith/...` source paths for SR09-PRE.
