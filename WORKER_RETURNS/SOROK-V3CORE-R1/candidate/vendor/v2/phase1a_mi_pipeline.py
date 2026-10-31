"""
Phase 1A: Mutual Information Pipeline

Implements the MI analysis pipeline as specified in Phase 1a.md:
1. Initialize demographics_catalog
2. Create question sets
3. Create MI runs
4. Extract data
5. Compute MI
6. Insert results
7. Aggregate and summarize
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder
from psycopg2.extras import RealDictCursor
from data_access import _get_db_connection
import json

# WVS7 var_codes derived from content layer (item_content_map.csv).
# Source of truth: data/final_codebooks/item_content_map.csv — all WVS:W7:Q* mappings
# verified against data/wvs/WVS7_codebook_2.csv. Replaces legacy 42-question list
# that used incorrect wave numbering (Q154→Q48, Q235/Q236→Q49, Q198/Q205-Q207→Q177-Q188).
def _natural_sort_var(x):
    m = re.search(r'Q(\d+)', x)
    return (int(m.group(1)), x) if m else (999, x)


def _load_wvs7_driver_var_codes():
    """Load WVS7 var_codes from item_content_map (content layer as source of truth)."""
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'final_codebooks', 'item_content_map.csv')
    if not os.path.exists(path):
        return _WVS7_DRIVER_SUBSET_FALLBACK
    codes = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('item_id'):
                continue
            parts = line.split(',')
            if len(parts) < 2:
                continue
            item_id = parts[0].strip()
            if item_id.startswith('WVS:W7:'):
                var = item_id.replace('WVS:W7:', '')
                if var and var not in codes:
                    codes.append(var)
    return sorted(codes, key=_natural_sort_var)

# Fallback if item_content_map missing (73 verified WVS7 codes from content layer)
_WVS7_DRIVER_SUBSET_FALLBACK = [
    'Q1', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q11', 'Q12', 'Q15', 'Q17', 'Q18', 'Q19', 'Q20', 'Q21', 'Q22',
    'Q27', 'Q29', 'Q30', 'Q31', 'Q33', 'Q37', 'Q38', 'Q40', 'Q42', 'Q45', 'Q46', 'Q48', 'Q49', 'Q50', 'Q51', 'Q52',
    'Q53', 'Q54', 'Q56', 'Q57', 'Q61', 'Q62', 'Q63', 'Q64', 'Q65', 'Q69', 'Q70', 'Q71', 'Q73', 'Q76', 'Q106', 'Q108',
    'Q110', 'Q111', 'Q112', 'Q118', 'Q121', 'Q131', 'Q146', 'Q147', 'Q148', 'Q151', 'Q164', 'Q171', 'Q172', 'Q173',
    'Q177', 'Q178', 'Q180', 'Q181', 'Q182', 'Q184', 'Q185', 'Q187', 'Q188', 'Q235',
]

WVS_DRIVER_SUBSET_VAR_CODES = _load_wvs7_driver_var_codes()


def initialize_demographics_catalog(conn):
    """Step 1.1: Populate demographics_catalog"""
    cur = conn.cursor()
    
    # Check if already populated
    cur.execute("SELECT COUNT(*) FROM wvs_analysis.demographics_catalog")
    if cur.fetchone()[0] > 0:
        print("demographics_catalog already populated, skipping...")
        cur.close()
        return
    
    print("Populating demographics_catalog...")
    
    cur.execute("""
        INSERT INTO wvs_analysis.demographics_catalog
        (name, label, source_column, data_type, details)
        VALUES
        -- Country
        ('country_code',    'Country',           'country_code',    'categorical', '{}'::jsonb),
        -- Sex
        ('sex',             'Sex',               'sex',             'categorical', '{}'::jsonb),
        -- Age group (we'll bin in Python, but record the binning here)
        ('age_group',       'Age group',         'age',             'ordinal',     '{"binning":[18,30,45,60,120]}'::jsonb),
        -- Education
        ('education_level', 'Education level',   'education_level', 'ordinal',     '{}'::jsonb),
        -- Income
        ('income_level',    'Income level',      'income_level',    'ordinal',     '{}'::jsonb),
        -- Urban / Rural
        ('urban_rural',     'Urban/Rural',       'urban_rural',     'categorical', '{}'::jsonb),
        -- Religion
        ('religion_code',   'Religion',          'religion_code',   'categorical', '{}'::jsonb)
    """)
    
    conn.commit()
    print("✓ demographics_catalog populated")
    cur.close()


def create_question_set(conn, name='core_values_v1', description=None, sections=None):
    """Step 1.2: Create a question set and populate question_set_variables"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if description is None:
        description = 'WVS items across multiple sections: values, family, religion, authority, gender, trust'
    
    if sections is None:
        sections = ['Values', 'Family', 'Religion', 'Politics', 'Trust']
    
    print(f"Creating question set: {name}...")
    
    # Step 1.2.1: Create question set record
    cur.execute("""
        INSERT INTO wvs_analysis.question_sets (name, description, selection_criteria)
        VALUES (%s, %s, jsonb_build_object('sections', %s::jsonb))
        RETURNING question_set_id
    """, (name, description, json.dumps(sections)))
    
    qs_row = cur.fetchone()
    question_set_id = qs_row['question_set_id']
    print(f"✓ Created question_set_id: {question_set_id}")
    
    # Step 1.2.2: Populate question_set_variables
    print(f"Populating question_set_variables for sections: {sections}...")
    
    # Build ILIKE conditions for flexible matching
    # (sections are stored as longer descriptions, so we match keywords)
    conditions = []
    params = [question_set_id]
    
    for section in sections:
        conditions.append("v.section ILIKE %s")
        params.append(f'%{section}%')
    
    where_clause = " OR ".join(conditions)
    
    cur.execute(f"""
        INSERT INTO wvs_analysis.question_set_variables (question_set_id, var_code)
        SELECT DISTINCT
            %s AS question_set_id,
            v.var_code
        FROM public.variables AS v
        WHERE {where_clause}
    """, params)
    
    var_count = cur.rowcount
    # If variables.section is not populated (e.g. load_wvs_data leaves it NULL), include all Q* vars
    if var_count == 0:
        print("  No variables matched by section; adding all question-like variables (var_code ~ '^Q[0-9]')...")
        cur.execute("""
            INSERT INTO wvs_analysis.question_set_variables (question_set_id, var_code)
            SELECT DISTINCT %s, v.var_code
            FROM public.variables AS v
            WHERE v.var_code ~ '^Q[0-9]'
              AND v.var_code NOT IN ('Q262', 'Q263', 'Q264', 'Q265')
        """, (question_set_id,))
        var_count = cur.rowcount
    print(f"✓ Added {var_count} variables to question set")
    
    conn.commit()
    cur.close()
    
    return question_set_id


def create_question_set_from_vars(conn, name='driver_subset_v1', description=None, var_codes=None):
    """Create a question set from an explicit list of var_codes (e.g. driver-subset from driverSchema.json)."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if var_codes is None:
        var_codes = WVS_DRIVER_SUBSET_VAR_CODES
    if description is None:
        description = 'WVS items mapped to drivers in driverSchema.json (construct-relevant subset)'
    print(f"Creating question set: {name} ({len(var_codes)} var_codes)...")
    cur.execute("""
        INSERT INTO wvs_analysis.question_sets (name, description, selection_criteria)
        VALUES (%s, %s, jsonb_build_object('var_codes', %s::jsonb))
        RETURNING question_set_id
    """, (name, description, json.dumps(var_codes)))
    qs_row = cur.fetchone()
    question_set_id = qs_row['question_set_id']
    print(f"✓ Created question_set_id: {question_set_id}")
    # Insert only var_codes that exist in public.variables
    cur.execute("""
        INSERT INTO wvs_analysis.question_set_variables (question_set_id, var_code)
        SELECT %s AS question_set_id, v.var_code
        FROM public.variables v
        WHERE v.var_code = ANY(%s::text[])
    """, (question_set_id, var_codes))
    var_count = cur.rowcount
    print(f"✓ Added {var_count} variables to question set (of {len(var_codes)} requested)")
    conn.commit()
    cur.close()
    return question_set_id


def create_mi_run(conn, question_set_id, method='mutual_information', params=None, notes=None):
    """Step 2: Create an MI run record"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if params is None:
        params = {
            'age_binning': [18, 30, 45, 60, 120],
            'min_respondents_per_question': 500,
            'mi_estimator': 'sklearn_mutual_info_classif',
            'drop_missing': True
        }
    
    if notes is None:
        notes = f'Initial MI run on question_set_id {question_set_id}'
    
    print(f"Creating MI run...")
    
    cur.execute("""
        INSERT INTO wvs_analysis.mi_runs (question_set_id, method, params, notes)
        VALUES (%s, %s, %s::jsonb, %s)
        RETURNING mi_run_id
    """, (question_set_id, method, json.dumps(params), notes))
    
    mi_row = cur.fetchone()
    mi_run_id = mi_row['mi_run_id']
    print(f"✓ Created mi_run_id: {mi_run_id}")
    
    conn.commit()
    cur.close()
    
    return mi_run_id, params


def extract_analysis_data(conn, question_set_id):
    """Step 3: Extract data for analysis"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print(f"Extracting data for question_set_id {question_set_id}...")
    
    # Age: prefer respondents.age, else Q262 from responses; coerce to numeric in Python
    cur.execute("""
        SELECT
            r.respondent_id,
            r.country_code,
            r.sex,
            r.age AS age_respondents,
            age_resp.value_raw AS age_responses,
            r.education_level,
            r.income_level,
            r.urban_rural,
            r.religion_code,
            rs.var_code,
            rs.value_raw
        FROM public.respondents AS r
        JOIN public.responses AS rs
          ON r.respondent_id = rs.respondent_id
        LEFT JOIN public.responses AS age_resp
          ON r.respondent_id = age_resp.respondent_id
          AND age_resp.var_code = 'Q262'
        JOIN wvs_analysis.question_set_variables AS qsv
          ON rs.var_code = qsv.var_code
        WHERE qsv.question_set_id = %s
    """, (question_set_id,))
    
    rows = cur.fetchall()
    print(f"✓ Extracted {len(rows)} rows")
    
    cur.close()
    
    # Convert to DataFrame and coalesce age (prefer respondents, then Q262)
    df = pd.DataFrame(rows)
    if len(df) == 0:
        raise ValueError(f"No data found for question_set_id {question_set_id}")
    age_r = pd.to_numeric(df['age_respondents'], errors='coerce')
    age_q = pd.to_numeric(df['age_responses'], errors='coerce')
    df['age'] = age_r.fillna(age_q)
    df = df.drop(columns=['age_respondents', 'age_responses'], errors='ignore')
    return df


def compute_mi(conn, df, mi_run_id, params):
    """Step 4: Compute MI for each question × demographic"""
    print("Computing mutual information...")
    
    # Step 4.1: Preprocessing
    print("  Preprocessing data...")
    
    # For large datasets, process in chunks to avoid memory issues
    if df is None or (isinstance(df, pd.DataFrame) and len(df) > 5_000_000):
        print(f"  ⚠️  Large dataset - processing directly from database (per question)")
        return compute_mi_from_db(conn, mi_run_id, params)
    
    # Drop missing or invalid responses
    valid = df['value_raw'].notnull()
    df = df.loc[valid].copy()
    print(f"  ✓ Valid responses: {len(df)}")
    
    # Create age_group according to binning from params
    # Convert age to numeric (it might be stored as text)
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df = df[df['age'].notna()]  # Drop rows where age couldn't be converted
    
    age_bins = params.get('age_binning', [18, 30, 45, 60, 120])
    age_labels = [f"{age_bins[i]}-{age_bins[i+1]-1}" if i < len(age_bins)-1 else f"{age_bins[i]}+" 
                  for i in range(len(age_bins)-1)]
    
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels[:len(age_bins)-1], right=False)
    
    # Restrict to respondents with non-missing demographics
    demo_cols = [
        'country_code',
        'sex',
        'age_group',
        'education_level',
        'income_level',
        'urban_rural',
        'religion_code'
    ]
    
    for col in demo_cols:
        if col == 'age_group':
            # age_group might have NaN from cut, handle separately
            df = df[df[col].notna()]
        else:
            df = df[df[col].notnull()]
    
    print(f"  ✓ After demographic filtering: {len(df)} rows")
    
    # Get mapping from demographics_catalog
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT demographic_id, name, source_column
        FROM wvs_analysis.demographics_catalog
    """)
    
    demo_catalog = pd.DataFrame(cur.fetchall())
    demo_name_to_id = dict(zip(demo_catalog['name'], demo_catalog['demographic_id']))
    source_to_name = dict(zip(demo_catalog['source_column'], demo_catalog['name']))
    cur.close()
    
    # Step 4.2: MI per question × demographic
    print("  Computing MI for each question × demographic...")
    
    results = []
    var_codes = df['var_code'].unique()
    min_respondents = params.get('min_respondents_per_question', 500)
    
    source_cols = ['country_code', 'sex', 'age_group', 'education_level', 
                   'income_level', 'urban_rural', 'religion_code']
    
    for i, var_code in enumerate(var_codes):
        if (i + 1) % 50 == 0:
            print(f"    Processing question {i+1}/{len(var_codes)}: {var_code}")
        
        df_q = df[df['var_code'] == var_code].copy()
        
        # Skip if too few respondents
        if len(df_q) < min_respondents:
            continue
        
        # Target: response values encoded as categorical labels
        y_raw = df_q['value_raw'].values
        
        # Remove invalid codes (WVS uses -1, -2, -4, -5 for missing/refused)
        valid_mask = (y_raw >= 0) & (y_raw <= 100)  # Adjust range as needed
        df_q = df_q[valid_mask]
        y_raw = df_q['value_raw'].values
        
        if len(df_q) < min_respondents:
            continue
        
        y = LabelEncoder().fit_transform(y_raw)
        
        for source_col in source_cols:
            # Map source column to demographic name + id
            demo_name = source_to_name.get(source_col, source_col)
            demographic_id = demo_name_to_id.get(demo_name)
            
            if demographic_id is None:
                continue
            
            # Get demographic values
            X_raw = df_q[source_col].astype(str).values
            
            # Skip if all same value (no variance)
            if len(np.unique(X_raw)) < 2:
                continue
            
            X = LabelEncoder().fit_transform(X_raw).reshape(-1, 1)
            
            # Compute mutual information
            try:
                mi_values = mutual_info_classif(
                    X, y,
                    discrete_features=True,
                    random_state=0
                )
                mi = float(mi_values[0])
            except Exception as e:
                print(f"    Warning: MI computation failed for {var_code} × {source_col}: {e}")
                continue
            
            results.append({
                'mi_run_id': int(mi_run_id),
                'var_code': str(var_code),
                'demographic_id': int(demographic_id),
                'mi_value': mi,
                'n_respondents': int(len(df_q)),
                'extra_stats': {}
            })
    
    print(f"  ✓ Computed {len(results)} MI values")
    
    return results


