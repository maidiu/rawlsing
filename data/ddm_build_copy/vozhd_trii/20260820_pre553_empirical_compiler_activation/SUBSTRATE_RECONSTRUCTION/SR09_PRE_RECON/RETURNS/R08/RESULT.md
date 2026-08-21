# SR09-PRE R08 — South Asia raw-source reconnaissance

Status: `COMPLETE__NON_DISPOSITIVE_RECONNAISSANCE`  
Branch: `agent/vozhd-trii-sr09pre-r08-south-asia`  
Starting HEAD: `491a2394e323c904128ca425ef9e793e33ca0d5d`

Token: `PRE553_SR09PRE_R08_SOUTH_ASIA_RECON_COMPLETE`

## Holding

The two exact South Asia snapshots are physically readable under the frozen SAV information boundary and expose **no new hazard class**, but they cannot share a naive family-level code/missing/routing law. Later certification needs source-specific hostile fixtures plus explicit documentary authority for respondent identity, geography, routing, semantic response states, weights/design, topology and cross-wave equivalence.

This return is reconnaissance only. It does **not** certify either source or infer semantic runtime states from labels.

## Frozen source identity

| source | bytes | SHA-256 | rows | vars | cells | ordinary | system missing | user missing |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| South Asia Wave 1.sav | 595,974 | `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571` | 8,442 | 68 | 574,056 | 553,061 | 6,387 | 14,608 |
| South Asia Wave 2.sav | 894,051 | `6a5329ea16f4546188167edd691e0e6adbeae0737a015470aa26df0e01206f22` | 10,617 | 73 | 775,041 | 758,778 | 16,263 | 0 |

