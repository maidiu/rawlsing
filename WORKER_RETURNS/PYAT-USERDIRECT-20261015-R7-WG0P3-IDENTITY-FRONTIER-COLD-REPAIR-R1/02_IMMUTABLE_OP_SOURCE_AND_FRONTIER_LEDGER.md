# Immutable Operation, Source and Frontier Ledger

## Frontier: 25 Operations

| Disposition | Count | Reason |
|-------------|-------|--------|
| PRODUCED | 3 | Permitted + GRANTED_FIXTURE |
| HELD | 16 | Grant/route/unproved/cross-unit |
| INADMISSIBLE | 6 | Cross-wave/source/unit |
| **Total** | **25** | |

## PRODUCED Operations (3)

| Op ID | Target | Item IDs | Risk Set | Release |
|-------|--------|----------|----------|---------|
| OP-WG0P-ORD-01-MARGINAL | WG0P-ORD-01 | WG0P-ORD-01 | R_ORD | REL-A-W1 |
| OP-WG0P-HH-MR-02-MARGINAL | WG0P-HH-MR-02 | WG0P-HH-MR-02 | R_HH | REL-A-W1 |
| OP-WG0P-ORD-05-MARGINAL | WG0P-ORD-05 | WG0P-ORD-05 | R_ORD2 | REL-A-W2 |

## HELD Operations (16)

- 5 marginals: ROUTED-03 (no route evidence), ORD-04 (WITHDRAWN grant)
- 11 conditionals: grant/route failures, same-grain JOINT_RISK_SET_UNPROVED

## INADMISSIBLE Operations (6)

- Cross-wave pairs: ORD-01↔ORD-04, ORD-01↔ORD-05
- Cross-source pairs: ORD-01↔ORD-04, ORD-05↔ORD-04
- Cross-unit pairs: ORD-01↔HH-MR-02, ORD-05↔HH-MR-02

## Source Editions

| Release | Source Edition | Source Bytes Hash |
|---------|---------------|-------------------|
| REL-A-W1 | SRC-EDITION-REL-A-W1-W1-v1 | (from actual rows) |
| REL-A-W2 | SRC-EDITION-REL-A-W2-W2-v1 | (from actual rows) |
| REL-B-W2 | SRC-EDITION-REL-B-W2-W2-v1 | (from actual rows) |

## Identity Binding

Each operation binds: `op_id, op_class, target, conditioners, disposition_reason, native_item_ids, risk_name, source_edition, grant, full_identity_hash`. Duplicate IDs with altered semantics are rejected.

## Frontier Enforcement

`validate_frontier` enforces exact counts 3/16/6=25. `validate_frontier_receipts` enforces exact set, status, reason, target, conditioners, item_ids match. Removing even a HELD or INADMISSIBLE operation is rejected.

## WG0P2 Documentary Error

WG0P2's ledger JSON declared `3+16+10=29` despite `total=25`. Actual oracle has `3+16+6=25`. This is both a documentary error and a separate operational omitted-frontier defect.
