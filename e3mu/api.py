"""Stable Python API for E3-miu-GNN checkpoints and workflows."""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Union

import numpy as np
import torch
from ase import Atoms
from ase.io import read as ase_read
from ase.io import write as ase_write
from ase.optimize import BFGS, FIRE

from ._backend import get_backend
from .calculator import E3MUCalculator, recommended_model_mode


API_SCHEMA_VERSION = "e3mu-api-v1"
MODEL_MANIFEST_SCHEMA = "e3mu-model-manifest-v1"
PREDICTION_SCHEMA = "e3mu-prediction-v1"
TASK_SCHEMA = "e3mu-task-v1"


def to_jsonable(value: Any) -> Any:
    if isinstance(value, torch.Tensor):
        return to_jsonable(value.detach().cpu().numpy())
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _sha256(path: Union[str, Path]) -> str:
    digest = hashlib.sha256()
    with Path(path).expanduser().open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_checkpoint(
    checkpoint: Union[str, Path],
    *,
    allow_unsafe_legacy: bool = False,
) -> torch.nn.Module:
    backend = get_backend()
    return backend.DualLayerFieldModel.load(
        str(Path(checkpoint).expanduser()),
        map_location="cpu",
        allow_unsafe_legacy=bool(allow_unsafe_legacy),
    )


def _model_outputs(model: torch.nn.Module, recommended_mode: str) -> Dict[str, Any]:
    backend = get_backend()
    cfg = getattr(model, "cfg", None)
    mixed = isinstance(model, backend.MixedGranularityE3GNN)
    potential = ["energy", "forces", "dipole", "polarizability", "bec"]
    if mixed:
        potential.extend(
            [
                "charges",
                "atomic_dipoles",
                "atomic_polarizability",
                "c6",
                "Jij",
                "Di",
                "DMIij",
                "magnetic_moments",
                "effective_field",
            ]
        )
    recommended = ["energy", "forces"]
    if recommended_mode == "full_coupled":
        recommended.extend(["dipole", "polarizability", "bec"])
        if bool(getattr(cfg, "enable_qeq", False) or getattr(cfg, "enable_pme", False)):
            recommended.append("charges")
        if bool(getattr(cfg, "enable_deq", False)):
            recommended.extend(["atomic_dipoles", "atomic_polarizability"])
        if bool(getattr(cfg, "enable_d4", False)):
            recommended.append("c6")
        if bool(getattr(cfg, "enable_spin", False)):
            recommended.extend(["Jij", "Di", "magnetic_moments", "effective_field"])
        if bool(getattr(cfg, "enable_dmi", False)):
            recommended.append("DMIij")
    return {
        "potential": sorted(set(potential)),
        "recommended": sorted(set(recommended)),
        "unsupported": ["stress", "virial"],
    }


