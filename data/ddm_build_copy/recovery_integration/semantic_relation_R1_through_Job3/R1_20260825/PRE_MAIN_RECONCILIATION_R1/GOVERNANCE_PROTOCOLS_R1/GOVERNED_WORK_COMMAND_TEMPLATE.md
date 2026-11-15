# GOVERNED WORK COMMAND TEMPLATE R1

Use this scaffold for future significant Rawlsing work.

```text
CANONICAL_PROJECT_HEAD: <exact SHA>
GROUND_VERSION: <version>
GROUNDING_RECEIPT: <receipt ID/ref or BOUNDED_EXECUTION_PARENT>
MODE: <GROUNDED_PROJECT_DECISION | GROUNDED_BOUNDED_EXECUTION | FORENSIC_READ_ONLY | DELIBERATELY_UNGROUNDED_EXPLORATION | HOSTILE_INDEPENDENT_AUDIT>
JURISDICTION: <exact>
STATE_IDS: <IDs>
OBLIGATION_IDS: <IDs>
AUTHORITY_CEILING: <exact>
RETURN_TO: <central/campaign destination>
WRITE_SCOPE: <exact paths/branch>
FORBIDDEN_ASSUMPTIONS: <explicit list>

QUESTION_BEING_ANSWERED:
<one exact project question>

LOCAL_SUCCESS:
<what this worker can complete locally>

PROJECT_CLOSURE:
<what additional reconciliation/adoption would be required before project-level CLOSED>

DEPENDENCIES:
<exact state/obligation IDs>

SUCCESSOR_SPAWN_POLICY:
Any newly necessary successor must receive a new obligation ID and explicit RETURN_TO edge. Spawning a successor does not close this parent.

MISSION:
<task-specific command>

RETURN REQUIREMENTS:
- what was accomplished;
- what was not accomplished;
- touched obligations and dispositions;
- new obligations;
- spawned successors and RETURN_TO destinations;
- authority actually obtained / explicitly not obtained;
- local status;
- reintegration status;
- required next central action.
```

A bounded mechanical worker need not reread the entire project if it inherits a valid exact grounded parent adjudication and stays inside its frozen jurisdiction. Any reinterpretation outside that frozen adjudication requires escalation to a grounded project-decision agent.
