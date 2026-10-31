"""
Create wvs_analysis schema and tables for Phase 1A (MI) and Phase 1B.
Run once when public.respondents, public.responses, public.variables exist.
Uses same DB config as phase1a_mi_pipeline / data_access.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data_access import _get_db_connection

def main():
    sql_path = os.path.join(os.path.dirname(__file__), "create_wvs_analysis_schema.sql")
    with open(sql_path, "r") as f:
        ddl = f.read()
    conn = _get_db_connection()
    cur = conn.cursor()
    cur.execute(ddl)
    conn.commit()
    cur.close()
    conn.close()
    print("wvs_analysis schema and tables created.")

if __name__ == "__main__":
    main()
