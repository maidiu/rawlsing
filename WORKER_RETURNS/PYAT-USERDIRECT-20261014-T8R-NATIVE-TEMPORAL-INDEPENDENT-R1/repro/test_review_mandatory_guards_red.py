"""T8R mandatory negative acceptance oracles. Expected RED on pinned T8C.
Do not xfail or modify T8C to pass. This records integrity gaps, not a test flake.
"""
from copy import deepcopy
from fractions import Fraction as F
import pytest
import test_hq297_t8c as t

def test_REQUIRES_rejection_of_tampered_delta_with_stale_producer_digest():
    a,b=t.fixtures(); p=t.compare(a,b); changed=deepcopy(p)
    changed['delta_later_minus_earlier']=F(999)
    with pytest.raises(t.Refusal):
        t.consume(changed)

def test_REQUIRES_rejection_of_tampered_native_zero_with_stale_producer_digest():
    a,b=t.fixtures(); p=t.compare(a,b); changed=deepcopy(p)
    changed['later']['categories']['0']=F(999)
    with pytest.raises(t.Refusal):
        t.consume(changed)

def test_REQUIRES_typed_refusal_on_invalid_asof():
    a,b=t.fixtures()
    with pytest.raises(t.Refusal):
        t.compare(a,b,asof='not-a-date')
