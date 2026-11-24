"""Actual saved-source zero/multiple I05 and checkpointed resume.

Fixture records are separately issued TEST_ONLY decisions, never mutations
of a claimed original-source or R03 complete compiler receipt.
"""
from dataclasses import replace
from collections import Counter
from pathlib import Path
import shutil
import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, DiscoveryAuthority, AuthoritySnapshot, canonicalize, semantic_hash,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_issued_workload import operation_jobs, WorkloadAdmissionError
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_governed_query_issuer_v2 import _issue_compiled_governed_queries_v2
from rawlsing_next.pre553_prepared_saved_i03 import PreparedI03Session
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_durable_empirical_closure import open_empirical_closure, DurableEmpiricalClosureError
from rawlsing_next.pre553_saved_durable_delivery import (
    execute_publish_saved, open_saved_product, SavedResumePin, SavedDeliveryError,
)
from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e
from rawlsing_next.tests.test_pyat997_r03_governed_query_issuer_v2 import _v2_admission


def _ref(kind, material):
    digest = semantic_hash(material)
    return ExactRef(kind, "urn:test:general-archive:" + digest, digest)


def _issued_shape(issued, mode):
    """Separate synthetic current issuer; preserve original compiler untouched."""
    original = issued.workload
    catalog = original.catalog
    if mode == "query-only":
        discoveries = ()
    else:
        old = catalog.resolve_discovery_authority_exact(original.discoveries[0])
        old_auth = catalog.authority_registry.resolve_exact(old.authority_snapshot_refs[0]).snapshot
        grammar = canonicalize(old.candidate_universe_definition)
        rules = grammar["rules"]
        assert len(rules) >= 2
        if mode == "multi-learned":
            # Two actual disjoint native frontiers with eligible conditional
            # rules on each, rather than two copies of the same result.
            conditional = [rule for rule in rules
                           if rule["family"] == "BRANCH_CONDITIONED_DISTRIBUTION"]
            others = [rule for rule in rules
                      if rule["family"] != "BRANCH_CONDITIONED_DISTRIBUTION"]
            assert len(conditional) >= 2
            partitions = (conditional[::2] + others[::2],
                          conditional[1::2] + others[1::2])
        else:
            partitions = (rules[:1], rules[1:])
        snapshots = []
        objects = []
        for i, part in enumerate(partitions):
            fields = canonicalize(old_auth.semantic_fields)
            fields["authority_id"] += "-B-TEST-PART-" + str(i)
            fields["authority_content_hash"] = semantic_hash({"test_only": True, "part": part})
            auth = AuthoritySnapshot(typed_state=old_auth.typed_state,
                authority_snapshot_refs=old_auth.authority_snapshot_refs,
                dependency_refs=old_auth.dependency_refs,
                producer_replay_locator_or_reference_root=old_auth.producer_replay_locator_or_reference_root,
                **fields)
            g = {**grammar, "rules": part}
            fields = canonicalize(old.semantic_fields)
            fields["candidate_universe_definition"] = g
            fields["candidate_grammar_ref"] = _ref("PRE553_I05_CANDIDATE_GRAMMAR", g)
            d = DiscoveryAuthority(typed_state=old.typed_state,
                authority_snapshot_refs=(auth.authority_ref,), dependency_refs=old.dependency_refs,
                producer_replay_locator_or_reference_root=old.producer_replay_locator_or_reference_root,
                **fields)
            snapshots.append(auth)
            objects.append(d)
        assert objects[0].candidate_grammar_ref != objects[1].candidate_grammar_ref
        catalog = RuntimeObjectCatalog(
            authorities=(*catalog.authorities, *snapshots), predicates=catalog.predicates,
            queries=catalog.queries, discovery_authorities=tuple(objects))
        discoveries = tuple(d.ref for d in objects)
    jobs = operation_jobs(original.requests, discoveries)
    expected = semantic_hash({"test_only_separately_issued": mode, "jobs": jobs})
    workload = replace(original, decision_ref=_ref("TEST_ONLY_DECISION", expected),
        expected_frontier_root=expected, catalog=catalog, discoveries=discoveries)
    record = replace(issued.record, decision_ref=workload.decision_ref,
        expected_frontier_root=expected, expected_jobs=jobs,
        envelope_sha256=semantic_hash(workload.envelope()))
    return workload, TestOnlyDecisionResolver(record)


