"""Deployment-only TEST_ONLY fixture principal; never accepts request work/register.

The read client receives a resolver closure, not the control capability. Files are
pinned installation inputs. This models separate fixture custody within a trusted
Python host, not sandboxing malicious code or an actual survey permission issuer.
"""

from pathlib import Path
from dataclasses import replace, dataclass
import hashlib, json, os
import pv2_original_scope_register as OLD
from rawlsing_next import pre553_original_identity_v2k_successor_candidate as K

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "original_six_consumers.json": "03ceb8fdb1f38cd68566076214f1a9c5663762a5ea9db6b3311aa2beb7f38210",
    "expected.json": "150611b89e93c5c14658207fd7b30592eaa67450828ce3422123e7768490a087",
    "register.json": "aa0f5b573fbba3261340210fed7457832073ccdb6b216b136d7143a813a2ba28",
    "independent_oracle.json": "321681bb0918e4119e3053aef8f0a6cb0d9db434eadc0a3225f897a686a55f79",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def pinned(name):
    b = (ROOT / "authority" / name).read_bytes()
    if hashlib.sha256(b).hexdigest() != PINS[name]:
        raise ValueError("FIXTURE_INSTALLATION_PIN_MISMATCH:" + name)
    return json.loads(b)


def _literal_source_hash(row, value):
    # Explicit source fixture rows in physical decoder order; no request helper.
    rows = [
        ["1", "1", "AB", "XY", "A", 2],
        ["0", "0", "BA", "XZ", "B", 1],
        ["1", "1", "AB", "XY", "A", 3],
    ]
    rows[row - 1][1] = value
    cells = [
        (i, k, v)
        for i, r in enumerate(rows, 1)
        for k, v in zip(("X", "Y", "O", "R", "G", "W"), r)
    ]
    return hashlib.sha256(json.dumps(cells, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class FixtureInstallation:
    identity: str
    profile: str
    register_root: str
    expected_json: str
    expected_root: str
    register: OLD.PrecommittedOriginalRegister
    source_editions: tuple
    baseline_links_json: str


@dataclass(frozen=True)
class CurrentDecision:
    namespace: str
    edition: str
    clock: int
    asof: int
    withdrawn: bool = False
    reason: str | None = None
    grant: str = "TEST_ONLY_FIXTURE_GRANT"
    issuer: str = "PV3_SEPARATELY_INSTALLED_FIXTURE_OWNER"
    ceiling: tuple = ("SOURCE_FREE_DEV",)


class FixtureOwnerControl:
    """Only the trusted composition/test harness holds this capability."""

    def __init__(self, profile="BASELINE", *, policy_path=None, provision=False):
        baseline = pinned("expected.json")
        pinned("independent_oracle.json")
        register = OLD.author_sourcefree_original_scope_register()
        frozen = pinned("register.json")
        if register.binding() != frozen["register_binding"]:
            raise ValueError("FIXTURE_REGISTER_INSTALL_MISMATCH")
        records = baseline["records"]
        if profile != "BASELINE":
            if profile not in ("R2_Y1", "R1_Y0"):
                raise ValueError("UNINSTALLED_FIXTURE_PROFILE")
            row, value = (2, "1") if profile == "R2_Y1" else (1, "0")
            h = _literal_source_hash(row, value)
            register = replace(
                register,
                source_native_inventory=tuple(
                    (
                        replace(c, raw_value=value)
                        if c.respondent_namespace == "PV2-ADULT-A"
                        and c.respondent_key == "R" + str(row)
                        and c.item_short_name == "Y"
                        else c
                    )
                    for c in register.source_native_inventory
                ),
            )
            for rec in records:
                if rec["original"]["respondent_namespace"] == "PV2-ADULT-A":
                    rec["original"]["source_release_ref"]["content_hash"] = h
                    rec["legacy"]["source_identity"] = h
                    # Reconstruct the static identity without trusting a supplied work key.
                    work = K.OriginalExpectedWork(
                        K.OriginalIdentity.from_preimage(rec["original"]),
                        K.legacy_from_preimage(rec["legacy"]),
                        *[
                            K.ExactRef(**rec[k])
                            for k in (
                                "original_operation_scope_ref",
                                "original_U_ref",
                                "independent_E_ref",
                                "independent_custody_ref",
                            )
                        ]
                    )
                    rec["expected_work_key"] = work.key
        expected = K.FrozenOriginalExpected.from_records(
            tuple(K.OriginalExpectedWork.from_record(r) for r in records),
            input_origin=K.ORIGIN,
        )
        editions = tuple(
            sorted(
                {
                    (
                        r["original"]["respondent_namespace"],
                        r["original"]["source_release_ref"]["content_hash"],
                    )
                    for r in records
                }
            )
        )
        self.installation = FixtureInstallation(
            "PV3_TEST_ONLY_OWNER@1",
            profile,
            register.committed_root,
            expected.payload_json,
            expected.payload_sha256,
            register,
            editions,
            canonical(pinned("original_six_consumers.json")),
        )
        self._state = {ns: CurrentDecision(ns, e, 1, 1) for ns, e in editions}
        self._policy_path = Path(policy_path) if policy_path is not None else None
        if self._policy_path is not None:
            if self._policy_path.exists():
                self._load_policy()
            elif provision:
                self._save_policy()
            else:
                raise ValueError("CURRENT_OWNER_SERVICE_UNAVAILABLE")
        self._accepted = {}
        self.resolutions = []

    def _load_policy(self):
        if self._policy_path is None:
            return
        try:
            payload = json.loads(self._policy_path.read_text())
        except (OSError, ValueError) as e:
            raise ValueError("CURRENT_OWNER_SERVICE_UNAVAILABLE") from e
        if (
            payload["owner"] != self.installation.identity
            or payload["expected_root"] != self.installation.expected_root
        ):
            raise ValueError("FOREIGN_CURRENT_OWNER_POLICY")
        state = {}
        for ns, row in payload["decisions"].items():
            row = dict(row)
            row["ceiling"] = tuple(row["ceiling"])
            d = CurrentDecision(**row)
            if (
                d.namespace != ns
                or ns not in dict(self.installation.source_editions)
                or d.issuer != "PV3_SEPARATELY_INSTALLED_FIXTURE_OWNER"
                or d.grant != "TEST_ONLY_FIXTURE_GRANT"
                or d.ceiling != ("SOURCE_FREE_DEV",)
                or d.clock < 1
                or d.asof < 1
            ):
                raise ValueError("CURRENT_OWNER_POLICY_NOT_AUTHORIZED")
            state[ns] = d
        if set(state) != dict(self.installation.source_editions).keys():
            raise ValueError("CURRENT_OWNER_POLICY_SOURCE_ANTI_JOIN")
        self._state = state

    def _save_policy(self):
        if self._policy_path is None:
            return
        self._policy_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "owner": self.installation.identity,
            "expected_root": self.installation.expected_root,
            "decisions": {ns: d.__dict__ for ns, d in self._state.items()},
        }
        temporary = self._policy_path.with_name(
            self._policy_path.name + "." + str(os.getpid()) + ".tmp"
        )
        with temporary.open("x") as f:
            os.chmod(temporary, 0o600)
            f.write(canonical(payload) + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, self._policy_path)
        directory_fd = os.open(self._policy_path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)

    def withdraw(self, namespace, reason="OWNER_WITHDRAWAL"):
        self._load_policy()
        d = self._state[namespace]
        self._state[namespace] = replace(
            d, clock=d.clock + 1, asof=d.asof + 1, withdrawn=True, reason=reason
        )
        self._save_policy()

    def advance(self, namespace, *, edition=None):
        self._load_policy()
        d = self._state[namespace]
        self._state[namespace] = replace(
            d, clock=d.clock + 1, asof=d.asof + 1, edition=edition or d.edition
        )
        self._save_policy()

    def _resolve(self, namespace):
        self._load_policy()
        d = self._state[namespace]
        self.resolutions.append((namespace, d.clock))
        return d

    def _attest(self, report):
        # Called only by the deployment's accepted execution path, after source,
        # journal/receipt and actual producer material have been verified.
        material = canonical(
            {
                key: report[key]
                for key in (
                    "links",
                    "nonrunnable",
                    "original_expected_digest",
                    "pv3_receipt_proofs",
                    "pv2_register",
                )
            }
        )
        digest = hashlib.sha256(material.encode()).hexdigest()
        self._accepted[digest] = material
        return {
            "owner": self.installation.identity,
            "profile": self.installation.profile,
            "expected_root": self.installation.expected_root,
            "material_sha256": digest,
        }

    def client(self):
        return FixtureOwnerReadClient(
            self.installation, self._resolve, lambda d: self._accepted.get(d)
        )


@dataclass(frozen=True)
class FixtureOwnerReadClient:
    installation: FixtureInstallation
    _resolve: object
    _custody: object

    def resolve(self, namespace):
        return self._resolve(namespace)

    def verify_history(self, report):
        seal = report.get("pv3_custody", {})
        if (
            seal.get("owner") != self.installation.identity
            or seal.get("expected_root") != self.installation.expected_root
        ):
            raise ValueError("FOREIGN_FIXTURE_CUSTODY")
        material = canonical(
            {
                key: report[key]
                for key in (
                    "links",
                    "nonrunnable",
                    "original_expected_digest",
                    "pv3_receipt_proofs",
                    "pv2_register",
                )
            }
        )
        d = hashlib.sha256(material.encode()).hexdigest()
        if seal.get("material_sha256") != d:
            raise ValueError("CONSUMER_CUSTODY_CONTENT_MISMATCH")
        if self._custody(d) != material:
            raise ValueError("OFFLINE_FACT_RESTORATION_HOLD")
