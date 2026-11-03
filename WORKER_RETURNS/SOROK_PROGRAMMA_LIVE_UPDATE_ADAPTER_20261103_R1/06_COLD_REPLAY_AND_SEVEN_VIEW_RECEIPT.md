# SOROK-LIVE-02-R1 — cold replay and seven-view receipt

**Status: `COLD_REPLAY_VERIFIED__7_OF_7_VIEWS_EXECUTED` at execution content SHA `bbcc46bf3b7aadfc582e284daea61f99060e0fc3`. This is machine output, not independent acceptance. No actual Sorok/Pyat production state, journal, snapshot, or W8-R guide file was read or written by this demonstration.**

## 1. Boundary

| Item | Value |
|---|---|
| Repository | `maidiu/rawlsing` |
| Branch | `agent/sorok-programma-live-update-adapter-20261103-r1` |
| Execution commit | `bbcc46bf3b7aadfc582e284daea61f99060e0fc3` (C1) |
| Starting SHA | `fe7b7c32bfe8aa508f556af649628930c12d9210` |
| Frozen guide | `a9ebf71e62d84e5dcc599662e976eca7fcd0e623` |
| Temporary state root | `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold` |
| Python | 3.11.3 |
| pytest | 9.1.1 |
| Working tree at C1 | clean |
| Runtime | Python CLI invocations, no daemon |
| Native / human / owner claim | NONE ISSUED |
| Guide mutation | NONE |
| Production state mutation | NONE |

The demonstration used a disposable state and journal outside the repository. The journal is the only durable input to replay; `state.json` and `SNAPSHOT.json` are derived files.

## 2. Exact command sequence

Each command below was a separate `python3` process. The intake process exited before the next command; the replay process was started only after `state.json` and `SNAPSHOT.json` were removed. The complete runnable transcript, including every `python3 -c` body, is `cold_replay/19_cold_replay_commands.sh`; the elided bodies in the block below are reproduced verbatim there.

```sh
export D=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold
cd SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1
export PYTHONDONTWRITEBYTECODE=1

python3 -c 'import living_reference as lr; ... GENESIS at 2026-11-03T12:00:00+00:00 ...'
python3 live_update_adapter.py --state "$D/state.json" freshness
python3 live_update_adapter.py --state "$D/state.json" intake fixtures/join_e_scoped_review.json --expected-head 21245d2a7f8233a5448cb6b42d2bd1ed26b2eaf017df822680c98e8444b89970
python3 live_update_adapter.py --state "$D/state.json" intake fixtures/s35_authored_sourcefree.json --expected-head 4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3
python3 live_update_adapter.py --state "$D/state.json" intake fixtures/rrif_r2_negative.json --expected-head 326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59
python3 -c '... read_journal and journal_head ...'
python3 -c '... load warm state ...'
cp "$D/state.json" "$D/state.warm.json"
rm -f "$D/state.json" "$D/SNAPSHOT.json"
python3 live_update_adapter.py --state "$D/state.json" freshness   # cold replay from journal only
python3 -c '... load cold state ...'
python3 live_update_adapter.py --state "$D/state.json" whole
python3 live_update_adapter.py --state "$D/state.json" focus C12@INTEGRATE
python3 live_update_adapter.py --state "$D/state.json" source-to-product E021@VERIFY
python3 live_update_adapter.py --state "$D/state.json" goal C9@INTEGRATE
python3 live_update_adapter.py --state "$D/state.json" work-now
python3 live_update_adapter.py --state "$D/state.json" changes-since a9ebf71e62d84e5dcc599662e976eca7fcd0e623
python3 live_update_adapter.py --state "$D/state.json" freshness
python3 live_update_adapter.py --state "$D/state.json" candidate-patch
```

The raw outputs are committed under `cold_replay/`. The full JSON shown below is the verbatim process stdout.

## 3. Head transitions

| Transition | Successor journal head | Previous event hash | Sequence | Status |
|---|---|---|---:|---|
| GENESIS | `21245d2a7f8233a5448cb6b42d2bd1ed26b2eaf017df822680c98e8444b89970` | `GENESIS` | 1 | `EVENT_APPENDED` |
| JOIN-E scoped review | `4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3` | `21245d2a7f8233a5448cb6b42d2bd1ed26b2eaf017df822680c98e8444b89970` | 2 | `SCOPED_SOURCEFREE_ACCEPTED` |
| S35 authored sourcefree return | `326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59` | `4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3` | 3 | `SOURCE_PRESENT_CANDIDATE` |
| RRIF-R2 independent negative | `57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93` | `326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59` | 4 | `EXACT_NEGATIVE_REVIEWED` |

## 4. Intake transcripts

### 4.1 JOIN-E

```json
{
  "applied": {
    "event_id": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
    "kind": "PROGRAMMA_DELTA",
    "status": "SCOPED_SOURCEFREE_ACCEPTED"
  },
  "axes": {
    "JOIN_E_7BF": {
      "authority": "NOT_ADOPTED",
      "consumer": "NONE_PROVEN_AT_PREMAIN",
      "engineering": "SOURCE_DEFINITION_ONLY",
      "human": "NOT_PROVEN",
      "operational": "CANDIDATE_ONLY",
      "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
      "science": "NOT_ISSUED",
      "source_recovery": "SOURCE_EXACT"
    }
  },
  "event": {
    "actor": {
      "principal": "SOURCE_DERIVED_NOT_HQ_IDENTITY",
      "role": "CANDIDATE_INTAKE",
      "verified": false
    },
    "created_at": "2026-11-03T18:50:12.912105+00:00",
    "event_id": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
    "kind": "PROGRAMMA_DELTA",
    "payload": {
      "coordinate": {
        "code": {
          "blob": "dc0894289e8b6a5e66148189e41d7efb563f25af",
          "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
          "object_type": "blob",
          "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/joined/session.py"
        },
        "code_sha": "7bf2da302996491ddf34b9a039fea47ac982d135",
        "first_consumer_symbol": "class JoinedSession",
        "root": "JOIN_E_7BF_SOURCEFREE",
        "scope": "SOURCEFREE_FORK_COLD_7BF",
        "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135"
      },
      "grade": "SOURCEFREE_SCOPED",
      "guide_ref": "E021@VERIFY",
      "guide_sha": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
      "kind": "SCOPED_REVIEW",
      "locator": {
        "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md",
        "quote": "TEST_ONLY_SOURCEFREE"
      },
      "next_evidence": "Joint C9 writer/C12 reader exact schema/root/ACK/anchor owner selection, separate new-tuple cold/severance and independent review. No native grant.",
      "node_id": "JOIN_E_7BF",
      "owner_slot": "JOIN_E_OWNER",
      "prior_negative": [
        "RRIF_R2_8090_REVISE_PERSISTS_OTHER_CUT"
      ],
      "return_sha": "7bf2da302996491ddf34b9a039fea47ac982d135",
      "review": {
        "blob": "52dfc715bed3ef14cc3dc4639132c409c4e99712",
        "commit": "4387dc818a96fda2d5271672505fbd9da1059703",
        "object_type": "blob",
        "path": "WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md"
      },
      "schema": "SOROK_PROGRAMMA_DELTA@1",
      "source": {
        "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
        "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
        "object_type": "blob",
        "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
      },
      "subject_sha": "7bf2da302996491ddf34b9a039fea47ac982d135",
      "transition_id": "JOIN_E_7BF_SCOPED_REVIEW"
    },
    "prev_event_hash": "21245d2a7f8233a5448cb6b42d2bd1ed26b2eaf017df822680c98e8444b89970",
    "schema": "SOROK_PROGRAMMA_EVIDENCE_JOURNAL@1",
    "sequence": 2,
    "source": {
      "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
      "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
      "object_type": "blob",
      "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
    }
  },
  "expected_head": "21245d2a7f8233a5448cb6b42d2bd1ed26b2eaf017df822680c98e8444b89970",
  "head": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
  "journal_head": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
  "revision": 2,
  "stale_expected_head": false,
  "state_digest": "465ee8c3d2d693ae80ddc2fccf7c5e1dc83d4c0991fb48a6a21d89ba5c908845",
  "status": "EVENT_APPENDED"
}
```

### 4.2 S35

```json
{
  "applied": {
    "event_id": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
    "kind": "PROGRAMMA_DELTA",
    "status": "SOURCE_PRESENT_CANDIDATE"
  },
  "axes": {
    "CAN011_RULE_T_MISSING": {
      "authority": "NOT_ADOPTED",
      "consumer": "NONE_PROVEN_AT_PREMAIN",
      "engineering": "SOURCE_DEFINITION_ONLY",
      "human": "NOT_PROVEN",
      "operational": "CANDIDATE_ONLY",
      "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
      "science": "NOT_ISSUED",
      "source_recovery": "SOURCE_EXACT"
    }
  },
  "event": {
    "actor": {
      "principal": "SOURCE_DERIVED_NOT_HQ_IDENTITY",
      "role": "CANDIDATE_INTAKE",
      "verified": false
    },
    "created_at": "2026-11-03T18:50:22.437934+00:00",
    "event_id": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
    "kind": "PROGRAMMA_DELTA",
    "payload": {
      "coordinate": {
        "code": {
          "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
          "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
          "object_type": "blob",
          "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
        },
        "code_sha": "b65c75a9e62618690f7d02265bc9e850af549161",
        "first_consumer_symbol": "NONE",
        "producer_symbol": "def evaluate(",
        "root": "P1_S35_TEST_ONLY",
        "scope": "DOCUMENTARY_RETURN_ONLY",
        "source_cut": "b65c75a9e62618690f7d02265bc9e850af549161"
      },
      "grade": "TEST_ONLY_SOURCEFREE",
      "guide_ref": "O05@ACCEPT",
      "guide_sha": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
      "kind": "RETURN_CANDIDATE",
      "locator": {
        "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py",
        "quote": "T_NO_CHANGE = {"
      },
      "next_evidence": "Only a competent CAN011 original Rule T acquired-practice or genuinely evaluated O07 no-change issuance can promote native C9; isolate first-reader access and later performed E2.",
      "node_id": "CAN011_RULE_T_MISSING",
      "owner_slot": "CAN011_OWNER",
      "prior_negative": [
        "CAN011_RULE_T_UNISSUED"
      ],
      "return_sha": "b65c75a9e62618690f7d02265bc9e850af549161",
      "schema": "SOROK_PROGRAMMA_DELTA@1",
      "source": {
        "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
        "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
        "object_type": "blob",
        "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
      },
      "subject_sha": "b65c75a9e62618690f7d02265bc9e850af549161",
      "transition_id": "S35_P1_SOURCEFREE_RETURN_ONLY"
    },
    "prev_event_hash": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
    "schema": "SOROK_PROGRAMMA_EVIDENCE_JOURNAL@1",
    "sequence": 3,
    "source": {
      "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
      "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
      "object_type": "blob",
      "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
    }
  },
  "expected_head": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
  "head": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
  "journal_head": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
  "revision": 3,
  "stale_expected_head": false,
  "state_digest": "9df4090e4a4a21bd7abdaf6c3fc6775ffa7cb47c42b459994f5956cf8da943a8",
  "status": "EVENT_APPENDED"
}
```

### 4.3 RRIF-R2 negative

```json
{
  "applied": {
    "event_id": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
    "kind": "PROGRAMMA_DELTA",
    "status": "EXACT_NEGATIVE_REVIEWED"
  },
  "axes": {
    "JOIN_C12_HOLD": {
      "authority": "NOT_ADOPTED",
      "consumer": "NONE_PROVEN_AT_PREMAIN",
      "engineering": "SOURCE_DEFINITION_ONLY",
      "human": "NOT_PROVEN",
      "operational": "CANDIDATE_ONLY",
      "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
      "science": "NOT_ISSUED",
      "source_recovery": "SOURCE_EXACT"
    }
  },
  "event": {
    "actor": {
      "principal": "SOURCE_DERIVED_NOT_HQ_IDENTITY",
      "role": "CANDIDATE_INTAKE",
      "verified": false
    },
    "created_at": "2026-11-03T18:50:35.669332+00:00",
    "event_id": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
    "kind": "PROGRAMMA_DELTA",
    "payload": {
      "coordinate": {
        "first_consumer_symbol": "NONE",
        "root": "RRIF_R2_SOURCEFREE_598D",
        "scope": "SOURCEFREE_RRIF_R2_NEGATIVE",
        "source_cut": "598d9e9eaba5143950c63317705fd09104fbf463"
      },
      "grade": "INDEPENDENT_NEGATIVE_SOURCE",
      "guide_ref": "C12@VERIFY",
      "guide_sha": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
      "kind": "REVIEW_REVISE",
      "locator": {
        "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md",
        "quote": "20/20"
      },
      "next_evidence": "Repair exact R2-T1/M1/C1/D1, choose new C9/C12 tuple and cold verify with fresh independent reader; keep 7bf accepted only at 7bf.",
      "node_id": "JOIN_C12_HOLD",
      "owner_slot": "C9_C12_OWNER",
      "prior_negative": [
        "R2_T1",
        "R2_M1",
        "R2_C1",
        "R2_D1"
      ],
      "return_sha": "598d9e9eaba5143950c63317705fd09104fbf463",
      "review": {
        "blob": "38c201199c3153ca58926b2f96b3ba0220d2b651",
        "commit": "8090a1ea308ab17f302f55bb2639c3e4cd774c7a",
        "object_type": "blob",
        "path": "WORKER_RETURNS/SOROK_RRIF_R2_INDEPENDENT_HOSTILE_FIRST_CONSUMER_REVIEW_R1/00_RETURN.md"
      },
      "schema": "SOROK_PROGRAMMA_DELTA@1",
      "source": {
        "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
        "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
        "object_type": "blob",
        "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
      },
      "subject_sha": "598d9e9eaba5143950c63317705fd09104fbf463",
      "transition_id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE"
    },
    "prev_event_hash": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
    "schema": "SOROK_PROGRAMMA_EVIDENCE_JOURNAL@1",
    "sequence": 4,
    "source": {
      "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
      "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
      "object_type": "blob",
      "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
    }
  },
  "expected_head": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
  "head": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
  "journal_head": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
  "revision": 4,
  "stale_expected_head": false,
  "state_digest": "a3f84a2afb21546e023f30d69bfdd36e44f85395fccf874218de076968c4dba6",
  "status": "EVENT_APPENDED"
}
```

## 5. Journal chain

```json
{
  "count": 4,
  "head": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
  "events": [
    {
      "sequence": 1,
      "kind": "GENESIS",
      "event_id": "21245d2a7f8233a5448cb6b42d2bd1ed26b2eaf017df822680c98e8444b89970",
      "prev_event_hash": "GENESIS",
      "transition_id": null
    },
    {
      "sequence": 2,
      "kind": "PROGRAMMA_DELTA",
      "event_id": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
      "prev_event_hash": "21245d2a7f8233a5448cb6b42d2bd1ed26b2eaf017df822680c98e8444b89970",
      "transition_id": "JOIN_E_7BF_SCOPED_REVIEW"
    },
    {
      "sequence": 3,
      "kind": "PROGRAMMA_DELTA",
      "event_id": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
      "prev_event_hash": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
      "transition_id": "S35_P1_SOURCEFREE_RETURN_ONLY"
    },
    {
      "sequence": 4,
      "kind": "PROGRAMMA_DELTA",
      "event_id": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
      "prev_event_hash": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
      "transition_id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE"
    }
  ]
}
```

## 6. Warm state, process termination, and cold replay

Warm state before deleting the derived files:

```json
{
  "warm_state_digest": "a3f84a2afb21546e023f30d69bfdd36e44f85395fccf874218de076968c4dba6",
  "journal_head": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
  "revision": 4,
  "journal_applied": [
    "GENESIS",
    "SCOPED_SOURCEFREE_ACCEPTED",
    "SOURCE_PRESENT_CANDIDATE",
    "EXACT_NEGATIVE_REVIEWED"
  ],
  "programma_deltas": 3
}
```

The state and snapshot were removed, and a new process replayed the journal. Cold state:

```json
{
  "cold_state_digest": "a3f84a2afb21546e023f30d69bfdd36e44f85395fccf874218de076968c4dba6",
  "journal_head": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
  "revision": 4,
  "programma_deltas": 3
}
```

