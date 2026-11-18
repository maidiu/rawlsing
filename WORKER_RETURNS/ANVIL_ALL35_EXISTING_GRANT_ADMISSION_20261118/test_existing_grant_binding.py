#!/usr/bin/env python3
"""Request-only tests for the existing-grant binding; no source I/O.

The positive CURRENT witness below is generated in-test with a TEST_ONLY key.
It exercises the external-trust/signature contract, not production authority.
"""
from __future__ import annotations

import copy
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
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from rawlsing_next.pre553_r157_projection_adapter import SourceReadAdmissionRefusal


def config():
    raw = json.loads((HERE / "fixtures/SRC04_CONFIG_BINDING.json").read_text())
    return m.ConfigBinding(**raw)


def trust():
    raw = json.loads((HERE / "TRUST_POLICY.json").read_text())
    return m.ExternalTrust(**{k: raw[k] for k in (
        "grant_sha256", "config_file_sha256", "config_canonical_sha256",
        "config_binding_sha256", "current_issuer", "current_public_key_hex",
        "current_evidence_sha256")})


def grant_bytes_path():
    return HERE / "fixtures/SRC04_FULL_SOURCE_GRANT.json"


def private_key():
    return Ed25519PrivateKey.generate()


def pubhex(key):
    return key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()


def signed_evidence(binding, key, issuer, currentness="CURRENT_GRANTED",
                     revocation_ref=None, limits=None, grant_ref=None,
                     permission_refs=None):
    request = binding.request
    grant_ref = binding.grant_ref if grant_ref is None else grant_ref
    payload = {
        "issuer": issuer,
        "grant_sha256": grant_ref.content_hash,
        "decision_ref": m._expected_decision_ref(request, grant_ref).as_dict(),
        "source_permission_refs": [r.as_dict() for r in (permission_refs or (grant_ref,))],
        "request_digest": m._request_digest(request),
        "currentness": currentness,
        "revocation_ref": revocation_ref,
        "effective_interval": "2026-11-18/TEST_ONLY_CURRENT_WITNESS",
        "retention_export_limits": limits or {
            "export": "DENY", "rowwise_response_artifacts": "DENY",
            "retention": "LOCAL_RUNTIME_ONLY", "source_bytes_in_git": "DENY",
        },
    }
    return {"payload": payload,
            "signature": key.sign(m._canonical(payload)).hex()}


