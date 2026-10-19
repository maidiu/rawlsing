"""Deterministic projection of frozen original metadata; never issue U/E_pre.

No raw reader, result-dependent selection or all-pairs scientific expansion.
Native executable units are produced only by pre553_issued_workload from an
authenticated original scientific decision. Research rows are not operations.
"""
from collections import Counter, defaultdict
import csv
import hashlib
import gzip
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def load(path):
    return json.loads((R / path).read_text())


def rows(path):
    return list(csv.DictReader((R / path).open()))


def lines(path):
    return [json.loads(x) for x in (R / path).read_text().splitlines()]


def dump(path, value):
    dest = R / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


def verify_freeze():
    frozen = load("PREIMPLEMENTATION_FREEZE.json")
    for path, sha in frozen["inputs"].items():
        if hashlib.sha256((R / path).read_bytes()).hexdigest() != sha:
            raise ValueError("PROSPECTIVE_INPUT_CHANGED:" + path)
    return frozen


def independent_union():
    p2 = lines("inputs/wg0x/sources/p2_identity_projection.jsonl")
    qra = lines("inputs/wg0x/sources/qra_identity_projection.jsonl")
    active = [q for q in qra if q["authority_status"] != "EXCLUDED_INACTIVE_WAVE"]
    qby = {q["p2_exact_identity_sha256"]: q for q in active if q["p2_exact_identity_sha256"]}
    out = []
    for p in p2:
        q = qby.get(p["exact_identity_sha256"])
        out.append(dict(identity="P2:" + p["exact_identity_sha256"], family=p["source_family"],
            wave=p["wave"], variable=p["source_variable_code"], p2=p, qra=q))
    for q in active:
        if not q["p2_exact_identity_sha256"]:
            out.append(dict(identity="QRA:" + q["question_id"], family=q["canonical_source"],
                wave=q["canonical_wave"], variable=q["var_code"], p2=None, qra=q))
    if len(p2) != 18276 or len(active) != 18259 or len(out) != 18285:
        raise ValueError("FROZEN_IDENTITY_CENSUS_CHANGED")
    if len({x["identity"] for x in out}) != len(out):
        raise ValueError("IDENTITY_MULTIPLICITY")
    return sorted(out, key=lambda x: x["identity"]), [q for q in qra if q["authority_status"] == "EXCLUDED_INACTIVE_WAVE"]


FAMILY_DECISIONS = {
    "I03_RAW_MARGINAL": "Exact occurrence/options/missing and source-local target/risk/denominator; no population implication.",
    "I03_DIRECTED_CONDITIONAL": "Independently meaningful target and eligible conditioner, exact direction and same-carrier risk; reverse is a separate decision.",
    "I03_WEIGHTED_ESTIMAND": "Explicit source/country design, valid weight, population/estimand and normalization authority; never weight=1 by default.",
    "I03_HIGHER_ORDER_JOINT": "Source-native co-signature with independently justified target tuple, nonredundancy and common respondent/household risk. Unlinked sources cannot be joined as people.",
    "I05_FINITE_DISCOVERY": "Frozen predicate/query grammar, depths, budgets, validation/support and complete expected frontier, including minority/opposing/low/null/zero outcomes.",
    "SOURCE_CARRIER_CONTEXT": "Country/region/time/design/admin and household/selected-person bindings are preserved inputs, never automatically substantive measurement targets.",
    "STRUCTURAL_F5_F6_F7": "Separate structural admission, independent-source transport and comparable-time authorities; empirical associations do not issue structural or causal truth.",
}


