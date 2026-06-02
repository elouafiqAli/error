"""Progressive-reflection helper.

Every HW notebook ends each concept block with a reflection cell.
The student calls `reflect.log(...)` with a one-line claim and a
self-assessed confidence level (HIGH / MEDIUM / LOW). All logs
land in `.reflection.jsonl` next to the notebook; the M5 capstone
notebook calls `reflect.render_capstone()` to assemble a calibrated
report from every notebook's log.

This module intentionally has *no* external dependencies (no
torch, no nbformat for the basic logging path) so that it can be
imported at the top of any notebook without slowing kernel start.
`render_capstone` lazily imports `nbformat` only when called.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

Level = Literal["HIGH", "MEDIUM", "LOW", "UNVERIFIED"]
_VALID_LEVELS: tuple[Level, ...] = ("HIGH", "MEDIUM", "LOW", "UNVERIFIED")

_DEFAULT_STORE = Path(".reflection.jsonl")


@dataclass
class _Entry:
    notebook: str
    concept: str
    claim: str
    level: Level
    timestamp: float


_state: dict = {"notebook": None, "store": _DEFAULT_STORE}


def start(notebook: str, store: str | os.PathLike | None = None) -> None:
    """Bind the current notebook name and reflection store path."""
    _state["notebook"] = notebook
    _state["store"] = Path(store) if store is not None else _DEFAULT_STORE


def log(concept: str, claim: str, level: Level) -> None:
    """Append one calibrated reflection entry to the store."""
    if _state["notebook"] is None:
        raise RuntimeError("reflect.start(notebook=...) must be called first")
    if level not in _VALID_LEVELS:
        raise ValueError(f"level must be one of {_VALID_LEVELS}; got {level!r}")
    entry = _Entry(
        notebook=str(_state["notebook"]),
        concept=concept,
        claim=claim,
        level=level,
        timestamp=time.time(),
    )
    store = Path(_state["store"])
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(entry)) + "\n")


def dump(store: str | os.PathLike | None = None) -> list[dict]:
    """Read all entries from the reflection store."""
    path = Path(store) if store is not None else Path(_state["store"])
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def render_capstone(
    store: str | os.PathLike | None = None,
    target_path: str | os.PathLike = "capstone/m5_calibrated_report.ipynb",
) -> Path:
    """Assemble the M5 calibrated report notebook from all reflections.

    Imports `nbformat` lazily so callers that only need `log` do not
    pay the import cost.
    """
    import nbformat as nbf

    rows = dump(store)
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell(
            "# Milestone 5 — Calibrated capstone report\n"
            "\n"
            "Auto-generated from every notebook's `reflect.log(...)` entries. "
            "Re-run `reflect.render_capstone()` after completing more cells "
            "to regenerate."
        )
    ]
    by_notebook: dict[str, list[dict]] = {}
    for r in rows:
        by_notebook.setdefault(r["notebook"], []).append(r)
    for nb_name in sorted(by_notebook):
        cells.append(nbf.v4.new_markdown_cell(f"## {nb_name}"))
        lines = ["| concept | claim | calibration |", "|---|---|---|"]
        for r in by_notebook[nb_name]:
            lines.append(
                f"| {r['concept']} | {r['claim']} | **{r['level']}** |"
            )
        cells.append(nbf.v4.new_markdown_cell("\n".join(lines)))
    counts = {lvl: 0 for lvl in _VALID_LEVELS}
    for r in rows:
        counts[r["level"]] = counts.get(r["level"], 0) + 1
    cells.append(nbf.v4.new_markdown_cell(
        "## Calibration summary\n\n"
        f"- HIGH: {counts['HIGH']}\n"
        f"- MEDIUM: {counts['MEDIUM']}\n"
        f"- LOW: {counts['LOW']}\n"
        f"- UNVERIFIED: {counts['UNVERIFIED']}\n"
    ))
    nb.cells = cells
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as f:
        nbf.write(nb, f)
    return target
