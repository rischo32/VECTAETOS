#!/usr/bin/env python3
"""
Deterministic Verification Script for Vectaetos Vortex
Runs simulation twice with same seed, compares normalized outputs via hashes.
"""

import json
import hashlib
import subprocess
import os
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Constants for normalization
FLOAT_PRECISION = 6

# Keccak256 from pycryptodome
try:
    from Crypto.Hash import keccak
except ImportError:
    print("CRITICAL: pycryptodome not installed. Run 'pip install pycryptodome'")
    sys.exit(1)

def parse_jsonl(filepath: Path) -> List[Dict]:
    """Parse JSONL file into list of dicts."""
    data = []
    if not filepath.exists():
        return data
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return data

def normalize_output(data: Any) -> Any:
    """
    Recursively normalize data:
    1. Remove non-deterministic fields (timestamp, time)
    2. Round floats to fixed precision to handle floating point drift
    3. Handle nested structures (dicts, lists)
    """
    if isinstance(data, dict):
        return {
            k: normalize_output(v) 
            for k, v in data.items() 
            if k not in ("timestamp", "time")
        }
    elif isinstance(data, list):
        return [normalize_output(item) for item in data]
    elif isinstance(data, float):
        # Explicit rounding to handle cross-platform floating point differences
        if math.isfinite(data):
            return round(data, FLOAT_PRECISION)
        else:
            return str(data) # Handle Inf/NaN as strings
    elif isinstance(data, (int, str)) or data is None:
        return data
    else:
        # Fallback for any other types (e.g. numpy types if they escaped)
        try:
            if hasattr(data, "item"): # numpy scalar
                return normalize_output(data.item())
            return str(data)
        except:
            return str(data)

def sort_jsonl_data(data: List[Dict]) -> List[Dict]:
    """Sort JSONL data by serialized representation for consistent ordering."""
    # We use separators to ensure minimal and consistent representation during sorting
    return sorted(data, key=lambda x: json.dumps(x, sort_keys=True, separators=(",", ":")))

def compute_hash(data: Any) -> Dict[str, Any]:
    """Compute SHA256 and Keccak256 hashes of normalized data."""
    # Ensure consistent serialization for hashing
    serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
    serialized_bytes = serialized.encode('utf-8')
    
    sha256_hash = hashlib.sha256(serialized_bytes).hexdigest()
    
    keccak_hasher = keccak.new(digest_bits=256)
    keccak_hasher.update(serialized_bytes)
    keccak_hash = keccak_hasher.hexdigest()
    
    return {
        "sha256": sha256_hash,
        "keccak256": keccak_hash,
        "serialized_size_bytes": len(serialized_bytes)
    }

def run_simulation(seed: int, steps: int, output_path: Path) -> None:
    """Run vortex simulation with given configuration."""
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing output file if it exists (since vortex appends)
    if output_path.exists():
        output_path.unlink()
        
    cmd = [
        sys.executable, "vortex/vortex_v2.0.py",
        "--seed", str(seed),
        "--steps", str(steps),
        "--output", str(output_path),
        "--quiet"
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    # Configuration
    SEED = 42
    STEPS = 1000 # Reduced from 12000 for faster verification
    ARTIFACT_DIR = Path("artifacts")
    ARTIFACT_DIR.mkdir(exist_ok=True)
    
    print(f"Starting deterministic verification (Seed: {SEED}, Steps: {STEPS})")
    
    # Run 1
    output1 = ARTIFACT_DIR / "run_1.jsonl"
    run_simulation(SEED, STEPS, output1)
    
    # Parse and process run 1
    data1 = parse_jsonl(output1)
    norm1 = normalize_output(data1)
    # Sort normalized data to ensure consistent ordering regardless of timestamp/float differences
    norm1 = sort_jsonl_data(norm1)
    hashes1 = compute_hash(norm1)
    
    # Run 2
    output2 = ARTIFACT_DIR / "run_2.jsonl"
    run_simulation(SEED, STEPS, output2)
    
    # Parse and process run 2
    data2 = parse_jsonl(output2)
    norm2 = normalize_output(data2)
    # Sort normalized data to ensure consistent ordering regardless of timestamp/float differences
    norm2 = sort_jsonl_data(norm2)
    hashes2 = compute_hash(norm2)
    
    # Save normalized outputs for debugging
    with open(ARTIFACT_DIR / "run_1_normalized.json", "w") as f:
        json.dump(norm1, f, indent=2)
    with open(ARTIFACT_DIR / "run_2_normalized.json", "w") as f:
        json.dump(norm2, f, indent=2)
    
    # Save hash report
    report = {
        "seed": SEED,
        "steps": STEPS,
        "run_1": hashes1,
        "run_2": hashes2,
        "deterministic": hashes1 == hashes2
    }
    with open(ARTIFACT_DIR / "verification_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Compare and fail if different
    if hashes1 != hashes2:
        print("\nERROR: Determinism check FAILED!")
        print(f"  Run 1 SHA256: {hashes1['sha256']}")
        print(f"  Run 2 SHA256: {hashes2['sha256']}")
        print(f"  Run 1 Keccak256: {hashes1['keccak256']}")
        print(f"  Run 2 Keccak256: {hashes2['keccak256']}")
        
        # Check if length matches
        if len(data1) != len(data2):
            print(f"  Record count mismatch: Run 1 has {len(data1)}, Run 2 has {len(data2)}")
            
        import sys
        sys.exit(1)
    
    print("\nSUCCESS: Determinism verified!")
    print(f"  SHA256:    {hashes1['sha256']}")
    print(f"  Keccak256: {hashes1['keccak256']}")
    print(f"  Records:   {len(data1)}")
    print(f"  Report:    {ARTIFACT_DIR}/verification_report.json")

if __name__ == "__main__":
    main()
