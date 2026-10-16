# SOROK HQ317 C07P — real cross-process evidence

Captured from actual `subprocess.run` invocations of three separate interpreters.

## Process A — build and persist

```
{
  "fingerprint": {
    "capsule_fields": {
      "cap-A": {
        "capsule_id": "cap-A",
        "coder_rubric_digest": "crd-cap-A",
        "content_digest": "cd-cap-A",
        "contribution_digest": "contrib-cap-A",
        "expired": false,
        "family_graph_digest": "fgd-cap-A",
        "freeze_timestamp": 1000.0,
        "generation_history_digest": "ghd-cap-A",
        "hidden_projection_digest": "hpd-cap-A",
        "lawful_set_digest": "lsd-cap-A",
        "public_projection_digest": "ppd-cap-A",
        "purpose": "SOURCEFREE_TEST_ONLY",
        "rejected_alternatives_digest": "rad-cap-A",
        "revoked": false,
        "scenario_frame": "frame-A",
        "schema_version": "1.0",
        "split_assignment_digest": "sad-cap-A",
        "version": 1
      }
    },
    "commitments": {
      "cap-A": "42188c0603871e6452044a27b9efed6c85dbc8dcbd992482c98e64746f654126"
    },
    "committed_ids": [
      "cap-A"
    ],
    "exposure_rows": [
      [
        "cap-A",
        "coder-7",
        "development"
      ]
    ],
    "holder_roles": {
      "custodian-alice": "CUSTODIAN",
      "holder": "CUSTODIAN",
      "runner1": "CUSTODIAN"
    },
    "integrity": true,
    "ledger_ops": [
      "COMMIT",
      "UNBLIND",
      "RELEASE",
      "EXPOSURE"
    ],
    "ledger_seq": [
      1,
      2,
      3,
      4
    ],
    "released": [
      "cap-A"
    ],
    "unblinded_holders": {
      "cap-A": "custodian-alice"
    },
    "unblinded_ids": [
      "cap-A"
    ]
  },
  "journal_records": 6,
  "provenance": {
    "bytes": 36648,
    "cwd": "/Users/matthewsmith/Desktop/Rawlsing",
    "git_blob_sha1": "4c185c18dbee57603038e97886da8fc4aa834082",
    "module_file": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07p-wt/WORKER_RETURNS/SOROK-R3-HQ317-C07P-CROSSPROCESS-CUSTODY-R1/repro/source/custody_protocol.py",
    "pid": 52299,
    "python": "3.11.3",
    "sha256": "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"
  },
  "role": "phaseA"
}
```

## Process B — cold restore in an independent interpreter

```
{
  "fingerprint": {
    "capsule_fields": {
      "cap-A": {
        "capsule_id": "cap-A",
        "coder_rubric_digest": "crd-cap-A",
        "content_digest": "cd-cap-A",
        "contribution_digest": "contrib-cap-A",
        "expired": false,
        "family_graph_digest": "fgd-cap-A",
        "freeze_timestamp": 1000.0,
        "generation_history_digest": "ghd-cap-A",
        "hidden_projection_digest": "hpd-cap-A",
        "lawful_set_digest": "lsd-cap-A",
        "public_projection_digest": "ppd-cap-A",
        "purpose": "SOURCEFREE_TEST_ONLY",
        "rejected_alternatives_digest": "rad-cap-A",
        "revoked": false,
        "scenario_frame": "frame-A",
        "schema_version": "1.0",
        "split_assignment_digest": "sad-cap-A",
        "version": 1
      }
    },
    "commitments": {
      "cap-A": "42188c0603871e6452044a27b9efed6c85dbc8dcbd992482c98e64746f654126"
    },
    "committed_ids": [
      "cap-A"
    ],
    "exposure_rows": [
      [
        "cap-A",
        "coder-7",
        "development"
      ]
    ],
    "holder_roles": {
      "custodian-alice": "CUSTODIAN",
      "holder": "CUSTODIAN",
      "runner1": "CUSTODIAN"
    },
    "integrity": true,
    "ledger_ops": [
      "COMMIT",
      "UNBLIND",
      "RELEASE",
      "EXPOSURE"
    ],
    "ledger_seq": [
      1,
      2,
      3,
      4
    ],
    "released": [
      "cap-A"
    ],
    "unblinded_holders": {
      "cap-A": "custodian-alice"
    },
    "unblinded_ids": [
      "cap-A"
    ]
  },
  "provenance": {
    "bytes": 36648,
    "cwd": "/Users/matthewsmith/Desktop/Rawlsing",
    "git_blob_sha1": "4c185c18dbee57603038e97886da8fc4aa834082",
    "module_file": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07p-wt/WORKER_RETURNS/SOROK-R3-HQ317-C07P-CROSSPROCESS-CUSTODY-R1/repro/source/custody_protocol.py",
    "pid": 52300,
    "python": "3.11.3",
    "sha256": "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"
  },
  "restore": {
    "applied": 6,
    "chain": {
      "head": "28e87b33123d3b3f11c7b9a328eb47cf061ede40f9005cf4e835a5384dd9ba93",
      "ok": true,
      "records": 6
    },
    "integrity": true
  },
  "role": "phaseB"
}
```