def inspect_checkpoint(
    checkpoint: Union[str, Path],
    *,
    allow_unsafe_legacy: bool = False,
) -> Dict[str, Any]:
    path = Path(checkpoint).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    model = load_checkpoint(path, allow_unsafe_legacy=allow_unsafe_legacy)
    mode, reason = recommended_model_mode(model)
    cfg = getattr(model, "cfg", None)
    metadata = getattr(model, "checkpoint_metadata", {})
    if not isinstance(metadata, Mapping):
        metadata = {}
    configured_physics = [
        name
        for name in ("qeq", "pme", "deq", "d4", "spin", "film", "dmi")
        if bool(getattr(cfg, f"enable_{name}", False))
    ]
    elements = [int(value) for value in getattr(model, "z_table_zs", [])]
    try:
        from ase.data import chemical_symbols

        symbols = [chemical_symbols[value] for value in elements]
    except Exception:
        symbols = [str(value) for value in elements]
    parameter_count = sum(int(parameter.numel()) for parameter in model.parameters())
    trainable_parameter_count = sum(
        int(parameter.numel()) for parameter in model.parameters() if parameter.requires_grad
    )
    limitations = [
        "Native checkpoints do not currently provide virial stress.",
        "SevenNet TorchScript export contains Layer-1 ground energy and forces only.",
    ]
    if mode == "ground_only":
        limitations.append(
            "The checkpoint metadata recommends ground_only inference; response and spin heads "
            "must not be treated as validated predictions."
        )
    public_metadata_keys = (
        "training_mode",
        "recommended_inference_mode",
        "best_epoch",
        "best_val_loss",
        "validation_score",
        "split",
        "loss_weights",
    )
    public_metadata = {
        key: metadata[key] for key in public_metadata_keys if key in metadata
    }
    return {
        "schema": MODEL_MANIFEST_SCHEMA,
        "ok": True,
        "checkpoint": {
            "path": str(path),
            "sha256": _sha256(path),
            "bytes": int(path.stat().st_size),
            "format": str(getattr(model, "checkpoint_format", "unknown")),
            "schema_version": int(getattr(model, "checkpoint_schema_version", 0) or 0),
        },
        "model": {
            "class": type(model).__name__,
            "config": to_jsonable(asdict(cfg)) if cfg is not None else {},
            "parameter_count": parameter_count,
            "trainable_parameter_count": trainable_parameter_count,
            "elements": elements,
            "chemical_symbols": symbols,
            "cutoff_A": float(getattr(cfg, "r_max", 0.0) or 0.0),
            "dtype": str(getattr(cfg, "dtype", "float32")),
            "configured_physics": configured_physics,
        },
        "inference": {
            "recommended_mode": mode,
            "reason": reason,
            "outputs": _model_outputs(model, mode),
            "limitations": limitations,
        },
        "training_metadata": to_jsonable(public_metadata),
    }


def create_calculator(
    checkpoint_or_model: Union[str, Path, torch.nn.Module],
    **kwargs: Any,
) -> E3MUCalculator:
    return E3MUCalculator(checkpoint_or_model, **kwargs)


def read_structures(path: Union[str, Path], *, index: str = "0") -> List[Atoms]:
    value = ase_read(str(Path(path).expanduser()), index=index)
    if isinstance(value, Atoms):
        return [value]
    return list(value)


def structure_record(atoms: Atoms) -> Dict[str, Any]:
    return {
        "formula": atoms.get_chemical_formula(),
        "atom_count": len(atoms),
        "atomic_numbers": atoms.get_atomic_numbers().astype(int).tolist(),
        "positions_A": np.asarray(atoms.get_positions(), dtype=float).tolist(),
        "cell_A": np.asarray(atoms.get_cell().array, dtype=float).tolist(),
        "pbc": [bool(value) for value in atoms.get_pbc()],
    }


def predict(
    checkpoint_or_model: Union[str, Path, torch.nn.Module],
    atoms: Atoms,
    *,
    device: str = "auto",
    model_mode: str = "auto",
    total_charge: float = 0.0,
    electric_field: Sequence[float] = (0.0, 0.0, 0.0),
    spin_policy: str = "auto",
    properties: Optional[Sequence[str]] = None,
    compile_inference: bool = False,
    allow_unsafe_legacy: bool = False,
    log: Callable[[str], None] = lambda _message: None,
) -> Dict[str, Any]:
    requested = list(properties or ("energy", "forces"))
    forbidden = sorted(set(requested) & {"stress", "virial"})
    if forbidden:
        raise NotImplementedError(
            "The native checkpoint does not provide conservative virial stress: "
            + ", ".join(forbidden)
        )
    calculator = create_calculator(
        checkpoint_or_model,
        device=device,
        model_mode=model_mode,
        total_charge=total_charge,
        electric_field=electric_field,
        spin_policy=spin_policy,
        compile_inference=compile_inference,
        compute_bec="bec" in requested,
        allow_unsafe_legacy=allow_unsafe_legacy,
        log=log,
    )
    structure = atoms.copy()
    calculator.calculate(structure, properties=requested)
    missing = [name for name in requested if name not in calculator.results and name not in calculator.last_outputs]
    if missing:
        raise KeyError(f"Requested outputs are unavailable: {', '.join(missing)}")
    selected: Dict[str, Any] = {}
    for name in requested:
        if name in calculator.results:
            selected[name] = calculator.results[name]
        else:
            selected[name] = calculator.last_outputs[name]
    return {
        "schema": PREDICTION_SCHEMA,
        "ok": True,
        "model": calculator.summary(),
        "structure": structure_record(structure),
        "units": {
            "energy": "eV",
            "forces": "eV/Angstrom",
            "dipole": "e*Angstrom",
            "polarizability": str(
                getattr(calculator._source_model.cfg, "polarizability_unit", "angstrom3")
            ),
            "electric_field": "V/Angstrom",
        },
        "results": to_jsonable(selected),
        "components": to_jsonable(calculator.last_components),
    }


