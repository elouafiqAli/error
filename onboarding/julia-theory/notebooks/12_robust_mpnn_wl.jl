### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "ε-robust MPNN–WL constancy (Lemma 6)"
#> tags = ["mpnn", "unit-4", "robustness"]

using Markdown, InteractiveUtils

# ╔═╡ a000000c-0001
using PlutoUI, Plots, LaTeXStrings, LinearAlgebra, Random

# ╔═╡ a000000c-0002
md"""
# Notebook 12 — $\varepsilon$-robust MPNN–WL constancy

> **Unit IV, item 2.** Lemma 6 made tactile. On a toy graph, run
> 1-WL refinement to get a colour partition; perturb node features
> within each cell by $\le \varepsilon$ in $\ell_\infty$; run two
> rounds of a GIN-style aggregation; report which cells remain
> constant.
>
> **The slider IS the perturbation budget $\varepsilon$.**
"""

# ╔═╡ a000000c-0003
md"## 1. Pick a toy graph"

# ╔═╡ a000000c-0004
@bind graph_name Select(["C_6 (6-cycle)" => :C6, "2 K_3 (two disjoint triangles)" => :K3K3, "Petersen" => :petersen])

# ╔═╡ a000000c-0005
# TODO(reader): build edge_index for each choice; verify visually.

# ╔═╡ a000000c-0006
md"## 2. Run 1-WL refinement → cell partition"

# ╔═╡ a000000c-0007
# TODO(reader): wl_refine step from PLAN/M1 (capstone) ported to Julia.
# Run depth 3; collect cells.

# ╔═╡ a000000c-0008
md"## 3. Perturbation slider"

# ╔═╡ a000000c-0009
@bind ε Slider(0.0:0.001:1.0, default=0.1, show_value=true)

# ╔═╡ a000000c-000a
md"## 4. Run two GIN-style rounds with perturbation"

# ╔═╡ a000000c-000b
# TODO(reader):
#   x = ones(n)  # initial constant features
#   for each cell: perturb x[cell] by Uniform(-ε, ε)
#   for round in 1:2: x = MLP(sum_aggregate(x))   # toy update
#   for each cell: compute within-cell standard deviation; report.

# ╔═╡ a000000c-000c
md"""
## 5. Plot — within-cell std vs ε

- TODO(reader): scatter (within-cell std) for each cell across a
  sweep of ε; identify the threshold above which a cell stops being
  constant. That threshold IS the Lemma-6 bound for this graph.

## 6. Compare to Lemma 6's prediction

- TODO(reader): the Lemma gives a closed-form upper bound on the
  surviving ε; plot it as a dashed line; compare.

## 7. Done

You have now slid through every theoretical object in the paper.
Open the abstract and re-read it. The constants should feel like
plot-points, not symbols.
"""

# ╔═╡ Cell order:
# ╠═a000000c-0001
# ╟─a000000c-0002
# ╟─a000000c-0003
# ╠═a000000c-0004
# ╠═a000000c-0005
# ╟─a000000c-0006
# ╠═a000000c-0007
# ╟─a000000c-0008
# ╠═a000000c-0009
# ╟─a000000c-000a
# ╠═a000000c-000b
# ╟─a000000c-000c
