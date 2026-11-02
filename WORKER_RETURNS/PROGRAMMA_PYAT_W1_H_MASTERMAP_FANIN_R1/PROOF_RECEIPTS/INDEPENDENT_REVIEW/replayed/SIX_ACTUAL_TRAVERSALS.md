# Six actual CLI traversals

All JSON receipts are emitted by fresh CLI processes from the same deterministic snapshot. Edges marked MISSING or CONDITIONAL are evidence of a gap or a scoped prerequisite; no route is an empirical run. Forward and inverse receipts use the same edge IDs.

## T1

```sh
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm focus N11 --route N10W N9 N8E SRC12 --brief
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm reverse SRC12 --route N8E N9 N10W N11 --brief
```

```json
{
  "actual_forward": {
    "hops": [
      {
        "edges": [
          {
            "condition": "Unconditional",
            "from": "PYAT:ASTRA:N10W",
            "id": "EDGE:2649e5f17ba64540fff38512",
            "record": "ROW:A:PLAN_CROSSWALK:XW0041",
            "to": "PYAT:ASTRA:N11",
            "type": "UNCONDITIONAL_PREREQUISITE"
          }
        ],
        "from": "PYAT:ASTRA:N11",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N10W"
      },
      {
        "edges": [
          {
            "condition": "Unconditional",
            "from": "PYAT:ASTRA:N9",
            "id": "EDGE:7b844d48f9011488b57692db",
            "record": "ROW:A:PLAN_CROSSWALK:XW0037",
            "to": "PYAT:ASTRA:N10W",
            "type": "UNCONDITIONAL_PREREQUISITE"
          }
        ],
        "from": "PYAT:ASTRA:N10W",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N9"
      },
      {
        "edges": [
          {
            "condition": "Its product family is required by this declared served-world scope.",
            "from": "PYAT:ASTRA:N8E",
            "id": "EDGE:a033e4a5e551afcd9882e929",
            "record": "ROW:A:PLAN_CROSSWALK:XW0030",
            "to": "PYAT:ASTRA:N9",
            "type": "CONDITIONAL_PREREQUISITE"
          }
        ],
        "from": "PYAT:ASTRA:N9",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N8E"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "Need original comparable release/item/population/design/weight pair",
              "scope": "Only for scoped EVS temporal claim with SRC14"
            },
            "from": "PYAT:SOURCE:SRC12",
            "id": "EDGE:7242bd9091f9be84ffe21f70",
            "record": "ROW:C:SEAMS:W1C-S27",
            "to": "PYAT:ASTRA:N8E",
            "type": "CONDITIONAL_SOURCE_PAIR_CANDIDATE"
          }
        ],
        "from": "PYAT:ASTRA:N8E",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:SOURCE:SRC12"
      }
    ],
    "ids": [
      "PYAT:ASTRA:N11",
      "PYAT:ASTRA:N10W",
      "PYAT:ASTRA:N9",
      "PYAT:ASTRA:N8E",
      "PYAT:SOURCE:SRC12"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "actual_reverse": {
    "hops": [
      {
        "edges": [
          {
            "condition": {
              "negative": "Need original comparable release/item/population/design/weight pair",
              "scope": "Only for scoped EVS temporal claim with SRC14"
            },
            "from": "PYAT:SOURCE:SRC12",
            "id": "EDGE:7242bd9091f9be84ffe21f70",
            "record": "ROW:C:SEAMS:W1C-S27",
            "to": "PYAT:ASTRA:N8E",
            "type": "CONDITIONAL_SOURCE_PAIR_CANDIDATE"
          }
        ],
        "from": "PYAT:SOURCE:SRC12",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N8E"
      },
      {
        "edges": [
          {
            "condition": "Its product family is required by this declared served-world scope.",
            "from": "PYAT:ASTRA:N8E",
            "id": "EDGE:a033e4a5e551afcd9882e929",
            "record": "ROW:A:PLAN_CROSSWALK:XW0030",
            "to": "PYAT:ASTRA:N9",
            "type": "CONDITIONAL_PREREQUISITE"
          }
        ],
        "from": "PYAT:ASTRA:N8E",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N9"
      },
      {
        "edges": [
          {
            "condition": "Unconditional",
            "from": "PYAT:ASTRA:N9",
            "id": "EDGE:7b844d48f9011488b57692db",
            "record": "ROW:A:PLAN_CROSSWALK:XW0037",
            "to": "PYAT:ASTRA:N10W",
            "type": "UNCONDITIONAL_PREREQUISITE"
          }
        ],
        "from": "PYAT:ASTRA:N9",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N10W"
      },
      {
        "edges": [
          {
            "condition": "Unconditional",
            "from": "PYAT:ASTRA:N10W",
            "id": "EDGE:2649e5f17ba64540fff38512",
            "record": "ROW:A:PLAN_CROSSWALK:XW0041",
            "to": "PYAT:ASTRA:N11",
            "type": "UNCONDITIONAL_PREREQUISITE"
          }
        ],
        "from": "PYAT:ASTRA:N10W",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N11"
      }
    ],
    "ids": [
      "PYAT:SOURCE:SRC12",
      "PYAT:ASTRA:N8E",
      "PYAT:ASTRA:N9",
      "PYAT:ASTRA:N10W",
      "PYAT:ASTRA:N11"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "same_edge_ids": true
}
```

