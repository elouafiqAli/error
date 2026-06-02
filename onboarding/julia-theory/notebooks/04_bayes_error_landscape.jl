### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Bayes-error landscape on a 3-cell partition"
#> tags = ["bracket", "unit-2"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a0000004-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a0000004-0000-0000-0000-000000000002
md"""
# Notebook 04 — Bayes-error landscape on a 3-cell partition

> **Unit II, building block 1.** Before the bracket of NB05, we
> compute its two operands on a hand-tunable 3-cell partition:
>
> - $\varepsilon(\Pi) = \sum_C q_C\, e_C$ — *linear* in the per-cell
>   errors;
> - $H(Y\mid\Pi) = \sum_C q_C\, H_{\mathrm{bin}}(e_C)$ — *concave*.
>
> The two quantities co-vary: slide a per-cell error and both move.
> The Exercises replicate this with 5-cell and 2-cell partitions.
"""

# ╔═╡ a0000004-0000-0000-0000-000000000003
Hbin(p::Real) = (p ≤ 0 || p ≥ 1) ? 0.0 : -p*log2(p) - (1-p)*log2(1-p)

# ╔═╡ a0000004-0000-0000-0000-000000000004
md"""
## 1. Sliders — two cell masses (the third is forced) and three per-cell errors
"""

# ╔═╡ a0000004-0000-0000-0000-000000000005
@bind q1 Slider(0.05:0.01:0.85, default=1/3, show_value=true)

# ╔═╡ a0000004-0000-0000-0000-000000000006
@bind q2 Slider(0.05:0.01:0.85, default=1/3, show_value=true)

# ╔═╡ a0000004-0000-0000-0000-000000000007
@bind e1 Slider(0.0:0.001:0.5, default=0.1, show_value=true)

# ╔═╡ a0000004-0000-0000-0000-000000000008
@bind e2 Slider(0.0:0.001:0.5, default=0.2, show_value=true)

# ╔═╡ a0000004-0000-0000-0000-000000000009
@bind e3 Slider(0.0:0.001:0.5, default=0.3, show_value=true)

# ╔═╡ a0000004-0000-0000-0000-00000000000a
md"""
## 2. Build the simplex point and compute the two operands
"""

# ╔═╡ a0000004-0000-0000-0000-00000000000b
begin
    q3_calc = 1.0 - q1 - q2
    valid_q = q3_calc ≥ 0.05
    q = [q1, q2, max(q3_calc, 0.0)]
    e = [e1, e2, e3]
    ε_of(q, e) = sum(q .* e)
    H_of(q, e) = sum(q .* Hbin.(e))
    εΠ = ε_of(q, e)
    HΠ = H_of(q, e)
    md"""
    | quantity | value |
    |---|---|
    | $q$ | $(round.(q; digits=4)) |
    | sum $= 1$? | $(isapprox(sum(q), 1.0; atol=1e-12)) |
    | $q_3 \ge 0.05$? | $(valid_q) |
    | $e$ | $(round.(e; digits=4)) |
    | $\varepsilon(\Pi)$ | $(round(εΠ; digits=4)) |
    | $H(Y\mid\Pi)$ (bits) | $(round(HΠ; digits=4)) |
    | $\varepsilon \le 1/2$ ? | $(εΠ ≤ 0.5 + 1e-12) |
    """
end

# ╔═╡ a0000004-0000-0000-0000-00000000000c
md"""
## 3. Linear vs concave — slide one $e_C$ and watch both move

Fix $q = (1/3, 1/3, 1/3)$ and $e_2 = e_3 = 0.25$; sweep $e_1$ from
$0$ to $1/2$. $\varepsilon(\Pi)$ traces a **straight line** of
slope $q_1 = 1/3$; $H(Y\mid\Pi)$ traces a **concave** curve
(weighted binary entropy of $e_1$).
"""

# ╔═╡ a0000004-0000-0000-0000-00000000000d
begin
    qs   = [1/3, 1/3, 1/3]
    e1s  = 0.0:0.001:0.5
    εs_e = [ε_of(qs, [u, 0.25, 0.25]) for u in e1s]
    Hs_e = [H_of(qs, [u, 0.25, 0.25]) for u in e1s]
    plot(e1s, εs_e; label = L"\varepsilon(\Pi)\ \mathrm{(linear)}",
         lw = 2, xlabel = L"e_1\ \mathrm{(others\ fixed\ at\ 0.25)}",
         ylabel = "value")
    plot!(e1s, Hs_e; label = L"H(Y\mid\Pi)\ \mathrm{(concave)}",
          lw = 2)
