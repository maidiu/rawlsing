from __future__ import annotations
import hashlib
from rawlsing_next.pre553_r5_parallel_compiler import _worker_sort
from rawlsing_next.pre553_r5_model import R5CanonicalRow

def _row(i): return R5CanonicalRow("r","f",f"{i}",hashlib.sha256(str(i).encode()).hexdigest(),{"i":i})

def test_worker_local_sorted_wire_is_scheduler_independent():
    a=_worker_sort(tuple(_row(i) for i in range(20))); b=_worker_sort(tuple(reversed([_row(i) for i in range(20)])))
    assert a==b
