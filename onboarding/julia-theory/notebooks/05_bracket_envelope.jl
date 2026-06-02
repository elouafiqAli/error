### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "The bracket envelope — centrepiece"
#> tags = ["bracket", "unit-2", "centrepiece"]

using Markdown, InteractiveUtils

# ╔═╡ a0000005-0001
using PlutoUI, Plots, LaTeXStrings, IntervalArithmetic

# ╔═╡ a0000005-0002
md"""
# Notebook 05 — The bracket envelope

> **Unit II, centrepiece.** This is the notebook the rest of the
> curriculum points at. Slide $\varepsilon$; watch the upper and
> lower envelopes; locate $w^*$.
>
> **Upper** (Theorem 1, upper side, via scalar Hellman–Raviv):
> $$\varepsilon \le \sum_C q_C \cdot 2 H_{\mathrm{bin}}^{-1}(2 e_C).$$
>
> **Lower** (Theorem 1, lower side, via Jensen):
> $$\varepsilon \ge H_{\mathrm{bin}}^{-1}\!\left(\sum_C q_C H_{\mathrm{bin}}(e_C)\right).$$
>
> **Slack**: their difference, $w(\Pi) = \mathrm{upper} - \mathrm{lower}$.
"""

# ╔═╡ a0000005-0003
md"## 1. `Hbin_inverse` — interval-arithmetic safe"

# ╔═╡ a0000005-0004
# TODO(reader): Hbin_inverse(h) on [0, 1/2] via bisection.
# Use IntervalArithmetic to bracket the answer; return midpoint of
# the final interval. Compare to a Roots.jl one-liner.

# ╔═╡ a0000005-0005
md"## 2. The bracket on a 5-cell uniform-mass family"

# ╔═╡ a0000005-0006
@bind ε Slider(0.0:0.001:0.5, default=0.2, show_value=true)

# ╔═╡ a0000005-0007
# TODO(reader):
#   m = 5; q = fill(1/m, m); e = fill(ε, m)
#   upper = sum(q .* 2 .* Hbin_inverse.(2 .* e))
#   lower = Hbin_inverse(sum(q .* Hbin.(e)))
#   slack = upper - lower
# print all three.

# ╔═╡ a0000005-0008
md"## 3. Plot upper, lower, slack across ε"

# ╔═╡ a0000005-0009
# TODO(reader): sweep ε ∈ [0, 0.5]; plot upper(ε), lower(ε), slack(ε)
# on a single axis; highlight the slider's current ε with a vline.

# ╔═╡ a0000005-000a
md"""
## 4. Find $w^*$ with the slider

Move the slider until the slack curve hits its visual maximum. You
should land near $\varepsilon^* = 0.2$ with slack $w^* \approx 0.161$.

The next notebook (06) automates this with `Optim.jl` and confirms
the value to 6 decimals.
"""

# ╔═╡ a0000005-000b
md"## 5. Falsify — change ½ to ⅓ in the upper envelope"

# ╔═╡ a0000005-000c
# TODO(reader): mutate upper to use (1/3) instead of 2 (i.e. drop
# the factor of 2). Plot alongside the original. The mutated upper
# crosses below a Hellman–Raviv-saturating witness — to be made
# explicit in notebook 09.

# ╔═╡ a0000005-000d
md"## 6. Next — Notebook 06: locate $w^*$ with Optim and Symbolics"

# ╔═╡ Cell order:
# ╠═a0000005-0001
# ╟─a0000005-0002
# ╟─a0000005-0003
# ╠═a0000005-0004
# ╟─a0000005-0005
# ╠═a0000005-0006
# ╠═a0000005-0007
# ╟─a0000005-0008
# ╠═a0000005-0009
# ╟─a0000005-000a
# ╟─a0000005-000b
# ╠═a0000005-000c
# ╟─a0000005-000d
