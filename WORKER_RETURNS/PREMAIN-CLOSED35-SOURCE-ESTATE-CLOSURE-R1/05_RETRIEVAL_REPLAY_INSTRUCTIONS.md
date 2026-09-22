# CLOSED35 Retrieval Replay Instructions

This replay is deliberately a **three-carrier byte-staging procedure**. It performs no survey decoding or semantic interpretation.

## 1. Materialize the three Library carriers

Use the exact Library identifiers below; do not rediscover by filename.

| role | file_id | library_file_id | Library path |
|---|---|---|---|
| 33-source archive | `file_0000000036e0822f963b9604cb2bad49` | `libfile_cbff8189aca48191bd9701a2433c6d6f` | `/surveys.zip` |
| LiTS-I alias | `file_0000000036dc81f8b8b546e356590a03` | `libfile_b0cc5a20ede8819198699487a5694080` | `/LITS-2006-data.dta` |
| WVS7 archive | `file_00000000386c820d8760e748b25ad7e1` | `libfile_ceec13dc81908191ad3959ac864c691c` | `/WVS Wave 7.sav.zip` |

A later worker should materialize them into a fresh cloud staging directory with collision-safe filenames.

## 2. Verify carrier roots before extraction

Require exactly:

- `surveys.zip`: 158180333 bytes; SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`
- `LITS-2006-data.dta`: 139531180 bytes; SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- `WVS Wave 7.sav.zip`: 26200230 bytes; SHA-256 `ce92993a022edbe39823f4a95d3f33522179ce4f388e2de2c1778c4ae6f1059a`

If any carrier root differs, stop before extraction.

## 3. Stage LiTS-I

Copy the exact bytes of `LITS-2006-data.dta` to the census staging name `LiTS_I.dta`. Renaming is transport-only; do not transform the bytes.

Then require:

```text
size = 139531180
sha256 = 7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09
```

## 4. Extract the 33 surveys.zip members

Extract **only** the exact member paths listed in `03_ARCHIVE_MEMBER_INDEX.json`. Ignore `__MACOSX/` sidecars and the directory entry.

For deterministic shell replay, for each manifest row whose `archive_filename` is `surveys.zip`:

```bash
unzip -p surveys.zip "$archive_member_path" > "$canonical_filename"
test "$(wc -c < "$canonical_filename" | tr -d ' ')" = "$canonical_expected_size"
test "$(sha256sum "$canonical_filename" | awk '{print $1}')" = "$canonical_sha256"
```

The exact member path, expected size, and expected SHA are row-bound in the CSV/JSON manifest.

## 5. Extract WVS7

```bash
unzip -p "WVS Wave 7.sav.zip" "WVS Wave 7.sav" > "WVS Wave 7.sav"
test "$(wc -c < "WVS Wave 7.sav" | tr -d ' ')" = "185163494"
test "$(sha256sum "WVS Wave 7.sav" | awk '{print $1}')" = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
```

## 6. Final estate assertion

After staging, enumerate exactly the 35 canonical filenames from `01_CLOSED35_SOURCE_ACQUISITION_MANIFEST.csv`. For every row require both byte-size equality and SHA-256 equality before a later representation census is allowed to decode anything.

Do not accept a source because its filename matches. Do not substitute another edition. Do not decode during acquisition.

Expected final count: **35 PASS / 0 unresolved**.
