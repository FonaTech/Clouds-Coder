"""Read current evolution metadata without restarting or mutating a running server."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from liquid_kernel.control import read_evolution_progress  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_id')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1]/'.clouds_coder_admin/liquid_kernel')
    args = parser.parse_args()
    print(json.dumps(read_evolution_progress(args.root, args.run_id), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
