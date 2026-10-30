"""Rebuild the standalone entry points' embedded package from local source."""
import argparse
import base64
import io
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sync(entrypoints=None):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name in ('__init__.py', 'control.py', 'models.py', 'agentic.py', 'context.py', 'execution.py', 'README.md'):
            entry = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, (ROOT / 'liquid_kernel' / name).read_bytes())
    encoded = base64.b64encode(stream.getvalue()).decode('ascii')
    assignment = '_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64 = (\n' + ''.join(
        '    "' + encoded[i:i + 120] + '"\n' for i in range(0, len(encoded), 120)
    ) + ')'
    for name in entrypoints or ('Clouds_Coder.py',):
        path = ROOT / name
        text, count = re.subn(r'_EMBEDDED_LIQUID_KERNEL_PACKAGE_B64 = \(\n.*?\n\)', lambda _: assignment, path.read_text(encoding='utf-8'), count=1, flags=re.S)
        if count != 1:
            raise RuntimeError(f'embedded package marker missing: {name}')
        path.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('entrypoints', nargs='*', help='Defaults to Clouds_Coder.py; historical snapshots are not overwritten.')
    sync(parser.parse_args().entrypoints)
