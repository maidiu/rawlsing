#!/usr/bin/env python3
"""Extract WVS question text for all questions used in driver mappings."""

import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

# Load driver schema
schema_path = Path('enneagrams/cross-data/driverSchema.json')
with open(schema_path) as f:
    schema = json.load(f)

# Extract all WVS question codes and map to drivers
question_to_drivers = {}
for driver_name, driver_def in schema.items():
    proxies = driver_def.get('proxies', [])
    for proxy in proxies:
        if isinstance(proxy, dict):
            var = proxy.get('variable', '')
        else:
            var = str(proxy)
        
        if var.startswith('wvs7.'):
            rest = var.split('.')[1]
            wvs_var = rest if rest.startswith('Q') else f'Q{rest[1:]}'
            if wvs_var not in question_to_drivers:
                question_to_drivers[wvs_var] = []
            question_to_drivers[wvs_var].append(driver_name)

# Connect to database
conn = psycopg2.connect(
    dbname="Rawlsing—WVS",
    user="postgres",
    password=os.getenv("PGPASSWORD", "rocketsauce"),
    host="localhost"
)
cur = conn.cursor(cursor_factory=RealDictCursor)

# Query question text for each question
questions_data = {}
for q_code in sorted(question_to_drivers.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 999):
    cur.execute("""
        SELECT var_code, question_text, section, response_type
        FROM public.variables
        WHERE var_code = %s
    """, (q_code,))
    
    row = cur.fetchone()
    if row:
        questions_data[q_code] = {
            'question_text': row['question_text'],
            'section': row['section'],
            'response_type': row['response_type'],
            'drivers': question_to_drivers[q_code]
        }
    else:
        questions_data[q_code] = {
            'question_text': 'NOT FOUND IN DATABASE',
            'section': None,
            'response_type': None,
            'drivers': question_to_drivers[q_code]
        }

cur.close()
conn.close()

# Generate markdown in format similar to WVS_QUESTIONS_FORMATTED.md
md_lines = ["# WVS Questions Used in Driver Mappings", ""]
md_lines.append("This document contains the WVS questions that are mapped to drivers in `driverSchema.json`.")
md_lines.append("")
md_lines.append(f"**Total questions**: {len(questions_data)}")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

for q_code in sorted(questions_data.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 999):
    data = questions_data[q_code]
    md_lines.append(f"### {q_code}")
    
    # Format question text
    if data['question_text']:
        q_text = data['question_text'].strip()
        md_lines.append(f"**Question:** {q_text}")
    else:
        md_lines.append("**Question:** NOT FOUND")
    
    md_lines.append("")
    
    # Response options
    if data['response_type']:
        md_lines.append("**Response Options:**")
        options = data['response_type']
        md_lines.append(options)
    else:
        md_lines.append("**Response Options:** Not available")
    
    md_lines.append("")
    
    # Drivers
    md_lines.append("**Used in Drivers:**")
    for driver in sorted(data['drivers']):
        driver_def = schema[driver]
        md_lines.append(f"- `{driver}`: {driver_def['definition']}")
    
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

# Write to file
output_path = Path('v2/WVS_QUESTIONS_DRIVER_SUBSET.md')
with open(output_path, 'w') as f:
    f.write('\n'.join(md_lines))

print(f"✅ Created {output_path}")
print(f"   Total questions: {len(questions_data)}")
