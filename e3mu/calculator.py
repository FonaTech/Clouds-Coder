"""ASE coupling for native E3-miu-GNN checkpoints."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Tuple, Union

import numpy as np
import torch
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
from torch_geometric.data import Batch as TGBatch

from ._backend import get_backend


MODEL_MODES = ("auto", "full_coupled", "ground_only")
SPIN_POLICIES = ("auto", "off", "required")
RESPONSE_LOSS_KEYS = (
    "w_dipole",
    "w_polarizability",
    "w_charges",
    "w_atomic_dipoles",
    "w_atomic_polarizability",
    "w_c6",
    "w_bec",
    "w_magnetic_moments",
    "w_effective_field",
    "w_j",
    "w_di",
    "w_dmi",
)


def _normalise_choice(value: str, choices: Sequence[str], *, name: str) -> str:
    selected = str(value or "").strip().lower()
    if selected not in choices:
        raise ValueError(f"{name} must be one of: {', '.join(choices)}")
    return selected


def _normalise_field(field: Sequence[float]) -> np.ndarray:
    values = np.asarray(field, dtype=float).reshape(-1)
    if values.size != 3 or not np.isfinite(values).all():
        raise ValueError("electric_field must contain three finite values")
    return values.reshape(3)


def recommended_model_mode(model: torch.nn.Module) -> Tuple[str, str]:
    """Infer the physically trained inference surface recorded by a checkpoint."""
    metadata = getattr(model, "checkpoint_metadata", {})
    if not isinstance(metadata, Mapping):
        metadata = {}

    explicit = str(metadata.get("recommended_inference_mode", "")).strip().lower()
    if explicit in ("full_coupled", "ground_only"):
        return explicit, "checkpoint recommended_inference_mode"

    training_mode = str(metadata.get("training_mode", "")).strip().lower()
    if training_mode == "base":
        return "ground_only", "checkpoint training_mode=base"
    if training_mode in ("response", "joint"):
        return "full_coupled", f"checkpoint training_mode={training_mode}"

    checkpoint_path = str(getattr(model, "checkpoint_path", "") or "")
    stem = Path(checkpoint_path).stem.lower() if checkpoint_path else ""
    if re.search(r"(?:^|[_\-.])base(?:$|[_\-.])", stem):
        return "ground_only", "legacy base-checkpoint filename"

    loss_weights = metadata.get("loss_weights")
    if isinstance(loss_weights, Mapping):
        found_response_weight = False
        active_response_weight = False
        for name in RESPONSE_LOSS_KEYS:
            if name not in loss_weights:
                continue
            found_response_weight = True
            try:
                active_response_weight = active_response_weight or float(loss_weights[name]) > 0.0
            except (TypeError, ValueError):
                continue
        if active_response_weight:
            return "full_coupled", "checkpoint has response supervision"
        if found_response_weight:
            return "ground_only", "legacy checkpoint has no response supervision"

    return "full_coupled", "no stage metadata; preserving complete-model behavior"


def spin_vectors_from_atoms(
    atoms: Atoms,
    *,
    policy: str,
    threshold: float = 1e-10,
) -> Optional[np.ndarray]:
    """Return unit spin directions while preserving explicitly non-magnetic sites."""
    selected = _normalise_choice(policy, SPIN_POLICIES, name="spin_policy")
    if selected == "off":
        return None

    raw: Optional[np.ndarray] = None
    for key in ("e3mu_spins", "spins"):
        if key in atoms.arrays:
            raw = np.asarray(atoms.arrays[key], dtype=float)
            break
    if raw is None and "initial_magmoms" in atoms.arrays:
        raw = np.asarray(atoms.arrays["initial_magmoms"], dtype=float)

    if raw is None or raw.size == 0:
        if selected == "required":
            raise ValueError(
                "spin_policy='required' but the structure has no spin vectors or "
                "ASE initial magnetic moments"
            )
        return None
    if not np.isfinite(raw).all():
        raise ValueError("Structure spin data contains non-finite values")

    atom_count = len(atoms)
    if raw.shape in ((atom_count,), (atom_count, 1)):
        scalar = raw.reshape(atom_count)
        spins = np.zeros((atom_count, 3), dtype=float)
        active = np.abs(scalar) > float(threshold)
        spins[active, 2] = np.sign(scalar[active])
    elif raw.shape == (atom_count, 3):
        norm = np.linalg.norm(raw, axis=1)
        active = norm > float(threshold)
        spins = np.zeros((atom_count, 3), dtype=float)
        spins[active] = raw[active] / norm[active, None]
    else:
        raise ValueError(
            f"Structure spin data has shape {raw.shape}; expected ({atom_count},) "
            f"or ({atom_count}, 3)"
        )

    if not np.any(active):
        if selected == "required":
            raise ValueError("spin_policy='required' but all structure spin moments are zero")
        return None
    return spins


def _tensor_value(value: torch.Tensor) -> Any:
    array = value.detach().cpu().numpy()
    if np.issubdtype(array.dtype, np.floating) and not np.isfinite(array).all():
        raise FloatingPointError("Native model produced a non-finite output")
    if array.ndim == 0:
        return array.item()
    return array


class E3MUCalculator(Calculator):
    """ASE calculator for safe native E3-miu-GNN checkpoint inference.

    Stress is intentionally absent because the current native model does not
    derive virial stress. SevenNet-compatible exports are ground-only and are
    handled separately by the project's exporter.
    """

    implemented_properties = (
        "energy",
        "free_energy",
        "forces",
        "dipole",
        "polarizability",
        "charges",
        "bec",
        "atomic_dipoles",
        "atomic_polarizability",
        "c6",
        "magnetic_moments",
        "effective_field",
    )

    def __init__(
        self,
        model: Union[str, Path, torch.nn.Module],
        *,
        device: str = "auto",
        model_mode: str = "auto",
        total_charge: float = 0.0,
        electric_field: Sequence[float] = (0.0, 0.0, 0.0),
        spin_policy: str = "auto",
        compile_inference: bool = False,
        compute_bec: bool = False,
        allow_unsafe_legacy: bool = False,
        log: Callable[[str], None] = print,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        backend = get_backend()
        if isinstance(model, (str, Path)):
            loaded = backend.DualLayerFieldModel.load(
                str(Path(model).expanduser()),
                map_location="cpu",
                allow_unsafe_legacy=bool(allow_unsafe_legacy),
            )
        else:
            loaded = model

        self.log = log
        self.requested_model_mode = _normalise_choice(
            model_mode, MODEL_MODES, name="model_mode"
        )
        if self.requested_model_mode == "auto":
            self.model_mode, self.model_mode_reason = recommended_model_mode(loaded)
        else:
            self.model_mode = self.requested_model_mode
            self.model_mode_reason = "explicit user selection"
        self.spin_policy = _normalise_choice(
            spin_policy, SPIN_POLICIES, name="spin_policy"
        )
        self.total_charge = float(total_charge)
        if not np.isfinite(self.total_charge):
            raise ValueError("total_charge must be finite")
        self.electric_field = _normalise_field(electric_field)
        self.compute_bec = bool(compute_bec)
        self._is_mixed = isinstance(loaded, backend.MixedGranularityE3GNN)
        if self.spin_policy == "required" and (
            self.model_mode != "full_coupled"
            or not self._is_mixed
            or not bool(getattr(loaded.cfg, "enable_spin", False))
        ):
            raise ValueError(
                "spin_policy='required' needs a full_coupled mixed-granularity "
                "checkpoint with enable_spin=True"
            )

        requested_dtype = str(getattr(getattr(loaded, "cfg", None), "dtype", "float32"))
        self.device, runtime_dtype = backend.resolve_device(device, dtype=requested_dtype)
        backend.set_default_dtype(runtime_dtype)
        self.dtype = torch.get_default_dtype()
        self._source_model = loaded
        self.model = loaded
        z_values = list(getattr(loaded, "z_table_zs", []) or [])
        self._z_to_index = {int(z): index for index, z in enumerate(z_values)}
        if not self._z_to_index:
            raise ValueError("Native checkpoint has an empty atomic-number table")
        self._z_table = backend.AtomicNumberTable(z_values)

        self._compiled = False
        self._compile_user_requested = bool(compile_inference)
        self._compile_requested = self._compile_user_requested
        self._compile_skip_reason = ""
        if self._compile_requested and self.device.type == "mps":
            self._compile_requested = False
            self._compile_skip_reason = (
                "disabled on MPS because torch.compile may abort in the Metal backend"
            )
            self.log(f"WARN: Native inference compile {self._compile_skip_reason}; using eager inference")
        self._warned_missing_spin = False
        self.calculation_count = 0
        self.last_components: Dict[str, float] = {}
        self.last_outputs: Dict[str, Any] = {}

        self.model.to(device=self.device, dtype=self.dtype)
        self.model.eval()
        if self._compile_requested:
            compile_fn = getattr(torch, "compile", None)
            if compile_fn is None:
                self._compile_skip_reason = "torch.compile is unavailable"
                self.log("WARN: torch.compile is unavailable; using eager inference")
            else:
                try:
                    self.model = compile_fn(self.model, dynamic=True, fullgraph=False)
                    self._compiled = True
                except Exception as exc:
                    self.model = self._source_model
                    self._compile_skip_reason = f"setup failed: {type(exc).__name__}: {exc}"
                    self.log(f"WARN: torch.compile setup failed; using eager inference: {exc}")

    def _forward(
        self,
        batch: Any,
        *,
        use_spin: bool,
        compute_forces: bool,
    ) -> Dict[str, torch.Tensor]:
        use_coupled = self.model_mode == "full_coupled"
        kwargs: Dict[str, Any] = {
            "training": False,
            "compute_forces": bool(compute_forces),
            "compute_bec": bool(self.compute_bec),
            "use_response_terms": use_coupled,
            "retain_graph": False,
        }
        if self._is_mixed:
            kwargs["use_domain_terms"] = bool(
                use_coupled
                and (
                    getattr(self._source_model.cfg, "enable_qeq", False)
                    or getattr(self._source_model.cfg, "enable_pme", False)
                )
            )
            kwargs["use_spin_terms"] = bool(use_coupled and use_spin)
        return self.model(batch, **kwargs)

    def summary(self) -> Dict[str, Any]:
        cfg = getattr(self._source_model, "cfg", None)
        metadata = getattr(self._source_model, "checkpoint_metadata", {})
        if not isinstance(metadata, Mapping):
            metadata = {}
        configured = [
            name
            for name in ("qeq", "pme", "deq", "d4", "spin", "film", "dmi")
            if bool(getattr(cfg, f"enable_{name}", False))
        ]
        return {
            "backend": "native_e3mu",
            "model_class": type(self._source_model).__name__,
            "mode": self.model_mode,
            "requested_mode": self.requested_model_mode,
            "mode_reason": self.model_mode_reason,
            "device": self.device.type,
            "dtype": str(self.dtype).replace("torch.", ""),
            "checkpoint_format": str(
                getattr(self._source_model, "checkpoint_format", "in_memory_model")
            ),
            "checkpoint_schema_version": int(
                getattr(self._source_model, "checkpoint_schema_version", 0) or 0
            ),
            "checkpoint_training_mode": str(metadata.get("training_mode", "unknown")),
            "configured_physics": configured,
            "spin_policy": self.spin_policy,
            "total_charge": self.total_charge,
            "electric_field_V_per_A": self.electric_field.tolist(),
            "compile_requested": self._compile_user_requested,
            "compiled": self._compiled,
            "compile_skip_reason": self._compile_skip_reason,
            "force_evaluations": self.calculation_count,
            "last_components_eV": dict(self.last_components),
        }

    def calculate(
        self,
        atoms: Optional[Atoms] = None,
        properties: Sequence[str] = ("energy", "forces"),
        system_changes: Sequence[str] = all_changes,
    ) -> None:
        super().calculate(atoms, properties, system_changes)
        if atoms is None:
            raise ValueError("atoms is None")
        backend = get_backend()

        cell = np.asarray(atoms.get_cell().array, dtype=float)
        pbc = tuple(bool(value) for value in atoms.get_pbc())
        positions = np.asarray(atoms.get_positions(), dtype=float)
        atomic_numbers = np.asarray(atoms.get_atomic_numbers(), dtype=int)
        if atomic_numbers.size == 0:
            raise ValueError("Empty structure")
        if not np.isfinite(positions).all():
            raise ValueError("Structure positions contain NaN or Inf")
        if any(pbc) and (
            not np.isfinite(cell).all() or abs(float(np.linalg.det(cell))) <= 1e-10
        ):
            raise ValueError("Periodic inference requires a finite, non-singular cell")

        missing = sorted({int(z) for z in atomic_numbers if int(z) not in self._z_to_index})
        if missing:
            raise ValueError(f"Structure contains elements not in checkpoint z_table_zs: {missing}")

        spins = spin_vectors_from_atoms(atoms, policy=self.spin_policy)
        use_spin = bool(
            self.model_mode == "full_coupled"
            and self._is_mixed
            and getattr(self._source_model.cfg, "enable_spin", False)
            and spins is not None
        )
        if (
            self.model_mode == "full_coupled"
            and self._is_mixed
            and getattr(self._source_model.cfg, "enable_spin", False)
            and spins is None
            and not self._warned_missing_spin
        ):
            self.log(
                "No magnetic state found; spin energy is disabled while the remaining "
                "coupled physics stays active"
            )
            self._warned_missing_spin = True

        model_properties: Dict[str, Any] = {
            "field": self.electric_field,
            "total_charge": self.total_charge,
        }
        if spins is not None:
            model_properties["spins"] = spins
        configuration = backend.Configuration(
            atomic_numbers=atomic_numbers,
            positions=positions,
            properties=model_properties,
            property_weights={},
            cell=cell,
            pbc=pbc,
        )
        data = backend.AtomicData.from_config(
            configuration,
            z_table=self._z_table,
            cutoff=float(getattr(self._source_model.cfg, "r_max", 5.0)),
        )
        batch = TGBatch.from_data_list([data]).to(self.device)
        # ASE commonly requests energy first and forces immediately afterwards.
        # Cache both from the same conservative Hamiltonian evaluation so a
        # later get_forces() can never observe the model's disabled-force zeros.
        compute_forces = True

        with torch.enable_grad():
            try:
                outputs = self._forward(
                    batch,
                    use_spin=use_spin,
                    compute_forces=compute_forces,
                )
            except Exception:
                if not self._compiled:
                    raise
                self.model = self._source_model
                self._compiled = False
                self._compile_skip_reason = "compiled execution failed; eager retry selected"
                outputs = self._forward(
                    batch,
                    use_spin=use_spin,
                    compute_forces=compute_forces,
                )

        converted: Dict[str, Any] = {}
        for name, value in outputs.items():
            if isinstance(value, torch.Tensor):
                converted[name] = _tensor_value(value)
        energy_value = converted.get("energy")
        if energy_value is None or np.asarray(energy_value).size != 1:
            raise RuntimeError("Native model returned an invalid scalar energy")
        energy = float(np.asarray(energy_value).reshape(-1)[0])
        forces = np.asarray(converted.get("forces", np.zeros_like(positions)), dtype=float)
        if forces.shape != positions.shape:
            raise RuntimeError(
                f"Native model returned forces with shape {forces.shape}; expected {positions.shape}"
            )

        component_keys = (
            "energy_short",
            "energy_qeq",
            "energy_pme",
            "energy_d4",
            "energy_spin",
            "energy_response",
            "qeq_residual",
            "deq_residual",
            "coupling_residual",
        )
        self.last_components = {
            key: float(np.asarray(converted[key]).reshape(-1)[0])
            for key in component_keys
            if key in converted and np.asarray(converted[key]).size
        }
        self.last_outputs = converted
        self.calculation_count += 1

        self.results["energy"] = energy
        self.results["free_energy"] = energy
        self.results["forces"] = forces.copy()
        for name in (
            "dipole",
            "polarizability",
            "charges",
            "bec",
            "atomic_dipoles",
            "atomic_polarizability",
            "c6",
            "magnetic_moments",
            "effective_field",
        ):
            if name not in converted:
                continue
            value = np.asarray(converted[name])
            if name in ("dipole", "polarizability") and value.shape[0:1] == (1,):
                value = value[0]
            self.results[name] = value.copy()


DualLayerPESCalculator = E3MUCalculator


__all__ = [
    "DualLayerPESCalculator",
    "E3MUCalculator",
    "MODEL_MODES",
    "SPIN_POLICIES",
    "recommended_model_mode",
    "spin_vectors_from_atoms",
]
