# D2I — independently checked two-number historical consumer: executable positive at SOURCEFREE_TEST_ONLY, operative HOLD

## Setup and actual run

Host: Python 3.13.5; pytest 9.0.2; git 2.47.3; local writable filesystem PASS. Ran exact command in clean created /mnt/data/d2i_workspace:

    python -m py_compile d2i_sourcefree.py
    python -m pytest -q --junitxml=pytest_receipt.xml
    # stdout: ........................................ [100%]
    #         40 passed in 0.11s
    # exit code: 0

Local source Git blob SHA-1: 0c902b55fed2508d3890e58e3ffae6b2237cd39b.
Local exact official-transcribed documentary fixture Git blob SHA-1: d714ab12157e5d17e8e164c78b260743ebbe09d9.
Local test-suite Git blob SHA-1: ee5dbb188aaad2a013225767fe66b1d8372e18ab.
These are **test artifacts**, NOT official GSS/NCA PDF binary hashes. Upload/readback for these exact files was checked separately against GitHub connector. No repo owner imports, N5/N6 issued fields, issued EE13 or operative OC05 were executed.

The test-only program uses two independently held field records, each bound to the exact official PDF URL, native definition, table-number payload, source observation/publication clock and nonissued permissions. A registry assigns fixture-content SHA256 identities. The reader receives only source refs and historical as-of date, dereferences both rows, computes separate typed output slots and a receipt hash. Request itself carries **no numerical values**.

## Two actual dereferenced outputs (historical publication cut = 2022-07-08)

**GSS_RURAL_LIGHTING**: field ref D2I_TEST_ONLY_FIELD:0ef2f616679ce0efde9e27cd0ed89cbb6f0643a169bcfaaff4df98502b6d1f5c. Data read: 2,388,192 electricity-main-lighting rural occupied units / 3,288,063 rural occupied units = 72.6% published rounded; mains 2,288,193, community grid 74,490, generator 3,640, solar inverter 21,512, wind 357. Native geography GHANA_RURAL; native unit OCCUPIED_DWELLING_UNIT_MAIN_LIGHTING.

**NCA_NATIONAL_DATA_SUBSCRIPTIONS**: field ref D2I_TEST_ONLY_FIELD:19bc9aa38688bf72466a4753b36d6a41be85c0cc8a22e67d3a53cd5d23c70433. Data read: 23,414,527 active national data subscriptions, prepaid 23,237,338 and postpaid 177,189. Native geography GHANA_NATIONAL; unit ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_90_DAY_ACTIVITY; NO unique-person, ownership, or rural conversion.

Returned status TWO_VALUES_DEREFERENCED_TEST_ONLY, as_of 2022-07-08, canonical test snapshot SHA-256 af980cf64a82546fea4481928dca1a86b2b68138fefca190cd5c8f694ba25896. Flags operative_OC05=false, N5N6_issued=false, N7_EE13_issued=false, person_inference=false, correlation=false, model_use=false.

## Clocks, revisions, and source-specific replay

| Documentary as-of | Observed candidate visibility | Grade |
|---|---|---|
| 2021-12-31 | GSS and NCA both NOT_YET_PUBLISHED | REQUIRED_SOURCE_UNAVAILABLE_HOLD |
| 2022-03-01 | GSS visible, NCA not published | PARTIAL_TEST_ONLY_NONPOSITIVE only with explicit partial; no pair-positive |
| 2022-07-07 | NCA still not published | REQUIRED_SOURCE_UNAVAILABLE_HOLD |
| 2022-07-08 | Both published and read into separate slots | TWO_VALUES_DEREFERENCED_TEST_ONLY |
| Replay same fixture, same as-of | Identical immutable value slots, source refs and snapshot digest | PASS |

Controlled **hypothetical test-only** mutation of GSS numerator -1 and mains subtype -1 changes GSS field identity and GSS value slot, while the entire NCA slot is exactly unchanged. Hypothetical NCA total +1 and prepaid +1 changes NCA identity/slot only, GSS exactly unchanged. A newly instantiated registry refuses a retired old ref (STALE_OR_UNKNOWN_SOURCE_REF). Refusal of one source (missing publication or REVOKED_TEST_ONLY) preserves the two attempted-ref readset; full pair returns HOLD, optional partial remains NONPOSITIVE. This exercises dependency-differencing, **not operative B5 owner invalidation** or an actual official corrected edition.

## Reuse and owner import boundary

N9C @ 9ab4a0192b7c951bb0b387637e6c74333246766c has a more general isolated historical two-field reader, previous **47/47** test-only tests and explicit ref/value-read separation. It should be reused for later source-qualified owner development; the D2I court adds independently observed publisher semantics, native geography, source clocks and a 40-test source-specific adversarial adapter. It does not install a second OC05.

Direct pinned code review at launch SHA 13e1403c75a9c2404fdfd05bf23f3fa6fd3a8b36 found current OC05 policy in objective_consumer_bounded_evidence.py = NOT_YET_APPLICABLE, seam=None (blob f30fca20e7b56e00348e82765d95f974b4b6a195). Direct producer transport (blob 4a8e27a226a9c06606f5ba493d2cc7356d491a7b) needs separately issued exact producer route and consumer acceptance. No signed external-GSS/NCA original-publication field producer is exposed. Git CLI direct private remote failed DNS (git ls-remote exit 128); GitHub connector successfully fetched exact pinned source modules, which were reviewed but not imported/activated as a whole checkout. Consequently **OWNER_IMPORT_GRADE = BLOCKED_AFTER_ATTEMPT**, not falsely claimed.

**Operative N5/N6 → N7/EE13 → N9/OC05 = HOLD**, with clear source archival/method, field issuance, nonpooling relation authorization, and OC05 applicability/signature gates. See 02.
