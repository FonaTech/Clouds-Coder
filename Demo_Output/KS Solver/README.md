# DFT Calculation Program

A Density Functional Theory (DFT) calculation program with Fortran backend and Python frontend.

## Features

- **Fortran Backend**: High-performance numerical computations
  - Grid management (3D real-space)
  - Kohn-Sham equation solver
  - SCF loop with convergence tracking
  - LDA exchange-correlation functional
  - Poisson solver (Gauss-Seidel/SOR)

- **Python Frontend**: User-friendly interface
  - Input configuration (JSON)
  - SCF visualization (matplotlib)
  - Result output and summary

## Prerequisites

- Python 3.7+
- NumPy
- Matplotlib
- gfortran (for Fortran backend)
- f2py (comes with NumPy)

## Installation

```bash
# Install Python dependencies
make install

# Build Fortran backend (optional, for full functionality)
make fortran
```

## Usage

```bash
# Run with default configuration (Hydrogen atom)
python main.py

# Run with custom input file
python main.py input.json

# Or use make
make python
```

## Project Structure

```
.
├── main.py              # Entry point
├── Makefile             # Build automation
├── README.md            # This file
├── docs/
│   └── architecture.md  # Architecture documentation
├── src/
│   ├── fortran/         # Fortran backend
│   │   ├── grid_manager.f90
│   │   ├── ks_solver.f90
│   │   ├── scf_loop.f90
│   │   ├── xc_functional.f90
│   │   └── poisson.f90
│   └── python/          # Python frontend
│       ├── dft_input.py
│       ├── dft_runner.py
│       ├── dft_visualize.py
│       └── dft_output.py
└── tests/               # Test directory
```

## Example Input

```json
{
  "title": "Hydrogen Atom",
  "atoms": [{"symbol": "H", "position": [0, 0, 0], "nuclear_charge": 1}],
  "grid": {"nx": 32, "ny": 32, "nz": 32, "box_size": [10, 10, 10]},
  "scf": {"max_iter": 100, "energy_tolerance": 1e-6, "mixing_alpha": 0.3},
  "xc_functional": "lda",
  "n_states": 1
}
```

## Output

- SCF convergence plot
- Total energy (Hartree and eV)
- Orbital energies
- Results saved to `output/results.json`

## License

MIT License