class ExistingGrantBindingTests(unittest.TestCase):
    def test_actual_src04_structural_request_is_held_without_current(self):
        result = m.bind_existing_grant(grant_path=grant_bytes_path(), config=config(), trust=trust())
        self.assertEqual(result.status, "RUNTIME_ISSUER_HOLD__INDEPENDENT_CURRENT_EVIDENCE_MISSING")
        self.assertIsNone(result.decision)
        self.assertEqual(result.request.source_id, "SRC04")
        self.assertEqual(result.request.source_sha256,
                         "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18")
        self.assertEqual(result.request.custody_locator_binding,
                         "SRC04_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING")
        self.assertEqual(result.grant_sha256,
                         "d8f13c67af276175266168e9af1a91e28fd543fcecadc1e79112a9854b4a8139")
        self.assertEqual(result.request.semantic_use_scope, tuple(sorted(m.SRC04_SEMANTIC_SCOPE)))

    def test_external_signed_current_can_bind_request_only(self):
        base = m.bind_existing_grant(grant_path=grant_bytes_path(), config=config(), trust=trust())
        key = private_key()
        issuer = "TEST_ONLY_EXTERNAL_CURRENT_ISSUER"
        evidence = signed_evidence(base, key, issuer)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "current.json"
            raw = json.dumps(evidence).encode()
            p.write_bytes(raw)
            t = m.ExternalTrust(
                grant_sha256=trust().grant_sha256,
                config_file_sha256=trust().config_file_sha256,
                config_canonical_sha256=trust().config_canonical_sha256,
                config_binding_sha256=trust().config_binding_sha256,
                current_issuer=issuer,
                current_public_key_hex=pubhex(key),
                current_evidence_sha256=hashlib.sha256(raw).hexdigest(),
            )
            result = m.bind_existing_grant(
                grant_path=grant_bytes_path(), config=config(), trust=t,
                current_evidence_path=p)
            self.assertEqual(result.status, "CURRENT_BOUND_REQUEST_ONLY")
            self.assertIsNotNone(result.decision)
            self.assertEqual(result.decision.currentness, "CURRENT_GRANTED")
            self.assertIsNone(result.decision.revocation_ref)
            self.assertEqual(result.decision.source_permission_refs, (result.grant_ref,))
            resolver = m.ExistingGrantResolver(result)
            self.assertEqual(resolver.resolve_current(result.request), result.decision)

    def test_static_grant_alone_never_creates_current(self):
        result = m.bind_existing_grant(grant_path=grant_bytes_path(), config=config(), trust=trust())
        self.assertIsNone(result.decision)
        self.assertEqual(result.reason, "STATIC_GRANT_HASH_IS_NOT_CURRENT")
        with self.assertRaises(SourceReadAdmissionRefusal) as ctx:
            m.ExistingGrantResolver(result).resolve_current(result.request)
        self.assertEqual(ctx.exception.code, "SOURCE_READ_CURRENT_EVIDENCE_HOLD")

    def test_grant_bytes_trust_mismatch(self):
        t = trust()
        bad = m.ExternalTrust(**{**t.__dict__, "grant_sha256": "0" * 64})
        with self.assertRaises(m.BindingRefusal) as ctx:
            m.bind_existing_grant(grant_path=grant_bytes_path(), config=config(), trust=bad)
        self.assertEqual(ctx.exception.code, "GRANT_TRUST_HASH_MISMATCH")

    def test_bad_current_signature_refused(self):
        base = m.bind_existing_grant(grant_path=grant_bytes_path(), config=config(), trust=trust())
        key = private_key()
        issuer = "TEST_ONLY_EXTERNAL_CURRENT_ISSUER"
        evidence = signed_evidence(base, key, issuer)
        evidence["signature"] = "00" * 64
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "current.json"
            p.write_text(json.dumps(evidence))
            t = m.ExternalTrust(
                grant_sha256=trust().grant_sha256,
                config_file_sha256=trust().config_file_sha256,
                config_canonical_sha256=trust().config_canonical_sha256,
                config_binding_sha256=trust().config_binding_sha256,
                current_issuer=issuer,
                current_public_key_hex=pubhex(key),
                current_evidence_sha256=None,
            )
            with self.assertRaises(m.BindingRefusal) as ctx:
                m.bind_existing_grant(grant_path=grant_bytes_path(), config=config(), trust=t,
                                      current_evidence_path=p)
            self.assertEqual(ctx.exception.code, "CURRENT_EVIDENCE_SIGNATURE_INVALID")

    def test_noncurrent_or_revoked_refused(self):
        base = m.bind_existing_grant(grant_path=grant_bytes_path(), config=config(), trust=trust())
        key = private_key()
        issuer = "TEST_ONLY_EXTERNAL_CURRENT_ISSUER"
        for evidence, code in (
            (signed_evidence(base, key, issuer, currentness="HELD"), "CURRENT_EVIDENCE_NOT_CURRENT"),
            (signed_evidence(base, key, issuer,
                             revocation_ref={"kind": "REVOCATION", "object_id": "r", "content_hash": "a" * 64}),
             "CURRENT_EVIDENCE_REVOKED"),
        ):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "current.json"
                p.write_text(json.dumps(evidence))
                t = m.ExternalTrust(
                    grant_sha256=trust().grant_sha256,
                    config_file_sha256=trust().config_file_sha256,
                    config_canonical_sha256=trust().config_canonical_sha256,
                    config_binding_sha256=trust().config_binding_sha256,
                    current_issuer=issuer,
                    current_public_key_hex=pubhex(key),
                    current_evidence_sha256=None,
                )
                with self.assertRaises(m.BindingRefusal) as ctx:
                    m.bind_existing_grant(grant_path=grant_bytes_path(), config=config(), trust=t,
                                          current_evidence_path=p)
                self.assertEqual(ctx.exception.code, code)

    def test_wrong_survey_config_refused(self):
        c = config()
        bad = m.ConfigBinding(**{**c.__dict__, "source_id": "SRC17"})
        with self.assertRaises(m.BindingRefusal) as ctx:
            m.bind_existing_grant(grant_path=grant_bytes_path(), config=bad, trust=trust())
        self.assertEqual(ctx.exception.code, "CONFIG_SOURCE_NOT_SRC04")

    def test_expanded_operation_or_extent_refused(self):
        from rawlsing_next.pre553_r157_projection_adapter import SourceReadRequest
        c = config()
        base = dict(
            source_id=c.source_id, source_sha256=c.source_sha256,
            source_format=c.source_format, custody_locator_binding=c.locator_id,
            host="USER_LOCAL_MAC", purpose="FULL_SRC04_ORIGINAL_C11_CONSTRUCTION",
            consumer_use="EXISTING_PRE553_SOURCE_BACKED_C11",
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
