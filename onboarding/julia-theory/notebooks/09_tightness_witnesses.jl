### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Tightness witnesses Π^HR and Π^J"
#> tags = ["bracket", "unit-3", "witnesses"]

using Markdown, InteractiveUtils

# ╔═╡ a0000009-0001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a0000009-0002
md"""
# Notebook 09 — Tightness witnesses

> **Unit III, item 2.** The boundary of the achievable region from
> notebook 07 is traced out by two explicit partition families:
> $\Pi_\alpha^{\mathrm{HR}}$ (saturates the upper, Hellman–Raviv
> side) and $\Pi_\alpha^{\mathrm{J}}$ (saturates the lower, Jensen
> side). Slide $\alpha$ and watch the boundary trace.
"""

# ╔═╡ a0000009-0003
md"## 1. Slider"

# ╔═╡ a0000009-0004
@bind α Slider(0.0:0.001:1.0, default=0.5, show_value=true)

# ╔═╡ a0000009-0005
md"## 2. Build the two witness families"

# ╔═╡ a0000009-0006
# TODO(reader): define Π_HR(α) and Π_J(α) — see paper §"Tightness witnesses".
# Each returns (q, e). For each, compute (ε, H(Y|Π)).

# ╔═╡ a0000009-0007
md"## 3. Overlay on the scatter from notebook 07"

# ╔═╡ a0000009-0008
# TODO(reader): redo the scatter (or load N=20_000 points from notebook 07),
# overlay the parametric curves Π_HR(α) and Π_J(α) for α ∈ [0, 1].
# Mark the current α with two large dots.

# ╔═╡ a0000009-0009
md"""
## 4. The reading

The cloud's *upper* edge IS Π^HR; its *lower* edge IS Π^J. There
is no third family — any proposed boundary curve would have to
match one of these two, which is the Prop 7 (unimprovability)
argument made visual.

## 5. Next — Notebook 10: unimprovability live
"""

# ╔═╡ Cell order:
# ╠═a0000009-0001
# ╟─a0000009-0002
# ╟─a0000009-0003
# ╠═a0000009-0004
# ╟─a0000009-0005
# ╠═a0000009-0006
# ╟─a0000009-0007
# ╠═a0000009-0008
# ╟─a0000009-0009
