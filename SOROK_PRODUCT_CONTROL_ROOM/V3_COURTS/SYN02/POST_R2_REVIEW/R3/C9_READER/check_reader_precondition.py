"""Reproduce the C9 candidate raw reader's required verification precondition."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

HASHES = {
    "c9_actor_r3.py": "ee4765e28d80531e6b5450296ed209ef4e3303b827910bbf20b73dfaba52725e",
    "schema_actor_r3.sql": "0ae69ef5b76177950c0b9c40e7bb20db11cf41d4697a5e4a1d6b08b459c82b90",
    "schema_mirror_r3.sql": "5f3f2895af2a5443dd87ade6714675677b96be23be15544714fdc16e12f58821",
}


def check(root: Path) -> dict:
    for filename, expected in HASHES.items():
        if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
            raise ValueError("SOURCE_CHANGED_BEFORE_IMPORT:" + filename)
    spec = importlib.util.spec_from_file_location("c9_reader_precondition_source", root / "c9_actor_r3.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="sorok-reader-precondition-") as temporary:
        actor = module.ActorAuthority(Path(temporary) / "own-fixture.sqlite", actor_id="TEST_ONLY_A")
        try:
            assert actor.verify()["ok"]
            actor.conn.execute("UPDATE actor_head SET head_semantic_hash=? WHERE actor_id=? AND branch_id=?",
                               ("tampered-semantic", "TEST_ONLY_A", "b0"))
            actor.conn.commit()
            raw = actor.read_semantic()
            checked = actor.verify()
            assert raw["semantic_hash"] == "tampered-semantic"
            assert not checked["ok"] and "head_semantic_mismatch" in checked["errors"]
            return {"source_candidate": "1e99681f58086f2784834df1186cfba71a2c50b9",
                    "scope": "DISPOSABLE_SOURCEFREE_FIXTURE_ONLY",
                    "observed_raw_reader_returns_unverified_head": True,
                    "separate_verifier_refuses": "head_semantic_mismatch",
                    "consumer_obligation": "Validate head/version/receipt bindings in a consistent read snapshot before exposing actor data; raw read_semantic alone is not a verified consumer.",
                    "source_modified": False, "native_authority": "NO_GRANT"}
        finally:
            actor.conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.source), indent=2))
