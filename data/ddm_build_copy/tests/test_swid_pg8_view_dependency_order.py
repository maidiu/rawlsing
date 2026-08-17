from __future__ import annotations

from data.ddm_build_copy import apply_postgres_facet_ready_substrate as db


class _Cursor:
    def __init__(self) -> None:
        self.statements: list[str] = []
        self.last_sql = ""
        self.closed = False

    def execute(self, sql, params=None):
        self.last_sql = str(sql)
        self.statements.append(self.last_sql.strip())

    def fetchall(self):
        if "FROM information_schema.tables" in self.last_sql:
            return [("respondentsDemoSmoke",)]
        if "FROM information_schema.columns" in self.last_sql:
            return [
                ("respondent_id",),
                ("source_family",),
                ("wave",),
                ("country_code",),
                ("survey_year",),
                ("sex",),
                ("age",),
                ("education_level",),
                ("income_level",),
                ("income_source_note",),
                ("survey_weight",),
                ("survey_weight_source_var",),
                ("urban_rural",),
                ("religion_label",),
                ("marital",),
                ("employment",),
                ("class_level",),
                ("household_size",),
                ("language",),
                ("region",),
                ("ethnicity",),
            ]
        return []

    def close(self):
        self.closed = True


class _Connection:
    def __init__(self) -> None:
        self.cursor_value = _Cursor()
        self.commits = 0

    def cursor(self):
        return self.cursor_value

    def commit(self):
        self.commits += 1


def test_view_rebuild_drops_known_dependents_in_dependency_order_without_cascade():
    conn = _Connection()

    db.create_respondent_position_view(conn)

    assert conn.cursor_value.statements[:3] == [
        "DROP VIEW IF EXISTS v_ddm_response_long_facet_ready_authority",
        "DROP VIEW IF EXISTS v_ddm_response_long_facet_ready",
        "DROP VIEW IF EXISTS respondent_position_fact",
    ]
    assert all("CASCADE" not in statement.upper() for statement in conn.cursor_value.statements[:3])
    assert conn.commits == 1
    assert conn.cursor_value.closed
