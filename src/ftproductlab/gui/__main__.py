"""Run ``python -m ftproductlab.gui``."""

from __future__ import annotations

import platform
import sys


def _main() -> int:
    try:
        from .app import main
    except ImportError as error:
        print(
            "FTProductLab GUI dependencies are unavailable.\n"
            f"Reason: {error}\n"
            f"Python: {platform.python_version()}\n"
            f"Platform: {platform.platform()}\n"
            'Install with: pip install "ftproductlab[gui]"',
            file=sys.stderr,
        )
        return 2
    return main()


if __name__ == "__main__":
    raise SystemExit(_main())
