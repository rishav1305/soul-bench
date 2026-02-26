"""Allow running as python3 -m soul_planner."""

import subprocess
import sys
from pathlib import Path

_PROJECT_DIR = Path(__file__).resolve().parent.parent


def _install_deps():
    """Install package in editable mode when dependencies are missing."""
    print("Dependencies missing -- installing soul-planner...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", f"{_PROJECT_DIR}[dev]",
         "--break-system-packages", "--quiet"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Install failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print("Installed. Restarting...")


try:
    from soul_planner.cli import main
except ImportError:
    _install_deps()
    from soul_planner.cli import main

main()
