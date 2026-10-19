import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from edge import consume_selected_release


def test_consumer_depends_on_selected_release():
    release = {'value': 3}
    assert consume_selected_release(release) == 3