## T2

```sh
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm focus N2 --route WHOLE151:Q002 WHOLE101:Q02 ROW:B:CURRENT_REALIZATION:F1.I03.QUERY CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_source_backed_c11_facade.py::execute_source_backed_empirical_query --brief
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm reverse CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_source_backed_c11_facade.py::execute_source_backed_empirical_query --route CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query ROW:B:CURRENT_REALIZATION:F1.I03.QUERY WHOLE101:Q02 WHOLE151:Q002 N2 --brief
```

```json
{
  "actual_forward": {
    "hops": [
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:WHOLE151:Q002",
            "id": "EDGE:42178f64e2d4384bb3c7f4fe",
            "record": "ROW:A:PLAN_CROSSWALK:XW0004",
            "to": "PYAT:ASTRA:N2",
            "type": "CROSS_MEMBERSHIP_NOT_IDENTITY"
          },
          {
            "condition": null,
            "from": "PYAT:ASTRA:N2",
            "id": "EDGE:5be92f1fe0bb71faff8f8984",
            "record": "ROW:A:PLAN_CROSSWALK:XW0109",
            "to": "PYAT:WHOLE151:Q002",
            "type": "CROSS_MEMBERSHIP_NOT_IDENTITY"
          }
        ],
        "from": "PYAT:ASTRA:N2",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:WHOLE151:Q002"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:WHOLE101:Q02",
            "id": "EDGE:71c73dbfafdc6352e5cc1eff",
            "record": "ROW:A:PLAN_CROSSWALK:XW0245",
            "to": "PYAT:WHOLE151:Q002",
            "type": "ALTERNATIVE_DECOMPOSITION_NOT_EQUIVALENCE"
          },
          {
            "condition": null,
            "from": "PYAT:WHOLE151:Q002",
            "id": "EDGE:99a1a0caf29343f4d363bf08",
            "record": "ROW:A:PLAN_CROSSWALK:XW0109",
            "to": "PYAT:WHOLE101:Q02",
            "type": "ALTERNATIVE_DECOMPOSITION_NOT_EQUIVALENCE"
          }
        ],
        "from": "PYAT:WHOLE151:Q002",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:WHOLE101:Q02"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "Not whole-task completion or source-native denominator issuance",
              "scope": "Only at the named typed function and selected source scope"
            },
            "from": "PYAT:WHOLE101:Q02",
            "id": "EDGE:d2d14419027f32f42b26808a",
            "record": "ROW:H:ADJUDICATION:H12-NESTED-QUERY",
            "to": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
            "type": "PARTIAL_SOURCEFREE_FUNCTION_MATCH"
          }
        ],
        "from": "PYAT:WHOLE101:Q02",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
            "id": "EDGE:44e0eee8d0a5c9ace7a7e885",
            "record": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
            "to": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
            "type": "REALIZATION_LOCATION"
          }
        ],
        "from": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query"
      },
      {
        "edges": [
          {
            "condition": "SOURCEFREE_CURRENT_CONSUMER",
            "from": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_source_backed_c11_facade.py::execute_source_backed_empirical_query",
            "id": "EDGE:6747b25d9285885ee75672f1",
            "record": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
            "to": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
            "type": "AUTHOR_REPORTED_STATIC_CALL_NOT_RUNTIME"
          }
        ],
        "from": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_source_backed_c11_facade.py::execute_source_backed_empirical_query"
      }
    ],
    "ids": [
      "PYAT:ASTRA:N2",
      "PYAT:WHOLE151:Q002",
      "PYAT:WHOLE101:Q02",
      "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
      "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
      "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_source_backed_c11_facade.py::execute_source_backed_empirical_query"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "actual_reverse": {
    "hops": [
      {
        "edges": [
          {
            "condition": "SOURCEFREE_CURRENT_CONSUMER",
            "from": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_source_backed_c11_facade.py::execute_source_backed_empirical_query",
            "id": "EDGE:6747b25d9285885ee75672f1",
            "record": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
            "to": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
            "type": "AUTHOR_REPORTED_STATIC_CALL_NOT_RUNTIME"
          }
        ],
        "from": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_source_backed_c11_facade.py::execute_source_backed_empirical_query",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
            "id": "EDGE:44e0eee8d0a5c9ace7a7e885",
            "record": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
            "to": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
            "type": "REALIZATION_LOCATION"
          }
        ],
        "from": "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "Not whole-task completion or source-native denominator issuance",
              "scope": "Only at the named typed function and selected source scope"
            },
            "from": "PYAT:WHOLE101:Q02",
            "id": "EDGE:d2d14419027f32f42b26808a",
            "record": "ROW:H:ADJUDICATION:H12-NESTED-QUERY",
            "to": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
            "type": "PARTIAL_SOURCEFREE_FUNCTION_MATCH"
          }
        ],
        "from": "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:WHOLE101:Q02"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:WHOLE101:Q02",
            "id": "EDGE:71c73dbfafdc6352e5cc1eff",
            "record": "ROW:A:PLAN_CROSSWALK:XW0245",
            "to": "PYAT:WHOLE151:Q002",
            "type": "ALTERNATIVE_DECOMPOSITION_NOT_EQUIVALENCE"
          },
          {
            "condition": null,
            "from": "PYAT:WHOLE151:Q002",
            "id": "EDGE:99a1a0caf29343f4d363bf08",
            "record": "ROW:A:PLAN_CROSSWALK:XW0109",
            "to": "PYAT:WHOLE101:Q02",
            "type": "ALTERNATIVE_DECOMPOSITION_NOT_EQUIVALENCE"
          }
        ],
        "from": "PYAT:WHOLE101:Q02",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:WHOLE151:Q002"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:WHOLE151:Q002",
            "id": "EDGE:42178f64e2d4384bb3c7f4fe",
            "record": "ROW:A:PLAN_CROSSWALK:XW0004",
            "to": "PYAT:ASTRA:N2",
            "type": "CROSS_MEMBERSHIP_NOT_IDENTITY"
          },
          {
            "condition": null,
            "from": "PYAT:ASTRA:N2",
            "id": "EDGE:5be92f1fe0bb71faff8f8984",
            "record": "ROW:A:PLAN_CROSSWALK:XW0109",
            "to": "PYAT:WHOLE151:Q002",
            "type": "CROSS_MEMBERSHIP_NOT_IDENTITY"
          }
        ],
        "from": "PYAT:WHOLE151:Q002",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N2"
      }
    ],
    "ids": [
      "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_source_backed_c11_facade.py::execute_source_backed_empirical_query",
      "CODE:9809203fd915a84bae056a67210e9213879840db:rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
      "ROW:B:CURRENT_REALIZATION:F1.I03.QUERY",
      "PYAT:WHOLE101:Q02",
      "PYAT:WHOLE151:Q002",
      "PYAT:ASTRA:N2"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "same_edge_ids": true
}
```

