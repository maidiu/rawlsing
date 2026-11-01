# Constructor and real compiler/batch receiver

## 1. Code

**Module:** `rawlsing_next/programma_pyat_original35_constructor.py`
**Tests:** `rawlsing_next/tests/test_programma_pyat_original35_constructor.py`
**Status:** sourcefree candidate, nonissuing, no PRE-MAIN integration.

Public entry point:

```python
from rawlsing_next.programma_pyat_original35_constructor import (
    Original35Input, WaveAdmission, WaveIdentity, SourceGrant,
    EligibleItem, ScientificMethodInput, construct_original35_epre,
)

plan = construct_original35_epre(Original35Input(waves=..., scientific_method=...))
```

The constructor is deterministic. It does not use Python `hash()`, time, random,
network, filesystem source reads or environment-dependent ordering. All
identities are `semantic_hash`-derived exact refs.

## 2. Actual receiving current code

The constructor calls two present current owners:

1. `rawlsing_next.pre553_issued_workload.original35_roster(...)` — exact 35-wave
   roster/admission validation.
2. `rawlsing_next.pre553_batch_runner.BatchManifest(...)` and
   `BatchUnitSpec(...)` — current batch manifest owner. Every compiled operation
   becomes an exact `BatchUnitSpec`; held/abstained operations never become batch
   units.

This is the **first consumer at manifest/admission grain**. It is not a claim of
C11/I03/I05 execution:

- no C11 logical releases are fabricated;
- no source factory is called;
- no `BatchExecutionRunner.run` is invoked;
- no empirical fact, measured result, selected world or N11/N12 product is
  produced.

The positive test proves the real current `BatchManifest` accepts 840 exact
units and rejects the fault cases through the constructor before a manifest is
created. Full C11/I03/I05 execution requires a separately authorized wave pack
with exact release refs and source rights.

## 3. Positive execution

Fixture: 35 synthetic waves, 2 items per wave, 3 response values per item,
DIST/CONDITIONAL/JOINT/HETEROGENEITY/RECURSIVE classes, explicit conditioner,
joint, stratum and recursive authorities.

| Item | Emitted operations per wave |
|---|---:|
| item A | 3 DIST |
| item B | 3 DIST + 6 CONDITIONAL + 6 JOINT + 3 HETEROGENEITY + 3 RECURSIVE = 21 |
| total | 24 |
| 35 waves | **840** |

Observed:

```text
18 passed
plan.no_drop_ok = True
roster = 35
waves = 35
operations = 840
batch_units = 840
holds = 0
abstentions = 0
BatchManifest.units = 840
source_qualification = TEST_ONLY_SOURCEFREE
all35_populated_claim = False
sourced_results_claim = False
```

Receipt: `test_receipts/constructor.log`,
`test_receipts/constructor_junit.xml`. The current batch owner also passes
`16/16` tests in `test_receipts/batch_consumer.log`.

## 4. What this advances—and what it does not

**Advances at sourcefree construction scope:**

- F1 exact substrate: exact wave/item/route/weight/eligibility/semantic/role/use
  refs, no invented metadata.
- F2 conditional requests: exact conditioner, values and same-eligibility binding.
- F3 heterogeneity/recursive requests: exact stratum and recursive authority.
- F4 joint requests: exact joint item, values and joint authority; no invented
  same-respondent join beyond the declared binding.
- Batch first-consumer admission: current `BatchManifest` receives exact units.

**Does not advance:**

- measured F1–F4 distributions/conditionals/joints (no source execution);
- F5–F8, N9/N10W or selected-world consumer;
- N11 objective acceptance or N12 wake;
- any population estimate or person/actor state.

The practical reason the manifest receiver matters is that it forces every
prospective operation into the same exact batch identity law used by the current
execution owner. It turns a “list of questionnaire tasks” into a no-drop,
content-addressed request frontier. It does not make that frontier scientifically
measured.

## 5. Exact first-reader contract

A future authorized execution owner receives:

```text
Original35EprePlan
  .roster                         35 exact OriginalWaveIdentity rows
  .waves[].u_item_refs            exact U_item refs
  .waves[].u_unit_ref             derived U_unit ref
  .waves[].u_app_ref              exact eligible-population/applicability ref
  .waves[].e_pre_ref              exact wave E_pre root
  .batch_manifest                 current BatchManifest
  .batch_units                    exact BatchUnitSpec units
  .holds / .abstentions           typed non-compiled records
  .no_drop_manifest               exact counts/reasons
  .source_qualification           TEST_ONLY / ORIGINAL / NONISSUING
  .all35_populated_claim          always False in this candidate
```

A real receiver must still resolve every unit through a real C11 repository and
I03/I05 executor. Until then the plan is a **prospective sourcefree request
frontier**, not an empirical result.

## 6. Consumer gap

`REAL_C11_I03_I05_RECEIVER_MISSING`:

- no exact C11 logical release refs for the synthetic waves;
- no original source/host/purpose grant;
- no semantic item registry authorized for original items;
- no named downstream empirical consumer.

The current BatchManifest is real. The full compiler/execution receiver is not
fabricated.
