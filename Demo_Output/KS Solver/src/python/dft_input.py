"""
dft_input.py - Input Parameter Handling for DFT Calculations
Provides configuration management for DFT calculation setup.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple


@dataclass
class Atom:
    """Represents an atom in the system."""
    symbol: str
    position: Tuple[float, float, float]  # (x, y, z) in Bohr
    nuclear_charge: int = 1
    
    def to_dict(self) -> Dict:
        return {
            'symbol': self.symbol,
            'position': list(self.position),
            'nuclear_charge': self.nuclear_charge
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Atom':
        return cls(
            symbol=data['symbol'],
            position=tuple(data['position']),
            nuclear_charge=data.get('nuclear_charge', 1)
        )


@dataclass
class GridSettings:
    """Grid parameters for real-space discretization."""
    nx: int = 32
    ny: int = 32
    nz: int = 32
    box_size: Tuple[float, float, float] = (10.0, 10.0, 10.0)  # Bohr
    
    def to_dict(self) -> Dict:
        return {
            'nx': self.nx,
            'ny': self.ny,
            'nz': self.nz,
            'box_size': list(self.box_size)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GridSettings':
        return cls(
            nx=data.get('nx', 32),
            ny=data.get('ny', 32),
            nz=data.get('nz', 32),
            box_size=tuple(data.get('box_size', [10.0, 10.0, 10.0]))
        )


@dataclass
class SCFSettings:
    """SCF convergence parameters."""
    max_iter: int = 100
    energy_tolerance: float = 1e-6  # Hartree
    density_tolerance: float = 1e-5  # e/Bohr^3
    mixing_alpha: float = 0.3  # Linear mixing parameter
    
    def to_dict(self) -> Dict:
        return {
            'max_iter': self.max_iter,
            'energy_tolerance': self.energy_tolerance,
            'density_tolerance': self.density_tolerance,
            'mixing_alpha': self.mixing_alpha
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SCFSettings':
        return cls(
            max_iter=data.get('max_iter', 100),
            energy_tolerance=data.get('energy_tolerance', 1e-6),
            density_tolerance=data.get('density_tolerance', 1e-5),
            mixing_alpha=data.get('mixing_alpha', 0.3)
        )


@dataclass
class DFTInput:
    """Complete DFT calculation input parameters."""
    
    # System description
    title: str = "DFT Calculation"
    atoms: List[Atom] = field(default_factory=list)
    
    # Grid settings
    grid: GridSettings = field(default_factory=GridSettings)
    
    # SCF settings
    scf: SCFSettings = field(default_factory=SCFSettings)
    
    # XC functional type: 'lda', 'gga'
    xc_functional: str = 'lda'
    
    # Number of occupied states (electrons / 2 for spin-paired)
    n_states: int = 1
    
    # Poisson solver settings
    poisson_max_iter: int = 1000
    poisson_tolerance: float = 1e-8
    
    # Output settings
    output_dir: str = './output'
    verbose: bool = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'atoms': [a.to_dict() for a in self.atoms],
            'grid': self.grid.to_dict(),
            'scf': self.scf.to_dict(),
            'xc_functional': self.xc_functional,
            'n_states': self.n_states,
            'poisson_max_iter': self.poisson_max_iter,
            'poisson_tolerance': self.poisson_tolerance,
            'output_dir': self.output_dir,
            'verbose': self.verbose
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DFTInput':
        """Create from dictionary."""
        atoms = [Atom.from_dict(a) for a in data.get('atoms', [])]
        grid = GridSettings.from_dict(data.get('grid', {}))
        scf = SCFSettings.from_dict(data.get('scf', {}))
        
        return cls(
            title=data.get('title', 'DFT Calculation'),
            atoms=atoms,
            grid=grid,
            scf=scf,
            xc_functional=data.get('xc_functional', 'lda'),
            n_states=data.get('n_states', 1),
            poisson_max_iter=data.get('poisson_max_iter', 1000),
            poisson_tolerance=data.get('poisson_tolerance', 1e-8),
            output_dir=data.get('output_dir', './output'),
            verbose=data.get('verbose', True)
        )


def get_default_input() -> DFTInput:
    """Get default input configuration for a simple H atom."""
    default = DFTInput(
        title="Hydrogen Atom",
        atoms=[Atom(symbol='H', position=(0.0, 0.0, 0.0), nuclear_charge=1)],
        grid=GridSettings(nx=32, ny=32, nz=32, box_size=(10.0, 10.0, 10.0)),
        scf=SCFSettings(max_iter=100, energy_tolerance=1e-6, mixing_alpha=0.3),
        xc_functional='lda',
        n_states=1
    )
    return default


def load_input(filename: str) -> DFTInput:
    """Load input configuration from JSON file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Input file not found: {filename}")
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    return DFTInput.from_dict(data)


