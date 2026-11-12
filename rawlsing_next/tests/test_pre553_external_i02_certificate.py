"""Adversarial native I03 and external-root tests for S2-B sourcefree certificate.

G5 is intentionally NOT claimed: these are author-side tests. The already
validated v1 I02 input still materializes full closure_refs upstream; this
suite cannot demonstrate an independently source-direct 100k I02 build.
"""
from dataclasses import replace
from pathlib import Path
from time import monotonic
import os
import sqlite3
import tracemalloc

import pytest

from rawlsing_next._pre553_external_i02_certificate import (
    ExternalI02IntegrityError, ExternalI02Roots, VerifiedExternalI02,
    _digest_file, _logical_root, build_sourcefree_external_i02,
    install_sourcefree_external_i02_i03,
)
from rawlsing_next.tests.test_pre553_verified_semantic_range import (
    _build_source, _release, _multi_i03_source,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _query_authority, _branch_predicate, _query, _run, _cell_map,
)


def _prepare(tmp_path, source, chunk=11):
    release = _release(source)
    universe = source["universe"].ref
    path = tmp_path / "whole-i02.sqlite"
    roots = build_sourcefree_external_i02(release, universe, path, chunk_size=chunk)
    return path, roots


def _facts(source, tag):
    qa = _query_authority(tag)
    pred = _branch_predicate(source, qa, tag=tag)
    query = _query(source, qa, pred, ("Y",), tag=tag)
    return qa, pred, query, _run(source, qa, pred, query)