The warm and cold derived state digests are identical (`a3f84a2afb21546e023f30d69bfdd36e44f85395fccf874218de076968c4dba6`), as are the journal head (`57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93`) and revision (`4`). No warm in-memory object was reused: the warm process exited before deletion, and the cold process rebuilt from the four-event journal.

## 7. Seven entering-agent views

All seven commands loaded the same reconstructed state. The post-view digest remains `a3f84a2afb21546e023f30d69bfdd36e44f85395fccf874218de076968c4dba6` at head `57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93`.

### 7.1 `whole`

```json
{
  "candidate_live_updates": [
    {
      "affected_typed_edges_not_automatically_promoted": [],
      "current_node_axes": {
        "JOIN_C12_HOLD": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "REVISE_MATERIAL_DEFECTS_AT_EXACT_CUT",
            "event_id": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "REVIEW_REVISE_MATERIAL_AT_EXACT_CUT",
            "source": {
              "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
              "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [
        {
          "id": "G-C12-SF-VERIFY",
          "remaining": [
            "C12:LOCAL_GUIDE:READER_ROOT@INTEGRATE",
            "C12:LOCAL_GUIDE:NEW_TUPLE_COLD_SEVERANCE@VERIFY",
            "C12:LOCAL_GUIDE:ACTUAL_ANCHOR@VERIFY"
          ],
          "review_red_at_selected_cut": true,
          "review_red_source_cuts": [
            "598d9e9eaba5143950c63317705fd09104fbf463"
          ],
          "status": "BLOCKED_MEMBERS_UNISSUED"
        }
      ],
      "possible_reverse_targets_not_automatically_unlocked": [],
      "receipts": [
        {
          "code_reader": "NONE",
          "grade": "INDEPENDENT_NEGATIVE_SOURCE",
          "id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE",
          "kind": "REVIEW_REVISE",
          "next_evidence": "Repair exact R2-T1/M1/C1/D1, choose new C9/C12 tuple and cold verify with fresh independent reader; keep 7bf accepted only at 7bf.",
          "owner": "C9_C12_OWNER",
          "source": {
            "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
            "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
            "object_type": "blob",
            "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
          },
          "source_cut": "598d9e9eaba5143950c63317705fd09104fbf463",
          "status": "EXACT_NEGATIVE_REVIEWED"
        }
      ],
      "ref": "C12@VERIFY"
    },
    {
      "affected_typed_edges_not_automatically_promoted": [
        {
          "blocking": false,
          "edge_id": "G-S10-SPECIFY::3",
          "required_ref": "E021@VERIFY",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "S10@SPECIFY"
        },
        {
          "blocking": false,
          "edge_id": "G-E008-MATRIX::4",
          "required_ref": "E021@VERIFY",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY"
        }
      ],
      "current_node_axes": {
        "JOIN_E_7BF": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "SOURCEFREE_REVIEWED_AT_EXACT_7BF_ONLY",
            "event_id": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "INDEPENDENT_SCOPED_7BF_REVIEWED_SOURCEFREE_ONLY",
            "source": {
              "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
              "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "JOIN_E_7BF_SCOPED_REVIEW"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [],
      "possible_reverse_targets_not_automatically_unlocked": [
        "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY",
        "S10@SPECIFY"
      ],
      "receipts": [
        {
          "code_reader": "class JoinedSession",
          "grade": "SOURCEFREE_SCOPED",
          "id": "JOIN_E_7BF_SCOPED_REVIEW",
          "kind": "SCOPED_REVIEW",
          "next_evidence": "Joint C9 writer/C12 reader exact schema/root/ACK/anchor owner selection, separate new-tuple cold/severance and independent review. No native grant.",
          "owner": "JOIN_E_OWNER",
          "source": {
            "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
            "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
            "object_type": "blob",
            "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
          },
          "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135",
          "status": "SCOPED_SOURCEFREE_ACCEPTED"
        }
      ],
      "ref": "E021@VERIFY"
    },
    {
      "affected_typed_edges_not_automatically_promoted": [
        {
          "blocking": true,
          "edge_id": "G-C9-T-ANY::1",
          "required_ref": "O05@ACCEPT",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "C9@INTEGRATE"
        },
        {
          "blocking": true,
          "edge_id": "G-C9-T-IF-ACQUIRED::1",
          "required_ref": "O05@ACCEPT",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "C9@ACCEPT"
        }
      ],
      "current_node_axes": {
        "CAN011_RULE_T_MISSING": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "SOURCE_PRESENT_AUTHOR_TESTED_NOT_NATIVE",
            "event_id": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "UNREVIEWED_RETURN_CANDIDATE",
            "source": {
              "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
              "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
              "object_type": "blob",
              "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "S35_P1_SOURCEFREE_RETURN_ONLY"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [
        {
          "id": "G-O05-POSITIVE-ACCEPT",
          "remaining": [
            "O05:LOCAL_GUIDE:RULE_T_DISCRIMINATOR@SPECIFY",
            "C4:LOCAL_GUIDE:ACTOR_SOURCE@ACCEPT",
            "C8:LOCAL_GUIDE:ACTION_OMISSION@VERIFY"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "BLOCKED_MEMBERS_UNISSUED"
        },
        {
          "id": "G-C9-T-ANY",
          "remaining": [
            "O05@ACCEPT",
            "O07@ACCEPT"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "MODE_UNSELECTED_HOLD"
        },
        {
          "id": "G-C9-T-IF-ACQUIRED",
          "remaining": [
            "O05@ACCEPT"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "MODE_UNSELECTED_HOLD"
        }
      ],
      "possible_reverse_targets_not_automatically_unlocked": [
        "C9@ACCEPT",
        "C9@INTEGRATE"
      ],
      "receipts": [
        {
          "code_reader": "NONE",
          "grade": "TEST_ONLY_SOURCEFREE",
          "id": "S35_P1_SOURCEFREE_RETURN_ONLY",
          "kind": "RETURN_CANDIDATE",
          "next_evidence": "Only a competent CAN011 original Rule T acquired-practice or genuinely evaluated O07 no-change issuance can promote native C9; isolate first-reader access and later performed E2.",
          "owner": "CAN011_OWNER",
          "source": {
            "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
            "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
            "object_type": "blob",
            "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
          },
          "source_cut": "b65c75a9e62618690f7d02265bc9e850af549161",
          "status": "SOURCE_PRESENT_CANDIDATE"
        }
      ],
      "ref": "O05@ACCEPT"
    }
  ],
  "no_new_native_claim": true,
  "purpose": {
    "id": "PURPOSE_UNCHOSEN_NEIGHBOR",
    "kind": "UNCHOSEN_NEIGHBOR",
    "maturity": {
      "A": {
        "status": "PARTIAL"
      },
      "C": {
        "status": "TEST_ONLY"
      },
      "E": {
        "status": "MISSING"
      },
      "I": {
        "status": "PRESENT"
      },
      "T": {
        "status": "PARTIAL"
      },
      "V": {
        "status": "MISSING"
      }
    },
    "owner": "SOROK_ORIGINAL_PRODUCT_OWNER",
    "purpose": "The product begins with a neighbor rather than a user-selected attractive, useful or congenial persona. Attachment, trust, health, pleasure, compliance, intimacy, benefit, dependency and access remain distinct.",
    "source": {
      "blob": "b715c67766073ee363720020466ea979ac29653a",
      "commit": "865b5b01e1a27e99020cf2bb389af8cd4c874b57",
      "depth": "FULL_TEXT_READ",
      "path": "SOROK_PRODUCT_CONTROL_ROOM/01_PRODUCT_CHARTER.md",
      "quote": "Rawlsing presents a neighbor. Attachment, trust, health, pleasure, compliance, intimacy, benefit, dependency and access must remain distinct."
    },
    "status": "PROVISIONAL_PRODUCT_LAW_R1",
    "summary": "The product begins with a neighbor rather than a user-selected attractive, useful or congenial persona. Attachment, trust, health, pleasure, compliance, intimacy, benefit, dependency and access remain distinct.",
    "title": "Meet an unchosen neighbor whose life places a claim on the user"
  },
  "source_cut": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
  "unfinished": {
    "blocked": 11,
    "count": 40,
    "counts_by_stage": {
      "A": 5,
      "C": 11,
      "E": 7,
      "I": 0,
      "T": 7,
      "V": 11
    },
    "filter": {
      "domain": "",
      "stage": ""
    },
    "groups": [
      {
        "domain": "A5",
        "gaps": [
          {
            "affected_consumer": "A5",
            "alternatives": [],
            "blocked_by": [
              "science not issued",
              "owner authority held",
              "no human A5 evidence"
            ],
            "blockers": [],
            "consequence": "No human-product proof.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "A5",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "NOT_PROVEN"
            ],
            "falsifier": "No human-product proof.",
            "hq_judgment_required": true,
            "id": "GAP_NATIVE_A5",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Human participant trial distinct from sourcefree encounter.",
            "node": "A5",
            "owner": "Sorok human A5/research owner",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "No human-product proof.",
            "return_sha": null,
            "smallest_useful_next_action": "Human participant trial distinct from sourcefree encounter.",
            "source_backed": true,
            "status": "NOT_PROVEN"
          }
        ]
      },
      {
        "domain": "C11",
        "gaps": [
          {
            "affected_consumer": "C11",
            "alternatives": [],
            "blocked_by": [
              "science not issued",
              "owner authority held"
            ],
            "blockers": [],
            "consequence": "No native continuing person exists.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "C11",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCEFREE_OR_SOURCE_ONLY"
            ],
            "falsifier": "No native continuing person exists.",
            "hq_judgment_required": true,
            "id": "GAP_NATIVE_C4_C11_PERSON",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Separate native world/C11 person authority and actual C12 consumer.",
            "node": "C11",
            "owner": "Original Pyat/C11/C12 owners",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "No native continuing person exists.",
            "return_sha": null,
            "smallest_useful_next_action": "Separate native world/C11 person authority and actual C12 consumer.",
            "source_backed": true,
            "status": "SOURCEFREE_OR_SOURCE_ONLY"
          }
        ]
      },
      {
        "domain": "C9C12-R2",
        "gaps": [
          {
            "affected_consumer": "C9C12-R2",
            "alternatives": [],
            "blocked_by": [
              "owner authority held"
            ],
            "blockers": [],
            "consequence": "C12 durability remains sourcefree-only.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "C9C12-R2",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "CANDIDATE"
            ],
            "falsifier": "C12 durability remains sourcefree-only.",
            "hq_judgment_required": true,
            "id": "GAP_C9_C12_ANCHOR",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "External anchor, mirror/outbox and durable actor readset decision.",
            "node": "C9C12-R2",
            "owner": "C9R/BP4/C12 owners",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "C12 durability remains sourcefree-only.",
            "return_sha": null,
            "smallest_useful_next_action": "External anchor, mirror/outbox and durable actor readset decision.",
            "source_backed": true,
            "status": "CANDIDATE"
          }
        ]
      },
      {
        "domain": "ECONOMICS",
        "gaps": [
          {
            "affected_consumer": "business + user",
            "alternatives": [
              "subscription",
              "usage-based",
              "no-charge alpha"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Revenue rises when the actor manufactures distress or the user returns compulsively.",
            "dependencies": [
              "S5 flourishing",
              "S14 privacy/abuse"
            ],
            "domain": "ECONOMICS",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "05_PROGRAM_MAP S13",
              "01_PRODUCT_CHARTER anti-goals"
            ],
            "falsifier": "Revenue rises when the actor manufactures distress or the user returns compulsively.",
            "hq_judgment_required": true,
            "id": "GAP-S13-NONEXTRACTIVE-REVENUE",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "T",
              "A",
              "E",
              "C",
              "V"
            ],
            "next": "Specify a non-extractive price/notification/retention rule and an adverse-incentive falsifier before any monetization build.",
            "node": "S13",
            "owner": "SOROK_BUSINESS_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "S13: sell without making attachment, suffering or compulsive return the revenue engine",
            "smallest_useful_next_action": "Specify a non-extractive price/notification/retention rule and an adverse-incentive falsifier before any monetization build.",
            "source_backed": true,
            "status": "MISSING"
          }
        ]
      },
      {
        "domain": "EXPRESSION_BINDING",
        "gaps": [
          {
            "affected_consumer": "alpha user",
            "alternatives": [
              "two-call realizer",
              "batching/appellate alternative",
              "local phenomenal compositor"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Changing user preferences changes the objective outward occurrence itself, or hidden interiority becomes user-visible without an admissible cue.",
            "dependencies": [
              "C11",
              "V2",
              "M6"
            ],
            "domain": "EXPRESSION_BINDING",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "101 binding surface",
              "M6 semantic ceiling",
              "GT0 tested negative"
            ],
            "falsifier": "Changing user preferences changes the objective outward occurrence itself, or hidden interiority becomes user-visible without an admissible cue.",
            "hq_judgment_required": true,
            "id": "GAP-SOROK101-PHENOMENAL-MEMBRANE",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "E",
              "C",
              "V"
            ],
            "next": "Prototype the anti-mirror wall with one exact occurrence and a changed user-attention filter; measure whether the occurrence stays fixed.",
            "node": "SOROK_101_OUTWARD_OCCURRENCE",
            "owner": "C11_OWNER / V2_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "101: separate objective actor/world occurrence from user-phenomenal access and hidden interiority",
            "smallest_useful_next_action": "Prototype the anti-mirror wall with one exact occurrence and a changed user-attention filter; measure whether the occurrence stays fixed.",
            "source_backed": true,
            "status": "PROPOSED"
          }
        ]
      },
      {
        "domain": "HUMAN_ALPHA",
        "gaps": [
          {
            "affected_consumer": "A5",
            "alternatives": [
              "lab demo",
              "sourcefree reader",
              "actual participant study"
            ],
            "blocked_by": [
              "native C11 source",
              "C9/C12 actor",
              "ethics approval"
            ],
            "blockers": [],
            "consequence": "A sourcefree or native code pass is presented as human validation.",
            "dependencies": [
              "C11 native source",
              "C9/C12",
              "ethics"
            ],
            "domain": "HUMAN_ALPHA",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "100/101 alpha constraints",
              "P1 TEST_ONLY trajectory",
              "Astra P1-P3 proposals"
            ],
            "falsifier": "A sourcefree or native code pass is presented as human validation.",
            "hq_judgment_required": true,
            "id": "GAP-A5-HUMAN-ALPHA",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "missing_stages": [
              "C",
              "V"
            ],
            "next": "Design a bounded consented participant study with actor-independent outcome measures and negative cases; do not infer A5 from code tests.",
            "node": "A5",
            "owner": "SOROK_ALPHA_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "S15 / A5: actual human encounter and evaluation distinct from sourcefree and native code",
            "smallest_useful_next_action": "Design a bounded consented participant study with actor-independent outcome measures and negative cases; do not infer A5 from code tests.",
            "source_backed": true,
            "status": "MISSING"
          }
        ]
      },
      {
        "domain": "KERNEL",
        "gaps": [
          {
            "affected_consumer": "whole program",
            "alternatives": [
              "relational organism",
              "Astra A-H",
              "original V3 M40",
              "Neo CAN/ADP",
              "S0-S16"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "A kernel is declared because it organizes documents but cannot derive or fail against a real consumer.",
            "dependencies": [
              "S0-S16",
              "CAN008/CAN011/ADP"
            ],
            "domain": "KERNEL",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "03_REAL_ALPHA_SPINE",
              "W1-A five rival spines",
              "W1-B competing science"
            ],
            "falsifier": "A kernel is declared because it organizes documents but cannot derive or fail against a real consumer.",
            "hq_judgment_required": true,
            "id": "GAP-KERNEL-UNRESOLVED",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "T",
              "A",
              "V"
            ],
            "next": "Run a hostile derivation comparing candidate kernels against actual consumer faults; do not elect a slogan.",
            "node": "Q_KERNEL_001",
            "owner": "SOROK_ORIGINAL_SCIENCE_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "K0: no adjudicated generative kernel",
            "smallest_useful_next_action": "Run a hostile derivation comparing candidate kernels against actual consumer faults; do not elect a slogan.",
            "source_backed": true,
            "status": "UNKNOWN"
          }
        ]
      },
      {
        "domain": "LEARNED_PRACTICE",
        "gaps": [
          {
            "affected_consumer": "native C9 later action",
            "alternatives": [
              "Leontiev activity/object",
              "Lahire context inhibition",
              "Seve act/capacity use-time",
              "Archer reflexive project"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "A later action after a tool or opportunity change is counted as acquired practice without a positive rule or actor evidence.",
            "dependencies": [
              "CAN008 Rule A",
              "ADP actor access",
              "C9 actor consumer"
            ],
            "domain": "LEARNED_PRACTICE",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "CAN_011 AUTHORITY 1.0.0",
              "P1 p1_s35.py T=NO_CHANGE",
              "S35 nonissuing resource"
            ],
            "falsifier": "A later action after a tool or opportunity change is counted as acquired practice without a positive rule or actor evidence.",
            "hq_judgment_required": true,
            "id": "GAP-CAN011-PRACTICE-ACQUISITION",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "T",
              "E",
              "C",
              "V"
            ],
            "next": "Issue an exact positive acquisition rule with rival discriminators, or retain MISSING_RULE and do not score missing T as NO_CHANGE.",
            "node": "CAN011_RULE_T_MISSING",
            "owner": "CAN011_OWNER / ADP_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "CAN-011 durable practice: distinguish acquired practice from opportunity, tool change, external scaffolding or evaluated NO_CHANGE",
            "smallest_useful_next_action": "Issue an exact positive acquisition rule with rival discriminators, or retain MISSING_RULE and do not score missing T as NO_CHANGE.",
            "source_backed": true,
            "status": "MISSING"
          }
        ]
      },
      {
        "domain": "N10",
        "gaps": [
          {
            "affected_consumer": "N10",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Sourcefree developmental behavior cannot be called native.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "N10",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "NOT_ISSUED"
            ],
            "falsifier": "Sourcefree developmental behavior cannot be called native.",
            "hq_judgment_required": true,
            "id": "GAP_NATIVE_SCIENCE_CAN_ADP",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Issue finite original rules and actor/event evidence.",
            "node": "N10",
            "owner": "CAN/ADP/SCI05 owners",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Sourcefree developmental behavior cannot be called native.",
            "return_sha": null,
            "smallest_useful_next_action": "Issue finite original rules and actor/event evidence.",
            "source_backed": true,
            "status": "NOT_ISSUED"
          }
        ]
      },
      {
        "domain": "NATIVE_PERSON_CUSTODY",
        "gaps": [
          {
            "affected_consumer": "native person",
            "alternatives": [
              "compatible migration",
              "honest unbridged hold"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Acceptance is moved across versions or roots, or used as native C9/C12 evidence.",
            "dependencies": [
              "C9/C12 owners",
              "external anchor"
            ],
            "domain": "NATIVE_PERSON_CUSTODY",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "JOIN-V ACCEPT_SCOPED exact 7bf",
              "C9_SOURCE_MISSING",
              "OWNER_ANCHOR_REQUIRED"
            ],
            "falsifier": "Acceptance is moved across versions or roots, or used as native C9/C12 evidence.",
            "hq_judgment_required": true,
            "id": "GAP-JOIN-NATIVE-C9-C12",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "C",
              "V"
            ],
            "next": "Keep the exact scope; open a separate owner decision for compatible writer/reader and external anchor.",
            "node": "JOIN_E_7BF",
            "owner": "C9_C12_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "JOIN-V scoped acceptance: preserve exact sourcefree acceptance without migrating native C9/C12",
            "smallest_useful_next_action": "Keep the exact scope; open a separate owner decision for compatible writer/reader and external anchor.",
            "source_backed": true,
            "status": "SCOPED_ACCEPTANCE"
          }
        ]
      },
      {
        "domain": "ORIGINAL_V3_ENGINEERING",
        "gaps": [
          {
            "affected_consumer": "current user alpha or NONE",
            "alternatives": [
              "port old V3 wholesale",
              "discard old V3",
              "source-grade exact sequencing/transaction patterns and require a current consumer"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "A current importer or consumer is claimed from the historical external call chain without exact source and test evidence.",
            "dependencies": [
              "CAN008/CAN011/ADP",
              "M6/V2",
              "original V3 source custodian"
            ],
            "domain": "ORIGINAL_V3_ENGINEERING",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "historical external simulation -> persona_sheet -> server turn -> V2 loader",
              "W1-C prior member hashes",
              "local external copy hashes differ"
            ],
            "falsifier": "A current importer or consumer is claimed from the historical external call chain without exact source and test evidence.",
            "hq_judgment_required": true,
            "id": "GAP-V3-YEARLY-PERSONA-MIGRATION",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "T",
              "A",
              "C",
              "V"
            ],
            "next": "Resolve the container/member cut and name one exact current-compatible consumer before adapting any old mechanism.",
            "node": "V3_RUN_ONE_YEAR",
            "owner": "ORIGINAL_V3_SOURCE_OWNER / C11_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Historical yearly_step/persona_sheet: preserve historical external function while deciding current reuse",
            "smallest_useful_next_action": "Resolve the container/member cut and name one exact current-compatible consumer before adapting any old mechanism.",
            "source_backed": true,
            "status": "UNKNOWN"
          }
        ]
      },
      {
        "domain": "PYAT",
        "gaps": [
          {
            "affected_consumer": "PYAT_EXTERNAL_BOUNDARY",
            "alternatives": [],
            "blocked_by": [
              "external owner held"
            ],
            "blockers": [],
            "consequence": "Sorok cannot infer the external world.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "PYAT",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "EXTERNAL_OWNER_HELD"
            ],
            "falsifier": "Sorok cannot infer the external world.",
            "hq_judgment_required": true,
            "id": "GAP_PYAT_BOUNDARY",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Supply qualified world/N11/N12/C11 grant to Sorok C0.",
            "node": "PYAT_EXTERNAL_BOUNDARY",
            "owner": "Pyat HQ/source owner",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Sorok cannot infer the external world.",
            "return_sha": null,
            "smallest_useful_next_action": "Supply qualified world/N11/N12/C11 grant to Sorok C0.",
            "source_backed": true,
            "status": "EXTERNAL_OWNER_HELD"
          }
        ]
      },
      {
        "domain": "RECEIVING_CUSTODY",
        "gaps": [
          {
            "affected_consumer": "PRE-MAIN receiver / CP-A5",
            "alternatives": [
              "separate guarded adapter",
              "hold until native C9/C12 owner cut"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "A packet integrity pass is treated as PRE-MAIN adoption or native person evidence.",
            "dependencies": [
              "C9 actor source",
              "C12 anchor",
              "PRE-MAIN receiving owner"
            ],
            "domain": "RECEIVING_CUSTODY",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "F1 independent defect",
              "F2 all-459 repair",
              "PASS_PARTIAL_SAME_ROOT_C9_C12"
            ],
            "falsifier": "A packet integrity pass is treated as PRE-MAIN adoption or native person evidence.",
            "hq_judgment_required": true,
            "id": "GAP-RRIF-F2-NATIVE-CONSUMER",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "C",
              "V"
            ],
            "next": "Select one compatible C9/C12 cut and external anchor; rerun the exact F2 negative/restore against the chosen cut.",
            "node": "RRIF_F2_FIRST_CONSUMER",
            "owner": "C9_C12_OWNER / PREMAIN_RECEIVING_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "RRIF F2: exact packet integrity repaired, but native receiving consumer remains partial",
            "smallest_useful_next_action": "Select one compatible C9/C12 cut and external anchor; rerun the exact F2 negative/restore against the chosen cut.",
            "source_backed": true,
            "status": "PARTIAL"
          }
        ]
      },
      {
        "domain": "S0",
        "gaps": [
          {
            "affected_consumer": "S0",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S0",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S0",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: charter, anti-goals, integrity constraints.",
            "node": "S0",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: charter, anti-goals, integrity constraints.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S1",
        "gaps": [
          {
            "affected_consumer": "S1",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S1",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S1",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: ontology, ownership boundaries, state classes.",
            "node": "S1",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: ontology, ownership boundaries, state classes.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S10",
        "gaps": [
          {
            "affected_consumer": "S10",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S10",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S10",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: state hierarchy, event log, summaries, retrieval law, checkpointing, simulation budget.",
            "node": "S10",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: state hierarchy, event log, summaries, retrieval law, checkpointing, simulation budget.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S11",
        "gaps": [
          {
            "affected_consumer": "S11",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "CP-A5 reader alone is not human-usable A5.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S11",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "CP-A5 reader alone is not human-usable A5.",
            "hq_judgment_required": true,
            "id": "GAP_S11_HUMAN_UX",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Issue accessible encounter flows and honest opacity behavior.",
            "node": "S11",
            "owner": "Product UX owner",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "CP-A5 reader alone is not human-usable A5.",
            "return_sha": null,
            "smallest_useful_next_action": "Issue accessible encounter flows and honest opacity behavior.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S12",
        "gaps": [
          {
            "affected_consumer": "S12",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S12",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S12",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: social options matrix, abuse analysis, minimum safe social architecture.",
            "node": "S12",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: social options matrix, abuse analysis, minimum safe social architecture.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S13",
        "gaps": [
          {
            "affected_consumer": "S13",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Engagement can be mistaken for human good.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S13",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Engagement can be mistaken for human good.",
            "hq_judgment_required": true,
            "id": "GAP_S13_REVENUE_MODEL",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Issue non-extractive pricing, notification and retention constraints.",
            "node": "S13",
            "owner": "Accountable business/product owner",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Engagement can be mistaken for human good.",
            "return_sha": null,
            "smallest_useful_next_action": "Issue non-extractive pricing, notification and retention constraints.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S14",
        "gaps": [
          {
            "affected_consumer": "S14",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Storage authenticity does not provide social safety.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S14",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Storage authenticity does not provide social safety.",
            "hq_judgment_required": true,
            "id": "GAP_S14_SOCIAL_SAFETY",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Issue abuse, consent, deletion and cross-user boundaries.",
            "node": "S14",
            "owner": "Safety/privacy owner",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Storage authenticity does not provide social safety.",
            "return_sha": null,
            "smallest_useful_next_action": "Issue abuse, consent, deletion and cross-user boundaries.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S15",
        "gaps": [
          {
            "affected_consumer": "S15",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Persuasive LLM presentation cannot establish a historically constituted other.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S15",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Persuasive LLM presentation cannot establish a historically constituted other.",
            "hq_judgment_required": true,
            "id": "GAP_S15_HUMAN_ALPHA",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Design bounded reference-person trial with ethics and actual participants.",
            "node": "S15",
            "owner": "Alpha/participant-research owner",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Persuasive LLM presentation cannot establish a historically constituted other.",
            "return_sha": null,
            "smallest_useful_next_action": "Design bounded reference-person trial with ethics and actual participants.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S16",
        "gaps": [
          {
            "affected_consumer": "S16",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S16",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S16",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: requirement packet with rationale, alternatives, evidence, dependencies, exact affected owners and reopen test.",
            "node": "S16",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: requirement packet with rationale, alternatives, evidence, dependencies, exact affected owners and reopen test.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S2",
        "gaps": [
          {
            "affected_consumer": "S2",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S2",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S2",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: accepted architecture requirements for eventual Pyat handoff.",
            "node": "S2",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: accepted architecture requirements for eventual Pyat handoff.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S3",
        "gaps": [
          {
            "affected_consumer": "S3",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S3",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S3",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: candidate V3 relational-prior schema and developmental derivation plan.",
            "node": "S3",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: candidate V3 relational-prior schema and developmental derivation plan.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S4",
        "gaps": [
          {
            "affected_consumer": "S4",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S4",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S4",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: relationship-state model and consequence laws.",
            "node": "S4",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: relationship-state model and consequence laws.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S5",
        "gaps": [
          {
            "affected_consumer": "S5",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "A5 cannot distinguish flourishing from affection/compliance.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S5",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "A5 cannot distinguish flourishing from affection/compliance.",
            "hq_judgment_required": true,
            "id": "GAP_S5_NORMATIVE_OUTPUT",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Issue normative alternatives, uncertainty law and harmful-attachment evaluation.",
            "node": "S5",
            "owner": "HQ / qualified product-science owner",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "A5 cannot distinguish flourishing from affection/compliance.",
            "return_sha": null,
            "smallest_useful_next_action": "Issue normative alternatives, uncertainty law and harmful-attachment evaluation.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S5_FLOURISHING",
        "gaps": [
          {
            "affected_consumer": "A5 and any future product benefit metric",
            "alternatives": [
              "attachment proxy",
              "retention/satisfaction proxy",
              "plural incommensurable dimensions"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "A model reports improved welfare because attachment rose while the actor lost agency, exit or outside relations.",
            "dependencies": [
              "Q-ONTO-001",
              "S13",
              "S14",
              "S15"
            ],
            "domain": "S5_FLOURISHING",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "01_PRODUCT_CHARTER",
              "SPD-0003",
              "24_COURT10",
              "05_PROGRAM_MAP"
            ],
            "falsifier": "A model reports improved welfare because attachment rose while the actor lost agency, exit or outside relations.",
            "hq_judgment_required": true,
            "id": "GAP-Q-HEALTH-FLOURISHING",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "T",
              "E",
              "C",
              "V"
            ],
            "next": "Adjudicate a plural flourishing rule with explicit non-collapse and a falsifiable human evaluation design; do not write a health_score.py stub.",
            "node": "Q_HEALTH_001",
            "owner": "SOROK_ORIGINAL_SCIENCE_OWNER / SOROK_ALPHA_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "S5 / Q-HEALTH-001: benefit to the other independent of liking, compliance or dependency",
            "smallest_useful_next_action": "Adjudicate a plural flourishing rule with explicit non-collapse and a falsifiable human evaluation design; do not write a health_score.py stub.",
            "source_backed": true,
            "status": "UNKNOWN"
          }
        ]
      },
      {
        "domain": "S6",
        "gaps": [
          {
            "affected_consumer": "S6",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S6",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S6",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: life-advancement and messaging constitution.",
            "node": "S6",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: life-advancement and messaging constitution.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S7",
        "gaps": [
          {
            "affected_consumer": "S7",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "User reflection can become pseudo-diagnosis or covert scoring.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S7",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "User reflection can become pseudo-diagnosis or covert scoring.",
            "hq_judgment_required": true,
            "id": "GAP_S7_PRAXIS_OUTPUT",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Issue evidence threshold, feedback cadence, opt-in and privacy policy.",
            "node": "S7",
            "owner": "HQ / user-praxis product owner",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "User reflection can become pseudo-diagnosis or covert scoring.",
            "return_sha": null,
            "smallest_useful_next_action": "Issue evidence threshold, feedback cadence, opt-in and privacy policy.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S8",
        "gaps": [
          {
            "affected_consumer": "S8",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S8",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S8",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: action vocabulary / open-action interpreter / consequence contract.",
            "node": "S8",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: action vocabulary / open-action interpreter / consequence contract.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "S9",
        "gaps": [
          {
            "affected_consumer": "S9",
            "alternatives": [],
            "blocked_by": [],
            "blockers": [],
            "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "S9",
            "evidence_locator": null,
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "SOURCE_DEFINED_CONSUMER_MISSING"
            ],
            "falsifier": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "hq_judgment_required": true,
            "id": "GAP_WORKSTREAM_S9",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Produce or verify the original output and name an actual first consumer: prompt/runtime boundary, expression tests, anti-sycophancy controls.",
            "node": "S9",
            "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
            "return_sha": null,
            "smallest_useful_next_action": "Produce or verify the original output and name an actual first consumer: prompt/runtime boundary, expression tests, anti-sycophancy controls.",
            "source_backed": true,
            "status": "SOURCE_DEFINED_CONSUMER_MISSING"
          }
        ]
      },
      {
        "domain": "SAFETY_PRIVACY",
        "gaps": [
          {
            "affected_consumer": "real users and personas",
            "alternatives": [
              "per-branch privacy",
              "abuse simulation law",
              "consent/deletion receipts"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "A user can stalk, coerce or extract another person's history without a boundary the system enforces.",
            "dependencies": [
              "S13",
              "C9/C12",
              "S15"
            ],
            "domain": "SAFETY_PRIVACY",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "05_PROGRAM_MAP S14",
              "01_PRODUCT_CHARTER anti-goals"
            ],
            "falsifier": "A user can stalk, coerce or extract another person's history without a boundary the system enforces.",
            "hq_judgment_required": true,
            "id": "GAP-S14-PRIVACY-ABUSE",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "T",
              "A",
              "E",
              "C",
              "V"
            ],
            "next": "Define a minimum abuse/consent/deletion contract with a hostile scenario and actual first consumer; do not treat storage hashes as social safety.",
            "node": "S14",
            "owner": "SOROK_SAFETY_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "S14: consent, deletion, coercion, harassment, stalking and cross-branch boundaries",
            "smallest_useful_next_action": "Define a minimum abuse/consent/deletion contract with a hostile scenario and actual first consumer; do not treat storage hashes as social safety.",
            "source_backed": true,
            "status": "MISSING"
          }
        ]
      },
      {
        "domain": "SOURCE_WITNESS",
        "gaps": [
          {
            "affected_consumer": "V3_EXTERNAL_MEMBER_HASH_MISMATCH",
            "alternatives": [],
            "blocked_by": [
              "source witness not available now",
              "science not issued",
              "owner authority held"
            ],
            "blockers": [],
            "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "SOURCE_WITNESS",
            "evidence_locator": null,
            "evidence_status": "WITNESS_STATUS_DERIVED",
            "existing_evidence": [
              "UNREAD"
            ],
            "falsifier": "The node keeps a historical or reported status but its current witness is not verified.",
            "hq_judgment_required": true,
            "id": "GAP_WITNESS_V3_EXTERNAL_MEMBER_HASH_MISMATCH",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "node": "V3_EXTERNAL_MEMBER_HASH_MISMATCH",
            "owner": "ORIGINAL_V3_SOURCE_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "The node keeps a historical or reported status but its current witness is not verified.",
            "return_sha": null,
            "smallest_useful_next_action": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "source_backed": false,
            "status": "UNREAD"
          },
          {
            "affected_consumer": "V3_EXTERNAL_SIMULATION",
            "alternatives": [],
            "blocked_by": [
              "source witness not available now",
              "science not issued",
              "owner authority held"
            ],
            "blockers": [],
            "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "SOURCE_WITNESS",
            "evidence_locator": null,
            "evidence_status": "WITNESS_STATUS_DERIVED",
            "existing_evidence": [
              "UNREAD"
            ],
            "falsifier": "The node keeps a historical or reported status but its current witness is not verified.",
            "hq_judgment_required": true,
            "id": "GAP_WITNESS_V3_EXTERNAL_SIMULATION",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "node": "V3_EXTERNAL_SIMULATION",
            "owner": "ORIGINAL_V3_SOURCE_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "The node keeps a historical or reported status but its current witness is not verified.",
            "return_sha": null,
            "smallest_useful_next_action": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "source_backed": false,
            "status": "UNREAD"
          },
          {
            "affected_consumer": "V3_PERSONA_SHEET",
            "alternatives": [],
            "blocked_by": [
              "source witness not available now",
              "science not issued",
              "owner authority held"
            ],
            "blockers": [],
            "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "SOURCE_WITNESS",
            "evidence_locator": null,
            "evidence_status": "WITNESS_STATUS_DERIVED",
            "existing_evidence": [
              "UNREAD"
            ],
            "falsifier": "The node keeps a historical or reported status but its current witness is not verified.",
            "hq_judgment_required": true,
            "id": "GAP_WITNESS_V3_PERSONA_SHEET",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "node": "V3_PERSONA_SHEET",
            "owner": "ORIGINAL_V3_SOURCE_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "The node keeps a historical or reported status but its current witness is not verified.",
            "return_sha": null,
            "smallest_useful_next_action": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "source_backed": false,
            "status": "UNREAD"
          },
          {
            "affected_consumer": "V3_RUN_ONE_YEAR",
            "alternatives": [],
            "blocked_by": [
              "source witness not available now",
              "science not issued",
              "owner authority held"
            ],
            "blockers": [],
            "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "SOURCE_WITNESS",
            "evidence_locator": null,
            "evidence_status": "WITNESS_STATUS_DERIVED",
            "existing_evidence": [
              "UNREAD"
            ],
            "falsifier": "The node keeps a historical or reported status but its current witness is not verified.",
            "hq_judgment_required": true,
            "id": "GAP_WITNESS_V3_RUN_ONE_YEAR",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "node": "V3_RUN_ONE_YEAR",
            "owner": "ORIGINAL_V3_SOURCE_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "The node keeps a historical or reported status but its current witness is not verified.",
            "return_sha": null,
            "smallest_useful_next_action": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "source_backed": false,
            "status": "UNREAD"
          },
          {
            "affected_consumer": "V3_SERVER_TURN",
            "alternatives": [],
            "blocked_by": [
              "source witness not available now",
              "science not issued",
              "owner authority held"
            ],
            "blockers": [],
            "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "SOURCE_WITNESS",
            "evidence_locator": null,
            "evidence_status": "WITNESS_STATUS_DERIVED",
            "existing_evidence": [
              "UNREAD"
            ],
            "falsifier": "The node keeps a historical or reported status but its current witness is not verified.",
            "hq_judgment_required": true,
            "id": "GAP_WITNESS_V3_SERVER_TURN",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "node": "V3_SERVER_TURN",
            "owner": "ORIGINAL_V3_SOURCE_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "The node keeps a historical or reported status but its current witness is not verified.",
            "return_sha": null,
            "smallest_useful_next_action": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "source_backed": false,
            "status": "UNREAD"
          },
          {
            "affected_consumer": "V3_V2_LOADER",
            "alternatives": [],
            "blocked_by": [
              "source witness not available now",
              "science not issued",
              "owner authority held"
            ],
            "blockers": [],
            "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
            "dependencies": [],
            "derived_gap": true,
            "domain": "SOURCE_WITNESS",
            "evidence_locator": null,
            "evidence_status": "WITNESS_STATUS_DERIVED",
            "existing_evidence": [
              "UNREAD"
            ],
            "falsifier": "The node keeps a historical or reported status but its current witness is not verified.",
            "hq_judgment_required": true,
            "id": "GAP_WITNESS_V3_V2_LOADER",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": false,
            "inference_rationale": null,
            "locator_reason": null,
            "missing_stages": [],
            "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "node": "V3_V2_LOADER",
            "owner": "ORIGINAL_V3_SOURCE_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "The node keeps a historical or reported status but its current witness is not verified.",
            "return_sha": null,
            "smallest_useful_next_action": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "source_backed": false,
            "status": "UNREAD"
          }
        ]
      },
      {
        "domain": "UX_ACCESSIBILITY",
        "gaps": [
          {
            "affected_consumer": "alpha user",
            "alternatives": [
              "conversational-only",
              "structured action surface",
              "local phenomenal compositor"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "The interface needs the user to guess hidden mechanics or rewards disclosure with access.",
            "dependencies": [
              "SOROK_101_BINDING",
              "S15"
            ],
            "domain": "UX_ACCESSIBILITY",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "05_PROGRAM_MAP S11",
              "Astra A-E experience scales"
            ],
            "falsifier": "The interface needs the user to guess hidden mechanics or rewards disclosure with access.",
            "hq_judgment_required": true,
            "id": "GAP-S11-ACCESSIBLE-ENCOUNTER-UX",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "T",
              "A",
              "E",
              "C",
              "V"
            ],
            "next": "Design and test one accessible ordinary scene with control return and honest opacity; no fabricated connection.",
            "node": "S11",
            "owner": "SOROK_PRODUCT_UX_OWNER",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "S11: encounter, opacity, time, commitment and repair without reducing people to stats",
            "smallest_useful_next_action": "Design and test one accessible ordinary scene with control return and honest opacity; no fabricated connection.",
            "source_backed": true,
            "status": "MISSING"
          }
        ]
      },
      {
        "domain": "WORK_CONTROL",
        "gaps": [
          {
            "affected_consumer": "HQ operator",
            "alternatives": [
              "manual dispatch",
              "bounded controller activation",
              "mechanical evidence only"
            ],
            "blocked_by": [],
            "blockers": [],
            "consequence": "A queue label, branch READY, session title or assistant marker is reported as observed execution.",
            "dependencies": [
              "user launch grant",
              "controller identity/lease"
            ],
            "domain": "WORK_CONTROL",
            "evidence_status": "SOURCE_DEFINED",
            "existing_evidence": [
              "R63 ROUTING_HOLD",
              "observed low vs requested high",
              "assistant marker not proof"
            ],
            "falsifier": "A queue label, branch READY, session title or assistant marker is reported as observed execution.",
            "hq_judgment_required": true,
            "id": "GAP-CONTROLLER-OBSERVED-EFFORT",
            "impact": {
              "affected_l0": [],
              "affected_sectors": [],
              "downstream_required_count": 0
            },
            "independently_actionable": true,
            "missing_stages": [
              "E",
              "C"
            ],
            "next": "Require an actual turn/process receipt before claiming model/effort or running state; no automatic retry.",
            "node": "CONTROLLER_R63_OBSERVED",
            "owner": "CONTROLLER_OWNER / SOROK_HQ",
            "parallel_group": "WHOLE_PROGRAM_GAP",
            "parent_obligation": "Controller: queued model/effort is not observed execution",
            "smallest_useful_next_action": "Require an actual turn/process receipt before claiming model/effort or running state; no automatic retry.",
            "source_backed": true,
            "status": "REVIEWED_NEGATIVE"
          }
        ]
      }
    ],
    "independently_actionable": 29,
    "note": "No completeness denominator and no automatic P0. Existing tickets are not the denominator.",
    "schema": "SOROK_WHOLE_PROGRAM_GAPS@1"
  }
}
```