## T3

```sh
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm focus SRC35 --route R157_CONFIGURATION P1_U_EPRE BATCH_MANIFEST_ADMISSION I03_I05_LOWERING N10E --brief
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm reverse N10E --route I03_I05_LOWERING BATCH_MANIFEST_ADMISSION P1_U_EPRE R157_CONFIGURATION SRC35 --brief
```

```json
{
  "actual_forward": {
    "hops": [
      {
        "edges": [
          {
            "condition": {
              "negative": "Configuration is not source-use authority or original measured output",
              "scope": null
            },
            "from": "PYAT:SOURCE:SRC35",
            "id": "EDGE:bed8bbcc1345ae6065239266",
            "record": "ROW:D:SOURCE35_COVERAGE:SRC35",
            "to": "PYAT:PLAN:R157_CONFIGURATION",
            "type": "HISTORICAL_CONFIG_FOR_SOURCE"
          }
        ],
        "from": "PYAT:SOURCE:SRC35",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:R157_CONFIGURATION"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "No current automatic original questionnaire/config ingress",
              "scope": null
            },
            "from": "PYAT:PLAN:R157_CONFIGURATION",
            "id": "EDGE:b97e3c0d0054dcaf077419eb",
            "record": "ROW:C:SEAMS:W1C-S02",
            "to": "PYAT:PLAN:P1_U_EPRE",
            "type": "MISSING_ORIGINAL_INVENTORY_ADAPTER"
          }
        ],
        "from": "PYAT:PLAN:R157_CONFIGURATION",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:P1_U_EPRE"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "Opaque operation refs are not executable I03/I05 catalog preimages",
              "scope": null
            },
            "from": "PYAT:PLAN:P1_U_EPRE",
            "id": "EDGE:849f701784d91d0b00c2e7ef",
            "record": "ROW:C:SEAMS:W1C-S03",
            "to": "PYAT:PLAN:BATCH_MANIFEST_ADMISSION",
            "type": "SOURCEFREE_MANIFEST_COMPATIBILITY"
          }
        ],
        "from": "PYAT:PLAN:P1_U_EPRE",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:BATCH_MANIFEST_ADMISSION"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "Existing governed frontier available; P1 NativeWorkload bridge absent",
              "scope": null
            },
            "from": "PYAT:PLAN:BATCH_MANIFEST_ADMISSION",
            "id": "EDGE:8f4043ada0ece7e8a7b54d5c",
            "record": "ROW:C:SEAMS:W1C-S04",
            "to": "PYAT:PLAN:I03_I05_LOWERING",
            "type": "MISSING_EXECUTABLE_PREIMAGE"
          }
        ],
        "from": "PYAT:PLAN:BATCH_MANIFEST_ADMISSION",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:I03_I05_LOWERING"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "No source-qualified output from P1 at this cut",
              "scope": null
            },
            "from": "PYAT:PLAN:I03_I05_LOWERING",
            "id": "EDGE:f276f523001e5b5562cb3190",
            "record": "ROW:C:SEAMS:W1C-S15",
            "to": "PYAT:ASTRA:N10E",
            "type": "MISSING_NATIVE_MEASURED_FIRST_RECEIVER"
          }
        ],
        "from": "PYAT:PLAN:I03_I05_LOWERING",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N10E"
      }
    ],
    "ids": [
      "PYAT:SOURCE:SRC35",
      "PYAT:PLAN:R157_CONFIGURATION",
      "PYAT:PLAN:P1_U_EPRE",
      "PYAT:PLAN:BATCH_MANIFEST_ADMISSION",
      "PYAT:PLAN:I03_I05_LOWERING",
      "PYAT:ASTRA:N10E"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "actual_reverse": {
    "hops": [
      {
        "edges": [
          {
            "condition": {
              "negative": "No source-qualified output from P1 at this cut",
              "scope": null
            },
            "from": "PYAT:PLAN:I03_I05_LOWERING",
            "id": "EDGE:f276f523001e5b5562cb3190",
            "record": "ROW:C:SEAMS:W1C-S15",
            "to": "PYAT:ASTRA:N10E",
            "type": "MISSING_NATIVE_MEASURED_FIRST_RECEIVER"
          }
        ],
        "from": "PYAT:ASTRA:N10E",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:I03_I05_LOWERING"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "Existing governed frontier available; P1 NativeWorkload bridge absent",
              "scope": null
            },
            "from": "PYAT:PLAN:BATCH_MANIFEST_ADMISSION",
            "id": "EDGE:8f4043ada0ece7e8a7b54d5c",
            "record": "ROW:C:SEAMS:W1C-S04",
            "to": "PYAT:PLAN:I03_I05_LOWERING",
            "type": "MISSING_EXECUTABLE_PREIMAGE"
          }
        ],
        "from": "PYAT:PLAN:I03_I05_LOWERING",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:BATCH_MANIFEST_ADMISSION"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "Opaque operation refs are not executable I03/I05 catalog preimages",
              "scope": null
            },
            "from": "PYAT:PLAN:P1_U_EPRE",
            "id": "EDGE:849f701784d91d0b00c2e7ef",
            "record": "ROW:C:SEAMS:W1C-S03",
            "to": "PYAT:PLAN:BATCH_MANIFEST_ADMISSION",
            "type": "SOURCEFREE_MANIFEST_COMPATIBILITY"
          }
        ],
        "from": "PYAT:PLAN:BATCH_MANIFEST_ADMISSION",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:P1_U_EPRE"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "No current automatic original questionnaire/config ingress",
              "scope": null
            },
            "from": "PYAT:PLAN:R157_CONFIGURATION",
            "id": "EDGE:b97e3c0d0054dcaf077419eb",
            "record": "ROW:C:SEAMS:W1C-S02",
            "to": "PYAT:PLAN:P1_U_EPRE",
            "type": "MISSING_ORIGINAL_INVENTORY_ADAPTER"
          }
        ],
        "from": "PYAT:PLAN:P1_U_EPRE",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:R157_CONFIGURATION"
      },
      {
        "edges": [
          {
            "condition": {
              "negative": "Configuration is not source-use authority or original measured output",
              "scope": null
            },
            "from": "PYAT:SOURCE:SRC35",
            "id": "EDGE:bed8bbcc1345ae6065239266",
            "record": "ROW:D:SOURCE35_COVERAGE:SRC35",
            "to": "PYAT:PLAN:R157_CONFIGURATION",
            "type": "HISTORICAL_CONFIG_FOR_SOURCE"
          }
        ],
        "from": "PYAT:PLAN:R157_CONFIGURATION",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:SOURCE:SRC35"
      }
    ],
    "ids": [
      "PYAT:ASTRA:N10E",
      "PYAT:PLAN:I03_I05_LOWERING",
      "PYAT:PLAN:BATCH_MANIFEST_ADMISSION",
      "PYAT:PLAN:P1_U_EPRE",
      "PYAT:PLAN:R157_CONFIGURATION",
      "PYAT:SOURCE:SRC35"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "same_edge_ids": true
}
```

