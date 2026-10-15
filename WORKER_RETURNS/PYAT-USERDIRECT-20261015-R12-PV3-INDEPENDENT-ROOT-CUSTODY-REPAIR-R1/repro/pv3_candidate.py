"""PV3 request API composed with an independently installed fixture read client.
No request argument can install/change its owner, expected root or current grant.
"""

import copy, json
from dataclasses import dataclass
from collections.abc import Mapping
from fixture_owner import FixtureOwnerReadClient
import pv2_original_scope_register as OLD
from rawlsing_next.pre553_empirical_objects import semantic_hash, ExactRef


class CustodyError(ValueError):
    pass


def validate_consumer_roles_against_declared(links, register):
    for l in links:
        m = l.get("consumer_material")
        if not isinstance(m, Mapping):
            raise CustodyError("MISSING_CONSUMER_MATERIAL")
        roles = m.get("roles")
        if not isinstance(roles, Mapping) or set(roles) != {"CONDITIONER", "TARGET"}:
            raise CustodyError("MISSING_REQUIRED_ROLES")
        for role in ("CONDITIONER", "TARGET"):
            if not isinstance(roles[role], Mapping) or not roles[role].get("ref"):
                raise CustodyError("MISSING_ROLE_REF:" + role)
        for k in (
            "producer_query_ref",
            "producer_fact_ref",
            "risk_set_ref",
            "empirical_universe_refs",
            "participant_role_order",
        ):
            if not m.get(k):
                raise CustodyError("MISSING_REQUIRED_MATERIAL:" + k)
        if m["participant_role_order"] != ["CONDITIONER", "TARGET"]:
            raise CustodyError("WRONG_ROLE_ORDER")
        if l.get("producer_result_ref") != m["producer_fact_ref"]:
            raise CustodyError("PRODUCER_FACT_REF_MISMATCH")
        projection = {
            k: v for k, v in m.items() if k not in ("object_id", "content_hash")
        }
        digest = semantic_hash(projection)
        expected_ref = ExactRef(
            m["relation_family"],
            "urn:rawlsing:field-forge:conditional-support:sha256:" + digest,
            digest,
        ).as_dict()
        if (
            l.get("consumer_ref") != expected_ref
            or m["content_hash"] != digest
            or m["object_id"] != expected_ref["object_id"]
        ):
            raise CustodyError("RELATION_REF_CONTENT_MISMATCH")
    OLD.validate_consumer_roles_against_declared(links, register)


def reconcile_journal(session):
    if not session.store.path.exists():
        if session.side_effect_journal_path.exists():
            raise CustodyError("JOURNAL_WITHOUT_CHECKPOINT")
        return []
    cp = session.store.load(identity=session.identity)
    rows = []
    if session.side_effect_journal_path.exists():
        rows = [
            json.loads(s)
            for s in session.side_effect_journal_path.read_text().splitlines()
            if s.strip()
        ]
    committed = {r.unit_key: r for r in cp.records if r.state == "COMMITTED"}
    if len(rows) != len(committed):
        raise CustodyError("JOURNAL_CHECKPOINT_ANTI_JOIN")
    seen = set()
    proof = []
    for index, j in enumerate(rows, 1):
        key = j.get("unit_key")
        if key in seen or key not in committed:
            raise CustodyError("JOURNAL_FOREIGN_OR_DUPLICATE_UNIT")
        seen.add(key)
        record = committed[key]
        receipt = record.rehydrate_verified()
        expected = {
            "unit_key": key,
            "attempt_index": receipt.attempt_index,
            "result_refs": [r.as_dict() for r in receipt.result_refs],
            "receipt_state": receipt.state,
            "manifest_hash": session.identity.manifest_hash,
            "journal_seq": index,
        }
        if j != expected:
            raise CustodyError("JOURNAL_RECEIPT_PROVENANCE_MISMATCH")
        if (
            receipt.manifest_hash != session.identity.manifest_hash
            or receipt.unit_ref != record.unit_ref
        ):
            raise CustodyError("RECEIPT_MANIFEST_IDENTITY_MISMATCH")
        unit = next(
            (u for u in session.manifest.units if u.unit_ref == receipt.unit_ref), None
        )
        if unit is None or set(receipt.provenance_refs) != set(
            (
                unit.job_ref,
                *unit.semantic_input_refs,
                *unit.release_refs,
                receipt.executor_ref,
            )
        ):
            raise CustodyError("RECEIPT_PROVENANCE_CLOSURE_MISMATCH")
        proof.append(
            {
                "unit_key": key,
                "checkpoint_ref": cp.checkpoint_ref.as_dict(),
                "receipt_hash": record.receipt_hash,
                "receipt_projection": receipt.projection(),
                "journal": j,
            }
        )
    return proof


