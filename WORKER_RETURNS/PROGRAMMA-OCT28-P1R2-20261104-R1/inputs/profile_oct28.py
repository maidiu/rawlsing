"""Sourcefree OCT28-E1 measurements from existing PRE553 fixture owners."""
import argparse
from contextlib import ExitStack
import json
import platform
import resource
import shutil
import sys
from collections import Counter
from functools import wraps
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path
from time import perf_counter_ns
from unittest.mock import patch

from rawlsing_next import (
    _pre553_query_common as common,
    _pre553_query_eval as evaluate,
    _pre553_query_predicate as predicate,
    pre553_empirical_query as i03,
    pre553_issued_workload as workload,
    pre553_physical_decoder as decoder,
    pre553_source_backed_c11_facade as facade,
    pre553_source_native_preimage_adapter as preimages,
    pre553_universal_world_binding as world,
)
from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash
from rawlsing_next.tests import (
    pre553_query_frontier_fixtures as frontier,
    test_pre553_empirical_query as cases,
    test_universal_world_binding as joined,
)

PHASES = (
    ("decode", decoder, "_decode"),
    ("source_preimages", preimages, "materialize_native_preimages"),
    ("candidate", facade, "project_c11_candidate_from_physical_cells"),
    ("validate_and_realize", facade, "validate_c11_source_release"),
    ("repository_exact_lookup_realization", common.C11Repository, "_commit_validated"),
    ("release_resolution", i03, "_resolve_release_indices"),
    ("index_build", i03, "_build_release_index"),
    ("authority_fitness", i03, "_require_exact_i03_authority_fitness"),
    ("target_plan_and_domain", i03, "_parse_target_plan"),
    ("evaluate_including_risk_predicate_weights_counts", i03, "_evaluate_index_group"),
    ("predicate_membership_compile", evaluate, "_compile_derived_branch_memberships"),
    ("predicate_eval", evaluate, "_eval_predicate"),
    ("risk_routing", evaluate, "_routing_fact_for"),
    ("risk_membership", evaluate, "_risk_membership"),
    ("numeric_target_resolution", evaluate, "_target_configuration"),
    ("weight_resolution", evaluate, "_weight_for"),
    ("fact_and_evidence", i03, "_build_fact"),
    ("negative_fact_and_evidence", i03, "_build_negative_fact"),
    ("replay_materialization", evaluate, "_make_execution_replay_ref"),
    ("complete_cell_materialization", evaluate, "_cell_projection"),
    ("batch_execute", workload, "execute_issued_workload"),
    ("route_b", workload, "execute_route_b_production"),
    ("checkpoint_capture", workload, "capture_joined_checkpoint"),
    ("checkpoint_restore", workload, "restore_joined_checkpoint"),
    ("checkpoint_resume", workload, "resume_joined_workloads"),
    ("p41", world, "_execute_p41_world"),
)

class Profile:
    def __init__(self):
        self.total = Counter()
        self.self_time = Counter()
        self.calls = Counter()
        self.stack = []
        self.checkpoint_bytes = []
        self.release_roots = {}
        self.decoder_roots = {}
        self.route_outputs = []

    def wrap(self, phase, original):
        @wraps(original)
        def measured(*args, **kwargs):
            self.stack.append(0)
            start = perf_counter_ns()
            try:
                output = original(*args, **kwargs)
            finally:
                elapsed = perf_counter_ns() - start
                self.total[phase] += elapsed
                self.self_time[phase] += elapsed - self.stack.pop()
                self.calls[phase] += 1
                if self.stack:
                    self.stack[-1] += elapsed
            if phase == "checkpoint_capture":
                self.checkpoint_bytes.append(len(workload.canonical(output.material())))
            if phase == "decode":
                self.decoder_roots[output.source_sha256] = {
                    "physical_metadata_digest": output.physical_metadata_digest,
                    "decoder_config_sha256": semantic_hash(output.reader_configuration),
                    "row_count": output.row_count,
                }
            if phase == "route_b":
                graph = output.object_graph
                facts = [f.as_dict() for f in graph.empirical_facts]
                self.route_outputs.append({
                    "fact_refs": [f.ref.as_dict() for f in graph.empirical_facts],
                    "query_refs": [q.ref.as_dict() for q in graph.executed_queries],
                    "predicate_refs": [p.ref.as_dict() for p in graph.executed_predicates],
                    "fact_replay_refs": [f.replay_ref for f in graph.empirical_facts],
                    "discovery_receipt_refs": [d.ref.as_dict() for d in graph.discovery_receipts],
                    "fact_bodies_root": semantic_hash(facts),
                    "fact_bytes": len(canonical_json(facts).encode()),
                    "replay_identity": output.replay_receipt["receipt_identity"],
                    "release_ref": output.c11_release.release_ref.as_dict(),
                })
            if phase == "batch_execute":
                item = args[0]
                self.release_roots[item.projection.cache_identity] = {
                    "projection_ref": item.projection.projection_identity_ref.as_dict(),
                    "projection_root": item.projection.cache_identity,
                    "authority_registry_root": semantic_hash(
                        [obj.ref.as_dict() for obj in item.catalog.authorities]),
                    "required_projection_authorities": [
                        obj.as_dict() for obj in item.projection.required_authority_refs],
                }
            return output
        return measured

    def report(self):
        return {
            key: {"calls": self.calls[key], "inclusive_ns": self.total[key],
                  "exclusive_of_other_probes_ns": self.self_time[key]}
            for key, _, _ in PHASES
        }

def result_material(result):
    return {"query_ref": result.query_ref.as_dict(),
            "release_refs": [ref.as_dict() for ref in result.release_refs],
            "source_scope_mode": result.source_scope_mode,
            "facts": [fact.as_dict() for fact in result.facts],
            "fact_refs": [fact.ref.as_dict() for fact in result.facts],
            "replay_refs": [fact.replay_ref for fact in result.facts]}