def save_input(dft_input: DFTInput, filename: str) -> None:
    """Save input configuration to JSON file."""
    with open(filename, 'w') as f:
        json.dump(dft_input.to_dict(), f, indent=2)


def validate_input(dft_input: DFTInput) -> Tuple[bool, List[str]]:
    """
    Validate input parameters.
    
    Returns:
        (is_valid, list of error messages)
    """
    errors = []
    
    # Check grid dimensions
    if dft_input.grid.nx < 4 or dft_input.grid.ny < 4 or dft_input.grid.nz < 4:
        errors.append("Grid dimensions must be at least 4 in each direction")
    
    # Check box size
    if any(s <= 0 for s in dft_input.grid.box_size):
        errors.append("Box size must be positive")
    
    # Check SCF parameters
    if dft_input.scf.max_iter < 1:
        errors.append("SCF max iterations must be at least 1")
    
    if dft_input.scf.mixing_alpha <= 0 or dft_input.scf.mixing_alpha > 1:
        errors.append("Mixing alpha must be in (0, 1]")
    
    # Check number of states
    if dft_input.n_states < 1:
        errors.append("Number of states must be at least 1")
    
    # Check XC functional
    valid_xc = ['lda', 'gga']
    if dft_input.xc_functional.lower() not in valid_xc:
        errors.append(f"XC functional must be one of: {valid_xc}")
    
    # Check atoms
    for i, atom in enumerate(dft_input.atoms):
        if atom.nuclear_charge < 1:
            errors.append(f"Atom {i}: nuclear charge must be positive")
        
        # Check if atom is within box
        pos = atom.position
        box = dft_input.grid.box_size
        if any(abs(p) > b/2 for p, b in zip(pos, box)):
            errors.append(f"Atom {i} ({atom.symbol}) is outside the simulation box")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def print_input_summary(dft_input: DFTInput) -> None:
    """Print a summary of the input configuration."""
    print("=" * 50)
    print(f"DFT Calculation: {dft_input.title}")
    print("=" * 50)
    print(f"\nGrid: {dft_input.grid.nx} x {dft_input.grid.ny} x {dft_input.grid.nz}")
    print(f"Box: {dft_input.grid.box_size} Bohr")
    print(f"\nAtoms ({len(dft_input.atoms)}):")
    for atom in dft_input.atoms:
        print(f"  {atom.symbol} at {atom.position}, Z={atom.nuclear_charge}")
    print(f"\nXC Functional: {dft_input.xc_functional.upper()}")
    print(f"States: {dft_input.n_states}")
    print(f"\nSCF: max_iter={dft_input.scf.max_iter}, "
          f"e_tol={dft_input.scf.energy_tolerance}, "
          f"alpha={dft_input.scf.mixing_alpha}")
    print("=" * 50)


# Example usage and testing
if __name__ == "__main__":
    # Create default input
    inp = get_default_input()
    
    # Validate
    is_valid, errors = validate_input(inp)
    if is_valid:
        print("Input is valid!")
    else:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
    
    # Print summary
    print_input_summary(inp)
    
    # Save to file
    save_input(inp, "example_input.json")
    print("\nSaved to example_input.json")