@dataclass(frozen=True)
class RequestAPI:
    _owner: FixtureOwnerReadClient
    _attest: object

    def _register(self, register):
        i = self._owner.installation
        if (
            not isinstance(register, OLD.PrecommittedOriginalRegister)
            or register.committed_root != i.register_root
            or register.binding() != i.register.binding()
        ):
            raise CustodyError("REQUEST_REGISTER_NOT_INSTALLED_ROOT")

    def run_sourcefree_with_register(
        self,
        *,
        expected,
        selected_scopes,
        register,
        scope_metadata,
        prior_consumer_refs=None,
        validate_topology=True,
        anchor_c11_inventory=True
    ):
        self._register(register)
        i = self._owner.installation
        expected.checked()
        if (
            expected.payload_sha256 != i.expected_root
            or expected.payload_json != i.expected_json
        ):
            raise CustodyError("ORIGINAL_EXPECTED_NOT_INSTALLED_ROOT")
        if not validate_topology or not anchor_c11_inventory:
            raise CustodyError("REQUIRED_GUARD_CANNOT_BE_DISABLED")
        for ns, edition in i.source_editions:
            d = self._owner.resolve(ns)
            if d.withdrawn or d.edition != edition:
                raise CustodyError("CURRENT_SOURCE_WITHDRAWN_OR_CHANGED:" + ns)
        scopes = tuple(selected_scopes)
        for scope in scopes:
            reconcile_journal(scope.p01_kwargs["session"])
        report = OLD.run_sourcefree_with_register(
            expected=expected,
            selected_scopes=scopes,
            register=i.register,
            scope_metadata=scope_metadata,
            prior_consumer_refs=prior_consumer_refs,
        )
        validate_consumer_roles_against_declared(report["links"], i.register)
        proofs = [reconcile_journal(s.p01_kwargs["session"]) for s in scopes]
        # Reconcile each emitted fact/relation against the exact accepted unit result.
        for s, proof in zip(scopes, proofs):
            receipts = {p["unit_key"]: p["receipt_projection"] for p in proof}
            for l in report["links"]:
                if l["original_expected_work_key"] not in s.original_work_keys:
                    continue
                unit_key = ExactRef(**l["batch_unit_ref"]).key
                receipt = receipts[unit_key]
                m = l["consumer_material"]
                if l["owner_job_ref"]["kind"].startswith("EmpiricalQuerySpec"):
                    if l["producer_result_ref"] not in receipt["result_refs"]:
                        raise CustodyError("CONSUMER_FACT_OUTSIDE_UNIT_RECEIPT")
                    fact = s.p01_kwargs["resolve_fact"](
                        ExactRef(**l["producer_result_ref"])
                    )
                    query = s.p01_kwargs["runtime_catalog"].resolve_query_exact(
                        ExactRef(**m["producer_query_ref"])
                    )
                else:
                    outcome = s.p01_kwargs["resolve_discovery"](
                        ExactRef(**receipt["result_refs"][0])
                    )
                    facts = [
                        f
                        for f in outcome.empirical_facts
                        if f.ref.as_dict() == l["producer_result_ref"]
                    ]
                    if len(facts) != 1:
                        raise CustodyError("DISCOVERY_FACT_OUTSIDE_OWNER_RESULT")
                    fact = facts[0]
                    query = next(
                        q
                        for q in outcome.executed_queries
                        if q.ref.as_dict() == m["producer_query_ref"]
                    )
                    discovery_receipt = next(
                        r
                        for r in outcome.receipts
                        if r.ref.as_dict() == receipt["result_refs"][0]
                    )
                    if l["producer_result_ref"] not in list(
                        discovery_receipt.empirical_fact_refs
                    ) or dict(fact.condition_predicate_ref) != dict(
                        discovery_receipt.winning_predicate_ref
                    ):
                        raise CustodyError("DISCOVERY_FACT_NOT_WINNER_CUSTODY")
                if (
                    fact.ref.as_dict() != m["producer_fact_ref"]
                    or semantic_hash(fact.semantic_projection())
                    != fact.ref.content_hash
                ):
                    raise CustodyError("FACT_CONTENT_PROVENANCE_MISMATCH")
                if (
                    query.ref.as_dict() != m["producer_query_ref"]
                    or semantic_hash(query.semantic_projection())
                    != query.ref.content_hash
                ):
                    raise CustodyError("QUERY_CONTENT_PROVENANCE_MISMATCH")
                from rawlsing_next.field_forge_conditional_support import (
                    produce_exact_conditional_support_profile,
                )

                actual = produce_exact_conditional_support_profile(
                    joint_fact=fact,
                    joint_query=query,
                    conditioner_ref=ExactRef(**m["roles"]["CONDITIONER"]["ref"]),
                    target_ref=ExactRef(**m["roles"]["TARGET"]["ref"]),
                    producer_permission_ceiling=("SOURCE_FREE_DEV",),
                )
                if actual.as_dict() != m:
                    raise CustodyError("ACTUAL_RELATION_MATERIAL_MISMATCH")
        baseline = json.loads(i.baseline_links_json)
        for link in report["links"]:
            ns = link["original_identity"]["original"]["respondent_namespace"]
            if i.profile == "BASELINE" or ns == "PV2-ADULT-B":
                if link not in baseline:
                    raise CustodyError("ORIGINAL_SIX_CONSUMER_CUSTODY_MISMATCH")
        report = copy.deepcopy(report)
        report["pv3_receipt_proofs"] = proofs
        report["pv3_limits"] = [
            "GENERIC_NATIVE_SEMANTICS_HOLD",
            "OFFLINE_FACT_RESTORATION_HOLD",
            "REAL_ORIGINAL_U_EPRE_SOURCE_RIGHTS_HOLD",
        ]
        report["pv3_custody"] = self._attest(report)
        return report

    def read_current_consumer_material(
        self,
        register,
        report,
        *,
        namespace=None,
        edition=None,
        clock=None,
        asof=None,
        semantics="SPECIALIZED_TEST_ONLY"
    ):
        self._register(register)
        self._owner.verify_history(report)
        validate_consumer_roles_against_declared(
            report["links"], self._owner.installation.register
        )
        if semantics != "SPECIALIZED_TEST_ONLY":
            return {
                "servable": False,
                "claim": "GENERIC_NATIVE_SEMANTICS_HOLD",
                "historical_links": len(report["links"]),
            }
        links = report["links"]
        if namespace is not None:
            if namespace not in dict(self._owner.installation.source_editions):
                raise CustodyError("UNINSTALLED_SOURCE_NAMESPACE")
            links = [
                l
                for l in links
                if l["original_identity"]["original"]["respondent_namespace"]
                == namespace
            ]
        decisions = {}
        allowed = []
        denied = []
        for ns in sorted(
            {l["original_identity"]["original"]["respondent_namespace"] for l in links}
        ):
            d = self._owner.resolve(ns)
            decisions[ns] = d.__dict__.copy()
            hist_edition = next(
                l["original_identity"]["original"]["source_release_ref"]["content_hash"]
                for l in links
                if l["original_identity"]["original"]["respondent_namespace"] == ns
            )
            stale = (
                d.edition != hist_edition
                or (edition is not None and edition != d.edition)
                or (clock is not None and clock != d.clock)
                or (asof is not None and asof != d.asof)
            )
            (denied if d.withdrawn or stale else allowed).append(ns)
        return copy.deepcopy(
            {
                "servable": not denied,
                "links": [
                    l
                    for l in links
                    if l["original_identity"]["original"]["respondent_namespace"]
                    in allowed
                ],
                "denied_namespaces": denied,
                "current_decisions": decisions,
                "claim": "PV3_TEST_ONLY_CURRENT_SOURCE_RESOLVED",
                "historical_links": len(report["links"]),
            }
        )
