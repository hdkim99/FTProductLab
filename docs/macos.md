# macOS GUI support

The official GUI is Tkinter/ttk. No Qt binding is declared, imported, or supported.

## Supported configuration

- macOS 13 or newer
- Python 3.10–3.14 for the core and CLI
- Apple Silicon and Intel where the matching Python installation includes Tk 8.6+
- launch command: `python -m ftproductlab.gui`

Local development verification on 2026-08-23 used Apple Silicon, macOS 27.0, Homebrew
Python 3.14.7, Tcl/Tk 9.0.4, and a virtual environment. Homebrew separates Tk from Python;
the missing `_tkinter` root cause was resolved with:

```bash
brew install python-tk@3.14
```

Use the formula matching the selected Python minor version. A Python.org installer commonly
bundles Tk, but its exact Tk version should still be checked.

## Backend policy

- Scientific core and CLI: no Matplotlib or GUI import.
- File figure export: explicit `Agg`, configured only inside the plotting adapter.
- Tk GUI: ttk widgets; no embedded Matplotlib canvas in version 0.1.
- Headless Linux: Xvfb for window workflow tests. This does not replace the macOS job.

The macOS workflow tests a clean wheel installation, core import, CLI, Tk import, window
creation, main analysis/export workflow, close, and process exit on Apple Silicon with
Python 3.10 and 3.14 and Intel with Python 3.13. The `setup-python` Python 3.10 build on
`macos-15-intel` is explicitly unsupported for the GUI: it was observed linking Tk 8.5
build metadata against the runner's Tk 8.6 runtime. This is a toolchain mismatch rather
than an application failure; core and CLI Python 3.10 support remains tested on DGX.
