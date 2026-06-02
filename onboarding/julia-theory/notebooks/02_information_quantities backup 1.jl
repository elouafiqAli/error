### A Pluto.jl notebook ###
# v0.20.28

#> [frontmatter]
#> title = "Information quantities — H(X), H(Y|X), I(X;Y)"
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

# ╔═╡ ddddf6b2-5ec6-11f1-8cf3-91ec54122cf1
using PlutoUI, Plots, LaTeXStrings, Symbolics

# ╔═╡ ddde099a-5ec6-11f1-819a-1123b94dcba4
md"""
# Notebook 02 — Information quantities

> **Unit I, primitive 2.** Joint distributions $P(X,Y)$ on a 2×2
> table. Build entropy, conditional entropy, mutual information from
> scratch. Verify the chain rule on the page.
>
> **Punchline.** $H(X,Y) = H(X) + H(Y\mid X) = H(Y) + H(X\mid Y)$
> and $I(X;Y) = H(Y) - H(Y\mid X) \ge 0$ with equality iff $X \perp Y$.
"""

# ╔═╡ ddde0d82-5ec6-11f1-bc24-c1b7240818db
md"## 1. Joint distribution on a 2×2 table"

# ╔═╡ ddde0de6-5ec6-11f1-a384-59448d7b5372
md"""
Slide three of the four entries; the fourth is forced by sum-to-one.
"""

# ╔═╡ ddde0e72-5ec6-11f1-9d88-dbaf2dd224f1
@bind p00 Slider(0.0:0.01:1.0, default=0.4, show_value=true)

# ╔═╡ ddde0ec0-5ec6-11f1-83de-bd0b8882b6ed
@bind p01 Slider(0.0:0.01:1.0, default=0.1, show_value=true)

# ╔═╡ ddde0f08-5ec6-11f1-a4ff-6f2f5243900d
@bind p10 Slider(0.0:0.01:1.0, default=0.1, show_value=true)

# ╔═╡ ddde0f4e-5ec6-11f1-8040-ffbcc181eebc
# TODO(reader): build the 2×2 matrix P with P[2,2] = 1 - p00 - p01 - p10,
# and reject if any entry is negative.

# ╔═╡ ddde1002-5ec6-11f1-a99c-5bdd671ef946
md"## 2. Marginals, conditionals, and the IT primitives"

# ╔═╡ ddde1052-5ec6-11f1-9841-17e2df8d3436
# TODO(reader): from P, compute
#   PX = sum along Y axis
#   PY = sum along X axis
#   PY_given_X = P ./ PX (broadcast safely; guard zero)
# H(X), H(Y), H(X,Y), H(Y|X), I(X;Y).

# ╔═╡ ddde1142-5ec6-11f1-b8d8-59af97478572
md"## 3. Verify the chain rule"

# ╔═╡ ddde1234-5ec6-11f1-9c36-4fe0aef392b9
# TODO(reader): assert |H(X,Y) - (H(X) + H(Y|X))| < 1e-12
# and the symmetric variant. Print both sides.

# ╔═╡ ddde12aa-5ec6-11f1-8a26-7516929b847f
md"## 4. Slide to independence; watch I(X;Y) → 0"

# ╔═╡ ddde12f0-5ec6-11f1-9f58-fdf7e65e6c2a
# TODO(reader): set sliders so that P factorises as PX * PY^T (one click);
# show I(X;Y) ≈ 0. Then perturb one slider by 0.01 and watch MI grow.

# ╔═╡ ddde1408-5ec6-11f1-861a-d15398ef4637
md"## 5. Falsify — what if P has a negative entry?"

# ╔═╡ ddde1494-5ec6-11f1-8db8-d9de45ca631c
# TODO(reader): force P[1,1] = -0.05 and observe which IT quantities
# break (some become complex; some go negative; H(X,Y) underflows).

# ╔═╡ ddde1516-5ec6-11f1-af14-bfb0df84be25
md"""
## 6. Take-aways

- TODO(reader): write one line on *why* MI is symmetric ($I(X;Y) = I(Y;X)$).
- TODO(reader): write one line on *why* conditional entropy is not.

## 7. Next

Notebook **03 — Fano vs Hellman–Raviv**.
"""

# ╔═╡ Cell order:
# ╠═ddddf6b2-5ec6-11f1-8cf3-91ec54122cf1
# ╠═ddde099a-5ec6-11f1-819a-1123b94dcba4
# ╠═ddde0d82-5ec6-11f1-bc24-c1b7240818db
# ╠═ddde0de6-5ec6-11f1-a384-59448d7b5372
# ╠═ddde0e72-5ec6-11f1-9d88-dbaf2dd224f1
# ╠═ddde0ec0-5ec6-11f1-83de-bd0b8882b6ed
# ╠═ddde0f08-5ec6-11f1-a4ff-6f2f5243900d
# ╠═ddde0f4e-5ec6-11f1-8040-ffbcc181eebc
# ╠═ddde1002-5ec6-11f1-a99c-5bdd671ef946
# ╠═ddde1052-5ec6-11f1-9841-17e2df8d3436
# ╠═ddde1142-5ec6-11f1-b8d8-59af97478572
# ╠═ddde1234-5ec6-11f1-9c36-4fe0aef392b9
# ╠═ddde12aa-5ec6-11f1-8a26-7516929b847f
# ╠═ddde12f0-5ec6-11f1-9f58-fdf7e65e6c2a
# ╠═ddde1408-5ec6-11f1-861a-d15398ef4637
# ╠═ddde1494-5ec6-11f1-8db8-d9de45ca631c
# ╠═ddde1516-5ec6-11f1-af14-bfb0df84be25
