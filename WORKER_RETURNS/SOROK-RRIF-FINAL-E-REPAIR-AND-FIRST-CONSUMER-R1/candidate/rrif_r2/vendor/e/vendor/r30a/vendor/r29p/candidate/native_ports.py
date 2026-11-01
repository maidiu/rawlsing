"""R26V explicit native owner ports: fail closed while authority is unissued."""
from __future__ import annotations


class NativeAuthorityUnissued(Exception):
    def __init__(self, port: str, owner: str) -> None:
        super().__init__(f"NATIVE_AUTHORITY_UNISSUED:{port}")
        self.code = "NATIVE_AUTHORITY_UNISSUED"
        self.port = port
        self.owner = owner


class NativeHistoricalActorPorts:
    """No method here issues authority; each names the competent owner."""

    PORTS = {
        "adp007_actor_genesis": "ADP007 competent actor genesis owner",
        "adp010_opportunity_encounter": "ADP010 opportunity/encounter owner",
        "adp019_e1_admission": "ADP019 external admission court",
        "can008_rule_a": "CAN008 competent rule issuer",
        "can011_target_grant": "CAN011 separate target/grant owner",
        "adp016_memory_adp017_knowability": "ADP016/017 owner",
        "later_e2": "actual action owner / E2 performer",
        "c8_d1_d2_d3": "C8 protected trust custodian",
        "pyat_n11_n12": "Pyat original-world custodian (R53 STOP)",
        "c11_weld": "C11 native weld authority",
    }

    def _refuse(self, port: str):
        raise NativeAuthorityUnissued(port, self.PORTS[port])

    def admit_actor_genesis(self, *_a, **_k):
        self._refuse("adp007_actor_genesis")

    def admit_opportunity_encounter(self, *_a, **_k):
        self._refuse("adp010_opportunity_encounter")

    def admit_e1(self, *_a, **_k):
        self._refuse("adp019_e1_admission")

    def issue_can008_rule_a(self, *_a, **_k):
        self._refuse("can008_rule_a")

    def issue_can011_target_grant(self, *_a, **_k):
        self._refuse("can011_target_grant")

    def admit_memory_knowledge(self, *_a, **_k):
        self._refuse("adp016_memory_adp017_knowability")

    def admit_later_e2(self, *_a, **_k):
        self._refuse("later_e2")

    def admit_c8_trust(self, *_a, **_k):
        self._refuse("c8_d1_d2_d3")

    def admit_pyat_world(self, *_a, **_k):
        self._refuse("pyat_n11_n12")

    def admit_c11_weld(self, *_a, **_k):
        self._refuse("c11_weld")

    def probe_all(self) -> dict:
        out = {}
        for name in self.PORTS:
            method = getattr(self, "admit_" + name) if hasattr(self, "admit_" + name) else None
            if method is None:
                out[name] = "NATIVE_AUTHORITY_UNISSUED"
                continue
            try:
                method()
            except NativeAuthorityUnissued as exc:
                out[name] = exc.code
        return out
