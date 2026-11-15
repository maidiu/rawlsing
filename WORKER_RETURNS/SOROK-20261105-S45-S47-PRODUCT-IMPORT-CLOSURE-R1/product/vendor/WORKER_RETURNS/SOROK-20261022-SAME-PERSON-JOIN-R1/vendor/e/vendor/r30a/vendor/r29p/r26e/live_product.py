"""Live BP2P4J product with the qualified C12 verifier and N1 method bridge.

The existing BP2P4J product, real BP2 target/E2, BP4 C12/world/M6 and A0-A3 are
reused unchanged. Only the C12 verification read path is qualified and the N1
screen/port compiler is exposed as a pre-gate that cannot create durable state.
"""
from __future__ import annotations

import sys
from pathlib import Path

from bp2p4.product import JoinedProduct

from .c12_integrity import QualifiedC12Store


class LiveProduct(JoinedProduct):
    def __init__(self, root, *, artifacts, branch_id: str = "root", **kwargs) -> None:
        super().__init__(root, artifacts=artifacts, branch_id=branch_id, **kwargs)
        path = self.store.path
        self.store.close()
        self.store = QualifiedC12Store(path)

    def c12_verify(self) -> dict:
        return self.store.verify(self.branch_id)

    def observe_verified(self) -> dict:
        verify = self.c12_verify()
        if not verify["ok"]:
            return {"schema": "BP2P4J_R26E_OBSERVE@1", "status": "HELD",
                    "code": "C12_CHAIN_INVALID", "verify": verify,
                    "native": False, "grade": "TEST_ONLY_SOURCEFREE_R26E"}
        observed = self.observe()
        observed["c12_verify"] = verify
        return observed

    def n1_screen(self, case) -> dict:
        from n1_eligibility import screen
        return screen(case)

    def n1_compile(self, case, *, now: int) -> dict:
        import bp2_joined.ports as ports
        from n1_eligibility import compile_test_only_bp2_resources
        return compile_test_only_bp2_resources(case, ports, now=now)

    def production_registries(self) -> dict:
        import bp2_joined.ports as ports
        return ports.production_registries()
