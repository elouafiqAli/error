"""HW4 — Aggregator inflation on C6 vs 2K3 blind spot."""
from __future__ import annotations

from pathlib import Path

from onboarding.projects.scaffold import Cell, write_pair, _setup_cells


HW4_CELLS: list[Cell] = [
    Cell("md",
         "# HW4 — Aggregator inflation on the $C_6$ vs $2K_3$ blind spot\n\n"
         "**Goal.** Show that no permutation-invariant node-local "
         "aggregator (sum, mean, max) separates $C_6$ from $2K_3$ "
         "under constant or degree features. Triangle counts globally "
         "distinguish them but remain constant *within* each graph, "
         "explaining why genuine 1-WL needs multisets of *colours*, not scalars."),
    *_setup_cells("hw4"),

    # graphs
    Cell("demo",
         "def edges_C6():\n"
         "    pairs = [(i,(i+1)%6) for i in range(6)]\n"
         "    e = []\n"
         "    for u,v in pairs:\n"
         "        e += [(u,v),(v,u)]\n"
         "    return np.array(e).T\n"
         "\n"
         "def edges_2K3():\n"
         "    pairs = [(0,1),(1,2),(0,2),(3,4),(4,5),(3,5)]\n"
         "    e = []\n"
         "    for u,v in pairs:\n"
         "        e += [(u,v),(v,u)]\n"
         "    return np.array(e).T\n"),

    # Q1 aggregators
    Cell("md", "## Q1 — Three aggregator partitions.\n\n"
               "`sum/mean/max_partition(edge_index, n, x)` groups nodes by `(x_u, σ_u)` where $σ_u$ aggregates over $\\{x_v : v \\sim u\\}$."),
    Cell("solution",
         "def _neighbours(edge_index, n):\n"
         "    nbrs = [[] for _ in range(n)]\n"
         "    for u, v in zip(edge_index[0], edge_index[1]):\n"
         "        nbrs[int(u)].append(int(v))\n"
         "    return nbrs\n"
         "\n"
         "def _partition_by_key(keys):\n"
         "    table = {}\n"
         "    for u, k in enumerate(keys):\n"
         "        table.setdefault(k, []).append(u)\n"
         "    return [np.array(v) for v in table.values()]\n"
         "\n"
         "def sum_partition(edge_index, n, x):\n"
         "    nbrs = _neighbours(edge_index, n)\n"
         "    keys = [(float(x[u]), float(sum(x[v] for v in nbrs[u]))) for u in range(n)]\n"
         "    return _partition_by_key(keys)\n"
         "\n"
         "def mean_partition(edge_index, n, x):\n"
         "    nbrs = _neighbours(edge_index, n)\n"
         "    keys = [(float(x[u]), float(np.mean([x[v] for v in nbrs[u]])) if nbrs[u] else 0.0) for u in range(n)]\n"
         "    return _partition_by_key(keys)\n"
         "\n"
         "def max_partition(edge_index, n, x):\n"
         "    nbrs = _neighbours(edge_index, n)\n"
         "    keys = [(float(x[u]), float(max([x[v] for v in nbrs[u]])) if nbrs[u] else 0.0) for u in range(n)]\n"
         "    return _partition_by_key(keys)\n"),
    Cell("md", "**Distinguish — partition vs label.** The aggregator groups *nodes*; it does not assign class labels. Partition cells coarsen as the key set shrinks."),
    Cell("demo",
         "# K2 with x=[1,1]: each aggregator → one cell.\n"
         "ei_k2 = np.array([[0,1],[1,0]])\n"
         "for name, fn in [('sum',sum_partition),('mean',mean_partition),('max',max_partition)]:\n"
         "    p = fn(ei_k2, 2, np.array([1.0,1.0]))\n"
         "    print(f'  K2 / {name}: {len(p)} cell(s)')\n"),
    Cell("md", "**Gate Q1.** All three aggregators yield 1 cell on $K_2$ with $x=(1,1)$."),
    Cell("gate",
         "for name, fn in [('sum',sum_partition),('mean',mean_partition),('max',max_partition)]:\n"
         "    p = fn(ei_k2, 2, np.array([1.0,1.0]))\n"
         "    assert len(p) == 1, f'Q1: {name} should collapse K2 to 1 cell'\n"
         "print('[GATE OK] Q1: sum/mean/max collapse K2 with constant features to 1 cell')\n"),
    Cell("reflect", "reflect.log('Q4.Q1_aggregators', 'sum/mean/max partitions implemented; collapse on K2/constant', 'HIGH')\n"),

    # Q2 constant features
    Cell("md", "## Q2 — Constant features collapse both $C_6$ and $2K_3$ under every aggregator."),
    Cell("demo",
         "x_const = np.ones(6)\n"
         "ei_c6, ei_k3 = edges_C6(), edges_2K3()\n"
         "results = {}\n"
         "for name, fn in [('sum',sum_partition),('mean',mean_partition),('max',max_partition)]:\n"
         "    for g, ei in [('C6', ei_c6), ('2K3', ei_k3)]:\n"
         "        p = fn(ei, 6, x_const)\n"
         "        results[(name,g)] = (len(p), tuple(sorted(len(c) for c in p)))\n"
         "        print(f'  {g} / {name}: {len(p)} cell(s), sizes {results[(name,g)][1]}')\n"),
    Cell("md", "**Gate Q2.** Every (aggregator × graph) pair returns exactly 1 cell of size 6."),
    Cell("gate",
         "for k, (ncells, sizes) in results.items():\n"
         "    assert ncells == 1 and sizes == (6,), f'Q2: {k} should be a single 6-cell, got {ncells},{sizes}'\n"
         "print('[GATE OK] Q2: constant features → 1×6 on both C6 and 2K3 under sum/mean/max')\n"),
    Cell("reflect", "reflect.log('Q4.Q2_constant_collapse', 'all 6 (agg×graph) cases collapse to 1×6', 'HIGH')\n"),

    # Q3 degree feature still blind
    Cell("md", "## Q3 — Degree feature. Both graphs are 2-regular, so feature is constant ⇒ still blind."),
    Cell("demo",
         "def degree(edge_index, n):\n"
         "    deg = np.zeros(n)\n"
         "    for u in edge_index[0]:\n"
         "        deg[int(u)] += 1\n"
         "    return deg\n"
         "\n"
         "deg_c6, deg_k3 = degree(ei_c6, 6), degree(ei_k3, 6)\n"
         "print(f'deg(C6)={deg_c6}, deg(2K3)={deg_k3}')\n"),
    Cell("md", "**Gate Q3.** Both degree vectors equal $(2,2,2,2,2,2)$, so the result is identical to Q2."),
    Cell("gate",
         "assert np.all(deg_c6 == 2) and np.all(deg_k3 == 2), f'Q3: not 2-regular: {deg_c6}, {deg_k3}'\n"
         "# As consequence, sum/mean/max with degree feature also collapse to 1×6.\n"
         "for name, fn in [('sum',sum_partition),('mean',mean_partition),('max',max_partition)]:\n"
         "    for g, ei, deg in [('C6', ei_c6, deg_c6), ('2K3', ei_k3, deg_k3)]:\n"
         "        p = fn(ei, 6, deg)\n"
         "        assert len(p) == 1 and len(p[0]) == 6, f'Q3: {g}/{name} did not collapse with degree feature'\n"
         "print('[GATE OK] Q3: degree feature is constant on both → identical aggregator collapse')\n"),
    Cell("reflect", "reflect.log('Q4.Q3_degree_blind', 'degree feature equal to constant on 2-regular graphs', 'HIGH')\n"),

    # Q4 triangle counts separate globally
    Cell("md", "## Q4 — Triangle count separates the two graphs globally but is constant within each."),
    Cell("solution",
         "def triangle_count(edge_index, n):\n"
         "    nbrs = [set() for _ in range(n)]\n"
         "    for u, v in zip(edge_index[0], edge_index[1]):\n"
         "        nbrs[int(u)].add(int(v))\n"
         "    out = np.zeros(n, dtype=int)\n"
         "    for u in range(n):\n"
         "        for v in nbrs[u]:\n"
         "            if v <= u: continue\n"
         "            for w in nbrs[u] & nbrs[v]:\n"
         "                if w > v:\n"
         "                    out[u] += 1; out[v] += 1; out[w] += 1\n"
         "    return out\n"),
    Cell("md", "**Distinguish.** Triangle count is a *global* invariant that distinguishes graphs but is constant within each graph here → still no within-graph partition refinement."),
    Cell("demo",
         "t_c6 = triangle_count(ei_c6, 6)\n"
         "t_k3 = triangle_count(ei_k3, 6)\n"
         "print(f'triangles(C6)={t_c6}  sum={t_c6.sum()}')\n"
         "print(f'triangles(2K3)={t_k3}  sum={t_k3.sum()}')\n"),
    Cell("md", "**Gate Q4.** $C_6$ → all 0; $2K_3$ → all 1; graphs distinguished by feature sum."),
    Cell("gate",
         "assert np.all(t_c6 == 0), f'Q4: C6 triangle vector {t_c6} ≠ 0'\n"
         "assert np.all(t_k3 == 1), f'Q4: 2K3 triangle vector {t_k3} ≠ 1'\n"
         "assert t_c6.sum() != t_k3.sum(), 'Q4: triangle feature did not separate the two graphs'\n"
         "print('[GATE OK] Q4: triangles(C6)=0 everywhere, triangles(2K3)=1 everywhere')\n"),
    Cell("reflect", "reflect.log('Q4.Q4_triangles', 'triangle-count separates C6 from 2K3 globally; constant within each', 'HIGH')\n"),

    # Q5
    Cell("md", "## Q5 — Writeup & calibration."),
    Cell("reflect",
         "reflect.log('Q4.Q5_writeup', 'no permutation-invariant node-local aggregator separates C6 from 2K3', 'HIGH')\n"
         "print('HW4 reflection log:')\n"
         "for r in reflect.dump():\n"
         "    if 'hw4' in r['notebook']:\n"
         "        print(f\"  [{r['level']:>10}] {r['concept']}: {r['claim']}\")\n"),
    Cell("md", "**End of HW4.**"),
]


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "psets" / "hw4"
    sol, stu = write_pair(HW4_CELLS, out_dir=out, stem="hw4")
    print(f"wrote {sol.relative_to(out.parent.parent)} and {stu.relative_to(out.parent.parent)}")


if __name__ == "__main__":
    main()
