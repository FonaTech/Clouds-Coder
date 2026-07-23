"""Lazy access to the single-file E3-miu-GNN implementation."""

from __future__ import annotations

from functools import lru_cache
from types import ModuleType


@lru_cache(maxsize=1)
def get_backend() -> ModuleType:
    try:
        import E3_miu_GNN as backend
    except ImportError:
        import Dual_Layer_Atomic_E3_GNN as backend  # type: ignore[no-redef]
    return backend
