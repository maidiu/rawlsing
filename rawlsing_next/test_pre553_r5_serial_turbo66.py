from rawlsing_next.pre553_r5_serial_turbo66 import BASELINE, TurboConfig


def test_authority_66_variants_are_single_process_and_baseline_root_is_explicit():
    assert BASELINE.temp_fsync is True
    assert BASELINE.temp_level == 6
    assert BASELINE.baseline_layout is True
    assert TurboConfig("V5", 65536, 64 * 2**20, 64, None, False, 16384, 16 * 2**20, 6).temp_level is None


def test_authority_66_final_relayout_is_explicit():
    v6 = TurboConfig("V6B", 65536, 64 * 2**20, 64, 1, False, 524288, 512 * 2**20, 6, False)
    assert v6.baseline_layout is False
    assert v6.shard_max_rows == 524288
    assert v6.final_level == 6
