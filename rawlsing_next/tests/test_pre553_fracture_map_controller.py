import pytest

from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec, canonical_json
from rawlsing_next.pre553_fracture_map_controller import (
    Authority37ControllerPolicy,
    FractureMapController,
    FractureMapControllerError,
    construct_four_way_branches,
)
from rawlsing_next.pre553_recursive_handoff import (
    load_recursive_handoff_bundle,
    write_recursive_handoff_bundle,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _query,
    _query_authority,
    _registry,
    _run,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _d_auth,
    _discovery_authority,
)


class Binder:
    def __init__(self, source, dauth, controller=None, probe=None):
        self.source = source
        self.dauth = dauth
        self.controller = controller
        self.probe = probe
        self.blocked_mutation = False

    def bind(self, frontier):
        if self.probe is not None:
            try:
                self.controller.seal_predictor_frontier(**self.probe)
            except FractureMapControllerError:
                self.blocked_mutation = True
        return _discovery_authority(
            self.source,
            frontier.candidate_universe_definition,
            self.dauth,
            grammar_ref=frontier.candidate_grammar_ref,
            tag="auth37-controller",
        )


def _policy(**kwargs):
    defaults = dict(minimum_split_raw_n=2, minimum_report_raw_n=1, maximum_depth=4)
    defaults.update(kwargs)
    return Authority37ControllerPolicy(**defaults)


def _setup(tag="controller"):
    rows = [
        {"id": "R1", "responses": {"Y": 1}, "coords": {"G": "A", "H": "X"}},
        {"id": "R2", "responses": {"Y": 1}, "coords": {"G": "A", "H": "Y"}},
        {"id": "R3", "responses": {"Y": 0}, "coords": {"G": "A", "H": "X"}},
        {"id": "R4", "responses": {"Y": 1}, "coords": {"G": "B", "H": "Y"}},
        {"id": "R5", "responses": {"Y": 0}, "coords": {"G": "B", "H": "X"}},
        {"id": "R6", "responses": {"Y": 0}, "coords": {"G": "B", "H": "Y"}},
        {"id": "R7", "responses": {"Y": 1}, "coords": {"H": "X"}},
    ]
    source = _build_source(tag, rows)
    qauth, dauth = _query_authority(tag), _d_auth(tag + "-discovery")
    parent = _branch_predicate(source, qauth, tag="root")
    root = _query(source, qauth, parent, ("Y",), tag="root")
    registry = _registry(source, qauth, dauth)
    controller = FractureMapController(policy=_policy())
    coord_auths = (source["coord_auth"].authority_ref,)
    return source, qauth, dauth, parent, root, registry, controller, coord_auths


def test_caller_supplies_root_not_winner_and_controller_enumerates_complete_coordinate_catalog():
    source, qauth, dauth, parent, root, registry, controller, coord_auths = _setup("catalog")
    morphology = controller.root_morphology(
        repository=source["repo"], root_query=root, root_predicate=parent,
        authority_registry=registry, release_refs=(source["release_ref"],),
    )
    assert morphology.unique_modal_cell == "1"
    catalog = controller.coordinate_catalog(
        repository=source["repo"], root_query=root, root_predicate=parent,
        release_refs=(source["release_ref"],), coordinate_authority_refs=coord_auths,
    )
    values = {(c.coordinate_ref.key, c.exact_value) for c in catalog}
    assert len(values) == 4
    assert {c.exact_value for c in catalog} == {"A", "B", "X", "Y"}
    frontier = controller.seal_predictor_frontier(
        parent_predicate=parent, root_query=root, coordinate_conditions=catalog, depth=0,
    )
    assert len(frontier.candidate_universe_definition["rules"][0]["atom_ids"]) == 4
    assert all(a["kind"] == "COORDINATE" for a in frontier.candidate_universe_definition["atoms"][1:])


