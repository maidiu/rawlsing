# SOROK HQ318 C07I — independent cold-process custody evidence

Produced by the reviewer's OWN worker `repro/c07i_worker.py`, not by the author's `c07_worker.py`,
so the A->B claim does not depend on the candidate's own helper. Real `subprocess.run`, real
interpreters, real filesystem.

**Distinct PIDs:** A=`63441`  B=`63442`  C=`63443`
**Module imported (all three):** `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07i-wt/WORKER_RETURNS/SOROK-R3-HQ318-C07I-C07P-INDEPENDENT-R1/repro/source/custody_protocol.py`
**Git blob:** `4c185c18dbee57603038e97886da8fc4aa834082`  **SHA256:** `ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b`  **bytes:** 36648

## Process A - build and persist (reviewer role `build`)

```json
{
  "identity": {
    "capsule_18_fields": {
      "cap-A": {
        "capsule_id": "cap-A",
        "coder_rubric_digest": "crd-cap-A",
        "content_digest": "cd-cap-A",
        "contribution_digest": "contrib-cap-A",
        "expired": false,
        "family_graph_digest": "fgd-cap-A",
        "freeze_timestamp": 1111.0,
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
    "committed_ids": [
      "cap-A"
    ],
    "escrow_ledger_ts": [
      1792186379.967896,
      1792186379.969177,
      1792186379.970371,
      1792186379.971839
    ],
    "escrow_unblinded_at": {
      "cap-A": 1792186379.9691641
    },
    "exposures": [
      [
        "cap-A",
        "coder-reviewer",
        "development"
      ]
    ],
    "holders": {
      "custodian-alice": "CUSTODIAN",
      "custodian-zoe": "CUSTODIAN",
      "holder": "CUSTODIAN",
      "runner1": "CUSTODIAN"
    },
    "integrity": true,
    "ledger": [
      [
        1,
        "COMMIT",
        "cap-A"
      ],
      [
        2,
        "UNBLIND",
        "cap-A"
      ],
      [
        3,
        "RELEASE",
        "cap-A"
      ],
      [
        4,
        "EXPOSURE",
        "cap-A"
      ]
    ],
    "released": [
      "cap-A"
    ],
    "seals": {
      "cap-A": "f933afde9cddf2c136a301d64ce86f6ff9e128d25ee0d8510d95f6b003ed0db7"
    },
    "unblinded": {
      "cap-A": "custodian-zoe"
    }
  },
  "journal_bytes": 1848,
  "journal_head": "ecb644222279b8367133aac58295b713336d1a04a8dcc97174562768f54c7d2d",
  "journal_records": 5,
  "provenance": {
    "argv_role": "build",
    "bytes": 36648,
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07i-wt",
    "git_blob_sha1": "4c185c18dbee57603038e97886da8fc4aa834082",
    "module_file": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07i-wt/WORKER_RETURNS/SOROK-R3-HQ318-C07I-C07P-INDEPENDENT-R1/repro/source/custody_protocol.py",
    "pid": 63441,
    "python": "3.11.3",
    "sha256": "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"
  },
  "role": "build"
}
```

## Process B - cold restore in an independent interpreter (role `recover`)

