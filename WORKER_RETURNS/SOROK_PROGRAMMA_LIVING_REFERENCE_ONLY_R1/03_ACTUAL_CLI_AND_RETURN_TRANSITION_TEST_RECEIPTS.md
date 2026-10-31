# Actual CLI and return-transition test receipts

## 1. Environment and source cuts

```text
Device: oldMac
OS: macOS 13.7.8 x86_64
Python: 3.11.3
pytest: 9.1.1
Candidate:
SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1
Startup/build PRE-MAIN: f40c26301d7d5b811c1bb92efa4934ad564ce5b3
Refreshed current PRE-MAIN: 8e44ca9c751049d65e6def47600b5c073ee04b29
R3 source cut: e50d32eb6816578145d17dcd637a0b90b3a1ef40
R3 review: 3f3d9ec2fddc36bd4047bc6c730382c65a5e692a
```

## 2. Refresh and state identity

```sh
cd SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1
PYTHONDONTWRITEBYTECODE=1 python3 living_reference.py refresh
```

Exit `0`. Generated `state.json` and `SNAPSHOT.json` are byte-identical in
content:

```text
state nodes:       198
state edges:       423
source rows:       144
gaps:               12
sectors:            22
owner slots:        46
state_digest:       95aeda5578983ae3ea8ec313d6154e656121646f6590cac8a1bc07db0139c03d
source manifest SHA-256: 7715c193b8307f03ed3de4088436bdff2d1fab56d7fe49de16b6d99ac947a086
source manifest digest:  8bbde425f4369b7945a82680f3f730b804c325ce61ba3ef6e1a6697d697b64c1
```

## 3. Same-state operator commands

All commands exited `0`, produced JSON, and read the same `state.json`:

```sh
python3 living_reference.py overview
python3 living_reference.py zoom S5 --depth 2
python3 living_reference.py gaps --domain S15
python3 living_reference.py critical-path L0_PERSON
python3 living_reference.py source S5
python3 living_reference.py consumer A5
python3 living_reference.py alternatives S5
python3 living_reference.py work-now
python3 living_reference.py workers
python3 living_reference.py history H0001
python3 living_reference.py export
```

Representative results:

- `overview`: 198 nodes, 423 edges, 144 sources, 22 sectors, 12 gaps, 46
  slots, 6 workers; one external Pyat boundary.
- `zoom S5 --depth 2`: includes `L0_S5_FLOURISHING_AGENCY`,
  `L1_S5_FLOURISHING`, `L3_S5_NORMATIVE_MODEL` and the S5 source/gap edges.
- `gaps --domain S15`: `GAP_S15_HUMAN_ALPHA`.
- `critical-path L0_PERSON`: returns a path ending at
  `L5_HISTORICAL_NEGATIVES`.
- `source S5`: exact Program Map commit/path/blob and typed source kind.
- `consumer A5`: `NONE_PROVEN_AT_PREMAIN`; human `NOT_PROVEN`.
- `work-now`: four evidence-backed candidate work areas, HQ decision required.
- `workers`: R3 returned/unadopted, R3 review sealed/not assumed running, four
  assets returned/author-tested/unadopted; no local process inferred.
- `export`: full 440,527-byte state export.

## 4. Source manifest refresh check

```sh
python3 verify_source_manifest.py
```

Exit `0`:

```text
result=PASS
rows=144
references=3
errors=[]
manifest_digest=8bbde425f4369b7945a82680f3f730b804c325ce61ba3ef6e1a6697d697b64c1
```

The verifier resolved every `commit:path`, object type/id and timestamp against
Git, including the R15 tree file list. This is the required S2 Git check; the
offline state is not proof by itself.

## 5. Actual unit/readback tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -o addopts='' -q test_living_reference.py
# 11 passed in 7.77s

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_living_reference.py
# Ran 11 tests — OK
```

The tests cover:

1. deterministic refresh and shared state;
2. material independent B path, with human/native still held;
3. V3 M25 source/owner and non-adoption;
4. all six S5/S7/S11/S13/S14/S15 L0–L5 paths and falsifiers;
5. arbitrary source/terminal or explicit gap;
6. authorized transition changes only one axis and invalidates downstream;
7. missing owner/reviewer transition refused;
8. returned CP-A5 engineering PASS cannot make human A5 green;
9. B source withdrawal invalidates Sorok dependents but not M01 or Pyat boundary;
10. new requirement enters visible gap while old history remains;
11. snapshot death/restore and forged source verifier failure.

## 6. Intake and authorized-transition CLI receipts

Run in a temporary copy (the candidate was not modified):

```sh
python3 living_reference.py intake-return intake.json
# H0002, R3-RETURN, CANDIDATE_NOT_PROMOTED, new gap GAP_NEW_REQUISITE

python3 living_reference.py gaps --domain DISCOVERED_REQUISITE
# GAP_NEW_REQUISITE, UNREPRESENTED_REQUIREMENT

python3 living_reference.py apply-authorized-transition transition.json
# APPLIED_CANDIDATE_ONLY
# node CP-A5-R2 engineering: AUTHOR_TESTED_UNADOPTED -> INDEPENDENT_ACCEPT_SCOPED
# invalidated L4_I1_CANDIDATE, L4_NAMED_FIRST_CONSUMER, L5_FOUR_AUTHOR_TESTS
# pyat_boundary_touched=false

python3 living_reference.py history H0003
# exact immutable transition record above
```

The transition did not set human `PROVEN`, authority adoption or Pyat state.
The sourcefree return was not promoted by its claimed test count.

## 7. NOT_RUN

- No native source/actor/world, C9/C12 adoption, Pyat N11/N12/C11, human A5,
  production import or PRE-MAIN merge.
- No full R6/R7 branch suite or four-asset suite; their author/source evidence
  is retained at declared grain only.
- No scientific rule issuance, priority choice or self-review.