### 7.2 `focus C12@INTEGRATE`

```json
{
  "existing_reference": {
    "axes": {
      "authority": "NOT_ADOPTED",
      "consumer": "NONE_PROVEN_AT_PREMAIN",
      "engineering": "SOURCE_DEFINITION_RECOVERED",
      "human": "NOT_PROVEN",
      "operational": "RETURNED_SHA__INDEX_INPUT",
      "review": "NOT_INDEPENDENTLY_REVIEWED",
      "science": "NOT_ISSUED",
      "source_recovery": "SOURCE_PRESENT"
    },
    "id": "C12",
    "incoming": [
      {
        "causal": false,
        "cycle_class": "INDEX_CONTAINMENT_OR_GOVERNANCE",
        "dependency_type": "INDEX_OR_GOVERNANCE",
        "edge_id": "EDGE_55f048bc8d735912",
        "from": "L1_PERSON",
        "grade": "INDEX_LINK",
        "hq_judgment_required": false,
        "hypothetical": false,
        "relation": "organ_contains_registry_item",
        "required": false,
        "source": {},
        "status": "INDEX_LINK",
        "to": "C12"
      },
      {
        "causal": false,
        "dependency_type": "INDEX_OR_GOVERNANCE",
        "edge_id": "EDGE_13f972151bf8da59",
        "from": "A0",
        "grade": "INDEX_LINK",
        "hq_judgment_required": true,
        "hypothetical": false,
        "relation": "backward_person_source_path",
        "required": false,
        "source": {},
        "status": "NAVIGATION_ONLY",
        "to": "C12"
      }
    ],
    "inverse_navigation": "Derived from the same directed edges; no second manual graph.",
    "maturity": {
      "id": "C12",
      "owner": null,
      "rule": "Stages are independent evidence axes; code does not prove theory and native validation is not inferred from a fixture.",
      "source_refs": [],
      "source_verification": {},
      "stages": {
        "A": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "C": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "E": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "I": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "T": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "V": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        }
      },
      "title": "Pipeline-produced continuing person and forks"
    },
    "missing_or_unproven": [],
    "neighbourhood": {
      "edges": 4,
      "nodes": [
        "C12",
        "A0",
        "C10",
        "L1_PERSON",
        "L4_NAMED_FIRST_CONSUMER"
      ]
    },
    "node": {
      "actual_current_importer": "NONE_PROVEN_AT_PREMAIN",
      "first_required_consumer": "A0 person life and reentry",
      "hq_judgment_required": false,
      "id": "C12",
      "kind": "TERMINAL_C_A",
      "layer": "L3",
      "registry_status": "HISTORICAL_DEFINITION_EXACT_FOUND__FULL_NATIVE_PRODUCT_NOT_PROVEN",
      "source_ref": "WORKER_RETURNS/SOROK-RCF-A-HISTORIC-DEV-MACHINE-R1/01_FUNCTION_SOURCE_OWNER_RECEIVER_LEDGER.json",
      "title": "Pipeline-produced continuing person and forks"
    },
    "outgoing": [
      {
        "causal": true,
        "dependency_type": "CONSUMER_DEPENDENCY",
        "edge_id": "EDGE_4c1f74692d95a510",
        "from": "C12",
        "grade": "SOURCE_DEFINED_REQUIREMENT",
        "hq_judgment_required": true,
        "hypothetical": false,
        "relation": "function_has_named_first_consumer",
        "required": true,
        "source": {},
        "status": "INDEX_LINK",
        "to": "L4_NAMED_FIRST_CONSUMER"
      },
      {
        "causal": false,
        "dependency_type": "INDEX_OR_GOVERNANCE",
        "edge_id": "EDGE_f69bcd38efb87e28",
        "from": "C12",
        "grade": "INDEX_LINK",
        "hq_judgment_required": true,
        "hypothetical": false,
        "relation": "backward_person_source_path",
        "required": false,
        "source": {},
        "status": "NAVIGATION_ONLY",
        "to": "C10"
      }
    ],
    "source_verification": null
  },
  "guide_phase_gates": [
    {
      "claim_scope": "NATIVE_CONTINUING_PERSON",
      "decision": "BLOCKED_MEMBERS_UNISSUED",
      "gate_id": "G-C12-NATIVE-INTEGRATE",
      "logic": "ALL_OF",
      "members": [
        {
          "predecessor_gates": [
            "G-C11-NATIVE"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C11@INTEGRATE",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [
            "G-C10-NATIVE"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C10@INTEGRATE",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [
            "G-C9-NATIVE-INTEGRATE",
            "G-C9-T-ANY"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C9@INTEGRATE",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [
            "G-E008-JOINT-BUILD"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C12:LOCAL_GUIDE:READER_ROOT@INTEGRATE",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C12:LOCAL_GUIDE:EXTERNAL_ANCHOR@VERIFY",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        }
      ],
      "owner": "C12/C11/C10/C9 and external custody owners",
      "remaining": [
        "C11@INTEGRATE",
        "C10@INTEGRATE",
        "C9@INTEGRATE",
        "C12:LOCAL_GUIDE:READER_ROOT@INTEGRATE",
        "C12:LOCAL_GUIDE:EXTERNAL_ANCHOR@VERIFY"
      ],
      "selected_mode": "UNSELECTED",
      "target_ref": "C12@INTEGRATE",
      "target_stage_issued": false
    }
  ],
  "receipts": [],
  "rule": "ALL same-target gates, actual member receipts and scope remain required",
  "source_cut": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
  "target": "C12@INTEGRATE"
}
```

