### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Information quantities — H(X), H(Y|X), I(X;Y)"
#> tags = ["information-theory", "primitives", "unit-1"]

using Markdown, InteractiveUtils

# ╔═╡ a0000002-0001
using PlutoUI, Plots, LaTeXStrings, Symbolics

# ╔═╡ a0000002-0002
md"""
# Notebook 02 — Information quantities

> **Unit I, primitive 2.** Joint distributions $P(X,Y)$ on a 2×2
> table. Build entropy, conditional entropy, mutual information from
> scratch. Verify the chain rule on the page.
>
> **Punchline.** $H(X,Y) = H(X) + H(Y\mid X) = H(Y) + H(X\mid Y)$
> and $I(X;Y) = H(Y) - H(Y\mid X) \ge 0$ with equality iff $X \perp Y$.
"""

# ╔═╡ a0000002-0003
md"## 1. Joint distribution on a 2×2 table"

# ╔═╡ a0000002-0004
md"""
Slide three of the four entries; the fourth is forced by sum-to-one.
"""

# ╔═╡ a0000002-0005
@bind p00 Slider(0.0:0.01:1.0, default=0.4, show_value=true)

# ╔═╡ a0000002-0006
@bind p01 Slider(0.0:0.01:1.0, default=0.1, show_value=true)

# ╔═╡ a0000002-0007
@bind p10 Slider(0.0:0.01:1.0, default=0.1, show_value=true)

# ╔═╡ a0000002-0008
# TODO(reader): build the 2×2 matrix P with P[2,2] = 1 - p00 - p01 - p10,
# and reject if any entry is negative.

# ╔═╡ a0000002-0009
md"## 2. Marginals, conditionals, and the IT primitives"

# ╔═╡ a0000002-000a
# TODO(reader): from P, compute
#   PX = sum along Y axis
#   PY = sum along X axis
#   PY_given_X = P ./ PX (broadcast safely; guard zero)
# H(X), H(Y), H(X,Y), H(Y|X), I(X;Y).

# ╔═╡ a0000002-000b
md"## 3. Verify the chain rule"

# ╔═╡ a0000002-000c
# TODO(reader): assert |H(X,Y) - (H(X) + H(Y|X))| < 1e-12
# and the symmetric variant. Print both sides.

# ╔═╡ a0000002-000d
md"## 4. Slide to independence; watch I(X;Y) → 0"

# ╔═╡ a0000002-000e
# TODO(reader): set sliders so that P factorises as PX * PY^T (one click);
# show I(X;Y) ≈ 0. Then perturb one slider by 0.01 and watch MI grow.

# ╔═╡ a0000002-000f
md"## 5. Falsify — what if P has a negative entry?"

# ╔═╡ a0000002-0010
# TODO(reader): force P[1,1] = -0.05 and observe which IT quantities
# break (some become complex; some go negative; H(X,Y) underflows).

# ╔═╡ a0000002-0011
md"""
## 6. Take-aways

- TODO(reader): write one line on *why* MI is symmetric ($I(X;Y) = I(Y;X)$).
- TODO(reader): write one line on *why* conditional entropy is not.

## 7. Next

Notebook **03 — Fano vs Hellman–Raviv**.
"""

# ╔═╡ Cell order:
# ╠═a0000002-0001
# ╟─a0000002-0002
# ╟─a0000002-0003
# ╟─a0000002-0004
# ╠═a0000002-0005
# ╠═a0000002-0006
# ╠═a0000002-0007
# ╠═a0000002-0008
# ╟─a0000002-0009
# ╠═a0000002-000a
# ╟─a0000002-000b
# ╠═a0000002-000c
# ╟─a0000002-000d
# ╠═a0000002-000e
# ╟─a0000002-000f
# ╠═a0000002-0010
# ╟─a0000002-0011
