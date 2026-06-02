### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "The achievable region in the (ε, H(Y|Π)) plane"
#> tags = ["bracket", "unit-2", "proposition-3"]

using Markdown, InteractiveUtils

# ╔═╡ a0000007-0001
using PlutoUI, Plots, LaTeXStrings, Random

# ╔═╡ a0000007-0002
md"""
# Notebook 07 — The achievable region

> **Unit II, capstone.** Proposition 3 made visual. Sample $N$
> partitions; scatter their $(\varepsilon, H(Y\mid\Pi))$; overlay
> the envelopes; observe that the cloud fills a *region*, not a
> curve.
"""

# ╔═╡ a0000007-0003
md"## 1. Sliders — number of cells, samples, seed"

# ╔═╡ a0000007-0004
@bind m Select([3, 5, 7, 10, 20])

# ╔═╡ a0000007-0005
@bind N Select([100, 1000, 5000, 20_000])

# ╔═╡ a0000007-0006
@bind seed NumberField(0:10_000, default=42)

# ╔═╡ a0000007-0007
md"## 2. Sample partitions"

# ╔═╡ a0000007-0008
# TODO(reader): for each of N samples,
#   q = rand Dirichlet(ones(m)); e = rand(m) * 0.5;
#   compute (ε(q,e), H(Y|Π)(q,e)).
# Collect into two N-vectors.

# ╔═╡ a0000007-0009
md"## 3. Scatter + envelopes"

# ╔═╡ a0000007-000a
# TODO(reader): scatter; overlay
#   upper envelope at uniform masses (notebook 05)
#   lower envelope = Hbin(ε)
# observe: every sample lies *between* the two envelopes.

# ╔═╡ a0000007-000b
md"""
## 4. Investigate

- TODO(reader): increase m. Does the cloud get denser near a boundary?
- TODO(reader): set m = 2. The cloud collapses to a 2D region with
  a sharp boundary — *the entire boundary IS the witness families
  from notebook 09*. Preview them now.

## 5. Next — Unit III, notebook 08: refinement monotonicity
"""

# ╔═╡ Cell order:
# ╠═a0000007-0001
# ╟─a0000007-0002
# ╟─a0000007-0003
# ╠═a0000007-0004
# ╠═a0000007-0005
# ╠═a0000007-0006
# ╟─a0000007-0007
# ╠═a0000007-0008
# ╟─a0000007-0009
# ╠═a0000007-000a
# ╟─a0000007-000b