### 7.3 `source-to-product E021@VERIFY`

```json
{
  "component": "E021",
  "existing_code_consumer": {
    "current_importer": "NONE_VERIFIED",
    "id": "E021"
  },
  "no_transitive_acceptance": true,
  "phase": {
    "existing_reference": {
      "id": "E021",
      "status": "NO_EXISTING_NODE"
    },
    "guide_phase_gates": [],
    "receipts": [
      {
        "affected_typed_edges_not_automatically_promoted": [
          {
            "blocking": false,
            "edge_id": "G-S10-SPECIFY::3",
            "required_ref": "E021@VERIFY",
            "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
            "target_ref": "S10@SPECIFY"
          },
          {
            "blocking": false,
            "edge_id": "G-E008-MATRIX::4",
            "required_ref": "E021@VERIFY",
            "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
            "target_ref": "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY"
          }
        ],
        "current_node_axes": {
          "JOIN_E_7BF": {
            "base_axis_preserved": {
              "authority": "NOT_ADOPTED",
              "consumer": "NONE_PROVEN_AT_PREMAIN",
              "engineering": "SOURCE_DEFINITION_ONLY",
              "human": "NOT_PROVEN",
              "operational": "CANDIDATE_ONLY",
              "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
              "science": "NOT_ISSUED",
              "source_recovery": "SOURCE_EXACT"
            },
            "exact_cut_phase_review": {
              "engineering": "SOURCEFREE_REVIEWED_AT_EXACT_7BF_ONLY",
              "event_id": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
              "human_evidence": "NOT_PROVEN",
              "native_science": "UNISSUED",
              "owner_authority": "UNISSUED",
              "review": "INDEPENDENT_SCOPED_7BF_REVIEWED_SOURCEFREE_ONLY",
              "source": {
                "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
                "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
                "object_type": "blob",
                "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
              },
              "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
              "transition_id": "JOIN_E_7BF_SCOPED_REVIEW"
            }
          }
        },
        "editorially_suppressed": [],
        "existing_work_packages": [],
        "gate_decisions": [],
        "possible_reverse_targets_not_automatically_unlocked": [
          "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY",
          "S10@SPECIFY"
        ],
        "receipts": [
          {
            "code_reader": "class JoinedSession",
            "grade": "SOURCEFREE_SCOPED",
            "id": "JOIN_E_7BF_SCOPED_REVIEW",
            "kind": "SCOPED_REVIEW",
            "next_evidence": "Joint C9 writer/C12 reader exact schema/root/ACK/anchor owner selection, separate new-tuple cold/severance and independent review. No native grant.",
            "owner": "JOIN_E_OWNER",
            "source": {
              "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
              "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
            },
            "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135",
            "status": "SCOPED_SOURCEFREE_ACCEPTED"
          }
        ],
        "ref": "E021@VERIFY"
      }
    ],
    "rule": "ALL same-target gates, actual member receipts and scope remain required",
    "source_cut": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
    "target": "E021@VERIFY"
  },
  "source": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623"
}
```

