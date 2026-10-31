#!/usr/bin/env python3
"""Extract specific WVS questions from WVS_QUESTIONS_FORMATTED.md"""

import re
from pathlib import Path

# Read the formatted file
formatted_path = Path('v2/WVS_QUESTIONS_FORMATTED.md')
with open(formatted_path, 'r') as f:
    content = f.read()

# Questions to extract
target_questions = ['Q20', 'Q45', 'Q46', 'Q51', 'Q55', 'Q58', 'Q63', 'Q66', 'Q67', 'Q68', 'Q69', 'Q70', 'Q71', 'Q72', 'Q78', 'Q79', 'Q82', 'Q99', 'Q100', 'Q105', 'Q138', 'Q140', 'Q144', 'Q145', 'Q146', 'Q147', 'Q151', 'Q154', 'Q160', 'Q174', 'Q198', 'Q199', 'Q200', 'Q205', 'Q206', 'Q207', 'Q210', 'Q211', 'Q235', 'Q236', 'Q245', 'Q248']

# Questions that are in grouped sections
grouped_sections = {
    'Q20': ('Q18-Q26', 'People who have AIDS'),
    'Q58': ('Q57-Q93', 'The armed forces'),
    'Q63': ('Q57-Q93', 'The courts'),
    'Q66': ('Q57-Q93', 'Parliament'),
    'Q67': ('Q57-Q93', 'The civil service'),
    'Q68': ('Q57-Q93', 'Universities'),
    'Q69': ('Q57-Q93', 'Major companies'),
    'Q70': ('Q57-Q93', 'Banks'),
    'Q71': ('Q57-Q93', 'Environmental organizations'),
    'Q72': ('Q57-Q93', "Women's organizations"),
    'Q78': ('Q57-Q93', 'The International Monetary Fund'),
    'Q79': ('Q57-Q93', 'The World Trade Organization'),
    'Q82': ('Q57-Q93', 'Various regional organizations'),
    'Q99': ('Q94-Q105', 'Environmental organizations'),
    'Q100': ('Q94-Q105', 'Professional organization'),
    'Q105': ('Q94-Q105', 'Other organization'),
    'Q138': ('Q131-Q151', 'Being infected with AIDS'),
    'Q140': ('Q131-Q151', 'An environmental catastrophe'),
}

extracted = []
md_lines = ["# WVS Questions Used in Driver Mappings (Extracted from Formatted File)", ""]
md_lines.append("This file contains the WVS questions that are mapped to drivers, extracted from `WVS_QUESTIONS_FORMATTED.md`.")
md_lines.append("")
md_lines.append(f"**Total questions**: {len(target_questions)}")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

for q_code in sorted(target_questions, key=lambda x: int(x[1:]) if x[1:].isdigit() else 999):
    # Check if it's in a grouped section
    if q_code in grouped_sections:
        group_name, item_name = grouped_sections[q_code]
        # Find the grouped section
        pattern = rf'^### {re.escape(group_name)}:(.*?)(?=^### |^## |\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            group_content = match.group(1)
            # Extract the specific item from the group
            item_pattern = rf'\*\*{re.escape(q_code)}:\*\*\s*{re.escape(item_name)}'
            if re.search(item_pattern, group_content):
                md_lines.append(f"### {q_code}: {item_name}")
                md_lines.append("")
                # Extract the question text from the group
                question_match = re.search(r'\*\*Question:\*\*\s*(.+?)(?=\*\*|$)', group_content, re.DOTALL)
                if question_match:
                    q_text = question_match.group(1).strip()
                    md_lines.append(f"**Question:** {q_text}")
                else:
                    md_lines.append(f"**Question:** (Part of {group_name} group)")
                md_lines.append("")
                # Extract response options
                options_match = re.search(r'\*\*Response Options:\*\*(.*?)(?=\*\*|$)', group_content, re.DOTALL)
                if options_match:
                    md_lines.append("**Response Options:**")
                    options = options_match.group(1).strip()
                    md_lines.append(options)
                md_lines.append("")
                md_lines.append("---")
                md_lines.append("")
                continue
    
    # Try to find individual question
    pattern = rf'^### {re.escape(q_code)}:(.*?)(?=^### |^## |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        section = match.group(1).strip()
        md_lines.append(f"### {q_code}:{section}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
    else:
        # Not found
        md_lines.append(f"### {q_code}")
        md_lines.append("")
        md_lines.append("**Question:** NOT FOUND in formatted file")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

# Write to file
output_path = Path('v2/WVS_QUESTIONS_DRIVER_SUBSET.md')
with open(output_path, 'w') as f:
    f.write('\n'.join(md_lines))

print(f"✅ Created {output_path}")
print(f"   Extracted {len(target_questions)} questions")
