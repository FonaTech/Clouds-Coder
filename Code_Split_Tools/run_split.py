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
        default="Clouds_Coder.py",
        help="Source Python file to split. Defaults to Clouds_Coder.py next to this launcher.",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="Code_Structure",
        help="Output directory. Defaults to Code_Structure next to this launcher.",
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
    return parser


def resolve_path(base_dir: Path, raw: str) -> Path:
    path = Path(str(raw or "").strip()).expanduser()
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    else:
        path = path.resolve()
    return path


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    launcher_dir = Path(__file__).resolve().parent
    split_coder = launcher_dir / "split_coder.py"
    if not split_coder.exists():
        print(f"[run_split] missing split_coder.py: {split_coder}", file=sys.stderr)
        return 2

    source_path = resolve_path(launcher_dir, args.source)
    output_dir = resolve_path(launcher_dir, args.output_dir)
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
    if not args.no_self_check and not args.dry_run:
        cmd.append("--self-check")

    print("[run_split] launcher =", launcher_dir, flush=True)
    print("[run_split] source   =", source_path, flush=True)
    print("[run_split] output   =", output_dir, flush=True)
    print("[run_split] command  =", " ".join(repr(part) for part in cmd), flush=True)

    completed = subprocess.run(cmd, cwd=str(launcher_dir))
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