### 7.4 `goal C9@INTEGRATE`

```json
{
  "existing_reference": {
    "axes": {
      "authority": "NOT_ADOPTED",
      "consumer": "NONE_PROVEN_AT_PREMAIN",
      "engineering": "SOURCE_DEFINITION_RECOVERED",
      "human": "NOT_PROVEN",
      "operational": "RETURNED_SHA__INDEX_INPUT",
      "review": "NOT_INDEPENDENTLY_REVIEWED",
      "science": "NOT_ISSUED",
      "source_recovery": "SOURCE_PRESENT"
    },
    "id": "C9",
    "incoming": [
      {
        "causal": false,
        "cycle_class": "INDEX_CONTAINMENT_OR_GOVERNANCE",
        "dependency_type": "INDEX_OR_GOVERNANCE",
        "edge_id": "EDGE_df3ed217a52ed046",
        "from": "L1_ACTOR",
        "grade": "INDEX_LINK",
        "hq_judgment_required": false,
        "hypothetical": false,
        "relation": "organ_contains_registry_item",
        "required": false,
        "source": {},
        "status": "INDEX_LINK",
        "to": "C9"
      },
      {
        "causal": false,
        "dependency_type": "INDEX_OR_GOVERNANCE",
        "edge_id": "EDGE_6c70c9e6dc8a0ec3",
        "from": "C10",
        "grade": "INDEX_LINK",
        "hq_judgment_required": true,
        "hypothetical": false,
        "relation": "backward_person_source_path",
        "required": false,
        "source": {},
        "status": "NAVIGATION_ONLY",
        "to": "C9"
      }
    ],
    "inverse_navigation": "Derived from the same directed edges; no second manual graph.",
    "maturity": {
      "id": "C9",
      "owner": null,
      "rule": "Stages are independent evidence axes; code does not prove theory and native validation is not inferred from a fixture.",
      "source_refs": [],
      "source_verification": {},
      "stages": {
        "A": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "C": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "E": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "I": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "T": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        },
        "V": {
          "note": "No stage-specific evidence in this vertical slice.",
          "owner": "UNKNOWN",
          "status": "UNKNOWN"
        }
      },
      "title": "Canonical actor decision/version and later semantic reader"
    },
    "missing_or_unproven": [],
    "neighbourhood": {
      "edges": 4,
      "nodes": [
        "C9",
        "C10",
        "C8",
        "L1_ACTOR",
        "L4_NAMED_FIRST_CONSUMER"
      ]
    },
    "node": {
      "actual_current_importer": "NONE_PROVEN_AT_PREMAIN",
      "first_required_consumer": "E2 actual semantic response, C12 actor mirror",
      "hq_judgment_required": false,
      "id": "C9",
      "kind": "TERMINAL_C_A",
      "layer": "L3",
      "registry_status": "HISTORICAL_DEFINITION_EXACT_FOUND__FULL_NATIVE_PRODUCT_NOT_PROVEN",
      "source_ref": "WORKER_RETURNS/SOROK-RCF-A-HISTORIC-DEV-MACHINE-R1/01_FUNCTION_SOURCE_OWNER_RECEIVER_LEDGER.json",
      "title": "Canonical actor decision/version and later semantic reader"
    },
    "outgoing": [
      {
        "causal": true,
        "dependency_type": "CONSUMER_DEPENDENCY",
        "edge_id": "EDGE_745a8442c99a4c8a",
        "from": "C9",
        "grade": "SOURCE_DEFINED_REQUIREMENT",
        "hq_judgment_required": true,
        "hypothetical": false,
        "relation": "function_has_named_first_consumer",
        "required": true,
        "source": {},
        "status": "INDEX_LINK",
        "to": "L4_NAMED_FIRST_CONSUMER"
      },
      {
        "causal": false,
        "dependency_type": "INDEX_OR_GOVERNANCE",
        "edge_id": "EDGE_ad6fbfd83288b5d1",
        "from": "C9",
        "grade": "INDEX_LINK",
        "hq_judgment_required": true,
        "hypothetical": false,
        "relation": "backward_person_source_path",
        "required": false,
        "source": {},
        "status": "NAVIGATION_ONLY",
        "to": "C8"
      }
    ],
    "source_verification": null
  },
  "guide_phase_gates": [
    {
      "claim_scope": "NATIVE_ACTOR_DECISION",
      "decision": "BLOCKED_MEMBERS_UNISSUED",
      "gate_id": "G-C9-NATIVE-INTEGRATE",
      "logic": "ALL_OF",
      "members": [
        {
          "predecessor_gates": [
            "G-C4-NATIVE-BUILD"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C4@BUILD",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [
            "G-C8-NATIVE-INTEGRATE"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C8@INTEGRATE",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [
            "G-O03-NATIVE-ACCEPT"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "O03@ACCEPT",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [
            "G-E008-C9-COSPEC"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C9:LOCAL_GUIDE:WRITER_SCHEMA@SPECIFY",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [
            "G-O15-VERIFY"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "O15:LOCAL_GUIDE:LATER_E2_READER@VERIFY",
          "required_scope": "NATIVE_E2_ACTUAL_SEMANTIC_READER"
        },
        {
          "predecessor_gates": [],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "C9:LOCAL_GUIDE:CLAIM_MODE@SPECIFY",
          "required_scope": "NONEMPTY_SELECTED_RULE_T_MODE"
        }
      ],
      "owner": "C9/CAN008/CAN011/ADP owners",
      "remaining": [
        "C4@BUILD",
        "C8@INTEGRATE",
        "O03@ACCEPT",
        "C9:LOCAL_GUIDE:WRITER_SCHEMA@SPECIFY",
        "O15:LOCAL_GUIDE:LATER_E2_READER@VERIFY",
        "C9:LOCAL_GUIDE:CLAIM_MODE@SPECIFY"
      ],
      "selected_mode": "UNSELECTED",
      "target_ref": "C9@INTEGRATE",
      "target_stage_issued": false
    },
    {
      "claim_scope": "NATIVE_STATE_UPDATE_OR_LAWFUL_NOCHANGE",
      "decision": "MODE_UNSELECTED_HOLD",
      "gate_id": "G-C9-T-ANY",
      "logic": "ANY_OF",
      "members": [
        {
          "predecessor_gates": [
            "G-O05-POSITIVE-ACCEPT"
          ],
          "present_but_not_promoting": [
            {
              "grade": "TEST_ONLY_SOURCEFREE",
              "source_cut": "b65c75a9e62618690f7d02265bc9e850af549161",
              "transition_id": "S35_P1_SOURCEFREE_RETURN_ONLY"
            }
          ],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "O05@ACCEPT",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        },
        {
          "predecessor_gates": [
            "G-O07-NOCHANGE-ACCEPT"
          ],
          "present_but_not_promoting": [],
          "qualifies_now": false,
          "reason": "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT",
          "ref": "O07@ACCEPT",
          "required_scope": "DOCUMENTARY_REQUIREMENT"
        }
      ],
      "owner": "CAN011 scientific issuer",
      "remaining": [
        "O05@ACCEPT",
        "O07@ACCEPT"
      ],
      "selected_mode": "UNSELECTED",
      "target_ref": "C9@INTEGRATE",
      "target_stage_issued": false
    }
  ],
  "missing_predecessors": [
    {
      "gate": "G-C9-NATIVE-INTEGRATE",
      "logic": "ALL_OF",
      "missing": [
        "C4@BUILD",
        "C8@INTEGRATE",
        "O03@ACCEPT",
        "C9:LOCAL_GUIDE:WRITER_SCHEMA@SPECIFY",
        "O15:LOCAL_GUIDE:LATER_E2_READER@VERIFY",
        "C9:LOCAL_GUIDE:CLAIM_MODE@SPECIFY"
      ],
      "scope": "NATIVE_ACTOR_DECISION"
    },
    {
      "gate": "G-C9-T-ANY",
      "logic": "ANY_OF",
      "missing": [
        "O05@ACCEPT",
        "O07@ACCEPT"
      ],
      "scope": "NATIVE_STATE_UPDATE_OR_LAWFUL_NOCHANGE"
    }
  ],
  "receipts": [],
  "rule": "ALL same-target gates, actual member receipts and scope remain required",
  "source_cut": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
  "target": "C9@INTEGRATE"
}
```

### 7.5 `work-now`

