# Makefile for DFT Calculation Program

FC = gfortran
FFLAGS = -O2 -fPIC
PYTHON = python3

# Fortran source files
FSRC = src/fortran/grid_manager.f90 src/fortran/ks_solver.f90 \
       src/fortran/scf_loop.f90 src/fortran/xc_functional.f90 \
       src/fortran/poisson.f90

# Python module output
PYMOD = dft_core.so

.PHONY: all clean test fortran python install

all: fortran python

# Build Fortran backend with f2py
fortran: $(PYMOD)

$(PYMOD): $(FSRC)
	f2py -c -m dft_core $(FSRC) $(FFLAGS)

# Run Python frontend (without Fortran)
python:
	$(PYTHON) main.py

# Run tests
test:
	$(PYTHON) -c "from src.python.dft_input import *; print('dft_input OK')"
	$(PYTHON) -c "from src.python.dft_runner import *; print('dft_runner OK')"
	$(PYTHON) -c "from src.python.dft_visualize import *; print('dft_visualize OK')"
	$(PYTHON) -c "from src.python.dft_output import *; print('dft_output OK')"
	$(PYTHON) main.py

# Install Python dependencies
install:
	pip install numpy matplotlib

# Clean build artifacts
clean:
	rm -f $(PYMOD) *.mod *.o
	rm -rf output/ __pycache__ src/python/__pycache__
	rm -f test_results.json example_input.json