end

# ╔═╡ a0000004-0000-0000-0000-00000000000e
md"""
## 4. The achievable set (preview of NB05/07)

For *the current* $q$, sweep all three per-cell errors $e_C$
uniformly on $[0, 1/2]$ and scatter $(\varepsilon(\Pi), H(Y\mid\Pi))$.
You see a 2-D region. NB05 sandwiches it with two envelopes.
"""

# ╔═╡ a0000004-0000-0000-0000-00000000000f
let
    qfixed = [q1, q2, max(1.0 - q1 - q2, 0.05)]
    qfixed ./= sum(qfixed)
    N = 4000
    pts = [(sum(qfixed .* uu), sum(qfixed .* Hbin.(uu)))
           for uu in eachcol(rand(3, N) .* 0.5)]
    εs_ = [p[1] for p in pts]
    Hs_ = [p[2] for p in pts]
    scatter(εs_, Hs_; ms=2, ma=0.3, label="$(N) random e ∈ [0,1/2]³",
            xlabel=L"\varepsilon(\Pi)", ylabel=L"H(Y\mid\Pi)")
    scatter!([εΠ], [HΠ]; ms=8, c=:red, label="slider point")
end

# ╔═╡ a0000004-0000-0000-0000-000000000010
md"""
## 5. Falsify — what if you forget the $q$-weights?

A common student bug: compute $\frac{1}{m}\sum e_C$ (unweighted)
instead of $\sum q_C e_C$. Plot both against $q_1$ while keeping
$e = (0.1, 0.4, 0.4)$ and $q_2 = q_3 = (1-q_1)/2$. The unweighted
average is constant (because $e$ is fixed); the weighted average
moves linearly — they only agree on the uniform $q$.
"""

# ╔═╡ a0000004-0000-0000-0000-000000000011
begin
    e_fix    = [0.1, 0.4, 0.4]
    q1_grid  = 0.05:0.005:0.95
    weighted = [sum([q1v, (1-q1v)/2, (1-q1v)/2] .* e_fix) for q1v in q1_grid]
    naive    = fill(sum(e_fix)/3, length(q1_grid))
    plot(q1_grid, weighted; label = L"\sum q_C e_C\ \mathrm{(correct)}",
         lw = 2, xlabel = L"q_1\ (q_2=q_3=(1-q_1)/2)",
         ylabel = "value of average error")
    plot!(q1_grid, naive; label = L"(1/3)\sum e_C\ \mathrm{(naive)}",
          lw = 2, ls = :dash)
    vline!([1/3]; label = "uniform q", c=:gray, ls=:dot)
end

# ╔═╡ a0000004-0000-0000-0000-000000000012
md"""
## 6. Take-aways

- $\varepsilon(\Pi)$ is **linear** in $(q, e)$ when one is fixed.
- $H(Y\mid\Pi)$ is **concave** in $e$ for fixed $q$ (Jensen).
- The reachable region in $(\varepsilon, H)$ has *positive area*:
  there is no single curve relating the two; the **bracket** of
  NB05 names a *band* both must live in.
- Forgetting the $q$-weights is a classical bug (§5). All
  PSet/capstone code uses the weighted form.

## 7. Exercises
"""

# ╔═╡ a0000004-0000-0000-0000-000000000013
md"""
### E1. Replicate §3 with $q = (0.5, 0.3, 0.2)$

Sweep $e_1$; observe the slope of $\varepsilon$ is now $0.5$
(equal to $q_1$); $H$'s concavity is asymmetric.
"""

# ╔═╡ a0000004-0000-0000-0000-000000000014
let
    qE1   = [0.5, 0.3, 0.2]
    e1g   = 0.0:0.001:0.5
    εg    = [sum(qE1 .* [u, 0.25, 0.25]) for u in e1g]
    Hg    = [sum(qE1 .* Hbin.([u, 0.25, 0.25])) for u in e1g]
    plot(e1g, εg; lw=2, label=L"\varepsilon\ \mathrm{slope}=q_1=0.5")
    plot!(e1g, Hg; lw=2, label=L"H(Y\mid\Pi)")
    xlabel!(L"e_1"); ylabel!("value")
