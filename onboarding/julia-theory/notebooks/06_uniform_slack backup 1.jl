### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Uniform slack w* and the critical point ε*=1/5"
#> tags = ["bracket", "unit-2", "optimisation"]

using Markdown, InteractiveUtils

# ╔═╡ a0000006-0001
using PlutoUI, Plots, LaTeXStrings, Symbolics, Optim

# ╔═╡ a0000006-0002
md"""
# Notebook 06 — Uniform slack $w^*$ and $\varepsilon^* = 1/5$

> **Unit II, payoff.** Auto-locate Corollary 2's constant using
> three independent paths and confirm they agree.
>
> **Three paths**:
> 1. `Optim.jl` Brent's method on the slack function;
> 2. `Symbolics.jl` derivative + root-find on $w'(\varepsilon^*) = 0$;
> 3. (Appendix A) `Enzyme.jl` forward-mode AD — same answer.
"""

# ╔═╡ a0000006-0003
md"## 1. Slack function (from notebook 05)"

# ╔═╡ a0000006-0004
# TODO(reader): reuse Hbin and Hbin_inverse; define
#   w(ε) = upper(ε; m=5, uniform) - lower(ε; m=5, uniform)

# ╔═╡ a0000006-0005
md"## 2. Path 1 — `Optim.jl` Brent's method"

# ╔═╡ a0000006-0006
# TODO(reader): optimize(ε -> -w(ε), 0.05, 0.45, Brent())
# extract Optim.minimizer; should be ≈ 0.2.

# ╔═╡ a0000006-0007
md"## 3. Path 2 — symbolic derivative"

# ╔═╡ a0000006-0008
# TODO(reader):
#   @variables ε_sym
#   w_sym = (build the symbolic version of w on the uniform family)
#   w_prime_sym = simplify(Symbolics.derivative(w_sym, ε_sym))
#   w_prime_fn = eval(build_function(w_prime_sym, ε_sym; expression=Val{false}))
#   find_zero(w_prime_fn, 0.2) using Roots.jl OR a simple bisection.

# ╔═╡ a0000006-0009
md"## 4. Cross-check both paths"

# ╔═╡ a0000006-000a
# TODO(reader): assert abs(eps_star_optim - eps_star_symbolic) < 1e-6;
# print w_star to 6 decimals; verify ≈ 0.161043.

# ╔═╡ a0000006-000b
md"## 5. Visualise"

# ╔═╡ a0000006-000c
# TODO(reader): plot w(ε); mark eps_star with a vline + scatter; annotate w_star.

# ╔═╡ a0000006-000d
md"""
## 6. Read Corollary 2 now

After running, *now* open the paper to Corollary 2 (cor:slack). The
constant you just produced is the one it states. The notebook is the
pre-reading; the paper is the post-reading.

## 7. Next — Notebook 07: the achievable region scatter
"""

# ╔═╡ Cell order:
# ╠═a0000006-0001
# ╟─a0000006-0002
# ╟─a0000006-0003
# ╠═a0000006-0004
# ╟─a0000006-0005
# ╠═a0000006-0006
# ╟─a0000006-0007
# ╠═a0000006-0008
# ╟─a0000006-0009
# ╠═a0000006-000a
# ╟─a0000006-000b
# ╠═a0000006-000c
# ╟─a0000006-000d
