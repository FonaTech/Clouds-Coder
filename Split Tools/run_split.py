#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cross-platform launcher for split_coder.py.",
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=None,
        help="Source Python file to split. Defaults to the nearest Clouds_Coder.py.",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Output directory. Defaults to Code_Structure next to the source file.",
    )
    parser.add_argument(
        "--report-name",
        default="FRAMEWORK.md",
        help="Framework markdown report filename.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Forward --update to split_coder.py.",
    )
    parser.add_argument(
        "--show-tree",
        action="store_true",
        help="Forward --show-tree to split_coder.py.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Forward --dry-run to split_coder.py.",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Forward --no-report to split_coder.py.",
    )
    parser.add_argument(
        "--no-self-check",
        action="store_true",
        help="Skip the split_coder.py --self-check phase.",
    )
    parser.add_argument(
        "--dump-layout",
        action="store_true",
        help="Print the detected statement-to-module layout.",
    )
    parser.add_argument(
        "--auto-layout",
        action="store_true",
        help="Use generic architecture heuristics instead of the Clouds_Coder layout.",
    )
    parser.add_argument(
        "--layout-file",
        help="Custom JSON module-to-symbol layout file.",
    )
    return parser


def resolve_path(base_dir: Path, raw: str) -> Path:
    path = Path(str(raw or "").strip()).expanduser()
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    else:
        path = path.resolve()
    return path


def discover_project_dir(launcher_dir: Path) -> Path:
    """Support launchers kept either in the project root or in Split Tools/."""
    for candidate in (launcher_dir, launcher_dir.parent):
        if (candidate / "Clouds_Coder.py").is_file():
            return candidate
    return launcher_dir


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    launcher_dir = Path(__file__).resolve().parent
    split_coder = launcher_dir / "split_coder.py"
    if not split_coder.exists():
        print(f"[run_split] missing split_coder.py: {split_coder}", file=sys.stderr)
        return 2

    project_dir = discover_project_dir(launcher_dir)
    source_path = (
        resolve_path(project_dir, args.source)
        if args.source
        else (project_dir / "Clouds_Coder.py").resolve()
    )
    output_dir = (
        resolve_path(project_dir, args.output_dir)
        if args.output_dir
        else (source_path.parent / "Code_Structure").resolve()
    )
    if not source_path.exists():
        print(f"[run_split] source file not found: {source_path}", file=sys.stderr)
        return 2

    cmd = [
        sys.executable,
        str(split_coder),
        str(source_path),
        "--output-dir",
        str(output_dir),
        "--report-name",
        str(args.report_name),
    ]
    if args.update:
        cmd.append("--update")
    if args.show_tree:
        cmd.append("--show-tree")
    if args.dry_run:
        cmd.append("--dry-run")
    if args.no_report:
        cmd.append("--no-report")
    if args.dump_layout:
        cmd.append("--dump-layout")
    if args.auto_layout:
        cmd.append("--auto-layout")
    if args.layout_file:
        cmd.extend(["--layout-file", str(resolve_path(project_dir, args.layout_file))])
    if not args.no_self_check and not args.dry_run:
        cmd.append("--self-check")

    print("[run_split] launcher =", launcher_dir, flush=True)
    print("[run_split] source   =", source_path, flush=True)
    print("[run_split] output   =", output_dir, flush=True)
    print("[run_split] command  =", " ".join(repr(part) for part in cmd), flush=True)

    completed = subprocess.run(cmd, cwd=str(project_dir))
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
