#!/usr/bin/env python3
"""main.py - DFT Calculation Program Entry Point"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'python'))

from dft_input import DFTInput, load_input, get_default_input, validate_input, print_input_summary
from dft_runner import DFTRunner, SCFResult
from dft_visualize import plot_scf_convergence, plot_density_1d
from dft_output import DFTResults, save_results, print_summary
import numpy as np

def run_dft_calculation(config_file: str = None, show_plots: bool = True):
    """Run complete DFT calculation from config file."""
    # Load input
    if config_file and os.path.exists(config_file):
        dft_input = load_input(config_file)
    else:
        print("Using default configuration (Hydrogen atom)")
        dft_input = get_default_input()
    
    # Validate
    is_valid, errors = validate_input(dft_input)
    if not is_valid:
        print("Validation errors:", errors)
        return None
    
    print_input_summary(dft_input)
    
    # Initialize runner
    runner = DFTRunner(
        nx=dft_input.grid.nx, ny=dft_input.grid.ny, nz=dft_input.grid.nz,
        box_size=dft_input.grid.box_size
    )
    runner.initialize(dft_input.atoms, n_states=dft_input.n_states)
    
    # Run SCF
    scf_result = runner.run_scf(
        max_iter=dft_input.scf.max_iter,
        e_tol=dft_input.scf.energy_tolerance,
        alpha=dft_input.scf.mixing_alpha
    )
    
    # Create results
    results = DFTResults(
        converged=scf_result.converged,
        n_iterations=scf_result.n_iterations,
        total_energy=scf_result.total_energy,
        eigenvalues=scf_result.eigenvalues.tolist(),
        energy_history=scf_result.energy_history,
        xc_functional=dft_input.xc_functional.upper()
    )
    
    # Visualize
    if show_plots and len(scf_result.energy_history) > 0:
        plot_scf_convergence(scf_result.energy_history, f"SCF: {dft_input.title}")
    
    # Output
    print_summary(results)
    save_results(results, os.path.join(dft_input.output_dir, "results.json"))
    
    return results

if __name__ == "__main__":
    config = sys.argv[1] if len(sys.argv) > 1 else None
    results = run_dft_calculation(config, show_plots=False)
    if results:
        print(f"\nFinal Energy: {results.total_energy:.6f} Hartree")