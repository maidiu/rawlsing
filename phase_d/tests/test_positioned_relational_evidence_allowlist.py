from pathlib import Path

from phase_d.code.compile_positioned_relational_evidence import scan_scope


def test_transport_and_context_surfaces_are_not_scanned(tmp_path: Path):
    (tmp_path / "core").mkdir()
    (tmp_path / "bridge").mkdir()
    (tmp_path / "determinicity").mkdir()
    (tmp_path / "clouds").mkdir()
    (tmp_path / "core" / "response_option_map.csv").write_text("question_impl.a,question_impl.b\n")
    (tmp_path / "bridge" / "v551_bridge_index.csv").write_text("question_impl.a,question_impl.b\n")
    (tmp_path / "determinicity" / "recursive_branch_nodes.csv").write_text("question_impl.a,question_impl.b\n")
    (tmp_path / "clouds" / "branch_relation_co_signature.csv").write_text("question_impl.a,question_impl.b\n")
    rows, _ = scan_scope(tmp_path)
    assert rows == []


def test_lawful_v550_surface_is_scanned(tmp_path: Path):
    surface = tmp_path / "clouds"
    surface.mkdir()
    (surface / "branch_relation_co_signature.csv").write_text(
        "question_impl.a,question_impl.b,n_unweighted\nquestion_impl.a,question_impl.b,12\n"
    )
    rows, scan = scan_scope(tmp_path)
    assert len(rows) == 1
    assert rows[0].impl_ids == {"question_impl.a", "question_impl.b"}
    assert scan["cloud_seen"] is True


def test_lawful_v550j_surface_is_scanned(tmp_path: Path):
    surface = tmp_path / "v550j" / "runs" / "x" / "joint_patterns"
    surface.mkdir(parents=True)
    (surface / "joint_response_pattern_index.csv").write_text(
        "question_impl.a,question_impl.b,joint_pattern_id\nquestion_impl.a,question_impl.b,JP1\n"
    )
    rows, _ = scan_scope(tmp_path)
    assert len(rows) == 1