## Process B — continue the authorised lifecycle after restore

```
{
  "continued_fingerprint": {
    "capsule_fields": {
      "cap-A": {
        "capsule_id": "cap-A",
        "coder_rubric_digest": "crd-cap-A",
        "content_digest": "cd-cap-A",
        "contribution_digest": "contrib-cap-A",
        "expired": false,
        "family_graph_digest": "fgd-cap-A",
        "freeze_timestamp": 1000.0,
        "generation_history_digest": "ghd-cap-A",
        "hidden_projection_digest": "hpd-cap-A",
        "lawful_set_digest": "lsd-cap-A",
        "public_projection_digest": "ppd-cap-A",
        "purpose": "SOURCEFREE_TEST_ONLY",
        "rejected_alternatives_digest": "rad-cap-A",
        "revoked": false,
        "scenario_frame": "frame-A",
        "schema_version": "1.0",
        "split_assignment_digest": "sad-cap-A",
        "version": 1
      },
      "cap-B": {
        "capsule_id": "cap-B",
        "coder_rubric_digest": "crd-cap-B",
        "content_digest": "cd-cap-B",
        "contribution_digest": "contrib-cap-B",
        "expired": false,
        "family_graph_digest": "fgd-cap-B",
        "freeze_timestamp": 1500.0,
        "generation_history_digest": "ghd-cap-B",
        "hidden_projection_digest": "hpd-cap-B",
        "lawful_set_digest": "lsd-cap-B",
        "public_projection_digest": "ppd-cap-B",
        "purpose": "SOURCEFREE_TEST_ONLY",
        "rejected_alternatives_digest": "rad-cap-B",
        "revoked": false,
        "scenario_frame": "frame-B",
        "schema_version": "1.0",
        "split_assignment_digest": "sad-cap-B",
        "version": 1
      }
    },
    "commitments": {
      "cap-A": "42188c0603871e6452044a27b9efed6c85dbc8dcbd992482c98e64746f654126",
      "cap-B": "b27dbaf6061533bd71152568bc9baaee4398bffdda8b5de40ebcb9f62a8c3371"
    },
    "committed_ids": [
      "cap-A",
      "cap-B"
    ],
    "exposure_rows": [
      [
        "cap-A",
        "coder-7",
        "development"
      ]
    ],
    "holder_roles": {
      "custodian-alice": "CUSTODIAN",
      "holder": "CUSTODIAN",
      "runner1": "CUSTODIAN",
      "runner9": "CUSTODIAN"
    },
    "integrity": true,
    "ledger_ops": [
      "COMMIT",
      "UNBLIND",
      "RELEASE",
      "EXPOSURE",
      "COMMIT",
      "UNBLIND",
      "RELEASE"
    ],
    "ledger_seq": [
      1,
      2,
      3,
      4,
      5,
      6,
      7
    ],
    "released": [
      "cap-A",
      "cap-B"
    ],
    "unblinded_holders": {
      "cap-A": "custodian-alice",
      "cap-B": "runner9"
    },
    "unblinded_ids": [
      "cap-A",
      "cap-B"
    ]
  },
  "fingerprint": {
    "capsule_fields": {
      "cap-A": {
        "capsule_id": "cap-A",
        "coder_rubric_digest": "crd-cap-A",
        "content_digest": "cd-cap-A",
        "contribution_digest": "contrib-cap-A",
        "expired": false,
        "family_graph_digest": "fgd-cap-A",
        "freeze_timestamp": 1000.0,
        "generation_history_digest": "ghd-cap-A",
        "hidden_projection_digest": "hpd-cap-A",
        "lawful_set_digest": "lsd-cap-A",
        "public_projection_digest": "ppd-cap-A",
        "purpose": "SOURCEFREE_TEST_ONLY",
        "rejected_alternatives_digest": "rad-cap-A",
        "revoked": false,
        "scenario_frame": "frame-A",
        "schema_version": "1.0",
        "split_assignment_digest": "sad-cap-A",
        "version": 1
      }
    },
    "commitments": {
      "cap-A": "42188c0603871e6452044a27b9efed6c85dbc8dcbd992482c98e64746f654126"
    },
    "committed_ids": [
      "cap-A"
    ],
    "exposure_rows": [
      [
        "cap-A",
        "coder-7",
        "development"
      ]
    ],
    "holder_roles": {
      "custodian-alice": "CUSTODIAN",
      "holder": "CUSTODIAN",
      "runner1": "CUSTODIAN"
    },
    "integrity": true,
    "ledger_ops": [
      "COMMIT",
      "UNBLIND",
      "RELEASE",
      "EXPOSURE"
    ],
    "ledger_seq": [
      1,
      2,
      3,
      4
    ],
    "released": [
      "cap-A"
    ],
    "unblinded_holders": {
      "cap-A": "custodian-alice"
    },
    "unblinded_ids": [
      "cap-A"
    ]
  },
  "journal_records_after": 10,
  "provenance": {
    "bytes": 36648,
    "cwd": "/Users/matthewsmith/Desktop/Rawlsing",
    "git_blob_sha1": "4c185c18dbee57603038e97886da8fc4aa834082",
    "module_file": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07p-wt/WORKER_RETURNS/SOROK-R3-HQ317-C07P-CROSSPROCESS-CUSTODY-R1/repro/source/custody_protocol.py",
    "pid": 52301,
    "python": "3.11.3",
    "sha256": "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"
  },
  "restore": {
    "applied": 6,
    "chain": {
      "head": "28e87b33123d3b3f11c7b9a328eb47cf061ede40f9005cf4e835a5384dd9ba93",
      "ok": true,
      "records": 6
    },
    "integrity": true
  },
  "role": "continueB"
}
```