def query_cases():
    rows = [{"id": f"R{i}", "responses": {"X": (i // 2) % 2, "Y": i % 2}}
            for i in range(1, 13)]
    risks = {"R": {target: {row["id"] for row in rows} for target in ("X", "Y")},
             "S": {"Y": {"R1", "R2"}}}
    source = cases._build_source("oct28-sourcefree", rows, risk_sets=risks)
    foreign = cases._build_source("oct28-second-sourcefree", rows, risk_sets=risks)
    topology = cases._build_source("oct28-multiselect", rows,
                                  topology_by_question={"Y": "UNORDERED_MULTISELECT_SET"})

    def bind(src, tags):
        auth = cases._query_authority(src["universe"].object_id)
        pred = cases._branch_predicate(src, auth)
        return [dict(repository=src["repo"], authority_registry=cases._registry(src, auth),
                     predicate=pred, release_refs=(src["release_ref"],),
                     query=cases._query(src, auth, pred, targets, risk=risk, tag=tag))
                for targets, risk, tag in tags]

    baseline, compatible, different_risk = bind(
        source, [(("Y",), "R", "unary"), (("X",), "R", "compatible"),
                 (("Y",), "S", "different-risk")])
    other, = bind(foreign, [(("Y",), "R", "other-universe")])
    multiselect, = bind(topology, [(("Y",), "R", "scalar-refuses-multiselect")])
    occurrence = frontier._build_event_source(
        "oct28-occurrence", [{"id": "R1", "events": {"Q": (
            {"value": "A", "event_id": "M-1", "order_fields": {"multiplicity_index": 0}},
            {"value": "A", "event_id": "M-2", "order_fields": {"multiplicity_index": 1}},
        )}}], {"Q": "REPEATED_EVENT"})
    qa = cases._query_authority("oct28-occurrence")
    pred = cases._branch_predicate(occurrence, qa)
    domain = frontier.FIXTURE_ORACLES["ORDERED_RANKED_MULTIPLICITY"].expected["repeated"]
    repeated = dict(
        repository=occurrence["repo"], authority_registry=cases._registry(occurrence, qa),
        release_refs=(occurrence["release_ref"],), predicate=pred,
        query=frontier._custom_query(
            occurrence, qa, pred, "Q", topology="REPEATED_EVENT", domain=[domain],
            included_states=("SUBSTANTIVE_RESPONSE",), tag="oct28-occurrence"),
    )
    return {"one": (baseline,), "identical": (baseline, baseline),
            "compatible_distinct": (baseline, compatible),
            "different_risk": (baseline, different_risk),
            "different_universe": (baseline, other),
            "multiselect_refusal": (multiselect, multiselect),
            "repeated_occurrence": (repeated, repeated)}

def tree_bytes(path):
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", choices=("joined", "queries"))
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--instrument", action="store_true")
    args = parser.parse_args()
    metadata = {"machine": platform.machine(), "system": platform.platform(),
                "python": sys.version, "dependencies": {
                    p: version(p) for p in ("pandas", "pyreadstat", "pyarrow", "pytest")}}
    if args.scenario == "joined":
        runtime, runtime_base = joined._materialize_p41_runtime()
        try:
            source = args.scratch / "same-source.sav"
            profile = Profile()
            with ExitStack() as stack:
                if args.instrument:
                    for phase, module, name in PHASES:
                        stack.enter_context(patch.object(
                            module, name, profile.wrap(phase, getattr(module, name))))
                start = perf_counter_ns()
                runs = [joined._same_source_connected(str(runtime), source)
                        for _ in range(args.rounds)]
                elapsed = perf_counter_ns() - start
            out = {"runs": [value["hashes"] for value in runs], "wall_ns": elapsed,
                   "p41_consumer_values": [value["view"].consumer_values_read for value in runs],
                   "route_outputs": profile.route_outputs,
                   "phases": profile.report(), "decoder_roots": profile.decoder_roots,
                   "projection_and_authority_roots": profile.release_roots,
                   "checkpoint_bytes": profile.checkpoint_bytes,
                   "source_sha256": sha256(source.read_bytes()).hexdigest(),
                   "source_bytes": source.stat().st_size,
                   "p41_runtime_scratch_bytes": tree_bytes(runtime_base),
                   "p41_commit": joined.P41_COMMIT}
        finally:
            shutil.rmtree(runtime_base)
    else:
        out = {}
        for label, operations in query_cases().items():
            repositories = {}
            isolated_operations = []
            for operation in operations:
                repo = operation["repository"]
                if repo not in repositories:
                    repositories[repo] = common.C11Repository(
                        repo.resolve_release_exact(ref) for ref in repo.release_refs)
                isolated_operations.append({**operation, "repository": repositories[repo]})
            profile = Profile()
            with ExitStack() as stack:
                if args.instrument:
                    for phase, module, name in PHASES:
                        stack.enter_context(patch.object(
                            module, name, profile.wrap(phase, getattr(module, name))))
                start = perf_counter_ns()
                for _ in range(args.rounds):
                    results = [i03.execute_empirical_query(**kw) for kw in isolated_operations]
                elapsed = perf_counter_ns() - start
            material = [result_material(result) for result in results]
            out[label] = {"wall_ns": elapsed, "rounds": args.rounds,
                          "operations_per_round": len(operations),
                          "phases": profile.report(), "results": material,
                          "result_bytes": len(canonical_json(material).encode())}
    print(canonical_json({"host": metadata, "scenario": args.scenario, "result": out,
                          "peak_rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))

if __name__ == "__main__":
    main()