def predict_file(
    checkpoint: Union[str, Path],
    structure_path: Union[str, Path],
    *,
    index: str = "0",
    **kwargs: Any,
) -> Dict[str, Any]:
    structures = read_structures(structure_path, index=index)
    results = [predict(checkpoint, atoms, **kwargs) for atoms in structures]
    if len(results) == 1:
        return results[0]
    return {
        "schema": "e3mu-prediction-batch-v1",
        "ok": True,
        "count": len(results),
        "predictions": results,
    }


def relax(
    checkpoint_or_model: Union[str, Path, torch.nn.Module],
    atoms: Atoms,
    *,
    device: str = "auto",
    model_mode: str = "auto",
    total_charge: float = 0.0,
    electric_field: Sequence[float] = (0.0, 0.0, 0.0),
    spin_policy: str = "auto",
    fmax: float = 0.05,
    steps: int = 200,
    optimizer: str = "FIRE",
    trajectory: Optional[Union[str, Path]] = None,
    output_structure: Optional[Union[str, Path]] = None,
    allow_unsafe_legacy: bool = False,
    log: Callable[[str], None] = lambda _message: None,
) -> Dict[str, Any]:
    if not np.isfinite(float(fmax)) or float(fmax) <= 0.0:
        raise ValueError("fmax must be finite and greater than zero")
    if int(steps) <= 0:
        raise ValueError("steps must be greater than zero")
    structure = atoms.copy()
    initial = structure_record(structure)
    calculator = create_calculator(
        checkpoint_or_model,
        device=device,
        model_mode=model_mode,
        total_charge=total_charge,
        electric_field=electric_field,
        spin_policy=spin_policy,
        allow_unsafe_legacy=allow_unsafe_legacy,
        log=log,
    )
    structure.calc = calculator
    optimizer_name = str(optimizer).strip().upper()
    optimizer_class = {"FIRE": FIRE, "BFGS": BFGS}.get(optimizer_name)
    if optimizer_class is None:
        raise ValueError("optimizer must be FIRE or BFGS")
    trajectory_path = str(Path(trajectory).expanduser()) if trajectory else None
    runner = optimizer_class(structure, trajectory=trajectory_path, logfile=None)
    converged = bool(runner.run(fmax=float(fmax), steps=int(steps)))
    energy = float(structure.get_potential_energy())
    forces = np.asarray(structure.get_forces(), dtype=float)
    max_force = float(np.max(np.linalg.norm(forces, axis=1))) if len(forces) else 0.0
    if output_structure:
        ase_write(str(Path(output_structure).expanduser()), structure)
    return {
        "schema": "e3mu-relaxation-v1",
        "ok": True,
        "converged": converged,
        "optimizer": optimizer_name,
        "steps": int(runner.nsteps),
        "fmax_target_eV_per_A": float(fmax),
        "max_force_eV_per_A": max_force,
        "energy_eV": energy,
        "model": calculator.summary(),
        "initial_structure": initial,
        "final_structure": structure_record(structure),
        "forces_eV_per_A": forces.tolist(),
        "trajectory": trajectory_path,
        "output_structure": str(Path(output_structure).expanduser()) if output_structure else None,
    }