## T4

```sh
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm focus F6 --route HR-F6 CODE:1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py:: --brief
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm reverse CODE:1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py:: --route HR-F6 F6 --brief
```

```json
{
  "actual_forward": {
    "hops": [
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:FUNCTION:F6",
            "id": "EDGE:a5c58cffe6047067854f09f1",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
            "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "PYAT:FUNCTION:F6",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
            "id": "EDGE:a5340902d23707be9359db96",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
            "to": "CODE:1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py::",
            "type": "HISTORICAL_VARIANT"
          }
        ],
        "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "CODE:1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py::"
      }
    ],
    "ids": [
      "PYAT:FUNCTION:F6",
      "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
      "CODE:1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py::"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "actual_reverse": {
    "hops": [
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
            "id": "EDGE:a5340902d23707be9359db96",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
            "to": "CODE:1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py::",
            "type": "HISTORICAL_VARIANT"
          }
        ],
        "from": "CODE:1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py::",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:FUNCTION:F6",
            "id": "EDGE:a5c58cffe6047067854f09f1",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
            "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:FUNCTION:F6"
      }
    ],
    "ids": [
      "CODE:1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa:WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py::",
      "ROW:G:HISTORICAL_REALIZATIONS:HR-F6",
      "PYAT:FUNCTION:F6"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "same_edge_ids": true
}
```

