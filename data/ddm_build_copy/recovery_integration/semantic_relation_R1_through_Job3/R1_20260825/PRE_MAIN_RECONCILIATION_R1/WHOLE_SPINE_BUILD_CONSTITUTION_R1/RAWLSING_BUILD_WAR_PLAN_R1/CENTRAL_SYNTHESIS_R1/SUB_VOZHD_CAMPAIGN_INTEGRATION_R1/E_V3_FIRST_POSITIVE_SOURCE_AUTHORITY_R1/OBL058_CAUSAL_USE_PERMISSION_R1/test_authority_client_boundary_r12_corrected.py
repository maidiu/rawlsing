"""Corrected producer-court surface for OBL058 R12.

The first governed execution established the R12 behavior but exposed one test
expectation mismatch: assignment to the read-only native identity property raises
AttributeError, not TypeError. This module changes only that assertion while
retaining the complete original R12 producer court unchanged otherwise.

Producer-side verification only. No self-review or independent review occurs.
"""
from __future__ import annotations

import test_authority_client_boundary_r12 as _source


def _corrected_native_client_type_contract(self):
    client = self.client
    client_type = type(client)
    with self.assertRaises(TypeError):
        client_type()
    with self.assertRaises(TypeError):
        object.__new__(client_type)
    with self.assertRaises(TypeError):
        setattr(client_type, "__call__", lambda *a, **k: _source.c.DECISION_PERMIT)
    with self.assertRaises(TypeError):
        client.__class__ = object
    with self.assertRaises(AttributeError):
        client.retained_capability_identity = 1
    with self.assertRaises(TypeError):
        _source.weakref.ref(client)
    with self.assertRaises(TypeError):
        class DerivedClient(client_type):
            pass
    for operation in (
        lambda: _source.copy.copy(client),
        lambda: _source.copy.deepcopy(client),
        lambda: _source.pickle.dumps(client),
        lambda: _source.json.dumps(client),
    ):
        with self.assertRaises(TypeError):
            operation()


_source.OBL058AuthorityClientBoundaryR12Court.test_r12_07_native_client_type_is_nonforgeable_nonmutable_and_nonserializable = _corrected_native_client_type_contract
OBL058AuthorityClientBoundaryR12Court = _source.OBL058AuthorityClientBoundaryR12Court
