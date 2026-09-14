from pathlib import Path

from rawlsing_next import rabochii_execution_protocol as protocol


def test_neutral_governed_court_execution_surface() -> None:
    assert Path(".github/workflows/rabochii-governed-bounded-court.yml").is_file()
    assert Path("rawlsing_next/rabochii_bounded_court.py").is_file()
    assert Path("rawlsing_next/rabochii_execution_protocol.py").is_file()
    assert protocol.COURT_SPEC_SCHEMA == "RABOCHII_COURT_SPEC@1.0.0"
