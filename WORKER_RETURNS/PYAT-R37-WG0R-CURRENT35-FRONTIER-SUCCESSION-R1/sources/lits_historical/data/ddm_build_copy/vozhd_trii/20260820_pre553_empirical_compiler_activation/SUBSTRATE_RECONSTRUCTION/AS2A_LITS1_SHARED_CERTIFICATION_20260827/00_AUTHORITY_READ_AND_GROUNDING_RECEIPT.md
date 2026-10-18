# AS2A LiTS-I authority-read / grounding receipt

Status: `GROUNDED__SHARED_CANDIDATE_NEUTRAL`

- Trii live control HEAD: `04a0109aa170c6041b199e5c6130a39a8e0f6029` (unchanged from dispatch).
- Verkhovod coordination HEAD: `0f61b3840ddae78f4a5df30cde22b1bc82aaec2e`.
- Dedicated branch: `as2a-lits1-shared-cert-20260827` from Trii control HEAD.
- Read first: `18_AS1_BANK_COMMON_SELECTION_MANIFEST_AND_LITS1_SHARED_ROUTING.md`.
- Consumed: Authority 74 and Authority 82; R07 LiTS packet/hostile fixtures; source-native constitution; decoder contract; C05R2A facade law; accepted active response-semantic binding; accepted LiTS response-option authority hash; accepted LiTS-2006 FQRA input identity; uploaded LiTS-I questionnaire.

## Uploaded source verification

- `LiTS_I.dta`: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09` / 139,531,180 bytes — exact expected source SHA PASS.
- `LiTSI_Questionnaire.pdf`: `b94bdcf4a9f2e2e025bf35e5364f79acf0b1f5fa05c035064e674fa58a921eae` / 240,732 bytes — exact expected questionnaire SHA PASS.
- uploaded `LiTS-I-codebook.csv`: `400ad9cf8b0b350a8ba1a2a778346f190ef2bba710145e648a12fc9ff464fc44` / 267,885 bytes. It is an inspection copy; it does not match the earlier accepted repository-codebook member SHA `91698cbc22d7498c3587bcacd7f96be47323d2bc9867cec5103e954e5099eb0c` and is not promoted to authority. Its 1,198 variable names/order match the uploaded DTA under a nonauthoritative diagnostic.

Frozen decoder remains `decode_dta(source_path, encoding="latin1")`; `latin1` remains compatibility execution only, not source-text authority.
