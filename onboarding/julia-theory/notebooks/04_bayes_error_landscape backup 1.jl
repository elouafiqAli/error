### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Bayes-error landscape on a 3-cell partition"
#> tags = ["bracket", "unit-2"]

using Markdown, InteractiveUtils

# ╔═╡ a0000004-0001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a0000004-0002
md"""
# Notebook 04 — Bayes-error landscape on a 3-cell partition

> **Unit II, building block 1.** Pre-bracket arithmetic. Slide cell
> masses on the 3-simplex and per-cell errors on a cube; watch
> $\varepsilon(\Pi)$ (linear) and $H(Y\mid\Pi)$ (concave) move
> together.
"""

# ╔═╡ a0000004-0003
md"## 1. Sliders — cell masses (simplex) and per-cell errors"

# ╔═╡ a0000004-0004
@bind q1 Slider(0.05:0.01:0.9, default=1/3, show_value=true)

# ╔═╡ a0000004-0005
@bind q2 Slider(0.05:0.01:0.9, default=1/3, show_value=true)

# ╔═╡ a0000004-0006
@bind e1 Slider(0.0:0.001:0.5, default=0.1, show_value=true)

# ╔═╡ a0000004-0007
@bind e2 Slider(0.0:0.001:0.5, default=0.2, show_value=true)

# ╔═╡ a0000004-0008
@bind e3 Slider(0.0:0.001:0.5, default=0.3, show_value=true)

# ╔═╡ a0000004-0009
# TODO(reader): build q = [q1, q2, 1 - q1 - q2]; reject if q[3] < 0.05.

# ╔═╡ a0000004-000a
md"## 2. Compute $\varepsilon(\Pi)$ and $H(Y\mid\Pi)$"

# ╔═╡ a0000004-000b
# TODO(reader):
#   Hbin(p) as before
#   ε(q, e) = dot(q, e)
#   HYgivenΠ(q, e) = dot(q, Hbin.(e))
# Print both.

# ╔═╡ a0000004-000c
md"## 3. Trace the achievable curve"

# ╔═╡ a0000004-000d
# TODO(reader): with q fixed, sweep e1 ∈ [0, 1/2] with e2 = e3 = e1;
# scatter (ε, HYgivenΠ); overlay the Hbin(ε) lower envelope and the
# upper envelope Σ q_C 2 Hbin^{-1}(2 e_C). Both will be added in
# notebook 05, so this is a *preview*.

# ╔═╡ a0000004-000e
md"## 4. Next — Notebook 05: the bracket envelope (centrepiece)"

# ╔═╡ Cell order:
# ╠═a0000004-0001
# ╟─a0000004-0002
# ╟─a0000004-0003
# ╠═a0000004-0004
# ╠═a0000004-0005
# ╠═a0000004-0006
# ╠═a0000004-0007
# ╠═a0000004-0008
# ╠═a0000004-0009
# ╟─a0000004-000a
# ╠═a0000004-000b
# ╟─a0000004-000c
# ╠═a0000004-000d
# ╟─a0000004-000e
