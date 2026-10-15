"""SC0I independent hostiles against SC0F repaired port. Read-only candidate."""
import sys
from pathlib import Path
sys.path.insert(0, "/tmp/wg0p/.sc0i_tmp")
sys.path.insert(0, "/tmp/wg0p")

import pytest
from sc0f import producer_bridge as pbmod
from sc0f import adapter as admod


def test_h01_n10e_c1_imported_never_invoked():
    """Frozen #2: _compute_via_n10e_c1 imports but never calls real functions."""
    import sc0f.producer_bridge as pb
    calls = {"n10e": 0, "c1": 0, "consumer": 0}
    try:
        import rawlsing_next.pre553_empirical_possibility_provider as n10e
        real_n10e = n10e.provide_empirical_possibility_slice
        def counted_n10e(*a, **k):
            calls["n10e"] += 1
            return real_n10e(*a, **k)
        n10e.provide_empirical_possibility_slice = counted_n10e
        patched = True
    except Exception:
        patched = False
    bridge = pb.SC0FProducerBridge(mode="N10E_C1_IF_AVAILABLE")
    sel = {"world": {"source_ref": "s", "source_release_ref": "r"}}
    dem = {"scope": "fx:scope:town2008"}
    try:
        bridge._compute_via_n10e_c1(sel, dem)
    except Exception:
        pass
    finally:
        if patched:
            n10e.provide_empirical_possibility_slice = real_n10e
    assert calls["n10e"] == 0, "real N10E function was actually invoked"
    names = [t.get("function", "") for t in bridge.tracer.calls]
    assert any("import" in str(t.get("detail", "")).lower() or "N10E" in n for t, n in
               zip(bridge.tracer.calls, names))


def test_h02_import_trace_uses_sha256_of_imported():
    import hashlib
    bridge = pbmod.SC0FProducerBridge(mode="N10E_C1_IF_AVAILABLE")
    try:
        bridge._compute_via_n10e_c1({"world": {}}, {"scope": "x"})
    except Exception:
        pass
    digests = {t["result_digest"] for t in bridge.tracer.calls}
    assert hashlib.sha256(b"imported").hexdigest() in digests


def test_h03_forged_warrant_accepted_after_self_registration():
    """Frozen #3: attacker self-registers then passes. Must be RED."""
    admod.clear_issuer_registry()
    forged = {"grant_id": "FORGED-1", "issuer": "ATTACKER",
              "scope": "s|r", "binds": {"target": "T", "reverse_target": "T",
              "risk_set": "R", "denominator": 60, "operation": "ROLE_REVERSAL_CONDITIONAL_QUERY"}}
    admod.register_issuer_warrant(forged)
    from sc0f.adapter import SC0FTwoContractAdapter
    ad = SC0FTwoContractAdapter.__new__(SC0FTwoContractAdapter)
    sel = {"world": {"source_ref": "s", "source_release_ref": "r"}}
    poss = {"risk_set": "R", "support": {"denominator": 60}}
    out = ad.request_role_reversal(sel, poss, dict(forged))
    assert out["state"] == "REVERSAL_PERMITTED_UNDER_REGISTERED_GRANT"


def test_h04_test06_options_nonempty_not_numeric():
    """Frozen #4: test_06 asserts options nonempty, not 50/10 values."""
    import inspect
    from pathlib import Path as _P
    src = _P("/tmp/wg0p/.sc0i_tmp/tests/test_sc0f_repair.py").read_text()
    assert "50" in src and "10" in src
    assert 'nonempty' in src.lower() or 'options' in src


def test_h05_selection_state_defaults_complete():
    from sc0f.adapter import SC0FTwoContractAdapter
    import inspect
    src = inspect.getsource(SC0FTwoContractAdapter.run)
    assert 'selection.get("selection_state", "COMPLETE")' in src or \
           "selection.get('selection_state', 'COMPLETE')" in src


def test_h06_fx_scope_allowlist_unconditional():
    from sc0f.adapter import SC0FTwoContractAdapter
    import inspect
    src = inspect.getsource(SC0FTwoContractAdapter.run)
    assert "fx:scope:town2008" in src


def test_h07_earlier_evidence_presence_not_issuer():
    from sc0f.adapter import SC0FTwoContractAdapter
    import inspect
    src = inspect.getsource(SC0FTwoContractAdapter.run)
    assert "earlier_knowledge_evidence_ref" in src
    assert "if not earlier:" in src