def test_s2b_real_i02_native_i03_complete_and_restore(tmp_path):
    source = _build_source("s2b-first-native", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-first-native")
    assert oracle.facts[0].typed_state == "SUPPORTED"
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as verified:
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref, verified,
        )
        changed_reader = _run(source, qa, pred, query)
        assert changed_reader == oracle
        assert _cell_map(changed_reader.facts[0])["1"]["raw_numerator_support"] == 2
        key = source["respondents"]["R2"].ref.key
        assert len(list(verified.event_refs(key))) == 1
        assert len(list(verified.selector_refs(key, source["qrefs"]["Y"]))) == 1
    # A future externally anchored version must change when a genuine
    # original I02 event changes, NOT just when an index self-hash changes.
    other = _build_source("s2b-first-native", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 1}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    other_path = tmp_path / "changed.sqlite"
    new_roots = build_sourcefree_external_i02(
        _release(other), other["universe"].ref, other_path, chunk_size=7,
    )
    assert new_roots.logical != roots.logical
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(other_path, roots=roots)
    qa2, pred2, query2, changed_oracle = _facts(other, "s2b-first-native")
    with VerifiedExternalI02(other_path, roots=new_roots) as valid:
        install_sourcefree_external_i02_i03(
            other["repo"], other["release_ref"], other["universe"].ref, valid,
        )
        assert _run(other, qa2, pred2, query2) == changed_oracle
        assert _cell_map(changed_oracle.facts[0])["1"]["raw_numerator_support"] == 3
    restored = _build_source("s2b-first-native", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    restore_path = tmp_path / "restored.sqlite"
    restored_roots = build_sourcefree_external_i02(
        _release(restored), restored["universe"].ref, restore_path, chunk_size=2,
    )
    assert restored_roots.logical == roots.logical
    with VerifiedExternalI02(restore_path, roots=restored_roots):
        pass


def test_s2b_forged_certificate_cannot_install_false_zero_into_real_i03(tmp_path):
    """Harden the *existing* S2-B G3 counterfeit-index refusal at its consumer.

    An attacker can copy genuine roots and the genuine respondent census,
    while replacing only selector_refs. An arbitrary Protocol must never be
    promoted into the ordinary native I03 index attestation.
    """
    from types import SimpleNamespace

    source = _build_source("s2b-b-forged-install", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-b-forged-install")
    assert _cell_map(oracle.facts[0])["1"]["raw_numerator_support"] == 2
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as real:
        forged = SimpleNamespace(
            roots=real.roots,
            respondent_refs=real.respondent_refs,
            selector_refs=lambda *args, **kwargs: iter(()),
        )
        with pytest.raises(ExternalI02IntegrityError, match="exact cold-verified"):
            install_sourcefree_external_i02_i03(
                source["repo"], source["release_ref"], source["universe"].ref,
                forged,
            )
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref,
            real,
        )
        assert _run(source, qa, pred, query) == oracle


def test_s2b_verified_subclass_cannot_substitute_postings(tmp_path):
    """A subclass can override the validated object's selector reader."""
    source = _build_source("s2b-b-subclass", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    path, roots = _prepare(tmp_path, source)

    class CounterfeitChild(VerifiedExternalI02):
        def selector_refs(self, *args, **kwargs):
            return iter(())

    with CounterfeitChild(path, roots=roots) as counterfeit:
        with pytest.raises(ExternalI02IntegrityError, match="exact cold-verified"):
            install_sourcefree_external_i02_i03(
                source["repo"], source["release_ref"], source["universe"].ref,
                counterfeit,
            )


def test_s2b_verified_connection_cannot_be_swapped_after_cold_root_check(tmp_path):
    """A genuine verified class must not become a counterfeit by db reassignment."""
    import shutil

    source = _build_source("s2b-b-connection-swap", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-b-connection-swap")
    assert _cell_map(oracle.facts[0])["1"]["raw_numerator_support"] == 2
    path, roots = _prepare(tmp_path, source)
    poisoned_path = tmp_path / "unanchored-copy.sqlite"
    shutil.copy2(path, poisoned_path)
    with sqlite3.connect(poisoned_path) as untrusted:
        untrusted.execute("DELETE FROM selectors WHERE kind='native'")
    with VerifiedExternalI02(path, roots=roots) as real:
        replaced_connection = sqlite3.connect(poisoned_path)
        try:
            try:
                real.db = replaced_connection
            except ExternalI02IntegrityError as exc:
                assert "immutable" in str(exc)
            else:
                # On Agent A's first implementation, the same trusted roots
                # and genuine class now serve the unverified empty postings.
                install_sourcefree_external_i02_i03(
                    source["repo"], source["release_ref"],
                    source["universe"].ref, real,
                )
                malicious_result = _run(source, qa, pred, query)
                assert malicious_result != oracle
                pytest.fail("post-verification DB swap corrupted real native I03 facts")
        finally:
            replaced_connection.close()
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref, real,
        )
        assert _run(source, qa, pred, query) == oracle


def test_s2b_closed_verified_reader_refuses_typed_native_selection(tmp_path):
    """An attested installed I03 index must not use a closed SQLite witness."""
    from rawlsing_next._pre553_query_predicate import _select_respondent_events

    source = _build_source("s2b-b-closed", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-b-closed")
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as verified:
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref, verified,
        )
        assert _run(source, qa, pred, query) == oracle
        index = source["repo"]._i03_release_indices[
            (source["release_ref"], source["universe"].ref)
        ]
        respondent = next(iter(index.respondents))
        target = source["qrefs"]["Y"]
    with pytest.raises(ExternalI02IntegrityError, match="closed"):
        list(_select_respondent_events(index, respondent, target))


def test_s2b_same_respondent_duplicate_occurrence_and_states(tmp_path):
    source = _multi_i03_source("s2b-duplicate")
    path, roots = _prepare(tmp_path, source)
    respondent = source["respondents"]["R1"].ref.key
    qref = source["qrefs"]["Y"]
    with VerifiedExternalI02(path, roots=roots) as cert:
        original = list(cert.selector_refs(respondent, qref))
        assert len(original) == 2
        assert len(set(ref.key for ref in original)) == 2
        assert len(list(cert.selector_refs(respondent, qref, native_only=True))) == 2
        assert list(cert.selector_refs(respondent, qref, states=frozenset())) == []
        assert len(list(cert.selector_refs(respondent, qref,
                          states=frozenset({"SUBSTANTIVE_RESPONSE"})))) == 2
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref, cert,
        )


def test_s2b_attacker_rehashes_omitted_selector_but_cold_verifier_refuses(tmp_path):
    source = _build_source("s2b-poison", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    path, held = _prepare(tmp_path, source)
    db = sqlite3.connect(path)
    try:
        assert db.execute("SELECT COUNT(*) FROM selectors").fetchone()[0] > 0
        db.execute("""DELETE FROM selectors WHERE rowid = (
          SELECT rowid FROM selectors ORDER BY event_ref LIMIT 1
        )""")
        db.commit()
        forged_local_logical = _logical_root(db)
    finally:
        db.close()
    forged_local = replace(held, logical=forged_local_logical, physical=_digest_file(path))
    # Even an adversary who knows the local recomputation algorithm cannot
    # make the originally held roots change. Whole selector completeness also
    # independently defeats an omitted entry under locally forged new roots.
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(path, roots=held)
    with pytest.raises(ExternalI02IntegrityError, match="omits"):
        VerifiedExternalI02(path, roots=forged_local)


def test_s2b_corpus_event_removal_alias_and_wrong_binding_fail(tmp_path):
    source = _build_source("s2b-event", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    path, roots = _prepare(tmp_path, source)
    with sqlite3.connect(path) as db:
        db.execute("""DELETE FROM objects WHERE ref = (
          SELECT ref FROM objects WHERE family='RespondentEvent' LIMIT 1
        )""")
    forged = replace(roots, physical=_digest_file(path))
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(path, roots=forged)

    other = tmp_path / "wrong-release.sqlite"
    wrong_source = _build_source("s2b-different", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    wrong = build_sourcefree_external_i02(
        _release(wrong_source), wrong_source["universe"].ref, other,
    )
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(other, roots=roots)
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(other, roots=replace(
            wrong, source=roots.source,
        ))


def test_s2b_deterministic_chunk_sizes_cold_reopen_orphan(tmp_path):
    source = _build_source("s2b-deterministic", [
        {"id": f"R{i}", "responses": {"Y": i % 2}} for i in range(72)
    ])
    a = tmp_path / "a.sqlite"
    b = tmp_path / "b.sqlite"
    release, universe = _release(source), source["universe"].ref
    first = build_sourcefree_external_i02(release, universe, a, chunk_size=1)
    second = build_sourcefree_external_i02(release, universe, b, chunk_size=19)
    assert first.logical == second.logical
    # Separate full cold independent verification, no in-memory witness passed.
    with VerifiedExternalI02(a, roots=first) as reader:
        assert len(list(reader.respondent_refs())) == 72
    with VerifiedExternalI02(b, roots=second) as reader:
        assert len(list(reader.respondent_refs())) == 72
    with pytest.raises(ExternalI02IntegrityError):
        build_sourcefree_external_i02(release, universe, a)
    fake_stage = tmp_path / ".s2b-stage-orphan.sqlite"
    fake_stage.write_bytes(a.read_bytes())
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(fake_stage, roots=first)


def test_s2b_material_sourcefree_resource_probe(tmp_path):
    """Narrow real I02 fixture; not 100k source-direct or 6GiB proof."""
    n = 2048
    source = _build_source("s2b-resource", [
        {"id": f"R{i:05d}", "responses": {"Y": i % 2}} for i in range(n)
    ])
    path = tmp_path / "material.sqlite"
    before = monotonic()
    tracemalloc.start()
    try:
        roots = build_sourcefree_external_i02(
            _release(source), source["universe"].ref, path, chunk_size=7,
        )
        elapsed_build = monotonic() - before
        _current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    before = monotonic()
    with VerifiedExternalI02(path, roots=roots) as verifier:
        assert len(list(verifier.respondent_refs())) == n
    elapsed_cold = monotonic() - before
    assert path.stat().st_size > 0
    assert peak < 64 * 1024 * 1024  # builder's incremental extra heap only
    # Actual resource measurements emitted into CI log, not made-up figures.
    rss_kb = None
    if Path("/proc/self/status").exists():
        for line in Path("/proc/self/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                rss_kb = int(line.split()[1])
    print({
        "respondents": n, "logical": roots.logical, "physical": roots.physical,
        "retained_bytes": path.stat().st_size,
        "build_s": round(elapsed_build, 4),
        "cold_full_verify_s": round(elapsed_cold, 4),
        "tracemalloc_peak_bytes": peak,
        "process_rss_kb": rss_kb,
        "peak_scratch": "NOT_MEASURED", "process_tree_peak": "NOT_MEASURED",
        "100k_pipeline": "NOT_RUN", "source_rights": "NOT_ISSUED",
    })


def test_s2b_h27_real_canonical_component_pairing_and_poisoned_index(tmp_path):
    from rawlsing_next.tests.test_pre553_verified_semantic_range import _s2a_relation_source
    from rawlsing_next._pre553_query_predicate import _select_respondent_events
    release, universe, repository, cref, sref = _s2a_relation_source(
        "s2b-h27-alias",
        bindings=(("V1", "C1", "A"), ("V1", "C2", "B")),
        event_canonical="C1", event_component="A",
    )
    path = tmp_path / "complete-alias.sqlite"
    roots = build_sourcefree_external_i02(release, universe, path, chunk_size=1)
    with VerifiedExternalI02(path, roots=roots) as verified:
        install_sourcefree_external_i02_i03(
            repository, release.release_ref, universe, verified,
        )
        index = repository._i03_release_indices[(release.release_ref, universe)]
        respondent = next(iter(index.respondents))
        assert len(list(_select_respondent_events(index, respondent, cref("C1")))) == 2
        assert len(list(_select_respondent_events(index, respondent, sref("A"),
                                                  include_component=True))) == 2
        assert list(_select_respondent_events(index, respondent, cref("C2"))) == []
        assert list(_select_respondent_events(index, respondent, sref("A"),
                                              native_only=True,
                                              include_component=True)) == []
        assert list(_select_respondent_events(index, respondent, cref("C1"),
                                              states=frozenset())) == []
        assert not hasattr(index.events_by_respondent[respondent], "all_events")

    # The attacker removes only the canonical selector and recomputes every
    # index-local digest/manifest it controls; the separately held root remains.
    with sqlite3.connect(path) as db:
        db.execute("DELETE FROM selectors WHERE kind='canonical'")
        local_new_root = _logical_root(db)
    forged = replace(roots, logical=local_new_root, physical=_digest_file(path))
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(path, roots=roots)
    with pytest.raises(ExternalI02IntegrityError, match="omits"):
        VerifiedExternalI02(path, roots=forged)


def test_s2b_all_concrete_m01_m18_object_families_omission_refused(tmp_path):
    from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
    from rawlsing_next.pre553_c11_repository import C11Repository
    from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate
    candidate = _candidate("s2b-all-closure")
    repository = C11Repository()
    result = ingest_c11_source_release(candidate, repository)
    assert result.accepted, result.errors
    release = repository.resolve_release_exact(result.release_ref)
    for family in (
        "RespondentEvent", "EmpiricalCoordinateFact", "RoutingEligibilityFact",
        "QuestionVariableBinding", "RespondentIdentity", "AuthoritySnapshot",
    ):
        path = tmp_path / (family + ".sqlite")
        roots = build_sourcefree_external_i02(
            release, candidate.empirical_universes[0].ref, path, chunk_size=2,
        )
        with sqlite3.connect(path) as db:
            assert db.execute(
                "SELECT COUNT(*) FROM objects WHERE family=?", (family,)
            ).fetchone()[0]
            db.execute(
                """DELETE FROM objects WHERE ref=(
                    SELECT ref FROM objects WHERE family=? ORDER BY ref LIMIT 1
                )""", (family,),
            )
            forged_root = _logical_root(db)
        forged = replace(roots, logical=forged_root, physical=_digest_file(path))
        with pytest.raises(ExternalI02IntegrityError):
            VerifiedExternalI02(path, roots=roots)
        # A separately trusted root cannot be replaced by a locally
        # self-consistent forged graph; v1 closure still catches missing refs.
        with pytest.raises(ExternalI02IntegrityError):
            VerifiedExternalI02(path, roots=forged)


def test_s2b_exact_weight_and_unknown_routing_preserved(tmp_path):
    source = _build_source(
        "s2b-weight-and-unknown",
        [{"id": "R1", "responses": {"Y": 1}},
         {"id": "R2", "responses": {}}],
        weights={"R1": ("WEIGHT_VALID_AUTHORIZED", "2"),
                 "R2": ("WEIGHT_MISSING", None)},
        risk_sets={"R": {"Y": {"R1"}}},
        nonmember_routing_state="ROUTING_UNKNOWN",
    )
    qa, pred, query, original = _facts(source, "s2b-weight-and-unknown")
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as verified:
        assert verified.db.execute(
            "SELECT COUNT(*) FROM objects WHERE family='WeightMeasureFact'"
        ).fetchone()[0] == 2
        assert verified.db.execute(
            "SELECT COUNT(*) FROM objects WHERE family='RoutingEligibilityFact'"
        ).fetchone()[0] > 0
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref, verified,
        )
        assert _run(source, qa, pred, query) == original
    with sqlite3.connect(path) as db:
        db.execute("""DELETE FROM objects WHERE ref=(
            SELECT ref FROM objects WHERE family='WeightMeasureFact' LIMIT 1
        )""")
        forged = replace(roots, logical=_logical_root(db))
    forged = replace(forged, physical=_digest_file(path))
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(path, roots=forged)


def test_s2b_crash_before_commit_leaves_only_refused_orphan(tmp_path):
    """Real subprocess SIG-equivalent hard death before final publication."""
    import subprocess
    import sys
    script = """
from pathlib import Path
import os
import rawlsing_next._pre553_external_i02_certificate as stage
from rawlsing_next.tests.test_pre553_empirical_query import _build_source
from rawlsing_next.tests.test_pre553_verified_semantic_range import _release
source = _build_source('s2b-crash-fixture', [
    {'id':'R1','responses':{'Y':1}}, {'id':'R2','responses':{'Y':0}}])
original = stage._insert_object
counter = [0]
def interrupt(db, obj, *, family):
    original(db, obj, family=family)
    counter[0] += 1
    if counter[0] == 2:
        os._exit(77)
stage._insert_object = interrupt
stage.build_sourcefree_external_i02(
    _release(source), source['universe'].ref, Path(%r))
""" % str(tmp_path / "not-committed.sqlite")
    result = subprocess.run([sys.executable, "-c", script], capture_output=True,
                            text=True, check=False)
    assert result.returncode == 77, (result.returncode, result.stderr)
    assert not (tmp_path / "not-committed.sqlite").exists()
    orphans = list(tmp_path.glob(".s2b-stage-*.tmp"))
    assert orphans, "hard crash must not publish nor invisibly lose stage evidence"
    forged = ExternalI02Roots("0" * 64, "0" * 64, "none", "none",
                             "none", "none")
    for orphan in orphans:
        with pytest.raises(ExternalI02IntegrityError):
            VerifiedExternalI02(orphan, roots=forged)


def test_s2b_a_counterattack_sqlite_temp_selector_shadow_changes_real_i03(tmp_path):
    """G3: an already-verified connection is not a writable selector authority.

    SQLite's PRAGMA query_only is itself mutable. An untrusted consumer holding
    the public db handle can turn it off and create a TEMP table that takes
    precedence over the authenticated main.selectors in ordinary unqualified
    SELECT statements. No root, file, class or Python attribute is reassigned.
    """
    source = _build_source("s2b-a-temp-shadow", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-a-temp-shadow")
    assert oracle.facts[0].typed_state == "SUPPORTED"
    assert _cell_map(oracle.facts[0])["1"]["raw_numerator_support"] == 2
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as verified:
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref, verified,
        )
        assert _run(source, qa, pred, query) == oracle
        try:
            verified.db.execute("PRAGMA query_only=OFF")
            verified.db.execute("""
                CREATE TEMP TABLE selectors(
                    respondent TEXT, kind TEXT, target TEXT, event_ref TEXT
                )
            """)
        except ExternalI02IntegrityError:
            pass  # fixed certificate does not expose mutable SQL commands
        else:
            # If both commands succeed, main.selector bytes/root are untouched
            # but native SELECT FROM selectors silently resolves temp.selectors.
            poisoned_result = _run(source, qa, pred, query)
            assert poisoned_result == oracle, (
                "G3 RED: post-verification TEMP selector shadow silently "
                "changed real native I03 result under unchanged trusted roots"
            )
        assert _run(source, qa, pred, query) == oracle
    # The original on-disk certificate has not changed.
    with VerifiedExternalI02(path, roots=roots) as fresh:
        assert list(fresh.respondent_refs())


def test_s2b_a_counterattack_temp_objects_shadow_cannot_invent_empty(tmp_path):
    """G3: independently authenticated main.objects must not resolve TEMP."""
    source = _build_source("s2b-a-object-shadow", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 1}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-a-object-shadow")
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as real:
        with pytest.raises(ExternalI02IntegrityError, match="only permits SELECT"):
            real.db.execute("PRAGMA query_only=OFF")
        with pytest.raises(ExternalI02IntegrityError, match="only permits SELECT"):
            real.db.execute(
                "CREATE TEMP TABLE objects AS SELECT * FROM main.objects WHERE 0"
            )
        # SELECT is allowed for existing read-only instrumentation, but no
        # sqlite3.Cursor.connection or session-mutating public methods leak.
        assert not hasattr(real.db.execute("SELECT 1"), "connection")
        assert not hasattr(real.db, "create_collation")
        assert len(list(real.respondent_refs())) == 2
        respondent = source["respondents"]["R1"].ref.key
        assert len(list(real.event_refs(respondent))) == 1
        assert len(list(real.selector_refs(respondent, source["qrefs"]["Y"]))) == 1
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref, real,
        )
        assert _run(source, qa, pred, query) == oracle
    with VerifiedExternalI02(path, roots=roots) as fresh:
        assert len(list(fresh.respondent_refs())) == 2


def test_s2b_a_counterattack_midstream_close_typed_refusal(tmp_path):
    """G3/G4: close between certified occurrences must not leak untyped SQL."""
    source = _multi_i03_source("s2b-a-close-between-occurrences")
    path, roots = _prepare(tmp_path, source)
    respondent = source["respondents"]["R1"].ref.key
    target = source["qrefs"]["Y"]
    cert = VerifiedExternalI02(path, roots=roots)
    try:
        iterator = cert.selector_refs(respondent, target, native_only=True)
        first = next(iterator)
        assert first.kind == source["repo"].resolve_object_exact(first).ref.kind
        cert.close()
        with pytest.raises(ExternalI02IntegrityError, match="closed|invalidated"):
            next(iterator)
        with pytest.raises(ExternalI02IntegrityError, match="closed|invalidated"):
            list(cert.event_refs(respondent))
    finally:
        cert.close()


def test_s2b_a_counterattack_publication_cannot_clobber_rival(tmp_path, monkeypatch):
    """G4: target acquired between precheck and publish must never be replaced.

    Two noncolliding writer leases must not accidentally inherit an os.replace
    overwrite primitive; the final CAS name is publish-once, not last-writer.
    """
    import rawlsing_next._pre553_external_i02_certificate as impl
    source = _build_source("s2b-a-race", [{"id": "R1", "responses": {"Y": 1}}])
    target = tmp_path / "race.sqlite"
    rival = b"other-writer-held-destination\n"
    orig_replace = impl.os.replace
    orig_link = impl.os.link
    def competing_replace(stage, destination, *args, **kwargs):
        target.write_bytes(rival)
        return orig_replace(stage, destination, *args, **kwargs)
    def competing_link(stage, destination, *args, **kwargs):
        target.write_bytes(rival)
        return orig_link(stage, destination, *args, **kwargs)
    monkeypatch.setattr(impl.os, "replace", competing_replace)
    monkeypatch.setattr(impl.os, "link", competing_link)
    with pytest.raises(ExternalI02IntegrityError, match="collision|claimed|destination"):
        build_sourcefree_external_i02(
            _release(source), source["universe"].ref, target, chunk_size=1,
        )
    assert target.read_bytes() == rival
    assert not any(tmp_path.glob(".s2b-stage-*.tmp"))


def test_s2b_a_counterattack_verified_db_cannot_mutate_sql_collation(tmp_path):
    """G3: even main-qualified SQL can be falsified by mutable BINARY collation.

    A genuine sqlite3.Connection admits create_collation('BINARY', fn), so
    respondent/target WHERE equality can match unrelated real I02 rows with
    no file/manifest/root change. This attack does NOT use Python setattr or
    arbitrary private-object mutation; it uses the public exposed db API.
    """
    source = _build_source("s2b-a-collation", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-a-collation")
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as verified:
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref, verified,
        )
        assert _run(source, qa, pred, query) == oracle
        try:
            verified.db.create_collation("BINARY", lambda a, b: 0)
        except (ExternalI02IntegrityError, AttributeError):
            pass  # no public ability to redefine authenticated SQL semantics
        else:
            # Under Agent B's raw verified.db sqlite connection, every
            # equality is now counterfeit. A derived I03 fact must not change.
            assert _run(source, qa, pred, query) == oracle, (
                "G3 RED: BINARY collation replaced after external root "
                "verification, changing real native I03 semantics"
            )
        assert _run(source, qa, pred, query) == oracle
    with VerifiedExternalI02(path, roots=roots) as fresh:
        assert len(list(fresh.respondent_refs())) == 3
