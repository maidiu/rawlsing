"""Exact R157 config to incumbent R17 packed-routing bridge.

Only indexed nonrespondent fixtures are executed. Original configs are read
as instrument documents, never as original source authorization or data.
"""
import hashlib
import json
import subprocess
import tempfile
import time
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from rawlsing_next import pre553_r157_projection_adapter as adapter
from rawlsing_next import pre553_source_backed_c11_facade as facade
from rawlsing_next import pre553_empirical_objects as objects

CUT="1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
INDEX="source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json"
INDEX_BLOB="ce68c271e1039ee56d2e53941c05d34a38c0d531"


def git_bytes(path):
    return subprocess.check_output(["git","show",f"{CUT}:{path}"])


class R157RuleGrainBridge(unittest.TestCase):
    def test_actual_indexed_configs_and_fixture_releases(self):
        self.assertEqual(subprocess.check_output(
            ["git","rev-parse",f"{CUT}:{INDEX}"],text=True).strip(),INDEX_BLOB)
        raw=git_bytes(INDEX)
        index=json.loads(raw)
        by_id={r["source_id"]:r for r in index["sources"]}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            ix=root/INDEX;ix.parent.mkdir(parents=True);ix.write_bytes(raw)
            for sid in ("SRC04","SRC16","SRC35"):
                with self.subTest(source=sid):
                    row=by_id[sid]
                    for path_key,sha_key in (
                        ("original_config_path","original_config_file_sha256"),
                        ("fixture_config_path","fixture_config_file_sha256"),
                        ("fixture_path","fixture_file_sha256"),
                    ):
                        path=row[path_key];data=git_bytes(path)
                        self.assertEqual(hashlib.sha256(data).hexdigest(),row[sha_key])
                        dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True)
                        dest.write_bytes(data)
                    library=adapter.SourceConfigLibrary(index_path=ix,root=root)
                    original=library.load_original(sid)
                    self.assertEqual(adapter.canonical_config_hash(original),
                                     row["original_config_canonical_sha256"])
                    config=library.load_fixture_config(sid)
                    stream=library.load_fixture_stream(sid)
                    keys=adapter._effective_row_native_keys(
                        config,stream=stream,incidence=None,explicit=None,batch_size=10000)
                    options=dict(source_sha256=stream.source_sha256,
                                 row_count=stream.row_count,row_native_keys=keys)
                    t=time.monotonic()
                    expanded=adapter.build_governed_c11_projection(config,**options)
                    expanded_seconds=time.monotonic()-t
                    t=time.monotonic()
                    packed=adapter.build_governed_c11_projection(
                        config,**options,packed_routing=True)
                    packed_seconds=time.monotonic()-t
                    self.assertIs(type(packed.routing),facade._PackedRoutingFacts)
                    self.assertEqual(tuple(packed.routing),expanded.routing)
                    self.assertEqual(packed.cache_identity(),expanded.cache_identity())
                    adapter.verify_config_projection_binding(config,packed,**options)
                    # Exact current producer and release identity. The
                    # historical fixture release is not assumed current ABI.
                    a=facade.build_validated_source_backed_c11_release_from_stream(stream,expanded)
                    b=facade.build_validated_source_backed_c11_release_from_stream(stream,packed)
                    self.assertEqual(a.release_ref,b.release_ref)
                    self.assertEqual(a.replay_manifest.ref,b.replay_manifest.ref)
                    self.assertEqual(a.source_release_manifest_hash,b.source_release_manifest_hash)
                    self.assertEqual(a.semantic_release_hash,b.semantic_release_hash)
                    # Existing config guard permits reordered identical
                    # routing, but refuses missing/duplicated incidences.
                    reversed_routes=facade._PackedRoutingFacts(reversed(expanded.routing))
                    adapter.verify_config_projection_binding(
                        config,replace(packed,routing=reversed_routes),**options)
                    self.assertGreater(len(expanded.routing),1)
                    bad=facade._PackedRoutingFacts(
                        (*expanded.routing[:-1],expanded.routing[0]))
                    with self.assertRaisesRegex(adapter.SourceConfigurationBindingError,
                                                "routing rules differ"):
                        adapter.verify_config_projection_binding(
                            config,replace(packed,routing=bad),**options)
                    print("R157_RULE_GRAIN_BRIDGE",json.dumps({
                        "source_id":sid,"original_config_sha":row["original_config_file_sha256"],
                        "original_routes":len(original.document["routing"]),
                        "fixture_rows":stream.row_count,"incidences":len(packed.routing),
                        "expanded_projection_seconds":expanded_seconds,
                        "packed_projection_seconds":packed_seconds,
                        "exact_ordered_routes_projection_and_release":True,
                        "reordered_accepted_duplicate_refused":True,
                        "grade":"INDEXED_SOURCEFREE_FIXTURE_NOT_ORIGINAL_COUNTRY_EXECUTION"
                    }),flush=True)


if __name__=="__main__":
    unittest.main()
