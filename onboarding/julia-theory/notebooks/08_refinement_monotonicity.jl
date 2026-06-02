### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Refinement monotonicity — and the endpoint false-lead"
#> tags = ["bracket", "unit-3", "proposition-5"]

using Markdown, InteractiveUtils

# ╔═╡ a0000008-0001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a0000008-0002
md"""
# Notebook 08 — Refinement monotonicity

> **Unit III, item 1.** Proposition 5 says: refining a partition
> shrinks the *interval* $[\mathrm{lower}, \mathrm{upper}]$. It does
> NOT say the individual endpoints are monotone. We exhibit a
> counter-example in 10 lines.
>
> **PLAN.md item 14d, lived in code.**
"""

# ╔═╡ a0000008-0003
md"## 1. Start: a 2-cell coarse partition"

# ╔═╡ a0000008-0004
# TODO(reader): q_coarse = [0.5, 0.5]; e_coarse = [0.1, 0.4]
# print (lower, upper, interval-width).

# ╔═╡ a0000008-0005
md"## 2. Refine: split cell 1 into two sub-cells"

# ╔═╡ a0000008-0006
@bind α Slider(0.01:0.01:0.99, default=0.5, show_value=true)

# ╔═╡ a0000008-0007
# TODO(reader): q_fine = [α/2, (1-α)/2, 0.5]; e_fine = [e1a, e1b, 0.4]
# with e1a, e1b chosen so q_coarse[1] * e_coarse[1] = α/2 * e1a + (1-α)/2 * e1b
# (mass-weighted average preserved). Print (lower, upper, width).

# ╔═╡ a0000008-0008
md"## 3. Counter-example to endpoint monotonicity"

# ╔═╡ a0000008-0009
# TODO(reader): set α = 0.99, e1a = 0.5, e1b ≈ 0 (so the average is preserved).
# Observe: lower_fine > lower_coarse (lower endpoint went *up*)
# but width_fine < width_coarse (interval still shrank).
# Plot both intervals side by side.

# ╔═╡ a0000008-000a
md"""
## 4. The lesson

> "The object that is monotone is the **interval**, not its individual
> ends." — PLAN.md §14d.

A naive proof attempt would try to show both endpoints are monotone
and then deduce containment. The above 10 lines kill that approach.
The actual proof has to argue about the interval-as-a-whole — see
[`partition-sandwich-preprint/main.tex`](../../../partition-sandwich-preprint/main.tex#L842)
§"Refinement monotonicity".

## 5. Next — Notebook 09: tightness witnesses
"""

# ╔═╡ Cell order:
# ╠═a0000008-0001
# ╟─a0000008-0002
# ╟─a0000008-0003
# ╠═a0000008-0004
# ╟─a0000008-0005
# ╠═a0000008-0006
# ╠═a0000008-0007
# ╟─a0000008-0008
# ╠═a0000008-0009
# ╟─a0000008-000a