## T5

```sh
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm focus F7 --route HR-F7-TEMP CODE:d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1:rawlsing_next/pre553_temporal_comparability.py:: --brief
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm reverse CODE:d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1:rawlsing_next/pre553_temporal_comparability.py:: --route HR-F7-TEMP F7 --brief
```

```json
{
  "actual_forward": {
    "hops": [
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:FUNCTION:F7",
            "id": "EDGE:569f67c91d0a2bec99baa4d4",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
            "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "PYAT:FUNCTION:F7",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
            "id": "EDGE:e2185d11e13632b80e0e1740",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
            "to": "CODE:d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1:rawlsing_next/pre553_temporal_comparability.py::",
            "type": "HISTORICAL_VARIANT"
          }
        ],
        "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "CODE:d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1:rawlsing_next/pre553_temporal_comparability.py::"
      }
    ],
    "ids": [
      "PYAT:FUNCTION:F7",
      "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
      "CODE:d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1:rawlsing_next/pre553_temporal_comparability.py::"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "actual_reverse": {
    "hops": [
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
            "id": "EDGE:e2185d11e13632b80e0e1740",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
            "to": "CODE:d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1:rawlsing_next/pre553_temporal_comparability.py::",
            "type": "HISTORICAL_VARIANT"
          }
        ],
        "from": "CODE:d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1:rawlsing_next/pre553_temporal_comparability.py::",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:FUNCTION:F7",
            "id": "EDGE:569f67c91d0a2bec99baa4d4",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
            "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:FUNCTION:F7"
      }
    ],
    "ids": [
      "CODE:d8a03fcdf77ca791d7f66ce58e2ed3b3d894bbb1:rawlsing_next/pre553_temporal_comparability.py::",
      "ROW:G:HISTORICAL_REALIZATIONS:HR-F7-TEMP",
      "PYAT:FUNCTION:F7"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "same_edge_ids": true
}
```

