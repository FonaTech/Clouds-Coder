"""dft_output.py - Output handling for DFT calculation results"""
import json
import numpy as np
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime

@dataclass
class DFTResults:
    """Container for DFT calculation results."""
    converged: bool
    n_iterations: int
    total_energy: float  # Hartree
    eigenvalues: List[float]
    energy_history: List[float]
    xc_functional: str = "LDA"
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

def save_results(results: DFTResults, filename: str = "dft_results.json"):
    """Save results to JSON file."""
    data = asdict(results)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Results saved to {filename}")

def print_summary(results: DFTResults):
    """Print formatted summary of DFT results."""
    print("\n" + "="*50)
    print("DFT CALCULATION RESULTS")
    print("="*50)
    print(f"Status: {'CONVERGED' if results.converged else 'NOT CONVERGED'}")
    print(f"SCF Iterations: {results.n_iterations}")
    print(f"XC Functional: {results.xc_functional}")
    print(f"\nTotal Energy: {results.total_energy:.6f} Ha")
    print(f"             ({results.total_energy * 27.2114:.4f} eV)")
    print(f"\nOrbital Energies:")
    for i, e in enumerate(results.eigenvalues):
        print(f"  ε_{i} = {e:.6f} Ha ({e * 27.2114:.4f} eV)")
    print(f"\nTimestamp: {results.timestamp}")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Test output module
    test_results = DFTResults(
        converged=True, n_iterations=15, total_energy=-0.5,
        eigenvalues=[-0.5], energy_history=[-0.4, -0.45, -0.48, -0.49, -0.5]
    )
    print_summary(test_results)
    save_results(test_results, "test_results.json")