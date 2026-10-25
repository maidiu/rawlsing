# R100 — retained Q86 CONTEXT → pinned P41 consumer

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity and gate

- Branch: `agent/opencode-pyat-r100-q86-context-consumer-r1`
- Startup: `b2cfe93cee854b7aff2081a7a223ada75295332a`
- Contract: `b885ce407322a5c4ad6a2f635bee1d1a868ca621` (R100 contract frozen
  before the code commit).
- Code: `e2a7d540d1a052eff0db315e95c329a18244157d`
- Executor: existing OpenCode/DeepSeek `ses_e98c905cbffekusoHURfKyEUKG`,
  `opencode-go/deepseek-v4.1-flash`, variant `max`, stable `r61-r01`.
- Root/branch/HEAD gate passed at startup; only untracked pycache existed.

## Implemented actual connection

`load_q86_context_evidence()` reloads the exact retained GT2 Q86B→Q86A
query/fact through the existing raw-data-free public owner
`pre553_repo_native_current_payload.load_current_gt2_query_fact_from_committed_transport`.
When the sparse worktree lacks the committed transport, it extracts only the
fixed `f148f9ba…` transport directory and owner module into a private temporary
root; it never opens the original `.sav`, Library or respondent rows.

It then executes the existing actual chain:

`exact conditional support → GT12 PREV3 admission → GT12 E2B current binding
→ V554 → V557/V558 CONTEXT resolution`.

The retained product preserves:

- source: Afrobarometer Round 5, source digest `c9200ba3…b651`;
- query `e4ec3998…d0d0`, fact `540236d5…1f46`, risk
  `0484fa5c…1313b`, denominator **19,210**;
- **36 typed joint cells** (6×6), including observed zero, DK, NOT_ASKED,
  REFUSAL, MISSING and minority cells;
- RAW/unweighted reported-context grade; permission `CONTEXT_ONLY`;
- exact relation/admission/F1/resolution refs and no V555/B1 use.

`receive_q86_context_view()` validates the supplied evidence against a fresh
actual load and then invokes the **actual pinned P41 service** (`f27d1101…`) for
all six Q86B condition states with a Q86-specific provider and
`world_part=False`. It returns six actual P41 receipts whose N10E context steps
carry the six conditional Q86A count distributions. The context assertion has:

- `state=Q86_CONTEXT_SELECTED_VIEW`;
- context cells and denominator;
- P41 receipt hashes and N10W positioned consumptions;
- `structural_assertion=None`, `actor_state="NOT_TOUCHED"`;
- no structural route mutation and no actor transition.

An `ENGINEERING_CONTROL` request may replace only in-memory cells for a
clearly labelled `NONORIGINAL_CONTEXT_CONTROL`; it proves the P41 consumer reads
the context payload. It is never issued as an altered Q86 fact.

## Qualification

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R100-Q86-CONTEXT-CONSUMER-R1/junit.xml -o addopts=''
```

`22 passed`, 0 failed/errors/skips, `228.051s`. R100-specific tests:

- actual retained Q86 → pinned P41 positive, 36 cells/19,210;
- P41 consumer dependency via a denominator-preserving counterfactual: receipt
  hashes and view hash change, restore passes;
- permission/evidence severance refuses, actual restore passes;
- wrong query/fact/conditioner/target/risk/relation/admission/F1/resolution/
  role-order refuses;
- cold fresh-process replay reproduces state, view hash, six P41 hashes and
  cell count.

Actual positive values:

- evidence content hash: `456735537da217dbeb765a51cbd8c21e7402b99a4e720f92bd8bf7c36cdfee63`
- view hash: `4199f922fbad332f59c06eb0d8f78537f75447bb07eb3eebd277f10c9d17ee2e`
- six P41 receipt hashes:
  `03cdfa17…17ed`, `ceeb772a…c465`, `e5216b6d…1ee9`,
  `6fcae3f2…6d19`, `d85cab71…c3f84`, `07d7417f…c0e7`.

The existing structural wrappers still return
`CONTEXT_STRUCTURAL_AUTHORITY_HELD` for CONTEXT fields; that R4 control remains
in the 22-test suite. No structural route is used or changed by this new path.

## Code blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `79a15a98876da763da8effb1da393dcd214d1f63` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `27ae5b4572e0815997a13eb80275ab26ba4eda0d` |

Only these two tracked code paths changed. R98/R99/R97 recovery, FF/temporal/
P41 owners, source/service/config and prior returns were read-only.

## Pins

- Q86 retained transport/owner cut: `f148f9ba34deb0ae2ad3983fe94bbcef8f004b03`
- Q86 owner blob: `b850e7794f387000afe4a6dfd49ca5092426f895`
- FF blob: `a70decb20747d84cbcbe27d1280babc6de88ef33`
- FF admission bridge blob: `ea04ec079e8d60e6e5c7236ec5b54898876be4b3`
- V554 bridge blob: `ca3d6b8d832d7ca8d959bd19e19a23b08cabde76`
- current GT12 binding blob: `5c0e730972ca7f31c3be92564c299822c431ccc5`
- P41 packet: `f27d1101048638bba395143a48efb7ef00bfcda4`
- R98 return: `d29a9db26821e937afc3d0ef19e243aafbff1744`
- R99 intake/grant/scope: `3d9dbb79153811715ac68b0ab0b32332ce939d13`

## Limits

- This is a **retained, originally derived historical context product**, not a
  fresh original respondent read, new measurement, population estimate or
  current operative world. `temporal_grade` is
  `RETAINED_HISTORICAL_CONTEXT_NOT_OPERATIVE_CURRENT`; `as_of_ref` is not
  applicable and refuses.
- The product is actor-independent reported social atmosphere. It does not
  create structural position, pressure, causal mechanism, V555/V556, actor
  state, route probability or cross-source person joint.
- The engineering counterfactual is nonoriginal control only; no altered Q86
  empirical fact is issued.
- The fixed retained evidence is cached per process for repeated reads; cold
  replay is a fresh process. No live permission revocation API exists; the
  test's permission/evidence severance is a supplied-evidence nonoriginal
  control, not an owner-issued revocation.
- Original 35/1890/global F6/F7/F8, R09/CI/prod, N11/N12, Sorok and J52/W52
  remain held. Z remains UNRESOLVED denominator 16.
- Distinct independent reviewer required; no self-adoption.
