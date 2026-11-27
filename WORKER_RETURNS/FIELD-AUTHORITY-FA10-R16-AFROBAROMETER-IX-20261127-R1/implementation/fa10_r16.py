"""Versioned FA10 orchestration sidecar. R3 remains the primary validator and reader."""
from contextlib import contextmanager
from copy import deepcopy
import csv
import fcntl
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "frozen"))
import fa10

read = fa10.r9.read
save = fa10.r9.save
digest = fa10.sha
SCHEMA = Draft202012Validator(read(ROOT / "FEEDBACK.schema.json"))
BLOCKING = {"REQUIRED", "RULE_MEMBERSHIP", "LINEAGE"}
OPS = {
    "ENRICH": {"ADD", "PATCH"}, "CORRECT": {"PATCH"}, "REOPEN": {"RECONSIDER"},
    "RECONSTITUTE": {"PATCH", "RECONSIDER"}, "RETRIEVE": {"RETRIEVE"},
    "PRESERVE_OVERFLOW": {"CONSERVE"}, "METHOD_PROPOSAL": {"PROPOSE_METHOD"},
    "AUTHORITY_HOLD": {"HOLD"},
}
METHOD_FIELDS = {"input", "transformation", "output", "stop", "positive", "negative",
                 "nontransfer", "reader", "matched_trial"}


