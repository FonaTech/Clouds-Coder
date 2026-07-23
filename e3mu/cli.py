"""Machine-readable command line interface for E3-miu-GNN."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from .api import (
    evaluate,
    execute_task,
    export_sevennet,
    inspect_checkpoint,
    predict_file,
    read_structures,
    relax,
    run_phonon,
    to_jsonable,
    write_json,
)
from .calculator import MODEL_MODES, SPIN_POLICIES


def _properties(value: str) -> Sequence[str]:
    properties = [item.strip() for item in str(value).split(",") if item.strip()]
    if not properties:
        raise argparse.ArgumentTypeError("at least one property is required")
    return properties


def _common_inference(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("checkpoint")
    parser.add_argument("structure")
    parser.add_argument("--index", default="0", help="ASE index expression, for example 0 or :")
    parser.add_argument("--device", default="auto", choices=("auto", "cpu", "mps", "cuda"))
    parser.add_argument("--model-mode", default="auto", choices=MODEL_MODES)
    parser.add_argument("--total-charge", type=float, default=0.0)
    parser.add_argument(
        "--electric-field",
        nargs=3,
        type=float,
        default=(0.0, 0.0, 0.0),
        metavar=("EX", "EY", "EZ"),
    )
    parser.add_argument("--spin-policy", default="auto", choices=SPIN_POLICIES)
    parser.add_argument("--allow-unsafe-legacy", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="e3mu",
        description="Stable Python, ASE, and JSON interfaces for E3-miu-GNN checkpoints.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect checkpoint capabilities")
    inspect_parser.add_argument("checkpoint")
    inspect_parser.add_argument("--allow-unsafe-legacy", action="store_true")
    inspect_parser.add_argument("--output")

    predict_parser = subparsers.add_parser("predict", help="Predict one or more ASE structures")
    _common_inference(predict_parser)
    predict_parser.add_argument("--properties", type=_properties, default=("energy", "forces"))
    predict_parser.add_argument("--compile-inference", action="store_true")
    predict_parser.add_argument("--output")

    relax_parser = subparsers.add_parser("relax", help="Relax one structure at fixed cell")
    _common_inference(relax_parser)
    relax_parser.add_argument("--fmax", type=float, default=0.05)
    relax_parser.add_argument("--steps", type=int, default=200)
    relax_parser.add_argument("--optimizer", choices=("FIRE", "BFGS"), default="FIRE")
    relax_parser.add_argument("--trajectory")
    relax_parser.add_argument("--output-structure")
    relax_parser.add_argument("--output")

    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate a canonical dataset split")
    evaluate_parser.add_argument("checkpoint")
    evaluate_parser.add_argument("dataset")
    evaluate_parser.add_argument("--split", choices=("train", "val", "test", "all"), default="test")
    evaluate_parser.add_argument("--batch-size", type=int, default=4)
    evaluate_parser.add_argument("--device", choices=("auto", "cpu", "mps", "cuda"), default="auto")
    evaluate_parser.add_argument("--output")

    phonon_parser = subparsers.add_parser("phonon", help="Run the Phonopy finite-displacement workflow")
    _common_inference(phonon_parser)
    phonon_parser.add_argument("--supercell", nargs=3, type=int, default=(2, 2, 2))
    phonon_parser.add_argument("--dos-mesh", nargs=3, type=int, default=(10, 10, 10))
    phonon_parser.add_argument("--displacement", type=float, default=0.01)
    phonon_parser.add_argument("--band-npoints", type=int, default=101)
    phonon_parser.add_argument("--no-equilibrium-force-correction", action="store_true")
    phonon_parser.add_argument("--output", required=True)

    export_parser = subparsers.add_parser(
        "export-sevennet", help="Export the ground-only SevenNet TorchScript interface"
    )
    export_parser.add_argument("checkpoint")
    export_parser.add_argument("--model-output")
    export_parser.add_argument("--output")

    task_parser = subparsers.add_parser("run-task", help="Execute an e3mu-task-v1 JSON request")
    task_parser.add_argument("task")
    task_parser.add_argument("--output")
    return parser


def _result(args: argparse.Namespace) -> Dict[str, Any]:
    if args.command == "inspect":
        return inspect_checkpoint(
            args.checkpoint, allow_unsafe_legacy=args.allow_unsafe_legacy
        )
    if args.command == "predict":
        return predict_file(
            args.checkpoint,
            args.structure,
            index=args.index,
            device=args.device,
            model_mode=args.model_mode,
            total_charge=args.total_charge,
            electric_field=args.electric_field,
            spin_policy=args.spin_policy,
            properties=args.properties,
            compile_inference=args.compile_inference,
            allow_unsafe_legacy=args.allow_unsafe_legacy,
        )
    if args.command == "relax":
        structures = read_structures(args.structure, index=args.index)
        if len(structures) != 1:
            raise ValueError("relax requires exactly one structure")
        return relax(
            args.checkpoint,
            structures[0],
            device=args.device,
            model_mode=args.model_mode,
            total_charge=args.total_charge,
            electric_field=args.electric_field,
            spin_policy=args.spin_policy,
            fmax=args.fmax,
            steps=args.steps,
            optimizer=args.optimizer,
            trajectory=args.trajectory,
            output_structure=args.output_structure,
            allow_unsafe_legacy=args.allow_unsafe_legacy,
        )
    if args.command == "evaluate":
        return evaluate(
            args.checkpoint,
            args.dataset,
            split=args.split,
            batch_size=args.batch_size,
            device=args.device,
            output_json=args.output,
        )
    if args.command == "phonon":
        result = run_phonon(
            args.checkpoint,
            args.structure,
            device=args.device,
            model_mode=args.model_mode,
            total_charge=args.total_charge,
            electric_field=args.electric_field,
            spin_policy=args.spin_policy,
            allow_unsafe_legacy_checkpoint=args.allow_unsafe_legacy,
            supercell_matrix=[[args.supercell[0], 0, 0], [0, args.supercell[1], 0], [0, 0, args.supercell[2]]],
            dos_mesh=tuple(args.dos_mesh),
            displacement_amplitude_A=args.displacement,
            band_npoints=args.band_npoints,
            subtract_equilibrium_forces=not args.no_equilibrium_force_correction,
            thermal_temperatures_K=None,
            log=lambda message: print(message, file=sys.stderr),
        )
        write_json(args.output, result, pretty=True)
        return result
    if args.command == "export-sevennet":
        return export_sevennet(args.checkpoint, output=args.model_output)
    if args.command == "run-task":
        task = json.loads(Path(args.task).expanduser().read_text(encoding="utf-8"))
        return execute_task(task)
    raise RuntimeError(f"Unsupported command: {args.command}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        result = _result(args)
        output = getattr(args, "output", None)
        if output and args.command not in ("evaluate", "phonon"):
            write_json(output, result, pretty=True)
        print(
            json.dumps(
                to_jsonable(result),
                indent=2 if args.pretty else None,
                sort_keys=bool(args.pretty),
                allow_nan=False,
            )
        )
        return 0
    except Exception as exc:
        error = {
            "schema": "e3mu-error-v1",
            "ok": False,
            "error": {"type": type(exc).__name__, "message": str(exc)},
        }
        print(json.dumps(error, sort_keys=True, allow_nan=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