```json
{
  "existing_P0_P1": [
    {
      "blockers": [
        {
          "axis": "authority",
          "node": "PYAT_EXTERNAL_BOUNDARY",
          "reason": "external owner held",
          "status": "EXTERNAL_OWNER_HELD"
        }
      ],
      "consequence": "Sorok cannot infer the external world.",
      "domain": "PYAT",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_PYAT_BOUNDARY",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Supply qualified world/N11/N12/C11 grant to Sorok C0.",
      "node": "PYAT_EXTERNAL_BOUNDARY",
      "owner": "Pyat HQ/source owner",
      "parallel_group": "EXTERNAL_BOUNDARY",
      "source_backed": true,
      "status": "EXTERNAL_OWNER_HELD",
      "terminal_contribution": "Sorok cannot infer the external world.",
      "uncertainty": {
        "blocker_count": 1,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "EXTERNAL_OWNER_HELD"
      }
    },
    {
      "blockers": [
        {
          "axis": "science",
          "node": "A5",
          "reason": "science not issued",
          "status": "NOT_ISSUED"
        },
        {
          "axis": "authority",
          "node": "A5",
          "reason": "owner authority held",
          "status": "NOT_ADOPTED"
        },
        {
          "axis": "human",
          "node": "A5",
          "reason": "no human A5 evidence",
          "status": "NOT_PROVEN"
        }
      ],
      "consequence": "No human-product proof.",
      "domain": "A5",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_NATIVE_A5",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "ALPHA_EVALUATION",
          "C_A_19",
          "UX_ACCESSIBILITY"
        ],
        "downstream_required_count": 1,
        "downstream_required_nodes": [
          "L4_NAMED_FIRST_CONSUMER"
        ]
      },
      "next": "Human participant trial distinct from sourcefree encounter.",
      "node": "A5",
      "owner": "Sorok human A5/research owner",
      "parallel_group": "HUMAN_ALPHA",
      "source_backed": true,
      "status": "NOT_PROVEN",
      "terminal_contribution": "No human-product proof.",
      "uncertainty": {
        "blocker_count": 3,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "NOT_PROVEN"
      }
    },
    {
      "blockers": [
        {
          "axis": "science",
          "node": "C11",
          "reason": "science not issued",
          "status": "NOT_ISSUED"
        },
        {
          "axis": "authority",
          "node": "C11",
          "reason": "owner authority held",
          "status": "NOT_ADOPTED"
        }
      ],
      "consequence": "No native continuing person exists.",
      "domain": "C11",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_NATIVE_C4_C11_PERSON",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "C_A_19"
        ],
        "downstream_required_count": 1,
        "downstream_required_nodes": [
          "L4_NAMED_FIRST_CONSUMER"
        ]
      },
      "next": "Separate native world/C11 person authority and actual C12 consumer.",
      "node": "C11",
      "owner": "Original Pyat/C11/C12 owners",
      "parallel_group": "NATIVE_PERSON",
      "source_backed": true,
      "status": "SOURCEFREE_OR_SOURCE_ONLY",
      "terminal_contribution": "No native continuing person exists.",
      "uncertainty": {
        "blocker_count": 2,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCEFREE_OR_SOURCE_ONLY"
      }
    },
    {
      "blockers": [
        {
          "axis": "authority",
          "node": "C9C12-R2",
          "reason": "owner authority held",
          "status": "UNADOPTED"
        }
      ],
      "consequence": "C12 durability remains sourcefree-only.",
      "domain": "C9C12-R2",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_C9_C12_ANCHOR",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "RECOVERY_ASSETS",
          "SAFETY_PRIVACY"
        ],
        "downstream_required_count": 1,
        "downstream_required_nodes": [
          "L4_NAMED_FIRST_CONSUMER"
        ]
      },
      "next": "External anchor, mirror/outbox and durable actor readset decision.",
      "node": "C9C12-R2",
      "owner": "C9R/BP4/C12 owners",
      "parallel_group": "NATIVE_PERSON",
      "source_backed": true,
      "status": "CANDIDATE",
      "terminal_contribution": "C12 durability remains sourcefree-only.",
      "uncertainty": {
        "blocker_count": 1,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "CANDIDATE"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S0",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S0",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: charter, anti-goals, integrity constraints.",
      "node": "S0",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S1",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S1",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: ontology, ownership boundaries, state classes.",
      "node": "S1",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S10",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S10",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: state hierarchy, event log, summaries, retrieval law, checkpointing, simulation budget.",
      "node": "S10",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "CP-A5 reader alone is not human-usable A5.",
      "domain": "S11",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_S11_HUMAN_UX",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16",
          "TRUST_INJURY_REPAIR_OPACITY",
          "USER_PRAXIS",
          "UX_ACCESSIBILITY",
          "V2_RENDERING_UX"
        ],
        "downstream_required_count": 3,
        "downstream_required_nodes": [
          "L3_S11_ENCOUNTER_SURFACE",
          "L4_S11_UX_OWNER",
          "L5_S11_OMNISCIENCE_AND_BLACKBOX_FALSIFIER"
        ]
      },
      "next": "Issue accessible encounter flows and honest opacity behavior.",
      "node": "S11",
      "owner": "Product UX owner",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "CP-A5 reader alone is not human-usable A5.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S12",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S12",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16",
          "SOCIAL_POSSIBILITIES"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: social options matrix, abuse analysis, minimum safe social architecture.",
      "node": "S12",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Engagement can be mistaken for human good.",
      "domain": "S13",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_S13_REVENUE_MODEL",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "PROFIT_RETENTION_ETHICS",
          "S0_S16"
        ],
        "downstream_required_count": 3,
        "downstream_required_nodes": [
          "L3_S13_REVENUE_MODEL",
          "L4_S13_BUSINESS_OWNER",
          "L5_S13_EXTRACTIVE_INCENTIVE_FALSIFIER"
        ]
      },
      "next": "Issue non-extractive pricing, notification and retention constraints.",
      "node": "S13",
      "owner": "Accountable business/product owner",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Engagement can be mistaken for human good.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Storage authenticity does not provide social safety.",
      "domain": "S14",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_S14_SOCIAL_SAFETY",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "RELATIONAL_CONSTITUTION",
          "S0_S16",
          "SAFETY_PRIVACY",
          "TRUST_INJURY_REPAIR_OPACITY"
        ],
        "downstream_required_count": 3,
        "downstream_required_nodes": [
          "L3_S14_ABUSE_PRIVACY_BOUNDARY",
          "L4_S14_SAFETY_OWNER",
          "L5_S14_COERCION_AND_CROSS_USER_FALSIFIER"
        ]
      },
      "next": "Issue abuse, consent, deletion and cross-user boundaries.",
      "node": "S14",
      "owner": "Safety/privacy owner",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Storage authenticity does not provide social safety.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Persuasive LLM presentation cannot establish a historically constituted other.",
      "domain": "S15",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_S15_HUMAN_ALPHA",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "ALPHA_EVALUATION",
          "S0_S16",
          "USER_PRAXIS",
          "UX_ACCESSIBILITY"
        ],
        "downstream_required_count": 3,
        "downstream_required_nodes": [
          "L3_S15_REFERENCE_AND_NATIVE_EVALUATION",
          "L4_S15_ALPHA_OWNER",
          "L5_S15_PERSUASIVE_LLM_FALSIFIER"
        ]
      },
      "next": "Design bounded reference-person trial with ethics and actual participants.",
      "node": "S15",
      "owner": "Alpha/participant-research owner",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Persuasive LLM presentation cannot establish a historically constituted other.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S16",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S16",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: requirement packet with rationale, alternatives, evidence, dependencies, exact affected owners and reopen test.",
      "node": "S16",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S2",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S2",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: accepted architecture requirements for eventual Pyat handoff.",
      "node": "S2",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S3",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S3",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: candidate V3 relational-prior schema and developmental derivation plan.",
      "node": "S3",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S4",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S4",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: relationship-state model and consequence laws.",
      "node": "S4",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "A5 cannot distinguish flourishing from affection/compliance.",
      "domain": "S5",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_S5_NORMATIVE_OUTPUT",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "RELATIONAL_CONSTITUTION",
          "S0_S16",
          "TRUST_INJURY_REPAIR_OPACITY"
        ],
        "downstream_required_count": 3,
        "downstream_required_nodes": [
          "L3_S5_NORMATIVE_MODEL",
          "L4_S5_FLOURISHING_OWNER",
          "L5_S5_HARMFUL_ATTACHMENT_COUNTEREXAMPLE"
        ]
      },
      "next": "Issue normative alternatives, uncertainty law and harmful-attachment evaluation.",
      "node": "S5",
      "owner": "HQ / qualified product-science owner",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "A5 cannot distinguish flourishing from affection/compliance.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S6",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S6",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: life-advancement and messaging constitution.",
      "node": "S6",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "User reflection can become pseudo-diagnosis or covert scoring.",
      "domain": "S7",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_S7_PRAXIS_OUTPUT",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16",
          "USER_PRAXIS"
        ],
        "downstream_required_count": 3,
        "downstream_required_nodes": [
          "L3_S7_PRACTICE_INFERENCE",
          "L4_S7_PRAXIS_OWNER",
          "L5_S7_ONE_ACTION_DIAGNOSIS_FALSIFIER"
        ]
      },
      "next": "Issue evidence threshold, feedback cadence, opt-in and privacy policy.",
      "node": "S7",
      "owner": "HQ / user-praxis product owner",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "User reflection can become pseudo-diagnosis or covert scoring.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S8",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S8",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16",
          "USER_PRAXIS"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: action vocabulary / open-action interpreter / consequence contract.",
      "node": "S8",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "domain": "S9",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_WORKSTREAM_S9",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "S0_S16",
          "V2_RENDERING_UX"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Produce or verify the original output and name an actual first consumer: prompt/runtime boundary, expression tests, anti-sycophancy controls.",
      "node": "S9",
      "owner": "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
      "parallel_group": "PRODUCT_WORKSTREAM",
      "source_backed": true,
      "status": "SOURCE_DEFINED_CONSUMER_MISSING",
      "terminal_contribution": "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "SOURCE_DEFINED_CONSUMER_MISSING"
      }
    },
    {
      "blockers": [],
      "consequence": "Sourcefree developmental behavior cannot be called native.",
      "domain": "N10",
      "evidence_status": "SOURCE_DEFINED",
      "gap_id": "GAP_NATIVE_SCIENCE_CAN_ADP",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [
          "CANON_HISTORY_EVENT_CLOCK_MEMORY",
          "NEO_N_12"
        ],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Issue finite original rules and actor/event evidence.",
      "node": "N10",
      "owner": "CAN/ADP/SCI05 owners",
      "parallel_group": "SCIENCE_OWNER",
      "source_backed": true,
      "status": "NOT_ISSUED",
      "terminal_contribution": "Sourcefree developmental behavior cannot be called native.",
      "uncertainty": {
        "blocker_count": 0,
        "evidence_status": "SOURCE_DEFINED",
        "source_backed": true,
        "status": "NOT_ISSUED"
      }
    },
    {
      "blockers": [
        {
          "axis": "source_recovery",
          "node": "V3_EXTERNAL_MEMBER_HASH_MISMATCH",
          "reason": "source witness not available now",
          "status": "UNREAD"
        },
        {
          "axis": "science",
          "node": "V3_EXTERNAL_MEMBER_HASH_MISMATCH",
          "reason": "science not issued",
          "status": "NOT_ISSUED"
        },
        {
          "axis": "authority",
          "node": "V3_EXTERNAL_MEMBER_HASH_MISMATCH",
          "reason": "owner authority held",
          "status": "NOT_ADOPTED"
        }
      ],
      "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
      "domain": "SOURCE_WITNESS",
      "evidence_status": "WITNESS_STATUS_DERIVED",
      "gap_id": "GAP_WITNESS_V3_EXTERNAL_MEMBER_HASH_MISMATCH",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
      "node": "V3_EXTERNAL_MEMBER_HASH_MISMATCH",
      "owner": "ORIGINAL_V3_SOURCE_OWNER",
      "parallel_group": "SOURCE_WITNESS",
      "source_backed": false,
      "status": "UNREAD",
      "terminal_contribution": "The node keeps a historical or reported status but its current witness is not verified.",
      "uncertainty": {
        "blocker_count": 3,
        "evidence_status": "WITNESS_STATUS_DERIVED",
        "source_backed": false,
        "status": "UNREAD"
      }
    },
    {
      "blockers": [
        {
          "axis": "source_recovery",
          "node": "V3_EXTERNAL_SIMULATION",
          "reason": "source witness not available now",
          "status": "UNREAD"
        },
        {
          "axis": "science",
          "node": "V3_EXTERNAL_SIMULATION",
          "reason": "science not issued",
          "status": "NOT_ISSUED"
        },
        {
          "axis": "authority",
          "node": "V3_EXTERNAL_SIMULATION",
          "reason": "owner authority held",
          "status": "NOT_ADOPTED"
        }
      ],
      "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
      "domain": "SOURCE_WITNESS",
      "evidence_status": "WITNESS_STATUS_DERIVED",
      "gap_id": "GAP_WITNESS_V3_EXTERNAL_SIMULATION",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
      "node": "V3_EXTERNAL_SIMULATION",
      "owner": "ORIGINAL_V3_SOURCE_OWNER",
      "parallel_group": "SOURCE_WITNESS",
      "source_backed": false,
      "status": "UNREAD",
      "terminal_contribution": "The node keeps a historical or reported status but its current witness is not verified.",
      "uncertainty": {
        "blocker_count": 3,
        "evidence_status": "WITNESS_STATUS_DERIVED",
        "source_backed": false,
        "status": "UNREAD"
      }
    },
    {
      "blockers": [
        {
          "axis": "source_recovery",
          "node": "V3_PERSONA_SHEET",
          "reason": "source witness not available now",
          "status": "UNREAD"
        },
        {
          "axis": "science",
          "node": "V3_PERSONA_SHEET",
          "reason": "science not issued",
          "status": "NOT_ISSUED"
        },
        {
          "axis": "authority",
          "node": "V3_PERSONA_SHEET",
          "reason": "owner authority held",
          "status": "NOT_ADOPTED"
        }
      ],
      "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
      "domain": "SOURCE_WITNESS",
      "evidence_status": "WITNESS_STATUS_DERIVED",
      "gap_id": "GAP_WITNESS_V3_PERSONA_SHEET",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
      "node": "V3_PERSONA_SHEET",
      "owner": "ORIGINAL_V3_SOURCE_OWNER",
      "parallel_group": "SOURCE_WITNESS",
      "source_backed": false,
      "status": "UNREAD",
      "terminal_contribution": "The node keeps a historical or reported status but its current witness is not verified.",
      "uncertainty": {
        "blocker_count": 3,
        "evidence_status": "WITNESS_STATUS_DERIVED",
        "source_backed": false,
        "status": "UNREAD"
      }
    },
    {
      "blockers": [
        {
          "axis": "source_recovery",
          "node": "V3_RUN_ONE_YEAR",
          "reason": "source witness not available now",
          "status": "UNREAD"
        },
        {
          "axis": "science",
          "node": "V3_RUN_ONE_YEAR",
          "reason": "science not issued",
          "status": "NOT_ISSUED"
        },
        {
          "axis": "authority",
          "node": "V3_RUN_ONE_YEAR",
          "reason": "owner authority held",
          "status": "NOT_ADOPTED"
        }
      ],
      "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
      "domain": "SOURCE_WITNESS",
      "evidence_status": "WITNESS_STATUS_DERIVED",
      "gap_id": "GAP_WITNESS_V3_RUN_ONE_YEAR",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
      "node": "V3_RUN_ONE_YEAR",
      "owner": "ORIGINAL_V3_SOURCE_OWNER",
      "parallel_group": "SOURCE_WITNESS",
      "source_backed": false,
      "status": "UNREAD",
      "terminal_contribution": "The node keeps a historical or reported status but its current witness is not verified.",
      "uncertainty": {
        "blocker_count": 3,
        "evidence_status": "WITNESS_STATUS_DERIVED",
        "source_backed": false,
        "status": "UNREAD"
      }
    },
    {
      "blockers": [
        {
          "axis": "source_recovery",
          "node": "V3_SERVER_TURN",
          "reason": "source witness not available now",
          "status": "UNREAD"
        },
        {
          "axis": "science",
          "node": "V3_SERVER_TURN",
          "reason": "science not issued",
          "status": "NOT_ISSUED"
        },
        {
          "axis": "authority",
          "node": "V3_SERVER_TURN",
          "reason": "owner authority held",
          "status": "NOT_ADOPTED"
        }
      ],
      "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
      "domain": "SOURCE_WITNESS",
      "evidence_status": "WITNESS_STATUS_DERIVED",
      "gap_id": "GAP_WITNESS_V3_SERVER_TURN",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
      "node": "V3_SERVER_TURN",
      "owner": "ORIGINAL_V3_SOURCE_OWNER",
      "parallel_group": "SOURCE_WITNESS",
      "source_backed": false,
      "status": "UNREAD",
      "terminal_contribution": "The node keeps a historical or reported status but its current witness is not verified.",
      "uncertainty": {
        "blocker_count": 3,
        "evidence_status": "WITNESS_STATUS_DERIVED",
        "source_backed": false,
        "status": "UNREAD"
      }
    },
    {
      "blockers": [
        {
          "axis": "source_recovery",
          "node": "V3_V2_LOADER",
          "reason": "source witness not available now",
          "status": "UNREAD"
        },
        {
          "axis": "science",
          "node": "V3_V2_LOADER",
          "reason": "science not issued",
          "status": "NOT_ISSUED"
        },
        {
          "axis": "authority",
          "node": "V3_V2_LOADER",
          "reason": "owner authority held",
          "status": "NOT_ADOPTED"
        }
      ],
      "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
      "domain": "SOURCE_WITNESS",
      "evidence_status": "WITNESS_STATUS_DERIVED",
      "gap_id": "GAP_WITNESS_V3_V2_LOADER",
      "hq_judgment_required": true,
      "impact": {
        "affected_l0": [],
        "affected_original_workstreams": [],
        "affected_sectors": [],
        "downstream_required_count": 0,
        "downstream_required_nodes": []
      },
      "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
      "node": "V3_V2_LOADER",
      "owner": "ORIGINAL_V3_SOURCE_OWNER",
      "parallel_group": "SOURCE_WITNESS",
      "source_backed": false,
      "status": "UNREAD",
      "terminal_contribution": "The node keeps a historical or reported status but its current witness is not verified.",
      "uncertainty": {
        "blocker_count": 3,
        "evidence_status": "WITNESS_STATUS_DERIVED",
        "source_backed": false,
        "status": "UNREAD"
      }
    }
  ],
  "existing_parallel_groups": [
    {
      "candidate_count": 1,
      "candidate_ids": [
        "GAP_PYAT_BOUNDARY"
      ],
      "group": "EXTERNAL_BOUNDARY",
      "parallel_possible": false
    },
    {
      "candidate_count": 1,
      "candidate_ids": [
        "GAP_NATIVE_A5"
      ],
      "group": "HUMAN_ALPHA",
      "parallel_possible": false
    },
    {
      "candidate_count": 2,
      "candidate_ids": [
        "GAP_NATIVE_C4_C11_PERSON",
        "GAP_C9_C12_ANCHOR"
      ],
      "group": "NATIVE_PERSON",
      "parallel_possible": true
    },
    {
      "candidate_count": 17,
      "candidate_ids": [
        "GAP_WORKSTREAM_S0",
        "GAP_WORKSTREAM_S1",
        "GAP_WORKSTREAM_S10",
        "GAP_S11_HUMAN_UX",
        "GAP_WORKSTREAM_S12",
        "GAP_S13_REVENUE_MODEL",
        "GAP_S14_SOCIAL_SAFETY",
        "GAP_S15_HUMAN_ALPHA",
        "GAP_WORKSTREAM_S16",
        "GAP_WORKSTREAM_S2",
        "GAP_WORKSTREAM_S3",
        "GAP_WORKSTREAM_S4",
        "GAP_S5_NORMATIVE_OUTPUT",
        "GAP_WORKSTREAM_S6",
        "GAP_S7_PRAXIS_OUTPUT",
        "GAP_WORKSTREAM_S8",
        "GAP_WORKSTREAM_S9"
      ],
      "group": "PRODUCT_WORKSTREAM",
      "parallel_possible": true
    },
    {
      "candidate_count": 1,
      "candidate_ids": [
        "GAP_NATIVE_SCIENCE_CAN_ADP"
      ],
      "group": "SCIENCE_OWNER",
      "parallel_possible": false
    },
    {
      "candidate_count": 6,
      "candidate_ids": [
        "GAP_WITNESS_V3_EXTERNAL_MEMBER_HASH_MISMATCH",
        "GAP_WITNESS_V3_EXTERNAL_SIMULATION",
        "GAP_WITNESS_V3_PERSONA_SHEET",
        "GAP_WITNESS_V3_RUN_ONE_YEAR",
        "GAP_WITNESS_V3_SERVER_TURN",
        "GAP_WITNESS_V3_V2_LOADER"
      ],
      "group": "SOURCE_WITNESS",
      "parallel_possible": true
    }
  ],
  "live_phase_changes": [
    {
      "affected_typed_edges_not_automatically_promoted": [],
      "current_node_axes": {
        "JOIN_C12_HOLD": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "REVISE_MATERIAL_DEFECTS_AT_EXACT_CUT",
            "event_id": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "REVIEW_REVISE_MATERIAL_AT_EXACT_CUT",
            "source": {
              "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
              "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [
        {
          "id": "G-C12-SF-VERIFY",
          "remaining": [
            "C12:LOCAL_GUIDE:READER_ROOT@INTEGRATE",
            "C12:LOCAL_GUIDE:NEW_TUPLE_COLD_SEVERANCE@VERIFY",
            "C12:LOCAL_GUIDE:ACTUAL_ANCHOR@VERIFY"
          ],
          "review_red_at_selected_cut": true,
          "review_red_source_cuts": [
            "598d9e9eaba5143950c63317705fd09104fbf463"
          ],
          "status": "BLOCKED_MEMBERS_UNISSUED"
        }
      ],
      "possible_reverse_targets_not_automatically_unlocked": [],
      "receipts": [
        {
          "code_reader": "NONE",
          "grade": "INDEPENDENT_NEGATIVE_SOURCE",
          "id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE",
          "kind": "REVIEW_REVISE",
          "next_evidence": "Repair exact R2-T1/M1/C1/D1, choose new C9/C12 tuple and cold verify with fresh independent reader; keep 7bf accepted only at 7bf.",
          "owner": "C9_C12_OWNER",
          "source": {
            "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
            "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
            "object_type": "blob",
            "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
          },
          "source_cut": "598d9e9eaba5143950c63317705fd09104fbf463",
          "status": "EXACT_NEGATIVE_REVIEWED"
        }
      ],
      "ref": "C12@VERIFY"
    },
    {
      "affected_typed_edges_not_automatically_promoted": [
        {
          "blocking": false,
          "edge_id": "G-S10-SPECIFY::3",
          "required_ref": "E021@VERIFY",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "S10@SPECIFY"
        },
        {
          "blocking": false,
          "edge_id": "G-E008-MATRIX::4",
          "required_ref": "E021@VERIFY",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY"
        }
      ],
      "current_node_axes": {
        "JOIN_E_7BF": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "SOURCEFREE_REVIEWED_AT_EXACT_7BF_ONLY",
            "event_id": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "INDEPENDENT_SCOPED_7BF_REVIEWED_SOURCEFREE_ONLY",
            "source": {
              "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
              "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "JOIN_E_7BF_SCOPED_REVIEW"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [],
      "possible_reverse_targets_not_automatically_unlocked": [
        "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY",
        "S10@SPECIFY"
      ],
      "receipts": [
        {
          "code_reader": "class JoinedSession",
          "grade": "SOURCEFREE_SCOPED",
          "id": "JOIN_E_7BF_SCOPED_REVIEW",
          "kind": "SCOPED_REVIEW",
          "next_evidence": "Joint C9 writer/C12 reader exact schema/root/ACK/anchor owner selection, separate new-tuple cold/severance and independent review. No native grant.",
          "owner": "JOIN_E_OWNER",
          "source": {
            "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
            "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
            "object_type": "blob",
            "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
          },
          "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135",
          "status": "SCOPED_SOURCEFREE_ACCEPTED"
        }
      ],
      "ref": "E021@VERIFY"
    },
    {
      "affected_typed_edges_not_automatically_promoted": [
        {
          "blocking": true,
          "edge_id": "G-C9-T-ANY::1",
          "required_ref": "O05@ACCEPT",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "C9@INTEGRATE"
        },
        {
          "blocking": true,
          "edge_id": "G-C9-T-IF-ACQUIRED::1",
          "required_ref": "O05@ACCEPT",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "C9@ACCEPT"
        }
      ],
      "current_node_axes": {
        "CAN011_RULE_T_MISSING": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "SOURCE_PRESENT_AUTHOR_TESTED_NOT_NATIVE",
            "event_id": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "UNREVIEWED_RETURN_CANDIDATE",
            "source": {
              "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
              "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
              "object_type": "blob",
              "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "S35_P1_SOURCEFREE_RETURN_ONLY"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [
        {
          "id": "G-O05-POSITIVE-ACCEPT",
          "remaining": [
            "O05:LOCAL_GUIDE:RULE_T_DISCRIMINATOR@SPECIFY",
            "C4:LOCAL_GUIDE:ACTOR_SOURCE@ACCEPT",
            "C8:LOCAL_GUIDE:ACTION_OMISSION@VERIFY"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "BLOCKED_MEMBERS_UNISSUED"
        },
        {
          "id": "G-C9-T-ANY",
          "remaining": [
            "O05@ACCEPT",
            "O07@ACCEPT"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "MODE_UNSELECTED_HOLD"
        },
        {
          "id": "G-C9-T-IF-ACQUIRED",
          "remaining": [
            "O05@ACCEPT"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "MODE_UNSELECTED_HOLD"
        }
      ],
      "possible_reverse_targets_not_automatically_unlocked": [
        "C9@ACCEPT",
        "C9@INTEGRATE"
      ],
      "receipts": [
        {
          "code_reader": "NONE",
          "grade": "TEST_ONLY_SOURCEFREE",
          "id": "S35_P1_SOURCEFREE_RETURN_ONLY",
          "kind": "RETURN_CANDIDATE",
          "next_evidence": "Only a competent CAN011 original Rule T acquired-practice or genuinely evaluated O07 no-change issuance can promote native C9; isolate first-reader access and later performed E2.",
          "owner": "CAN011_OWNER",
          "source": {
            "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
            "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
            "object_type": "blob",
            "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
          },
          "source_cut": "b65c75a9e62618690f7d02265bc9e850af549161",
          "status": "SOURCE_PRESENT_CANDIDATE"
        }
      ],
      "ref": "O05@ACCEPT"
    }
  ],
  "no_agent_dispatch": true,
  "programma_live": {
    "changed_refs": [
      "C12@VERIFY",
      "E021@VERIFY",
      "O05@ACCEPT"
    ],
    "guide_cut": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
    "pending": [
      {
        "affected_typed_edges_not_automatically_promoted": [],
        "current_node_axes": {
          "JOIN_C12_HOLD": {
            "base_axis_preserved": {
              "authority": "NOT_ADOPTED",
              "consumer": "NONE_PROVEN_AT_PREMAIN",
              "engineering": "SOURCE_DEFINITION_ONLY",
              "human": "NOT_PROVEN",
              "operational": "CANDIDATE_ONLY",
              "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
              "science": "NOT_ISSUED",
              "source_recovery": "SOURCE_EXACT"
            },
            "exact_cut_phase_review": {
              "engineering": "REVISE_MATERIAL_DEFECTS_AT_EXACT_CUT",
              "event_id": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
              "human_evidence": "NOT_PROVEN",
              "native_science": "UNISSUED",
              "owner_authority": "UNISSUED",
              "review": "REVIEW_REVISE_MATERIAL_AT_EXACT_CUT",
              "source": {
                "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
                "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
                "object_type": "blob",
                "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
              },
              "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
              "transition_id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE"
            }
          }
        },
        "editorially_suppressed": [],
        "existing_work_packages": [],
        "gate_decisions": [
          {
            "id": "G-C12-SF-VERIFY",
            "remaining": [
              "C12:LOCAL_GUIDE:READER_ROOT@INTEGRATE",
              "C12:LOCAL_GUIDE:NEW_TUPLE_COLD_SEVERANCE@VERIFY",
              "C12:LOCAL_GUIDE:ACTUAL_ANCHOR@VERIFY"
            ],
            "review_red_at_selected_cut": true,
            "review_red_source_cuts": [
              "598d9e9eaba5143950c63317705fd09104fbf463"
            ],
            "status": "BLOCKED_MEMBERS_UNISSUED"
          }
        ],
        "possible_reverse_targets_not_automatically_unlocked": [],
        "receipts": [
          {
            "code_reader": "NONE",
            "grade": "INDEPENDENT_NEGATIVE_SOURCE",
            "id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE",
            "kind": "REVIEW_REVISE",
            "next_evidence": "Repair exact R2-T1/M1/C1/D1, choose new C9/C12 tuple and cold verify with fresh independent reader; keep 7bf accepted only at 7bf.",
            "owner": "C9_C12_OWNER",
            "source": {
              "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
              "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
            },
            "source_cut": "598d9e9eaba5143950c63317705fd09104fbf463",
            "status": "EXACT_NEGATIVE_REVIEWED"
          }
        ],
        "ref": "C12@VERIFY"
      },
      {
        "affected_typed_edges_not_automatically_promoted": [
          {
            "blocking": false,
            "edge_id": "G-S10-SPECIFY::3",
            "required_ref": "E021@VERIFY",
            "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
            "target_ref": "S10@SPECIFY"
          },
          {
            "blocking": false,
            "edge_id": "G-E008-MATRIX::4",
            "required_ref": "E021@VERIFY",
            "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
            "target_ref": "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY"
          }
        ],
        "current_node_axes": {
          "JOIN_E_7BF": {
            "base_axis_preserved": {
              "authority": "NOT_ADOPTED",
              "consumer": "NONE_PROVEN_AT_PREMAIN",
              "engineering": "SOURCE_DEFINITION_ONLY",
              "human": "NOT_PROVEN",
              "operational": "CANDIDATE_ONLY",
              "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
              "science": "NOT_ISSUED",
              "source_recovery": "SOURCE_EXACT"
            },
            "exact_cut_phase_review": {
              "engineering": "SOURCEFREE_REVIEWED_AT_EXACT_7BF_ONLY",
              "event_id": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
              "human_evidence": "NOT_PROVEN",
              "native_science": "UNISSUED",
              "owner_authority": "UNISSUED",
              "review": "INDEPENDENT_SCOPED_7BF_REVIEWED_SOURCEFREE_ONLY",
              "source": {
                "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
                "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
                "object_type": "blob",
                "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
              },
              "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
              "transition_id": "JOIN_E_7BF_SCOPED_REVIEW"
            }
          }
        },
        "editorially_suppressed": [],
        "existing_work_packages": [],
        "gate_decisions": [],
        "possible_reverse_targets_not_automatically_unlocked": [
          "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY",
          "S10@SPECIFY"
        ],
        "receipts": [
          {
            "code_reader": "class JoinedSession",
            "grade": "SOURCEFREE_SCOPED",
            "id": "JOIN_E_7BF_SCOPED_REVIEW",
            "kind": "SCOPED_REVIEW",
            "next_evidence": "Joint C9 writer/C12 reader exact schema/root/ACK/anchor owner selection, separate new-tuple cold/severance and independent review. No native grant.",
            "owner": "JOIN_E_OWNER",
            "source": {
              "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
              "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
            },
            "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135",
            "status": "SCOPED_SOURCEFREE_ACCEPTED"
          }
        ],
        "ref": "E021@VERIFY"
      },
      {
        "affected_typed_edges_not_automatically_promoted": [
          {
            "blocking": true,
            "edge_id": "G-C9-T-ANY::1",
            "required_ref": "O05@ACCEPT",
            "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
            "target_ref": "C9@INTEGRATE"
          },
          {
            "blocking": true,
            "edge_id": "G-C9-T-IF-ACQUIRED::1",
            "required_ref": "O05@ACCEPT",
            "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
            "target_ref": "C9@ACCEPT"
          }
        ],
        "current_node_axes": {
          "CAN011_RULE_T_MISSING": {
            "base_axis_preserved": {
              "authority": "NOT_ADOPTED",
              "consumer": "NONE_PROVEN_AT_PREMAIN",
              "engineering": "SOURCE_DEFINITION_ONLY",
              "human": "NOT_PROVEN",
              "operational": "CANDIDATE_ONLY",
              "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
              "science": "NOT_ISSUED",
              "source_recovery": "SOURCE_EXACT"
            },
            "exact_cut_phase_review": {
              "engineering": "SOURCE_PRESENT_AUTHOR_TESTED_NOT_NATIVE",
              "event_id": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
              "human_evidence": "NOT_PROVEN",
              "native_science": "UNISSUED",
              "owner_authority": "UNISSUED",
              "review": "UNREVIEWED_RETURN_CANDIDATE",
              "source": {
                "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
                "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
                "object_type": "blob",
                "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
              },
              "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
              "transition_id": "S35_P1_SOURCEFREE_RETURN_ONLY"
            }
          }
        },
        "editorially_suppressed": [],
        "existing_work_packages": [],
        "gate_decisions": [
          {
            "id": "G-O05-POSITIVE-ACCEPT",
            "remaining": [
              "O05:LOCAL_GUIDE:RULE_T_DISCRIMINATOR@SPECIFY",
              "C4:LOCAL_GUIDE:ACTOR_SOURCE@ACCEPT",
              "C8:LOCAL_GUIDE:ACTION_OMISSION@VERIFY"
            ],
            "review_red_at_selected_cut": false,
            "review_red_source_cuts": [],
            "status": "BLOCKED_MEMBERS_UNISSUED"
          },
          {
            "id": "G-C9-T-ANY",
            "remaining": [
              "O05@ACCEPT",
              "O07@ACCEPT"
            ],
            "review_red_at_selected_cut": false,
            "review_red_source_cuts": [],
            "status": "MODE_UNSELECTED_HOLD"
          },
          {
            "id": "G-C9-T-IF-ACQUIRED",
            "remaining": [
              "O05@ACCEPT"
            ],
            "review_red_at_selected_cut": false,
            "review_red_source_cuts": [],
            "status": "MODE_UNSELECTED_HOLD"
          }
        ],
        "possible_reverse_targets_not_automatically_unlocked": [
          "C9@ACCEPT",
          "C9@INTEGRATE"
        ],
        "receipts": [
          {
            "code_reader": "NONE",
            "grade": "TEST_ONLY_SOURCEFREE",
            "id": "S35_P1_SOURCEFREE_RETURN_ONLY",
            "kind": "RETURN_CANDIDATE",
            "next_evidence": "Only a competent CAN011 original Rule T acquired-practice or genuinely evaluated O07 no-change issuance can promote native C9; isolate first-reader access and later performed E2.",
            "owner": "CAN011_OWNER",
            "source": {
              "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
              "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
              "object_type": "blob",
              "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
            },
            "source_cut": "b65c75a9e62618690f7d02265bc9e850af549161",
            "status": "SOURCE_PRESENT_CANDIDATE"
          }
        ],
        "ref": "O05@ACCEPT"
      }
    ],
    "readiness_warning": "ELIGIBLE_PREREQUISITES_ONLY IS NOT TARGET_DONE; ALL SAME-TARGET GATES AND OWNER NATIVE HUMAN EVIDENCE STILL REQUIRED"
  },
  "source_cut": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623"
}
```

