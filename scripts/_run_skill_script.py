from __future__ import annotations

import runpy
import sys
from pathlib import Path


def run(wrapper_file: str) -> None:
    script = Path(wrapper_file).resolve().parents[1] / "skill" / "scripts" / Path(wrapper_file).name
    sys.path.insert(0, str(script.parent))
    runpy.run_path(str(script), run_name="__main__")
