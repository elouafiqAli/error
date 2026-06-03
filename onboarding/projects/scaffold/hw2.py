"""HW2 — Partitions, conditional entropy, and 1-WL on toy graphs."""
from __future__ import annotations

from pathlib import Path

from onboarding.projects.scaffold import Cell, write_pair, _setup_cells


HW2_CELLS: list[Cell] = [
    Cell("md",
         "# HW2 — Partitions, conditional entropy, and 1-WL on toy graphs\n\n"
         "**Reading.** `handout.md` Q1–Q5; "
         "[`PAPER-ARXIV.md`](../../../../PAPER-ARXIV.md) §3.1 "
         "(Definitions 3.1–3.2, **Lemma 3.1**) and §3.3 (scope: "
         "$\\mathcal{F}_\\mathrm{WL}$).\n\n"
         "**Goal.** Hand-derive $H(Y\\mid\\Pi)$ on a 6-node toy, code "
         "`cond_entropy`, prove **Lemma 3.1** (*purity ⟺ zero "
         "conditional entropy*) numerically, implement one round of 1-WL "
         "refinement, and exhibit the $C_6$ vs $2K_3$ blind spot — the "
         "**qualitative ceiling** of Xu et al. (ICLR 2019, GIN) and "
         "Morris et al. (AAAI 2019, $k$-GNNs) that **HW3's bracket will "
         "quantify**. Six assertion gates.\n\n"
         "**Julia companion (optional).** "
         "[`julia-theory/notebooks/04_bayes_error_landscape.jl`](../../../julia-theory/notebooks/04_bayes_error_landscape.jl) "
         "is the reactive slider twin of Q2 (per-cell $e_C$, $q_C$ on a 3-simplex)."),
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

    # --- Q2.5: Lemma 3.1 (purity iff zero conditional entropy) ---------
    Cell("md",
         "## Q2.5 — **Lemma 3.1** (purity ⟺ zero conditional entropy)\n\n"
         "**Statement (Paper §3.1).** Call $\\Pi$ **pure for $Y$** if every "
         "cell $C \\in \\Pi$ is label-constant ($y$ is constant on $C$). Then\n\n"
         "$$\n"
         "H(Y \\mid \\Pi) = 0 \\iff \\Pi \\text{ is pure for } Y.\n"
         "$$\n\n"
         "**Sketch.** $H(Y\\mid\\Pi) = \\sum_C q_C H_\\mathrm{bin}(e_C)$ with "
         "$q_C > 0$ and $H_\\mathrm{bin}(e) \\ge 0$, equality iff $e \\in \\{0, 1\\}$. "
         "After per-cell binarisation $e_C \\leftarrow \\min(e_C, 1-e_C) \\in [0, 1/2]$, "
         "the only zero is $e_C = 0$, i.e. cell is single-class.\n\n"
         "**Adversarial framing.** A reader who only memorises Theorem 1 may "
         "conflate \"low $H$\" with \"low $\\varepsilon$\". Lemma 3.1 is the "
         "*iff* that grounds the lower bracket: $H=0$ is **not** an accident "
         "of one cell, it is purity of the entire partition."),
    Cell("solution",
         "def is_pure(partition, labels) -> bool:\n"
         "    \"\"\"True iff every cell is label-constant.\"\"\"\n"
         "    for C in partition:\n"
         "        if len(set(labels[C].tolist())) > 1:\n"
         "            return False\n"
         "    return True\n"),
    Cell("md", "**Distinguish — *iff*, not just *if*.** A naive reader might prove only the easy direction (purity $\\Rightarrow H=0$). The reverse — $H=0 \\Rightarrow$ purity — uses strict positivity of $H_\\mathrm{bin}$ on $(0, 1)$."),
    Cell("demo",
         "# Build a non-trivial witness of each direction.\n"
         "# (a) Pure partition: split y by label.\n"
         "y_pure = np.array([0,0,0,1,1,1])\n"
         "Pi_pure = [np.array([0,1,2]), np.array([3,4,5])]\n"
         "H_pure  = cond_entropy(Pi_pure, y_pure)\n"
         "print(f'pure: H={H_pure:.6f}, is_pure={is_pure(Pi_pure, y_pure)}')\n"
         "\n"
         "# (b) Mixed cell ⇒ H>0.\n"
         "y_mix = np.array([0,0,1,1,1,0])\n"
         "Pi_mix = [np.array([0,1,2,3,4,5])]\n"
         "H_mix  = cond_entropy(Pi_mix, y_mix)\n"
         "print(f'mixed: H={H_mix:.6f}, is_pure={is_pure(Pi_mix, y_mix)}')\n"
         "\n"
         "# (c) Border case: every singleton ⇒ trivially pure ⇒ H=0.\n"
         "Pi_sing = [np.array([i]) for i in range(6)]\n"
         "H_sing2 = cond_entropy(Pi_sing, y_mix)\n"
         "print(f'singletons: H={H_sing2:.6f}, is_pure={is_pure(Pi_sing, y_mix)}')\n"),
    Cell("md", "**Gate Q2.5.** Forward (purity $\\Rightarrow H=0$) AND reverse (mixed cell $\\Rightarrow H>0$) on three witnesses."),
    Cell("gate",
         "# Lemma 3.1 — forward direction: pure ⇒ H = 0.\n"
         "assert is_pure(Pi_pure, y_pure) and H_pure == 0.0, f'Q2.5: pure partition has H={H_pure} ≠ 0'\n"
         "assert is_pure(Pi_sing, y_mix) and H_sing2 == 0.0, f'Q2.5: singletons have H={H_sing2} ≠ 0'\n"
         "# Reverse direction: H > 0 ⇒ NOT pure.\n"
         "assert H_mix > 0 and not is_pure(Pi_mix, y_mix), f'Q2.5: mixed cell has H={H_mix} but is_pure={is_pure(Pi_mix, y_mix)}'\n"
         "# Final: sweep 200 random partitions; the equivalence must never break.\n"
         "import random\n"
         "random.seed(1)\n"
         "for trial in range(200):\n"
         "    yy = np.array([random.randint(0, 1) for _ in range(8)])\n"
         "    nc = random.randint(1, 4)\n"
         "    perm = list(range(8)); random.shuffle(perm)\n"
         "    cuts = sorted(random.sample(range(1, 8), nc - 1)) if nc > 1 else []\n"
         "    edges = [0] + cuts + [8]\n"
         "    PP = [np.array(perm[edges[i]:edges[i+1]]) for i in range(nc)]\n"
         "    HH = cond_entropy(PP, yy)\n"
         "    pp = is_pure(PP, yy)\n"
         "    assert (HH == 0.0) == pp, f'Q2.5 random trial {trial}: H={HH}, is_pure={pp}'\n"
         "print('[GATE OK] Q2.5: Lemma 3.1 verified on 3 hand witnesses + 200 random partitions')\n"),
    Cell("reflect",
         "reflect.log('Q2.hw2.Q2.5_lemma_3_1',\n"
         "            'Lemma 3.1 (purity ⟺ H(Y|Π)=0) verified on 3 witnesses + 200 random partitions',\n"
         "            'HIGH')\n"),

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

    # --- Q4.5: provenance — Xu 2019 / Morris 2019 -----------------------
    Cell("md",
         "## Q4.5 — Provenance: Xu et al. (GIN) and Morris et al. ($k$-GNN)\n\n"
         "The $C_6$ vs $2K_3$ blind spot you just exhibited is the central "
         "negative result of **two ICLR/AAAI 2019 papers**:\n\n"
         "- **Xu, Hu, Leskovec, Jegelka.** *How Powerful are Graph Neural Networks?* "
         "  ICLR 2019. The **GIN** paper. Theorem 3: any MPNN with countable "
         "  multiset aggregator is at most as expressive as 1-WL.\n"
         "- **Morris, Ritzert, Fey, Hamilton, Lenssen, Rattan, Grohe.** *Weisfeiler "
         "  and Leman Go Neural: Higher-order Graph Neural Networks.* AAAI 2019. "
         "  The **$k$-GNN** paper. Same qualitative ceiling at 1-WL; lifts it to "
         "  $k$-WL via tuple states.\n\n"
         "Both papers say *qualitatively*: \"MPNNs can never separate $C_6$ from "
         "$2K_3$.\" **Paper A** (Theorem 1, HW3 next week) sharpens this to a "
         "**quantitative budget**: for any MPNN-induced partition $\\Pi$, the "
         "Bayes error obeys\n\n"
         "$$\n"
         "H_\\mathrm{bin}^{-1}\\!\\big(H(Y\\mid\\Pi)\\big) \\;\\le\\; \\varepsilon^*_\\Pi \\;\\le\\; \\tfrac{1}{2}\\, H(Y\\mid\\Pi).\n"
         "$$\n\n"
         "The slack at the worst point is **$w^\\star \\approx 0.1610$** "
         "attained at **$\\varepsilon^\\star = 1/5$** — the number HW3.Q4 will "
         "grid-search you to. *That* is the upgrade from \"impossible\" to "
         "\"impossible by exactly this much.\""),
    Cell("reflect",
         "reflect.log('Q2.hw2.Q4.5_provenance',\n"
         "            'Xu 2019 (GIN) + Morris 2019 (k-GNN) give the qualitative 1-WL ceiling; Theorem 1 quantifies it (w*≈0.1610).',\n"
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