### 7.6 `changes-since a9ebf71e...`

```json
{
  "changes": [
    {
      "guide_ref": "E021@VERIFY",
      "id": "JOIN_E_7BF_SCOPED_REVIEW",
      "kind": "SCOPED_REVIEW",
      "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135",
      "status": "SCOPED_SOURCEFREE_ACCEPTED"
    },
    {
      "guide_ref": "O05@ACCEPT",
      "id": "S35_P1_SOURCEFREE_RETURN_ONLY",
      "kind": "RETURN_CANDIDATE",
      "source_cut": "b65c75a9e62618690f7d02265bc9e850af549161",
      "status": "SOURCE_PRESENT_CANDIDATE"
    },
    {
      "guide_ref": "C12@VERIFY",
      "id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE",
      "kind": "REVIEW_REVISE",
      "source_cut": "598d9e9eaba5143950c63317705fd09104fbf463",
      "status": "EXACT_NEGATIVE_REVIEWED"
    }
  ],
  "count": 3,
  "since": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623"
}
```

### 7.7 `freshness`

```json
{
  "adoption": "OWNER_PENDING",
  "changes": 3,
  "changes_since_guide_cut": 3,
  "guide_sha": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
  "journal_head": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
  "not_checked_automatically": "No background fetch, process observation or unseen worker import",
  "pending": [
    {
      "affected_typed_edges_not_automatically_promoted": [],
      "current_node_axes": {
        "JOIN_C12_HOLD": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "REVISE_MATERIAL_DEFECTS_AT_EXACT_CUT",
            "event_id": "57a4676794ee031a6b30f5ac8928a0b97af245338ced5aaea8eb60348a380b93",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "REVIEW_REVISE_MATERIAL_AT_EXACT_CUT",
            "source": {
              "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
              "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [
        {
          "id": "G-C12-SF-VERIFY",
          "remaining": [
            "C12:LOCAL_GUIDE:READER_ROOT@INTEGRATE",
            "C12:LOCAL_GUIDE:NEW_TUPLE_COLD_SEVERANCE@VERIFY",
            "C12:LOCAL_GUIDE:ACTUAL_ANCHOR@VERIFY"
          ],
          "review_red_at_selected_cut": true,
          "review_red_source_cuts": [
            "598d9e9eaba5143950c63317705fd09104fbf463"
          ],
          "status": "BLOCKED_MEMBERS_UNISSUED"
        }
      ],
      "possible_reverse_targets_not_automatically_unlocked": [],
      "receipts": [
        {
          "code_reader": "NONE",
          "grade": "INDEPENDENT_NEGATIVE_SOURCE",
          "id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE",
          "kind": "REVIEW_REVISE",
          "next_evidence": "Repair exact R2-T1/M1/C1/D1, choose new C9/C12 tuple and cold verify with fresh independent reader; keep 7bf accepted only at 7bf.",
          "owner": "C9_C12_OWNER",
          "source": {
            "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
            "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
            "object_type": "blob",
            "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
          },
          "source_cut": "598d9e9eaba5143950c63317705fd09104fbf463",
          "status": "EXACT_NEGATIVE_REVIEWED"
        }
      ],
      "ref": "C12@VERIFY"
    },
    {
      "affected_typed_edges_not_automatically_promoted": [
        {
          "blocking": false,
          "edge_id": "G-S10-SPECIFY::3",
          "required_ref": "E021@VERIFY",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "S10@SPECIFY"
        },
        {
          "blocking": false,
          "edge_id": "G-E008-MATRIX::4",
          "required_ref": "E021@VERIFY",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY"
        }
      ],
      "current_node_axes": {
        "JOIN_E_7BF": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "SOURCEFREE_REVIEWED_AT_EXACT_7BF_ONLY",
            "event_id": "4e60465911c3437250f99655194f2a1410c8369dd2058773ad66522425465bd3",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "INDEPENDENT_SCOPED_7BF_REVIEWED_SOURCEFREE_ONLY",
            "source": {
              "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
              "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
              "object_type": "blob",
              "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "JOIN_E_7BF_SCOPED_REVIEW"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [],
      "possible_reverse_targets_not_automatically_unlocked": [
        "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY",
        "S10@SPECIFY"
      ],
      "receipts": [
        {
          "code_reader": "class JoinedSession",
          "grade": "SOURCEFREE_SCOPED",
          "id": "JOIN_E_7BF_SCOPED_REVIEW",
          "kind": "SCOPED_REVIEW",
          "next_evidence": "Joint C9 writer/C12 reader exact schema/root/ACK/anchor owner selection, separate new-tuple cold/severance and independent review. No native grant.",
          "owner": "JOIN_E_OWNER",
          "source": {
            "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
            "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
            "object_type": "blob",
            "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
          },
          "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135",
          "status": "SCOPED_SOURCEFREE_ACCEPTED"
        }
      ],
      "ref": "E021@VERIFY"
    },
    {
      "affected_typed_edges_not_automatically_promoted": [
        {
          "blocking": true,
          "edge_id": "G-C9-T-ANY::1",
          "required_ref": "O05@ACCEPT",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "C9@INTEGRATE"
        },
        {
          "blocking": true,
          "edge_id": "G-C9-T-IF-ACQUIRED::1",
          "required_ref": "O05@ACCEPT",
          "status": "REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT",
          "target_ref": "C9@ACCEPT"
        }
      ],
      "current_node_axes": {
        "CAN011_RULE_T_MISSING": {
          "base_axis_preserved": {
            "authority": "NOT_ADOPTED",
            "consumer": "NONE_PROVEN_AT_PREMAIN",
            "engineering": "SOURCE_DEFINITION_ONLY",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_ONLY",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "science": "NOT_ISSUED",
            "source_recovery": "SOURCE_EXACT"
          },
          "exact_cut_phase_review": {
            "engineering": "SOURCE_PRESENT_AUTHOR_TESTED_NOT_NATIVE",
            "event_id": "326272437d126c804eb71f58cf1cebfb39ea16e63df584a506c4db4fa92dee59",
            "human_evidence": "NOT_PROVEN",
            "native_science": "UNISSUED",
            "owner_authority": "UNISSUED",
            "review": "UNREVIEWED_RETURN_CANDIDATE",
            "source": {
              "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
              "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
              "object_type": "blob",
              "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
            },
            "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
            "transition_id": "S35_P1_SOURCEFREE_RETURN_ONLY"
          }
        }
      },
      "editorially_suppressed": [],
      "existing_work_packages": [],
      "gate_decisions": [
        {
          "id": "G-O05-POSITIVE-ACCEPT",
          "remaining": [
            "O05:LOCAL_GUIDE:RULE_T_DISCRIMINATOR@SPECIFY",
            "C4:LOCAL_GUIDE:ACTOR_SOURCE@ACCEPT",
            "C8:LOCAL_GUIDE:ACTION_OMISSION@VERIFY"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "BLOCKED_MEMBERS_UNISSUED"
        },
        {
          "id": "G-C9-T-ANY",
          "remaining": [
            "O05@ACCEPT",
            "O07@ACCEPT"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "MODE_UNSELECTED_HOLD"
        },
        {
          "id": "G-C9-T-IF-ACQUIRED",
          "remaining": [
            "O05@ACCEPT"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "MODE_UNSELECTED_HOLD"
        }
      ],
      "possible_reverse_targets_not_automatically_unlocked": [
        "C9@ACCEPT",
        "C9@INTEGRATE"
      ],
      "receipts": [
        {
          "code_reader": "NONE",
          "grade": "TEST_ONLY_SOURCEFREE",
          "id": "S35_P1_SOURCEFREE_RETURN_ONLY",
          "kind": "RETURN_CANDIDATE",
          "next_evidence": "Only a competent CAN011 original Rule T acquired-practice or genuinely evaluated O07 no-change issuance can promote native C9; isolate first-reader access and later performed E2.",
          "owner": "CAN011_OWNER",
          "source": {
            "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
            "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
            "object_type": "blob",
            "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
          },
          "source_cut": "b65c75a9e62618690f7d02265bc9e850af549161",
          "status": "SOURCE_PRESENT_CANDIDATE"
        }
      ],
      "ref": "O05@ACCEPT"
    }
  ],
  "pending_qualification": "SOURCE_GRADED_UPDATES__HQ_ADOPTION_PENDING",
  "revision": 4,
  "runtime": "NO_DAEMON",
  "source_snapshot": {
    "heads": {
      "o_science": {
        "committed_at": "UNKNOWN",
        "ref": "OSCIENCE_CUT",
        "sha": "45efe65f73475e6a815e5fe93c3ee5179de27f67"
      },
      "olive": {
        "committed_at": "UNKNOWN",
        "ref": "origin/agent/sorok-programma-living-reference-s2-sourcegraded-operating-map-r1-20261031",
        "sha": "67f667421fc90b22aad95cfc253a16feabc92348"
      },
      "premain": {
        "committed_at": "UNKNOWN",
        "ref": "origin/integration/pre-main-reconciliation-r1",
        "sha": "UNKNOWN"
      },
      "r3": {
        "committed_at": "UNKNOWN",
        "ref": "origin/agent/sorok-oindex-r3-exact-source-integrity-repair-20261031-r1",
        "sha": "e50d32eb6816578145d17dcd637a0b90b3a1ef40"
      },
      "r3_review": {
        "committed_at": "UNKNOWN",
        "ref": "origin/review/sorok-oindex-r3-independent-source-and-map-acceptance-20261031",
        "sha": "06f40a3eabb4acfc57f433144224695c2427c25f"
      }
    },
    "read_at": "STATIC_FALLBACK",
    "status": "GIT_DISABLED"
  }
}
```