@pytest.mark.parametrize("mode", ["query-only", "multi-discovery"])
def test_physical_source_general_archive_resume(tmp_path, monkeypatch, mode):
    handoff, estate, initial, v1, _, _ = s1e._full(tmp_path/"source")
    issued = _issue_compiled_governed_queries_v2(v1).issued
    workload, resolver = _issued_shape(issued, mode)
    assert handoff.stats.source_reads == 1
    # No original file exists during partial or resumed native execution.
    for p in (tmp_path/"source").rglob("*.sav"):
        p.unlink()
    common = dict(workload=workload, resolver=resolver, host=s1e._NATIVE_HOST,
                  purpose=s1e._NATIVE_PURPOSE)
    def factory():
        return _v2_admission(initial, workload.catalog)
    counts = Counter()
    real_q, real_d = PreparedI03Session.execute_i03, PreparedI03Session.execute_i05
    def query(self, *, query_ref, predicate_ref):
        counts[("QUERY", query_ref.key)] += 1
        return real_q(self, query_ref=query_ref, predicate_ref=predicate_ref)
    def discovery(self, *, discovery_authority_ref):
        counts[("DISCOVERY", discovery_authority_ref.key)] += 1
        return real_d(self, discovery_authority_ref=discovery_authority_ref)
    monkeypatch.setattr(PreparedI03Session, "execute_i03", query)
    monkeypatch.setattr(PreparedI03Session, "execute_i05", discovery)
    root = tmp_path/"products"
    partial = execute_publish_saved(**common, saved_admission_factory=factory,
                                    root_dir=root, max_units=3)
    assert not partial.complete and partial.batch_census["completed_count"] == 3
    assert sum(counts.values()) == 3
    pinned = dict(expected_release_ref=initial.release_ref,
                  expected_saved_manifest_sha256=initial.manifest_sha256)
    first_pin = SavedResumePin(partial.receipt.root_path, partial.receipt.root_identity, **pinned)
    with pytest.raises(SavedDeliveryError, match="PARTIAL_EXPLICIT"):
        open_saved_product(partial.receipt.root_path, expected_root=partial.receipt.root_identity,
                           **pinned, **common)
    first = open_saved_product(partial.receipt.root_path, expected_root=partial.receipt.root_identity,
                               **pinned, **common, allow_partial=True)
    assert first.batch_census == partial.batch_census
    with pytest.raises(DurableEmpiricalClosureError):
        execute_publish_saved(**common, saved_admission_factory=lambda: pytest.fail("bad root opened C11"),
                              root_dir=root, resume_from=replace(first_pin, expected_root="0"*64))
    # A second partial checkpoint, with prior receipts and preimages retained.
    middle = execute_publish_saved(**common, saved_admission_factory=factory,
                                  root_dir=root, resume_from=first_pin, max_units=2)
    assert middle.batch_census["completed_count"] == 5
    assert not middle.complete and sum(counts.values()) == 5
    mid_pin = SavedResumePin(middle.receipt.root_path, middle.receipt.root_identity, **pinned)
    final = execute_publish_saved(**common, saved_admission_factory=factory,
                                  root_dir=root, resume_from=mid_pin)
    assert final.complete
    assert final.batch_census["completed_count"] == len(workload.requests)+len(workload.discoveries)
    assert set(counts.values()) == {1}, "completed native unit reexecuted during resume"
    assert sum(counts.values()) == final.batch_census["unit_count"]
    for k, v in partial.batch_census["per_unit_full_preimage_sha256"].items():
        assert final.batch_census["per_unit_full_preimage_sha256"][k] == v
    # A complete run must be used cold, never reopen C11 on a resume request.
    with pytest.raises(SavedDeliveryError, match="ALREADY_COMPLETE"):
        execute_publish_saved(**common, saved_admission_factory=lambda: pytest.fail("complete replay opened C11"),
            root_dir=root, resume_from=SavedResumePin(final.receipt.root_path, final.receipt.root_identity, **pinned))
    shutil.rmtree(estate.path)
    monkeypatch.setattr(SavedC11Admission, "open", lambda *a, **k: pytest.fail("cold result opened C11"))
    cold = open_saved_product(final.receipt.root_path, expected_root=final.receipt.root_identity,
                              **pinned, **common)
    assert cold.complete
    assert cold.batch_census == final.batch_census
    assert len(cold._closure.discovery_results) == len(workload.discoveries)
    assert cold._closure.i05_result is None
    assert cold._closure.manifest["core"]["native_result"]["typed_states"]["resumed_from_root"] == middle.receipt.root_identity
    assert len(cold._closure.object_graph.discovery_authorities) == len(workload.discoveries)
    if mode == "query-only":
        assert not cold._closure.object_graph.discovery_receipts
        assert cold._closure.census["declared"]["unvisited_state"] == "NO_NATIVE_DISCOVERY_EXECUTED"
    else:
        # Each actual frontier retained separately, never combined as one.
        refs = set()
        for d in cold._closure.discovery_results:
            assert d.candidate_count > 0
            assert d.candidate_count == len(d.receipts)
            for r in d.receipts:
                assert r.ref not in refs
                refs.add(r.ref)
                assert cold._closure.discovery_by_receipt(r.ref).replay_ref == d.replay_ref
        assert len(refs) == len(cold._closure.object_graph.discovery_receipts)
    reads = [cold.read_s04(r.query_ref) for r in workload.requests]
    assert any(r.first_consumer.knowledge.material()["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE" for r in reads)
    assert any(r.first_consumer.knowledge.material()["state"] == "PRODUCER_TYPED_HELD" for r in reads)
    # Original checkpoint remains exact and readable after later publication.
    restored = open_saved_product(partial.receipt.root_path, expected_root=partial.receipt.root_identity,
                                  **pinned, **common, allow_partial=True)
    assert restored.batch_census == partial.batch_census
    print("GENERAL_ARCHIVE", mode, final.batch_census["unit_count"],
          len(cold._closure.discovery_results), final.receipt.root_identity,
          "checkpoint_completed", 3, 5, final.batch_census["completed_count"],
          "native_calls", sum(counts.values()))


def test_failed_and_deferred_attempts_retained_without_reexecuting_completed_units(tmp_path, monkeypatch):
    from rawlsing_next.pre553_batch_runner import BatchDeferred
    handoff, estate, initial, v1, _, _ = s1e._full(tmp_path/"source")
    issued = _issue_compiled_governed_queries_v2(v1).issued
    workload, resolver = _issued_shape(issued, "query-only")
    common = dict(workload=workload, resolver=resolver, host=s1e._NATIVE_HOST,
                  purpose=s1e._NATIVE_PURPOSE)
    def factory():
        return _v2_admission(initial, workload.catalog)
    calls = Counter()
    failure_refs = []
    actual = PreparedI03Session.execute_i03
    def fail_twice(self, *, query_ref, predicate_ref):
        calls[query_ref.key] += 1
        if sum(calls.values()) == 1:
            failure_refs.append(query_ref)
            raise OSError("injected interrupted native operation")
        if sum(calls.values()) == 2:
            failure_refs.append(query_ref)
            raise BatchDeferred("TEST_ONLY_PENDING_DEPENDENCY", "explicit retry required")
        return actual(self, query_ref=query_ref, predicate_ref=predicate_ref)
    monkeypatch.setattr(PreparedI03Session, "execute_i03", fail_twice)
    root = tmp_path/"products"
    part = execute_publish_saved(**common, saved_admission_factory=factory,
                                 root_dir=root, max_units=3)
    assert part.batch_census["completed_count"] == 1
    pinned = dict(expected_release_ref=initial.release_ref,
                  expected_saved_manifest_sha256=initial.manifest_sha256)
    cold = open_saved_product(part.receipt.root_path, expected_root=part.receipt.root_identity,
                              **pinned, **common, allow_partial=True)
    assert {r.state for r in cold._receipts} == {"COMPLETED", "FAILED", "DEFERRED"}
    for ref in failure_refs:
        with pytest.raises(SavedDeliveryError, match="QUERY_NOT_IN_RETAINED"):
            cold.read_s04(ref)
    final = execute_publish_saved(**common, saved_admission_factory=factory, root_dir=root,
        resume_from=SavedResumePin(part.receipt.root_path, part.receipt.root_identity, **pinned))
    assert final.complete
    end = open_saved_product(final.receipt.root_path, expected_root=final.receipt.root_identity,
                              **pinned, **common)
    assert len(end._receipts) == len(workload.requests) + 2
    assert {r.state for r in end._receipts} == {"COMPLETED", "FAILED", "DEFERRED"}
    for ref in failure_refs:
        assert calls[ref.key] == 2
        assert end.read_s04(ref).first_consumer.execution.query_ref == ref
    assert all(n == 1 for key,n in calls.items() if key not in {ref.key for ref in failure_refs})
    assert all(final.batch_census["per_unit_full_preimage_sha256"][k] == v
               for k,v in part.batch_census["per_unit_full_preimage_sha256"].items())
    print("RETAINED_RETRY", final.batch_census["unit_count"], len(end._receipts),
          "failed_deferred_retained", final.receipt.root_identity)


def test_inflight_checkpoint_survives_abrupt_process_loss(tmp_path, monkeypatch):
    """Kill a publisher mid-attempt, then recover from independently held root.

    Only the caller's pin and persisted C11/S2-F survive. Fork is used to carry
    the already-issued test-only catalog, not a live native result/session.
    Uncommitted work may be repeated; completed checkpointed units must not.
    """
    import json
    import os
    import multiprocessing
    from rawlsing_next.pre553_empirical_objects import exact_ref
    from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session

    if "fork" not in multiprocessing.get_all_start_methods():
        pytest.skip("OS fork required for abrupt process-loss court")
    handoff, estate, initial, v1, _, _ = s1e._full(tmp_path/"source")
    issued = _issue_compiled_governed_queries_v2(v1).issued
    workload, resolver = _issued_shape(issued, "query-only")
    for p in (tmp_path/"source").rglob("*.sav"):
        p.unlink()
    common = dict(workload=workload, resolver=resolver, host=s1e._NATIVE_HOST,
                  purpose=s1e._NATIVE_PURPOSE)
    root = tmp_path/"products"
    journal = tmp_path/"external-pins.jsonl"
    calls = tmp_path/"native-calls.jsonl"
    builds = tmp_path/"prepared-builds.jsonl"
    original = PreparedI03Session.execute_i03
    original_build = DirectEstateI03Session._build
    parent_pid = os.getpid()
    attempt_count = 0

    def append(path, item):
        # Independent test custodian: fsync each returned pin before
        # acknowledging it; never discover a pin by scanning archive names.
        with path.open("a", encoding="utf8") as stream:
            stream.write(json.dumps(item, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    def rows(path):
        return [json.loads(line) for line in path.read_text().splitlines()]

    def query(self, *, query_ref, predicate_ref):
        nonlocal attempt_count
        attempt_count += 1
        output = original(self, query_ref=query_ref, predicate_ref=predicate_ref)
        append(calls, {"pid": os.getpid(), "query": query_ref.key})
        if os.getpid() != parent_pid and attempt_count == 5:
            # No Python finally/ExitStack cleanup, after real native work,
            # before the fifth attempt can return to the Batch owner.
            os._exit(73)
        return output

    def build(self):
        append(builds, {"pid": os.getpid()})
        return original_build(self)

    monkeypatch.setattr(PreparedI03Session, "execute_i03", query)
    monkeypatch.setattr(DirectEstateI03Session, "_build", build)
    def factory():
        return _v2_admission(initial, workload.catalog)

    def observe(pin, publication):
        append(journal, {
            "path": str(pin.closure_path), "root": pin.expected_root,
            "release": pin.expected_release_ref.as_dict(),
            "saved_manifest": pin.expected_saved_manifest_sha256,
            "completed": publication.batch_census["completed_count"],
            "hashes": publication.batch_census["per_unit_full_preimage_sha256"],
        })

    def run():
        execute_publish_saved(**common, saved_admission_factory=factory,
                              root_dir=root, checkpoint_every=3,
                              checkpoint_observer=observe)

    process = multiprocessing.get_context("fork").Process(target=run)
    process.start()
    process.join(120)
    if process.is_alive():
        process.kill()
        process.join()
        pytest.fail("publisher did not terminate at real process-loss failpoint")
    assert process.exitcode == 73, "publisher did not reach the injected abrupt exit"
    first, = rows(journal)
    assert first["completed"] == 3
    assert len(rows(calls)) == 5
    assert len(rows(builds)) == 1
    pin = SavedResumePin(first["path"], first["root"], exact_ref(first["release"]),
                         first["saved_manifest"])
    cold = open_saved_product(pin.closure_path, expected_root=pin.expected_root,
        expected_release_ref=pin.expected_release_ref,
        expected_saved_manifest_sha256=pin.expected_saved_manifest_sha256,
        **common, allow_partial=True)
    assert cold.batch_census["completed_count"] == 3
    retained_queries = {r.query_ref.key for r in cold._closure.i03_results}
    assert retained_queries == {r["query"] for r in rows(calls)[:3]}
    result = execute_publish_saved(**common, saved_admission_factory=factory,
        root_dir=root, resume_from=pin, checkpoint_every=3,
        checkpoint_observer=observe)
    assert result.complete
    entries = rows(journal)
    assert [x["completed"] for x in entries] == [3, 6, 9, 12]
    assert entries[-1]["root"] == result.receipt.root_identity
    assert len(rows(builds)) == 2, "each process must reuse one prepared saved reader"
    history = rows(calls)
    frequencies = Counter(x["query"] for x in history)
    assert all(frequencies[key] == 1 for key in retained_queries)
    assert len(frequencies) == len(workload.requests)
    assert sum(frequencies.values()) == len(workload.requests) + 2
    assert all(result.batch_census["per_unit_full_preimage_sha256"][k] == v
               for k, v in first["hashes"].items())
    # Every root is independently cold readable; explicit prior-root ancestry
    # is conserved even across process death.
    shutil.rmtree(estate.path)
    monkeypatch.setattr(SavedC11Admission, "open", lambda *a, **k: pytest.fail("cold reopened C11"))
    for idx, item in enumerate(entries):
        reopened = open_saved_product(item["path"], expected_root=item["root"],
            expected_release_ref=exact_ref(item["release"]),
            expected_saved_manifest_sha256=item["saved_manifest"],
            **common, allow_partial=True)
        assert reopened.batch_census["completed_count"] == item["completed"]
        assert reopened._closure.manifest["core"]["native_result"]["typed_states"]["resumed_from_root"] == (
            None if idx == 0 else entries[idx-1]["root"])
    assert len([cold.read_s04(r.query_ref) for r in cold._closure.i03_results]) == 3
    print("ABRUPT_RECOVERY", process.exitcode, [x["completed"] for x in entries],
          "native_calls", len(history), "checkpointed_no_repeat", len(retained_queries),
          "prepared_builds", len(rows(builds)), "final", result.receipt.root_identity)
