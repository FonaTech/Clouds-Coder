"""dft_visualize.py - Visualization for DFT calculations (SCF, density, orbitals)"""
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional

def plot_scf_convergence(energy_history: List[float], title: str = "SCF Convergence"):
    """Plot SCF energy vs iteration number."""
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(energy_history)+1), energy_history, 'b-o', markersize=4)
    plt.xlabel("Iteration")
    plt.ylabel("Total Energy (Hartree)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_density_1d(density: np.ndarray, x_grid: np.ndarray, title: str = "Electron Density"):
    """Plot 1D slice of electron density."""
    plt.figure(figsize=(8, 5))
    plt.plot(x_grid, density, 'r-', linewidth=2)
    plt.xlabel("Position (Bohr)")
    plt.ylabel("Density (e/Bohr³)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_wavefunction(psi: np.ndarray, x_grid: np.ndarray, n: int = 0):
    """Plot nth Kohn-Sham orbital wavefunction."""
    plt.figure(figsize=(8, 5))
    plt.plot(x_grid, psi, 'g-', linewidth=2, label=f"ψ_{n}")
    plt.xlabel("Position (Bohr)")
    plt.ylabel("Wavefunction")
    plt.title(f"Kohn-Sham Orbital n={n}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_energy_levels(eigenvalues: np.ndarray, title: str = "Orbital Energies"):
    """Plot energy level diagram."""
    plt.figure(figsize=(6, 5))
    for i, e in enumerate(eigenvalues):
        plt.hlines(e, i-0.3, i+0.3, colors='blue', linewidth=3)
        plt.text(i+0.4, e, f"{e:.4f} Ha", va='center')
    plt.ylabel("Energy (Hartree)")
    plt.xlabel("Orbital Index")
    plt.title(title)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Test visualization
    test_energy = [-0.5, -0.48, -0.49, -0.495, -0.498, -0.499, -0.5]
    plot_scf_convergence(test_energy, "Test SCF Convergence")
    x = np.linspace(-5, 5, 100)
    rho = np.exp(-x**2)
    plot_density_1d(rho, x, "Test Density (Gaussian)")
    psi = np.exp(-x**2/2) / np.sqrt(np.sqrt(np.pi))
    plot_wavefunction(psi, x, n=0)