```json
{
  "identity": {
    "capsule_18_fields": {
      "cap-A": {
        "capsule_id": "cap-A",
        "coder_rubric_digest": "crd-cap-A",
        "content_digest": "cd-cap-A",
        "contribution_digest": "contrib-cap-A",
        "expired": false,
        "family_graph_digest": "fgd-cap-A",
        "freeze_timestamp": 1111.0,
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
    "committed_ids": [
      "cap-A"
    ],
    "escrow_ledger_ts": [
      1792186380.089189,
      1792186380.089341,
      1792186380.089503,
      1792186380.0896719
    ],
    "escrow_unblinded_at": {
      "cap-A": 1792186380.089331
    },
    "exposures": [
      [
        "cap-A",
        "coder-reviewer",
        "development"
      ]
    ],
    "holders": {
      "custodian-alice": "CUSTODIAN",
      "custodian-zoe": "CUSTODIAN",
      "holder": "CUSTODIAN",
      "runner1": "CUSTODIAN"
    },
    "integrity": true,
    "ledger": [
      [
        1,
        "COMMIT",
        "cap-A"
      ],
      [
        2,
        "UNBLIND",
        "cap-A"
      ],
      [
        3,
        "RELEASE",
        "cap-A"
      ],
      [
        4,
        "EXPOSURE",
        "cap-A"
      ]
    ],
    "released": [
      "cap-A"
    ],
    "seals": {
      "cap-A": "f933afde9cddf2c136a301d64ce86f6ff9e128d25ee0d8510d95f6b003ed0db7"
    },
    "unblinded": {
      "cap-A": "custodian-zoe"
    }
  },
  "journal_exposure_ts": [
    1792186379.971825
  ],
  "journal_head": "ecb644222279b8367133aac58295b713336d1a04a8dcc97174562768f54c7d2d",
  "journal_unblinded_at": [
    1792186379.9691641
  ],
  "provenance": {
    "argv_role": "recover",
    "bytes": 36648,
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07i-wt",
    "git_blob_sha1": "4c185c18dbee57603038e97886da8fc4aa834082",
    "module_file": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07i-wt/WORKER_RETURNS/SOROK-R3-HQ318-C07I-C07P-INDEPENDENT-R1/repro/source/custody_protocol.py",
    "pid": 63442,
    "python": "3.11.3",
    "sha256": "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"
  },
  "restore": {
    "applied": 5,
    "chain": {
      "head": "ecb644222279b8367133aac58295b713336d1a04a8dcc97174562768f54c7d2d",
      "ok": true,
      "records": 5
    },
    "integrity": true
  },
  "role": "recover"
}
```

## Process B - continue the authorised lifecycle after restore (role `continue`)

```json
{
  "identity_after_continue": {
    "capsule_18_fields": {
      "cap-A": {
        "capsule_id": "cap-A",
        "coder_rubric_digest": "crd-cap-A",
        "content_digest": "cd-cap-A",
        "contribution_digest": "contrib-cap-A",
        "expired": false,
        "family_graph_digest": "fgd-cap-A",
        "freeze_timestamp": 1111.0,
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
        "freeze_timestamp": 2222.0,
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
    "committed_ids": [
      "cap-A",
      "cap-B"
    ],
    "escrow_ledger_ts": [
      1792186380.20835,
      1792186380.208572,
      1792186380.208725,
      1792186380.2088819,
      1792186380.2106261,
      1792186380.211972,
      1792186380.21327,
      1792186380.2146418
    ],
    "escrow_unblinded_at": {
      "cap-A": 1792186380.208558,
      "cap-B": 1792186380.2119591
    },
    "exposures": [
      [
        "cap-A",
        "coder-reviewer",
        "development"
      ],
      [
        "cap-B",
        "coder-reviewer",
        "development"
      ]
    ],
    "holders": {
      "custodian-alice": "CUSTODIAN",
      "custodian-zoe": "CUSTODIAN",
      "holder": "CUSTODIAN",
      "runner1": "CUSTODIAN"
    },
    "integrity": true,
    "ledger": [
      [
        1,
        "COMMIT",
        "cap-A"
      ],
      [
        2,
        "UNBLIND",
        "cap-A"
      ],
      [
        3,
        "RELEASE",
        "cap-A"
      ],
      [
        4,
        "EXPOSURE",
        "cap-A"
      ],
      [
        5,
        "COMMIT",
        "cap-B"
      ],
      [
        6,
        "UNBLIND",
        "cap-B"
      ],
      [
        7,
        "RELEASE",
        "cap-B"
      ],
      [
        8,
        "EXPOSURE",
        "cap-B"
      ]
    ],
    "released": [
      "cap-A",
      "cap-B"
    ],
    "seals": {
      "cap-A": "f933afde9cddf2c136a301d64ce86f6ff9e128d25ee0d8510d95f6b003ed0db7",
      "cap-B": "e6a26efa642594824809d762c9bc3d41552b80e8e1bf6ec876acb14faa402f76"
    },
    "unblinded": {
      "cap-A": "custodian-zoe",
      "cap-B": "custodian-zoe"
    }
  },
  "identity_after_restore": {
    "capsule_18_fields": {
      "cap-A": {
        "capsule_id": "cap-A",
        "coder_rubric_digest": "crd-cap-A",
        "content_digest": "cd-cap-A",
        "contribution_digest": "contrib-cap-A",
        "expired": false,
        "family_graph_digest": "fgd-cap-A",
        "freeze_timestamp": 1111.0,
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
    "committed_ids": [
      "cap-A"
    ],
    "escrow_ledger_ts": [
      1792186380.20835,
      1792186380.208572,
      1792186380.208725,
      1792186380.2088819
    ],
    "escrow_unblinded_at": {
      "cap-A": 1792186380.208558
    },
    "exposures": [
      [
        "cap-A",
        "coder-reviewer",
        "development"
      ]
    ],
    "holders": {
      "custodian-alice": "CUSTODIAN",
      "custodian-zoe": "CUSTODIAN",
      "holder": "CUSTODIAN",
      "runner1": "CUSTODIAN"
    },
    "integrity": true,
    "ledger": [
      [
        1,
        "COMMIT",
        "cap-A"
      ],
      [
        2,
        "UNBLIND",
        "cap-A"
      ],
      [
        3,
        "RELEASE",
        "cap-A"
      ],
      [
        4,
        "EXPOSURE",
        "cap-A"
      ]
    ],
    "released": [
      "cap-A"
    ],
    "seals": {
      "cap-A": "f933afde9cddf2c136a301d64ce86f6ff9e128d25ee0d8510d95f6b003ed0db7"
    },
    "unblinded": {
      "cap-A": "custodian-zoe"
    }
  },
  "journal_records_after": 10,
  "provenance": {
    "argv_role": "continue",
    "bytes": 36648,
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07i-wt",
    "git_blob_sha1": "4c185c18dbee57603038e97886da8fc4aa834082",
    "module_file": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c07i-wt/WORKER_RETURNS/SOROK-R3-HQ318-C07I-C07P-INDEPENDENT-R1/repro/source/custody_protocol.py",
    "pid": 63443,
    "python": "3.11.3",
    "sha256": "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"
  },
  "restore": {
    "applied": 5,
    "chain": {
      "head": "ecb644222279b8367133aac58295b713336d1a04a8dcc97174562768f54c7d2d",
      "ok": true,
      "records": 5
    },
    "integrity": true
  },
  "role": "continue"
}
```

