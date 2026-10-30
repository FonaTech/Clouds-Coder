"""Initialize the shipped single-file runtime before collecting kernel tests.

A clean checkout may contain only Clouds_Coder.py; its embedded framework is
restored by the public entrypoint. Kernel-first test imports must not depend on
another test importing that entrypoint later in collection order.
"""
import importlib
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# Respect an entrypoint already loaded by the isolated-release verifier.
importlib.import_module("Clouds_Coder")
