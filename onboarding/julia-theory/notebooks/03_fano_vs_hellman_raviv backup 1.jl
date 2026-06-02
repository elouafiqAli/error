### A Pluto.jl notebook ###
# v0.20.28

#> [frontmatter]
#> title = "Fano vs Hellman–Raviv"
#> tags = ["information-theory", "primitives", "unit-1"]

using Markdown
using InteractiveUtils

# This Pluto notebook uses @bind for interactivity. When running this notebook outside of Pluto, the following 'mock version' of @bind gives bound variables a default value (instead of an error).
macro bind(def, element)
    #! format: off
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
    #! format: on
end

# ╔═╡ 30fe0afc-5ec8-11f1-a0b7-5df412edcc9e
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ 3100772e-5ec8-11f1-be04-51e2447d3514
md"""
# Notebook 03 — Fano vs Hellman–Raviv

> **Unit I, primitive 3.** Two bounds, two sliders. One holds on
> $K$ classes (Fano); one is tighter on $K = 2$ but does not lift
> as cleanly (Hellman–Raviv).
>
> **Distinguish cell at the end.** Two-line X-vs-Y between the two
> inequalities.
"""

# ╔═╡ 31007a4e-5ec8-11f1-88ab-6b9524df18b0
md"## 1. Sliders"

# ╔═╡ 31007a9e-5ec8-11f1-bae7-f59f348d52b1
@bind ε Slider(0.0:0.001:0.5, default=0.2, show_value=true)

# ╔═╡ 31007ae4-5ec8-11f1-9699-6966d34c2c94
@bind K Select([2, 3, 4, 5, 10])

# ╔═╡ 31007b70-5ec8-11f1-bf3d-59e7ec9b6032
md"## 2. The two bounds"

# ╔═╡ 31007bae-5ec8-11f1-8584-670e59663e2c
# TODO(reader):
#   Hbin(x) as in notebook 01
#   Fano_bound(ε, K) = Hbin(ε) + ε * log2(K - 1)        # bound on H(Y|Ŷ)
#   HR_inverted(ε)   = ε ≤ 0.5 * Hbin(ε)                # bound on ε itself, K=2 only
# Print both at the current (ε, K).

# ╔═╡ 310081ec-5ec8-11f1-b4e4-63dc07650bb9
md"## 3. Plot — both bounds across ε for the selected K"

# ╔═╡ 310082a0-5ec8-11f1-b006-35ba277d168c
# TODO(reader): two-panel plot
#   left: Fano upper bound on H(Y|Ŷ) as a function of ε for current K
#   right: HR upper bound on ε; overlay the trivial bound ε ≤ 1/2.

# ╔═╡ 31008390-5ec8-11f1-bb7a-ad3ed7d413fe
md"## 4. Distinguish (text cell)"

# ╔═╡ 310083d6-5ec8-11f1-b24f-27df5f9498c2
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

# ╔═╡ 310085de-5ec8-11f1-b126-2f0319696c71
md"## 5. Next — Unit II: Bayes error on a partition"

# ╔═╡ Cell order:
# ╠═30fe0afc-5ec8-11f1-a0b7-5df412edcc9e
# ╠═3100772e-5ec8-11f1-be04-51e2447d3514
# ╠═31007a4e-5ec8-11f1-88ab-6b9524df18b0
# ╠═31007a9e-5ec8-11f1-bae7-f59f348d52b1
# ╠═31007ae4-5ec8-11f1-9699-6966d34c2c94
# ╠═31007b70-5ec8-11f1-bf3d-59e7ec9b6032
# ╠═31007bae-5ec8-11f1-8584-670e59663e2c
# ╠═310081ec-5ec8-11f1-b4e4-63dc07650bb9
# ╠═310082a0-5ec8-11f1-b006-35ba277d168c
# ╠═31008390-5ec8-11f1-bb7a-ad3ed7d413fe
# ╠═310083d6-5ec8-11f1-b24f-27df5f9498c2
# ╠═310085de-5ec8-11f1-b126-2f0319696c71