def build():
    freeze = verify_freeze()
    wg0r_freeze = load("WG0R_INPUT_FREEZE.json")
    if hashlib.sha256((R / wg0r_freeze["local_input"]).read_bytes()).hexdigest() != wg0r_freeze["sha256"]:
        raise ValueError("FROZEN_WG0R_REPAIRED_ACCOUNTING_CHANGED")
    wg0r_rows = rows(wg0r_freeze["local_input"])
    wg0r = {row["exact_identity_sha256"]: row for row in wg0r_rows}
    if (len(wg0r), sum(row["hard_fail"] == "True" for row in wg0r_rows),
            sum(row["route_predicate_required"] == "True" for row in wg0r_rows)) != (18276,10418,4447):
        raise ValueError("WG0R_FLAGS_OR_IDENTITY_CONSERVATION")
    union, inactive = independent_union()
    waves = load("inputs/wg0x/sources/o35e_scope.json")["waves"]
    if len(waves) != 35 or Counter(w["dataset_manifest_identity"]["format"] for w in waves) != {"sav": 31, "dta": 4}:
        raise ValueError("ORIGINAL35_PHYSICAL_FORMAT_DENOMINATOR_CHANGED")
    wm = {(w["canonical_source_family"], w["canonical_wave"]): w for w in waves}
    countries = defaultdict(list)
    for row in rows("inputs/startup/country_source_mapping_registry.csv"):
        countries[row["source_family"], row["canonical_wave"]].append(row)
    structure = {(x["source_family"], x["canonical_wave"]): x for x in rows("inputs/startup/source_structure_validation_manifest.csv") if x["canonical_intended"] == "True"}
    semantic = defaultdict(list)
    for ordinal, row in enumerate(rows("inputs/startup/question_structural_mapping_live_PLUS4_FINAL_APPLIED_R1.csv"), 1):
        semantic[row["source"], row["canonical_wave"], row["var_code"]].append(dict(record=ordinal, row=row, sha256=digest(row)))
    frontier = []
    for u in union:
        key = (u["family"], u["wave"])
        if key not in wm:
            raise ValueError("UNEXPECTED_ORIGINAL_WAVE")
        w = wm[key]; p = u["p2"] or {}; q = u["qra"] or {}
        role = p.get("authority_semantic_role", q.get("authority_status"))
        is_carrier = role in {"admin", "administrative_metadata", "GOVERNED_ADMINISTRATIVE_DISPOSITION"}
        # These are decision dimensions, not eligible operation identities.
        requested = ["SOURCE_CARRIER_CONTEXT"] if is_carrier else list(FAMILY_DECISIONS)
        frontier.append(dict(research_identity=u["identity"], atlas_id=w["atlas_id"],
            family=u["family"], wave=u["wave"], native_code_as_retained=u["variable"],
            retained_p2_identity=p.get("exact_identity_sha256"),
            retained_p2_record=p.get("csv_record"), retained_qra_record=q.get("csv_record"),
            qra_payload_sha256=q.get("governed_row_payload_hash"),
            inherited_role=role, inherited_response_binding=p.get("response_binding_status"),
            inherited_WG0R_disposition=wg0r.get(p.get("exact_identity_sha256")),
            retained_response_form=q.get("manual_response_topology", q.get("p2_response_topology")),
            country_scope_as_recorded=q.get("country_code_scope"),
            semantic_assertions=semantic.get((u["family"],u["wave"],u["variable"]), []),
            operation_family_decisions=requested,
            status="NOT_YET_ISSUED", eligible_operation_ids=None,
            source_native_occurrence_and_form=None, options_missing_route=None,
            carrier_sampling_unit_and_risk=None, weight_design_estimand=None,
            source_permission_ref=None, scientific_permission_ref=None,
            missing_requirement_refs=[w["atlas_id"]+":"+x for x in (
                "SOURCE_HOST_PURPOSE", "COMPLETE_NATIVE_U", "RESPONSE_ROUTING_CARRIER", "SCIENTIFIC_E_PRE")],
            science_boundary="RESEARCH_RECORD_NOT_ADMINISTERED_ITEM_OR_ELIGIBLE_OPERATION"))
    bywave = defaultdict(list)
    for item in frontier:
        bywave[item["atlas_id"]].append(item)
    packets = []; waveout = []
    for w in waves:
        key = (w["canonical_source_family"],w["canonical_wave"])
        items = bywave[w["atlas_id"]]; cs = countries[key]
        shas = sorted({c["source_file_sha256"] for c in cs if c["source_file_sha256"]})
        itemroot = digest([(r["research_identity"],digest(r)) for r in items])
        source = dict(atlas_id=w["atlas_id"], family=key[0], wave=key[1],
            original_manifest_identity=w["dataset_manifest_identity"],
            historical_country_registry_source_hashes=shas,
            historical_country_rows=cs, historical_structure=structure.get(key),
            current_source_edition_hash=None, current_source_access_permission=None,
            historical_hash_is_current_grant=False, raw_source_opened=False,
            research_identity_count=len(items), research_identity_root=itemroot,
            original_U_count=None, eligible_E_pre_count=None,
            permitted_native_execution_manifests=[], native_BatchManifest=None,
            measured_original_products=0,
            reason="NO_VERIFIED_CURRENT_SOURCE_HOST_PURPOSE_AND_SCIENTIFIC_E_PRE_ISSUANCE")
        waveout.append(source)
        demands = [
            ("SOURCE_HOST_PURPOSE", "Competent original source access/licence custodian (not project HQ)",
             ["Confirm exact physical edition/hash and release", "Authenticate local qualified U43/B43 host identity", "Grant read purpose: instrument/metadata prospective U freeze, then only separately permitted aggregate I03/I05/Batch", "State retention/export limits, expiry/revocation and authenticated permission ref"]),
            ("COMPLETE_NATIVE_U", "Original questionnaire/instrument and source-structure issuer",
             ["Issue complete administered occurrence inventory, including country/split/repeated/ranked/MR forms", "Resolve retained-code to physical column/occurrence with no parent/stem aliases by inference", "Include source-only items beyond retained research union or explicitly certify completeness"]),
            ("RESPONSE_ROUTING_CARRIER", "Source response/routing/subject-identity and sampling-design issuers",
             ["Issue full response options, missing-state/routing and risk-set rules", "Bind respondent versus household versus selected adult and namespace", "Bind country/geography/frame/design/weights and explicit eligible population/estimand; no imputed unit weights"]),
            ("SCIENTIFIC_E_PRE", "Competent source-specific scientific operation issuer and semantic role owner",
             ["Freeze U and E_pre roots before empirical outcomes", "Issue meaningful target/conditioner directions and higher-order joints, no automatic all-pairs", "Issue finite discovery grammar and minority/counterpattern/null/zero/low-support coverage", "Provide exact native projection/catalog/query/predicate/discovery preimages and authenticated descriptor envelope"]),
            ("CONSUMER_PURPOSE", "Original source purpose issuer plus existing M1/I4/F1-F8/N9/N10E/N10W consumer authorities",
             ["Name permitted downstream consumers and scope per fact", "Separate scientific structural/transport/temporal permissions from empirical query grants", "Leave N11/N12/actor and Sorok decisions to their competent owners"]),
        ]
        packets.append(dict(atlas_id=w["atlas_id"], source=source,
            status="DECISION_READY_UNSIGNED_REQUEST__NOT_A_GRANT",
            requested_host="U43 isolated native local environment; authenticate exact host in decision",
            requested_purpose="Prospective complete source-native workload into selected Route B; nonperson aggregate receipts to B43/A42",
            research_inventory_root=itemroot, competent_issuer_identity=None,
            demands=[dict(demand_id=w["atlas_id"]+":"+code, owner=owner,
                authenticated_owner_ref=None, exact_next_actions=actions) for code,owner,actions in demands],
            native_entrypoint="rawlsing_next.pre553_issued_workload.execute_issued_workload",
            no_raw_or_respondent_publication=True))
    return frontier, waveout, packets, inactive


