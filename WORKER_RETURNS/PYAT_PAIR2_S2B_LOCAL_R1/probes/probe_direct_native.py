import os, sys, tempfile, pathlib
from dataclasses import replace
from types import MappingProxyType

sys.path.insert(0, os.environ.get("RAWLSING_ROOT", "."))

from rawlsing_next.tests.test_pre553_direct_i02_sourcefree import _direct
from rawlsing_next._pre553_direct_i02_sourcefree import (
    direct_sections_from_candidate, build_sourcefree_direct_i02,
)
from rawlsing_next._pre553_external_i02_certificate import (
    VerifiedExternalI02, _DiskSelectedRespondent,
)
from rawlsing_next._pre553_query_predicate import _build_release_index, _select_respondent_events
from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release, validate_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository

candidate, _, source = _direct("probe-direct-native")
historical = validate_c11_source_release(candidate)
replay = candidate.candidate_replay_manifest
direct = direct_sections_from_candidate(
    replace(candidate, candidate_replay_manifest=None),
    replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
    replay_protocol_version=replay.replay_protocol_version,
    deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref)
d = pathlib.Path(tempfile.mkdtemp(prefix="probe-direct-native-"))
path = d / "cert.sqlite"
roots = build_sourcefree_direct_i02(direct, candidate.empirical_universes[0].ref, path, chunk_size=1)
repo = C11Repository()
admission = ingest_c11_source_release(candidate, repo)
assert admission.accepted
with VerifiedExternalI02(path, roots=roots) as cert:
    native = _build_release_index(historical, candidate.empirical_universes[0].ref)
    selector = MappingProxyType({
        key: _DiskSelectedRespondent(key, cert, repo) for key in native.respondents
    })
    index = replace(native, events_by_respondent=selector)
    for respondent in native.respondents:
        for q in candidate.question_variable_bindings:
            for native_only in (True, False):
                for include_component in (False, True):
                    for states in (None, frozenset({"SUBSTANTIVE_RESPONSE"}), frozenset()):
                        exp = [e.ref.key for e in _select_respondent_events(
                            native, respondent, q.native_question_ref,
                            native_only=native_only, include_component=include_component,
                            states=states)]
                        got = [e.ref.key for e in _select_respondent_events(
                            index, respondent, q.native_question_ref,
                            native_only=native_only, include_component=include_component,
                            states=states)]
                        assert got == exp, (respondent, q.native_question_ref.key,
                                            native_only, include_component, states, got, exp)
        assert [e.ref.key for e in index.events_by_respondent[respondent]] == [
            e.ref.key for e in native.events_by_respondent[respondent]]
print("DIRECT_NATIVE_SELECTOR_CONSUMER_OK", roots.logical[:12])
