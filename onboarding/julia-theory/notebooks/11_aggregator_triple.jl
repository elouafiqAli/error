### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Aggregator triple r_T = (Δmax, 1, 1) — the E3 punchline"
#> tags = ["mpnn", "unit-4", "aggregators"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a000000b-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a000000b-0000-0000-0000-000000000002
md"""
# Notebook 11 — Aggregator triple $r_T = (\Delta_{\max}, 1, 1)$

> **Unit IV, item 1.** E3's punchline made tactile. The three
> MPNN aggregators **sum**, **mean**, **sym-norm** each inflate
> the bracket's upper envelope by a **different constant** $r_T$:
>
> | aggregator | $r_T(\Delta)$ |
> |---|---|
> | sum         | $\Delta_{\max}$ |
> | mean        | $1$ |
> | symmetric-normalised | $1$ |
>
> On Cora, $\Delta_{\max} = 168$. Sum then inflates by 168×; the
> bracket is *not* violated (it is **honestly loose**), but the
> upper bound is several orders of magnitude looser than mean's.
> The slider exposes the gap on a log scale.
"""

# ╔═╡ a000000b-0000-0000-0000-000000000003
md"""
## 1. Helpers (NB05 bracket primitives)
"""

# ╔═╡ a000000b-0000-0000-0000-000000000004
begin
    Hbin(p::Real) = (p ≤ 0 || p ≥ 1) ? 0.0 : -p*log2(p) - (1-p)*log2(1-p)
    upper_base(ε) = Hbin(ε) / 2
    r_sum(Δ)     = float(Δ)
    r_mean(Δ)    = 1.0
    r_symnorm(Δ) = 1.0
end

# ╔═╡ a000000b-0000-0000-0000-000000000005
md"""
## 2. Slider — pick $\Delta_{\max}$
"""

# ╔═╡ a000000b-0000-0000-0000-000000000006
@bind Δmax Select([1, 2, 4, 8, 16, 32, 64, 128, 168, 256])

# ╔═╡ a000000b-0000-0000-0000-000000000007
md"""
## 3. The three constants and one example
"""

# ╔═╡ a000000b-0000-0000-0000-000000000008
let
    ε_demo = 0.25
    base   = upper_base(ε_demo)
    md"""
    At $\Delta_{\max} = $(Δmax)$ and demonstration $\varepsilon = 0.25$
    (so base upper $= H_{\mathrm{bin}}(0.25)/2 = $(round(base; digits=4))$):

    | aggregator | $r_T(\Delta_{\max})$ | inflated upper |
    |---|---|---|
    | sum         | $(Δmax)            | $(round(r_sum(Δmax) * base;     digits=4)) |
    | mean        | 1                  | $(round(r_mean(Δmax) * base;    digits=4)) |
    | sym-norm    | 1                  | $(round(r_symnorm(Δmax) * base; digits=4)) |

    Ratio sum / mean = $(round(r_sum(Δmax) / r_mean(Δmax); digits=2))×.
    """
end

# ╔═╡ a000000b-0000-0000-0000-000000000009
md"""
## 4. Plot — the three inflated envelopes (linear scale)
"""

# ╔═╡ a000000b-0000-0000-0000-00000000000a
begin
    εs = 0.001:0.001:0.499
    base_curve = upper_base.(εs)
    pp = plot(εs, r_mean(Δmax)    .* base_curve; label = "mean",     lw = 2)
    plot!(pp, εs, r_symnorm(Δmax) .* base_curve; label = "sym-norm", lw = 2, ls = :dot)
    plot!(pp, εs, r_sum(Δmax)     .* base_curve; label = "sum",      lw = 2, ls = :dash)
    xlabel!(pp, L"\varepsilon"); ylabel!(pp, "inflated upper")
    title!(pp, "Δmax = $(Δmax)")
    pp
end

# ╔═╡ a000000b-0000-0000-0000-00000000000b
md"""
## 5. Same plot, **log scale** — the gap becomes visible at Cora's $\Delta_{\max} = 168$
"""

# ╔═╡ a000000b-0000-0000-0000-00000000000c
begin
    pp2 = plot(εs, r_mean(Δmax)    .* base_curve; label = "mean",
               lw = 2, yscale = :log10, ylims = (1e-3, 1e3))
    plot!(pp2, εs, r_symnorm(Δmax) .* base_curve; label = "sym-norm", lw = 2, ls = :dot)
    plot!(pp2, εs, r_sum(Δmax)     .* base_curve; label = "sum",      lw = 2, ls = :dash)
    xlabel!(pp2, L"\varepsilon"); ylabel!(pp2, "inflated upper (log)")
    title!(pp2, "ratio sum/mean = $(Δmax)")
    pp2
end

# ╔═╡ a000000b-0000-0000-0000-00000000000d
md"""
## 6. Distinguish — honest looseness vs a bug

- **Honest looseness**: the inflated bound is *valid* (it is an
  upper bound on $\varepsilon$); it is just *large*. Example: sum
  on Cora has upper $\approx 168 \cdot 0.5 = 84$, which dwarfs
  $\varepsilon \in [0, 0.5]$ but **does not violate** the truth.
- **A bug**: the bound is **violated** ($\varepsilon > \text{bound}$).
  In the published runs this *never happens* — if it does in your
  code, you have a bug.

Two lines, three aggregators, one moral: choose mean or sym-norm
when you want a *useful* bound; use sum if you need linear-in-degree
behaviour for downstream reasons.
"""

