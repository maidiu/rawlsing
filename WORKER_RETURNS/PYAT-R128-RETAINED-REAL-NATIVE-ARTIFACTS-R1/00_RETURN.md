# R128 — retained real native artifact recovery

**Status:** `ARTIFACT_RECOVERY_PASS__M1_INPUT_REFUSED__CONFLICTING_AUTHORITY_SNAPSHOT_PREIMAGES__FULL_CONSUMER_NOT_REACHED`

**Evidence class:** `FRESH_RETAINED_REPLAY__NO_SOURCE_EXECUTION__ORIGINAL_SOURCE_NOT_EXECUTED`

No raw survey, DTA, SAV, archive, source hash, metadata decode, C11 respondent
snapshot expansion, Library scan, candidate run, or source-derived measurement
was performed. The only real input was the exact retained final-success
checkpoint authorized by the commission.

## Exact input verified

- Private locator:
  `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json`
- Size: `3404445161` bytes.
- Document SHA-256:
  `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726` — PASS.
- Internal checkpoint identity:
  `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`.
- Canonical closure identity:
  `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415` —
  independently recomputed from the canonical closure body — PASS.
- Closure schema:
  `FIABC_LITS_CANONICAL_CURRENT_EMPIRICAL_OBJECT_CLOSURE@1.0.0`.

No source fallback was attempted. A mismatch would have been a refusal; none
occurred.

The final-success owner loader was **not** invoked: its
`_load_lits_materialization_checkpoint` uses `path.read_bytes()` plus full JSON
decoding, and `_validate_lits_canonical_empirical_closure` retains all 234
hydrated objects (about 3.9GB of object material), exceeding the 3GiB RSS
budget. R128 instead used the same exact public constructors, canonicalization/
hash law, closure schema/identity law, and per-object closure checks in the
bounded streaming wrapper recorded in `COMMANDS.md`.

## Artifact recovery — PASS

The 234 retained public-object preimages were streamed, hydrated, and
re-materialized with the existing native constructor
`rawlsing_next.pre553_carrier_execution.materialize_public_object`; every
object round-tripped to its exact canonical preimage and content identity.

| Class | Retained |
| --- | ---: |
| `EmpiricalFact@1.0.0` | 60 |
| `EmpiricalQuerySpec@1.0.0` | 63 |
| `EmpiricalPredicate@1.0.0` | 35 |
| `AuthoritySnapshot@1.0.0` | 24 |
| `DiscoveryAuthority@1.0.0` | 1 |
| `DiscoveryResultReceipt@1.0.0` | 50 |
| `EmpiricalUniverse@1.0.0` | 1 |
| **Total** | **234** |

Conservation/closure results:

- candidate frontier: 50; query roles: 77;
- terminal coverage: 49 `EVALUATED_SUPPORTED`, 1 `EVALUATED_VALID_EMPTY`;
- typed terminals: 49 `DISCOVERED_RESULT_SUPPORTED`, 1 `VALID_EMPTY`;
- empirical facts: 60 `SUPPORTED`;
- structural admissions: 0;
- valid-empty receipt:
  `urn:rawlsing:pre553:DiscoveryResultReceipt:sha256:33275ddf7a09d4de1baea25bf83851ef1dc6195a541f96712118cde3522c29c9`;
- adopted mixed-predicate authority:
  authority `0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55`,
  snapshot object
  `c22cccad0add0048047f4edc3852ebce5d7f87ca0e7b81acb18587abb98ece4e`;
- final native release:
  `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`;
- replay:
  `30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08`;
- representation authority:
  `9fce3b606413c2a5d3e9a05eda967067d191fbb31ff869d445d962bdf321393d`.

All retained fact preimages remain private and complete, including 6,718,857
`source_empirical_provenance_refs`, 1,582,862 risk-member refs, 864,925
denominator-member refs, all 60 target-topology projections, missingness/
uncertainty material, and all 58 deduplicated canonical preimage fragments.
The canonical C11 release retention document and the historical ASTRA-shaped
summary were retained separately from the native object graph. The ASTRA
summary is not treated as the native object ontology.

## Existing consumer edge — actual native refusal

The artifacts were passed to the existing M1 owner
`rawlsing_next.pre553_learned_empirical_adjudication` from one actual supported
discovery receipt and its real fact(s), all real queries/predicates, all 24
retained authority snapshots, and the real discovery authority.

The reached call
`build_m1_adjudication_input_bundle(...)` refused with the native error:

`M1IntegrityError: conflicting exact authority snapshot preimages`

There are six retained `AuthorityRef`s with two different exact snapshot
preimages each. The exact authority refs, both snapshot refs per conflict, the
input counts, and the blocked call are in
`CONSUMER_RECEIPT_OR_REFUSAL.json`. No M1 bundle was created, no family rule was
reached, no M1/M2/B5 positive was manufactured, and no N10E/FF/V553 values were
read.

The smallest observed dependency is an owner-approved canonical resolution of
the duplicate retained `AuthoritySnapshot` preimages (one exact preimage per
`AuthorityRef`); then the exact family rule/validator/admission can be selected.
R128 does not choose between the retained preimages and does not write a new
authority object.

## Severance/restoration

Using one real `EmpiricalFact` and the native constructor:

- `object_id` identity severance rejected;
- exact query-reference severance rejected;
- exact original document restoration passed with the same fact ref and content
  hash.

No 3.4GB checkpoint reread was used for these probes; only the exported private
object was used.

## Resource and privacy

- Extraction peak RSS: `1040838656` bytes (under 3GiB; host 16GiB).
- Consumer-attempt peak RSS: `662142976` bytes.
- Full checkpoint JSON loads: 0.
- Source accesses: 0.
- Private object store: 234 content-addressed gzip objects, approximately
  `716703620` bytes compressed; `3898153099` bytes of hydrated object material.
- No respondent rows, respondent IDs, risk-member lists, provenance refs, or
  reversible person/event preimages were written to Git.
- `NATIVE_VALIDATION.json`, `OBJECT_GRAPH.json`, `RESOURCE_AND_ACCESS.json`,
  `CONSUMER_RECEIPT_OR_REFUSAL.json`, and this return contain only nonperson
  refs/counts/summaries.

Historical 50/77/60/50 counts are conservation checks for this retained artifact,
not current survey/workload scope, current permission, or milestone acceptance.

## Exact next step

1. Existing owner resolves the six duplicate retained authority preimages by an
   exact canonical rule (or supplies one exact unique snapshot per
   `AuthorityRef`).
2. Rebuild the real M1 input bundle and identify the exact family
   rule/validator/admission required for these retained evidence objects.
3. Only then attempt M1 -> M2/B5 and the actual FF/V553/N10E consuming edge.

The complete representative milestone, learned products, source re-execution,
and downstream positive remain **NOT_REACHED**.

## Holds

Original-source/current measurement, CI/prod/R09, actor/dyad/V3, N11/N12,
Sorok, J52/W52, full35/1890/F1–F8/globalF6F7F8/LongMemory, and parallel C5 remain
held/unchanged. No current permission or scientific conclusion is inferred from
this retained artifact.