def evaluate(
    checkpoint: Union[str, Path],
    dataset: Union[str, Path],
    *,
    split: str = "test",
    batch_size: int = 4,
    device: str = "auto",
    output_json: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    backend = get_backend()
    return to_jsonable(
        backend.evaluate_checkpoint(
            str(Path(checkpoint).expanduser()),
            str(Path(dataset).expanduser()),
            split=split,
            batch_size=int(batch_size),
            device_name=device,
            output_json=str(Path(output_json).expanduser()) if output_json else None,
        )
    )


def run_phonon(
    checkpoint: Union[str, Path],
    structure: Union[str, Path],
    **kwargs: Any,
) -> Dict[str, Any]:
    from Verify_Program_Phonon import compute_phonon_thermo_phonopy

    return to_jsonable(
        compute_phonon_thermo_phonopy(
            model_ckpt=str(Path(checkpoint).expanduser()),
            structure_path=str(Path(structure).expanduser()),
            **kwargs,
        )
    )


def export_sevennet(
    checkpoint: Union[str, Path],
    *,
    output: Optional[Union[str, Path]] = None,
    log: Callable[[str], None] = lambda _message: None,
) -> Dict[str, Any]:
    path = Path(checkpoint).expanduser().resolve()
    manifest = inspect_checkpoint(path)
    backend = get_backend()
    backend.export_sevennet_torchscript(str(path), log)
    generated = path.with_name(f"{path.stem}_compat_sevennet.pt")
    target = Path(output).expanduser().resolve() if output else generated
    if target != generated:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(generated, target)
    return {
        "schema": "e3mu-sevennet-export-v1",
        "ok": True,
        "source_checkpoint": str(path),
        "output": str(target),
        "sha256": _sha256(target),
        "scope": "ground_only",
        "supported_outputs": ["energy", "forces"],
        "unsupported_outputs": [
            "stress",
            "dipole",
            "polarizability",
            "charges",
            "spin_hamiltonian",
        ],
        "source_manifest": manifest,
    }


def execute_task(task: Mapping[str, Any]) -> Dict[str, Any]:
    if str(task.get("schema", TASK_SCHEMA)) != TASK_SCHEMA:
        raise ValueError(f"task schema must be {TASK_SCHEMA!r}")
    action = str(task.get("action", "")).strip().lower().replace("-", "_")
    options = dict(task.get("options", {})) if isinstance(task.get("options"), Mapping) else {}
    checkpoint = task.get("checkpoint")
    if action == "inspect":
        return inspect_checkpoint(
            checkpoint,
            allow_unsafe_legacy=bool(options.get("allow_unsafe_legacy", False)),
        )
    if action == "predict":
        return predict_file(
            checkpoint,
            task["structure"],
            index=str(options.pop("index", "0")),
            **options,
        )
    if action == "relax":
        structures = read_structures(task["structure"], index=str(options.pop("index", "0")))
        if len(structures) != 1:
            raise ValueError("relax requires exactly one input structure")
        return relax(checkpoint, structures[0], **options)
    if action == "evaluate":
        return evaluate(checkpoint, task["dataset"], **options)
    if action == "phonon":
        return run_phonon(checkpoint, task["structure"], **options)
    if action in ("export_sevennet", "sevennet_export"):
        return export_sevennet(checkpoint, **options)
    raise ValueError(
        "action must be one of: inspect, predict, relax, evaluate, phonon, export_sevennet"
    )


def write_json(path: Union[str, Path], payload: Any, *, pretty: bool = True) -> str:
    destination = Path(path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            to_jsonable(payload),
            indent=2 if pretty else None,
            sort_keys=bool(pretty),
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(destination)
    return str(destination)


__all__ = [
    "API_SCHEMA_VERSION",
    "MODEL_MANIFEST_SCHEMA",
    "PREDICTION_SCHEMA",
    "TASK_SCHEMA",
    "create_calculator",
    "evaluate",
    "execute_task",
    "export_sevennet",
    "inspect_checkpoint",
    "load_checkpoint",
    "predict",
    "predict_file",
    "read_structures",
    "relax",
    "run_phonon",
    "structure_record",
    "to_jsonable",
    "write_json",
]
