# Packaging Guide (PyInstaller + Nuitka)

This project provides helper scripts for Windows, Linux, and macOS builds.

Supported packaging modes:

- `onedir` / `standalone` (existing)
- `onefile` (new)

The packaged binary keeps CLI support for:

- `--host` (default `0.0.0.0`)
- `--port` (custom WebUI port)

## Directory Layout

- `packaging/windows/` (`.bat`)
- `packaging/linux/` (`.sh`)
- `packaging/macos/` (`.sh`)

## Build Commands

### Windows (cmd)

Onedir / Standalone:

- PyInstaller: `packaging\windows\build_pyinstaller.bat`
- Nuitka: `packaging\windows\build_nuitka.bat`

Onefile:

- PyInstaller: `packaging\windows\build_pyinstaller_onefile.bat`
- Nuitka: `packaging\windows\build_nuitka_onefile.bat`

### Linux

Onedir / Standalone:

- PyInstaller: `bash packaging/linux/build_pyinstaller.sh`
- Nuitka: `bash packaging/linux/build_nuitka.sh`

Onefile:

- PyInstaller: `bash packaging/linux/build_pyinstaller_onefile.sh`
- Nuitka: `bash packaging/linux/build_nuitka_onefile.sh`

### macOS

Onedir / Standalone:

- PyInstaller: `bash packaging/macos/build_pyinstaller.sh`
- Nuitka: `bash packaging/macos/build_nuitka.sh`

Onefile:

- PyInstaller: `bash packaging/macos/build_pyinstaller_onefile.sh`
- Nuitka: `bash packaging/macos/build_nuitka_onefile.sh`

## Run Packaged Binary

### Windows

Onedir / Standalone:

- PyInstaller: `packaging\windows\run_pyinstaller.bat --port 8080`
- Nuitka: `packaging\windows\run_nuitka.bat --port 8080`

Onefile:

- PyInstaller: `packaging\windows\run_pyinstaller_onefile.bat --port 8080`
- Nuitka: `packaging\windows\run_nuitka_onefile.bat --port 8080`

### Linux

Onedir / Standalone:

- PyInstaller: `bash packaging/linux/run_pyinstaller.sh --port 8080`
- Nuitka: `bash packaging/linux/run_nuitka.sh --port 8080`

Onefile:

- PyInstaller: `bash packaging/linux/run_pyinstaller_onefile.sh --port 8080`
- Nuitka: `bash packaging/linux/run_nuitka_onefile.sh --port 8080`

### macOS

Onedir / Standalone:

- PyInstaller: `bash packaging/macos/run_pyinstaller.sh --port 8080`
- Nuitka: `bash packaging/macos/run_nuitka.sh --port 8080`

Onefile:

- PyInstaller: `bash packaging/macos/run_pyinstaller_onefile.sh --port 8080`
- Nuitka: `bash packaging/macos/run_nuitka_onefile.sh --port 8080`

You can pass host explicitly:

- `... --host 0.0.0.0 --port 9000`

## Direct Manual Commands (without helper scripts)

### PyInstaller

Onedir:

```bash
python3 -m PyInstaller --noconfirm --clean --onedir --name web-session-agent-pyinstaller --distpath dist/pyinstaller --workpath build/pyinstaller --specpath build/pyinstaller Clouds_Coder.py
```

Onefile:

```bash
python3 -m PyInstaller --noconfirm --clean --onefile --name web-session-agent-pyinstaller-onefile --distpath dist/pyinstaller --workpath build/pyinstaller_onefile --specpath build/pyinstaller_onefile Clouds_Coder.py
```

### Nuitka

Standalone:

```bash
python3 -m nuitka --standalone --assume-yes-for-downloads --remove-output --output-dir=dist/nuitka --output-filename=web-session-agent-nuitka Clouds_Coder.py
```

Onefile:

```bash
python3 -m nuitka --onefile --assume-yes-for-downloads --remove-output --output-dir=dist/nuitka --output-filename=web-session-agent-nuitka-onefile Clouds_Coder.py
```

## Expected Output Paths

- PyInstaller onedir:
  - Linux/macOS: `dist/pyinstaller/web-session-agent-pyinstaller/web-session-agent-pyinstaller`
  - Windows: `dist\pyinstaller\web-session-agent-pyinstaller\web-session-agent-pyinstaller.exe`
- PyInstaller onefile:
  - Linux/macOS: `dist/pyinstaller/web-session-agent-pyinstaller-onefile`
  - Windows: `dist\pyinstaller\web-session-agent-pyinstaller-onefile.exe`
- Nuitka standalone:
  - Linux/macOS: `dist/nuitka/Clouds_Coder.dist/web-session-agent-nuitka`
  - Windows: `dist\nuitka\Clouds_Coder.dist\web-session-agent-nuitka.exe`
- Nuitka onefile:
  - Linux/macOS: `dist/nuitka/web-session-agent-nuitka-onefile`
  - Windows: `dist\nuitka\web-session-agent-nuitka-onefile.exe`

## Notes

- Build scripts include a post-build smoke check (`--help`) to verify the packaged executable starts.
- Onefile builds are slower to produce and may have slower cold-start than onedir/standalone.
