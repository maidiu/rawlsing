from __future__ import annotations
from rawlsing_next.pre553_r5_parallel_compiler import ParallelConfig, QUEUE_CAPACITY, WORKER_COUNT

def test_parallel12_fixed_topology_and_queue_bound():
    cfg=ParallelConfig(); assert cfg.workers==WORKER_COUNT==12; assert cfg.queue_capacity<=QUEUE_CAPACITY

def test_parallel12_rejects_worker_count_drift():
    import pytest
    with pytest.raises(ValueError): ParallelConfig(workers=11)
    with pytest.raises(ValueError): ParallelConfig(workers=13)
