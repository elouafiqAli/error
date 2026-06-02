# onboarding/projects — open-courseware-grade verification harness.
#
# Two lanes:
#   `make all`           — CPU-only: HWs + M1/M2 + shared unit tests.
#   `make modal-verify`  — invokes Modal: M3/M4/M6 GPU notebooks.
#
# Lay this out from the *repo root*:
#   make -C onboarding/projects all

PY := python
PYTEST := pytest -q
NBCLI := jupyter nbconvert --to notebook --execute --inplace

# Files
HW_NBS := psets/hw1/hw1.ipynb psets/hw2/hw2.ipynb psets/hw3/hw3.ipynb psets/hw4/hw4.ipynb
M_CPU_NBS := capstone/milestone1/m1.ipynb capstone/milestone2/m2.ipynb
M_GPU_NBS := capstone/milestone3/m3.ipynb capstone/milestone4/m4.ipynb capstone/milestone6/m6_advanced.ipynb

.PHONY: all setup unit grade grade-hw1 grade-hw2 grade-hw3 grade-hw4 hw1 hw2 hw3 hw4 m1 m2 m3 m4 m5 m6 modal-verify clean help

help:
	@echo "Targets: setup unit hw1..hw4 m1..m6 all modal-verify"
	@echo "         grade-hw1..hw4 grade  (run student-facing tests; GRADE=1)"

setup:
	$(PY) -m pip install -r requirements.txt

unit:
	cd ../.. && $(PYTEST) onboarding/projects/shared/tests onboarding/projects/ci

# Student-facing grading lane: pset tests intentionally raise
# NotImplementedError until the student fills the starters. The GRADE=1
# env var opts back in to those tests (see conftest.py).
grade-hw1: ; GRADE=1 $(PYTEST) psets/hw1
grade-hw2: ; GRADE=1 $(PYTEST) psets/hw2
grade-hw3: ; GRADE=1 $(PYTEST) psets/hw3
grade-hw4: ; GRADE=1 $(PYTEST) psets/hw4
grade: grade-hw1 grade-hw2 grade-hw3 grade-hw4

# HWs (CPU-fast, no GPU)
hw1: ; $(NBCLI) psets/hw1/hw1.ipynb
hw2: ; $(NBCLI) psets/hw2/hw2.ipynb
hw3: ; $(NBCLI) psets/hw3/hw3.ipynb
hw4: ; $(NBCLI) psets/hw4/hw4.ipynb

# Capstones
m1: ; $(NBCLI) capstone/milestone1/m1.ipynb
m2: ; $(NBCLI) capstone/milestone2/m2.ipynb
m3: ; $(NBCLI) capstone/milestone3/m3.ipynb   # invokes Modal GPU
m4: ; $(NBCLI) capstone/milestone4/m4.ipynb   # invokes Modal GPU
m5: ; $(NBCLI) capstone/milestone5/m5.ipynb   # auto-assembled
m6: ; $(NBCLI) capstone/milestone6/m6_advanced.ipynb

# CPU lane: everything that runs without GPU/Modal
all: unit hw1 hw2 hw3 hw4 m1 m2 m5
	@echo "[OK] CPU lane green"

# GPU lane: actually invokes Modal (requires `modal token new` first)
modal-verify: m3 m4 m6
	@echo "[OK] Modal GPU lane green"

clean:
	rm -rf .pytest_cache
	find . -name '*.ipynb_checkpoints' -prune -exec rm -rf {} +
