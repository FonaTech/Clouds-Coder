"""Shared pytest bootstrap for repository-local imports."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
project_root = str(PROJECT_ROOT)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