def verify_no_drop(candidate, expected=None):
    expected = build()[0] if expected is None else expected
    a = Counter((r["research_identity"], digest(r)) for r in candidate)
    b = Counter((r["research_identity"], digest(r)) for r in expected)
    if a != b:
        raise ValueError("ORIGINAL35_EXACT_NO_DROP_ASSERTION:" + str(dict(missing=sum((b-a).values()), unexpected=sum((a-b).values()))))
    return dict(expected=len(expected), actual=len(candidate), missing=0, unexpected=0)


def main():
    frontier, waves, packets, inactive = build()
    verify_no_drop(frontier)
    out = R / "source_wave_item_operation_frontier.jsonl.gz"
    content = "".join(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",", ":"))+"\n" for x in frontier).encode()
    with out.open("wb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, mtime=0) as compressed:
            compressed.write(content)
    dump("original35_wave_execution_manifest.json", waves)
    dump("original35_issuer_decision_packets.json", packets)
    dump("inactive259_preserved.json", inactive)
    dump("operation_family_decision_requirements.json", FAMILY_DECISIONS)
    summary = dict(waves=len(waves), format_counts=dict(Counter(w["original_manifest_identity"]["format"] for w in waves)),
        research_identities=len(frontier), original_U_count=None, eligible_E_pre_count=None,
        original_measured=0, original_permitted_manifests=0, sourcefree_is_original=False,
        historical_source_hash_waves=sum(bool(w["historical_country_registry_source_hashes"]) for w in waves),
        source_specific_issuer_packets=len(packets), exact_owner_decisions=sum(len(p["demands"]) for p in packets),
        WG0R_hard_fail_flags=10418, WG0R_route_predicate_required_flags=4447,
        frontier_sha256=hashlib.sha256(content).hexdigest(),
        compressed_frontier_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        anti_join=verify_no_drop(frontier), acceptance_cells=1890, eligible_operations_from_cells=False,
        status="EXECUTABLE_ISSUER_INGRESS_READY__ORIGINAL_U_E_PRE_AND_SOURCE_EXECUTION_UNISSUED")
    dump("evidence/original35_frontier_summary.json", summary)
    print(json.dumps(summary,sort_keys=True))


if __name__ == "__main__":
    main()
