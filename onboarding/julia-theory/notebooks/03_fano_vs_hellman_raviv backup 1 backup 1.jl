### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Fano vs Hellman–Raviv"
#> tags = ["information-theory", "primitives", "unit-1"]

using Markdown, InteractiveUtils

# ╔═╡ a0000003-0001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a0000003-0002
md"""
# Notebook 03 — Fano vs Hellman–Raviv

> **Unit I, primitive 3.** Two bounds, two sliders. One holds on
> $K$ classes (Fano); one is tighter on $K = 2$ but does not lift
> as cleanly (Hellman–Raviv).
>
> **Distinguish cell at the end.** Two-line X-vs-Y between the two
> inequalities.
"""

# ╔═╡ a0000003-0003
md"## 1. Sliders"

# ╔═╡ a0000003-0004
@bind ε Slider(0.0:0.001:0.5, default=0.2, show_value=true)

# ╔═╡ a0000003-0005
@bind K Select([2, 3, 4, 5, 10])

# ╔═╡ a0000003-0006
md"## 2. The two bounds"

# ╔═╡ a0000003-0007
# TODO(reader):
#   Hbin(x) as in notebook 01
#   Fano_bound(ε, K) = Hbin(ε) + ε * log2(K - 1)        # bound on H(Y|Ŷ)
#   HR_inverted(ε)   = ε ≤ 0.5 * Hbin(ε)                # bound on ε itself, K=2 only
# Print both at the current (ε, K).

# ╔═╡ a0000003-0008
md"## 3. Plot — both bounds across ε for the selected K"

# ╔═╡ a0000003-0009
# TODO(reader): two-panel plot
#   left: Fano upper bound on H(Y|Ŷ) as a function of ε for current K
#   right: HR upper bound on ε; overlay the trivial bound ε ≤ 1/2.

# ╔═╡ a0000003-000a
md"## 4. Distinguish (text cell)"

# ╔═╡ a0000003-000b
md"""
**Fano** bounds $H(Y\mid\hat Y)$ *from above*, in terms of the
classifier's error $\varepsilon$ and the class count $K$. It tells
you: if you make few mistakes, the residual uncertainty in $Y$ is
small.

**Hellman–Raviv (binary)** bounds $\varepsilon$ *from above*, in
terms of $H_{\mathrm{bin}}(\varepsilon)$ itself. It tells you: the
minimum-error classifier cannot do better than half the binary
entropy of its own error.

- TODO(reader): in two more lines, name what *fails* if you try to
  use HR for $K = 3$.
"""

# ╔═╡ a0000003-000c
md"## 5. Next — Unit II: Bayes error on a partition"

# ╔═╡ Cell order:
# ╠═a0000003-0001
# ╟─a0000003-0002
# ╟─a0000003-0003
# ╠═a0000003-0004
# ╠═a0000003-0005
# ╟─a0000003-0006
# ╠═a0000003-0007
# ╟─a0000003-0008
# ╠═a0000003-0009
# ╟─a0000003-000a
# ╟─a0000003-000b
# ╟─a0000003-000c
