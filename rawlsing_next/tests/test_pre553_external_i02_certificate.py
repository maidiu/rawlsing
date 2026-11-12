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


def test_s2b_a_r2_public_sqlite_connection_rollback_corrupts_native_i03(tmp_path):
    """RED on B: public db.execute('ROLLBACK') releases the verified snapshot.

    A second writer can now alter the real SQLite file; the already-attested
    I03 index reopens the changed posting keyspace under the *old* roots.
    This is not object.__setattr__, subclassing or a forged certificate type.
    """
    source = _build_source("s2b-a-r2-rollback", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-a-r2-rollback")
    assert _cell_map(oracle.facts[0])["1"]["raw_numerator_support"] == 2
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as verified:
        install_sourcefree_external_i02_i03(
            source["repo"], source["release_ref"], source["universe"].ref,
            verified,
        )
        assert _run(source, qa, pred, query) == oracle
        try:
            verified.db.execute("ROLLBACK")
        except ExternalI02IntegrityError:
            assert _run(source, qa, pred, query) == oracle
            return
        # The read transaction was actually destroyed; real on-disk data
        # changes are now observed by the exact previously verified instance.
        with sqlite3.connect(path) as attacker:
            removed = attacker.execute(
                "DELETE FROM selectors WHERE kind='native'"
            ).rowcount
            assert removed == 3
        poisoned_result = _run(source, qa, pred, query)
        assert poisoned_result != oracle, "repro requires real native fact corruption"
        pytest.fail(
            "post-validation public SQLite rollback silently changed native I03 facts"
        )


def test_s2b_a_r2_deleting_verifier_seal_allows_db_substitution(tmp_path):
    """RED on B: ordinary delattr(_sealed) disables __setattr__ guard."""
    import shutil
    source = _build_source("s2b-a-r2-delattr", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa, pred, query, oracle = _facts(source, "s2b-a-r2-delattr")
    assert _cell_map(oracle.facts[0])["1"]["raw_numerator_support"] == 2
    path, roots = _prepare(tmp_path, source)
    poison = tmp_path / "locally-rehashed-but-not-anchored.sqlite"
    shutil.copy2(path, poison)
    with sqlite3.connect(poison) as untrusted:
        removed = untrusted.execute(
            "DELETE FROM selectors WHERE kind='native'"
        ).rowcount
        assert removed == 3
    with VerifiedExternalI02(path, roots=roots) as verified:
        try:
            del verified._sealed
        except ExternalI02IntegrityError:
            install_sourcefree_external_i02_i03(
                source["repo"], source["release_ref"], source["universe"].ref,
                verified,
            )
            assert _run(source, qa, pred, query) == oracle
            return
        replacement = sqlite3.connect(poison)
        try:
            verified.db = replacement
            install_sourcefree_external_i02_i03(
                source["repo"], source["release_ref"], source["universe"].ref,
                verified,
            )
            poisoned_result = _run(source, qa, pred, query)
            assert poisoned_result != oracle
            pytest.fail(
                "ordinary delattr bypassed B's attribute seal and altered native I03"
            )
        finally:
            replacement.close()


def test_s2b_a_r2_atomic_publication_collision_preserves_other_writer(tmp_path, monkeypatch):
    """A checked-absent final path can be claimed while builder works.

    B inherited A's TOCTOU exists()->os.replace(): the competing final file
    was silently lost. This test inserts the rival exactly at publication and
    requires a typed refusal without clobbering that file.
    """
    source = _build_source("s2b-a-r2-publish-race", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    destination = tmp_path / "published.sqlite"
    import os
    real_link = os.link
    collision_called = []

    def race_link(source_path, target_path, *, follow_symlinks=True):
        collision_called.append((source_path, target_path))
        Path(target_path).write_bytes(b"unrelated-writer-exclusive-claim")
        return real_link(source_path, target_path,
                         follow_symlinks=follow_symlinks)

    monkeypatch.setattr(os, "link", race_link)
    with pytest.raises(ExternalI02IntegrityError, match="destination collision"):
        build_sourcefree_external_i02(
            _release(source), source["universe"].ref, destination,
            chunk_size=2,
        )
    assert len(collision_called) == 1
    assert destination.read_bytes() == b"unrelated-writer-exclusive-claim"
    assert not list(tmp_path.glob(".s2b-stage-*.tmp"))


def test_s2b_a_r2_only_readonly_select_rows_and_closed_iterators(tmp_path):
    source = _build_source("s2b-a-r2-facade", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    path, roots = _prepare(tmp_path, source)
    with VerifiedExternalI02(path, roots=roots) as verified:
        assert verified.db.execute("SELECT 1").fetchone() == (1,)
        for invalid in (
            "ROLLBACK", "COMMIT", "PRAGMA query_only=OFF",
            "CREATE TEMP TABLE selectors(kind TEXT)",
            "SELECT 1; ROLLBACK", "SELECT * FROM nonexistent",
        ):
            with pytest.raises(ExternalI02IntegrityError):
                verified.db.execute(invalid)
        cursor = verified.db.execute("SELECT ref FROM main.objects ORDER BY ref")
        assert not hasattr(cursor, "connection")
        assert not hasattr(verified.db, "create_collation")
        assert next(iter(cursor))[0]
        verified.close()
        with pytest.raises(ExternalI02IntegrityError, match="closed"):
            next(cursor)
        with pytest.raises(ExternalI02IntegrityError, match="closed"):
            verified.db.execute("SELECT 1")
