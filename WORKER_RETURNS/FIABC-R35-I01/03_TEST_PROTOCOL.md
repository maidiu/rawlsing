# FIABC-R35-I01 — Test Protocol

## Court file

`rawlsing_next/tests/test_r35_i01_physical_metadata.py`

Framework: Python `unittest`.

All fixtures are synthetic.

No canonical raw source carrier is opened by this test court.

## Hostile cases

### R35-I01-H01 — header/layout count differs from traversed geometry

Fixture:
- synthetic standard SAV fixed header;
- `nominal_case_size = 174`;
- normalized variable inventory size `= 332`.

Required:
- raw header receipt retains `174`;
- normalized dictionary count retains `332`;
- normalized stream width retains `332`;
- no equality is forced.

Test:

`test_nominal_header_count_and_traversed_stream_width_both_survive`

### R35-I01-H02 — mismatch normalized away

Fixture:
- format-native header witness `174`;
- reader-declared / normalized geometry `332`.

Required:
- both witnesses remain separately addressable;
- no corrected/resolved/authoritative count field is manufactured.

Test:

`test_metadata_mismatch_is_preserved_not_normalized`

### R35-I01-H03 — display format replaces stored magnitude

Fixture:
- variable display format `F2.0`;
- physical cell raw value `9876543210`.

Required:
- display format remains metadata;
- raw cell magnitude remains unchanged.

Test:

`test_display_format_remains_distinct_from_stored_magnitude`

### R35-I01-H04 — candidate drops one physical witness

Fixture:
- valid incidence;
- expected metadata digest frozen;
- hostile candidate removes `raw_layout_declarations`.

Required:
- digest verification fails closed with `DecoderError`;
- smaller self-consistent object is not accepted.

Test:

`test_candidate_representation_dropping_physical_witness_is_rejected`

### R35-I01-H05 — semantic projection equal, physical metadata unequal

Fixture A:
- same canonical source SHA;
- same synthetic semantic projection;
- SAV `nominal_case_size = 174`.

Fixture B:
- same canonical source SHA;
- same synthetic semantic projection;
- SAV `nominal_case_size = 175`.

Required:
- semantic projection equality remains true;
- physical metadata digests differ.

Test:

`test_equal_semantic_projection_can_have_unequal_required_physical_metadata_digest`

### R35-I01-H06 — reader/config drift

Fixture:
- identical source/variables/file metadata;
- different reader version identity.

Required:
- physical metadata digest differs.

Test:

`test_reader_config_is_bound_into_physical_metadata_digest`

## Positive control

The synthetic `174 / 332` fixture is a positive preservation control.

The PASS condition is not "counts match".

The PASS condition is:

`BOTH ACCEPTED PHYSICAL WITNESSES SURVIVE WITHOUT RECONCILIATION`.

## Intended command at fan-in / qualification

```bash
python -m unittest rawlsing_next.tests.test_r35_i01_physical_metadata
```

or under the repository's broader unittest/pytest harness.

## Execution status in this worker

`NOT_EXECUTED_LOCALLY__GITHUB_BROWSER_ONLY`

Reason:
- commission forbids local-machine execution workflow;
- no measured P2X may be run;
- no GitHub Actions status was attached to the implementation/test commit when checked.

No PASS count is fabricated here.

The code and hostile court are committed for HQ fan-in and R35-Q01 qualification.

## Measured P2X

`NOT_RUN`

## Canonical raw carriers

`NOT_OPENED`
