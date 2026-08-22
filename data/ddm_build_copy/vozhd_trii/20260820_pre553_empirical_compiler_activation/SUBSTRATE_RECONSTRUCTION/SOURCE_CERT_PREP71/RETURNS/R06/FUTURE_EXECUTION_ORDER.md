# PRE553 SOURCE CERT PREP71 — R06 FUTURE EXECUTION ORDER

Status: `NON_DISPOSITIVE_PACKET__DO_NOT_CERTIFY`

## Universal fail-closed preflight

1. Start from the exact governed future certification HEAD and this R06 packet.
2. Materialize `surveys.zip` from ChatGPT Library only; require bundle size `158180333` and SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`.
3. Extract only the assigned substantive member and require its exact `SOURCE_BYTE_INVENTORY.csv` SHA before any read. Ignore `__MACOSX/` and AppleDouble members.
4. Decoder/config gate: `$FL2`, little-endian layout 2, raw values, SPSS user-missing preserved, labels/dictionaries retained, source-row ordinal retained, subtype-20 UTF-8, **no compatibility encoding override**. Latinobarómetro is not on the frozen compatibility allowlist.
5. Do not consult legacy PostgreSQL as truth. Do not normalize, repair, infer equivalence from names, or convert questionnaire response codes into released SAV storage codes.

## Latinobarometro 1995

1. Require SHA `4b7fc6da17dfddafd6a835717e8dc06981208eb4120fa33bdd16e12ae95926f7`.
2. Replay `LB95_HEADER_STANDARD`: header/dictionary/weight pointer all 203, 9069 cases.
3. Replay row-identity duplicates; hard identity remains `(source_snapshot_id, source_row_ordinal)`.
4. Replay user-missing `region=-7` and ordinary `p33b=98`; preserve physical classes before semantic binding.
5. Replay exact PAIS country counts. **STOP sample-identity closure** if the official 1995 technical record still says Brazil `n=1080` while frozen raw has `PAIS=76` count `1200`. No row may be dropped to make the document fit.
6. Bind questionnaire wording/routing from official 1995 instrument and released storage codes from official 2019 codebook; preserve both layers.
7. Retain `wt` raw and its official Weighting role, but do not invent construction/estimand beyond documentary authority.
8. Only after the Brazil discrepancy is explicitly resolved or governed as a recorded documentary conflict may future source-equivalence assertions proceed.

## Latinobarometro 2011

1. Require SHA `a44e89e08e564e4e175199eeeabfa6163f32f4ba0a19a6c3f5b4752de6cca22e`.
2. Replay header/dictionary/weight pointer all 414 and 20204 cases.
3. Replay exact 18-country counts; require parity with official methodological sample counts.
4. Keep `NUMENTRE` and `(IDENPA,NUMENTRE)` as native attributes/candidate identity only; source-row ordinal stays hard replay identity even though the composite is empirically injective.
5. Replay `P1ST=-2` user-missing and assert the instrument/codebook layer distinction: questionnaire `Q1ST` prints DNK/DNA `0`, while released codebook/raw use negative missing states.
6. Replay WT extrema and preserve country-specific weighting/design documentation without constructing a universal pooled estimand.
7. Replay P2ST as the 2011 “most important problem” semantic baseline.
8. Proceed to exact carrier/C11 equivalence only if every raw state/label/dictionary/topology remains recoverable and no cross-wave rule is imported.

## Latinobarometro 2024 — mandatory P0 first court

1. Require SHA `ff5cef18c87969026e7f993d09f10c38a547bf81d5d398784fb59b960b7b0a40`.
2. **Before any ordinary decoder/canonical work, execute:**

   `python latinobarometro_2024_width_hostile_fixture.py --source <exact-scratch-source> --json-out <scratch-receipt>`

3. Require fixture status `PASS__NON_DISPOSITIVE_PHYSICAL_HOSTILE_FIXTURE` and all of:
   - raw `nominal_case_size=174`;
   - parsed dictionary variable records `=332`;
   - `weight_index=332`;
   - `ncases=19214`;
   - `data_offset=145498`;
   - total decoded values `=6379048 = 19214 * 332`;
   - zero partial-case remainder;
   - compressed EOF reaches exact file size `7886834`;
   - final variable `WT`, zero-based ordinal `331`;
   - raw header hash and header+dictionary hash exactly match the committed receipt.
4. **FAIL CLOSED** if a reader reports/uses 174 variables, if it silently rewrites 174 to 332, if dictionary traversal differs, if source SHA differs, or if the full stream does not end at exact physical EOF after 19214x332 values. The lawful physical representation must preserve both the abnormal header value and the 332-wide decoded incidence.
5. Require raw 17-country counts and the official 2024 technical record’s 19214/17-country sample parity. Treat the generic landing-page “18 countries/territories” phrase as a recorded caveat, not correction authority.
6. Replay user-missing `P14STGBS.A=-4`, ordinary `P56N.1=96`, ranked `P23STM.1/.2/.3`, and source-row identity.
7. Replay `WT=19.7793` and **STOP weight-semantic closure** while official results describe WT as `0.01-10`. Do not clip, normalize, or relabel raw WT values.
8. Replay hostile name drift: 2011/2024 exact shared names cannot map by name; P2ST/P13ST/P19ST must be wave-specific.
9. Bind only documentary mappings explicitly supported by official questionnaire/results/technical records; unmatched Q->P export correspondences remain `UNKNOWN`.
10. Only after both the 332-width hostile court and WT documentary conflict are closed may exact carrier/C11 source-equivalence assertions proceed.

## Negative/fail-closed assertions

- Wrong source SHA => immediate stop.
- Missing Library bundle or wrong bundle SHA/size => immediate stop.
- Any compatibility encoding override for these three sources => immediate stop and HQ review.
- Any dropped user-missing cell, row reorder without reversible ordinal map, label/dictionary loss, or weight clipping => fail source-equivalence.
- Any same-name longitudinal mapping without wave-specific source authority => fail mapping assertion.
- Any attempt to “fix” the 2024 header before recording the original 174 and proving 332-wide traversal => fail the P0 hostile court.
- No future court may emit `CERTIFIED`, `FAILED`, or `BLOCKED` merely from this Prep71 packet; it is preparation evidence only.
