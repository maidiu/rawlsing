"""Explicit PV2I -> PV3 interface adapter. Original tests/oracle remain exact.

Legacy revocation snapshots are translated to a trusted TEST_ONLY owner control
withdrawal for those guards only; they are never an authority source in PV3.
Native label guard remains a raw failure, separately adjudicated HOLD; no rename.
"""

import deployment as D
import pv2_original_scope_register as OLD


class Adapter:
    def __getattr__(self, name):
        return getattr(OLD, name)

    def run_sourcefree_with_register(self, **kw):
        return record_api_call("run", D.api.run_sourcefree_with_register, (), kw)

    def validate_consumer_roles_against_declared(self, *args):
        from pv3_candidate import validate_consumer_roles_against_declared

        return record_api_call(
            "roles",
            lambda *a: (validate_consumer_roles_against_declared(*a) or {}),
            args,
            {},
        )

    def read_current_consumer_material(self, register, report):
        if register.fixture_use_grant.revoked:
            for ns in D.owner._state:
                D.owner.withdraw(
                    ns,
                    register.fixture_use_grant.revocation_reason
                    or "LEGACY_GUARD_OWNER_WITHDRAWAL",
                )
            return {
                "servable": False,
                "historical_links": len(report["links"]),
                "claim": "PV3_TRUSTED_TEST_OWNER_WITHDRAWAL",
            }
        try:
            return record_api_call(
                "current_read",
                D.api.read_current_consumer_material,
                (register, report),
                {},
            )
        except ValueError as e:
            return {"servable": False, "claim": str(e)}


V = Adapter()
EVENTS = []
ACTIVE_CASE = None


def record_api_call(name, fn, args, kw):
    event = {"case": ACTIVE_CASE, "operation": name}
    try:
        result = fn(*args, **kw)
        event.update(
            outcome="RETURNED",
            servable=result.get("servable"),
            links=len(result.get("links", [])),
            held=len(result.get("nonrunnable", [])),
            claim=result.get("claim"),
        )
        return result
    except ValueError as e:
        event.update(outcome="REFUSED", error_type=type(e).__name__, message=str(e))
        raise
    finally:
        EVENTS.append(event)


def adapt_common(C, R):
    C.R = R
    C.RT = R / "runtime_root"
    C.V = V
    original_numeric = C.make_numeric_fixture

    def numeric(root, row=2, new_value="1"):
        D.install_test_profile("R2_Y1" if row == 2 and new_value == "1" else "R1_Y0")
        return original_numeric(root, row=row, new_value=new_value)

    C.make_numeric_fixture = numeric