## Field-by-field comparison

| field | process A | process B (restored) | equal |
|---|---|---|---|
| `capsule_fields` | `{"cap-A": {"capsule_id": "cap-A", "coder_rubric_digest": "cr` | `{"cap-A": {"capsule_id": "cap-A", "coder_rubric_digest": "cr` | YES |
| `commitments` | `{"cap-A": "42188c0603871e6452044a27b9efed6c85dbc8dcbd992482c` | `{"cap-A": "42188c0603871e6452044a27b9efed6c85dbc8dcbd992482c` | YES |
| `committed_ids` | `["cap-A"]` | `["cap-A"]` | YES |
| `exposure_rows` | `[["cap-A", "coder-7", "development"]]` | `[["cap-A", "coder-7", "development"]]` | YES |
| `holder_roles` | `{"custodian-alice": "CUSTODIAN", "holder": "CUSTODIAN", "run` | `{"custodian-alice": "CUSTODIAN", "holder": "CUSTODIAN", "run` | YES |
| `integrity` | `true` | `true` | YES |
| `ledger_ops` | `["COMMIT", "UNBLIND", "RELEASE", "EXPOSURE"]` | `["COMMIT", "UNBLIND", "RELEASE", "EXPOSURE"]` | YES |
| `ledger_seq` | `[1, 2, 3, 4]` | `[1, 2, 3, 4]` | YES |
| `released` | `["cap-A"]` | `["cap-A"]` | YES |
| `unblinded_holders` | `{"cap-A": "custodian-alice"}` | `{"cap-A": "custodian-alice"}` | YES |
| `unblinded_ids` | `["cap-A"]` | `["cap-A"]` | YES |

Distinct OS PIDs: A=52299 B=52300 -> **distinct**

Module actually imported, both processes: blob `4c185c18dbee57603038e97886da8fc4aa834082`, sha256 `ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b`, 36648 bytes

Journal after continuation: 10 records.

Escrow event timestamps are deliberately excluded from the fingerprint: the native public
API re-stamps them on replay. That is typed hold `C07_DEPENDENCY_TS`, not a silent pass.