## T6

```sh
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm focus M2_LOCAL_RELEASE --route H05-I01 N9 H06-E03 HR-N9-N10W CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py:: --brief
/usr/local/bin/python3 -m rawlsing_next.programma_pyat_reference --store /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/w1h-replay-rkp8_z0d/warm reverse CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py:: --route HR-N9-N10W H06-E03 N9 H05-I01 M2_LOCAL_RELEASE --brief
```

```json
{
  "actual_forward": {
    "hops": [
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:PLAN:M2_LOCAL_RELEASE",
            "id": "EDGE:3f65116e2143ddb048f3a3f9",
            "record": "ROW:H:ADJUDICATION:H05-I01",
            "to": "ROW:H:ADJUDICATION:H05-I01",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "PYAT:PLAN:M2_LOCAL_RELEASE",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:H:ADJUDICATION:H05-I01"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:ASTRA:N9",
            "id": "EDGE:1cf7575775fc53c8c10ddea7",
            "record": "ROW:H:ADJUDICATION:H05-I01",
            "to": "ROW:H:ADJUDICATION:H05-I01",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "ROW:H:ADJUDICATION:H05-I01",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N9"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:ASTRA:N9",
            "id": "EDGE:39479d163cb856aa166fb7b7",
            "record": "ROW:H:ADJUDICATION:H06-E03",
            "to": "ROW:H:ADJUDICATION:H06-E03",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "PYAT:ASTRA:N9",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:H:ADJUDICATION:H06-E03"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:H:ADJUDICATION:H06-E03",
            "id": "EDGE:fa2ebdb17453d310128affd1",
            "record": "ROW:H:ADJUDICATION:H06-E03",
            "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
            "type": "RECONCILES_WITHOUT_PROMOTION"
          }
        ],
        "from": "ROW:H:ADJUDICATION:H06-E03",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
            "id": "EDGE:2af2c1b241455dfb6b03be0b",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
            "to": "CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py::",
            "type": "CURRENT_COMPARISON"
          }
        ],
        "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py::"
      }
    ],
    "ids": [
      "PYAT:PLAN:M2_LOCAL_RELEASE",
      "ROW:H:ADJUDICATION:H05-I01",
      "PYAT:ASTRA:N9",
      "ROW:H:ADJUDICATION:H06-E03",
      "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
      "CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py::"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "actual_reverse": {
    "hops": [
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
            "id": "EDGE:2af2c1b241455dfb6b03be0b",
            "record": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
            "to": "CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py::",
            "type": "CURRENT_COMPARISON"
          }
        ],
        "from": "CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py::",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "ROW:H:ADJUDICATION:H06-E03",
            "id": "EDGE:fa2ebdb17453d310128affd1",
            "record": "ROW:H:ADJUDICATION:H06-E03",
            "to": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
            "type": "RECONCILES_WITHOUT_PROMOTION"
          }
        ],
        "from": "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:H:ADJUDICATION:H06-E03"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:ASTRA:N9",
            "id": "EDGE:39479d163cb856aa166fb7b7",
            "record": "ROW:H:ADJUDICATION:H06-E03",
            "to": "ROW:H:ADJUDICATION:H06-E03",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "ROW:H:ADJUDICATION:H06-E03",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:ASTRA:N9"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:ASTRA:N9",
            "id": "EDGE:1cf7575775fc53c8c10ddea7",
            "record": "ROW:H:ADJUDICATION:H05-I01",
            "to": "ROW:H:ADJUDICATION:H05-I01",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "PYAT:ASTRA:N9",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "ROW:H:ADJUDICATION:H05-I01"
      },
      {
        "edges": [
          {
            "condition": null,
            "from": "PYAT:PLAN:M2_LOCAL_RELEASE",
            "id": "EDGE:3f65116e2143ddb048f3a3f9",
            "record": "ROW:H:ADJUDICATION:H05-I01",
            "to": "ROW:H:ADJUDICATION:H05-I01",
            "type": "HAS_ASSERTION"
          }
        ],
        "from": "ROW:H:ADJUDICATION:H05-I01",
        "proof_scope": "NAVIGATION_ONLY; read each edge type/condition, including missing edges",
        "to": "PYAT:PLAN:M2_LOCAL_RELEASE"
      }
    ],
    "ids": [
      "CODE:ee31e3edfb1b5a26aa945a55ededbf0b7ff2a7a7:rawlsing_next/pre553_n9_n10w_progressive_candidate.py::",
      "ROW:G:HISTORICAL_REALIZATIONS:HR-N9-N10W",
      "ROW:H:ADJUDICATION:H06-E03",
      "PYAT:ASTRA:N9",
      "ROW:H:ADJUDICATION:H05-I01",
      "PYAT:PLAN:M2_LOCAL_RELEASE"
    ],
    "reverse_uses_same_edge_ids": true
  },
  "same_edge_ids": true
}
```