Both were extracted only from the frozen Library `surveys.zip` after the bundle matched 158,180,333 bytes and SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`. Both member hashes matched before probing and remained identical afterward.

## Precise cross-wave result

### 1. Identity and coordinates

Wave 1 exposes no evident native respondent-ID variable in its 68-variable dictionary. Wave 2 adds `resno`, but the field cannot serve as hard replay identity: 2,487 rows are system-missing, exactly the Pakistan block, and among the 8,130 present rows only 1,403 distinct `resno` values occur. Even `(ccode,resno)` has 6,927 rows participating in duplicate pairs/groups. Rows 54 and 90 both have Bangladesh `ccode=1,resno=1` but visibly different response content.

Country coding also drifts rather than merely extending. Wave 1: Bangladesh=1, India=2, Nepal=3, Pakistan=4, Srilanka=5. Wave 2: Bangladesh=1, India=2, Maldives=3, Nepal=4, Pakistan=5, Sri Lanka=6. Wave 2 defines Maldives in the dictionary but contains zero code-3 cases. Raw numeric country codes therefore cannot be pooled across waves.

### 2. Missingness is structurally incompatible across waves

Wave 1 contains 14,608 realized SPSS user-missing cells across nine variables, plus 6,387 system-missing cells. Wave 2 declares **no** SPSS user-missing values at all and instead contains 16,263 system-missing cells across ten variables.

The decisive hostile pair is Wave 1 code `8` labeled “No opinion”: it is ordinary storage in `b7` (1,518 rows) but a declared SPSS user-missing value in `c12` (2,742 rows). The same wave therefore disproves family-wide inference from code or label. Wave 2 intensifies the warning: DK/no-response/refusal-like codes `8/9/98/99/998/999` are ordinary observed values because no user-missing declarations exist.

### 3. Routing/module clues are physical, not semantic authority

Wave 1 `c10ai` is labeled “(If yes) Which party?(India)”. All 6,387 non-India rows are system-missing; all 2,055 India rows are non-system-missing, with 98/99 preserved as user-missing codes. This is a strong routing fixture, but the prior “If yes” condition still requires questionnaire authority.

Wave 2 has country-perfect missing masks: `resno` and `GBC31a/b/c` are system-missing on all 2,487 Pakistan rows; `GBC27`, `z15d`, and `z15i` are system-missing on all 1,945 Nepal rows. `GBC32` is system-missing on only 476 Nepal rows. Its label says “(If answered for GBC31)”, yet those 476 cells overlap **zero** rows where all three GBC31 slots are system-missing. Missingness alone therefore cannot reconstruct the printed routing logic.

Wave 2 also contains unlabeled ordinary `-1` values with country-perfect blocks: `GB7a=-1` on every Bangladesh row; `GB7b/e/l/m`, `GB29`, and `GB30` on every Nepal row; `GB7f` on every Nepal and Pakistan row. No semantic meaning is inferred from those patterns.

### 4. Ordered topology exists without SPSS MR-set metadata

Neither file declares an SPSS multiple-response set. That absence is only a physical metadata fact. Wave 2 nevertheless has explicit ordered topology in three adjacent variables: `GBC31a`, `GBC31b`, `GBC31c`, whose labels name the **First**, **Second**, and **Third** most important problem. Row 1 contains `33,4,2`. Certification must retain slot order and cannot impose `(respondent, canonical_question)` scalar uniqueness.

### 5. Schema and code drift are pervasive

Wave 1 has 68 variables and Wave 2 has 73. Their exact **and case-folded variable-name intersection is empty**. Recurrent concepts therefore require explicit mapping rather than name reuse.

Several exact examples are high-risk:

- **Religion**: Wave 1 `d10` and Wave 2 `z10` ask the same question but reuse codes for different religions (`1: Buddhist -> Hindu`, `2: Christian -> Muslim`, `3: Hindu -> Christian`).
- **Education**: Wave 1 `d3` uses coarse `0..8` plus user-missing `9`; Wave 2 `z7a` expands to `0..17,20,99`, with `99 No response` ordinary.
- **Democracy satisfaction**: Wave 1 `c12` code 8 is user-missing “No opinion”; Wave 2 `GBC26` code 8 is ordinary “D.K./Can’t say” and code 9 ordinary “No response”.
- **Media frequency**: Wave 1 uses five substantive frequency points; Wave 2 uses four differently bounded weekly categories.
- **Institution trust**: the core battery recurs, but membership changes and Wave 2 introduces country-block `-1` values.
- **Locality and household assets** show reusable core codes but changed physical applicability/missingness, so even stable values need wave-specific state fixtures.

### 6. Unicode and file metadata

Both files explicitly declare UTF-8 and required no compatibility encoding override. Wave 1 has zero non-ASCII variable/value-label strings. Wave 2 has ten, including U+2019 RIGHT SINGLE QUOTATION MARK in DK/can’t labels and U+2013 EN DASH in `z7a` education labels. Exact Unicode preservation is therefore a Wave 2 hostile fixture.

The SPSS extension surface also drifts: Wave 1 contains subtypes `3,4,11,13,16,17,18,20`; Wave 2 contains `3,4,11,13,16,18,20`. This is metadata drift, not a semantic defect.

### 7. Weight/design

Both SAV headers report weight index 0, and neither dictionary exposes an evident weight/PSU/stratum/cluster/design candidate by name or label. That does **not** authorize an “unweighted survey” conclusion. Official methodology remains required for estimand/design authority.

## Full-scan rationale

Both compact sources were fully traversed after metadata-first inspection. The user-authorized R08 mission specifically demands a near-complete two-wave comparison; exact row/cell conservation, user/system-missing realization, `resno` collisions, country masks, ordinary semantic-like code frequencies, ranked-slot observations and hostile row ordinals cannot be established from metadata alone. No other survey source was scanned.

## Output surface

- `SOURCE_BURDEN.csv`: 34 measured burden rows.
- `HOSTILE_SENTINELS.csv`: 32 exact replay fixtures (11 Wave 1; 21 Wave 2).
- `CROSS_WAVE_DRIFT.csv`: 30 near-complete family drift rows.
- `AUTHORITY_GAPS.csv`: 13 unresolved documentary authority rows.
- `PROBE_RECEIPT.json`: exact transport/probe/publication receipt.

No production runtime, database, source byte, or Library artifact was modified.
