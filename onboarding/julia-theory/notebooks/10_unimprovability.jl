### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Unimprovability (Prop 7) — live"
#> tags = ["bracket", "unit-3", "unimprovability"]

using Markdown, InteractiveUtils

# ╔═╡ a000000a-0001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a000000a-0002
md"""
# Notebook 10 — Unimprovability

> **Unit III, item 3.** Try to improve the upper envelope by a
> multiplicative factor $\beta \in (0, 1)$. The witness family
> $\Pi_\alpha^{\mathrm{HR}}$ from notebook 09 forces $\beta \ge 1$ —
> any attempted improvement *violates* a feasible partition.
"""

# ╔═╡ a000000a-0003
md"## 1. Slider"

# ╔═╡ a000000a-0004
@bind β Slider(0.5:0.001:1.0, default=0.95, show_value=true)

# ╔═╡ a000000a-0005
md"## 2. Proposed improved upper"

# ╔═╡ a000000a-0006
# TODO(reader):
#   improved_upper(ε; q, e) = β * (original upper from notebook 05)
# plot it against the witness Π_HR's (ε, ε) point — the witness has
# its ε = its ε (trivially), so we plot the witness on the upper-envelope
# overlay from notebook 05.

# ╔═╡ a000000a-0007
md"## 3. Read off the contradiction"

# ╔═╡ a000000a-0008
# TODO(reader): for β < 1, find the α at which improved_upper(ε(Π_HR(α))) < ε(Π_HR(α))
# — that's the contradiction. Highlight the violating α on the plot.

# ╔═╡ a000000a-0009
md"""
## 4. The lesson

> "Tightness witnesses are the verification you owe before announcing
> an improvement." — PLAN.md §11c, generalised.

If you propose to sharpen the upper bound, the witness you must
defeat *is named in the paper*. The slider lets you stress-test any
candidate sharpening before publishing it.

## 5. Next — Unit IV: aggregator triple on Cora
"""

# ╔═╡ Cell order:
# ╠═a000000a-0001
# ╟─a000000a-0002
# ╟─a000000a-0003
# ╠═a000000a-0004
# ╟─a000000a-0005
# ╠═a000000a-0006
# ╟─a000000a-0007
# ╠═a000000a-0008
# ╟─a000000a-0009