end

# ╔═╡ a0000004-0000-0000-0000-000000000015
md"""
### E2. Replicate §2 with $m = 5$ cells

Use $q = (0.2, 0.2, 0.2, 0.2, 0.2)$ and $e = (0.05, 0.1, 0.2, 0.3, 0.4)$;
print $\varepsilon$, $H$. The formulas extend by summation.
"""

# ╔═╡ a0000004-0000-0000-0000-000000000016
let
    q5 = fill(0.2, 5)
    e5 = [0.05, 0.10, 0.20, 0.30, 0.40]
    (ε = sum(q5 .* e5), H = sum(q5 .* Hbin.(e5)))
end

# ╔═╡ a0000004-0000-0000-0000-000000000017
md"""
### E3. Binary special case ($m = 2$)

With $q = (q_1, 1-q_1)$ and $e = (e_1, e_2)$, derive that
$H(Y\mid\Pi)$ achieves its maximum when both per-cell errors equal
$1/2$. Verify numerically by sweeping $(e_1, e_2)$.
"""

# ╔═╡ a0000004-0000-0000-0000-000000000018
let
    grid   = 0.0:0.02:0.5
    best_H = -Inf
    best_e = (0.0, 0.0)
    for u in grid, v in grid
        H = 0.5*Hbin(u) + 0.5*Hbin(v)
        if H > best_H
            best_H = H
            best_e = (u, v)
        end
    end
    (best_H = best_H, best_e = best_e)
end

# ╔═╡ a0000004-0000-0000-0000-000000000019
md"""
### E4. The reachable region for $q = (1, 0, 0)$ degenerates

If all mass sits in one cell, sweeping the other two $e$ values
does not change $(\varepsilon, H)$. Verify by re-doing §4 with
$q_1 = 0.9$. The scatter collapses toward a 1-D curve.
"""

# ╔═╡ a0000004-0000-0000-0000-00000000001a
let
    qE4 = [0.9, 0.05, 0.05]
    N   = 2000
    εs_ = Float64[]
    Hs_ = Float64[]
    for _ in 1:N
        uu = rand(3) .* 0.5
        push!(εs_, sum(qE4 .* uu))
        push!(Hs_, sum(qE4 .* Hbin.(uu)))
    end
    scatter(εs_, Hs_; ms=2, ma=0.3, label="degenerate q=(0.9,0.05,0.05)",
            xlabel=L"\varepsilon(\Pi)", ylabel=L"H(Y\mid\Pi)")
end

# ╔═╡ a0000004-0000-0000-0000-00000000001b
md"""
## 8. Next — NB05: the bracket envelope (centrepiece)
"""

# ╔═╡ Cell order:
# ╠═a0000004-0000-0000-0000-000000000001
# ╟─a0000004-0000-0000-0000-000000000002
# ╠═a0000004-0000-0000-0000-000000000003
# ╟─a0000004-0000-0000-0000-000000000004
# ╠═a0000004-0000-0000-0000-000000000005
# ╠═a0000004-0000-0000-0000-000000000006
# ╠═a0000004-0000-0000-0000-000000000007
# ╠═a0000004-0000-0000-0000-000000000008
# ╠═a0000004-0000-0000-0000-000000000009
# ╟─a0000004-0000-0000-0000-00000000000a
# ╠═a0000004-0000-0000-0000-00000000000b
# ╟─a0000004-0000-0000-0000-00000000000c
# ╠═a0000004-0000-0000-0000-00000000000d
# ╟─a0000004-0000-0000-0000-00000000000e
# ╠═a0000004-0000-0000-0000-00000000000f
# ╟─a0000004-0000-0000-0000-000000000010
# ╠═a0000004-0000-0000-0000-000000000011
# ╟─a0000004-0000-0000-0000-000000000012
# ╟─a0000004-0000-0000-0000-000000000013
# ╠═a0000004-0000-0000-0000-000000000014
# ╟─a0000004-0000-0000-0000-000000000015
# ╠═a0000004-0000-0000-0000-000000000016
# ╟─a0000004-0000-0000-0000-000000000017
# ╠═a0000004-0000-0000-0000-000000000018
# ╟─a0000004-0000-0000-0000-000000000019
# ╠═a0000004-0000-0000-0000-00000000001a
# ╟─a0000004-0000-0000-0000-00000000001b