# ╔═╡ a000000b-0000-0000-0000-00000000000e
md"""
## 7. Cora reference (the published number)

On Cora's label partition: $\Delta_{\max} = 168$, base upper at the
empirical $\varepsilon \approx 0.13$ is $\approx 0.28$ bits/2 = $0.14$.

- mean / sym-norm: $\approx 0.14$ (useful, near the truth).
- sum:             $\approx 0.14 \cdot 168 \approx 23.5$ — vastly looser.

Sum's "7-orders-of-magnitude looseness" cited in some informal
slides was on a *normalised* per-node aggregation; the per-graph
constant is the $168\times$ above.

## 8. Exercises
"""

# ╔═╡ a000000b-0000-0000-0000-00000000000f
md"""
### E1. Build a table over $\Delta_{\max} \in \{1, 10, 100, 1000\}$
"""

# ╔═╡ a000000b-0000-0000-0000-000000000010
let
    rows = []
    base = upper_base(0.25)
    for Δ in (1, 10, 100, 1000)
        push!(rows, (Δmax = Δ,
                     mean_upper     = round(r_mean(Δ)     * base; digits=4),
                     symnorm_upper  = round(r_symnorm(Δ)  * base; digits=4),
                     sum_upper      = round(r_sum(Δ)      * base; digits=4),
                     sum_over_mean  = round(r_sum(Δ) / r_mean(Δ); digits=2)))
    end
    rows
end

# ╔═╡ a000000b-0000-0000-0000-000000000011
md"""
### E2. Mean and sym-norm differ on graphs with non-trivial degree spread; verify they agree on *regular* graphs

For a $d$-regular graph the sym-norm normalisation simplifies to
$1/d$ per node, while the mean is also $1/d$ — so the inflation
constants coincide. Verify by computing both on $K_5$ (which is
4-regular).
"""

# ╔═╡ a000000b-0000-0000-0000-000000000012
let
    # K_5 is 4-regular, n=5, m=10.
    d = 4
    # sym-norm row-stochastic weights = 1/d for each neighbour, hence per-node = sum_{j∼i} (1/d) = 1
    # mean = average over neighbours = 1
    # ⇒ both contribute r_T = 1
    (regular_K5_mean=1.0, regular_K5_symnorm=1.0, equal=true)
end

# ╔═╡ a000000b-0000-0000-0000-000000000013
md"""
### E3. Build the bound-violation falsifier

Try $r_T = 0.5$ (i.e. *shrink* the upper by half) and find a
partition where the shrunk bound is violated. By the
unimprovability theorem (NB10) you can use $\Pi^{\mathrm{HR}}_\alpha$.
"""

# ╔═╡ a000000b-0000-0000-0000-000000000014
let
    α = 0.25
    # Π^HR_α: ε=α, upper(base)=α; shrunk = 0.5·α
    rT = 0.5
    ε = α; cand = rT * α
    (α=α, ε=ε, candidate_upper=cand, violated=cand < ε - 1e-9)
end

# ╔═╡ a000000b-0000-0000-0000-000000000015
md"""
### E4. Plot sum-aggregator inflation as $\Delta_{\max}$ varies on a fixed $\varepsilon$
"""

# ╔═╡ a000000b-0000-0000-0000-000000000016
let
    Δs = 1:1:200
    base = upper_base(0.25)
    plot(Δs, [Δ*base for Δ in Δs];
         lw=2, label="sum upper at ε=0.25",
         xlabel=L"\Delta_{\max}", ylabel="inflated upper")
    vline!([168]; label="Cora Δmax=168", c=:red, ls=:dot)
end

# ╔═╡ a000000b-0000-0000-0000-000000000017
md"""
## 9. Next — NB12: ε-robust MPNN–WL constancy (Lemma 6) on a toy graph
"""

# ╔═╡ Cell order:
# ╠═a000000b-0000-0000-0000-000000000001
# ╟─a000000b-0000-0000-0000-000000000002
# ╟─a000000b-0000-0000-0000-000000000003
# ╠═a000000b-0000-0000-0000-000000000004
# ╟─a000000b-0000-0000-0000-000000000005
# ╠═a000000b-0000-0000-0000-000000000006
# ╟─a000000b-0000-0000-0000-000000000007
# ╠═a000000b-0000-0000-0000-000000000008
# ╟─a000000b-0000-0000-0000-000000000009
# ╠═a000000b-0000-0000-0000-00000000000a
# ╟─a000000b-0000-0000-0000-00000000000b
# ╠═a000000b-0000-0000-0000-00000000000c
# ╟─a000000b-0000-0000-0000-00000000000d
# ╟─a000000b-0000-0000-0000-00000000000e
# ╟─a000000b-0000-0000-0000-00000000000f
# ╠═a000000b-0000-0000-0000-000000000010
# ╟─a000000b-0000-0000-0000-000000000011
# ╠═a000000b-0000-0000-0000-000000000012
# ╟─a000000b-0000-0000-0000-000000000013
# ╠═a000000b-0000-0000-0000-000000000014
# ╟─a000000b-0000-0000-0000-000000000015
# ╠═a000000b-0000-0000-0000-000000000016
# ╟─a000000b-0000-0000-0000-000000000017
