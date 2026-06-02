"""Pytest configuration for the projects/ subtree.

Tests live in psets/hw{1..4}/tests/ and shared/tests/, with intentionally
clashing basenames (test_q1.py, test_q2.py, ...) — one per question per
homework. The legacy pytest import mode (rootdir + sys.path mangling)
treats those as collisions; importlib mode (configured in pytest.ini)
loads each test file by its absolute path with no name-based caching.

Student-facing pset tests intentionally raise NotImplementedError until
students fill the starters. We exclude them from the default collection
via `collect_ignore`; grade them explicitly with
`pytest onboarding/projects/psets/hwN`.
"""

from __future__ import annotations

import os
import pathlib

_HERE = pathlib.Path(__file__).resolve().parent

# Opt back in to the student tests with `GRADE=1 pytest ...` (used by
# the hw-grading Make targets / by students checking their own work).
if not os.environ.get("GRADE"):
    collect_ignore_glob = [str(_HERE / "psets" / "hw*" / "tests")]
