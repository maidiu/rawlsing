from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "rawlsing_next/runtime/ee_p2x"
BACKEND = ROOT / "rawlsing_next/ee_p2x_darwin_stage_backend.py"
MANIFEST = RUNTIME / "RUNTIME_PACKAGING_BINDING.json"
NODE4A = ROOT / "WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py"

EXPECTED_ASSET_BLOBS = {
    "01_LITS_CURRENT_RUNTIME_MATERIALIZER.py": "9406bacfd928393f6a159a46216aa1f7ec129f34",
    "02_WVS7_P2F2_RUNTIME_PACKAGE.json": "e04e84b76f8b4eb53905276dd025938bf2e5f6fe",
    "05_WVS7_PROJECTION_MATERIALIZER.py": "11b28416aac5a4899706150721f2f8ac8bb6ee43",
}
NODE4A_BLOB = "504944f9533b7385d201076e2e834b8a9446dee8"
OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
FROZEN_OWNER_SPECS = {
    "A": {"path": "rawlsing_next/pre553_r5_source_backed_adapter.py", "git_blob_sha": "d4915e7e6755ba1850756aebff72f982f73a332b"},
    "B": {"path": "rawlsing_next/pre553_source_backed_c11_facade.py", "git_blob_sha": "7c509c2098d0030f253344eb3f682471378812a8"},
    "C": {"path": "rawlsing_next/pre553_route_c_accelerators.py", "git_blob_sha": "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889"},
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()


def assigned_constants(path: Path) -> dict[str, object]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    out: dict[str, object] = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            for target in targets:
                if isinstance(target, ast.Name):
                    try:
                        out[target.id] = ast.literal_eval(value)
                    except Exception:
                        pass
    return out


class RuntimePackagingRebindTests(unittest.TestCase):
    def test_rebound_runtime_assets_are_byte_identical(self) -> None:
        for name, expected in EXPECTED_ASSET_BLOBS.items():
            path = RUNTIME / name
            self.assertTrue(path.is_file(), f"missing rebound runtime asset: {path}")
            self.assertEqual(git_blob_sha(path), expected, f"byte identity drift: {name}")

    def test_node4a_exact_accepted_carrier_is_fanned_in(self) -> None:
        self.assertTrue(NODE4A.is_file(), "accepted Node4A support carrier absent")
        self.assertEqual(git_blob_sha(NODE4A), NODE4A_BLOB)
        lits = RUNTIME / "01_LITS_CURRENT_RUNTIME_MATERIALIZER.py"
        const = assigned_constants(lits)
        self.assertEqual(
            const.get("NODE4A_SUPPORT"),
            "WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py",
        )
        self.assertEqual(const.get("NODE4A_BLOB"), NODE4A_BLOB)
        # Exact materializer bytes use Path(__file__).resolve().parents[3].
        self.assertEqual(lits.resolve().parents[3], ROOT.resolve())

    def test_backend_uses_only_stable_current_runtime_bindings(self) -> None:
        const = assigned_constants(BACKEND)
        self.assertEqual(
            const.get("R6S_LITS_SUPPORT"),
            "rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py",
        )
        self.assertEqual(
            const.get("R6S_RUNTIME_PACKAGE"),
            "rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json",
        )
        self.assertEqual(
            const.get("R6S_MATERIALIZER"),
            "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py",
        )
        source = BACKEND.read_text(encoding="utf-8")
        for forbidden in (
            "WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py",
            "WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json",
            "WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py",
        ):
            self.assertNotIn(forbidden, source)

    def test_governed_runtime_identities_and_dependency_hashes_are_unchanged(self) -> None:
        const = assigned_constants(BACKEND)
        self.assertEqual(const.get("OWNER_COMMIT"), OWNER_COMMIT)
        self.assertEqual(const.get("R6O_RUNTIME_CATALOG"), "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02")
        self.assertEqual(const.get("R6O_ACTIVE_BINDING"), "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308")
        self.assertEqual(const.get("R6O_RUNTIME_RELEASE"), "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f")
        self.assertEqual(const.get("WVS_LOCK2"), "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188")
        self.assertEqual(const.get("R6S_WVS_PROJECTION"), "838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d")
        package = json.loads((RUNTIME / "02_WVS7_P2F2_RUNTIME_PACKAGE.json").read_text(encoding="utf-8"))
        self.assertEqual(package.get("lock2"), const.get("WVS_LOCK2"))
        self.assertEqual(
            package.get("counts"),
            {"authorities": 6, "predicates": 11, "queries": 3, "discovery_authorities": 1, "candidates": 46},
        )

    def test_current_tree_lookalike_cannot_replace_frozen_candidate_owner(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        preserved = manifest["preserved_runtime_identities"]
        self.assertEqual(preserved["frozen_candidate_owner_commit"], OWNER_COMMIT)
        self.assertEqual(preserved["candidate_owner_binding_mode"], "IMMUTABLE_GIT_BY_EXACT_BLOB")
        self.assertEqual(preserved["frozen_candidate_owner_specs"], FROZEN_OWNER_SPECS)

        current_b = ROOT / FROZEN_OWNER_SPECS["B"]["path"]
        self.assertTrue(current_b.is_file(), "current-tree B facade unexpectedly absent")
        self.assertNotEqual(
            git_blob_sha(current_b),
            FROZEN_OWNER_SPECS["B"]["git_blob_sha"],
            "current-tree lookalike became indistinguishable from frozen B owner; immutable owner root must still govern deployment",
        )

    def test_packaging_manifest_declares_no_semantic_owner_move(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertFalse(manifest["semantic_owner_change"])
        self.assertFalse(manifest["measured_p2x_authorized"])
        self.assertIn("CURRENT_TREE_CANDIDATE_OWNER_SUBSTITUTION", manifest["forbidden"])
        self.assertIn("NODE4A_RECONSTRUCTION", manifest["forbidden"])


if __name__ == "__main__":
    unittest.main()
