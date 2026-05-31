PY ?= python3

.PHONY: all e1 e2 e4 e5 clean

all: e5 e4 e1 e2

e5:
	$(PY) e5_scatter.py

e4:
	$(PY) e4_duel.py

e1:
	$(PY) e1_trees.py

e2:
	$(PY) e2_vq_proxy.py

clean:
	rm -rf results/ figures/*.pdf __pycache__
