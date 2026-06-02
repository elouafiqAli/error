"""HW2 — Partitions, conditional entropy, and 1-WL on toy graphs."""
from __future__ import annotations

from pathlib import Path

from onboarding.projects.scaffold import Cell, write_pair, _setup_cells


HW2_CELLS: list[Cell] = [
    Cell("md",
         "# HW2 — Partitions, conditional entropy, and 1-WL on toy graphs\n\n"
         "**Reading.** `handout.md` Q1–Q5.\n\n"
         "**Goal.** Hand-derive $H(Y\\mid\\Pi)$ on a 6-node toy, code "
         "`cond_entropy`, implement one round of 1-WL refinement, and "
         "exhibit the $C_6$ vs $2K_3$ blind spot. Five assertion gates."),
    *_setup_cells("hw2"),
    Cell("demo",
         "# Reuse hbin from HW1's solution if exported, else re-define inline.\n"
         "from math import log2\n"
         "def hbin(p: float) -> float:\n"
         "    return 0.0 if (p <= 0 or p >= 1) else -(p*log2(p) + (1-p)*log2(1-p))\n"),

    # --- Q1 hand check --------------------------------------------------
    Cell("md",
         "## Q1 — Hand-compute on a 6-node toy\n\n"
         "$y = (0,0,1,1,1,0)$, $\\Pi = \\{\\{0,1,2\\}, \\{3,4\\}, \\{5\\}\\}$.\n\n"
         "By hand: $q = (1/2, 1/3, 1/6)$, $e = (1/3, 0, 0)$, "
         "$\\varepsilon(\\Pi) = 1/6 \\approx 0.1667$, "
         "$H(Y\\mid\\Pi) = \\tfrac{1}{2} H_\\mathrm{bin}(1/3) \\approx 0.4591$."),
    Cell("demo",
         "y = np.array([0,0,1,1,1,0])\n"
         "Pi = [np.array([0,1,2]), np.array([3,4]), np.array([5])]\n"
         "n = sum(len(c) for c in Pi)\n"
         "q = [len(c)/n for c in Pi]\n"
         "e = []\n"
         "for c in Pi:\n"
         "    lbls = y[c]\n"
         "    vals, counts = np.unique(lbls, return_counts=True)\n"
         "    e.append(1 - counts.max()/len(c))\n"
         "eps = sum(qi*ei for qi, ei in zip(q, e))\n"
         "H = sum(qi*hbin(ei) for qi, ei in zip(q, e))\n"
         "print(f'q={q}, e={e}, eps={eps:.4f}, H(Y|Pi)={H:.4f}')\n"),
    Cell("md",
         "**Gate Q1.** Hand and code must agree to $10^{-12}$."),
    Cell("gate",
         "assert abs(q[0]-1/2) < 1e-12 and abs(q[1]-1/3) < 1e-12 and abs(q[2]-1/6) < 1e-12\n"
         "assert abs(e[0]-1/3) < 1e-12 and e[1]==0 and e[2]==0\n"
         "assert abs(eps - 1/6) < 1e-12, f'eps {eps} ≠ 1/6'\n"
         "assert abs(H - 0.5*hbin(1/3)) < 1e-12, f'H {H} ≠ 0.5·hbin(1/3)'\n"
         "print(f'[GATE OK] Q1: q,e,eps,H match hand computation; H={H:.6f}')\n"),
    Cell("reflect",
         "reflect.log('Q2.hw2.Q1_hand', f'H(Y|Pi) on 6-node toy ≈ {H:.4f}', 'HIGH')\n"),

    # --- Q2 cond_entropy -------------------------------------------------
    Cell("md",
         "## Q2 — `cond_entropy(partition, labels)`\n\n"
         "**Concept.** Sum cell-wise $q_C \\cdot H_\\mathrm{bin}(e_C)$. Edge cases: "
         "every cell singleton ⇒ $H = 0$. Single all-of-$\\{0,\\dots,n-1\\}$ cell ⇒ $H = H_\\mathrm{bin}(\\varepsilon)$ (global Bayes error)."),
    Cell("solution",
         "def cond_entropy(partition, labels):\n"
         "    \"\"\"H(Y|Π) in bits.\"\"\"\n"
         "    n = sum(len(c) for c in partition)\n"
         "    total = 0.0\n"
         "    for c in partition:\n"
         "        q_C = len(c) / n\n"
         "        lbls = labels[c]\n"
         "        _, counts = np.unique(lbls, return_counts=True)\n"
         "        e_C = 1 - counts.max() / len(c)\n"
         "        total += q_C * hbin(e_C)\n"
         "    return total\n"),
    Cell("md",
         "**Distinguish — partition-entropy vs label-entropy.** $H(Y\\mid\\Pi)$ "
         "is NOT $H(Y)$; it's $H$ of the *Bayes error inside each cell*. "
         "Singletons drive $H$ to 0; the trivial 1-cell partition recovers $H_\\mathrm{bin}(\\varepsilon_{\\mathrm{global}})$."),
    Cell("demo",
         "# Singleton-cell partition: every cell has e=0 ⇒ H = 0.\n"
         "sing = [np.array([i]) for i in range(len(y))]\n"
         "H_sing = cond_entropy(sing, y)\n"
         "# Trivial 1-cell partition: H = hbin(global Bayes error).\n"
         "triv = [np.arange(len(y))]\n"
         "H_triv = cond_entropy(triv, y)\n"
         "_, counts = np.unique(y, return_counts=True)\n"
         "eps_global = 1 - counts.max()/len(y)\n"
         "print(f'H_sing={H_sing:.6f} H_triv={H_triv:.6f} hbin(eps_global)={hbin(eps_global):.6f}')\n"
         "H_toy = cond_entropy(Pi, y)\n"
         "print(f'H_toy={H_toy:.6f}')\n"),
    Cell("md",
         "**Gate Q2.** Singletons ⇒ 0; trivial ⇒ $H_\\mathrm{bin}(\\varepsilon)$; toy matches Q1."),
    Cell("gate",
         "assert H_sing == 0.0, f'Q2: singleton H={H_sing} should be 0'\n"
         "assert abs(H_triv - hbin(eps_global)) < 1e-12, f'Q2: triv {H_triv} ≠ hbin({eps_global})'\n"
         "assert abs(H_toy - H) < 1e-12, f'Q2: toy {H_toy} ≠ hand {H}'\n"
         "print(f'[GATE OK] Q2: cond_entropy matches edges and toy (H_toy={H_toy:.4f})')\n"),
    Cell("reflect",
         "reflect.log('Q2.hw2.Q2_cond_entropy', 'cond_entropy correct on singleton, trivial, toy', 'HIGH')\n"),

    # --- Q3+Q4: wl_step + C6 vs 2K3 -------------------------------------
    Cell("md",
         "## Q3+Q4 — One-round 1-WL refinement and the $C_6$ vs $2K_3$ blind spot\n\n"
         "**Concept.** $\\mathrm{color}_{t+1}(u) = \\mathrm{hash}(\\mathrm{color}_t(u), \\{\\!\\!\\{\\mathrm{color}_t(v) : v \\sim u\\}\\!\\!\\})$. "
         "Rename signatures densely each round. $C_6$ and $2K_3$ are both 2-regular and indistinguishable by 1-WL."),
    Cell("solution",
         "def wl_step(edge_index, n, colors):\n"
         "    \"\"\"One round of 1-WL refinement on a directed-edge-index graph.\"\"\"\n"
         "    # Group neighbour colours per node.\n"
         "    neighbours = [[] for _ in range(n)]\n"
         "    src, dst = edge_index[0], edge_index[1]\n"
         "    for u, v in zip(src, dst):\n"
         "        neighbours[int(u)].append(int(colors[int(v)]))\n"
         "    sigs = [(int(colors[u]), tuple(sorted(neighbours[u]))) for u in range(n)]\n"
         "    table = {}\n"
         "    new = np.zeros(n, dtype=int)\n"
         "    for u, s in enumerate(sigs):\n"
         "        if s not in table:\n"
         "            table[s] = len(table)\n"
         "        new[u] = table[s]\n"
         "    return new\n"),
    Cell("md",
         "**Distinguish — 1-WL vs degree.** A 1-WL round subsumes degree (multiset size). "
         "Two regular graphs of the same degree (e.g. $C_6$ and $2K_3$) cannot be told apart even after stability."),
    Cell("demo",
         "def edges_C6():\n"
         "    pairs = [(i, (i+1) % 6) for i in range(6)]\n"
         "    e = []\n"
         "    for u, v in pairs:\n"
         "        e += [(u, v), (v, u)]\n"
         "    return np.array(e).T\n"
         "\n"
         "def edges_2K3():\n"
         "    pairs = [(0,1),(1,2),(0,2),(3,4),(4,5),(3,5)]\n"
         "    e = []\n"
         "    for u, v in pairs:\n"
         "        e += [(u, v), (v, u)]\n"
         "    return np.array(e).T\n"
         "\n"
         "def wl_stabilise(edge_index, n, rounds=10):\n"
         "    colors = np.zeros(n, dtype=int)\n"
         "    for _ in range(rounds):\n"
         "        new = wl_step(edge_index, n, colors)\n"
         "        if np.array_equal(new, colors):\n"
         "            break\n"
         "        colors = new\n"
         "    return colors\n"
         "\n"
         "c6 = wl_stabilise(edges_C6(), 6)\n"
         "k3 = wl_stabilise(edges_2K3(), 6)\n"
         "def multiset(arr):\n"
         "    _, cnts = np.unique(arr, return_counts=True)\n"
         "    return tuple(sorted(cnts.tolist()))\n"
         "print(f'C6 stable colors: {c6}  multiset {multiset(c6)}')\n"
         "print(f'2K3 stable colors: {k3}  multiset {multiset(k3)}')\n"),
    Cell("md",
         "**Gate Q3+Q4.** $C_6$ and $2K_3$ stable multisets coincide; both equal $(6,)$."),
    Cell("gate",
         "assert multiset(c6) == multiset(k3) == (6,), f'1-WL multisets {multiset(c6)} vs {multiset(k3)} — blind-spot test failed'\n"
         "# Also check wl_step is non-trivial on the path P_3: endpoints split from middle.\n"
         "p3 = np.array([[0,1,1,2],[1,0,2,1]])\n"
         "col = np.zeros(3, dtype=int)\n"
         "for _ in range(3):\n"
         "    col = wl_step(p3, 3, col)\n"
         "assert len(set(col.tolist())) == 2, f'P3 should split into 2 colour classes; got {col}'\n"
         "assert col[0] == col[2] and col[0] != col[1], f'P3 endpoints {col[0]},{col[2]} vs middle {col[1]}'\n"
         "print(f'[GATE OK] Q3+Q4: C6 and 2K3 indistinguishable by 1-WL; P3 endpoints split from middle')\n"),
    Cell("reflect",
         "reflect.log('Q2.hw2.Q3Q4_wl_blindspot',\n"
         "            'C6 vs 2K3 share stable-colour multiset (6,) under 1-WL; P3 separates endpoints from middle',\n"
         "            'HIGH')\n"),

    # --- Q5 writeup -----------------------------------------------------
    Cell("md",
         "## Q5 — Writeup & calibration\n\n"
         "`writeup.md` should mirror §Q1–§Q4. Below we roll up the reflection log."),
    Cell("reflect",
         "reflect.log('Q2.hw2.Q5_writeup',\n"
         "            'Writeup mirrors hand-comp, cond_entropy, wl_step, blind-spot demonstration',\n"
         "            'MEDIUM')\n"
         "print('HW2 reflection log:')\n"
         "for r in reflect.dump():\n"
         "    if 'hw2' in r['notebook']:\n"
         "        print(f\"  [{r['level']:>10}] {r['concept']}: {r['claim']}\")\n"),
    Cell("md", "**End of HW2.**"),
]


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "psets" / "hw2"
    sol, stu = write_pair(HW2_CELLS, out_dir=out, stem="hw2")
    print(f"wrote {sol.relative_to(out.parent.parent)} and {stu.relative_to(out.parent.parent)}")


if __name__ == "__main__":
    main()
