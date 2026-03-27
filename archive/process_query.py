#!/usr/bin/env python3
"""
VECTAETOS Query Processor
Processes user query and returns tension map + projection
"""

import sys
import json

# Import your actual epistemic_field.py
# from epistemic_field import process_query

def calculate_tensions(query_text: str) -> dict:
    """
    Calculate axiom tensions based on query
    
    TODO: Replace with actual VECTAETOS pipeline:
    - Epistemic Gates (3-Gate filtering)
    - 4ES state determination  
    - K(Φ) coherence calculation
    - Simulation Vortex (if needed)
    - Runic projection
    """
    
    # MOCK IMPLEMENTATION - Replace with real logic
    query_lower = query_text.lower()
    
    # Simple keyword-based tension calculation (placeholder)
    tensions = {
        'INT': 0.5,  # Default
        'LEX': 0.5,
        'VER': 0.5,
        'LIB': 0.5,
        'UNI': 0.5,
        'REL': 0.5,
        'WIS': 0.5,
        'CRE': 0.5
    }
    
    # Example: detect uncertainty → increase WIS tension
    if any(word in query_lower for word in ['neviem', 'uncertain', 'don\'t know']):
        tensions['WIS'] = 0.85
        tensions['VER'] = 0.30
    
    # Example: detect conflict → increase REL tension
    if any(word in query_lower for word in ['konflikt', 'problem', 'rozhodnutie']):
        tensions['REL'] = 0.75
        tensions['INT'] = 0.65
    
    return tensions

def generate_projection(query_text: str, tensions: dict) -> str:
    """
    Generate human-readable projection text
    """
    
    # Find highest tension axioms
    sorted_tensions = sorted(tensions.items(), key=lambda x: x[1], reverse=True)
    top_axiom = sorted_tensions[0]
    low_axiom = sorted_tensions[-1]
    
    projection = f"""
Pole detekuje napätie medzi {top_axiom[0]} ({top_axiom[1]*100:.0f}%) 
a {low_axiom[0]} ({low_axiom[1]*100:.0f}%).

[TODO: Insert actual VECTAETOS projection logic]

Tvoj problém nie je v odpovedi.
Je v otázke, ktorú si ešte nepoložil.
    """.strip()
    
    return projection

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_query.py '<query text>'")
        sys.exit(1)
    
    query = sys.argv[1]
    
    # Calculate tensions
    tensions = calculate_tensions(query)
    
    # Generate projection
    projection_text = generate_projection(query, tensions)
    
    # Output as JSON
    result = {
        'tensions': tensions,
        'projection': projection_text,
        'timestamp': '2026-02-02T00:00:00Z'  # Add real timestamp
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
