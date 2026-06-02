"""Notebook scaffolder for HW + Capstone notebooks.

Doctrine:
- Each notebook is defined as a list of `Cell` instances.
- A Cell tagged `kind="solution"` has its `code` shown in the
  solution notebook and *replaced* by a TODO stub in the student
  notebook. The TODO stub preserves the function signature lines
  (so subsequent assertion cells still parse) and replaces the body
  with `raise NotImplementedError("TODO(student): ...")`.
- Markdown cells, demo code cells (`kind="demo"`), and assertion-
  gate cells (`kind="gate"`) are identical in both notebooks.

After generation, both notebooks are executed with `nbclient`. The
solution notebook must run cleanly end-to-end; the student notebook
must fail on the first solution cell (we *expect* the
NotImplementedError as proof the gates would fire).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import nbformat as nbf

Kind = Literal["md", "demo", "solution", "gate", "reflect"]


@dataclass
class Cell:
    kind: Kind
    src: str          # for solution cells: the full reference code
    # For solution cells only, the TODO stub used in the student notebook.
    # If None, the scaffolder auto-derives a stub from the first def/class line.
    student_stub: str | None = None


def _todo_stub_from(src: str) -> str:
    """Derive a TODO stub from a solution cell's source.

    Keeps every line up to and including the first `def` / `class`
    line (so the signature still parses for downstream cells) and
    replaces the body with `raise NotImplementedError`. If no
    `def`/`class` is found, returns a `raise NotImplementedError`
    at the top.
    """
    lines = src.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s*(def |class )", line):
            # Collect signature lines (until the colon ends the header).
            sig_end = i
            while sig_end < len(lines) and not lines[sig_end].rstrip().endswith(":"):
                sig_end += 1
            sig = "\n".join(lines[: sig_end + 1])
            return (
                sig
                + '\n    """TODO(student): implement.\n\n'
                + "    See the §Concept and §Distinguish cells above for the\n"
                + "    derivation. The §Gate cell that follows will fail until\n"
                + '    you replace this body."""\n'
                + '    raise NotImplementedError("TODO(student): see §Concept above")\n'
            )
    return (
        '"""TODO(student): replace this cell with your solution."""\n'
        'raise NotImplementedError("TODO(student): see §Concept above")\n'
    )


def build_notebook(cells: list[Cell], *, solution: bool) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    }
    out_cells = []
    for c in cells:
        if c.kind == "md":
            out_cells.append(nbf.v4.new_markdown_cell(c.src))
        elif c.kind == "reflect":
            out_cells.append(nbf.v4.new_code_cell(c.src))
        elif c.kind == "demo":
            out_cells.append(nbf.v4.new_code_cell(c.src))
        elif c.kind == "gate":
            out_cells.append(nbf.v4.new_code_cell(c.src))
        elif c.kind == "solution":
            body = c.src if solution else (c.student_stub or _todo_stub_from(c.src))
            out_cells.append(nbf.v4.new_code_cell(body))
        else:
            raise ValueError(f"unknown cell kind: {c.kind!r}")
    nb.cells = out_cells
    return nb


def write_pair(
    cells: list[Cell],
    out_dir: Path,
    stem: str,
) -> tuple[Path, Path]:
    """Write `<stem>_solution.ipynb` and `<stem>.ipynb` into out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    sol_nb = build_notebook(cells, solution=True)
    stu_nb = build_notebook(cells, solution=False)
    sol_path = out_dir / f"{stem}_solution.ipynb"
    stu_path = out_dir / f"{stem}.ipynb"
    with sol_path.open("w") as f:
        nbf.write(sol_nb, f)
    with stu_path.open("w") as f:
        nbf.write(stu_nb, f)
    return sol_path, stu_path


def execute(notebook_path: Path, timeout: int = 120) -> tuple[bool, str | None]:
    """Run a notebook in place with nbclient. Returns (ok, last_error_repr)."""
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    nb = nbf.read(notebook_path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(notebook_path.parent)}},
    )
    try:
        client.execute()
    except CellExecutionError as e:
        with notebook_path.open("w") as f:
            nbf.write(nb, f)
        return False, str(e).splitlines()[-1]
    with notebook_path.open("w") as f:
        nbf.write(nb, f)
    return True, None


def _setup_cells(notebook_name: str) -> list[Cell]:
    """Standard preamble used by every HW / milestone notebook."""
    return [
        Cell("md",
             "## Setup\n\n"
             "Resolve `onboarding/projects/` on `sys.path`, attach the "
             "reflection log, and import the canonical references "
             "(used only for spot-checks; the student version derives "
             "its own implementations)."),
        Cell("demo",
             "import os, sys\n"
             "from pathlib import Path\n"
             "_here = Path(os.getcwd()).resolve()\n"
             "for _p in [_here, *_here.parents]:\n"
             "    if (_p / 'shared' / '__init__.py').exists() and _p.name == 'projects':\n"
             "        _PROJECTS = _p\n"
             "        break\n"
             "else:\n"
             "    raise RuntimeError('could not locate onboarding/projects/')\n"
             "_REPO = _PROJECTS.parent.parent\n"
             "if str(_REPO) not in sys.path:\n"
             "    sys.path.insert(0, str(_REPO))\n"
             "\n"
             "import numpy as np\n"
             "import matplotlib\n"
             "matplotlib.use('Agg')   # headless for CI\n"
             "import matplotlib.pyplot as plt\n"
             "\n"
             "from onboarding.projects import reflect\n"
             f"reflect.start(notebook={notebook_name!r}, store=_PROJECTS / '.reflection.jsonl')\n"
             f"print(f'[setup] projects root: {{_PROJECTS}}')\n"),
    ]


__all__ = ["Cell", "build_notebook", "write_pair", "execute", "_setup_cells", "_todo_stub_from"]
