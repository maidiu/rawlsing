# SRC04 original full release — independent review

## Verdict

**PASS_SCOPED_ORIGINAL_SRC04_RELEASE**

The actual 7,337-row SRC04 original release at
`9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1`
independently matches the admitted source at the asserted 177-response +
3-coordinate full scope, closes over the durable native object bundle, preserves
authority boundaries, and replays the exact release identity.

## Identity and custody

- Reviewer role: existing distinct SRC04 reviewer, not A/B author.
- Review branch: `agent/pyat-src04-original-release-review-20261028`
- Review startup HEAD: `6ac3489d0913299f4151dfbcef7c7d0488d467fb`
- Reviewed candidate: `303a57851785557fff8229e29a5554717168cbd1`
- Actual primary process: PID `93597`, exit `0`
- Source: SRC04, SHA `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- Source release manifest hash: `cf5b990ec740134b77a4acf34653be02640450110ae86bff1b23aa4ffca44472`
- Durable local bundle: `SRC04-9ddec98561a0fc54`
- Author code writes: none. Review writes: `campaign_src04_completion/original_review/**` only.

## Measured qualification

### Source and release

- Source rows: `7,337`; source columns/physical slots: `181`
- Selected response fields: `177`; selected coordinates: `3`
- Response positions: `1,298,649`; coordinate positions: `22,011`
- Public objects: `2,619,317`; internal records: `7,514`
- Public file SHA: `873cef612c3c038901a77224e4ce98810a1f1798e0907534192c0da1defd4645`
- Internal file SHA: `db9b4b9442488792713504d348cd8e421e64b74145ee354020ba2a9ffea1e60d`
- Replay manifest file SHA: `ff84ea7b327ffc5d49b10ba53a4346eb7dc02fce3bce45bc0c4202264bc478e3`
- Replay manifest semantic content hash: `893f24ae10b297cd21422d154ec1649d522da4add006d1d3ac3da9a3da111a49`
- Recomputed release semantic hash: `9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1`

### Actual source correspondence

The admitted decoder was used once under the existing full-source grant
(`d8f13c…`), with two admission resolutions. All source cells were processed in
bounded streaming form; no respondent rows, raw values or member lists were
emitted.

- Compared all selected source cells to release events/coordinate facts by
  source row, field, raw-witness digest and response/coordinate state.
- Response fields matching: `177/177`; coordinate fields matching: `3/3`.
- Response state counts: `SUBSTANTIVE_RESPONSE=1,093,307`, `DK=76,218`,
  `REFUSAL=1,200`, `SOURCE_SPECIFIC_SPECIAL=6,453`, `MISSING=121,471`.
- Coordinate state counts: `OBSERVED_COORDINATE=20,700`, `MISSING=1,311`.
- Distinct respondent rows: `7,337`; all `181` physical slots accounted.
- Canonical response/coordinate values present: `0`.
- Binding targets matched at full count: `q235`–`q244`, actual income fields
  `q715withoutmorocco`/`q716withoutmorocco`, fractional decile fields
  `q715incomedeciles`/`q716incomedeciles`, and age coordinate `q701`.
- `q217` held: `7,337` cells, `187` missing, exactly `38` source-unbound cells;
  no release events and no guessed labels.
- Routing: `ROUTING_UNKNOWN` for all `1,298,649` routing facts; no eligibility
  or population claim.

### Closure, authority and replay

- Release closure: `2,626,833` exact refs, matching all public/internal objects
  plus the two source refs.
- M01–M18 coverage is complete; the release hash was recomputed from the exact
  replay manifest projection and matched the asserted release ref.
- Authority: `7` exact snapshots; `1` `ALLOW` replay protocol and `6` `DEFER`
  source-preparation snapshots; `1,298,649` events, `22,011` coordinates and
  `1,298,649` routing facts reference authorities; `0` missing authority refs;
  no non-replay scientific `ALLOW` adoption.
- Local bundle files and counts match the frozen receipts; the cold local replay
  was verified without reconstructing or copying the 7.4 GiB bundle.

### Negative checks

- Wrong-source grant: `GRANT_SOURCE_MISMATCH`
- Held-authority grant: `GRANT_NOT_CURRENT`
- Existing wrong-source and held-authority receipts remain preserved.

## Tests

```sh
PYTHONPATH=. python3 campaign_src04_completion/original_review/qualify_release.py
PYTHONPATH=. python3 -m pytest campaign_src04_completion/release/tests -q -o addopts=''
PYTHONPATH=. python3 -m pytest campaign_src04_completion/bindings/test_numeric_domain_binding.py -q -o addopts=''
```

- Independent qualification: **PASS**, exit `0`
- Release author tests: **11 passed**
- Numeric binding tests: **8 passed**

## Limits

- PASS is scoped to this actual SRC04 full release at the asserted 177+3,
  7,337-row original-source scope.
- This is not an N11/N12, full-estate, actor, CI/prod, Sorok/J52W52 or broader
  source-family claim.
- Routing remains unknown; no population/weight, canonical, currency or
  structural meaning was adopted.
- `q217` remains held at exactly 38 source-unbound cells.
- Source access used only the existing full SRC04 grant/admitted decoder; no
  other original source was read.

## Evidence

- `REVIEW.json`
- `QUALIFICATION_RESULTS.json`
- `TEST_RESULTS.json`
- `MANIFEST.json`
- `qualify_release.py`
- Preserved receipts under `campaign_src04_completion/original_review/`