## A vs B field-by-field

| field | A | B (restored) | equal |
|---|---|---|---|
| `capsule_18_fields` | `{"cap-A": {"capsule_id": "cap-A", "coder_rubric_dige` | `{"cap-A": {"capsule_id": "cap-A", "coder_rubric_dige` | YES |
| `committed_ids` | `["cap-A"]` | `["cap-A"]` | YES |
| `escrow_ledger_ts` | `[1792186379.967896, 1792186379.969177, 1792186379.97` | `[1792186380.089189, 1792186380.089341, 1792186380.08` | NO - see notes |
| `escrow_unblinded_at` | `{"cap-A": 1792186379.9691641}` | `{"cap-A": 1792186380.089331}` | NO - see notes |
| `exposures` | `[["cap-A", "coder-reviewer", "development"]]` | `[["cap-A", "coder-reviewer", "development"]]` | YES |
| `holders` | `{"custodian-alice": "CUSTODIAN", "custodian-zoe": "C` | `{"custodian-alice": "CUSTODIAN", "custodian-zoe": "C` | YES |
| `integrity` | `true` | `true` | YES |
| `ledger` | `[[1, "COMMIT", "cap-A"], [2, "UNBLIND", "cap-A"], [3` | `[[1, "COMMIT", "cap-A"], [2, "UNBLIND", "cap-A"], [3` | YES |
| `released` | `["cap-A"]` | `["cap-A"]` | YES |
| `seals` | `{"cap-A": "f933afde9cddf2c136a301d64ce86f6ff9e128d25` | `{"cap-A": "f933afde9cddf2c136a301d64ce86f6ff9e128d25` | YES |
| `unblinded` | `{"cap-A": "custodian-zoe"}` | `{"cap-A": "custodian-zoe"}` | YES |

## Timestamp hold, measured (IP10 / IH-T1)

- journal `unblinded_at` as written by A: `[1792186379.9691641]`
- escrow `unblinded_at` observed in A: `{'cap-A': 1792186379.9691641}`
- escrow `unblinded_at` reconstructed in B: `{'cap-A': 1792186380.089331}`

The journal is faithful; the **reconstructed escrow re-stamps** the event time. Integrity is still
`True` in B, which is exactly why this hold is silent rather than loud. `unblind` and
`record_exposure` expose no timestamp parameter, so it cannot be closed from outside the native API.

## Continuation after restore

- committed: `['cap-A']` -> `['cap-A', 'cap-B']`
- released: `['cap-A']` -> `['cap-A', 'cap-B']`
- integrity after continuing: `True`
- journal records after: `10`

Reviewer finding: the A->B claim is **independently reproduced with reviewer-authored tooling**.
