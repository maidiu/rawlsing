"""Independent G5-R1 recheck: direct certificate -> real native I03 2->3->2."""
from dataclasses import replace

from rawlsing_next._pre553_direct_i02_sourcefree import (
    build_sourcefree_direct_i02, direct_sections_from_candidate,
)
from rawlsing_next._pre553_external_i02_certificate import (
    VerifiedExternalI02, install_direct_sourcefree_i02_i03,
)
from rawlsing_next.tests.test_pre553_verified_semantic_range import (
    _build_source,
)
from rawlsing_next.tests.test_pre553_external_i02_certificate import _facts
from rawlsing_next.tests.test_pre553_empirical_query import _run, _cell_map
import rawlsing_next.tests.test_pre553_empirical_query as empirical_query


def main():
    captured = []
    original = empirical_query.ingest_c11_source_release

    def spy(candidate, repo):
        captured.append(candidate)
        return original(candidate, repo)

    empirical_query.ingest_c11_source_release = spy
    try:
        tag = "g5r2-native-232"
        rows_before = [
            {"id": "R1", "responses": {"Y": 1}},
            {"id": "R2", "responses": {"Y": 0}},
            {"id": "R3", "responses": {"Y": 1}},
        ]
        rows_changed = [
            {"id": "R1", "responses": {"Y": 1}},
            {"id": "R2", "responses": {"Y": 1}},
            {"id": "R3", "responses": {"Y": 1}},
        ]

        import tempfile
        from pathlib import Path
        root = Path(tempfile.mkdtemp(prefix="g5r2-native-"))

        def direct_run(rows, name):
            source = _build_source(tag, rows)
            candidate = captured[-1]
            qa, pred, query, oracle = _facts(source, tag)
            replay = candidate.candidate_replay_manifest
            direct = direct_sections_from_candidate(
                replace(candidate, candidate_replay_manifest=None),
                replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
                replay_protocol_version=replay.replay_protocol_version,
                deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
            )
            path = root / (name + ".sqlite")
            roots = build_sourcefree_direct_i02(
                direct, source["universe"].ref, path, chunk_size=3,
            )
            with VerifiedExternalI02(path, roots=roots) as cert:
                install_direct_sourcefree_i02_i03(
                    source["repo"], source["release_ref"],
                    source["universe"].ref, cert,
                )
                result = _run(source, qa, pred, query)
                assert result == oracle, (name, "oracle mismatch")
                numerator = _cell_map(result.facts[0])["1"]["raw_numerator_support"]
                print(name, "raw_numerator_support", numerator)
                return numerator, roots.logical

        before, before_root = direct_run(rows_before, "before")
        changed, changed_root = direct_run(rows_changed, "changed")
        restored, restored_root = direct_run(rows_before, "restored")
        assert (before, changed, restored) == (2, 3, 2)
        assert before_root == restored_root
        assert changed_root != before_root
        print("NATIVE_2_3_2_RESTORE_PASS")
    finally:
        empirical_query.ingest_c11_source_release = original


if __name__ == "__main__":
    main()
