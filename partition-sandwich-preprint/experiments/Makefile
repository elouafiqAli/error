PY ?= python3

.PHONY: all e1 e2 e2b e3 e4 e5 e6 e6_cost e7 clean

all: e5 e4 e1 e2 e2b e3 e6 e6_cost e7

e5:
	$(PY) e5_scatter.py

e4:
	$(PY) e4_duel.py

e1:
	$(PY) e1_trees.py

e2:
	$(PY) e2_vq_proxy.py

e2b:
	$(PY) e2b_marginal_aware.py

e3:
	$(PY) e3_wl_bracket.py

e6:
	$(PY) -W ignore e6_nas.py

e6_cost:
	$(PY) -W ignore e6_cost.py

e7:
	$(PY) e7_pop_concentration.py

clean:
	rm -rf results/ figures/*.pdf __pycache__
