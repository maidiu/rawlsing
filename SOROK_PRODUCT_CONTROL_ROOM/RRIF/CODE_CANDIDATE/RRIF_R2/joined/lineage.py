"""Shared branch-lineage contract for joined and targetless sessions.

The C12 store can create real forks. Session metadata must not be able to
select an arbitrary branch independently of that store. This module records the
actual created branch clock/root and validates the full parent-child chain.
"""
from __future__ import annotations

ROOT_BRANCH = 'first_session'


def _receipt(parent: str, created: dict) -> dict:
    return {
        'parent_branch': parent,
        'new_branch': created.get('branch_id'),
        'fork_clock': created.get('fork_clock'),
        'root_hash': created.get('root_hash'),
        'created_clock': created.get('created_clock'),
    }


def new_lineage(parent: str, previous: dict | None, created: dict) -> dict:
    """Build the next lineage record from the actual created branch row."""
    if created.get('parent_branch_id') != parent:
        raise ValueError('FORK_PARENT_MISMATCH')
    if not created.get('branch_id') or created.get('branch_id') == parent:
        raise ValueError('FORK_NEW_BRANCH_INVALID')
    if created.get('fork_clock') is None or not created.get('root_hash'):
        raise ValueError('FORK_RECEIPT_INCOMPLETE')
    previous = previous or {}
    receipts = list(previous.get('fork_receipts') or [])
    if not receipts and previous.get('fork_receipt'):
        receipts.append(previous['fork_receipt'])
    receipts.append(_receipt(parent, created))
    return {
        'root_branch': previous.get('root_branch', ROOT_BRANCH),
        'current_branch': created['branch_id'],
        'fork_receipts': receipts,
        'fork_receipt': receipts[-1],
    }


def validate(meta: dict, branch_id: str, store) -> dict:
    """Validate metadata branch selection against the actual C12 branch rows."""
    checks: dict[str, bool] = {}
    observed: dict = {'branch_id': branch_id}
    lineage = meta.get('branch_lineage')
    try:
        if not lineage:
            checks['no_lineage_is_root_session'] = branch_id == ROOT_BRANCH
            row = store.branch(branch_id)
            checks['parent_is_c12_root'] = row.get('parent_branch_id') in (None, '', 'root')
            observed['branch'] = row
            return {'ok': all(checks.values()), 'checks': checks,
                    'observed': observed}
        checks['lineage_is_mapping'] = isinstance(lineage, dict)
        checks['root_branch'] = lineage.get('root_branch') == ROOT_BRANCH
        checks['current_matches_selection'] = (
            lineage.get('current_branch') == branch_id)
        receipts = list(lineage.get('fork_receipts') or [])
        if not receipts and lineage.get('fork_receipt'):
            receipts = [lineage['fork_receipt']]
        checks['receipts_present'] = bool(receipts)
        checks['last_receipt_matches_current'] = bool(
            receipts and receipts[-1].get('new_branch') == branch_id)
        checks['first_parent_is_root'] = bool(
            receipts and receipts[0].get('parent_branch') == ROOT_BRANCH)
        chain_ok = True
        for index, receipt in enumerate(receipts):
            parent = receipt.get('parent_branch')
            child = receipt.get('new_branch')
            clock = receipt.get('fork_clock')
            root_hash = receipt.get('root_hash')
            created_clock = receipt.get('created_clock')
            if not parent or not child or child == parent:
                chain_ok = False
                continue
            if type(clock) is not int or not isinstance(root_hash, str) or not root_hash:
                chain_ok = False
                continue
            if type(created_clock) is not int:
                chain_ok = False
                continue
            row = store.branch(child)
            if row.get('parent_branch_id') != parent:
                chain_ok = False
            if row.get('fork_clock') != clock:
                chain_ok = False
            if row.get('root_hash') != root_hash:
                chain_ok = False
            if row.get('created_clock') != created_clock:
                chain_ok = False
            if index and receipts[index - 1].get('new_branch') != parent:
                chain_ok = False
        checks['receipt_chain_matches_store'] = chain_ok
        branch_row = store.branch(branch_id)
        checks['selected_branch_exists'] = bool(branch_row)
        checks['selected_is_last_child'] = bool(
            receipts and branch_row.get('parent_branch_id') ==
            receipts[-1].get('parent_branch'))
        observed['branch'] = branch_row
        observed['lineage'] = lineage
    except Exception as exc:  # missing branch/store refusal is a failed line
        checks['lineage_readable'] = False
        observed['error'] = type(exc).__name__ + ':' + str(exc)
    checks.setdefault('lineage_readable', True)
    return {'ok': all(checks.values()), 'checks': checks, 'observed': observed}

class ForkContractError(ValueError):
    """Typed invalid-fork or fork-transaction refusal."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}:{detail}")
        self.code = code


def validate_fork_request(store, parent: str, new_branch_id: str) -> None:
    """Validate identity against the actual store before any mutation."""
    if not isinstance(new_branch_id, str) or not new_branch_id.strip():
        raise ForkContractError('FORK_BRANCH_EMPTY')
    if new_branch_id == parent:
        raise ForkContractError('FORK_BRANCH_IS_CURRENT')
    if store._branch(parent) is None:
        raise ForkContractError('FORK_PARENT_ABSENT')
    if store._branch(new_branch_id) is not None:
        raise ForkContractError('FORK_BRANCH_EXISTS')


def create_fork(product, parent: str, new_branch_id: str,
                previous: dict | None) -> tuple[dict, dict]:
    """Create and record one fork atomically; rollback on receipt failure.

    ``C12Store`` uses autocommit, so an explicit SQLite savepoint is required
    for the branch insert, copied rows, root update and receipt validation.
    """
    store = product.store
    validate_fork_request(store, parent, new_branch_id)
    store.db.execute('SAVEPOINT join_fork')
    try:
        fork = product.fork(new_branch_id)
        created = fork.get('branch')
        if not created:
            raise ForkContractError('FORK_BRANCH_RECORD_MISSING')
        lineage = new_lineage(parent, previous, created)
        store.db.execute('RELEASE join_fork')
        return fork, lineage
    except Exception:
        try:
            store.db.execute('ROLLBACK TO join_fork')
            store.db.execute('RELEASE join_fork')
        except Exception:  # noqa: BLE001 - preserve original fork failure
            pass
        raise
