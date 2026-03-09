# DFT Calculation Program Architecture

## Overview

Density Functional Theory (DFT) calculation program with Fortran backend for high-performance numerical computations and Python frontend for user interaction and visualization.

## System Architecture

```
+------------------+     f2py interface     +-------------------+
|  Python Frontend | <-------------------> |  Fortran Backend  |
+------------------+                       +-------------------+
| - Input parsing  |                       | - KS solver       |
| - Visualization  |                       | - SCF loop        |
| - Result output  |                       | - XC functional   |
+------------------+                       | - Poisson solver  |
                                           | - Grid management |
                                           +-------------------+
```

## Fortran Backend Modules

### 1. `grid_manager.f90`
- 3D real-space grid initialization
- Grid spacing and boundary handling
- Memory allocation for wavefunctions

### 2. `ks_solver.f90`
- Kohn-Sham equation solver
- Eigenvalue/eigenvector computation
- Kinetic energy operator

### 3. `scf_loop.f90`
- Self-consistent field iteration
- Density mixing (simple/linear/Pulay)
- Convergence checking

### 4. `xc_functional.f90`
- LDA (Local Density Approximation)
- GGA (Generalized Gradient Approximation)
- Exchange-correlation potential calculation

### 5. `poisson.f90`
- Hartree potential solver
- FFT-based Poisson equation solver
- Periodic boundary conditions

## Python Frontend Components

### `dft_input.py`
- Configuration file parsing (JSON/YAML)
- Atom/molecule specification
- Calculation parameters

### `dft_runner.py`
- Interface to Fortran via f2py
- Calculation orchestration
- Error handling

### `dft_visualize.py`
- Kohn-Sham orbital visualization
- SCF convergence plots
- Electron density plots (matplotlib)

### `dft_output.py`
- Final energy output
- Orbital energies
- Convergence summary

## Data Flow

```
1. Input (Python) -> Parse configuration
2. Grid Setup (Fortran) -> Initialize 3D grid
3. Initial Guess (Fortran) -> Starting electron density
4. SCF Loop:
   a. Compute Hartree potential (Poisson)
   b. Compute XC potential
   c. Solve KS equations -> new orbitals
   d. Compute new density
   e. Check convergence
   f. Mix densities if not converged
5. Output (Python) -> Results + Visualization
```

## f2py Interface

```python
# Build command
f2py -c -m dft_core src/fortran/*.f90

# Python usage
import dft_core
result = dft_core.run_scf(grid_params, atom_positions, scf_config)
```

## File Structure

```
project/
├── src/
│   ├── fortran/
│   │   ├── grid_manager.f90
│   │   ├── ks_solver.f90
│   │   ├── scf_loop.f90
│   │   ├── xc_functional.f90
│   │   ├── poisson.f90
│   │   └── dft_main.f90
│   └── python/
│       ├── dft_input.py
│       ├── dft_runner.py
│       ├── dft_visualize.py
│       └── dft_output.py
├── tests/
├── docs/
└── README.md
```

## Key Algorithms

### SCF Convergence
- Maximum iterations: 100
- Energy tolerance: 1e-6 Ha
- Density tolerance: 1e-5 e/bohr³

### Kohn-Sham Solver
- Finite difference discretization
- LAPACK eigenvalue routines
- Iterative diagonalization for large systems

## Visualization Outputs

1. **SCF Convergence Plot**: Energy vs. iteration number
2. **Electron Density**: 2D slice or 3D isosurface
3. **Kohn-Sham Orbitals**: Selected orbital visualization
4. **Energy Level Diagram**: Orbital energies