def compute_mi_from_db(conn, mi_run_id, params):
    """Compute MI by extracting data per question from database (avoids memory issues)"""
    print("  Using database-per-question extraction to avoid memory issues...")
    
    # Get question set ID from mi_run
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT question_set_id FROM wvs_analysis.mi_runs WHERE mi_run_id = %s
    """, (mi_run_id,))
    question_set_id = cur.fetchone()['question_set_id']
    
    # Get list of variables
    cur.execute("""
        SELECT DISTINCT var_code
        FROM wvs_analysis.question_set_variables
        WHERE question_set_id = %s
        ORDER BY var_code
    """, (question_set_id,))
    var_codes = [row['var_code'] for row in cur.fetchall()]
    
    # Get mapping from demographics_catalog
    cur.execute("""
        SELECT demographic_id, name, source_column
        FROM wvs_analysis.demographics_catalog
    """)
    demo_catalog = pd.DataFrame(cur.fetchall())
    demo_name_to_id = dict(zip(demo_catalog['name'], demo_catalog['demographic_id']))
    source_to_name = dict(zip(demo_catalog['source_column'], demo_catalog['name']))
    
    results = []
    min_respondents = params.get('min_respondents_per_question', 500)
    source_cols = ['country_code', 'sex', 'age_group', 'education_level', 
                   'income_level', 'urban_rural', 'religion_code']
    age_bins = params.get('age_binning', [18, 30, 45, 60, 120])
    
    print(f"  Processing {len(var_codes)} questions one at a time...")
    
    for i, var_code in enumerate(var_codes):
        if (i + 1) % 25 == 0:
            print(f"    Progress: {i+1}/{len(var_codes)} questions ({len(results)} MI values computed so far)")
        
        # Extract data for this question only; age from respondents or Q262, coalesce in Python
        cur.execute("""
            SELECT
                r.respondent_id,
                r.country_code,
                r.sex,
                r.age AS age_respondents,
                age_resp.value_raw AS age_responses,
                r.education_level,
                r.income_level,
                r.urban_rural,
                r.religion_code,
                rs.value_raw
            FROM public.respondents AS r
            JOIN public.responses AS rs
              ON r.respondent_id = rs.respondent_id
              AND rs.var_code = %s
            LEFT JOIN public.responses AS age_resp
              ON r.respondent_id = age_resp.respondent_id
              AND age_resp.var_code = 'Q262'
            WHERE rs.value_raw IS NOT NULL
        """, (var_code,))
        
        rows = cur.fetchall()
        if len(rows) < min_respondents:
            continue
        
        df_q = pd.DataFrame(rows)
        age_r = pd.to_numeric(df_q['age_respondents'], errors='coerce')
        age_q = pd.to_numeric(df_q['age_responses'], errors='coerce')
        df_q['age'] = age_r.fillna(age_q)
        df_q = df_q.drop(columns=['age_respondents', 'age_responses'], errors='ignore')
        # Preprocess
        df_q['age'] = pd.to_numeric(df_q['age'], errors='coerce')
        df_q = df_q[df_q['age'].notna()]
        
        if len(df_q) < min_respondents:
            continue
        
        # Create age_group
        age_labels = [f"{age_bins[i]}-{age_bins[i+1]-1}" if i < len(age_bins)-1 else f"{age_bins[i]}+" 
                      for i in range(len(age_bins)-1)]
        df_q['age_group'] = pd.cut(df_q['age'], bins=age_bins, labels=age_labels[:len(age_bins)-1], right=False)
        
        # Filter demographics
        demo_cols = ['country_code', 'sex', 'age_group', 'education_level', 
                     'income_level', 'urban_rural', 'religion_code']
        for col in demo_cols:
            if col == 'age_group':
                df_q = df_q[df_q[col].notna()]
            else:
                df_q = df_q[df_q[col].notnull()]
        
        if len(df_q) < min_respondents:
            continue
        
        # Target: response values
        y_raw = df_q['value_raw'].values
        valid_mask = (y_raw >= 0) & (y_raw <= 100)
        df_q = df_q[valid_mask]
        y_raw = df_q['value_raw'].values
        
        if len(df_q) < min_respondents:
            continue
        
        y = LabelEncoder().fit_transform(y_raw)
        
        # Compute MI for each demographic
        for source_col in source_cols:
            demo_name = source_to_name.get(source_col, source_col)
            demographic_id = demo_name_to_id.get(demo_name)
            
            if demographic_id is None:
                continue
            
            X_raw = df_q[source_col].astype(str).values
            
            if len(np.unique(X_raw)) < 2:
                continue
            
            X = LabelEncoder().fit_transform(X_raw).reshape(-1, 1)
            
            try:
                mi_values = mutual_info_classif(
                    X, y,
                    discrete_features=True,
                    random_state=0
                )
                mi = float(mi_values[0])
            except Exception as e:
                continue
            
            results.append({
                'mi_run_id': int(mi_run_id),
                'var_code': str(var_code),
                'demographic_id': int(demographic_id),
                'mi_value': mi,
                'n_respondents': int(len(df_q)),
                'extra_stats': {}
            })
        
        del df_q
    
    cur.close()
    print(f"  ✓ Computed {len(results)} MI values")
    return results


def insert_mi_results(conn, results):
    """Step 4.3: Insert MI results into database"""
    print("Inserting MI results into database...")
    
    if len(results) == 0:
        print("  No results to insert")
        return
    
    mi_df = pd.DataFrame(results)
    
    # Use direct psycopg2 for bulk insert (more reliable)
    cur = conn.cursor()
    
    # Prepare insert statement
    insert_sql = """
        INSERT INTO wvs_analysis.mi_results 
        (mi_run_id, var_code, demographic_id, mi_value, n_respondents, extra_stats)
        VALUES (%s, %s, %s, %s, %s, %s::jsonb)
    """
    
    # Insert in batches
    batch_size = 1000
    for i in range(0, len(mi_df), batch_size):
        batch = mi_df.iloc[i:i+batch_size]
        values = [
            (row['mi_run_id'], row['var_code'], row['demographic_id'], 
             row['mi_value'], row['n_respondents'], json.dumps(row['extra_stats']))
            for _, row in batch.iterrows()
        ]
        cur.executemany(insert_sql, values)
    
    conn.commit()
    cur.close()
    
    print(f"  ✓ Inserted {len(results)} MI results")


def aggregate_mi_summary(conn, mi_run_id):
    """Step 5: Aggregate per-demographic MI summary"""
    cur = conn.cursor()
    
    print("Aggregating MI summary...")
    
    cur.execute("""
        INSERT INTO wvs_analysis.mi_demographic_summary (
            mi_run_id,
            demographic_id,
            mean_mi,
            median_mi,
            sd_mi,
            n_questions
        )
        SELECT
            mi_run_id,
            demographic_id,
            AVG(mi_value)        AS mean_mi,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mi_value) AS median_mi,
            STDDEV_POP(mi_value) AS sd_mi,
            COUNT(*)             AS n_questions
        FROM wvs_analysis.mi_results
        WHERE mi_run_id = %s
        GROUP BY mi_run_id, demographic_id
    """, (mi_run_id,))
    
    conn.commit()
    print(f"  ✓ Aggregated summary for {cur.rowcount} demographics")
    cur.close()


def report_results(conn, mi_run_id):
    """Step 6: Report ranking of demographics"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "="*80)
    print("MI RESULTS SUMMARY")
    print("="*80)
    
    cur.execute("""
        SELECT
            d.demographic_id,
            d.name,
            d.label,
            s.mean_mi,
            s.median_mi,
            s.sd_mi,
            s.n_questions
        FROM wvs_analysis.mi_demographic_summary AS s
        JOIN wvs_analysis.demographics_catalog AS d
          ON s.demographic_id = d.demographic_id
        WHERE s.mi_run_id = %s
        ORDER BY s.mean_mi DESC
    """, (mi_run_id,))
    
    results = cur.fetchall()
    
    print(f"\n{'Demographic':<20} {'Mean MI':<12} {'Median MI':<12} {'SD':<12} {'N Questions':<12}")
    print("-" * 80)
    
    for row in results:
        print(f"{row['label']:<20} {row['mean_mi']:>10.4f}  {row['median_mi']:>10.4f}  "
              f"{row['sd_mi']:>10.4f}  {row['n_questions']:>10}")
    
    cur.close()
    
    return results


