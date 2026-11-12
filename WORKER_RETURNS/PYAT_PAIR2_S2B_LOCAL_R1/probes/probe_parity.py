import os, sys, tempfile, pathlib, json
from dataclasses import replace

sys.path.insert(0, os.environ.get("RAWLSING_ROOT", "."))

import rawlsing_next.tests.test_pre553_empirical_query as m
from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next._pre553_direct_i02_sourcefree import (
    direct_sections_from_candidate, build_sourcefree_direct_i02,
)
from rawlsing_next._pre553_external_i02_certificate import VerifiedExternalI02
from rawlsing_next._pre553_query_predicate import _build_release_index, _select_respondent_events
from rawlsing_next.pre553_empirical_objects import exact_ref

orig = m.ingest_c11_source_release
captured = {}
def spy(candidate, repo):
    captured['c'] = candidate
    return orig(candidate, repo)
m.ingest_c11_source_release = spy

def run(tag, rows, weights=None, reverse=False, topo=None):
    src = m._build_source(tag, rows, weights=weights, reverse_sections=reverse,
                          topology_by_question=topo)
    cand = captured['c']
    replay = cand.candidate_replay_manifest
    assert replay is not None
    historical = validate_c11_source_release(cand)
    direct_input = direct_sections_from_candidate(
        replace(cand, candidate_replay_manifest=None),
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    d = pathlib.Path(tempfile.mkdtemp(prefix="probe-"))
    path = d / "cert.sqlite"
    roots = build_sourcefree_direct_i02(direct_input, cand.empirical_universes[0].ref, path, chunk_size=3)
    with VerifiedExternalI02(path, roots=roots) as cert:
        header = dict(cert._rows("SELECT name,value FROM main.header"))
        assert header["candidate_projection_hash"] == historical.replay_manifest.semantic_projection_hash, (tag, "projection")
        assert header["reconstructed_v1_replay_ref"] == historical.replay_manifest.ref.key, (tag, "replay")
        assert header["reconstructed_v1_release_ref"] == historical.release_ref.key, (tag, "release")
        assert roots.replay == historical.replay_manifest.ref.key
        idx = _build_release_index(historical, cand.empirical_universes[0].ref)
        for resp in idx.respondents:
            assert {r.key for r in cert.event_refs(resp)} == {e.ref.key for e in idx.events_by_respondent[resp]}
            for q in cand.question_variable_bindings:
                for native_only in (True, False):
                    for include_component in (False, True):
                        exp = [e.ref.key for e in _select_respondent_events(
                            idx, resp, q.native_question_ref,
                            native_only=native_only, include_component=include_component)]
                        got = [r.key for r in cert.selector_refs(
                            resp, q.native_question_ref,
                            native_only=native_only, include_component=include_component)]
                        assert got == exp, (tag, resp, q.native_question_ref.key, native_only, include_component, got, exp)
    print("OK", tag, roots.logical[:12], "events", len(cand.respondent_events), "weights", len(cand.weight_measure_facts_or_typed_absence) if not hasattr(cand.weight_measure_facts_or_typed_absence,'state') else 0)

rows = [
    {'id': 'R1', 'responses': {'Q1': 'A', 'Q2': 'B'}, 'coords': {'AGE': '45'}},
    {'id': 'R2', 'responses': {'Q1': 'C', 'Q2': 'D'}, 'coords': {'AGE': '33'}},
]
run("probe-plain", rows)
run("probe-weights", rows, weights={'R1': ('WEIGHT_VALID_AUTHORIZED','1.0'), 'R2': ('WEIGHT_VALID_AUTHORIZED','2.0')})
run("probe-rev", rows, weights={'R1': ('WEIGHT_VALID_AUTHORIZED','1.0'), 'R2': ('WEIGHT_VALID_AUTHORIZED','2.0')}, reverse=True)
run("probe-multi", [{'id': f'R{i}', 'responses': {'Q1': str(i)}, 'coords': {'AGE': str(20+i)}} for i in range(19)], reverse=True)
print("ALL_PROBE_PARITY_OK")