def test_alternative_converger_and_predictor_violating_deviant_are_discovered_and_missing_G_not_absent():
    source, qauth, dauth, parent, root, registry, controller, coord_auths = _setup("branches")
    morphology = controller.root_morphology(
        repository=source["repo"], root_query=root, root_predicate=parent,
        authority_registry=registry, release_refs=(source["release_ref"],),
    )
    catalog = controller.coordinate_catalog(
        repository=source["repo"], root_query=root, root_predicate=parent,
        release_refs=(source["release_ref"],), coordinate_authority_refs=coord_auths,
    )
    frontier = controller.seal_predictor_frontier(
        parent_predicate=parent, root_query=root, coordinate_conditions=catalog, depth=0,
    )
    binder = Binder(source, dauth)
    result = controller.execute_frontier(
        repository=source["repo"], frontier=frontier, binder=binder,
        authority_registry=registry, release_refs=(source["release_ref"],), depth=0,
    )
    supported = controller.supported_predictor_conditions(result=result, frontier=frontier)
    g_a = next(c for c in supported if c.exact_value == "A" and c.coordinate_ref == source["crefs"]["G"])
    roles = {r.role: r for r in construct_four_way_branches(
        parent_predicate=parent, root_query=root, morphology=morphology, predictor=g_a,
    )}
    dev = _run(source, qauth, roles["DEVIANT_EXIT"].predicate,
               _query(source, qauth, roles["DEVIANT_EXIT"].predicate, ("Y",), tag="dev"),
               registry=_registry(source, qauth)).facts[0]
    alt = _run(source, qauth, roles["ALT_CONVERGER"].predicate,
               _query(source, qauth, roles["ALT_CONVERGER"].predicate, ("Y",), tag="alt"),
               registry=_registry(source, qauth)).facts[0]
    assert dev.raw_denominator_support == 1
    assert alt.raw_denominator_support == 1
    # R7 has no G coordinate and must not be absorbed into NOT(G=A).
    alt_ids = {ref["object_id"] for ref in alt.denominator_member_refs}
    assert source["respondents"]["R7"].ref.object_id not in alt_ids


def test_exact_tie_never_forces_modal_winner():
    rows = [
        {"id": "R1", "responses": {"Y": 0}, "coords": {"G": "A"}},
        {"id": "R2", "responses": {"Y": 0}, "coords": {"G": "B"}},
        {"id": "R3", "responses": {"Y": 1}, "coords": {"G": "A"}},
        {"id": "R4", "responses": {"Y": 1}, "coords": {"G": "B"}},
    ]
    source = _build_source("tie-controller", rows)
    qauth, dauth = _query_authority("tie-controller"), _d_auth("tie-controller-discovery")
    parent = _branch_predicate(source, qauth)
    root = _query(source, qauth, parent, ("Y",), tag="tie")
    controller = FractureMapController(policy=_policy())
    morphology = controller.root_morphology(
        repository=source["repo"], root_query=root, root_predicate=parent,
        authority_registry=_registry(source, qauth, dauth), release_refs=(source["release_ref"],),
    )
    assert morphology.unresolved_maximal_tie is True
    assert set(morphology.modal_cells) == {"0", "1"}
    assert morphology.unique_modal_cell is None


def test_DK_refusal_missing_are_not_substantive_nonmodal():
    source, qauth, dauth, parent, base, registry, controller, coord_auths = _setup("nonresponse")
    fields = dict(base.semantic_fields)
    topo = dict(fields["target_arity_and_topology"])
    comps = [dict(topo["components"][0])]
    comps[0]["domain"] = ["0", "1", "DK", "REFUSED", "MISSING"]
    topo["components"] = comps
    fields["target_arity_and_topology"] = topo
    root = EmpiricalQuerySpec(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **fields,
    )
    policy = _policy(non_substantive_response_cells=(
        canonical_json("DK"), canonical_json("REFUSED"), canonical_json("MISSING"),
    ))
    controller = FractureMapController(policy=policy)
    morphology = controller.root_morphology(
        repository=source["repo"], root_query=root, root_predicate=parent,
        authority_registry=registry, release_refs=(source["release_ref"],),
    )
    assert set(morphology.substantive_cells) == {"0", "1"}
    catalog = controller.coordinate_catalog(
        repository=source["repo"], root_query=root, root_predicate=parent,
        release_refs=(source["release_ref"],), coordinate_authority_refs=coord_auths,
    )
    g_a = next(c for c in catalog if c.exact_value == "A" and c.coordinate_ref == source["crefs"]["G"])
    roles = construct_four_way_branches(
        parent_predicate=parent, root_query=root, morphology=morphology, predictor=g_a,
    )
    dev = next(r for r in roles if r.role == "DEVIANT_EXIT")
    rendered = canonical_json(dev.predicate.predicate_ast)
    assert "DK" not in rendered and "REFUSED" not in rendered and "MISSING" not in rendered


