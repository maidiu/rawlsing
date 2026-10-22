def test_r2_mmap_between_batch_change_cannot_release_altered_c11_i03_under_old_identity(
    tmp_path, monkeypatch
):
    path = _write_source(tmp_path / "r2-mmap.sav", "sav")
    alternate = _write_source(tmp_path / "r2-mmap-alt.sav", "sav", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    baseline = _observe(path, "sav", expected_sha)
    assert baseline["ok"] is True
    baseline_facts = baseline["facts"]
    assert baseline_facts["i03_y_cells"] == {"0": 1, "1": 1}

    incidence = _decode(path, "sav", expected_sha)
    mapped = None
    try:
        fixture = _fixture("r04byte-r2-mmap")
        projection = _bind_projection(fixture["projection"], incidence)
        mapped = mmap.mmap(incidence._source_snapshot.fd, 0, access=mmap.ACCESS_WRITE)
        alternate_bytes = alternate.read_bytes()
        original_chunks = pyreadstat.read_file_in_chunks

        def hostile_chunks(reader, source, *args, **kwargs):
            iterator = original_chunks(reader, source, *args, **kwargs)
            first = next(iterator)
            mapped[: len(alternate_bytes)] = alternate_bytes
            if len(alternate_bytes) < len(mapped):
                mapped[len(alternate_bytes):] = b"\x00" * (len(mapped) - len(alternate_bytes))
            yield first
            yield from iterator

        monkeypatch.setattr(pyreadstat, "read_file_in_chunks", hostile_chunks)
        release = build_validated_source_backed_c11_release(incidence, projection, batch_size=4)
        source = {
            **fixture,
            "source_sha": incidence.source_sha256,
            "projection": projection,
            "repo": C11Repository((release,)),
            "release_ref": release.release_ref,
        }
        query_authority = _query_authority("r04byte-r2-mmap")
        predicate = _branch_predicate(source, query_authority)
        query = _query(source, query_authority, predicate, ("Y",), tag="r04byte-r2-mmap")
        result = execute_empirical_query(
            repository=source["repo"],
            query=query,
            predicate=predicate,
            authority_registry=AuthorityRegistry((*fixture["authorities"], query_authority)),
            release_refs=(release.release_ref,),
        )
        fact = result.facts[0]
        assert release.source_artifact_ref.content_hash == expected_sha
        assert fact.typed_state == baseline_facts["i03_typed_state"]
        assert fact.raw_denominator_support == baseline_facts["i03_raw_denominator_support"]
        assert {key: value["raw_numerator_support"] for key, value in _cell_map(fact).items()} == (
            baseline_facts["i03_y_cells"]
        )
        assert fact.ref.content_hash == baseline_facts["i03_fact_ref"]
    finally:
        if mapped is not None:
            mapped.close()
        incidence.close()