class Refused(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Refused(message)


def reference(record):
    return {key: record[key] for key in ("record_id", "revision_sha256", "scope", "kind")}


def verify_rows(base, edition, rows):
    fa10.r9.check_packet(base)
    require(base["source"] == edition, "wrong exact source")
    for key, row in {**base["selected"], **base["context"]}.items():
        require(key in rows and rows[key] == row["source_metadata"]
                and digest(rows[key]) == row["row_sha256"], "wrong literal row or row digest")


def verify_wvs(archive):
    csv.field_size_limit(10**7)
    base = read(ROOT / "wvs/O_PACKET.json")
    response = read(ROOT / "wvs/O_RESPONSE.json")
    ledger = read(ROOT / "wvs/O_LEDGER.json")
    coverage = read(ROOT / "wvs/O_COVERAGE.json")
    edition, rows = fa10.r9.source(archive, "World Values Survey Wave 7 codebook.csv")
    verify_rows(base["source_packet"], edition, rows)
    require(fa10.validate(base, response), "inherited primary response refused")
    require(set(rows) == set(ledger["records"]) == set(coverage["all_ids"]), "WVS census mismatch")
    require(len(rows) == 613 and len(ledger["rules"]) == 148, "WVS source or rule count")
    require(sum(bool(r.get("inherited_candidates")) for r in ledger["records"].values()) == 324,
            "WVS prior candidate identity count")
    splits = {"all": "all", "substantive": "substantive", "special": "special"}
    for field, record in ledger["records"].items():
        require(record["rule"] in ledger["rules"] and record["target"] == rows[field]["question_text"]
                and record["source_row_sha256"] == digest(rows[field]), "WVS row or rule mismatch")
        for key, source_key in splits.items():
            value = rows[field]["response_options_" + source_key].encode()
            require(record["literal_domain_ref"][key + "_domain_sha256"] == fa10.r9.sha(value),
                    "WVS domain loss")
    return edition, rows, ledger


class Sidecar:
    """One locked state transaction for every mutation, with immutable prior versions."""

    def __init__(self, path, edition, rows, scopes, *, limit=16):
        self.path = Path(path)
        self.edition = edition
        self.rows = rows
        self.scopes = frozenset(scopes)
        self.limit = limit
        with self.edit():
            pass

    @contextmanager
    def edit(self):
        with self.path.with_suffix(".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            prior = read(self.path) if self.path.exists() else {
                "edition": self.edition, "limit": self.limit,
                "row_digests_sha256": digest({key: digest(value) for key, value in self.rows.items()}),
                "active": {}, "versions": {}, "dispatch": {}, "events": {}, "inbox": {},
                "pending": {}, "fingerprints": {}, "disputes": [], "reviews": {}, "scope": sorted(self.scopes),
            }
            require(prior["edition"] == self.edition and prior["limit"] == self.limit
                    and prior["scope"] == sorted(self.scopes)
                    and prior["row_digests_sha256"] == digest({key: digest(value) for key, value in self.rows.items()}),
                    "journal source/cut changed")
            yield prior
            save(self.path, prior)

    def register(self, packet, response, role, scope):
        """Called by the controller after independent process dispatch, never by a model."""
        fa10.r9.check_packet(packet)
        require(scope in self.scopes and packet["role"] == role, "wrong dispatched role/scope")
        if "source_packet" in packet:
            verify_rows(packet["source_packet"], self.edition, self.rows)
        else:
            require(packet.get("source") == self.edition, "dispatch source mismatch")
        if role != "J" and "response_contract" in packet:
            require(fa10.validate(packet, response), "primary role rejected")
        role_receipt = {"role": role, "scope": scope, "packet_sha256": packet["packet_sha256"],
                        "response_sha256": digest(response)}
        with self.edit() as s:
            key = digest(role_receipt)
            prior = s["dispatch"].setdefault(key, role_receipt)
            require(prior == role_receipt, "dispatch identity conflict")
            if role == "J":
                require(response.get("packet_sha256") == packet["packet_sha256"]
                        and isinstance(response.get("decisions"), dict), "review not packet-bound")
                key_decisions = set(response["decisions"])
                require(key_decisions == set(packet["events"]), "review disposition mismatch")
                s["reviews"][key] = {"decisions": response["decisions"], "events": packet["events"]}
        return role_receipt

    def _known(self, state, ref, *, active=False):
        record = state["versions"].get(ref["revision_sha256"])
        require(record and reference(record) == ref, "unrecognized or incompatible exact revision")
        if active:
            require(state["active"].get(ref["record_id"]) == ref["revision_sha256"], "stale revision")
        return record

    def _record(self, state, rid, scope, owner, kind, content, deps, predecessor=None, evidence=None):
        require(scope in self.scopes, "record outside scope")
        if kind == "ANSWER":
            _, field, code = rid.rsplit(":", 2)
            require(field in self.rows and code in fa10.codes({"source_metadata":self.rows[field]}),
                    "answer record uses nonexistent field or code")
        for dependency in deps:
            target = self._known(state, dependency["ref"], active=dependency["kind"] in BLOCKING)
            if dependency["kind"] == "LINEAGE":
                frontier = [target]
                while frontier:
                    prior = frontier.pop()
                    require(prior["record_id"] != rid, "lineage cycle")
                    frontier.extend(self._known(state, d["ref"]) for d in prior["deps"]
                                    if d["kind"] == "LINEAGE")
        entry = {"record_id": rid, "scope": scope, "owner": owner, "kind": kind,
                 "content": content, "deps": deps, "predecessor": predecessor, "evidence": evidence}
        entry["revision_sha256"] = digest(entry)
        state["versions"].setdefault(entry["revision_sha256"], entry)
        state["active"][rid] = entry["revision_sha256"]
        return reference(entry)

    def seed(self, rid, scope, owner, kind, content, deps=()):
        with self.edit() as state:
            require(rid not in state["active"], "existing record")
            return self._record(state, rid, scope, owner, kind, content, list(deps))

    def _evidence(self, evidence, kind):
        require(evidence["source_sha256"] == self.edition["sha256"], "wrong source identity")
        field = evidence["locator"]
        row = self.rows.get(field)
        e_kind = evidence["evidence_kind"]
        require(row is not None, "unknown field")
        if e_kind == "LOCATOR_ONLY":
            require(kind == "RETRIEVE" and evidence["row_sha256"] is None, "locator is not literal evidence")
        elif e_kind == "MISSING_SOURCE":
            require(kind == "AUTHORITY_HOLD" and evidence["row_sha256"] is None, "missing evidence is not a proof")
        else:
            require(e_kind in {"LITERAL_ROW", "VERIFIED_CONSERVATION", "METHOD_EVIDENCE"}
                    and evidence["row_sha256"] == digest(row), "unverified evidence or wrong row digest")
            q = evidence["quote_or_fact"]
            require(q.strip() and any(q in row[k] for k in ("question_text", "response_options_all")),
                    "unsupported literal")

    def submit(self, event):
        SCHEMA.validate(event)
        eid = event["event_id"]
        with self.edit() as state:
            prior = state["events"].get(eid)
            if prior:
                if prior["event"] == event:
                    return "DUPLICATE"
                state["disputes"].append({"reason": "event ID conflict", "proposal": event})
                return "DISPUTED"
            entry = {"event": event, "status": "REJECTED"}
            state["events"][eid] = entry
            try:
                require(event["requested_operation"] in OPS[event["kind"]], "wrong requested operation")
                require(state["dispatch"].get(digest(event["origin"])) == event["origin"], "wrong role, packet or response")
                for ref in event["targets"] + event["known_affected"] + [
                        d["ref"] for d in event["read_dependencies"]]:
                    self._known(state, ref, active=True)
                    require(ref["scope"] == event["origin"]["scope"], "wrong target scope")
                for evidence in event["evidence"]:
                    self._evidence(evidence, event["kind"])
                if event["kind"] == "METHOD_PROPOSAL":
                    method = json.loads(event["minimal_delta_or_request"])
                    require(set(method) == METHOD_FIELDS and all(fa10.r9.substantive(v) for v in method.values()),
                            "incomplete matched method proposal")
                material = {k: event[k] for k in ("kind", "targets", "new_scope", "minimal_delta_or_request")}
                fp = digest(material)
                if fp in state["fingerprints"]:
                    entry["status"] = "DUPLICATE_CHANGE"
                elif len(state["fingerprints"]) >= self.limit:
                    entry["status"] = "HOLD_BUDGET"
                else:
                    state["fingerprints"][fp] = eid
                    entry["status"] = {
                        "AUTHORITY_HOLD": "HELD", "PRESERVE_OVERFLOW": "SUPPLEMENTARY",
                        "METHOD_PROPOSAL": "METHOD_CANDIDATE",
                    }.get(event["kind"], "ROUTED")
                owners = sorted({self._known(state, t)["owner"] for t in event["targets"]})
                state["inbox"][eid] = owners
            except (Refused, TypeError, KeyError, ValueError) as error:
                entry["error"] = str(error)
            return entry["status"]

    def reveal(self, eid, archive, member, locator):
        with self.edit() as state:
            event = state["events"][eid]["event"]
            require(event["kind"] == "RETRIEVE" and state["events"][eid]["status"] == "ROUTED", "no retrieval route")
            edition, actual = fa10.r9.source(archive, member)
            require(edition == self.edition, "retrieval edition drift")
            revealed = {}
            for evidence in event["evidence"]:
                field = evidence["locator"]
                row = actual[field]
                require(digest(row) == locator[field]["row_sha256"] and row == self.rows[field],
                        "distal row drift")
                revealed[field] = {"source_metadata": row, "row_sha256": digest(row)}
            state["events"][eid]["reveal"] = revealed
            state["events"][eid]["status"] = "RETRIEVED_RECONSIDER"
            return deepcopy(revealed)

    def adjudicate(self, eid, reviewer, *, owner, patch=None):
        with self.edit() as state:
            entry = state["events"][eid]
            event = entry["event"]
            review = state["reviews"].get(digest(reviewer))
            require(review and state["dispatch"].get(digest(reviewer)) == reviewer
                    and reviewer["role"] == "J" and reviewer["scope"] == event["origin"]["scope"]
                    and reviewer["packet_sha256"] != event["origin"]["packet_sha256"]
                    and review["events"].get(eid) == digest(event), "distinct source-bound review required")
            decision = review["decisions"][eid]
            require(fa10.r9.substantive(decision.get("reason")), "review lacks exact rationale")
            require(entry["status"] == "ROUTED", "event is not pending review")
            entry["review"] = {"reviewer": reviewer, "decision": decision}
            if decision["decision"] in {"REJECT", "HOLD"}:
                entry["status"] = decision["decision"]
                return entry["status"]
            require(decision["decision"] == "APPLY" and len(event["targets"]) == 1, "no exact reviewed patch")
            target = event["targets"][0]
            old = self._known(state, target)
            if state["active"][target["record_id"]] != target["revision_sha256"]:
                entry.update(status="DISPUTED", variant=patch)
                return "DISPUTED"
            require(owner == old["owner"] and isinstance(patch, dict) and len(patch) == 1
                    and set(patch) <= {"note", "meaning", "exception"}, "non-minimal or wrong owner patch")
            require(decision.get("patch_sha256") == digest(patch), "patch differs from reviewed bytes")
            require(set(patch) <= set(old["content"]), "patch changes content schema")
            new = self._record(state, old["record_id"], old["scope"], owner, old["kind"],
                               {**old["content"], **patch}, old["deps"], old["revision_sha256"],
                               {"event_id": eid, "review": reviewer})
            affected, queue = set(), [old["revision_sha256"]]
            while queue:
                obsolete = queue.pop()
                for rid, sha in state["active"].items():
                    if rid == old["record_id"] or rid in affected:
                        continue
                    dependent = state["versions"][sha]
                    if any(d["kind"] in BLOCKING and d["ref"]["revision_sha256"] == obsolete for d in dependent["deps"]):
                        affected.add(rid)
                        queue.append(sha)
            if event["dependency_scope"] == "CONSERVATIVE_SCOPE_REQUIRED":
                affected.update(rid for rid, sha in state["active"].items() if rid != old["record_id"]
                                and state["versions"][sha]["scope"] == old["scope"])
            for rid in affected:
                state["pending"].setdefault(rid, {})[eid] = {"parent_before": target, "parent_after": new}
            entry.update(status="APPLIED_CANDIDATE", current=new, affected=sorted(affected))
            return new

    def reconsider(self, rid, *, owner, decision, rationale, patch=None):
        require(decision in {"KEEP", "REVISE", "WITHDRAW", "HOLD"} and fa10.r9.substantive(rationale), "invalid disposition")
        with self.edit() as state:
            pending = state["pending"][rid]
            prior = state["versions"][state["active"][rid]]
            require(prior["owner"] == owner, "wrong affected owner")
            if decision == "REVISE":
                require(isinstance(patch, dict) and set(patch) <= {"note", "meaning", "exception"}
                        and set(patch) <= set(prior["content"]), "invalid reevaluation edit")
            else:
                require(patch is None, "only a revise decision can change content")
            required_parents = {d["ref"]["record_id"] for d in prior["deps"] if d["kind"] in BLOCKING}
            require(not (required_parents & state["pending"].keys()),
                    "upstream dependent must be reconsidered first")
            deps = [{"kind": d["kind"], "ref": reference(state["versions"][state["active"][d["ref"]["record_id"]]])}
                    if d["kind"] in BLOCKING else d for d in prior["deps"]]
            value = {**prior["content"], **(patch or {}), "reevaluation": decision}
            new = self._record(state, rid, prior["scope"], owner, prior["kind"], value, deps,
                               prior["revision_sha256"], {"pending": pending, "rationale": rationale})
            del state["pending"][rid]
            return new

    def retrieve(self, rid, *, revision=None):
        state = read(self.path)
        sha = revision or state["active"][rid]
        record = state["versions"][sha]
        require(record["record_id"] == rid and digest({k: v for k,v in record.items() if k != "revision_sha256"}) == sha,
                "stored record identity mismatch")
        return {"record": record, "pending": state["pending"].get(rid, {})}

    def reproject(self, base, delta, target, *, bindings, complete_domains=True):
        """Apply reviewed text to an existing R9 delta. Source domains remain exact."""
        result = deepcopy(delta)
        for (field, code), rid in bindings.items():
            data = self.retrieve(rid)
            record = data["record"]
            require(not data["pending"] and record["kind"] in {"ANSWER", "FIELD"}
                    and record["content"].get("reevaluation") not in {"HOLD", "WITHDRAW"}, "unresolved active record")
            if code is None:
                require(rid.rsplit(":",1)[-1] == field and record["kind"] == "FIELD", "field projection identity mismatch")
                result["items"][field]["note"] = record["content"]["note"]
            else:
                require(record["kind"]=="ANSWER" and rid.rsplit(":",2)[-2:]==[field,str(code)]
                        and str(code) in fa10.codes(base["selected"][field]), "wrong exact answer binding")
                result["items"][field]["answer_notes"][str(code)] = record["content"]["meaning"]
        fa10.r9.validate(base, result)
        if complete_domains:
            verify_projection(base, result)
        require(all(set(result["items"][field].get("answer_notes",{})) >= set(item.get("answer_notes",{}))
                    for field,item in delta["items"].items()), "projection dropped an inherited answer note")
        save(target, result)
        persisted = read(target)
        if complete_domains:
            verify_projection(base, persisted)
        require(persisted == result, "persisted projection mismatch")
        return persisted


def verify_projection(base, delta):
    fa10.r9.validate(base, delta)
    for field, entry in base["selected"].items():
        require(set(delta["items"][field]["answer_notes"]) == fa10.codes(entry), "projection lost exact code")