def test_discovered_child_survives_process_boundary_and_becomes_N_plus_1_parent(tmp_path):
    source, qauth, dauth, parent, root, registry, controller, coord_auths = _setup("handoff-controller")
    morphology = controller.root_morphology(
        repository=source["repo"], root_query=root, root_predicate=parent,
        authority_registry=registry, release_refs=(source["release_ref"],),
    )
    catalog = controller.coordinate_catalog(
        repository=source["repo"], root_query=root, root_predicate=parent,
        release_refs=(source["release_ref"],), coordinate_authority_refs=coord_auths,
    )
    g_a = next(c for c in catalog if c.exact_value == "A" and c.coordinate_ref == source["crefs"]["G"])
    roles = construct_four_way_branches(
        parent_predicate=parent, root_query=root, morphology=morphology, predictor=g_a,
    )
    branch_frontier = controller.seal_branch_frontier(
        parent_predicate=parent, root_query=root, branch_roles=roles, depth=0,
    )
    wrapped = controller.execute_frontier(
        repository=source["repo"], frontier=branch_frontier, binder=Binder(source, dauth),
        authority_registry=registry, release_refs=(source["release_ref"],), depth=0,
        recursive_handoffs=True,
    )
    assert wrapped.handoffs
    path = tmp_path / "handoffs.json"
    write_recursive_handoff_bundle(path, wrapped.handoffs)
    _, loaded = load_recursive_handoff_bundle(path)
    chosen = loaded[0]
    next_frontier = controller.next_frontier_from_handoff(
        handoff=chosen, root_query=root, repository=source["repo"],
        release_refs=(source["release_ref"],), coordinate_authority_refs=coord_auths, depth=1,
    )
    assert next_frontier.parent_predicate.ref == chosen.winning_predicate.ref
    parent_atom = next_frontier.candidate_universe_definition["atoms"][0]
    assert chosen.ref.as_dict() in parent_atom["ancestry_refs"]


def test_identical_inputs_produce_identical_frontier_hashes():
    source, qauth, dauth, parent, root, registry, controller, coord_auths = _setup("replay")
    catalog = controller.coordinate_catalog(
        repository=source["repo"], root_query=root, root_predicate=parent,
        release_refs=(source["release_ref"],), coordinate_authority_refs=coord_auths,
    )
    a = controller.seal_predictor_frontier(
        parent_predicate=parent, root_query=root, coordinate_conditions=catalog, depth=0,
    )
    b = controller.seal_predictor_frontier(
        parent_predicate=parent, root_query=root, coordinate_conditions=tuple(reversed(catalog)), depth=0,
    )
    # Controller canonically sorts the catalog at discovery time; callers cannot control reachability order.
    assert a.candidate_grammar_ref == b.candidate_grammar_ref


def test_partial_generation_cannot_mutate_open_I05_frontier():
    source, qauth, dauth, parent, root, registry, controller, coord_auths = _setup("noninterference")
    catalog = controller.coordinate_catalog(
        repository=source["repo"], root_query=root, root_predicate=parent,
        release_refs=(source["release_ref"],), coordinate_authority_refs=coord_auths,
    )
    frontier = controller.seal_predictor_frontier(
        parent_predicate=parent, root_query=root, coordinate_conditions=catalog, depth=0,
    )
    probe = dict(parent_predicate=parent, root_query=root, coordinate_conditions=catalog, depth=1)
    binder = Binder(source, dauth, controller=controller, probe=probe)
    controller.execute_frontier(
        repository=source["repo"], frontier=frontier, binder=binder,
        authority_registry=registry, release_refs=(source["release_ref"],), depth=0,
    )
    assert binder.blocked_mutation is True
