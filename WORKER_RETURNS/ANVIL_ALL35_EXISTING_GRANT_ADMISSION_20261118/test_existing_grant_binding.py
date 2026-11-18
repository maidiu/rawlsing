#!/usr/bin/env python3
"""Request-only tests for the accepted SRC04 grant route; no source I/O."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = Path(os.environ.get("ANVIL_R157_SNAPSHOT",
    "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil-aee954-r157")).resolve()
sys.path.insert(0, str(SNAP))
import existing_grant_binding as m
from rawlsing_next.pre553_r157_projection_adapter import SourceReadAdmissionRefusal, SourceReadRequest


def config():
    return m.ConfigBinding(**json.loads((HERE / "fixtures/SRC04_CONFIG_BINDING.json").read_text()))


def trust(grant_path=None, grant_sha=None):
    raw = json.loads((HERE / "TRUST_POLICY.json").read_text())
    return m.ExternalTrust(**{
        **{k: raw[k] for k in ("grant_sha256", "config_file_sha256",
                               "config_canonical_sha256", "config_binding_sha256")},
        "grant_path": str(grant_path or HERE / raw["grant_path"]),
        **({"grant_sha256": grant_sha} if grant_sha else {}),
    })


def grant_path():
    return HERE / "fixtures/SRC04_FULL_SOURCE_GRANT.json"


class ExistingGrantBindingTests(unittest.TestCase):
    def test_actual_src04_request_only_allowed(self):
        result = m.bind_existing_grant(grant_path=grant_path(), config=config(), trust=trust())
        self.assertEqual(result.status, "REQUEST_ONLY_ALLOWED")
        self.assertEqual(result.grant_sha256,
                         "d8f13c67af276175266168e9af1a91e28fd543fcecadc1e79112a9854b4a8139")
        self.assertEqual(result.request.source_id, "SRC04")
        self.assertEqual(result.request.custody_locator_binding,
                         "SRC04_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING")
        self.assertEqual(result.decision.currentness, "CURRENT_GRANTED")
        self.assertEqual(result.decision.revocation_ref, None)
        self.assertEqual(result.decision.retention_export_limits, m.RETENTION_EXPORT_LIMITS)

    def test_resolver_rechecks_same_bound_permission_twice(self):
        result = m.bind_existing_grant(grant_path=grant_path(), config=config(), trust=trust())
        resolver = m.ExistingGrantResolver(grant_path(), trust(), result.request)
        first = resolver.resolve_current(result.request)
        second = resolver.resolve_current(result.request)
        self.assertEqual(first, second)
        self.assertEqual(first, result.decision)
        self.assertEqual(resolver.calls, 2)

    def test_wrong_request_refused(self):
        result = m.bind_existing_grant(grant_path=grant_path(), config=config(), trust=trust())
        resolver = m.ExistingGrantResolver(grant_path(), trust(), result.request)
        wrong = dataclasses.replace(result.request, host="OTHER_HOST")
        with self.assertRaises(SourceReadAdmissionRefusal) as ctx:
            resolver.resolve_current(wrong)
        self.assertEqual(ctx.exception.code, "FULL_GRANT_REQUEST_MISMATCH")

    def test_grant_drift_refused_on_recheck(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "grant.json"
            p.write_bytes(grant_path().read_bytes())
            t = trust(p)
            result = m.bind_existing_grant(grant_path=p, config=config(), trust=t)
            resolver = m.ExistingGrantResolver(p, t, result.request)
            self.assertEqual(resolver.resolve_current(result.request).currentness, "CURRENT_GRANTED")
            p.write_bytes(p.read_bytes() + b"\n")
            with self.assertRaises(SourceReadAdmissionRefusal) as ctx:
                resolver.resolve_current(result.request)
            self.assertEqual(ctx.exception.code, "FULL_GRANT_CURRENTNESS_MISMATCH")

    def test_grant_location_drift_refused(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "grant.json"
            p.write_bytes(grant_path().read_bytes())
            t = trust(HERE / "fixtures/SRC04_FULL_SOURCE_GRANT.json")
            with self.assertRaises(m.BindingRefusal) as ctx:
                m.bind_existing_grant(grant_path=p, config=config(), trust=t)
            self.assertEqual(ctx.exception.code, "GRANT_LOCATION_MISMATCH")

    def test_revoked_grant_refused(self):
        with tempfile.TemporaryDirectory() as td:
            doc = json.loads(grant_path().read_text())
            doc["revocation"] = "REVOKED"
            p = Path(td) / "grant.json"
            p.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
            t = trust(p, hashlib.sha256(p.read_bytes()).hexdigest())
            with self.assertRaises(m.BindingRefusal) as ctx:
                m.bind_existing_grant(grant_path=p, config=config(), trust=t)
            self.assertEqual(ctx.exception.code, "GRANT_REVOKED")

    def test_wrong_scope_refused(self):
        with tempfile.TemporaryDirectory() as td:
            doc = json.loads(grant_path().read_text())
            doc["scope"] = "FIRST_SLICE_ONLY"
            p = Path(td) / "grant.json"
            p.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
            t = trust(p, hashlib.sha256(p.read_bytes()).hexdigest())
            with self.assertRaises(m.BindingRefusal) as ctx:
                m.bind_existing_grant(grant_path=p, config=config(), trust=t)
            self.assertEqual(ctx.exception.code, "GRANT_SCOPE_NOT_FULL")

    def test_snapshot_presence_alone_is_not_permission(self):
        t = m.ExternalTrust(**{**trust().__dict__, "grant_sha256": "0" * 64})
        with self.assertRaises(m.BindingRefusal) as ctx:
            m.bind_existing_grant(grant_path=grant_path(), config=config(), trust=t)
        self.assertEqual(ctx.exception.code, "GRANT_TRUST_HASH_MISMATCH")

    def test_wrong_survey_config_refused(self):
        c = config()
        bad = m.ConfigBinding(**{**c.__dict__, "source_id": "SRC17"})
        with self.assertRaises(m.BindingRefusal) as ctx:
            m.bind_existing_grant(grant_path=grant_path(), config=bad, trust=trust())
        self.assertEqual(ctx.exception.code, "CONFIG_SOURCE_NOT_SRC04")

    def test_expanded_operation_or_extent_refused(self):
        c = config()
        base = dict(
            source_id=c.source_id, source_sha256=c.source_sha256,
            source_format=c.source_format, custody_locator_binding=c.locator_id,
            host="USER_LOCAL_MAC", purpose=m.SRC04_PURPOSE,
            consumer_use=m.SRC04_CONSUMER,
            metadata_freeze_refs=c.metadata_freeze_refs,
            semantic_use_scope=m.SRC04_SEMANTIC_SCOPE)
        with self.assertRaises(SourceReadAdmissionRefusal):
            SourceReadRequest(**base, read_operation="I03_QUERY")
        with self.assertRaises(SourceReadAdmissionRefusal):
            SourceReadRequest(**base, physical_read_extent="SLICE")

    def test_src17_scope_is_construction_only_and_not_reusable(self):
        scope = m.check_src17_reuse_scope(
            grant_path=HERE / "fixtures/SRC17_USER_GRANT.json",
            authentication_path=HERE / "fixtures/SRC17_GRANT_AUTHENTICATION.json",
            expected_grant_sha256="d6272ba68d737fa9da27704e18bf6ee00ef1d31f685ba76f84f4a0dcc4764e3d",
            expected_authentication_sha256="f7fb429bb77779556e2e0a591ea2b089bf1f0a97d85d059545baf5fd66dd052b")
        self.assertFalse(scope["reusable_for_src04_binding"])
        self.assertFalse(scope["reusable_for_i03_i05"])
        self.assertTrue(scope["scope_is_source_specific"])
        self.assertTrue(scope["no_i03_i05_expansion"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
