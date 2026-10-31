#!/usr/bin/env python3
"""
Systematically review WVS questions to identify demographic/objective status variables
vs. attitudinal/perspectival questions.
"""

import re
from pathlib import Path

# Keywords that suggest demographic/objective status
DEMOGRAPHIC_KEYWORDS = [
    # Basic demographics
    'age', 'years old', 'born', 'birth', 'citizen', 'citizenship',
    'marital status', 'married', 'single', 'divorced', 'widowed',
    'children', 'child', 'household', 'people in household',
    'living with', 'live with', 'parents',
    
    # Employment/economic status
    'employed', 'employment', 'unemployed', 'retired', 'student',
    'wage earner', 'chief wage', 'income', 'savings', 'economic situation',
    'social class', 'class',
    
    # Education
    'education', 'educational', 'school', 'university', 'degree',
    'highest educational level', 'mother education', 'father education',
    
    # Residence/housing
    'settlement', 'town', 'village', 'city', 'urban', 'rural',
    'language at home', 'language spoken',
    
    # Family background
    'father born', 'mother born', 'country of birth',
    
    # Health/objective conditions
    'health', 'illness', 'disability',
    
    # Membership/affiliation (objective)
    'member of', 'belong to', 'organization', 'union',
]

# Keywords that suggest attitudinal/perspectival
ATTITUDINAL_KEYWORDS = [
    'important', 'agree', 'disagree', 'satisfied', 'happy', 'trust',
    'confidence', 'perception', 'opinion', 'believe', 'think', 'feel',
    'should', 'would', 'prefer', 'like', 'dislike', 'fear', 'worry',
    'proud', 'ashamed', 'values', 'norms', 'acceptable', 'justifiable',
    'right', 'wrong', 'moral', 'ethical', 'tolerance', 'respect',
]

def parse_codebook(codebook_path):
    """Parse the WVS codebook and extract all Q variables with their questions."""
    questions = []
    
    with open(codebook_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Match Q variable codes (Q1, Q2, Q273, Q279, etc.)
        match = re.match(r'^(Q\d+[A-Z_]*)\s+(.+)$', line)
        if match:
            var_code = match.group(1)
            var_label = match.group(2)
            
            # Get question text (next few lines)
            question_text = ""
            j = i + 1
            while j < len(lines) and j < i + 5:
                next_line = lines[j].strip()
                # Stop if we hit another Q variable or empty line after question
                if re.match(r'^Q\d+', next_line):
                    break
                if next_line and not next_line.startswith('-') and not next_line.startswith('1.-'):
                    if question_text:
                        question_text += " " + next_line
                    else:
                        question_text = next_line
                j += 1
            
            questions.append({
                'var_code': var_code,
                'var_label': var_label,
                'question_text': question_text.strip()
            })
        
        i += 1
    
    return questions

def classify_question(question):
    """Classify a question as demographic, attitudinal, or mixed."""
    text = (question['var_label'] + " " + question['question_text']).lower()
    
    demo_score = sum(1 for keyword in DEMOGRAPHIC_KEYWORDS if keyword in text)
    att_score = sum(1 for keyword in ATTITUDINAL_KEYWORDS if keyword in text)
    
    # Special cases - known demographics
    known_demos = ['Q262', 'Q269', 'Q271', 'Q273', 'Q274', 'Q275', 'Q276', 
                   'Q277', 'Q278', 'Q279', 'Q280', 'Q285', 'Q286', 'Q287',
                   'Q288', 'Q289', 'Q290', 'Q266', 'Q267', 'Q268', 'Q270',
                   'Q272', 'Q281', 'Q282', 'Q283', 'Q284']
    
    if question['var_code'] in known_demos:
        return 'demographic', 'Known demographic variable'
    
    # Check for objective status indicators
    objective_indicators = [
        'how many', 'number of', 'count', 'years', 'hours', 'times',
        'member of', 'belong to', 'do you have', 'have you',
        'are you', 'is your', 'was your', 'were you',
    ]
    
    has_objective = any(indicator in text for indicator in objective_indicators)
    
    if demo_score > att_score and has_objective:
        return 'demographic', f'Demographic indicators: {demo_score} vs attitudinal: {att_score}'
    elif att_score > demo_score:
        return 'attitudinal', f'Attitudinal indicators: {att_score} vs demographic: {demo_score}'
    elif demo_score > 0:
        return 'mixed', f'Mixed: demographic={demo_score}, attitudinal={att_score}'
    else:
        return 'unclear', 'No clear indicators'

def main():
    codebook_path = Path('data/WVS7_Codebook_Variables.txt')
    
    print("Parsing WVS codebook...")
    questions = parse_codebook(codebook_path)
    print(f"Found {len(questions)} Q variables\n")
    
    # Classify all questions
    classifications = {
        'demographic': [],
        'attitudinal': [],
        'mixed': [],
        'unclear': []
    }
    
    for q in questions:
        category, reason = classify_question(q)
        classifications[category].append((q, reason))
    
    # Write report
    output_path = Path('v2/WVS_DEMOGRAPHIC_QUESTIONS_REVIEW.md')
    with open(output_path, 'w') as f:
        f.write("# WVS Questions: Demographic vs. Attitudinal Classification\n\n")
        f.write("This document reviews all WVS questions to identify which are **demographic/objective status** variables\n")
        f.write("vs. **attitudinal/perspectival** questions.\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Demographic/Objective Status**: {len(classifications['demographic'])}\n")
        f.write(f"- **Attitudinal/Perspectival**: {len(classifications['attitudinal'])}\n")
        f.write(f"- **Mixed/Unclear**: {len(classifications['mixed']) + len(classifications['unclear'])}\n\n")
        f.write("---\n\n")
        
        # Demographic questions
        f.write("## Demographic / Objective Status Questions\n\n")
        f.write("These questions ask about **objective facts, status, or experiences** rather than attitudes or values.\n\n")
        for q, reason in sorted(classifications['demographic'], key=lambda x: x[0]['var_code']):
            f.write(f"### {q['var_code']}: {q['var_label']}\n\n")
            f.write(f"**Question**: {q['question_text']}\n\n")
            f.write(f"**Reason**: {reason}\n\n")
            f.write("---\n\n")
        
        # Mixed/Unclear
        if classifications['mixed']:
            f.write("## Mixed / Unclear Questions\n\n")
            f.write("These questions may have both demographic and attitudinal elements, or are unclear.\n\n")
            for q, reason in sorted(classifications['mixed'], key=lambda x: x[0]['var_code']):
                f.write(f"### {q['var_code']}: {q['var_label']}\n\n")
                f.write(f"**Question**: {q['question_text']}\n\n")
                f.write(f"**Reason**: {reason}\n\n")
                f.write("---\n\n")
    
    print(f"✅ Report written to {output_path}")
    print(f"\nSummary:")
    print(f"  Demographic: {len(classifications['demographic'])}")
    print(f"  Attitudinal: {len(classifications['attitudinal'])}")
    print(f"  Mixed/Unclear: {len(classifications['mixed']) + len(classifications['unclear'])}")

if __name__ == '__main__':
    main()