## 8. Candidate patch

```json
{
  "base_guide_sha": "a9ebf71e62d84e5dcc599662e976eca7fcd0e623",
  "instruction": "Qualified HQ edits existing 00/06-15 after owner decision; adapter never silently rewrites guide.",
  "patches": [
    {
      "guide_ref": "C12@VERIFY",
      "proposed_current_stage_gates": [
        {
          "id": "G-C12-SF-VERIFY",
          "remaining": [
            "C12:LOCAL_GUIDE:READER_ROOT@INTEGRATE",
            "C12:LOCAL_GUIDE:NEW_TUPLE_COLD_SEVERANCE@VERIFY",
            "C12:LOCAL_GUIDE:ACTUAL_ANCHOR@VERIFY"
          ],
          "review_red_at_selected_cut": true,
          "review_red_source_cuts": [
            "598d9e9eaba5143950c63317705fd09104fbf463"
          ],
          "status": "BLOCKED_MEMBERS_UNISSUED"
        }
      ],
      "reverse_edges": [],
      "source_return_receipts": [
        {
          "code_reader": "NONE",
          "grade": "INDEPENDENT_NEGATIVE_SOURCE",
          "id": "RRIF_R2_598D_8090_INDEPENDENT_REVISE",
          "kind": "REVIEW_REVISE",
          "next_evidence": "Repair exact R2-T1/M1/C1/D1, choose new C9/C12 tuple and cold verify with fresh independent reader; keep 7bf accepted only at 7bf.",
          "owner": "C9_C12_OWNER",
          "source": {
            "blob": "9d7eeb0970e90bf0bbef1e912cf0f04e97a7de53",
            "commit": "598d9e9eaba5143950c63317705fd09104fbf463",
            "object_type": "blob",
            "path": "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
          },
          "source_cut": "598d9e9eaba5143950c63317705fd09104fbf463",
          "status": "EXACT_NEGATIVE_REVIEWED"
        }
      ]
    },
    {
      "guide_ref": "E021@VERIFY",
      "proposed_current_stage_gates": [],
      "reverse_edges": [
        "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY",
        "S10@SPECIFY"
      ],
      "source_return_receipts": [
        {
          "code_reader": "class JoinedSession",
          "grade": "SOURCEFREE_SCOPED",
          "id": "JOIN_E_7BF_SCOPED_REVIEW",
          "kind": "SCOPED_REVIEW",
          "next_evidence": "Joint C9 writer/C12 reader exact schema/root/ACK/anchor owner selection, separate new-tuple cold/severance and independent review. No native grant.",
          "owner": "JOIN_E_OWNER",
          "source": {
            "blob": "9a185f7c03ac66056e366a2deecf4ea4dd2da188",
            "commit": "7bf2da302996491ddf34b9a039fea47ac982d135",
            "object_type": "blob",
            "path": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
          },
          "source_cut": "7bf2da302996491ddf34b9a039fea47ac982d135",
          "status": "SCOPED_SOURCEFREE_ACCEPTED"
        }
      ]
    },
    {
      "guide_ref": "O05@ACCEPT",
      "proposed_current_stage_gates": [
        {
          "id": "G-O05-POSITIVE-ACCEPT",
          "remaining": [
            "O05:LOCAL_GUIDE:RULE_T_DISCRIMINATOR@SPECIFY",
            "C4:LOCAL_GUIDE:ACTOR_SOURCE@ACCEPT",
            "C8:LOCAL_GUIDE:ACTION_OMISSION@VERIFY"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "BLOCKED_MEMBERS_UNISSUED"
        },
        {
          "id": "G-C9-T-ANY",
          "remaining": [
            "O05@ACCEPT",
            "O07@ACCEPT"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "MODE_UNSELECTED_HOLD"
        },
        {
          "id": "G-C9-T-IF-ACQUIRED",
          "remaining": [
            "O05@ACCEPT"
          ],
          "review_red_at_selected_cut": false,
          "review_red_source_cuts": [],
          "status": "MODE_UNSELECTED_HOLD"
        }
      ],
      "reverse_edges": [
        "C9@ACCEPT",
        "C9@INTEGRATE"
      ],
      "source_return_receipts": [
        {
          "code_reader": "NONE",
          "grade": "TEST_ONLY_SOURCEFREE",
          "id": "S35_P1_SOURCEFREE_RETURN_ONLY",
          "kind": "RETURN_CANDIDATE",
          "next_evidence": "Only a competent CAN011 original Rule T acquired-practice or genuinely evaluated O07 no-change issuance can promote native C9; isolate first-reader access and later performed E2.",
          "owner": "CAN011_OWNER",
          "source": {
            "blob": "02d656868b1963fc6468bab1b25ef98fecdb5141",
            "commit": "b65c75a9e62618690f7d02265bc9e850af549161",
            "object_type": "blob",
            "path": "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py"
          },
          "source_cut": "b65c75a9e62618690f7d02265bc9e850af549161",
          "status": "SOURCE_PRESENT_CANDIDATE"
        }
      ]
    }
  ],
  "status": "HQ_REVIEW_PATCH_CANDIDATE_NOT_APPLIED"
}
```

## 9. Readback inspection

| View | Actual result |
|---|---|
| `whole` | Purpose `PURPOSE_UNCHOSEN_NEIGHBOR` at `PROVISIONAL_PRODUCT_LAW_R1`; 40 unfinished gaps, 11 blocked; three candidate live updates `C12@VERIFY`, `E021@VERIFY`, `O05@ACCEPT`; `source_cut=a9ebf71e...`; `no_new_native_claim=true`. |
| `focus C12@INTEGRATE` | `G-C12-NATIVE-INTEGRATE` is `BLOCKED_MEMBERS_UNISSUED`; all five members remain missing; `target_stage_issued=false`. |
| `source-to-product E021@VERIFY` | Existing node lookup reports `NO_EXISTING_NODE`; importer is `NONE_VERIFIED`; the exact JOIN-E receipt is visible with `code_reader=class JoinedSession` at `7bf2da30...`; `no_transitive_acceptance=true`. |
| `goal C9@INTEGRATE` | `G-C9-NATIVE-INTEGRATE` is `BLOCKED_MEMBERS_UNISSUED`; `G-C9-T-ANY` is `MODE_UNSELECTED_HOLD`; neither gate issued a target stage. |
| `work-now` | 28 existing P0/P1 candidates and 6 parallel groups remain; live refs are exactly `C12@VERIFY`, `E021@VERIFY`, `O05@ACCEPT`; `programma_live.changed_refs` is the same three refs; `no_agent_dispatch=true`. |
| `changes-since a9ebf71e...` | Count 3, in journal order: `JOIN_E_7BF_SCOPED_REVIEW`, `S35_P1_SOURCEFREE_RETURN_ONLY`, `RRIF_R2_598D_8090_INDEPENDENT_REVISE`. |
| `freshness` | Head `57a46767...`, revision 4, changes 3, pending refs `C12@VERIFY`, `E021@VERIFY`, `O05@ACCEPT`; `SOURCE_GRADED_UPDATES__HQ_ADOPTION_PENDING`; `OWNER_PENDING`; `NO_DAEMON`. |
| `candidate-patch` | `HQ_REVIEW_PATCH_CANDIDATE_NOT_APPLIED` at base guide `a9ebf71e...`; three exact receipt groups; no guide file was written. |

No view promotes sourcefree evidence to native, human, product, or first-consumer acceptance. The S35 receipt remains `SOURCE_PRESENT_CANDIDATE` with `code_reader=NONE`; the JOIN-E receipt remains scoped to `7bf2da30...`; the RRIF negative remains `REVIEW_REVISE_MATERIAL_AT_EXACT_CUT` at `598d9e9e...`.

## 10. Artifact hashes

```text
3642fb012dadd5ccbb77186f4aa49063961abecb6142696b75fa552c9c4b0e2d  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/view_1_whole.json
6b4eabc1d7a5633b864641eb1d28f577752b9eff3a7a3b790b3be1c1bcaef5a7  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/view_2_focus_c12.json
5d247ed01714608d1d24ddf98210225ad086fb080e24687237d5edbceb53f46a  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/view_3_source_to_product_e021.json
8660174f66de0c157b0e81df9ded877367938ac40e0a9c4b1e4cf59fe4ac5d6b  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/view_4_goal_c9.json
25e229d0b1cfe2e6f2b0e3b92e5dffa7f33959345c5acb3b0e15f624a8f531eb  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/view_5_work_now.json
d4c4dfca8da3ad88245d5e0d9c29539c05ae338030874638cbbec64150326f47  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/view_6_changes_since.json
197775f59655dbe6c2f4a5cc4df40b9dc97bf71e2454751ac5a34a0efeb6410f  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/view_7_freshness.json
c4df30c9bb9730f2a2a09809994fd6552f44f8053ef13e5fd56fb8f3716ba0ff  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/view_8_candidate_patch.json
a16b2a15e7e00e390877b70da3ab3ac960f72351e8c3990040024c07e81b3efa  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/sorok-live02-r1-final-cold/state.warm.json
```

## 11. Boundary

This is a sourcefree cold replay. It does not establish a native continuing person, a C9/C12 native writer or reader, an owner-adopted guide, a human A5 result, a production runtime, or an independent review. The seven views are readbacks over the existing P0/P1 engine and the frozen W8-R guide; they create no second graph, database, scheduler, or journal.
