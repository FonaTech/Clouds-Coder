#!/usr/bin/env python3
"""
Mixed-Granularity E(3)-mu-GNN
-----------------------------

This module implements a three-layer atomistic GNN coupling local bonding,
long-range electrostatic/polarization physics, and time-reversal-aware spins.

Architecture overview:
    1. Local atomic layer (parity-aware O(3)):
       Learns the short-range potential energy surface and tensor features.

    2. Electrostatic/domain layer:
       Couples electric response to constrained QEq, periodic PME/Ewald,
       self-consistent polarization, and D4 dispersion.

    3. Spin/domain layer:
       Learns Heisenberg exchange J, single-ion anisotropy Di, and axial DMI
       while enforcing exact invariance under simultaneous spin reversal.

Effective Hamiltonian:
    H_eff = E_short + E_QEq + E_PME + E_D4 + E_spin + E_response
    E_response = -mu.e - 0.5 e^T alpha e

Forces are obtained analytically through autograd:
    F_i = -dH_eff/dR_i  (Formula 10, 11)

This keeps the energy-force relation self-consistent, even when the field
response terms are active.

Key components:
    MixedGranularityE3GNN — complete three-layer architecture.
    DualLayerFieldModel    — top-level model combining ground and response layers.
    BackupGroundModel      — ground-state energy model.
    BackupResponseModel    — dipole / polarizability response model.
    FastEquivariantBlock   — SO(3) message-passing block.
    FastEquivariantBlockO3 — O(3) parity-aware message-passing block.
    train_dual_layer       — training entry point for base / response / joint modes.
    AutoSearchEngine       — greedy random search with a lightweight GP surrogate.
    ModernE3MUGui          — default PyQt6 research and training interface.
    App                    — retained legacy Tkinter interface.
"""

# ══════════════════════════════════════════════════════════════════════════
# SECTION: Imports
# Standard library, third-party scientific stack, ASE, and PyG dependencies.
# ══════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import ast
import argparse
import collections
import copy
import gc
import hashlib
import importlib.util
import io
import itertools
import json
import math
import os
import queue
import re
import subprocess
import sys
import threading
import time
import traceback
from collections.abc import Iterable
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

try:
    from scipy.spatial import cKDTree as _SciPyKDTree
except Exception:
    _SciPyKDTree = None

try:
    import tkinter as tk
    import tkinter.font as tkfont
    from tkinter import filedialog, messagebox, ttk
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

    class _UnavailableTkWidget:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            raise RuntimeError(
                "Tkinter is unavailable. Install the platform Tk package or use "
                "the headless e3mu API."
            )

    class _UnavailableTkModule:
        Tk = _UnavailableTkWidget
        Canvas = _UnavailableTkWidget
        Frame = _UnavailableTkWidget
        Label = _UnavailableTkWidget
        Text = _UnavailableTkWidget
        PanedWindow = _UnavailableTkWidget
        Variable = _UnavailableTkWidget
        StringVar = _UnavailableTkWidget
        BooleanVar = _UnavailableTkWidget
        TclError = RuntimeError

    class _UnavailableTkNamespace:
        def __getattr__(self, _name: str) -> Any:
            return _UnavailableTkWidget

    tk = _UnavailableTkModule()  # type: ignore[assignment]
    tkfont = _UnavailableTkNamespace()  # type: ignore[assignment]
    ttk = _UnavailableTkNamespace()  # type: ignore[assignment]
    filedialog = _UnavailableTkNamespace()  # type: ignore[assignment]
    messagebox = _UnavailableTkNamespace()  # type: ignore[assignment]

from ase import Atoms
from ase.data import atomic_numbers as ASE_ATOMIC_NUMBERS
from ase.data import chemical_symbols as ASE_CHEMICAL_SYMBOLS
from ase.io.extxyz import key_val_str_to_dict
from ase.neighborlist import neighbor_list

from torch_geometric.data import Batch as _TGBatch
from torch_geometric.data import Data as _TGData

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
    HAS_PYQT6 = True
except Exception:
    class _UnavailableQtBase:
        pass

    class _UnavailableQtSignal:
        def connect(self, *_args: Any, **_kwargs: Any) -> None:
            pass

        def emit(self, *_args: Any, **_kwargs: Any) -> None:
            pass

    class _UnavailableQtCore:
        QObject = _UnavailableQtBase

        @staticmethod
        def pyqtSignal(*_args: Any, **_kwargs: Any) -> _UnavailableQtSignal:
            return _UnavailableQtSignal()

        @staticmethod
        def pyqtProperty(_value_type: Any) -> Callable[[Any], property]:
            return lambda getter: property(getter)

        @staticmethod
        def pyqtSlot(*_args: Any, **_kwargs: Any) -> Callable[[Any], Any]:
            return lambda function: function

    class _UnavailableQtWidgets:
        QAbstractButton = _UnavailableQtBase
        QFrame = _UnavailableQtBase
        QMainWindow = _UnavailableQtBase
        QStyledItemDelegate = _UnavailableQtBase

    QtCore = _UnavailableQtCore()  # type: ignore[assignment]
    QtGui = object()  # type: ignore[assignment]
    QtWidgets = _UnavailableQtWidgets()  # type: ignore[assignment]
    HAS_PYQT6 = False

# Optional physics/data backends. The core model remains importable without them;
# enabling the corresponding layer raises a focused dependency error.
try:
    import h5py
    HAS_H5PY = True
except Exception:
    h5py = None  # type: ignore[assignment]
    HAS_H5PY = False

try:
    import pyarrow.parquet as _pyarrow_parquet
    HAS_PYARROW = True
except Exception:
    _pyarrow_parquet = None  # type: ignore[assignment]
    HAS_PYARROW = False

try:
    import torchpme
    HAS_TORCHPME = True
except Exception:
    torchpme = None  # type: ignore[assignment]
    HAS_TORCHPME = False

try:
    import tad_dftd4
    HAS_TAD_DFTD4 = True
except Exception:
    tad_dftd4 = None  # type: ignore[assignment]
    HAS_TAD_DFTD4 = False

try:
    import dftd4 as _official_dftd4
    HAS_OFFICIAL_DFTD4 = True
except Exception:
    _official_dftd4 = None  # type: ignore[assignment]
    HAS_OFFICIAL_DFTD4 = False


# alpha[Ang^3] * E[V/Ang]^2 * this factor gives energy in eV.
ALPHA_VOLUME_TO_EV_PER_FIELD2 = 0.06944615422483141
COULOMB_EV_ANGSTROM = 14.3996454784255
MU_B_EV_PER_TESLA = 5.7883817982e-5
HDF5_SCHEMA_VERSION = "e3mu-hdf5-v1"
COMPOSITE_HDF5_SCHEMA_VERSION = "e3mu-composite-hdf5-v1"
OMAT24_BYTE_SHARD_SCHEMA_VERSION = "hdf5-byte-shards-v1"
OMAT24_MATERIALIZED_SCHEMA_VERSION = "hdf5-materialized-parquet-v1"
OMAT24_PACKED_SCHEMA_VERSION = "hdf5-packed-structures-v1"
HDF5_CANONICAL_ROOT_GROUPS: Tuple[str, ...] = (
    "structures",
    "labels",
    "masks",
    "metadata",
)
HDF5_METADATA_FIELDS: Tuple[str, ...] = (
    "source",
    "method_id",
    "system_id",
    "group_id",
    "split",
    "sample_id",
    "parent_id",
    "domain",
    "energy_reference",
    "provenance_id",
    "dataset_role",
    "curriculum_role",
)
_TORCH_RUNTIME_LOCK = threading.RLock()


@contextmanager
def _isolated_torch_runtime() -> Any:
    """Serialize model construction and restore process-global torch state."""
    with _TORCH_RUNTIME_LOCK:
        previous_dtype = torch.get_default_dtype()
        cpu_rng_state = torch.random.get_rng_state()
        try:
            yield
        finally:
            torch.set_default_dtype(previous_dtype)
            torch.random.set_rng_state(cpu_rng_state)

# Optional MACE neighborhood builder — faster and PBC-correct compared to ASE.
# Falls back to ase.neighborlist transparently when mace is not installed.
HAS_MACE_NEIGHBORHOOD = False
_mace_get_neighborhood = None
try:
    from mace.data.neighborhood import get_neighborhood as _get_neighborhood

    _mace_get_neighborhood = _get_neighborhood
    HAS_MACE_NEIGHBORHOOD = True
except Exception:
    HAS_MACE_NEIGHBORHOOD = False



# ══════════════════════════════════════════════════════════════════════════
# SECTION: Low-Level Utility Functions
# Time formatting, dtype control, and input-parsing helpers used throughout
# the data loading and configuration pipeline.
# ══════════════════════════════════════════════════════════════════════════

def _now() -> str:
    """Return current local time as a formatted string for log prefixes."""
    return time.strftime("%Y-%m-%d %H:%M:%S")


def set_default_dtype(dtype: str) -> None:
    """Set PyTorch's global default floating-point dtype.

    Args:
        dtype: Either 'float32' or 'float64'.  Any other value raises ValueError.
    """
    d = str(dtype or "float32").strip().lower()
    if d not in ("float32", "float64"):
        raise ValueError("dtype must be 'float32' or 'float64'")
    torch.set_default_dtype(torch.float32 if d == "float32" else torch.float64)


def _mps_is_available() -> bool:
    try:
        return bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
    except Exception:
        return False


def _default_device_name() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if _mps_is_available():
        return "mps"
    return "cpu"


def _process_rss_bytes() -> int:
    """Return resident memory without requiring psutil at runtime."""
    try:
        import resource

        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        # macOS reports bytes; Linux reports KiB. This is a peak fallback only.
        return value if sys.platform == "darwin" else value * 1024
    except Exception:
        return 0


def _memory_snapshot(device: torch.device) -> Dict[str, float]:
    rss = 0
    try:
        import psutil  # type: ignore[import-not-found]

        rss = int(psutil.Process().memory_info().rss)
    except Exception:
        rss = _process_rss_bytes()
    snapshot = {
        "rss_mib": float(rss) / float(1 << 20),
        "mps_active_mib": 0.0,
        "mps_driver_mib": 0.0,
        "mps_cache_mib": 0.0,
    }
    if device.type == "mps":
        active = int(torch.mps.current_allocated_memory())
        driver = int(torch.mps.driver_allocated_memory())
        snapshot["mps_active_mib"] = active / float(1 << 20)
        snapshot["mps_driver_mib"] = driver / float(1 << 20)
        snapshot["mps_cache_mib"] = max(0, driver - active) / float(1 << 20)
    return snapshot


def resolve_device(name: Optional[str], *, dtype: str = "float32") -> Tuple[torch.device, str]:
    requested = str(name or "auto").strip().lower()
    if requested == "auto":
        requested = _default_device_name()
    if requested == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA was requested but is not available")
    if requested == "mps" and not _mps_is_available():
        raise ValueError("MPS was requested but is not available")
    if requested not in ("cpu", "mps", "cuda"):
        raise ValueError("device must be one of: auto, cpu, mps, cuda")
    runtime_dtype = str(dtype).lower()
    if requested == "mps" and runtime_dtype == "float64":
        runtime_dtype = "float32"
    return torch.device(requested), runtime_dtype


def _available_cpu_threads() -> int:
    """Return the CPU concurrency available to this process."""
    try:
        affinity = getattr(os, "sched_getaffinity", None)
        if callable(affinity):
            allowed = len(affinity(0))
            if allowed > 0:
                return int(allowed)
    except (OSError, TypeError, ValueError):
        pass
    return max(1, int(os.cpu_count() or 1))


def _parse_cpu_threads(value: Any) -> Any:
    """Normalize a CPU-thread request to ``"auto"`` or a positive integer."""
    if value is None:
        return "auto"
    if isinstance(value, str):
        text = value.strip().lower()
        if not text or text == "auto":
            return "auto"
        try:
            value = int(text)
        except ValueError as exc:
            raise ValueError(
                f"cpu_threads must be 'auto' or a positive integer, got {value!r}"
            ) from exc
    if isinstance(value, bool):
        raise ValueError("cpu_threads must be 'auto' or a positive integer")
    try:
        threads = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"cpu_threads must be 'auto' or a positive integer, got {value!r}"
        ) from exc
    if threads < 1:
        raise ValueError(f"cpu_threads must be at least 1, got {threads}")
    return threads


def _resolve_cpu_thread_policy(requested: Any, device: torch.device) -> Dict[str, Any]:
    """Resolve CPU threading without mutating the process-wide PyTorch runtime."""
    normalized = _parse_cpu_threads(requested)
    available = _available_cpu_threads()
    source = "user"
    if normalized == "auto":
        environment_override = os.environ.get("E3MU_NUM_THREADS", "").strip()
        if environment_override:
            effective = int(_parse_cpu_threads(environment_override))
            source = "E3MU_NUM_THREADS"
        elif device.type == "cpu":
            effective = available
            source = "auto-cpu-all"
        else:
            # Accelerator execution needs only a bounded CPU helper pool. Four
            # threads overlap small fallbacks and preparation without competing
            # heavily with MPS/CUDA driver work.
            effective = min(4, available)
            source = f"auto-{device.type}-helper"
    else:
        effective = min(int(normalized), available)
        if int(normalized) > available:
            source = "user-clamped-to-available"
    return {
        "requested": normalized,
        "effective": max(1, int(effective)),
        "available": int(available),
        "source": source,
        "inherited_omp": os.environ.get("OMP_NUM_THREADS"),
    }


def _configure_torch_cpu_threads(requested: Any, device: torch.device) -> Dict[str, Any]:
    """Apply the process-wide PyTorch intra-op thread policy.

    PyTorch reads ``OMP_NUM_THREADS`` during import. Some macOS/Conda launch
    environments set it to one, so relying on the inherited value can silently
    serialize CPU training. An explicit ``torch.set_num_threads`` call remains
    effective after import and behaves consistently on macOS, Linux, and Windows.
    """
    policy = _resolve_cpu_thread_policy(requested, device)
    torch.set_num_threads(int(policy["effective"]))
    return {
        **policy,
        "effective": int(torch.get_num_threads()),
        "interop": int(torch.get_num_interop_threads()),
    }


def parse_vector3(v: Any, *, name: str = "vector") -> np.ndarray:
    """Parse a 3-vector from a variety of Python/string representations.

    Handles list/tuple/ndarray of length 3, or a string that can be a
    Python literal (e.g. "[1, 2, 3]") or whitespace/comma-separated floats.

    Args:
        v:    Input to parse — list, tuple, ndarray, or str.
        name: Descriptive name used in error messages.

    Returns:
        float64 ndarray of shape (3,).

    Raises:
        ValueError: If the input cannot be interpreted as a 3-vector.
    """
    if v is None:
        raise ValueError(f"{name} is None")
    if isinstance(v, (list, tuple, np.ndarray)) and len(v) == 3:
        return np.asarray(v, dtype=float)
    if isinstance(v, str):
        s = v.strip()
        try:
            obj = ast.literal_eval(s)
            if isinstance(obj, (list, tuple)) and len(obj) == 3:
                return np.asarray(obj, dtype=float)
        except Exception:
            pass
        parts = s.replace(",", " ").split()
        if len(parts) == 3:
            return np.asarray([float(x) for x in parts], dtype=float)
    raise ValueError(f"Could not parse {name} as 3-vector from: {v!r}")


def parse_matrix3x3(v: Any, *, name: str = "matrix") -> np.ndarray:
    """Parse a 3x3 matrix from array, nested list, flat list, or string.

    Accepts:
        - ndarray of shape (3, 3) or size 9.
        - List/tuple of 3 rows (each length 3) or flat length-9 sequence.
        - String containing a Python literal or 9 whitespace/comma-separated floats.

    Args:
        v:    Input to parse.
        name: Descriptive name for error messages.

    Returns:
        float64 ndarray of shape (3, 3).

    Raises:
        ValueError: If the input cannot be reshaped to (3, 3).
    """
    if v is None:
        raise ValueError(f"{name} is None")
    if isinstance(v, np.ndarray):
        arr = np.asarray(v, dtype=float)
        if arr.shape == (3, 3):
            return arr
        if arr.size == 9:
            return arr.reshape(3, 3)
    if isinstance(v, (list, tuple)):
        if len(v) == 3 and all(isinstance(r, (list, tuple, np.ndarray)) and len(r) == 3 for r in v):
            return np.asarray(v, dtype=float)
        if len(v) == 9:
            return np.asarray(v, dtype=float).reshape(3, 3)
    if isinstance(v, str):
        s = v.strip()
        try:
            obj = ast.literal_eval(s)
            return parse_matrix3x3(obj, name=name)
        except Exception:
            pass
        parts = s.replace(",", " ").split()
        if len(parts) == 9:
            return np.asarray([float(x) for x in parts], dtype=float).reshape(3, 3)
    raise ValueError(f"Could not parse {name} as 3x3 from: {v!r}")


def _parse_pbc(v: Any) -> Tuple[bool, bool, bool]:
    """Parse periodic boundary condition flags into a 3-bool tuple.

    Accepts string triplets (e.g. "T F T"), bool/int lists, or numpy arrays.
    Returns (False, False, False) for any unrecognised input.

    Args:
        v: Representation of PBC flags.

    Returns:
        Tuple of three booleans (pbc_x, pbc_y, pbc_z).
    """
    if v is None:
        return (False, False, False)
    if isinstance(v, str):
        parts = v.strip().replace(",", " ").split()
        if len(parts) == 3:
            out = []
            for p in parts:
                p = p.strip()
                if p in ("1", "True", "true", "T", "t", "Y", "y", "yes", "on"):
                    out.append(True)
                else:
                    out.append(False)
            return (bool(out[0]), bool(out[1]), bool(out[2]))
        return (False, False, False)
    if isinstance(v, (list, tuple, np.ndarray)) and len(v) == 3:
        return (bool(v[0]), bool(v[1]), bool(v[2]))
    return (False, False, False)


def _open_text(path: str):
    """Open a plain-text or gzip-compressed text file for reading.

    Args:
        path: Filesystem path.  Files ending in '.gz' are decompressed on the fly.

    Returns:
        A text-mode file object.
    """
    if path.endswith(".gz"):
        import gzip
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "rt", encoding="utf-8", errors="replace")


def _parse_properties_spec(spec: str) -> List[Tuple[str, str, int]]:
    """Parse an extXYZ ``Properties`` header string into (name, type, count) triples.

    The extXYZ format encodes per-atom column layout as colon-separated triples, e.g.:
        "species:S:1:pos:R:3:forces:R:3"

    Args:
        spec: Raw Properties string from the comment line of an extXYZ frame.

    Returns:
        List of (column_name, dtype_char, width) triples.

    Raises:
        ValueError: If the spec cannot be split into complete triples.
    """
    parts = str(spec or "").strip().split(":")
    if not parts or len(parts) % 3 != 0:
        raise ValueError(f"Invalid Properties spec (expected triples): {spec!r}")
    out: List[Tuple[str, str, int]] = []
    for i in range(0, len(parts), 3):
        name = parts[i]
        typ = parts[i + 1]
        out.append((name, typ, int(parts[i + 2])))
    return out


# ══════════════════════════════════════════════════════════════════════════
# SECTION: Data Structures
# DatasetKeys, ExtXYZFrame, and the raw extXYZ file parser.
# These form the first stage of the data pipeline: disk → Python objects.
# ══════════════════════════════════════════════════════════════════════════

@dataclass
class DatasetKeys:
    """Configurable key names for physical quantities stored in extXYZ comment lines.

    Separating keys from code lets users with non-standard column names (e.g.
    from GPAW, VASP, or custom DFT outputs) connect their datasets without
    modifying any parsing logic.

    Attributes:
        energy_key:          Key for total system energy E_PES (0th-order, eV).
        forces_key:          Key for atomic force vectors F (eV/Angstrom).
        field_key:           Key for external electric field vector epsilon (eV/Angstrom/e).
        dipole_key:          Key for molecular dipole moment mu (e*Angstrom).
        polarizability_key:  Key for polarizability tensor alpha (Angstrom^3).
        total_charge_key:    Key for total system charge Q (e), used for charge-centre
                             correction when computing the dipole from partial charges.
    """
    energy_key: str = "energy"                       # E_PES (0th order)
    forces_key: str = "forces"                       # F (total atomic force)
    field_key: str = "field"                         # epsilon (external electric field)
    dipole_key: str = "dipole"                       # mu (1st-order response)
    polarizability_key: str = "polarizability"       # alpha (2nd-order response)
    total_charge_key: str = "total_charge"           # Q (for charge-centre correction)
    charges_key: str = "charges"
    atomic_dipoles_key: str = "atomic_dipoles"
    atomic_polarizability_key: str = "atomic_polarizability"
    c6_key: str = "c6"
    bec_key: str = "bec"
    spins_key: str = "spins"
    magnetic_moments_key: str = "magmoms"
    effective_field_key: str = "effective_field"
    source_key: str = "source"
    method_key: str = "method_id"
    system_key: str = "system_id"
    group_key: str = "group_id"
    split_key: str = "split"


@dataclass
class ExtXYZFrame:
    """Container for a single parsed extXYZ snapshot (one molecular geometry).

    This is an intermediate representation produced by ``load_extxyz_frames``
    before any graph construction.  All numerical data is stored as raw NumPy
    arrays so that graph building (and the associated cutoff / PBC logic) can
    be deferred until needed.

    Attributes:
        atomic_numbers:          Integer atomic numbers, shape (N,).
        positions:               Cartesian coordinates in Angstroms, shape (N, 3).
        cell:                    Lattice matrix in Angstroms, shape (3, 3).
                                 Set to 100*I for non-periodic systems.
        has_lattice:             True if the frame contains a ``Lattice`` key.
        pbc:                     Periodic boundary condition flags (x, y, z).
        energy:                  Total energy in eV (0 if absent).
        forces:                  Atomic forces in eV/Ang, shape (N, 3) (zeros if absent).
        field:                   External electric field in eV/Ang/e, shape (3,).
        dipole:                  Dipole moment in e*Ang, shape (3,).
        polarizability:          Polarizability tensor in Ang^3, shape (3, 3).
        total_charge:            Net charge in electrons.
        energy_weight:           1.0 if energy label present, else 0.0.
        forces_weight:           1.0 if force labels present, else 0.0.
        dipole_weight:           1.0 if dipole label present, else 0.0.
        polarizability_weight:   1.0 if polarizability label present, else 0.0.
    """
    atomic_numbers: np.ndarray
    positions: np.ndarray
    cell: np.ndarray
    has_lattice: bool
    pbc: Tuple[bool, bool, bool]
    energy: float
    forces: np.ndarray
    field: np.ndarray
    dipole: np.ndarray
    polarizability: np.ndarray
    total_charge: float
    energy_weight: float
    forces_weight: float
    dipole_weight: float
    polarizability_weight: float
    charges: Optional[np.ndarray] = None
    atomic_dipoles: Optional[np.ndarray] = None
    atomic_polarizability: Optional[np.ndarray] = None
    c6: Optional[np.ndarray] = None
    bec: Optional[np.ndarray] = None
    spins: Optional[np.ndarray] = None
    magnetic_moments: Optional[np.ndarray] = None
    effective_field: Optional[np.ndarray] = None
    source: str = "unknown"
    method_id: str = "unknown"
    system_id: str = "unknown"
    group_id: str = "unknown"


def load_extxyz_frames(
    path: str,
    keys: DatasetKeys,
    *,
    require_field: bool,
    stop_flag: Optional[Callable[[], bool]] = None,
    log: Optional[Callable[[str], None]] = None,
    max_frames: Optional[int] = None,
    sample_fraction: float = 1.0,
    sample_seed: int = 0,
) -> List[ExtXYZFrame]:
    """Parse an extended XYZ file into a list of raw ``ExtXYZFrame`` objects.

    Supports both plain text and gzip-compressed (.gz) files.  Per-atom
    properties are decoded according to the ``Properties`` key in each frame's
    comment line; missing labels produce zero-valued arrays with weight=0.

    Args:
        path:          Filesystem path to the extXYZ file.
        keys:          DatasetKeys mapping label names to their column identifiers.
        require_field: If True, raise KeyError when a frame lacks the field label.
        stop_flag:     Optional callable; parsing stops early when it returns True.
        log:           Optional logging callable for progress messages.

    Returns:
        List of ExtXYZFrame objects, one per successfully parsed frame.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        KeyError:          If ``require_field=True`` and a frame has no field label.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    if log: log(f"[{_now()}] Reading raw frames from {p.name} ...")

    fraction = float(sample_fraction)
    if not (0.0 < fraction <= 1.0):
        raise ValueError("sample_fraction must be in (0, 1]")
    frames: List[ExtXYZFrame] = []
    with _open_text(str(p)) as f:
        count = 0
        while True:
            if stop_flag is not None and stop_flag():
                break
            line = f.readline()
            if not line: break
            line = line.strip()
            if not line: continue

            # First line of each frame is the atom count.
            nat = int(line)
            comment = f.readline()
            if comment is None: break
            c = comment.strip()

            # Parse the comment line as a key=value dictionary (ASE convention).
            info: Dict[str, Any] = {}
            if c and "=" in c:
                try: info = key_val_str_to_dict(c)
                except Exception: info = {}

            group_value = str(info.get(keys.group_key, info.get("sample_id", count)))
            if fraction < 1.0:
                digest = hashlib.sha256(
                    f"{int(sample_seed)}|{group_value}".encode("utf-8")
                ).digest()
                selected = int.from_bytes(digest[:8], "big") / float(1 << 64) < fraction
                if not selected:
                    for _ in range(nat):
                        f.readline()
                    count += 1
                    if log and count % 5000 == 0:
                        log(f"[{_now()}] Scanned {count} frames...")
                    continue

            # Default Properties spec: species + pos (no forces).
            props = _parse_properties_spec(info.get("Properties", "species:S:1:pos:R:3"))
            symbols: List[str] = []
            zs: List[int] = []
            positions = np.zeros((nat, 3), dtype=float)
            forces: Optional[np.ndarray] = None
            force_names = {str(keys.forces_key), "forces", "force", "F"}
            per_atom: Dict[str, np.ndarray] = {}
            extra_names: Dict[str, Tuple[set, int]] = {
                "charges": ({str(keys.charges_key), "charges", "charge", "q", "hCHG"}, 1),
                "atomic_dipoles": ({str(keys.atomic_dipoles_key), "atomic_dipoles", "hVDIP"}, 3),
                "atomic_polarizability": ({str(keys.atomic_polarizability_key), "atomic_polarizability", "atPOL"}, -1),
                "c6": ({str(keys.c6_key), "c6", "C6", "atC6"}, 1),
                "bec": ({str(keys.bec_key), "bec", "BEC"}, 9),
                "spins": ({str(keys.spins_key), "spins", "spin"}, 3),
                "magnetic_moments": ({str(keys.magnetic_moments_key), "magmoms", "magmom", "magnetic_moments"}, -1),
                "effective_field": ({str(keys.effective_field_key), "effective_field", "spin_field"}, 3),
            }

            # Read per-atom rows, dispatching tokens by the Properties spec.
            for ai in range(nat):
                row = f.readline()
                tokens = row.strip().split()
                t = 0
                for name, _typ, count_p in props:
                    vals = tokens[t : t + count_p]
                    t += count_p
                    if name in ("species", "symbol") and count_p == 1:
                        symbols.append(str(vals[0]).strip())
                    elif name in ("Z", "atomic_number", "atomic_numbers") and count_p == 1:
                        zs.append(int(float(vals[0])))
                    elif name in ("pos", "positions") and count_p >= 3:
                        positions[ai, :] = [float(vals[0]), float(vals[1]), float(vals[2])]
                    elif name in force_names and count_p == 3:
                        if forces is None: forces = np.zeros((nat, 3), dtype=float)
                        forces[ai, :] = [float(vals[0]), float(vals[1]), float(vals[2])]
                    else:
                        for canonical, (aliases, expected) in extra_names.items():
                            if name not in aliases or (expected > 0 and count_p != expected):
                                continue
                            width = count_p
                            if canonical not in per_atom:
                                per_atom[canonical] = np.zeros((nat, width), dtype=float)
                            per_atom[canonical][ai, :] = [float(x) for x in vals]
                            break

            # Resolve atomic numbers: prefer explicit Z column over chemical symbols.
            if zs:
                atomic_numbers = np.asarray(zs, dtype=int)
            else:
                atomic_numbers = np.asarray([ASE_ATOMIC_NUMBERS[str(s).capitalize()] for s in symbols], dtype=int)

            # Cell / PBC handling: default to large vacuum box if no Lattice key.
            cell = info.get("Lattice", None)
            has_lattice = cell is not None
            if not has_lattice:
                cell_arr = np.eye(3, dtype=float) * 100.0
                pbc = _parse_pbc(info.get("pbc", None)) if "pbc" in info else (False, False, False)
            else:
                lat_raw = np.asarray(cell, dtype=float).reshape(3, 3)
                cell_arr = lat_raw
                pbc = _parse_pbc(info.get("pbc", None)) if "pbc" in info else (True, True, True)

            # Energy: first matching key wins; missing label → weight=0.
            energy_val = next((info[k] for k in (keys.energy_key, "energy") if k in info), None)
            energy = float(energy_val) if energy_val is not None else 0.0
            e_w = 1.0 if energy_val is not None else 0.0
            f_w = 1.0 if forces is not None else 0.0
            if forces is None: forces = np.zeros((nat, 3), dtype=float)

            # External field: required when ``require_field=True``.
            field_val = next((info[k] for k in (keys.field_key, "field") if k in info), None)
            if field_val is None:
                if require_field: raise KeyError(f"Missing '{keys.field_key}'")
                field = np.zeros(3, dtype=float)
            else:
                field = parse_vector3(field_val, name=keys.field_key)

            # Dipole moment (mu): 1st-order field response.
            dip = next((info[k] for k in (keys.dipole_key, "dipole") if k in info), None)
            if dip is None:
                dipole = np.zeros(3, dtype=float)
                d_w = 0.0
            else:
                dipole = parse_vector3(dip, name=keys.dipole_key)
                d_w = 1.0

            # Polarizability (alpha): 2nd-order field response.
            pol = next((info[k] for k in (keys.polarizability_key, "polarizability") if k in info), None)
            if pol is None:
                polarizability = np.zeros((3, 3), dtype=float)
                a_w = 0.0
            else:
                polarizability = parse_matrix3x3(pol, name=keys.polarizability_key)
                a_w = 1.0

            total_charge = float(info.get(keys.total_charge_key, 0.0))

            atomic_polar = per_atom.get("atomic_polarizability")
            if atomic_polar is not None and atomic_polar.shape[1] == 9:
                atomic_polar = atomic_polar.reshape(nat, 3, 3)
            elif atomic_polar is not None and atomic_polar.shape[1] == 1:
                atomic_polar = np.eye(3)[None, :, :] * atomic_polar.reshape(nat, 1, 1)
            bec = per_atom.get("bec")
            if bec is not None:
                bec = bec.reshape(nat, 3, 3)
            magmoms = per_atom.get("magnetic_moments")
            if magmoms is not None and magmoms.shape[1] == 1:
                magmoms = np.pad(magmoms, ((0, 0), (0, 2)))

            frames.append(ExtXYZFrame(
                atomic_numbers=atomic_numbers, positions=positions, cell=cell_arr, has_lattice=has_lattice,
                pbc=pbc, energy=energy, forces=forces, field=field, dipole=dipole, polarizability=polarizability,
                total_charge=total_charge, energy_weight=e_w, forces_weight=f_w, dipole_weight=d_w,
                polarizability_weight=a_w,
                charges=(None if "charges" not in per_atom else per_atom["charges"].reshape(nat)),
                atomic_dipoles=per_atom.get("atomic_dipoles"),
                atomic_polarizability=atomic_polar,
                c6=(None if "c6" not in per_atom else per_atom["c6"].reshape(nat)),
                bec=bec,
                spins=per_atom.get("spins"),
                magnetic_moments=magmoms,
                effective_field=per_atom.get("effective_field"),
                source=str(info.get(keys.source_key, "unknown")),
                method_id=str(info.get(keys.method_key, "unknown")),
                system_id=str(info.get(keys.system_key, "unknown")),
                group_id=group_value,
            ))
            count += 1
            if max_frames is not None and count >= int(max_frames):
                break
            if log and count % 5000 == 0:
                log(f"[{_now()}] Read {count} frames...")

    if log:
        suffix = f" from {count} scanned" if fraction < 1.0 else ""
        log(f"[{_now()}] Finished reading {len(frames)} frames{suffix}.")
    return frames


# ══════════════════════════════════════════════════════════════════════════
# SECTION: Core Data Structures — AtomicNumberTable, Configuration, AtomicData
# Bridge between parsed raw frames and PyG graph objects fed to the GNN.
# ══════════════════════════════════════════════════════════════════════════

class AtomicNumberTable:
    """Bidirectional mapping between atomic numbers and contiguous integer indices.

    The GNN embedding layer uses 0-based indices rather than atomic numbers
    directly (which can be sparse up to Z=118).  This table defines the
    mapping for the species present in the training dataset.

    Attributes:
        zs:          Ordered list of unique atomic numbers (e.g. [1, 6, 8]).
        z_to_index:  Dict mapping Z → contiguous index.
    """
    def __init__(self, zs: Sequence[int]):
        self.zs = [int(z) for z in zs]
        self.z_to_index = {int(z): i for i, z in enumerate(self.zs)}
    def __len__(self) -> int:
        return len(self.zs)


def _fast_nonperiodic_neighborhood(
    positions: np.ndarray,
    cutoff: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """Build a deterministic directed neighbor list without ASE overhead."""
    coordinates = np.asarray(positions, dtype=np.float64).reshape(-1, 3)
    atom_count = int(coordinates.shape[0])
    if atom_count <= 1:
        return (
            np.empty((2, 0), dtype=np.int64),
            np.empty((0, 3), dtype=np.float64),
        )
    if atom_count <= 512 or _SciPyKDTree is None:
        # The exact vectorized path is faster for typical atomistic structures
        # and makes the cutoff decision directly in float64 with no candidates.
        delta = coordinates[:, None, :] - coordinates[None, :, :]
        distance2 = np.einsum("ijk,ijk->ij", delta, delta)
        undirected = np.argwhere(
            np.triu(distance2 < float(cutoff) ** 2, k=1)
        ).astype(np.int64, copy=False)
    else:
        candidates = _SciPyKDTree(coordinates).query_pairs(
            np.nextafter(float(cutoff), math.inf),
            eps=0.0,
            output_type="ndarray",
        )
        candidates = np.asarray(candidates, dtype=np.int64).reshape(-1, 2)
        if candidates.size:
            # Recheck candidates in float64 with the same strict cutoff rule as
            # ASE. KD-tree only accelerates discovery; it never decides labels.
            delta = coordinates[candidates[:, 0]] - coordinates[candidates[:, 1]]
            distance2 = np.einsum("ij,ij->i", delta, delta)
            undirected = candidates[distance2 < float(cutoff) ** 2]
        else:
            undirected = candidates
    if undirected.size == 0:
        return (
            np.empty((2, 0), dtype=np.int64),
            np.empty((0, 3), dtype=np.float64),
        )
    order = np.lexsort((undirected[:, 1], undirected[:, 0]))
    undirected = undirected[order]
    sources = np.concatenate([undirected[:, 0], undirected[:, 1]])
    destinations = np.concatenate([undirected[:, 1], undirected[:, 0]])
    directed_order = np.lexsort((destinations, sources))
    edge_index = np.stack(
        [sources[directed_order], destinations[directed_order]], axis=0
    ).astype(np.int64, copy=False)
    shifts = np.zeros((edge_index.shape[1], 3), dtype=np.float64)
    return edge_index, shifts


@dataclass
class Configuration:
    """Intermediate data object holding geometry + labels for one molecular configuration.

    Sits between raw ``ExtXYZFrame`` (disk I/O) and ``AtomicData`` (graph object).
    Provides a clean interface for dataset subsetting and train/val splitting without
    triggering expensive neighbor-list computation.

    Attributes:
        atomic_numbers:    Integer Z values, shape (N,).
        positions:         Cartesian positions in Angstroms, shape (N, 3).
        properties:        Dict of physical labels (energy, forces, field, dipole, …).
        property_weights:  Dict of per-label training weights (0 = label absent).
        cell:              Lattice matrix (3, 3); None interpreted as aperiodic.
        pbc:               Periodic boundary flags (x, y, z).
        weight:            Overall sample weight (default 1.0).
        config_type:       Human-readable tag (e.g. "Default", "transition_state").
        head:              Multi-head training target identifier (default "Default").
    """
    atomic_numbers: np.ndarray
    positions: np.ndarray
    properties: Dict[str, Any]
    property_weights: Dict[str, float]
    cell: Optional[np.ndarray] = None
    pbc: Tuple[bool, bool, bool] = (False, False, False)
    weight: float = 1.0
    config_type: str = "Default"
    head: str = "Default"


class AtomicData(_TGData):
    """PyG graph object consumed directly by the model.

    This container sits at the final step of the data pipeline:
        ExtXYZFrame / Configuration -> AtomicData -> Batched PyG graph

    In addition to geometry and graph connectivity, it stores all supervised
    labels and their per-target weights so the training loop can assemble the
    multi-objective loss without any extra bookkeeping.
    """

    @staticmethod
    def from_config(
        cfg: Configuration,
        *,
        z_table: AtomicNumberTable,
        cutoff: float,
        topology: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    ) -> "AtomicData":
        cell_np = np.asarray(cfg.cell if cfg.cell is not None else np.eye(3) * 100.0, dtype=float).reshape(3, 3).copy()
        if topology is None:
            edge_index_np, shifts_np = _configuration_neighbor_topology(
                cfg, cutoff=float(cutoff), cell=cell_np
            )
        else:
            edge_index_np, shifts_np = topology
        edge_index = torch.tensor(
            np.asarray(edge_index_np, dtype=np.int64), dtype=torch.long
        )
        shifts = torch.tensor(
            np.asarray(shifts_np, dtype=float), dtype=torch.get_default_dtype()
        )
        atom_types = torch.tensor([z_table.z_to_index[int(z)] for z in cfg.atomic_numbers], dtype=torch.long)
        
        cell = cell_np
        data = AtomicData(
            positions=torch.tensor(np.asarray(cfg.positions, dtype=float), dtype=torch.get_default_dtype()),
            atom_types=atom_types,
            atomic_numbers=torch.tensor(
                np.asarray(cfg.atomic_numbers, dtype=np.int64), dtype=torch.long
            ),
            edge_index=edge_index,
            shifts=shifts,
            cell=torch.tensor(cell, dtype=torch.get_default_dtype()),
            pbc=torch.tensor(np.asarray(cfg.pbc, dtype=bool), dtype=torch.bool).view(1, 3),
        )
        data.num_nodes = int(atom_types.numel())

        props = dict(cfg.properties or {})
        wts = dict(cfg.property_weights or {})
        data.group_id = str(props.get("group_id", "unknown"))
        data.sample_id = str(props.get("sample_id", data.group_id))
        data.dataset_role = str(props.get("dataset_role", "unknown"))

        has_energy = "energy" in props
        has_forces = "forces" in props
        data.energy = torch.tensor(float(props.get("energy", 0.0)), dtype=torch.get_default_dtype())
        data.forces = torch.tensor(
            np.asarray(props.get("forces", np.zeros((int(data.num_nodes), 3))), dtype=float),
            dtype=torch.get_default_dtype(),
        ).reshape(int(data.num_nodes), 3)

        if "field" in props:
            data.field = torch.tensor(np.asarray(props["field"], dtype=float), dtype=torch.get_default_dtype()).view(1, 3)
        else:
            data.field = torch.zeros((1, 3), dtype=torch.get_default_dtype())

        if "dipole" in props:
            data.dipole = torch.tensor(np.asarray(props["dipole"], dtype=float), dtype=torch.get_default_dtype()).view(1, 3)
        else:
            data.dipole = torch.zeros((1, 3), dtype=torch.get_default_dtype())

        if "polarizability" in props:
            data.polarizability = torch.tensor(np.asarray(props["polarizability"], dtype=float), dtype=torch.get_default_dtype()).view(1, 3, 3)
        else:
            data.polarizability = torch.zeros((1, 3, 3), dtype=torch.get_default_dtype())

        data.total_charge = torch.tensor(float(props.get("total_charge", 0.0)), dtype=torch.get_default_dtype())

        # Per-property weights (0 for missing labels).
        data.energy_weight = torch.tensor(
            float(wts.get("energy", 1.0 if has_energy else 0.0)), dtype=torch.get_default_dtype()
        )
        data.forces_weight = torch.tensor(
            float(wts.get("forces", 1.0 if has_forces else 0.0)), dtype=torch.get_default_dtype()
        )
        data.dipole_weight = torch.tensor(float(wts.get("dipole", 0.0)), dtype=torch.get_default_dtype()).view(1, 1)
        data.polarizability_weight = torch.tensor(float(wts.get("polarizability", 0.0)), dtype=torch.get_default_dtype())
        per_atom_shapes = {
            "charges": (-1,),
            "atomic_dipoles": (-1, 3),
            "atomic_polarizability": (-1, 3, 3),
            "c6": (-1,),
            "bec": (-1, 3, 3),
            "spins": (-1, 3),
            "magnetic_moments": (-1, 3),
            "effective_field": (-1, 3),
            "Di": (-1, 3, 3),
        }
        for name, shape in per_atom_shapes.items():
            value = props.get(name)
            if value is None:
                value_tensor = torch.zeros(
                    tuple(int(data.num_nodes) if dim == -1 else dim for dim in shape),
                    dtype=torch.get_default_dtype(),
                )
                present = 0.0
            else:
                value_tensor = torch.tensor(np.asarray(value, dtype=float), dtype=torch.get_default_dtype()).reshape(
                    tuple(int(data.num_nodes) if dim == -1 else dim for dim in shape)
                )
                present = 1.0
            setattr(data, name, value_tensor)
            setattr(data, f"{name}_weight", torch.tensor(float(wts.get(name, present)), dtype=torch.get_default_dtype()))
        structure_shapes = {
            "J_effective": (),
            "DMI_effective": (1, 3),
            "Di_effective": (1, 3, 3),
            "spin_mapping_rmse": (),
        }
        for name, shape in structure_shapes.items():
            value = props.get(name)
            present = float(value is not None)
            if value is None:
                value_tensor = torch.zeros(shape or (), dtype=torch.get_default_dtype())
            else:
                value_tensor = torch.tensor(
                    np.asarray(value, dtype=float), dtype=torch.get_default_dtype()
                ).reshape(shape or ())
            setattr(data, name, value_tensor)
            setattr(data, f"{name}_weight", torch.tensor(float(wts.get(name, present)), dtype=torch.get_default_dtype()))
        data.source = str(props.get("source", "unknown"))
        data.method_id = str(props.get("method_id", "unknown"))
        data.system_id = str(props.get("system_id", "unknown"))
        data.group_id = str(props.get("group_id", "unknown"))
        data.sample_id = str(props.get("sample_id", data.group_id))
        return data


def _configuration_neighbor_topology(
    cfg: Configuration,
    *,
    cutoff: float,
    cell: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Build the exact topology used by both materialized and streamed graphs."""
    cell_np = np.asarray(
        cell if cell is not None else (
            cfg.cell if cfg.cell is not None else np.eye(3) * 100.0
        ),
        dtype=float,
    ).reshape(3, 3)
    if not any(bool(value) for value in cfg.pbc):
        return _fast_nonperiodic_neighborhood(
            np.asarray(cfg.positions, dtype=float), float(cutoff)
        )
    if HAS_MACE_NEIGHBORHOOD and _mace_get_neighborhood is not None:
        edge_index, shifts, _unit_shifts, _cell_used = _mace_get_neighborhood(
            positions=np.asarray(cfg.positions, dtype=float),
            cutoff=float(cutoff),
            pbc=cfg.pbc,
            cell=cell_np,
            true_self_interaction=False,
        )
        return (
            np.asarray(edge_index, dtype=np.int64),
            np.asarray(shifts, dtype=np.float64),
        )
    atoms = Atoms(
        numbers=cfg.atomic_numbers,
        positions=cfg.positions,
        cell=cell_np,
        pbc=cfg.pbc,
    )
    i, j, unit_shifts = neighbor_list("ijS", atoms, cutoff=float(cutoff))
    shift_vectors = np.einsum(
        "ni,ij->nj",
        np.asarray(unit_shifts, dtype=float),
        np.asarray(atoms.cell.array, dtype=float),
    )
    return np.stack([i, j], axis=0).astype(np.int64), shift_vectors


def load_extxyz_configurations(
    path: str,
    keys: DatasetKeys,
    *,
    require_energy: bool,
    require_forces: bool,
    require_field: bool,
    stop_flag: Optional[Callable[[], bool]] = None,
    log: Optional[Callable[[str], None]] = None,
    max_frames: Optional[int] = None,
    sample_fraction: float = 1.0,
    sample_seed: int = 0,
) -> Tuple[List[Configuration], List[np.ndarray]]:
    """Convert raw extXYZ frames into ``Configuration`` objects plus fields.

    The returned configurations keep labels in plain NumPy form and delay graph
    construction until the cutoff and element table are known.

    Args:
        path:           Input extXYZ file.
        keys:           DatasetKeys describing label names in the file.
        require_energy: Require every frame to contain an energy label.
        require_forces: Require every frame to contain force labels.
        require_field:  Require every frame to contain an external field label.
        stop_flag:      Optional early-stop callback.
        log:            Optional progress logger.

    Returns:
        Tuple ``(configs, fields)`` where ``fields`` stores the per-frame
        external electric field vectors.

    Raises:
        KeyError: If a required label is missing from any frame.
    """
    frames = load_extxyz_frames(
        path,
        keys,
        require_field=require_field,
        stop_flag=stop_flag,
        log=log,
        max_frames=max_frames,
        sample_fraction=sample_fraction,
        sample_seed=sample_seed,
    )
    configs: List[Configuration] = []
    fields: List[np.ndarray] = []
    for fr in frames:
        if require_energy and fr.energy_weight <= 0.0:
            raise KeyError(f"Missing '{keys.energy_key}' in dataset: {path}")
        if require_forces and fr.forces_weight <= 0.0:
            raise KeyError(f"Missing '{keys.forces_key}' in dataset: {path}")

        props: Dict[str, Any] = {}
        wts: Dict[str, float] = {}
        if fr.energy_weight > 0.0:
            props["energy"] = float(fr.energy)
            wts["energy"] = float(fr.energy_weight)
        if fr.forces_weight > 0.0:
            props["forces"] = np.asarray(fr.forces, dtype=float)
            wts["forces"] = float(fr.forces_weight)
        props["field"] = np.asarray(fr.field, dtype=float).reshape(3)
        if fr.dipole_weight > 0.0:
            props["dipole"] = np.asarray(fr.dipole, dtype=float).reshape(3)
            wts["dipole"] = float(fr.dipole_weight)
        if fr.polarizability_weight > 0.0:
            props["polarizability"] = np.asarray(fr.polarizability, dtype=float).reshape(3, 3)
            wts["polarizability"] = float(fr.polarizability_weight)
        props["total_charge"] = float(fr.total_charge)
        for name in (
            "charges", "atomic_dipoles", "atomic_polarizability", "c6", "bec",
            "spins", "magnetic_moments", "effective_field",
        ):
            value = getattr(fr, name)
            if value is not None:
                props[name] = np.asarray(value, dtype=float)
                wts[name] = 1.0
        props["source"] = fr.source
        props["method_id"] = fr.method_id
        props["system_id"] = fr.system_id
        props["group_id"] = fr.group_id

        cell = np.asarray(fr.cell, dtype=float).reshape(3, 3) if fr.has_lattice else np.eye(3, dtype=float) * 100.0
        cfg = Configuration(
            atomic_numbers=np.asarray(fr.atomic_numbers, dtype=int),
            positions=np.asarray(fr.positions, dtype=float),
            properties=props,
            property_weights=wts,
            cell=cell,
            pbc=tuple(bool(x) for x in fr.pbc),
            weight=1.0,
            config_type="Default",
            head="Default",
        )
        configs.append(cfg)
        fields.append(np.asarray(fr.field, dtype=float).reshape(3))
    return configs, fields


def fit_atomic_energies_from_configs(configs: Sequence[Configuration], zs: Sequence[int]) -> np.ndarray:
    """Fit per-element atomic reference energies from labeled configurations.

    The fit uses composition counts with a weak ridge prior.  This remains
    finite when a small AutoSearch subset does not span every element or when
    several elemental composition columns are linearly dependent.
    """
    z_to_col = {int(z): i for i, z in enumerate(zs)}
    y: List[float] = []
    A: List[np.ndarray] = []
    weights: List[float] = []
    for cfg in configs:
        if cfg.properties.get("energy") is None:
            raise KeyError("Configuration missing 'energy' in properties")
        energy = float(cfg.properties["energy"])
        weight = float(cfg.property_weights.get("energy", 1.0))
        if not math.isfinite(energy) or not math.isfinite(weight) or weight <= 0.0:
            continue
        y.append(energy)
        weights.append(weight)
        counts = np.zeros((len(zs),), dtype=float)
        for z in np.asarray(cfg.atomic_numbers, dtype=int):
            counts[z_to_col[int(z)]] += 1.0
        A.append(counts)
    if not y:
        raise ValueError("Cannot fit atomic energies: empty dataset")

    A_arr = np.asarray(A, dtype=np.float64)
    y_arr = np.asarray(y, dtype=float)
    sample_scale = np.sqrt(np.asarray(weights, dtype=np.float64))
    A_weighted = A_arr * sample_scale[:, None]
    y_weighted = y_arr * sample_scale

    atoms_per_structure = np.sum(A_arr, axis=1)
    prior = float(np.median(y_arr / np.maximum(atoms_per_structure, 1.0)))
    largest_singular = float(np.linalg.norm(A_weighted, ord=2))
    ridge_root = max(1e-12, 1e-3 * largest_singular)
    augmented_a = np.concatenate(
        [A_weighted, ridge_root * np.eye(len(zs), dtype=np.float64)], axis=0
    )
    augmented_y = np.concatenate(
        [y_weighted, ridge_root * np.full(len(zs), prior, dtype=np.float64)]
    )
    x, *_ = np.linalg.lstsq(augmented_a, augmented_y, rcond=None)
    if not np.isfinite(x).all():
        raise FloatingPointError("Atomic reference-energy fit produced non-finite values")
    return np.asarray(x, dtype=float).reshape(-1)


def _prepare_legacy_dataset_role(
    configurations: Sequence[Configuration],
    *,
    role: str,
    suppress_ground_labels: bool,
) -> Tuple[List[Configuration], Dict[str, int]]:
    """Copy legacy configurations and isolate static/response supervision."""
    prepared: List[Configuration] = []
    masked = {"energy": 0, "forces": 0}
    for index, cfg in enumerate(configurations):
        properties = dict(cfg.properties)
        weights = dict(cfg.property_weights)
        original_group = str(properties.get("group_id", f"structure-{index}"))
        properties["group_id"] = f"{role}:{original_group}"
        properties["dataset_role"] = str(role)
        if suppress_ground_labels:
            for name in masked:
                if float(weights.get(name, 0.0)) > 0.0:
                    masked[name] += 1
                weights[name] = 0.0
        prepared.append(
            Configuration(
                atomic_numbers=cfg.atomic_numbers,
                positions=cfg.positions,
                properties=properties,
                property_weights=weights,
                cell=cfg.cell,
                pbc=cfg.pbc,
                weight=cfg.weight,
                config_type=cfg.config_type,
                head=cfg.head,
            )
        )
    return prepared, masked


def configs_to_atomicdata_list(
    configs: Sequence[Configuration],
    fields: Sequence[np.ndarray],
    *,
    z_table: AtomicNumberTable,
    r_max: float,
) -> List[AtomicData]:
    """Convert configurations into graph objects using a fixed cutoff and Z table."""
    out: List[AtomicData] = []
    for cfg, field_value in zip(configs, fields):
        cfg2 = Configuration(
            atomic_numbers=cfg.atomic_numbers,
            positions=cfg.positions,
            properties=dict(cfg.properties),
            property_weights=dict(cfg.property_weights),
            cell=cfg.cell,
            pbc=cfg.pbc,
            weight=cfg.weight,
            config_type=cfg.config_type,
            head=cfg.head,
        )
        cfg2.properties["field"] = np.asarray(field_value, dtype=float).reshape(3)
        out.append(AtomicData.from_config(cfg2, z_table=z_table, cutoff=float(r_max)))
    return out


HDF5_STRUCTURE_LABELS: Dict[str, Tuple[int, ...]] = {
    "energy": (),
    "energy_base": (),
    "energy_dispersion": (),
    "field": (3,),
    "dipole": (3,),
    "polarizability": (3, 3),
    "total_charge": (),
    "J_effective": (),
    "DMI_effective": (3,),
    "Di_effective": (3, 3),
    "spin_mapping_rmse": (),
    "spin_variant": (),
    "soc": (),
    # OMat24 publishes the symmetric Cauchy stress in eV/Angstrom^3.  The
    # current optimizer does not attach a stress loss, but canonical storage
    # retains the source label losslessly for future cell-gradient training.
    "stress": (3, 3),
    "stress_volume_normalized": (),
}
HDF5_ATOM_LABELS: Dict[str, Tuple[int, ...]] = {
    "forces": (3,),
    "forces_base": (3,),
    "forces_dispersion": (3,),
    "charges": (),
    "atomic_dipoles": (3,),
    "atomic_polarizability": (3, 3),
    "c6": (),
    "bec": (3, 3),
    "spins": (3,),
    "magnetic_moments": (3,),
    "effective_field": (3,),
    "Di": (3, 3),
}
HDF5_UNITS = {
    "atomic_numbers": "dimensionless",
    "cell": "angstrom",
    "pbc": "boolean",
    "positions": "angstrom",
    "energy": "eV",
    "energy_base": "eV",
    "energy_dispersion": "eV",
    "forces": "eV/angstrom",
    "forces_base": "eV/angstrom",
    "forces_dispersion": "eV/angstrom",
    "field": "V/angstrom",
    "dipole": "e*angstrom",
    "polarizability": "angstrom^3",
    "total_charge": "e",
    "charges": "e",
    "atomic_dipoles": "e*angstrom",
    "atomic_polarizability": "angstrom^3",
    "c6": "eV*angstrom^6",
    "bec": "e",
    "spins": "dimensionless",
    "magnetic_moments": "mu_B",
    "effective_field": "eV/spin",
    "Di": "eV",
    "J_effective": "eV",
    "DMI_effective": "eV",
    "Di_effective": "eV",
    "spin_mapping_rmse": "eV",
    "spin_variant": "integer_id",
    "soc": "boolean",
    "stress": "eV/angstrom^3",
    "stress_volume_normalized": "boolean",
}


def sha256_file(path: str, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def stable_split(group_id: str, *, train: int = 80, val: int = 10) -> str:
    bucket = int(hashlib.sha256(str(group_id).encode("utf-8")).hexdigest()[:8], 16) % 100
    if bucket < train:
        return "train"
    if bucket < train + val:
        return "val"
    return "test"


_DATASET_PREPARATION_EXPORTS = frozenset({
    "NEO_MANIFEST_VERSION",
    "NEO_HF_TIER_PATHS",
    "NEO_HF_REQUIRED_DOCUMENTS",
    "assign_stable_group_splits",
    "download_with_sha256",
    "write_hdf5_dataset",
    "write_hdf5_dataset_stream",
    "extxyz_to_hdf5",
    "rebuild_qm7x_hdf5",
    "extract_verified_zip_member",
    "scan_jarvis_multi_element_candidates",
    "select_jarvis_multi_element_candidates",
    "rebuild_jarvis_multi_element_hdf5",
    "select_jarvis_dfpt_candidates",
    "download_jarvis_dfpt_archives",
    "rebuild_jarvis_dfpt_hdf5",
    "rebuild_so3lr_hdf5",
    "rebuild_deepspin_hdf5",
    "scan_mptrj_magnetic_candidates",
    "select_mptrj_magnetic_candidates",
    "rebuild_mptrj_magnetic_hdf5",
    "rebuild_mptrj_large_hdf5",
    "select_static_mptrj_parquet_rows",
    "rebuild_static_mptrj_hdf5",
    "rebuild_scfnn_from_combined_extxyz",
    "rebuild_bec_from_combined_response",
    "select_neo_stratified_hdf5_indices",
    "build_neo_stratified_tier",
    "audit_neo_tier_hierarchy",
    "build_neo_mixed_dataset",
    "build_neo_smoke_dataset",
    "validate_neo_hdf5",
    "hdf5_dataset_summary",
    "build_neo_omat24_composite",
    "build_neo_composite_half",
    "embed_omat24_parquet_in_composite",
    "embed_neo_large_in_composite",
    "prepare_neo_huggingface_release",
    "generate_vasp_magnetic_jobs",
    "run_vasp_job",
    "attach_spin_energy_mappings",
    "collect_vasp_magnetic_jobs",
    "_base_magnetic_structures",
    "_initial_spin_vectors",
    "_order_atoms_for_vasp",
    "_spin_family",
    "_spin_mapping_features",
})


def _load_dataset_preparation_module() -> Any:
    """Load the sibling offline-tool module without relying on the CWD."""
    module_name = "Datasets_Preparation"
    source = Path(__file__).with_name(f"{module_name}.py").resolve()
    existing = sys.modules.get(module_name)
    if existing is not None:
        raw_path = getattr(existing, "__file__", None)
        if raw_path and Path(raw_path).resolve() == source:
            return existing
    if not source.is_file():
        raise ModuleNotFoundError(
            f"Offline dataset tools are unavailable: {source} does not exist"
        )
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load offline dataset tools from {source}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if sys.modules.get(module_name) is module:
            del sys.modules[module_name]
        raise
    return module


def __getattr__(name: str) -> Any:
    """Resolve legacy dataset-preparation APIs only when explicitly requested."""
    if name not in _DATASET_PREPARATION_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    preparation = _load_dataset_preparation_module()

    value = getattr(preparation, name)
    globals()[name] = value
    return value



def iter_hdf5_configurations(
    path: str,
    *,
    split: Optional[str] = None,
    sample_fraction: float = 1.0,
    sample_seed: int = 0,
    selected_indices: Optional[Sequence[int]] = None,
) -> Iterable[Configuration]:
    """Yield selected canonical structures while keeping HDF5 arrays on disk."""
    if not HAS_H5PY:
        raise RuntimeError("HDF5 support requires h5py")
    with h5py.File(path, "r") as handle:
        schema = str(handle.attrs.get("schema_version", ""))
        if schema not in {HDF5_SCHEMA_VERSION, COMPOSITE_HDF5_SCHEMA_VERSION}:
            raise ValueError(f"Unsupported HDF5 schema: {schema!r}")
        missing_groups = [
            name for name in HDF5_CANONICAL_ROOT_GROUPS if name not in handle
        ]
        if missing_groups:
            raise ValueError(
                "HDF5 file does not contain a canonical numerical payload: "
                + ", ".join(missing_groups)
            )
        structures, labels, masks, metadata_group = (
            handle["structures"], handle["labels"], handle["masks"], handle["metadata"]
        )
        atom_ptr = np.asarray(structures["atom_ptr"], dtype=np.int64)
        split_values = (
            [str(x) for x in metadata_group["split"].asstr()[:]]
            if split is not None else None
        )
        fraction = float(sample_fraction)
        if not (0.0 < fraction <= 1.0):
            raise ValueError("sample_fraction must be in (0, 1]")
        sampled_indices: Optional[set] = None
        if fraction < 1.0:
            group_values = (
                [str(x) for x in metadata_group["group_id"].asstr()[:]]
                if "group_id" in metadata_group
                else [f"structure-{index}" for index in range(len(atom_ptr) - 1)]
            )
            target_structures = max(2, int(round((len(atom_ptr) - 1) * fraction)))
            group_indices: Dict[str, List[int]] = {}
            for index, group in enumerate(group_values):
                group_indices.setdefault(group, []).append(index)
            ranked_groups = sorted(
                group_indices,
                key=lambda group: hashlib.sha256(
                    f"{int(sample_seed)}|{group}".encode("utf-8")
                ).hexdigest(),
            )
            for group, indices in group_indices.items():
                indices.sort(
                    key=lambda index: hashlib.sha256(
                        f"{int(sample_seed)}|{group}|{index}".encode("utf-8")
                    ).hexdigest()
                )
            sampled_indices = set()
            depth = 0
            while len(sampled_indices) < target_structures:
                made_progress = False
                for group in ranked_groups:
                    indices = group_indices[group]
                    if depth >= len(indices):
                        continue
                    sampled_indices.add(indices[depth])
                    made_progress = True
                    if len(sampled_indices) >= target_structures:
                        break
                if not made_progress:
                    break
                depth += 1
        index_filter = (
            None
            if selected_indices is None
            else {int(value) for value in selected_indices}
        )
        for index in range(len(atom_ptr) - 1):
            if index_filter is not None and index not in index_filter:
                continue
            if split is not None and split_values is not None and split_values[index] != split:
                continue
            if sampled_indices is not None and index not in sampled_indices:
                continue
            start, end = int(atom_ptr[index]), int(atom_ptr[index + 1])
            props: Dict[str, Any] = {}
            weights: Dict[str, float] = {}
            for name in HDF5_STRUCTURE_LABELS:
                if name not in masks or name not in labels:
                    continue
                if bool(masks[name][index]):
                    props[name] = np.asarray(labels[name][index])
                    if props[name].shape == ():
                        props[name] = float(props[name])
                    weights[name] = 1.0
            for name in HDF5_ATOM_LABELS:
                if name not in masks or name not in labels:
                    continue
                if bool(masks[name][index]):
                    props[name] = np.asarray(labels[name][start:end])
                    weights[name] = 1.0
            for name in HDF5_METADATA_FIELDS:
                if name in metadata_group:
                    props[name] = str(metadata_group[name].asstr()[index])
            yield Configuration(
                atomic_numbers=np.asarray(structures["atomic_numbers"][start:end], dtype=int),
                positions=np.asarray(structures["positions"][start:end], dtype=float),
                properties=props,
                property_weights=weights,
                cell=np.asarray(structures["cell"][index], dtype=float),
                pbc=tuple(bool(x) for x in structures["pbc"][index]),
                config_type="Default",
                head=str(props.get("method_id", "Default")),
            )


def load_hdf5_configurations(
    path: str,
    *,
    split: Optional[str] = None,
    sample_fraction: float = 1.0,
    sample_seed: int = 0,
    selected_indices: Optional[Sequence[int]] = None,
) -> List[Configuration]:
    """Materialize a selected canonical subset for graph construction/training."""
    return list(
        iter_hdf5_configurations(
            path,
            split=split,
            sample_fraction=sample_fraction,
            sample_seed=sample_seed,
            selected_indices=selected_indices,
        )
    )


HDF5_TOPOLOGY_CACHE_VERSION = "e3mu-topology-cache-v5-shift-dictionary"


def _compact_unsigned_dtype_for_upper_bound(upper_bound: int) -> np.dtype:
    """Return an unsigned dtype that safely represents a declared upper bound."""
    maximum = max(0, int(upper_bound))
    if maximum <= np.iinfo(np.uint8).max:
        return np.dtype(np.uint8)
    if maximum <= np.iinfo(np.uint16).max:
        return np.dtype(np.uint16)
    if maximum <= np.iinfo(np.uint32).max:
        return np.dtype(np.uint32)
    if maximum <= np.iinfo(np.uint64).max:
        return np.dtype(np.uint64)
    raise OverflowError(f"Cannot represent upper bound {maximum} with uint64")


def _encode_bitwise_shift_dictionary(
    shifts: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Encode nonzero float64 shift rows without changing their bit patterns."""
    exact = np.ascontiguousarray(shifts, dtype=np.float64).reshape(-1, 3)
    bits = exact.view(np.uint64).reshape(-1, 3)
    # An all-positive-zero row needs no stored value. Any other bit pattern,
    # including signed zero or a non-canonical NaN payload, is retained.
    local_indices = np.flatnonzero(np.any(bits != 0, axis=1))
    if local_indices.size == 0:
        return (
            np.empty((0,), dtype=np.uint64),
            np.empty((0,), dtype=np.uint64),
            np.empty((0, 3), dtype=np.float64),
        )
    unique_bits, codes = np.unique(
        bits[local_indices], axis=0, return_inverse=True
    )
    dictionary = (
        np.ascontiguousarray(unique_bits)
        .view(np.float64)
        .reshape(-1, 3)
    )
    return (
        local_indices.astype(np.uint64, copy=False),
        np.asarray(codes, dtype=np.uint64),
        dictionary,
    )


@dataclass
class HDF5StreamPlan:
    """Small in-memory index for an otherwise disk-resident canonical corpus."""

    path: str
    atom_ptr: np.ndarray
    group_ids: Tuple[str, ...]
    split_values: Tuple[str, ...]
    metadata_values: Dict[str, Tuple[str, ...]]
    label_masks: Dict[str, np.ndarray]
    train_indices: np.ndarray
    val_indices: np.ndarray
    elements: Tuple[int, ...]
    split_info: Dict[str, Any]
    source_size: int
    source_mtime_ns: int

    @property
    def selected_indices(self) -> np.ndarray:
        return np.sort(
            np.concatenate([self.train_indices, self.val_indices]).astype(
                np.int64, copy=False
            )
        )


def _curriculum_role_matches(value: str, mode: str) -> bool:
    """Return whether one canonical record participates in a training stage."""
    normalized = str(value or "all").strip().lower().replace("_", "-")
    selected_mode = str(mode or "joint").strip().lower()
    if normalized in {"", "all", "any", "legacy", "unknown", "mixed"}:
        return True
    tokens = {
        token.strip()
        for token in re.split(r"[,;+|/]", normalized)
        if token.strip()
    }
    aliases = {
        "base": {"base", "foundation", "l1", "ground"},
        "response": {"response", "l2", "l3", "domain", "spin"},
        "joint": {"joint", "mixed", "coupled"},
    }
    if selected_mode == "joint":
        return bool(tokens & (aliases["base"] | aliases["response"] | aliases["joint"]))
    return bool(tokens & aliases.get(selected_mode, {selected_mode}))


def _filter_hdf5_stream_plan_for_mode(
    plan: HDF5StreamPlan, mode: str
) -> HDF5StreamPlan:
    """Select stage-role indices while preserving legacy HDF5 behavior."""
    roles = plan.metadata_values.get("curriculum_role")
    if roles is None or not any(str(value).strip() for value in roles):
        return plan
    train = np.asarray(
        [
            int(index)
            for index in plan.train_indices
            if _curriculum_role_matches(roles[int(index)], mode)
        ],
        dtype=np.int64,
    )
    val = np.asarray(
        [
            int(index)
            for index in plan.val_indices
            if _curriculum_role_matches(roles[int(index)], mode)
        ],
        dtype=np.int64,
    )
    if train.size == 0 or val.size == 0:
        raise ValueError(
            f"Canonical curriculum role filter for mode={mode!r} produced "
            f"train={train.size}, val={val.size}."
        )
    split_info = dict(plan.split_info)
    split_info.update({
        "curriculum_mode": str(mode),
        "curriculum_filtered": True,
        "train_structures": int(train.size),
        "val_structures": int(val.size),
        "train_groups": len({plan.group_ids[int(index)] for index in train}),
        "val_groups": len({plan.group_ids[int(index)] for index in val}),
    })
    return replace(
        plan,
        train_indices=train,
        val_indices=val,
        split_info=split_info,
    )


def _group_stratified_hdf5_sample_indices(
    group_ids: Sequence[str], *, fraction: float, seed: int
) -> np.ndarray:
    """Match canonical group-aware subsetting without materializing structures."""
    count = len(group_ids)
    if not (0.0 < float(fraction) <= 1.0):
        raise ValueError("sample_fraction must be in (0, 1]")
    if float(fraction) >= 1.0 or count <= 2:
        return np.arange(count, dtype=np.int64)
    target = max(2, int(round(count * float(fraction))))
    group_indices: Dict[str, List[int]] = {}
    for index, group_id in enumerate(group_ids):
        group_indices.setdefault(str(group_id), []).append(index)
    ranked_groups = sorted(
        group_indices,
        key=lambda group: hashlib.sha256(
            f"{int(seed)}|{group}".encode("utf-8")
        ).hexdigest(),
    )
    for group, indices in group_indices.items():
        indices.sort(
            key=lambda index: hashlib.sha256(
                f"{int(seed)}|{group}|{index}".encode("utf-8")
            ).hexdigest()
        )
    selected: List[int] = []
    depth = 0
    while len(selected) < target:
        made_progress = False
        for group in ranked_groups:
            indices = group_indices[group]
            if depth >= len(indices):
                continue
            selected.append(int(indices[depth]))
            made_progress = True
            if len(selected) >= target:
                break
        if not made_progress:
            break
        depth += 1
    return np.asarray(sorted(selected), dtype=np.int64)


def prepare_hdf5_stream_plan(
    path: str,
    *,
    val_fraction: float,
    seed: int,
    sample_fraction: float = 1.0,
    sample_seed: int = 0,
    require_train_val: bool = True,
) -> HDF5StreamPlan:
    """Read only canonical indices, masks, and split metadata into memory."""
    if not HAS_H5PY:
        raise RuntimeError("HDF5 streaming requires h5py")
    resolved = str(Path(path).expanduser().resolve())
    source_stat = Path(resolved).stat()
    with h5py.File(resolved, "r") as handle:
        schema = str(handle.attrs.get("schema_version", ""))
        if schema not in {HDF5_SCHEMA_VERSION, COMPOSITE_HDF5_SCHEMA_VERSION}:
            raise ValueError(f"Unsupported HDF5 schema: {schema!r}")
        missing_groups = [
            name for name in HDF5_CANONICAL_ROOT_GROUPS if name not in handle
        ]
        if missing_groups:
            raise ValueError(
                "HDF5 file does not contain a canonical numerical payload: "
                + ", ".join(missing_groups)
            )
        structures = handle["structures"]
        metadata = handle["metadata"]
        masks = handle["masks"]
        atom_ptr = np.asarray(structures["atom_ptr"][:], dtype=np.int64)
        n_structures = len(atom_ptr) - 1
        group_ids = tuple(
            str(value) for value in metadata["group_id"].asstr()[:]
        )
        split_values = tuple(
            str(value).strip().lower() for value in metadata["split"].asstr()[:]
        )
        metadata_values = {
            name: tuple(str(value) for value in metadata[name].asstr()[:])
            for name in HDF5_METADATA_FIELDS
            if name in metadata
        }
        if len(group_ids) != n_structures or len(split_values) != n_structures:
            raise ValueError("Canonical metadata length does not match atom_ptr")
        selected = _group_stratified_hdf5_sample_indices(
            group_ids, fraction=float(sample_fraction), seed=int(sample_seed)
        )

        group_indices: Dict[str, List[int]] = {}
        group_split: Dict[str, str] = {}
        for raw_index in selected:
            index = int(raw_index)
            group_id = group_ids[index]
            group_indices.setdefault(group_id, []).append(index)
            split_name = split_values[index]
            if split_name in ("train", "val", "test"):
                previous = group_split.setdefault(group_id, split_name)
                if previous != split_name:
                    raise ValueError(
                        f"group_id {group_id!r} appears in both {previous!r} "
                        f"and {split_name!r}"
                    )

        explicit_train = [group for group, name in group_split.items() if name == "train"]
        explicit_val = [group for group, name in group_split.items() if name == "val"]
        test_groups = {group for group, name in group_split.items() if name == "test"}
        used_explicit = bool(explicit_train and explicit_val)
        if used_explicit:
            train_groups = set(explicit_train)
            val_groups = set(explicit_val)
            train_groups.update(
                set(group_indices) - train_groups - val_groups - test_groups
            )
        else:
            eligible = sorted(
                set(group_indices) - test_groups,
                key=lambda value: hashlib.sha256(
                    f"{int(seed)}|{value}".encode("utf-8")
                ).hexdigest(),
            )
            if len(eligible) <= 1:
                train_groups = set(eligible)
                val_groups = set(eligible)
            else:
                n_val_groups = max(
                    1,
                    min(
                        len(eligible) - 1,
                        int(round(len(eligible) * float(val_fraction))),
                    ),
                )
                val_groups = set(eligible[:n_val_groups])
                train_groups = set(eligible[n_val_groups:])
        train_indices = np.asarray(
            [
                index
                for group in sorted(train_groups)
                for index in group_indices[group]
            ],
            dtype=np.int64,
        )
        val_indices = np.asarray(
            [
                index
                for group in sorted(val_groups)
                for index in group_indices[group]
            ],
            dtype=np.int64,
        )
        if require_train_val and (train_indices.size == 0 or val_indices.size == 0):
            raise ValueError("Grouped split produced an empty training or validation set")

        label_masks = {
            name: np.asarray(masks[name][:], dtype=np.bool_)
            for name in itertools.chain(HDF5_STRUCTURE_LABELS, HDF5_ATOM_LABELS)
            if name in masks
        }
        elements: set = set()
        atomic_numbers_dataset = structures["atomic_numbers"]
        # Match the materialized path's checkpoint element table, including
        # types present only in the held-out test split. Read atomic numbers in
        # bounded contiguous chunks; geometry and labels remain disk-resident.
        element_chunk_atoms = 1_000_000
        for start in range(0, int(atomic_numbers_dataset.shape[0]), element_chunk_atoms):
            end = min(int(atomic_numbers_dataset.shape[0]), start + element_chunk_atoms)
            values = np.asarray(
                atomic_numbers_dataset[start:end], dtype=np.int16
            )
            elements.update(int(value) for value in np.unique(values))

    split_info = {
        "strategy": "metadata" if used_explicit else "stable_group_hash",
        "train_structures": int(train_indices.size),
        "val_structures": int(val_indices.size),
        "test_structures_excluded": int(
            sum(len(group_indices[group]) for group in test_groups)
        ),
        "train_groups": len(train_groups),
        "val_groups": len(val_groups),
        "group_overlap": sorted(train_groups & val_groups),
        "streaming": True,
    }
    return HDF5StreamPlan(
        path=resolved,
        atom_ptr=atom_ptr,
        group_ids=group_ids,
        split_values=split_values,
        metadata_values=metadata_values,
        label_masks=label_masks,
        train_indices=train_indices,
        val_indices=val_indices,
        elements=tuple(sorted(elements)),
        split_info=split_info,
        source_size=int(source_stat.st_size),
        source_mtime_ns=int(source_stat.st_mtime_ns),
    )


def _hdf5_elements_for_indices(
    plan: HDF5StreamPlan, indices: Sequence[int]
) -> Tuple[int, ...]:
    """Read the element set for selected structures with bounded memory."""
    selected = np.unique(np.asarray(indices, dtype=np.int64))
    if selected.size == 0:
        return ()
    spans: List[Tuple[int, int]] = []
    for raw_index in selected:
        index = int(raw_index)
        start = int(plan.atom_ptr[index])
        end = int(plan.atom_ptr[index + 1])
        if spans and spans[-1][1] == start:
            spans[-1] = (spans[-1][0], end)
        else:
            spans.append((start, end))
    elements: set[int] = set()
    chunk_atoms = 1_000_000
    with h5py.File(plan.path, "r") as handle:
        numbers = handle["structures/atomic_numbers"]
        for span_start, span_end in spans:
            for start in range(span_start, span_end, chunk_atoms):
                end = min(span_end, start + chunk_atoms)
                elements.update(
                    int(value)
                    for value in np.unique(
                        np.asarray(numbers[start:end], dtype=np.int16)
                    )
                )
    return tuple(sorted(elements))


def _read_hdf5_configuration_at(
    handle: Any,
    plan: HDF5StreamPlan,
    index: int,
    *,
    include_labels: bool = True,
) -> Configuration:
    """Read one indexed canonical structure without retaining corpus arrays."""
    structure_index = int(index)
    start = int(plan.atom_ptr[structure_index])
    end = int(plan.atom_ptr[structure_index + 1])
    structures = handle["structures"]
    props: Dict[str, Any] = {"group_id": plan.group_ids[structure_index]}
    weights: Dict[str, float] = {}
    if include_labels:
        labels = handle["labels"]
        for name in HDF5_STRUCTURE_LABELS:
            mask = plan.label_masks.get(name)
            if mask is None or not bool(mask[structure_index]) or name not in labels:
                continue
            value = np.asarray(labels[name][structure_index])
            props[name] = float(value) if value.shape == () else value
            weights[name] = 1.0
        for name in HDF5_ATOM_LABELS:
            mask = plan.label_masks.get(name)
            if mask is None or not bool(mask[structure_index]) or name not in labels:
                continue
            props[name] = np.asarray(labels[name][start:end])
            weights[name] = 1.0
        for name, values in plan.metadata_values.items():
            props[name] = values[structure_index]
    return Configuration(
        atomic_numbers=np.asarray(
            structures["atomic_numbers"][start:end], dtype=int
        ),
        positions=np.asarray(structures["positions"][start:end], dtype=float),
        properties=props,
        property_weights=weights,
        cell=np.asarray(structures["cell"][structure_index], dtype=float),
        pbc=tuple(bool(value) for value in structures["pbc"][structure_index]),
        config_type="Default",
        head=str(props.get("method_id", "Default")),
    )


def fit_atomic_energies_from_hdf5_plan(
    plan: HDF5StreamPlan, zs: Sequence[int]
) -> np.ndarray:
    """Fit a bounded-memory ridge reference model from canonical HDF5."""
    z_to_col = {int(z): index for index, z in enumerate(zs)}
    energy_mask = plan.label_masks.get("energy")
    if energy_mask is None:
        raise ValueError("Cannot fit atomic energies: dataset has no energy mask")
    normal = np.zeros((len(zs), len(zs)), dtype=np.float64)
    rhs = np.zeros((len(zs),), dtype=np.float64)
    ratio_chunks: List[np.ndarray] = []
    ratio_buffer: List[float] = []
    with h5py.File(plan.path, "r") as handle:
        structures = handle["structures"]
        energies = handle["labels/energy"]
        for raw_index in plan.train_indices:
            index = int(raw_index)
            if not bool(energy_mask[index]):
                continue
            energy = float(energies[index])
            if not math.isfinite(energy):
                continue
            start, end = int(plan.atom_ptr[index]), int(plan.atom_ptr[index + 1])
            numbers = np.asarray(
                structures["atomic_numbers"][start:end], dtype=int
            )
            counts = np.zeros((len(zs),), dtype=np.float64)
            for number in numbers:
                counts[z_to_col[int(number)]] += 1.0
            normal += np.outer(counts, counts)
            rhs += counts * energy
            ratio_buffer.append(energy / max(1, len(numbers)))
            if len(ratio_buffer) >= 65536:
                ratio_chunks.append(np.asarray(ratio_buffer, dtype=np.float64))
                ratio_buffer.clear()
    if ratio_buffer:
        ratio_chunks.append(np.asarray(ratio_buffer, dtype=np.float64))
    if not ratio_chunks:
        raise ValueError("Cannot fit atomic energies: empty dataset")
    largest_singular = math.sqrt(
        max(0.0, float(np.linalg.eigvalsh(normal)[-1]))
    )
    ridge_root = max(1e-12, 1e-3 * largest_singular)
    ridge = ridge_root * ridge_root
    prior = float(np.median(np.concatenate(ratio_chunks)))
    system = normal + ridge * np.eye(len(zs), dtype=np.float64)
    target = rhs + ridge * np.full(len(zs), prior, dtype=np.float64)
    solution = np.linalg.solve(system, target)
    if not np.isfinite(solution).all():
        raise FloatingPointError("Atomic reference-energy fit produced non-finite values")
    return np.asarray(solution, dtype=float).reshape(-1)


def _topology_cache_spec(
    plan: HDF5StreamPlan, cutoff: float
) -> Tuple[Dict[str, Any], np.ndarray]:
    source = Path(plan.path)
    selected = plan.selected_indices
    backend = (
        "mace-periodic" if HAS_MACE_NEIGHBORHOOD else "ase-periodic"
    ) + "+exact-nonperiodic-v2"
    spec = {
        "version": HDF5_TOPOLOGY_CACHE_VERSION,
        "source": str(source.resolve()),
        "source_size": int(plan.source_size),
        "source_mtime_ns": int(plan.source_mtime_ns),
        "selected_sha256": hashlib.sha256(selected.tobytes()).hexdigest(),
        "selected_count": int(selected.size),
        "cutoff": format(float(cutoff), ".17g"),
        "backend": backend,
    }
    return spec, selected


def _default_topology_cache_directory() -> Path:
    configured = os.environ.get("E3MU_GRAPH_CACHE_DIR", "").strip()
    return (
        Path(configured).expanduser()
        if configured
        else Path.home() / ".cache" / "e3mu" / "graph_topology"
    )


def build_hdf5_topology_cache(
    plan: HDF5StreamPlan,
    *,
    cutoff: float,
    cache_directory: str = "",
    log: Callable[[str], None] = print,
    progress: Optional[Callable[[Dict[str, Any]], None]] = None,
    stop_flag: Optional[Callable[[], bool]] = None,
) -> Optional[str]:
    """Build or reuse an exact disk topology cache with bounded working memory."""
    spec, selected = _topology_cache_spec(plan, cutoff)
    cache_root = (
        Path(cache_directory).expanduser()
        if str(cache_directory).strip()
        else _default_topology_cache_directory()
    ).resolve()
    cache_root.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(
        json.dumps(spec, sort_keys=True).encode("utf-8")
    ).hexdigest()[:24]
    cache_path = cache_root / f"{Path(plan.path).stem}.{key}.h5"
    spec_json = json.dumps(spec, sort_keys=True)

    def valid_cache(candidate: Path) -> bool:
        try:
            with h5py.File(candidate, "r") as handle:
                return bool(
                    str(handle.attrs.get("spec_json", "")) == spec_json
                    and str(handle.attrs.get("storage_layout", ""))
                    == "contiguous-mmap-v1"
                    and int(handle["global_indices"].shape[0]) == int(selected.size)
                    and int(handle["edge_ptr"].shape[0]) == int(selected.size) + 1
                    and int(handle["edge_ptr"][-1]) == int(handle["edge_index"].shape[0])
                    and str(handle.attrs.get("shift_storage", ""))
                    == "per-structure-bitwise-dictionary-v1"
                    and "shift_nonzero_local_indices" in handle
                    and "shift_codes" in handle
                    and "shift_unique_values" in handle
                    and int(handle["shift_nonzero_local_indices"].shape[0])
                    == int(handle["shift_codes"].shape[0])
                    and "shift_ptr" in handle
                    and int(handle["shift_ptr"].shape[0]) == int(selected.size) + 1
                    and int(handle["shift_ptr"][-1])
                    == int(handle["shift_nonzero_local_indices"].shape[0])
                    and "shift_value_ptr" in handle
                    and int(handle["shift_value_ptr"].shape[0])
                    == int(selected.size) + 1
                    and int(handle["shift_value_ptr"][-1])
                    == int(handle["shift_unique_values"].shape[0])
                    and int(handle.attrs.get("max_edges_per_structure", -1)) >= 0
                    and int(handle.attrs.get("max_unique_shifts_per_structure", -1)) >= 0
                    and (
                        int(handle["edge_index"].shape[0]) == 0
                        or handle["edge_index"].chunks is None
                    )
                    and (
                        int(handle["shift_nonzero_local_indices"].shape[0]) == 0
                        or (
                            handle["shift_nonzero_local_indices"].chunks is None
                            and handle["shift_codes"].chunks is None
                        )
                    )
                    and (
                        int(handle["shift_unique_values"].shape[0]) == 0
                        or handle["shift_unique_values"].chunks is None
                    )
                )
        except Exception:
            return False

    if cache_path.exists() and valid_cache(cache_path):
        size_mib = cache_path.stat().st_size / (1024.0 * 1024.0)
        log(
            f"[{_now()}] Reusing disk topology cache: {cache_path} "
            f"({size_mib:.1f} MiB)."
        )
        return str(cache_path)
    if cache_path.exists():
        cache_path.unlink()

    temporary = cache_path.with_name(
        f"{cache_path.name}.building-{os.getpid()}"
    )
    optimized = cache_path.with_name(
        f"{cache_path.name}.contiguous-{os.getpid()}"
    )
    temporary.unlink(missing_ok=True)
    optimized.unlink(missing_ok=True)
    total = int(selected.size)
    log(
        f"[{_now()}] Building streamed topology cache for {total} structures "
        f"(cutoff={float(cutoff):g}) ..."
    )
    if progress is not None:
        progress(
            {
                "type": "prep",
                "task": "Build disk topology cache",
                "overall_frac": 0.05,
                "current": 0,
                "total": total,
                "stage": "neighbor_list",
            }
        )
    started = time.perf_counter()
    try:
        with h5py.File(plan.path, "r") as source, h5py.File(temporary, "w") as output:
            output.attrs["spec_json"] = spec_json
            output.attrs["created_at"] = _now()
            output.create_dataset("global_indices", data=selected, compression="gzip")
            edge_ptr = np.zeros((total + 1,), dtype=np.int64)
            atom_counts = np.empty((total,), dtype=np.int32)
            edge_counts = np.empty((total,), dtype=np.int64)
            shift_nonzero_counts = np.empty((total,), dtype=np.int64)
            shift_unique_counts = np.empty((total,), dtype=np.int64)
            edge_dataset = output.create_dataset(
                "edge_index",
                shape=(0, 2),
                maxshape=(None, 2),
                dtype=np.int32,
                chunks=(65536, 2),
                compression="lzf",
                shuffle=True,
            )
            shift_index_dataset = output.create_dataset(
                "shift_nonzero_local_indices",
                shape=(0,),
                maxshape=(None,),
                dtype=np.uint64,
                chunks=(65536,),
                compression="lzf",
                shuffle=True,
            )
            shift_code_dataset = output.create_dataset(
                "shift_codes",
                shape=(0,),
                maxshape=(None,),
                dtype=np.uint64,
                chunks=(65536,),
                compression="lzf",
                shuffle=True,
            )
            shift_value_dataset = output.create_dataset(
                "shift_unique_values",
                shape=(0, 3),
                maxshape=(None, 3),
                dtype=np.float64,
                chunks=(65536, 3),
                compression="lzf",
                shuffle=True,
            )
            edge_buffer: List[np.ndarray] = []
            shift_index_buffer: List[np.ndarray] = []
            shift_code_buffer: List[np.ndarray] = []
            shift_value_buffer: List[np.ndarray] = []
            buffered_edges = 0
            written_edges = 0
            written_nonzero_shifts = 0
            written_unique_shifts = 0

            def flush() -> None:
                nonlocal buffered_edges, written_edges
                nonlocal written_nonzero_shifts, written_unique_shifts
                if buffered_edges <= 0:
                    return
                edges = np.concatenate(edge_buffer, axis=0)
                new_end = written_edges + int(edges.shape[0])
                edge_dataset.resize((new_end, 2))
                edge_dataset[written_edges:new_end] = edges
                if shift_index_buffer:
                    local_indices = np.concatenate(shift_index_buffer)
                    codes = np.concatenate(shift_code_buffer)
                    new_shift_end = written_nonzero_shifts + int(local_indices.size)
                    shift_index_dataset.resize((new_shift_end,))
                    shift_code_dataset.resize((new_shift_end,))
                    shift_index_dataset[written_nonzero_shifts:new_shift_end] = local_indices
                    shift_code_dataset[written_nonzero_shifts:new_shift_end] = codes
                    written_nonzero_shifts = new_shift_end
                if shift_value_buffer:
                    unique_values = np.concatenate(shift_value_buffer, axis=0)
                    new_value_end = written_unique_shifts + int(unique_values.shape[0])
                    shift_value_dataset.resize((new_value_end, 3))
                    shift_value_dataset[written_unique_shifts:new_value_end] = unique_values
                    written_unique_shifts = new_value_end
                written_edges = new_end
                edge_buffer.clear()
                shift_index_buffer.clear()
                shift_code_buffer.clear()
                shift_value_buffer.clear()
                buffered_edges = 0

            emit_every = max(1, min(100, total // 20 or 1))
            for row, raw_index in enumerate(selected):
                if stop_flag is not None and stop_flag():
                    return None
                cfg = _read_hdf5_configuration_at(
                    source, plan, int(raw_index), include_labels=False
                )
                edge_index, shifts = _configuration_neighbor_topology(
                    cfg, cutoff=float(cutoff)
                )
                count = int(edge_index.shape[1])
                atom_counts[row] = int(len(cfg.atomic_numbers))
                edge_counts[row] = count
                local_indices, shift_codes, unique_shifts = (
                    _encode_bitwise_shift_dictionary(shifts)
                )
                shift_nonzero_counts[row] = int(local_indices.size)
                shift_unique_counts[row] = int(unique_shifts.shape[0])
                edge_ptr[row + 1] = edge_ptr[row] + count
                if count:
                    edge_buffer.append(
                        np.asarray(edge_index.T, dtype=np.int32)
                    )
                    if local_indices.size:
                        shift_index_buffer.append(local_indices)
                        shift_code_buffer.append(shift_codes)
                        shift_value_buffer.append(unique_shifts)
                    buffered_edges += count
                if buffered_edges >= 250000:
                    flush()
                current = row + 1
                if progress is not None and (
                    current == total or current % emit_every == 0
                ):
                    progress(
                        {
                            "type": "prep",
                            "task": "Build disk topology cache",
                            "overall_frac": 0.05
                            + 0.15 * current / max(1, total),
                            "current": current,
                            "total": total,
                            "stage": "neighbor_list",
                        }
                    )
            flush()
            output.create_dataset("edge_ptr", data=edge_ptr, compression="gzip")
            output.create_dataset("atom_counts", data=atom_counts, compression="gzip")
            output.create_dataset("edge_counts", data=edge_counts, compression="gzip")
            shift_ptr = np.zeros((total + 1,), dtype=np.int64)
            np.cumsum(shift_nonzero_counts, out=shift_ptr[1:])
            if int(shift_ptr[-1]) != int(written_nonzero_shifts):
                raise RuntimeError("Sparse shift pointer construction is inconsistent")
            output.create_dataset("shift_ptr", data=shift_ptr, compression="gzip")
            shift_value_ptr = np.zeros((total + 1,), dtype=np.int64)
            np.cumsum(shift_unique_counts, out=shift_value_ptr[1:])
            if int(shift_value_ptr[-1]) != int(written_unique_shifts):
                raise RuntimeError("Shift dictionary pointer construction is inconsistent")
            output.create_dataset(
                "shift_value_ptr", data=shift_value_ptr, compression="gzip"
            )
        if stop_flag is not None and stop_flag():
            return None
        if progress is not None:
            progress(
                {
                    "type": "prep",
                    "task": "Finalize read-optimized topology cache",
                    "overall_frac": 0.20,
                    "current": 0,
                    "total": 1,
                    "stage": "cache_finalize",
                }
            )
        # Resizable HDF5 datasets must be chunked. Rewrite them once into
        # contiguous arrays so training can memory-map exact topology bytes
        # without repeated HDF5 chunk decompression or per-epoch cache writes.
        with h5py.File(temporary, "r") as source, h5py.File(
            optimized, "w", libver="latest"
        ) as output:
            for name, value in source.attrs.items():
                output.attrs[name] = value
            output.attrs["storage_layout"] = "contiguous-mmap-v1"
            output.attrs["shift_storage"] = "per-structure-bitwise-dictionary-v1"
            for name in (
                "global_indices",
                "edge_ptr",
                "atom_counts",
                "edge_counts",
                "shift_ptr",
                "shift_value_ptr",
            ):
                output.create_dataset(name, data=source[name][:])
            copy_edges = 1_000_000
            max_atoms = int(np.max(source["atom_counts"][:], initial=0))
            compact_edge_dtype = _compact_unsigned_dtype_for_upper_bound(max_atoms)
            output.attrs["edge_index_storage_dtype"] = compact_edge_dtype.name
            input_edges = source["edge_index"]
            output_edges = output.create_dataset(
                "edge_index", shape=input_edges.shape, dtype=compact_edge_dtype
            )
            for start in range(0, int(input_edges.shape[0]), copy_edges):
                end = min(int(input_edges.shape[0]), start + copy_edges)
                output_edges[start:end] = input_edges[start:end]
            edge_counts = source["edge_counts"][:]
            max_edges = int(np.max(edge_counts, initial=0))
            output.attrs["max_edges_per_structure"] = max_edges
            compact_index_dtype = _compact_unsigned_dtype_for_upper_bound(max_edges)
            output.attrs["shift_index_storage_dtype"] = compact_index_dtype.name
            input_indices = source["shift_nonzero_local_indices"]
            output_indices = output.create_dataset(
                "shift_nonzero_local_indices",
                shape=input_indices.shape,
                dtype=compact_index_dtype,
            )
            for start in range(0, int(input_indices.shape[0]), copy_edges):
                end = min(int(input_indices.shape[0]), start + copy_edges)
                output_indices[start:end] = input_indices[start:end]
            shift_value_ptr = source["shift_value_ptr"][:]
            max_unique_shifts = int(
                np.max(np.diff(shift_value_ptr), initial=0)
            )
            output.attrs["max_unique_shifts_per_structure"] = max_unique_shifts
            compact_code_dtype = _compact_unsigned_dtype_for_upper_bound(
                max_unique_shifts
            )
            output.attrs["shift_code_storage_dtype"] = compact_code_dtype.name
            input_codes = source["shift_codes"]
            output_codes = output.create_dataset(
                "shift_codes", shape=input_codes.shape, dtype=compact_code_dtype
            )
            for start in range(0, int(input_codes.shape[0]), copy_edges):
                end = min(int(input_codes.shape[0]), start + copy_edges)
                output_codes[start:end] = input_codes[start:end]
            input_shift_values = source["shift_unique_values"]
            output_shift_values = output.create_dataset(
                "shift_unique_values",
                shape=input_shift_values.shape,
                dtype=input_shift_values.dtype,
            )
            for start in range(0, int(input_shift_values.shape[0]), copy_edges):
                end = min(int(input_shift_values.shape[0]), start + copy_edges)
                output_shift_values[start:end] = input_shift_values[start:end]
        optimized.replace(cache_path)
        if progress is not None:
            progress(
                {
                    "type": "prep",
                    "task": "Finalize read-optimized topology cache",
                    "overall_frac": 0.20,
                    "current": 1,
                    "total": 1,
                    "stage": "done",
                }
            )
    finally:
        if temporary.exists():
            temporary.unlink()
        if optimized.exists():
            optimized.unlink()
    size_mib = cache_path.stat().st_size / (1024.0 * 1024.0)
    log(
        f"[{_now()}] Built disk topology cache in "
        f"{time.perf_counter() - started:.2f} s: {cache_path} ({size_mib:.1f} MiB)."
    )
    return str(cache_path)


class HDF5AtomicDataDataset(Dataset):
    """Map-style graph dataset whose structures and topology remain on disk."""

    def __init__(
        self,
        plan: HDF5StreamPlan,
        indices: Sequence[int],
        *,
        z_table: AtomicNumberTable,
        cutoff: float,
        topology_cache: Optional[str],
    ) -> None:
        self.plan = plan
        self.indices = np.asarray(indices, dtype=np.int64)
        self.z_table = z_table
        self.cutoff = float(cutoff)
        self.topology_cache = str(topology_cache or "")
        self._source_handle = None
        self._topology_handle = None
        self._edge_memmap: Optional[np.memmap] = None
        self._shift_memmap: Optional[np.memmap] = None
        self._shift_index_memmap: Optional[np.memmap] = None
        self._shift_code_memmap: Optional[np.memmap] = None
        self._shift_value_memmap: Optional[np.memmap] = None
        self._topology_mmap_specs: Optional[Dict[str, Tuple[int, np.dtype, Tuple[int, ...]]]] = None
        self._fallback_shift_indices: Optional[np.ndarray] = None
        self._handle_pid: Optional[int] = None
        self.cache_rows: Optional[np.ndarray] = None
        self.edge_ptr: Optional[np.ndarray] = None
        self.shift_ptr: Optional[np.ndarray] = None
        self.shift_value_ptr: Optional[np.ndarray] = None
        self.edge_counts: Optional[np.ndarray] = None
        self.atom_counts = (
            plan.atom_ptr[self.indices + 1] - plan.atom_ptr[self.indices]
        ).astype(np.int64, copy=False)
        if self.topology_cache:
            with h5py.File(self.topology_cache, "r") as cache:
                cache_indices = np.asarray(cache["global_indices"][:], dtype=np.int64)
                rows = np.searchsorted(cache_indices, self.indices)
                if np.any(rows >= len(cache_indices)) or not np.array_equal(
                    cache_indices[rows], self.indices
                ):
                    raise ValueError("Topology cache does not cover dataset indices")
                self.cache_rows = rows.astype(np.int64, copy=False)
                self.edge_ptr = np.asarray(cache["edge_ptr"][:], dtype=np.int64)
                if "shift_ptr" in cache:
                    self.shift_ptr = np.asarray(cache["shift_ptr"][:], dtype=np.int64)
                if "shift_value_ptr" in cache:
                    self.shift_value_ptr = np.asarray(
                        cache["shift_value_ptr"][:], dtype=np.int64
                    )
                all_edge_counts = np.asarray(cache["edge_counts"][:], dtype=np.int64)
                self.edge_counts = all_edge_counts[self.cache_rows]
                edge_dataset = cache["edge_index"]
                edge_offset = edge_dataset.id.get_offset()
                mmap_specs: Dict[str, Tuple[int, np.dtype, Tuple[int, ...]]] = {}
                if edge_dataset.chunks is None and edge_offset is not None:
                    mmap_specs["edge_index"] = (
                        int(edge_offset),
                        np.dtype(edge_dataset.dtype),
                        tuple(int(value) for value in edge_dataset.shape),
                    )
                if "shifts" in cache:
                    shift_names = ("shifts",)
                elif "shift_codes" in cache:
                    shift_names = (
                        "shift_nonzero_local_indices",
                        "shift_codes",
                        "shift_unique_values",
                    )
                else:
                    shift_names = (
                        "shift_nonzero_indices",
                        "shift_nonzero_values",
                    )
                for name in shift_names:
                    dataset = cache[name]
                    offset = dataset.id.get_offset()
                    if dataset.chunks is not None or offset is None:
                        mmap_specs.clear()
                        break
                    mmap_specs[name] = (
                        int(offset),
                        np.dtype(dataset.dtype),
                        tuple(int(value) for value in dataset.shape),
                    )
                if "edge_index" in mmap_specs and all(
                    name in mmap_specs for name in shift_names
                ):
                    self._topology_mmap_specs = mmap_specs
                elif "shift_nonzero_indices" in cache and self.shift_ptr is None:
                    self._fallback_shift_indices = np.asarray(
                        cache["shift_nonzero_indices"][:], dtype=np.int64
                    )

    def __len__(self) -> int:
        return int(self.indices.size)

    def _ensure_handles(self) -> None:
        pid = os.getpid()
        if self._handle_pid == pid and self._source_handle is not None:
            return
        self.close()
        self._source_handle = h5py.File(self.plan.path, "r")
        if self.topology_cache and self._topology_mmap_specs is not None:
            edge_offset, edge_dtype, edge_shape = self._topology_mmap_specs["edge_index"]
            self._edge_memmap = np.memmap(
                self.topology_cache,
                mode="r",
                offset=edge_offset,
                dtype=edge_dtype,
                shape=edge_shape,
                order="C",
            )
            if "shifts" in self._topology_mmap_specs:
                shift_offset, shift_dtype, shift_shape = self._topology_mmap_specs["shifts"]
                self._shift_memmap = np.memmap(
                    self.topology_cache,
                    mode="r",
                    offset=shift_offset,
                    dtype=shift_dtype,
                    shape=shift_shape,
                    order="C",
                )
            elif "shift_codes" in self._topology_mmap_specs:
                index_offset, index_dtype, index_shape = self._topology_mmap_specs[
                    "shift_nonzero_local_indices"
                ]
                code_offset, code_dtype, code_shape = self._topology_mmap_specs[
                    "shift_codes"
                ]
                value_offset, value_dtype, value_shape = self._topology_mmap_specs[
                    "shift_unique_values"
                ]
                self._shift_index_memmap = np.memmap(
                    self.topology_cache,
                    mode="r",
                    offset=index_offset,
                    dtype=index_dtype,
                    shape=index_shape,
                    order="C",
                )
                self._shift_code_memmap = np.memmap(
                    self.topology_cache,
                    mode="r",
                    offset=code_offset,
                    dtype=code_dtype,
                    shape=code_shape,
                    order="C",
                )
                self._shift_value_memmap = np.memmap(
                    self.topology_cache,
                    mode="r",
                    offset=value_offset,
                    dtype=value_dtype,
                    shape=value_shape,
                    order="C",
                )
            else:
                index_offset, index_dtype, index_shape = self._topology_mmap_specs[
                    "shift_nonzero_indices"
                ]
                value_offset, value_dtype, value_shape = self._topology_mmap_specs[
                    "shift_nonzero_values"
                ]
                self._shift_index_memmap = np.memmap(
                    self.topology_cache,
                    mode="r",
                    offset=index_offset,
                    dtype=index_dtype,
                    shape=index_shape,
                    order="C",
                )
                self._shift_value_memmap = np.memmap(
                    self.topology_cache,
                    mode="r",
                    offset=value_offset,
                    dtype=value_dtype,
                    shape=value_shape,
                    order="C",
                )
            self._topology_handle = None
        else:
            self._topology_handle = (
                h5py.File(self.topology_cache, "r") if self.topology_cache else None
            )
        self._handle_pid = pid

    def __getitem__(self, item: int) -> AtomicData:
        self._ensure_handles()
        index = int(self.indices[int(item)])
        cfg = _read_hdf5_configuration_at(
            self._source_handle, self.plan, index, include_labels=True
        )
        topology = None
        if (
            self._edge_memmap is not None
            and self._shift_index_memmap is not None
            and self._shift_code_memmap is not None
            and self._shift_value_memmap is not None
        ):
            row = int(self.cache_rows[int(item)])
            start, end = int(self.edge_ptr[row]), int(self.edge_ptr[row + 1])
            left = int(self.shift_ptr[row])
            right = int(self.shift_ptr[row + 1])
            value_left = int(self.shift_value_ptr[row])
            value_right = int(self.shift_value_ptr[row + 1])
            shifts = np.zeros((end - start, 3), dtype=np.float64)
            if right > left:
                local_indices = np.asarray(
                    self._shift_index_memmap[left:right], dtype=np.int64
                )
                codes = np.asarray(
                    self._shift_code_memmap[left:right], dtype=np.int64
                )
                dictionary = np.asarray(
                    self._shift_value_memmap[value_left:value_right],
                    dtype=np.float64,
                )
                shifts[local_indices] = dictionary[codes]
            topology = (
                np.asarray(self._edge_memmap[start:end], dtype=np.int64).T,
                shifts,
            )
        elif (
            self._edge_memmap is not None
            and self._shift_index_memmap is not None
            and self._shift_value_memmap is not None
        ):
            row = int(self.cache_rows[int(item)])
            start, end = int(self.edge_ptr[row]), int(self.edge_ptr[row + 1])
            if self.shift_ptr is not None:
                left = int(self.shift_ptr[row])
                right = int(self.shift_ptr[row + 1])
            else:
                left = int(np.searchsorted(self._shift_index_memmap, start, side="left"))
                right = int(np.searchsorted(self._shift_index_memmap, end, side="left"))
            shifts = np.zeros((end - start, 3), dtype=np.float64)
            if right > left:
                local_indices = np.asarray(
                    self._shift_index_memmap[left:right], dtype=np.int64
                ) - start
                shifts[local_indices] = np.asarray(
                    self._shift_value_memmap[left:right], dtype=np.float64
                )
            topology = (
                np.asarray(self._edge_memmap[start:end], dtype=np.int64).T,
                shifts,
            )
        elif self._edge_memmap is not None and self._shift_memmap is not None:
            row = int(self.cache_rows[int(item)])
            start, end = int(self.edge_ptr[row]), int(self.edge_ptr[row + 1])
            topology = (
                np.asarray(self._edge_memmap[start:end], dtype=np.int64).T,
                np.asarray(self._shift_memmap[start:end], dtype=float),
            )
        elif self._topology_handle is not None:
            row = int(self.cache_rows[int(item)])
            start, end = int(self.edge_ptr[row]), int(self.edge_ptr[row + 1])
            edges = np.asarray(
                self._topology_handle["edge_index"][start:end], dtype=np.int64
            ).T
            if "shifts" in self._topology_handle:
                shifts = np.asarray(
                    self._topology_handle["shifts"][start:end], dtype=float
                )
            elif "shift_codes" in self._topology_handle:
                left = int(self.shift_ptr[row])
                right = int(self.shift_ptr[row + 1])
                value_left = int(self.shift_value_ptr[row])
                value_right = int(self.shift_value_ptr[row + 1])
                shifts = np.zeros((end - start, 3), dtype=np.float64)
                if right > left:
                    local_indices = np.asarray(
                        self._topology_handle["shift_nonzero_local_indices"][left:right],
                        dtype=np.int64,
                    )
                    codes = np.asarray(
                        self._topology_handle["shift_codes"][left:right],
                        dtype=np.int64,
                    )
                    dictionary = np.asarray(
                        self._topology_handle["shift_unique_values"][
                            value_left:value_right
                        ],
                        dtype=np.float64,
                    )
                    shifts[local_indices] = dictionary[codes]
            else:
                indices = self._fallback_shift_indices
                if self.shift_ptr is not None:
                    left = int(self.shift_ptr[row])
                    right = int(self.shift_ptr[row + 1])
                    if indices is None:
                        indices = np.asarray(
                            self._topology_handle["shift_nonzero_indices"][left:right],
                            dtype=np.int64,
                        )
                        index_slice = indices
                    else:
                        index_slice = indices[left:right]
                else:
                    left = int(np.searchsorted(indices, start, side="left"))
                    right = int(np.searchsorted(indices, end, side="left"))
                    index_slice = indices[left:right]
                shifts = np.zeros((end - start, 3), dtype=np.float64)
                if right > left:
                    shifts[index_slice - start] = np.asarray(
                        self._topology_handle["shift_nonzero_values"][left:right],
                        dtype=np.float64,
                    )
            topology = (edges, shifts)
        return AtomicData.from_config(
            cfg,
            z_table=self.z_table,
            cutoff=self.cutoff,
            topology=topology,
        )

    def close(self) -> None:
        for name in ("_source_handle", "_topology_handle"):
            handle = getattr(self, name, None)
            if handle is not None:
                try:
                    handle.close()
                except Exception:
                    pass
                setattr(self, name, None)
        for name in (
            "_edge_memmap",
            "_shift_memmap",
            "_shift_index_memmap",
            "_shift_code_memmap",
            "_shift_value_memmap",
        ):
            array = getattr(self, name, None)
            if array is not None:
                memory_map = getattr(array, "_mmap", None)
                if memory_map is not None:
                    try:
                        memory_map.close()
                    except Exception:
                        pass
                setattr(self, name, None)
        self._handle_pid = None

    def __getstate__(self) -> Dict[str, Any]:
        state = dict(self.__dict__)
        state["_source_handle"] = None
        state["_topology_handle"] = None
        state["_edge_memmap"] = None
        state["_shift_memmap"] = None
        state["_shift_index_memmap"] = None
        state["_shift_code_memmap"] = None
        state["_shift_value_memmap"] = None
        state["_handle_pid"] = None
        return state

    def __del__(self) -> None:
        self.close()


@dataclass
class CompositeStreamPlan:
    """Bounded-memory index for an OMat24-Parquet + canonical-HDF5 corpus."""

    path: str
    omat_root: str
    source_files: Tuple[str, ...]
    source_orders: np.ndarray
    row_indices: np.ndarray
    split_codes: np.ndarray
    omat_atom_counts: np.ndarray
    large_plan: HDF5StreamPlan
    mode: str
    train_omat_indices: np.ndarray
    val_omat_indices: np.ndarray
    train_large_indices: np.ndarray
    val_large_indices: np.ndarray
    elements: Tuple[int, ...]
    label_counts: Dict[str, int]
    split_info: Dict[str, Any]
    omat_embedded: bool = False
    omat_materialized: bool = False
    omat_packed: bool = False
    embedded_shard_names: Tuple[str, ...] = ()


class _HDF5ByteStream(io.RawIOBase):
    """Seekable read-only file facade over one embedded HDF5 byte dataset."""

    def __init__(self, dataset: Any) -> None:
        super().__init__()
        self._dataset = dataset
        self._position = 0
        self._size = int(dataset.shape[0])

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return int(self._position)

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        value = int(offset)
        if whence == io.SEEK_CUR:
            value += self._position
        elif whence == io.SEEK_END:
            value += self._size
        elif whence != io.SEEK_SET:
            raise ValueError(f"Unsupported seek mode: {whence}")
        self._position = max(0, min(self._size, value))
        return int(self._position)

    def read(self, size: int = -1) -> bytes:
        if size is None or int(size) < 0:
            count = self._size - self._position
        else:
            count = min(int(size), self._size - self._position)
        if count <= 0:
            return b""
        start = int(self._position)
        end = start + int(count)
        self._position = end
        return np.asarray(self._dataset[start:end], dtype=np.uint8).tobytes()

    def readinto(self, buffer: Any) -> int:
        data = self.read(len(buffer))
        buffer[: len(data)] = data
        return len(data)


def _deterministic_subsample_indices(
    indices: np.ndarray, fraction: float, seed: int, namespace: str
) -> np.ndarray:
    values = np.asarray(indices, dtype=np.int64)
    if float(fraction) >= 1.0 or values.size <= 2:
        return values
    if not (0.0 < float(fraction) <= 1.0):
        raise ValueError("sample_fraction must be in (0, 1]")
    target = max(2, int(round(values.size * float(fraction))))
    rng = np.random.default_rng(
        int(hashlib.sha256(f"{namespace}|{seed}".encode()).hexdigest()[:16], 16)
    )
    sampled = np.sort(rng.choice(values, size=target, replace=False))
    if values.size < np.iinfo(np.uint32).max:
        return sampled.astype(np.uint32, copy=False)
    return sampled.astype(np.int64, copy=False)


def _flatnonzero_uint32(mask: np.ndarray, *, chunk_size: int = 8_000_000) -> np.ndarray:
    """Return large selector indices without an intermediate int64 full index."""
    values = np.asarray(mask, dtype=np.bool_).reshape(-1)
    if values.size >= np.iinfo(np.uint32).max:
        raise ValueError("Composite selector exceeds uint32 index capacity")
    output = np.empty((int(np.count_nonzero(values)),), dtype=np.uint32)
    cursor = 0
    step = max(1, int(chunk_size))
    for start in range(0, int(values.size), step):
        local = np.flatnonzero(values[start:start + step]).astype(np.uint32)
        end = cursor + int(local.size)
        output[cursor:end] = local + np.uint32(start)
        cursor = end
    return output


def prepare_composite_stream_plan(
    path: str,
    *,
    mode: str,
    val_fraction: float,
    seed: int,
    sample_fraction: float = 1.0,
) -> CompositeStreamPlan:
    """Load Plus/Max selectors while numerical arrays remain disk-resident."""
    composite = Path(path).expanduser().resolve()
    with h5py.File(composite, "r") as handle:
        if str(handle.attrs.get("schema_version", "")) != COMPOSITE_HDF5_SCHEMA_VERSION:
            raise ValueError("Unsupported composite HDF5 schema")
        omat = handle["sources/omat24"]
        omat_embedded = bool(omat.attrs.get("embedded", False))
        omat_storage = str(omat.attrs.get("storage", ""))
        omat_packed = omat_storage == OMAT24_PACKED_SCHEMA_VERSION
        omat_materialized = bool(omat.attrs.get("materialized", False)) or (
            omat_storage in {
                OMAT24_MATERIALIZED_SCHEMA_VERSION, OMAT24_PACKED_SCHEMA_VERSION
            }
        )
        omat_root = (
            _resolve_composite_source(composite, str(omat.attrs.get("root", ".")))
            if not omat_embedded
            else composite.parent
        )
        relative_source_files = tuple(
            str(value) for value in omat["file_paths"].asstr()[:]
        )
        source_files = (
            relative_source_files
            if omat_embedded
            else tuple(str((omat_root / value).resolve()) for value in relative_source_files)
        )
        embedded_shard_names: Tuple[str, ...] = ()
        if omat_embedded and not omat_packed:
            payload = omat.get("embedded_parquet")
            if payload is None or "shard_names" not in payload:
                raise ValueError("Embedded OMat24 payload is missing shard_names")
            embedded_shard_names = tuple(
                str(value) for value in payload["shard_names"].asstr()[:]
            )
            if len(embedded_shard_names) != len(source_files):
                raise ValueError("Embedded OMat24 shard count does not match file_paths")
        source_orders = np.asarray(handle["selection/source_order"][:], dtype=np.uint16)
        row_indices = np.asarray(handle["selection/row_index"][:], dtype=np.uint32)
        split_codes = np.asarray(handle["selection/split_code"][:], dtype=np.uint8)
        omat_atom_counts = np.asarray(handle["selection/atom_count"][:], dtype=np.uint16)
        large_group = handle["sources/neo_large"]
        large_embedded = bool(large_group.attrs.get("embedded", False))
        large_path = (
            composite
            if large_embedded
            else _resolve_composite_source(composite, str(large_group.attrs["path"]))
        )
        metadata = json.loads(str(handle.attrs.get("metadata_json", "{}")))
    for source in (() if omat_embedded else source_files) + (str(large_path),):
        if not Path(source).is_file():
            raise FileNotFoundError(f"Composite source is unavailable: {source}")

    selected_mode = str(mode).strip().lower()
    if selected_mode not in {"base", "response", "joint"}:
        raise ValueError(f"Unsupported composite training mode: {mode!r}")
    omat_train = _flatnonzero_uint32(split_codes == 0)
    omat_val = _flatnonzero_uint32(split_codes == 1)
    if selected_mode == "response":
        omat_train = np.zeros((0,), dtype=np.int64)
        omat_val = np.zeros((0,), dtype=np.int64)
    elif float(sample_fraction) < 1.0:
        omat_train = _deterministic_subsample_indices(
            omat_train, sample_fraction, seed, f"{composite}:omat-train"
        )
        omat_val = _deterministic_subsample_indices(
            omat_val, sample_fraction, seed, f"{composite}:omat-val"
        )

    large_plan = prepare_hdf5_stream_plan(
        str(large_path), val_fraction=val_fraction, seed=seed,
        sample_fraction=1.0, sample_seed=seed,
    )
    large_masks = large_plan.label_masks
    large_roles = np.asarray(
        [
            _large_curriculum_role(large_masks, index)[1]
            for index in range(len(large_plan.group_ids))
        ],
        dtype=object,
    )
    large_train = np.asarray(
        [int(index) for index in large_plan.train_indices
         if _curriculum_role_matches(str(large_roles[int(index)]), selected_mode)],
        dtype=np.int64,
    )
    large_val = np.asarray(
        [int(index) for index in large_plan.val_indices
         if _curriculum_role_matches(str(large_roles[int(index)]), selected_mode)],
        dtype=np.int64,
    )
    if float(sample_fraction) < 1.0:
        large_train = _deterministic_subsample_indices(
            large_train, sample_fraction, seed, f"{composite}:large-train:{selected_mode}"
        )
        large_val = _deterministic_subsample_indices(
            large_val, sample_fraction, seed, f"{composite}:large-val:{selected_mode}"
        )
    if selected_mode == "response" and (large_train.size == 0 or large_val.size == 0):
        raise ValueError("Composite response role has no train/validation records")
    if selected_mode != "response" and (omat_train.size + large_train.size == 0):
        raise ValueError("Composite stage has no training records")

    elements = set(int(value) for value in large_plan.elements)
    elements.update(
        int(value) for value in metadata.get("omat24", {}).get("elements", [])
    )
    label_counts = dict(metadata.get("neo_large", {}).get("labels", {}))
    omat_selected = int(omat_train.size + omat_val.size)
    if selected_mode != "response":
        for name in ("energy", "forces", "stress"):
            label_counts[name] = int(label_counts.get(name, 0)) + omat_selected
    split_info = {
        "strategy": "composite_metadata_curriculum",
        "curriculum_mode": selected_mode,
        "train_structures": int(omat_train.size + large_train.size),
        "val_structures": int(omat_val.size + large_val.size),
        "train_omat24": int(omat_train.size),
        "val_omat24": int(omat_val.size),
        "train_large": int(large_train.size),
        "val_large": int(large_val.size),
        "test_structures_excluded": int(np.count_nonzero(split_codes == 2)),
        "group_overlap": [],
        "streaming": True,
    }
    return CompositeStreamPlan(
        path=str(composite), omat_root=str(omat_root), source_files=source_files,
        source_orders=source_orders, row_indices=row_indices, split_codes=split_codes,
        omat_atom_counts=omat_atom_counts,
        large_plan=large_plan, mode=selected_mode,
        train_omat_indices=omat_train, val_omat_indices=omat_val,
        train_large_indices=large_train, val_large_indices=large_val,
        elements=tuple(sorted(elements)), label_counts={str(k): int(v) for k, v in label_counts.items()},
        split_info=split_info,
        omat_embedded=omat_embedded,
        omat_materialized=omat_materialized,
        omat_packed=omat_packed,
        embedded_shard_names=embedded_shard_names,
    )


class CompositeAtomicDataDataset(Dataset):
    """Random-access streamed graphs from OMat24 Parquet and Neo Large HDF5."""

    def __init__(
        self,
        plan: CompositeStreamPlan,
        omat_indices: Sequence[int],
        large_indices: Sequence[int],
        *,
        z_table: AtomicNumberTable,
        cutoff: float,
    ) -> None:
        self.plan = plan
        self.omat_indices = np.asarray(omat_indices, dtype=np.uint32)
        self.large_indices = np.asarray(large_indices, dtype=np.int64)
        self.z_table = z_table
        self.cutoff = float(cutoff)
        self._parquet_handles: Dict[int, Any] = {}
        self._embedded_streams: Dict[int, _HDF5ByteStream] = {}
        self._parquet_streams: Dict[int, Dict[str, Any]] = {}
        self._large_handle = None
        self._handle_pid: Optional[int] = None
        self.curriculum_roles = np.concatenate([
            np.full(self.omat_indices.size, "foundation", dtype=object),
            np.full(self.large_indices.size, "response", dtype=object),
        ])
        self.atom_counts = np.concatenate([
            plan.omat_atom_counts[self.omat_indices].astype(np.int64, copy=False),
            (plan.large_plan.atom_ptr[self.large_indices + 1]
             - plan.large_plan.atom_ptr[self.large_indices]).astype(np.int64, copy=False),
        ])
        self.edge_counts = None

    def __len__(self) -> int:
        return int(self.omat_indices.size + self.large_indices.size)

    def _ensure_handles(self) -> None:
        pid = os.getpid()
        if self._handle_pid == pid and self._large_handle is not None:
            return
        self.close()
        self._large_handle = h5py.File(self.plan.large_plan.path, "r")
        self._handle_pid = pid

    def _parquet_file(self, source_order: int) -> Any:
        handle = self._parquet_handles.get(int(source_order))
        if handle is None:
            source_index = int(source_order)
            if self.plan.omat_embedded:
                if self._large_handle is None:
                    raise RuntimeError("Embedded OMat24 handle is not open")
                payload = self._large_handle["sources/omat24/embedded_parquet"]
                shard_name = self.plan.embedded_shard_names[source_index]
                stream = _HDF5ByteStream(payload["shards"][shard_name])
                self._embedded_streams[source_index] = stream
                handle = _pyarrow_parquet.ParquetFile(stream)
            else:
                handle = _pyarrow_parquet.ParquetFile(
                    self.plan.source_files[source_index]
                )
            self._parquet_handles[int(source_order)] = handle
        return handle

    def _parquet_row(self, source_order: int, row_index: int) -> Dict[str, Any]:
        source = int(source_order)
        target = int(row_index)
        if self.plan.omat_materialized:
            state = self._parquet_streams.get(source)
            if state is None or (
                state.get("access_mode") == "stream"
                and target < int(state.get("batch_start", 0))
            ):
                parquet = self._parquet_file(source)
                counts = np.asarray(
                    [
                        parquet.metadata.row_group(index).num_rows
                        for index in range(parquet.metadata.num_row_groups)
                    ],
                    dtype=np.int64,
                )
                if counts.size and int(np.max(counts)) <= 16_384:
                    state = {
                        "access_mode": "row_group",
                        "row_group_offsets": np.concatenate((
                            np.zeros((1,), dtype=np.int64),
                            np.cumsum(counts, dtype=np.int64),
                        )),
                        "row_group": -1,
                        "table": None,
                    }
                else:
                    # Identity shards retain their exact source bytes and may
                    # contain one very large row group. Stream small batches in
                    # selector order instead of materializing that group in RAM.
                    state = {
                        "access_mode": "stream",
                        "iterator": parquet.iter_batches(
                            batch_size=2048,
                            columns=list(OMAT24_PARQUET_COLUMNS),
                        ),
                        "next_start": 0,
                        "batch_start": 0,
                        "batch": None,
                    }
                self._parquet_streams[source] = state
            if state["access_mode"] == "row_group":
                offsets = state["row_group_offsets"]
                if target < 0 or target >= int(offsets[-1]):
                    raise IndexError(
                        f"Parquet row {target} is outside materialized shard {source}"
                    )
                row_group = int(np.searchsorted(offsets, target, side="right") - 1)
                if int(state["row_group"]) != row_group:
                    state["table"] = self._parquet_file(source).read_row_group(
                        row_group, columns=list(OMAT24_PARQUET_COLUMNS)
                    )
                    state["row_group"] = row_group
                local = target - int(offsets[row_group])
                return state["table"].slice(local, 1).to_pylist()[0]

            while True:
                batch = state.get("batch")
                start = int(state["batch_start"])
                if batch is not None and start <= target < start + len(batch):
                    return batch.slice(target - start, 1).to_pylist()[0]
                try:
                    batch = next(state["iterator"])
                except StopIteration as exc:
                    raise IndexError(
                        f"Parquet row {target} is outside materialized shard {source}"
                    ) from exc
                state["batch_start"] = int(state["next_start"])
                state["next_start"] = int(state["next_start"]) + len(batch)
                state["batch"] = batch

        state = self._parquet_streams.get(source)
        if state is None or target < int(state.get("batch_start", 0)):
            state = {
                "iterator": self._parquet_file(source).iter_batches(
                    batch_size=2048, columns=list(OMAT24_PARQUET_COLUMNS)
                ),
                "next_start": 0,
                "batch_start": 0,
                "batch": None,
            }
            self._parquet_streams[source] = state
        while True:
            batch = state.get("batch")
            start = int(state["batch_start"])
            if batch is not None and start <= target < start + len(batch):
                return batch.slice(target - start, 1).to_pylist()[0]
            try:
                batch = next(state["iterator"])
            except StopIteration as exc:
                raise IndexError(
                    f"Parquet row {target} is outside source shard {source}"
                ) from exc
            state["batch_start"] = int(state["next_start"])
            state["next_start"] = int(state["next_start"]) + len(batch)
            state["batch"] = batch

    def _configuration_at(self, position: int) -> Configuration:
        if position < self.omat_indices.size:
            selector = int(self.omat_indices[position])
            if self.plan.omat_packed:
                packed = self._large_handle["sources/omat24/packed"]
                start = int(packed["atom_ptr"][selector])
                end = int(packed["atom_ptr"][selector + 1])
                props: Dict[str, Any] = {
                    "energy": float(packed["energy"][selector]),
                    "forces": np.asarray(packed["forces"][start:end], dtype=np.float64),
                    "stress": np.asarray(packed["stress"][selector], dtype=np.float64),
                    "stress_volume_normalized": float(
                        packed["stress_volume_normalized"][selector]
                    ),
                    "method_id": str(self._large_handle["sources/omat24"].attrs.get(
                        "method_id", "OMat24/PBE+U"
                    )),
                    "group_id": str(packed["material_id"].asstr()[selector]),
                    "system_id": str(packed["material_id"].asstr()[selector]),
                    "sample_id": str(packed["configuration_id"].asstr()[selector]),
                    "provenance_id": (
                        f"OMat24:{int(self.plan.source_orders[selector])}:"
                        f"{int(packed['source_row_index'][selector])}"
                    ),
                    "energy_reference": "OMat24 PBE+U",
                    "dataset_role": "l1-foundation",
                    "curriculum_role": "base+joint",
                }
                return Configuration(
                    atomic_numbers=np.asarray(
                        packed["atomic_numbers"][start:end], dtype=int
                    ),
                    positions=np.asarray(packed["positions"][start:end], dtype=np.float64),
                    properties=props,
                    property_weights={
                        "energy": 1.0, "forces": 1.0, "stress": 1.0,
                        "stress_volume_normalized": 1.0,
                    },
                    cell=np.asarray(packed["cell"][selector], dtype=np.float64),
                    pbc=tuple(bool(value) for value in packed["pbc"][selector]),
                    head="OMat24/PBE+U",
                )
            source_order = int(self.plan.source_orders[selector])
            row_index = int(self.plan.row_indices[selector])
            row = self._parquet_row(source_order, row_index)
            source_path = Path(self.plan.source_files[source_order])
            corpus_name = source_path.parent.parent.name
            return _omat24_configuration_from_row(row, corpus_name=corpus_name)
        index = int(self.large_indices[position - self.omat_indices.size])
        cfg = _read_hdf5_configuration_at(
            self._large_handle, self.plan.large_plan, index, include_labels=True
        )
        role, curriculum = _large_curriculum_role(
            self.plan.large_plan.label_masks, index
        )
        cfg.properties["dataset_role"] = role
        cfg.properties["curriculum_role"] = curriculum
        if self.plan.mode in {"response", "joint"} and "energy" in cfg.properties:
            cfg.property_weights["energy"] = 0.0
        return cfg

    def __getitem__(self, item: int) -> AtomicData:
        self._ensure_handles()
        position = int(item)
        return AtomicData.from_config(
            self._configuration_at(position),
            z_table=self.z_table,
            cutoff=self.cutoff,
        )

    def __getitems__(self, items: Sequence[int]) -> List[AtomicData]:
        self._ensure_handles()
        return [
            AtomicData.from_config(
                self._configuration_at(int(item)),
                z_table=self.z_table,
                cutoff=self.cutoff,
            )
            for item in items
        ]

    def close(self) -> None:
        if self._large_handle is not None:
            try:
                self._large_handle.close()
            except Exception:
                pass
        self._large_handle = None
        self._parquet_handles.clear()
        self._embedded_streams.clear()
        self._parquet_streams.clear()
        self._handle_pid = None

    def __getstate__(self) -> Dict[str, Any]:
        state = dict(self.__dict__)
        state["_parquet_handles"] = {}
        state["_embedded_streams"] = {}
        state["_parquet_streams"] = {}
        state["_large_handle"] = None
        state["_handle_pid"] = None
        return state

    def __del__(self) -> None:
        self.close()


def fit_atomic_energies_from_composite_plan(
    plan: CompositeStreamPlan,
    zs: Sequence[int],
    *,
    max_samples: int = 1_000_000,
) -> np.ndarray:
    """Fit stable element references from a deterministic bounded composite sample."""
    z_to_col = {int(value): index for index, value in enumerate(zs)}
    normal = np.zeros((len(zs), len(zs)), dtype=np.float64)
    rhs = np.zeros((len(zs),), dtype=np.float64)
    with h5py.File(plan.path, "r") as handle:
        reference = handle["atomic_reference"]
        source_elements = np.asarray(reference["elements"][:], dtype=np.int16)
        source_normal = np.asarray(reference["normal_matrix"][:], dtype=np.float64)
        source_rhs = np.asarray(reference["rhs"][:], dtype=np.float64)
    for source_row, atomic_number in enumerate(source_elements):
        target_row = z_to_col.get(int(atomic_number))
        if target_row is None:
            continue
        rhs[target_row] = source_rhs[source_row]
        for source_column, other_number in enumerate(source_elements):
            target_column = z_to_col.get(int(other_number))
            if target_column is not None:
                normal[target_row, target_column] = source_normal[
                    source_row, source_column
                ]
    ridge = 1e-8 * max(1.0, float(np.trace(normal)) / max(1, len(zs)))
    try:
        return np.linalg.solve(normal + ridge * np.eye(len(zs)), rhs)
    except np.linalg.LinAlgError:
        return np.linalg.lstsq(normal + ridge * np.eye(len(zs)), rhs, rcond=None)[0]


class _ThreadPrefetchLoader:
    """Overlap bounded CPU/HDF5 batch assembly with accelerator execution."""

    def __init__(self, loader: DataLoader, depth: int = 2) -> None:
        self.loader = loader
        self.depth = max(1, int(depth))

    def __len__(self) -> int:
        return len(self.loader)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.loader, name)

    def __iter__(self) -> Iterable[Any]:
        output: queue.Queue = queue.Queue(maxsize=self.depth)
        stopped = threading.Event()
        sentinel = object()

        def offer(value: Any) -> bool:
            while not stopped.is_set():
                try:
                    output.put(value, timeout=0.1)
                    return True
                except queue.Full:
                    continue
            return False

        def produce() -> None:
            try:
                for value in self.loader:
                    if not offer(("value", value)):
                        return
            except BaseException as exc:
                offer(("error", exc))
            finally:
                offer(("end", sentinel))

        worker = threading.Thread(
            target=produce,
            name="e3mu-hdf5-prefetch",
            daemon=True,
        )
        worker.start()
        try:
            while True:
                kind, value = output.get()
                if kind == "end":
                    break
                if kind == "error":
                    raise value
                yield value
        finally:
            stopped.set()
            worker.join(timeout=2.0)



def _validate_configuration(cfg: Configuration, *, context: str) -> None:
    atomic_numbers = np.asarray(cfg.atomic_numbers, dtype=int).reshape(-1)
    positions = np.asarray(cfg.positions, dtype=float)
    if atomic_numbers.size == 0 or np.any(atomic_numbers <= 0):
        raise ValueError(f"{context}: invalid atomic numbers")
    if positions.shape != (len(atomic_numbers), 3) or not np.isfinite(positions).all():
        raise ValueError(f"{context}: positions must be finite with shape (N, 3)")
    cell = np.asarray(cfg.cell, dtype=float)
    if cell.shape != (3, 3) or not np.isfinite(cell).all():
        raise ValueError(f"{context}: cell must be finite with shape (3, 3)")
    for name, value in cfg.properties.items():
        if name not in HDF5_STRUCTURE_LABELS and name not in HDF5_ATOM_LABELS:
            continue
        array = np.asarray(value, dtype=float)
        if not np.isfinite(array).all():
            raise ValueError(f"{context}: label {name!r} contains non-finite values")



OMAT24_PARQUET_COLUMNS: Tuple[str, ...] = (
    "configuration_id",
    "configuration_hash",
    "structure_hash",
    "names",
    "method",
    "software",
    "energy",
    "atomic_forces",
    "cauchy_stress",
    "cauchy_stress_volume_normalized",
    "atomic_numbers",
    "positions",
    "cell",
    "pbc",
)


def _omat24_material_id(row: Dict[str, Any]) -> str:
    names = row.get("names") or []
    name = str(names[0]) if names else ""
    match = re.search(r"OMat24__(agm[0-9]+)_", name)
    return match.group(1) if match else str(row.get("configuration_id", "unknown"))


def _omat24_configuration_from_row(
    row: Dict[str, Any], *, corpus_name: str
) -> Configuration:
    """Decode one ColabFit OMat24 row without changing numerical values."""
    numbers = np.asarray(row["atomic_numbers"], dtype=np.int16).reshape(-1)
    positions = np.asarray(row["positions"], dtype=np.float64).reshape(-1, 3)
    forces = np.asarray(row["atomic_forces"], dtype=np.float64).reshape(-1, 3)
    if len(numbers) == 0 or positions.shape != (len(numbers), 3):
        raise ValueError("OMat24 row has inconsistent atoms/positions")
    if forces.shape != positions.shape:
        raise ValueError("OMat24 row has inconsistent positions/forces")
    configuration_id = str(row["configuration_id"])
    material_id = _omat24_material_id(row)
    source = f"OMat24/{corpus_name}"
    group_id = f"OMat24:{material_id}"
    props: Dict[str, Any] = {
        "energy": float(row["energy"]),
        "forces": forces,
        "source": source,
        "method_id": f"OMat24:{row.get('method') or 'PBE+U'}",
        "system_id": material_id,
        "group_id": group_id,
        "split": stable_split(group_id),
        "sample_id": f"OMat24:{configuration_id}",
        "parent_id": material_id,
        "domain": "periodic",
        "energy_reference": "OMat24:VASP-PBE+U:absolute",
        "provenance_id": (
            f"ColabFit:{corpus_name}:{configuration_id}:"
            f"{row.get('configuration_hash') or row.get('structure_hash') or 'unknown'}"
        ),
        "dataset_role": "l1-foundation",
        "curriculum_role": "base+joint",
    }
    weights: Dict[str, float] = {"energy": 1.0, "forces": 1.0}
    if row.get("cauchy_stress") is not None:
        stress = np.asarray(row["cauchy_stress"], dtype=np.float64).reshape(3, 3)
        props["stress"] = 0.5 * (stress + stress.T)
        props["stress_volume_normalized"] = float(
            bool(row.get("cauchy_stress_volume_normalized"))
        )
        weights.update({"stress": 1.0, "stress_volume_normalized": 1.0})
    cfg = Configuration(
        atomic_numbers=numbers,
        positions=positions,
        properties=props,
        property_weights=weights,
        cell=np.asarray(row["cell"], dtype=np.float64).reshape(3, 3),
        pbc=tuple(bool(value) for value in row["pbc"]),
        head=str(props["method_id"]),
    )
    _validate_configuration(cfg, context=f"OMat24/{configuration_id}")
    return cfg


def _large_curriculum_role(
    label_masks: Dict[str, np.ndarray], index: int
) -> Tuple[str, str]:
    response_labels = {
        "field", "dipole", "polarizability", "charges", "atomic_dipoles",
        "atomic_polarizability", "c6", "bec", "spins", "magnetic_moments",
        "effective_field", "J_effective", "Di", "Di_effective", "DMI_effective",
    }
    active_response = any(
        bool(mask[int(index)])
        for name, mask in label_masks.items()
        if name in response_labels
    )
    active_local = any(
        bool(label_masks[name][int(index)])
        for name in ("energy", "forces")
        if name in label_masks
    )
    if active_response:
        return "l1-l2-l3-response", "response+joint"
    if active_local:
        return "l1-non-equilibrium", "joint"
    return "auxiliary", "joint"



def _resolve_composite_source(composite: Path, raw_value: str) -> Path:
    value = Path(str(raw_value)).expanduser()
    return value.resolve() if value.is_absolute() else (composite.parent / value).resolve()



def inspect_composite_dataset(
    path: str, *, verify_sources: bool = False
) -> Dict[str, Any]:
    """Inspect Plus/Max selectors and strictly validate the embedded Large payload."""
    composite = Path(path).expanduser().resolve()
    with h5py.File(composite, "r") as handle:
        if str(handle.attrs.get("schema_version", "")) != COMPOSITE_HDF5_SCHEMA_VERSION:
            raise ValueError("Not an E3MU composite HDF5 dataset")
        omat = handle["sources/omat24"]
        omat_embedded = bool(omat.attrs.get("embedded", False))
        omat_storage = str(omat.attrs.get("storage", ""))
        omat_packed = omat_storage == OMAT24_PACKED_SCHEMA_VERSION
        omat_materialized = bool(omat.attrs.get("materialized", False)) or (
            omat_storage in {
                OMAT24_MATERIALIZED_SCHEMA_VERSION, OMAT24_PACKED_SCHEMA_VERSION
            }
        )
        omat_root = _resolve_composite_source(
            composite, str(omat.attrs.get("root", "."))
        )
        file_paths = [str(value) for value in omat["file_paths"].asstr()[:]]
        file_hashes = [str(value) for value in omat["file_sha256"].asstr()[:]]
        missing: List[str] = []
        mismatched: List[str] = []
        embedded_errors: List[str] = []
        selection = handle["selection"]
        selection_lengths = {
            name: int(selection[name].shape[0])
            for name in ("source_order", "row_index", "split_code", "atom_count")
            if name in selection
        }
        if "source_row_index" in selection:
            selection_lengths["source_row_index"] = int(
                selection["source_row_index"].shape[0]
            )
        required_lengths = {
            name: selection_lengths[name]
            for name in ("source_order", "row_index", "split_code", "atom_count")
            if name in selection_lengths
        }
        if len(required_lengths) != 4:
            embedded_errors.append("one or more OMat24 selector arrays are missing")
        elif len(set(selection_lengths.values())) != 1:
            embedded_errors.append(
                "OMat24 selector lengths disagree: "
                + json.dumps(selection_lengths, sort_keys=True)
            )
        source_counts = np.zeros((len(file_paths),), dtype=np.int64)
        selector_count = int(selection_lengths.get("source_order", 0))
        selector_chunk = 4_000_000
        if not embedded_errors and selector_count:
            for start in range(0, selector_count, selector_chunk):
                orders = np.asarray(
                    selection["source_order"][start:start + selector_chunk],
                    dtype=np.int64,
                )
                if np.any(orders < 0) or np.any(orders >= len(file_paths)):
                    embedded_errors.append(
                        "one or more selector source_order values exceed the "
                        f"{len(file_paths)} declared OMat24 shards"
                    )
                    break
                source_counts += np.bincount(orders, minlength=len(file_paths))
        if omat_embedded and omat_packed:
            packed = omat.get("packed")
            if packed is None:
                embedded_errors.append("packed OMat24 payload is missing")
            else:
                packed_structures = max(0, int(packed["atom_ptr"].shape[0]) - 1)
                if packed_structures != selector_count:
                    embedded_errors.append(
                        "packed OMat24 structure count does not match selectors"
                    )
                required = {
                    "atomic_numbers", "positions", "forces", "cell", "pbc",
                    "energy", "stress", "stress_volume_normalized",
                    "configuration_id", "material_id", "source_row_index",
                }
                absent = sorted(required - set(packed))
                if absent:
                    embedded_errors.append(
                        "packed OMat24 fields are missing: " + ", ".join(absent)
                    )
                elif selector_count and int(packed["atom_ptr"][-1]) != int(
                    np.sum(selection["atom_count"][:], dtype=np.int64)
                ):
                    embedded_errors.append("packed OMat24 atom count is inconsistent")
        elif omat_embedded:
            payload = omat.get("embedded_parquet")
            if payload is None or "shard_names" not in payload or "shards" not in payload:
                embedded_errors.append("embedded OMat24 shard payload is missing")
            else:
                shard_names = [str(value) for value in payload["shard_names"].asstr()[:]]
                if len(shard_names) != len(file_paths):
                    embedded_errors.append(
                        "embedded OMat24 shard count does not match file_paths"
                    )
                elif any(name not in payload["shards"] for name in shard_names):
                    embedded_errors.append("one or more embedded OMat24 shards are missing")
                expected_hashes = file_hashes
                if omat_materialized:
                    if "materialized_rows" not in payload:
                        embedded_errors.append(
                            "materialized OMat24 payload is missing materialized_rows"
                        )
                    elif "materialized_sha256" not in payload:
                        embedded_errors.append(
                            "materialized OMat24 payload is missing materialized_sha256"
                        )
                    else:
                        materialized_rows = np.asarray(
                            payload["materialized_rows"][:], dtype=np.int64
                        )
                        expected_hashes = [
                            str(value)
                            for value in payload["materialized_sha256"].asstr()[:]
                        ]
                        if materialized_rows.shape != source_counts.shape:
                            embedded_errors.append(
                                "materialized row-count array does not match source shards"
                            )
                        elif not np.array_equal(materialized_rows, source_counts):
                            embedded_errors.append(
                                "materialized row counts do not match selector counts"
                            )
                        elif selector_count:
                            for start in range(0, selector_count, selector_chunk):
                                orders = np.asarray(
                                    selection["source_order"][
                                        start:start + selector_chunk
                                    ],
                                    dtype=np.int64,
                                )
                                rows = np.asarray(
                                    selection["row_index"][
                                        start:start + selector_chunk
                                    ],
                                    dtype=np.int64,
                                )
                                if np.any(rows < 0) or np.any(
                                    rows >= materialized_rows[orders]
                                ):
                                    embedded_errors.append(
                                        "materialized selector row_index exceeds its shard"
                                    )
                                    break
                if verify_sources and not embedded_errors:
                    for name, expected in zip(shard_names, expected_hashes):
                        dataset = payload["shards"][name]
                        digest = hashlib.sha256()
                        for start in range(0, int(dataset.shape[0]), 8 * 1024 * 1024):
                            digest.update(
                                np.asarray(
                                    dataset[start:start + 8 * 1024 * 1024],
                                    dtype=np.uint8,
                                ).tobytes()
                            )
                        if digest.hexdigest() != expected:
                            mismatched.append(f"embedded://{name}")
        elif verify_sources:
            for relative, expected in zip(file_paths, file_hashes):
                source = omat_root / relative
                if not source.is_file():
                    missing.append(str(source))
                elif sha256_file(str(source)) != expected:
                    mismatched.append(str(source))
        large_group = handle["sources/neo_large"]
        large_embedded = bool(large_group.attrs.get("embedded", False))
        if large_embedded:
            absent = [
                name for name in HDF5_CANONICAL_ROOT_GROUPS if name not in handle
            ]
            if absent:
                embedded_errors.append(
                    "missing embedded groups: " + ", ".join(absent)
                )
            else:
                atom_ptr = handle["structures/atom_ptr"]
                embedded_structures = max(0, int(atom_ptr.shape[0]) - 1)
                embedded_atoms = int(atom_ptr[-1]) if atom_ptr.shape[0] else 0
                declared_structures = int(large_group.attrs["structures"])
                declared_atoms = int(large_group.attrs["atoms"])
                if embedded_structures != declared_structures:
                    embedded_errors.append(
                        f"embedded structures={embedded_structures}, "
                        f"declared={declared_structures}"
                    )
                if embedded_atoms != declared_atoms:
                    embedded_errors.append(
                        f"embedded atoms={embedded_atoms}, declared={declared_atoms}"
                    )
                for name, dataset in handle["metadata"].items():
                    if int(dataset.shape[0]) != declared_structures:
                        embedded_errors.append(
                            f"metadata/{name} length={dataset.shape[0]}"
                        )
                for name, dataset in handle["masks"].items():
                    if int(dataset.shape[0]) != declared_structures:
                        embedded_errors.append(
                            f"masks/{name} length={dataset.shape[0]}"
                        )
                for name, dataset in handle["labels"].items():
                    expected = (
                        declared_atoms if name in HDF5_ATOM_LABELS
                        else declared_structures
                    )
                    if int(dataset.shape[0]) != expected:
                        embedded_errors.append(
                            f"labels/{name} length={dataset.shape[0]}, expected={expected}"
                        )
        else:
            raw_path = str(large_group.attrs.get("path", ""))
            large = _resolve_composite_source(composite, raw_path)
            if verify_sources:
                if not large.is_file():
                    missing.append(str(large))
                elif sha256_file(str(large)) != str(
                    large_group.attrs.get("sha256", "")
                ):
                    mismatched.append(str(large))
        metadata = json.loads(str(handle.attrs.get("metadata_json", "{}")))
        split_names = np.asarray(["train", "val", "test"], dtype=object)
        codes = np.asarray(handle["selection/split_code"][:], dtype=np.uint8)
        split_counts = np.bincount(codes, minlength=3)
        splits = {
            str(split_names[index]): int(count)
            for index, count in enumerate(split_counts)
            if int(count) > 0
        }
        large_info = dict(metadata.get("neo_large", {}))
        for name, count in dict(large_info.get("splits", {})).items():
            splits[str(name)] = splits.get(str(name), 0) + int(count)
        labels = {"energy": int(handle.attrs["omat24_structures"]),
                  "forces": int(handle.attrs["omat24_structures"]),
                  "stress": int(handle.attrs["omat24_structures"])}
        for name, count in dict(large_info.get("labels", {})).items():
            labels[str(name)] = labels.get(str(name), 0) + int(count)
        return {
            "ready": not missing and not mismatched and not embedded_errors,
            "valid": not missing and not mismatched and not embedded_errors,
            "path": str(composite),
            "kind": "Neo composite HDF5",
            "schema_version": COMPOSITE_HDF5_SCHEMA_VERSION,
            "tier": str(handle.attrs["tier"]),
            "structures": int(handle.attrs["structures"]),
            "atoms": int(handle.attrs.get("atoms", 0)),
            "elements": [int(value) for value in json.loads(
                str(handle.attrs.get("elements_json", "[]"))
            )],
            "omat24_structures": int(handle.attrs["omat24_structures"]),
            "large_structures": int(handle.attrs["large_structures"]),
            "periodic_structures": int(handle.attrs["omat24_structures"])
                + int(large_info.get("periodic_structures", 0)),
            "labels": labels,
            "splits": dict(sorted(splits.items())),
            "sources": {
                **{f"OMat24/{item['name']}": int(item["selected_unique"])
                   for item in metadata.get("omat24", {}).get("corpora", [])},
                **{str(name): int(count)
                   for name, count in dict(large_info.get("sources", {})).items()},
            },
            "missing_sources": missing,
            "checksum_mismatches": mismatched,
            "embedded_large": large_embedded,
            "embedded_omat24": omat_embedded,
            "materialized_omat24": omat_materialized,
            "omat24_storage": omat_storage,
            "embedded_errors": embedded_errors,
            "source_files": len(file_paths),
            "sha256": sha256_file(str(composite)) if verify_sources else None,
        }



_CAPABILITY_STRUCTURE_ALIASES: Dict[str, set] = {
    "energy": {"energy"},
    "energy_dispersion": {"energy_dispersion"},
    "field": {"field"},
    "dipole": {"dipole"},
    "polarizability": {"polarizability"},
    "total_charge": {"total_charge"},
    "J_effective": {"J_effective", "j_effective"},
    "DMI_effective": {"DMI_effective", "dmi_effective"},
    "Di_effective": {"Di_effective", "di_effective"},
    "soc": {"soc"},
}
_CAPABILITY_ATOM_ALIASES: Dict[str, set] = {
    "forces": {"forces", "force", "F"},
    "forces_dispersion": {"forces_dispersion"},
    "charges": {"charges", "charge", "q", "hCHG"},
    "atomic_dipoles": {"atomic_dipoles", "hVDIP"},
    "atomic_polarizability": {"atomic_polarizability", "atPOL"},
    "c6": {"c6", "C6", "atC6"},
    "bec": {"bec", "BEC"},
    "spins": {"spins", "spin"},
    "magnetic_moments": {"magmoms", "magmom", "magnetic_moments"},
    "effective_field": {"effective_field", "spin_field"},
    "Di": {"Di", "di"},
}


def inspect_dataset_capabilities(path: str) -> Dict[str, Any]:
    """Read only dataset metadata needed by the GUI architecture guard."""
    dataset = Path(path).expanduser()
    if not dataset.is_file():
        raise FileNotFoundError(str(dataset))
    labels: Dict[str, int] = {}
    elements: set = set()
    structures = 0
    periodic_structures = 0

    if _is_hdf5_path(str(dataset)):
        if not HAS_H5PY:
            raise RuntimeError("HDF5 capability detection requires h5py")
        with h5py.File(dataset, "r") as handle:
            if str(handle.attrs.get("schema_version", "")) == COMPOSITE_HDF5_SCHEMA_VERSION:
                return inspect_composite_dataset(str(dataset), verify_sources=False)
            ptr = np.asarray(handle["structures/atom_ptr"], dtype=np.int64)
            structures = int(len(ptr) - 1)
            elements.update(
                int(value)
                for value in np.unique(handle["structures/atomic_numbers"][:])
            )
            if "masks" in handle:
                labels = {
                    str(name): int(np.count_nonzero(handle["masks"][name][:]))
                    for name in handle["masks"].keys()
                }
            if "structures/pbc" in handle:
                pbc = np.asarray(handle["structures/pbc"], dtype=bool).reshape(-1, 3)
                periodic_structures = int(np.count_nonzero(np.any(pbc, axis=1)))
        kind = "canonical HDF5"
    else:
        with _open_text(str(dataset)) as handle:
            while True:
                first_line = handle.readline()
                if not first_line:
                    break
                first_line = first_line.strip()
                if not first_line:
                    continue
                atom_count = int(first_line)
                comment = handle.readline()
                if not comment:
                    break
                try:
                    info = key_val_str_to_dict(comment.strip())
                except Exception:
                    info = {}
                try:
                    properties = _parse_properties_spec(
                        str(info.get("Properties", "species:S:1:pos:R:3"))
                    )
                except Exception:
                    properties = [("species", "S", 1), ("pos", "R", 3)]
                property_names = {name for name, _kind, _width in properties}
                frame_labels = {
                    canonical
                    for canonical, aliases in _CAPABILITY_STRUCTURE_ALIASES.items()
                    if any(alias in info for alias in aliases)
                }
                frame_labels.update(
                    canonical
                    for canonical, aliases in _CAPABILITY_ATOM_ALIASES.items()
                    if bool(property_names & aliases)
                )
                for label in frame_labels:
                    labels[label] = labels.get(label, 0) + 1

                has_lattice = "Lattice" in info
                pbc = (
                    _parse_pbc(info.get("pbc"))
                    if "pbc" in info
                    else (True, True, True) if has_lattice else (False, False, False)
                )
                periodic_structures += int(any(pbc))

                offsets: Dict[str, Tuple[int, int]] = {}
                offset = 0
                for name, _kind, width in properties:
                    offsets[name] = (offset, int(width))
                    offset += int(width)
                symbol_column = next(
                    (offsets[name] for name in ("species", "symbol") if name in offsets),
                    None,
                )
                number_column = next(
                    (
                        offsets[name]
                        for name in ("Z", "atomic_number", "atomic_numbers")
                        if name in offsets
                    ),
                    None,
                )
                for _atom_index in range(atom_count):
                    row = handle.readline()
                    if not row:
                        raise ValueError(f"Unexpected end of file in {dataset}")
                    tokens = row.split()
                    try:
                        if number_column is not None:
                            elements.add(int(float(tokens[number_column[0]])))
                        elif symbol_column is not None:
                            symbol = str(tokens[symbol_column[0]]).capitalize()
                            elements.add(int(ASE_ATOMIC_NUMBERS[symbol]))
                    except (IndexError, KeyError, ValueError):
                        continue
                structures += 1
        kind = "legacy extXYZ"

    return {
        "ready": True,
        "path": str(dataset.resolve()),
        "kind": kind,
        "structures": int(structures),
        "periodic_structures": int(periodic_structures),
        "elements": sorted(int(value) for value in elements),
        "labels": {str(name): int(count) for name, count in labels.items()},
    }


def merge_dataset_capabilities(capabilities: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge canonical or legacy-role capability reports."""
    reports = [report for report in capabilities if bool(report.get("ready"))]
    if not reports:
        return {
            "ready": False,
            "structures": 0,
            "periodic_structures": 0,
            "elements": [],
            "labels": {},
        }
    labels: Dict[str, int] = {}
    for report in reports:
        for name, count in dict(report.get("labels", {})).items():
            labels[str(name)] = labels.get(str(name), 0) + int(count)
    return {
        "ready": True,
        "kind": " + ".join(str(report.get("kind", "dataset")) for report in reports),
        "paths": [str(report.get("path", "")) for report in reports],
        "structures": sum(int(report.get("structures", 0)) for report in reports),
        "periodic_structures": sum(
            int(report.get("periodic_structures", 0)) for report in reports
        ),
        "elements": sorted(
            set().union(*(set(report.get("elements", [])) for report in reports))
        ),
        "labels": labels,
    }


def architecture_switch_availability(
    capability: Dict[str, Any],
    *,
    has_torchpme: bool = HAS_TORCHPME,
    has_dftd4: bool = HAS_TAD_DFTD4,
) -> Dict[str, Tuple[bool, str]]:
    """Return data-aware availability and a concise reason for every switch."""
    keys = (
        "e3mu_use_parity", "e3mu_use_l3", "enable_continuous_chem",
        "enable_qeq", "enable_pme", "enable_deq", "enable_d4",
        "enable_spin", "enable_film", "enable_dmi",
    )
    if not bool(capability.get("ready")):
        return {key: (True, "Select a dataset to evaluate this switch") for key in keys}

    labels = {
        str(name)
        for name, count in dict(capability.get("labels", {})).items()
        if int(count) > 0
    }
    elements = set(capability.get("elements", []))
    periodic = int(capability.get("periodic_structures", 0)) > 0
    local_signal = bool(labels & {"energy", "forces"})
    electric_signal = bool(
        labels
        & {
            "charges", "dipole", "polarizability", "atomic_dipoles",
            "atomic_polarizability", "c6", "bec",
        }
    )
    polarization_signal = bool(
        labels & {"dipole", "polarizability", "atomic_polarizability", "bec"}
    )
    dispersion_signal = bool(
        labels & {"energy", "forces", "energy_dispersion", "forces_dispersion", "c6"}
    )
    magnetic_targets = bool(
        labels
        & {
            "magnetic_moments", "effective_field", "J_effective", "Di",
            "Di_effective", "DMI_effective",
        }
    )
    spin_signal = "spins" in labels and (magnetic_targets or "energy" in labels)
    dmi_signal = spin_signal and (
        "DMI_effective" in labels or ("soc" in labels and "energy" in labels)
    )

    availability: Dict[str, Tuple[bool, str]] = {
        "e3mu_use_parity": (True, "Core symmetry option; independent of labels"),
        "e3mu_use_l3": (True, "Higher-order geometric channel; independent of labels"),
        "enable_continuous_chem": (
            len(elements) > 1,
            "Requires at least two chemical elements" if len(elements) <= 1 else "Supported",
        ),
        "enable_qeq": (
            electric_signal,
            "Requires charge, dipole, polarizability, C6, or BEC supervision"
            if not electric_signal else "Supported",
        ),
        "enable_pme": (
            electric_signal and periodic and has_torchpme,
            "torch-pme is not installed"
            if not has_torchpme
            else "Requires periodic structures"
            if not periodic
            else "Requires electric-response supervision"
            if not electric_signal
            else "Supported",
        ),
        "enable_deq": (
            polarization_signal,
            "Requires dipole, polarizability, atomic polarizability, or BEC labels"
            if not polarization_signal else "Supported",
        ),
        "enable_d4": (
            dispersion_signal and has_dftd4,
            "tad-dftd4 is not installed"
            if not has_dftd4
            else "Requires energy, force, dispersion-energy, or C6 labels"
            if not dispersion_signal
            else "Supported for molecular graphs; periodic graphs are masked",
        ),
        "enable_spin": (
            spin_signal,
            "Requires spin vectors plus magnetic or spin-resolved energy labels"
            if not spin_signal else "Supported",
        ),
        "enable_film": (
            local_signal and (electric_signal or spin_signal),
            "Requires local energy/force labels and an electric or spin domain"
            if not (local_signal and (electric_signal or spin_signal)) else "Supported",
        ),
        "enable_dmi": (
            dmi_signal,
            "Requires DMI labels or SOC spin-energy configurations"
            if not dmi_signal else "Supported",
        ),
    }
    return availability


ARCHITECTURE_SWITCH_PARAMETERS: Tuple[str, ...] = (
    "e3mu_use_parity",
    "e3mu_use_l3",
    "enable_continuous_chem",
    "enable_qeq",
    "enable_pme",
    "enable_deq",
    "enable_d4",
    "enable_spin",
    "enable_film",
    "enable_dmi",
)

DATASET_LOSS_LABELS: Dict[str, set] = {
    "w_energy": {"energy"},
    "w_forces": {"forces"},
    "w_dipole": {"dipole"},
    "w_polarizability": {"polarizability"},
    "w_charges": {"charges"},
    "w_atomic_dipoles": {"atomic_dipoles"},
    "w_atomic_polarizability": {"atomic_polarizability"},
    "w_c6": {"c6"},
    "w_bec": {"bec"},
    "w_magnetic_moments": {"magnetic_moments"},
    "w_effective_field": {"effective_field"},
    "w_j": {"J_effective"},
    "w_di": {"Di", "Di_effective"},
    "w_dmi": {"DMI_effective"},
}


def _architecture_value(values: Any, name: str, default: bool = False) -> bool:
    if isinstance(values, dict):
        return bool(values.get(name, default))
    return bool(getattr(values, name, default))


def _parameter_value(values: Any, name: str, default: Any) -> Any:
    if isinstance(values, dict):
        return values.get(name, default)
    return getattr(values, name, default)


def _live_numeric_parameter(
    values: Any,
    name: str,
    default: Any,
    converter: Callable[[Any], Any] = float,
) -> Any:
    """Read transient GUI numeric text without raising during editing.

    Live tooltips and search previews run on every ``textChanged`` signal. An
    empty or partially typed value is therefore expected; strict validation is
    still performed when a training/search action is started.
    """
    value = _parameter_value(values, name, default)
    try:
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError
        converted = converter(value)
        if isinstance(converted, float) and not math.isfinite(converted):
            raise ValueError
        return converted
    except (TypeError, ValueError, OverflowError):
        return converter(default)


def _plan_structure_batches(
    item_loads: Sequence[int],
    batch_size: int,
    *,
    max_load: Optional[int] = None,
) -> Tuple[List[List[int]], List[int]]:
    """Best-fit deterministic packing used by the MPS edge safety policy."""
    limit = max(1, int(batch_size))
    loads = [max(0, int(value)) for value in item_loads]
    ranked = sorted(range(len(loads)), key=lambda index: loads[index], reverse=True)
    batches: List[List[int]] = []
    batch_loads: List[int] = []
    for index in ranked:
        item_load = loads[index]
        candidates = [
            batch_index
            for batch_index, indices in enumerate(batches)
            if len(indices) < limit
            and (max_load is None or batch_loads[batch_index] + item_load <= max_load)
        ]
        if candidates:
            target = max(candidates, key=lambda batch_index: batch_loads[batch_index])
            batches[target].append(index)
            batch_loads[target] += item_load
        else:
            batches.append([index])
            batch_loads.append(item_load)
    return batches, batch_loads


def batch_plan_summary(
    item_loads: Sequence[int],
    batch_size: int,
    *,
    device_type: str,
    max_edges: Optional[int] = None,
) -> Dict[str, Any]:
    """Return backend-specific batch counts without loading graph tensors."""
    count = len(item_loads)
    requested = max(1, int(batch_size))
    effective = max(1, min(requested, count if count else 1))
    if str(device_type).lower() != "mps":
        return {
            "device": str(device_type).lower(),
            "requested_batch_size": requested,
            "steps": int(math.ceil(count / effective)) if count else 0,
            "structure_loads": [
                min(effective, count - start) for start in range(0, count, effective)
            ],
            "edge_loads": None,
            "edge_budget": None,
        }
    batches, edge_loads = _plan_structure_batches(
        item_loads, effective, max_load=max_edges
    )
    return {
        "device": "mps",
        "requested_batch_size": requested,
        "steps": len(batches),
        "structure_loads": [len(indices) for indices in batches],
        "edge_loads": edge_loads,
        "edge_budget": max_edges,
    }


def architecture_parameter_relevance(values: Any) -> Dict[str, Tuple[bool, str]]:
    """Resolve which controls are meaningful for a fixed architecture.

    The result is intentionally GUI-toolkit agnostic. Both the Qt front end and
    AutoSearch use this function so inactive sublayers cannot retain editable
    solver controls or enter the search space accidentally.
    """
    qeq = _architecture_value(values, "enable_qeq")
    pme = _architecture_value(values, "enable_pme")
    deq = _architecture_value(values, "enable_deq")
    d4 = _architecture_value(values, "enable_d4")
    spin = _architecture_value(values, "enable_spin")
    film = _architecture_value(values, "enable_film")
    dmi = _architecture_value(values, "enable_dmi")
    continuous_chem = _architecture_value(values, "enable_continuous_chem")
    electrostatic = qeq or pme
    electric_domain = electrostatic or deq or d4
    mixed_domain = electric_domain or spin

    return {
        "enable_dmi": (
            spin,
            "DMI is part of the spin Hamiltonian and requires Spin.",
        ),
        "enable_film": (
            mixed_domain,
            "FiLM feedback requires at least one electric or spin domain layer.",
        ),
        "qeq_smearing": (
            electrostatic or deq,
            "Used only by QEq/PME electrostatics or DEQ dipole damping.",
        ),
        "qeq_hardness_min": (
            electrostatic,
            "Atomic hardness is used only by QEq/PME charge equilibration.",
        ),
        "qeq_stability_floor": (
            electrostatic,
            "The neutral-space stability floor is used only by QEq/PME.",
        ),
        "qeq_pme_smearing": (
            pme,
            "Real/reciprocal Ewald splitting is active only when PME is enabled.",
        ),
        "qeq_pme_lr_wavelength": (
            pme,
            "The reciprocal-space wavelength is active only when PME is enabled.",
        ),
        "deq_max_iter": (False, "Legacy setting; the stable direct DEQ solve has no iteration cap."),
        "deq_tol": (False, "Diagnostic compatibility setting; the direct DEQ solve is not tolerance-truncated."),
        "deq_damping": (
            deq,
            "Thole damping is used only by the DEQ induced-dipole interaction.",
        ),
        "deq_alpha_max": (deq, "The polarizability cap is used only by DEQ polarization."),
        "d4_functional": (d4, "The reference functional is used only by D4 dispersion."),
        "spin_cutoff": (spin, "Magnetic pair construction is active only when Spin is enabled."),
        "coupling_iterations": (film, "Outer coupling iterations are used only by FiLM feedback."),
        "coupling_tol": (film, "The coupling tolerance is used only by FiLM feedback."),
        "chem_max_z": (
            continuous_chem,
            "The periodic-table descriptor table is used only by continuous chemistry.",
        ),
        "chem_aug_prob": (
            continuous_chem,
            "Alchemical augmentation is used only by continuous chemistry.",
        ),
        "chem_aug_noise_std": (
            continuous_chem,
            "Descriptor noise is used only by continuous chemistry.",
        ),
        "chem_aug_mix_max": (
            continuous_chem,
            "Element mixing is used only by continuous chemistry.",
        ),
        "w_charges": (electrostatic, "Charge supervision requires QEq or PME."),
        "w_atomic_dipoles": (
            electrostatic or deq,
            "Atomic dipole supervision requires an electrostatic or DEQ domain.",
        ),
        "w_atomic_polarizability": (
            electrostatic or deq,
            "Atomic polarizability supervision requires an electrostatic or DEQ domain.",
        ),
        "w_c6": (d4, "C6 supervision is meaningful only when D4 is enabled."),
        "w_magnetic_moments": (spin, "Magnetic moments require the spin Hamiltonian."),
        "w_effective_field": (spin, "Effective spin fields require the spin Hamiltonian."),
        "w_j": (spin, "Exchange J requires the spin Hamiltonian."),
        "w_di": (spin, "Single-ion anisotropy Di requires the spin Hamiltonian."),
        "w_dmi": (spin and dmi, "DMI supervision requires both Spin and DMI."),
    }


def dataset_loss_parameter_availability(
    capability: Dict[str, Any],
) -> Dict[str, Tuple[bool, str]]:
    """Return whether each loss parameter has labels in the selected dataset."""
    if not bool(capability.get("ready")):
        return {
            name: (True, "Select a dataset to verify target labels")
            for name in DATASET_LOSS_LABELS
        }
    labels = {
        str(name)
        for name, count in dict(capability.get("labels", {})).items()
        if int(count) > 0
    }
    return {
        name: (
            bool(labels & supported_labels),
            "Supported"
            if labels & supported_labels
            else f"Dataset has no {'/'.join(sorted(supported_labels))} labels.",
        )
        for name, supported_labels in DATASET_LOSS_LABELS.items()
    }


def architecture_locked_search_exclusions(
    values: Any,
    capability: Optional[Dict[str, Any]] = None,
) -> set:
    """Return dimensions excluded when AutoSearch respects the selected architecture."""
    excluded = set(ARCHITECTURE_SWITCH_PARAMETERS)
    excluded.update(
        name
        for name, (relevant, _reason) in architecture_parameter_relevance(values).items()
        if not relevant
    )
    if capability is not None:
        excluded.update(
            name
            for name, (available, _reason) in architecture_switch_availability(capability).items()
            if not available
        )
        excluded.update(
            name
            for name, (available, _reason) in dataset_loss_parameter_availability(capability).items()
            if not available
        )
    return excluded


def dynamic_parameter_reference_ranges(
    values: Any,
    capability: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    """Describe reference ranges that depend on the current model and dataset."""
    capability = capability or {"ready": False}
    structures = max(0, int(capability.get("structures", 0) or 0))
    periodic = int(capability.get("periodic_structures", 0) or 0) > 0
    elements = []
    for value in capability.get("elements", []):
        try:
            elements.append(int(value))
        except (TypeError, ValueError, OverflowError):
            continue
    r_max = max(0.5, _live_numeric_parameter(values, "r_max", 5.0))
    hardness = max(
        1e-4, _live_numeric_parameter(values, "qeq_hardness_min", 0.25)
    )
    deq_tol = max(1e-10, _live_numeric_parameter(values, "deq_tol", 1e-6))
    channels = max(
        1, _live_numeric_parameter(values, "num_channels", 64, lambda x: int(float(x)))
    )
    active_physics = sum(
        int(_architecture_value(values, name))
        for name in (
            "enable_qeq", "enable_pme", "enable_deq", "enable_d4",
            "enable_spin", "enable_film",
        )
    )
    r_low, r_high = ((5.0, 10.0) if periodic else (4.0, 8.0))
    if _architecture_value(values, "enable_spin"):
        spin_value = _compatible_spin_cutoff(
            r_max, _live_numeric_parameter(values, "spin_cutoff", r_max)
        )
        r_low = max(r_low, min(spin_value, 8.0))
        r_high = max(r_high, r_low)
    spin_low = min(r_max, max(0.5, min(4.0, 0.65 * r_max)))
    qeq_smear_low = max(0.10, 0.03 * r_max)
    qeq_smear_high = min(1.20, max(0.35, 0.16 * r_max))
    stability_low = max(1e-3, 0.04 * hardness)
    stability_high = max(stability_low * 5.0, min(2.0, 4.0 * hardness))
    min_validation = 0.2 if 0 < structures < 50 else 0.1 if structures < 500 else 0.05
    max_validation = 0.3 if 0 < structures < 50 else 0.2
    min_subset = min(100.0, 10000.0 / structures) if structures else 1.0
    lr_high = 2e-3 if channels >= 96 or active_physics >= 4 else 5e-3
    channel_range = "64-128" if active_physics >= 4 else "32-96"

    return {
        "r_max": (
            f"{r_low:.1f}-{r_high:.1f} Angstrom"
            + ("; must be >= Spin cutoff" if _architecture_value(values, "enable_spin") else "")
        ),
        "spin_cutoff": f"{spin_low:.2g}-{r_max:.3g} Angstrom; cannot exceed r_max",
        "num_channels": f"{channel_range}; more active physics layers favor the upper half",
        "num_interactions": "2-4 message-passing blocks; use 1-2 only for very small smoke tests",
        "num_radial_basis": "6-16; increase with r_max and geometric diversity",
        "lr": f"1e-4-{lr_high:.0e}; large/back-coupled models favor the lower half",
        "batch_size": (
            "1-8 for Spin/PME/FiLM-heavy models; 2-16 otherwise"
            if active_physics >= 3 else "2-16; reduce when memory or force Hessians dominate"
        ),
        "val_fraction": f"{min_validation:.2g}-{max_validation:.2g} for {structures or 'unknown'} structures",
        "qeq_smearing": f"{qeq_smear_low:.3g}-{qeq_smear_high:.3g} Angstrom for r_max={r_max:.3g}",
        "qeq_hardness_min": "0.05-2.0 eV; raise it when charge amplitudes or conditioning are unstable",
        "qeq_stability_floor": f"{stability_low:.3g}-{stability_high:.3g} eV from hardness={hardness:.3g}",
        "qeq_pme_smearing": "0.5-2.0 Angstrom; balance real- and reciprocal-space work",
        "qeq_pme_lr_wavelength": f"{max(0.35, 0.08 * r_max):.3g}-{min(2.0, 0.30 * r_max):.3g} Angstrom",
        "deq_max_iter": "35-100; tighter tolerance and strong polarizability require more iterations",
        "deq_tol": "1e-7-1e-4; 1e-6 is a balanced training default",
        "deq_damping": (
            "0.2-0.8 dimensionless Thole parameter; lower values damp short-range "
            "dipole coupling more strongly"
        ),
        "deq_alpha_max": "10-300 Angstrom^3; keep close to the largest plausible atomic response",
        "coupling_iterations": "1-4 outer updates; start at 2",
        "coupling_tol": f"{max(1e-8, deq_tol * 0.1):.1e}-{max(1e-4, deq_tol * 100):.1e} relative to DEQ tol={deq_tol:.1e}",
        "chem_max_z": f"{max(elements) if elements else 1}-118; must cover every selected element",
        "chem_aug_prob": "0-0.30; start at 0.05 only after a stable non-augmented baseline",
        "chem_aug_noise_std": "0-0.10 standardized descriptor units",
        "chem_aug_mix_max": "0-0.30; keep below 0.15 for chemically narrow datasets",
        "auto_subset": f"{min_subset:.3g}-100%; aim for at least 100 structures per search trial",
    }


def dynamic_architecture_search_space(
    values: Any,
    capability: Optional[Dict[str, Any]] = None,
) -> Dict[str, tuple]:
    """Build data- and architecture-aware overrides for AutoSearch samplers."""
    capability = capability or {"ready": False}
    periodic = int(capability.get("periodic_structures", 0) or 0) > 0
    r_choices = (
        [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        if periodic
        else [4.0, 5.0, 6.0, 7.0, 8.0]
    )
    active_physics = sum(
        int(_architecture_value(values, name))
        for name in (
            "enable_qeq", "enable_pme", "enable_deq", "enable_d4",
            "enable_spin", "enable_film",
        )
    )
    channel_choices = [64, 96, 128] if active_physics >= 4 else [32, 48, 64, 96]
    r_max = max(0.5, _live_numeric_parameter(values, "r_max", 5.0))
    r_choices = sorted({*r_choices, round(r_max, 6)})
    hardness = max(
        1e-4, _live_numeric_parameter(values, "qeq_hardness_min", 0.25)
    )
    qeq_low = max(0.10, 0.03 * r_max)
    qeq_high = min(1.20, max(0.35, 0.16 * r_max))
    spin_low = min(r_max, max(0.5, min(4.0, 0.65 * r_max)))
    current_spin = _compatible_spin_cutoff(
        r_max, _live_numeric_parameter(values, "spin_cutoff", r_max)
    )
    spin_choices = sorted(
        {
            round(max(spin_low, min(r_max, value)), 6)
            for value in (
                spin_low,
                0.80 * r_max,
                0.90 * r_max,
                current_spin,
                r_max,
            )
        }
    )
    return {
        "lr": ("log_uniform", 1e-4, 2e-3 if active_physics >= 4 else 5e-3),
        "batch_size": ("choice", [1, 2, 4, 8] if active_physics >= 3 else [2, 4, 8, 16]),
        "r_max": ("choice", r_choices),
        "num_channels": ("choice", channel_choices),
        "qeq_smearing": ("uniform", qeq_low, qeq_high),
        "qeq_stability_floor": (
            "log_uniform", max(1e-3, 0.04 * hardness), max(0.05, min(2.0, 4.0 * hardness))
        ),
        "qeq_pme_lr_wavelength": (
            "uniform", max(0.35, 0.08 * r_max), min(2.0, 0.30 * r_max)
        ),
        "qeq_pme_smearing": (
            "uniform", max(0.35, 0.10 * r_max), min(2.5, 0.35 * r_max)
        ),
        # The direct DEQ equilibrium solve has no iterative damping/truncation;
        # only its physical polarizability cap remains an active dimension.
        "deq_alpha_max": (
            "log_uniform",
            max(5.0, 10.0 * hardness),
            max(25.0, min(300.0, 400.0 * hardness)),
        ),
        "deq_damping": ("uniform", 0.2, 0.8),
        "spin_cutoff": ("choice", spin_choices),
        "coupling_iterations": (
            "randint", 1, 2 if active_physics >= 4 else 4
        ),
        "coupling_tol": (
            "log_uniform", 1e-7, 1e-4 if active_physics >= 4 else 1e-3
        ),
        "chem_aug_prob": ("choice", [0.0, 0.025, 0.05, 0.10, 0.20, 0.30]),
        "chem_aug_noise_std": ("choice", [0.0, 0.005, 0.01, 0.025, 0.05, 0.10]),
        "chem_aug_mix_max": ("choice", [0.0, 0.025, 0.05, 0.10, 0.20, 0.30]),
    }


def estimate_model_parameter_count(
    cfg: ModelConfig,
    elements: Sequence[int],
) -> Dict[str, int]:
    """Instantiate the configured architecture on CPU and count its parameters."""
    element_values = sorted({int(value) for value in elements if int(value) > 0}) or [1]
    z_table = AtomicNumberTable(element_values)
    model_cls = (
        MixedGranularityE3GNN
        if any(
            bool(getattr(cfg, name, False))
            for name in (
                "enable_qeq", "enable_pme", "enable_deq", "enable_d4",
                "enable_spin", "enable_film",
            )
        )
        else DualLayerFieldModel
    )
    with _isolated_torch_runtime():
        model = model_cls(
            z_table=z_table,
            atomic_energies_1d=np.zeros(len(element_values), dtype=float),
            cfg=cfg,
        )
        counts = {
            "total": sum(int(parameter.numel()) for parameter in model.parameters()),
            "trainable": sum(
                int(parameter.numel()) for parameter in model.parameters() if parameter.requires_grad
            ),
            "ground": sum(
                int(parameter.numel()) for parameter in model.ground.parameters()
            ),
            "response": sum(
                int(parameter.numel()) for parameter in model.response.parameters()
            ),
            "physics": sum(
                int(parameter.numel())
                for name, parameter in model.named_parameters()
                if not name.startswith("ground.") and not name.startswith("response.")
            ),
            "elements": len(element_values),
        }
        del model
    return counts



def get_neighborhood(
    *,
    positions: np.ndarray,
    cutoff: float,
    pbc: Tuple[bool, bool, bool],
    cell: Optional[np.ndarray],
) -> Tuple[np.ndarray, Any, Any]:
    """Build a neighbor list with either MACE or ASE.

    MACE is preferred when available because it handles periodic systems more
    robustly and is typically faster. ASE remains the fallback so the parser and
    training loop still work in a minimal environment.
    """
    if not any(bool(value) for value in pbc):
        edge_index, _shifts = _fast_nonperiodic_neighborhood(
            np.asarray(positions, dtype=float), float(cutoff)
        )
        return edge_index, None, None
    if HAS_MACE_NEIGHBORHOOD and _mace_get_neighborhood is not None:
        return _mace_get_neighborhood(positions=positions, cutoff=float(cutoff), pbc=pbc, cell=cell)
    atoms = Atoms(numbers=np.ones((len(positions),), dtype=int), positions=positions, cell=cell, pbc=pbc)
    i, j = neighbor_list("ij", atoms, cutoff=float(cutoff))
    edge_index = np.stack([i, j], axis=0)
    return edge_index, None, None


def avg_num_neighbors_from_configs(configs: Sequence[Configuration], r_max: float) -> float:
    """Estimate the average number of neighbors per atom for a cutoff."""
    tot_neighbors = 0
    tot_atoms = 0
    for cfg in configs:
        edge_index, *_ = get_neighborhood(positions=cfg.positions, cutoff=float(r_max), pbc=cfg.pbc, cell=cfg.cell)
        tot_neighbors += int(edge_index.shape[1])
        tot_atoms += int(len(cfg.atomic_numbers))
    if tot_atoms == 0:
        return 1.0
    return max(1.0, float(tot_neighbors) / float(tot_atoms))


def fit_atomic_energies(frames: Sequence[ExtXYZFrame], zs: Sequence[int]) -> np.ndarray:
    """Legacy atomic-energy fit directly from raw ``ExtXYZFrame`` objects."""
    z_to_col = {int(z): i for i, z in enumerate(zs)}
    y, A = [], []
    for fr in frames:
        if fr.energy_weight <= 0.0: continue
        y.append(float(fr.energy))
        counts = np.zeros((len(zs),), dtype=float)
        for z in fr.atomic_numbers: counts[z_to_col[int(z)]] += 1.0
        A.append(counts)
    if not y: raise ValueError("Cannot fit atomic energies: no frames have energy labels.")
    x, *_ = np.linalg.lstsq(np.asarray(A), np.asarray(y), rcond=None)
    return x.astype(float).reshape(-1)


def split_train_val(data: Sequence[Any], val_fraction: float, seed: int) -> Tuple[List[Any], List[Any]]:
    """Randomly split a sequence into train and validation subsets."""
    if not (0.0 < float(val_fraction) < 1.0):
        raise ValueError("val_fraction must be between 0 and 1")
    rng = np.random.default_rng(int(seed))
    idx = np.arange(len(data))
    rng.shuffle(idx)
    n_val = max(1, int(round(float(val_fraction) * len(data))))
    return [data[int(i)] for i in idx[n_val:]], [data[int(i)] for i in idx[:n_val]]


def _is_hdf5_path(path: str) -> bool:
    return Path(path).suffix.lower() in (".h5", ".hdf5", ".hdf")


def _hdf5_schema(path: str) -> str:
    if not _is_hdf5_path(path) or not HAS_H5PY:
        return ""
    try:
        with h5py.File(Path(path).expanduser(), "r") as handle:
            return str(handle.attrs.get("schema_version", ""))
    except Exception:
        return ""


def _is_composite_hdf5_path(path: str) -> bool:
    return _hdf5_schema(path) == COMPOSITE_HDF5_SCHEMA_VERSION


def load_configurations_auto(
    path: str,
    keys: DatasetKeys,
    *,
    stop_flag: Optional[Callable[[], bool]] = None,
    log: Optional[Callable[[str], None]] = None,
    sample_fraction: float = 1.0,
    sample_seed: int = 0,
) -> Tuple[List[Configuration], List[np.ndarray]]:
    if _is_hdf5_path(path):
        configurations = load_hdf5_configurations(
            path,
            sample_fraction=sample_fraction,
            sample_seed=sample_seed,
        )
        fields = [
            np.asarray(cfg.properties.get("field", np.zeros(3)), dtype=float).reshape(3)
            for cfg in configurations
        ]
        if log:
            log(f"[{_now()}] Loaded canonical HDF5 frames: {len(configurations)}")
        return configurations, fields
    return load_extxyz_configurations(
        path,
        keys,
        require_energy=False,
        require_forces=False,
        require_field=False,
        stop_flag=stop_flag,
        log=log,
        sample_fraction=sample_fraction,
        sample_seed=sample_seed,
    )


def subsample_configurations_grouped(
    configurations: Sequence[Configuration],
    fields: Sequence[np.ndarray],
    *,
    fraction: float,
    seed: int,
) -> Tuple[List[Configuration], List[np.ndarray]]:
    if not (0.0 < float(fraction) < 1.0) or len(configurations) <= 2:
        return list(configurations), list(fields)
    groups: Dict[str, List[int]] = {}
    for index, cfg in enumerate(configurations):
        group_id = str(cfg.properties.get("group_id", f"structure-{index}"))
        groups.setdefault(group_id, []).append(index)
    ranked = sorted(
        groups,
        key=lambda value: hashlib.sha256(f"{seed}|{value}".encode("utf-8")).hexdigest(),
    )
    target = max(2, int(round(len(configurations) * float(fraction))))
    selected: List[int] = []
    for group_id in ranked:
        selected.extend(groups[group_id])
        if len(selected) >= target:
            break
    selected = sorted(selected)
    return [configurations[i] for i in selected], [np.asarray(fields[i]) for i in selected]


def split_configurations_grouped(
    configurations: Sequence[Configuration],
    fields: Sequence[np.ndarray],
    *,
    val_fraction: float,
    seed: int,
) -> Tuple[List[Configuration], List[np.ndarray], List[Configuration], List[np.ndarray], Dict[str, Any]]:
    if not (0.0 < float(val_fraction) < 1.0):
        raise ValueError("val_fraction must be between 0 and 1")
    if len(configurations) != len(fields):
        raise ValueError("Configuration/field length mismatch")
    group_indices: Dict[str, List[int]] = {}
    group_split: Dict[str, str] = {}
    for index, cfg in enumerate(configurations):
        group_id = str(cfg.properties.get("group_id", f"structure-{index}"))
        group_indices.setdefault(group_id, []).append(index)
        split_name = str(cfg.properties.get("split", "")).strip().lower()
        if split_name in ("train", "val", "test"):
            previous = group_split.setdefault(group_id, split_name)
            if previous != split_name:
                raise ValueError(f"group_id {group_id!r} appears in both {previous!r} and {split_name!r}")

    explicit_train = [group for group, name in group_split.items() if name == "train"]
    explicit_val = [group for group, name in group_split.items() if name == "val"]
    test_groups = {group for group, name in group_split.items() if name == "test"}
    used_explicit = bool(explicit_train and explicit_val)
    if used_explicit:
        train_groups = set(explicit_train)
        val_groups = set(explicit_val)
        unassigned = set(group_indices) - train_groups - val_groups - test_groups
        train_groups.update(unassigned)
    else:
        eligible = sorted(
            set(group_indices) - test_groups,
            key=lambda value: hashlib.sha256(f"{seed}|{value}".encode("utf-8")).hexdigest(),
        )
        if len(eligible) <= 1:
            train_groups = set(eligible)
            val_groups = set(eligible)
        else:
            n_val_groups = max(1, min(len(eligible) - 1, int(round(len(eligible) * float(val_fraction)))))
            val_groups = set(eligible[:n_val_groups])
            train_groups = set(eligible[n_val_groups:])

    train_indices = [index for group in sorted(train_groups) for index in group_indices[group]]
    val_indices = [index for group in sorted(val_groups) for index in group_indices[group]]
    if not train_indices or not val_indices:
        raise ValueError("Grouped split produced an empty training or validation set")
    overlap = train_groups & val_groups
    info = {
        "strategy": "metadata" if used_explicit else "stable_group_hash",
        "train_structures": len(train_indices),
        "val_structures": len(val_indices),
        "test_structures_excluded": sum(len(group_indices[group]) for group in test_groups),
        "train_groups": len(train_groups),
        "val_groups": len(val_groups),
        "group_overlap": sorted(overlap),
    }
    return (
        [configurations[i] for i in train_indices],
        [np.asarray(fields[i], dtype=float) for i in train_indices],
        [configurations[i] for i in val_indices],
        [np.asarray(fields[i], dtype=float) for i in val_indices],
        info,
    )


class AtomicDataDataset(Dataset):
    """Dataset wrapper that builds graphs lazily from raw frames.

    This path is useful when the caller wants PyTorch's dataset abstraction
    while postponing neighbor-list construction until sampling time.
    """
    def __init__(self, frames: List[ExtXYZFrame], z_table: AtomicNumberTable, r_max: float):
        self.frames = frames
        self.z_table = z_table
        self.r_max = float(r_max)

    def __len__(self) -> int:
        return len(self.frames)

    def __getitem__(self, idx: int) -> _TGData:
        fr = self.frames[idx]
        
        cell = np.asarray(fr.cell, dtype=float).reshape(3, 3)
        atoms = Atoms(numbers=fr.atomic_numbers, positions=fr.positions, cell=cell, pbc=fr.pbc)
        i, j, S = neighbor_list("ijS", atoms, cutoff=self.r_max)
        
        edge_index = torch.tensor(np.stack([i, j], axis=0), dtype=torch.long)
        shift_vectors = np.einsum(
            "ni,ij->nj", np.asarray(S, dtype=float), np.asarray(atoms.cell.array, dtype=float)
        )
        shifts = torch.tensor(shift_vectors, dtype=torch.get_default_dtype())
        atom_types = np.asarray([self.z_table.z_to_index[int(z)] for z in fr.atomic_numbers], dtype=int)
        
        data = _TGData(
            positions=torch.tensor(fr.positions, dtype=torch.get_default_dtype()),
            atom_types=torch.tensor(atom_types, dtype=torch.long),
            edge_index=edge_index,
            shifts=shifts,
            cell=torch.tensor(cell, dtype=torch.get_default_dtype()),
            pbc=torch.tensor(np.asarray(fr.pbc, dtype=bool), dtype=torch.bool).view(1, 3),
        )
        data.num_nodes = int(len(fr.atomic_numbers))
        data.energy = torch.tensor(fr.energy, dtype=torch.get_default_dtype())
        data.forces = torch.tensor(fr.forces, dtype=torch.get_default_dtype())
        data.field = torch.tensor(fr.field, dtype=torch.get_default_dtype()).view(1, 3)
        data.dipole = torch.tensor(fr.dipole, dtype=torch.get_default_dtype()).view(1, 3)
        data.polarizability = torch.tensor(fr.polarizability, dtype=torch.get_default_dtype()).view(1, 3, 3)
        data.total_charge = torch.tensor(fr.total_charge, dtype=torch.get_default_dtype()).view(1)
        data.energy_weight = torch.tensor(fr.energy_weight, dtype=torch.get_default_dtype()).view(1)
        data.forces_weight = torch.tensor(fr.forces_weight, dtype=torch.get_default_dtype()).view(1)
        data.dipole_weight = torch.tensor(fr.dipole_weight, dtype=torch.get_default_dtype()).view(1)
        data.polarizability_weight = torch.tensor(fr.polarizability_weight, dtype=torch.get_default_dtype()).view(1)
        
        return data


def _as_bool_tensor(x: Any, *, device: torch.device) -> Optional[torch.Tensor]:
    if x is None:
        return None
    if torch.is_tensor(x):
        return x.to(device=device, dtype=torch.bool)
    try:
        return torch.tensor(np.asarray(x, dtype=bool), device=device, dtype=torch.bool)
    except Exception:
        return None


def scatter_sum(
    src: torch.Tensor,
    index: torch.Tensor,
    dim: int = 0,
    dim_size: Optional[int] = None,
) -> torch.Tensor:
    if dim != 0:
        raise NotImplementedError("scatter_sum supports dim=0 only")
    if index.dtype != torch.long:
        index = index.to(torch.long)
    if dim_size is None:
        dim_size = int(index.max().item()) + 1 if index.numel() > 0 else 0
    if src.ndim == 1:
        out = torch.zeros((dim_size,), dtype=src.dtype, device=src.device)
    elif src.ndim == 2:
        out = torch.zeros((dim_size, int(src.shape[1])), dtype=src.dtype, device=src.device)
    elif src.ndim == 3:
        out = torch.zeros((dim_size, int(src.shape[1]), int(src.shape[2])), dtype=src.dtype, device=src.device)
    elif src.ndim == 4:
        out = torch.zeros(
            (dim_size, int(src.shape[1]), int(src.shape[2]), int(src.shape[3])),
            dtype=src.dtype,
            device=src.device,
        )
    else:
        raise NotImplementedError("scatter_sum unsupported src.ndim (expected 1..4)")
    if src.numel() == 0:
        return out
    out.index_add_(0, index, src)
    return out


def scatter_mean(
    src: torch.Tensor,
    index: torch.Tensor,
    dim: int = 0,
    dim_size: Optional[int] = None,
) -> torch.Tensor:
    if dim != 0:
        raise NotImplementedError("scatter_mean supports dim=0 only")
    if index.dtype != torch.long:
        index = index.to(torch.long)
    if dim_size is None:
        dim_size = int(index.max().item()) + 1 if index.numel() > 0 else 0
    out = scatter_sum(src=src, index=index, dim=0, dim_size=dim_size)
    ones = torch.ones((index.shape[0],), dtype=src.dtype, device=src.device)
    counts = scatter_sum(src=ones, index=index, dim=0, dim_size=dim_size).clamp(min=1.0)
    if out.ndim == 1:
        return out / counts
    if out.ndim == 2:
        return out / counts.unsqueeze(-1)
    if out.ndim == 3:
        return out / counts.unsqueeze(-1).unsqueeze(-1)
    if out.ndim == 4:
        return out / counts.unsqueeze(-1).unsqueeze(-1).unsqueeze(-1)
    raise NotImplementedError("scatter_mean unsupported out.ndim (expected 1..4)")


def _reshape_batched_cell(cell: torch.Tensor, num_graphs: int) -> torch.Tensor:
    if cell.ndim == 2:
        if cell.shape == (3, 3):
            return cell.unsqueeze(0).expand(int(num_graphs), 3, 3)
        if cell.shape[1] == 3 and cell.shape[0] == 3 * int(num_graphs):
            return cell.view(int(num_graphs), 3, 3)
        raise ValueError(
            f"Unexpected cell shape {tuple(cell.shape)} for num_graphs={int(num_graphs)}; "
            "expected (3,3) or (3*num_graphs,3)."
        )
    if cell.ndim == 3:
        if cell.shape != (int(num_graphs), 3, 3):
            raise ValueError(
                f"Unexpected 3D cell shape {tuple(cell.shape)} for num_graphs={int(num_graphs)}; "
                "expected (num_graphs,3,3)."
            )
        return cell
    raise ValueError(f"Unexpected cell.ndim={int(cell.ndim)}; expected 2 or 3.")


def minimal_image_relative_positions(
    *, positions: torch.Tensor, center: torch.Tensor, batch: torch.Tensor,
    cell: torch.Tensor, pbc: Optional[torch.Tensor], num_graphs: int
) -> torch.Tensor:
    rel = positions - center[batch]
    if pbc is None:
        return rel
    cell_b = _reshape_batched_cell(cell, int(num_graphs)).to(device=positions.device, dtype=positions.dtype)
    pbc_b = _as_bool_tensor(pbc, device=positions.device)
    if pbc_b is None:
        return rel
    if pbc_b.ndim == 1 and pbc_b.numel() == 3:
        pbc_b = pbc_b.view(1, 3).expand(int(num_graphs), 3)
    if not bool(pbc_b.any().item()):
        return rel
    inv_cell = torch.linalg.inv(cell_b)
    frac = torch.einsum("ni,nij->nj", rel, inv_cell[batch])
    pbc_a = pbc_b[batch].to(dtype=positions.dtype)
    frac = frac - torch.round(frac) * pbc_a
    return torch.einsum("ni,nij->nj", frac, cell_b[batch])


def _weighted_mse(pred: torch.Tensor, target: torch.Tensor, weight: Optional[torch.Tensor]) -> torch.Tensor:
    if weight is None:
        return torch.mean((pred - target) ** 2)
    expanded = weight.to(device=pred.device, dtype=pred.dtype)
    while expanded.ndim < pred.ndim:
        expanded = expanded.unsqueeze(-1)
    expanded = expanded.expand_as(pred)
    active = expanded > 0.0
    if not bool(torch.any(active).detach().cpu()):
        return torch.zeros((), dtype=pred.dtype, device=pred.device)
    if not bool(torch.isfinite(target[active]).all().detach().cpu()):
        raise FloatingPointError("An active MSE target contains NaN or Inf")
    difference = pred[active] - target[active]
    active_weight = expanded[active]
    return torch.sum(difference * difference * active_weight) / torch.sum(
        active_weight
    ).clamp(min=1e-12)


def _weighted_huber(
    pred: torch.Tensor,
    target: torch.Tensor,
    weight: Optional[torch.Tensor],
    *,
    delta: float,
) -> torch.Tensor:
    """Weighted Huber loss scaled to match MSE in the quadratic region."""
    threshold = float(delta)
    if not math.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("force_huber_delta must be finite and greater than zero")
    if weight is None:
        absolute = torch.abs(pred - target)
        values = torch.where(
            absolute <= threshold,
            absolute * absolute,
            2.0 * threshold * absolute - threshold * threshold,
        )
        return torch.mean(values)
    expanded = weight.to(device=pred.device, dtype=pred.dtype)
    while expanded.ndim < pred.ndim:
        expanded = expanded.unsqueeze(-1)
    expanded = expanded.expand_as(pred)
    active = expanded > 0.0
    if not bool(torch.any(active).detach().cpu()):
        return torch.zeros((), dtype=pred.dtype, device=pred.device)
    if not bool(torch.isfinite(target[active]).all().detach().cpu()):
        raise FloatingPointError("An active Huber target contains NaN or Inf")
    absolute = torch.abs(pred[active] - target[active])
    values = torch.where(
        absolute <= threshold,
        absolute * absolute,
        2.0 * threshold * absolute - threshold * threshold,
    )
    active_weight = expanded[active]
    return torch.sum(values * active_weight) / torch.sum(active_weight).clamp(min=1e-12)


def _configured_force_loss(
    pred: torch.Tensor,
    target: torch.Tensor,
    weight: Optional[torch.Tensor],
    cfg: "TrainConfig",
) -> torch.Tensor:
    loss_name = str(getattr(cfg, "force_loss", "mse")).strip().lower()
    if loss_name == "mse":
        return _weighted_mse(pred, target, weight)
    if loss_name == "huber":
        return _weighted_huber(
            pred,
            target,
            weight,
            delta=float(getattr(cfg, "force_huber_delta", 1.0)),
        )
    raise ValueError(f"Unsupported force_loss={loss_name!r}; expected 'mse' or 'huber'")


def _loss_mse(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    return torch.mean((pred - target) ** 2)


def _compatible_spin_cutoff(r_max: Any, spin_cutoff: Any) -> float:
    """Return a finite positive spin cutoff bounded by the local graph cutoff."""
    local_cutoff = float(r_max)
    magnetic_cutoff = float(spin_cutoff)
    if not math.isfinite(local_cutoff) or local_cutoff <= 0.0:
        raise ValueError("r_max must be finite and greater than zero")
    if not math.isfinite(magnetic_cutoff) or magnetic_cutoff <= 0.0:
        raise ValueError("spin_cutoff must be finite and greater than zero")
    return min(magnetic_cutoff, local_cutoff)


@dataclass
class ModelConfig:
    """Model hyperparameters controlling geometry, channels, and physics options."""
    r_max: float = 5.0
    num_radial_basis: int = 8
    num_interactions: int = 2
    num_channels: int = 64
    field_scale: float = 1.0
    dtype: str = "float32"

    # O(3) parity-aware options.
    # Enables explicit polar / axial separation, which is required for physically
    # correct cross-product handling in centrosymmetric systems.
    e3mu_use_parity: bool = True
    # Adds optional L=3 symmetric-traceless channels.
    # This implicitly requires parity-aware mode.
    e3mu_use_l3: bool = False

    # Radial basis function family.
    # "gaussian"           : fixed Gaussian basis
    # "trainable_gaussian" : learnable centers and widths
    # "bessel"             : spherical Bessel basis with stronger orthogonality
    rbf_type: str = "gaussian"

    # Continuous chemical-space embedding options.
    # When enabled, one-hot element IDs are replaced by learned periodic-table
    # descriptors with optional alchemical augmentation.
    enable_continuous_chem: bool = False
    chem_max_z: int = 96
    chem_aug_prob: float = 0.0        # alchemical augmentation probability per atom
    chem_aug_noise_std: float = 0.0   # Gaussian noise added to element descriptors
    chem_aug_mix_max: float = 0.0     # max mix fraction with random other element

    # Mixed-granularity physics layers.
    enable_qeq: bool = False
    enable_pme: bool = False
    enable_deq: bool = False
    enable_d4: bool = False
    enable_spin: bool = False
    enable_film: bool = False
    qeq_smearing: float = 0.35
    qeq_hardness_min: float = 0.25
    qeq_pme_smearing: float = 1.0
    qeq_pme_lr_wavelength: float = 0.8
    qeq_stability_floor: float = 0.1
    deq_max_iter: int = 50
    deq_tol: float = 1e-6
    deq_damping: float = 0.5
    deq_alpha_max: float = 100.0
    d4_functional: str = "pbe"
    spin_cutoff: float = 5.0
    # DMI remains opt-in because it requires SOC/DMI supervision; MPtrj
    # collinear magnetic moments alone do not identify this interaction.
    enable_dmi: bool = False
    coupling_iterations: int = 2
    coupling_tol: float = 1e-5
    polarizability_unit: str = "angstrom3"

    def __post_init__(self) -> None:
        # Keep old JSON/checkpoint configurations usable when they contain the
        # former 6 Angstrom magnetic default with the 5 Angstrom local cutoff.
        self.r_max = float(self.r_max)
        self.spin_cutoff = _compatible_spin_cutoff(self.r_max, self.spin_cutoff)

# ══════════════════════════════════════════════════════════════════════════
# SECTION: E(3)-mu-GNN Core
# Core tensor bases, element encoders, and equivariant message-passing blocks.
# ══════════════════════════════════════════════════════════════════════════

def _build_st_basis(dtype: torch.dtype) -> torch.Tensor:
    """Build the real basis for symmetric-traceless rank-2 tensors.

    The returned matrix is the fixed projection basis used to map Cartesian
    vector products into the 5-component L=2 representation.
    """
    s2 = 1.0 / math.sqrt(2.0)
    s6 = 1.0 / math.sqrt(6.0)
    B = torch.zeros((5, 3, 3), dtype=dtype)
    B[0, 0, 0] = s2; B[0, 1, 1] = -s2
    B[1, 0, 0] = -s6; B[1, 1, 1] = -s6; B[1, 2, 2] = 2.0 * s6
    B[2, 0, 1] = s2; B[2, 1, 0] = s2
    B[3, 0, 2] = s2; B[3, 2, 0] = s2
    B[4, 1, 2] = s2; B[4, 2, 1] = s2
    return B


def _build_st3_basis(dtype: torch.dtype) -> torch.Tensor:
    """Build an orthonormal basis for rank-3 symmetric-traceless tensors.

    A deterministic Gram-Schmidt procedure is used so that every run produces
    the same 7 real basis tensors for the L=3 channel.

    Returns:
        Tensor of shape ``(7, 3, 3, 3)`` whose basis elements are fully
        symmetric, traceless, and mutually orthonormal.
    """
    # 10 symmetric monomials of degree 3: xxx, xxy, xxz, xyy, xyz, xzz, yyy, yyz, yzz, zzz
    cand: List[torch.Tensor] = []
    for a in range(3):
        for b in range(a, 3):
            for c in range(b, 3):
                T = torch.zeros((3, 3, 3), dtype=dtype)
                idx = (a, b, c)
                # Symmetrise over index permutations.
                perms = sorted({p for p in itertools.permutations(idx)})
                for p in perms:
                    T[p] = T[p] + 1.0
                T = T / float(len(perms))
                cand.append(T)

    def _proj_traceless(T: torch.Tensor) -> torch.Tensor:
        # For symmetric rank-3 tensors, the traceless projection is:
        #   ST(T) = T - (1/5) * (delta_ij t_k + delta_ik t_j + delta_jk t_i)
        # where t_k = sum_i T_{iik}.
        t = torch.einsum("iik->k", T)
        out = T.clone()
        for i in range(3):
            out[i, i, :] -= 0.2 * t
            out[i, :, i] -= 0.2 * t
            out[:, i, i] -= 0.2 * t
        return out

    vecs = [_proj_traceless(T).reshape(-1) for T in cand]
    basis_vecs: List[torch.Tensor] = []
    for v in vecs:
        for b in basis_vecs:
            v = v - torch.dot(v, b) * b
        n = torch.linalg.norm(v)
        if float(n) > 1e-6:
            basis_vecs.append(v / n)

    if len(basis_vecs) != 7:
        raise RuntimeError(f"ST3 basis construction failed: expected 7 vectors, got {len(basis_vecs)}")
    return torch.stack(basis_vecs, dim=0).reshape(7, 3, 3, 3)


# --------------------------------------------------------------------------
# Continuous chemical-space embedding helpers.
# Utilities for constructing periodic-table descriptors used by the optional
# learned element encoder.
# --------------------------------------------------------------------------

def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return float(default)
        return float(x)
    except Exception:
        return float(default)


def _valence_electron_count_from_group(group: Optional[int]) -> float:
    """Heuristic valence electron count from periodic-table IUPAC group (1..18)."""
    if group is None:
        return 0.0
    g = int(group)
    if g in (1, 2):
        return float(g)
    if 13 <= g <= 18:
        return float(g - 10)
    return float(g)


def _build_periodic_table_property_matrix(
    *,
    max_z: int,
    log: Optional[Callable[[str], None]] = None,
) -> Tuple[torch.Tensor, List[str]]:
    """Build a descriptor table for elements ``1..max_z``.

    The routine prefers pymatgen because its chemical metadata is richer, but
    falls back to ASE when pymatgen is unavailable.

    Features:
        0. group id
        1. period
        2. Pauling electronegativity
        3. atomic radius (Angstrom)
        4. first ionization energy (eV)
        5. electron affinity (eV)
        6. valence-electron proxy
        7. atomic mass (amu)
    """
    max_z = int(max(1, max_z))
    feat_names = [
        "group", "period", "en_pauling", "atomic_radius_A",
        "ionization_eV", "electron_affinity_eV", "valence_e_proxy", "atomic_mass_amu",
    ]
    props = np.full((max_z, len(feat_names)), np.nan, dtype=float)

    try:
        from pymatgen.core.periodic_table import Element as _PMGElement  # type: ignore
        import warnings

        def _getattr_safe(obj: Any, name: str) -> Any:
            try:
                return getattr(obj, name)
            except Exception:
                return None

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="No Pauling electronegativity*", category=UserWarning)
            for z in range(1, max_z + 1):
                try:
                    el = _PMGElement.from_Z(z)
                except Exception:
                    continue
                group = _getattr_safe(el, "group")
                period = _getattr_safe(el, "row")
                en = _getattr_safe(el, "X")
                r = _getattr_safe(el, "atomic_radius")
                ie = _getattr_safe(el, "ionization_energy")
                ea = _getattr_safe(el, "electron_affinity")
                mass = _getattr_safe(el, "atomic_mass")
                props[z - 1, 0] = _safe_float(group, default=float("nan"))
                props[z - 1, 1] = _safe_float(period, default=float("nan"))
                props[z - 1, 2] = _safe_float(en, default=float("nan"))
                props[z - 1, 3] = _safe_float(r, default=float("nan"))
                props[z - 1, 4] = _safe_float(ie, default=float("nan"))
                props[z - 1, 5] = _safe_float(ea, default=float("nan"))
                try:
                    gi = None if group is None else int(group)
                except Exception:
                    gi = None
                props[z - 1, 6] = _valence_electron_count_from_group(gi)
                props[z - 1, 7] = _safe_float(mass, default=float("nan"))
        if log is not None:
            log(f"[{_now()}] PeriodicTableEmbedder: descriptors loaded via pymatgen (max_z={max_z}).")
    except Exception as e:
        if log is not None:
            log(f"[{_now()}] WARN: pymatgen unavailable ({type(e).__name__}: {e}); using ASE fallback for element descriptors.")
        try:
            from ase.data import atomic_masses as _ase_masses, covalent_radii as _ase_radii  # type: ignore
        except Exception:
            _ase_masses = None
            _ase_radii = None
        for z in range(1, max_z + 1):
            props[z - 1, 3] = float(_ase_radii[z]) if _ase_radii is not None and z < len(_ase_radii) else float("nan")
            props[z - 1, 7] = float(_ase_masses[z]) if _ase_masses is not None and z < len(_ase_masses) else float("nan")

    # Impute NaNs with column means.
    finite_count = np.sum(np.isfinite(props), axis=0)
    finite_sum = np.nansum(props, axis=0)
    col_mean = np.divide(
        finite_sum,
        finite_count,
        out=np.zeros_like(finite_sum),
        where=finite_count > 0,
    )
    inds = np.where(~np.isfinite(props))
    props[inds] = np.take(col_mean, inds[1])

    # Z-score normalization.
    mean = props.mean(axis=0, keepdims=True)
    std = props.std(axis=0, keepdims=True) + 1e-6
    props = (props - mean) / std

    return torch.tensor(props, dtype=torch.get_default_dtype()), feat_names


class PeriodicTableEmbedder(torch.nn.Module):
    """
    Physics-informed element embedding: Z -> V_phys(Z) -> MLP -> h0

    Reduces the "one-hot island" effect and improves transfer across chemically similar
    elements (same group/period) by encoding periodic-table physical descriptors
    (electronegativity, atomic radius, ionization energy, etc.) as a continuous input.

    Optionally applies alchemical augmentation during training to further improve
    chemical transferability.
    """

    def __init__(
        self,
        *,
        embedding_dim: int,
        max_z: int = 96,
        aug_prob: float = 0.0,
        aug_noise_std: float = 0.0,
        aug_mix_max: float = 0.0,
        log: Optional[Callable[[str], None]] = None,
    ):
        super().__init__()
        self.max_z = int(max(1, max_z))
        self.embedding_dim = int(embedding_dim)
        self.aug_prob = float(max(0.0, aug_prob))
        self.aug_noise_std = float(max(0.0, aug_noise_std))
        self.aug_mix_max = float(max(0.0, aug_mix_max))

        prop_matrix, feat_names = _build_periodic_table_property_matrix(max_z=self.max_z, log=log)
        self._feat_names = list(feat_names)
        self.register_buffer("prop_matrix", prop_matrix, persistent=True)

        n_feat = int(self.prop_matrix.shape[1])
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(n_feat, 64),
            torch.nn.SiLU(),
            torch.nn.Linear(64, self.embedding_dim),
            torch.nn.LayerNorm(self.embedding_dim),
        )

    def forward(self, atomic_numbers: torch.Tensor) -> torch.Tensor:
        z = atomic_numbers.to(dtype=torch.long)
        z = torch.clamp(z, 1, int(self.max_z))
        idx = z - 1
        phys = self.prop_matrix[idx]  # (n_nodes, n_feat)

        if self.training and self.aug_prob > 0.0:
            m = (torch.rand((phys.shape[0],), device=phys.device) < float(self.aug_prob)).view(-1, 1)
            if self.aug_mix_max > 0.0:
                idx2 = torch.randint(low=0, high=int(self.max_z), size=(phys.shape[0],), device=phys.device)
                phys2 = self.prop_matrix[idx2]
                lam = torch.rand((phys.shape[0], 1), device=phys.device) * float(min(1.0, self.aug_mix_max))
                phys = torch.where(m, (1.0 - lam) * phys + lam * phys2, phys)
            if self.aug_noise_std > 0.0:
                noise = float(self.aug_noise_std) * torch.randn_like(phys)
                phys = torch.where(m, phys + noise, phys)

        return self.encoder(phys.to(dtype=self.prop_matrix.dtype))


class CosineCutoff(torch.nn.Module):
    def __init__(self, r_max: float):
        super().__init__()
        self.r_max = float(r_max)
    def forward(self, r: torch.Tensor) -> torch.Tensor:
        x = r / max(1e-12, self.r_max)
        out = 0.5 * (torch.cos(math.pi * x) + 1.0)
        return out * (x < 1.0).to(out.dtype)

class GaussianRBF(torch.nn.Module):
    def __init__(self, num_basis: int, r_max: float):
        super().__init__()
        self.num_basis = int(num_basis)
        self.r_max = float(r_max)
        centers = torch.linspace(0.0, self.r_max, steps=self.num_basis)
        gamma = float(self.num_basis) / max(1e-12, self.r_max) ** 2
        self.register_buffer("centers", centers)
        self.register_buffer("gamma", torch.tensor(gamma))
    def forward(self, r: torch.Tensor) -> torch.Tensor:
        diff = r.unsqueeze(-1) - self.centers.unsqueeze(0)
        return torch.exp(-self.gamma * diff * diff)


class TrainableGaussianRBF(torch.nn.Module):
    """
    Gaussian RBF with learnable centers and widths.

    When bond-length distributions are highly non-uniform, the model can "focus" basis
    functions on chemically relevant distance ranges, improving radial expressiveness.
    """

    def __init__(self, num_basis: int, r_max: float):
        super().__init__()
        if num_basis < 1:
            raise ValueError("num_basis must be >= 1")
        self.num_basis = int(num_basis)
        self.r_max = float(r_max)
        centers0 = torch.linspace(0.0, self.r_max, steps=self.num_basis)
        self.centers = torch.nn.Parameter(centers0)
        gamma0 = float(self.num_basis) / max(1e-12, self.r_max) ** 2
        # Store unconstrained; apply softplus in forward to keep gamma > 0.
        inv = gamma0 if gamma0 > 20.0 else math.log(max(1e-12, math.expm1(gamma0)))
        self._gamma_unconstrained = torch.nn.Parameter(torch.full((self.num_basis,), float(inv)))

    def forward(self, r: torch.Tensor) -> torch.Tensor:
        centers = torch.clamp(self.centers, 0.0, self.r_max)
        gamma = torch.nn.functional.softplus(self._gamma_unconstrained).clamp(min=1e-12)
        diff = r.unsqueeze(-1) - centers.unsqueeze(0)
        return torch.exp(-gamma.unsqueeze(0) * diff * diff)


class BesselRBF(torch.nn.Module):
    """
    Spherical Bessel (j0-like) radial basis:

      e_n(r) = sqrt(2/r_max) * sin(n*pi*r/r_max) / r

    Better orthogonality than Gaussians; physically motivated by radial solutions to
    the Schrodinger equation in spherical coordinates (used in DimeNet/GemNet).
    """

    def __init__(self, num_basis: int, r_max: float):
        super().__init__()
        if num_basis < 1:
            raise ValueError("num_basis must be >= 1")
        self.num_basis = int(num_basis)
        self.r_max = float(r_max)
        n = torch.arange(1, self.num_basis + 1, dtype=torch.get_default_dtype())
        self.register_buffer("freq", n * (math.pi / max(1e-12, self.r_max)))
        self.register_buffer(
            "norm",
            torch.tensor(math.sqrt(2.0 / max(1e-12, self.r_max)), dtype=torch.get_default_dtype()),
        )

    def forward(self, r: torch.Tensor) -> torch.Tensor:
        rr = r.clamp(min=1e-12)
        x = rr.unsqueeze(-1) * self.freq.unsqueeze(0)
        return self.norm * torch.sin(x) / rr.unsqueeze(-1)


class ScaledRadialBasis(torch.nn.Module):
    """
    Wrap a radial basis and apply an inverse-distance scaling: phi(r) -> phi(r) / (r+eps)^p.
    p=0 disables scaling.
    """

    def __init__(self, base: torch.nn.Module, *, power: int = 0, eps: float = 1e-8):
        super().__init__()
        self.base = base
        self.power = int(power)
        self.eps = float(eps)

    def forward(self, r: torch.Tensor) -> torch.Tensor:
        out = self.base(r)
        p = int(self.power)
        if p == 0:
            return out
        rr = r + float(self.eps)
        inv = 1.0 / rr
        if p == 1:
            scale = inv
        elif p == 2:
            scale = inv * inv
        elif p == 3:
            scale = inv * inv * inv
        else:
            scale = torch.pow(rr, float(-p))
        return out * scale.unsqueeze(-1)


def _make_e3mu_rbf(cfg: Optional["ModelConfig"], num_basis: int, r_max: float) -> torch.nn.Module:
    """Factory: return an RBF module based on cfg.rbf_type (default 'gaussian')."""
    rbf_type = "gaussian"
    if cfg is not None:
        try:
            rbf_type = str(getattr(cfg, "rbf_type", rbf_type) or rbf_type).strip().lower()
        except Exception:
            rbf_type = "gaussian"

    if rbf_type in ("gaussian", "g", "gauss"):
        return GaussianRBF(num_basis, r_max)
    elif rbf_type in ("trainable_gaussian", "trainable-gaussian", "learnable_gaussian", "tg"):
        return TrainableGaussianRBF(num_basis, r_max)
    elif rbf_type in ("bessel", "b"):
        return BesselRBF(num_basis, r_max)
    else:
        raise ValueError(
            f"Unknown rbf_type: {rbf_type!r} (expected 'gaussian', 'trainable_gaussian', or 'bessel')"
        )


def _smooth_scalar_bound(value: torch.Tensor, max_abs: float = 32.0) -> torch.Tensor:
    """Near-identity smooth saturation for invariant scalar channels."""
    cap = float(max_abs)
    return value * torch.rsqrt(1.0 + torch.square(value / cap))


def _smooth_equivariant_bound(value: torch.Tensor, max_norm: float = 100.0) -> torch.Tensor:
    """Bound an irreducible feature by an invariant norm-preserving scale.

    Component-wise clipping would break rotational equivariance. This radial
    map leaves small features unchanged and smoothly saturates only unusually
    large vector/tensor channels before their polynomial couplings overflow.
    """
    cap = float(max_norm)
    # Use the squared norm directly. ``vector_norm`` has an undefined derivative
    # at the all-zero vectors used to initialize equivariant channels.
    norm_squared = torch.sum(value * value, dim=-1, keepdim=True)
    scale = torch.rsqrt(1.0 + norm_squared / (cap * cap))
    return value * scale

class FastEquivariantBlock(torch.nn.Module):
    r"""
    Core equivariant message passing block.
    Implements Formula 5 :
    m_ij = W * (h_j \ times Y(\hat{r}_ij))
    
    This scalar-vector coupled mechanism efficiently extracts high-order geometric
    features, allowing both invariant (scalar) and equivariant (vector/tensor)
    outputs .
    """
    def __init__(self, hidden: int, rbf_dim: int):
        super().__init__()
        self.hidden = int(hidden)
        self.register_buffer("st_basis", _build_st_basis(torch.get_default_dtype()), persistent=False)
        self.filter = torch.nn.Sequential(
            torch.nn.Linear(rbf_dim, hidden),
            torch.nn.SiLU(),
            torch.nn.Linear(hidden, 10 * hidden),
        )
        self.update = torch.nn.Sequential(
            torch.nn.Linear(4 * hidden, hidden),
            torch.nn.SiLU(),
            torch.nn.Linear(hidden, 4 * hidden),
        )
        self.self_v_a = torch.nn.Linear(hidden, hidden, bias=False)
        self.self_v_b = torch.nn.Linear(hidden, hidden, bias=False)
        self.t_act_s = torch.nn.Linear(hidden, hidden)
        self.t_act_norm = torch.nn.Linear(hidden, hidden)
        self.norm = torch.nn.LayerNorm(hidden)

    def forward(
        self,
        *,
        s: torch.Tensor,
        v: torch.Tensor,
        t: torch.Tensor,
        edge_index: torch.Tensor,
        edge_vec: torch.Tensor,
        r: torch.Tensor,
        rbf: torch.Tensor,
        cutoff: torch.Tensor,
        num_nodes: int,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        src, dst = edge_index[0], edge_index[1]
        s_j, v_j, t_j = s[dst], v[dst], t[dst]
        w = self.filter(rbf) * cutoff.unsqueeze(-1)
        w_ss, w_sd, w_sq, w_vv, w_vs, w_vc, w_vt, w_tt, w_tu, w_tv = torch.chunk(w, 10, dim=-1)
        
        u = edge_vec / (r.unsqueeze(-1) + 1e-12)
        dot_vu = torch.einsum("ehc,ec->eh", v_j, u)
        uu_l2 = torch.einsum("ec,kcd,ed->ek", u, self.st_basis, u)
        quad_t = torch.einsum("ehk,ek->eh", t_j, uu_l2)
        msg_s = w_ss * s_j + w_sd * dot_vu + w_sq * quad_t

        u_exp = u[:, None, :].expand_as(v_j)
        cross_vu = torch.cross(v_j, u_exp, dim=-1)
        t_u = torch.einsum("ehk,kcd,ed->ehc", t_j, self.st_basis, u)
        msg_v = w_vv.unsqueeze(-1)*v_j + (w_vs*s_j).unsqueeze(-1)*u[:,None,:] + w_vc.unsqueeze(-1)*cross_vu + w_vt.unsqueeze(-1)*t_u

        vu_l2 = torch.einsum("ehc,ed,kcd->ehk", v_j, u, self.st_basis)
        msg_t = w_tt.unsqueeze(-1)*t_j + (w_tu*s_j).unsqueeze(-1)*uu_l2[:,None,:] + w_tv.unsqueeze(-1)*vu_l2

        agg_s = scatter_mean(msg_s, src, dim_size=num_nodes)
        agg_v = scatter_mean(msg_v, src, dim_size=num_nodes)
        agg_t = scatter_mean(msg_t, src, dim_size=num_nodes)

        v2 = torch.sum(v * v, dim=-1)
        t2 = torch.sum(t * t, dim=-1)
        x = torch.cat([s, agg_s, v2, t2], dim=-1)
        ds, gate_v, gate_t, gate_self = torch.chunk(self.update(x), 4, dim=-1)
        s_new = self.norm(s + ds)

        vt = v.permute(0, 2, 1)
        a = self.self_v_a(vt).permute(0, 2, 1)
        b = self.self_v_b(vt).permute(0, 2, 1)
        self_vec = torch.cross(a, b, dim=-1)

        v_new = _smooth_equivariant_bound(
            v
            + _smooth_scalar_bound(gate_v).unsqueeze(-1) * agg_v
            + _smooth_scalar_bound(gate_self).unsqueeze(-1) * self_vec
        )
        t_new = _smooth_equivariant_bound(
            t + _smooth_scalar_bound(gate_t).unsqueeze(-1) * agg_t
        )
        t_norm = torch.sqrt(torch.sum(t_new * t_new, dim=-1) + 1e-12)
        t_gate = _smooth_scalar_bound(
            torch.nn.functional.silu(self.t_act_s(s_new) + self.t_act_norm(t_norm))
        )
        t_new = _smooth_equivariant_bound(t_new * t_gate.unsqueeze(-1))
        return s_new, v_new, t_new


class FastEquivariantBlockO3(torch.nn.Module):
    """
    Parity-aware O(3) equivariant update with explicit polar/axial separation.

    Fixes the key symmetry bug in FastEquivariantBlock: cross products produce axial
    (pseudo-)vectors (1e, even parity), not polar vectors (1o, odd parity). Mixing
    them violates O(3) equivariance and can cause unphysical dipole predictions on
    centrosymmetric structures.

    Channels:
      s   : (n, H)      scalar       [0e]  — invariant
      v   : (n, H, 3)   polar vec    [1o]  — true vectors, e.g. forces/dipoles
      a   : (n, H, 3)   axial vec    [1e]  — pseudo-vectors, cross products live here
      t2  : (n, H, 5)   ST rank-2    [2e]  — symmetric traceless quadrupole
      t3  : (n, H, 7)   ST rank-3    [3o]  — optional octupole channel
    """

    def __init__(self, hidden: int, rbf_dim: int, *, use_l3: bool):
        super().__init__()
        self.hidden = int(hidden)
        self.use_l3 = bool(use_l3)
        self.register_buffer("st_basis", _build_st_basis(torch.get_default_dtype()), persistent=False)
        if self.use_l3:
            self.register_buffer("st3_basis", _build_st3_basis(torch.get_default_dtype()), persistent=False)
        else:
            self.register_buffer("st3_basis", torch.zeros((7, 3, 3, 3), dtype=torch.get_default_dtype()), persistent=False)

        # Number of filter weight chunks:
        #   Without L=3: 12 (3 scalar + 4 polar-v + 2 axial-a + 3 tensor-t2)
        #   With    L=3: 18 (+1 scalar-from-t3, +1 polar-from-t3, +1 t2-from-t3, +3 t3-updates)
        n_chunks = 18 if self.use_l3 else 12
        self._n_chunks = int(n_chunks)
        self.filter = torch.nn.Sequential(
            torch.nn.Linear(rbf_dim, hidden),
            torch.nn.SiLU(),
            torch.nn.Linear(hidden, self._n_chunks * hidden),
        )

        # Update MLP uses only parity-even invariants (norms) to preserve O(3) symmetry.
        # Inputs: s, agg_s, ||v||^2, ||a||^2, ||t2||^2, (||t3||^2 if use_l3)
        # Outputs: ds, gate_v, gate_a, gate_t2, gate_self_a, (gate_t3 if use_l3)
        in_mult = 6 if self.use_l3 else 5
        out_mult = 6 if self.use_l3 else 5
        self.update = torch.nn.Sequential(
            torch.nn.Linear(in_mult * hidden, hidden),
            torch.nn.SiLU(),
            torch.nn.Linear(hidden, out_mult * hidden),
        )

        # Self-coupling: (v x v) -> axial (1e). Updates 'a', NOT 'v'.
        self.self_v_a = torch.nn.Linear(hidden, hidden, bias=False)
        self.self_v_b = torch.nn.Linear(hidden, hidden, bias=False)

        # Separate gated nonlinearities for t2 and t3.
        self.t2_act_s = torch.nn.Linear(hidden, hidden)
        self.t2_act_norm = torch.nn.Linear(hidden, hidden)
        self.t3_act_s = torch.nn.Linear(hidden, hidden)
        self.t3_act_norm = torch.nn.Linear(hidden, hidden)
        self.norm = torch.nn.LayerNorm(hidden)

    def forward(
        self,
        *,
        s: torch.Tensor,        # (n_nodes, H)
        v: torch.Tensor,        # (n_nodes, H, 3) polar
        a: torch.Tensor,        # (n_nodes, H, 3) axial
        t2: torch.Tensor,       # (n_nodes, H, 5)
        t3: torch.Tensor,       # (n_nodes, H, 7) — ignored when use_l3=False
        edge_index: torch.Tensor,
        edge_vec: torch.Tensor,
        r: torch.Tensor,
        rbf: torch.Tensor,
        cutoff: torch.Tensor,
        num_nodes: int,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        src = edge_index[0]
        dst = edge_index[1]

        s_j = s[dst]
        v_j = v[dst]
        a_j = a[dst]
        t2_j = t2[dst]
        t3_j = t3[dst]

        w = self.filter(rbf) * cutoff.unsqueeze(-1)
        chunks = torch.chunk(w, self._n_chunks, dim=-1)
        zero_chunk = torch.zeros_like(chunks[0])

        # --- Scalar (0e) weight chunks ---
        w_ss = chunks[0]    # s_j -> scalar
        w_sd = chunks[1]    # v_j . u -> scalar (1o x 1o -> 0e dot product)
        w_sq2 = chunks[2]   # t2:(u x u) -> scalar
        w_sq3 = zero_chunk
        off = 3
        if self.use_l3:
            w_sq3 = chunks[3]   # t3:(u x u x u) -> scalar
            off = 4

        # --- Polar vector (1o) weight chunks ---
        w_vv = chunks[off + 0]   # v_j -> polar
        w_vs = chunks[off + 1]   # s_j * u -> polar
        w_vt = chunks[off + 2]   # t2 . u -> polar (2e x 1o -> 1o)
        w_va = chunks[off + 3]   # a x u -> polar (1e x 1o -> 1o)
        w_v3 = zero_chunk
        off2 = off + 4
        if self.use_l3:
            w_v3 = chunks[off2]  # t3:(u x u) -> polar (3o contracted -> 1o)
            off2 += 1

        # --- Axial vector (1e) weight chunks ---
        w_aa = chunks[off2 + 0]  # a_j -> axial
        w_av = chunks[off2 + 1]  # v x u -> axial (1o x 1o -> 1e cross product)
        off3 = off2 + 2

        # --- ST2 tensor (2e) weight chunks ---
        w_t2t = chunks[off3 + 0]  # t2_j -> tensor
        w_t2u = chunks[off3 + 1]  # s_j * ST(u x u) -> tensor
        w_t2v = chunks[off3 + 2]  # ST(v x u) -> tensor (1o x 1o -> 2e)
        w_t2_3u = zero_chunk
        off4 = off3 + 3
        if self.use_l3:
            w_t2_3u = chunks[off4]  # t3 x u -> 2e
            off4 += 1

        # --- ST3 tensor (3o) weight chunks (use_l3 only) ---
        w_t3t = zero_chunk
        w_t3u3 = zero_chunk
        w_t3t2u = zero_chunk
        if self.use_l3:
            w_t3t = chunks[off4 + 0]    # t3_j -> t3
            w_t3u3 = chunks[off4 + 1]   # s_j * ST3(u x u x u) -> t3
            w_t3t2u = chunks[off4 + 2]  # t2 x u -> 3o (2e x 1o -> 3o)

        u = edge_vec / (r.unsqueeze(-1) + 1e-12)
        u_exp = u[:, None, :].expand_as(v_j)

        # --- Precompute geometry tensors ---
        uu_l2 = torch.einsum("ec,kcd,ed->ek", u, self.st_basis, u)         # (n_edges,5)
        uuu_l3 = torch.zeros((u.shape[0], 7), dtype=u.dtype, device=u.device)
        if self.use_l3:
            uuu_l3 = torch.einsum("ea,mabc,eb,ec->em", u, self.st3_basis, u, u)  # (n_edges,7)

        # --- Scalar messages ---
        dot_vu = torch.einsum("ehc,ec->eh", v_j, u)
        quad_t2 = torch.einsum("ehk,ek->eh", t2_j, uu_l2)
        msg_s = w_ss * s_j + w_sd * dot_vu + w_sq2 * quad_t2
        if self.use_l3:
            quad_t3 = torch.einsum("ehm,em->eh", t3_j, uuu_l3)
            msg_s = msg_s + w_sq3 * quad_t3

        # --- Polar vector messages (1o only — no cross products here!) ---
        t2_u = torch.einsum("ehk,kcd,ed->ehc", t2_j, self.st_basis, u)
        cross_au = torch.cross(a_j, u_exp, dim=-1)   # 1e x 1o -> 1o (correct!)
        msg_v = (
            w_vv.unsqueeze(-1) * v_j
            + (w_vs * s_j).unsqueeze(-1) * u[:, None, :]
            + w_vt.unsqueeze(-1) * t2_u
            + w_va.unsqueeze(-1) * cross_au
        )
        if self.use_l3:
            t3_uu = torch.einsum("ehm,mabc,eb,ec->eha", t3_j, self.st3_basis, u, u)
            msg_v = msg_v + w_v3.unsqueeze(-1) * t3_uu

        # --- Axial vector messages (1e only — cross products go here!) ---
        cross_vu = torch.cross(v_j, u_exp, dim=-1)   # 1o x 1o -> 1e (correct!)
        msg_a = w_aa.unsqueeze(-1) * a_j + w_av.unsqueeze(-1) * cross_vu

        # --- ST2 tensor messages ---
        vu_l2 = torch.einsum("ehc,ed,kcd->ehk", v_j, u, self.st_basis)
        msg_t2 = (
            w_t2t.unsqueeze(-1) * t2_j
            + (w_t2u * s_j).unsqueeze(-1) * uu_l2[:, None, :]
            + w_t2v.unsqueeze(-1) * vu_l2
        )
        if self.use_l3:
            t3_u_mat = torch.einsum("ehm,mabc,ec->ehab", t3_j, self.st3_basis, u)
            t3_u_l2 = torch.einsum("ehab,kab->ehk", t3_u_mat, self.st_basis)
            msg_t2 = msg_t2 + w_t2_3u.unsqueeze(-1) * t3_u_l2

        # --- ST3 tensor messages ---
        msg_t3 = t3_j
        if self.use_l3:
            t2u_l3 = torch.einsum("ehk,kab,ec,mabc->ehm", t2_j, self.st_basis, u, self.st3_basis)
            msg_t3 = (
                w_t3t.unsqueeze(-1) * t3_j
                + (w_t3u3 * s_j).unsqueeze(-1) * uuu_l3[:, None, :]
                + w_t3t2u.unsqueeze(-1) * t2u_l3
            )

        # --- Aggregation ---
        agg_s = scatter_mean(msg_s, src, dim_size=num_nodes)
        agg_v = scatter_mean(msg_v, src, dim_size=num_nodes)
        agg_a = scatter_mean(msg_a, src, dim_size=num_nodes)
        agg_t2 = scatter_mean(msg_t2, src, dim_size=num_nodes)
        agg_t3 = scatter_mean(msg_t3, src, dim_size=num_nodes)

        # --- Update gate (uses only even-parity invariants -> O(3)-safe) ---
        v2 = torch.sum(v * v, dim=-1)
        a2 = torch.sum(a * a, dim=-1)
        t2n = torch.sum(t2 * t2, dim=-1)
        if self.use_l3:
            t3n = torch.sum(t3 * t3, dim=-1)
            x = torch.cat([s, agg_s, v2, a2, t2n, t3n], dim=-1)
            ds, gate_v, gate_a, gate_t2, gate_self_a, gate_t3 = torch.chunk(self.update(x), 6, dim=-1)
        else:
            x = torch.cat([s, agg_s, v2, a2, t2n], dim=-1)
            ds, gate_v, gate_a, gate_t2, gate_self_a = torch.chunk(self.update(x), 5, dim=-1)
            gate_t3 = torch.zeros_like(gate_v)

        s_new = self.norm(s + ds)

        # Self axial boost: v x v -> axial (1e). Updates 'a', NOT 'v'.
        vt = v.permute(0, 2, 1)
        aa_self = self.self_v_a(vt).permute(0, 2, 1)
        bb_self = self.self_v_b(vt).permute(0, 2, 1)
        self_ax = torch.cross(aa_self, bb_self, dim=-1)  # (n_nodes, H, 3) axial

        v_new = _smooth_equivariant_bound(
            v + _smooth_scalar_bound(gate_v).unsqueeze(-1) * agg_v
        )
        a_new = _smooth_equivariant_bound(
            a
            + _smooth_scalar_bound(gate_a).unsqueeze(-1) * agg_a
            + _smooth_scalar_bound(gate_self_a).unsqueeze(-1) * self_ax
        )
        t2_new = _smooth_equivariant_bound(
            t2 + _smooth_scalar_bound(gate_t2).unsqueeze(-1) * agg_t2
        )
        t3_new = _smooth_equivariant_bound(
            t3 + _smooth_scalar_bound(gate_t3).unsqueeze(-1) * agg_t3
        )

        t2_norm = torch.sqrt(torch.sum(t2_new * t2_new, dim=-1) + 1e-12)
        t2_gate = _smooth_scalar_bound(
            torch.nn.functional.silu(self.t2_act_s(s_new) + self.t2_act_norm(t2_norm))
        )
        t2_new = _smooth_equivariant_bound(t2_new * t2_gate.unsqueeze(-1))

        if self.use_l3:
            t3_norm = torch.sqrt(torch.sum(t3_new * t3_new, dim=-1) + 1e-12)
            t3_gate = _smooth_scalar_bound(
                torch.nn.functional.silu(self.t3_act_s(s_new) + self.t3_act_norm(t3_norm))
            )
            t3_new = _smooth_equivariant_bound(t3_new * t3_gate.unsqueeze(-1))
        else:
            t3_new = torch.zeros_like(t3_new)

        return s_new, v_new, a_new, t2_new, t3_new


class FastEquivariantCore(torch.nn.Module):
    """Baseline SO(3) equivariant core with scalar, vector, and L=2 channels."""

    def __init__(self, *, num_elements, hidden, num_layers, rbf_dim, r_max):
        super().__init__()
        self.num_elements = int(num_elements)
        self.hidden = int(hidden)
        self.r_max = float(r_max)
        self.embed = torch.nn.Linear(self.num_elements, self.hidden, bias=False)
        self.rbf = GaussianRBF(rbf_dim, self.r_max)
        self.cutoff = CosineCutoff(self.r_max)
        self.layers = torch.nn.ModuleList([FastEquivariantBlock(self.hidden, rbf_dim) for _ in range(int(num_layers))])

    def forward(self, batch):
        pos = batch.positions
        edge_index = batch.edge_index
        shifts = getattr(batch, "shifts", None)
        if shifts is None:
            shifts = torch.zeros((edge_index.shape[1], 3), dtype=pos.dtype, device=pos.device)
        src, dst = edge_index[0], edge_index[1]
        edge_vec = pos[dst] + shifts - pos[src]
        r = torch.linalg.norm(edge_vec, dim=-1).clamp(min=1e-12)
        rbf = self.rbf(r)
        cutoff = self.cutoff(r)

        if hasattr(batch, "atom_types"):
            atom_types = batch.atom_types.view(-1).to(dtype=torch.long, device=pos.device)
            w = self.embed.weight.transpose(0, 1)  # (n_el,H)
            s = torch.nn.functional.embedding(atom_types, w)
        elif hasattr(batch, "node_attrs"):
            s = self.embed(batch.node_attrs.to(device=pos.device, dtype=pos.dtype))
        else:
            raise ValueError("FastEquivariantCore requires atom_types or node_attrs")

        v = torch.zeros((pos.shape[0], self.hidden, 3), dtype=pos.dtype, device=pos.device)
        t = torch.zeros((pos.shape[0], self.hidden, 5), dtype=pos.dtype, device=pos.device)
        for layer in self.layers:
            s, v, t = layer(s=s, v=v, t=t, edge_index=edge_index, edge_vec=edge_vec, r=r, rbf=rbf, cutoff=cutoff, num_nodes=int(pos.shape[0]))
        return s, v, t, edge_vec, r, cutoff


class FastEquivariantCoreO3(torch.nn.Module):
    """Parity-aware O(3) core built from ``FastEquivariantBlockO3``.

    Output tuple:
        ``(s, v, a, t2, t3, edge_vec, r, cutoff)``

    This module is a drop-in replacement for ``FastEquivariantCore`` whenever
    parity separation or L=3 channels are enabled in ``ModelConfig``.
    """

    def __init__(
        self,
        *,
        num_elements: int,
        type_zs: Optional[Sequence[int]] = None,
        cfg: Optional["ModelConfig"] = None,
        hidden: int,
        num_layers: int,
        rbf_dim: int,
        r_max: float,
    ):
        super().__init__()
        self.num_elements = int(num_elements)
        self.hidden = int(hidden)
        self.r_max = float(r_max)
        self.cfg = cfg if cfg is not None else ModelConfig()

        self.use_l3 = bool(getattr(self.cfg, "e3mu_use_l3", False))

        # Fallback one-hot embedding used when periodic-table features are disabled.
        self.embed = torch.nn.Linear(self.num_elements, self.hidden, bias=False)
        if type_zs is None:
            type_zs = list(range(1, int(self.num_elements) + 1))
        self.register_buffer(
            "type_zs",
            torch.tensor([int(z) for z in type_zs], dtype=torch.long),
            persistent=False,
        )

        self.rbf = _make_e3mu_rbf(self.cfg, rbf_dim, self.r_max)
        self.cutoff = CosineCutoff(self.r_max)
        self.layers = torch.nn.ModuleList(
            [FastEquivariantBlockO3(self.hidden, rbf_dim, use_l3=self.use_l3) for _ in range(int(num_layers))]
        )
        self.enable_film = bool(getattr(self.cfg, "enable_film", False))
        self.film_layers = torch.nn.ModuleList(
            [torch.nn.Linear(4, 3 * self.hidden) for _ in range(int(num_layers))]
            if self.enable_film else []
        )

        # Optional periodic-table descriptor encoder.
        self.element_encoder: Optional[PeriodicTableEmbedder] = None
        if bool(getattr(self.cfg, "enable_continuous_chem", False)):
            try:
                self.element_encoder = PeriodicTableEmbedder(
                    embedding_dim=self.hidden,
                    max_z=int(getattr(self.cfg, "chem_max_z", 96)),
                    aug_prob=float(getattr(self.cfg, "chem_aug_prob", 0.0)),
                    aug_noise_std=float(getattr(self.cfg, "chem_aug_noise_std", 0.0)),
                    aug_mix_max=float(getattr(self.cfg, "chem_aug_mix_max", 0.0)),
                )
            except Exception:
                self.element_encoder = None

    def forward(self, batch: Any) -> Tuple[torch.Tensor, ...]:
        pos = batch.positions
        edge_index = batch.edge_index
        shifts = getattr(batch, "shifts", None)
        if shifts is None:
            shifts = torch.zeros((edge_index.shape[1], 3), dtype=pos.dtype, device=pos.device)
        src = edge_index[0]
        dst = edge_index[1]
        edge_vec = pos[dst] + shifts - pos[src]
        r = torch.linalg.norm(edge_vec, dim=-1).clamp(min=1e-12)
        rbf = self.rbf(r)
        cutoff = self.cutoff(r)

        # Initial scalar embedding from either element descriptors or one-hot types.
        if self.element_encoder is not None:
            # Resolve atomic numbers from various batch layouts.
            if hasattr(batch, "atomic_numbers"):
                z = getattr(batch, "atomic_numbers").view(-1).to(device=pos.device, dtype=torch.long)
            elif hasattr(batch, "z"):
                z = getattr(batch, "z").view(-1).to(device=pos.device, dtype=torch.long)
            elif hasattr(batch, "atom_types"):
                atom_types = batch.atom_types.view(-1).to(device=pos.device, dtype=torch.long)
                z = self.type_zs.to(device=pos.device)[torch.clamp(atom_types, 0, self.type_zs.numel() - 1)]
            else:
                idx = torch.argmax(batch.node_attrs, dim=-1).to(device=pos.device, dtype=torch.long)
                z = self.type_zs.to(device=pos.device)[torch.clamp(idx, 0, self.type_zs.numel() - 1)]
            s = self.element_encoder(z)
        else:
            if hasattr(batch, "atom_types"):
                atom_types = batch.atom_types.view(-1).to(dtype=torch.long, device=pos.device)
                w = self.embed.weight.transpose(0, 1)
                s = torch.nn.functional.embedding(atom_types, w)
            elif hasattr(batch, "node_attrs"):
                s = self.embed(batch.node_attrs.to(device=pos.device, dtype=pos.dtype))
            else:
                raise ValueError("FastEquivariantCoreO3 requires atom_types, node_attrs, or atomic_numbers")

        n = int(pos.shape[0])
        v = torch.zeros((n, self.hidden, 3), dtype=pos.dtype, device=pos.device)   # polar
        a = torch.zeros((n, self.hidden, 3), dtype=pos.dtype, device=pos.device)   # axial
        t2 = torch.zeros((n, self.hidden, 5), dtype=pos.dtype, device=pos.device)
        t3 = torch.zeros((n, self.hidden, 7), dtype=pos.dtype, device=pos.device)

        film_condition = getattr(batch, "film_condition", None)
        if film_condition is not None:
            film_condition = film_condition.to(device=pos.device, dtype=pos.dtype)
            if film_condition.ndim != 2 or film_condition.shape != (n, 4):
                raise ValueError(
                    f"film_condition must have shape ({n}, 4), got {tuple(film_condition.shape)}"
                )

        for layer_idx, layer in enumerate(self.layers):
            if self.enable_film and film_condition is not None:
                gamma_s, beta_s, gamma_tensor = torch.chunk(
                    self.film_layers[layer_idx](film_condition), 3, dim=-1
                )
                gamma_s = 0.25 * torch.tanh(gamma_s)
                beta_s = _smooth_scalar_bound(beta_s, max_abs=5.0)
                gamma_tensor = 0.25 * torch.tanh(gamma_tensor)
                s = s * (1.0 + gamma_s) + beta_s
                gate = (1.0 + gamma_tensor).unsqueeze(-1)
                v = v * gate
                a = a * gate
                t2 = t2 * gate
                t3 = t3 * gate
            s, v, a, t2, t3 = layer(
                s=s, v=v, a=a, t2=t2, t3=t3,
                edge_index=edge_index, edge_vec=edge_vec, r=r, rbf=rbf,
                cutoff=cutoff, num_nodes=n,
            )

        return s, v, a, t2, t3, edge_vec, r, cutoff


class BackupGroundModel(torch.nn.Module):
    """Ground-state energy layer responsible for ``E_PES(R)``.

    This branch models the field-free potential energy surface and provides the
    stable scalar backbone of the dual-layer architecture.
    """
    def __init__(self, *, z_table, atomic_energies_1d, cfg):
        super().__init__()
        # Select either the parity-aware O(3) core or the classic SO(3) core.
        use_o3 = bool(getattr(cfg, "e3mu_use_parity", False) or getattr(cfg, "e3mu_use_l3", False))
        if getattr(cfg, "e3mu_use_l3", False) and not getattr(cfg, "e3mu_use_parity", False):
            cfg.e3mu_use_parity = True  # L=3 requires parity separation
            use_o3 = True
        if use_o3:
            self.core: torch.nn.Module = FastEquivariantCoreO3(
                num_elements=len(z_table),
                type_zs=list(getattr(z_table, "zs", [])),
                cfg=cfg,
                hidden=int(cfg.num_channels),
                num_layers=int(cfg.num_interactions),
                rbf_dim=int(cfg.num_radial_basis),
                r_max=float(cfg.r_max),
            )
        else:
            self.core = FastEquivariantCore(
                num_elements=len(z_table),
                hidden=int(cfg.num_channels),
                num_layers=int(cfg.num_interactions),
                rbf_dim=int(cfg.num_radial_basis),
                r_max=float(cfg.r_max),
            )
        self.energy_head = torch.nn.Sequential(
            torch.nn.Linear(int(cfg.num_channels), int(cfg.num_channels)),
            torch.nn.SiLU(),
            torch.nn.Linear(int(cfg.num_channels), 1),
        )
        ae = torch.tensor(np.asarray(atomic_energies_1d, dtype=float).reshape(-1), dtype=torch.get_default_dtype())
        self.register_buffer("atomic_energies", ae)

    def forward(self, batch):
        out = self.core(batch)
        # SO(3) core returns 6-tuple; O3 core returns 8-tuple.
        s = out[0]
        e_atom = self.energy_head(s).squeeze(-1)
        idx = batch.atom_types.view(-1).to(torch.long)
        e_atom = e_atom + self.atomic_energies[idx]
        num_graphs = int(batch.ptr.numel() - 1)
        e = scatter_sum(e_atom, batch.batch, dim_size=num_graphs)
        return e, e_atom

class BackupResponseModel(torch.nn.Module):
    """Field-response layer predicting charges, dipoles, and polarizability.

    The response branch is intentionally separated from the ground-state energy
    branch so field-induced targets can be learned without destabilising the
    baseline PES.
    """
    def __init__(self, *, z_table, cfg):
        super().__init__()
        self.cfg = cfg
        self.hidden = int(cfg.num_channels)
        self.register_buffer("st_basis", _build_st_basis(torch.get_default_dtype()), persistent=False)
        # Match the response head to the same symmetry setting as the backbone.
        use_o3 = bool(getattr(cfg, "e3mu_use_parity", False) or getattr(cfg, "e3mu_use_l3", False))
        if getattr(cfg, "e3mu_use_l3", False) and not getattr(cfg, "e3mu_use_parity", False):
            cfg.e3mu_use_parity = True
            use_o3 = True
        if use_o3:
            self.core: torch.nn.Module = FastEquivariantCoreO3(
                num_elements=len(z_table),
                type_zs=list(getattr(z_table, "zs", [])),
                cfg=cfg,
                hidden=self.hidden,
                num_layers=int(cfg.num_interactions),
                rbf_dim=int(cfg.num_radial_basis),
                r_max=float(cfg.r_max),
            )
        else:
            self.core = FastEquivariantCore(
                num_elements=len(z_table),
                hidden=self.hidden,
                num_layers=int(cfg.num_interactions),
                rbf_dim=int(cfg.num_radial_basis),
                r_max=float(cfg.r_max),
            )
        self.q_head = torch.nn.Sequential(torch.nn.Linear(self.hidden, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, 1))
        self.mu_gate = torch.nn.Sequential(torch.nn.Linear(self.hidden, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, self.hidden), torch.nn.Tanh())
        self.alpha_iso_head = torch.nn.Sequential(torch.nn.Linear(self.hidden, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, 1))
        self.alpha_aniso_gate = torch.nn.Sequential(torch.nn.Linear(self.hidden, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, self.hidden))
        self.chi_head = torch.nn.Sequential(
            torch.nn.Linear(self.hidden, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, 1)
        )
        self.hardness_head = torch.nn.Sequential(
            torch.nn.Linear(self.hidden, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, 1)
        )
        self.c6_scale_head = torch.nn.Sequential(
            torch.nn.Linear(self.hidden, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, 1)
        )

    def forward_components(self, batch) -> Dict[str, torch.Tensor]:
        out = self.core(batch)
        # SO(3) core: (s, v, t, edge_vec, r, cutoff) — 6-tuple
        # O3  core:   (s, v, a, t2, t3, edge_vec, r, cutoff) — 8-tuple
        # We extract s (scalars), v (polar vectors), t (L=2 tensor, always at position 2 or 3).
        if len(out) == 6:
            s, v, t = out[0], out[1], out[2]
        else:
            s, v, t = out[0], out[1], out[3]  # out[3] = t2 in O3 core

        # Partial charges used in the long-range electrostatic correction.
        q = self.q_head(s).squeeze(-1)

        # Atomic dipoles are read out from the polar-vector channel.
        w_mu = self.mu_gate(s)
        atomic_dipoles = torch.sum(w_mu.unsqueeze(-1) * v, dim=1)

        # Polarizability is decomposed into isotropic and anisotropic parts.
        # The isotropic component is kept positive with softplus.
        alpha_raw = self.alpha_iso_head(s).squeeze(-1)
        alpha_iso = torch.nn.functional.softplus(alpha_raw)
        w_a = self.alpha_aniso_gate(s)
        alpha_l2 = torch.einsum("nh,nhk->nk", w_a, t)
        alpha_aniso = torch.einsum("nk,kcd->ncd", alpha_l2, self.st_basis)
        I = torch.eye(3, dtype=t.dtype, device=t.device).view(1, 3, 3)
        atomic_alpha = alpha_iso.view(-1, 1, 1) * I + alpha_aniso
        # Project away the small numerical asymmetry introduced by finite precision.
        atomic_alpha = 0.5 * (atomic_alpha + atomic_alpha.transpose(-1, -2))

        num_graphs = int(batch.ptr.numel() - 1)
        alpha = scatter_sum(atomic_alpha, batch.batch, dim_size=num_graphs)

        # Compact spherical-like packing kept for downstream extensions.
        # Slot 0 stores the isotropic term; slots 1..5 store the L=2 components.
        atomic_polar_sh = torch.zeros((s.shape[0], 6), dtype=s.dtype, device=s.device)
        atomic_polar_sh[:, 0] = alpha_raw
        atomic_polar_sh[:, 1:6] = alpha_l2.to(dtype=s.dtype)

        hardness = torch.nn.functional.softplus(self.hardness_head(s).squeeze(-1))
        hardness = hardness + float(getattr(self.cfg, "qeq_hardness_min", 0.25))
        return {
            "raw_charges": q,
            "atomic_dipoles": atomic_dipoles,
            "atomic_polarizability": atomic_alpha,
            "polarizability": alpha,
            "chi": self.chi_head(s).squeeze(-1),
            "hardness": hardness,
            "c6_scale": torch.nn.functional.softplus(self.c6_scale_head(s).squeeze(-1)),
            "scalar_features": s,
            "polar_features": v,
            "tensor_features": t,
            "axial_features": out[2] if len(out) == 8 else torch.zeros_like(v),
        }

    def forward(self, batch):
        components = self.forward_components(batch)
        return (
            components["raw_charges"],
            components["atomic_dipoles"],
            components["polarizability"],
        )


def _batch_num_graphs(batch: Any) -> int:
    if hasattr(batch, "ptr"):
        return int(batch.ptr.numel() - 1)
    return int(getattr(batch, "num_graphs", 1))


def _batch_field(batch: Any, num_graphs: int) -> torch.Tensor:
    pos = batch.positions
    field_value = getattr(batch, "field", None)
    if field_value is None:
        return torch.zeros((num_graphs, 3), dtype=pos.dtype, device=pos.device)
    out = torch.as_tensor(field_value, dtype=pos.dtype, device=pos.device)
    if out.numel() == 3:
        return out.reshape(1, 3).expand(num_graphs, 3)
    if out.numel() == 3 * num_graphs:
        return out.reshape(num_graphs, 3)
    raise ValueError(f"field cannot be reshaped to ({num_graphs}, 3): {tuple(out.shape)}")


def _batch_total_charge(batch: Any, num_graphs: int, dtype: torch.dtype) -> torch.Tensor:
    value = getattr(batch, "total_charge", None)
    if value is None:
        return torch.zeros((num_graphs,), dtype=dtype, device=batch.positions.device)
    out = torch.as_tensor(value, dtype=dtype, device=batch.positions.device).reshape(-1)
    if out.numel() == 1:
        return out.expand(num_graphs)
    if out.numel() != num_graphs:
        raise ValueError(f"total_charge has {out.numel()} values for {num_graphs} graphs")
    return out


def _batch_atomic_numbers(batch: Any, type_zs: torch.Tensor) -> torch.Tensor:
    for name in ("atomic_numbers", "z"):
        value = getattr(batch, name, None)
        if value is not None:
            return torch.as_tensor(value, device=batch.positions.device, dtype=torch.long).reshape(-1)
    atom_types = batch.atom_types.reshape(-1).to(device=batch.positions.device, dtype=torch.long)
    return type_zs.to(batch.positions.device)[atom_types]


def _minimum_image_pair_matrix(
    positions: torch.Tensor,
    cell: torch.Tensor,
    pbc: torch.Tensor,
) -> torch.Tensor:
    """Return r_i-r_j with a differentiable minimum-image convention."""
    dr = positions[:, None, :] - positions[None, :, :]
    if bool(torch.any(pbc).detach().cpu()):
        inv = torch.linalg.inv(cell)
        frac = torch.einsum("ijc,cd->ijd", dr, inv)
        periodic = pbc.to(dtype=positions.dtype).view(1, 1, 3)
        frac = frac - torch.round(frac) * periodic
        dr = torch.einsum("ijc,cd->ijd", frac, cell)
    return dr


def _graph_cell_pbc(batch: Any, graph_index: int, num_graphs: int) -> Tuple[torch.Tensor, torch.Tensor]:
    cells = _reshape_batched_cell(batch.cell, num_graphs)
    pbc_value = getattr(batch, "pbc", None)
    if pbc_value is None:
        pbc = torch.zeros((num_graphs, 3), dtype=torch.bool, device=batch.positions.device)
    else:
        pbc = torch.as_tensor(pbc_value, dtype=torch.bool, device=batch.positions.device).reshape(-1, 3)
        if pbc.shape[0] == 1 and num_graphs > 1:
            pbc = pbc.expand(num_graphs, 3)
    return cells[graph_index], pbc[graph_index]


class DifferentiableQEq(torch.nn.Module):
    """Charge equilibration with an exact graph-wise charge constraint."""

    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.smearing = float(cfg.qeq_smearing)
        self.use_pme = bool(cfg.enable_pme)
        self.pme_smearing = float(cfg.qeq_pme_smearing)
        self.pme_lr_wavelength = float(cfg.qeq_pme_lr_wavelength)
        self.stability_floor = float(cfg.qeq_stability_floor)

    @staticmethod
    def _half_pairs(dr: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        n = int(dr.shape[0])
        idx = torch.triu_indices(n, n, offset=1, device=dr.device)
        vectors = dr[idx[0], idx[1]]
        return idx.T.contiguous(), vectors, torch.linalg.norm(vectors, dim=-1).clamp(min=1e-10)

    @staticmethod
    def _neutral_helmert_basis(
        n: int,
        *,
        dtype: torch.dtype,
        device: torch.device,
    ) -> torch.Tensor:
        """Return an analytic orthonormal basis for vectors whose sum is zero."""
        if int(n) <= 1:
            return torch.zeros((int(n), 0), dtype=dtype, device=device)
        columns = torch.arange(1, int(n), dtype=dtype, device=device)
        rows = torch.arange(int(n), dtype=dtype, device=device).unsqueeze(1)
        before = (rows < columns).to(dtype)
        pivot = (rows == columns).to(dtype)
        raw = before - pivot * columns.unsqueeze(0)
        norm = torch.sqrt(columns * (columns + 1.0))
        return raw / norm.unsqueeze(0)

    @staticmethod
    def _smallest_symmetric_eigenvalue(matrix: torch.Tensor) -> torch.Tensor:
        """Evaluate the stability spectrum robustly, with a rigorous fallback."""
        symmetric = 0.5 * (matrix + matrix.transpose(0, 1))
        if not bool(torch.isfinite(symmetric).all().detach().cpu()):
            raise FloatingPointError("QEq projected Hessian contains non-finite values")
        # Determine the eigenpair on CPU float64 without attaching its device
        # transfers to autograd.  A Rayleigh-quotient surrogate below restores
        # the exact first derivative v v^T on the original device, preserving
        # conservative forces without asking MPS to backpropagate float64 ops.
        with torch.no_grad():
            symmetric_cpu = symmetric.detach().to("cpu")
            try:
                eigenvalues, eigenvectors = torch.linalg.eigh(
                    symmetric_cpu.to(torch.float64)
                )
                eigenvalue = eigenvalues[0]
                eigenvector = eigenvectors[:, 0]
            except (RuntimeError, TypeError):
                # Gershgorin supplies a conservative lower bound on lambda_min,
                # preserving positive curvature if eigensolution still fails.
                diagonal = torch.diagonal(symmetric)
                off_diagonal_radius = (
                    torch.sum(torch.abs(symmetric), dim=1) - torch.abs(diagonal)
                )
                return torch.min(diagonal - off_diagonal_radius)
        eigenvalue_local = eigenvalue.to(device=matrix.device, dtype=matrix.dtype)
        eigenvector_local = eigenvector.to(device=matrix.device, dtype=matrix.dtype)
        rayleigh = eigenvector_local @ symmetric @ eigenvector_local
        return eigenvalue_local + rayleigh - rayleigh.detach()

    def _kernel(self, pos: torch.Tensor, cell: torch.Tensor, pbc: torch.Tensor) -> torch.Tensor:
        dr = _minimum_image_pair_matrix(pos, cell, pbc)
        r2 = torch.sum(dr * dr, dim=-1)
        n = int(pos.shape[0])
        direct = COULOMB_EV_ANGSTROM / torch.sqrt(r2 + self.smearing * self.smearing)
        direct = direct - torch.diag_embed(torch.diagonal(direct))
        if not self.use_pme or not bool(torch.any(pbc).detach().cpu()):
            return direct
        if not HAS_TORCHPME:
            raise RuntimeError("enable_pme=True requires torch-pme")
        pairs, _vectors, distances = self._half_pairs(dr)
        potential = torchpme.CoulombPotential(
            smearing=self.pme_smearing,
            prefactor=COULOMB_EV_ANGSTROM,
        )
        calculator = torchpme.EwaldCalculator(
            potential,
            lr_wavelength=self.pme_lr_wavelength,
            full_neighbor_list=False,
        ).to(device=pos.device, dtype=pos.dtype)
        basis_charges = torch.eye(n, dtype=pos.dtype, device=pos.device)
        response_kernel = calculator(
            charges=basis_charges,
            cell=cell,
            positions=pos,
            neighbor_indices=pairs,
            neighbor_distances=distances,
            periodic=pbc,
        )
        return 0.5 * (response_kernel + response_kernel.transpose(0, 1))

    def forward(
        self,
        *,
        chi: torch.Tensor,
        hardness: torch.Tensor,
        batch: Any,
        total_charge: torch.Tensor,
        field: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:
        num_graphs = _batch_num_graphs(batch)
        q_out = torch.zeros_like(chi)
        potential_out = torch.zeros_like(chi)
        e_local: List[torch.Tensor] = []
        e_coulomb: List[torch.Tensor] = []
        residuals: List[torch.Tensor] = []
        stability_shifts: List[torch.Tensor] = []
        for graph_index in range(num_graphs):
            mask = batch.batch == graph_index
            pos = batch.positions[mask]
            chi_g = chi[mask]
            hard_g = hardness[mask]
            cell, pbc = _graph_cell_pbc(batch, graph_index, num_graphs)
            kernel = self._kernel(pos, cell, pbc)
            center = torch.mean(pos, dim=0, keepdim=True)
            rel = _minimum_image_pair_matrix(pos, cell, pbc)[:, 0, :]
            # Re-center explicitly for non-periodic systems; periodic uniform fields
            # remain a finite-cell convention and are recorded in the dataset metadata.
            if not bool(torch.any(pbc).detach().cpu()):
                rel = pos - center
            phi_ext = -torch.sum(rel * field[graph_index].view(1, 3), dim=-1)
            n = int(pos.shape[0])
            base_hessian = kernel + torch.diag(hard_g)
            if n > 1:
                neutral_basis = self._neutral_helmert_basis(
                    n, dtype=pos.dtype, device=pos.device
                )
                projected = neutral_basis.transpose(0, 1) @ base_hessian @ neutral_basis
                min_eigenvalue = self._smallest_symmetric_eigenvalue(projected)
                stability_shift = torch.relu(
                    torch.as_tensor(self.stability_floor, dtype=pos.dtype, device=pos.device)
                    - min_eigenvalue
                )
            else:
                stability_shift = torch.zeros((), dtype=pos.dtype, device=pos.device)
            effective_hardness = hard_g + stability_shift
            hessian = kernel + torch.diag(effective_hardness)
            linear_term = chi_g + phi_ext
            graph_charge = total_charge[graph_index]
            if n == 1:
                q_g = graph_charge.view(1)
                lagrange = -(hessian @ q_g + linear_term)[0]
            else:
                # Eliminate the exact charge constraint analytically.  The
                # resulting neutral-space Hessian is SPD after the stability
                # shift, avoiding the indefinite KKT/LU backward path that is
                # unreliable for larger systems on Apple MPS.
                ones = torch.ones(n, dtype=pos.dtype, device=pos.device)
                q_reference = (graph_charge / float(n)) * ones
                reduced_hessian = (
                    neutral_basis.transpose(0, 1) @ hessian @ neutral_basis
                )
                reduced_hessian = 0.5 * (
                    reduced_hessian + reduced_hessian.transpose(0, 1)
                )
                reduced_rhs = -neutral_basis.transpose(0, 1) @ (
                    hessian @ q_reference + linear_term
                )
                jitter_value = max(1e-10, 10.0 * torch.finfo(pos.dtype).eps)
                reduced_hessian = reduced_hessian + jitter_value * torch.eye(
                    n - 1, dtype=pos.dtype, device=pos.device
                )
                cholesky = torch.linalg.cholesky(reduced_hessian)
                intermediate = torch.linalg.solve_triangular(
                    cholesky, reduced_rhs.unsqueeze(-1), upper=False
                )
                neutral_coordinates = torch.linalg.solve_triangular(
                    cholesky.transpose(0, 1), intermediate, upper=True
                ).squeeze(-1)
                q_g = q_reference + neutral_basis @ neutral_coordinates
                lagrange = -torch.mean(hessian @ q_g + linear_term)
            potential = kernel @ q_g
            q_out[mask] = q_g
            potential_out[mask] = potential
            e_local.append(
                torch.sum(chi_g * q_g + 0.5 * effective_hardness * q_g * q_g + phi_ext * q_g)
            )
            e_coulomb.append(0.5 * torch.dot(q_g, potential))
            stationarity = hessian @ q_g + linear_term + lagrange
            charge_error = torch.abs(torch.sum(q_g) - total_charge[graph_index])
            residuals.append(torch.maximum(torch.max(torch.abs(stationarity)), charge_error))
            stability_shifts.append(stability_shift)
        return {
            "charges": q_out,
            "potential": potential_out,
            "energy_local": torch.stack(e_local),
            "energy_coulomb": torch.stack(e_coulomb),
            "residual": torch.stack(residuals),
            "stability_shift": torch.stack(stability_shifts),
        }


class SelfConsistentPolarization(torch.nn.Module):
    """Thole-damped induced dipoles from the exact linear equilibrium solve."""

    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.max_iter = int(cfg.deq_max_iter)
        self.tol = float(cfg.deq_tol)
        self.damping = float(cfg.deq_damping)
        self.alpha_max = float(cfg.deq_alpha_max)
        self.smearing = float(cfg.qeq_smearing)
        if not math.isfinite(self.damping) or self.damping <= 0.0:
            raise ValueError("deq_damping must be finite and greater than zero")
        if not math.isfinite(self.alpha_max) or self.alpha_max <= 0.0:
            raise ValueError("deq_alpha_max must be finite and greater than zero")

    def _interaction_tensor(
        self,
        pos: torch.Tensor,
        cell: torch.Tensor,
        pbc: torch.Tensor,
        alpha_volume: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Return displacements, damped charge fields, and the Thole dipole tensor."""
        dr = _minimum_image_pair_matrix(pos, cell, pbc)
        r2 = torch.sum(dr * dr, dim=-1)
        atom_count = int(pos.shape[0])
        diagonal = torch.eye(atom_count, dtype=torch.bool, device=pos.device)
        r = torch.sqrt(torch.clamp(r2, min=1e-12))
        raw_inv_r3 = torch.where(
            diagonal,
            torch.zeros_like(r),
            torch.pow(torch.clamp(r2, min=1e-12), -1.5),
        )
        if alpha_volume is None:
            # Compatibility path for callers without learned polarizabilities.
            reference = max(self.smearing**3, 1e-6)
            alpha_volume = torch.full(
                (atom_count,), reference, dtype=pos.dtype, device=pos.device
            )
        alpha_volume = torch.clamp(
            alpha_volume.to(dtype=pos.dtype, device=pos.device),
            min=1e-8,
            max=self.alpha_max,
        )
        # Exponential Thole damping uses the polarizability-scaled separation
        # u_ij = r_ij / (alpha_i alpha_j)^(1/6).  The distinct f3/f5 factors
        # preserve the tensor form while preventing a short-range polarization
        # catastrophe.  ``deq_damping`` is the conventional dimensionless a.
        pair_scale = torch.pow(
            torch.clamp(alpha_volume[:, None] * alpha_volume[None, :], min=1e-16),
            1.0 / 6.0,
        )
        damp_argument = float(self.damping) * torch.pow(r / pair_scale, 3)
        damp_argument = torch.clamp(damp_argument, min=0.0, max=50.0)
        exponential = torch.exp(-damp_argument)
        f3 = 1.0 - exponential
        f5 = 1.0 - (1.0 + damp_argument) * exponential
        f3 = torch.where(diagonal, torch.zeros_like(f3), f3)
        f5 = torch.where(diagonal, torch.zeros_like(f5), f5)
        charge_inv_r3 = raw_inv_r3 * f3
        rhat = dr / r.unsqueeze(-1).clamp(min=1e-12)
        identity = torch.eye(3, dtype=pos.dtype, device=pos.device)
        tensor = COULOMB_EV_ANGSTROM * raw_inv_r3.unsqueeze(-1).unsqueeze(-1) * (
            3.0 * f5.unsqueeze(-1).unsqueeze(-1)
            * rhat.unsqueeze(-1) * rhat.unsqueeze(-2)
            - f3.unsqueeze(-1).unsqueeze(-1) * identity
        )
        return dr, charge_inv_r3, tensor

    def _fields(
        self,
        pos: torch.Tensor,
        q: torch.Tensor,
        dipoles: torch.Tensor,
        cell: torch.Tensor,
        pbc: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        dr, inv_r3, interaction = self._interaction_tensor(pos, cell, pbc)
        charge_field = COULOMB_EV_ANGSTROM * torch.sum(
            q.view(1, -1, 1) * dr * inv_r3.unsqueeze(-1), dim=1
        )
        dipole_field = torch.einsum("ijab,jb->ia", interaction, dipoles)
        return charge_field, dipole_field

    def forward(
        self,
        *,
        atomic_alpha: torch.Tensor,
        charges: torch.Tensor,
        permanent_dipoles: torch.Tensor,
        batch: Any,
        field: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:
        num_graphs = _batch_num_graphs(batch)
        induced = torch.zeros_like(batch.positions)
        energies: List[torch.Tensor] = []
        residuals: List[torch.Tensor] = []
        iterations: List[torch.Tensor] = []
        stability_shifts: List[torch.Tensor] = []
        for graph_index in range(num_graphs):
            mask = batch.batch == graph_index
            pos = batch.positions[mask]
            q = charges[mask]
            p0 = permanent_dipoles[mask]
            alpha_volume = torch.diagonal(atomic_alpha[mask], dim1=-2, dim2=-1).mean(dim=-1)
            alpha = torch.clamp(
                alpha_volume * ALPHA_VOLUME_TO_EV_PER_FIELD2,
                min=1e-8,
                max=self.alpha_max * ALPHA_VOLUME_TO_EV_PER_FIELD2,
            )
            cell, pbc = _graph_cell_pbc(batch, graph_index, num_graphs)
            dr, inv_r3, interaction = self._interaction_tensor(
                pos, cell, pbc, alpha_volume=alpha_volume
            )
            charge_field = COULOMB_EV_ANGSTROM * torch.sum(
                q.view(1, -1, 1) * dr * inv_r3.unsqueeze(-1), dim=1
            )
            permanent_field = torch.einsum("ijab,jb->ia", interaction, p0)
            driving = (
                field[graph_index].view(1, 3)
                + charge_field
                + permanent_field
            )

            # The fixed-point equation is linear. Solving its symmetric form
            # directly is both more accurate and much more memory efficient
            # than retaining up to 50 unrolled iterations for force training.
            sqrt_alpha = torch.sqrt(alpha)
            scaled_interaction = (
                sqrt_alpha[:, None, None, None]
                * interaction
                * sqrt_alpha[None, :, None, None]
            )
            atom_count = int(pos.shape[0])
            matrix_size = 3 * atom_count
            interaction_matrix = scaled_interaction.permute(0, 2, 1, 3).reshape(
                matrix_size, matrix_size
            )
            identity = torch.eye(
                matrix_size, dtype=pos.dtype, device=pos.device
            )
            hessian = identity - 0.5 * (
                interaction_matrix + interaction_matrix.transpose(0, 1)
            )
            # A 1e-5 floor permits a 1e5 response amplification and is not a
            # meaningful equilibrium for a learned polarizable model.  Keep the
            # scaled Hessian safely positive while retaining an exact solve.
            stability_floor = max(
                5e-2,
                32.0 * float(matrix_size) * float(torch.finfo(pos.dtype).eps),
            )
            min_eigenvalue = DifferentiableQEq._smallest_symmetric_eigenvalue(
                hessian
            )
            stability_shift = torch.relu(
                torch.as_tensor(
                    stability_floor, dtype=pos.dtype, device=pos.device
                )
                - min_eigenvalue
            )
            stable_hessian = hessian + stability_shift * identity
            rhs = (sqrt_alpha.unsqueeze(-1) * driving).reshape(-1)
            cholesky = torch.linalg.cholesky(stable_hessian)
            intermediate = torch.linalg.solve_triangular(
                cholesky, rhs.unsqueeze(-1), upper=False
            )
            transformed = torch.linalg.solve_triangular(
                cholesky.transpose(0, 1), intermediate, upper=True
            ).squeeze(-1)
            p = sqrt_alpha.unsqueeze(-1) * transformed.reshape(atom_count, 3)
            residual = torch.max(
                torch.abs(stable_hessian @ transformed - rhs)
            )
            energy = (
                0.5 * transformed @ stable_hessian @ transformed
                - transformed @ rhs
            )
            induced[mask] = p
            energies.append(energy)
            residuals.append(residual)
            iterations.append(
                torch.ones((), dtype=pos.dtype, device=pos.device)
            )
            stability_shifts.append(stability_shift)
        return {
            "induced_dipoles": induced,
            "energy": torch.stack(energies),
            "residual": torch.stack(residuals),
            "iterations": torch.stack(iterations),
            "stability_shift": torch.stack(stability_shifts),
        }


class D4DispersionLayer(torch.nn.Module):
    """Differentiable molecular DFT-D4 energy with learned QEq charges."""

    BOHR_TO_ANGSTROM = 0.529177210903
    HARTREE_TO_EV = 27.211386245988

    def __init__(self, cfg: ModelConfig, type_zs: Sequence[int]):
        super().__init__()
        self.functional = str(cfg.d4_functional).lower()
        self.register_buffer("type_zs", torch.tensor(list(type_zs), dtype=torch.long), persistent=True)
        if not HAS_TAD_DFTD4:
            raise RuntimeError("enable_d4=True requires tad-dftd4")
        self.params = tad_dftd4.get_params(method="d4", functional=self.functional)

    def forward(
        self,
        *,
        batch: Any,
        charges: torch.Tensor,
        c6_scale: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        num_graphs = _batch_num_graphs(batch)
        numbers_all = _batch_atomic_numbers(batch, self.type_zs)
        energies: List[torch.Tensor] = []
        c6_diag = torch.zeros_like(charges)
        d4_alpha = torch.zeros_like(charges)
        for graph_index in range(num_graphs):
            mask = batch.batch == graph_index
            _cell, graph_pbc = _graph_cell_pbc(batch, graph_index, num_graphs)
            if bool(torch.any(graph_pbc).detach().cpu()):
                # tad-dftd4's molecular API does not include lattice images.
                # Returning a masked zero keeps mixed periodic batches valid;
                # periodic dispersion requires a dedicated periodic backend.
                energies.append(
                    torch.zeros((), dtype=charges.dtype, device=charges.device)
                )
                continue
            numbers = numbers_all[mask]
            positions_bohr = batch.positions[mask] / self.BOHR_TO_ANGSTROM
            total_charge = torch.sum(charges[mask])
            output_device = positions_bohr.device
            # tad-dftd4 0.8 loads float64 reference tables on the calculation
            # device.  Apple MPS cannot represent float64, so run this small
            # physics sublayer on CPU while preserving autograd through the
            # explicit device transfers.
            if output_device.type == "mps":
                numbers_work = numbers.to("cpu")
                positions_work = positions_bohr.to("cpu")
                charge_work = total_charge.to("cpu")
                q_work = charges[mask].to("cpu")
            else:
                numbers_work = numbers
                positions_work = positions_bohr
                charge_work = total_charge
                q_work = charges[mask]
            e_atom = tad_dftd4.dftd4(
                numbers_work,
                positions_work,
                charge_work,
                self.params,
                q=q_work,
            )
            energies.append(
                (torch.sum(e_atom) * self.HARTREE_TO_EV).to(
                    device=output_device, dtype=charges.dtype
                )
            )
            try:
                _cn, _q_ref, c6, alpha = tad_dftd4.get_properties(
                    numbers_work, positions_work, charge_work
                )
                converted_c6 = torch.diagonal(c6, dim1=-2, dim2=-1)
                converted_c6 = converted_c6 * self.HARTREE_TO_EV * self.BOHR_TO_ANGSTROM**6
                converted_c6 = converted_c6.to(
                    device=output_device, dtype=c6_diag.dtype
                )
                if c6_scale is not None:
                    converted_c6 = converted_c6 * c6_scale[mask]
                c6_diag[mask] = converted_c6
                d4_alpha[mask] = alpha.to(
                    device=output_device, dtype=d4_alpha.dtype
                ) * self.BOHR_TO_ANGSTROM**3
            except Exception:
                pass
        return {"energy": torch.stack(energies), "atomic_c6": c6_diag, "atomic_polarizability": d4_alpha}


class TimeReversalSpinHamiltonian(torch.nn.Module):
    """Geometry-parameterized J/D/DMI Hamiltonian, exactly even under S -> -S."""

    def __init__(self, hidden: int, rbf_dim: int, spin_cutoff: float, enable_dmi: bool):
        super().__init__()
        self.hidden = int(hidden)
        self.spin_cutoff = float(spin_cutoff)
        self.enable_dmi = bool(enable_dmi)
        self.rbf = GaussianRBF(rbf_dim, self.spin_cutoff)
        pair_dim = 2 * self.hidden + rbf_dim
        self.j_head = torch.nn.Sequential(
            torch.nn.Linear(pair_dim, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, 1)
        )
        self.dmi_gate = torch.nn.Sequential(
            torch.nn.Linear(pair_dim, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, self.hidden)
        )
        self.polar_a = torch.nn.Linear(self.hidden, self.hidden, bias=False)
        self.polar_b = torch.nn.Linear(self.hidden, self.hidden, bias=False)
        self.di_gate = torch.nn.Sequential(
            torch.nn.Linear(self.hidden, self.hidden), torch.nn.SiLU(), torch.nn.Linear(self.hidden, self.hidden)
        )
        self.moment_head = torch.nn.Sequential(
            torch.nn.Linear(self.hidden, self.hidden),
            torch.nn.SiLU(),
            torch.nn.Linear(self.hidden, 1),
        )
        self.register_buffer("st_basis", _build_st_basis(torch.get_default_dtype()), persistent=False)

    def forward(
        self,
        *,
        batch: Any,
        scalar_features: torch.Tensor,
        polar_features: torch.Tensor,
        axial_features: torch.Tensor,
        tensor_features: torch.Tensor,
        spins: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:
        src_all, dst_all = batch.edge_index[0], batch.edge_index[1]
        di_weights = self.di_gate(scalar_features)
        di_l2 = torch.einsum("nh,nhk->nk", di_weights, tensor_features)
        di = torch.einsum("nk,kcd->ncd", di_l2, self.st_basis)
        di = 0.5 * (di + di.transpose(-1, -2))
        trace = torch.diagonal(di, dim1=-2, dim2=-1).sum(-1) / 3.0
        eye = torch.eye(3, dtype=di.dtype, device=di.device)
        di = di - trace.view(-1, 1, 1) * eye
        moment_magnitude = torch.nn.functional.softplus(self.moment_head(scalar_features).squeeze(-1))
        magnetic_moments = moment_magnitude.unsqueeze(-1) * spins
        shifts = getattr(batch, "shifts", torch.zeros((src_all.numel(), 3), dtype=spins.dtype, device=spins.device))
        edge_vec = batch.positions[dst_all] + shifts - batch.positions[src_all]
        edge_r = torch.linalg.norm(edge_vec, dim=-1)
        pair_mask = (src_all < dst_all) & (edge_r <= self.spin_cutoff)
        src, dst = src_all[pair_mask], dst_all[pair_mask]
        r = edge_r[pair_mask].clamp(min=1e-10)
        if src.numel() == 0:
            n_graphs = _batch_num_graphs(batch)
            atom_energy = torch.einsum("ni,nij,nj->n", spins, di, spins)
            single_ion_energy = scatter_sum(atom_energy, batch.batch, dim_size=n_graphs)
            return {
                "energy": single_ion_energy,
                "pair_index": torch.zeros((2, 0), dtype=torch.long, device=spins.device),
                "Jij": torch.zeros((0,), dtype=spins.dtype, device=spins.device),
                "Di": di,
                "DMIij": torch.zeros((0, 3), dtype=spins.dtype, device=spins.device),
                "magnetic_moments": magnetic_moments,
            }
        pair_scalar = torch.cat(
            [
                scalar_features[src] + scalar_features[dst],
                torch.abs(scalar_features[src] - scalar_features[dst]),
                self.rbf(r),
            ],
            dim=-1,
        )
        jij = self.j_head(pair_scalar).squeeze(-1)
        gate = self.dmi_gate(pair_scalar)
        axial_pair = torch.sum(gate.unsqueeze(-1) * (axial_features[src] + axial_features[dst]), dim=1)
        p_a = self.polar_a(polar_features[src].transpose(1, 2)).transpose(1, 2)
        p_b = self.polar_b(polar_features[dst].transpose(1, 2)).transpose(1, 2)
        axial_pair = axial_pair + torch.sum(torch.cross(p_a, p_b, dim=-1), dim=1) / max(1, self.hidden)
        dmi = axial_pair if self.enable_dmi else torch.zeros_like(axial_pair)

        spin_dot = torch.sum(spins[src] * spins[dst], dim=-1)
        spin_cross = torch.cross(spins[src], spins[dst], dim=-1)
        pair_energy = -jij * spin_dot + torch.sum(dmi * spin_cross, dim=-1)
        atom_energy = torch.einsum("ni,nij,nj->n", spins, di, spins)
        pair_graph = batch.batch[src]
        n_graphs = _batch_num_graphs(batch)
        energy = scatter_sum(pair_energy, pair_graph, dim_size=n_graphs)
        energy = energy + scatter_sum(atom_energy, batch.batch, dim_size=n_graphs)
        return {
            "energy": energy,
            "pair_index": torch.stack([src, dst], dim=0),
            "Jij": jij,
            "Di": di,
            "DMIij": dmi,
            "magnetic_moments": magnetic_moments,
        }


class DualLayerFieldModel(torch.nn.Module):
    """Full dual-layer model combining the ground and response branches.

    The design cleanly separates field-free energy learning from field-induced
    tensor prediction, then recombines both terms through the effective
    Hamiltonian used for energies and forces.
    """
    def __init__(self, *, z_table, atomic_energies_1d, cfg):
        super().__init__()
        self.cfg = cfg
        self.z_table_zs = list(z_table.zs)
        self.ground = BackupGroundModel(z_table=z_table, atomic_energies_1d=atomic_energies_1d, cfg=cfg)
        self.response = BackupResponseModel(z_table=z_table, cfg=cfg)

    def freeze_ground(self) -> None:
        self.ground.eval()
        for p in self.ground.parameters():
            p.requires_grad_(False)

    def unfreeze_ground(self) -> None:
        self.ground.train()
        for p in self.ground.parameters():
            p.requires_grad_(True)

    def freeze_response(self) -> None:
        self.response.eval()
        for p in self.response.parameters():
            p.requires_grad_(False)

    def unfreeze_response(self) -> None:
        self.response.train()
        for p in self.response.parameters():
            p.requires_grad_(True)

    def save(self, path, extra=None):
        ckpt = {
            "format": "e3mu_dual_layer_v2",
            "schema_version": 2,
            "model_config": asdict(self.cfg),
            "z_table_zs": list(self.z_table_zs),
            "atomic_energies": self.ground.atomic_energies.detach().cpu(),
            "ground_state_dict": self.ground.state_dict(),
            "response_state_dict": self.response.state_dict(),
        }
        if extra:
            safe_extra = _checkpoint_safe(extra)
            ckpt["extra"] = safe_extra
            # Keep the historical top-level metadata keys readable by older
            # evaluators while new readers use the uniform ``extra`` block.
            ckpt.update(safe_extra)
        torch.save(ckpt, path)

    @classmethod
    def load(cls, path, map_location="cpu", *, allow_unsafe_legacy: bool = False):
        try:
            main_mod = sys.modules.get("__main__")
            if main_mod is not None:
                for nm in (
                    "CosineCutoff",
                    "GaussianRBF",
                    "FastEquivariantBlock",
                    "FastEquivariantCore",
                    "BackupGroundModel",
                    "BackupResponseModel",
                    "DualLayerFieldModel",
                    "AtomicNumberTable",
                    "ModelConfig",
                ):
                    if hasattr(main_mod, nm):
                        continue
                    if nm in globals():
                        setattr(main_mod, nm, globals()[nm])
        except Exception:
            pass

        try:
            obj = torch.load(path, map_location=map_location, weights_only=True)
        except Exception as exc:
            if not allow_unsafe_legacy:
                raise ValueError(
                    "Checkpoint is not weights-only compatible. For a trusted legacy local "
                    "checkpoint, reload with allow_unsafe_legacy=True and save it again."
                ) from exc
            obj = torch.load(path, map_location=map_location, weights_only=False)

        def _finalize_loaded_model(model: "DualLayerFieldModel") -> "DualLayerFieldModel":
            """Attach non-persistent checkpoint provenance used by inference tools."""
            metadata: Dict[str, Any] = {}
            checkpoint_format = "legacy_module"
            schema_version = 0
            if isinstance(obj, dict):
                checkpoint_format = str(obj.get("format", "state_dict_bundle"))
                try:
                    schema_version = int(obj.get("schema_version", 0) or 0)
                except (TypeError, ValueError):
                    schema_version = 0
                extra = obj.get("extra")
                if isinstance(extra, dict):
                    metadata.update(extra)
                # Older dual-layer checkpoints stored these fields at top level.
                for key in (
                    "training_mode",
                    "recommended_inference_mode",
                    "loss_weights",
                    "best_epoch",
                    "best_val_loss",
                    "validation_score",
                    "split",
                ):
                    if key in obj and key not in metadata:
                        metadata[key] = obj[key]
            model.checkpoint_format = checkpoint_format
            model.checkpoint_schema_version = schema_version
            model.checkpoint_metadata = metadata
            model.checkpoint_path = str(Path(path).expanduser().resolve())
            return model

        if isinstance(obj, dict) and obj.get("format") == "e3mu_mixed_granularity_v1":
            cfg_values = {
                k: v for k, v in obj["model_config"].items()
                if k in ModelConfig.__dataclass_fields__
            }
            cfg = ModelConfig(**cfg_values)
            z_table = AtomicNumberTable(obj["z_table_zs"])
            ae = torch.as_tensor(obj["atomic_energies"]).detach().cpu().numpy().reshape(-1)
            model = MixedGranularityE3GNN(
                z_table=z_table, atomic_energies_1d=ae, cfg=cfg
            )
            model.load_state_dict(obj["state_dict"], strict=True)
            return _finalize_loaded_model(model)

        # 1) Native checkpoint dict (preferred)
        if isinstance(obj, dict) and obj.get("format") in ("e3mu_dual_layer", "e3mu_dual_layer_v2"):
            _mc = {k: v for k, v in obj["model_config"].items()
                   if k in ModelConfig.__dataclass_fields__}
            cfg = ModelConfig(**_mc)
            z_table = AtomicNumberTable(obj["z_table_zs"])
            ae = np.asarray(torch.as_tensor(obj["atomic_energies"]).cpu(), dtype=float).reshape(-1)
            model = cls(z_table=z_table, atomic_energies_1d=ae, cfg=cfg)
            model.ground.load_state_dict(obj["ground_state_dict"])
            model.response.load_state_dict(obj["response_state_dict"])
            return _finalize_loaded_model(model)

        # 2) Backup .pth fallback: state_dict bundle
        if isinstance(obj, dict) and ("state_dict" in obj):
            sd = obj.get("state_dict", None)
            if not isinstance(sd, dict):
                raise ValueError("Invalid state_dict bundle (state_dict must be a dict).")
            cfg_d = obj.get("model_config", None)
            cfg_values = (
                {
                    key: value
                    for key, value in cfg_d.items()
                    if key in ModelConfig.__dataclass_fields__
                }
                if isinstance(cfg_d, dict)
                else {}
            )
            cfg = ModelConfig(**cfg_values)
            zs = obj.get("z_table_zs", None)
            if not isinstance(zs, (list, tuple)) or not zs:
                raise ValueError("state_dict bundle missing z_table_zs; cannot reconstruct model.")
            if sd and all(str(name).startswith("module.") for name in sd):
                sd = {str(name)[7:]: value for name, value in sd.items()}
            ae_t = sd.get("ground.atomic_energies", obj.get("atomic_energies"))
            if ae_t is None:
                raise ValueError("state_dict bundle missing ground.atomic_energies; cannot reconstruct model.")
            ae = np.asarray(torch.as_tensor(ae_t).detach().cpu().numpy(), dtype=float).reshape(-1)
            mixed_state_prefixes = (
                "qeq.", "polarization_solver.", "d4.", "spin_layer."
            )
            model_class = (
                MixedGranularityE3GNN
                if _model_uses_mixed_granularity(cfg)
                or any(str(name).startswith(mixed_state_prefixes) for name in sd)
                else cls
            )
            model = model_class(
                z_table=AtomicNumberTable(zs), atomic_energies_1d=ae, cfg=cfg
            )
            model.load_state_dict(sd, strict=False)
            return _finalize_loaded_model(model)

        # 3) Pickled full model object (.pth): return directly
        if isinstance(obj, cls):
            return _finalize_loaded_model(obj)
        if isinstance(obj, torch.nn.Module) and hasattr(obj, "ground") and hasattr(obj, "response"):
            return _finalize_loaded_model(obj)

        raise ValueError(f"Unrecognized model file format: {path}")

    def forward(
        self,
        batch,
        *,
        training: Optional[bool] = None,
        compute_forces: bool = True,
        compute_bec: bool = False,
        use_response_terms: bool = True,
        retain_graph: bool = False,
        use_response: Optional[bool] = None,
    ):
        """Assemble the effective Hamiltonian and derive observables.

        Workflow:
            1. Predict the field-free energy ``E_PES`` from the ground branch.
            2. Predict partial charges, atomic dipoles, and polarizability from
               the response branch.
            3. Build the field-dependent correction
               ``E_resp = -mu.E - 0.5 E^T alpha E``.
            4. Differentiate the total energy to obtain conservative forces.

        Returns:
            Dictionary containing total energy, forces, dipole, and
            polarizability for each graph in the batch.
        """
        if training is None:
            training = bool(self.training)
        if use_response is not None:
            use_response_terms = bool(use_response)

        if compute_forces or compute_bec:
            batch.positions.requires_grad_(True)
        
        # Zeroth-order ground-state potential energy term.
        e_pes, _ = self.ground(batch)
        num_graphs = int(batch.ptr.numel() - 1)
        mu = torch.zeros((num_graphs, 3), dtype=batch.positions.dtype, device=batch.positions.device)
        alpha = torch.zeros((num_graphs, 3, 3), dtype=batch.positions.dtype, device=batch.positions.device)

        if use_response_terms:
            q, atomic_dipoles, alpha = self.response(batch)
            
            # Enforce graph-wise charge neutrality before computing the charge dipole.
            if hasattr(batch, "total_charge"):
                Q = batch.total_charge.view(-1)
                if Q.numel() == 1 and num_graphs > 1: Q = Q.expand(num_graphs)
            else:
                Q = torch.zeros((num_graphs,), dtype=q.dtype, device=q.device)
            
            n_atoms_g = scatter_sum(torch.ones_like(q), batch.batch, dim_size=num_graphs)
            q_sum_g = scatter_sum(q, batch.batch, dim_size=num_graphs)
            corr = (q_sum_g - Q) / n_atoms_g.clamp(min=1.0)
            q = q - corr[batch.batch]

            # Total dipole = atomic dipoles + charge-displacement contribution.
            mu_atomic = scatter_sum(atomic_dipoles, batch.batch, dim_size=num_graphs)
            center = scatter_mean(batch.positions, batch.batch, dim_size=num_graphs)
            rel = minimal_image_relative_positions(positions=batch.positions, center=center, batch=batch.batch, cell=batch.cell, pbc=getattr(batch, "pbc", None), num_graphs=num_graphs)
            mu_charge = scatter_sum(rel * q.unsqueeze(-1), batch.batch, dim_size=num_graphs)
            mu = mu_atomic + mu_charge

        field = batch.field if hasattr(batch, "field") else torch.zeros((num_graphs, 3), dtype=batch.positions.dtype, device=batch.positions.device)
        field = field * float(self.cfg.field_scale)

        if use_response_terms:
            # Field-induced response energy from dipole and polarizability terms.
            alpha_factor = (
                ALPHA_VOLUME_TO_EV_PER_FIELD2
                if str(getattr(self.cfg, "polarizability_unit", "angstrom3")).lower() == "angstrom3"
                else 1.0
            )
            e_resp = -(mu * field).sum(dim=-1) - 0.5 * alpha_factor * torch.einsum(
                "bi,bij,bj->b", field, alpha, field
            )
        else:
            e_resp = torch.zeros_like(e_pes)

        e_total = e_pes + e_resp

        bec = torch.zeros(
            (batch.positions.shape[0], 3, 3),
            dtype=batch.positions.dtype,
            device=batch.positions.device,
        )
        if compute_bec and use_response_terms and mu.requires_grad:
            bec_rows: List[torch.Tensor] = []
            for component in range(3):
                derivative = torch.autograd.grad(
                    mu[:, component].sum(),
                    batch.positions,
                    create_graph=bool(training),
                    retain_graph=True,
                    allow_unused=True,
                )[0]
                bec_rows.append(derivative if derivative is not None else torch.zeros_like(batch.positions))
            bec = torch.stack(bec_rows, dim=1)
        
        if compute_forces:
            # Forces are derived directly from the total energy to preserve consistency.
            forces = -torch.autograd.grad(
                [e_total.sum()],
                [batch.positions],
                create_graph=bool(training),
                retain_graph=bool(retain_graph),
            )[0]
        else:
            forces = torch.zeros_like(batch.positions)
        return {
            "energy": e_total,
            "forces": forces,
            "dipole": mu,
            "polarizability": alpha,
            "bec": bec,
        }


def _checkpoint_safe(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return torch.as_tensor(value)
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): _checkpoint_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_checkpoint_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool, type(None), torch.Tensor)):
        return value
    return str(value)


def _model_uses_mixed_granularity(cfg: ModelConfig) -> bool:
    return any(
        bool(getattr(cfg, name, False))
        for name in (
            "enable_qeq", "enable_pme", "enable_deq", "enable_d4",
            "enable_spin", "enable_film",
        )
    )


def _copy_matching_pretrained_weights(
    target: torch.nn.Module,
    source: torch.nn.Module,
    *,
    source_elements: Sequence[int],
    target_elements: Sequence[int],
    source_cfg: Optional[ModelConfig] = None,
    target_cfg: Optional[ModelConfig] = None,
) -> Dict[str, Any]:
    """Warm-start compatible tensors, remapping element-indexed rows exactly."""
    target_state = target.state_dict()
    source_state = source.state_dict()
    source_index = {int(z): index for index, z in enumerate(source_elements)}
    target_index = {int(z): index for index, z in enumerate(target_elements)}
    shared_elements = sorted(set(source_index) & set(target_index))
    element_keys = {
        "ground.atomic_energies",
        "ground.core.embed.weight",
        "response.core.embed.weight",
    }
    loaded: List[str] = []
    remapped: List[str] = []
    skipped: Dict[str, str] = {}
    loaded_numel = 0
    loaded_ground_trainable_numel = 0
    target_parameters = dict(target.named_parameters())
    radial_settings_match = bool(
        source_cfg is not None
        and target_cfg is not None
        and str(source_cfg.rbf_type) == str(target_cfg.rbf_type)
        and float(source_cfg.r_max) == float(target_cfg.r_max)
        and int(source_cfg.num_radial_basis) == int(target_cfg.num_radial_basis)
    )
    for name, target_value in target_state.items():
        source_value = source_state.get(name)
        if source_value is None:
            skipped[name] = "missing from checkpoint"
            continue
        if name == "d4.type_zs":
            skipped[name] = "kept target element table"
            continue
        if not radial_settings_match and ".core.rbf." in name:
            skipped[name] = "kept target radial-basis geometry"
            continue
        if name in element_keys:
            if name.endswith("embed.weight"):
                if (
                    source_value.ndim != 2
                    or target_value.ndim != 2
                    or source_value.shape[0] != target_value.shape[0]
                ):
                    skipped[name] = (
                        f"incompatible shape {tuple(source_value.shape)} -> "
                        f"{tuple(target_value.shape)}"
                    )
                    continue
                copied = target_value.clone()
                for atomic_number in shared_elements:
                    copied[:, target_index[atomic_number]] = source_value[
                        :, source_index[atomic_number]
                    ].to(dtype=copied.dtype)
            else:
                if source_value.ndim != 1 or target_value.ndim != 1:
                    skipped[name] = "invalid atomic-reference shape"
                    continue
                copied = target_value.clone()
                for atomic_number in shared_elements:
                    copied[target_index[atomic_number]] = source_value[
                        source_index[atomic_number]
                    ].to(dtype=copied.dtype)
            target_state[name] = copied
            loaded.append(name)
            remapped.append(name)
            copied_entries = (
                len(shared_elements) * int(copied.shape[0])
                if name.endswith("embed.weight")
                else len(shared_elements)
            )
            loaded_numel += copied_entries
            if name.startswith("ground.") and name in target_parameters:
                loaded_ground_trainable_numel += copied_entries
            continue
        if source_value.shape != target_value.shape:
            skipped[name] = (
                f"incompatible shape {tuple(source_value.shape)} -> "
                f"{tuple(target_value.shape)}"
            )
            continue
        target_state[name] = source_value.to(dtype=target_value.dtype)
        loaded.append(name)
        loaded_numel += int(target_value.numel())
        if name.startswith("ground.") and name in target_parameters:
            loaded_ground_trainable_numel += int(target_value.numel())
    target.load_state_dict(target_state, strict=True)
    return {
        "loaded": loaded,
        "remapped": remapped,
        "skipped": skipped,
        "shared_elements": shared_elements,
        "missing_dataset_elements": sorted(set(target_index) - set(source_index)),
        "loaded_numel": int(loaded_numel),
        "loaded_ground_trainable_numel": int(loaded_ground_trainable_numel),
    }


def _initialize_model_from_checkpoint(
    *,
    checkpoint_path: str,
    target_cfg: ModelConfig,
    target_elements: Sequence[int],
    atomic_energies: Optional[Sequence[float]] = None,
    missing_atomic_energies_factory: Optional[Callable[[], Sequence[float]]] = None,
) -> Tuple[DualLayerFieldModel, Dict[str, Any]]:
    """Construct the selected architecture and warm-start compatible weights."""
    source = DualLayerFieldModel.load(
        checkpoint_path, map_location="cpu", allow_unsafe_legacy=True
    )
    source_index = {
        int(atomic_number): index
        for index, atomic_number in enumerate(source.z_table_zs)
    }
    target_values = [int(value) for value in target_elements]
    missing_elements = sorted(set(target_values) - set(source_index))
    fitted_missing = False
    if atomic_energies is None:
        target_atomic_energies = np.zeros((len(target_values),), dtype=float)
        if missing_elements:
            if missing_atomic_energies_factory is None:
                raise ValueError(
                    "Pretrained checkpoint is missing dataset elements "
                    f"{missing_elements}; target atomic references are required"
                )
            target_atomic_energies = np.asarray(
                missing_atomic_energies_factory(), dtype=float
            ).reshape(-1)
            fitted_missing = True
    else:
        target_atomic_energies = np.asarray(atomic_energies, dtype=float).reshape(-1)
    if target_atomic_energies.size != len(target_values):
        raise ValueError(
            "Target atomic-energy table has "
            f"{target_atomic_energies.size} entries for {len(target_values)} elements"
        )
    source_atomic_energies = (
        source.ground.atomic_energies.detach().cpu().numpy().reshape(-1)
    )
    for target_index, atomic_number in enumerate(target_values):
        if atomic_number in source_index:
            target_atomic_energies[target_index] = source_atomic_energies[
                source_index[atomic_number]
            ]
    model_class = (
        MixedGranularityE3GNN
        if _model_uses_mixed_granularity(target_cfg)
        else DualLayerFieldModel
    )
    target = model_class(
        z_table=AtomicNumberTable(target_elements),
        atomic_energies_1d=target_atomic_energies,
        cfg=target_cfg,
    )
    report = _copy_matching_pretrained_weights(
        target,
        source,
        source_elements=source.z_table_zs,
        target_elements=target_elements,
        source_cfg=source.cfg,
        target_cfg=target_cfg,
    )
    if int(report["loaded_ground_trainable_numel"]) <= 0:
        raise ValueError(
            "Pretrained checkpoint has no compatible Layer-1 trainable weights. "
            "Match num_channels, parity mode, and radial basis dimensions."
        )
    report["source_architecture"] = asdict(source.cfg)
    report["target_architecture"] = asdict(target_cfg)
    report["fitted_missing_atomic_energies"] = bool(fitted_missing)
    return target, report


class MixedGranularityE3GNN(DualLayerFieldModel):
    """Atomic, domain, and spin layers coupled through scalar FiLM feedback."""

    def __init__(self, *, z_table: AtomicNumberTable, atomic_energies_1d: Any, cfg: ModelConfig):
        if cfg.enable_film and not cfg.e3mu_use_parity:
            raise ValueError("FiLM mixed-granularity mode requires parity-aware O(3)")
        if cfg.enable_spin and cfg.enable_dmi and not cfg.e3mu_use_parity:
            raise ValueError("DMI spin mode requires parity-aware O(3)")
        super().__init__(z_table=z_table, atomic_energies_1d=atomic_energies_1d, cfg=cfg)
        self.qeq = DifferentiableQEq(cfg) if (cfg.enable_qeq or cfg.enable_pme) else None
        self.polarization_solver = SelfConsistentPolarization(cfg) if cfg.enable_deq else None
        self.d4 = D4DispersionLayer(cfg, z_table.zs) if cfg.enable_d4 else None
        self.spin_layer = (
            TimeReversalSpinHamiltonian(
                hidden=int(cfg.num_channels),
                rbf_dim=int(cfg.num_radial_basis),
                spin_cutoff=float(cfg.spin_cutoff),
                enable_dmi=bool(cfg.enable_dmi),
            )
            if cfg.enable_spin else None
        )

    def freeze_response(self) -> None:
        super().freeze_response()
        if self.spin_layer is not None:
            for parameter in self.spin_layer.parameters():
                parameter.requires_grad_(False)

    def unfreeze_response(self) -> None:
        super().unfreeze_response()
        if self.spin_layer is not None:
            for parameter in self.spin_layer.parameters():
                parameter.requires_grad_(True)

    def save(self, path: str, extra: Optional[Dict[str, Any]] = None) -> None:
        checkpoint: Dict[str, Any] = {
            "format": "e3mu_mixed_granularity_v1",
            "schema_version": 1,
            "model_config": asdict(self.cfg),
            "z_table_zs": list(self.z_table_zs),
            "atomic_energies": self.ground.atomic_energies.detach().cpu(),
            "state_dict": self.state_dict(),
            # Kept so the existing ground-only TorchScript exporter remains usable.
            "ground_state_dict": self.ground.state_dict(),
            "response_state_dict": self.response.state_dict(),
        }
        if extra:
            checkpoint["extra"] = _checkpoint_safe(extra)
        torch.save(checkpoint, path)

    @classmethod
    def load(
        cls,
        path: str,
        map_location: str = "cpu",
        *,
        allow_unsafe_legacy: bool = False,
    ) -> "MixedGranularityE3GNN":
        model = DualLayerFieldModel.load(
            path,
            map_location=map_location,
            allow_unsafe_legacy=allow_unsafe_legacy,
        )
        if not isinstance(model, cls):
            raise ValueError("Checkpoint is a legacy dual-layer model, not a mixed-granularity model")
        return model

    @staticmethod
    def _neutralize(raw_q: torch.Tensor, batch: Any, total_charge: torch.Tensor) -> torch.Tensor:
        n_graphs = _batch_num_graphs(batch)
        count = scatter_sum(torch.ones_like(raw_q), batch.batch, dim_size=n_graphs)
        current = scatter_sum(raw_q, batch.batch, dim_size=n_graphs)
        return raw_q - ((current - total_charge) / count.clamp(min=1.0))[batch.batch]

    @staticmethod
    def _spin_condition(batch: Any, spins: torch.Tensor) -> torch.Tensor:
        src, dst = batch.edge_index[0], batch.edge_index[1]
        pair_dot = torch.sum(spins[src] * spins[dst], dim=-1)
        return scatter_mean(pair_dot.unsqueeze(-1), src, dim_size=int(spins.shape[0])).squeeze(-1)

    def _domain_and_spin(
        self,
        *,
        batch: Any,
        components: Dict[str, torch.Tensor],
        field: torch.Tensor,
        total_charge: torch.Tensor,
        spins: torch.Tensor,
        use_domain: bool,
        use_spin: bool,
    ) -> Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]:
        n_graphs = _batch_num_graphs(batch)
        zero_graph = torch.zeros((n_graphs,), dtype=batch.positions.dtype, device=batch.positions.device)
        if use_domain and self.qeq is not None:
            domain = self.qeq(
                chi=components["chi"],
                hardness=components["hardness"],
                batch=batch,
                total_charge=total_charge,
                field=field,
            )
        else:
            q = self._neutralize(components["raw_charges"], batch, total_charge)
            domain = {
                "charges": q,
                "potential": torch.zeros_like(q),
                "energy_local": zero_graph,
                "energy_coulomb": zero_graph,
                "residual": torch.abs(
                    scatter_sum(q, batch.batch, dim_size=n_graphs) - total_charge
                ),
                "stability_shift": zero_graph,
            }
        if use_spin and self.spin_layer is not None:
            spin = self.spin_layer(
                batch=batch,
                scalar_features=components["scalar_features"],
                polar_features=components["polar_features"],
                axial_features=components["axial_features"],
                tensor_features=components["tensor_features"],
                spins=spins,
            )
        else:
            spin = {
                "energy": zero_graph,
                "pair_index": torch.zeros((2, 0), dtype=torch.long, device=batch.positions.device),
                "Jij": torch.zeros((0,), dtype=batch.positions.dtype, device=batch.positions.device),
                "Di": torch.zeros((batch.positions.shape[0], 3, 3), dtype=batch.positions.dtype, device=batch.positions.device),
                "DMIij": torch.zeros((0, 3), dtype=batch.positions.dtype, device=batch.positions.device),
                "magnetic_moments": torch.zeros_like(spins),
            }
        return domain, spin

    def forward(
        self,
        batch: Any,
        *,
        training: Optional[bool] = None,
        compute_forces: bool = True,
        compute_bec: bool = False,
        use_response_terms: bool = True,
        retain_graph: bool = False,
        use_response: Optional[bool] = None,
        use_domain_terms: Optional[bool] = None,
        use_spin_terms: Optional[bool] = None,
    ) -> Dict[str, torch.Tensor]:
        if training is None:
            training = bool(self.training)
        if use_response is not None:
            use_response_terms = bool(use_response)
        use_domain = bool(use_response_terms and (self.cfg.enable_qeq or self.cfg.enable_pme))
        use_spin = bool(use_response_terms and self.cfg.enable_spin)
        if use_domain_terms is not None:
            use_domain = bool(use_domain_terms)
        if use_spin_terms is not None:
            use_spin = bool(use_spin_terms)
        if (compute_forces or compute_bec) and not batch.positions.requires_grad:
            batch.positions.requires_grad_(True)

        n_graphs = _batch_num_graphs(batch)
        field = _batch_field(batch, n_graphs) * float(self.cfg.field_scale)
        total_charge = _batch_total_charge(batch, n_graphs, batch.positions.dtype)
        spin_value = getattr(batch, "spins", None)
        if spin_value is None:
            spins = torch.zeros_like(batch.positions, requires_grad=use_spin)
        else:
            spins = torch.as_tensor(spin_value, dtype=batch.positions.dtype, device=batch.positions.device)
            if use_spin and not spins.requires_grad:
                spins = spins.clone().requires_grad_(True)

        if self.cfg.enable_film:
            batch.film_condition = torch.zeros(
                (batch.positions.shape[0], 4), dtype=batch.positions.dtype, device=batch.positions.device
            )
        e_pes, _ = self.ground(batch)
        components = self.response.forward_components(batch)
        domain, spin = self._domain_and_spin(
            batch=batch,
            components=components,
            field=field,
            total_charge=total_charge,
            spins=spins,
            use_domain=use_domain,
            use_spin=use_spin,
        )

        coupling_residual = torch.zeros((n_graphs,), dtype=field.dtype, device=field.device)
        if self.cfg.enable_film and use_response_terms:
            previous_q = domain["charges"]
            n_steps = max(1, int(self.cfg.coupling_iterations))
            for _ in range(n_steps):
                q_cond = torch.tanh(previous_q)
                potential_cond = torch.tanh(domain["potential"] / 10.0)
                spin_norm2 = _smooth_scalar_bound(
                    torch.sum(spins * spins, dim=-1), max_abs=4.0
                )
                spin_pair = _smooth_scalar_bound(
                    self._spin_condition(batch, spins), max_abs=4.0
                )
                batch.film_condition = torch.stack(
                    [q_cond, potential_cond, spin_norm2, spin_pair], dim=-1
                )
                e_pes, _ = self.ground(batch)
                components = self.response.forward_components(batch)
                domain, spin = self._domain_and_spin(
                    batch=batch,
                    components=components,
                    field=field,
                    total_charge=total_charge,
                    spins=spins,
                    use_domain=use_domain,
                    use_spin=use_spin,
                )
                q_delta = torch.abs(domain["charges"] - previous_q)
                coupling_residual = scatter_mean(q_delta, batch.batch, dim_size=n_graphs)
                # Under-relax the feedback state to prevent charge/FiLM
                # oscillations while retaining the converged physical output.
                previous_q = 0.5 * previous_q + 0.5 * domain["charges"]
                if float(torch.max(coupling_residual).detach().cpu()) <= float(self.cfg.coupling_tol):
                    break

        charges = domain["charges"]
        atomic_dipoles = components["atomic_dipoles"]
        atomic_alpha = components["atomic_polarizability"]
        alpha = components["polarizability"]
        zero_graph = torch.zeros((n_graphs,), dtype=field.dtype, device=field.device)

        if use_response_terms and self.polarization_solver is not None:
            polarization = self.polarization_solver(
                atomic_alpha=atomic_alpha,
                charges=charges,
                permanent_dipoles=atomic_dipoles,
                batch=batch,
                field=field,
            )
        else:
            polarization = {
                "induced_dipoles": torch.zeros_like(batch.positions),
                "energy": zero_graph,
                "residual": zero_graph,
                "iterations": zero_graph,
                "stability_shift": zero_graph,
            }
        induced = polarization["induced_dipoles"]

        center = scatter_mean(batch.positions, batch.batch, dim_size=n_graphs)
        rel = minimal_image_relative_positions(
            positions=batch.positions,
            center=center,
            batch=batch.batch,
            cell=batch.cell,
            pbc=getattr(batch, "pbc", None),
            num_graphs=n_graphs,
        )
        mu_permanent = scatter_sum(atomic_dipoles, batch.batch, dim_size=n_graphs)
        mu_charge = scatter_sum(rel * charges.unsqueeze(-1), batch.batch, dim_size=n_graphs)
        mu_induced = scatter_sum(induced, batch.batch, dim_size=n_graphs)
        mu = mu_permanent + mu_charge + mu_induced

        bec = torch.zeros(
            (batch.positions.shape[0], 3, 3),
            dtype=batch.positions.dtype,
            device=batch.positions.device,
        )
        if compute_bec and use_response_terms and mu.requires_grad:
            bec_rows: List[torch.Tensor] = []
            for component in range(3):
                derivative = torch.autograd.grad(
                    mu[:, component].sum(),
                    batch.positions,
                    create_graph=bool(training),
                    retain_graph=True,
                    allow_unused=True,
                )[0]
                bec_rows.append(derivative if derivative is not None else torch.zeros_like(batch.positions))
            bec = torch.stack(bec_rows, dim=1)

        e_response = zero_graph
        if use_response_terms:
            e_response = -torch.sum(mu_permanent * field, dim=-1)
            if self.qeq is None or not use_domain:
                e_response = e_response - torch.sum(mu_charge * field, dim=-1)
            if self.polarization_solver is not None:
                e_response = e_response + polarization["energy"]
            else:
                e_response = e_response - 0.5 * ALPHA_VOLUME_TO_EV_PER_FIELD2 * torch.einsum(
                    "bi,bij,bj->b", field, alpha, field
                )

        if use_response_terms and self.d4 is not None:
            d4 = self.d4(
                batch=batch,
                charges=charges,
                c6_scale=components.get("c6_scale"),
            )
        else:
            d4 = {
                "energy": zero_graph,
                "atomic_c6": torch.zeros_like(charges),
                "atomic_polarizability": torch.zeros_like(charges),
            }

        e_qeq = domain["energy_local"] if use_domain else zero_graph
        e_pme = domain["energy_coulomb"] if use_domain else zero_graph
        e_spin = spin["energy"] if use_spin else zero_graph
        e_total = e_pes + e_qeq + e_pme + d4["energy"] + e_spin + e_response

        pair_index = spin["pair_index"]
        if pair_index.shape[1] > 0:
            pair_graph = batch.batch[pair_index[0]]
            j_effective = scatter_mean(spin["Jij"], pair_graph, dim_size=n_graphs)
            dmi_effective = scatter_mean(spin["DMIij"], pair_graph, dim_size=n_graphs)
        else:
            j_effective = zero_graph
            dmi_effective = torch.zeros((n_graphs, 3), dtype=field.dtype, device=field.device)
        di_effective = scatter_mean(spin["Di"], batch.batch, dim_size=n_graphs)

        if use_spin:
            spin_grad = torch.autograd.grad(
                e_spin.sum(),
                spins,
                create_graph=bool(training),
                retain_graph=True,
                allow_unused=True,
            )[0]
            effective_field = -spin_grad if spin_grad is not None else torch.zeros_like(spins)
        else:
            effective_field = torch.zeros_like(spins)

        if compute_forces:
            grad_pos = torch.autograd.grad(
                e_total.sum(),
                batch.positions,
                create_graph=bool(training),
                retain_graph=bool(retain_graph or training),
            )[0]
            forces = -grad_pos
        else:
            forces = torch.zeros_like(batch.positions)

        return {
            "energy": e_total,
            "forces": forces,
            "energy_short": e_pes,
            "energy_qeq": e_qeq,
            "energy_pme": e_pme,
            "energy_d4": d4["energy"],
            "energy_spin": e_spin,
            "energy_response": e_response,
            "charges": charges,
            "dipole": mu,
            "polarizability": alpha,
            "atomic_dipoles": atomic_dipoles,
            "induced_dipoles": induced,
            "atomic_polarizability": atomic_alpha,
            "c6": d4["atomic_c6"],
            "bec": bec,
            "Jij": spin["Jij"],
            "Di": spin["Di"],
            "DMIij": spin["DMIij"],
            "spin_pair_index": spin["pair_index"],
            "J_effective": j_effective,
            "Di_effective": di_effective,
            "DMI_effective": dmi_effective,
            "magnetic_moments": spin["magnetic_moments"],
            "effective_field": effective_field,
            "qeq_residual": domain["residual"],
            "qeq_stability_shift": domain["stability_shift"],
            "deq_residual": polarization["residual"],
            "deq_iterations": polarization["iterations"],
            "deq_stability_shift": polarization["stability_shift"],
            "coupling_residual": coupling_residual,
        }

# ══════════════════════════════════════════════════════════════════════════
# SECTION: TorchScript Export
# TorchScript-friendly wrappers for exporting the ground-state model in a
# SevenNet-compatible format.
# ══════════════════════════════════════════════════════════════════════════

# SO(3) TorchScript core with multi-RBF support.
# ``@torch.jit.interface`` is avoided here because older PyTorch versions do
# not handle it reliably in class-body annotations.
class _FastEquivariantCoreTS(torch.nn.Module):
    def __init__(self, num_elements: int, hidden: int, num_layers: int, rbf_dim: int,
                 r_max: float, rbf_type: str):
        super().__init__()
        self.num_elements = int(num_elements)
        self.hidden = int(hidden)
        self.r_max = float(r_max)
        self.embed = torch.nn.Linear(self.num_elements, self.hidden, bias=False)
        _rdim = int(rbf_dim); _rmax = float(r_max)
        self.rbf_gaussian   = GaussianRBF(_rdim, _rmax)
        self.rbf_bessel     = BesselRBF(_rdim, _rmax)
        self.rbf_trainable  = TrainableGaussianRBF(_rdim, _rmax)
        if rbf_type == "bessel":
            self.rbf_mode = 1
        elif rbf_type == "trainable_gaussian":
            self.rbf_mode = 2
        else:
            self.rbf_mode = 0
        self.cutoff = CosineCutoff(self.r_max)
        self.layers = torch.nn.ModuleList(
            [FastEquivariantBlock(self.hidden, int(rbf_dim)) for _ in range(int(num_layers))]
        )

    def _rbf(self, r: torch.Tensor) -> torch.Tensor:
        if self.rbf_mode == 1:
            return self.rbf_bessel(r)
        elif self.rbf_mode == 2:
            return self.rbf_trainable(r)
        return self.rbf_gaussian(r)

    def forward(self, *, positions: torch.Tensor, edge_index: torch.Tensor,
                shifts: torch.Tensor, atom_types: torch.Tensor) -> torch.Tensor:
        src = edge_index[0]; dst = edge_index[1]
        edge_vec = positions[dst] + shifts - positions[src]
        r = torch.linalg.norm(edge_vec, dim=-1).clamp(min=1e-12)
        rbf = self._rbf(r); cutoff = self.cutoff(r)
        w = self.embed.weight.transpose(0, 1)
        s = torch.nn.functional.embedding(atom_types.view(-1).to(torch.long), w)
        n = int(positions.shape[0])
        v = torch.zeros((n, self.hidden, 3), dtype=positions.dtype, device=positions.device)
        t = torch.zeros((n, self.hidden, 5), dtype=positions.dtype, device=positions.device)
        for layer in self.layers:
            s, v, t = layer(s=s, v=v, t=t, edge_index=edge_index, edge_vec=edge_vec,
                            r=r, rbf=rbf, cutoff=cutoff, num_nodes=n)
        return s


# O(3) TorchScript core with parity-aware channels and multi-RBF support.
class _FastEquivariantCoreO3TS(torch.nn.Module):
    def __init__(self, num_elements: int, hidden: int, num_layers: int, rbf_dim: int,
                 r_max: float, use_l3: bool, rbf_type: str,
                 type_zs: Sequence[int], enable_continuous_chem: bool,
                 chem_max_z: int, enable_film: bool):
        super().__init__()
        self.num_elements = int(num_elements)
        self.hidden = int(hidden)
        self.r_max = float(r_max)
        self.use_l3 = bool(use_l3)
        self.enable_continuous_chem = bool(enable_continuous_chem)
        self.enable_film = bool(enable_film)
        self.embed = torch.nn.Linear(self.num_elements, self.hidden, bias=False)
        self.register_buffer(
            "type_zs",
            torch.tensor([int(z) for z in type_zs], dtype=torch.long),
            persistent=False,
        )
        _rdim = int(rbf_dim); _rmax = float(r_max)
        self.rbf_gaussian   = GaussianRBF(_rdim, _rmax)
        self.rbf_bessel     = BesselRBF(_rdim, _rmax)
        self.rbf_trainable  = TrainableGaussianRBF(_rdim, _rmax)
        self.element_encoder = PeriodicTableEmbedder(
            embedding_dim=self.hidden,
            max_z=int(chem_max_z),
            aug_prob=0.0,
            aug_noise_std=0.0,
            aug_mix_max=0.0,
        )
        if rbf_type == "bessel":
            self.rbf_mode = 1
        elif rbf_type == "trainable_gaussian":
            self.rbf_mode = 2
        else:
            self.rbf_mode = 0
        self.cutoff = CosineCutoff(self.r_max)
        self.layers = torch.nn.ModuleList(
            [FastEquivariantBlockO3(self.hidden, int(rbf_dim), use_l3=self.use_l3)
             for _ in range(int(num_layers))]
        )
        # Always materialize one FiLM layer per interaction so TorchScript can
        # iterate over paired ModuleLists. The branch is constant-folded when
        # FiLM is disabled, and missing weights are allowed by the exporter.
        self.film_layers = torch.nn.ModuleList(
            [torch.nn.Linear(4, 3 * self.hidden) for _ in range(int(num_layers))]
        )

    def _rbf(self, r: torch.Tensor) -> torch.Tensor:
        if self.rbf_mode == 1:
            return self.rbf_bessel(r)
        elif self.rbf_mode == 2:
            return self.rbf_trainable(r)
        return self.rbf_gaussian(r)

    def forward(self, *, positions: torch.Tensor, edge_index: torch.Tensor,
                shifts: torch.Tensor, atom_types: torch.Tensor) -> torch.Tensor:
        src = edge_index[0]; dst = edge_index[1]
        edge_vec = positions[dst] + shifts - positions[src]
        r = torch.linalg.norm(edge_vec, dim=-1).clamp(min=1e-12)
        rbf = self._rbf(r); cutoff = self.cutoff(r)
        atom_types = atom_types.view(-1).to(torch.long)
        if self.enable_continuous_chem:
            idx = torch.clamp(atom_types, 0, self.type_zs.numel() - 1)
            s = self.element_encoder(self.type_zs[idx])
        else:
            w = self.embed.weight.transpose(0, 1)
            s = torch.nn.functional.embedding(atom_types, w)
        n = int(positions.shape[0])
        v  = torch.zeros((n, self.hidden, 3), dtype=positions.dtype, device=positions.device)
        a  = torch.zeros((n, self.hidden, 3), dtype=positions.dtype, device=positions.device)
        t2 = torch.zeros((n, self.hidden, 5), dtype=positions.dtype, device=positions.device)
        t3 = torch.zeros((n, self.hidden, 7), dtype=positions.dtype, device=positions.device)
        film_condition = torch.zeros((n, 4), dtype=positions.dtype, device=positions.device)
        for layer, film_layer in zip(self.layers, self.film_layers):
            if self.enable_film:
                gamma_s, beta_s, gamma_tensor = torch.chunk(
                    film_layer(film_condition), 3, dim=-1
                )
                gamma_s = 0.25 * torch.tanh(gamma_s)
                beta_s = _smooth_scalar_bound(beta_s, max_abs=5.0)
                gamma_tensor = 0.25 * torch.tanh(gamma_tensor)
                s = s * (1.0 + gamma_s) + beta_s
                gate = (1.0 + gamma_tensor).unsqueeze(-1)
                v = v * gate
                a = a * gate
                t2 = t2 * gate
                t3 = t3 * gate
            s, v, a, t2, t3 = layer(s=s, v=v, a=a, t2=t2, t3=t3, edge_index=edge_index,
                                     edge_vec=edge_vec, r=r, rbf=rbf, cutoff=cutoff, num_nodes=n)
        return s


# SO(3) ground-model wrapper used during SevenNet export.
class _E3MUGroundModelSO3TS(torch.nn.Module):
    def __init__(self, num_elements: int, atomic_energies_1d: Any, cfg: ModelConfig):
        super().__init__()
        self.core = _FastEquivariantCoreTS(
            num_elements=int(num_elements), hidden=int(cfg.num_channels),
            num_layers=int(cfg.num_interactions), rbf_dim=int(cfg.num_radial_basis),
            r_max=float(cfg.r_max), rbf_type=str(getattr(cfg, "rbf_type", "gaussian")),
        )
        self.energy_head = torch.nn.Sequential(
            torch.nn.Linear(int(cfg.num_channels), int(cfg.num_channels)),
            torch.nn.SiLU(),
            torch.nn.Linear(int(cfg.num_channels), 1),
        )
        self.register_buffer(
            "atomic_energies",
            torch.tensor(np.asarray(atomic_energies_1d, dtype=float).reshape(-1),
                         dtype=torch.get_default_dtype()),
        )

    def forward(self, *, positions: torch.Tensor, edge_index: torch.Tensor,
                shifts: torch.Tensor, atom_types: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        s = self.core(positions=positions, edge_index=edge_index, shifts=shifts, atom_types=atom_types)
        e_atom = self.energy_head(s).squeeze(-1)
        e_atom = e_atom + self.atomic_energies[atom_types.view(-1).to(torch.long)]
        return torch.sum(e_atom), e_atom


# Preserve the legacy class name for backward compatibility.
_E3MUGroundModelTS = _E3MUGroundModelSO3TS


# O(3) ground-model wrapper used during SevenNet export.
class _E3MUGroundModelO3TS(torch.nn.Module):
    def __init__(self, num_elements: int, atomic_energies_1d: Any, cfg: ModelConfig):
        super().__init__()
        self.core = _FastEquivariantCoreO3TS(
            num_elements=int(num_elements), hidden=int(cfg.num_channels),
            num_layers=int(cfg.num_interactions), rbf_dim=int(cfg.num_radial_basis),
            r_max=float(cfg.r_max),
            use_l3=bool(getattr(cfg, "e3mu_use_l3", False)),
            rbf_type=str(getattr(cfg, "rbf_type", "gaussian")),
            type_zs=list(range(1, int(num_elements) + 1)),
            enable_continuous_chem=bool(getattr(cfg, "enable_continuous_chem", False)),
            chem_max_z=int(getattr(cfg, "chem_max_z", 96)),
            enable_film=bool(getattr(cfg, "enable_film", False)),
        )
        self.energy_head = torch.nn.Sequential(
            torch.nn.Linear(int(cfg.num_channels), int(cfg.num_channels)),
            torch.nn.SiLU(),
            torch.nn.Linear(int(cfg.num_channels), 1),
        )
        self.register_buffer(
            "atomic_energies",
            torch.tensor(np.asarray(atomic_energies_1d, dtype=float).reshape(-1),
                         dtype=torch.get_default_dtype()),
        )

    def forward(self, *, positions: torch.Tensor, edge_index: torch.Tensor,
                shifts: torch.Tensor, atom_types: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        s = self.core(positions=positions, edge_index=edge_index, shifts=shifts, atom_types=atom_types)
        e_atom = self.energy_head(s).squeeze(-1)
        e_atom = e_atom + self.atomic_energies[atom_types.view(-1).to(torch.long)]
        return torch.sum(e_atom), e_atom


# Thin wrappers matching the SevenNet inference contract.
def _sevennet_forward_so3(ground: _E3MUGroundModelSO3TS,
                           data: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
    pos = data["pos"]
    if not pos.requires_grad:
        pos = pos.clone().requires_grad_(True)
    edge_index = data["edge_index"].to(torch.long)
    shift = data["pbc_shift"].to(dtype=pos.dtype)
    cell = data["cell_lattice_vectors"].to(dtype=pos.dtype)
    if cell.ndim == 3:
        cell = cell[0]
    shifts_cart = torch.matmul(shift, cell)
    atom_types = data["x"].view(-1).to(torch.long)
    e_total, e_atom = ground(positions=pos, edge_index=edge_index,
                              shifts=shifts_cart, atom_types=atom_types)
    grad_opt = torch.autograd.grad([e_total], [pos], create_graph=False, allow_unused=True)[0]
    if grad_opt is None:
        grad = torch.zeros_like(pos)
    else:
        grad = grad_opt
    return {
        "inferred_total_energy": e_total,
        "atomic_energy": e_atom,
        "inferred_force": -grad,
        "inferred_stress": torch.zeros(6, dtype=pos.dtype, device=pos.device),
        "edge_index": edge_index,
        "num_atoms": data["num_atoms"],
    }


class E3MUAsSevenNetTorchScriptModel(torch.nn.Module):
    """SevenNet-compatible wrapper for SO(3) ground model."""
    def __init__(self, ground: _E3MUGroundModelSO3TS):
        super().__init__()
        self.ground = ground

    def forward(self, data: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        pos = data["pos"]
        if not pos.requires_grad:
            pos = pos.clone().requires_grad_(True)
        edge_index = data["edge_index"].to(torch.long)
        shift = data["pbc_shift"].to(dtype=pos.dtype)
        cell = data["cell_lattice_vectors"].to(dtype=pos.dtype)
        if cell.ndim == 3:
            cell = cell[0]
        shifts_cart = torch.matmul(shift, cell)
        atom_types = data["x"].view(-1).to(torch.long)
        e_total, e_atom = self.ground(positions=pos, edge_index=edge_index,
                                       shifts=shifts_cart, atom_types=atom_types)
        grad_opt = torch.autograd.grad([e_total], [pos], create_graph=False, allow_unused=True)[0]
        if grad_opt is None:
            grad = torch.zeros_like(pos)
        else:
            grad = grad_opt
        return {
            "inferred_total_energy": e_total,
            "atomic_energy": e_atom,
            "inferred_force": -grad,
            "inferred_stress": torch.zeros(6, dtype=pos.dtype, device=pos.device),
            "edge_index": edge_index,
            "num_atoms": data["num_atoms"],
        }


class E3MUAsSevenNetTorchScriptModelO3(torch.nn.Module):
    """SevenNet-compatible wrapper for O(3) ground model."""
    def __init__(self, ground: _E3MUGroundModelO3TS):
        super().__init__()
        self.ground = ground

    def forward(self, data: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        pos = data["pos"]
        if not pos.requires_grad:
            pos = pos.clone().requires_grad_(True)
        edge_index = data["edge_index"].to(torch.long)
        shift = data["pbc_shift"].to(dtype=pos.dtype)
        cell = data["cell_lattice_vectors"].to(dtype=pos.dtype)
        if cell.ndim == 3:
            cell = cell[0]
        shifts_cart = torch.matmul(shift, cell)
        atom_types = data["x"].view(-1).to(torch.long)
        e_total, e_atom = self.ground(positions=pos, edge_index=edge_index,
                                       shifts=shifts_cart, atom_types=atom_types)
        grad_opt = torch.autograd.grad([e_total], [pos], create_graph=False, allow_unused=True)[0]
        if grad_opt is None:
            grad = torch.zeros_like(pos)
        else:
            grad = grad_opt
        return {
            "inferred_total_energy": e_total,
            "atomic_energy": e_atom,
            "inferred_force": -grad,
            "inferred_stress": torch.zeros(6, dtype=pos.dtype, device=pos.device),
            "edge_index": edge_index,
            "num_atoms": data["num_atoms"],
        }


def export_sevennet_torchscript(ckpt_path: str, log: Callable) -> None:
    def _remap_rbf_state_dict(sd: Dict[str, Any], rbf_type: str) -> Dict[str, Any]:
        target = (
            "rbf_bessel" if rbf_type == "bessel"
            else "rbf_trainable" if rbf_type == "trainable_gaussian"
            else "rbf_gaussian"
        )
        return {
            (k.replace("core.rbf.", f"core.{target}.", 1) if k.startswith("core.rbf.") else k): v
            for k, v in sd.items()
        }

    def _load_export_state_dict(ground: torch.nn.Module, sd: Dict[str, Any], cfg_obj: ModelConfig) -> None:
        mapped = _remap_rbf_state_dict(sd, str(getattr(cfg_obj, "rbf_type", "gaussian")))
        incompat = ground.load_state_dict(mapped, strict=False)

        active_rbf = (
            "rbf_bessel" if getattr(cfg_obj, "rbf_type", "gaussian") == "bessel"
            else "rbf_trainable" if getattr(cfg_obj, "rbf_type", "gaussian") == "trainable_gaussian"
            else "rbf_gaussian"
        )
        inactive_rbf_prefixes = [
            f"core.{name}."
            for name in ("rbf_gaussian", "rbf_bessel", "rbf_trainable")
            if name != active_rbf
        ]
        allowed_missing_prefixes = list(inactive_rbf_prefixes)
        if not bool(getattr(cfg_obj, "enable_continuous_chem", False)):
            allowed_missing_prefixes.append("core.element_encoder.")
        if not bool(getattr(cfg_obj, "enable_film", False)):
            allowed_missing_prefixes.append("core.film_layers.")

        remaining_missing = [
            k for k in incompat.missing_keys
            if not any(k.startswith(prefix) for prefix in allowed_missing_prefixes)
        ]
        remaining_unexpected = list(incompat.unexpected_keys)
        if remaining_missing or remaining_unexpected:
            raise RuntimeError(
                "Error(s) in loading export state_dict:\n"
                f"  Missing keys: {remaining_missing}\n"
                f"  Unexpected keys: {remaining_unexpected}"
            )

    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=True)
    cfg = ModelConfig(**{k: v for k, v in ckpt["model_config"].items()
                         if k in ModelConfig.__dataclass_fields__})
    zs: List[int] = list(ckpt["z_table_zs"])
    ae = np.asarray(ckpt["atomic_energies"], dtype=float).reshape(-1)
    symbols = [ASE_CHEMICAL_SYMBOLS[z] for z in zs]

    use_o3 = bool(getattr(cfg, "e3mu_use_parity", False) or getattr(cfg, "e3mu_use_l3", False))

    out_path = str(Path(ckpt_path).with_name(f"{Path(ckpt_path).stem}_compat_sevennet.pt"))
    extra = {
        "chemical_symbols_to_index": " ".join(symbols).encode("utf-8"),
        "cutoff": str(float(cfg.r_max)).encode("utf-8"),
        "num_species": str(len(symbols)).encode("utf-8"),
    }

    if use_o3:
        ground = _E3MUGroundModelO3TS(num_elements=len(zs), atomic_energies_1d=ae, cfg=cfg)
        ground.core.type_zs.copy_(torch.tensor([int(z) for z in zs], dtype=torch.long))
        _load_export_state_dict(ground, ckpt["ground_state_dict"], cfg)
        scripted = torch.jit.script(E3MUAsSevenNetTorchScriptModelO3(ground.eval()).eval())
    else:
        ground = _E3MUGroundModelSO3TS(num_elements=len(zs), atomic_energies_1d=ae, cfg=cfg)
        _load_export_state_dict(ground, ckpt["ground_state_dict"], cfg)
        scripted = torch.jit.script(E3MUAsSevenNetTorchScriptModel(ground.eval()).eval())

    torch.jit.save(scripted, out_path, _extra_files=extra)
    arch = "O3" if use_o3 else "SO3"
    rbf = str(getattr(cfg, "rbf_type", "gaussian"))
    log(f"[{_now()}] Exported SevenNet TS ({arch}, rbf={rbf}): {out_path}")

# ══════════════════════════════════════════════════════════════════════════
# SECTION: Training, Search, and GUI
# Training entry points, automatic parameter search, and the Tkinter front end.
# ══════════════════════════════════════════════════════════════════════════

@dataclass
class TrainConfig:
    """Training configuration shared by base, response, and joint modes."""
    mode: str
    device: str = "auto"
    # ``auto`` uses all available CPU threads for CPU training and a bounded
    # four-thread helper pool for MPS/CUDA. A positive integer is honored exactly.
    cpu_threads: Any = "auto"
    dataset: str = ""
    static_data: str = ""
    response_data: str = ""
    base_ckpt: str = ""
    out_ckpt: str = "model.pt"
    keys: DatasetKeys = field(default_factory=DatasetKeys)
    model: ModelConfig = field(default_factory=ModelConfig)
    epochs: int = 50
    lr: float = 1e-3
    batch_size: int = 4
    val_fraction: float = 0.1
    seed: int = 0
    w_energy: float = 1.0
    w_forces: float = 10.0
    force_loss: str = "mse"              # "mse" | "huber"
    force_huber_delta: float = 1.0       # eV/Angstrom; used only by Huber
    w_dipole: float = 0.0
    w_polarizability: float = 0.0
    w_charges: float = 0.0
    w_atomic_dipoles: float = 0.0
    w_atomic_polarizability: float = 0.0
    w_c6: float = 0.0
    w_bec: float = 0.0
    w_magnetic_moments: float = 0.0
    w_effective_field: float = 0.0
    w_j: float = 0.0
    w_di: float = 0.0
    w_dmi: float = 0.0
    grad_clip_norm: float = 100.0
    export_sevennet: bool = True

    # Joint fine-tuning / cascade options.
    # Per-branch learning rates for joint mode. ``None`` means "reuse cfg.lr".
    lr_ground: Optional[float] = None
    lr_response: Optional[float] = None
    # Scheduler used within a single ``train_dual_layer`` call.
    lr_scheduler: str = "flat"          # "flat" | "cosine"
    # Number of warmup epochs with the ground branch frozen.
    warmup_freeze_epochs: int = 0
    # Final target weights for the linear loss ramp. ``None`` disables the ramp.
    w_dipole_final: Optional[float] = None
    w_polarizability_final: Optional[float] = None
    # Optional per-dataset subsampling before the train/val split.
    # ``1.0`` keeps all frames, ``0.2`` keeps 20 percent of each dataset.
    subset_fraction: float = 1.0
    # Canonical HDF5 datasets keep only their split/mask index in RAM. Structures
    # and labels are read for the current batch; legacy extXYZ remains materialized.
    stream_hdf5: bool = True
    # Persist exact neighbor topology on disk so streaming does not rebuild the
    # same graph every epoch. Geometry and labels remain in canonical HDF5.
    cache_neighbor_graphs: bool = True
    graph_cache_dir: str = ""
    # Composite Joint epochs use every response record and a rotating,
    # deterministic foundation window. This prevents rare L2/L3 labels from
    # being diluted by tens of millions of OMat24 L1 structures.
    composite_joint_foundation_ratio: float = 4.0
    # Write per-epoch .pt checkpoints + scatter/MAE plots to ./train/.
    # Set to False during AutoSearch trials to avoid I/O overhead.
    save_epoch_artifacts: bool = True
    # Keep restart checkpoints and metric histories while allowing long
    # unattended runs to disable memory-intensive matplotlib rendering.
    save_epoch_plots: bool = True
    # Stop after this many validation epochs without a material improvement.
    # Zero disables early stopping.
    early_stopping_patience: int = 0
    early_stopping_min_delta: float = 0.0
    # Recover from a rare finite-update/next-forward overflow by restoring the
    # last fully validated epoch, clearing Adam moments, and reducing every LR.
    # This retries the same batch; no structure or label is silently discarded.
    nonfinite_recovery_attempts: int = 3
    nonfinite_lr_decay: float = 0.25
    # Isolate structures that reproducibly produce non-finite values instead
    # of terminating a long production run. The failing batch is restored to
    # the latest finite model state and retried structure by structure.
    skip_bad_samples: bool = True
    max_bad_samples: int = 1000
    max_bad_sample_fraction: float = 0.01
    # Auto Research fixes this target set across baseline and candidates so a
    # zero loss weight cannot improve the score merely by hiding its own metric.
    validation_targets: Tuple[str, ...] = ()


# Characteristic scales make the AutoSearch score dimensionless without letting
# a candidate win merely by shrinking its own loss weights.
VALIDATION_MAE_SCALES: Dict[str, float] = {
    "energy": 1.0,
    "forces": 1.0,
    "dipole": 1.0,
    "polarizability": 1.0,
    "charges": 0.1,
    "atomic_dipoles": 0.1,
    "atomic_polarizability": 0.1,
    "c6": 10.0,
    "bec": 0.1,
    "magnetic_moments": 1.0,
    "effective_field": 0.01,
    "J_effective": 0.01,
    "Di_effective": 0.01,
    "Di": 0.01,
    "DMI_effective": 0.01,
}


def _expanded_property_weight(
    batch: Any,
    name: str,
    prediction: torch.Tensor,
    *,
    atomwise: bool,
) -> torch.Tensor:
    raw = getattr(batch, f"{name}_weight", None)
    if raw is None:
        return torch.ones((prediction.shape[0],), dtype=prediction.dtype, device=prediction.device)
    weight = torch.as_tensor(raw, dtype=prediction.dtype, device=prediction.device).reshape(-1)
    if atomwise and weight.numel() == _batch_num_graphs(batch):
        weight = weight[batch.batch]
    if weight.numel() == 1 and prediction.shape[0] > 1:
        weight = weight.expand(prediction.shape[0])
    if weight.numel() != prediction.shape[0]:
        raise ValueError(
            f"{name}_weight has {weight.numel()} entries for prediction shape {tuple(prediction.shape)}"
        )
    return weight


def _batch_has_label(batch: Any, name: str) -> bool:
    """Check a collated label mask before constructing expensive derivatives."""
    raw = getattr(batch, f"{name}_weight", None)
    if raw is None:
        return False
    weight = torch.as_tensor(raw).detach()
    return bool(torch.any(torch.isfinite(weight) & (weight > 0.0)).cpu())


def _masked_mae_statistics(
    prediction: torch.Tensor,
    target: torch.Tensor,
    weight: torch.Tensor,
) -> Tuple[float, int]:
    expanded = weight.detach()
    while expanded.ndim < prediction.ndim:
        expanded = expanded.unsqueeze(-1)
    expanded = expanded.expand_as(prediction)
    active = expanded > 0.0
    count = int(torch.count_nonzero(active).item())
    if count == 0:
        return 0.0, 0
    absolute = torch.abs(prediction.detach()[active] - target.detach()[active])
    return float(torch.sum(absolute * expanded[active]).cpu()), count


def _batch_structure_summary(batch: Any, *, limit: int = 8) -> str:
    """Return compact structure identifiers for numerical-error diagnostics."""
    raw = getattr(batch, "group_id", None)
    if raw is None:
        identifiers: List[str] = []
    elif isinstance(raw, str):
        identifiers = [raw]
    elif isinstance(raw, (list, tuple)):
        identifiers = [str(value) for value in raw]
    else:
        identifiers = [str(raw)]
    if len(identifiers) > limit:
        identifiers = identifiers[:limit] + [f"...+{len(identifiers) - limit}"]
    atom_count = int(batch.positions.shape[0])
    edge_count = int(batch.edge_index.shape[1])
    return (
        f"structures={identifiers or ['unknown']} atoms={atom_count} "
        f"edges={edge_count}"
    )


def _batch_structure_ids(batch: Any) -> List[str]:
    """Return stable sample IDs, falling back to leakage-safe group IDs."""
    for attribute in ("sample_id", "group_id"):
        raw = getattr(batch, attribute, None)
        if raw is None:
            continue
        if isinstance(raw, str):
            return [raw]
        if isinstance(raw, (list, tuple)):
            return [str(value) for value in raw]
        return [str(raw)]
    return [f"unknown-{index}" for index in range(_batch_num_graphs(batch))]


class _BadSampleError(FloatingPointError):
    """Signals a numerical failure that can be isolated at structure level."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = str(kind)
        self.detail = str(detail)


def _is_isolatable_numerical_exception(exc: BaseException) -> bool:
    if isinstance(exc, (_BadSampleError, FloatingPointError, torch.linalg.LinAlgError)):
        return True
    message = str(exc).lower()
    return any(
        token in message
        for token in (
            "non-finite", "nan", "infinity", "singular", "ill-conditioned",
            "failed to converge", "cholesky", "linalg.eigh", "linalg.eig",
        )
    )


def _split_graph_batch(batch: Any) -> List[AtomicData]:
    """Detach a PyG batch into independent CPU graphs for fault isolation."""
    graphs = batch.detach().cpu().to_data_list()
    for graph in graphs:
        if hasattr(graph, "film_condition"):
            graph.film_condition = None
    return graphs


def _atomic_data_is_finite(graph: AtomicData) -> Tuple[bool, List[str]]:
    """Check geometry and every active label before accelerator execution."""
    invalid: List[str] = []
    for name in ("positions", "cell", "shifts"):
        value = getattr(graph, name, None)
        if torch.is_tensor(value) and value.is_floating_point():
            if not bool(torch.isfinite(value).all().cpu()):
                invalid.append(name)
    for name in (
        "energy", "forces", "dipole", "polarizability", "total_charge",
        "charges", "atomic_dipoles", "atomic_polarizability", "c6", "bec",
        "spins", "magnetic_moments", "effective_field", "Di",
        "J_effective", "DMI_effective", "Di_effective",
    ):
        value = getattr(graph, name, None)
        weight = getattr(graph, f"{name}_weight", None)
        if not torch.is_tensor(value) or not value.is_floating_point():
            continue
        active = True
        if torch.is_tensor(weight):
            active = bool(torch.any(torch.isfinite(weight) & (weight > 0.0)).cpu())
        if active and not bool(torch.isfinite(value).all().cpu()):
            invalid.append(name)
    return not invalid, invalid


def _collate_valid_atomic_data(
    values: Sequence[AtomicData],
    *,
    invalid_callback: Optional[Callable[[AtomicData, Sequence[str]], None]] = None,
) -> Optional[_TGBatch]:
    valid: List[AtomicData] = []
    for graph in values:
        finite, invalid_fields = _atomic_data_is_finite(graph)
        if finite:
            valid.append(graph)
        elif invalid_callback is not None:
            invalid_callback(graph, invalid_fields)
    return _TGBatch.from_data_list(valid) if valid else None


def _nonfinite_gradient_parameters(
    model: torch.nn.Module,
    *,
    limit: int = 12,
) -> List[str]:
    """List parameters whose gradient contains NaN or Inf."""
    failures: List[str] = []
    for name, parameter in model.named_parameters():
        gradient = parameter.grad
        if gradient is None:
            continue
        finite = torch.isfinite(gradient.detach())
        if not bool(finite.all().cpu()):
            bad_count = int((~finite).sum().detach().cpu())
            failures.append(f"{name} ({bad_count}/{gradient.numel()} non-finite)")
            if len(failures) >= limit:
                break
    return failures


def _nonfinite_model_state_names(
    model: torch.nn.Module,
    *,
    limit: int = 12,
) -> List[str]:
    """List parameters or persistent buffers corrupted by an optimizer update."""
    failures: List[str] = []
    for name, value in model.state_dict().items():
        if not torch.is_tensor(value) or not value.is_floating_point():
            continue
        if not bool(torch.isfinite(value.detach()).all().cpu()):
            failures.append(str(name))
            if len(failures) >= limit:
                break
    return failures


def _nonfinite_optimizer_state_names(
    optimizer: torch.optim.Optimizer,
    *,
    limit: int = 12,
) -> List[str]:
    """List non-finite Adam moment tensors after a nominally finite update."""
    failures: List[str] = []
    parameter_names = {
        id(parameter): name
        for group_index, group in enumerate(optimizer.param_groups)
        for parameter_index, parameter in enumerate(group["params"])
        for name in [f"group{group_index}.param{parameter_index}"]
    }
    for parameter, state in optimizer.state.items():
        parameter_name = parameter_names.get(id(parameter), "parameter")
        for state_name, value in state.items():
            if not torch.is_tensor(value) or not value.is_floating_point():
                continue
            if not bool(torch.isfinite(value.detach()).all().cpu()):
                failures.append(f"{parameter_name}.{state_name}")
                if len(failures) >= limit:
                    return failures
    return failures


def _clip_grad_norm_stable(
    parameters: Iterable[torch.nn.Parameter],
    max_norm: float,
) -> float:
    """Clip a global L2 gradient norm without overflowing float32 reductions."""
    gradients = [
        parameter.grad
        for parameter in parameters
        if parameter.grad is not None
    ]
    if not gradients:
        return 0.0
    limit = float(max_norm)
    if not math.isfinite(limit) or limit <= 0.0:
        raise ValueError("grad_clip_norm must be finite and greater than zero")
    maxima: List[float] = []
    for gradient in gradients:
        detached = gradient.detach()
        if not bool(torch.isfinite(detached).all().cpu()):
            return float("nan")
        maxima.append(float(torch.max(torch.abs(detached)).cpu()))
    scale = max(maxima, default=0.0)
    if scale == 0.0:
        return 0.0

    # Dividing first keeps every squared term <= 1.  Python float combines the
    # per-tensor sums in float64 even on MPS, where tensors themselves remain
    # float32.  This avoids the inf norm / finite gradients failure mode of the
    # standard reduction for very large but still representable gradients.
    scaled_square_sum = 0.0
    for gradient in gradients:
        normalized = gradient.detach() / scale
        scaled_square_sum += float(torch.sum(normalized * normalized).cpu())
    total_norm = scale * math.sqrt(max(0.0, scaled_square_sum))
    if not math.isfinite(total_norm):
        return total_norm
    coefficient = min(1.0, limit / (total_norm + 1e-12))
    if coefficient < 1.0:
        with torch.no_grad():
            for gradient in gradients:
                gradient.mul_(coefficient)
    return total_norm


def _nonfinite_output_names(outputs: Dict[str, Any]) -> List[str]:
    """List model outputs containing NaN or Inf for focused diagnostics."""
    failures: List[str] = []
    for name, value in outputs.items():
        if torch.is_tensor(value) and not bool(
            torch.isfinite(value.detach()).all().cpu()
        ):
            failures.append(str(name))
    return failures


def _additional_physics_loss(
    out: Dict[str, torch.Tensor],
    batch: Any,
    cfg: TrainConfig,
    *,
    metric_targets: Sequence[str] = (),
) -> Tuple[torch.Tensor, Dict[str, Tuple[float, int]]]:
    zero = torch.zeros((), dtype=batch.positions.dtype, device=batch.positions.device)
    total = zero
    metrics: Dict[str, Tuple[float, int]] = {}
    specs = [
        ("charges", "charges", float(cfg.w_charges), True),
        ("atomic_dipoles", "atomic_dipoles", float(cfg.w_atomic_dipoles), True),
        ("atomic_polarizability", "atomic_polarizability", float(cfg.w_atomic_polarizability), True),
        ("c6", "c6", float(cfg.w_c6), True),
        ("bec", "bec", float(cfg.w_bec), True),
        ("magnetic_moments", "magnetic_moments", float(cfg.w_magnetic_moments), True),
        ("effective_field", "effective_field", float(cfg.w_effective_field), True),
        ("J_effective", "J_effective", float(cfg.w_j), False),
        ("DMI_effective", "DMI_effective", float(cfg.w_dmi), False),
    ]
    requested_metrics = {str(value) for value in metric_targets}
    for target_name, output_name, coefficient, atomwise in specs:
        collect_metric = target_name in requested_metrics
        if coefficient <= 0.0 and not collect_metric:
            continue
        if output_name not in out:
            raise ValueError(f"Model does not provide required output {output_name!r}")
        prediction = out[output_name]
        target = torch.as_tensor(
            getattr(batch, target_name), dtype=prediction.dtype, device=prediction.device
        ).reshape_as(prediction)
        weight = _expanded_property_weight(
            batch, target_name, prediction, atomwise=atomwise
        )
        if float(weight.sum().detach().cpu()) <= 0.0:
            continue
        if coefficient > 0.0:
            total = total + coefficient * _weighted_mse(prediction, target, weight)
        metrics[target_name] = _masked_mae_statistics(prediction, target, weight)

    if float(cfg.w_di) > 0.0 or bool({"Di", "Di_effective"} & requested_metrics):
        use_effective = (
            hasattr(batch, "Di_effective_weight")
            and float(torch.as_tensor(batch.Di_effective_weight).sum().detach().cpu()) > 0.0
        )
        target_name = "Di_effective" if use_effective else "Di"
        output_name = target_name
        prediction = out[output_name]
        target = torch.as_tensor(
            getattr(batch, target_name), dtype=prediction.dtype, device=prediction.device
        ).reshape_as(prediction)
        weight = _expanded_property_weight(
            batch, target_name, prediction, atomwise=not use_effective
        )
        if float(weight.sum().detach().cpu()) > 0.0:
            if float(cfg.w_di) > 0.0:
                total = total + float(cfg.w_di) * _weighted_mse(prediction, target, weight)
            metrics[target_name] = _masked_mae_statistics(prediction, target, weight)
    return total, metrics


# --------------------------------------------------------------------------
# AutoSearch.
# Greedy random search with a small Bayesian surrogate for later-stage
# exploitation.
# --------------------------------------------------------------------------

@dataclass
class AutoSearchConfig:
    """Configuration for automatic hyperparameter search."""
    level: int = 0          # 0=off; 1=loss weights; 2=all HP; 3=HP+JFT; 4=HP+JFT+Arch
    n_trials: int = 20      # number of candidate trials (excluding the baseline)
    trial_epochs: int = 10  # short epoch budget per trial
    seed: int = 42
    subset_fraction: float = 0.01  # fraction of each dataset used per trial (default 1%)
    excluded_params: Tuple[str, ...] = ()  # data-incompatible GUI dimensions
    # The GUI treats Architecture Switches as a deliberate model choice. Search
    # tunes only parameters that remain meaningful inside that fixed topology.
    lock_selected_architecture: bool = True
    search_space_overrides: Dict[str, tuple] = field(default_factory=dict)
    # ``None`` selects the dimensions implied by ``level``. A tuple is an exact,
    # user-editable selection and may add or remove any compatible dimension.
    search_params: Optional[Tuple[str, ...]] = None


_AUTOSEARCH_SAMPLERS = {
    "uniform", "log_uniform", "zero_log_uniform", "randint", "choice", "bool"
}


def normalize_search_space_spec(name: str, spec: Sequence[Any]) -> tuple:
    """Validate and canonicalize one editable Auto Research sampler."""
    if isinstance(spec, (str, bytes)) or not isinstance(spec, Sequence) or not spec:
        raise ValueError(f"Search space for {name!r} must be a non-empty sequence")
    kind = str(spec[0]).strip().lower()
    if kind not in _AUTOSEARCH_SAMPLERS:
        raise ValueError(
            f"Unsupported sampler {kind!r} for {name!r}; expected one of "
            f"{sorted(_AUTOSEARCH_SAMPLERS)}"
        )
    if kind == "bool":
        if len(spec) != 1:
            raise ValueError(f"Boolean search space for {name!r} takes no domain")
        return (kind,)
    if kind == "choice":
        if len(spec) != 2 or isinstance(spec[1], (str, bytes)):
            raise ValueError(f"Choice search space for {name!r} requires a value list")
        values = list(spec[1])
        if not values:
            raise ValueError(f"Choice search space for {name!r} cannot be empty")
        if len({json.dumps(value, sort_keys=True) for value in values}) != len(values):
            raise ValueError(f"Choice search space for {name!r} contains duplicates")
        return (kind, values)
    if len(spec) < 3:
        raise ValueError(f"Sampler {kind!r} for {name!r} requires lower and upper bounds")
    if kind == "randint":
        lower, upper = int(spec[1]), int(spec[2])
        if lower > upper:
            raise ValueError(f"Integer search bounds for {name!r} must satisfy lower <= upper")
        return (kind, lower, upper)
    lower, upper = float(spec[1]), float(spec[2])
    if not math.isfinite(lower) or not math.isfinite(upper) or lower >= upper:
        raise ValueError(f"Search bounds for {name!r} must be finite with lower < upper")
    if kind in {"log_uniform", "zero_log_uniform"} and lower <= 0.0:
        raise ValueError(f"Log search lower bound for {name!r} must be greater than zero")
    if kind == "zero_log_uniform":
        probability = float(spec[3]) if len(spec) > 3 else 0.2
        if not math.isfinite(probability) or not 0.0 < probability < 1.0:
            raise ValueError(
                f"Zero probability for {name!r} must be strictly between zero and one"
            )
        return (kind, lower, upper, probability)
    return (kind, lower, upper)


def search_space_spec_to_editor(spec: Sequence[Any]) -> Tuple[str, str]:
    """Return sampler name and JSON domain for the Qt range editor."""
    normalized = normalize_search_space_spec("parameter", spec)
    kind = str(normalized[0])
    if kind == "bool":
        domain: Any = []
    elif kind == "choice":
        domain = list(normalized[1])
    else:
        domain = list(normalized[1:])
    return kind, json.dumps(domain, ensure_ascii=True)


def search_space_spec_from_editor(name: str, kind: str, domain_text: str) -> tuple:
    """Parse the JSON domain entered in the Qt Auto Research editor."""
    sampler = str(kind).strip().lower()
    try:
        domain = json.loads(str(domain_text).strip() or "[]")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Search domain for {name!r} must be valid JSON: {exc.msg}") from exc
    if not isinstance(domain, list):
        raise ValueError(f"Search domain for {name!r} must be a JSON list")
    if sampler == "choice":
        raw: tuple = (sampler, domain)
    else:
        raw = (sampler, *domain)
    return normalize_search_space_spec(name, raw)


def _auto_emit(pq: Callable, trial: int, n_trials: int,
               best_loss: float, trial_loss: float,
               best_params: Dict[str, Any], trial_params: Dict[str, Any],
               improved: bool) -> None:
    """Push an auto_search progress event to the GUI queue."""
    try:
        pq({
            "type": "auto_search",
            "trial": trial,
            "n_trials": n_trials,
            "best_loss": best_loss,
            "trial_loss": trial_loss,
            "params": dict(best_params),
            "trial_params": dict(trial_params),
            "improved": improved,
        })
    except Exception:
        pass


class _TinyTorchGP:
    """Small pure-PyTorch Gaussian-process regressor.

    Keeping the whole implementation inside PyTorch avoids external BLAS /
    OpenMP interactions that can occasionally deadlock on macOS.
    """
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.tensor(X, dtype=torch.float32)
        # Normalize targets to zero mean and unit variance for a stabler fit.
        self.y_mu = float(np.mean(y))
        self.y_std = float(np.std(y)) + 1e-6
        self.y = torch.tensor((y - self.y_mu) / self.y_std, dtype=torch.float32)
        
        # Learnable kernel length scale and observation noise.
        self.log_ls = torch.nn.Parameter(torch.zeros(self.X.shape[1]))
        self.log_noise = torch.nn.Parameter(torch.tensor(-4.0))
        
        # Fit the kernel by maximizing the marginal likelihood.
        opt = torch.optim.Adam([self.log_ls, self.log_noise], lr=0.1)
        for _ in range(100):
            opt.zero_grad()
            ls = torch.exp(self.log_ls) + 1e-3
            X_s = self.X / ls
            dist2 = torch.cdist(X_s, X_s)**2
            K = torch.exp(-0.5 * dist2) + torch.exp(self.log_noise) * torch.eye(self.X.shape[0])
            try:
                L = torch.linalg.cholesky(K)
                alpha = torch.cholesky_solve(self.y.unsqueeze(1), L).squeeze(1)
                # Negative log marginal likelihood.
                loss = 0.5 * torch.dot(self.y, alpha) + torch.sum(torch.log(torch.diag(L)))
                loss.backward()
                opt.step()
            except RuntimeError:
                # Fall back gracefully if the kernel matrix becomes non-PSD.
                self.log_noise.data += 1.0
                break

    def predict(self, X_test: np.ndarray) -> Tuple[torch.Tensor, torch.Tensor]:
        with torch.no_grad():
            Xt = torch.tensor(X_test, dtype=torch.float32)
            ls = torch.exp(self.log_ls) + 1e-3
            X_s = self.X / ls
            Xt_s = Xt / ls
            
            dist2 = torch.cdist(X_s, X_s)**2
            K = torch.exp(-0.5 * dist2) + torch.exp(self.log_noise) * torch.eye(self.X.shape[0])
            L = torch.linalg.cholesky(K)
            alpha = torch.cholesky_solve(self.y.unsqueeze(1), L)
            
            dist2_s = torch.cdist(Xt_s, X_s)**2
            K_s = torch.exp(-0.5 * dist2_s)
            
            # Posterior mean.
            mu = K_s @ alpha
            mu_real = mu.squeeze(1) * self.y_std + self.y_mu
            
            # Posterior variance.
            v = torch.linalg.solve_triangular(L, K_s.T, upper=False)
            var = 1.0 - torch.sum(v**2, dim=0)
            std_real = torch.sqrt(torch.clamp(var, min=1e-6)) * self.y_std
            
            return mu_real, std_real


class _BayesianCore:
    """Bayesian helper used to guide later AutoSearch trials."""
    def __init__(self, param_names: List[str], search_space: Dict[str, tuple]) -> None:
        self._names = param_names
        self._space = search_space
        self._X: List[np.ndarray] = []
        self._y: List[float]      = []
        self._gp    = None
        self._ready = False

    def _encode(self, params: Dict[str, Any]) -> np.ndarray:
        vec = np.empty(len(self._names), dtype=np.float64)
        for i, name in enumerate(self._names):
            v, spec = params[name], self._space[name]
            kind = spec[0]
            if kind == "zero_log_uniform":
                lo, hi, zero_probability = spec[1], spec[2], spec[3]
                if float(v) == 0.0:
                    vec[i] = 0.0
                else:
                    v_clamped = float(np.clip(float(v), lo, hi))
                    log_position = (
                        (np.log(v_clamped) - np.log(lo))
                        / (np.log(hi) - np.log(lo))
                    )
                    # Reserve a continuous prefix for the zero atom so the GP
                    # can distinguish disabling a target from a small weight.
                    vec[i] = float(zero_probability) + (
                        1.0 - float(zero_probability)
                    ) * log_position
            elif kind == "log_uniform":
                lo, hi = spec[1], spec[2]
                v_clamped = float(np.clip(float(v), lo, hi))
                vec[i] = (np.log(v_clamped) - np.log(lo)) / (np.log(hi) - np.log(lo))
            elif kind == "uniform":
                lo, hi = spec[1], spec[2]
                vec[i] = (float(v) - lo) / (hi - lo)
            elif kind == "choice":
                opts = spec[1]
                idx  = opts.index(v) if v in opts else 0
                vec[i] = idx / max(1, len(opts) - 1)
            elif kind == "randint":
                lo, hi = int(spec[1]), int(spec[2])
                vec[i] = (int(v) - lo) / max(1, hi - lo)
            elif kind == "bool":
                vec[i] = 1.0 if v else 0.0
            else:
                vec[i] = 0.5
        return np.clip(vec, 0.0, 1.0)

    def _decode(self, vec: np.ndarray) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        for i, name in enumerate(self._names):
            x    = float(np.clip(vec[i], 0.0, 1.0))
            spec = self._space[name]
            kind = spec[0]
            if kind == "zero_log_uniform":
                lo, hi, zero_probability = spec[1], spec[2], spec[3]
                if x < float(zero_probability):
                    params[name] = 0.0
                else:
                    scaled = (x - float(zero_probability)) / (
                        1.0 - float(zero_probability)
                    )
                    params[name] = float(
                        np.exp(
                            scaled * (np.log(hi) - np.log(lo)) + np.log(lo)
                        )
                    )
            elif kind == "log_uniform":
                lo, hi = spec[1], spec[2]
                params[name] = float(np.exp(x * (np.log(hi) - np.log(lo)) + np.log(lo)))
            elif kind == "uniform":
                lo, hi = spec[1], spec[2]
                params[name] = float(x * (hi - lo) + lo)
            elif kind == "choice":
                opts = spec[1]
                idx  = max(0, min(len(opts) - 1, int(round(x * (len(opts) - 1)))))
                params[name] = opts[idx]
            elif kind == "randint":
                lo, hi = int(spec[1]), int(spec[2])
                params[name] = max(lo, min(hi, int(round(x * (hi - lo) + lo))))
            elif kind == "bool":
                params[name] = bool(round(x))
        return params

    def add_observation(self, params: Dict[str, Any], fmae: float) -> None:
        self._X.append(self._encode(params))
        self._y.append(float(fmae))
        if len(self._y) >= 3:
            self._fit()

    @property
    def ready(self) -> bool:
        return self._ready

    def _fit(self) -> None:
        try:
            # Use the in-house PyTorch GP so search remains self-contained.
            self._gp = _TinyTorchGP(np.array(self._X), np.array(self._y))
            self._ready = True
        except Exception as e:
            print(f"GP Fit error: {e}")
            self._ready = False

    def suggest(self, rng: "np.random.Generator", n_candidates: int = 2000) -> "Optional[Dict[str, Any]]":
        if not self._ready or self._gp is None:
            return None
        try:
            dim = len(self._names)
            best_y = min(self._y)
            cands = rng.uniform(0.0, 1.0, size=(n_candidates, dim))
            
            # Predict posterior mean and standard deviation.
            mu, sigma = self._gp.predict(cands)
            
            # Expected Improvement acquisition score.
            imp = best_y - mu - 0.01
            Z = imp / (sigma + 1e-9)
            
            # Pure PyTorch normal CDF / PDF to avoid an extra SciPy dependency.
            cdf = 0.5 * (1.0 + torch.erf(Z / math.sqrt(2.0)))
            pdf = torch.exp(-0.5 * Z**2) / math.sqrt(2.0 * math.pi)
            
            ei = imp * cdf + sigma * pdf
            ei[sigma < 1e-10] = 0.0
            
            best_idx = int(torch.argmax(ei).item())
            return self._decode(cands[best_idx])
        except Exception as e:
            print(f"Suggest error: {e}")
            return None

class AutoSearchEngine:
    """Greedy random search engine with optional Bayesian guidance.

    The search begins with pure exploration, then gradually shifts toward
    surrogate-guided proposals once enough observations have been collected.
    """

    # Search space: param_name → (sampler_type, *args)
    SEARCH_SPACE: Dict[str, tuple] = {
        # ── Level 1: loss weights ─────────────────────────────────────────────
        # A real zero is a meaningful model-selection choice for every optional
        # objective. ``zero_log_uniform`` samples it explicitly instead of using
        # an invalid logarithmic interval with lower bound zero.
        "w_energy":               ("zero_log_uniform", 0.1,   10.0, 0.10),
        "w_forces":               ("zero_log_uniform", 1.0,   100.0, 0.10),
        "w_dipole":               ("zero_log_uniform", 0.001, 1.0, 0.20),
        "w_polarizability":       ("zero_log_uniform", 0.001, 1.0, 0.20),
        "w_charges":               ("zero_log_uniform", 0.001, 10.0, 0.20),
        "w_atomic_dipoles":        ("zero_log_uniform", 0.001, 1.0, 0.20),
        "w_atomic_polarizability": ("zero_log_uniform", 0.001, 1.0, 0.20),
        "w_c6":                    ("zero_log_uniform", 1e-6, 0.1, 0.20),
        "w_bec":                   ("zero_log_uniform", 0.001, 10.0, 0.20),
        "w_magnetic_moments":      ("zero_log_uniform", 0.001, 10.0, 0.20),
        "w_effective_field":       ("zero_log_uniform", 0.001, 10.0, 0.20),
        "w_j":                     ("zero_log_uniform", 0.001, 10.0, 0.20),
        "w_di":                    ("zero_log_uniform", 0.001, 10.0, 0.20),
        "w_dmi":                   ("zero_log_uniform", 0.001, 10.0, 0.20),
        # ── Level 2: training hyperparams ────────────────────────────────────
        "lr":                     ("log_uniform", 1e-4,  5e-3),
        "batch_size":             ("choice",      [2, 4, 8, 16]),
        "force_loss":             ("choice",      ["mse", "huber"]),
        "force_huber_delta":      ("log_uniform", 0.25, 2.0),
        "r_max":                  ("choice",      [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]),
        "num_channels":           ("choice",      [32, 48, 64, 96, 128]),
        "num_interactions":       ("choice",      [1, 2, 3, 4]),
        "num_radial_basis":       ("choice",      [4, 6, 8, 12, 16]),
        "field_scale":            ("uniform",     0.5,   2.0),
        # ── Level 3: JFT cascade params ──────────────────────────────────────
        "joint_stages":           ("randint",     1,     4),
        "lr_ground_scale":        ("log_uniform", 0.01,  0.5),
        "lr_response_scale":      ("log_uniform", 0.05,  0.5),
        "warmup_epochs":          ("randint",     0,     10),
        "w_dipole_final":         ("log_uniform", 1e-4,  0.1),
        "w_alpha_final":          ("log_uniform", 1e-4,  0.1),
        # ── Level 4: architecture flags ───────────────────────────────────────
        "e3mu_use_parity":        ("bool",),
        "e3mu_use_l3":            ("bool",),
        "rbf_type":               ("choice",      ["gaussian", "trainable_gaussian", "bessel"]),
        "enable_continuous_chem": ("bool",),
        "enable_qeq":             ("bool",),
        "enable_pme":             ("bool",),
        "enable_deq":             ("bool",),
        "enable_d4":              ("bool",),
        "enable_spin":            ("bool",),
        "enable_film":            ("bool",),
        "enable_dmi":             ("bool",),
        "qeq_smearing":           ("uniform", 0.15, 0.8),
        "qeq_hardness_min":       ("log_uniform", 0.05, 2.0),
        "qeq_pme_smearing":       ("uniform", 0.5, 2.0),
        "qeq_pme_lr_wavelength":  ("uniform", 0.4, 1.5),
        "qeq_stability_floor":    ("log_uniform", 0.01, 1.0),
        "deq_damping":            ("uniform", 0.1, 0.9),
        "deq_max_iter":           ("choice", [20, 35, 50, 75, 100]),
        "deq_tol":                ("log_uniform", 1e-7, 1e-4),
        "deq_alpha_max":          ("log_uniform", 10.0, 300.0),
        "d4_functional":          ("choice", ["pbe", "pbe0", "b3lyp"]),
        "spin_cutoff":            ("choice", [3.0, 4.0, 5.0]),
        "coupling_iterations":    ("randint", 1, 4),
        "coupling_tol":           ("log_uniform", 1e-7, 1e-3),
        "chem_aug_prob":          ("choice", [0.0, 0.025, 0.05, 0.10, 0.20, 0.30]),
        "chem_aug_noise_std":     ("choice", [0.0, 0.005, 0.01, 0.025, 0.05, 0.10]),
        "chem_aug_mix_max":       ("choice", [0.0, 0.025, 0.05, 0.10, 0.20, 0.30]),
    }

    # Parameters searched at each level (cumulative)
    LEVEL_PARAMS: Dict[int, List[str]] = {
        1: [
            "w_energy", "w_forces", "w_dipole", "w_polarizability",
            "w_charges", "w_atomic_dipoles", "w_atomic_polarizability", "w_c6",
            "w_bec", "w_magnetic_moments", "w_effective_field", "w_j", "w_di", "w_dmi",
        ],
        2: [
            "w_energy", "w_forces", "w_dipole", "w_polarizability",
            "w_charges", "w_atomic_dipoles", "w_atomic_polarizability", "w_c6",
            "w_bec", "w_magnetic_moments", "w_effective_field", "w_j", "w_di", "w_dmi",
            "lr", "batch_size", "r_max", "num_channels",
            "num_interactions", "num_radial_basis", "field_scale",
            "force_loss", "force_huber_delta",
        ],
        3: [
            "w_energy", "w_forces", "w_dipole", "w_polarizability",
            "w_charges", "w_atomic_dipoles", "w_atomic_polarizability", "w_c6",
            "w_bec", "w_magnetic_moments", "w_effective_field", "w_j", "w_di", "w_dmi",
            "lr", "batch_size", "r_max", "num_channels",
            "num_interactions", "num_radial_basis", "field_scale",
            "force_loss", "force_huber_delta",
            "joint_stages", "lr_ground_scale", "lr_response_scale",
            "warmup_epochs", "w_dipole_final", "w_alpha_final",
        ],
        4: [
            "w_energy", "w_forces", "w_dipole", "w_polarizability",
            "w_charges", "w_atomic_dipoles", "w_atomic_polarizability", "w_c6",
            "w_bec", "w_magnetic_moments", "w_effective_field", "w_j", "w_di", "w_dmi",
            "lr", "batch_size", "r_max", "num_channels",
            "num_interactions", "num_radial_basis", "field_scale",
            "force_loss", "force_huber_delta",
            "joint_stages", "lr_ground_scale", "lr_response_scale",
            "warmup_epochs", "w_dipole_final", "w_alpha_final",
            "e3mu_use_parity", "e3mu_use_l3", "rbf_type", "enable_continuous_chem",
            "enable_qeq", "enable_pme", "enable_deq", "enable_d4", "enable_spin",
            "enable_film", "enable_dmi", "qeq_smearing", "qeq_hardness_min",
            "qeq_pme_smearing", "qeq_pme_lr_wavelength", "qeq_stability_floor",
            "deq_damping", "deq_alpha_max",
            "d4_functional", "spin_cutoff", "coupling_iterations", "coupling_tol",
            "chem_aug_prob", "chem_aug_noise_std", "chem_aug_mix_max",
        ],
    }

    LOSS_PARAM_TO_ATTR: Dict[str, str] = {
        name: name for name in (
            "w_energy", "w_forces", "w_dipole", "w_polarizability", "w_charges",
            "w_atomic_dipoles", "w_atomic_polarizability", "w_c6", "w_bec",
            "w_magnetic_moments", "w_effective_field", "w_j", "w_di", "w_dmi",
        )
    }
    LOSS_PARAM_TO_TARGET: Dict[str, str] = {
        "w_energy": "energy",
        "w_forces": "forces",
        "w_dipole": "dipole",
        "w_polarizability": "polarizability",
        "w_charges": "charges",
        "w_atomic_dipoles": "atomic_dipoles",
        "w_atomic_polarizability": "atomic_polarizability",
        "w_c6": "c6",
        "w_bec": "bec",
        "w_magnetic_moments": "magnetic_moments",
        "w_effective_field": "effective_field",
        "w_j": "J_effective",
        "w_di": "Di_effective",
        "w_dmi": "DMI_effective",
    }

    def __init__(self, base_cfg: "TrainConfig", auto_cfg: AutoSearchConfig, tmp_dir: str) -> None:
        self.base_cfg  = base_cfg
        self.auto_cfg  = auto_cfg
        self.tmp_dir   = tmp_dir
        requested = (
            list(auto_cfg.search_params)
            if auto_cfg.search_params is not None
            else list(self.LEVEL_PARAMS.get(auto_cfg.level, []))
        )
        excluded = set(auto_cfg.excluded_params)
        if bool(auto_cfg.lock_selected_architecture):
            excluded.update(architecture_locked_search_exclusions(base_cfg.model))
        unknown = sorted(set(requested) - set(self.SEARCH_SPACE))
        if unknown:
            raise ValueError(f"Unknown Auto Research parameter(s): {unknown}")
        self.search_space = {
            name: normalize_search_space_spec(name, spec)
            for name, spec in self.SEARCH_SPACE.items()
        }
        for name, spec in dict(auto_cfg.search_space_overrides).items():
            if name not in self.SEARCH_SPACE:
                raise ValueError(f"Unknown Auto Research override parameter: {name!r}")
            self.search_space[name] = normalize_search_space_spec(name, spec)
        # Dataset masks and architecture relevance determine availability. The
        # current numeric value does not: zero must remain searchable.
        self._params = list(dict.fromkeys(
            name for name in requested if name not in excluded
        ))
        fixed_loss_params = {
            name
            for name in self.LOSS_PARAM_TO_TARGET
            if float(getattr(base_cfg, name, 0.0)) > 0.0 or name in self._params
        }
        self.validation_targets = tuple(
            dict.fromkeys(
                self.LOSS_PARAM_TO_TARGET[name]
                for name in self.LOSS_PARAM_TO_TARGET
                if name in fixed_loss_params
            )
        )
        self._bo       = _BayesianCore(self._params, self.search_space) if self._params else None

    # Helper methods.

    @staticmethod
    def _extract_current(cfg: "TrainConfig") -> Dict[str, Any]:
        """Flatten TrainConfig + ModelConfig into a single param dict."""
        mc = cfg.model
        return {
            "w_energy":            float(cfg.w_energy),
            "w_forces":            float(cfg.w_forces),
            "w_dipole":            float(cfg.w_dipole),
            "w_polarizability":    float(cfg.w_polarizability),
            "w_charges":            float(cfg.w_charges),
            "w_atomic_dipoles":     float(cfg.w_atomic_dipoles),
            "w_atomic_polarizability": float(cfg.w_atomic_polarizability),
            "w_c6":                 float(cfg.w_c6),
            "w_bec":                float(cfg.w_bec),
            "w_magnetic_moments":   float(cfg.w_magnetic_moments),
            "w_effective_field":    float(cfg.w_effective_field),
            "w_j":                  float(cfg.w_j),
            "w_di":                 float(cfg.w_di),
            "w_dmi":                float(cfg.w_dmi),
            "lr":                  float(cfg.lr),
            "batch_size":          int(cfg.batch_size),
            "force_loss":          str(getattr(cfg, "force_loss", "mse")),
            "force_huber_delta":   float(getattr(cfg, "force_huber_delta", 1.0)),
            "r_max":               float(mc.r_max),
            "num_channels":        int(mc.num_channels),
            "num_interactions":    int(mc.num_interactions),
            "num_radial_basis":    int(mc.num_radial_basis),
            "field_scale":         float(mc.field_scale),
            # Joint fine-tuning defaults used by the GUI-driven cascade.
            "joint_stages":        2,   # GUI default; not stored directly in TrainConfig.
            "lr_ground_scale":     0.05,
            "lr_response_scale":   0.20,
            "warmup_epochs":       int(getattr(cfg, "warmup_freeze_epochs", 0)),
            "w_dipole_final":      float(cfg.w_dipole_final) if cfg.w_dipole_final is not None else 1e-4,
            "w_alpha_final":       float(cfg.w_polarizability_final) if cfg.w_polarizability_final is not None else 1e-4,
            # Architecture flags mirrored from ``ModelConfig``.
            "e3mu_use_parity":     bool(getattr(mc, "e3mu_use_parity", False)),
            "e3mu_use_l3":         bool(getattr(mc, "e3mu_use_l3", False)),
            "rbf_type":            str(getattr(mc, "rbf_type", "gaussian")),
            "enable_continuous_chem": bool(getattr(mc, "enable_continuous_chem", False)),
            "enable_qeq":          bool(mc.enable_qeq),
            "enable_pme":          bool(mc.enable_pme),
            "enable_deq":          bool(mc.enable_deq),
            "enable_d4":           bool(mc.enable_d4),
            "enable_spin":         bool(mc.enable_spin),
            "enable_film":         bool(mc.enable_film),
            "enable_dmi":          bool(mc.enable_dmi),
            "qeq_smearing":        float(mc.qeq_smearing),
            "qeq_hardness_min":    float(mc.qeq_hardness_min),
            "qeq_pme_smearing":    float(mc.qeq_pme_smearing),
            "qeq_pme_lr_wavelength": float(mc.qeq_pme_lr_wavelength),
            "qeq_stability_floor": float(mc.qeq_stability_floor),
            "deq_damping":         float(mc.deq_damping),
            "deq_max_iter":        int(mc.deq_max_iter),
            "deq_tol":             float(mc.deq_tol),
            "deq_alpha_max":       float(mc.deq_alpha_max),
            "d4_functional":       str(mc.d4_functional),
            "spin_cutoff":         float(mc.spin_cutoff),
            "coupling_iterations": int(mc.coupling_iterations),
            "coupling_tol":        float(mc.coupling_tol),
            "chem_aug_prob":       float(mc.chem_aug_prob),
            "chem_aug_noise_std":  float(mc.chem_aug_noise_std),
            "chem_aug_mix_max":    float(mc.chem_aug_mix_max),
        }

    def _sample_candidate(self, rng: "np.random.Generator") -> Dict[str, Any]:
        """Sample one random candidate over all level params."""
        candidate: Dict[str, Any] = {}
        for p in self._params:
            spec = self.search_space[p]
            kind = spec[0]
            if kind == "zero_log_uniform":
                lo, hi, zero_probability = spec[1], spec[2], spec[3]
                candidate[p] = (
                    0.0
                    if float(rng.random()) < float(zero_probability)
                    else float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
                )
            elif kind == "log_uniform":
                lo, hi = spec[1], spec[2]
                candidate[p] = float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
            elif kind == "uniform":
                lo, hi = spec[1], spec[2]
                candidate[p] = float(rng.uniform(lo, hi))
            elif kind == "choice":
                opts = spec[1]
                candidate[p] = opts[int(rng.integers(0, len(opts)))]
            elif kind == "randint":
                lo, hi = int(spec[1]), int(spec[2])
                candidate[p] = int(rng.integers(lo, hi + 1))
            elif kind == "bool":
                candidate[p] = bool(rng.integers(0, 2))
            else:
                raise ValueError(f"Unknown sampler type: {kind}")
        return candidate

    def _constrain_cutoff_pair(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the conditional spin/local cutoff constraint to a flat trial."""
        constrained = dict(params)
        local_cutoff = constrained.get("r_max", self.base_cfg.model.r_max)
        magnetic_cutoff = constrained.get(
            "spin_cutoff", self.base_cfg.model.spin_cutoff
        )
        constrained["spin_cutoff"] = _compatible_spin_cutoff(
            local_cutoff, magnetic_cutoff
        )
        return constrained

    def _build_trial_cfg(self, params: Dict[str, Any], trial_idx: int) -> "TrainConfig":
        """Build a TrainConfig for a single trial from flat param dict."""
        model_values = asdict(self.base_cfg.model)
        for name in ModelConfig.__dataclass_fields__:
            if name in params:
                model_values[name] = params[name]

        spin_supervised = any(
            float(params.get(name, getattr(self.base_cfg, name))) > 0.0
            for name in ("w_magnetic_moments", "w_effective_field", "w_j", "w_di", "w_dmi")
        )
        extended_electric = any(
            float(params.get(name, getattr(self.base_cfg, name))) > 0.0
            for name in ("w_charges", "w_atomic_dipoles", "w_atomic_polarizability", "w_c6")
        )
        if spin_supervised:
            model_values["enable_spin"] = True
        if float(params.get("w_dmi", self.base_cfg.w_dmi)) > 0.0:
            model_values["enable_dmi"] = True
        if extended_electric:
            model_values["enable_qeq"] = True
        if float(params.get("w_c6", self.base_cfg.w_c6)) > 0.0:
            model_values["enable_d4"] = True
        if bool(model_values.get("enable_pme")):
            model_values["enable_qeq"] = True
        if (
            bool(model_values.get("enable_film"))
            or bool(model_values.get("e3mu_use_l3"))
            or (bool(model_values.get("enable_spin")) and bool(model_values.get("enable_dmi")))
        ):
            model_values["e3mu_use_parity"] = True
        if bool(model_values.get("enable_spin")):
            model_values["spin_cutoff"] = min(
                float(model_values["spin_cutoff"]), float(model_values["r_max"])
            )
        mc = ModelConfig(**model_values)
        tmp_path = str(Path(self.tmp_dir) / f"trial_{trial_idx:04d}.tmp.pt")

        # Use joint mode when response data exists so response weights are
        # meaningfully evaluated during search.
        _has_resp = bool(
            (self.base_cfg.dataset and self.base_cfg.dataset.strip())
            or (self.base_cfg.response_data and self.base_cfg.response_data.strip())
        )
        _mode     = "joint" if _has_resp else "base"

        # Subsetting already reduces the number of optimization steps. Scaling
        # batch size by the same fraction turns batch=32 into batch=1 at 1%,
        # causing excessive MPSGraph shape compilation and memory caching.
        _bs_raw = int(params.get("batch_size", self.base_cfg.batch_size))
        _bs     = max(1, _bs_raw)

        return TrainConfig(
            mode                   = _mode,
            device                 = self.base_cfg.device,
            cpu_threads            = self.base_cfg.cpu_threads,
            dataset                = self.base_cfg.dataset,
            static_data            = self.base_cfg.static_data,
            response_data          = self.base_cfg.response_data if _has_resp else "",
            base_ckpt              = "",   # Search trials always start from scratch.
            out_ckpt               = tmp_path,
            model                  = mc,
            epochs                 = int(self.auto_cfg.trial_epochs),
            lr                     = float(params.get("lr",            self.base_cfg.lr)),
            batch_size             = _bs,
            val_fraction           = self.base_cfg.val_fraction,
            # Keep one deterministic subset/split across all candidates so the
            # objective remains comparable and parsed data can be reused safely.
            seed                   = self.base_cfg.seed,
            w_energy               = float(params.get("w_energy",      self.base_cfg.w_energy)),
            w_forces               = float(params.get("w_forces",      self.base_cfg.w_forces)),
            force_loss             = str(params.get("force_loss", self.base_cfg.force_loss)),
            force_huber_delta      = float(params.get(
                "force_huber_delta", self.base_cfg.force_huber_delta
            )),
            w_dipole               = float(params.get("w_dipole",      self.base_cfg.w_dipole)),
            w_polarizability       = float(params.get("w_polarizability", self.base_cfg.w_polarizability)),
            w_charges              = float(params.get("w_charges", self.base_cfg.w_charges)),
            w_atomic_dipoles       = float(params.get("w_atomic_dipoles", self.base_cfg.w_atomic_dipoles)),
            w_atomic_polarizability = float(params.get("w_atomic_polarizability", self.base_cfg.w_atomic_polarizability)),
            w_c6                   = float(params.get("w_c6", self.base_cfg.w_c6)),
            w_bec                  = float(params.get("w_bec", self.base_cfg.w_bec)),
            w_magnetic_moments     = float(params.get("w_magnetic_moments", self.base_cfg.w_magnetic_moments)),
            w_effective_field      = float(params.get("w_effective_field", self.base_cfg.w_effective_field)),
            w_j                    = float(params.get("w_j", self.base_cfg.w_j)),
            w_di                   = float(params.get("w_di", self.base_cfg.w_di)),
            w_dmi                  = float(params.get("w_dmi", self.base_cfg.w_dmi)),
            grad_clip_norm         = self.base_cfg.grad_clip_norm,
            export_sevennet        = False,    # Skip TorchScript export during search trials.
            save_epoch_artifacts   = False,    # Skip per-epoch checkpoints and plots during search.
            subset_fraction        = float(self.auto_cfg.subset_fraction),
            stream_hdf5            = bool(self.base_cfg.stream_hdf5),
            cache_neighbor_graphs  = bool(self.base_cfg.cache_neighbor_graphs),
            graph_cache_dir        = str(self.base_cfg.graph_cache_dir),
            validation_targets     = self.validation_targets,
        )

    # Main search loop.

    @staticmethod
    def _make_progress(pq_put: Callable, trial_idx: int, n_trials: int) -> Callable:
        """Return a progress callback that emits auto_search_epoch events."""
        def _cb(d: Dict[str, Any]) -> None:
            if d.get("type") == "epoch":
                pq_put({
                    "type":     "auto_search_epoch",
                    "trial":    trial_idx,
                    "n_trials": n_trials,
                    "epoch":    int(d.get("epoch", 0)),
                    "epochs":   int(d.get("epochs", 1)),
                })
            # Suppress detailed prep events to keep the GUI quieter during search.
        return _cb

    def run(
        self,
        log: Callable,
        pq_put: Callable,
        stop_flag: Callable,
    ) -> "Tuple[Dict[str, Any], float]":
        """Run the search and return ``(best_params, best_validation_score)``."""
        rng = np.random.default_rng(self.auto_cfg.seed)
        current = self._constrain_cutoff_pair(self._extract_current(self.base_cfg))
        best_params = dict(current)

        if str(self.base_cfg.device).lower() in ("auto", "mps") and _mps_is_available():
            torch.mps.synchronize()
            torch.mps.empty_cache()

        # Cache parsed datasets so repeated trials do not re-read large XYZ files.
        _data_cache: Dict[str, Any] = {}

        def _cleanup_failed_trial(path: str) -> None:
            try:
                os.remove(path)
            except OSError:
                pass
            gc.collect()
            if str(self.base_cfg.device).lower() in ("auto", "mps") and _mps_is_available():
                torch.mps.synchronize()
                torch.mps.empty_cache()

        # Baseline trial using the current GUI parameters.
        log(f"[{_now()}] AutoSearch: running baseline trial "
            f"({self.auto_cfg.trial_epochs} epochs, subset={self.auto_cfg.subset_fraction:.0%})…")
        cfg0 = self._build_trial_cfg(current, trial_idx=0)
        _prog0 = self._make_progress(pq_put, 0, self.auto_cfg.n_trials)
        try:
            _, best_loss = train_dual_layer(
                cfg0, log, _prog0, stop_flag, _cache=_data_cache
            )
        except Exception as exc:
            _cleanup_failed_trial(cfg0.out_ckpt)
            raise RuntimeError(
                "AutoSearch baseline failed with the currently selected "
                f"architecture and parameters: {type(exc).__name__}: {exc}"
            ) from exc
        if stop_flag():
            _cleanup_failed_trial(cfg0.out_ckpt)
            log(f"[{_now()}] AutoSearch: stopped during baseline trial.")
            return best_params, float("inf")
        if not math.isfinite(best_loss):
            _cleanup_failed_trial(cfg0.out_ckpt)
            raise FloatingPointError(
                "AutoSearch baseline returned a non-finite validation score."
            )
        try:
            os.remove(cfg0.out_ckpt)
        except Exception:
            pass
        log(f"[{_now()}] AutoSearch: baseline normalized multi-task score={best_loss:.4f}")
        if self._bo is not None:
            self._bo.add_observation(current, best_loss)
        _auto_emit(pq_put, 0, self.auto_cfg.n_trials, best_loss, best_loss,
                   best_params, current, improved=False)

        # Three-phase schedule:
        #   Phase 1: pure random exploration
        #   Phase 2: alternate BO-guided and random proposals
        #   Phase 3: mostly exploit the surrogate, with periodic random refresh
        _n  = self.auto_cfg.n_trials
        _p1 = max(1, _n // 3)                       # phase 1 ends (exclusive)
        _p2 = max(_p1 + 1, 2 * _n // 3)             # phase 2 ends (exclusive)

        for i in range(_n):
            if stop_flag():
                log(f"[{_now()}] AutoSearch: stopped at trial {i}.")
                break

            if i < _p1:
                # Phase 1: explore broadly with pure random search.
                candidate = self._sample_candidate(rng)
                _src = "explore"
            elif i < _p2:
                # Phase 2: balance exploration and exploitation.
                _want_bo = ((i - _p1) % 2 == 0) and (self._bo is not None)
                if _want_bo:
                    bo_cand = self._bo.suggest(rng)
                    candidate = bo_cand if bo_cand is not None else self._sample_candidate(rng)
                    _src = "BO" if bo_cand is not None else "random(BO-init)"
                else:
                    candidate = self._sample_candidate(rng)
                    _src = "random"
            else:
                # Phase 3: mostly exploit the surrogate, with one random trial
                # every five iterations to avoid premature convergence.
                _want_bo = ((i - _p2) % 5 != 4) and (self._bo is not None)
                if _want_bo:
                    bo_cand = self._bo.suggest(rng)
                    candidate = bo_cand if bo_cand is not None else self._sample_candidate(rng)
                    _src = "BO" if bo_cand is not None else "random(BO-init)"
                else:
                    candidate = self._sample_candidate(rng)
                    _src = "random"

            merged = self._constrain_cutoff_pair({**best_params, **candidate})
            trial_cfg = self._build_trial_cfg(merged, trial_idx=i + 1)

            log(f"[{_now()}] AutoSearch trial {i+1}/{_n} [phase {'1-explore' if i<_p1 else '2-balance' if i<_p2 else '3-exploit'}/{_src}]: "
                f"{', '.join(f'{k}={_fmt_p(v)}' for k, v in candidate.items())}")

            _prog = self._make_progress(pq_put, i + 1, _n)
            try:
                _, trial_loss = train_dual_layer(
                    trial_cfg, log, _prog, stop_flag, _cache=_data_cache
                )
                if stop_flag():
                    _cleanup_failed_trial(trial_cfg.out_ckpt)
                    log(f"[{_now()}] AutoSearch: stopped during trial {i + 1}.")
                    break
                if not math.isfinite(trial_loss):
                    raise FloatingPointError(
                        "trial returned a non-finite validation score"
                    )
            except Exception as exc:
                trial_loss = float("inf")
                log(
                    f"[{_now()}] AutoSearch trial {i+1}: FAILED "
                    f"[{_src}] {type(exc).__name__}: {exc}. "
                    "The search will continue."
                )
                _auto_emit(
                    pq_put, i + 1, _n, best_loss, trial_loss,
                    best_params, merged, improved=False,
                )
                _cleanup_failed_trial(trial_cfg.out_ckpt)
                continue

            # The surrogate is updated with every trial, not only the winners.
            if self._bo is not None:
                self._bo.add_observation(merged, trial_loss)

            improved = trial_loss < best_loss
            if improved:
                best_loss   = trial_loss
                best_params = dict(merged)
                log(f"[{_now()}] AutoSearch trial {i+1}: IMPROVED → "
                    f"normalized score={trial_loss:.4f} [{_src}]")
            else:
                log(f"[{_now()}] AutoSearch trial {i+1}: no improvement "
                    f"(trial={trial_loss:.4f} >= best={best_loss:.4f}) [{_src}]")

            _auto_emit(pq_put, i + 1, _n, best_loss, trial_loss,
                       best_params, merged, improved)

            try:
                os.remove(trial_cfg.out_ckpt)
            except Exception:
                pass

        log(f"[{_now()}] AutoSearch complete. Best normalized multi-task score={best_loss:.4f}")
        log(f"[{_now()}] Best params: {best_params}")
        return best_params, best_loss


def train_dual_layer(cfg: TrainConfig, log: Callable, progress: Optional[Callable] = None, stop_flag: Optional[Callable] = None, _cache: Optional[Dict] = None) -> "Tuple[str, float]":
    """Train the mixed-granularity model and return ``(checkpoint_path, val_metric)``.

    Depending on ``cfg.mode``, the routine can train:
        - the ground-state branch only,
        - the response branch on top of a frozen base checkpoint,
        - or both branches jointly.

    The returned validation metric is a normalized mean of all active target
    MAEs, so AutoSearch can compare mixed physical quantities without units
    or candidate loss weights determining the ranking. If the caller requests
    a stop before any validation epoch completes, the function returns
    ``("", inf)`` and leaves any existing output checkpoint untouched.
    """
    if int(cfg.epochs) < 1:
        raise ValueError(f"epochs must be at least 1, got {cfg.epochs}")
    if int(cfg.batch_size) < 1:
        raise ValueError(f"batch_size must be at least 1, got {cfg.batch_size}")
    if int(getattr(cfg, "nonfinite_recovery_attempts", 3)) < 0:
        raise ValueError("nonfinite_recovery_attempts cannot be negative")
    _nonfinite_lr_decay = float(getattr(cfg, "nonfinite_lr_decay", 0.25))
    if not math.isfinite(_nonfinite_lr_decay) or not 0.0 < _nonfinite_lr_decay < 1.0:
        raise ValueError("nonfinite_lr_decay must be finite and strictly between 0 and 1")
    if int(getattr(cfg, "max_bad_samples", 1000)) < 0:
        raise ValueError("max_bad_samples cannot be negative")
    _max_bad_fraction = float(getattr(cfg, "max_bad_sample_fraction", 0.01))
    if not math.isfinite(_max_bad_fraction) or not 0.0 <= _max_bad_fraction <= 1.0:
        raise ValueError("max_bad_sample_fraction must be finite and in [0, 1]")

    device, runtime_dtype = resolve_device(getattr(cfg, "device", "auto"), dtype=cfg.model.dtype)
    thread_runtime = _configure_torch_cpu_threads(
        getattr(cfg, "cpu_threads", "auto"), device
    )
    cfg.cpu_threads = thread_runtime["requested"]
    cfg.model.dtype = runtime_dtype
    with _TORCH_RUNTIME_LOCK:
        torch.manual_seed(cfg.seed)
        np.random.seed(cfg.seed)
        set_default_dtype(runtime_dtype)

    log(f"[{_now()}] Device: {device}, dtype={runtime_dtype}")
    log(
        f"[{_now()}] CPU threads: requested={thread_runtime['requested']} "
        f"effective={thread_runtime['effective']}/{thread_runtime['available']} "
        f"interop={thread_runtime['interop']} policy={thread_runtime['source']}"
        + (
            f" inherited_OMP_NUM_THREADS={thread_runtime['inherited_omp']} "
            "(overridden for PyTorch)"
            if thread_runtime["inherited_omp"]
            and str(thread_runtime["inherited_omp"]) != str(thread_runtime["effective"])
            else ""
        )
    )
    log(f"[{_now()}] Neighborhood: {'mace' if HAS_MACE_NEIGHBORHOOD else 'ase'}")
    log(f"[{_now()}] CWD: {os.getcwd()}")
    log(f"[{_now()}] Script: {Path(__file__).resolve()}")
    active_architecture = [
        name
        for name in (
            "e3mu_use_parity", "e3mu_use_l3", "enable_continuous_chem",
            "enable_qeq", "enable_pme", "enable_deq", "enable_d4",
            "enable_spin", "enable_film", "enable_dmi",
        )
        if bool(getattr(cfg.model, name, False))
    ]
    active_losses = {
        name: float(getattr(cfg, name))
        for name in (
            "w_energy", "w_forces", "w_dipole", "w_polarizability",
            "w_charges", "w_atomic_dipoles", "w_atomic_polarizability",
            "w_c6", "w_bec", "w_magnetic_moments", "w_effective_field",
            "w_j", "w_di", "w_dmi",
        )
        if float(getattr(cfg, name)) > 0.0
    }
    log(
        f"[{_now()}] Architecture: "
        f"{', '.join(active_architecture) if active_architecture else 'local SO(3) only'}; "
        f"rbf={cfg.model.rbf_type} channels={cfg.model.num_channels} "
        f"interactions={cfg.model.num_interactions} radial_basis={cfg.model.num_radial_basis}"
    )
    log(
        f"[{_now()}] Optimizer: Adam lr={float(cfg.lr):g} "
        f"batch_size={int(cfg.batch_size)} grad_clip_norm={float(cfg.grad_clip_norm):g}; "
        f"force_loss={str(getattr(cfg, 'force_loss', 'mse')).lower()}"
        + (
            f"(delta={float(getattr(cfg, 'force_huber_delta', 1.0)):g})"
            if str(getattr(cfg, "force_loss", "mse")).lower() == "huber"
            else ""
        )
        + f"; loss_weights={json.dumps(active_losses, sort_keys=True)}"
    )
    _validation_targets = {
        str(value) for value in getattr(cfg, "validation_targets", ())
    }

    # Reuse parsed datasets when ``_cache`` is available so repeated search
    # trials do not spend most of their time on disk I/O.
    def _load_cached(path: str, role: str) -> Tuple[List[Configuration], List[np.ndarray]]:
        subset = float(getattr(cfg, "subset_fraction", 1.0))
        # Canonical HDF5 supports group-aware sampling before atom arrays are
        # materialized.  This is critical for low-memory Auto Research trials.
        parse_fraction = subset if subset < 1.0 else 1.0
        parse_seed = int(cfg.seed) + (1 if role == "static" else 2 if role == "response" else 0)
        cache_key = f"{role}|{path}|{parse_fraction:.12g}|{parse_seed}"
        if _cache is not None and cache_key in _cache:
            cached_cfgs, cached_fields = _cache[cache_key]
            log(f"[{_now()}] {role.title()} frames from cache: {len(cached_cfgs)}")
            return list(cached_cfgs), list(cached_fields)
        loaded_cfgs, loaded_fields = load_configurations_auto(
            path,
            cfg.keys,
            stop_flag=stop_flag,
            log=log,
            sample_fraction=parse_fraction,
            sample_seed=parse_seed,
        )
        if _cache is not None:
            _cache[cache_key] = (loaded_cfgs, loaded_fields)
        log(f"[{_now()}] Loaded {role} frames: {len(loaded_cfgs)}")
        return loaded_cfgs, loaded_fields

    def _release_mps_cache() -> None:
        if device.type != "mps":
            return
        torch.mps.synchronize()
        torch.mps.empty_cache()

    def _cancelled_result(stage: str) -> "Tuple[str, float]":
        log(
            f"[{_now()}] Training stopped by user during {stage}; "
            "no unvalidated checkpoint was written."
        )
        if progress is not None:
            progress(
                {
                    "type": "run_stopped",
                    "stage": str(stage),
                    "checkpoint_saved": False,
                }
            )
        gc.collect()
        _release_mps_cache()
        return "", float("inf")

    # A GUI process may have just estimated several candidate models. Start a
    # real run without inheriting their reclaimable MPS allocator blocks.
    _release_mps_cache()

    stream_plan: Optional[HDF5StreamPlan] = None
    use_hdf5_stream = bool(
        cfg.dataset
        and _is_hdf5_path(cfg.dataset)
        and getattr(cfg, "stream_hdf5", True)
    )
    composite_plan: Optional[CompositeStreamPlan] = None
    use_composite_stream = bool(use_hdf5_stream and _is_composite_hdf5_path(cfg.dataset))
    if use_composite_stream:
        composite_plan = prepare_composite_stream_plan(
            cfg.dataset,
            mode=cfg.mode,
            val_fraction=float(cfg.val_fraction),
            seed=int(cfg.seed),
            sample_fraction=float(cfg.subset_fraction),
        )
        split_info = dict(composite_plan.split_info)
        zs = list(composite_plan.elements)
        log(
            f"[{_now()}] Composite HDF5 streaming index: "
            f"train={split_info['train_structures']} val={split_info['val_structures']} "
            f"(OMat24={split_info['train_omat24']}/{split_info['val_omat24']}, "
            f"Large={split_info['train_large']}/{split_info['val_large']}); "
            "Parquet/HDF5 numerical arrays remain on disk."
        )
        log(f"[{_now()}] Grouped split: {json.dumps(split_info, sort_keys=True)}")
        static_cfgs = static_fields = resp_cfgs = resp_fields = []
        all_cfgs = all_fields = train_cfgs = train_fields = val_cfgs = val_fields = []
    elif use_hdf5_stream:
        plan_key = (
            "hdf5_stream_plan",
            str(Path(cfg.dataset).expanduser().resolve()),
            int(Path(cfg.dataset).expanduser().stat().st_size),
            int(Path(cfg.dataset).expanduser().stat().st_mtime_ns),
            float(cfg.val_fraction),
            int(cfg.seed),
            float(cfg.subset_fraction),
        )
        stream_plan = _cache.get(plan_key) if _cache is not None else None
        if stream_plan is None:
            stream_plan = prepare_hdf5_stream_plan(
                cfg.dataset,
                val_fraction=float(cfg.val_fraction),
                seed=int(cfg.seed),
                sample_fraction=float(cfg.subset_fraction),
                sample_seed=int(cfg.seed),
            )
            if _cache is not None:
                _cache[plan_key] = stream_plan
        stream_plan = _filter_hdf5_stream_plan_for_mode(stream_plan, cfg.mode)
        split_info = dict(stream_plan.split_info)
        zs = list(stream_plan.elements)
        log(
            f"[{_now()}] Canonical HDF5 streaming index: "
            f"train={len(stream_plan.train_indices)} "
            f"val={len(stream_plan.val_indices)}; structures and labels remain on disk."
        )
        log(f"[{_now()}] Grouped split: {json.dumps(split_info, sort_keys=True)}")
        static_cfgs = static_fields = resp_cfgs = resp_fields = []
        all_cfgs = all_fields = train_cfgs = train_fields = val_cfgs = val_fields = []
    elif cfg.dataset:
        unified_cfgs, unified_fields = _load_cached(cfg.dataset, "unified")
        static_cfgs, static_fields = unified_cfgs, unified_fields
        resp_cfgs, resp_fields = [], []
    else:
        if cfg.mode in ("base", "joint"):
            if not cfg.static_data:
                raise ValueError("static_data or dataset is required for mode 'base'/'joint'")
            static_cfgs, static_fields = _load_cached(cfg.static_data, "static")
        else:
            static_cfgs, static_fields = [], []
        if cfg.mode in ("response", "joint"):
            if not cfg.response_data:
                raise ValueError("response_data or dataset is required for mode 'response'/'joint'")
            resp_cfgs, resp_fields = _load_cached(cfg.response_data, "response")
        else:
            resp_cfgs, resp_fields = [], []

        # The two legacy files intentionally represent different supervision
        # roles and may use unrelated absolute energy references.  Namespace
        # their group identifiers and keep response frames from supervising the
        # shared ground-state energy/force branch.  Canonical HDF5 datasets use
        # their explicit per-label masks and are not altered here.
        if static_cfgs:
            static_cfgs, _unused_masked = _prepare_legacy_dataset_role(
                static_cfgs, role="static", suppress_ground_labels=False
            )
        if resp_cfgs:
            resp_cfgs, masked = _prepare_legacy_dataset_role(
                resp_cfgs, role="response", suppress_ground_labels=True
            )
            if masked["energy"] or masked["forces"]:
                log(
                    f"[{_now()}] Legacy response role: masked ground-state labels "
                    f"(energy={masked['energy']}, forces={masked['forces']}); "
                    "response targets remain active."
                )

    if not use_hdf5_stream:
        if cfg.mode == "base" or cfg.dataset:
            all_cfgs, all_fields = static_cfgs, static_fields
        elif cfg.mode == "response":
            all_cfgs, all_fields = resp_cfgs, resp_fields
        else:
            all_cfgs, all_fields = static_cfgs + resp_cfgs, static_fields + resp_fields
        if not all_cfgs:
            raise ValueError("No data provided.")
        train_cfgs, train_fields, val_cfgs, val_fields, split_info = split_configurations_grouped(
            all_cfgs,
            all_fields,
            val_fraction=cfg.val_fraction,
            seed=cfg.seed,
        )
        log(f"[{_now()}] Grouped split: {json.dumps(split_info, sort_keys=True)}")
        zs = sorted({int(z) for c in all_cfgs for z in c.atomic_numbers})
    if stop_flag is not None and stop_flag():
        return _cancelled_result("dataset indexing")
    z_table = AtomicNumberTable(zs)
    log(f"[{_now()}] Elements: {zs}")
    use_mixed_model = _model_uses_mixed_granularity(cfg.model)

    def _fit_atomic_references() -> np.ndarray:
        if composite_plan is not None:
            return fit_atomic_energies_from_composite_plan(composite_plan, zs)
        if stream_plan is not None and "energy" in stream_plan.label_masks:
            return fit_atomic_energies_from_hdf5_plan(stream_plan, zs)
        energy_fit_cfgs = [
            item for item in train_cfgs
            if "energy" in item.properties
            and float(item.property_weights.get("energy", 1.0)) > 0.0
        ]
        if energy_fit_cfgs:
            return fit_atomic_energies_from_configs(energy_fit_cfgs, zs)
        log(f"[{_now()}] No training energy labels; atomic reference energies initialized to zero.")
        return np.zeros((len(zs),), dtype=float)

    def _warm_start(path: str, *, purpose: str) -> DualLayerFieldModel:
        if not Path(path).expanduser().is_file():
            raise FileNotFoundError(f"Pretrained checkpoint not found: {path}")
        loaded, report = _initialize_model_from_checkpoint(
            checkpoint_path=path,
            target_cfg=cfg.model,
            target_elements=zs,
            missing_atomic_energies_factory=_fit_atomic_references,
        )
        log(
            f"[{_now()}] Pretrained {purpose}: {path}; "
            f"loaded={len(report['loaded'])} tensors/"
            f"{int(report['loaded_numel']):,} values, "
            f"shared_elements={len(report['shared_elements'])}, "
            f"new_elements={report['missing_dataset_elements']}, "
            f"fitted_new_element_references="
            f"{report['fitted_missing_atomic_energies']}, "
            f"architecture_skips={len(report['skipped'])}. Optimizer starts fresh."
        )
        return loaded

    # Instantiate the model and freeze / unfreeze branches according to mode.
    if cfg.mode == "response":
        if not cfg.base_ckpt:
            raise ValueError("base_ckpt is required for mode 'response'")
        model = _warm_start(cfg.base_ckpt, purpose="initialization for Response")
        model.freeze_ground()
        model.unfreeze_response()
        z_table = AtomicNumberTable(model.z_table_zs)
    elif cfg.mode == "joint" and cfg.base_ckpt:
        model = _warm_start(cfg.base_ckpt, purpose="initialization for Joint")
        model.unfreeze_ground()
        model.unfreeze_response()
        z_table = AtomicNumberTable(model.z_table_zs)
    elif cfg.mode == "base" and cfg.base_ckpt:
        model = _warm_start(cfg.base_ckpt, purpose="initialization for Base")
        model.unfreeze_ground()
        model.freeze_response()
        z_table = AtomicNumberTable(model.z_table_zs)
    else:
        if progress is not None:
            progress({"type": "prep", "task": "Fit atomic energies", "overall_frac": 0.01, "current": 0, "total": 1, "stage": "start"})
        log(f"[{_now()}] Fitting atomic energies ...")
        atomic_energies = _fit_atomic_references()
        if progress is not None:
            progress({"type": "prep", "task": "Fit atomic energies", "overall_frac": 0.03, "current": 1, "total": 1, "stage": "done"})
        model_cls = MixedGranularityE3GNN if use_mixed_model else DualLayerFieldModel
        with _TORCH_RUNTIME_LOCK:
            # Re-seed immediately before construction so a GUI estimator cannot
            # perturb initialization between data preparation and this point.
            torch.manual_seed(cfg.seed)
            model = model_cls(
                z_table=z_table,
                atomic_energies_1d=atomic_energies,
                cfg=cfg.model,
            )
        if cfg.mode == "base":
            model.unfreeze_ground()
            model.freeze_response()
        else:
            model.unfreeze_ground()
            model.unfreeze_response()

    model.to(device=device, dtype=torch.get_default_dtype())
    
    # Stream canonical HDF5 or materialize legacy inputs after the group-safe split.
    stopped = False
    if composite_plan is not None:
        train_data = CompositeAtomicDataDataset(
            composite_plan,
            composite_plan.train_omat_indices,
            composite_plan.train_large_indices,
            z_table=z_table,
            cutoff=float(model.cfg.r_max),
        )
        val_data = CompositeAtomicDataDataset(
            composite_plan,
            composite_plan.val_omat_indices,
            composite_plan.val_large_indices,
            z_table=z_table,
            cutoff=float(model.cfg.r_max),
        )
        train_atoms = int(np.sum(train_data.atom_counts, dtype=np.int64))
        avg_n = float("nan")
        log(
            f"[{_now()}] Composite dataset streaming: train={len(train_data)} "
            f"val={len(val_data)} mode={cfg.mode}; source shards are opened lazily "
            "and RAM retains only selectors/masks."
        )
    elif stream_plan is not None:
        topology_cache: Optional[str] = None
        if bool(getattr(cfg, "cache_neighbor_graphs", True)):
            topology_cache = build_hdf5_topology_cache(
                stream_plan,
                cutoff=float(model.cfg.r_max),
                cache_directory=str(getattr(cfg, "graph_cache_dir", "")),
                log=log,
                progress=progress,
                stop_flag=stop_flag,
            )
            if topology_cache is None:
                del model
                return _cancelled_result("disk topology-cache construction")
        else:
            log(
                f"[{_now()}] HDF5 streaming uses on-demand neighbor construction; "
                "enable cache_neighbor_graphs to reuse exact topology across epochs."
            )
        train_data = HDF5AtomicDataDataset(
            stream_plan,
            stream_plan.train_indices,
            z_table=z_table,
            cutoff=float(model.cfg.r_max),
            topology_cache=topology_cache,
        )
        val_data = HDF5AtomicDataDataset(
            stream_plan,
            stream_plan.val_indices,
            z_table=z_table,
            cutoff=float(model.cfg.r_max),
            topology_cache=topology_cache,
        )
        train_atoms = int(np.sum(train_data.atom_counts, dtype=np.int64))
        if train_data.edge_counts is not None:
            train_edges = int(np.sum(train_data.edge_counts, dtype=np.int64))
            avg_n = float(train_edges) / float(max(1, train_atoms))
        else:
            avg_n = float("nan")
        log(
            f"[{_now()}] Dataset streaming: train={len(train_data)} "
            f"val={len(val_data)} strategy={split_info['strategy']} "
            + (
                f"avg_neighbors/atom={avg_n:.2f}; "
                if math.isfinite(avg_n) else ""
            )
            + "RAM retains only indices/masks; HDF5 graphs load per batch."
        )
    else:
        selected_cfgs = train_cfgs + val_cfgs
        selected_fields = train_fields + val_fields
        total_all = int(len(selected_cfgs))
        n_train_graphs = len(train_cfgs)
        if total_all <= 0:
            raise ValueError("No frames to train on after mode selection.")
        graph_cache_key = (
            "graphs",
            float(model.cfg.r_max),
            tuple(int(z) for z in zs),
            tuple(
                str(c.properties.get("group_id", index))
                for index, c in enumerate(selected_cfgs)
            ),
        )
        cached_graphs = _cache.get(graph_cache_key) if _cache is not None else None
        graph_start = time.perf_counter()
        if cached_graphs is not None:
            data_all = list(cached_graphs)
            log(
                f"[{_now()}] Reused {len(data_all)} cached graphs "
                f"for cutoff={float(model.cfg.r_max):g}."
            )
        else:
            data_all = []
            emit_every = max(1, min(25, total_all // 10 or 1))
            if progress is not None:
                progress(
                    {
                        "type": "prep",
                        "task": "Build neighbor graphs",
                        "overall_frac": 0.05,
                        "current": 0,
                        "total": int(total_all),
                        "stage": "neighbor_list",
                    }
                )
            log(f"[{_now()}] Building {total_all} neighbor graphs ...")
            for i, (c, f) in enumerate(zip(selected_cfgs, selected_fields), start=1):
                if stop_flag is not None and stop_flag():
                    stopped = True
                    break
                c2 = Configuration(
                    atomic_numbers=c.atomic_numbers,
                    positions=c.positions,
                    properties=dict(c.properties),
                    property_weights=dict(c.property_weights),
                    cell=c.cell,
                    pbc=c.pbc,
                    weight=c.weight,
                    config_type=c.config_type,
                    head=c.head,
                )
                c2.properties["field"] = np.asarray(f, dtype=float).reshape(3)
                data_all.append(
                    AtomicData.from_config(
                        c2, z_table=z_table, cutoff=float(model.cfg.r_max)
                    )
                )
                if progress is not None and (
                    i == total_all or (i % emit_every == 0)
                ):
                    frac = 0.05 + 0.15 * (float(i) / float(max(1, total_all)))
                    progress(
                        {
                            "type": "prep",
                            "task": "Build neighbor graphs",
                            "overall_frac": float(max(0.0, min(1.0, frac))),
                            "current": int(i),
                            "total": int(total_all),
                            "stage": "neighbor_list",
                        }
                    )
            if not stopped and _cache is not None:
                for key in [
                    value
                    for value in _cache
                    if isinstance(value, tuple) and value and value[0] == "graphs"
                ]:
                    if key != graph_cache_key:
                        del _cache[key]
                _cache[graph_cache_key] = tuple(data_all)
            log(
                f"[{_now()}] Built {len(data_all)} neighbor graphs in "
                f"{time.perf_counter() - graph_start:.2f} s."
            )
        if stopped:
            del data_all, selected_cfgs, selected_fields, model
            return _cancelled_result("neighbor-graph construction")
        train_data = data_all[:n_train_graphs]
        val_data = data_all[n_train_graphs:]
        train_atoms = sum(int(graph.num_nodes) for graph in train_data)
        train_edges = sum(int(graph.edge_index.shape[1]) for graph in train_data)
        avg_n = float(train_edges) / float(max(1, train_atoms))
        del data_all, selected_cfgs, selected_fields
        gc.collect()
        log(
            f"[{_now()}] Dataset graphs: train={len(train_data)} "
            f"val={len(val_data)} strategy={split_info['strategy']} "
            f"avg_neighbors/atom={avg_n:.2f}"
        )

    # DataLoader policy tuned for CPU-heavy atomistic workloads.
    def _effective_num_workers() -> int:
        # On macOS/CPU, extra workers often increase RAM pressure more than they help.
        if device.type == "cuda":
            return int(min(4, max(0, (os.cpu_count() or 4))))
        return 0

    _dl_num_workers = _effective_num_workers()
    _dl_pin_memory = False
    _dl_persistent = bool(_dl_num_workers > 0)
    _dl_prefetch = 2
    _dl_thread_prefetch = 2 if (stream_plan is not None or composite_plan is not None) else 0
    _input_bad_samples: Dict[str, Dict[str, Any]] = {}
    log(
        f"[{_now()}] DataLoader: num_workers={_dl_num_workers} pin_memory={_dl_pin_memory} "
        f"persistent_workers={_dl_persistent} prefetch_factor={_dl_prefetch} "
        f"stream_thread_prefetch={_dl_thread_prefetch}"
    )
    # Release every materialized representation before optimization. Streamed
    # datasets retain only their compact plan plus disk-backed dataset objects.
    del all_cfgs, all_fields, train_cfgs, train_fields, val_cfgs, val_fields
    del static_cfgs, static_fields, resp_cfgs, resp_fields
    gc.collect()

    def _collate(lst: List[AtomicData]) -> Optional[_TGBatch]:
        def rejected(graph: AtomicData, fields: Sequence[str]) -> None:
            sample_id = str(
                getattr(graph, "sample_id", getattr(graph, "group_id", "unknown"))
            )
            entry = _input_bad_samples.setdefault(
                sample_id,
                {
                    "sample_id": sample_id,
                    "phase": "input",
                    "occurrences": 0,
                    "reason": "",
                },
            )
            entry["occurrences"] = int(entry["occurrences"]) + 1
            entry["reason"] = "non-finite input fields: " + ", ".join(fields)

        return _collate_valid_atomic_data(lst, invalid_callback=rejected)

    class _FixedGraphBatchSampler:
        """Reuse memory-bounded MPS batch shapes while randomizing batch order."""

        def __init__(
            self,
            ds: Sequence[AtomicData],
            batch_size: int,
            seed: int,
            max_edges: Optional[int] = None,
            shuffle: bool = True,
        ) -> None:
            edge_counts = getattr(ds, "edge_counts", None)
            item_edge_loads = (
                [int(value) for value in edge_counts]
                if edge_counts is not None
                else [int(ds[index].edge_index.shape[1]) for index in range(len(ds))]
            )
            batches, edge_loads = _plan_structure_batches(
                item_edge_loads, batch_size, max_load=max_edges
            )
            self.batches = batches
            self.edge_loads = edge_loads
            self.structure_loads = [len(indices) for indices in batches]
            self.requested_batch_size = int(batch_size)
            self.edge_budget = int(max_edges) if max_edges is not None else None
            self.oversized_structures = sum(
                int(load > max_edges) for load in edge_loads
            ) if max_edges is not None else 0
            self.seed = int(seed)
            self.shuffle = bool(shuffle)
            self.epoch = 0

        def __iter__(self) -> Iterable[List[int]]:
            if self.shuffle:
                order = np.random.default_rng(self.seed + self.epoch).permutation(
                    len(self.batches)
                )
                self.epoch += 1
            else:
                order = np.arange(len(self.batches), dtype=np.int64)
            return iter([self.batches[int(index)] for index in order])

        def __len__(self) -> int:
            return len(self.batches)

    class _CompositeCurriculumBatchSampler:
        """Shard-local OMat batches with rotating role-balanced Joint windows."""

        def __init__(
            self,
            ds: CompositeAtomicDataDataset,
            batch_size: int,
            seed: int,
            *,
            shuffle: bool,
        ) -> None:
            self.ds = ds
            self.batch_size = max(1, int(batch_size))
            self.seed = int(seed)
            self.shuffle = bool(shuffle)
            self.epoch = 0
            self.omat_count = int(ds.omat_indices.size)
            self.large_count = int(ds.large_indices.size)
            self.large_local = np.arange(
                self.omat_count, self.omat_count + self.large_count, dtype=np.int64
            )
            self.omat_by_source: Dict[int, np.ndarray] = {}
            if self.omat_count:
                orders = ds.plan.source_orders[ds.omat_indices]
                rows = ds.plan.row_indices[ds.omat_indices]
                for source_order in np.unique(orders):
                    local = np.flatnonzero(orders == source_order).astype(np.uint32)
                    self.omat_by_source[int(source_order)] = local[
                        np.argsort(rows[local], kind="stable")
                    ]

        def _omat_epoch_indices(self, rng: np.random.Generator) -> np.ndarray:
            if self.omat_count == 0:
                return np.zeros((0,), dtype=np.int64)
            if self.ds.plan.mode != "joint" or self.large_count == 0:
                selected = np.arange(self.omat_count, dtype=np.uint32)
            else:
                ratio = float(getattr(cfg, "composite_joint_foundation_ratio", 4.0))
                if not math.isfinite(ratio) or ratio <= 0.0:
                    raise ValueError(
                        "composite_joint_foundation_ratio must be finite and > 0"
                    )
                target = min(self.omat_count, max(1, int(round(ratio * self.large_count))))
                start = (self.epoch * target) % self.omat_count
                selected = np.asarray(
                    (start + np.arange(target, dtype=np.uint64)) % self.omat_count,
                    dtype=np.uint32,
                )
            if not self.omat_by_source:
                return selected
            selected_set = np.zeros((self.omat_count,), dtype=np.bool_)
            selected_set[selected] = True
            source_order = np.asarray(list(self.omat_by_source), dtype=np.int64)
            if self.shuffle:
                rng.shuffle(source_order)
            blocks: List[np.ndarray] = []
            for source in source_order:
                local = self.omat_by_source[int(source)]
                kept = local[selected_set[local]]
                if kept.size:
                    blocks.append(kept)
            return np.concatenate(blocks) if blocks else np.zeros((0,), dtype=np.int64)

        def __iter__(self) -> Iterable[List[int]]:
            rng = np.random.default_rng(self.seed + self.epoch)
            omat = self._omat_epoch_indices(rng)
            large = self.large_local.copy()
            if self.shuffle:
                rng.shuffle(large)
            omat_batches = [
                omat[start:start + self.batch_size].tolist()
                for start in range(0, int(omat.size), self.batch_size)
            ]
            large_batches = [
                large[start:start + self.batch_size].tolist()
                for start in range(0, int(large.size), self.batch_size)
            ]
            if omat_batches and large_batches:
                merged: List[List[int]] = []
                omat_step = max(1, int(math.ceil(len(omat_batches) / len(large_batches))))
                cursor = 0
                for response_batch in large_batches:
                    merged.extend(omat_batches[cursor:cursor + omat_step])
                    cursor += omat_step
                    merged.append(response_batch)
                merged.extend(omat_batches[cursor:])
            else:
                merged = omat_batches + large_batches
            self.epoch += 1
            return iter(merged)

        def __len__(self) -> int:
            if self.ds.plan.mode == "joint" and self.large_count:
                ratio = max(1e-12, float(getattr(cfg, "composite_joint_foundation_ratio", 4.0)))
                omat_count = min(self.omat_count, max(1, int(round(ratio * self.large_count))))
            else:
                omat_count = self.omat_count
            return int(math.ceil(omat_count / self.batch_size)) + int(
                math.ceil(self.large_count / self.batch_size)
            )

    def _make_loader(ds: Sequence[AtomicData], *, shuffle: bool) -> Any:
        # Clamp the batch size so tiny validation sets still produce a batch.
        _eff_bs = max(1, min(int(cfg.batch_size), len(ds) if ds else 1))
        kwargs: Dict[str, Any] = dict(
            collate_fn=_collate,
            num_workers=int(_dl_num_workers),
            pin_memory=bool(_dl_pin_memory),
        )
        if isinstance(ds, CompositeAtomicDataDataset):
            kwargs["batch_sampler"] = _CompositeCurriculumBatchSampler(
                ds, _eff_bs, int(cfg.seed), shuffle=shuffle
            )
        elif device.type == "mps":
            # Force/BEC training differentiates through positions twice. Bound
            # edges rather than only structures because edge count drives memory.
            # Apply the same policy to validation, where conservative forces
            # still construct the higher-order graph; only training shuffles.
            edge_budget = 12000 if (cfg.w_forces > 0.0 or cfg.w_bec > 0.0) else 30000
            kwargs["batch_sampler"] = _FixedGraphBatchSampler(
                ds,
                _eff_bs,
                int(cfg.seed),
                max_edges=edge_budget,
                shuffle=shuffle,
            )
        else:
            kwargs["batch_size"] = _eff_bs
            kwargs["shuffle"] = bool(shuffle)
        if _dl_num_workers > 0:
            kwargs["persistent_workers"] = bool(_dl_persistent)
            kwargs["prefetch_factor"] = int(_dl_prefetch)
        try:
            created: Any = DataLoader(ds, **kwargs)
        except TypeError:
            kwargs.pop("persistent_workers", None)
            kwargs.pop("prefetch_factor", None)
            created = DataLoader(ds, **kwargs)
        if isinstance(ds, (HDF5AtomicDataDataset, CompositeAtomicDataDataset)) and _dl_thread_prefetch > 0:
            return _ThreadPrefetchLoader(created, depth=_dl_thread_prefetch)
        return created

    opt = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=float(cfg.lr))

    # Optional joint fine-tuning setup with per-branch learning rates.
    _use_groups = (
        cfg.mode == "joint"
        and (cfg.lr_ground is not None or cfg.lr_response is not None)
    )
    _lr_g = cfg.lr_ground if cfg.lr_ground is not None else float(cfg.lr)
    _lr_r = cfg.lr_response if cfg.lr_response is not None else float(cfg.lr)
    _warmup_done = True

    if _use_groups:
        _response_parameters = [
            parameter for name, parameter in model.named_parameters()
            if not name.startswith("ground.") and parameter.requires_grad
        ]
        if getattr(cfg, "warmup_freeze_epochs", 0) > 0:
            # Warm up the response branch before unfreezing the ground branch.
            model.freeze_ground()
            opt = torch.optim.Adam(
                _response_parameters, lr=_lr_r
            )
            _warmup_done = False
        else:
            def _joint_optimizer() -> torch.optim.Optimizer:
                return torch.optim.Adam([
                    {
                        "params": [
                            parameter for parameter in model.ground.parameters()
                            if parameter.requires_grad
                        ],
                        "lr": _lr_g,
                    },
                    {
                        "params": [
                            parameter for name, parameter in model.named_parameters()
                            if not name.startswith("ground.") and parameter.requires_grad
                        ],
                        "lr": _lr_r,
                    },
                ])

            opt = _joint_optimizer()

    _sched = None
    if getattr(cfg, "lr_scheduler", "flat") == "cosine":
        from torch.optim.lr_scheduler import CosineAnnealingLR as _CosLR
        _sched = _CosLR(opt, T_max=max(1, int(cfg.epochs)), eta_min=1e-7)

    def _reduce_optimizer_learning_rates(
        optimizer: torch.optim.Optimizer,
    ) -> List[float]:
        updated: List[float] = []
        for group in optimizer.param_groups:
            group["lr"] = max(1e-8, float(group["lr"]) * _nonfinite_lr_decay)
            updated.append(float(group["lr"]))
        if _sched is not None:
            _sched.base_lrs = [
                max(1e-8, float(value) * _nonfinite_lr_decay)
                for value in _sched.base_lrs
            ]
            if hasattr(_sched, "_last_lr"):
                _sched._last_lr = list(updated)
        return updated

    def _prepare_retry_batch(batch: Any) -> None:
        batch.positions = batch.positions.detach()
        if hasattr(batch, "film_condition"):
            batch.film_condition = None

    _max_nonfinite_recoveries = int(getattr(cfg, "nonfinite_recovery_attempts", 3))
    _last_validated_state: Dict[str, torch.Tensor] = {
        name: value.detach().cpu().clone() for name, value in model.state_dict().items()
    }
    _last_validated_epoch = 0
    _numerical_recoveries: List[Dict[str, Any]] = []
    _bad_samples: Dict[str, Dict[str, Any]] = {}
    _bad_validation_samples: Dict[str, Dict[str, Any]] = {}
    _skipped_occurrences = 0
    _skipped_validation_occurrences = 0
    _consecutive_bad_batches = 0
    
    # Main training loop for the multi-objective loss:
    #   L_total = L_E + L_F + L_mu + L_alpha
    prog_train_base = 0.20
    prog_train_span = 0.80

    _final_val_loss: float = float("inf")
    _final_val_fmae: float = float("inf")
    _final_val_emae: float = float("inf")
    _best_val_loss: float = float("inf")
    _best_validation_score: float = float("inf")
    _best_epoch: int = 0
    _best_state: Optional[Dict[str, torch.Tensor]] = None
    _epochs_without_improvement = 0
    t0 = time.time()

    def _record_bad_sample(
        sample_id: str,
        *,
        epoch: int,
        step: int,
        phase: str,
        reason: BaseException,
    ) -> None:
        nonlocal _skipped_occurrences, _skipped_validation_occurrences
        key = str(sample_id)
        registry = _bad_validation_samples if phase == "validation" else _bad_samples
        entry = registry.setdefault(
            key,
            {
                "sample_id": key,
                "first_epoch": int(epoch),
                "first_step": int(step),
                "phase": str(phase),
                "occurrences": 0,
                "reason": "",
            },
        )
        entry["occurrences"] = int(entry["occurrences"]) + 1
        entry["last_epoch"] = int(epoch)
        entry["last_step"] = int(step)
        entry["reason"] = f"{type(reason).__name__}: {reason}"[:2000]
        if phase == "validation":
            _skipped_validation_occurrences += 1
        else:
            _skipped_occurrences += 1

    def _enforce_bad_sample_limit() -> None:
        bad_count = len(set(_bad_samples) | set(_input_bad_samples))
        fraction_limit = max(
            1,
            int(math.ceil(_max_bad_fraction * max(1, len(train_data)))),
        )
        configured_limit = int(getattr(cfg, "max_bad_samples", 1000))
        effective_limit = min(configured_limit, fraction_limit)
        if bad_count > effective_limit:
            raise FloatingPointError(
                f"Aborting after {bad_count} unique invalid training samples; "
                f"the safety limit is {effective_limit} "
                f"(max_bad_samples={configured_limit}, "
                f"max_bad_sample_fraction={_max_bad_fraction:g}). This indicates "
                "a systematic model, unit, or dataset problem rather than an isolated record."
            )

    def _checked_optimizer_step() -> None:
        """Apply one update and roll back any corrupted parameters or moments."""
        try:
            opt.step()
        except Exception as exc:
            if not _is_isolatable_numerical_exception(exc):
                raise
            model.load_state_dict(_last_validated_state, strict=True)
            opt.state.clear()
            updated_lrs = _reduce_optimizer_learning_rates(opt)
            raise _BadSampleError(
                "optimizer_exception",
                f"{type(exc).__name__}: {exc}; restored epoch "
                f"{_last_validated_epoch}, lr={updated_lrs}",
            ) from exc
        bad_model = _nonfinite_model_state_names(model)
        bad_optimizer = _nonfinite_optimizer_state_names(opt)
        if not bad_model and not bad_optimizer:
            return
        model.load_state_dict(_last_validated_state, strict=True)
        opt.state.clear()
        updated_lrs = _reduce_optimizer_learning_rates(opt)
        raise _BadSampleError(
            "nonfinite_optimizer_update",
            f"model={bad_model or ['finite']} optimizer="
            f"{bad_optimizer or ['finite']}; restored epoch "
            f"{_last_validated_epoch}, lr={updated_lrs}",
        )

    def _forward_loss_backward(
        batch: Any,
        *,
        response_weight_mu: float,
        response_weight_alpha: float,
    ) -> Dict[str, Any]:
        """Run one finite training calculation without mutating optimizer state."""
        use_response_terms = cfg.mode != "base"
        need_energy = bool(cfg.w_energy > 0.0 and _batch_has_label(batch, "energy"))
        need_forces = bool(cfg.w_forces > 0.0 and _batch_has_label(batch, "forces"))
        need_mu = bool(cfg.w_dipole > 0.0 and _batch_has_label(batch, "dipole"))
        need_alpha = bool(
            cfg.w_polarizability > 0.0
            and _batch_has_label(batch, "polarizability")
        )
        need_bec = bool(cfg.w_bec > 0.0 and _batch_has_label(batch, "bec"))
        batch_use_spin = bool(
            isinstance(model, MixedGranularityE3GNN)
            and cfg.model.enable_spin
            and _batch_has_label(batch, "spins")
        )
        options: Dict[str, Any] = {
            "training": True,
            "compute_forces": need_forces,
            "compute_bec": need_bec,
            "use_response_terms": use_response_terms,
            "retain_graph": need_forces,
        }
        if isinstance(model, MixedGranularityE3GNN):
            options["use_spin_terms"] = batch_use_spin
        _prepare_retry_batch(batch)
        try:
            out = model(batch, **options)
        except Exception as exc:
            if _is_isolatable_numerical_exception(exc):
                raise _BadSampleError("forward_exception", str(exc)) from exc
            raise
        bad_outputs = _nonfinite_output_names(out)
        if bad_outputs:
            del out
            raise _BadSampleError(
                "nonfinite_forward", f"non-finite outputs={bad_outputs}"
            )

        loss = torch.zeros(
            (), dtype=batch.positions.dtype, device=batch.positions.device
        )
        metrics: Dict[str, Any] = {
            "energy": (0.0, 0),
            "forces": (0.0, 0),
            "extra": {},
        }
        try:
            if need_energy:
                target_energy = batch.energy.to(out["energy"].dtype)
                if target_energy.ndim == 0:
                    target_energy = target_energy.unsqueeze(0)
                atoms_per_graph = (
                    (batch.ptr[1:] - batch.ptr[:-1]).to(target_energy.dtype)
                    if hasattr(batch, "ptr") and batch.ptr.numel() > 1
                    else torch.ones(
                        target_energy.numel(),
                        dtype=target_energy.dtype,
                        device=target_energy.device,
                    )
                )
                energy_weight = _expanded_property_weight(
                    batch, "energy", out["energy"], atomwise=False
                )
                loss = loss + float(cfg.w_energy) * _weighted_mse(
                    out["energy"] / atoms_per_graph,
                    target_energy / atoms_per_graph,
                    energy_weight,
                )
                metrics["energy"] = _masked_mae_statistics(
                    out["energy"] / atoms_per_graph,
                    target_energy / atoms_per_graph,
                    energy_weight,
                )
            if need_forces:
                target_forces = batch.forces.to(out["forces"].dtype)
                force_weight = _expanded_property_weight(
                    batch, "forces", out["forces"], atomwise=True
                )
                loss = loss + float(cfg.w_forces) * _configured_force_loss(
                    out["forces"], target_forces, force_weight, cfg
                )
                metrics["forces"] = _masked_mae_statistics(
                    out["forces"], target_forces, force_weight
                )
            if need_mu:
                target_mu = (
                    batch.dipole.squeeze(1)
                    if batch.dipole.ndim == 3 else batch.dipole
                )
                mu_weight = _expanded_property_weight(
                    batch, "dipole", out["dipole"], atomwise=False
                )
                target_mu = target_mu.to(out["dipole"].dtype)
                loss = loss + response_weight_mu * _weighted_mse(
                    out["dipole"], target_mu, mu_weight
                )
                metrics["extra"]["dipole"] = _masked_mae_statistics(
                    out["dipole"], target_mu, mu_weight
                )
            if need_alpha:
                target_alpha = (
                    batch.polarizability.squeeze(1)
                    if batch.polarizability.ndim == 4
                    else batch.polarizability
                )
                alpha_weight = _expanded_property_weight(
                    batch,
                    "polarizability",
                    out["polarizability"],
                    atomwise=False,
                )
                target_alpha = target_alpha.to(out["polarizability"].dtype)
                loss = loss + response_weight_alpha * _weighted_mse(
                    out["polarizability"], target_alpha, alpha_weight
                )
                metrics["extra"]["polarizability"] = _masked_mae_statistics(
                    out["polarizability"], target_alpha, alpha_weight
                )
            additional_loss, additional_metrics = _additional_physics_loss(
                out, batch, cfg
            )
            loss = loss + additional_loss
            metrics["extra"].update(additional_metrics)
        except Exception as exc:
            del loss, out
            if _is_isolatable_numerical_exception(exc):
                raise _BadSampleError("loss_exception", str(exc)) from exc
            raise
        if not bool(torch.isfinite(loss.detach()).all().cpu()):
            del loss, out
            raise _BadSampleError("nonfinite_loss", "loss assembly is non-finite")
        if loss.requires_grad:
            try:
                loss.backward()
            except Exception as exc:
                del loss, out
                if _is_isolatable_numerical_exception(exc):
                    raise _BadSampleError("backward_exception", str(exc)) from exc
                raise
            bad_parameters = _nonfinite_gradient_parameters(model)
            if bad_parameters:
                del loss, out
                raise _BadSampleError(
                    "nonfinite_gradient", f"parameters={bad_parameters}"
                )
            grad_norm = _clip_grad_norm_stable(
                model.parameters(), float(cfg.grad_clip_norm)
            )
            if not math.isfinite(grad_norm):
                del loss, out
                raise _BadSampleError(
                    "gradient_norm_overflow",
                    "individual gradients are finite but their norm overflowed",
                )
        metrics["loss"] = float(loss.detach().cpu())
        del loss, out
        return metrics

    def _validation_batch_is_finite(batch: Any) -> None:
        """Probe validation numerics without changing metric accumulators."""
        use_response_terms = cfg.mode != "base"
        need_forces = bool(
            (cfg.w_forces > 0.0 or "forces" in _validation_targets)
            and _batch_has_label(batch, "forces")
        )
        need_bec = bool(
            (cfg.w_bec > 0.0 or "bec" in _validation_targets)
            and _batch_has_label(batch, "bec")
        )
        batch_use_spin = bool(
            isinstance(model, MixedGranularityE3GNN)
            and cfg.model.enable_spin
            and _batch_has_label(batch, "spins")
        )
        options: Dict[str, Any] = {
            "training": False,
            "compute_forces": need_forces,
            "compute_bec": need_bec,
            "use_response_terms": use_response_terms,
            "retain_graph": False,
        }
        if isinstance(model, MixedGranularityE3GNN):
            options["use_spin_terms"] = batch_use_spin
        try:
            with torch.set_grad_enabled(need_forces or need_bec or batch_use_spin):
                probe = model(batch, **options)
        except Exception as exc:
            if _is_isolatable_numerical_exception(exc):
                raise _BadSampleError("validation_forward_exception", str(exc)) from exc
            raise
        bad_outputs = _nonfinite_output_names(probe)
        del probe
        if bad_outputs:
            raise _BadSampleError(
                "nonfinite_validation_forward", f"non-finite outputs={bad_outputs}"
            )

    def _validation_forward_with_quarantine(
        batch: Any,
        *,
        options: Dict[str, Any],
        sample_ids: Sequence[str],
        epoch: int,
        step: int,
    ) -> Tuple[Optional[Any], Optional[Dict[str, torch.Tensor]]]:
        """Run validation once, isolating only individually reproducible faults."""
        def calculate(selected: Any) -> Dict[str, torch.Tensor]:
            try:
                prediction = model(selected, **options)
            except Exception as exc:
                if _is_isolatable_numerical_exception(exc):
                    raise _BadSampleError(
                        "validation_forward_exception", str(exc)
                    ) from exc
                raise
            bad_outputs = _nonfinite_output_names(prediction)
            if bad_outputs:
                del prediction
                raise _BadSampleError(
                    "nonfinite_validation_forward",
                    f"non-finite outputs={bad_outputs}",
                )
            return prediction

        try:
            return batch, calculate(batch)
        except _BadSampleError as batch_error:
            if not bool(getattr(cfg, "skip_bad_samples", True)):
                raise FloatingPointError(
                    f"{batch_error.kind} at validation epoch={epoch}, step={step}; "
                    f"{_batch_structure_summary(batch)}; {batch_error.detail}"
                ) from batch_error
            graphs = _split_graph_batch(batch)
            valid_graphs: List[AtomicData] = []
            invalid_ids: List[str] = []
            for graph_index, graph in enumerate(graphs):
                sample_id = (
                    str(sample_ids[graph_index])
                    if graph_index < len(sample_ids)
                    else f"validation-{epoch}-{step}-{graph_index}"
                )
                single = _TGBatch.from_data_list([graph]).to(device)
                try:
                    _validation_batch_is_finite(single)
                    valid_graphs.append(graph)
                except _BadSampleError as sample_error:
                    _record_bad_sample(
                        sample_id,
                        epoch=epoch,
                        step=step,
                        phase="validation",
                        reason=sample_error,
                    )
                    invalid_ids.append(sample_id)
                finally:
                    del single
            if not invalid_ids:
                del graphs, valid_graphs
                raise FloatingPointError(
                    f"Validation batch failed at epoch={epoch}, step={step}, but "
                    "every structure is finite when evaluated independently. This "
                    "is a systemic batching/backend failure and will not be hidden "
                    "by skipping scientific records."
                ) from batch_error
            log(
                f"[{_now()}] WARN: excluded {len(invalid_ids)} individually "
                f"invalid validation structure(s) at epoch={epoch}, step={step}: "
                f"{invalid_ids[:8]}."
            )
            del batch, graphs
            if not valid_graphs:
                return None, None
            rebuilt = _TGBatch.from_data_list(valid_graphs).to(device)
            del valid_graphs
            try:
                return rebuilt, calculate(rebuilt)
            except _BadSampleError as residual_error:
                del rebuilt
                raise FloatingPointError(
                    f"Validation remained non-finite after removing individually "
                    f"reproducible bad samples at epoch={epoch}, step={step}; "
                    f"{residual_error.detail}"
                ) from residual_error

    # ------------------------------------------------------------------
    # Per-epoch artifact setup: checkpoints, regression plots, MAE chart.
    # Skipped when save_epoch_artifacts=False (e.g. AutoSearch trials).
    # ------------------------------------------------------------------
    _out_p_base = Path(str(cfg.out_ckpt)).expanduser()
    if not _out_p_base.is_absolute():
        _out_p_base = Path(__file__).resolve().parent / _out_p_base
    # Use the checkpoint stem as the subdirectory name so base/response/joint
    # stages each get their own folder (e.g. train/model_base/, train/model_resp/).
    _train_dir = _out_p_base.parent / "train" / _out_p_base.stem
    _plots_dir = _train_dir / "plots"
    _epoch_emae_hist: List[float] = []
    _epoch_fmae_hist: List[float] = []
    _epoch_force_stats: List[Dict[str, float]] = []
    _epoch_multitask_hist: Dict[str, Dict[str, List[float]]] = {}
    _epoch_residual_hist: Dict[str, List[float]] = {}
    _epoch_memory_hist: List[Dict[str, float]] = []
    _HAS_MPL = False
    _scatter_clip_lo = 2.0
    _scatter_clip_hi = 98.0
    if cfg.save_epoch_artifacts:
        _train_dir.mkdir(parents=True, exist_ok=True)
        _plots_dir.mkdir(parents=True, exist_ok=True)
    if cfg.save_epoch_artifacts and bool(getattr(cfg, "save_epoch_plots", True)):
        try:
            import matplotlib                          # type: ignore[import]
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt           # type: ignore[import]
            _HAS_MPL = True
        except ImportError:
            log(f"[{_now()}] WARN: matplotlib not available — per-epoch plots disabled")

    def _subsample_pairs(
        actual: np.ndarray,
        pred: np.ndarray,
        *,
        max_points: int,
        seed: int,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Keep at most ``max_points`` paired samples for lightweight plotting."""
        if actual.size <= max_points or pred.size <= max_points:
            return actual, pred
        ridx = np.random.default_rng(seed).choice(actual.size, max_points, replace=False)
        return actual[ridx], pred[ridx]

    def _global_limits(actual: np.ndarray, pred: np.ndarray) -> Tuple[float, float]:
        """Return a symmetric plotting range that covers both axes."""
        lo = float(min(actual.min(), pred.min()))
        hi = float(max(actual.max(), pred.max()))
        if not np.isfinite(lo) or not np.isfinite(hi):
            return -1.0, 1.0
        if hi <= lo:
            pad = max(1e-6, abs(lo) * 0.05 + 1e-6)
            return lo - pad, hi + pad
        pad = 0.03 * (hi - lo)
        return lo - pad, hi + pad

    def _clipped_pairs(
        actual: np.ndarray,
        pred: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray, int, Tuple[float, float]]:
        """Clip scatter pairs to the central percentile window of the actual values."""
        lo = float(np.percentile(actual, _scatter_clip_lo))
        hi = float(np.percentile(actual, _scatter_clip_hi))
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            return actual, pred, 0, _global_limits(actual, pred)
        in_view = (
            (actual >= lo) & (actual <= hi) &
            (pred >= lo) & (pred <= hi)
        )
        hidden = int((~in_view).sum())
        if not np.any(in_view):
            return actual, pred, 0, _global_limits(actual, pred)
        return actual[in_view], pred[in_view], hidden, (lo, hi)

    def _plot_regression_panel(
        ax,
        *,
        actual: Optional[np.ndarray],
        pred: Optional[np.ndarray],
        color: str,
        xlabel: str,
        ylabel: str,
        title: str,
        limits: Optional[Tuple[float, float]] = None,
        point_size: float = 8.0,
        point_alpha: float = 0.35,
    ) -> None:
        """Draw one actual-vs-predicted regression scatter panel."""
        if actual is None or pred is None or actual.size == 0 or pred.size == 0:
            ax.text(0.5, 0.5, "No validation data", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.2)
            return
        lo, hi = limits if limits is not None else _global_limits(actual, pred)
        ax.scatter(actual, pred, s=point_size, alpha=point_alpha, color=color, edgecolors="none")
        ax.plot([lo, hi], [lo, hi], "--", color="#111111", lw=1.0)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, alpha=0.25)
        try:
            ax.set_aspect("equal", adjustable="box")
        except Exception:
            pass

    def _stream_mean_std(sum_v: float, sq_sum_v: float, count_v: int) -> Tuple[float, float]:
        """Recover mean/std from streaming accumulators without storing all samples."""
        if count_v <= 0:
            return float("nan"), float("nan")
        mean_v = float(sum_v) / float(count_v)
        var_v = max(0.0, float(sq_sum_v) / float(count_v) - mean_v * mean_v)
        return mean_v, math.sqrt(var_v)

    if train_data:
        loader = _make_loader(train_data, shuffle=True)
        v_loader = _make_loader(val_data, shuffle=False)
    else:
        loader = _make_loader([], shuffle=True)
        v_loader = _make_loader([], shuffle=False)
    def _log_mps_batch_plan(name: str, selected_loader: Any, count: int) -> None:
        sampler = getattr(selected_loader, "batch_sampler", None)
        edge_loads = getattr(sampler, "edge_loads", None)
        structure_loads = getattr(sampler, "structure_loads", None)
        if not edge_loads or not structure_loads:
            return
        requested_bs = int(getattr(sampler, "requested_batch_size", cfg.batch_size))
        edge_budget = int(getattr(sampler, "edge_budget", 0))
        structure_only_steps = int(math.ceil(count / requested_bs)) if count else 0
        extra_edge_steps = max(0, len(structure_loads) - structure_only_steps)
        full_steps = sum(int(size >= requested_bs) for size in structure_loads)
        underfilled_steps = len(structure_loads) - full_steps
        oversized = int(getattr(sampler, "oversized_structures", 0))
        log(
            f"[{_now()}] Batch plan [mps/{name}]: requested_structures={requested_bs} "
            f"steps={len(structure_loads)} structure_only_steps={structure_only_steps} "
            f"extra_edge_budget_steps={extra_edge_steps}; "
            f"structures/step mean={np.mean(structure_loads):.2f} "
            f"min={min(structure_loads)} max={max(structure_loads)}; "
            f"edge_budget={edge_budget} edges/step mean={np.mean(edge_loads):.0f} "
            f"max={max(edge_loads)}; full_steps={full_steps} "
            f"underfilled_steps={underfilled_steps} "
            f"oversized_single_structures={oversized}."
        )

    if device.type == "mps":
        _log_mps_batch_plan("train", loader, len(train_data))
        _log_mps_batch_plan("validation", v_loader, len(val_data))
        log(
            f"[{_now()}] MPS batching uses exact graphs and all structures; "
            "the edge budget only bounds unified-memory work per step."
        )
    else:
        _effective_bs = max(
            1, min(int(cfg.batch_size), len(train_data) if train_data else 1)
        )
        log(
            f"[{_now()}] Batch plan [{device.type}]: "
            f"requested_structures={int(cfg.batch_size)} "
            f"effective_structures={_effective_bs} steps={len(loader)}; "
            "standard structure-count batching (no edge-budget split)."
        )

    for epoch in range(1, int(cfg.epochs) + 1):
        if stop_flag and stop_flag():
            stopped = True
            break

        # End warmup by reintroducing the ground branch into optimization.
        if not _warmup_done and epoch > getattr(cfg, "warmup_freeze_epochs", 0):
            model.unfreeze_ground()
            _ground_ps = [p for p in model.ground.parameters() if p.requires_grad]
            opt.add_param_group({"params": _ground_ps, "lr": _lr_g})
            _warmup_done = True
            log(f"[{_now()}] Warmup done — base unfrozen at epoch {epoch}")
            if _sched is not None:
                from torch.optim.lr_scheduler import CosineAnnealingLR as _CosLR
                _sched = _CosLR(opt, T_max=max(1, int(cfg.epochs) - epoch + 1), eta_min=1e-7)

        # Linearly ramp response-target weights when requested.
        _t = (epoch - 1) / max(1, int(cfg.epochs) - 1)
        _w_mu = float(cfg.w_dipole) + _t * (
            float(cfg.w_dipole_final) - float(cfg.w_dipole)
            if cfg.w_dipole_final is not None else 0.0
        )
        _w_alpha = float(cfg.w_polarizability) + _t * (
            float(cfg.w_polarizability_final) - float(cfg.w_polarizability)
            if cfg.w_polarizability_final is not None else 0.0
        )

        model.train()
        train_loss = 0.0
        train_fmae_sum = 0.0;  train_fmae_n = 0
        train_emae_sum = 0.0;  train_emae_n = 0
        train_extra_metrics: Dict[str, List[float]] = {}
        n_steps = max(1, len(loader))
        total_steps_global = int(cfg.epochs) * int(n_steps)
        for step, batch in enumerate(loader, start=1):
            if stop_flag and stop_flag():
                stopped = True
                break
            if batch is None:
                if not bool(getattr(cfg, "skip_bad_samples", True)):
                    raise FloatingPointError(
                        "A training batch contains only non-finite input records"
                    )
                _enforce_bad_sample_limit()
                continue
            _enforce_bad_sample_limit()
            original_graphs: Optional[List[AtomicData]] = None
            original_ids = _batch_structure_ids(batch)
            batch = batch.to(device)
            opt.zero_grad(set_to_none=True)
            try:
                result = _forward_loss_backward(
                    batch,
                    response_weight_mu=_w_mu,
                    response_weight_alpha=_w_alpha,
                )
                _checked_optimizer_step()
                _consecutive_bad_batches = 0
                accepted_results = [result]
            except _BadSampleError as batch_error:
                opt.zero_grad(set_to_none=True)
                retry_error = batch_error
                accepted_results = []
                # A backend/kernel fault can be transient. Retry the untouched
                # batch once before classifying any scientific record as bad.
                if _max_nonfinite_recoveries > 0:
                    _release_mps_cache()
                    try:
                        result = _forward_loss_backward(
                            batch,
                            response_weight_mu=_w_mu,
                            response_weight_alpha=_w_alpha,
                        )
                        _checked_optimizer_step()
                        accepted_results = [result]
                        _consecutive_bad_batches = 0
                        recovery = {
                            "epoch": int(epoch),
                            "step": int(step),
                            "attempt": 1,
                            "source": "same unchanged batch/model state",
                            "outputs": [batch_error.kind],
                            "learning_rates": [
                                float(group["lr"]) for group in opt.param_groups
                            ],
                        }
                        _numerical_recoveries.append(recovery)
                        log(
                            f"[{_now()}] Numerical recovery "
                            f"{len(_numerical_recoveries)}: epoch={epoch} "
                            f"step={step}, transient {batch_error.kind}; "
                            "retrying the same batch succeeded."
                        )
                    except _BadSampleError as repeated_error:
                        opt.zero_grad(set_to_none=True)
                        retry_error = repeated_error
                if accepted_results:
                    pass
                elif not bool(getattr(cfg, "skip_bad_samples", True)):
                    raise FloatingPointError(
                        f"{retry_error.kind} at epoch={epoch}, step={step}. "
                        f"{_batch_structure_summary(batch)}; {retry_error.detail}"
                    ) from retry_error
                if accepted_results:
                    original_graphs = None
                else:
                    original_graphs = _split_graph_batch(batch)
                del batch
                _release_mps_cache()
                newly_bad: List[str] = []
                for graph_index, graph in enumerate(original_graphs or []):
                    sample_id = (
                        original_ids[graph_index]
                        if graph_index < len(original_ids)
                        else f"epoch-{epoch}-step-{step}-graph-{graph_index}"
                    )
                    if sample_id in _bad_samples:
                        _record_bad_sample(
                            sample_id,
                            epoch=epoch,
                            step=step,
                            phase="train",
                            reason=retry_error,
                        )
                        continue
                    single = _TGBatch.from_data_list([graph]).to(device)
                    opt.zero_grad(set_to_none=True)
                    try:
                        single_result = _forward_loss_backward(
                            single,
                            response_weight_mu=_w_mu,
                            response_weight_alpha=_w_alpha,
                        )
                        _checked_optimizer_step()
                        accepted_results.append(single_result)
                    except _BadSampleError as sample_error:
                        opt.zero_grad(set_to_none=True)
                        _record_bad_sample(
                            sample_id,
                            epoch=epoch,
                            step=step,
                            phase="train",
                            reason=sample_error,
                        )
                        newly_bad.append(sample_id)
                    finally:
                        del single
                        _release_mps_cache()
                if newly_bad:
                    log(
                        f"[{_now()}] WARN: isolated and skipped {len(newly_bad)} "
                        f"invalid structure(s) at epoch={epoch}, step={step}: "
                        f"{newly_bad[:8]}; batch_failure={batch_error.kind}."
                    )
                    if progress is not None:
                        progress(
                            {
                                "type": "bad_samples",
                                "epoch": int(epoch),
                                "step": int(step),
                                "sample_ids": list(newly_bad),
                                "unique_bad_samples": len(_bad_samples),
                            }
                        )
                _enforce_bad_sample_limit()
                if accepted_results:
                    _consecutive_bad_batches = 0
                else:
                    _consecutive_bad_batches += 1
                    if _consecutive_bad_batches >= 8:
                        raise FloatingPointError(
                            "Eight consecutive batches contained no numerically valid "
                            "structures; refusing to mask a systematic divergence."
                        )

            if accepted_results:
                train_loss += float(np.mean(
                    [float(result["loss"]) for result in accepted_results]
                ))
            for result in accepted_results:
                energy_sum, energy_count = result["energy"]
                force_sum, force_count = result["forces"]
                train_emae_sum += float(energy_sum)
                train_emae_n += int(energy_count)
                train_fmae_sum += float(force_sum)
                train_fmae_n += int(force_count)
                for name, (value_sum, value_count) in result["extra"].items():
                    accumulator = train_extra_metrics.setdefault(name, [0.0, 0.0])
                    accumulator[0] += float(value_sum)
                    accumulator[1] += float(value_count)
            accepted_results.clear()
            if original_graphs is not None:
                del original_graphs
            if "batch" in locals():
                del batch

            if progress is not None:
                # Convert epoch / step progress into a single overall fraction.
                frac_epoch = (float(epoch - 1) + float(step) / float(n_steps)) / float(max(1, int(cfg.epochs)))
                frac = prog_train_base + prog_train_span * frac_epoch
                steps_done = int((epoch - 1) * n_steps + step)
                elapsed_s = float(time.time() - t0)
                avg_step = elapsed_s / float(max(1, steps_done))
                eta_s = avg_step * float(max(0, total_steps_global - steps_done))
                progress(
                    {
                        "type": "train",
                        "overall_frac": float(max(0.0, min(1.0, frac))),
                        "epoch": int(epoch),
                        "epochs": int(cfg.epochs),
                        "step": int(step),
                        "steps": int(n_steps),
                        "elapsed_s": elapsed_s,
                        "eta_s": float(eta_s),
                    }
                )
        if stopped:
            break

        # Validation pass.
        model.eval()
        val_loss = 0.0
        val_fmae_sum = 0.0;  val_fmae_n = 0
        val_emae_sum = 0.0;  val_emae_n = 0
        val_step = 0
        val_e_actual_buf: List[np.ndarray] = []
        val_e_pred_buf:   List[np.ndarray] = []
        val_f_actual_buf: List[np.ndarray] = []
        val_f_pred_buf:   List[np.ndarray] = []
        val_fn_actual_buf: List[np.ndarray] = []
        val_fn_pred_buf:   List[np.ndarray] = []
        val_f_pred_sum = 0.0;      val_f_pred_sq_sum = 0.0;      val_f_pred_maxabs = 0.0;      val_f_pred_n = 0
        val_f_actual_sum = 0.0;    val_f_actual_sq_sum = 0.0;    val_f_actual_maxabs = 0.0;    val_f_actual_n = 0
        val_fn_pred_sum = 0.0;     val_fn_pred_sq_sum = 0.0;     val_fn_pred_max = 0.0;        val_fn_pred_n = 0
        val_fn_actual_sum = 0.0;   val_fn_actual_sq_sum = 0.0;   val_fn_actual_max = 0.0;      val_fn_actual_n = 0
        val_fnorm_mae_sum = 0.0;   val_fnorm_mae_n = 0
        val_extra_metrics: Dict[str, List[float]] = {}
        val_residual_max: Dict[str, float] = {}
        val_batches_used = 0
        for batch in v_loader:
            if stop_flag and stop_flag():
                stopped = True
                break
            if batch is None:
                if not bool(getattr(cfg, "skip_bad_samples", True)):
                    raise FloatingPointError(
                        "A validation batch contains only non-finite input records"
                    )
                continue
            val_step += 1
            if progress is not None:
                progress({
                    "type":   "val",
                    "epoch":  int(epoch),
                    "epochs": int(cfg.epochs),
                    "step":   int(val_step),
                    "steps":  int(len(v_loader)),
                })
            validation_ids = _batch_structure_ids(batch)
            batch = batch.to(device)
            use_response_terms = (cfg.mode != "base")
            need_energy = bool(
                (cfg.w_energy > 0.0 or "energy" in _validation_targets)
                and _batch_has_label(batch, "energy")
            )
            need_forces = bool(
                (cfg.w_forces > 0.0 or "forces" in _validation_targets)
                and _batch_has_label(batch, "forces")
            )
            need_mu = bool(
                (cfg.w_dipole > 0.0 or "dipole" in _validation_targets)
                and _batch_has_label(batch, "dipole")
            )
            need_alpha = bool(
                (cfg.w_polarizability > 0.0 or "polarizability" in _validation_targets)
                and _batch_has_label(batch, "polarizability")
            )
            need_bec = bool(
                (cfg.w_bec > 0.0 or "bec" in _validation_targets)
                and _batch_has_label(batch, "bec")
            )
            compute_forces = bool(need_forces)
            batch_use_spin = bool(
                isinstance(model, MixedGranularityE3GNN)
                and cfg.model.enable_spin
                and _batch_has_label(batch, "spins")
            )
            need_internal_grad = bool(
                compute_forces
                or need_bec
                or batch_use_spin
            )
            with torch.set_grad_enabled(need_internal_grad):
                forward_options = {
                    "training": False,
                    "compute_forces": compute_forces,
                    "compute_bec": need_bec,
                    "use_response_terms": use_response_terms,
                    "retain_graph": False,
                }
                if isinstance(model, MixedGranularityE3GNN):
                    forward_options["use_spin_terms"] = batch_use_spin
                batch, out = _validation_forward_with_quarantine(
                    batch,
                    options=forward_options,
                    sample_ids=validation_ids,
                    epoch=epoch,
                    step=val_step,
                )
                if batch is None or out is None:
                    _release_mps_cache()
                    continue
                l = torch.zeros((), dtype=batch.positions.dtype, device=batch.positions.device)
                if need_energy:
                    y_e = batch.energy.to(out["energy"].dtype)
                    if y_e.ndim == 0:
                        y_e = y_e.unsqueeze(0)
                    # Per-atom normalisation (same as training loss).
                    if hasattr(batch, "ptr") and batch.ptr.numel() > 1:
                        _npa_val = (batch.ptr[1:] - batch.ptr[:-1]).to(y_e.dtype)
                    else:
                        _npa_val = torch.ones(y_e.numel(), dtype=y_e.dtype, device=y_e.device)
                    w_e = _expanded_property_weight(batch, "energy", out["energy"], atomwise=False)
                    if float(cfg.w_energy) > 0.0:
                        l = l + float(cfg.w_energy) * _weighted_mse(
                            out["energy"] / _npa_val, y_e / _npa_val, w_e
                        )
                    _sum, _count = _masked_mae_statistics(
                        out["energy"] / _npa_val, y_e / _npa_val, w_e
                    )
                    val_emae_sum += _sum
                    val_emae_n += _count
                    if _HAS_MPL:
                        # Store E/atom so the scatter plot is comparable across system sizes.
                        _npa_np = _npa_val.detach().cpu().numpy().ravel()
                        _mask_e = w_e.detach().cpu().numpy().ravel() > 0.0
                        val_e_actual_buf.append(y_e.detach().cpu().numpy().ravel()[_mask_e] / _npa_np[_mask_e])
                        val_e_pred_buf.append(out["energy"].detach().cpu().numpy().ravel()[_mask_e] / _npa_np[_mask_e])
                if need_forces:
                    y_f = batch.forces.to(out["forces"].dtype)
                    w_f = _expanded_property_weight(batch, "forces", out["forces"], atomwise=True)
                    if float(cfg.w_forces) > 0.0:
                        l = l + float(cfg.w_forces) * _configured_force_loss(
                            out["forces"], y_f, w_f, cfg
                        )
                    _f_pred = out["forces"].detach()
                    _f_true = y_f.detach()
                    _sum, _count = _masked_mae_statistics(_f_pred, _f_true, w_f)
                    val_fmae_sum += _sum
                    val_fmae_n += _count
                    _labeled_atoms = w_f > 0.0
                    _labeled_weights = w_f[_labeled_atoms]
                    _f_pred_labeled = _f_pred[_labeled_atoms]
                    _f_true_labeled = _f_true[_labeled_atoms]
                    _f_pred_flat = _f_pred_labeled.reshape(-1)
                    _f_true_flat = _f_true_labeled.reshape(-1)
                    val_f_pred_sum += float(_f_pred_flat.sum())
                    val_f_pred_sq_sum += float(torch.sum(_f_pred_flat * _f_pred_flat))
                    val_f_pred_maxabs = max(val_f_pred_maxabs, float(_f_pred_flat.abs().max()))
                    val_f_pred_n += int(_f_pred_flat.numel())
                    val_f_actual_sum += float(_f_true_flat.sum())
                    val_f_actual_sq_sum += float(torch.sum(_f_true_flat * _f_true_flat))
                    val_f_actual_maxabs = max(val_f_actual_maxabs, float(_f_true_flat.abs().max()))
                    val_f_actual_n += int(_f_true_flat.numel())

                    _fn_pred = torch.linalg.norm(_f_pred_labeled, dim=-1)
                    _fn_true = torch.linalg.norm(_f_true_labeled, dim=-1)
                    val_fn_pred_sum += float(_fn_pred.sum())
                    val_fn_pred_sq_sum += float(torch.sum(_fn_pred * _fn_pred))
                    val_fn_pred_max = max(val_fn_pred_max, float(_fn_pred.max()))
                    val_fn_pred_n += int(_fn_pred.numel())
                    val_fn_actual_sum += float(_fn_true.sum())
                    val_fn_actual_sq_sum += float(torch.sum(_fn_true * _fn_true))
                    val_fn_actual_max = max(val_fn_actual_max, float(_fn_true.max()))
                    val_fn_actual_n += int(_fn_true.numel())
                    val_fnorm_mae_sum += float(
                        ((_fn_pred - _fn_true).abs() * _labeled_weights).sum().detach()
                    )
                    val_fnorm_mae_n += int(_fn_pred.numel())
                    if _HAS_MPL:
                        val_f_actual_buf.append(_f_true_labeled.cpu().numpy().ravel())
                        val_f_pred_buf.append(_f_pred_labeled.cpu().numpy().ravel())
                        val_fn_actual_buf.append(_fn_true.cpu().numpy().ravel())
                        val_fn_pred_buf.append(_fn_pred.cpu().numpy().ravel())
                if need_mu:
                    y_mu = batch.dipole.squeeze(1) if batch.dipole.ndim == 3 else batch.dipole
                    w_mu = _expanded_property_weight(batch, "dipole", out["dipole"], atomwise=False)
                    if _w_mu > 0.0:
                        l = l + _w_mu * _weighted_mse(
                            out["dipole"], y_mu.to(out["dipole"].dtype), w_mu
                        )
                    _sum, _count = _masked_mae_statistics(
                        out["dipole"], y_mu.to(out["dipole"].dtype), w_mu
                    )
                    _acc = val_extra_metrics.setdefault("dipole", [0.0, 0.0])
                    _acc[0] += _sum
                    _acc[1] += _count
                if need_alpha:
                    y_a = batch.polarizability.squeeze(1) if batch.polarizability.ndim == 4 else batch.polarizability
                    w_a = _expanded_property_weight(
                        batch, "polarizability", out["polarizability"], atomwise=False
                    )
                    if _w_alpha > 0.0:
                        l = l + _w_alpha * _weighted_mse(
                            out["polarizability"], y_a.to(out["polarizability"].dtype), w_a
                        )
                    _sum, _count = _masked_mae_statistics(
                        out["polarizability"], y_a.to(out["polarizability"].dtype), w_a
                    )
                    _acc = val_extra_metrics.setdefault("polarizability", [0.0, 0.0])
                    _acc[0] += _sum
                    _acc[1] += _count
                additional_loss, additional_metrics = _additional_physics_loss(
                    out, batch, cfg, metric_targets=_validation_targets
                )
                l = l + additional_loss
                for name, (value_sum, value_count) in additional_metrics.items():
                    accumulator = val_extra_metrics.setdefault(name, [0.0, 0.0])
                    accumulator[0] += value_sum
                    accumulator[1] += value_count
                for residual_name in (
                    "qeq_residual", "qeq_stability_shift", "deq_residual",
                    "deq_stability_shift",
                    "deq_iterations", "coupling_residual",
                ):
                    if residual_name in out:
                        value = float(torch.max(torch.abs(out[residual_name].detach())).cpu())
                        val_residual_max[residual_name] = max(
                            val_residual_max.get(residual_name, 0.0), value
                        )
                if not bool(torch.isfinite(l.detach()).all().cpu()):
                    raise FloatingPointError(
                        f"Validation loss assembly is non-finite at epoch={epoch}, "
                        f"step={val_step} despite finite model outputs; "
                        "check active label units and loss weights."
                    )
                val_loss += float(l.detach().cpu().item())
                val_batches_used += 1
            del l, out, batch
        if stopped:
            break

        if val_batches_used <= 0:
            raise FloatingPointError(
                "Validation contains no numerically valid structures; refusing "
                "to create a checkpoint from training-only metrics."
            )
        _final_val_loss = val_loss / float(val_batches_used)
        _final_val_fmae = (val_fmae_sum / val_fmae_n) if val_fmae_n > 0 else float("nan")
        _final_val_emae = (val_emae_sum / val_emae_n) if val_emae_n > 0 else float("nan")
        _final_val_fnorm_mae = (val_fnorm_mae_sum / val_fnorm_mae_n) if val_fnorm_mae_n > 0 else float("nan")
        validation_terms: List[float] = []
        if val_emae_n > 0:
            validation_terms.append(_final_val_emae / VALIDATION_MAE_SCALES["energy"])
        if val_fmae_n > 0:
            validation_terms.append(_final_val_fmae / VALIDATION_MAE_SCALES["forces"])
        for metric_name, (metric_sum, metric_count) in val_extra_metrics.items():
            if metric_count > 0:
                scale = VALIDATION_MAE_SCALES.get(metric_name, 1.0)
                validation_terms.append((metric_sum / metric_count) / scale)
        _epoch_validation_score = (
            float(np.mean(validation_terms)) if validation_terms else _final_val_loss
        )
        if not math.isfinite(_epoch_validation_score):
            raise FloatingPointError(
                f"Non-finite normalized validation score at epoch={epoch}; "
                "no checkpoint will be saved."
            )
        # Select checkpoints with the same normalized multi-task metric used by
        # AutoSearch; raw weighted loss is not comparable across task weights.
        _early_stopping_delta = max(
            0.0, float(getattr(cfg, "early_stopping_min_delta", 0.0))
        )
        _previous_best_validation_score = _best_validation_score
        if _epoch_validation_score < _best_validation_score:
            _best_val_loss = _final_val_loss
            _best_validation_score = _epoch_validation_score
            _best_epoch = int(epoch)
            _best_state = {
                name: value.detach().cpu().clone() for name, value in model.state_dict().items()
            }
        _last_validated_state = {
            name: value.detach().cpu().clone() for name, value in model.state_dict().items()
        }
        _last_validated_epoch = int(epoch)
        if (
            _epoch_validation_score
            < _previous_best_validation_score - _early_stopping_delta
        ):
            _epochs_without_improvement = 0
        else:
            _epochs_without_improvement += 1
        _ep_str = (f"Epoch {epoch}: Train={train_loss/max(1,len(loader)):.4f} "
                   f"Val={_final_val_loss:.4f}")
        if val_emae_n > 0 or val_fmae_n > 0:
            _ep_str += "  |"
        if val_emae_n > 0:
            _ep_str += (f"  E/atom-MAE  tr={train_emae_sum/max(1,train_emae_n):.4f}"
                        f"  val={_final_val_emae:.4f}  eV/atom")
        if val_fmae_n > 0:
            _ep_str += (f"  F-MAE  tr={train_fmae_sum/max(1,train_fmae_n):.4f}"
                        f"  val={_final_val_fmae:.4f}  eV/Å")
        for metric_name in sorted(val_extra_metrics):
            val_sum, val_count = val_extra_metrics[metric_name]
            train_sum, train_count = train_extra_metrics.get(metric_name, [0.0, 0.0])
            if val_count > 0:
                _ep_str += (
                    f"  {metric_name}-MAE tr={train_sum/max(1.0, train_count):.4g}"
                    f" val={val_sum/max(1.0, val_count):.4g}"
                )
                history = _epoch_multitask_hist.setdefault(
                    metric_name, {"train": [], "val": []}
                )
                history["train"].append(train_sum / max(1.0, train_count))
                history["val"].append(val_sum / max(1.0, val_count))
        for residual_name, value in val_residual_max.items():
            _epoch_residual_hist.setdefault(residual_name, []).append(value)
        log(_ep_str)
        if val_residual_max:
            log(
                f"[{_now()}] Physics epoch {epoch}: "
                + " ".join(
                    f"{name}={value:.4g}"
                    for name, value in sorted(val_residual_max.items())
                )
            )

        if val_fmae_n > 0:
            _f_pred_mean, _f_pred_std = _stream_mean_std(val_f_pred_sum, val_f_pred_sq_sum, val_f_pred_n)
            _f_true_mean, _f_true_std = _stream_mean_std(val_f_actual_sum, val_f_actual_sq_sum, val_f_actual_n)
            _fn_pred_mean, _fn_pred_std = _stream_mean_std(val_fn_pred_sum, val_fn_pred_sq_sum, val_fn_pred_n)
            _fn_true_mean, _fn_true_std = _stream_mean_std(val_fn_actual_sum, val_fn_actual_sq_sum, val_fn_actual_n)
            _force_stats = {
                "epoch": float(epoch),
                "force_component_pred_mean": float(_f_pred_mean),
                "force_component_pred_std": float(_f_pred_std),
                "force_component_pred_maxabs": float(val_f_pred_maxabs),
                "force_component_actual_mean": float(_f_true_mean),
                "force_component_actual_std": float(_f_true_std),
                "force_component_actual_maxabs": float(val_f_actual_maxabs),
                "force_norm_pred_mean": float(_fn_pred_mean),
                "force_norm_pred_std": float(_fn_pred_std),
                "force_norm_pred_max": float(val_fn_pred_max),
                "force_norm_actual_mean": float(_fn_true_mean),
                "force_norm_actual_std": float(_fn_true_std),
                "force_norm_actual_max": float(val_fn_actual_max),
                "force_norm_mae": float(_final_val_fnorm_mae),
            }
            _epoch_force_stats.append(_force_stats)
            if cfg.save_epoch_artifacts:
                with (_train_dir / "force_stats_history.json").open("w", encoding="utf-8") as _fout:
                    json.dump(_epoch_force_stats, _fout, indent=2, ensure_ascii=True)

        # ── Per-epoch checkpoint ──────────────────────────────────────────────
        if cfg.save_epoch_artifacts:
            _epoch_ckpt = str(_train_dir / f"epoch_{epoch:04d}.pt")
            model.save(_epoch_ckpt)

        # ── MAE history accumulation ──────────────────────────────────────────
        _epoch_emae_hist.append(
            _final_val_emae if val_emae_n > 0 else float("nan")
        )
        _epoch_fmae_hist.append(
            _final_val_fmae if val_fmae_n > 0 else float("nan")
        )
        if cfg.save_epoch_artifacts:
            metrics_payload = {
                "energy_mae": _epoch_emae_hist,
                "force_mae": _epoch_fmae_hist,
                "multitask_mae": _epoch_multitask_hist,
                "physics_residual_max": _epoch_residual_hist,
            }
            (_train_dir / "multitask_metrics_history.json").write_text(
                json.dumps(metrics_payload, indent=2, sort_keys=True), encoding="utf-8"
            )

        # ── Scatter plots + MAE history chart ─────────────────────────────────
        if cfg.save_epoch_artifacts and _HAS_MPL:
            _ep_x = list(range(1, epoch + 1))
            _energy_color = "#2563eb"
            _force_color = "#d97706"

            _e_act_all = np.concatenate(val_e_actual_buf) if val_e_actual_buf else None
            _e_prd_all = np.concatenate(val_e_pred_buf) if val_e_pred_buf else None
            _f_act_all = np.concatenate(val_f_actual_buf) if val_f_actual_buf else None
            _f_prd_all = np.concatenate(val_f_pred_buf) if val_f_pred_buf else None
            _fn_act_all = np.concatenate(val_fn_actual_buf) if val_fn_actual_buf else None
            _fn_prd_all = np.concatenate(val_fn_pred_buf) if val_fn_pred_buf else None

            # Full-range parity chart: energy on the left, forces on the right.
            _fig, (_ax_e_full, _ax_f_full) = plt.subplots(1, 2, figsize=(11.5, 5.2))
            if _e_act_all is not None and _e_prd_all is not None:
                _e_act_full, _e_prd_full = _subsample_pairs(_e_act_all, _e_prd_all, max_points=5000, seed=epoch * 17 + 1)
            else:
                _e_act_full = _e_prd_full = None
            if _f_act_all is not None and _f_prd_all is not None:
                _f_act_full, _f_prd_full = _subsample_pairs(_f_act_all, _f_prd_all, max_points=5000, seed=epoch * 17 + 2)
            else:
                _f_act_full = _f_prd_full = None
            _plot_regression_panel(
                _ax_e_full,
                actual=_e_act_full,
                pred=_e_prd_full,
                color=_energy_color,
                xlabel="Actual E/atom (eV)",
                ylabel="Predicted E/atom (eV)",
                title=f"Energy/atom  full range  E-MAE={_final_val_emae:.4f} eV/atom",
                point_size=10.0,
                point_alpha=0.50,
            )
            _plot_regression_panel(
                _ax_f_full,
                actual=_f_act_full,
                pred=_f_prd_full,
                color=_force_color,
                xlabel="Actual F (eV/Å)",
                ylabel="Predicted F (eV/Å)",
                title=f"Forces  full range  F-MAE={_final_val_fmae:.4f} eV/Å",
                point_size=5.0,
                point_alpha=0.30,
            )
            _fig.suptitle(f"Validation Regression  Epoch {epoch}  (Full Range)", fontsize=12)
            _fig.tight_layout()
            _fig.savefig(str(_plots_dir / f"regression_full_epoch_{epoch:04d}.png"),
                         dpi=110, bbox_inches="tight")
            plt.close(_fig)

            # Clipped parity chart: energy on the left, forces on the right.
            _fig, (_ax_e_clip, _ax_f_clip) = plt.subplots(1, 2, figsize=(11.5, 5.2))
            if _e_act_all is not None and _e_prd_all is not None:
                _e_act_clip, _e_prd_clip, _e_hidden, _e_lim = _clipped_pairs(_e_act_all, _e_prd_all)
                _e_act_clip, _e_prd_clip = _subsample_pairs(_e_act_clip, _e_prd_clip, max_points=5000, seed=epoch * 17 + 3)
                _e_note = f" [{_e_hidden} hidden outside p{int(_scatter_clip_lo)}-p{int(_scatter_clip_hi)}]" if _e_hidden > 0 else ""
            else:
                _e_act_clip = _e_prd_clip = None
                _e_lim = None
                _e_note = ""
            if _f_act_all is not None and _f_prd_all is not None:
                _f_act_clip, _f_prd_clip, _f_hidden, _f_lim = _clipped_pairs(_f_act_all, _f_prd_all)
                _f_act_clip, _f_prd_clip = _subsample_pairs(_f_act_clip, _f_prd_clip, max_points=5000, seed=epoch * 17 + 4)
                _f_note = f" [{_f_hidden} hidden outside p{int(_scatter_clip_lo)}-p{int(_scatter_clip_hi)}]" if _f_hidden > 0 else ""
            else:
                _f_act_clip = _f_prd_clip = None
                _f_lim = None
                _f_note = ""
            _plot_regression_panel(
                _ax_e_clip,
                actual=_e_act_clip,
                pred=_e_prd_clip,
                color=_energy_color,
                xlabel="Actual E/atom (eV)",
                ylabel="Predicted E/atom (eV)",
                title=f"Energy/atom  clipped{_e_note}",
                limits=_e_lim,
                point_size=10.0,
                point_alpha=0.55,
            )
            _plot_regression_panel(
                _ax_f_clip,
                actual=_f_act_clip,
                pred=_f_prd_clip,
                color=_force_color,
                xlabel="Actual F (eV/Å)",
                ylabel="Predicted F (eV/Å)",
                title=f"Forces  clipped{_f_note}",
                limits=_f_lim,
                point_size=5.0,
                point_alpha=0.35,
            )
            _fig.suptitle(
                f"Validation Regression  Epoch {epoch}  (Clipped to p{int(_scatter_clip_lo)}-p{int(_scatter_clip_hi)})",
                fontsize=12,
            )
            _fig.tight_layout()
            _fig.savefig(str(_plots_dir / f"regression_clipped_epoch_{epoch:04d}.png"),
                         dpi=110, bbox_inches="tight")
            plt.close(_fig)

            # Force-norm parity chart: a more stable view than raw signed components.
            _force_norm_color = "#059669"
            _fig, (_ax_fn_full, _ax_fn_clip) = plt.subplots(1, 2, figsize=(11.5, 5.2))
            if _fn_act_all is not None and _fn_prd_all is not None:
                _fn_act_full, _fn_prd_full = _subsample_pairs(_fn_act_all, _fn_prd_all, max_points=5000, seed=epoch * 17 + 5)
            else:
                _fn_act_full = _fn_prd_full = None
            _plot_regression_panel(
                _ax_fn_full,
                actual=_fn_act_full,
                pred=_fn_prd_full,
                color=_force_norm_color,
                xlabel="Actual ||F|| (eV/Å)",
                ylabel="Predicted ||F|| (eV/Å)",
                title=f"Per-atom ||F||  full range  MAE={_final_val_fnorm_mae:.4f} eV/Å",
                point_size=7.0,
                point_alpha=0.34,
            )
            if _fn_act_all is not None and _fn_prd_all is not None:
                _fn_act_clip, _fn_prd_clip, _fn_hidden, _fn_lim = _clipped_pairs(_fn_act_all, _fn_prd_all)
                _fn_act_clip, _fn_prd_clip = _subsample_pairs(_fn_act_clip, _fn_prd_clip, max_points=5000, seed=epoch * 17 + 6)
                _fn_note = f" [{_fn_hidden} hidden outside p{int(_scatter_clip_lo)}-p{int(_scatter_clip_hi)}]" if _fn_hidden > 0 else ""
            else:
                _fn_act_clip = _fn_prd_clip = None
                _fn_lim = None
                _fn_note = ""
            _plot_regression_panel(
                _ax_fn_clip,
                actual=_fn_act_clip,
                pred=_fn_prd_clip,
                color=_force_norm_color,
                xlabel="Actual ||F|| (eV/Å)",
                ylabel="Predicted ||F|| (eV/Å)",
                title=f"Per-atom ||F||  clipped{_fn_note}",
                limits=_fn_lim,
                point_size=7.0,
                point_alpha=0.38,
            )
            _fig.suptitle(f"Force-Norm Regression  Epoch {epoch}", fontsize=12)
            _fig.tight_layout()
            _fig.savefig(str(_plots_dir / f"force_norm_regression_epoch_{epoch:04d}.png"),
                         dpi=110, bbox_inches="tight")
            plt.close(_fig)

            # Cumulative MAE history line chart with separate y-axes for E and F.
            _fig, _ax_e = plt.subplots(figsize=(7.6, 4.2))
            _ax_f = _ax_e.twinx()
            _lines = []
            _labels = []
            if any(e < float("inf") for e in _epoch_emae_hist):
                _line_e, = _ax_e.plot(
                    _ep_x, _epoch_emae_hist, label="E-MAE (eV)",
                    marker=".", linewidth=1.6, color=_energy_color,
                )
                _lines.append(_line_e)
                _labels.append(_line_e.get_label())
            if any(e < float("inf") for e in _epoch_fmae_hist):
                _line_f, = _ax_f.plot(
                    _ep_x, _epoch_fmae_hist, label="F-MAE (eV/Å)",
                    marker=".", linewidth=1.6, color=_force_color,
                )
                _lines.append(_line_f)
                _labels.append(_line_f.get_label())
            _ax_e.set_xlabel("Epoch")
            _ax_e.set_ylabel("Energy/atom MAE (eV/atom)", color=_energy_color)
            _ax_f.set_ylabel("Force MAE (eV/Å)", color=_force_color)
            _ax_e.tick_params(axis="y", colors=_energy_color)
            _ax_f.tick_params(axis="y", colors=_force_color)
            _ax_e.set_title("Validation MAE History")
            _ax_e.grid(True, alpha=0.3)
            if _lines:
                _ax_e.legend(_lines, _labels, loc="upper right")
            _fig.tight_layout()
            _fig.savefig(str(_plots_dir / "mae_history.png"), dpi=100, bbox_inches="tight")
            plt.close(_fig)

            if _epoch_multitask_hist:
                metric_names = sorted(_epoch_multitask_hist)
                columns = 2
                rows = int(math.ceil(len(metric_names) / columns))
                _fig, axes = plt.subplots(rows, columns, figsize=(12.0, max(3.4, 3.2 * rows)))
                axes_array = np.asarray(axes, dtype=object).reshape(-1)
                for axis, metric_name in zip(axes_array, metric_names):
                    history = _epoch_multitask_hist[metric_name]
                    x_values = np.arange(1, len(history["val"]) + 1)
                    axis.plot(x_values, history["train"], label="train", linewidth=1.5)
                    axis.plot(x_values, history["val"], label="validation", linewidth=1.5)
                    axis.set_title(f"{metric_name} MAE")
                    axis.set_xlabel("Epoch")
                    axis.set_ylabel("MAE")
                    axis.grid(True, alpha=0.3)
                    axis.legend()
                for axis in axes_array[len(metric_names):]:
                    axis.set_visible(False)
                _fig.tight_layout()
                _fig.savefig(str(_plots_dir / "multitask_mae_history.png"), dpi=110, bbox_inches="tight")
                plt.close(_fig)

            if _epoch_residual_hist:
                _fig, axis = plt.subplots(figsize=(8.2, 4.8))
                for residual_name, values in sorted(_epoch_residual_hist.items()):
                    axis.semilogy(
                        np.arange(1, len(values) + 1),
                        np.maximum(np.asarray(values, dtype=float), 1e-16),
                        label=residual_name,
                    )
                axis.set_xlabel("Epoch")
                axis.set_ylabel("Validation maximum")
                axis.set_title("Physics Solver Diagnostics")
                axis.grid(True, alpha=0.3)
                axis.legend(fontsize=8)
                _fig.tight_layout()
                _fig.savefig(str(_plots_dir / "physics_residual_history.png"), dpi=110, bbox_inches="tight")
                plt.close(_fig)

        if progress:
            progress({
                "type": "artifacts",
                "epoch": int(epoch),
                "artifact_dir": str(_train_dir),
                "plots_dir": str(_plots_dir),
                "plots_updated": bool(
                    cfg.save_epoch_artifacts
                    and bool(getattr(cfg, "save_epoch_plots", True))
                    and _HAS_MPL
                ),
            })
            progress({"type": "epoch", "epoch": int(epoch), "epochs": int(cfg.epochs)})
        if _sched is not None:
            _sched.step()
        opt.zero_grad(set_to_none=True)
        _release_mps_cache()
        gc.collect()
        memory = _memory_snapshot(device)
        memory["epoch"] = float(epoch)
        baseline_rss = (
            _epoch_memory_hist[0]["rss_mib"] if _epoch_memory_hist else memory["rss_mib"]
        )
        memory["rss_growth_mib"] = memory["rss_mib"] - baseline_rss
        _epoch_memory_hist.append(memory)
        growth_values = [item["rss_growth_mib"] for item in _epoch_memory_hist]
        leak_warning = bool(
            len(growth_values) >= 4
            and all(
                growth_values[index] > growth_values[index - 1] + 8.0
                for index in range(len(growth_values) - 3, len(growth_values))
            )
            and growth_values[-1] > 256.0
        )
        log(
            f"[{_now()}] Memory epoch {epoch}: RSS={memory['rss_mib']:.1f} MiB "
            f"(delta={memory['rss_growth_mib']:+.1f}); "
            f"MPS active={memory['mps_active_mib']:.1f} MiB "
            f"driver={memory['mps_driver_mib']:.1f} MiB "
            f"cache={memory['mps_cache_mib']:.1f} MiB"
            + (" [possible cross-epoch leak]" if leak_warning else "")
        )
        if cfg.save_epoch_artifacts:
            (_train_dir / "memory_history.json").write_text(
                json.dumps(_epoch_memory_hist, indent=2, sort_keys=True),
                encoding="utf-8",
            )
        if progress is not None:
            progress({
                "type": "metrics",
                "epoch": int(epoch),
                "epochs": int(cfg.epochs),
                "train_loss": float(train_loss / max(1, len(loader))),
                "val_loss": float(_final_val_loss),
                "validation_score": float(_epoch_validation_score),
                "energy_mae": float(_final_val_emae) if val_emae_n > 0 else None,
                "force_mae": float(_final_val_fmae) if val_fmae_n > 0 else None,
                "multitask_mae": {
                    name: float(total / count)
                    for name, (total, count) in val_extra_metrics.items()
                    if count > 0
                },
                "physics_residual_max": dict(val_residual_max),
                "memory": dict(memory),
                "memory_leak_warning": leak_warning,
                "numerical_recoveries": int(len(_numerical_recoveries)),
                "unique_bad_samples": int(len(_bad_samples)),
                "unique_bad_input_samples": int(len(_input_bad_samples)),
                "skipped_bad_sample_occurrences": int(_skipped_occurrences),
                "unique_bad_validation_samples": int(
                    len(_bad_validation_samples)
                ),
                "artifact_dir": str(_train_dir),
                "plots_dir": str(_plots_dir),
            })
        _early_stopping_patience = max(
            0, int(getattr(cfg, "early_stopping_patience", 0))
        )
        if (
            _early_stopping_patience > 0
            and _epochs_without_improvement >= _early_stopping_patience
        ):
            log(
                f"[{_now()}] Early stopping at epoch {epoch}: no validation "
                f"improvement greater than {_early_stopping_delta:g} for "
                f"{_epochs_without_improvement} epochs; best epoch={_best_epoch}."
            )
            if progress is not None:
                progress(
                    {
                        "type": "early_stopping",
                        "epoch": int(epoch),
                        "best_epoch": int(_best_epoch),
                        "patience": int(_early_stopping_patience),
                    }
                )
            break

    if stopped and _best_state is None:
        opt.zero_grad(set_to_none=True)
        for dataset_object in (train_data, val_data):
            close = getattr(dataset_object, "close", None)
            if callable(close):
                close()
        del opt, model, loader, v_loader, train_data, val_data, _best_state
        if _sched is not None:
            del _sched
        return _cancelled_result("the first training/validation epoch")

    out_p = Path(str(cfg.out_ckpt)).expanduser()
    if not out_p.is_absolute():
        out_p = Path(__file__).resolve().parent / out_p
    out_path = str(out_p)
    if not out_path.strip():
        raise ValueError("out_ckpt is required (path to save checkpoints/models).")
    Path(os.path.dirname(out_path) or ".").mkdir(parents=True, exist_ok=True)
    if _best_state is None or _best_epoch <= 0 or not math.isfinite(
        _best_validation_score
    ):
        raise FloatingPointError(
            "Training produced no finite validation checkpoint; refusing to save "
            "an unvalidated epoch-0 model."
        )
    if stopped:
        log(
            f"[{_now()}] Training stopped by user; saving the best completed "
            f"validation checkpoint from epoch {_best_epoch}."
        )
    model.cpu()
    if _best_state is not None:
        model.load_state_dict(_best_state, strict=True)
    model.save(
        out_path,
        extra={
            "training_mode": str(cfg.mode),
            "recommended_inference_mode": (
                "ground_only" if str(cfg.mode) == "base" else "full_coupled"
            ),
            "best_epoch": int(_best_epoch),
            "best_val_loss": float(_best_val_loss),
            "validation_score": float(_best_validation_score),
            "split": split_info,
            "memory_history": _checkpoint_safe(_epoch_memory_hist),
            "memory_leak_warning": bool(
                len(_epoch_memory_hist) >= 4
                and all(
                    _epoch_memory_hist[index]["rss_growth_mib"]
                    > _epoch_memory_hist[index - 1]["rss_growth_mib"] + 8.0
                    for index in range(len(_epoch_memory_hist) - 3, len(_epoch_memory_hist))
                )
                and _epoch_memory_hist[-1]["rss_growth_mib"] > 256.0
            ),
            "numerical_recoveries": _checkpoint_safe(_numerical_recoveries),
            "bad_samples": _checkpoint_safe(list(_bad_samples.values())),
            "bad_input_samples": _checkpoint_safe(
                list(_input_bad_samples.values())
            ),
            "skipped_bad_sample_occurrences": int(_skipped_occurrences),
            "bad_validation_samples": _checkpoint_safe(
                list(_bad_validation_samples.values())
            ),
            "skipped_bad_validation_occurrences": int(
                _skipped_validation_occurrences
            ),
            "loss_weights": {
                name: float(getattr(cfg, name))
                for name in (
                    "w_energy", "w_forces", "w_dipole", "w_polarizability",
                    "w_charges", "w_atomic_dipoles", "w_atomic_polarizability",
                    "w_c6", "w_bec", "w_magnetic_moments", "w_effective_field",
                    "w_j", "w_di", "w_dmi",
                )
            },
        },
    )
    log(
        f"[{_now()}] Saved best checkpoint: {out_path} "
        f"epoch={_best_epoch} val_loss={_best_val_loss:.6g} "
        f"normalized_score={_best_validation_score:.6g}"
    )
    if _bad_samples:
        log(
            f"[{_now()}] Training retained {len(_bad_samples)} quarantined "
            f"sample ID(s), skipped {_skipped_occurrences} occurrence(s); "
            "the complete audit is stored in checkpoint extra.bad_samples."
        )
    if _input_bad_samples:
        log(
            f"[{_now()}] Input validation quarantined {len(_input_bad_samples)} "
            "sample ID(s); the audit is stored in checkpoint "
            "extra.bad_input_samples."
        )
    if _bad_validation_samples:
        log(
            f"[{_now()}] Validation excluded {len(_bad_validation_samples)} "
            "invalid sample ID(s); the audit is stored in checkpoint "
            "extra.bad_validation_samples."
        )
    if cfg.export_sevennet:
        try:
            export_sevennet_torchscript(out_path, log)
        except Exception as e:
            log(f"[{_now()}] WARN: SevenNet TS export failed: {e}")
    # Adam state remains on the accelerator even after model.cpu(). Drop every
    # owner before the next AutoSearch trial, then return allocator pages.
    for dataset_object in (train_data, val_data):
        close = getattr(dataset_object, "close", None)
        if callable(close):
            close()
    del opt, model, loader, v_loader, train_data, val_data, _best_state
    if _sched is not None:
        del _sched
    gc.collect()
    _release_mps_cache()
    return out_path, _best_validation_score


def _coerce_config_bool(value: Any) -> bool:
    """Parse JSON/legacy GUI booleans without treating ``"false"`` as true."""
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"1", "true", "yes", "y", "on", "enabled"}:
            return True
        if text in {"0", "false", "no", "n", "off", "disabled", ""}:
            return False
        raise ValueError(f"Invalid boolean value: {value!r}")
    return bool(value)


def _coerce_like_default(value: Any, default: Any) -> Any:
    if value is None:
        return None
    if isinstance(default, bool):
        return _coerce_config_bool(value)
    if isinstance(default, int) and not isinstance(default, bool):
        return int(value)
    if isinstance(default, float):
        return float(value)
    if isinstance(default, tuple):
        return tuple(value) if not isinstance(value, str) else (value,)
    return value


def _deep_merge_config(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    """Merge generated config values while retaining unknown future fields."""
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge_config(dict(result[key]), value)
        else:
            result[key] = copy.deepcopy(value)
    return result


_GUI_TRAIN_DIRECT_FIELDS: Tuple[str, ...] = (
    "device", "cpu_threads", "dataset", "static_data", "response_data",
    "base_ckpt", "out_ckpt", "epochs", "lr", "batch_size", "val_fraction",
    "seed", "w_energy", "w_forces", "force_loss", "force_huber_delta",
    "w_dipole", "w_polarizability", "w_charges", "w_atomic_dipoles",
    "w_atomic_polarizability", "w_c6", "w_bec", "w_magnetic_moments",
    "w_effective_field", "w_j", "w_di", "w_dmi", "lr_scheduler",
    "export_sevennet", "save_epoch_artifacts", "stream_hdf5",
    "cache_neighbor_graphs",
)


def _legacy_vars_to_gui_values(raw_vars: Dict[str, Any]) -> Dict[str, Any]:
    mapping = globals().get("LEGACY_TK_VARIABLES", {})
    reverse = {str(variable): str(key) for key, variable in dict(mapping).items()}
    # These aliases predate the shared Qt/Tk variable map.
    reverse.update({"var_out": "out_ckpt"})
    return {
        reverse[str(name)]: value
        for name, value in raw_vars.items()
        if str(name) in reverse
    }


def _train_payload_from_gui_values(
    values: Dict[str, Any], training_mode: str = "joint"
) -> Dict[str, Any]:
    """Convert GUI-shaped values into a typed, canonical TrainConfig payload."""
    selected_mode = str(training_mode or "joint").strip().lower()
    if selected_mode == "full_chain":
        selected_mode = "joint"
    if selected_mode not in {"base", "response", "joint"}:
        selected_mode = "joint"
    train_defaults = TrainConfig(mode=selected_mode)
    model_defaults = ModelConfig()
    payload: Dict[str, Any] = {"mode": selected_mode}
    for name in _GUI_TRAIN_DIRECT_FIELDS:
        if name not in values:
            continue
        default = getattr(train_defaults, name)
        payload[name] = (
            _parse_cpu_threads(values[name])
            if name == "cpu_threads"
            else _coerce_like_default(values[name], default)
        )
    model_payload: Dict[str, Any] = {}
    for name in ModelConfig.__dataclass_fields__:
        if name in values:
            model_payload[name] = _coerce_like_default(
                values[name], getattr(model_defaults, name)
            )
    if model_payload:
        if bool(model_payload.get("enable_pme")):
            model_payload["enable_qeq"] = True
        if bool(model_payload.get("e3mu_use_l3")) or bool(
            model_payload.get("enable_film")
        ):
            model_payload["e3mu_use_parity"] = True
        if bool(model_payload.get("enable_dmi")):
            model_payload["enable_spin"] = True
            model_payload["e3mu_use_parity"] = True
        payload["model"] = model_payload
    aliases = {
        "warmup_epochs": "warmup_freeze_epochs",
        "w_alpha_final": "w_polarizability_final",
    }
    for gui_name, config_name in aliases.items():
        if gui_name in values:
            payload[config_name] = _coerce_like_default(
                values[gui_name], getattr(train_defaults, config_name)
            )
    if selected_mode == "joint" and "lr" in payload:
        learning_rate = float(payload["lr"])
        if "lr_ground_scale" in values:
            payload["lr_ground"] = learning_rate * float(values["lr_ground_scale"])
        if "lr_response_scale" in values:
            payload["lr_response"] = learning_rate * float(values["lr_response_scale"])
    return payload


def _extract_train_config_payload(values: Dict[str, Any]) -> Dict[str, Any]:
    """Accept canonical, modern GUI, and legacy Tk JSON configuration shapes."""
    if not isinstance(values, dict):
        raise TypeError("Training configuration must be a JSON object")
    if isinstance(values.get("train_config"), dict):
        canonical = copy.deepcopy(dict(values["train_config"]))
        if isinstance(values.get("values"), dict):
            # GUI values are the most recently visible/edited state. Overlay
            # them onto hidden TrainConfig fields while retaining the latter.
            gui_payload = _train_payload_from_gui_values(
                dict(values["values"]),
                str(values.get("training_mode", canonical.get("mode", "joint"))),
            )
            canonical = _deep_merge_config(canonical, gui_payload)
        return canonical
    if isinstance(values.get("values"), dict):
        return _train_payload_from_gui_values(
            dict(values["values"]), str(values.get("training_mode", "joint"))
        )
    raw_vars = values.get("vars")
    if isinstance(raw_vars, dict):
        return _train_payload_from_gui_values(
            _legacy_vars_to_gui_values(raw_vars),
            str(values.get("training_mode", "joint")),
        )
    return copy.deepcopy(values)


def _extract_gui_values_from_config(values: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten any supported configuration shape into modern GUI keys."""
    payload = _extract_train_config_payload(values)
    flattened: Dict[str, Any] = {
        key: value
        for key, value in payload.items()
        if key in _GUI_TRAIN_DIRECT_FIELDS
    }
    model_values = payload.get("model", payload.get("model_config", {}))
    if isinstance(model_values, dict):
        flattened.update(
            (key, value)
            for key, value in model_values.items()
            if key in ModelConfig.__dataclass_fields__
        )
    if "warmup_freeze_epochs" in payload:
        flattened["warmup_epochs"] = payload["warmup_freeze_epochs"]
    if "w_polarizability_final" in payload:
        flattened["w_alpha_final"] = payload["w_polarizability_final"]
    try:
        learning_rate = float(payload.get("lr", 0.0))
        if learning_rate != 0.0 and payload.get("lr_ground") is not None:
            flattened["lr_ground_scale"] = float(payload["lr_ground"]) / learning_rate
        if learning_rate != 0.0 and payload.get("lr_response") is not None:
            flattened["lr_response_scale"] = float(payload["lr_response"]) / learning_rate
    except (TypeError, ValueError, ZeroDivisionError):
        pass
    raw_vars = values.get("vars")
    if isinstance(raw_vars, dict):
        flattened.update(_legacy_vars_to_gui_values(raw_vars))
    if isinstance(values.get("values"), dict):
        flattened.update(copy.deepcopy(dict(values["values"])))
    return flattened


def train_config_from_dict(values: Dict[str, Any]) -> TrainConfig:
    """Load a TrainConfig with schema migration and unknown-field tolerance."""
    payload = _extract_train_config_payload(values)
    if "model" not in payload and isinstance(payload.get("model_config"), dict):
        payload["model"] = payload.pop("model_config")
    payload.setdefault("mode", "joint")
    model_values = payload.pop("model", {})
    key_values = payload.pop("keys", {})

    model_defaults = ModelConfig()
    typed_model = {
        key: _coerce_like_default(value, getattr(model_defaults, key))
        for key, value in dict(model_values).items()
        if key in ModelConfig.__dataclass_fields__
    }
    model = ModelConfig(**typed_model)
    key_defaults = DatasetKeys()
    keys = DatasetKeys(
        **{
            key: _coerce_like_default(value, getattr(key_defaults, key))
            for key, value in dict(key_values).items()
            if key in DatasetKeys.__dataclass_fields__
        }
    )
    train_defaults = TrainConfig(mode=str(payload.get("mode", "joint")))
    allowed = {
        key: (
            _parse_cpu_threads(value)
            if key == "cpu_threads"
            else _coerce_like_default(value, getattr(train_defaults, key))
        )
        for key, value in payload.items()
        if key in TrainConfig.__dataclass_fields__ and key not in {"model", "keys"}
    }
    allowed["model"] = model
    allowed["keys"] = keys
    return TrainConfig(**allowed)


def evaluate_checkpoint(
    checkpoint_path: str,
    dataset_path: str,
    *,
    split: Optional[str] = "test",
    batch_size: int = 4,
    device_name: str = "auto",
    output_json: Optional[str] = None,
) -> Dict[str, Any]:
    device, runtime_dtype = resolve_device(device_name)
    set_default_dtype(runtime_dtype)
    model = DualLayerFieldModel.load(checkpoint_path, map_location="cpu", allow_unsafe_legacy=False)
    model.to(device=device, dtype=torch.get_default_dtype()).eval()
    streamed_dataset: Optional[HDF5AtomicDataDataset] = None
    if _is_hdf5_path(dataset_path):
        plan = prepare_hdf5_stream_plan(
            dataset_path,
            val_fraction=0.1,
            seed=0,
            require_train_val=False,
        )
        if split in (None, "all"):
            evaluation_indices = np.arange(len(plan.group_ids), dtype=np.int64)
        else:
            requested_split = str(split).strip().lower()
            evaluation_indices = np.asarray(
                [
                    index
                    for index, split_name in enumerate(plan.split_values)
                    if split_name == requested_split
                ],
                dtype=np.int64,
            )
        if evaluation_indices.size == 0:
            raise ValueError(f"No structures found for split={split!r}")
        selected_elements = set(_hdf5_elements_for_indices(plan, evaluation_indices))
        structure_count = int(evaluation_indices.size)
        atom_count = int(
            np.sum(
                plan.atom_ptr[evaluation_indices + 1]
                - plan.atom_ptr[evaluation_indices],
                dtype=np.int64,
            )
        )
        z_table = AtomicNumberTable(model.z_table_zs)
        missing_elements = sorted(selected_elements - set(model.z_table_zs))
        if missing_elements:
            raise ValueError(f"Checkpoint does not contain element types: {missing_elements}")
        streamed_dataset = HDF5AtomicDataDataset(
            plan,
            evaluation_indices,
            z_table=z_table,
            cutoff=float(model.cfg.r_max),
            topology_cache=None,
        )
        graph_data: Sequence[AtomicData] = streamed_dataset
    else:
        configurations, _ = load_configurations_auto(dataset_path, DatasetKeys())
        if split not in (None, "all"):
            selected = [
                cfg for cfg in configurations
                if str(cfg.properties.get("split", "")).lower() == str(split).lower()
            ]
            if selected:
                configurations = selected
        if not configurations:
            raise ValueError(f"No structures found for split={split!r}")
        z_table = AtomicNumberTable(model.z_table_zs)
        missing_elements = sorted(
            {int(z) for cfg in configurations for z in cfg.atomic_numbers}
            - set(model.z_table_zs)
        )
        if missing_elements:
            raise ValueError(f"Checkpoint does not contain element types: {missing_elements}")
        graph_data = [
            AtomicData.from_config(cfg, z_table=z_table, cutoff=float(model.cfg.r_max))
            for cfg in configurations
        ]
        structure_count = len(configurations)
        atom_count = int(sum(len(cfg.atomic_numbers) for cfg in configurations))
    loader = DataLoader(
        graph_data,
        batch_size=max(1, min(int(batch_size), len(graph_data))),
        shuffle=False,
        collate_fn=lambda values: _TGBatch.from_data_list(values),
        num_workers=0,
    )
    label_specs = [
        ("energy", "energy", False),
        ("forces", "forces", True),
        ("dipole", "dipole", False),
        ("polarizability", "polarizability", False),
        ("charges", "charges", True),
        ("atomic_dipoles", "atomic_dipoles", True),
        ("atomic_polarizability", "atomic_polarizability", True),
        ("c6", "c6", True),
        ("bec", "bec", True),
        ("magnetic_moments", "magnetic_moments", True),
        ("effective_field", "effective_field", True),
        ("J_effective", "J_effective", False),
        ("Di_effective", "Di_effective", False),
        ("DMI_effective", "DMI_effective", False),
    ]
    accumulators: Dict[str, Dict[str, float]] = {}
    residual_values: Dict[str, List[float]] = {
        "qeq_residual": [],
        "qeq_stability_shift": [],
        "deq_residual": [],
        "deq_stability_shift": [],
        "coupling_residual": [],
        "charge_conservation": [],
    }
    for batch in loader:
        batch = batch.to(device)
        batch_has_forces = _batch_has_label(batch, "forces")
        batch_has_bec = _batch_has_label(batch, "bec")
        batch_has_spins = bool(
            isinstance(model, MixedGranularityE3GNN)
            and model.cfg.enable_spin
            and _batch_has_label(batch, "spins")
        )
        with torch.enable_grad():
            forward_options: Dict[str, Any] = {
                "training": False,
                "compute_forces": batch_has_forces,
                "compute_bec": batch_has_bec,
                "use_response_terms": True,
                "retain_graph": False,
            }
            if isinstance(model, MixedGranularityE3GNN):
                forward_options["use_spin_terms"] = batch_has_spins
            out = model(batch, **forward_options)
        for target_name, output_name, atomwise in label_specs:
            if output_name not in out or not hasattr(batch, target_name):
                continue
            prediction = out[output_name].detach()
            target = torch.as_tensor(
                getattr(batch, target_name), dtype=prediction.dtype, device=prediction.device
            )
            if target.numel() != prediction.numel():
                continue
            target = target.reshape_as(prediction)
            weight = _expanded_property_weight(
                batch, target_name, prediction, atomwise=atomwise
            ).detach()
            expanded = weight
            while expanded.ndim < prediction.ndim:
                expanded = expanded.unsqueeze(-1)
            expanded = expanded.expand_as(prediction)
            difference = prediction - target
            item = accumulators.setdefault(target_name, {"absolute": 0.0, "squared": 0.0, "count": 0.0})
            item["absolute"] += float(torch.sum(torch.abs(difference) * expanded).cpu())
            item["squared"] += float(torch.sum(difference * difference * expanded).cpu())
            item["count"] += float(torch.count_nonzero(expanded > 0.0).cpu())
        for name in (
            "qeq_residual", "qeq_stability_shift", "deq_residual",
            "deq_stability_shift", "coupling_residual"
        ):
            if name in out:
                residual_values[name].extend(
                    torch.as_tensor(out[name]).detach().cpu().reshape(-1).tolist()
                )
        if "charges" in out:
            total_charge = _batch_total_charge(batch, _batch_num_graphs(batch), out["charges"].dtype)
            charge_sum = scatter_sum(out["charges"], batch.batch, dim_size=_batch_num_graphs(batch))
            residual_values["charge_conservation"].extend(
                torch.abs(charge_sum - total_charge).detach().cpu().tolist()
            )
    metrics = {
        name: {
            "mae": values["absolute"] / max(1.0, values["count"]),
            "rmse": math.sqrt(values["squared"] / max(1.0, values["count"])),
            "components": int(values["count"]),
            "unit": HDF5_UNITS.get(name, "unknown"),
        }
        for name, values in accumulators.items()
        if values["count"] > 0.0
    }
    residuals = {
        name: {
            "mean": float(np.mean(values)) if values else 0.0,
            "max": float(np.max(values)) if values else 0.0,
        }
        for name, values in residual_values.items()
    }
    if streamed_dataset is not None:
        streamed_dataset.close()
    report = {
        "schema": "e3mu-evaluation-v1",
        "created_at": _now(),
        "checkpoint": str(Path(checkpoint_path).expanduser().resolve()),
        "dataset": str(Path(dataset_path).expanduser().resolve()),
        "dataset_sha256": sha256_file(dataset_path),
        "split": split or "all",
        "structures": structure_count,
        "atoms": atom_count,
        "streaming": bool(streamed_dataset is not None),
        "metrics": metrics,
        "residuals": residuals,
    }
    if output_json:
        output = Path(output_json).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def run_physics_self_tests(*, seed: int = 7, output_json: Optional[str] = None) -> Dict[str, Any]:
    torch.manual_seed(int(seed))
    np.random.seed(int(seed))
    previous_dtype = torch.get_default_dtype()
    torch.set_default_dtype(torch.float64)
    try:
        z_table = AtomicNumberTable([26])
        positions = np.asarray([[-1.0, 0.0, 0.0], [1.0, 0.2, 0.1]], dtype=float)
        spins = np.asarray([[0.0, 0.0, 1.0], [0.3, 0.0, -math.sqrt(0.91)]], dtype=float)
        config = Configuration(
            atomic_numbers=np.asarray([26, 26]),
            positions=positions,
            properties={"field": np.asarray([0.01, -0.02, 0.005]), "total_charge": 0.0, "spins": spins},
            property_weights={"spins": 1.0},
            cell=np.eye(3) * 20.0,
            pbc=(False, False, False),
        )
        model_config = ModelConfig(
            num_channels=8,
            num_radial_basis=4,
            num_interactions=1,
            enable_qeq=True,
            enable_spin=True,
            enable_film=True,
            coupling_iterations=2,
            dtype="float64",
        )
        model = MixedGranularityE3GNN(
            z_table=z_table,
            atomic_energies_1d=np.zeros(1),
            cfg=model_config,
        ).double().eval()

        def _predict(pos: np.ndarray, spin: np.ndarray, transform: Optional[np.ndarray] = None) -> Dict[str, torch.Tensor]:
            cfg_local = Configuration(
                atomic_numbers=config.atomic_numbers,
                positions=np.asarray(pos, dtype=float),
                properties={
                    "field": (
                        config.properties["field"]
                        if transform is None
                        else np.asarray(config.properties["field"]) @ transform.T
                    ),
                    "total_charge": 0.0,
                    "spins": np.asarray(spin, dtype=float),
                },
                property_weights={"spins": 1.0},
                cell=np.eye(3) * 20.0,
                pbc=(False, False, False),
            )
            graph = AtomicData.from_config(cfg_local, z_table=z_table, cutoff=model_config.r_max)
            batch = _TGBatch.from_data_list([graph])
            return model(batch, training=False, compute_forces=True, compute_bec=True, retain_graph=False)

        base = _predict(positions, spins)
        angle = 0.71
        rotation = np.asarray(
            [[math.cos(angle), -math.sin(angle), 0.0], [math.sin(angle), math.cos(angle), 0.0], [0.0, 0.0, 1.0]]
        )
        rotated = _predict(positions @ rotation.T, spins @ rotation.T, rotation)
        reflection = np.diag([-1.0, 1.0, 1.0])
        reflected_spins = np.linalg.det(reflection) * (spins @ reflection.T)
        reflected = _predict(positions @ reflection.T, reflected_spins, reflection)
        reversed_spin = _predict(positions, -spins)

        def _max_error(left: torch.Tensor, right: torch.Tensor) -> float:
            return float(torch.max(torch.abs(left.detach().cpu() - right.detach().cpu())))

        rotation_force_target = base["forces"] @ torch.as_tensor(rotation.T)
        rotation_dipole_target = base["dipole"] @ torch.as_tensor(rotation.T)
        rotation_alpha_target = torch.einsum(
            "ij,bjk,lk->bil", torch.as_tensor(rotation), base["polarizability"], torch.as_tensor(rotation)
        )
        reflection_force_target = base["forces"] @ torch.as_tensor(reflection.T)
        reflection_dipole_target = base["dipole"] @ torch.as_tensor(reflection.T)
        reflection_alpha_target = torch.einsum(
            "ij,bjk,lk->bil", torch.as_tensor(reflection), base["polarizability"], torch.as_tensor(reflection)
        )

        epsilon = 1e-5
        plus = positions.copy(); plus[0, 0] += epsilon
        minus = positions.copy(); minus[0, 0] -= epsilon
        e_plus = float(_predict(plus, spins)["energy"].detach())
        e_minus = float(_predict(minus, spins)["energy"].detach())
        finite_difference_force = -(e_plus - e_minus) / (2.0 * epsilon)
        autograd_force = float(base["forces"][0, 0].detach())
        charge_error = float(abs(torch.sum(base["charges"]).detach()))
        checks = {
            "rotation_energy": _max_error(rotated["energy"], base["energy"]),
            "rotation_force": _max_error(rotated["forces"], rotation_force_target),
            "rotation_dipole": _max_error(rotated["dipole"], rotation_dipole_target),
            "rotation_polarizability": _max_error(rotated["polarizability"], rotation_alpha_target),
            "reflection_energy": _max_error(reflected["energy"], base["energy"]),
            "reflection_force": _max_error(reflected["forces"], reflection_force_target),
            "reflection_dipole": _max_error(reflected["dipole"], reflection_dipole_target),
            "reflection_polarizability": _max_error(reflected["polarizability"], reflection_alpha_target),
            "time_reversal_energy": _max_error(reversed_spin["energy"], base["energy"]),
            "time_reversal_effective_field": _max_error(
                reversed_spin["effective_field"], -base["effective_field"]
            ),
            "charge_conservation": charge_error,
            "force_finite_difference": abs(finite_difference_force - autograd_force),
            "qeq_residual": float(torch.max(base["qeq_residual"]).detach()),
        }
        thresholds = {name: (2e-5 if name == "force_finite_difference" else 2e-8) for name in checks}
        passed = {name: bool(value <= thresholds[name]) for name, value in checks.items()}
        report = {
            "schema": "e3mu-self-test-v1",
            "created_at": _now(),
            "checks": checks,
            "thresholds": thresholds,
            "passed": passed,
            "all_passed": bool(all(passed.values())),
        }
        if output_json:
            output = Path(output_json).expanduser().resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        return report
    finally:
        torch.set_default_dtype(previous_dtype)


def _fmt_p(v: Any) -> str:
    """Format a parameter value for display in the auto-search treeview."""
    if isinstance(v, bool):  return "T" if v else "F"
    if isinstance(v, float): return f"{v:.4g}"
    return str(v)


class GuiLogger:
    """Thread-safe logger that buffers messages before inserting them into Tk."""
    def __init__(self, text): self.text = text; self.q = queue.Queue()
    def log(self, msg): self.q.put(msg)
    def pump(self):
        for _ in range(200):
            if self.q.empty():
                break
            self.text.insert("end", self.q.get() + "\n")
            self.text.see("end")


def _rounded_polygon_points(
    x1: float, y1: float, x2: float, y2: float, radius: float
) -> List[float]:
    radius = max(0.0, min(float(radius), (x2 - x1) / 2.0, (y2 - y1) / 2.0))
    return [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]


class _MacaronButton(tk.Canvas):
    """Small canvas-backed button with true rounded corners."""

    def __init__(
        self,
        master: Any,
        *,
        text: str,
        command: Optional[Callable[[], None]] = None,
        width: int = 92,
        height: int = 36,
        radius: int = 13,
        background: str = "#f8f6fc",
        fill: str = "#eee9f8",
        hover_fill: str = "#e2daf3",
        selected_fill: str = "#9b87d8",
        foreground: str = "#3e3a52",
        selected_foreground: str = "#ffffff",
        font: Any = None,
    ) -> None:
        super().__init__(
            master,
            width=width,
            height=height,
            background=background,
            highlightthickness=0,
            borderwidth=0,
            cursor="hand2",
            takefocus=1,
        )
        self._text = str(text)
        self._command = command
        self._radius = int(radius)
        self._fill = fill
        self._hover_fill = hover_fill
        self._selected_fill = selected_fill
        self._foreground = foreground
        self._selected_foreground = selected_foreground
        self._font = font or ("TkDefaultFont", 10, "bold")
        self._selected = False
        self._hovered = False
        self._enabled = True
        self.bind("<Configure>", lambda _event: self._redraw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonRelease-1>", self._invoke)
        self.bind("<Return>", self._invoke)
        self.bind("<space>", self._invoke)
        self._redraw()

    def set_selected(self, selected: bool) -> None:
        self._selected = bool(selected)
        self._redraw()

    def set_enabled(self, enabled: bool, reason: str = "") -> None:
        self._enabled = bool(enabled)
        self._disabled_reason = "" if self._enabled else str(reason)
        self.configure(cursor="hand2" if self._enabled else "arrow")
        self._redraw()

    def _current_fill(self) -> str:
        if self._selected:
            return self._selected_fill
        return self._hover_fill if self._hovered else self._fill

    def _redraw(self) -> None:
        self.delete("all")
        width = max(2, int(self.winfo_width() or self.cget("width")))
        height = max(2, int(self.winfo_height() or self.cget("height")))
        points = _rounded_polygon_points(1, 1, width - 1, height - 1, self._radius)
        self.create_polygon(
            points,
            smooth=True,
            splinesteps=24,
            fill=self._current_fill(),
            outline="",
        )
        self.create_text(
            width / 2.0,
            height / 2.0,
            text=self._text,
            fill=(
                "#aaa4b4"
                if not self._enabled
                else self._selected_foreground if self._selected else self._foreground
            ),
            font=self._font,
        )

    def _on_enter(self, _event: Any) -> None:
        if not self._enabled:
            return
        self._hovered = True
        self._redraw()

    def _on_leave(self, _event: Any) -> None:
        self._hovered = False
        self._redraw()

    def _invoke(self, _event: Any = None) -> None:
        if self._enabled and self._command is not None:
            self._command()


class _MacaronToggle(_MacaronButton):
    """Rounded toggle chip synchronized with a Tk BooleanVar."""

    def __init__(self, master: Any, *, variable: tk.BooleanVar, **kwargs: Any) -> None:
        self._variable = variable
        super().__init__(master, command=self._toggle, **kwargs)
        self._trace_id = self._variable.trace_add("write", self._sync)
        self._sync()

    def _toggle(self) -> None:
        self._variable.set(not bool(self._variable.get()))

    def _sync(self, *_args: Any) -> None:
        self.set_selected(bool(self._variable.get()))


class _RoundedCard(tk.Canvas):
    """Rounded canvas surface containing a normal Tk frame for child widgets."""

    def __init__(
        self,
        master: Any,
        *,
        fill: str,
        background: str,
        radius: int = 20,
        padding: int = 14,
        shadow: str = "#e8e3ef",
        auto_height: bool = True,
        height: int = 90,
    ) -> None:
        super().__init__(
            master,
            background=background,
            highlightthickness=0,
            borderwidth=0,
            height=height,
        )
        self._fill = fill
        self._shadow = shadow
        self._radius = int(radius)
        self._padding = int(padding)
        self._auto_height = bool(auto_height)
        self.body = tk.Frame(self, background=fill, borderwidth=0, highlightthickness=0)
        self._window = self.create_window(
            self._padding,
            self._padding,
            anchor="nw",
            window=self.body,
        )
        self.bind("<Configure>", self._on_configure)
        self.body.bind("<Configure>", self._on_body_configure)

    def _on_body_configure(self, _event: Any) -> None:
        if not self._auto_height:
            return
        target = max(40, int(self.body.winfo_reqheight()) + 2 * self._padding)
        if abs(int(float(self.cget("height"))) - target) > 1:
            self.configure(height=target)

    def _on_configure(self, event: Any) -> None:
        width = max(4, int(event.width))
        height = max(4, int(event.height))
        self.delete("surface")
        shadow_points = _rounded_polygon_points(3, 4, width - 1, height - 1, self._radius)
        self.create_polygon(
            shadow_points,
            smooth=True,
            splinesteps=24,
            fill=self._shadow,
            outline="",
            tags="surface",
        )
        card_points = _rounded_polygon_points(1, 1, width - 3, height - 3, self._radius)
        self.create_polygon(
            card_points,
            smooth=True,
            splinesteps=24,
            fill=self._fill,
            outline="",
            tags="surface",
        )
        self.tag_lower("surface")
        self.itemconfigure(
            self._window,
            width=max(1, width - 2 * self._padding - 3),
        )
        if not self._auto_height:
            self.itemconfigure(
                self._window,
                height=max(1, height - 2 * self._padding - 3),
            )


class App(tk.Tk):
    """Tkinter front end for dataset selection, training, and export workflows."""
    def __init__(self):
        super().__init__()
        self.title("Mixed-Granularity E(3)-mu-GNN Trainer")
        self.geometry("1480x960")
        self.minsize(1080, 700)
        
        # Dataset and checkpoint paths.
        self.var_dataset = tk.StringVar()
        self.var_static = tk.StringVar()
        self.var_response = tk.StringVar()
        self.var_base_ckpt = tk.StringVar()
        self.var_out_ckpt = tk.StringVar(value="model.pt")
        
        # Core training hyperparameters.
        self.var_device = tk.StringVar(value="auto")
        self.var_cpu_threads = tk.StringVar(value="auto")
        self.var_dtype = tk.StringVar(value="float32")
        self.var_epochs = tk.StringVar(value="50")
        self.var_bs = tk.StringVar(value="4")
        self.var_lr = tk.StringVar(value="1e-3")
        self.var_val_fraction = tk.StringVar(value="0.1")
        self.var_seed = tk.StringVar(value="0")
        self.var_lr_scheduler = tk.StringVar(value="flat")
        self.var_force_loss = tk.StringVar(value="mse")
        self.var_force_huber_delta = tk.StringVar(value="1.0")
        self.var_rmax = tk.StringVar(value="5.0")
        self.var_channels = tk.StringVar(value="64")
        self.var_interactions = tk.StringVar(value="2")
        self.var_num_radial_basis = tk.StringVar(value="8")
        self.var_field_scale = tk.StringVar(value="1.0")
        
        self.var_we = tk.StringVar(value="1.0")
        self.var_wf = tk.StringVar(value="10.0")
        self.var_wmu = tk.StringVar(value="0.0")
        self.var_walpha = tk.StringVar(value="0.0")
        self.var_w_charges = tk.StringVar(value="0.0")
        self.var_w_atomic_dipoles = tk.StringVar(value="0.0")
        self.var_w_atomic_polarizability = tk.StringVar(value="0.0")
        self.var_w_c6 = tk.StringVar(value="0.0")
        self.var_w_bec = tk.StringVar(value="0.0")
        self.var_w_magnetic_moments = tk.StringVar(value="0.0")
        self.var_w_effective_field = tk.StringVar(value="0.0")
        self.var_w_j = tk.StringVar(value="0.0")
        self.var_w_di = tk.StringVar(value="0.0")
        self.var_w_dmi = tk.StringVar(value="0.0")
        
        self.var_export_sevennet = tk.BooleanVar(value=True)
        self.var_save_epoch_artifacts = tk.BooleanVar(value=True)
        self.var_stream_hdf5 = tk.BooleanVar(value=True)
        self.var_cache_neighbor_graphs = tk.BooleanVar(value=True)

        # Physics and architecture flags mirrored from ``ModelConfig``.
        self.var_e3mu_use_parity = tk.BooleanVar(value=True)
        self.var_e3mu_use_l3 = tk.BooleanVar(value=False)
        self.var_rbf_type = tk.StringVar(value="gaussian")
        self.var_enable_continuous_chem = tk.BooleanVar(value=False)
        self.var_chem_max_z = tk.StringVar(value="96")
        self.var_chem_aug_prob = tk.StringVar(value="0.0")
        self.var_chem_aug_noise_std = tk.StringVar(value="0.0")
        self.var_chem_aug_mix_max = tk.StringVar(value="0.0")
        self.var_enable_qeq = tk.BooleanVar(value=False)
        self.var_enable_pme = tk.BooleanVar(value=False)
        self.var_enable_deq = tk.BooleanVar(value=False)
        self.var_enable_d4 = tk.BooleanVar(value=False)
        self.var_enable_spin = tk.BooleanVar(value=False)
        self.var_enable_film = tk.BooleanVar(value=False)
        self.var_enable_dmi = tk.BooleanVar(value=False)

        self.var_qeq_smearing = tk.StringVar(value="0.35")
        self.var_qeq_hardness_min = tk.StringVar(value="0.25")
        self.var_qeq_pme_smearing = tk.StringVar(value="1.0")
        self.var_qeq_pme_lr_wavelength = tk.StringVar(value="0.8")
        self.var_qeq_stability_floor = tk.StringVar(value="0.1")
        self.var_deq_max_iter = tk.StringVar(value="50")
        self.var_deq_tol = tk.StringVar(value="1e-6")
        self.var_deq_damping = tk.StringVar(value="0.5")
        self.var_deq_alpha_max = tk.StringVar(value="100.0")
        self.var_d4_functional = tk.StringVar(value="pbe")
        self.var_spin_cutoff = tk.StringVar(value="5.0")
        self.var_coupling_iterations = tk.StringVar(value="2")
        self.var_coupling_tol = tk.StringVar(value="1e-5")

        # Full-chain fine-tuning options.
        self.var_joint_stages       = tk.StringVar(value="2")
        self.var_lr_ground_scale    = tk.StringVar(value="0.05")   # lr_ground = lr * scale
        self.var_lr_response_scale  = tk.StringVar(value="0.20")   # lr_response = lr * scale
        self.var_warmup_epochs      = tk.StringVar(value="3")
        self.var_w_dipole_final     = tk.StringVar(value="0.0")
        self.var_w_alpha_final      = tk.StringVar(value="0.0")

        # AutoSearch controls.
        self.var_auto_level        = tk.StringVar(value="0: Disabled")
        self.var_auto_trials       = tk.StringVar(value="20")
        self.var_auto_trial_epochs = tk.StringVar(value="10")
        self.var_auto_subset       = tk.StringVar(value="1")   # percentage of each dataset per trial (1%)
        self.var_live_plot = tk.StringVar(value="Regression")
        self._dataset_capability_text_var = tk.StringVar(
            value="Dataset guard: select a dataset to evaluate architecture switches."
        )
        self._model_size_text_var = tk.StringVar(value="Model size: estimating current configuration...")
        self._auto_tree: Optional[ttk.Treeview] = None
        self._auto_best_params: Dict[str, Any] = {}
        self._auto_best_score: Optional[float] = None
        self._auto_best_level = 0
        self._selected_training_mode = "joint"
        self._custom_search_specs: Dict[str, tuple] = {}
        self._search_space_customized = False
        self._auto_apply_button: Optional[_MacaronButton] = None
        self._auto_best_text_var = tk.StringVar(value="No completed search result yet.")

        self._stop = False
        self._progress_q = queue.Queue()
        self._progress_text_var = tk.StringVar(value="")
        self._run_status_var = tk.StringVar(value="Ready")
        self._epoch_status_var = tk.StringVar(value="Epoch -- / --")
        self._score_status_var = tk.StringVar(value="Score --")
        self._live_metric_history: List[Dict[str, Any]] = []
        self._live_metric_names: List[str] = []
        self._live_artifact_dir: Optional[Path] = None
        self._live_figure = None
        self._live_canvas = None
        self._live_axes: List[Any] = []
        self._training_running = False
        self._training_buttons: List[_MacaronButton] = []
        self._architecture_toggles: Dict[str, _MacaronToggle] = {}
        self._architecture_disabled_reasons: Dict[str, str] = {}
        self._dataset_capability: Dict[str, Any] = {"ready": False}
        self._dataset_scan_after_id: Optional[str] = None
        self._dataset_scan_generation = 0
        self._dataset_selection_revision = 0
        self._dataset_scan_pending = False
        self._dataset_scan_error = ""
        self._dataset_capability_cache: Dict[Tuple[str, int, int], Dict[str, Any]] = {}
        self._model_estimate_after_id: Optional[str] = None
        self._model_estimate_generation = 0
        self._model_estimate_cache: Dict[str, Dict[str, int]] = {}

        self._build_ui()
        # Persist only the user-facing ``var_*`` settings.
        self._default_config_path = Path.home() / ".dual_layer_field_gui.defaults.json"
        self._factory_config: Dict[str, Any] = self._collect_config()
        self._maybe_load_default_config()
        self._install_dataset_capability_traces()
        self._install_model_parameter_traces()
        self._schedule_dataset_capability_scan()
        self._schedule_model_parameter_estimate()
        self.after(100, self._pump)

    # Config import / export helpers for all ``self.var_*`` Tk variables.
    def _iter_config_vars(self):
        for name, obj in list(self.__dict__.items()):
            if name.startswith("var_") and isinstance(obj, tk.Variable):
                yield name, obj

    @staticmethod
    def _json_safe(x: Any) -> Any:
        if x is None or isinstance(x, (str, int, float, bool)):
            return x
        if isinstance(x, (list, tuple)):
            return [App._json_safe(v) for v in x]
        if isinstance(x, dict):
            return {str(k): App._json_safe(v) for k, v in x.items()}
        return str(x)

    def _collect_config(self) -> Dict[str, Any]:
        vars_out: Dict[str, Any] = {}
        for name, var in self._iter_config_vars():
            try:
                vars_out[name] = self._json_safe(var.get())
            except Exception:
                continue
        return {"version": 2, "saved_at": _now(), "vars": vars_out, "state": {}}

    def _apply_config(self, cfg: Dict[str, Any]) -> None:
        if not isinstance(cfg, dict):
            raise TypeError("Config must be a dict.")
        vars_in = cfg.get("vars", None)
        if isinstance(vars_in, dict):
            var_map = vars_in
        else:
            var_map = {k: v for k, v in cfg.items() if str(k).startswith("var_")}
            
        if "var_out" in var_map and "var_out_ckpt" not in var_map:
            var_map["var_out_ckpt"] = var_map.get("var_out")

        for name, value in var_map.items():
            var = getattr(self, str(name), None)
            if not isinstance(var, tk.Variable):
                continue
            try:
                var.set(value)
            except Exception:
                try:
                    cur = var.get()
                    if isinstance(cur, bool):
                        if isinstance(value, str):
                            var.set(value.strip().lower() in ("1", "true", "yes", "y", "on"))
                        else:
                            var.set(bool(value))
                    elif isinstance(cur, int):
                        var.set(int(value))
                    elif isinstance(cur, float):
                        var.set(float(value))
                    else:
                        var.set(str(value))
                except Exception:
                    pass
        if int(cfg.get("version", 1)) < 2:
            self.var_e3mu_use_parity.set(True)
        try:
            bounded_spin = _compatible_spin_cutoff(
                self.var_rmax.get(), self.var_spin_cutoff.get()
            )
            self.var_spin_cutoff.set(f"{bounded_spin:.12g}")
        except (tk.TclError, TypeError, ValueError):
            pass

    def _save_config_to_file(self, path: str) -> None:
        cfg = self._collect_config()
        Path(os.path.dirname(path) or ".").mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, sort_keys=True, ensure_ascii=True)

    def _load_config_from_file(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if not isinstance(cfg, dict):
            raise ValueError("Config file must contain a JSON object.")
        return cfg

    def _maybe_load_default_config(self) -> None:
        try:
            p = Path(self._default_config_path)
            if p.is_file():
                cfg = self._load_config_from_file(str(p))
                self._apply_config(cfg)
                self.logger.log(f"[{_now()}] Loaded default config: {p}")
        except Exception as e:
            self.logger.log(f"[{_now()}] WARN: failed to load default config: {e}")

    def _import_config(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            cfg = self._load_config_from_file(path)
            self._apply_config(cfg)
            self.logger.log(f"[{_now()}] Imported config: {path}")
        except Exception as e:
            messagebox.showerror("Import failed", str(e))

    def _export_config(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            self._save_config_to_file(path)
            self.logger.log(f"[{_now()}] Exported config: {path}")
        except Exception as e:
            messagebox.showerror("Export failed", str(e))

    def _save_default_config(self) -> None:
        try:
            self._save_config_to_file(str(self._default_config_path))
            self.logger.log(f"[{_now()}] Saved default config: {self._default_config_path}")
        except Exception as e:
            messagebox.showerror("Save default failed", str(e))

    def _reset_factory_config(self) -> None:
        try:
            self._apply_config(dict(self._factory_config))
            self.logger.log(f"[{_now()}] Reset to factory defaults.")
        except Exception as e:
            messagebox.showerror("Reset failed", str(e))

    def _configure_modern_theme(self) -> None:
        """Apply the shared typography and macaron palette."""
        self.configure(background="#f7f4fa")
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        family = "SF Pro Text" if sys.platform == "darwin" else "Segoe UI"
        available = set(tkfont.families(self))
        if family not in available:
            family = "Helvetica" if "Helvetica" in available else "TkDefaultFont"
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family=family, size=11)
        tkfont.nametofont("TkTextFont").configure(family=family, size=10)

        bg = "#f7f4fa"
        surface = "#fffdfd"
        text_color = "#3d3a50"
        muted = "#777287"
        border = "#e7e0eb"
        accent = "#9b87d8"
        accent_hover = "#8973ca"
        danger = "#c86b7c"
        style.configure(".", background=bg, foreground=text_color, font=(family, 11))
        style.configure("App.TFrame", background=bg)
        style.configure("Surface.TFrame", background=surface)
        style.configure("Header.TFrame", background="#675c86")
        style.configure("HeaderTitle.TLabel", background="#675c86", foreground="#fffdfd",
                        font=(family, 19, "bold"))
        style.configure("HeaderSub.TLabel", background="#675c86", foreground="#ebe4fa",
                        font=(family, 10))
        style.configure("Status.TLabel", background="#675c86", foreground="#fffdfd",
                        font=(family, 10, "bold"))
        style.configure("Card.TLabelframe", background=surface, bordercolor=border,
                        relief="solid", borderwidth=1)
        style.configure("Card.TLabelframe.Label", background=surface, foreground=text_color,
                        font=(family, 11, "bold"))
        style.configure("Card.TFrame", background=surface)
        style.configure("Card.TLabel", background=surface, foreground=text_color)
        style.configure("Muted.Card.TLabel", background=surface, foreground=muted,
                        font=(family, 9))
        style.configure("MetricName.TLabel", background=surface, foreground=muted,
                        font=(family, 9))
        style.configure("MetricValue.TLabel", background=surface, foreground=text_color,
                        font=(family, 14, "bold"))
        style.configure("TEntry", fieldbackground=surface, foreground=text_color,
                        bordercolor=border, lightcolor=border, darkcolor=border, padding=6)
        style.configure("TCombobox", fieldbackground=surface, foreground=text_color,
                        bordercolor=border, arrowcolor=text_color, padding=5)
        style.map("TCombobox", fieldbackground=[("readonly", surface)],
                  foreground=[("readonly", text_color)])
        style.configure("TCheckbutton", background=surface, foreground=text_color, padding=3)
        style.map("TCheckbutton", background=[("active", surface)])
        style.configure("TButton", padding=(11, 7), borderwidth=0,
                        background="#eee9f5", foreground=text_color)
        style.map("TButton", background=[("active", "#e5dcf1"), ("pressed", "#dbcfeb")])
        style.configure("Primary.TButton", background=accent, foreground="#ffffff",
                        font=(family, 10, "bold"), padding=(13, 8))
        style.map("Primary.TButton", background=[("active", accent_hover), ("pressed", "#7962ba")],
                  foreground=[("disabled", "#eee9f7")])
        style.configure("Danger.TButton", background="#f8e3e8", foreground=danger,
                        font=(family, 10, "bold"))
        style.map("Danger.TButton", background=[("active", "#f2d6de")])
        style.configure("Accent.Horizontal.TProgressbar", troughcolor="#e8e1ef",
                        background=accent, lightcolor=accent, darkcolor=accent, thickness=8)
        style.configure("Treeview", background=surface, fieldbackground=surface,
                        foreground=text_color, rowheight=27, bordercolor=border)
        style.configure("Treeview.Heading", background="#efeaf4", foreground=text_color,
                        font=(family, 9, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#e6ddf5")],
                  foreground=[("selected", text_color)])
        style.configure("TNotebook", background=bg, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(14, 8), background="#e7ecf4",
                        foreground=muted)
        style.map("TNotebook.Tab", background=[("selected", surface)],
                  foreground=[("selected", text_color)])

    @staticmethod
    def _artifact_dir_for_checkpoint(checkpoint_value: str) -> Path:
        checkpoint = Path(checkpoint_value or "model.pt").expanduser()
        if not checkpoint.is_absolute():
            checkpoint = Path(__file__).resolve().parent / checkpoint
        return checkpoint.parent / "train" / checkpoint.stem

    def _make_scrollable(self, parent: Any) -> ttk.Frame:
        host = ttk.Frame(parent, style="App.TFrame")
        host.pack(fill="both", expand=True)
        canvas = tk.Canvas(host, bd=0, highlightthickness=0, background="#f3f6fb")
        scrollbar = ttk.Scrollbar(host, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        content = ttk.Frame(canvas, style="App.TFrame")
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")
        content.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window_id, width=e.width))

        def _wheel(event: Any) -> None:
            delta = getattr(event, "delta", 0)
            if delta:
                units = -1 if delta > 0 else 1
                canvas.yview_scroll(units * max(1, abs(int(delta / 120))), "units")
            elif getattr(event, "num", None) == 4:
                canvas.yview_scroll(-1, "units")
            elif getattr(event, "num", None) == 5:
                canvas.yview_scroll(1, "units")

        canvas.bind("<MouseWheel>", _wheel)
        canvas.bind("<Button-4>", _wheel)
        canvas.bind("<Button-5>", _wheel)
        content.bind("<MouseWheel>", _wheel)
        return content

    def _make_page_scroll(self, parent: Any, background: str) -> tk.Frame:
        host = tk.Frame(parent, background=background)
        host.pack(fill="both", expand=True)
        canvas = tk.Canvas(host, background=background, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(host, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        content = tk.Frame(canvas, background=background)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")
        content.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window_id, width=e.width))

        def _wheel(event: Any) -> None:
            delta = getattr(event, "delta", 0)
            if delta:
                canvas.yview_scroll(-1 if delta > 0 else 1, "units")
            elif getattr(event, "num", None) == 4:
                canvas.yview_scroll(-1, "units")
            elif getattr(event, "num", None) == 5:
                canvas.yview_scroll(1, "units")

        canvas.bind("<MouseWheel>", _wheel)
        canvas.bind("<Button-4>", _wheel)
        canvas.bind("<Button-5>", _wheel)
        content.bind("<MouseWheel>", _wheel)
        return content

    def _make_settings_card(
        self,
        parent: Any,
        title: str,
        subtitle: str,
        fill: str,
        palette: Dict[str, str],
    ) -> tk.Frame:
        card = _RoundedCard(
            parent,
            fill=fill,
            background=palette["bg"],
            radius=22,
            padding=16,
            shadow="#e9e3ed",
        )
        card.pack(fill="x", padx=(0, 7), pady=(0, 12))
        tk.Label(
            card.body,
            text=title,
            background=fill,
            foreground=palette["text"],
            font=("TkDefaultFont", 13, "bold"),
        ).pack(anchor="w")
        tk.Label(
            card.body,
            text=subtitle,
            background=fill,
            foreground=palette["muted"],
            font=("TkDefaultFont", 9),
            wraplength=490,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(3, 12))
        return card.body

    def _make_labeled_field(
        self,
        parent: Any,
        label: str,
        variable: tk.Variable,
        kind: str,
        values: Optional[Sequence[str]],
        background: str,
    ) -> tk.Frame:
        field_frame = tk.Frame(parent, background=background)
        tk.Label(
            field_frame,
            text=label,
            background=background,
            foreground="#686276",
            font=("TkDefaultFont", 9, "bold"),
        ).pack(anchor="w", pady=(0, 4))
        if kind == "combo":
            widget = ttk.Combobox(
                field_frame,
                textvariable=variable,
                values=list(values or []),
                state="readonly",
            )
        else:
            widget = ttk.Entry(field_frame, textvariable=variable)
        widget.pack(fill="x")
        return field_frame

    def _build_field_grid(
        self,
        parent: tk.Frame,
        fields: Sequence[Tuple[str, tk.Variable, str, Optional[Sequence[str]]]],
    ) -> None:
        background = str(parent.cget("background"))
        grid = tk.Frame(parent, background=background)
        grid.pack(fill="x")
        grid.columnconfigure((0, 1), weight=1, uniform="fields")
        for index, (label, variable, kind, values) in enumerate(fields):
            row, column = divmod(index, 2)
            field_frame = self._make_labeled_field(
                grid, label, variable, kind, values, background
            )
            field_frame.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=(0 if column == 0 else 8, 8 if column == 0 else 0),
                pady=(0, 10),
            )

    def _browse_for_variable(self, variable: tk.StringVar, mode: str) -> None:
        if mode == "save":
            value = filedialog.asksaveasfilename(
                defaultextension=".pt",
                filetypes=[
                    ("PyTorch Checkpoint", "*.pt"),
                    ("PyTorch Model", "*.pth"),
                    ("All files", "*.*"),
                ],
            )
        else:
            value = filedialog.askopenfilename()
        if value:
            variable.set(value)

    def _build_file_field_grid(
        self,
        parent: tk.Frame,
        fields: Sequence[Tuple[str, tk.StringVar, str]],
        palette: Dict[str, str],
    ) -> None:
        background = str(parent.cget("background"))
        grid = tk.Frame(parent, background=background)
        grid.pack(fill="x")
        grid.columnconfigure((0, 1), weight=1, uniform="files")
        for index, (label, variable, mode) in enumerate(fields):
            row, column = divmod(index, 2)
            cell = tk.Frame(grid, background=background)
            cell.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=(0 if column == 0 else 8, 8 if column == 0 else 0),
                pady=(0, 11),
            )
            tk.Label(
                cell,
                text=label,
                background=background,
                foreground=palette["muted"],
                font=("TkDefaultFont", 9, "bold"),
            ).pack(anchor="w", pady=(0, 4))
            row_frame = tk.Frame(cell, background=background)
            row_frame.pack(fill="x")
            ttk.Entry(row_frame, textvariable=variable).pack(side="left", fill="x", expand=True)
            _MacaronButton(
                row_frame,
                text="Choose",
                command=lambda v=variable, m=mode: self._browse_for_variable(v, m),
                width=66,
                height=31,
                radius=11,
                background=background,
                fill="#f8fbff",
                hover_fill="#d7e6f7",
                selected_fill=palette["lavender_strong"],
                font=("TkDefaultFont", 8, "bold"),
            ).pack(side="right", padx=(6, 0))

    def _build_toggle_grid(
        self,
        parent: tk.Frame,
        flags: Sequence[Tuple[str, str, tk.BooleanVar]],
    ) -> Dict[str, _MacaronToggle]:
        background = str(parent.cget("background"))
        grid = tk.Frame(parent, background=background)
        grid.pack(fill="x")
        grid.columnconfigure((0, 1), weight=1, uniform="toggles")
        toggles: Dict[str, _MacaronToggle] = {}
        for index, (key, label, variable) in enumerate(flags):
            row, column = divmod(index, 2)
            toggle = _MacaronToggle(
                grid,
                text=label,
                variable=variable,
                height=34,
                radius=12,
                background=background,
                fill="#fffafd",
                hover_fill="#f2dce7",
                selected_fill="#cf8fac",
                font=("TkDefaultFont", 9, "bold"),
            )
            toggle.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=(0 if column == 0 else 5, 5 if column == 0 else 0),
                pady=4,
            )
            toggles[str(key)] = toggle
        return toggles

    def _install_dataset_capability_traces(self) -> None:
        for variable in (self.var_dataset, self.var_static, self.var_response):
            variable.trace_add(
                "write", lambda *_args: self._on_dataset_selection_changed()
            )

    def _on_dataset_selection_changed(self) -> None:
        self._dataset_selection_revision += 1
        self._auto_best_params = {}
        self._auto_best_score = None
        self._auto_best_text_var.set(
            "Dataset selection changed; run AutoSearch to obtain compatible best values."
        )
        if self._auto_apply_button is not None:
            self._auto_apply_button.set_enabled(False, "Dataset selection changed")
        self._schedule_dataset_capability_scan()

    def _install_model_parameter_traces(self) -> None:
        variables = (
            self.var_channels,
            self.var_interactions,
            self.var_num_radial_basis,
            self.var_e3mu_use_parity,
            self.var_e3mu_use_l3,
            self.var_rbf_type,
            self.var_enable_continuous_chem,
            self.var_enable_qeq,
            self.var_enable_pme,
            self.var_enable_deq,
            self.var_enable_d4,
            self.var_enable_spin,
            self.var_enable_film,
            self.var_enable_dmi,
        )
        for variable in variables:
            variable.trace_add(
                "write", lambda *_args: self._schedule_model_parameter_estimate()
            )

    def _schedule_model_parameter_estimate(self) -> None:
        if self._model_estimate_after_id is not None:
            try:
                self.after_cancel(self._model_estimate_after_id)
            except tk.TclError:
                pass
        self._model_estimate_after_id = self.after(
            180, self._start_model_parameter_estimate
        )

    def _start_model_parameter_estimate(self) -> None:
        self._model_estimate_after_id = None
        self._model_estimate_generation += 1
        generation = self._model_estimate_generation
        try:
            use_l3 = bool(self.var_e3mu_use_l3.get())
            enable_film = bool(self.var_enable_film.get())
            enable_spin = bool(self.var_enable_spin.get())
            enable_dmi = bool(self.var_enable_dmi.get())
            enable_pme = bool(self.var_enable_pme.get())
            use_parity = bool(self.var_e3mu_use_parity.get()) or use_l3 or enable_film
            use_parity = use_parity or (enable_spin and enable_dmi)
            cfg = ModelConfig(
                r_max=float(self.var_rmax.get()),
                num_channels=int(self.var_channels.get()),
                num_interactions=int(self.var_interactions.get()),
                num_radial_basis=int(self.var_num_radial_basis.get()),
                field_scale=float(self.var_field_scale.get()),
                dtype=str(self.var_dtype.get()),
                e3mu_use_parity=use_parity,
                e3mu_use_l3=use_l3,
                rbf_type=str(self.var_rbf_type.get()),
                enable_continuous_chem=bool(self.var_enable_continuous_chem.get()),
                enable_qeq=bool(self.var_enable_qeq.get()) or enable_pme,
                enable_pme=enable_pme,
                enable_deq=bool(self.var_enable_deq.get()),
                enable_d4=bool(self.var_enable_d4.get()),
                enable_spin=enable_spin,
                enable_film=enable_film,
                enable_dmi=enable_dmi,
                spin_cutoff=float(self.var_spin_cutoff.get()),
            )
        except (ValueError, RuntimeError, tk.TclError) as exc:
            self._model_size_text_var.set(f"Model size: waiting for valid settings ({exc}).")
            return
        elements = list(self._dataset_capability.get("elements", [])) or [1]
        cache_key = json.dumps(
            {"model": asdict(cfg), "elements": sorted(int(value) for value in elements)},
            sort_keys=True,
        )
        cached = self._model_estimate_cache.get(cache_key)
        if cached is not None:
            self._apply_model_parameter_estimate(cached)
            return
        self._model_size_text_var.set("Model size: estimating current configuration...")

        def estimate() -> None:
            try:
                counts = estimate_model_parameter_count(cfg, elements)
                self._model_estimate_cache[cache_key] = counts
                self._progress_q.put(
                    {
                        "type": "model_parameter_estimate",
                        "generation": generation,
                        "counts": counts,
                    }
                )
            except Exception as exc:
                self._progress_q.put(
                    {
                        "type": "model_parameter_estimate",
                        "generation": generation,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

        threading.Thread(target=estimate, daemon=True).start()

    @staticmethod
    def _human_parameter_count(value: int) -> str:
        number = float(value)
        if number >= 1_000_000:
            return f"{number / 1_000_000.0:.3g}M"
        if number >= 1_000:
            return f"{number / 1_000.0:.3g}K"
        return str(int(value))

    def _apply_model_parameter_estimate(
        self, counts: Dict[str, int], error: str = ""
    ) -> None:
        if error:
            self._model_size_text_var.set(f"Model size unavailable: {error}")
            return
        total = int(counts.get("total", 0))
        trainable = int(counts.get("trainable", 0))
        ground = int(counts.get("ground", 0))
        response = int(counts.get("response", 0))
        physics = int(counts.get("physics", 0))
        elements = int(counts.get("elements", 0))
        self._model_size_text_var.set(
            f"Exact parameters: {total:,} ({self._human_parameter_count(total)}) total / "
            f"{trainable:,} trainable  |  L1 {ground:,}  |  L2 {response:,}  |  "
            f"L3/physics {physics:,}  |  {elements} element types"
        )

    def _schedule_dataset_capability_scan(self) -> None:
        selected = bool(
            self.var_dataset.get().strip()
            or self.var_static.get().strip()
            or self.var_response.get().strip()
        )
        self._dataset_scan_pending = selected
        self._dataset_scan_error = ""
        if self._dataset_scan_after_id is not None:
            try:
                self.after_cancel(self._dataset_scan_after_id)
            except tk.TclError:
                pass
        self._dataset_scan_after_id = self.after(300, self._start_dataset_capability_scan)

    def _cached_dataset_capability(self, path_value: str) -> Dict[str, Any]:
        path = Path(path_value).expanduser().resolve()
        stat = path.stat()
        cache_key = (str(path), int(stat.st_size), int(stat.st_mtime_ns))
        cached = self._dataset_capability_cache.get(cache_key)
        if cached is None:
            cached = inspect_dataset_capabilities(str(path))
            self._dataset_capability_cache[cache_key] = cached
        return dict(cached)

    def _start_dataset_capability_scan(self) -> None:
        self._dataset_scan_after_id = None
        canonical = self.var_dataset.get().strip()
        legacy_paths = [
            value for value in (self.var_static.get().strip(), self.var_response.get().strip())
            if value
        ]
        selected_paths = [canonical] if canonical else legacy_paths
        self._dataset_scan_generation += 1
        generation = self._dataset_scan_generation
        if not selected_paths:
            self._dataset_scan_pending = False
            self._dataset_scan_error = ""
            self._apply_dataset_capability({"ready": False})
            return
        self._dataset_scan_pending = True
        self._dataset_scan_error = ""
        self._dataset_capability_text_var.set("Dataset guard: scanning selected data...")

        def scan() -> None:
            try:
                reports = [self._cached_dataset_capability(path) for path in selected_paths]
                capability = merge_dataset_capabilities(reports)
                self._progress_q.put(
                    {
                        "type": "dataset_capability",
                        "generation": generation,
                        "capability": capability,
                    }
                )
            except Exception as exc:
                self._progress_q.put(
                    {
                        "type": "dataset_capability",
                        "generation": generation,
                        "capability": {"ready": False},
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

        threading.Thread(target=scan, daemon=True).start()

    def _apply_dataset_capability(
        self, capability: Dict[str, Any], error: str = ""
    ) -> None:
        self._dataset_scan_pending = False
        self._dataset_scan_error = str(error)
        self._dataset_capability = dict(capability)
        availability = architecture_switch_availability(capability)
        disabled: List[str] = []
        display_names = {
            "e3mu_use_parity": "O(3)",
            "e3mu_use_l3": "L=3",
            "enable_continuous_chem": "Chem",
            "enable_qeq": "QEq",
            "enable_pme": "PME",
            "enable_deq": "DEQ",
            "enable_d4": "D4",
            "enable_spin": "Spin",
            "enable_film": "FiLM",
            "enable_dmi": "DMI",
        }
        self._architecture_disabled_reasons.clear()
        for key, toggle in self._architecture_toggles.items():
            allowed, reason = availability.get(key, (True, "Supported"))
            toggle.set_enabled(allowed, reason)
            if not allowed:
                variable = getattr(self, f"var_{key}", None)
                if isinstance(variable, tk.BooleanVar) and bool(variable.get()):
                    variable.set(False)
                self._architecture_disabled_reasons[key] = reason
                disabled.append(f"{display_names.get(key, key)}: {reason}")

        if error:
            self._dataset_capability_text_var.set(
                f"Dataset guard could not inspect the selection ({error}); switches remain editable."
            )
            return
        if not bool(capability.get("ready")):
            self._dataset_capability_text_var.set(
                "Dataset guard: select a dataset to evaluate architecture switches."
            )
            return
        structures = int(capability.get("structures", 0))
        elements = len(capability.get("elements", []))
        periodic = int(capability.get("periodic_structures", 0))
        labels = sorted(
            name
            for name, count in dict(capability.get("labels", {})).items()
            if int(count) > 0
        )
        summary = (
            f"Detected {structures} structures / {elements} elements / "
            f"{periodic} periodic; labels: {', '.join(labels) if labels else 'none'}."
        )
        if disabled:
            summary += " Disabled - " + "; ".join(disabled) + "."
        else:
            summary += " All architecture switches are meaningful for this dataset."
        self._dataset_capability_text_var.set(summary)
        self._model_size_text_var.set(
            "Model size: re-estimating with detected element types..."
        )
        self._schedule_model_parameter_estimate()

    def _show_settings_page(self, name: str) -> None:
        page = self._settings_pages.get(name)
        if page is None:
            return
        page.tkraise()
        for page_name, button in self._settings_nav_buttons.items():
            button.set_selected(page_name == name)

    def _build_ui(self):
        self._configure_modern_theme()
        palette = {
            "bg": "#f7f4fa",
            "surface": "#fffdfd",
            "text": "#3d3a50",
            "muted": "#777287",
            "lavender": "#eee9f8",
            "lavender_strong": "#9b87d8",
            "mint": "#e3f3ec",
            "peach": "#fbe9df",
            "blue": "#e4eef9",
            "pink": "#f7e5ed",
            "yellow": "#f8f0d8",
        }
        shell = tk.Frame(self, background=palette["bg"])
        shell.pack(fill="both", expand=True)

        header = tk.Frame(shell, background="#675c86", padx=24, pady=15)
        header.pack(fill="x")
        brand = tk.Frame(header, background="#675c86")
        brand.pack(side="left", fill="x", expand=True)
        tk.Label(
            brand,
            text="Mixed-Granularity E(3)-mu-GNN",
            background="#675c86",
            foreground="#fffdfd",
            font=("TkDefaultFont", 19, "bold"),
        ).pack(anchor="w")
        tk.Label(
            brand,
            text="L1 local chemistry  /  L2 electrostatic response  /  L3 spin Hamiltonian",
            background="#675c86",
            foreground="#ebe4fa",
            font=("TkDefaultFont", 10),
        ).pack(anchor="w", pady=(2, 0))
        header_state = tk.Frame(header, background="#675c86")
        header_state.pack(side="right")
        tk.Label(
            header_state,
            textvariable=self._run_status_var,
            background="#675c86",
            foreground="#fffdfd",
            font=("TkDefaultFont", 10, "bold"),
        ).pack(anchor="e")
        tk.Label(
            header_state,
            textvariable=self._progress_text_var,
            background="#675c86",
            foreground="#ebe4fa",
            font=("TkDefaultFont", 9),
        ).pack(anchor="e", pady=(3, 0))

        body = tk.PanedWindow(
            shell,
            orient="horizontal",
            sashwidth=8,
            sashrelief="flat",
            background=palette["bg"],
            borderwidth=0,
            relief="flat",
        )
        body.pack(fill="both", expand=True, padx=16, pady=16)
        settings_panel = tk.Frame(body, background=palette["bg"], width=560)
        dashboard_panel = tk.Frame(body, background=palette["bg"], width=860)
        body.add(settings_panel, minsize=480, stretch="always")
        body.add(dashboard_panel, minsize=590, stretch="always")
        self._settings_paned = body

        utility = tk.Frame(settings_panel, background=palette["bg"])
        utility.pack(fill="x", pady=(0, 10))
        for text_value, command, fill in (
            ("Import", self._import_config, palette["blue"]),
            ("Export", self._export_config, palette["mint"]),
            ("Save Default", self._save_default_config, palette["yellow"]),
            ("Factory Reset", self._reset_factory_config, palette["pink"]),
        ):
            _MacaronButton(
                utility,
                text=text_value,
                command=command,
                width=100 if " " in text_value else 82,
                background=palette["bg"],
                fill=fill,
                hover_fill=palette["lavender"],
                selected_fill=palette["lavender_strong"],
            ).pack(side="left", padx=(0, 7))

        nav = tk.Frame(settings_panel, background=palette["bg"])
        nav.pack(fill="x", pady=(0, 10))
        page_host = tk.Frame(settings_panel, background=palette["bg"])
        page_host.pack(fill="both", expand=True)
        self._settings_pages: Dict[str, tk.Frame] = {}
        self._settings_nav_buttons: Dict[str, _MacaronButton] = {}
        page_specs = [
            ("Data", palette["blue"]),
            ("Training", palette["mint"]),
            ("Losses", palette["peach"]),
            ("Physics", palette["pink"]),
            ("Search", palette["yellow"]),
        ]
        for index, (name, fill) in enumerate(page_specs):
            nav.columnconfigure(index, weight=1, uniform="nav")
            button = _MacaronButton(
                nav,
                text=name,
                command=lambda page=name: self._show_settings_page(page),
                width=90,
                background=palette["bg"],
                fill=fill,
                hover_fill=palette["lavender"],
                selected_fill=palette["lavender_strong"],
            )
            button.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=(0 if index == 0 else 3, 0 if index == 4 else 3),
            )
            self._settings_nav_buttons[name] = button
            page = tk.Frame(page_host, background=palette["bg"])
            page.grid(row=0, column=0, sticky="nsew")
            self._settings_pages[name] = page
        page_host.rowconfigure(0, weight=1)
        page_host.columnconfigure(0, weight=1)

        data_root = self._make_page_scroll(self._settings_pages["Data"], palette["bg"])
        data_card = self._make_settings_card(
            data_root,
            "Datasets & Checkpoints",
            "Choose one canonical HDF5 file for mixed labels, or use the legacy static/response pair.",
            palette["blue"],
            palette,
        )
        self._build_file_field_grid(
            data_card,
            [
                ("Canonical HDF5", self.var_dataset, "open"),
                ("Legacy static", self.var_static, "open"),
                ("Legacy response", self.var_response, "open"),
                ("Pretrained / base checkpoint", self.var_base_ckpt, "open"),
                ("Output checkpoint", self.var_out_ckpt, "save"),
            ],
            palette,
        )

        training_root = self._make_page_scroll(self._settings_pages["Training"], palette["bg"])
        train_card = self._make_settings_card(
            training_root,
            "Optimizer & Backbone",
            "Two aligned columns keep values readable across window sizes.",
            palette["mint"],
            palette,
        )
        self._build_field_grid(
            train_card,
            [
                ("Epochs", self.var_epochs, "entry", None),
                ("Batch size", self.var_bs, "entry", None),
                ("Learning rate", self.var_lr, "entry", None),
                ("Schedule", self.var_lr_scheduler, "combo", ["flat", "cosine"]),
                ("Force loss", self.var_force_loss, "combo", ["mse", "huber"]),
                ("Huber delta", self.var_force_huber_delta, "entry", None),
                ("Device", self.var_device, "combo", ["auto", "cpu", "mps", "cuda"]),
                (
                    "CPU threads",
                    self.var_cpu_threads,
                    "combo",
                    ["auto", *[str(value) for value in range(1, _available_cpu_threads() + 1)]],
                ),
                ("Dtype", self.var_dtype, "combo", ["float32", "float64"]),
                ("Cutoff r_max", self.var_rmax, "entry", None),
                ("Channels", self.var_channels, "entry", None),
                ("Interactions", self.var_interactions, "entry", None),
                ("Radial basis count", self.var_num_radial_basis, "entry", None),
                ("Field scale", self.var_field_scale, "entry", None),
                ("Validation fraction", self.var_val_fraction, "entry", None),
                ("Random seed", self.var_seed, "entry", None),
            ],
        )
        tk.Label(
            train_card,
            textvariable=self._model_size_text_var,
            background=palette["mint"],
            foreground=palette["muted"],
            font=("TkDefaultFont", 9, "bold"),
            justify="left",
            anchor="w",
            wraplength=490,
        ).pack(fill="x", pady=(2, 7))
        train_toggles = tk.Frame(train_card, background=palette["mint"])
        train_toggles.pack(fill="x", pady=(4, 0))
        _MacaronToggle(
            train_toggles,
            text="SevenNet export",
            variable=self.var_export_sevennet,
            width=142,
            background=palette["mint"],
            fill="#f8fcfa",
            hover_fill="#d7ebe2",
            selected_fill="#73b99a",
        ).pack(side="left", padx=(0, 8))
        _MacaronToggle(
            train_toggles,
            text="Live plots + artifacts",
            variable=self.var_save_epoch_artifacts,
            width=176,
            background=palette["mint"],
            fill="#f8fcfa",
            hover_fill="#d7ebe2",
            selected_fill="#73b99a",
        ).pack(side="left")
        cascade_card = self._make_settings_card(
            training_root,
            "Joint Fine-Tuning Cascade",
            "Base -> Response -> progressively lower-rate joint stages.",
            palette["lavender"],
            palette,
        )
        self._build_field_grid(
            cascade_card,
            [
                ("Joint stages", self.var_joint_stages, "entry", None),
                ("Warmup epochs", self.var_warmup_epochs, "entry", None),
                ("Base LR scale", self.var_lr_ground_scale, "entry", None),
                ("Response LR scale", self.var_lr_response_scale, "entry", None),
                ("Final dipole weight", self.var_w_dipole_final, "entry", None),
                ("Final alpha weight", self.var_w_alpha_final, "entry", None),
            ],
        )

        losses_root = self._make_page_scroll(self._settings_pages["Losses"], palette["bg"])
        losses_card = self._make_settings_card(
            losses_root,
            "Multi-Task Loss Weights",
            "Zero disables a target; only active targets enter AutoSearch.",
            palette["peach"],
            palette,
        )
        self._build_field_grid(
            losses_card,
            [
                ("Energy", self.var_we, "entry", None),
                ("Forces", self.var_wf, "entry", None),
                ("Dipole", self.var_wmu, "entry", None),
                ("Polarizability", self.var_walpha, "entry", None),
                ("Charges", self.var_w_charges, "entry", None),
                ("Atomic dipoles", self.var_w_atomic_dipoles, "entry", None),
                ("Atomic polarizability", self.var_w_atomic_polarizability, "entry", None),
                ("C6", self.var_w_c6, "entry", None),
                ("BEC", self.var_w_bec, "entry", None),
                ("Magnetic moments", self.var_w_magnetic_moments, "entry", None),
                ("Effective spin field", self.var_w_effective_field, "entry", None),
                ("J effective", self.var_w_j, "entry", None),
                ("Di", self.var_w_di, "entry", None),
                ("DMI", self.var_w_dmi, "entry", None),
            ],
        )

        physics_root = self._make_page_scroll(self._settings_pages["Physics"], palette["bg"])
        flags_card = self._make_settings_card(
            physics_root,
            "Architecture Switches",
            "Dataset labels and physical applicability control which switches are available.",
            palette["pink"],
            palette,
        )
        self._architecture_toggles = self._build_toggle_grid(
            flags_card,
            [
                ("e3mu_use_parity", "O(3) parity", self.var_e3mu_use_parity),
                ("e3mu_use_l3", "L=3 tensor", self.var_e3mu_use_l3),
                (
                    "enable_continuous_chem",
                    "Continuous chemistry",
                    self.var_enable_continuous_chem,
                ),
                ("enable_qeq", "QEq", self.var_enable_qeq),
                ("enable_pme", "PME / Ewald", self.var_enable_pme),
                ("enable_deq", "DEQ polarization", self.var_enable_deq),
                ("enable_d4", "D4 dispersion", self.var_enable_d4),
                ("enable_spin", "Spin J / Di / DMI", self.var_enable_spin),
                ("enable_film", "FiLM coupling", self.var_enable_film),
                ("enable_dmi", "DMI term", self.var_enable_dmi),
            ],
        )
        tk.Label(
            flags_card,
            textvariable=self._dataset_capability_text_var,
            background=palette["pink"],
            foreground=palette["muted"],
            font=("TkDefaultFont", 8),
            justify="left",
            anchor="w",
            wraplength=490,
        ).pack(fill="x", pady=(9, 0))
        radial_field = self._make_labeled_field(
            flags_card,
            "Radial basis family",
            self.var_rbf_type,
            "combo",
            ["gaussian", "trainable_gaussian", "bessel"],
            palette["pink"],
        )
        radial_field.pack(fill="x", pady=(10, 0))
        solver_card = self._make_settings_card(
            physics_root,
            "Physics Solver Parameters",
            "Long-range, stability, convergence, dispersion, spin, and coupling controls.",
            palette["lavender"],
            palette,
        )
        self._build_field_grid(
            solver_card,
            [
                ("QEq smearing", self.var_qeq_smearing, "entry", None),
                ("Hardness minimum", self.var_qeq_hardness_min, "entry", None),
                ("PME smearing", self.var_qeq_pme_smearing, "entry", None),
                ("PME wavelength", self.var_qeq_pme_lr_wavelength, "entry", None),
                ("QEq stability floor", self.var_qeq_stability_floor, "entry", None),
                ("DEQ max iterations", self.var_deq_max_iter, "entry", None),
                ("DEQ tolerance", self.var_deq_tol, "entry", None),
                ("DEQ damping", self.var_deq_damping, "entry", None),
                ("DEQ alpha max", self.var_deq_alpha_max, "entry", None),
                ("D4 functional", self.var_d4_functional, "entry", None),
                ("Spin cutoff", self.var_spin_cutoff, "entry", None),
                ("Coupling iterations", self.var_coupling_iterations, "entry", None),
                ("Coupling tolerance", self.var_coupling_tol, "entry", None),
            ],
        )

        search_root = self._make_page_scroll(self._settings_pages["Search"], palette["bg"])
        search_card = self._make_settings_card(
            search_root,
            "AutoSearch",
            "Candidates are ranked with normalized multi-task validation MAE.",
            palette["yellow"],
            palette,
        )
        self._build_field_grid(
            search_card,
            [
                ("Search level", self.var_auto_level, "combo", [
                    "0: Disabled", "1: Loss Weights", "2: All Hyperparams",
                    "3: HP + JFT", "4: HP + JFT + Architecture",
                ]),
                ("Trials", self.var_auto_trials, "entry", None),
                ("Trial epochs", self.var_auto_trial_epochs, "entry", None),
                ("Sample %", self.var_auto_subset, "entry", None),
            ],
        )
        auto_actions = tk.Frame(search_card, background=palette["yellow"])
        auto_actions.pack(fill="x", pady=(4, 0))
        auto_run_button = _MacaronButton(
            auto_actions,
            text="Run AutoSearch",
            command=self._run_auto_search,
            width=150,
            background=palette["yellow"],
            fill=palette["lavender_strong"],
            hover_fill="#8973ca",
            selected_fill="#7962ba",
            foreground="#ffffff",
        )
        auto_run_button.pack(side="left", padx=(0, 8))
        self._training_buttons.append(auto_run_button)
        self._auto_apply_button = _MacaronButton(
            auto_actions,
            text="Apply Best",
            command=self._apply_saved_auto_best,
            width=126,
            background=palette["yellow"],
            fill="#f3e5bd",
            hover_fill="#ead59a",
            selected_fill="#cfaa53",
            foreground=palette["text"],
        )
        self._auto_apply_button.pack(side="left")
        self._auto_apply_button.set_enabled(False, "Run AutoSearch first")
        tk.Label(
            search_card,
            textvariable=self._auto_best_text_var,
            background=palette["yellow"],
            foreground=palette["muted"],
            font=("TkDefaultFont", 9, "bold"),
            anchor="w",
            justify="left",
            wraplength=490,
        ).pack(fill="x", pady=(8, 0))
        table_card = self._make_settings_card(
            search_root,
            "Search Trials",
            "Best and most recent values update as trials finish.",
            palette["surface"],
            palette,
        )
        columns = ("parameter", "best", "tried", "status")
        self._auto_tree = ttk.Treeview(table_card, columns=columns, show="headings", height=10)
        for name, title, width in (
            ("parameter", "Parameter", 170),
            ("best", "Best", 90),
            ("tried", "Last", 90),
            ("status", "Status", 70),
        ):
            self._auto_tree.heading(name, text=title)
            self._auto_tree.column(name, width=width, anchor="w" if name == "parameter" else "center")
        tree_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self._auto_tree.yview)
        self._auto_tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")
        self._auto_tree.pack(side="left", fill="both", expand=True)
        self.var_auto_level.trace_add(
            "write",
            lambda *_args: self._reset_auto_tree(int(self.var_auto_level.get()[0])),
        )

        self._show_settings_page("Data")
        self._build_dashboard(dashboard_panel, palette)

    def _build_ui_legacy_reference(self):
        """Retained as a non-production reference for legacy config migrations."""
        self._configure_modern_theme()
        shell = ttk.Frame(self, style="App.TFrame")
        shell.pack(fill="both", expand=True)

        header = ttk.Frame(shell, style="Header.TFrame", padding=(22, 15))
        header.pack(fill="x")
        brand = ttk.Frame(header, style="Header.TFrame")
        brand.pack(side="left", fill="x", expand=True)
        ttk.Label(brand, text="Mixed-Granularity E(3)-mu-GNN", style="HeaderTitle.TLabel").pack(anchor="w")
        ttk.Label(
            brand,
            text="L1 local chemistry  /  L2 electrostatics & response  /  L3 spin Hamiltonian",
            style="HeaderSub.TLabel",
        ).pack(anchor="w", pady=(2, 0))
        header_state = ttk.Frame(header, style="Header.TFrame")
        header_state.pack(side="right")
        ttk.Label(header_state, textvariable=self._run_status_var, style="Status.TLabel").pack(anchor="e")
        ttk.Label(header_state, textvariable=self._progress_text_var, style="HeaderSub.TLabel").pack(anchor="e", pady=(3, 0))

        body = ttk.Panedwindow(shell, orient="horizontal")
        body.pack(fill="both", expand=True, padx=14, pady=14)
        settings_panel = ttk.Frame(body, style="App.TFrame", width=540)
        dashboard_panel = ttk.Frame(body, style="App.TFrame", width=900)
        body.add(settings_panel, weight=4)
        body.add(dashboard_panel, weight=6)
        root = self._make_scrollable(settings_panel)

        cfgbar = ttk.Frame(root, style="App.TFrame")
        cfgbar.pack(fill="x", padx=(0, 8), pady=(0, 8))
        ttk.Button(cfgbar, text="Import", command=self._import_config).pack(side="left")
        ttk.Button(cfgbar, text="Export", command=self._export_config).pack(side="left", padx=5)
        ttk.Button(cfgbar, text="Save Default", command=self._save_default_config).pack(side="left")
        ttk.Button(cfgbar, text="Factory Reset", command=self._reset_factory_config).pack(side="right")

        lf = ttk.Labelframe(root, text="Data & Checkpoints", style="Card.TLabelframe", padding=10)
        lf.pack(fill="x", padx=(0, 8), pady=(0, 8))
        rows = [
            ("Canonical HDF5", self.var_dataset, "open"),
            ("Legacy static", self.var_static, "open"),
            ("Legacy response", self.var_response, "open"),
            ("Pretrained / base checkpoint", self.var_base_ckpt, "open"),
            ("Output checkpoint", self.var_out_ckpt, "save"),
        ]
        for i, (lbl, var, browse_mode) in enumerate(rows):
            ttk.Label(lf, text=lbl, style="Card.TLabel").grid(row=i, column=0, sticky="w", padx=(0, 8), pady=4)
            ttk.Entry(lf, textvariable=var).grid(row=i, column=1, sticky="ew", pady=4)
            if browse_mode == "open":
                ttk.Button(
                    lf,
                    text="Choose",
                    command=lambda v=var: v.set(filedialog.askopenfilename() or v.get()),
                ).grid(row=i, column=2, padx=(8, 0), pady=4)
            elif browse_mode == "save":
                ttk.Button(
                    lf,
                    text="Choose",
                    command=lambda v=var: v.set(
                        filedialog.asksaveasfilename(
                            defaultextension=".pt",
                            filetypes=[
                                ("PyTorch Checkpoint", "*.pt"),
                                ("PyTorch Model", "*.pth"),
                                ("All files", "*.*"),
                            ],
                        ) or v.get()
                    ),
                ).grid(row=i, column=2, padx=(8, 0), pady=4)
        lf.columnconfigure(1, weight=1)

        hp = ttk.Labelframe(root, text="Training & Backbone", style="Card.TLabelframe", padding=10)
        hp.pack(fill="x", padx=(0, 8), pady=8)
        def add(r, c, txt, var):
            ttk.Label(hp, text=txt, style="Card.TLabel").grid(row=r, column=c, sticky="w", padx=(0, 5), pady=4)
            ttk.Entry(hp, textvariable=var, width=9).grid(row=r, column=c+1, sticky="ew", padx=(0, 10), pady=4)
        add(0, 0, "Epochs",       self.var_epochs)
        add(0, 2, "Batch Size",   self.var_bs)
        add(0, 4, "LR",           self.var_lr)
        ttk.Label(hp, text="Schedule", style="Card.TLabel").grid(row=0, column=6, sticky="w", padx=(0, 5))
        ttk.Combobox(hp, textvariable=self.var_lr_scheduler,
                     values=["flat", "cosine"], state="readonly", width=8
                     ).grid(row=0, column=7, sticky="ew", pady=4)
        ttk.Label(hp, text="Device", style="Card.TLabel").grid(row=1, column=6, sticky="w", padx=(0, 5))
        ttk.Combobox(hp, textvariable=self.var_device,
                     values=["auto", "cpu", "mps", "cuda"], state="readonly", width=8
                     ).grid(row=1, column=7, sticky="ew", pady=4)
        add(1, 0, "r_max",        self.var_rmax)
        add(1, 2, "Channels",     self.var_channels)
        add(1, 4, "Interactions", self.var_interactions)
        add(2, 0, "Radial Basis", self.var_num_radial_basis)
        add(2, 2, "Field Scale",  self.var_field_scale)
        add(2, 4, "Val Fraction", self.var_val_fraction)
        add(2, 6, "Seed",         self.var_seed)
        ttk.Label(hp, text="Dtype", style="Card.TLabel").grid(row=3, column=0, sticky="w")
        ttk.Combobox(hp, textvariable=self.var_dtype,
                     values=["float32", "float64"], state="readonly", width=8
                     ).grid(row=3, column=1, sticky="ew", padx=(0, 10), pady=4)
        ttk.Checkbutton(hp, text="Export SevenNet TS",
                        variable=self.var_export_sevennet).grid(row=3, column=2, columnspan=2, sticky="w", padx=4)
        ttk.Checkbutton(hp, text="Epoch artifacts + live plots",
                        variable=self.var_save_epoch_artifacts).grid(row=3, column=4, columnspan=4, sticky="w", padx=4)
        ttk.Checkbutton(hp, text="Stream canonical HDF5",
                        variable=self.var_stream_hdf5).grid(row=4, column=0, columnspan=3, sticky="w", padx=4)
        ttk.Checkbutton(hp, text="Disk topology cache",
                        variable=self.var_cache_neighbor_graphs).grid(row=4, column=3, columnspan=3, sticky="w", padx=4)
        for column in (1, 3, 5, 7):
            hp.columnconfigure(column, weight=1)

        losses = ttk.Labelframe(root, text="Multi-Task Loss Weights  (0 disables target)", style="Card.TLabelframe", padding=10)
        losses.pack(fill="x", padx=(0, 8), pady=8)
        loss_vars = [
            ("Energy", self.var_we), ("Forces", self.var_wf),
            ("Dipole", self.var_wmu), ("Polarizability", self.var_walpha),
            ("Charges", self.var_w_charges), ("Atomic dipoles", self.var_w_atomic_dipoles),
            ("Atomic polarizability", self.var_w_atomic_polarizability), ("C6", self.var_w_c6),
            ("BEC", self.var_w_bec), ("Magnetic moments", self.var_w_magnetic_moments),
            ("Effective spin field", self.var_w_effective_field), ("J effective", self.var_w_j),
            ("Di", self.var_w_di), ("DMI", self.var_w_dmi),
        ]
        for index, (label, variable) in enumerate(loss_vars):
            row, pair = divmod(index, 4)
            column = pair * 2
            ttk.Label(losses, text=label, style="Card.TLabel").grid(row=row, column=column, sticky="w", padx=(0, 5), pady=4)
            ttk.Entry(losses, textvariable=variable, width=9).grid(row=row, column=column + 1, sticky="ew", padx=(0, 10), pady=4)
        for column in (1, 3, 5, 7):
            losses.columnconfigure(column, weight=1)

        phys = ttk.Labelframe(root, text="Physics & Architecture", style="Card.TLabelframe", padding=10)
        phys.pack(fill="x", padx=(0, 8), pady=8)
        ttk.Checkbutton(phys, text="O(3) Parity  (e3mu_use_parity)",
                        variable=self.var_e3mu_use_parity).grid(row=0, column=0, columnspan=2, sticky="w", padx=6)
        ttk.Checkbutton(phys, text="L=3 ST Tensor  (e3mu_use_l3)",
                        variable=self.var_e3mu_use_l3).grid(row=0, column=2, columnspan=2, sticky="w", padx=6)
        ttk.Checkbutton(phys, text="Continuous Chem Embedding",
                        variable=self.var_enable_continuous_chem).grid(row=0, column=4, columnspan=2, sticky="w", padx=6)
        ttk.Label(phys, text="RBF type:").grid(row=1, column=0, sticky="w", padx=6, pady=2)
        ttk.Combobox(phys, textvariable=self.var_rbf_type,
                     values=["gaussian", "trainable_gaussian", "bessel"],
                     width=20, state="readonly").grid(row=1, column=1, columnspan=2, sticky="w")
        physics_flags = [
            ("QEq", self.var_enable_qeq), ("PME / Ewald", self.var_enable_pme),
            ("DEQ polarization", self.var_enable_deq), ("D4 dispersion", self.var_enable_d4),
            ("Spin J/Di/DMI", self.var_enable_spin), ("FiLM coupling", self.var_enable_film),
            ("DMI term", self.var_enable_dmi),
        ]
        for index, (label, variable) in enumerate(physics_flags):
            ttk.Checkbutton(phys, text=label, variable=variable).grid(
                row=2 + index // 4, column=(index % 4) * 2,
                columnspan=2, sticky="w", padx=6, pady=1,
            )

        solver = ttk.Labelframe(root, text="Physics Solver Parameters", style="Card.TLabelframe", padding=10)
        solver.pack(fill="x", padx=(0, 8), pady=8)
        solver_vars = [
            ("QEq smearing", self.var_qeq_smearing),
            ("Hardness min", self.var_qeq_hardness_min),
            ("PME smearing", self.var_qeq_pme_smearing),
            ("PME wavelength", self.var_qeq_pme_lr_wavelength),
            ("QEq stability", self.var_qeq_stability_floor),
            ("DEQ max iter", self.var_deq_max_iter),
            ("DEQ tolerance", self.var_deq_tol),
            ("DEQ damping", self.var_deq_damping),
            ("DEQ alpha max", self.var_deq_alpha_max),
            ("D4 functional", self.var_d4_functional),
            ("Spin cutoff", self.var_spin_cutoff),
            ("Coupling iter", self.var_coupling_iterations),
            ("Coupling tol", self.var_coupling_tol),
        ]
        for index, (label, variable) in enumerate(solver_vars):
            row, pair = divmod(index, 4)
            column = pair * 2
            ttk.Label(solver, text=label, style="Card.TLabel").grid(row=row, column=column, sticky="w", padx=(0, 5), pady=4)
            ttk.Entry(solver, textvariable=variable, width=9).grid(row=row, column=column + 1, sticky="ew", padx=(0, 10), pady=4)
        for column in (1, 3, 5, 7):
            solver.columnconfigure(column, weight=1)

        jft = ttk.Labelframe(root, text="Joint Fine-Tuning Cascade", style="Card.TLabelframe", padding=10)
        jft.pack(fill="x", padx=(0, 8), pady=8)
        def jadd(r, c, txt, var, w=6):
            ttk.Label(jft, text=txt).grid(row=r, column=c, sticky="w", padx=4)
            ttk.Entry(jft, textvariable=var, width=w).grid(row=r, column=c+1, sticky="w")
        jadd(0, 0, "Joint Stages",      self.var_joint_stages, 4)
        jadd(0, 2, "LR Base Scale",     self.var_lr_ground_scale)
        jadd(0, 4, "LR Response Scale", self.var_lr_response_scale)
        jadd(1, 0, "Warmup Epochs",     self.var_warmup_epochs, 4)
        jadd(1, 2, "w_dipole final",    self.var_w_dipole_final)
        jadd(1, 4, "w_alpha final",     self.var_w_alpha_final)
        ttk.Label(jft,
                  text="Stages: Base→Response→JFT×N  |  LR scales: base×scale, response×scale  |  Warmup: freeze base N epochs each JFT stage",
                  style="Muted.Card.TLabel").grid(row=2, column=0, columnspan=8, sticky="w", padx=4, pady=(4, 0))

        asf = ttk.Labelframe(root, text="AutoSearch", style="Card.TLabelframe", padding=10)
        asf.pack(fill="x", padx=(0, 8), pady=8)

        _asrow = ttk.Frame(asf); _asrow.pack(fill="x", padx=4, pady=(4, 2))
        ttk.Label(_asrow, text="Level:").pack(side="left")
        _level_cb = ttk.Combobox(
            _asrow, textvariable=self.var_auto_level,
            values=["0: Disabled", "1: Loss Weights", "2: All Hyperparams",
                    "3: HP + JFT", "4: HP + JFT + Architecture"],
            width=28, state="readonly",
        )
        _level_cb.pack(side="left", padx=(2, 10))
        ttk.Label(_asrow, text="Trials:").pack(side="left")
        ttk.Entry(_asrow, textvariable=self.var_auto_trials, width=5).pack(side="left", padx=(2, 8))
        ttk.Label(_asrow, text="Trial Epochs:").pack(side="left")
        ttk.Entry(_asrow, textvariable=self.var_auto_trial_epochs, width=5).pack(side="left", padx=(2, 8))
        ttk.Label(_asrow, text="Sample%:").pack(side="left")
        ttk.Entry(_asrow, textvariable=self.var_auto_subset, width=5).pack(side="left", padx=(2, 10))
        ttk.Button(_asrow, text="Run AutoSearch", style="Primary.TButton", command=self._run_auto_search).pack(side="left")

        _tree_frame = ttk.Frame(asf); _tree_frame.pack(fill="x", padx=4, pady=(0, 4))
        cols = ("parameter", "best", "tried", "status")
        self._auto_tree = ttk.Treeview(_tree_frame, columns=cols, show="headings", height=6)
        self._auto_tree.heading("parameter", text="Parameter")
        self._auto_tree.heading("best",      text="Best Value")
        self._auto_tree.heading("tried",     text="Last Tried")
        self._auto_tree.heading("status",    text="Status")
        self._auto_tree.column("parameter", width=180, anchor="w")
        self._auto_tree.column("best",      width=100, anchor="center")
        self._auto_tree.column("tried",     width=100, anchor="center")
        self._auto_tree.column("status",    width=90,  anchor="center")
        _tree_sb2 = ttk.Scrollbar(_tree_frame, orient="vertical", command=self._auto_tree.yview)
        self._auto_tree.configure(yscrollcommand=_tree_sb2.set)
        self._auto_tree.pack(side="left", fill="x", expand=True)
        _tree_sb2.pack(side="right", fill="y")

        _level_cb.bind("<<ComboboxSelected>>",
                       lambda _e: self._reset_auto_tree(int(self.var_auto_level.get()[0])))

        self._build_dashboard(dashboard_panel)

    def _build_dashboard(
        self, parent: Any, palette: Optional[Dict[str, str]] = None
    ) -> None:
        """Build the persistent training controls, live plots, and log surface."""
        palette = palette or {
            "bg": "#f7f4fa",
            "surface": "#fffdfd",
            "text": "#3d3a50",
            "muted": "#777287",
            "lavender": "#eee9f8",
            "lavender_strong": "#9b87d8",
            "mint": "#e3f3ec",
            "peach": "#fbe9df",
            "blue": "#e4eef9",
            "pink": "#f7e5ed",
            "yellow": "#f8f0d8",
        }
        control_surface = _RoundedCard(
            parent,
            fill=palette["surface"],
            background=palette["bg"],
            radius=21,
            padding=13,
            shadow="#e8e2ec",
        )
        control_surface.pack(fill="x", pady=(0, 10))
        control_card = control_surface.body
        controls = tk.Frame(control_card, background=palette["surface"])
        controls.pack(fill="x")
        control_buttons = [
            ("Mixed Joint", lambda: self._start("joint"), palette["lavender_strong"], "#ffffff", 118),
            ("Base", lambda: self._start("base"), palette["mint"], palette["text"], 70),
            ("Response", lambda: self._start("response"), palette["blue"], palette["text"], 96),
            ("Full Chain", self._run_full_chain, palette["peach"], palette["text"], 98),
            ("Artifacts", self._open_artifacts, palette["yellow"], palette["text"], 86),
        ]
        for text_value, command, fill, foreground, width in control_buttons:
            button = _MacaronButton(
                controls,
                text=text_value,
                command=command,
                width=width,
                height=37,
                background=palette["surface"],
                fill=fill,
                hover_fill=palette["lavender"],
                selected_fill=palette["lavender_strong"],
                foreground=foreground,
            )
            button.pack(side="left", padx=(0, 7))
            self._training_buttons.append(button)
        _MacaronButton(
            controls,
            text="Stop",
            command=self._stop_fn,
            width=70,
            height=37,
            background=palette["surface"],
            fill=palette["pink"],
            hover_fill="#efd2dd",
            selected_fill="#c86b7c",
            foreground="#a4495d",
        ).pack(side="right")
        self.progress = ttk.Progressbar(
            control_card, mode="determinate", style="Accent.Horizontal.TProgressbar"
        )
        self.progress.pack(fill="x", pady=(12, 0))

        metrics = tk.Frame(parent, background=palette["bg"])
        metrics.pack(fill="x", pady=(0, 10))
        metrics.columnconfigure((0, 1, 2), weight=1, uniform="metric")
        metric_specs = [
            ("STATE", self._run_status_var, palette["mint"]),
            ("PROGRESS", self._epoch_status_var, palette["blue"]),
            ("NORMALIZED VALIDATION", self._score_status_var, palette["peach"]),
        ]
        for column, (label, variable, fill) in enumerate(metric_specs):
            card_surface = _RoundedCard(
                metrics,
                fill=fill,
                background=palette["bg"],
                radius=18,
                padding=12,
                shadow="#e8e2ec",
                height=78,
            )
            card_surface.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=(0 if column == 0 else 5, 0 if column == 2 else 5),
            )
            tk.Label(
                card_surface.body,
                text=label,
                background=fill,
                foreground=palette["muted"],
                font=("TkDefaultFont", 8, "bold"),
            ).pack(anchor="w")
            tk.Label(
                card_surface.body,
                textvariable=variable,
                background=fill,
                foreground=palette["text"],
                font=("TkDefaultFont", 13, "bold"),
            ).pack(anchor="w", pady=(4, 0))

        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)
        live_tab = ttk.Frame(notebook, style="Surface.TFrame", padding=10)
        log_tab = ttk.Frame(notebook, style="Surface.TFrame", padding=10)
        notebook.add(live_tab, text="Live Analysis")
        notebook.add(log_tab, text="Training Log")

        live_toolbar = ttk.Frame(live_tab, style="Card.TFrame")
        live_toolbar.pack(fill="x", pady=(0, 8))
        ttk.Label(live_toolbar, text="View", style="Card.TLabel").pack(side="left")
        live_view = ttk.Combobox(
            live_toolbar,
            textvariable=self.var_live_plot,
            values=["Regression", "MAE History", "Multi-Task", "Physics Residuals"],
            state="readonly",
            width=20,
        )
        live_view.pack(side="left", padx=(7, 0))
        live_view.bind("<<ComboboxSelected>>", lambda _e: self._render_live_dashboard())
        ttk.Label(
            live_toolbar,
            text="Updates after each validation epoch",
            style="Muted.Card.TLabel",
        ).pack(side="right")

        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure

            self._live_figure = Figure(figsize=(8.8, 5.8), dpi=100, facecolor="#ffffff")
            self._live_canvas = FigureCanvasTkAgg(self._live_figure, master=live_tab)
            canvas_widget = self._live_canvas.get_tk_widget()
            canvas_widget.configure(background="#ffffff", highlightthickness=0)
            canvas_widget.pack(fill="both", expand=True)
            self._render_live_dashboard()
        except Exception as exc:
            self._live_figure = None
            self._live_canvas = None
            ttk.Label(
                live_tab,
                text=f"Live charts unavailable: {exc}",
                style="Muted.Card.TLabel",
            ).pack(expand=True)

        log_container = ttk.Frame(log_tab, style="Card.TFrame")
        log_container.pack(fill="both", expand=True)
        self.log_widget = tk.Text(
            log_container,
            height=10,
            wrap="word",
            relief="flat",
            borderwidth=0,
            background="#101827",
            foreground="#d8e2f0",
            insertbackground="#ffffff",
            selectbackground="#315c9f",
            padx=12,
            pady=10,
        )
        log_scroll = ttk.Scrollbar(log_container, orient="vertical", command=self.log_widget.yview)
        self.log_widget.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side="right", fill="y")
        self.log_widget.pack(side="left", fill="both", expand=True)
        self.logger = GuiLogger(self.log_widget)

    @staticmethod
    def _finite_history_values(history: Sequence[Dict[str, Any]], key: str) -> Tuple[List[int], List[float]]:
        epochs: List[int] = []
        values: List[float] = []
        for item in history:
            value = item.get(key)
            if value is None:
                continue
            number = float(value)
            if not math.isfinite(number):
                continue
            epochs.append(int(item.get("epoch", len(epochs) + 1)))
            values.append(number)
        return epochs, values

    def _style_live_axis(self, axis: Any, title: str, ylabel: str = "") -> None:
        axis.set_facecolor("#ffffff")
        axis.set_title(title, loc="left", fontsize=11, fontweight="bold", color="#172033", pad=10)
        axis.set_xlabel("Epoch", color="#667085", fontsize=9)
        if ylabel:
            axis.set_ylabel(ylabel, color="#667085", fontsize=9)
        axis.grid(True, color="#e7ebf1", linewidth=0.8, alpha=0.9)
        axis.tick_params(colors="#667085", labelsize=8)
        for spine in axis.spines.values():
            spine.set_color("#d8dee9")

    def _render_live_dashboard(self) -> None:
        """Redraw the selected analysis view from in-memory epoch metrics."""
        if self._live_figure is None or self._live_canvas is None:
            return
        figure = self._live_figure
        figure.clear()
        view = str(self.var_live_plot.get() or "Regression")
        history = list(self._live_metric_history)

        if not history:
            axis = figure.add_subplot(111)
            axis.set_axis_off()
            axis.text(
                0.5, 0.54, "Live analysis is ready", ha="center", va="center",
                fontsize=16, fontweight="bold", color="#172033", transform=axis.transAxes,
            )
            axis.text(
                0.5, 0.44,
                "Start training to stream validation metrics and plots after every epoch.",
                ha="center", va="center", fontsize=10, color="#667085", transform=axis.transAxes,
            )
            figure.tight_layout(pad=2.0)
            self._live_canvas.draw_idle()
            return

        colors = {
            "energy": "#3167e3",
            "forces": "#e4872b",
            "train": "#667085",
            "score": "#7a5af8",
            "residual": "#159570",
        }
        if view == "Regression":
            image_path = self._latest_regression_image()
            if image_path is not None:
                axis = figure.add_subplot(111)
                from matplotlib import image as mpl_image
                image_data = mpl_image.imread(str(image_path))
                axis.imshow(image_data)
                axis.set_axis_off()
                axis.set_title(
                    f"Latest validation parity  /  {image_path.name}", loc="left",
                    fontsize=11, fontweight="bold", color="#172033", pad=8,
                )
            else:
                view = "MAE History"

        if view == "MAE History":
            left = figure.add_subplot(121)
            right = figure.add_subplot(122)
            for key, label, color in (
                ("train_loss", "Train loss", colors["train"]),
                ("val_loss", "Validation loss", colors["score"]),
            ):
                x, y = self._finite_history_values(history, key)
                if y:
                    left.plot(x, y, marker="o", markersize=3, linewidth=1.8, label=label, color=color)
            self._style_live_axis(left, "Objective history", "Loss")
            if left.lines:
                left.legend(frameon=False, fontsize=8)
            for key, label, color in (
                ("energy_mae", "Energy MAE", colors["energy"]),
                ("force_mae", "Force MAE", colors["forces"]),
                ("validation_score", "Normalized score", colors["score"]),
            ):
                x, y = self._finite_history_values(history, key)
                if y:
                    right.plot(x, y, marker="o", markersize=3, linewidth=1.8, label=label, color=color)
            self._style_live_axis(right, "Validation quality", "MAE / score")
            if right.lines:
                right.legend(frameon=False, fontsize=8)

        elif view == "Multi-Task":
            metric_names = sorted({
                name for item in history for name in item.get("multitask_mae", {})
            })
            axis = figure.add_subplot(111)
            palette = ["#3167e3", "#e4872b", "#159570", "#7a5af8", "#d14f69", "#70859f"]
            for index, name in enumerate(metric_names):
                x: List[int] = []
                y: List[float] = []
                for item in history:
                    value = item.get("multitask_mae", {}).get(name)
                    if value is not None and math.isfinite(float(value)):
                        x.append(int(item["epoch"]))
                        y.append(float(value))
                if y:
                    axis.plot(x, y, marker="o", markersize=3, linewidth=1.6,
                              label=name, color=palette[index % len(palette)])
            self._style_live_axis(axis, "Active multi-task validation MAE", "MAE")
            if axis.lines:
                axis.legend(frameon=False, fontsize=8, ncol=min(3, max(1, len(metric_names))))
            else:
                axis.text(0.5, 0.5, "No auxiliary targets are active", ha="center", va="center",
                          color="#667085", transform=axis.transAxes)

        elif view == "Physics Residuals":
            names = sorted({
                name for item in history for name in item.get("physics_residual_max", {})
            })
            axis = figure.add_subplot(111)
            palette = ["#159570", "#3167e3", "#e4872b", "#7a5af8", "#d14f69"]
            for index, name in enumerate(names):
                x: List[int] = []
                y: List[float] = []
                for item in history:
                    value = item.get("physics_residual_max", {}).get(name)
                    if value is not None and math.isfinite(float(value)):
                        x.append(int(item["epoch"]))
                        y.append(max(float(value), 1e-16))
                if y:
                    axis.semilogy(x, y, marker="o", markersize=3, linewidth=1.6,
                                  label=name, color=palette[index % len(palette)])
            self._style_live_axis(axis, "Physics solver diagnostics", "Validation maximum")
            if axis.lines:
                axis.legend(frameon=False, fontsize=8, ncol=min(3, max(1, len(names))))
            else:
                axis.text(0.5, 0.5, "No iterative physics solver is active", ha="center", va="center",
                          color="#667085", transform=axis.transAxes)

        figure.tight_layout(pad=1.5)
        self._live_canvas.draw_idle()

    def _latest_regression_image(self) -> Optional[Path]:
        artifact_dir = self._live_artifact_dir or self._artifact_dir_for_checkpoint(
            self.var_out_ckpt.get()
        )
        plots_dir = artifact_dir / "plots"
        candidates = sorted(plots_dir.glob("regression_full_epoch_*.png"))
        return candidates[-1] if candidates else None

    def _reset_live_dashboard(self, checkpoint_value: Optional[str] = None) -> None:
        self._live_metric_history.clear()
        self._live_artifact_dir = self._artifact_dir_for_checkpoint(
            checkpoint_value or self.var_out_ckpt.get()
        )
        self._run_status_var.set("Preparing")
        self._epoch_status_var.set("Epoch 0 / --")
        self._score_status_var.set("Score --")
        self._render_live_dashboard()

    def _consume_metric_event(self, event: Dict[str, Any]) -> None:
        self._live_metric_history.append(dict(event))
        artifact_value = event.get("artifact_dir")
        if artifact_value:
            self._live_artifact_dir = Path(str(artifact_value))
        epoch = int(event.get("epoch", 0))
        epochs = int(event.get("epochs", 0))
        score = float(event.get("validation_score", float("nan")))
        self._run_status_var.set("Training")
        self._epoch_status_var.set(f"Epoch {epoch} / {epochs}")
        self._score_status_var.set(
            f"Score {score:.4g}" if math.isfinite(score) else "Score --"
        )
        self._render_live_dashboard()

    def _set_training_running(self, running: bool) -> None:
        self._training_running = bool(running)
        for button in self._training_buttons:
            button.set_enabled(not self._training_running)
        if self._auto_apply_button is not None:
            self._auto_apply_button.set_enabled(
                bool(self._auto_best_params) and not self._training_running,
                "Training is running" if self._training_running else "Run AutoSearch first",
            )

    def _fmt_eta(self, eta_s: float) -> str:
        if not math.isfinite(eta_s) or eta_s < 0:
            return "ETA ?"
        m, s = divmod(int(round(eta_s)), 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"ETA {h:d}:{m:02d}:{s:02d}"
        return f"ETA {m:02d}:{s:02d}"

    def _stop_fn(self):
        self._stop = True
        self._run_status_var.set("Stopping")

    def _open_artifacts(self) -> None:
        artifact_dir = self._live_artifact_dir or self._artifact_dir_for_checkpoint(
            self.var_out_ckpt.get()
        )
        artifact_dir.mkdir(parents=True, exist_ok=True)
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", str(artifact_dir)])
            elif os.name == "nt":
                os.startfile(str(artifact_dir))  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", str(artifact_dir)])
        except Exception as exc:
            messagebox.showerror("Open Artifacts", f"Could not open {artifact_dir}: {exc}")

    def _build_gui_model_config(self) -> ModelConfig:
        extended_electric = any(
            float(variable.get()) > 0.0
            for variable in (
                self.var_w_charges,
                self.var_w_atomic_dipoles,
                self.var_w_atomic_polarizability,
            )
        )
        spin_supervised = any(
            float(variable.get()) > 0.0
            for variable in (
                self.var_w_magnetic_moments,
                self.var_w_effective_field,
                self.var_w_j,
                self.var_w_di,
                self.var_w_dmi,
            )
        )
        required_switches: Dict[str, bool] = {
            "enable_qeq": extended_electric or float(self.var_w_c6.get()) > 0.0,
            "enable_d4": float(self.var_w_c6.get()) > 0.0,
            "enable_spin": spin_supervised,
            "enable_dmi": float(self.var_w_dmi.get()) > 0.0,
        }
        for switch, required in required_switches.items():
            if required and switch in self._architecture_disabled_reasons:
                reason = self._architecture_disabled_reasons[switch]
                raise ValueError(
                    f"The active loss weights require {switch}, but the selected "
                    f"dataset disables it: {reason}. Set the unsupported loss weight "
                    "to zero or select a compatible dataset."
                )
        if extended_electric:
            self.var_enable_qeq.set(True)
        if float(self.var_w_c6.get()) > 0.0:
            self.var_enable_d4.set(True)
            self.var_enable_qeq.set(True)
        if spin_supervised:
            self.var_enable_spin.set(True)
        if float(self.var_w_dmi.get()) > 0.0:
            self.var_enable_dmi.set(True)
        use_parity = bool(self.var_e3mu_use_parity.get())
        use_l3 = bool(self.var_e3mu_use_l3.get())
        enable_film = bool(self.var_enable_film.get())
        enable_pme = bool(self.var_enable_pme.get())
        enable_qeq = bool(self.var_enable_qeq.get()) or enable_pme
        if use_l3 or enable_film or (bool(self.var_enable_spin.get()) and bool(self.var_enable_dmi.get())):
            use_parity = True
            self.var_e3mu_use_parity.set(True)
        if enable_pme:
            self.var_enable_qeq.set(True)
        if enable_pme and not HAS_TORCHPME:
            raise RuntimeError("PME requires torch-pme. Install dependencies from requirements.txt.")
        if bool(self.var_enable_d4.get()) and not HAS_TAD_DFTD4:
            raise RuntimeError("D4 requires tad-dftd4. Install dependencies from requirements.txt.")
        return ModelConfig(
            r_max=float(self.var_rmax.get()),
            num_channels=int(self.var_channels.get()),
            num_interactions=int(self.var_interactions.get()),
            num_radial_basis=int(self.var_num_radial_basis.get()),
            field_scale=float(self.var_field_scale.get()),
            dtype=str(self.var_dtype.get()),
            e3mu_use_parity=use_parity,
            e3mu_use_l3=use_l3,
            rbf_type=str(self.var_rbf_type.get()),
            enable_continuous_chem=bool(self.var_enable_continuous_chem.get()),
            chem_max_z=int(self.var_chem_max_z.get()),
            chem_aug_prob=float(self.var_chem_aug_prob.get()),
            chem_aug_noise_std=float(self.var_chem_aug_noise_std.get()),
            chem_aug_mix_max=float(self.var_chem_aug_mix_max.get()),
            enable_qeq=enable_qeq,
            enable_pme=enable_pme,
            enable_deq=bool(self.var_enable_deq.get()),
            enable_d4=bool(self.var_enable_d4.get()),
            enable_spin=bool(self.var_enable_spin.get()),
            enable_film=enable_film,
            enable_dmi=bool(self.var_enable_dmi.get()),
            qeq_smearing=float(self.var_qeq_smearing.get()),
            qeq_hardness_min=float(self.var_qeq_hardness_min.get()),
            qeq_pme_smearing=float(self.var_qeq_pme_smearing.get()),
            qeq_pme_lr_wavelength=float(self.var_qeq_pme_lr_wavelength.get()),
            qeq_stability_floor=float(self.var_qeq_stability_floor.get()),
            deq_max_iter=int(self.var_deq_max_iter.get()),
            deq_tol=float(self.var_deq_tol.get()),
            deq_damping=float(self.var_deq_damping.get()),
            deq_alpha_max=float(self.var_deq_alpha_max.get()),
            d4_functional=str(self.var_d4_functional.get()),
            spin_cutoff=float(self.var_spin_cutoff.get()),
            coupling_iterations=int(self.var_coupling_iterations.get()),
            coupling_tol=float(self.var_coupling_tol.get()),
        )

    def _gui_common_train_kwargs(self) -> Dict[str, Any]:
        dataset = self.var_dataset.get().strip()
        if dataset and not _is_hdf5_path(dataset):
            raise ValueError("Canonical dataset must be an HDF5 file (.h5/.hdf5).")
        return {
            "device": str(self.var_device.get()),
            "cpu_threads": _parse_cpu_threads(self.var_cpu_threads.get()),
            "dataset": dataset,
            "static_data": self.var_static.get().strip(),
            "response_data": self.var_response.get().strip(),
            "model": self._build_gui_model_config(),
            "batch_size": int(self.var_bs.get()),
            "val_fraction": float(self.var_val_fraction.get()),
            "seed": int(self.var_seed.get()),
            "w_energy": float(self.var_we.get()),
            "w_forces": float(self.var_wf.get()),
            "force_loss": str(self.var_force_loss.get()),
            "force_huber_delta": float(self.var_force_huber_delta.get()),
            "w_dipole": float(self.var_wmu.get()),
            "w_polarizability": float(self.var_walpha.get()),
            "w_charges": float(self.var_w_charges.get()),
            "w_atomic_dipoles": float(self.var_w_atomic_dipoles.get()),
            "w_atomic_polarizability": float(self.var_w_atomic_polarizability.get()),
            "w_c6": float(self.var_w_c6.get()),
            "w_bec": float(self.var_w_bec.get()),
            "w_magnetic_moments": float(self.var_w_magnetic_moments.get()),
            "w_effective_field": float(self.var_w_effective_field.get()),
            "w_j": float(self.var_w_j.get()),
            "w_di": float(self.var_w_di.get()),
            "w_dmi": float(self.var_w_dmi.get()),
            "lr_scheduler": str(self.var_lr_scheduler.get()),
            "export_sevennet": bool(self.var_export_sevennet.get()),
            "save_epoch_artifacts": bool(self.var_save_epoch_artifacts.get()),
            "stream_hdf5": bool(self.var_stream_hdf5.get()),
            "cache_neighbor_graphs": bool(self.var_cache_neighbor_graphs.get()),
        }

    def _gui_train_kwargs_for_mode(self, mode: str) -> Dict[str, Any]:
        values = self._gui_common_train_kwargs()
        if mode == "base":
            for name in (
                "w_dipole", "w_polarizability", "w_charges", "w_atomic_dipoles",
                "w_atomic_polarizability", "w_c6", "w_bec", "w_magnetic_moments",
                "w_effective_field", "w_j", "w_di", "w_dmi",
            ):
                values[name] = 0.0
        return values

    def _validate_gui_data_paths(self, mode: str) -> None:
        if self._dataset_scan_pending:
            raise ValueError("Dataset capability scan is still running; wait a moment and retry.")
        if self._dataset_scan_error:
            raise ValueError(
                f"Dataset capability scan failed: {self._dataset_scan_error}. "
                "Correct the selected data path before training."
            )
        if self.var_dataset.get().strip():
            return
        if mode in ("base", "joint") and not self.var_static.get().strip():
            raise ValueError("Select a canonical HDF5 dataset or a legacy static extXYZ dataset.")
        if mode in ("response", "joint") and not self.var_response.get().strip():
            raise ValueError("Select a canonical HDF5 dataset or a legacy response extXYZ dataset.")

    def _start(self, mode):
        self._stop = False
        if mode == "response" and not self.var_base_ckpt.get().strip():
            answer = messagebox.askyesno(
                "No Base Checkpoint",
                "No base checkpoint selected.\n\n"
                "Run Base training first, then Response automatically?\n\n"
                "  Yes — chain: Base → Response (recommended)\n"
                "  No  — abort (select a checkpoint manually)",
            )
            if not answer:
                return
            # Offer the built-in two-step chain when no Base checkpoint is selected.
            self._run_chained()
            return
        try:
            self._validate_gui_data_paths(mode)
            cfg = TrainConfig(
                mode=mode,
                base_ckpt=self.var_base_ckpt.get(), out_ckpt=self.var_out_ckpt.get(),
                epochs=int(self.var_epochs.get()), lr=float(self.var_lr.get()),
                **self._gui_train_kwargs_for_mode(mode),
            )
        except (ValueError, RuntimeError) as e:
            return messagebox.showerror("Error", str(e))

        self._reset_live_dashboard(cfg.out_ckpt)
        self._set_training_running(True)

        def run():
            try:
                train_dual_layer(cfg, self.logger.log, lambda d: self._progress_q.put(d), lambda: self._stop)
                self._progress_q.put({"type": "run_complete", "stopped": bool(self._stop)})
            except Exception as e:
                self._progress_q.put({"type": "run_error", "message": str(e)})
                self.logger.log(f"Error: {e}\n{traceback.format_exc()}")
        threading.Thread(target=run, daemon=True).start()

    def _run_chained(self):
        """Run Base training first, then Response training in the same worker thread."""
        try:
            self._validate_gui_data_paths("joint")
            out_ckpt = self.var_out_ckpt.get()
            # Save the Base checkpoint separately so the final output stays reserved for Response.
            base_out = str(Path(out_ckpt).with_name(Path(out_ckpt).stem + "_base.pt"))
            cfg_base = TrainConfig(
                mode="base", out_ckpt=base_out,
                epochs=int(self.var_epochs.get()), lr=float(self.var_lr.get()),
                **self._gui_train_kwargs_for_mode("base"),
            )
            cfg_resp = TrainConfig(
                mode="response", base_ckpt=base_out, out_ckpt=out_ckpt,
                epochs=int(self.var_epochs.get()), lr=float(self.var_lr.get()),
                **self._gui_train_kwargs_for_mode("response"),
            )
        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Error", str(e))
            return

        self._reset_live_dashboard(base_out)
        self._set_training_running(True)

        def run():
            try:
                self.logger.log(f"[{_now()}] === Chain step 1/2: Training Base model → {base_out} ===")
                train_dual_layer(cfg_base, self.logger.log, lambda d: self._progress_q.put(d), lambda: self._stop)
                if self._stop:
                    self.logger.log(f"[{_now()}] Chain aborted after Base step.")
                    self._progress_q.put({"type": "run_complete", "stopped": True})
                    return
                self.logger.log(f"[{_now()}] === Chain step 2/2: Training Response model (base={base_out}) → {out_ckpt} ===")
                # Reflect the generated base checkpoint back into the GUI.
                self._progress_q.put({"type": "base_checkpoint", "path": base_out})
                train_dual_layer(cfg_resp, self.logger.log, lambda d: self._progress_q.put(d), lambda: self._stop)
                self.logger.log(f"[{_now()}] === Chain complete. Final model: {out_ckpt} ===")
                self._progress_q.put({"type": "run_complete", "stopped": bool(self._stop)})
            except Exception as e:
                self._progress_q.put({"type": "run_error", "message": str(e)})
                self.logger.log(f"Error: {e}\n{traceback.format_exc()}")
        threading.Thread(target=run, daemon=True).start()

    def _run_full_chain(self):
        """Run the full cascade: Base -> Response -> Joint fine-tuning stages."""
        self._stop = False
        try:
            lr        = float(self.var_lr.get())
            epochs    = int(self.var_epochs.get())
            n_stages  = max(1, int(self.var_joint_stages.get()))
            lr_g_sc   = float(self.var_lr_ground_scale.get())
            lr_r_sc   = float(self.var_lr_response_scale.get())
            warmup    = int(self.var_warmup_epochs.get())
            w_mu_f    = float(self.var_w_dipole_final.get())
            w_al_f    = float(self.var_w_alpha_final.get())
            out_ckpt  = self.var_out_ckpt.get()
            initial_checkpoint = self.var_base_ckpt.get().strip()
            if initial_checkpoint and not Path(initial_checkpoint).expanduser().is_file():
                raise FileNotFoundError(initial_checkpoint)

            self._validate_gui_data_paths("joint")
            stem = Path(out_ckpt).stem
            par  = Path(out_ckpt).parent
            base_out = str(par / f"{stem}_base.pt")
            resp_out = str(par / f"{stem}_resp.pt")

            cfg_base = TrainConfig(
                mode="base", base_ckpt=initial_checkpoint,
                out_ckpt=base_out, epochs=epochs, lr=lr,
                **self._gui_train_kwargs_for_mode("base"),
            )
            cfg_resp = TrainConfig(
                mode="response", out_ckpt=resp_out, base_ckpt=base_out,
                epochs=epochs, lr=lr, **self._gui_train_kwargs_for_mode("response"),
            )

            # Build the joint fine-tuning stages with geometrically decaying learning rates.
            joint_cfgs = []
            prev = resp_out
            for i in range(n_stages):
                j_lr     = lr * (0.2 ** (i + 1))           # lr/5, lr/25, ...
                j_epochs = max(2, epochs // (4 * (2 ** i))) # N/4, N/8, N/16, ...
                is_last  = (i == n_stages - 1)
                j_out    = out_ckpt if is_last else str(par / f"{stem}_jft{i+1}.pt")
                joint_common = self._gui_train_kwargs_for_mode("joint")
                joint_common["lr_scheduler"] = "cosine"
                joint_cfgs.append(TrainConfig(
                    mode="joint", base_ckpt=prev, out_ckpt=j_out,
                    epochs=j_epochs, lr=j_lr,
                    lr_ground=j_lr * lr_g_sc,
                    lr_response=j_lr * lr_r_sc,
                    warmup_freeze_epochs=warmup,
                    w_dipole_final=w_mu_f,
                    w_polarizability_final=w_al_f,
                    **joint_common,
                ))
                prev = j_out

        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Error", str(e))
            return

        total = 2 + n_stages
        self._reset_live_dashboard(base_out)
        self._set_training_running(True)

        def run():
            try:
                _log = self.logger.log
                _pq  = lambda d: self._progress_q.put(d)
                _sf  = lambda: self._stop

                _log(f"[{_now()}] === Full Chain: {total} stages ===")
                _log(
                    f"[{_now()}] Stage 1/{total}: Base "
                    + (
                        f"(pretrained={initial_checkpoint}) "
                        if initial_checkpoint else "(from scratch) "
                    )
                    + f"→ {base_out}"
                )
                train_dual_layer(cfg_base, _log, _pq, _sf)
                if self._stop:
                    self._progress_q.put({"type": "run_complete", "stopped": True})
                    return
                self._progress_q.put({"type": "base_checkpoint", "path": base_out})

                _log(f"[{_now()}] Stage 2/{total}: Response (base={base_out}) → {resp_out}")
                train_dual_layer(cfg_resp, _log, _pq, _sf)
                if self._stop:
                    self._progress_q.put({"type": "run_complete", "stopped": True})
                    return

                for i, j_cfg in enumerate(joint_cfgs):
                    _log(f"[{_now()}] Stage {3+i}/{total}: Joint FT{i+1}  "
                         f"lr={j_cfg.lr:.2e}  lr_ground={j_cfg.lr_ground:.2e}  "
                         f"lr_response={j_cfg.lr_response:.2e}  "
                         f"epochs={j_cfg.epochs}  warmup={j_cfg.warmup_freeze_epochs} → {j_cfg.out_ckpt}")
                    train_dual_layer(j_cfg, _log, _pq, _sf)
                    if self._stop:
                        self._progress_q.put({"type": "run_complete", "stopped": True})
                        return

                _log(f"[{_now()}] === Full Chain complete. Final: {out_ckpt} ===")
                self._progress_q.put({"type": "run_complete", "stopped": bool(self._stop)})
            except Exception as e:
                self._progress_q.put({"type": "run_error", "message": str(e)})
                self.logger.log(f"Error: {e}\n{traceback.format_exc()}")
        threading.Thread(target=run, daemon=True).start()

    # AutoSearch helpers.

    # Map flat AutoSearch parameter keys to GUI variable names.
    _PARAM_TO_VAR: Dict[str, str] = {
        "w_energy":            "var_we",
        "w_forces":            "var_wf",
        "force_loss":          "var_force_loss",
        "force_huber_delta":   "var_force_huber_delta",
        "w_dipole":            "var_wmu",
        "w_polarizability":    "var_walpha",
        "w_charges":           "var_w_charges",
        "w_atomic_dipoles":    "var_w_atomic_dipoles",
        "w_atomic_polarizability": "var_w_atomic_polarizability",
        "w_c6":                "var_w_c6",
        "w_bec":               "var_w_bec",
        "w_magnetic_moments":  "var_w_magnetic_moments",
        "w_effective_field":   "var_w_effective_field",
        "w_j":                 "var_w_j",
        "w_di":                "var_w_di",
        "w_dmi":               "var_w_dmi",
        "lr":                  "var_lr",
        "batch_size":          "var_bs",
        "r_max":               "var_rmax",
        "num_channels":        "var_channels",
        "num_interactions":    "var_interactions",
        "num_radial_basis":    "var_num_radial_basis",
        "field_scale":         "var_field_scale",
        "joint_stages":        "var_joint_stages",
        "lr_ground_scale":     "var_lr_ground_scale",
        "lr_response_scale":   "var_lr_response_scale",
        "warmup_epochs":       "var_warmup_epochs",
        "w_dipole_final":      "var_w_dipole_final",
        "w_alpha_final":       "var_w_alpha_final",
        "e3mu_use_parity":     "var_e3mu_use_parity",
        "e3mu_use_l3":         "var_e3mu_use_l3",
        "rbf_type":            "var_rbf_type",
        "enable_continuous_chem": "var_enable_continuous_chem",
        "chem_aug_prob":       "var_chem_aug_prob",
        "chem_aug_noise_std":  "var_chem_aug_noise_std",
        "chem_aug_mix_max":    "var_chem_aug_mix_max",
        "enable_qeq":          "var_enable_qeq",
        "enable_pme":          "var_enable_pme",
        "enable_deq":          "var_enable_deq",
        "enable_d4":           "var_enable_d4",
        "enable_spin":         "var_enable_spin",
        "enable_film":         "var_enable_film",
        "enable_dmi":          "var_enable_dmi",
        "qeq_smearing":        "var_qeq_smearing",
        "qeq_hardness_min":    "var_qeq_hardness_min",
        "qeq_pme_smearing":    "var_qeq_pme_smearing",
        "qeq_pme_lr_wavelength": "var_qeq_pme_lr_wavelength",
        "qeq_stability_floor": "var_qeq_stability_floor",
        "deq_damping":         "var_deq_damping",
        "deq_max_iter":        "var_deq_max_iter",
        "deq_tol":             "var_deq_tol",
        "deq_alpha_max":       "var_deq_alpha_max",
        "d4_functional":       "var_d4_functional",
        "spin_cutoff":         "var_spin_cutoff",
        "coupling_iterations": "var_coupling_iterations",
        "coupling_tol":        "var_coupling_tol",
    }

    def _reset_auto_tree(self, level: int) -> None:
        """Repopulate the auto-search treeview rows for the given level."""
        if self._auto_tree is None:
            return
        for row in self._auto_tree.get_children():
            self._auto_tree.delete(row)
        if level == 0:
            return
        excluded = self._auto_excluded_params() if level >= 4 else set()
        params = [
            name for name in AutoSearchEngine.LEVEL_PARAMS.get(level, [])
            if name not in excluded
        ]
        for p in params:
            # Seed the "best" column with the current GUI value.
            var_name = self._PARAM_TO_VAR.get(p)
            cur_val = ""
            if var_name:
                var = getattr(self, var_name, None)
                if var is not None:
                    try:
                        cur_val = _fmt_p(var.get())
                    except Exception:
                        cur_val = ""
            self._auto_tree.insert("", "end", values=(p, cur_val, "—", "—"))

    def _auto_excluded_params(self) -> set:
        architecture = {
            name: bool(getattr(self, f"var_{name}").get())
            for name in ARCHITECTURE_SWITCH_PARAMETERS
        }
        return architecture_locked_search_exclusions(
            architecture, self._dataset_capability
        )

    def _apply_auto_params(self, best_params: Dict[str, Any]) -> None:
        """Write the best AutoSearch parameters back into the GUI state."""
        for p, v in best_params.items():
            var_name = self._PARAM_TO_VAR.get(p)
            if not var_name:
                continue
            var = getattr(self, var_name, None)
            if var is None:
                continue
            try:
                var.set(v)
            except Exception:
                try:
                    var.set(str(v))
                except Exception:
                    pass

    def _store_auto_best(
        self, best_params: Dict[str, Any], best_score: float, level: int
    ) -> None:
        self._auto_best_params = dict(best_params)
        self._auto_best_score = float(best_score)
        self._auto_best_level = int(level)
        self._auto_best_text_var.set(
            f"Best result ready: normalized score {best_score:.6g} / "
            f"level {level} / {len(best_params)} values. Review the table, then Apply Best."
        )
        if self._auto_apply_button is not None:
            self._auto_apply_button.set_enabled(not self._training_running)

    def _apply_saved_auto_best(self) -> None:
        if not self._auto_best_params:
            messagebox.showinfo("AutoSearch", "No completed best-parameter result is available.")
            return
        self._apply_auto_params(self._auto_best_params)
        self._reset_auto_tree(self._auto_best_level)
        score_text = (
            f"{self._auto_best_score:.6g}"
            if self._auto_best_score is not None
            else "unknown"
        )
        self._auto_best_text_var.set(
            f"Applied {len(self._auto_best_params)} best values to the GUI "
            f"(normalized score {score_text})."
        )
        self._schedule_model_parameter_estimate()
        self.logger.log(
            f"[{_now()}] Applied AutoSearch best parameters to GUI "
            f"(score={score_text}, level={self._auto_best_level})."
        )

    def _run_auto_search(self) -> None:
        """Launch AutoSearch and retain the winning parameters for explicit apply."""
        self._stop = False
        level_str = self.var_auto_level.get()
        try:
            level = int(level_str[0])
        except (ValueError, IndexError):
            level = 0
        if level == 0:
            messagebox.showinfo("Auto Search", "Level 0 = Disabled.\nSelect level 1–4 to enable search.")
            return

        try:
            n_trials       = max(1, int(self.var_auto_trials.get()))
            trial_epochs   = max(1, int(self.var_auto_trial_epochs.get()))
            _pct           = float(self.var_auto_subset.get())
            if not (0.0 < _pct <= 100.0):
                raise ValueError(f"Sample% must be in (0, 100], got {_pct}")
            subset_frac    = _pct / 100.0
            if not self.var_dataset.get().strip() and not self.var_static.get().strip():
                raise ValueError("Canonical HDF5 or legacy static dataset is required for Auto Search.")
            search_mode = "joint" if self.var_dataset.get().strip() or self.var_response.get().strip() else "base"
            self._validate_gui_data_paths(search_mode)
            base_cfg = TrainConfig(
                mode          = search_mode,
                out_ckpt      = self.var_out_ckpt.get(),
                epochs        = trial_epochs,   # overridden by engine anyway
                lr            = float(self.var_lr.get()),
                **self._gui_train_kwargs_for_mode(search_mode),
            )
            base_cfg.export_sevennet = False
            base_cfg.save_epoch_artifacts = False
            auto_cfg = AutoSearchConfig(
                level=level,
                n_trials=n_trials,
                trial_epochs=trial_epochs,
                subset_fraction=subset_frac,
                excluded_params=tuple(sorted(self._auto_excluded_params())),
                search_space_overrides=dynamic_architecture_search_space(
                    base_cfg.model, self._dataset_capability
                ),
            )
        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Auto Search Error", str(e))
            return

        self._run_status_var.set("AutoSearch")
        self._epoch_status_var.set("Baseline")
        self._score_status_var.set("Score --")
        self._set_training_running(True)
        search_dataset_revision = self._dataset_selection_revision
        self._auto_best_params = {}
        self._auto_best_score = None
        self._auto_best_level = level
        self._auto_best_text_var.set("Search in progress; best values will appear when complete.")
        if self._auto_apply_button is not None:
            self._auto_apply_button.set_enabled(False, "Search is still running")

        # Prepare the temporary checkpoint directory and the result table.
        tmp_dir = str(Path(self.var_out_ckpt.get()).parent / "_auto_trials")
        try:
            Path(tmp_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self._set_training_running(False)
            self._run_status_var.set("Error")
            messagebox.showerror("Auto Search Error", f"Cannot create temp dir: {e}")
            return
        self._reset_auto_tree(level)

        def run() -> None:
            try:
                engine = AutoSearchEngine(base_cfg, auto_cfg, tmp_dir)
                best_params, best_loss = engine.run(
                    self.logger.log,
                    lambda d: self._progress_q.put(d),
                    lambda: self._stop,
                )
                if self._stop:
                    self._progress_q.put({"type": "run_complete", "stopped": True})
                    return
                self.logger.log(
                    f"[{_now()}] === Auto Search complete. "
                    f"Best normalized score={best_loss:.4f}  Level={level} ==="
                )
                applicable_params = {
                    name: best_params[name]
                    for name in engine._params
                    if name in best_params
                }
                self._progress_q.put({
                    "type": "auto_complete",
                    "params": applicable_params,
                    "score": float(best_loss),
                    "level": level,
                    "dataset_revision": search_dataset_revision,
                })
                self._progress_q.put({"type": "run_complete", "stopped": bool(self._stop)})
            except Exception as e:
                self._progress_q.put({"type": "run_error", "message": str(e)})
                self.logger.log(f"Auto Search Error: {e}\n{traceback.format_exc()}")

        threading.Thread(target=run, daemon=True).start()

    def _pump(self):
        self.logger.pump()
        while not self._progress_q.empty():
            d = self._progress_q.get()
            typ = d.get("type", "")
            if typ == "train":
                frac = float(d.get("overall_frac", 0.0))
                self.progress["value"] = 100.0 * max(0.0, min(1.0, frac))
                ep = int(d.get("epoch", 0))
                eps = int(d.get("epochs", 0))
                st = int(d.get("step", 0))
                sts = int(d.get("steps", 0))
                eta_s = float(d.get("eta_s", float("nan")))
                self._progress_text_var.set(f"Epoch {ep}/{eps}  Batch {st}/{sts}  {self._fmt_eta(eta_s)}")
            elif typ == "prep":
                frac = float(d.get("overall_frac", 0.0))
                self.progress["value"] = 100.0 * max(0.0, min(1.0, frac))
                task = str(d.get("task", ""))
                cur = d.get("current", None)
                tot = d.get("total", None)
                stage = str(d.get("stage", ""))
                msg = task or "Preparing"
                if cur is not None and tot is not None:
                    msg = f"{msg}: {int(cur)}/{int(tot)}"
                if stage:
                    msg = f"{msg}  {stage}"
                self._progress_text_var.set(msg)
            elif typ == "epoch":
                self.progress["value"] = (float(d.get("epoch", 0)) / float(max(1, d.get("epochs", 1)))) * 100.0
            elif typ == "metrics":
                self._consume_metric_event(d)
            elif typ == "artifacts":
                artifact_value = d.get("artifact_dir")
                if artifact_value:
                    self._live_artifact_dir = Path(str(artifact_value))
                self._render_live_dashboard()
            elif typ == "val":
                ep  = int(d.get("epoch", 0))
                eps = int(d.get("epochs", 0))
                st  = int(d.get("step", 0))
                sts = int(d.get("steps", 0))
                self._progress_text_var.set(f"Epoch {ep}/{eps}  Validating {st}/{sts}")
            elif typ == "auto_search":
                trial    = int(d.get("trial", 0))
                n        = int(d.get("n_trials", 1))
                b_loss   = float(d.get("best_loss", 0.0))
                t_loss   = float(d.get("trial_loss", 0.0))
                improved = bool(d.get("improved", False))
                self.progress["value"] = 100.0 * trial / max(1, n)
                self._progress_text_var.set(
                    f"Auto Search  Trial {trial}/{n}  "
                    f"Best score={b_loss:.4f}  Trial={t_loss:.4f}  "
                    f"{'✓ Improved' if improved else '—'}"
                )
                if self._auto_tree is not None:
                    best_p   = d.get("params", {})
                    trial_p  = d.get("trial_params", {})
                    for row_id in self._auto_tree.get_children():
                        pname = self._auto_tree.item(row_id, "values")[0]
                        bval  = _fmt_p(best_p.get(pname, ""))
                        tval  = _fmt_p(trial_p.get(pname, ""))
                        stat  = "✓" if (improved and pname in trial_p) else "—"
                        self._auto_tree.item(row_id, values=(pname, bval, tval, stat))
            elif typ == "auto_search_epoch":
                trial  = int(d.get("trial", 0))
                n      = int(d.get("n_trials", 1))
                epoch  = int(d.get("epoch", 0))
                epochs = int(d.get("epochs", 1))
                # Progress bar shows intra-trial epoch fraction
                self.progress["value"] = 100.0 * epoch / max(1, epochs)
                prefix = "Baseline" if trial == 0 else f"Trial {trial}/{n}"
                self._progress_text_var.set(
                    f"Auto Search  {prefix}  Epoch {epoch}/{epochs}"
                )
                self._epoch_status_var.set(f"{prefix}: {epoch} / {epochs}")
            elif typ == "run_complete":
                stopped = bool(d.get("stopped", False))
                self._set_training_running(False)
                self._run_status_var.set("Stopped" if stopped else "Complete")
                self._progress_text_var.set("Stopped by user" if stopped else "Training complete")
                if not stopped:
                    self.progress["value"] = 100.0
                self._render_live_dashboard()
            elif typ == "base_checkpoint":
                self.var_base_ckpt.set(str(d.get("path", "")))
            elif typ == "dataset_capability":
                if int(d.get("generation", -1)) == self._dataset_scan_generation:
                    self._apply_dataset_capability(
                        dict(d.get("capability", {"ready": False})),
                        str(d.get("error", "")),
                    )
            elif typ == "model_parameter_estimate":
                if int(d.get("generation", -1)) == self._model_estimate_generation:
                    self._apply_model_parameter_estimate(
                        dict(d.get("counts", {})), str(d.get("error", ""))
                    )
            elif typ == "auto_complete":
                if int(d.get("dataset_revision", -1)) == self._dataset_selection_revision:
                    self._store_auto_best(
                        dict(d.get("params", {})),
                        float(d.get("score", float("inf"))),
                        int(d.get("level", 0)),
                    )
                else:
                    self._auto_best_text_var.set(
                        "Search result discarded because the dataset selection changed."
                    )
            elif typ == "run_error":
                self._set_training_running(False)
                self._run_status_var.set("Error")
                self._progress_text_var.set(str(d.get("message", "Training failed")))
        self.after(100, self._pump)


# =========================================================================
# SECTION: Modern PyQt6 Research Studio
# Parameter metadata and the complete Qt interface are intentionally kept in
# this single executable module so GUI and training configuration cannot drift.
# =========================================================================


@dataclass(frozen=True)
class ParameterInfo:
    title: str
    purpose: str
    principle: str
    reference: str
    dependency: str = "Always available when the selected dataset supports it."


def _p(
    title: str,
    purpose: str,
    principle: str,
    reference: str,
    dependency: str = "Always available when the selected dataset supports it.",
) -> ParameterInfo:
    return ParameterInfo(title, purpose, principle, reference, dependency)


PARAMETER_INFO: Dict[str, ParameterInfo] = {
    "dataset": _p(
        "Canonical HDF5",
        "Loads one mixed-label dataset with explicit masks, units, groups, and splits.",
        "A canonical file lets L1/L2/L3 targets coexist without treating missing labels as zeros.",
        "Prefer the canonical HDF5 path for mixed-granularity training.",
    ),
    "static_data": _p(
        "Legacy static dataset",
        "Supplies field-free structures for energy and force learning.",
        "These frames primarily supervise the short-range potential-energy surface in Layer 1.",
        "Use extXYZ or extXYZ.gz; leave empty when Canonical HDF5 is selected.",
    ),
    "response_data": _p(
        "Legacy response dataset",
        "Supplies electric-field response structures and tensor targets.",
        "Response energies use a separate role because their energy zero may differ from static data.",
        "Use extXYZ or extXYZ.gz paired with a compatible static dataset.",
    ),
    "base_ckpt": _p(
        "Pretrained / base checkpoint",
        "Warm-starts Base, Response, Joint, and the first stage of Full Chain.",
        "Compatible Layer-1 weights are transferred into the selected architecture; Response mode then freezes Layer 1, while other modes fine-tune it with a fresh optimizer.",
        "Required for Response mode; optional for Base, Joint, and Full Chain. Match channels and parity for the largest transfer.",
    ),
    "out_ckpt": _p(
        "Output checkpoint",
        "Stores the final safe model checkpoint and determines the artifact directory.",
        "Per-epoch diagnostics are written beside it under train/<checkpoint stem>/.",
        "Use a writable .pt path with a distinct name for each experiment.",
    ),
    "epochs": _p(
        "Epochs",
        "Controls full passes over the training split.",
        "More epochs reduce optimization error but do not correct model or dataset bias.",
        "Smoke test: 1-5; tuning: 20-100; converged studies: monitor validation curves.",
    ),
    "batch_size": _p(
        "Batch size",
        "Sets the maximum number of structures differentiated in one optimizer step.",
        "CPU/CUDA use this limit directly. MPS additionally caps graph edges per step because force and BEC derivatives can exhaust unified memory.",
        "Typical 2-16. On MPS, dense structures can reach the edge safety budget first, so the realized mean can be lower.",
    ),
    "lr": _p(
        "Learning rate",
        "Controls the optimizer step size.",
        "Too large a step destabilizes coupled charge/polarization solvers; too small slows convergence.",
        "Usually 1e-4 to 5e-3; start near 1e-3 for a 64-channel model.",
    ),
    "lr_scheduler": _p(
        "Learning-rate schedule",
        "Chooses a constant or cosine-decayed optimizer rate.",
        "Cosine decay anneals parameter motion as the validation basin is approached.",
        "flat for short baselines; cosine for longer or joint fine-tuning runs.",
    ),
    "device": _p(
        "Compute device",
        "Selects CPU, Apple MPS, CUDA, or automatic detection.",
        "The backend preserves differentiability when QEq/D4 require CPU sub-operations on MPS.",
        "auto is recommended; use CPU for numerical diagnosis.",
    ),
    "cpu_threads": _p(
        "CPU compute threads",
        "Controls PyTorch intra-op parallelism for tensor kernels and CPU training.",
        "CPU auto uses every CPU visible to the process; MPS/CUDA auto reserves a bounded helper pool to avoid driver contention.",
        "Use auto first. Choose 1 for reproducible performance diagnosis or a specific positive count for shared machines.",
    ),
    "dtype": _p(
        "Floating-point dtype",
        "Sets the model's primary arithmetic precision.",
        "float64 improves conditioning tests; Apple MPS supports float32 only.",
        "float32 for MPS/CUDA training; float64 for small CPU validation studies.",
    ),
    "r_max": _p(
        "Local cutoff r_max",
        "Defines graph edges and the Layer-1 receptive field per interaction.",
        "A smooth cosine envelope forces messages to zero at the cutoff, preserving continuous forces.",
        "Molecules: 4-6 Angstrom; periodic/ionic systems: 5-8 Angstrom.",
    ),
    "num_channels": _p(
        "Equivariant channels",
        "Controls feature width in scalar, vector, axial, and tensor irreducible channels.",
        "Wider channels increase the multiplicity of learned O(3) representations and parameter count.",
        "32-96 for development; 64-128 for multi-physics production models.",
    ),
    "num_interactions": _p(
        "Interaction blocks",
        "Controls message-passing depth and effective receptive field.",
        "Each block couples radial filters to equivariant angular channels.",
        "Usually 2-4; one block is suitable only for smoke tests.",
    ),
    "num_radial_basis": _p(
        "Radial basis count",
        "Sets radial resolution between zero and r_max.",
        "Gaussian or Bessel bases expand pair distance before tensor-product message passing.",
        "6-16; increase for a large cutoff or diverse bond-length distribution.",
    ),
    "field_scale": _p(
        "External-field scale",
        "Rescales electric fields before response-energy assembly.",
        "The Hamiltonian uses E_response = -mu.E - 1/2 E^T alpha E.",
        "Normally 1.0 when dataset field units are eV/(e Angstrom); 0.5-2 only for calibration.",
    ),
    "val_fraction": _p(
        "Validation fraction",
        "Reserves complete structure groups for validation.",
        "Group-level splitting prevents conformer or magnetic-family leakage.",
        "Usually 0.05-0.20; use at least 10-20 validation groups.",
    ),
    "seed": _p(
        "Random seed",
        "Controls splits, initialization, shuffling, and AutoSearch sampling.",
        "Fixed seeds make small-data comparisons reproducible but do not replace multi-seed evaluation.",
        "Any non-negative integer; report several seeds for final accuracy claims.",
    ),
    "export_sevennet": _p(
        "SevenNet export",
        "Exports the compatible local ground branch after training.",
        "Only the local equivariant potential is serialized to the compatibility format.",
        "Enable for deployment; disable during quick experiments to reduce finalization time.",
    ),
    "save_epoch_artifacts": _p(
        "Live plots and artifacts",
        "Writes checkpoints, parity plots, histories, and solver diagnostics each epoch.",
        "Validation observables are streamed to the GUI and saved as machine-readable JSON.",
        "Enable for normal runs; disable only for I/O-sensitive searches.",
    ),
    "stream_hdf5": _p(
        "Stream canonical HDF5",
        "Keeps structures, labels, and graph tensors on disk until their batch is requested.",
        "A compact split/mask index remains in RAM; only the current PyG batch is transferred to the accelerator.",
        "Recommended on for canonical HDF5. Legacy extXYZ is still materialized before training.",
        "Available for canonical HDF5 input.",
    ),
    "cache_neighbor_graphs": _p(
        "Disk topology cache",
        "Stores exact neighbor indices and periodic shifts on disk for reuse across epochs and runs.",
        "The cache uses the same deterministic cutoff and neighbor implementation as uncached graph construction.",
        "Recommended on. Disable only when disk space is constrained or geometry changes every epoch.",
        "Used with canonical HDF5 streaming.",
    ),
    "joint_stages": _p(
        "Joint fine-tuning stages",
        "Controls progressively lower-rate L1/L2/L3 joint refinement stages.",
        "A staged schedule limits catastrophic drift of a pretrained ground-state potential.",
        "1-4; two stages are a balanced default.",
    ),
    "warmup_epochs": _p(
        "Warmup freeze epochs",
        "Keeps Layer 1 frozen at the beginning of each joint stage.",
        "Response and domain heads first adapt before gradients alter the short-range PES.",
        "0-10; start with 2-3 for pretrained Layer 1.",
    ),
    "lr_ground_scale": _p(
        "Layer-1 LR scale",
        "Multiplies the joint-stage learning rate for the ground branch.",
        "A smaller rate protects conservative energy/force behavior while other layers adapt.",
        "0.01-0.20; default 0.05.",
    ),
    "lr_response_scale": _p(
        "Response LR scale",
        "Multiplies the joint-stage learning rate for electric and spin response branches.",
        "Response features generally need more adaptation than a pretrained Layer 1.",
        "0.05-0.50; default 0.20.",
    ),
    "w_dipole_final": _p(
        "Final dipole weight",
        "Sets the endpoint of a linear dipole-loss ramp during joint fine-tuning.",
        "Gradual activation avoids an abrupt response gradient on the ground branch.",
        "0 disables the ramp; otherwise usually 1e-4 to 0.1.",
    ),
    "w_alpha_final": _p(
        "Final polarizability weight",
        "Sets the endpoint of a linear polarizability-loss ramp.",
        "The tensor response is introduced gradually to stabilize higher-order derivatives.",
        "0 disables the ramp; otherwise usually 1e-4 to 0.1.",
    ),
    "w_energy": _p(
        "Energy loss weight",
        "Weights total-energy supervision.",
        "Energy is normalized per atom inside the loss to avoid large systems dominating.",
        "0.1-10; start at 1.",
    ),
    "w_forces": _p(
        "Force loss weight",
        "Weights conservative atomic-force supervision.",
        "Forces are -dE/dR and provide three local derivatives per atom.",
        "1-100; start near 10 when energy is weighted 1.",
    ),
    "force_loss": _p(
        "Force loss",
        "Chooses squared error or an outlier-robust Huber objective for force training.",
        "Scaled Huber matches MSE near zero but caps the gradient from extreme-force structures.",
        "Use MSE for clean homogeneous data; use Huber after auditing force outliers.",
    ),
    "force_huber_delta": _p(
        "Huber force delta",
        "Sets the force-error threshold where the robust loss becomes linear.",
        "Errors below delta retain the quadratic MSE curvature; larger errors have bounded slope.",
        "Usually 0.5-2.0 eV/Angstrom; start at 1.0 after inspecting the force distribution.",
        "Available only when Force loss is set to huber.",
    ),
    "w_dipole": _p(
        "Dipole loss weight",
        "Weights molecular or cell dipole-vector supervision.",
        "Dipoles combine charge displacement, permanent atomic dipoles, and induced response.",
        "1e-3-1; normalize against a dipole baseline before final tuning.",
    ),
    "w_polarizability": _p(
        "Polarizability loss weight",
        "Weights the symmetric molecular polarizability tensor.",
        "The model decomposes alpha into positive isotropic and L=2 anisotropic components.",
        "1e-3-1 for Angstrom^3 targets.",
    ),
    "w_charges": _p(
        "Charge loss weight",
        "Weights local partial charges under an exact total-charge constraint.",
        "QEq minimizes electronegativity, hardness, and Coulomb energy in the neutral subspace.",
        "1e-3-10; meaningful when QEq/PME is enabled.",
        "Requires QEq or PME and charge labels.",
    ),
    "w_atomic_dipoles": _p(
        "Atomic-dipole loss weight",
        "Weights per-atom polar-vector response.",
        "Equivariant vector channels make atomic dipoles rotate with the geometry.",
        "1e-3-1.",
        "Requires an active electric domain and atomic-dipole labels.",
    ),
    "w_atomic_polarizability": _p(
        "Atomic-polarizability loss weight",
        "Weights per-atom rank-2 response tensors.",
        "Isotropic plus symmetric-traceless L=2 terms preserve rotational covariance.",
        "1e-3-1.",
        "Requires an electric/DEQ domain and atomic-polarizability labels.",
    ),
    "w_c6": _p(
        "C6 loss weight",
        "Weights atomwise dispersion coefficients.",
        "D4 obtains environment- and charge-dependent dispersion coefficients.",
        "1e-6-0.1 because C6 magnitudes are numerically larger than energies.",
        "Requires molecular D4 and C6 labels.",
    ),
    "w_bec": _p(
        "Born effective charge weight",
        "Weights d(mu_alpha)/d(R_i,beta).",
        "BEC is a mixed field-displacement derivative evaluated by autograd.",
        "1e-3-10; begin near 0.1 after dipole learning is stable.",
        "Requires BEC labels; its second derivatives increase memory cost.",
    ),
    "w_magnetic_moments": _p(
        "Magnetic-moment loss weight",
        "Weights atomwise magnetic-moment vectors.",
        "A positive learned magnitude multiplies the time-reversal-odd spin direction.",
        "1e-3-10.",
        "Requires Spin and magnetic-moment labels.",
    ),
    "w_effective_field": _p(
        "Effective spin-field weight",
        "Weights -dE_spin/dS.",
        "The target probes the local derivative of exchange, anisotropy, and DMI energy.",
        "1e-3-10 after checking target units.",
        "Requires Spin and effective-field labels.",
    ),
    "w_j": _p(
        "Exchange-J loss weight",
        "Weights effective Heisenberg exchange.",
        "Pair energy contains -J_ij S_i dot S_j and is even under global spin reversal.",
        "1e-3-10 for eV-valued mapped targets.",
        "Requires Spin and J labels.",
    ),
    "w_di": _p(
        "Single-ion anisotropy weight",
        "Weights traceless per-atom or effective Di tensors.",
        "The term S_i^T Di S_i is time-reversal even and captures SOC anisotropy.",
        "1e-3-10.",
        "Requires Spin and Di/Di_effective labels.",
    ),
    "w_dmi": _p(
        "DMI loss weight",
        "Weights the axial Dzyaloshinskii-Moriya interaction.",
        "D_ij dot (S_i cross S_j) couples an axial geometric feature to spin chirality.",
        "1e-3-10.",
        "Requires both Spin and DMI plus DMI/SOC labels.",
    ),
    "e3mu_use_parity": _p(
        "O(3) parity channels",
        "Separates polar and axial representations under reflection.",
        "O(3) parity is required to distinguish vectors from pseudovectors such as spin and DMI.",
        "Recommended on; mandatory for L=3, FiLM, or Spin+DMI.",
    ),
    "e3mu_use_l3": _p(
        "L=3 tensor channel",
        "Adds seven-component symmetric-traceless rank-3 geometric features.",
        "Higher angular order resolves complex local environments at additional memory cost.",
        "Off for baselines; enable when validation shows L=2 angular capacity is insufficient.",
        "Requires O(3) parity.",
    ),
    "rbf_type": _p(
        "Radial basis family",
        "Chooses fixed Gaussian, trainable Gaussian, or spherical Bessel distance features.",
        "Radial expansion is multiplied by a smooth cutoff before equivariant message passing.",
        "gaussian is robust; bessel is orthogonal; trainable_gaussian adapts to bond statistics.",
    ),
    "enable_continuous_chem": _p(
        "Continuous chemistry",
        "Embeds periodic-table descriptors instead of isolated one-hot element identities.",
        "Electronegativity, radius, ionization, valence, and mass descriptors support chemical transfer.",
        "Enable for multi-element transfer studies; keep off for a single-element dataset.",
        "Requires at least two elements.",
    ),
    "enable_qeq": _p(
        "Differentiable QEq",
        "Solves charge equilibration with an exact graph-wise total-charge constraint.",
        "The neutral-space Hessian minimizes chi.q + 1/2 q^T H q while preserving conservative forces.",
        "Enable for charge-aware molecular or domain electrostatics.",
        "Requires electric-response labels.",
    ),
    "enable_pme": _p(
        "PME / Ewald electrostatics",
        "Adds periodic long-range Coulomb interactions to QEq.",
        "Ewald splitting combines real-space and reciprocal-space electrostatic sums.",
        "Enable only for periodic electric-response datasets.",
        "Requires QEq, periodic cells, and torch-pme.",
    ),
    "enable_deq": _p(
        "Self-consistent polarization",
        "Solves the induced-dipole equilibrium with a differentiable linear solve.",
        "The Thole-damped response Hessian receives only the stability shift needed to prevent a polarization catastrophe.",
        "Enable for dipole/polarizability/BEC response studies.",
        "Requires electric polarization labels.",
    ),
    "enable_d4": _p(
        "D4 dispersion",
        "Adds charge-dependent molecular dispersion energy and C6 coefficients.",
        "The differentiable tad-dftd4 layer contributes to total energy and conservative forces.",
        "Enable for non-periodic molecular datasets with dispersion signal.",
        "Current implementation excludes periodic images.",
    ),
    "enable_spin": _p(
        "Spin Hamiltonian",
        "Adds Heisenberg J, traceless single-ion Di, magnetic moments, and optional DMI.",
        "The energy remains invariant under simultaneous S -> -S time reversal.",
        "Enable only for spin-resolved structures.",
        "Requires spin vectors and magnetic or spin-resolved energy labels.",
    ),
    "enable_film": _p(
        "FiLM cross-granularity feedback",
        "Feeds charge, potential, and spin-domain state back into Layer 1.",
        "Feature-wise affine modulation iterates local and domain representations toward consistency.",
        "Start with two coupling iterations after uncoupled layers are stable.",
        "Requires O(3) parity and an electric or spin domain.",
    ),
    "enable_dmi": _p(
        "DMI interaction",
        "Activates the antisymmetric spin-exchange term.",
        "An axial D vector contracts with S_i cross S_j, requiring correct O(3) parity and SOC signal.",
        "Enable only when chiral/SOC configurations identify DMI.",
        "Requires Spin, O(3), and DMI or SOC labels.",
    ),
    "chem_max_z": _p(
        "Maximum atomic number",
        "Sizes the continuous periodic-table descriptor lookup.",
        "Every selected element Z must be represented before descriptor encoding.",
        "At least max(dataset Z), at most 118; default 96.",
        "Used only by Continuous chemistry.",
    ),
    "chem_aug_prob": _p(
        "Alchemical augmentation probability",
        "Chooses the fraction of atoms whose chemical descriptors are perturbed during training.",
        "Small stochastic perturbations regularize interpolation in continuous chemical space.",
        "0-0.30; start at 0.05 after an unaugmented baseline.",
        "Used only by Continuous chemistry.",
    ),
    "chem_aug_noise_std": _p(
        "Chemical descriptor noise",
        "Sets Gaussian noise on standardized periodic-table descriptors.",
        "Noise regularizes descriptor sensitivity without changing atomic identities in the graph.",
        "0-0.10; start near 0.01.",
        "Used only by Continuous chemistry.",
    ),
    "chem_aug_mix_max": _p(
        "Alchemical mixing limit",
        "Caps interpolation toward a randomly sampled element descriptor.",
        "Descriptor mixing approximates smooth alchemical paths while preserving geometric inputs.",
        "0-0.30; stay below 0.15 for narrow chemical domains.",
        "Used only by Continuous chemistry.",
    ),
    "qeq_smearing": _p(
        "QEq Coulomb smearing",
        "Regularizes the short-range 1/r charge kernel.",
        "The softened kernel 1/sqrt(r^2+a^2) avoids singular charge curvature at small separation.",
        "0.15-0.8 Angstrom, adjusted with cutoff and bond lengths.",
        "Used by QEq/PME and DEQ field damping.",
    ),
    "qeq_hardness_min": _p(
        "Minimum atomic hardness",
        "Adds a positive lower bound to learned QEq diagonal hardness.",
        "Positive hardness penalizes excessive charge transfer and improves Hessian conditioning.",
        "0.05-2.0 eV; default 0.25.",
        "Used only by QEq/PME.",
    ),
    "qeq_pme_smearing": _p(
        "PME Ewald smearing",
        "Controls the Ewald real/reciprocal decomposition width.",
        "The total electrostatic energy is invariant in the converged limit, while computational balance changes.",
        "0.5-2.0 Angstrom; start at 1.0.",
        "Used only by PME.",
    ),
    "qeq_pme_lr_wavelength": _p(
        "PME reciprocal wavelength",
        "Controls long-range mesh or reciprocal-space resolution.",
        "Shorter wavelength increases reciprocal resolution and cost.",
        "0.4-1.5 Angstrom, adjusted with r_max and cell size.",
        "Used only by PME.",
    ),
    "qeq_stability_floor": _p(
        "QEq stability floor",
        "Enforces minimum neutral-space curvature before the constrained solve.",
        "A spectral shift makes the reduced charge Hessian positive definite without breaking charge conservation.",
        "0.01-1.0 eV and normally below the hardness scale.",
        "Used only by QEq/PME.",
    ),
    "deq_max_iter": _p(
        "DEQ legacy iteration cap",
        "Retains compatibility with checkpoints from the former fixed-point solver.",
        "The stable direct equilibrium solver no longer truncates an iterative path.",
        "Not used by the current direct solver.",
        "Used only by DEQ polarization.",
    ),
    "deq_tol": _p(
        "DEQ residual reference",
        "Defines the expected linear-equilibrium residual for diagnostics.",
        "The exact solve reports the residual without truncating the response path.",
        "1e-7-1e-4; use about 1e-5 for float32.",
        "Used only by DEQ polarization.",
    ),
    "deq_damping": _p(
        "DEQ Thole damping",
        "Damps short-range charge-dipole and dipole-dipole interactions.",
        "Polarizability-scaled Thole factors prevent the induced-dipole polarization catastrophe.",
        "0.2-0.8 dimensionless; lower values apply stronger short-range damping.",
        "Used only by DEQ polarization.",
    ),
    "deq_alpha_max": _p(
        "DEQ polarizability cap",
        "Bounds atomic polarizability entering the induced-dipole solve.",
        "The cap prevents a polarization catastrophe when mutual dipole gain exceeds unity.",
        "10-300 Angstrom^3; default 100, but use a chemistry-informed upper bound.",
        "Used only by DEQ polarization.",
    ),
    "d4_functional": _p(
        "D4 reference functional",
        "Selects damping parameters calibrated for the parent density functional.",
        "D4 short-range damping prevents double counting correlation already present in the functional.",
        "Match the dataset method, commonly pbe, pbe0, or b3lyp.",
        "Used only by D4.",
    ),
    "spin_cutoff": _p(
        "Spin-pair cutoff",
        "Limits pairs entering J and DMI interactions.",
        "Magnetic exchange is evaluated only on graph edges within this radius.",
        "4-8 Angstrom and no larger than r_max.",
        "Used only by Spin.",
    ),
    "coupling_iterations": _p(
        "FiLM coupling iterations",
        "Caps alternating local/domain feedback updates.",
        "Each outer step recomputes local features conditioned on charge, potential, and spin state.",
        "1-4; default 2.",
        "Used only by FiLM.",
    ),
    "coupling_tol": _p(
        "FiLM coupling tolerance",
        "Stops outer feedback when mean charge change is small.",
        "A self-consistent domain state avoids unnecessary repeated local passes.",
        "1e-7-1e-3; default 1e-5.",
        "Used only by FiLM.",
    ),
    "auto_level": _p(
        "AutoSearch level",
        "Chooses cumulative loss, backbone, cascade, and active-physics search dimensions.",
        "The selected architecture is locked; only parameters meaningful inside it are proposed.",
        "1 loss weights; 2 +backbone; 3 +cascade; 4 +active physics solvers.",
    ),
    "auto_trials": _p(
        "AutoSearch trials",
        "Sets candidate evaluations after the current-configuration baseline.",
        "Search transitions from random exploration to Gaussian-process-guided proposals.",
        "5-20 for development; 30-100 for a serious search.",
    ),
    "auto_trial_epochs": _p(
        "Epochs per search trial",
        "Sets the short optimization budget used to rank candidates.",
        "Too few epochs favor fast starters; too many reduce the number of explored configurations.",
        "5-20, then retrain the winner to convergence.",
    ),
    "auto_subset": _p(
        "Search sample percent",
        "Subsamples complete structure groups for each trial.",
        "Group-aware sampling preserves leakage protection while reducing search cost.",
        "1-20%, but retain at least about 100 diverse structures when possible.",
    ),
    "live_plot": _p(
        "Live analysis view",
        "Chooses parity images, objectives, multi-task MAE, solver residuals, or memory telemetry.",
        "Each view consumes structured validation events emitted after every epoch.",
        "Use Memory to verify stable RSS and MPS cache behavior across epochs.",
    ),
}


GUI_DEFAULTS = {
    "dataset": "",
    "static_data": "",
    "response_data": "",
    "base_ckpt": "",
    "out_ckpt": "model.pt",
    "device": "auto",
    "cpu_threads": "auto",
    "dtype": "float32",
    "epochs": "50",
    "batch_size": "4",
    "lr": "1e-3",
    "lr_scheduler": "flat",
    "r_max": "5.0",
    "num_channels": "64",
    "num_interactions": "2",
    "num_radial_basis": "8",
    "field_scale": "1.0",
    "val_fraction": "0.1",
    "seed": "0",
    "export_sevennet": True,
    "save_epoch_artifacts": True,
    "stream_hdf5": True,
    "cache_neighbor_graphs": True,
    "joint_stages": "2",
    "warmup_epochs": "3",
    "lr_ground_scale": "0.05",
    "lr_response_scale": "0.20",
    "w_dipole_final": "0.0",
    "w_alpha_final": "0.0",
    "w_energy": "1.0",
    "w_forces": "10.0",
    "force_loss": "mse",
    "force_huber_delta": "1.0",
    "w_dipole": "0.0",
    "w_polarizability": "0.0",
    "w_charges": "0.0",
    "w_atomic_dipoles": "0.0",
    "w_atomic_polarizability": "0.0",
    "w_c6": "0.0",
    "w_bec": "0.0",
    "w_magnetic_moments": "0.0",
    "w_effective_field": "0.0",
    "w_j": "0.0",
    "w_di": "0.0",
    "w_dmi": "0.0",
    "e3mu_use_parity": True,
    "e3mu_use_l3": False,
    "rbf_type": "gaussian",
    "enable_continuous_chem": False,
    "chem_max_z": "96",
    "chem_aug_prob": "0.0",
    "chem_aug_noise_std": "0.0",
    "chem_aug_mix_max": "0.0",
    "enable_qeq": False,
    "enable_pme": False,
    "enable_deq": False,
    "enable_d4": False,
    "enable_spin": False,
    "enable_film": False,
    "enable_dmi": False,
    "qeq_smearing": "0.35",
    "qeq_hardness_min": "0.25",
    "qeq_pme_smearing": "1.0",
    "qeq_pme_lr_wavelength": "0.8",
    "qeq_stability_floor": "0.1",
    "deq_max_iter": "50",
    "deq_tol": "1e-6",
    "deq_damping": "0.5",
    "deq_alpha_max": "100.0",
    "d4_functional": "pbe",
    "spin_cutoff": "5.0",
    "coupling_iterations": "2",
    "coupling_tol": "1e-5",
    "auto_level": "0: Disabled",
    "auto_trials": "20",
    "auto_trial_epochs": "10",
    "auto_subset": "1",
    "live_plot": "Regression",
}


@dataclass(frozen=True)
class GUINumericRule:
    """Strict action-time rule paired with a permissive live Qt editor."""

    kind: str
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    minimum_inclusive: bool = True
    maximum_inclusive: bool = True


def _int_rule(
    minimum: Optional[int] = None, maximum: Optional[int] = None
) -> GUINumericRule:
    return GUINumericRule("int", minimum, maximum)


def _float_rule(
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
    *,
    minimum_inclusive: bool = True,
    maximum_inclusive: bool = True,
) -> GUINumericRule:
    return GUINumericRule(
        "float", minimum, maximum, minimum_inclusive, maximum_inclusive
    )


# QLineEdit validators prevent accidental suffixes such as ``48s``. These
# rules are also checked independently before an action, because setText(),
# imported JSON, and old defaults can bypass a Qt validator.
GUI_NUMERIC_RULES: Dict[str, GUINumericRule] = {
    "epochs": _int_rule(1),
    "batch_size": _int_rule(1),
    "lr": _float_rule(0.0, minimum_inclusive=False),
    "force_huber_delta": _float_rule(0.0, minimum_inclusive=False),
    "r_max": _float_rule(0.0, minimum_inclusive=False),
    "num_channels": _int_rule(1),
    "num_interactions": _int_rule(1),
    "num_radial_basis": _int_rule(1),
    "field_scale": _float_rule(0.0),
    "val_fraction": _float_rule(
        0.0, 1.0, minimum_inclusive=False, maximum_inclusive=False
    ),
    "seed": _int_rule(0),
    "joint_stages": _int_rule(1),
    "warmup_epochs": _int_rule(0),
    "lr_ground_scale": _float_rule(0.0),
    "lr_response_scale": _float_rule(0.0),
    "w_dipole_final": _float_rule(0.0),
    "w_alpha_final": _float_rule(0.0),
    "w_energy": _float_rule(0.0),
    "w_forces": _float_rule(0.0),
    "w_dipole": _float_rule(0.0),
    "w_polarizability": _float_rule(0.0),
    "w_charges": _float_rule(0.0),
    "w_atomic_dipoles": _float_rule(0.0),
    "w_atomic_polarizability": _float_rule(0.0),
    "w_c6": _float_rule(0.0),
    "w_bec": _float_rule(0.0),
    "w_magnetic_moments": _float_rule(0.0),
    "w_effective_field": _float_rule(0.0),
    "w_j": _float_rule(0.0),
    "w_di": _float_rule(0.0),
    "w_dmi": _float_rule(0.0),
    "chem_max_z": _int_rule(1, 118),
    "chem_aug_prob": _float_rule(0.0, 1.0),
    "chem_aug_noise_std": _float_rule(0.0),
    "chem_aug_mix_max": _float_rule(0.0, 1.0),
    "qeq_smearing": _float_rule(0.0, minimum_inclusive=False),
    "qeq_hardness_min": _float_rule(0.0, minimum_inclusive=False),
    "qeq_pme_smearing": _float_rule(0.0, minimum_inclusive=False),
    "qeq_pme_lr_wavelength": _float_rule(0.0, minimum_inclusive=False),
    "qeq_stability_floor": _float_rule(0.0),
    "deq_max_iter": _int_rule(1),
    "deq_tol": _float_rule(0.0, minimum_inclusive=False),
    "deq_damping": _float_rule(0.0, minimum_inclusive=False),
    "deq_alpha_max": _float_rule(0.0, minimum_inclusive=False),
    "spin_cutoff": _float_rule(0.0, minimum_inclusive=False),
    "coupling_iterations": _int_rule(1),
    "coupling_tol": _float_rule(0.0, minimum_inclusive=False),
    "auto_trials": _int_rule(1),
    "auto_trial_epochs": _int_rule(1),
    "auto_subset": _float_rule(
        0.0, 100.0, minimum_inclusive=False, maximum_inclusive=True
    ),
}


def _parse_gui_numeric_value(
    name: str, value: Any, rule: Optional[GUINumericRule] = None
) -> Any:
    """Parse one GUI number exactly and reject empty, malformed, or non-finite input."""
    selected = rule or GUI_NUMERIC_RULES[name]
    text = str(value).strip()
    if not text:
        raise ValueError("a value is required")
    try:
        parsed: Any = int(text, 10) if selected.kind == "int" else float(text)
    except (TypeError, ValueError, OverflowError) as exc:
        expected = "an integer" if selected.kind == "int" else "a number"
        raise ValueError(f"expected {expected}, got {text!r}") from exc
    if isinstance(parsed, float) and not math.isfinite(parsed):
        raise ValueError("NaN and infinity are not allowed")
    if selected.minimum is not None:
        below = parsed < selected.minimum
        on_excluded_minimum = (
            not selected.minimum_inclusive and parsed == selected.minimum
        )
        if below or on_excluded_minimum:
            relation = ">=" if selected.minimum_inclusive else ">"
            raise ValueError(f"must be {relation} {selected.minimum:g}")
    if selected.maximum is not None:
        above = parsed > selected.maximum
        on_excluded_maximum = (
            not selected.maximum_inclusive and parsed == selected.maximum
        )
        if above or on_excluded_maximum:
            relation = "<=" if selected.maximum_inclusive else "<"
            raise ValueError(f"must be {relation} {selected.maximum:g}")
    return parsed


LEGACY_TK_VARIABLES = {
    "dataset": "var_dataset",
    "static_data": "var_static",
    "response_data": "var_response",
    "base_ckpt": "var_base_ckpt",
    "out_ckpt": "var_out_ckpt",
    "device": "var_device",
    "cpu_threads": "var_cpu_threads",
    "dtype": "var_dtype",
    "epochs": "var_epochs",
    "batch_size": "var_bs",
    "lr": "var_lr",
    "lr_scheduler": "var_lr_scheduler",
    "r_max": "var_rmax",
    "num_channels": "var_channels",
    "num_interactions": "var_interactions",
    "num_radial_basis": "var_num_radial_basis",
    "field_scale": "var_field_scale",
    "val_fraction": "var_val_fraction",
    "seed": "var_seed",
    "export_sevennet": "var_export_sevennet",
    "save_epoch_artifacts": "var_save_epoch_artifacts",
    "stream_hdf5": "var_stream_hdf5",
    "cache_neighbor_graphs": "var_cache_neighbor_graphs",
    "joint_stages": "var_joint_stages",
    "warmup_epochs": "var_warmup_epochs",
    "lr_ground_scale": "var_lr_ground_scale",
    "lr_response_scale": "var_lr_response_scale",
    "w_dipole_final": "var_w_dipole_final",
    "w_alpha_final": "var_w_alpha_final",
    "w_energy": "var_we",
    "w_forces": "var_wf",
    "force_loss": "var_force_loss",
    "force_huber_delta": "var_force_huber_delta",
    "w_dipole": "var_wmu",
    "w_polarizability": "var_walpha",
    "w_charges": "var_w_charges",
    "w_atomic_dipoles": "var_w_atomic_dipoles",
    "w_atomic_polarizability": "var_w_atomic_polarizability",
    "w_c6": "var_w_c6",
    "w_bec": "var_w_bec",
    "w_magnetic_moments": "var_w_magnetic_moments",
    "w_effective_field": "var_w_effective_field",
    "w_j": "var_w_j",
    "w_di": "var_w_di",
    "w_dmi": "var_w_dmi",
    "e3mu_use_parity": "var_e3mu_use_parity",
    "e3mu_use_l3": "var_e3mu_use_l3",
    "rbf_type": "var_rbf_type",
    "enable_continuous_chem": "var_enable_continuous_chem",
    "chem_max_z": "var_chem_max_z",
    "chem_aug_prob": "var_chem_aug_prob",
    "chem_aug_noise_std": "var_chem_aug_noise_std",
    "chem_aug_mix_max": "var_chem_aug_mix_max",
    "enable_qeq": "var_enable_qeq",
    "enable_pme": "var_enable_pme",
    "enable_deq": "var_enable_deq",
    "enable_d4": "var_enable_d4",
    "enable_spin": "var_enable_spin",
    "enable_film": "var_enable_film",
    "enable_dmi": "var_enable_dmi",
    "qeq_smearing": "var_qeq_smearing",
    "qeq_hardness_min": "var_qeq_hardness_min",
    "qeq_pme_smearing": "var_qeq_pme_smearing",
    "qeq_pme_lr_wavelength": "var_qeq_pme_lr_wavelength",
    "qeq_stability_floor": "var_qeq_stability_floor",
    "deq_max_iter": "var_deq_max_iter",
    "deq_tol": "var_deq_tol",
    "deq_damping": "var_deq_damping",
    "deq_alpha_max": "var_deq_alpha_max",
    "d4_functional": "var_d4_functional",
    "spin_cutoff": "var_spin_cutoff",
    "coupling_iterations": "var_coupling_iterations",
    "coupling_tol": "var_coupling_tol",
    "auto_level": "var_auto_level",
    "auto_trials": "var_auto_trials",
    "auto_trial_epochs": "var_auto_trial_epochs",
    "auto_subset": "var_auto_subset",
    "live_plot": "var_live_plot",
}


AUTOSEARCH_TO_GUI = {
    "w_energy": "w_energy",
    "w_forces": "w_forces",
    "w_dipole": "w_dipole",
    "w_polarizability": "w_polarizability",
    "w_charges": "w_charges",
    "w_atomic_dipoles": "w_atomic_dipoles",
    "w_atomic_polarizability": "w_atomic_polarizability",
    "w_c6": "w_c6",
    "w_bec": "w_bec",
    "w_magnetic_moments": "w_magnetic_moments",
    "w_effective_field": "w_effective_field",
    "w_j": "w_j",
    "w_di": "w_di",
    "w_dmi": "w_dmi",
    "lr": "lr",
    "batch_size": "batch_size",
    "force_loss": "force_loss",
    "force_huber_delta": "force_huber_delta",
    "r_max": "r_max",
    "num_channels": "num_channels",
    "num_interactions": "num_interactions",
    "num_radial_basis": "num_radial_basis",
    "field_scale": "field_scale",
    "joint_stages": "joint_stages",
    "lr_ground_scale": "lr_ground_scale",
    "lr_response_scale": "lr_response_scale",
    "warmup_epochs": "warmup_epochs",
    "w_dipole_final": "w_dipole_final",
    "w_alpha_final": "w_alpha_final",
    "rbf_type": "rbf_type",
    "qeq_smearing": "qeq_smearing",
    "qeq_hardness_min": "qeq_hardness_min",
    "qeq_pme_smearing": "qeq_pme_smearing",
    "qeq_pme_lr_wavelength": "qeq_pme_lr_wavelength",
    "qeq_stability_floor": "qeq_stability_floor",
    "deq_damping": "deq_damping",
    "deq_max_iter": "deq_max_iter",
    "deq_tol": "deq_tol",
    "deq_alpha_max": "deq_alpha_max",
    "d4_functional": "d4_functional",
    "spin_cutoff": "spin_cutoff",
    "coupling_iterations": "coupling_iterations",
    "coupling_tol": "coupling_tol",
    "chem_aug_prob": "chem_aug_prob",
    "chem_aug_noise_std": "chem_aug_noise_std",
    "chem_aug_mix_max": "chem_aug_mix_max",
}



PALETTE = {
    "background": "#F7F5FA",
    "surface": "#FFFDFE",
    "ink": "#302C3C",
    "muted": "#797386",
    "line": "#E9E3ED",
    "purple": "#8F7AC8",
    "purple_dark": "#6C5A9E",
    "lavender": "#EEE9F8",
    "mint": "#DFF2EA",
    "blue": "#E2EDF9",
    "peach": "#F9E7DD",
    "pink": "#F6E3EC",
    "yellow": "#F7EFD5",
    "danger": "#B6536A",
    "terminal": "#151421",
}


def _human_count(value: int) -> str:
    number = float(value)
    if number >= 1_000_000:
        return f"{number / 1_000_000.0:.3g}M"
    if number >= 1_000:
        return f"{number / 1_000.0:.3g}K"
    return str(int(value))


class _SignalBus(QtCore.QObject):
    log = QtCore.pyqtSignal(str)
    event = QtCore.pyqtSignal(object)
    dataset_ready = QtCore.pyqtSignal(int, object, str)
    estimate_ready = QtCore.pyqtSignal(int, object, str)


class ModernSwitch(QtWidgets.QAbstractButton):
    """Compact animated switch rendered consistently on macOS and Linux."""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(46, 26)
        self._position = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"position", self)
        self._animation.setDuration(135)
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.toggled.connect(self._animate)

    @QtCore.pyqtProperty(float)
    def position(self) -> float:
        return self._position

    @position.setter
    def position(self, value: float) -> None:
        self._position = float(value)
        self.update()

    def _animate(self, checked: bool) -> None:
        self._animation.stop()
        self._animation.setStartValue(self._position)
        self._animation.setEndValue(1.0 if checked else 0.0)
        self._animation.start()

    def setChecked(self, checked: bool) -> None:  # noqa: N802
        super().setChecked(checked)
        self._position = 1.0 if checked else 0.0
        self.update()

    def paintEvent(self, _event: QtGui.QPaintEvent) -> None:  # noqa: N802
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        rect = QtCore.QRectF(1.0, 2.0, 44.0, 22.0)
        if not self.isEnabled():
            track = QtGui.QColor("#E5E0E8")
            knob = QtGui.QColor("#BEB8C4")
        elif self.isChecked():
            track = QtGui.QColor(PALETTE["purple"])
            knob = QtGui.QColor("#FFFFFF")
        else:
            track = QtGui.QColor("#DAD4DE")
            knob = QtGui.QColor("#FFFFFF")
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(track)
        painter.drawRoundedRect(rect, 11.0, 11.0)
        knob_x = 4.0 + self._position * 20.0
        painter.setBrush(knob)
        painter.drawEllipse(QtCore.QRectF(knob_x, 5.0, 16.0, 16.0))


class ToggleTile(QtWidgets.QFrame):
    """Rounded label and switch tile used for architecture choices."""

    toggled = QtCore.pyqtSignal(bool)

    def __init__(self, text: str, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self._available = True
        self.setObjectName("toggleTile")
        self.setProperty("locked", False)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(13, 9, 10, 9)
        layout.setSpacing(8)
        self.label = QtWidgets.QLabel(text)
        self.label.setObjectName("toggleLabel")
        self.label.setWordWrap(True)
        self.switch = ModernSwitch()
        self.status_tag = QtWidgets.QLabel()
        self.status_tag.setObjectName("statusTag")
        self.status_tag.setFixedSize(9, 9)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.status_tag, 0)
        layout.addWidget(self.switch, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.switch.toggled.connect(self.toggled)
        self.setStyleSheet(
            "QFrame#toggleTile { background-color: #FFFDFE; "
            "border: 1px solid #D6CDE0; border-radius: 14px; }"
            "QFrame#toggleTile:hover { background-color: #F4EFFB; "
            "border-color: #8F7AC8; }"
            "QLabel#toggleLabel { color: #3A3445; font-weight: 600; background: transparent; }"
            "QLabel#statusTag { background-color: #5AA47D; border-radius: 4px; }"
            "QFrame#toggleTile[locked=\"true\"] { background-color: #F8F5FA; border-color: #DDD6E2; }"
            "QFrame#toggleTile[locked=\"true\"] QLabel#toggleLabel { color: #7F7887; }"
        )

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if self.isEnabled() and event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.switch.toggle()
        super().mouseReleaseEvent(event)

    def isChecked(self) -> bool:  # noqa: N802
        return self.switch.isChecked()

    def setChecked(self, checked: bool) -> None:  # noqa: N802
        self.switch.setChecked(bool(checked))

    def setEnabled(self, enabled: bool) -> None:  # noqa: N802
        self._available = bool(enabled)
        # Keep the tile hoverable so unavailable features still expose help.
        super().setEnabled(True)
        self.switch.setEnabled(self._available)
        self.setProperty("locked", not self._available)
        self.style().unpolish(self)
        self.style().polish(self)

    def isEnabled(self) -> bool:  # noqa: N802
        return self._available

    def set_status(self, status: str) -> None:
        colors = {
            "enabled": "#8F7AC8",
            "available": "#5AA47D",
            "unavailable": "#C8667C",
            "required": "#D5A43B",
        }
        normalized = status.lower()
        self.status_tag.setStyleSheet(
            f"background-color:{colors.get(normalized, colors['available'])}; "
            "border-radius:4px;"
        )
        self.status_tag.setAccessibleName(normalized.title())


class Card(QtWidgets.QFrame):
    def __init__(
        self,
        title: str,
        subtitle: str,
        color: str,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet(
            f"QFrame#card {{ background: {color}; border: 1px solid rgba(76,58,91,15); "
            "border-radius: 21px; }"
        )
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24.0)
        shadow.setOffset(0.0, 5.0)
        shadow.setColor(QtGui.QColor(63, 45, 77, 24))
        self.setGraphicsEffect(shadow)
        self.body_layout = QtWidgets.QVBoxLayout(self)
        self.body_layout.setContentsMargins(18, 17, 18, 18)
        self.body_layout.setSpacing(11)
        heading = QtWidgets.QLabel(title)
        heading.setObjectName("cardTitle")
        heading.setStyleSheet(
            "font-size: 15px; font-weight: 700; color: #342F40; background: transparent;"
        )
        self.body_layout.addWidget(heading)
        if subtitle:
            detail = QtWidgets.QLabel(subtitle)
            detail.setObjectName("cardSubtitle")
            detail.setWordWrap(True)
            detail.setStyleSheet(
                "font-size: 11px; color: #777080; background: transparent;"
            )
            self.body_layout.addWidget(detail)


class OpaqueToolTip(QtWidgets.QFrame):
    """In-window tooltip that avoids the native translucent window shell."""

    def __init__(self, owner: QtWidgets.QWidget) -> None:
        # A child overlay has no native macOS tooltip frame or translucent
        # shadow. The whole visible surface is therefore painted by Qt CSS.
        super().__init__(owner)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setObjectName("opaqueToolTip")
        self.setStyleSheet(
            "QFrame#opaqueToolTip { background-color:#F4EFFB; border:2px solid #C5B4DC; "
            "border-radius:11px; } "
            "QLabel#opaqueToolTipText { color:#302C3C; background-color:#F4EFFB; "
            "border:none; padding:0; }"
        )
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(13, 11, 13, 11)
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("opaqueToolTipText")
        self.label.setWordWrap(True)
        self.label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label.setFixedWidth(390)
        layout.addWidget(self.label)
        self.hide()

    def show_html(self, html: str, global_position: QtCore.QPoint) -> None:
        self.label.setText(html)
        self.adjustSize()
        owner = self.parentWidget()
        point = owner.mapFromGlobal(global_position) + QtCore.QPoint(14, 18)
        bounds = owner.rect().adjusted(8, 8, -8, -8)
        max_x = max(bounds.left(), bounds.right() - self.width() + 1)
        max_y = max(bounds.top(), bounds.bottom() - self.height() + 1)
        point.setX(max(bounds.left(), min(point.x(), max_x)))
        point.setY(max(bounds.top(), min(point.y(), max_y)))
        self.move(point)
        self.show()
        self.raise_()


class ParameterToolTipFilter(QtCore.QObject):
    def __init__(self, owner: "ModernE3MUGui") -> None:
        super().__init__(owner)
        self.owner = owner
        self.popup = OpaqueToolTip(owner)

    def eventFilter(self, watched: Any, event: Any) -> bool:  # noqa: N802
        event_type = event.type()
        if event_type == QtCore.QEvent.Type.ToolTip:
            key = str(watched.property("parameterKey") or "")
            if not key and bool(watched.property("parameterTable")):
                table = watched.parentWidget()
                while table is not None and not isinstance(
                    table, QtWidgets.QTableWidget
                ):
                    table = table.parentWidget()
                item = table.itemAt(event.pos()) if table is not None else None
                if item is not None:
                    key = str(
                        item.data(QtCore.Qt.ItemDataRole.UserRole) or ""
                    )
            if key:
                global_position = event.globalPos()
                self.popup.show_html(self.owner._tooltip_html(key), global_position)
                return True
        elif event_type in (
            QtCore.QEvent.Type.Leave,
            QtCore.QEvent.Type.Hide,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.Wheel,
        ):
            self.popup.hide()
        return False


class AutoResearchEditorDelegate(QtWidgets.QStyledItemDelegate):
    """Opaque, full-cell editor for Auto Research sampler specifications."""

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        _option: QtWidgets.QStyleOptionViewItem,
        _index: QtCore.QModelIndex,
    ) -> QtWidgets.QLineEdit:
        editor = QtWidgets.QLineEdit(parent)
        editor.setObjectName("autoResearchEditor")
        editor.setAutoFillBackground(True)
        editor.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        palette = editor.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor("#FFFDFE"))
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("#FFFDFE"))
        palette.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor("#302C3C"))
        editor.setPalette(palette)
        editor.setStyleSheet(
            "QLineEdit#autoResearchEditor { background-color:#FFFDFE; color:#302C3C; "
            "border:2px solid #8F7AC8; border-radius:8px; padding:3px 8px; "
            "selection-background-color:#DCCFEC; }"
        )
        return editor

    def setEditorData(
        self, editor: QtWidgets.QLineEdit, index: QtCore.QModelIndex
    ) -> None:
        editor.setText(str(index.data(QtCore.Qt.ItemDataRole.EditRole) or ""))
        editor.selectAll()

    def setModelData(
        self,
        editor: QtWidgets.QLineEdit,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ) -> None:
        model.setData(index, editor.text(), QtCore.Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QLineEdit,
        option: QtWidgets.QStyleOptionViewItem,
        _index: QtCore.QModelIndex,
    ) -> None:
        editor.setGeometry(option.rect.adjusted(1, 1, -1, -1))


class ModernE3MUGui(QtWidgets.QMainWindow):
    """PyQt6 front end backed by the existing model and training module."""

    PAGE_SPECS = (
        ("Data", "#D8E8F7"),
        ("Training", "#D8EEE5"),
        ("Losses", "#F7E1D5"),
        ("Physics", "#F3DCE7"),
        ("Search", "#F4EACB"),
    )

    def __init__(self, backend: Any) -> None:
        super().__init__()
        self.backend = backend
        self.setWindowTitle("Mixed-Granularity E(3)-mu-GNN Research Studio")
        self.resize(1510, 960)
        self.setMinimumSize(1080, 720)
        self.controls: Dict[str, QtWidgets.QWidget] = {}
        self.field_rows: Dict[str, QtWidgets.QWidget] = {}
        self.architecture_tiles: Dict[str, ToggleTile] = {}
        self.loss_keys: List[str] = []
        self._capability: Dict[str, Any] = {"ready": False}
        self._architecture_disabled_reasons: Dict[str, str] = {}
        self._control_disabled_reasons: Dict[str, str] = {}
        self._dataset_cache: Dict[Tuple[str, int, int], Dict[str, Any]] = {}
        self._dataset_generation = 0
        self._dataset_revision = 0
        self._estimate_generation = 0
        self._training_running = False
        self._stop_event = threading.Event()
        self._search_context_revision = 0
        self._auto_best_params: Dict[str, Any] = {}
        self._auto_best_score: Optional[float] = None
        self._auto_best_level = 0
        self._custom_search_specs: Dict[str, tuple] = {}
        self._search_space_customized = False
        self._metric_history: List[Dict[str, Any]] = []
        self._artifact_dir: Optional[Path] = None
        self._stage_histories: Dict[str, List[Dict[str, Any]]] = {}
        self._stage_artifacts: Dict[str, Path] = {}
        self._stage_latest_artifact_epoch: Dict[str, int] = {}
        self._stage_info: Dict[str, Dict[str, Any]] = {}
        self._stage_order: List[str] = []
        self._active_stage_id = ""
        self._default_path = Path.home() / ".dual_layer_field_gui.defaults.json"
        self._factory_values = dict(GUI_DEFAULTS)
        self._config_passthrough: Dict[str, Any] = {}
        self._imported_train_payload: Dict[str, Any] = {}
        self._last_config_warnings: List[str] = []
        self._signal_guard = False
        self._tooltip_filter = ParameterToolTipFilter(self)

        self.bus = _SignalBus(self)
        self.bus.log.connect(self._append_log)
        self.bus.event.connect(self._handle_worker_event)
        self.bus.dataset_ready.connect(self._apply_dataset_result)
        self.bus.estimate_ready.connect(self._apply_estimate_result)

        self.dataset_timer = QtCore.QTimer(self)
        self.dataset_timer.setSingleShot(True)
        self.dataset_timer.setInterval(350)
        self.dataset_timer.timeout.connect(self._start_dataset_scan)
        self.estimate_timer = QtCore.QTimer(self)
        self.estimate_timer.setSingleShot(True)
        self.estimate_timer.setInterval(220)
        self.estimate_timer.timeout.connect(self._start_parameter_estimate)

        self._apply_global_style()
        self._build_ui()
        self._load_default(silent=True)
        self._connect_reactivity()
        self._refresh_architecture_state()
        self._refresh_tooltips()
        self.dataset_timer.start()
        self.estimate_timer.start()

    def _apply_global_style(self) -> None:
        self.setStyleSheet(
            f"""
            QMainWindow, QWidget#root {{ background: {PALETTE['background']}; }}
            QWidget {{ color: {PALETTE['ink']}; font-size: 12px; }}
            QLabel {{ background: transparent; }}
            QLineEdit, QComboBox {{
                min-height: 36px; padding: 0 11px; background: #FFFDFE;
                border: 1px solid #CFC5D7; border-radius: 11px;
                selection-background-color: #B8A8E2;
            }}
            QLineEdit:focus, QComboBox:focus {{ border: 1.5px solid {PALETTE['purple']}; background: #FFFFFF; }}
            QLineEdit[invalidInput="true"] {{
                color: #8C3048; background: #FCE9EE; border: 1.5px solid {PALETTE['danger']};
            }}
            QLineEdit:disabled, QComboBox:disabled {{ color: #847D8B; background: #F1EDF3; border-color: #DDD6E2; }}
            QComboBox::drop-down {{ border: 0; width: 25px; }}
            QComboBox QAbstractItemView {{
                background: #FFFFFF; border: 1px solid #E2DCE7; border-radius: 9px;
                padding: 5px; selection-background-color: #EAE3F6;
            }}
            QPushButton {{
                min-height: 36px; padding: 0 16px; border: 1px solid #BEB0CC; border-radius: 12px;
                background: #FFFDFE; color: #443B54; font-weight: 650;
            }}
            QPushButton:hover {{ background: #EEE8F7; border-color: #8F7AC8; }}
            QPushButton:pressed {{ background: #DED3EE; border-color: #6C5A9E; }}
            QPushButton:disabled {{ color: #918A98; background: #EFEBF1; border-color: #D8D1DC; }}
            QPushButton[primary="true"] {{ background: {PALETTE['purple']}; color: #FFFFFF; border-color: #6C5A9E; }}
            QPushButton[primary="true"]:hover {{ background: #7E68B9; }}
            QPushButton[danger="true"] {{ background: #F8E9EE; color: {PALETTE['danger']}; border-color: #DDAEBB; }}
            QPushButton[nav="true"] {{ min-height: 38px; padding: 0 11px; }}
            QPushButton[nav="true"]:checked {{ background: {PALETTE['purple']}; color: #FFFFFF; }}
            QScrollArea {{ background: transparent; border: 0; }}
            QScrollBar:vertical {{ background: transparent; width: 8px; margin: 4px 0; }}
            QScrollBar::handle:vertical {{ background: #CFC6D8; border-radius: 4px; min-height: 35px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
            QScrollBar:horizontal {{ background: transparent; height: 8px; margin: 0 4px; }}
            QScrollBar::handle:horizontal {{ background: #CFC6D8; border-radius: 4px; min-width: 35px; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
            QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}
            QAbstractScrollArea::corner {{ background: #FFFDFE; border: 0; }}
            QSplitter::handle {{ background: transparent; width: 10px; }}
            QProgressBar {{
                min-height: 8px; max-height: 8px; border: 0; border-radius: 4px; background: #E7E0EA;
            }}
            QProgressBar::chunk {{ background: {PALETTE['purple']}; border-radius: 4px; }}
            QTabWidget::pane {{ border: 0; background: #FFFDFE; border-radius: 18px; top: -1px; }}
            QTabBar::tab {{
                background: #E9E5ED; color: #777080; padding: 10px 20px; margin-right: 5px;
                border-top-left-radius: 11px; border-top-right-radius: 11px; font-weight: 650;
            }}
            QTabBar::tab:selected {{ background: #FFFDFE; color: #40374F; }}
            QTableWidget {{
                background: #FFFDFE; alternate-background-color: #F7F3FA;
                border: 1px solid rgba(76,58,91,20); border-radius: 12px; gridline-color: #EEE9F1;
                selection-background-color: #E6DEF3;
            }}
            QHeaderView::section {{
                background: #EEE9F3; color: #5E5668; border: 0; padding: 8px; font-weight: 700;
            }}
            QToolTip {{
                background-color: #F4EFFB; color: #302C3C; border: 1px solid #8F7AC8;
                border-radius: 9px; padding: 9px;
            }}
            """
        )

    def _build_ui(self) -> None:
        root = QtWidgets.QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        shell = QtWidgets.QVBoxLayout(root)
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)
        shell.addWidget(self._build_header())

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(10)
        self.splitter.addWidget(self._build_settings_panel())
        self.splitter.addWidget(self._build_dashboard())
        self.splitter.setStretchFactor(0, 4)
        self.splitter.setStretchFactor(1, 6)
        self.splitter.setSizes([565, 895])
        shell.addWidget(self.splitter, 1)

    def _build_header(self) -> QtWidgets.QWidget:
        header = QtWidgets.QFrame()
        header.setObjectName("hero")
        header.setStyleSheet(
            "QFrame#hero { background: qlineargradient(x1:0,y1:0,x2:1,y2:1, "
            "stop:0 #665782, stop:0.55 #7E6AA2, stop:1 #9A7EAE); }"
        )
        layout = QtWidgets.QHBoxLayout(header)
        layout.setContentsMargins(27, 17, 27, 17)
        layout.setSpacing(20)
        brand = QtWidgets.QVBoxLayout()
        brand.setSpacing(2)
        title = QtWidgets.QLabel("Mixed-Granularity E(3)-mu-GNN")
        title.setStyleSheet("color:#FFFFFF; font-size:21px; font-weight:750;")
        subtitle = QtWidgets.QLabel(
            "Research Studio  /  L1 local chemistry  /  L2 electrostatics  /  L3 spin Hamiltonian"
        )
        subtitle.setStyleSheet("color:#EEE9F7; font-size:11px;")
        brand.addWidget(title)
        brand.addWidget(subtitle)
        layout.addLayout(brand, 1)
        state = QtWidgets.QVBoxLayout()
        state.setSpacing(2)
        self.header_status = QtWidgets.QLabel("Ready")
        self.header_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.header_status.setStyleSheet("color:#FFFFFF; font-size:12px; font-weight:700;")
        self.header_progress = QtWidgets.QLabel("Select a dataset to begin")
        self.header_progress.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.header_progress.setStyleSheet("color:#EEE9F7; font-size:10px;")
        state.addWidget(self.header_status)
        state.addWidget(self.header_progress)
        layout.addLayout(state)
        return header

    def _build_settings_panel(self) -> QtWidgets.QWidget:
        panel = QtWidgets.QWidget()
        panel.setMinimumWidth(470)
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(18, 17, 5, 18)
        layout.setSpacing(10)

        utility = QtWidgets.QHBoxLayout()
        utility.setSpacing(7)
        for text, slot, color in (
            ("Import", self._import_config, PALETTE["blue"]),
            ("Export", self._export_config, PALETTE["mint"]),
            ("Save Default", self._save_default, PALETTE["yellow"]),
            ("Factory Reset", self._factory_reset, PALETTE["pink"]),
        ):
            button = QtWidgets.QPushButton(text)
            button.setStyleSheet(
                f"QPushButton {{ background-color:#FFFDFE; border:2px solid {color}; }} "
                f"QPushButton:hover {{ background-color:{color}; border-color:#8F7AC8; }}"
            )
            button.clicked.connect(slot)
            utility.addWidget(button)
        layout.addLayout(utility)

        nav = QtWidgets.QHBoxLayout()
        nav.setSpacing(6)
        self.nav_group = QtWidgets.QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.page_stack = QtWidgets.QStackedWidget()
        for index, (name, color) in enumerate(self.PAGE_SPECS):
            button = QtWidgets.QPushButton(name)
            button.setCheckable(True)
            button.setProperty("nav", True)
            button.setStyleSheet(
                f"QPushButton {{ background-color:#FFFDFE; border:2px solid {color}; }}"
                f"QPushButton:hover {{ background-color:{color}; border-color:#8F7AC8; }}"
                f"QPushButton:checked {{ background-color:{PALETTE['purple']}; color:#FFFFFF; border-color:#6C5A9E; }}"
            )
            button.clicked.connect(lambda _checked, page=index: self.page_stack.setCurrentIndex(page))
            nav.addWidget(button, 1)
            self.nav_group.addButton(button, index)
            self.page_stack.addWidget(self._build_page(name))
            if index == 0:
                button.setChecked(True)
        layout.addLayout(nav)
        layout.addWidget(self.page_stack, 1)
        return panel

    def _build_page(self, name: str) -> QtWidgets.QScrollArea:
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QtWidgets.QWidget()
        content.setStyleSheet("background: transparent;")
        body = QtWidgets.QVBoxLayout(content)
        body.setContentsMargins(1, 3, 10, 18)
        body.setSpacing(13)
        if name == "Data":
            self._populate_data_page(body)
        elif name == "Training":
            self._populate_training_page(body)
        elif name == "Losses":
            self._populate_losses_page(body)
        elif name == "Physics":
            self._populate_physics_page(body)
        elif name == "Search":
            self._populate_search_page(body)
        body.addStretch(1)
        scroll.setWidget(content)
        return scroll

    def _populate_data_page(self, layout: QtWidgets.QVBoxLayout) -> None:
        card = Card(
            "Datasets & Checkpoints",
            "Choose one canonical mixed-label file, or use the legacy static/response pair.",
            PALETTE["blue"],
        )
        for key, title, mode in (
            ("dataset", "Canonical HDF5", "dataset"),
            ("static_data", "Legacy static", "data"),
            ("response_data", "Legacy response", "data"),
            ("base_ckpt", "Pretrained / base checkpoint", "checkpoint"),
            ("out_ckpt", "Output checkpoint", "save"),
        ):
            card.body_layout.addWidget(self._make_file_field(key, title, mode))
        layout.addWidget(card)

        guide = Card(
            "Dataset Guard",
            "Architecture availability is derived from label masks, elements, and periodicity.",
            PALETTE["surface"],
        )
        self.dataset_summary = QtWidgets.QLabel("Select a dataset to inspect its physical capabilities.")
        self.dataset_summary.setWordWrap(True)
        self.dataset_summary.setStyleSheet("color:#665E70; line-height:1.3;")
        guide.body_layout.addWidget(self.dataset_summary)
        layout.addWidget(guide)

    def _populate_training_page(self, layout: QtWidgets.QVBoxLayout) -> None:
        card = Card(
            "Optimizer & Backbone",
            "Aligned controls and an exact live parameter count for the detected element table.",
            PALETTE["mint"],
        )
        self._add_field_grid(
            card,
            (
                ("epochs", "Epochs", None),
                ("batch_size", "Batch size", None),
                ("lr", "Learning rate", None),
                ("lr_scheduler", "Schedule", ("flat", "cosine")),
                ("force_loss", "Force loss", ("mse", "huber")),
                ("force_huber_delta", "Huber delta", None),
                ("device", "Device", ("auto", "cpu", "mps", "cuda")),
                (
                    "cpu_threads",
                    "CPU threads",
                    ("auto", *tuple(str(value) for value in range(1, _available_cpu_threads() + 1))),
                ),
                ("dtype", "Dtype", ("float32", "float64")),
                ("r_max", "Cutoff r_max", None),
                ("num_channels", "Channels", None),
                ("num_interactions", "Interactions", None),
                ("num_radial_basis", "Radial basis count", None),
                ("field_scale", "Field scale", None),
                ("val_fraction", "Validation fraction", None),
                ("seed", "Random seed", None),
            ),
        )
        self.model_size_label = QtWidgets.QLabel("Model size: estimating current configuration...")
        self.model_size_label.setWordWrap(True)
        self.model_size_label.setStyleSheet("color:#4F6C60; font-weight:650;")
        card.body_layout.addWidget(self.model_size_label)
        self.thread_policy_label = QtWidgets.QLabel()
        self.thread_policy_label.setWordWrap(True)
        self.thread_policy_label.setStyleSheet("color:#4F6C60;")
        card.body_layout.addWidget(self.thread_policy_label)
        self._update_thread_policy_label()
        toggle_row = QtWidgets.QHBoxLayout()
        toggle_row.addWidget(self._make_toggle_tile("export_sevennet", "SevenNet export"))
        toggle_row.addWidget(self._make_toggle_tile("save_epoch_artifacts", "Live plots + artifacts"))
        card.body_layout.addLayout(toggle_row)
        streaming_row = QtWidgets.QHBoxLayout()
        streaming_row.addWidget(self._make_toggle_tile("stream_hdf5", "Stream HDF5 batches"))
        streaming_row.addWidget(self._make_toggle_tile("cache_neighbor_graphs", "Disk graph cache"))
        card.body_layout.addLayout(streaming_row)
        layout.addWidget(card)

        cascade = Card(
            "Joint Fine-Tuning Cascade",
            "Base -> Response -> progressively lower-rate mixed-granularity refinement.",
            PALETTE["lavender"],
        )
        self._add_field_grid(
            cascade,
            (
                ("joint_stages", "Joint stages", None),
                ("warmup_epochs", "Warmup epochs", None),
                ("lr_ground_scale", "Layer-1 LR scale", None),
                ("lr_response_scale", "Response LR scale", None),
                ("w_dipole_final", "Final dipole weight", None),
                ("w_alpha_final", "Final alpha weight", None),
            ),
        )
        layout.addWidget(cascade)

    def _populate_losses_page(self, layout: QtWidgets.QVBoxLayout) -> None:
        card = Card(
            "Multi-Task Loss Weights",
            "Zero disables a target. Missing labels and architecture-incompatible targets are locked.",
            PALETTE["peach"],
        )
        specs = (
            ("w_energy", "Energy", None),
            ("w_forces", "Forces", None),
            ("w_dipole", "Dipole", None),
            ("w_polarizability", "Polarizability", None),
            ("w_charges", "Charges", None),
            ("w_atomic_dipoles", "Atomic dipoles", None),
            ("w_atomic_polarizability", "Atomic polarizability", None),
            ("w_c6", "C6", None),
            ("w_bec", "BEC", None),
            ("w_magnetic_moments", "Magnetic moments", None),
            ("w_effective_field", "Effective spin field", None),
            ("w_j", "J effective", None),
            ("w_di", "Di", None),
            ("w_dmi", "DMI", None),
        )
        self.loss_keys = [key for key, _label, _items in specs]
        self._add_field_grid(card, specs)
        layout.addWidget(card)

    def _populate_physics_page(self, layout: QtWidgets.QVBoxLayout) -> None:
        switches = Card(
            "Architecture Switches",
            "The dataset controls availability; selected layers control every dependent field and search dimension.",
            PALETTE["pink"],
        )
        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(9)
        grid.setVerticalSpacing(9)
        specs = (
            ("e3mu_use_parity", "O(3) parity"),
            ("e3mu_use_l3", "L=3 tensor"),
            ("enable_continuous_chem", "Continuous chemistry"),
            ("enable_qeq", "QEq"),
            ("enable_pme", "PME / Ewald"),
            ("enable_deq", "DEQ polarization"),
            ("enable_d4", "D4 dispersion"),
            ("enable_spin", "Spin J / Di / DMI"),
            ("enable_film", "FiLM coupling"),
            ("enable_dmi", "DMI term"),
        )
        for index, (key, label) in enumerate(specs):
            tile = ToggleTile(label)
            tile.setChecked(bool(GUI_DEFAULTS[key]))
            tile.toggled.connect(lambda _checked, name=key: self._architecture_changed(name))
            self.controls[key] = tile
            self.field_rows[key] = tile
            self.architecture_tiles[key] = tile
            self._set_tooltip_targets(
                key, tile, tile.label, tile.status_tag, tile.switch
            )
            grid.addWidget(tile, index // 2, index % 2)
        switches.body_layout.addLayout(grid)
        self.architecture_summary = QtWidgets.QLabel(
            "Select data to evaluate physical applicability. Architecture choices remain fixed during AutoSearch."
        )
        self.architecture_summary.setWordWrap(True)
        self.architecture_summary.setStyleSheet("color:#705D68; font-size:11px;")
        switches.body_layout.addWidget(self.architecture_summary)
        self._add_field_grid(
            switches,
            (("rbf_type", "Radial basis family", ("gaussian", "trainable_gaussian", "bessel")),),
        )
        layout.addWidget(switches)

        chemistry = Card(
            "Continuous Chemistry",
            "Periodic-table descriptors and optional alchemical regularization.",
            PALETTE["mint"],
        )
        self._add_field_grid(
            chemistry,
            (
                ("chem_max_z", "Maximum atomic number", None),
                ("chem_aug_prob", "Augmentation probability", None),
                ("chem_aug_noise_std", "Descriptor noise", None),
                ("chem_aug_mix_max", "Mixing limit", None),
            ),
        )
        layout.addWidget(chemistry)

        solver = Card(
            "Physics Solver Parameters",
            "Only controls used by the selected layers remain editable.",
            PALETTE["lavender"],
        )
        self._add_field_grid(
            solver,
            (
                ("qeq_smearing", "QEq smearing", None),
                ("qeq_hardness_min", "Hardness minimum", None),
                ("qeq_pme_smearing", "PME smearing", None),
                ("qeq_pme_lr_wavelength", "PME wavelength", None),
                ("qeq_stability_floor", "QEq stability floor", None),
                ("deq_max_iter", "DEQ max iterations", None),
                ("deq_tol", "DEQ tolerance", None),
                ("deq_damping", "DEQ damping", None),
                ("deq_alpha_max", "DEQ alpha max", None),
                ("d4_functional", "D4 functional", ("pbe", "pbe0", "b3lyp")),
                ("spin_cutoff", "Spin cutoff", None),
                ("coupling_iterations", "Coupling iterations", None),
                ("coupling_tol", "Coupling tolerance", None),
            ),
        )
        layout.addWidget(solver)

    def _populate_search_page(self, layout: QtWidgets.QVBoxLayout) -> None:
        card = Card(
            "Auto Research / AutoSearch",
            "The selected architecture is locked. Search automatically attaches only its active solver parameters.",
            PALETTE["yellow"],
        )
        self._add_field_grid(
            card,
            (
                (
                    "auto_level",
                    "Search level",
                    (
                        "0: Disabled",
                        "1: Active Loss Weights",
                        "2: + Optimizer & Backbone",
                        "3: + Joint Fine-Tuning",
                        "4: + Active Physics Solvers",
                    ),
                ),
                ("auto_trials", "Trials", None),
                ("auto_trial_epochs", "Trial epochs", None),
                ("auto_subset", "Sample %", None),
            ),
        )
        actions = QtWidgets.QHBoxLayout()
        self.auto_run_button = QtWidgets.QPushButton("Run Auto Research")
        self.auto_run_button.setProperty("primary", True)
        self.auto_run_button.setStyleSheet(
            "QPushButton { background-color:#765FB0; color:#FFFFFF; "
            "border:2px solid #5F4B96; font-weight:700; } "
            "QPushButton:hover { background-color:#654E9F; border-color:#493875; } "
            "QPushButton:pressed { background-color:#58438D; } "
            "QPushButton:disabled { background-color:#D8D0E4; color:#847B91; "
            "border-color:#C7BDCF; }"
        )
        self.auto_run_button.clicked.connect(self._run_auto_search)
        self.auto_apply_button = QtWidgets.QPushButton("Apply Best")
        self.auto_apply_button.setStyleSheet(
            "QPushButton { background-color:#FFFDFE; color:#5F4B96; "
            "border:2px solid #765FB0; font-weight:700; } "
            "QPushButton:hover { background-color:#E8DFF4; border-color:#5F4B96; } "
            "QPushButton:pressed { background-color:#DCCFEC; } "
            "QPushButton:disabled { background-color:#F0ECF2; color:#98909F; "
            "border-color:#D2CBD7; }"
        )
        self.auto_apply_button.clicked.connect(self._apply_auto_best)
        self.auto_apply_button.setEnabled(False)
        actions.addWidget(self.auto_run_button, 1)
        actions.addWidget(self.auto_apply_button, 1)
        card.body_layout.addLayout(actions)
        self.auto_summary = QtWidgets.QLabel("No completed search result yet.")
        self.auto_summary.setWordWrap(True)
        self.auto_summary.setStyleSheet("color:#756640; font-weight:650;")
        card.body_layout.addWidget(self.auto_summary)
        layout.addWidget(card)

        table_card = Card(
            "Active Search Dimensions",
            "The table updates immediately when architecture, labels, losses, or search level change.",
            PALETTE["surface"],
        )
        self.search_table = QtWidgets.QTableWidget(0, 6)
        self.search_table.setHorizontalHeaderLabels(
            ("Parameter", "Sampler", "Domain (JSON)", "Best / current", "Last tried", "Status")
        )
        search_header = self.search_table.horizontalHeader()
        search_header.setMinimumSectionSize(72)
        for column in range(6):
            search_header.setSectionResizeMode(
                column, QtWidgets.QHeaderView.ResizeMode.Interactive
            )
        for column, width in enumerate((145, 105, 285, 115, 105, 82)):
            self.search_table.setColumnWidth(column, width)
        self.search_table.verticalHeader().setVisible(False)
        self.search_table.setAlternatingRowColors(True)
        self.search_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked
            | QtWidgets.QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.search_table.setMinimumHeight(340)
        self.search_table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.search_table.setWordWrap(False)
        self.search_scroll_corner = QtWidgets.QWidget(self.search_table)
        self.search_scroll_corner.setStyleSheet(
            "background-color:#FFFDFE; border:0;"
        )
        self.search_table.setCornerWidget(self.search_scroll_corner)
        self.search_editor_delegate = AutoResearchEditorDelegate(self.search_table)
        self.search_table.setItemDelegateForColumn(1, self.search_editor_delegate)
        self.search_table.setItemDelegateForColumn(2, self.search_editor_delegate)
        search_viewport = self.search_table.viewport()
        search_viewport.setProperty("parameterTable", True)
        search_viewport.installEventFilter(self._tooltip_filter)
        table_card.body_layout.addWidget(self.search_table)
        editor_actions = QtWidgets.QGridLayout()
        editor_actions.setHorizontalSpacing(9)
        editor_actions.setVerticalSpacing(8)
        self.search_add_button = QtWidgets.QPushButton("Add Parameter")
        self.search_remove_button = QtWidgets.QPushButton("Remove Selected")
        self.search_reset_button = QtWidgets.QPushButton("Reset Suggested Ranges")
        self.search_add_button.clicked.connect(self._add_search_parameter)
        self.search_remove_button.clicked.connect(self._remove_search_parameters)
        self.search_reset_button.clicked.connect(self._reset_search_space_editor)
        self.search_table.itemChanged.connect(self._search_space_item_changed)
        for button in (self.search_add_button, self.search_remove_button):
            button.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Fixed,
            )
        self.search_reset_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        editor_actions.addWidget(self.search_add_button, 0, 0)
        editor_actions.addWidget(self.search_remove_button, 0, 1)
        editor_actions.addWidget(self.search_reset_button, 1, 0, 1, 2)
        editor_actions.setColumnStretch(0, 1)
        editor_actions.setColumnStretch(1, 1)
        table_card.body_layout.addLayout(editor_actions)
        range_help = QtWidgets.QLabel(
            "Double-click Sampler or Domain to edit. Domains are JSON lists: "
            "[min,max], [min,max,zero_probability], or [choice,...]."
        )
        range_help.setWordWrap(True)
        range_help.setStyleSheet("color:#7E7585;")
        table_card.body_layout.addWidget(range_help)
        layout.addWidget(table_card)

    def _build_dashboard(self) -> QtWidgets.QWidget:
        panel = QtWidgets.QWidget()
        panel.setMinimumWidth(570)
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(5, 17, 18, 18)
        layout.setSpacing(12)

        controls = Card(
            "Run Control",
            "Select one workflow and choose whether canonical HDF5 stays streamed.",
            PALETTE["surface"],
        )
        self.training_buttons: List[QtWidgets.QPushButton] = []
        mode_row = QtWidgets.QHBoxLayout()
        mode_row.setSpacing(8)
        mode_label = QtWidgets.QLabel("Training mode")
        mode_label.setStyleSheet("color:#665E70; font-weight:700;")
        mode_row.addWidget(mode_label)
        self.training_mode_group = QtWidgets.QButtonGroup(self)
        self.training_mode_group.setExclusive(True)
        self.training_mode_buttons: Dict[str, QtWidgets.QPushButton] = {}
        for mode, text in (
            ("base", "Base"),
            ("response", "Response"),
            ("joint", "Mixed Joint"),
            ("full_chain", "Full Chain"),
        ):
            button = QtWidgets.QPushButton(text)
            button.setCheckable(True)
            button.setStyleSheet(
                "QPushButton { background-color:#FFFDFE; color:#403849; "
                "border:2px solid #CFC5D7; }"
                "QPushButton:hover { background-color:#EEE8F7; border-color:#8F7AC8; }"
                "QPushButton:checked { background-color:#8F7AC8; color:#FFFFFF; "
                "border-color:#6C5A9E; }"
            )
            button.setToolTip(f"Select {text} training workflow")
            button.toggled.connect(
                lambda checked, selected=mode: (
                    self._set_selected_training_mode(selected) if checked else None
                )
            )
            self.training_mode_group.addButton(button)
            self.training_mode_buttons[mode] = button
            self.training_buttons.append(button)
            mode_row.addWidget(button, 1)
        self.training_mode_buttons["joint"].setChecked(True)
        controls.body_layout.addLayout(mode_row)

        row = QtWidgets.QHBoxLayout()
        row.setSpacing(8)
        self.streaming_mode_button = QtWidgets.QPushButton()
        self.streaming_mode_button.setCheckable(True)
        self.streaming_mode_button.setStyleSheet(
            "QPushButton { background-color:#F9E7DD; color:#6D4E45; "
            "border:2px solid #E5BFAE; }"
            "QPushButton:hover { background-color:#F4D9CA; border-color:#C9957D; }"
            "QPushButton:checked { background-color:#DFF2EA; color:#376553; "
            "border-color:#86BDA8; }"
        )
        self.streaming_mode_button.setChecked(bool(self.value("stream_hdf5")))
        self.streaming_mode_button.toggled.connect(self._streaming_mode_toggled)
        self._update_streaming_mode_button()
        self._set_tooltip_targets("stream_hdf5", self.streaming_mode_button)
        self.training_buttons.append(self.streaming_mode_button)
        row.addWidget(self.streaming_mode_button)

        self.start_training_button = QtWidgets.QPushButton("Start Training")
        self.start_training_button.setProperty("primary", True)
        self.start_training_button.clicked.connect(self._start_selected_training)
        self.training_buttons.append(self.start_training_button)
        row.addWidget(self.start_training_button)

        artifacts = QtWidgets.QPushButton("Artifacts")
        artifacts.clicked.connect(self._open_artifacts)
        row.addWidget(artifacts)
        row.addStretch(1)
        stop = QtWidgets.QPushButton("Stop")
        stop.setProperty("danger", True)
        stop.clicked.connect(self._stop_current_run)
        row.addWidget(stop)
        controls.body_layout.addLayout(row)
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 1000)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        controls.body_layout.addWidget(self.progress_bar)
        layout.addWidget(controls)

        metrics = QtWidgets.QHBoxLayout()
        metrics.setSpacing(9)
        self.state_value = self._metric_card(metrics, "STATE", "Ready", PALETTE["mint"])
        self.epoch_value = self._metric_card(metrics, "PROGRESS", "Epoch -- / --", PALETTE["blue"])
        self.score_value = self._metric_card(metrics, "NORMALIZED VALIDATION", "Score --", PALETTE["peach"])
        layout.addLayout(metrics)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setDocumentMode(True)
        analysis = QtWidgets.QWidget()
        analysis_layout = QtWidgets.QVBoxLayout(analysis)
        analysis_layout.setContentsMargins(13, 13, 13, 13)
        toolbar = QtWidgets.QHBoxLayout()
        toolbar.addWidget(QtWidgets.QLabel("View"))
        live_view = self._make_combo(
            "live_plot",
            ("Regression", "MAE History", "Multi-Task", "Physics Residuals", "Memory"),
        )
        live_view.setMaximumWidth(210)
        toolbar.addWidget(live_view)
        toolbar.addWidget(QtWidgets.QLabel("Stage"))
        self.analysis_stage_selector = QtWidgets.QComboBox()
        self.analysis_stage_selector.addItem("All Stages", "")
        self.analysis_stage_selector.setMinimumWidth(150)
        self.analysis_stage_selector.setMaximumWidth(220)
        self.analysis_stage_selector.currentIndexChanged.connect(
            lambda _index: self._render_live_dashboard()
        )
        toolbar.addWidget(self.analysis_stage_selector)
        toolbar.addStretch(1)
        hint = QtWidgets.QLabel("Updates after every validation epoch")
        hint.setStyleSheet("color:#8A8391;")
        toolbar.addWidget(hint)
        analysis_layout.addLayout(toolbar)
        self.analysis_stage_summary = QtWidgets.QLabel("Stage: current run")
        self.analysis_stage_summary.setWordWrap(True)
        self.analysis_stage_summary.setStyleSheet(
            "color:#665E70; background:#F5F0F8; border-radius:9px; "
            "padding:6px 9px; font-size:10px;"
        )
        analysis_layout.addWidget(self.analysis_stage_summary)
        try:
            from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
            from matplotlib.figure import Figure

            self.figure = Figure(figsize=(8.5, 5.4), dpi=100, facecolor="#FFFDFE")
            self.canvas = FigureCanvasQTAgg(self.figure)
            self.canvas.setMinimumHeight(360)
            analysis_layout.addWidget(self.canvas, 1)
        except Exception as exc:
            self.figure = None
            self.canvas = None
            unavailable = QtWidgets.QLabel(f"Live charts unavailable: {exc}")
            unavailable.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            analysis_layout.addWidget(unavailable, 1)
        self.tabs.addTab(analysis, "Live Analysis")

        log_page = QtWidgets.QWidget()
        log_layout = QtWidgets.QVBoxLayout(log_page)
        log_layout.setContentsMargins(11, 11, 11, 11)
        self.log_view = QtWidgets.QPlainTextEdit()
        self.log_view.setObjectName("trainingLog")
        self.log_view.setReadOnly(True)
        self.log_view.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.log_view.setStyleSheet(
            f"QPlainTextEdit#trainingLog {{ background-color: {PALETTE['terminal']}; "
            "color: #DDE4F0; border: none; border-radius: 13px; padding: 12px; "
            "font-family: Menlo; font-size: 11px; }"
        )
        log_layout.addWidget(self.log_view)
        self.tabs.addTab(log_page, "Training Log")
        layout.addWidget(self.tabs, 1)
        self._render_live_dashboard()
        return panel

    def _metric_card(
        self, layout: QtWidgets.QHBoxLayout, title: str, value: str, color: str
    ) -> QtWidgets.QLabel:
        frame = QtWidgets.QFrame()
        frame.setStyleSheet(f"QFrame {{ background:{color}; border-radius:17px; }}")
        box = QtWidgets.QVBoxLayout(frame)
        box.setContentsMargins(14, 11, 14, 12)
        box.setSpacing(3)
        name = QtWidgets.QLabel(title)
        name.setStyleSheet("color:#817989; font-size:9px; font-weight:700;")
        content = QtWidgets.QLabel(value)
        content.setStyleSheet("color:#3B3544; font-size:15px; font-weight:750;")
        box.addWidget(name)
        box.addWidget(content)
        layout.addWidget(frame, 1)
        return content

    def _make_file_field(self, key: str, title: str, mode: str) -> QtWidgets.QWidget:
        row = QtWidgets.QWidget()
        row.setStyleSheet("background: transparent;")
        layout = QtWidgets.QGridLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(4)
        label = QtWidgets.QLabel(title)
        label.setStyleSheet("font-weight:650; color:#4E4659;")
        entry = QtWidgets.QLineEdit(str(GUI_DEFAULTS[key]))
        browse = QtWidgets.QPushButton("Browse")
        browse.setFixedWidth(78)
        browse.clicked.connect(lambda _checked=False, name=key, kind=mode: self._browse(name, kind))
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(entry, 1, 0)
        layout.addWidget(browse, 1, 1)
        self.controls[key] = entry
        self.field_rows[key] = row
        self._set_tooltip_targets(key, row, label, entry, browse)
        return row

    def _add_field_grid(
        self,
        card: Card,
        specs: Sequence[Tuple[str, str, Optional[Sequence[str]]]],
    ) -> None:
        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(11)
        grid.setVerticalSpacing(10)
        for index, (key, title, items) in enumerate(specs):
            row, column = divmod(index, 2)
            field = QtWidgets.QWidget()
            field.setStyleSheet("background: transparent;")
            box = QtWidgets.QVBoxLayout(field)
            box.setContentsMargins(0, 0, 0, 0)
            box.setSpacing(5)
            label = QtWidgets.QLabel(title)
            label.setStyleSheet("font-weight:650; color:#514958;")
            control = self._make_combo(key, items) if items is not None else self._make_line_edit(key)
            box.addWidget(label)
            box.addWidget(control)
            grid.addWidget(field, row, column)
            self.field_rows[key] = field
            self._set_tooltip_targets(key, field, label, control)
        card.body_layout.addLayout(grid)

    def _make_line_edit(self, key: str) -> QtWidgets.QLineEdit:
        control = QtWidgets.QLineEdit(str(GUI_DEFAULTS[key]))
        rule = GUI_NUMERIC_RULES.get(key)
        if rule is not None:
            if rule.kind == "int":
                lower = int(rule.minimum) if rule.minimum is not None else -2147483648
                upper = int(rule.maximum) if rule.maximum is not None else 2147483647
                validator: QtGui.QValidator = QtGui.QIntValidator(
                    lower, upper, control
                )
            else:
                validator = QtGui.QDoubleValidator(control)
                validator.setNotation(
                    QtGui.QDoubleValidator.Notation.ScientificNotation
                )
                # Range enforcement remains in the strict preflight so users
                # can naturally replace a value via intermediate text states.
            control.setValidator(validator)
            control.setProperty("numericParameter", True)
        self.controls[key] = control
        return control

    def _make_combo(self, key: str, items: Sequence[str]) -> QtWidgets.QComboBox:
        control = QtWidgets.QComboBox()
        control.addItems([str(item) for item in items])
        configured = str(GUI_DEFAULTS[key])
        control.setCurrentText(configured if control.findText(configured) >= 0 else str(items[0]))
        self.controls[key] = control
        return control

    def _make_toggle_tile(self, key: str, title: str) -> ToggleTile:
        tile = ToggleTile(title)
        tile.setChecked(bool(GUI_DEFAULTS[key]))
        self.controls[key] = tile
        self.field_rows[key] = tile
        self._set_tooltip_targets(key, tile, tile.label, tile.status_tag, tile.switch)
        return tile

    def _set_tooltip_targets(self, key: str, *widgets: QtWidgets.QWidget) -> None:
        for widget in widgets:
            widget.setProperty("parameterKey", key)
            widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
            widget.installEventFilter(self._tooltip_filter)

    def value(self, key: str) -> Any:
        control = self.controls[key]
        if isinstance(control, QtWidgets.QLineEdit):
            return control.text().strip()
        if isinstance(control, QtWidgets.QComboBox):
            return control.currentText()
        if isinstance(control, ToggleTile):
            return control.isChecked()
        raise TypeError(f"Unsupported GUI control for {key}: {type(control).__name__}")

    def set_value(self, key: str, value: Any) -> None:
        control = self.controls.get(key)
        if control is None:
            return
        blocker = QtCore.QSignalBlocker(control)
        switch_blocker = None
        if isinstance(control, QtWidgets.QLineEdit):
            control.setText(str(value))
        elif isinstance(control, QtWidgets.QComboBox):
            text = str(value)
            index = control.findText(text)
            if index >= 0:
                control.setCurrentIndex(index)
            else:
                if key == "cpu_threads":
                    control.setCurrentText("auto")
                    raise ValueError(
                        f"requested {value!r} exceeds this machine's selectable "
                        f"range (1-{self.backend._available_cpu_threads()}); using auto"
                    )
                raise ValueError(
                    f"Unsupported value {value!r} for {key}; "
                    f"expected one of {[control.itemText(i) for i in range(control.count())]}"
                )
        elif isinstance(control, ToggleTile):
            switch_blocker = QtCore.QSignalBlocker(control.switch)
            control.setChecked(self.backend._coerce_config_bool(value))
        del blocker
        if switch_blocker is not None:
            del switch_blocker
        if key == "stream_hdf5" and hasattr(self, "streaming_mode_button"):
            mode_blocker = QtCore.QSignalBlocker(self.streaming_mode_button)
            self.streaming_mode_button.setChecked(bool(value))
            del mode_blocker
            self._update_streaming_mode_button()

    def _set_selected_training_mode(self, mode: str) -> None:
        selected = str(mode).strip().lower()
        if selected not in {"base", "response", "joint", "full_chain"}:
            raise ValueError(f"Unsupported GUI training mode: {mode!r}")
        self._selected_training_mode = selected
        button = getattr(self, "training_mode_buttons", {}).get(selected)
        if button is not None and not button.isChecked():
            button.setChecked(True)

    def _start_selected_training(self) -> None:
        if self._selected_training_mode == "full_chain":
            self._run_full_chain()
        else:
            self._start_training(self._selected_training_mode)

    def _update_streaming_mode_button(self) -> None:
        if not hasattr(self, "streaming_mode_button"):
            return
        streamed = self.streaming_mode_button.isChecked()
        self.streaming_mode_button.setText(
            "Streaming ON" if streamed else "Full Load"
        )
        self.streaming_mode_button.setAccessibleName(
            "Streaming training enabled" if streamed else "Full dataset loading enabled"
        )

    def _streaming_mode_toggled(self, checked: bool) -> None:
        self.set_value("stream_hdf5", bool(checked))
        self._update_streaming_mode_button()
        self._parameter_changed("stream_hdf5")

    def _streaming_setting_toggled(self, checked: bool) -> None:
        if not hasattr(self, "streaming_mode_button"):
            return
        blocker = QtCore.QSignalBlocker(self.streaming_mode_button)
        self.streaming_mode_button.setChecked(bool(checked))
        del blocker
        self._update_streaming_mode_button()

    def _enforce_spin_cutoff_bound(self) -> bool:
        """Clamp stale/imported magnetic cutoffs to the current local graph."""
        if "r_max" not in self.controls or "spin_cutoff" not in self.controls:
            return False
        try:
            local_cutoff = float(self.value("r_max"))
            magnetic_cutoff = float(self.value("spin_cutoff"))
            bounded = self.backend._compatible_spin_cutoff(
                local_cutoff, magnetic_cutoff
            )
        except (TypeError, ValueError):
            return False
        if math.isclose(bounded, magnetic_cutoff, rel_tol=0.0, abs_tol=1e-12):
            return False
        self.set_value("spin_cutoff", f"{bounded:.12g}")
        return True

    def _cutoff_editing_finished(self) -> None:
        if not self._enforce_spin_cutoff_bound():
            return
        self._refresh_tooltips()
        self._refresh_search_table()
        self.estimate_timer.start()

    def current_values(self) -> Dict[str, Any]:
        return {key: self.value(key) for key in self.controls}

    def _update_thread_policy_label(self) -> None:
        if not hasattr(self, "thread_policy_label"):
            return
        requested_device = str(self.value("device") or "auto").strip().lower()
        resolved_device = (
            self.backend._default_device_name()
            if requested_device == "auto"
            else requested_device
        )
        try:
            policy = self.backend._resolve_cpu_thread_policy(
                self.value("cpu_threads"), torch.device(resolved_device)
            )
            suffix = (
                "all available CPU threads"
                if policy["source"] == "auto-cpu-all"
                else "bounded accelerator helper pool"
                if str(policy["source"]).endswith("-helper")
                else str(policy["source"])
            )
            self.thread_policy_label.setText(
                f"Runtime thread policy: {policy['effective']} / "
                f"{policy['available']} CPU threads ({suffix})."
            )
        except Exception as exc:
            self.thread_policy_label.setText(f"Runtime thread policy is invalid: {exc}")

    def _connect_reactivity(self) -> None:
        dataset_keys = {"dataset", "static_data", "response_data"}
        architecture_keys = set(self.architecture_tiles)
        for key, control in self.controls.items():
            if isinstance(control, QtWidgets.QLineEdit):
                if key in dataset_keys:
                    control.textChanged.connect(lambda _text, name=key: self._dataset_selection_changed(name))
                else:
                    control.textChanged.connect(lambda _text, name=key: self._parameter_changed(name))
                if key in {"r_max", "spin_cutoff"}:
                    control.editingFinished.connect(self._cutoff_editing_finished)
            elif isinstance(control, QtWidgets.QComboBox):
                control.currentTextChanged.connect(lambda _text, name=key: self._parameter_changed(name))
            elif isinstance(control, ToggleTile) and key not in architecture_keys:
                control.toggled.connect(lambda _checked, name=key: self._parameter_changed(name))
                if key == "stream_hdf5":
                    control.toggled.connect(self._streaming_setting_toggled)

    def _parameter_changed(self, key: str) -> None:
        if self._signal_guard:
            return
        self._update_numeric_control_state(key)
        try:
            if key in {"device", "cpu_threads"} and hasattr(self, "thread_policy_label"):
                self._update_thread_policy_label()
            if key in {
                "r_max", "num_channels", "num_interactions", "num_radial_basis",
                "dtype", "rbf_type", "field_scale", "spin_cutoff",
            }:
                self.estimate_timer.start()
            search_dependencies = {
                "r_max", "num_channels", "num_interactions", "num_radial_basis",
                "field_scale", "lr", "batch_size", "force_loss", "force_huber_delta",
                "qeq_smearing",
                "qeq_hardness_min", "qeq_pme_smearing",
                "qeq_pme_lr_wavelength", "qeq_stability_floor",
                "deq_alpha_max", "d4_functional", "spin_cutoff",
                "coupling_iterations", "coupling_tol", "chem_aug_prob",
                "chem_aug_noise_std", "chem_aug_mix_max", "auto_level",
                "auto_trials", "auto_trial_epochs", "auto_subset",
            }
            if key in search_dependencies or key.startswith("w_"):
                self._refresh_tooltips()
                self._refresh_search_table()
            if key == "force_loss":
                row = self.field_rows.get("force_huber_delta")
                if row is not None:
                    enabled = str(self.value("force_loss")).lower() == "huber"
                    row.setEnabled(enabled)
                    if enabled:
                        self._control_disabled_reasons.pop("force_huber_delta", None)
                    else:
                        self._control_disabled_reasons["force_huber_delta"] = (
                            "Huber delta is used only when Force loss is huber."
                        )
                self._refresh_tooltips()
            if key == "live_plot":
                self._render_live_dashboard()
        except (TypeError, ValueError, OverflowError, ArithmeticError) as exc:
            # TextChanged emits expected intermediate values such as "" and
            # "1e". Keep the editor responsive; action handlers remain strict.
            self._append_log(
                f"[{self.backend._now()}] Waiting for a valid {key} value: {exc}"
            )

    def _numeric_validation_errors(
        self, keys: Optional[Iterable[str]] = None
    ) -> Dict[str, str]:
        selected = set(GUI_NUMERIC_RULES if keys is None else keys)
        errors: Dict[str, str] = {}
        for name in GUI_NUMERIC_RULES:
            if name not in selected or name not in self.controls:
                continue
            control = self.controls[name]
            # Disabled architecture-dependent values cannot affect the run.
            if not control.isEnabled():
                continue
            try:
                _parse_gui_numeric_value(name, self.value(name))
            except (TypeError, ValueError, OverflowError) as exc:
                errors[name] = str(exc)

        # This dependency is clearer as a field-level validation than as the
        # silent clamp retained solely for old imported configurations.
        if not ({"r_max", "spin_cutoff"} & set(errors)):
            try:
                if bool(self.value("enable_spin")):
                    local_cutoff = float(self.value("r_max"))
                    magnetic_cutoff = float(self.value("spin_cutoff"))
                    if magnetic_cutoff > local_cutoff:
                        errors["spin_cutoff"] = (
                            f"must be <= r_max ({local_cutoff:g})"
                        )
            except (KeyError, TypeError, ValueError, OverflowError):
                pass
        return errors

    def _update_numeric_control_state(self, key: str) -> None:
        control = self.controls.get(key)
        if key not in GUI_NUMERIC_RULES or not isinstance(
            control, QtWidgets.QLineEdit
        ):
            return
        invalid = False
        if control.text().strip():
            try:
                _parse_gui_numeric_value(key, control.text())
            except (TypeError, ValueError, OverflowError):
                invalid = True
        control.setProperty("invalidInput", invalid)
        control.style().unpolish(control)
        control.style().polish(control)

    def _validate_numeric_preflight(self, action: str) -> bool:
        errors = self._numeric_validation_errors()
        for name in GUI_NUMERIC_RULES:
            self._update_numeric_control_state(name)
        if not errors:
            return True
        first = next(iter(errors))
        control = self.controls.get(first)
        if control is not None:
            control.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)
        details = "\n".join(
            f"- {PARAMETER_INFO.get(name).title if name in PARAMETER_INFO else name}: {message}"
            for name, message in errors.items()
        )
        QtWidgets.QMessageBox.critical(
            self,
            f"{action} configuration",
            "Correct the following numeric fields before continuing:\n\n" + details,
        )
        return False

    def _architecture_changed(self, key: str) -> None:
        if self._signal_guard:
            return
        if key == "enable_pme" and bool(self.value(key)):
            self.set_value("enable_qeq", True)
        if key in {"e3mu_use_l3", "enable_film"} and bool(self.value(key)):
            self.set_value("e3mu_use_parity", True)
        if key == "enable_dmi" and bool(self.value(key)):
            self.set_value("enable_spin", True)
            self.set_value("e3mu_use_parity", True)
        if key == "enable_spin" and not bool(self.value(key)):
            self.set_value("enable_dmi", False)
        self._invalidate_auto_result("Architecture selection changed")
        self._refresh_architecture_state()
        self._refresh_tooltips()
        self._refresh_search_table()
        self.estimate_timer.start()

    def _dataset_selection_changed(self, _key: str) -> None:
        if self._signal_guard:
            return
        self._dataset_revision += 1
        self._invalidate_auto_result("Dataset selection changed")
        self.dataset_summary.setText("Scanning selected dataset metadata...")
        self.dataset_timer.start()

    def _architecture_values(self) -> Dict[str, Any]:
        values = self.current_values()
        for key in self.backend.ARCHITECTURE_SWITCH_PARAMETERS:
            values[key] = bool(values.get(key, False))
        return values

    def _refresh_architecture_state(self) -> None:
        values = self._architecture_values()
        availability = self.backend.architecture_switch_availability(self._capability)
        self._architecture_disabled_reasons.clear()
        for key, tile in self.architecture_tiles.items():
            allowed, reason = availability.get(key, (True, "Supported"))
            if key == "enable_dmi" and not bool(values.get("enable_spin")):
                allowed, reason = False, "DMI is part of the spin Hamiltonian and requires Spin."
            if key == "enable_film":
                active_domain = any(
                    bool(values.get(name))
                    for name in (
                        "enable_qeq", "enable_pme", "enable_deq", "enable_d4", "enable_spin"
                    )
                )
                if not active_domain:
                    allowed, reason = False, "FiLM requires an active electric or spin domain."
            tile.setEnabled(allowed)
            if not allowed:
                if tile.isChecked():
                    self.set_value(key, False)
                    values[key] = False
                self._architecture_disabled_reasons[key] = reason
                tile.set_status("unavailable")
            else:
                tile.set_status("enabled" if tile.isChecked() else "available")

        # Hard physical dependencies remain selected and locked.
        forced: Dict[str, str] = {}
        if bool(values.get("enable_pme")):
            self.set_value("enable_qeq", True)
            forced["enable_qeq"] = "PME solves long-range electrostatics inside QEq."
        if bool(values.get("e3mu_use_l3")) or bool(values.get("enable_film")):
            self.set_value("e3mu_use_parity", True)
            forced["e3mu_use_parity"] = "L=3 and FiLM require parity-aware O(3)."
        if bool(values.get("enable_spin")) and bool(values.get("enable_dmi")):
            self.set_value("e3mu_use_parity", True)
            forced["e3mu_use_parity"] = "Spin DMI requires polar/axial parity separation."
        for key, reason in forced.items():
            self.architecture_tiles[key].setEnabled(False)
            self._architecture_disabled_reasons[key] = reason
            self.architecture_tiles[key].set_status("required")

        values = self._architecture_values()
        relevance = self.backend.architecture_parameter_relevance(values)
        self._control_disabled_reasons.clear()
        for key, (relevant, reason) in relevance.items():
            row = self.field_rows.get(key)
            if row is None:
                continue
            dataset_ok = True
            dataset_reason = ""
            if key in self.backend.DATASET_LOSS_LABELS:
                dataset_ok, dataset_reason = self.backend.dataset_loss_parameter_availability(
                    self._capability
                ).get(key, (True, "Supported"))
            enabled = bool(relevant and dataset_ok)
            row.setEnabled(enabled)
            if not enabled:
                lock_reason = reason if not relevant else dataset_reason
                self._control_disabled_reasons[key] = lock_reason
                if key.startswith("w_") and key in self.controls:
                    self.set_value(key, "0.0")

        # Dataset labels also lock losses that are architecture-independent.
        loss_availability = self.backend.dataset_loss_parameter_availability(self._capability)
        for key in self.loss_keys:
            if key in relevance:
                continue
            available, reason = loss_availability.get(key, (True, "Supported"))
            row = self.field_rows[key]
            row.setEnabled(available)
            if not available:
                self.set_value(key, "0.0")
                self._control_disabled_reasons[key] = reason

        force_delta_row = self.field_rows.get("force_huber_delta")
        if force_delta_row is not None:
            huber_enabled = str(self.value("force_loss")).lower() == "huber"
            force_delta_row.setEnabled(huber_enabled)
            if huber_enabled:
                self._control_disabled_reasons.pop("force_huber_delta", None)
            else:
                self._control_disabled_reasons["force_huber_delta"] = (
                    "Huber delta is used only when Force loss is huber."
                )

        active = [
            PARAMETER_INFO[key].title
            for key in self.backend.ARCHITECTURE_SWITCH_PARAMETERS
            if bool(values.get(key))
        ]
        locked = [
            PARAMETER_INFO[key].title
            for key in self.backend.ARCHITECTURE_SWITCH_PARAMETERS
            if key in self._architecture_disabled_reasons
        ]
        message = "Active architecture: " + (", ".join(active) if active else "basic L1/L2 backbone") + "."
        if locked:
            message += " Locked by data/dependencies: " + ", ".join(locked) + "."
        self.architecture_summary.setText(message)

    def _tooltip_html(self, key: str) -> str:
        info = PARAMETER_INFO.get(key)
        if info is None:
            return key
        try:
            ranges = self.backend.dynamic_parameter_reference_ranges(
                self.current_values(), self._capability
            )
        except (TypeError, ValueError, OverflowError, ArithmeticError):
            ranges = {}
        reference = ranges.get(key, info.reference)
        reason = self._control_disabled_reasons.get(
            key, self._architecture_disabled_reasons.get(key, "")
        )
        control = self.controls.get(key)
        if isinstance(control, ToggleTile):
            if key in self._architecture_disabled_reasons:
                status = control.status_tag.accessibleName() or "Unavailable"
            else:
                status = "Enabled" if control.isChecked() else "Available"
        else:
            status = "Unavailable" if reason else "Available"
        state_text = (
            f"<br><b style='color:#6C5A9E'>Status:</b> {status}"
            + (f" - {reason}" if reason else "")
        )
        return (
            f"<div style='width:390px; color:#302C3C; background-color:#F4EFFB'>"
            f"<b style='font-size:13px'>{info.title}</b><br>"
            f"<b>Purpose:</b> {info.purpose}<br>"
            f"<b>Physical principle:</b> {info.principle}<br>"
            f"<b>Recommended range:</b> {reference}<br>"
            f"<b>Dependencies:</b> {info.dependency}{state_text}</div>"
        )

    def _refresh_tooltips(self) -> None:
        for key, control in self.controls.items():
            tooltip = self._tooltip_html(key)
            control.setToolTip(tooltip)
            row = self.field_rows.get(key)
            if row is not None:
                row.setToolTip(tooltip)
            if isinstance(control, ToggleTile):
                control.label.setToolTip(tooltip)
                control.switch.setToolTip(tooltip)
                control.status_tag.setToolTip(tooltip)

    def _selected_dataset_paths(self) -> List[str]:
        canonical = str(self.value("dataset")).strip()
        if canonical:
            return [canonical]
        return [
            value
            for value in (
                str(self.value("static_data")).strip(),
                str(self.value("response_data")).strip(),
            )
            if value
        ]

    def _cached_capability(self, path_value: str) -> Dict[str, Any]:
        path = Path(path_value).expanduser().resolve()
        stat = path.stat()
        cache_key = (str(path), int(stat.st_size), int(stat.st_mtime_ns))
        if cache_key not in self._dataset_cache:
            self._dataset_cache[cache_key] = self.backend.inspect_dataset_capabilities(str(path))
        return dict(self._dataset_cache[cache_key])

    def _start_dataset_scan(self) -> None:
        paths = self._selected_dataset_paths()
        self._dataset_generation += 1
        generation = self._dataset_generation
        if not paths:
            self._apply_dataset_result(generation, {"ready": False}, "")
            return

        def scan() -> None:
            try:
                reports = [self._cached_capability(path) for path in paths]
                result = self.backend.merge_dataset_capabilities(reports)
                self.bus.dataset_ready.emit(generation, result, "")
            except Exception as exc:
                self.bus.dataset_ready.emit(
                    generation, {"ready": False}, f"{type(exc).__name__}: {exc}"
                )

        threading.Thread(target=scan, daemon=True).start()

    @QtCore.pyqtSlot(int, object, str)
    def _apply_dataset_result(self, generation: int, capability: object, error: str) -> None:
        if generation != self._dataset_generation:
            return
        self._capability = dict(capability) if isinstance(capability, dict) else {"ready": False}
        if error:
            self.dataset_summary.setText(f"Dataset scan failed: {error}")
        elif not bool(self._capability.get("ready")):
            self.dataset_summary.setText("Select a dataset to inspect its physical capabilities.")
        else:
            labels = sorted(
                name
                for name, count in dict(self._capability.get("labels", {})).items()
                if int(count) > 0
            )
            self.dataset_summary.setText(
                f"Detected {int(self._capability.get('structures', 0)):,} structures / "
                f"{len(self._capability.get('elements', []))} elements / "
                f"{int(self._capability.get('periodic_structures', 0)):,} periodic. "
                f"Labels: {', '.join(labels) if labels else 'none'}."
            )
        self._refresh_architecture_state()
        self._refresh_tooltips()
        self._refresh_search_table()
        self.estimate_timer.start()

    def _model_config(self) -> Any:
        values = self.current_values()
        local_cutoff = float(values["r_max"])
        spin_cutoff = self.backend._compatible_spin_cutoff(
            local_cutoff, values["spin_cutoff"]
        )
        enable_pme = bool(values["enable_pme"])
        use_l3 = bool(values["e3mu_use_l3"])
        enable_film = bool(values["enable_film"])
        enable_spin = bool(values["enable_spin"])
        enable_dmi = bool(values["enable_dmi"])
        use_parity = bool(values["e3mu_use_parity"] or use_l3 or enable_film)
        use_parity = use_parity or (enable_spin and enable_dmi)
        if enable_pme and not self.backend.HAS_TORCHPME:
            raise RuntimeError("PME requires torch-pme.")
        if bool(values["enable_d4"]) and not self.backend.HAS_TAD_DFTD4:
            raise RuntimeError("D4 requires tad-dftd4.")
        max_element = max([int(value) for value in self._capability.get("elements", [])] or [1])
        if bool(values["enable_continuous_chem"]) and int(values["chem_max_z"]) < max_element:
            raise ValueError(f"chem_max_z must cover dataset max Z={max_element}.")
        return self.backend.ModelConfig(
            r_max=local_cutoff,
            num_channels=int(values["num_channels"]),
            num_interactions=int(values["num_interactions"]),
            num_radial_basis=int(values["num_radial_basis"]),
            field_scale=float(values["field_scale"]),
            dtype=str(values["dtype"]),
            e3mu_use_parity=use_parity,
            e3mu_use_l3=use_l3,
            rbf_type=str(values["rbf_type"]),
            enable_continuous_chem=bool(values["enable_continuous_chem"]),
            chem_max_z=int(values["chem_max_z"]),
            chem_aug_prob=float(values["chem_aug_prob"]),
            chem_aug_noise_std=float(values["chem_aug_noise_std"]),
            chem_aug_mix_max=float(values["chem_aug_mix_max"]),
            enable_qeq=bool(values["enable_qeq"] or enable_pme),
            enable_pme=enable_pme,
            enable_deq=bool(values["enable_deq"]),
            enable_d4=bool(values["enable_d4"]),
            enable_spin=enable_spin,
            enable_film=enable_film,
            enable_dmi=enable_dmi,
            qeq_smearing=float(values["qeq_smearing"]),
            qeq_hardness_min=float(values["qeq_hardness_min"]),
            qeq_pme_smearing=float(values["qeq_pme_smearing"]),
            qeq_pme_lr_wavelength=float(values["qeq_pme_lr_wavelength"]),
            qeq_stability_floor=float(values["qeq_stability_floor"]),
            deq_max_iter=int(values["deq_max_iter"]),
            deq_tol=float(values["deq_tol"]),
            deq_damping=float(values["deq_damping"]),
            deq_alpha_max=float(values["deq_alpha_max"]),
            d4_functional=str(values["d4_functional"]),
            spin_cutoff=spin_cutoff,
            coupling_iterations=int(values["coupling_iterations"]),
            coupling_tol=float(values["coupling_tol"]),
        )

    def _start_parameter_estimate(self) -> None:
        if self._training_running:
            return
        self._estimate_generation += 1
        generation = self._estimate_generation
        try:
            cfg = self._model_config()
        except Exception as exc:
            self.model_size_label.setText(f"Model size waiting for valid settings: {exc}")
            return
        elements = list(self._capability.get("elements", [])) or [1]
        self.model_size_label.setText("Model size: estimating current configuration...")

        def estimate() -> None:
            try:
                result = self.backend.estimate_model_parameter_count(cfg, elements)
                self.bus.estimate_ready.emit(generation, result, "")
            except Exception as exc:
                self.bus.estimate_ready.emit(
                    generation, {}, f"{type(exc).__name__}: {exc}"
                )

        threading.Thread(target=estimate, daemon=True).start()

    @QtCore.pyqtSlot(int, object, str)
    def _apply_estimate_result(self, generation: int, counts: object, error: str) -> None:
        if generation != self._estimate_generation:
            return
        if error:
            self.model_size_label.setText(f"Model size unavailable: {error}")
            return
        values = dict(counts)
        total = int(values.get("total", 0))
        self.model_size_label.setText(
            f"Exact parameters: {total:,} ({_human_count(total)}) total / "
            f"{int(values.get('trainable', 0)):,} trainable  |  "
            f"L1 {int(values.get('ground', 0)):,}  |  "
            f"L2 {int(values.get('response', 0)):,}  |  "
            f"L3/physics {int(values.get('physics', 0)):,}  |  "
            f"{int(values.get('elements', 0))} element types"
        )

    def _common_train_kwargs(self) -> Dict[str, Any]:
        values = self.current_values()
        dataset = str(values["dataset"]).strip()
        if dataset and not self.backend._is_hdf5_path(dataset):
            raise ValueError("Canonical dataset must be HDF5 (.h5/.hdf5).")
        return {
            "device": str(values["device"]),
            "cpu_threads": self.backend._parse_cpu_threads(values["cpu_threads"]),
            "dataset": dataset,
            "static_data": str(values["static_data"]).strip(),
            "response_data": str(values["response_data"]).strip(),
            "model": self._model_config(),
            "batch_size": int(values["batch_size"]),
            "val_fraction": float(values["val_fraction"]),
            "seed": int(values["seed"]),
            "w_energy": float(values["w_energy"]),
            "w_forces": float(values["w_forces"]),
            "force_loss": str(values["force_loss"]),
            "force_huber_delta": float(values["force_huber_delta"]),
            "w_dipole": float(values["w_dipole"]),
            "w_polarizability": float(values["w_polarizability"]),
            "w_charges": float(values["w_charges"]),
            "w_atomic_dipoles": float(values["w_atomic_dipoles"]),
            "w_atomic_polarizability": float(values["w_atomic_polarizability"]),
            "w_c6": float(values["w_c6"]),
            "w_bec": float(values["w_bec"]),
            "w_magnetic_moments": float(values["w_magnetic_moments"]),
            "w_effective_field": float(values["w_effective_field"]),
            "w_j": float(values["w_j"]),
            "w_di": float(values["w_di"]),
            "w_dmi": float(values["w_dmi"]),
            "lr_scheduler": str(values["lr_scheduler"]),
            "export_sevennet": bool(values["export_sevennet"]),
            "save_epoch_artifacts": bool(values["save_epoch_artifacts"]),
            "stream_hdf5": bool(values["stream_hdf5"]),
            "cache_neighbor_graphs": bool(values["cache_neighbor_graphs"]),
        }

    def _train_kwargs_for_mode(self, mode: str) -> Dict[str, Any]:
        result = self._common_train_kwargs()
        if mode == "base":
            for key in (
                "w_dipole", "w_polarizability", "w_charges", "w_atomic_dipoles",
                "w_atomic_polarizability", "w_c6", "w_bec", "w_magnetic_moments",
                "w_effective_field", "w_j", "w_di", "w_dmi",
            ):
                result[key] = 0.0
        return result

    def _validate_paths(self, mode: str) -> None:
        dataset = str(self.value("dataset")).strip()
        static = str(self.value("static_data")).strip()
        response = str(self.value("response_data")).strip()
        if dataset:
            if not Path(dataset).expanduser().is_file():
                raise FileNotFoundError(dataset)
            return
        if mode in {"base", "joint"} and not static:
            raise ValueError("Select canonical HDF5 or legacy static data.")
        if mode in {"response", "joint"} and not response:
            raise ValueError("Select canonical HDF5 or legacy response data.")
        for path in (static, response):
            if path and not Path(path).expanduser().is_file():
                raise FileNotFoundError(path)

    def _make_train_config(
        self,
        mode: str,
        *,
        out_ckpt: Optional[str] = None,
        base_ckpt: Optional[str] = None,
        epochs: Optional[int] = None,
        lr: Optional[float] = None,
    ) -> Any:
        values = self.current_values()
        generated = self.backend.TrainConfig(
            mode=mode,
            base_ckpt=str(values["base_ckpt"] if base_ckpt is None else base_ckpt),
            out_ckpt=str(values["out_ckpt"] if out_ckpt is None else out_ckpt),
            epochs=int(values["epochs"] if epochs is None else epochs),
            lr=float(values["lr"] if lr is None else lr),
            **self._train_kwargs_for_mode(mode),
        )
        if not self._imported_train_payload:
            return generated
        # Preserve valid TrainConfig fields that do not currently have a GUI
        # control (for example early stopping and non-finite recovery), while
        # every visible setting remains authoritative.
        imported = self.backend.train_config_from_dict(self._imported_train_payload)
        visible_fields = set(self.backend._GUI_TRAIN_DIRECT_FIELDS) | {
            "mode", "base_ckpt", "out_ckpt", "epochs", "lr",
            "lr_ground", "lr_response", "warmup_freeze_epochs",
            "w_dipole_final", "w_polarizability_final",
        }
        for field_name in self.backend.TrainConfig.__dataclass_fields__:
            if field_name not in visible_fields:
                setattr(generated, field_name, copy.deepcopy(getattr(imported, field_name)))
        visible_model_fields = set(self.controls) & set(
            self.backend.ModelConfig.__dataclass_fields__
        )
        for field_name in self.backend.ModelConfig.__dataclass_fields__:
            if field_name not in visible_model_fields:
                setattr(
                    generated.model,
                    field_name,
                    copy.deepcopy(getattr(imported.model, field_name)),
                )
        return generated

    def _set_running(self, running: bool, label: str = "") -> None:
        self._training_running = bool(running)
        if running:
            self.estimate_timer.stop()
            self._estimate_generation += 1
        for button in self.training_buttons:
            button.setEnabled(not running)
        self.auto_run_button.setEnabled(not running)
        self.auto_apply_button.setEnabled(bool(self._auto_best_params) and not running)
        if label:
            self.header_status.setText(label)
            self.state_value.setText(label)

    def _reset_dashboard(self, checkpoint: str, state: str = "Preparing") -> None:
        self._metric_history.clear()
        self._stage_histories.clear()
        self._stage_artifacts.clear()
        self._stage_latest_artifact_epoch.clear()
        self._stage_info.clear()
        self._stage_order.clear()
        self._active_stage_id = ""
        selector = getattr(self, "analysis_stage_selector", None)
        if selector is not None:
            blocker = QtCore.QSignalBlocker(selector)
            selector.clear()
            selector.addItem("All Stages", "")
            del blocker
        self._artifact_dir = self._artifact_dir_for_checkpoint(checkpoint)
        self.progress_bar.setValue(0)
        self.header_status.setText(state)
        self.header_progress.setText("Preparing data and model")
        self.state_value.setText(state)
        self.epoch_value.setText("Epoch 0 / --")
        self.score_value.setText("Score --")
        if hasattr(self, "analysis_stage_summary"):
            self.analysis_stage_summary.setText("Stage: current run")
        self._render_live_dashboard()

    @staticmethod
    def _stage_progress_callback(
        callback: Callable[[Dict[str, Any]], None],
        *,
        stage_id: str,
        stage_label: str,
        stage_index: int,
        stage_total: int,
        checkpoint: str,
    ) -> Callable[[Dict[str, Any]], None]:
        """Attach immutable workflow-stage identity to every backend event."""
        def emit(payload: Dict[str, Any]) -> None:
            event = dict(payload)
            event.update(
                {
                    "stage_id": str(stage_id),
                    "stage_label": str(stage_label),
                    "stage_index": int(stage_index),
                    "stage_total": int(stage_total),
                    "stage_checkpoint": str(checkpoint),
                }
            )
            callback(event)

        return emit

    def _activate_stage(self, event: Dict[str, Any]) -> str:
        stage_id = str(event.get("stage_id", "")).strip()
        if not stage_id:
            return ""
        if stage_id not in self._stage_order:
            self._stage_order.append(stage_id)
            selector = getattr(self, "analysis_stage_selector", None)
            if selector is not None:
                label = str(event.get("stage_label", stage_id))
                index = int(event.get("stage_index", len(self._stage_order)))
                total = int(event.get("stage_total", len(self._stage_order)))
                blocker = QtCore.QSignalBlocker(selector)
                selector.addItem(f"{index}/{total} {label}", stage_id)
                del blocker
        info = self._stage_info.setdefault(stage_id, {})
        info.update(
            {
                key: event[key]
                for key in (
                    "stage_label", "stage_index", "stage_total", "stage_checkpoint"
                )
                if key in event
            }
        )
        self._stage_histories.setdefault(stage_id, [])
        self._active_stage_id = stage_id
        return stage_id

    def _selected_analysis_stage(self) -> str:
        selector = getattr(self, "analysis_stage_selector", None)
        if selector is None:
            return ""
        return str(selector.currentData() or "")

    def _launch_worker(self, target: Any, state: str) -> None:
        if self._training_running:
            return
        self._stop_event.clear()
        self._set_running(True, state)

        def wrapped() -> None:
            try:
                target()
            except Exception as exc:
                self.bus.log.emit(f"Error: {exc}\n{traceback.format_exc()}")
                self.bus.event.emit(
                    {"type": "run_error", "message": f"{type(exc).__name__}: {exc}"}
                )

        threading.Thread(target=wrapped, daemon=True).start()

    def _start_training(self, mode: str) -> None:
        if self._training_running:
            return
        if not self._validate_numeric_preflight("Training"):
            return
        if mode == "response" and not str(self.value("base_ckpt")).strip():
            answer = QtWidgets.QMessageBox.question(
                self,
                "No Base Checkpoint",
                "No base checkpoint is selected. Run Base -> Response automatically?",
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.Yes,
            )
            if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                self._run_chained()
            return
        try:
            self._validate_paths(mode)
            cfg = self._make_train_config(mode)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Training configuration", str(exc))
            return
        self._reset_dashboard(cfg.out_ckpt)

        def work() -> None:
            progress = self._stage_progress_callback(
                self.bus.event.emit,
                stage_id=f"single-{mode}",
                stage_label=mode.title(),
                stage_index=1,
                stage_total=1,
                checkpoint=cfg.out_ckpt,
            )
            self.backend.train_dual_layer(
                cfg,
                self.bus.log.emit,
                progress,
                self._stop_event.is_set,
            )
            self.bus.event.emit(
                {"type": "run_complete", "stopped": self._stop_event.is_set()}
            )

        self._launch_worker(work, "Training")

    def _run_chained(self) -> None:
        if not self._validate_numeric_preflight("Chained training"):
            return
        try:
            self._validate_paths("joint")
            out_ckpt = str(self.value("out_ckpt"))
            path = Path(out_ckpt)
            base_out = str(path.with_name(path.stem + "_base.pt"))
            base_cfg = self._make_train_config("base", out_ckpt=base_out, base_ckpt="")
            response_cfg = self._make_train_config(
                "response", out_ckpt=out_ckpt, base_ckpt=base_out
            )
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Chained training", str(exc))
            return
        self._reset_dashboard(base_out, "Chained")

        def work() -> None:
            self.bus.log.emit(
                f"[{self.backend._now()}] === Chain 1/2: Base -> {base_out} ==="
            )
            base_progress = self._stage_progress_callback(
                self.bus.event.emit,
                stage_id="chain-base",
                stage_label="Base",
                stage_index=1,
                stage_total=2,
                checkpoint=base_cfg.out_ckpt,
            )
            self.backend.train_dual_layer(
                base_cfg, self.bus.log.emit, base_progress, self._stop_event.is_set
            )
            if self._stop_event.is_set():
                self.bus.event.emit({"type": "run_complete", "stopped": True})
                return
            self.bus.event.emit({"type": "base_checkpoint", "path": base_out})
            self.bus.log.emit(
                f"[{self.backend._now()}] === Chain 2/2: Response -> {out_ckpt} ==="
            )
            response_progress = self._stage_progress_callback(
                self.bus.event.emit,
                stage_id="chain-response",
                stage_label="Response",
                stage_index=2,
                stage_total=2,
                checkpoint=response_cfg.out_ckpt,
            )
            self.backend.train_dual_layer(
                response_cfg,
                self.bus.log.emit,
                response_progress,
                self._stop_event.is_set,
            )
            self.bus.event.emit(
                {"type": "run_complete", "stopped": self._stop_event.is_set()}
            )

        self._launch_worker(work, "Chained")

    def _run_full_chain(self) -> None:
        if not self._validate_numeric_preflight("Full chain"):
            return
        try:
            self._validate_paths("joint")
            values = self.current_values()
            out_ckpt = str(values["out_ckpt"])
            path = Path(out_ckpt)
            base_out = str(path.with_name(path.stem + "_base.pt"))
            response_out = str(path.with_name(path.stem + "_resp.pt"))
            epochs = int(values["epochs"])
            lr = float(values["lr"])
            stages = max(1, int(values["joint_stages"]))
            initial_checkpoint = str(values["base_ckpt"]).strip()
            if initial_checkpoint and not Path(initial_checkpoint).expanduser().is_file():
                raise FileNotFoundError(initial_checkpoint)
            base_cfg = self._make_train_config(
                "base", out_ckpt=base_out, base_ckpt=initial_checkpoint,
                epochs=epochs, lr=lr
            )
            response_cfg = self._make_train_config(
                "response",
                out_ckpt=response_out,
                base_ckpt=base_out,
                epochs=epochs,
                lr=lr,
            )
            joint_cfgs: List[Any] = []
            previous = response_out
            for index in range(stages):
                stage_lr = lr * (0.2 ** (index + 1))
                stage_epochs = max(2, epochs // (4 * (2**index)))
                last = index == stages - 1
                stage_out = (
                    out_ckpt
                    if last
                    else str(path.with_name(f"{path.stem}_jft{index + 1}.pt"))
                )
                cfg = self._make_train_config(
                    "joint",
                    out_ckpt=stage_out,
                    base_ckpt=previous,
                    epochs=stage_epochs,
                    lr=stage_lr,
                )
                cfg.lr_ground = stage_lr * float(values["lr_ground_scale"])
                cfg.lr_response = stage_lr * float(values["lr_response_scale"])
                cfg.lr_scheduler = "cosine"
                cfg.warmup_freeze_epochs = int(values["warmup_epochs"])
                cfg.w_dipole_final = float(values["w_dipole_final"])
                cfg.w_polarizability_final = float(values["w_alpha_final"])
                joint_cfgs.append(cfg)
                previous = stage_out
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Full chain configuration", str(exc))
            return

        self._reset_dashboard(base_out, "Full Chain")
        total = 2 + len(joint_cfgs)

        def work() -> None:
            configs = [base_cfg, response_cfg, *joint_cfgs]
            for index, cfg in enumerate(configs, start=1):
                if self._stop_event.is_set():
                    self.bus.event.emit({"type": "run_complete", "stopped": True})
                    return
                self.bus.log.emit(
                    f"[{self.backend._now()}] === Full Chain {index}/{total}: "
                    f"{cfg.mode}"
                    + (
                        f" (pretrained={initial_checkpoint})"
                        if index == 1 and initial_checkpoint else ""
                    )
                    + f" -> {cfg.out_ckpt} ==="
                )
                stage_label = (
                    "Base" if index == 1
                    else "Response" if index == 2
                    else f"Joint FT {index - 2}"
                )
                stage_progress = self._stage_progress_callback(
                    self.bus.event.emit,
                    stage_id=f"full-chain-{index:02d}-{cfg.mode}",
                    stage_label=stage_label,
                    stage_index=index,
                    stage_total=total,
                    checkpoint=cfg.out_ckpt,
                )
                self.backend.train_dual_layer(
                    cfg,
                    self.bus.log.emit,
                    stage_progress,
                    self._stop_event.is_set,
                )
                if index == 1:
                    self.bus.event.emit(
                        {"type": "base_checkpoint", "path": base_out}
                    )
            self.bus.event.emit(
                {"type": "run_complete", "stopped": self._stop_event.is_set()}
            )

        self._launch_worker(work, "Full Chain")

    def _stop_current_run(self) -> None:
        if not self._training_running:
            return
        self._stop_event.set()
        self.header_status.setText("Stopping")
        self.state_value.setText("Stopping")

    def _active_search_preview(self) -> Tuple[Optional[Any], List[str], str]:
        try:
            level_text = str(self.value("auto_level"))
            level = int(level_text.split(":", 1)[0])
        except (ValueError, IndexError):
            level = 0
        if level <= 0:
            return None, [], "Select a search level to preview dimensions."
        try:
            base = self._make_train_config(
                "joint" if str(self.value("dataset")).strip() or str(self.value("response_data")).strip() else "base",
                epochs=max(1, int(self.value("auto_trial_epochs"))),
            )
            excluded = self.backend.architecture_locked_search_exclusions(
                base.model, self._capability
            )
            suggested = self.backend.dynamic_architecture_search_space(
                self.current_values(), self._capability
            )
            default_params = list(self.backend.AutoSearchEngine.LEVEL_PARAMS.get(level, []))
            selected_params = (
                list(self._custom_search_specs)
                if self._search_space_customized
                else default_params
            )
            search_overrides = dict(suggested)
            search_overrides.update(self._custom_search_specs)
            auto_cfg = self.backend.AutoSearchConfig(
                level=level,
                n_trials=max(1, int(self.value("auto_trials"))),
                trial_epochs=max(1, int(self.value("auto_trial_epochs"))),
                subset_fraction=float(self.value("auto_subset")) / 100.0,
                excluded_params=tuple(sorted(excluded)),
                lock_selected_architecture=True,
                search_space_overrides=search_overrides,
                search_params=tuple(selected_params),
            )
            tmp_dir = str(self._artifact_dir_for_checkpoint(str(self.value("out_ckpt"))) / "auto_trials")
            engine = self.backend.AutoSearchEngine(base, auto_cfg, tmp_dir)
            return engine, list(engine._params), ""
        except Exception as exc:
            return None, [], str(exc)

    def _refresh_search_table(self) -> None:
        if not hasattr(self, "search_table"):
            return
        selected_rows = {
            self.search_table.item(row, 0).text()
            for row in range(self.search_table.rowCount())
            if self.search_table.item(row, 0) is not None
            and self.search_table.item(row, 0).isSelected()
        }
        _engine, params, error = self._active_search_preview()
        blocker = QtCore.QSignalBlocker(self.search_table)
        self.search_table.setRowCount(len(params) if params else (1 if error else 0))
        if error:
            item = QtWidgets.QTableWidgetItem(error)
            item.setForeground(QtGui.QColor(PALETTE["danger"]))
            self.search_table.setItem(0, 0, item)
            self.search_table.setSpan(0, 0, 1, 6)
            del blocker
            return
        self.search_table.clearSpans()
        for row, parameter in enumerate(params):
            gui_key = AUTOSEARCH_TO_GUI.get(parameter, parameter)
            try:
                current = self.value(gui_key)
            except (KeyError, TypeError):
                current = ""
            sampler, search_domain = self.backend.search_space_spec_to_editor(
                _engine.search_space[parameter]
            )
            cells = (parameter, sampler, search_domain, str(current), "", "Active")
            for column, text in enumerate(cells):
                item = QtWidgets.QTableWidgetItem(text)
                if column not in (1, 2):
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                if column == 5:
                    item.setForeground(QtGui.QColor("#4B806A"))
                item.setData(QtCore.Qt.ItemDataRole.UserRole, gui_key)
                self.search_table.setItem(row, column, item)
            tooltip = self._tooltip_html(gui_key)
            for column in range(6):
                table_item = self.search_table.item(row, column)
                if table_item is not None:
                    table_item.setToolTip(tooltip)
            if parameter in selected_rows:
                self.search_table.selectRow(row)
        del blocker

    @staticmethod
    def _format_search_domain(spec: tuple) -> str:
        kind = str(spec[0])
        if kind == "choice":
            return "{" + ", ".join(str(value) for value in spec[1]) + "}"
        if kind == "bool":
            return "{off, on}"
        if kind in {"uniform", "log_uniform", "zero_log_uniform", "randint"}:
            scale = "log " if kind in {"log_uniform", "zero_log_uniform"} else ""
            return f"{scale}[{_fmt_p(spec[1])}, {_fmt_p(spec[2])}]"
        return str(spec)

    def _sync_search_space_editor(self, *, mark_custom: bool = True) -> None:
        if not hasattr(self, "search_table"):
            return
        parsed: Dict[str, tuple] = {}
        for row in range(self.search_table.rowCount()):
            parameter_item = self.search_table.item(row, 0)
            sampler_item = self.search_table.item(row, 1)
            domain_item = self.search_table.item(row, 2)
            if parameter_item is None or sampler_item is None or domain_item is None:
                continue
            parameter = parameter_item.text().strip()
            if not parameter:
                continue
            parsed[parameter] = self.backend.search_space_spec_from_editor(
                parameter, sampler_item.text(), domain_item.text()
            )
        self._custom_search_specs = parsed
        if mark_custom:
            self._search_space_customized = True

    def _search_space_item_changed(self, item: QtWidgets.QTableWidgetItem) -> None:
        if self._signal_guard or item.column() not in (1, 2):
            return
        try:
            self._sync_search_space_editor()
            item.setBackground(QtGui.QColor("#FFFDFE"))
            item.setToolTip("Editable Auto Research range")
            self._invalidate_auto_result("Search space changed")
        except Exception as exc:
            item.setBackground(QtGui.QColor("#FBE2E7"))
            item.setToolTip(str(exc))

    def _add_search_parameter(self) -> None:
        active = {
            self.search_table.item(row, 0).text()
            for row in range(self.search_table.rowCount())
            if self.search_table.item(row, 0) is not None
        }
        candidates = [
            name for name in self.backend.AutoSearchEngine.SEARCH_SPACE
            if name not in active
        ]
        if not candidates:
            QtWidgets.QMessageBox.information(
                self, "Auto Research", "Every supported parameter is already present."
            )
            return
        parameter, accepted = QtWidgets.QInputDialog.getItem(
            self, "Add Search Parameter", "Parameter", candidates, 0, False
        )
        if not accepted or not parameter:
            return
        try:
            self._sync_search_space_editor()
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Search range", str(exc))
            return
        suggested = self.backend.dynamic_architecture_search_space(
            self.current_values(), self._capability
        )
        self._custom_search_specs[str(parameter)] = self.backend.normalize_search_space_spec(
            str(parameter),
            suggested.get(
                str(parameter), self.backend.AutoSearchEngine.SEARCH_SPACE[str(parameter)]
            ),
        )
        self._search_space_customized = True
        self._refresh_search_table()

    def _remove_search_parameters(self) -> None:
        rows = sorted(
            {index.row() for index in self.search_table.selectedIndexes()}, reverse=True
        )
        if not rows:
            return
        try:
            self._sync_search_space_editor()
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Search range", str(exc))
            return
        for row in rows:
            item = self.search_table.item(row, 0)
            if item is not None:
                self._custom_search_specs.pop(item.text().strip(), None)
        self._search_space_customized = True
        self._refresh_search_table()

    def _reset_search_space_editor(self) -> None:
        self._custom_search_specs.clear()
        self._search_space_customized = False
        self._refresh_search_table()

    def _run_auto_search(self) -> None:
        if self._training_running:
            return
        if not self._validate_numeric_preflight("Auto Research"):
            return
        try:
            self._sync_search_space_editor(
                mark_custom=self._search_space_customized
            )
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Search range", str(exc))
            return
        engine, params, error = self._active_search_preview()
        if engine is None or not params:
            QtWidgets.QMessageBox.information(
                self,
                "Auto Research",
                error or "No active search dimensions. Enable supported losses or physics layers.",
            )
            return
        try:
            self._validate_paths(engine.base_cfg.mode)
            Path(engine.tmp_dir).mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Auto Research", str(exc))
            return
        revision = self._dataset_revision
        architecture_signature = self._architecture_signature()
        self._search_context_revision += 1
        context_revision = self._search_context_revision
        self._invalidate_auto_result("Search in progress")
        self.auto_summary.setText(
            f"Searching {len(params)} active dimensions inside the fixed architecture."
        )
        self._reset_dashboard(str(self.value("out_ckpt")), "Auto Research")

        def work() -> None:
            best_params, best_score = engine.run(
                self.bus.log.emit,
                self.bus.event.emit,
                self._stop_event.is_set,
            )
            if self._stop_event.is_set():
                self.bus.event.emit({"type": "run_complete", "stopped": True})
                return
            applicable = {
                name: best_params[name]
                for name in engine._params
                if name in best_params
            }
            self.bus.event.emit(
                {
                    "type": "auto_complete",
                    "params": applicable,
                    "score": float(best_score),
                    "level": int(engine.auto_cfg.level),
                    "dataset_revision": revision,
                    "architecture_signature": architecture_signature,
                    "context_revision": context_revision,
                }
            )
            self.bus.event.emit(
                {"type": "run_complete", "stopped": self._stop_event.is_set()}
            )

        self._launch_worker(work, "Auto Research")

    def _architecture_signature(self) -> str:
        return json.dumps(
            {
                key: bool(self.value(key))
                for key in self.backend.ARCHITECTURE_SWITCH_PARAMETERS
            },
            sort_keys=True,
        )

    def _invalidate_auto_result(self, reason: str) -> None:
        self._auto_best_params.clear()
        self._auto_best_score = None
        if hasattr(self, "auto_apply_button"):
            self.auto_apply_button.setEnabled(False)
        if hasattr(self, "auto_summary"):
            self.auto_summary.setText(f"{reason}; run Auto Research for compatible values.")

    def _store_auto_result(self, event: Dict[str, Any]) -> None:
        if int(event.get("dataset_revision", -1)) != self._dataset_revision:
            self.auto_summary.setText(
                "Search result discarded because the dataset selection changed."
            )
            return
        if str(event.get("architecture_signature", "")) != self._architecture_signature():
            self.auto_summary.setText(
                "Search result discarded because Architecture Switches changed."
            )
            return
        self._auto_best_params = dict(event.get("params", {}))
        self._auto_best_score = float(event.get("score", float("inf")))
        self._auto_best_level = int(event.get("level", 0))
        self.auto_apply_button.setEnabled(
            bool(self._auto_best_params) and not self._training_running
        )
        self.auto_summary.setText(
            f"Best result ready: normalized score {self._auto_best_score:.6g}; "
            f"{len(self._auto_best_params)} values can be applied."
        )

    def _apply_auto_best(self) -> None:
        if not self._auto_best_params:
            return
        self._signal_guard = True
        try:
            for parameter, value in self._auto_best_params.items():
                key = AUTOSEARCH_TO_GUI.get(parameter)
                if key:
                    self.set_value(key, value)
        finally:
            self._signal_guard = False
        self._enforce_spin_cutoff_bound()
        self.auto_summary.setText(
            f"Applied {len(self._auto_best_params)} best values "
            f"(score {self._auto_best_score:.6g})."
        )
        self._refresh_architecture_state()
        self._refresh_tooltips()
        self._refresh_search_table()
        self.estimate_timer.start()

    @QtCore.pyqtSlot(object)
    def _handle_worker_event(self, payload: object) -> None:
        if not isinstance(payload, dict):
            return
        event = dict(payload)
        kind = str(event.get("type", ""))
        stage_id = self._activate_stage(event)
        stage_prefix = ""
        if stage_id:
            label = str(self._stage_info[stage_id].get("stage_label", stage_id))
            index = int(self._stage_info[stage_id].get("stage_index", 1))
            total = int(self._stage_info[stage_id].get("stage_total", 1))
            stage_prefix = f"{label} ({index}/{total})  "
        if kind == "train":
            fraction = max(0.0, min(1.0, float(event.get("overall_frac", 0.0))))
            self.progress_bar.setValue(int(round(1000.0 * fraction)))
            epoch = int(event.get("epoch", 0))
            epochs = int(event.get("epochs", 0))
            step = int(event.get("step", 0))
            steps = int(event.get("steps", 0))
            eta = self._format_eta(float(event.get("eta_s", float("nan"))))
            text = f"{stage_prefix}Epoch {epoch}/{epochs}  Batch {step}/{steps}  {eta}"
            self.header_progress.setText(text)
            self.epoch_value.setText(f"{stage_prefix}Epoch {epoch} / {epochs}")
        elif kind == "prep":
            task = str(event.get("task", "Preparing"))
            current = event.get("current")
            total = event.get("total")
            text = task
            if current is not None and total is not None:
                text += f"  {int(current)}/{int(total)}"
            self.header_progress.setText(stage_prefix + text)
            self.progress_bar.setValue(
                int(1000.0 * max(0.0, min(1.0, float(event.get("overall_frac", 0.0)))))
            )
        elif kind == "val":
            epoch = int(event.get("epoch", 0))
            epochs = int(event.get("epochs", 0))
            step = int(event.get("step", 0))
            steps = int(event.get("steps", 0))
            self.header_progress.setText(
                f"{stage_prefix}Epoch {epoch}/{epochs}  Validating {step}/{steps}"
            )
        elif kind == "metrics":
            self._consume_metrics(event)
        elif kind == "artifacts":
            artifact = event.get("artifact_dir")
            if artifact:
                self._artifact_dir = Path(str(artifact))
                if stage_id:
                    self._stage_artifacts[stage_id] = self._artifact_dir
                    if bool(event.get("plots_updated", False)):
                        self._stage_latest_artifact_epoch[stage_id] = int(
                            event.get("epoch", 0)
                        )
            self._render_live_dashboard()
        elif kind == "epoch":
            epoch = int(event.get("epoch", 0))
            epochs = max(1, int(event.get("epochs", 1)))
            self.progress_bar.setValue(int(1000 * epoch / epochs))
        elif kind == "auto_search_epoch":
            trial = int(event.get("trial", 0))
            trials = int(event.get("n_trials", 1))
            epoch = int(event.get("epoch", 0))
            epochs = int(event.get("epochs", 1))
            prefix = "Baseline" if trial == 0 else f"Trial {trial}/{trials}"
            self.header_progress.setText(f"Auto Research  {prefix}  Epoch {epoch}/{epochs}")
            self.epoch_value.setText(f"{prefix}: {epoch} / {epochs}")
            self.progress_bar.setValue(int(1000 * epoch / max(1, epochs)))
        elif kind == "auto_search":
            self._consume_search_trial(event)
        elif kind == "auto_complete":
            self._store_auto_result(event)
        elif kind == "base_checkpoint":
            self.set_value("base_ckpt", str(event.get("path", "")))
        elif kind == "run_complete":
            stopped = bool(event.get("stopped", False))
            self._set_running(False, "Stopped" if stopped else "Complete")
            self.header_progress.setText("Stopped by user" if stopped else "Run complete")
            if not stopped:
                self.progress_bar.setValue(1000)
            self._render_live_dashboard()
        elif kind == "run_error":
            self._set_running(False, "Error")
            message = str(event.get("message", "Training failed"))
            self.header_progress.setText(message)
            QtWidgets.QMessageBox.critical(self, "Run error", message)

    def _consume_search_trial(self, event: Dict[str, Any]) -> None:
        trial = int(event.get("trial", 0))
        trials = max(1, int(event.get("n_trials", 1)))
        best_score = float(event.get("best_loss", float("nan")))
        trial_score = float(event.get("trial_loss", float("nan")))
        improved = bool(event.get("improved", False))
        self.progress_bar.setValue(int(1000 * trial / trials))
        self.header_progress.setText(
            f"Auto Research {trial}/{trials}  best={best_score:.4g}  trial={trial_score:.4g}"
        )
        best = dict(event.get("params", {}))
        latest = dict(event.get("trial_params", {}))
        for row in range(self.search_table.rowCount()):
            first = self.search_table.item(row, 0)
            if first is None:
                continue
            parameter = first.text()
            if parameter in best:
                self.search_table.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(self.backend._fmt_p(best[parameter])))
                )
            if parameter in latest:
                self.search_table.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(str(self.backend._fmt_p(latest[parameter])))
                )
                status_text = (
                    "Failed" if not math.isfinite(trial_score)
                    else "Improved" if improved else "Tried"
                )
                status = QtWidgets.QTableWidgetItem(status_text)
                status.setForeground(
                    QtGui.QColor(
                        "#B6536A" if not math.isfinite(trial_score)
                        else "#3F8065" if improved else "#8A7B54"
                    )
                )
                self.search_table.setItem(row, 5, status)

    @staticmethod
    def _format_eta(seconds: float) -> str:
        if not math.isfinite(seconds) or seconds < 0:
            return "ETA ?"
        minutes, second = divmod(int(round(seconds)), 60)
        hour, minute = divmod(minutes, 60)
        return (
            f"ETA {hour}:{minute:02d}:{second:02d}"
            if hour
            else f"ETA {minute:02d}:{second:02d}"
        )

    @QtCore.pyqtSlot(str)
    def _append_log(self, text: str) -> None:
        self.log_view.appendPlainText(str(text))
        scrollbar = self.log_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _consume_metrics(self, event: Dict[str, Any]) -> None:
        metric = dict(event)
        self._metric_history.append(metric)
        stage_id = self._activate_stage(metric)
        if stage_id:
            self._stage_histories.setdefault(stage_id, []).append(metric)
        artifact = event.get("artifact_dir")
        if artifact:
            self._artifact_dir = Path(str(artifact))
            if stage_id:
                self._stage_artifacts[stage_id] = self._artifact_dir
        epoch = int(event.get("epoch", 0))
        epochs = int(event.get("epochs", 0))
        score = float(event.get("validation_score", float("nan")))
        self.header_status.setText("Training")
        self.state_value.setText("Training")
        stage_label = ""
        if stage_id:
            info = self._stage_info[stage_id]
            stage_label = str(info.get("stage_label", stage_id))
            stage_index = int(info.get("stage_index", 1))
            stage_total = int(info.get("stage_total", 1))
            self.epoch_value.setText(
                f"{stage_label} {stage_index}/{stage_total}  Epoch {epoch}/{epochs}"
            )
        else:
            self.epoch_value.setText(f"Epoch {epoch} / {epochs}")
        self.score_value.setText(
            f"Score {score:.4g}" if math.isfinite(score) else "Score --"
        )
        memory = event.get("memory")
        if isinstance(memory, dict):
            self.header_progress.setText(
                (f"{stage_label}  " if stage_label else "")
                + f"Epoch {epoch}/{epochs}  RSS {float(memory.get('rss_mib', 0.0)):.0f} MiB  "
                f"MPS {float(memory.get('mps_driver_mib', 0.0)):.0f} MiB"
                + ("  MEMORY GROWTH WARNING" if event.get("memory_leak_warning") else "")
            )
        self._render_live_dashboard()

    @staticmethod
    def _finite_history(
        history: Sequence[Dict[str, Any]], key: str
    ) -> Tuple[List[int], List[float]]:
        x: List[int] = []
        y: List[float] = []
        for item in history:
            value = item.get(key)
            if value is None or not math.isfinite(float(value)):
                continue
            x.append(int(item.get("epoch", len(x) + 1)))
            y.append(float(value))
        return x, y

    @staticmethod
    def _style_axis(axis: Any, title: str, ylabel: str = "") -> None:
        axis.set_facecolor("#FFFDFE")
        axis.set_title(title, loc="left", fontsize=11, fontweight="bold", color="#302C3C", pad=10)
        axis.set_xlabel("Epoch", color="#797386", fontsize=9)
        if ylabel:
            axis.set_ylabel(ylabel, color="#797386", fontsize=9)
        axis.grid(True, color="#E9E3ED", linewidth=0.8, alpha=0.9)
        axis.tick_params(colors="#797386", labelsize=8)
        for spine in axis.spines.values():
            spine.set_color("#DED7E3")

    def _latest_regression_image(
        self, stage_id: Optional[str] = None
    ) -> Optional[Path]:
        selected_stage = str(stage_id or self._active_stage_id).strip()
        if selected_stage:
            directory = self._stage_artifacts.get(selected_stage)
            if directory is None:
                checkpoint = self._stage_info.get(selected_stage, {}).get(
                    "stage_checkpoint"
                )
                if checkpoint:
                    directory = self._artifact_dir_for_checkpoint(str(checkpoint))
            if directory is None:
                return None
            expected_epoch = self._stage_latest_artifact_epoch.get(selected_stage)
            if expected_epoch is None:
                return None
            if expected_epoch > 0:
                candidate = (
                    directory
                    / "plots"
                    / f"regression_full_epoch_{expected_epoch:04d}.png"
                )
                return candidate if candidate.is_file() else None
            return None
        directory = self._artifact_dir or self._artifact_dir_for_checkpoint(
            str(self.value("out_ckpt"))
        )
        candidates = sorted((directory / "plots").glob("regression_full_epoch_*.png"))
        return candidates[-1] if candidates else None

    def _render_live_dashboard(self) -> None:
        if getattr(self, "figure", None) is None or getattr(self, "canvas", None) is None:
            return
        figure = self.figure
        figure.clear()
        selected_stage = self._selected_analysis_stage()
        history = list(
            self._stage_histories.get(selected_stage, [])
            if selected_stage
            else self._metric_history
        )
        stage_groups = [
            (stage_id, list(self._stage_histories.get(stage_id, [])))
            for stage_id in self._stage_order
            if self._stage_histories.get(stage_id)
            and (not selected_stage or stage_id == selected_stage)
        ]
        if not stage_groups and history:
            stage_groups = [("", history)]
        stage_text = "All stages (independent epoch axes)"
        if selected_stage:
            info = self._stage_info.get(selected_stage, {})
            stage_text = (
                f"Stage {int(info.get('stage_index', 1))}/"
                f"{int(info.get('stage_total', 1))}: "
                f"{info.get('stage_label', selected_stage)}"
            )
        elif self._stage_order:
            labels = [
                str(self._stage_info.get(stage_id, {}).get("stage_label", stage_id))
                for stage_id in self._stage_order
            ]
            stage_text += " - " + " | ".join(labels)
        if hasattr(self, "analysis_stage_summary"):
            self.analysis_stage_summary.setText(stage_text)
        view = str(self.value("live_plot")) if "live_plot" in self.controls else "Regression"
        if not history:
            axis = figure.add_subplot(111)
            axis.set_axis_off()
            axis.text(
                0.5, 0.56, "Live analysis is ready", ha="center", va="center",
                fontsize=17, fontweight="bold", color="#302C3C", transform=axis.transAxes,
            )
            axis.text(
                0.5, 0.45,
                "Start training to stream validation metrics, parity plots, and physics residuals.",
                ha="center", va="center", fontsize=10, color="#797386", transform=axis.transAxes,
            )
            figure.tight_layout(pad=2.0)
            self.canvas.draw_idle()
            return
        if view == "Regression":
            regression_stages = (
                [selected_stage]
                if selected_stage
                else [
                    stage_id
                    for stage_id in self._stage_order
                    if self._stage_histories.get(stage_id)
                ]
            )
            regression_images = [
                (stage_id, self._latest_regression_image(stage_id))
                for stage_id in regression_stages
            ]
            regression_images = [
                (stage_id, path)
                for stage_id, path in regression_images
                if path is not None
            ]
            if regression_images:
                from matplotlib import image as mpl_image
                columns = 2 if len(regression_images) > 1 else 1
                rows = int(math.ceil(len(regression_images) / columns))
                for index, (stage_id, image_path) in enumerate(regression_images):
                    axis = figure.add_subplot(rows, columns, index + 1)
                    axis.imshow(mpl_image.imread(str(image_path)))
                    axis.set_axis_off()
                    info = self._stage_info.get(stage_id, {})
                    label = str(info.get("stage_label", stage_id or "Current run"))
                    epoch = self._stage_latest_artifact_epoch.get(
                        stage_id,
                        int(self._stage_histories.get(stage_id, [{}])[-1].get("epoch", 0)),
                    )
                    axis.set_title(
                        f"{label} - epoch {epoch}", loc="left",
                        fontsize=10, fontweight="bold", color="#302C3C", pad=6,
                    )
            else:
                axis = figure.add_subplot(111)
                axis.set_axis_off()
                axis.text(
                    0.5, 0.54,
                    "Waiting for a current-stage regression image",
                    ha="center", va="center", fontsize=14, fontweight="bold",
                    color="#302C3C", transform=axis.transAxes,
                )
                axis.text(
                    0.5, 0.44,
                    "Stale images already present in the output directory are intentionally ignored.",
                    ha="center", va="center", fontsize=9, color="#797386",
                    transform=axis.transAxes,
                )
        if view == "MAE History":
            left = figure.add_subplot(121)
            right = figure.add_subplot(122)
            colors = ("#4A7FC1", "#D48851", "#4A9478", "#8F7AC8", "#C35F79", "#76869B")
            for index, (stage_id, stage_history) in enumerate(stage_groups):
                info = self._stage_info.get(stage_id, {})
                label = str(info.get("stage_label", stage_id or "Current run"))
                color = colors[index % len(colors)]
                x, y = self._finite_history(stage_history, "train_loss")
                if y:
                    left.plot(x, y, marker="o", markersize=3, linewidth=1.6,
                              linestyle="--", label=f"{label} train", color=color, alpha=0.7)
                x, y = self._finite_history(stage_history, "val_loss")
                if y:
                    left.plot(x, y, marker="o", markersize=3, linewidth=2.0,
                              label=f"{label} val", color=color)
            self._style_axis(left, "Objective by stage", "Loss")
            if left.lines:
                left.legend(frameon=False, fontsize=8)
            metric_styles = (
                ("energy_mae", "E-MAE", "-"),
                ("force_mae", "F-MAE", "--"),
                ("validation_score", "Score", ":"),
            )
            for index, (stage_id, stage_history) in enumerate(stage_groups):
                info = self._stage_info.get(stage_id, {})
                label = str(info.get("stage_label", stage_id or "Current run"))
                color = colors[index % len(colors)]
                for key, metric_label, line_style in metric_styles:
                    x, y = self._finite_history(stage_history, key)
                    if y:
                        right.plot(
                            x, y, marker="o", markersize=3, linewidth=1.8,
                            linestyle=line_style,
                            label=f"{label} {metric_label}", color=color,
                        )
            self._style_axis(right, "Validation metrics by stage", "MAE / score")
            if right.lines:
                right.legend(frameon=False, fontsize=8)
        elif view == "Multi-Task":
            axis = figure.add_subplot(111)
            colors = ("#4A7FC1", "#D48851", "#4A9478", "#8F7AC8", "#C35F79", "#76869B")
            line_index = 0
            for stage_id, stage_history in stage_groups:
                stage_label = str(
                    self._stage_info.get(stage_id, {}).get(
                        "stage_label", stage_id or "Current run"
                    )
                )
                names = sorted({
                    name for item in stage_history
                    for name in item.get("multitask_mae", {})
                })
                for name in names:
                    x, y = [], []
                    for item in stage_history:
                        value = item.get("multitask_mae", {}).get(name)
                        if value is not None and math.isfinite(float(value)):
                            x.append(int(item.get("epoch", len(x) + 1)))
                            y.append(float(value))
                    if y:
                        axis.plot(x, y, marker="o", markersize=3, linewidth=1.6,
                                  label=f"{stage_label}: {name}",
                                  color=colors[line_index % len(colors)])
                        line_index += 1
            self._style_axis(axis, "Multi-task MAE by stage", "MAE")
            if axis.lines:
                axis.legend(frameon=False, fontsize=8, ncol=min(3, max(1, line_index)))
            else:
                axis.text(0.5, 0.5, "No auxiliary targets are active", ha="center", va="center",
                          color="#797386", transform=axis.transAxes)
        elif view == "Physics Residuals":
            axis = figure.add_subplot(111)
            colors = ("#4A9478", "#4A7FC1", "#D48851", "#8F7AC8", "#C35F79")
            line_index = 0
            for stage_id, stage_history in stage_groups:
                stage_label = str(
                    self._stage_info.get(stage_id, {}).get(
                        "stage_label", stage_id or "Current run"
                    )
                )
                names = sorted({
                    name for item in stage_history
                    for name in item.get("physics_residual_max", {})
                })
                for name in names:
                    x, y = [], []
                    for item in stage_history:
                        value = item.get("physics_residual_max", {}).get(name)
                        if value is not None and math.isfinite(float(value)):
                            x.append(int(item.get("epoch", len(x) + 1)))
                            y.append(max(float(value), 1e-16))
                    if y:
                        axis.semilogy(x, y, marker="o", markersize=3, linewidth=1.6,
                                      label=f"{stage_label}: {name}",
                                      color=colors[line_index % len(colors)])
                        line_index += 1
            self._style_axis(axis, "Physics diagnostics by stage", "Validation maximum")
            if axis.lines:
                axis.legend(frameon=False, fontsize=8, ncol=min(3, max(1, line_index)))
            else:
                axis.text(0.5, 0.5, "No iterative physics solver is active", ha="center", va="center",
                          color="#797386", transform=axis.transAxes)
        elif view == "Memory":
            axis = figure.add_subplot(111)
            colors = ("#8F7AC8", "#4A7FC1", "#4A9478", "#D48851", "#C35F79", "#76869B")
            for index, (stage_id, stage_history) in enumerate(stage_groups):
                memory_history = [
                    item for item in stage_history
                    if isinstance(item.get("memory"), dict)
                ]
                if not memory_history:
                    continue
                stage_label = str(
                    self._stage_info.get(stage_id, {}).get(
                        "stage_label", stage_id or "Current run"
                    )
                )
                x_values = [int(item.get("epoch", position + 1)) for position, item in enumerate(memory_history)]
                y_values = [float(item["memory"].get("rss_mib", 0.0)) for item in memory_history]
                axis.plot(x_values, y_values, marker="o", markersize=3,
                          linewidth=1.7, label=f"{stage_label}: RSS",
                          color=colors[index % len(colors)])
            self._style_axis(axis, "Process memory by stage", "MiB")
            if axis.lines:
                axis.legend(frameon=False, fontsize=8)
            else:
                axis.text(
                    0.5, 0.5, "Memory telemetry starts after the first epoch",
                    ha="center", va="center", color="#797386", transform=axis.transAxes,
                )
        figure.tight_layout(pad=1.5)
        self.canvas.draw_idle()

    @staticmethod
    def _artifact_dir_for_checkpoint(checkpoint: str) -> Path:
        path = Path(checkpoint or "model.pt").expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path
        return path.parent / "train" / path.stem

    def _open_artifacts(self) -> None:
        directory = self._artifact_dir or self._artifact_dir_for_checkpoint(
            str(self.value("out_ckpt"))
        )
        directory.mkdir(parents=True, exist_ok=True)
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", str(directory)])
            elif os.name == "nt":
                os.startfile(str(directory))  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", str(directory)])
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Open artifacts", str(exc))

    def _collect_config(self) -> Dict[str, Any]:
        self._enforce_spin_cutoff_bound()
        current = self.current_values()
        generated_train = self.backend._train_payload_from_gui_values(
            current, self._selected_training_mode
        )
        train_payload = self.backend._deep_merge_config(
            self._imported_train_payload, generated_train
        )
        managed = {
            "schema": "e3mu-gui-config-v5",
            "version": 5,
            "gui": "pyqt6",
            "training_mode": self._selected_training_mode,
            "saved_at": self.backend._now(),
            "values": current,
            "train_config": train_payload,
            "auto_research_space": {
                name: list(spec)
                for name, spec in self._custom_search_specs.items()
            } if self._search_space_customized else None,
            "vars": {
                LEGACY_TK_VARIABLES[key]: value
                for key, value in current.items()
                if key in LEGACY_TK_VARIABLES
            },
        }
        return self.backend._deep_merge_config(self._config_passthrough, managed)

    def _apply_config(self, payload: Dict[str, Any]) -> None:
        if not isinstance(payload, dict):
            raise TypeError("Configuration must be a JSON object.")
        values = self.backend._extract_gui_values_from_config(payload)
        if not values and not any(
            isinstance(payload.get(name), dict)
            for name in ("values", "vars", "train_config")
        ):
            raise TypeError(
                "Configuration does not contain recognized GUI or TrainConfig values."
            )
        self._config_passthrough = copy.deepcopy(payload)
        self._imported_train_payload = self.backend._extract_train_config_payload(payload)
        self._last_config_warnings = []
        raw_search_space = payload.get("auto_research_space")
        if raw_search_space is None:
            custom_search_space: Dict[str, tuple] = {}
            search_space_customized = False
        elif not isinstance(raw_search_space, dict):
            raise TypeError("auto_research_space must be an object or null")
        else:
            custom_search_space = {
                str(name): self.backend.normalize_search_space_spec(str(name), spec)
                for name, spec in raw_search_space.items()
            }
            search_space_customized = True
        self._signal_guard = True
        try:
            for key, value in values.items():
                if key in self.controls:
                    try:
                        self.set_value(key, value)
                    except (TypeError, ValueError) as exc:
                        self._last_config_warnings.append(f"{key}: {exc}")
        finally:
            self._signal_guard = False
        self._enforce_spin_cutoff_bound()
        imported_mode = payload.get("training_mode")
        if imported_mode is None:
            imported_mode = self._imported_train_payload.get(
                "mode", self._selected_training_mode
            )
        self._set_selected_training_mode(str(imported_mode))
        self._custom_search_specs = custom_search_space
        self._search_space_customized = search_space_customized
        self._dataset_revision += 1
        self._invalidate_auto_result("Configuration changed")
        self._refresh_architecture_state()
        self._refresh_tooltips()
        self._refresh_search_table()
        self.dataset_timer.start()
        self.estimate_timer.start()
        self._update_thread_policy_label()

    def _import_config(self) -> None:
        path, _filter = QtWidgets.QFileDialog.getOpenFileName(
            self, "Import GUI configuration", str(Path.home()), "JSON (*.json);;All files (*)"
        )
        if not path:
            return
        try:
            self._apply_config(json.loads(Path(path).read_text(encoding="utf-8")))
            self._append_log(f"[{self.backend._now()}] Imported GUI config: {path}")
            if self._last_config_warnings:
                self._append_log(
                    f"[{self.backend._now()}] Config migration warnings: "
                    + "; ".join(self._last_config_warnings)
                )
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Import configuration", str(exc))

    def _export_config(self) -> None:
        path, _filter = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export GUI configuration", "e3mu_gui_config.json", "JSON (*.json)"
        )
        if not path:
            return
        try:
            Path(path).write_text(
                json.dumps(self._collect_config(), indent=2, sort_keys=True),
                encoding="utf-8",
            )
            self._append_log(f"[{self.backend._now()}] Exported GUI config: {path}")
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Export configuration", str(exc))

    def _save_default(self) -> None:
        try:
            self._default_path.write_text(
                json.dumps(self._collect_config(), indent=2, sort_keys=True),
                encoding="utf-8",
            )
            self._append_log(
                f"[{self.backend._now()}] Saved default config: {self._default_path}"
            )
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Save default", str(exc))

    def _load_default(self, *, silent: bool) -> None:
        if not self._default_path.is_file():
            return
        try:
            self._apply_config(
                json.loads(self._default_path.read_text(encoding="utf-8"))
            )
            if not silent:
                self._append_log(
                    f"[{self.backend._now()}] Loaded default config: {self._default_path}"
                )
        except Exception as exc:
            if not silent:
                QtWidgets.QMessageBox.warning(self, "Default configuration", str(exc))

    def _factory_reset(self) -> None:
        result = QtWidgets.QMessageBox.question(
            self,
            "Factory reset",
            "Reset every visible setting to the PyQt6 factory defaults?",
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if result != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        self._apply_config({"values": self._factory_values})
        self._config_passthrough.clear()
        self._imported_train_payload.clear()

    def _browse(self, key: str, mode: str) -> None:
        current = str(self.value(key)).strip()
        start = str(Path(current).expanduser().parent) if current else str(Path.cwd())
        if mode == "save":
            path, _filter = QtWidgets.QFileDialog.getSaveFileName(
                self, "Select output checkpoint", current or "model.pt", "PyTorch (*.pt *.pth);;All files (*)"
            )
        else:
            filters = {
                "dataset": "HDF5 (*.h5 *.hdf5);;All files (*)",
                "data": "Datasets (*.h5 *.hdf5 *.extxyz *.xyz *.gz);;All files (*)",
                "checkpoint": "PyTorch (*.pt *.pth);;All files (*)",
            }
            path, _filter = QtWidgets.QFileDialog.getOpenFileName(
                self, "Select file", start, filters.get(mode, "All files (*)")
            )
        if path:
            self.set_value(key, path)
            if key in {"dataset", "static_data", "response_data"}:
                self._dataset_selection_changed(key)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: N802
        if self._training_running:
            result = QtWidgets.QMessageBox.question(
                self,
                "Training is running",
                "Stop the worker and close the application?",
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No,
            )
            if result != QtWidgets.QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            self._stop_event.set()
        event.accept()


def run_qt_gui(backend: Any, argv: Optional[Sequence[str]] = None) -> int:
    """Create or reuse QApplication and run the modern research studio."""
    if not HAS_PYQT6:
        raise RuntimeError("PyQt6>=6.7,<7 is required for the modern GUI")
    app = QtWidgets.QApplication.instance()
    owns_application = app is None
    if app is None:
        app = QtWidgets.QApplication(list(argv or []))
    app.setApplicationName("E3MU Research Studio")
    app.setOrganizationName("Fona Group")
    app.setStyle("Fusion")
    window = ModernE3MUGui(backend)
    window.show()
    if owns_application:
        return int(app.exec())
    return 0

def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mixed-granularity E(3)-mu GNN training and inference tools."
    )
    subparsers = parser.add_subparsers(dest="command")

    train_parser = subparsers.add_parser(
        "train", help="Train from canonical HDF5 or legacy extXYZ"
    )
    train_parser.add_argument("--config", help="JSON TrainConfig file")
    train_parser.add_argument("--dataset")
    train_parser.add_argument("--static-data")
    train_parser.add_argument("--response-data")
    train_parser.add_argument("--mode", choices=("base", "response", "joint"))
    train_parser.add_argument("--base-ckpt")
    train_parser.add_argument("--out-ckpt")
    train_parser.add_argument("--device")
    train_parser.add_argument(
        "--cpu-threads", help="PyTorch CPU threads: 'auto' or a positive integer"
    )
    train_parser.add_argument("--dtype", choices=("float32", "float64"))
    train_parser.add_argument("--epochs", type=int)
    train_parser.add_argument("--batch-size", type=int)
    train_parser.add_argument("--lr", type=float)
    train_parser.add_argument("--force-loss", choices=("mse", "huber"))
    train_parser.add_argument("--force-huber-delta", type=float)
    train_parser.add_argument("--val-fraction", type=float)
    train_parser.add_argument("--seed", type=int)
    train_parser.add_argument("--r-max", type=float)
    train_parser.add_argument("--channels", type=int)
    train_parser.add_argument("--interactions", type=int)
    train_parser.add_argument("--radial-basis", type=int)
    for name in (
        "energy", "forces", "dipole", "polarizability", "charges",
        "atomic-dipoles", "atomic-polarizability", "c6", "bec",
        "magnetic-moments", "effective-field", "j", "di", "dmi",
    ):
        train_parser.add_argument(f"--w-{name}", type=float)
    for name in ("qeq", "pme", "deq", "d4", "spin", "film", "dmi"):
        train_parser.add_argument(f"--enable-{name}", action="store_true")
    train_parser.add_argument("--enable-all-physics", action="store_true")
    train_parser.add_argument("--no-epoch-artifacts", action="store_true")
    train_parser.add_argument("--no-sevennet", action="store_true")
    train_parser.add_argument(
        "--no-stream-hdf5", action="store_true",
        help="Materialize canonical HDF5 in RAM (debug/compatibility only)",
    )
    train_parser.add_argument(
        "--no-graph-cache", action="store_true",
        help="Build neighbors on demand every epoch instead of using a disk cache",
    )
    train_parser.add_argument("--graph-cache-dir")

    evaluate_parser = subparsers.add_parser(
        "evaluate", help="Evaluate a safe checkpoint"
    )
    evaluate_parser.add_argument("checkpoint")
    evaluate_parser.add_argument("dataset")
    evaluate_parser.add_argument(
        "--split", default="test", choices=("train", "val", "test", "all")
    )
    evaluate_parser.add_argument("--batch-size", type=int, default=4)
    evaluate_parser.add_argument("--device", default="auto")
    evaluate_parser.add_argument("--output")

    self_test_parser = subparsers.add_parser(
        "self-test", help="Run deterministic physics checks"
    )
    self_test_parser.add_argument("--seed", type=int, default=7)
    self_test_parser.add_argument("--output")
    subparsers.add_parser("gui", help="Launch the modern PyQt6 research GUI")
    subparsers.add_parser("gui-tk", help="Launch the legacy Tk training GUI")
    return parser



def _cli_train(args: argparse.Namespace) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    if args.config:
        raw_payload = json.loads(
            Path(args.config).expanduser().read_text(encoding="utf-8")
        )
        payload = _extract_train_config_payload(raw_payload)
    payload.setdefault("mode", "joint")
    direct_names = (
        "dataset", "static_data", "response_data", "mode", "base_ckpt", "out_ckpt",
        "device", "cpu_threads", "epochs", "batch_size", "lr", "force_loss",
        "force_huber_delta", "val_fraction", "seed",
    )
    for name in direct_names:
        value = getattr(args, name, None)
        if value is not None:
            payload[name] = value
    model_payload = dict(payload.get("model", {}))
    model_mapping = {
        "dtype": "dtype",
        "r_max": "r_max",
        "channels": "num_channels",
        "interactions": "num_interactions",
        "radial_basis": "num_radial_basis",
    }
    for argument_name, config_name in model_mapping.items():
        value = getattr(args, argument_name, None)
        if value is not None:
            model_payload[config_name] = value
    for name in ("qeq", "pme", "deq", "d4", "spin", "film", "dmi"):
        if getattr(args, f"enable_{name}"):
            model_payload[f"enable_{name}"] = True
    if args.enable_all_physics:
        for name in ("qeq", "pme", "deq", "d4", "spin", "film", "dmi"):
            model_payload[f"enable_{name}"] = True
    payload["model"] = model_payload
    weight_mapping = {
        "energy": "w_energy",
        "forces": "w_forces",
        "dipole": "w_dipole",
        "polarizability": "w_polarizability",
        "charges": "w_charges",
        "atomic_dipoles": "w_atomic_dipoles",
        "atomic_polarizability": "w_atomic_polarizability",
        "c6": "w_c6",
        "bec": "w_bec",
        "magnetic_moments": "w_magnetic_moments",
        "effective_field": "w_effective_field",
        "j": "w_j",
        "di": "w_di",
        "dmi": "w_dmi",
    }
    for argument_name, config_name in weight_mapping.items():
        value = getattr(args, f"w_{argument_name}", None)
        if value is not None:
            payload[config_name] = value
    if args.no_epoch_artifacts:
        payload["save_epoch_artifacts"] = False
    if args.no_sevennet:
        payload["export_sevennet"] = False
    if args.no_stream_hdf5:
        payload["stream_hdf5"] = False
    if args.no_graph_cache:
        payload["cache_neighbor_graphs"] = False
    if args.graph_cache_dir:
        payload["graph_cache_dir"] = str(args.graph_cache_dir)
    config = train_config_from_dict(payload)
    checkpoint, validation_score = train_dual_layer(config, print)
    return {
        "checkpoint": checkpoint,
        "validation_score": validation_score,
        "config": _checkpoint_safe(asdict(config)),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and (
        arguments[0].startswith("dataset-")
        or arguments[0].startswith("vasp-")
    ):
        # Preserve old command lines without importing offline tooling during
        # normal GUI, training, evaluation, or library use.
        preparation = _load_dataset_preparation_module()
        return preparation.main(arguments)
    if not arguments:
        if HAS_PYQT6:
            return run_qt_gui(sys.modules[__name__])
        if not HAS_TKINTER:
            print(
                "No GUI toolkit is available. Install PyQt6 or Tkinter, or use "
                "the headless 'e3mu' and E3_miu_GNN.py CLI commands.",
                file=sys.stderr,
            )
            return 2
        print(
            "PyQt6 is unavailable; falling back to the legacy Tk GUI. "
            "Install PyQt6>=6.7,<7 for the modern interface.",
            file=sys.stderr,
        )
        App().mainloop()
        return 0
    parser = _build_cli_parser()
    args = parser.parse_args(arguments)
    if args.command == "gui":
        if not HAS_PYQT6:
            parser.error(
                "PyQt6 is required for 'gui'; use 'gui-tk' for the legacy interface"
            )
        return run_qt_gui(sys.modules[__name__])
    if args.command == "gui-tk":
        if not HAS_TKINTER:
            parser.error("Tkinter is required for 'gui-tk'")
        App().mainloop()
        return 0
    if args.command == "train":
        result: Any = _cli_train(args)
    elif args.command == "evaluate":
        result = evaluate_checkpoint(
            args.checkpoint, args.dataset, split=args.split,
            batch_size=args.batch_size, device_name=args.device,
            output_json=args.output,
        )
    elif args.command == "self-test":
        result = run_physics_self_tests(seed=args.seed, output_json=args.output)
    else:
        parser.print_help()
        return 2
    print(json.dumps(_checkpoint_safe(result), indent=2, sort_keys=True))
    if args.command == "self-test" and not bool(result["all_passed"]):
        return 1
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
