"""Source-free hostile tests for FIABC split R2-E bytecode-prestate closure.

No survey source path is accepted or opened.  These tests exercise only the
successor cache-neutrality control and static protected/control code surfaces.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import py_compile
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
HELPER_PATH = ROOT / "HQ_HANDOFF" / "launchers" / "FIABC_PYTHON_CACHE_NEUTRALITY_SUCCESSOR.py"
spec = importlib.util.spec_from_file_location("fiabc_cache_neutrality", HELPER_PATH)
assert spec and spec.loader
CACHE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CACHE)

PROTECTED_ENVELOPE = ROOT / "rawlsing_next" / "ee_p2x_candidate_process_envelope.py"
PROTECTED_BACKEND = ROOT / "rawlsing_next" / "ee_p2x_darwin_stage_backend.py"
JOINED_LAUNCHER = ROOT / "HQ_HANDOFF" / "launchers" / "RUN_DISPOSITIVE_FIABC_SIX_CELL.sh"
SPLIT_LAUNCHER = ROOT / "HQ_HANDOFF" / "launchers" / "RUN_FIABC_SOURCE_LOCAL_SPLIT.sh"
OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"


class CacheNeutralityTests(unittest.TestCase):
    def test_prepare_requires_empty_prefix_and_binds_both_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            env = CACHE.prepare_environment(work)
            prefix = CACHE.cache_prefix(work)
            self.assertTrue(prefix.is_dir())
            self.assertEqual(tuple(prefix.rglob("*")), ())
            self.assertEqual(env["PYTHONDONTWRITEBYTECODE"], "1")
            self.assertEqual(env["PYTHONPYCACHEPREFIX"], str(prefix))
            self.assertEqual(env["RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR"], "1")
            rogue = prefix / "rogue.pyc"
            rogue.write_bytes(b"not-bytecode")
            with self.assertRaisesRegex(CACHE.CacheNeutralityError, "not empty"):
                CACHE.prepare_environment(work)

    def test_receipt_cannot_admit_split_without_joined_successor(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            CACHE.prepare_environment(work)
            old = {
                key: __import__("os").environ.get(key)
                for key in (
                    "PYTHONDONTWRITEBYTECODE",
                    "PYTHONPYCACHEPREFIX",
                    "RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR",
                )
            }
            try:
                __import__("os").environ.update(CACHE.prepare_environment(work))
                prior_write = sys.dont_write_bytecode
                prior_prefix = sys.pycache_prefix
                sys.dont_write_bytecode = True
                sys.pycache_prefix = str(CACHE.cache_prefix(work))
                doc = CACHE.build_receipt(
                    work_root=work,
                    scope="SPLIT_SOURCE_LOCAL",
                    protected_head=CACHE.EXPECTED_CURRENT_PROTECTED_HEAD,
                    joined_successor_identity=None,
                )
                with self.assertRaisesRegex(CACHE.CacheNeutralityError, "joined successor adoption"):
                    CACHE.verify_receipt(
                        doc,
                        expected_scope="SPLIT_SOURCE_LOCAL",
                        require_joined_successor=True,
                    )
            finally:
                sys.dont_write_bytecode = prior_write
                sys.pycache_prefix = prior_prefix
                for key, value in old.items():
                    if value is None:
                        __import__("os").environ.pop(key, None)
                    else:
                        __import__("os").environ[key] = value


    def test_redirected_empty_prefix_ignores_valid_source_tree_pyc_and_writes_nothing(self):
        """A valid ordinary .pyc must be invisible under the successor cache law."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "sample_cache_probe.py"
            cached_text = "VALUE = 'cachex'\n"
            source_text = "VALUE = 'source'\n"
            self.assertEqual(len(cached_text), len(source_text))
            source.write_text(cached_text, encoding="utf-8")
            stamp = source.stat().st_mtime_ns
            pyc = Path(
                py_compile.compile(
                    str(source),
                    doraise=True,
                    invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
                )
            )
            self.assertTrue(pyc.is_file())
            # Keep timestamp and size identical so the ordinary timestamp pyc remains valid.
            source.write_text(source_text, encoding="utf-8")
            os.utime(source, ns=(stamp, stamp))
            self.assertEqual(source.stat().st_size, len(source_text.encode("utf-8")))

            ordinary = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    (
                        "import importlib.util, json, pathlib, sys;"
                        "p=pathlib.Path(sys.argv[1]);"
                        "spec=importlib.util.spec_from_file_location('probe',p);"
                        "m=importlib.util.module_from_spec(spec);"
                        "spec.loader.exec_module(m);"
                        "print(json.dumps({'value':m.VALUE,'prefix':sys.pycache_prefix,"
                        "'dont_write':sys.dont_write_bytecode}))"
                    ),
                    str(source),
                ],
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(json.loads(ordinary.stdout)["value"], "cachex")

            prefix = root / "neutral-prefix"
            prefix.mkdir()
            env = dict(os.environ)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["PYTHONPYCACHEPREFIX"] = str(prefix)
            neutral = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    (
                        "import importlib.util, json, pathlib, sys;"
                        "p=pathlib.Path(sys.argv[1]);"
                        "spec=importlib.util.spec_from_file_location('probe',p);"
                        "m=importlib.util.module_from_spec(spec);"
                        "spec.loader.exec_module(m);"
                        "print(json.dumps({'value':m.VALUE,'prefix':sys.pycache_prefix,"
                        "'dont_write':sys.dont_write_bytecode}))"
                    ),
                    str(source),
                ],
                check=True,
                stdout=subprocess.PIPE,
                text=True,
                env=env,
            )
            doc = json.loads(neutral.stdout)
            self.assertEqual(doc["value"], "source")
            self.assertTrue(doc["dont_write"])
            self.assertEqual(str(Path(doc["prefix"]).resolve()), str(prefix.resolve()))
            self.assertEqual(tuple(p for p in prefix.rglob("*") if p.is_file()), ())

    def test_current_protected_envelope_propagates_parent_environment_to_main_child(self):
        source = PROTECTED_ENVELOPE.read_text(encoding="utf-8")
        self.assertIn("env = dict(os.environ)", source)
        self.assertIn("subprocess.Popen(", source)
        self.assertIn("env=env", source)
        self.assertNotIn('env.pop("PYTHONDONTWRITEBYTECODE"', source)
        self.assertNotIn('env.pop("PYTHONPYCACHEPREFIX"', source)

    def test_s15_fresh_replay_inherits_main_candidate_environment(self):
        source = PROTECTED_BACKEND.read_text(encoding="utf-8")
        marker = '[sys.executable,str(Path(__file__).resolve()),"--fresh-replay",str(plan_path)]'
        self.assertIn(marker, source)
        start = source.index(marker)
        call = source[start:source.index(")", start) + 1]
        self.assertNotIn("env=", call)

    def test_lits_r5_import_surface_is_raw_value_dependent(self):
        seam = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{OWNER_COMMIT}:rawlsing_next/pre553_r5_seam.py"],
            check=True, stdout=subprocess.PIPE, text=True,
        ).stdout
        self.assertIn("if permit_vector_hot_path and _all_finite_floats(batch):", seam)
        self.assertIn("import numpy as np", seam)
        self.assertIn("for batch in iter_normalized_batches(", seam)
        self.assertIn("yield cell_record_row(cell)", seam)

    def test_current_launchers_do_not_yet_adopt_cache_neutral_successor(self):
        joined = JOINED_LAUNCHER.read_text(encoding="utf-8")
        split = SPLIT_LAUNCHER.read_text(encoding="utf-8")
        for source in (joined, split):
            self.assertNotIn("RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR", source)
            self.assertNotIn("PYTHONPYCACHEPREFIX", source)
        self.assertIn("-m rawlsing_next.ee_p2x_darwin_court_driver", joined)

    def test_compileall_is_explicitly_not_an_admission_strategy(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            CACHE.prepare_environment(work)
            old = {
                key: __import__("os").environ.get(key)
                for key in (
                    "PYTHONDONTWRITEBYTECODE",
                    "PYTHONPYCACHEPREFIX",
                    "RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR",
                )
            }
            try:
                __import__("os").environ.update(CACHE.prepare_environment(work))
                prior_write = sys.dont_write_bytecode
                prior_prefix = sys.pycache_prefix
                sys.dont_write_bytecode = True
                sys.pycache_prefix = str(CACHE.cache_prefix(work))
                doc = CACHE.build_receipt(
                    work_root=work,
                    scope="JOINED_SIX_CELL",
                    protected_head="successor-head",
                    joined_successor_identity="successor-control",
                )
                self.assertFalse(
                    doc["law"]["compileall_or_precompiled_cache_substitution_authorized"]
                )
            finally:
                sys.dont_write_bytecode = prior_write
                sys.pycache_prefix = prior_prefix
                for key, value in old.items():
                    if value is None:
                        __import__("os").environ.pop(key, None)
                    else:
                        __import__("os").environ[key] = value


if __name__ == "__main__":
    unittest.main(verbosity=2)