def run_phase1a_pipeline(question_set_name='core_values_v1',
                         question_set_sections=None,
                         use_driver_subset=True,
                         driver_subset_var_codes=None,
                         mi_params=None):
    """Run the complete Phase 1A pipeline.
    use_driver_subset=True: use 42 WVS questions from driverSchema.json (construct-relevant).
    use_driver_subset=False: use section-based set (Values, Family, Religion, Politics, Trust).
    """
    
    print("="*80)
    print("PHASE 1A: MUTUAL INFORMATION PIPELINE")
    print("="*80)
    
    conn = _get_db_connection()
    
    try:
        # Step 1: Initialize
        initialize_demographics_catalog(conn)
        
        # Step 1.2: Create question set (driver subset or section-based)
        if use_driver_subset:
            question_set_id = create_question_set_from_vars(
                conn,
                name=question_set_name or 'driver_subset_v1',
                var_codes=driver_subset_var_codes or WVS_DRIVER_SUBSET_VAR_CODES,
            )
        else:
            question_set_id = create_question_set(
                conn,
                name=question_set_name,
                sections=question_set_sections
            )
        
        # Step 2: Create MI run
        mi_run_id, params = create_mi_run(conn, question_set_id, params=mi_params)
        
        # Step 3: Check data size and decide extraction strategy
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT COUNT(*) as total_responses
            FROM public.responses rs
            JOIN wvs_analysis.question_set_variables qsv ON rs.var_code = qsv.var_code
            WHERE qsv.question_set_id = %s
        """, (question_set_id,))
        data_size = cur.fetchone()['total_responses']
        cur.close()
        
        # Step 4: Extract and compute MI
        if data_size > 5_000_000:
            print(f"  Large dataset ({data_size:,} rows) - using per-question extraction")
            df = None  # Skip bulk extraction
        else:
            print(f"  Extracting data ({data_size:,} rows)...")
            df = extract_analysis_data(conn, question_set_id)
        
        results = compute_mi(conn, df, mi_run_id, params)
        
        # Step 4.3: Insert results
        insert_mi_results(conn, results)
        
        # Step 5: Aggregate summary
        aggregate_mi_summary(conn, mi_run_id)
        
        # Step 6: Report
        summary = report_results(conn, mi_run_id)
        
        print("\n" + "="*80)
        print("PHASE 1A COMPLETE")
        print("="*80)
        print(f"Question Set ID: {question_set_id}")
        print(f"MI Run ID: {mi_run_id}")
        print(f"Total MI computations: {len(results)}")
        
        return {
            'question_set_id': question_set_id,
            'mi_run_id': mi_run_id,
            'summary': summary
        }
        
    finally:
        conn.close()


if __name__ == '__main__':
    # Run Phase 1A on driver-subset (42 construct-relevant questions) to settle deterministicity
    run_phase1a_pipeline(
        question_set_name='driver_subset_v1',
        use_driver_subset=True,
    )

