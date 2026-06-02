### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Unimprovability (Prop 7) — live"
#> tags = ["bracket", "unit-3", "unimprovability"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a000000a-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a000000a-0000-0000-0000-000000000002
md"""
# Notebook 10 — Unimprovability of the upper envelope

> **Unit III, item 3.** The upper envelope $\mathrm{up}(\Pi) = H/2$
> is **unimprovable**: no multiplicative shrinking factor $\beta < 1$
> can replace the $1/2$ without making the bound *fail* on some
> partition. The witness family $\Pi^{\mathrm{HR}}_\alpha$ from
> NB09 is the **named refuter** — slide $\beta$ down and watch
> $\beta \cdot H/2$ fall *below* $\varepsilon$ on the witness.
"""

# ╔═╡ a000000a-0000-0000-0000-000000000003
md"""
## 1. Helpers + the witness
"""

# ╔═╡ a000000a-0000-0000-0000-000000000004
begin
    Hbin(p::Real) = (p ≤ 0 || p ≥ 1) ? 0.0 : -p*log2(p) - (1-p)*log2(1-p)
    Π_HR(α) = ([1 - 2α, 2α], [0.0, 0.5])
    bracket_at(q, e) = (ε = sum(q .* e),
                        H = sum(q .* Hbin.(e)),
                        upper = sum(q .* Hbin.(e)) / 2)
end

# ╔═╡ a000000a-0000-0000-0000-000000000005
md"""
## 2. Slider — proposed shrink factor $\beta$
"""

# ╔═╡ a000000a-0000-0000-0000-000000000006
@bind β Slider(0.50:0.001:1.05, default=0.95, show_value=true)

# ╔═╡ a000000a-0000-0000-0000-000000000007
md"""
## 3. The candidate "improved" upper bound

Candidate: $\mathrm{up}_\beta(\Pi) := \beta \cdot H(Y\mid\Pi) / 2$.
If $\beta = 1$ we recover the genuine upper. If $\beta < 1$ we have
a **strictly tighter** candidate bound. We compute the *gap*
$\beta \cdot H/2 - \varepsilon$ on $\Pi^{\mathrm{HR}}_\alpha$ as
$\alpha$ varies. A negative gap = the candidate bound is **below**
the true $\varepsilon$ = the candidate **fails**.
"""

# ╔═╡ a000000a-0000-0000-0000-000000000008
begin
    αs = 0.001:0.001:0.499
    gap_HR = Float64[]
    for αi in αs
        b = bracket_at(Π_HR(αi)...)
        push!(gap_HR, β * b.upper - b.ε)
    end
    min_gap   = minimum(gap_HR)
    α_violate = αs[argmin(gap_HR)]
    md"""
    With $\beta = $(round(β; digits=4))$:
    - minimum of $\beta \cdot H/2 - \varepsilon$ on the HR witness: $(round(min_gap; digits=6))
    - achieved at $\alpha = $(round(α_violate; digits=4))$
    - candidate **fails**? $(min_gap < -1e-9)
    """
end

# ╔═╡ a000000a-0000-0000-0000-000000000009
md"""
## 4. Plot — the candidate vs the witness's $\varepsilon$
"""

# ╔═╡ a000000a-0000-0000-0000-00000000000a
begin
    HR_ε = αs                                        # by construction ε(HR_α) = α
    HR_upper_true   = αs                             # H/2 = α
    HR_upper_cand   = β .* HR_upper_true             # β·H/2
    pp = plot(αs, HR_ε; label = L"\varepsilon(\Pi^{\mathrm{HR}}_\alpha) = \alpha",
              lw = 2, c = :black, xlabel = L"\alpha",
              ylabel = L"\mathrm{value}")
    plot!(pp, αs, HR_upper_true; label = L"\mathrm{true\ upper}\ =\ \alpha",
          lw = 2, c = :blue, ls = :dot)
    plot!(pp, αs, HR_upper_cand;
          label = L"\beta \cdot \mathrm{upper}\ \mathrm{(candidate)}",
          lw = 2, c = :red, ls = :dash)
    # Highlight any region where candidate < ε
    viol_mask = HR_upper_cand .< HR_ε .- 1e-12
    if any(viol_mask)
        viol_αs = αs[viol_mask]
        scatter!(pp, viol_αs, HR_ε[viol_mask];
                 label = "violations", ms = 2, c = :red)
    end
    title!(pp, β < 1 ? "candidate fails everywhere" : "no improvement: β ≥ 1")
    pp
end

# ╔═╡ a000000a-0000-0000-0000-00000000000b
md"""
## 5. Robust assertion — for any $\beta < 1$, the candidate fails
"""

# ╔═╡ a000000a-0000-0000-0000-00000000000c
let
    failed_for_all_β_less_than_1 = true
    for βtest in (0.5, 0.7, 0.9, 0.99, 0.999)
        # any α > 0 produces ε = α > β·α = candidate
        αtest = 0.1
        b = bracket_at(Π_HR(αtest)...)
        cand = βtest * b.upper
        if !(cand < b.ε - 1e-12)
            failed_for_all_β_less_than_1 = false
        end
    end
    md"""
    For every $\beta \in \{0.5, 0.7, 0.9, 0.99, 0.999\}$ the
    HR witness with $\alpha = 0.1$ refutes the candidate.
    Confirmed: $(failed_for_all_β_less_than_1).
    """
end

# ╔═╡ a000000a-0000-0000-0000-00000000000d
md"""
## 6. The lesson

> "Tightness witnesses are the verification you owe before
> announcing an improvement." — PLAN.md §11c, generalised.

If you propose to sharpen the bracket's upper bound by a
multiplicative factor — or by any other transformation — the
witness you must defeat is **named in the paper**. The slider
lets you stress-test any candidate sharpening before publishing
it. Failing to consult the witness is the most common
reviewer-side rejection.

## 7. Exercises — replicate
"""

# ╔═╡ a000000a-0000-0000-0000-00000000000e
md"""
### E1. Try an **additive** sharpening: $\mathrm{up}_\delta(\Pi) = H/2 - \delta$

For $\delta > 0$ the candidate is shifted down. It still fails on
the HR witness at small $\alpha$: $\mathrm{up}_\delta = \alpha - \delta < \alpha = \varepsilon$
whenever $\alpha < \delta$. Plot to verify.
"""

# ╔═╡ a000000a-0000-0000-0000-00000000000f
let
    δ = 0.05
    αs_E1 = 0.001:0.001:0.499
    cand  = αs_E1 .- δ
    plot(αs_E1, αs_E1; label=L"\varepsilon = \alpha", lw=2, c=:black)
    plot!(αs_E1, cand; label=L"\mathrm{up}_\delta = H/2 - \delta", lw=2, c=:red, ls=:dash)
    vline!([δ]; label="break at α = δ", c=:gray, ls=:dot)
    xlabel!(L"\alpha"); title!("additive sharpening fails for α < δ")
end

# ╔═╡ a000000a-0000-0000-0000-000000000010
md"""
### E2. Try a **power** sharpening: $\mathrm{up}_p(\Pi) = (H/2)^p$ for $p > 1$

For $p > 1$, $(H/2)^p < H/2$ on $H/2 \in (0, 1)$ — strictly
tighter. Show it fails on the HR witness at small $\alpha$
(where $H/2 = \alpha$ is small, so $\alpha^p \ll \alpha$).
"""

# ╔═╡ a000000a-0000-0000-0000-000000000011
let
    p = 1.5
    αs_E2 = 0.001:0.001:0.499
    cand  = αs_E2 .^ p
    plot(αs_E2, αs_E2; label=L"\varepsilon = \alpha", lw=2, c=:black)
    plot!(αs_E2, cand; label=L"\mathrm{up}_p = (H/2)^p,\ p=1.5", lw=2, c=:red, ls=:dash)
    xlabel!(L"\alpha"); title!("power sharpening fails at small α")
end

# ╔═╡ a000000a-0000-0000-0000-000000000012
md"""
### E3. Replicate the §3 calculation for $\Pi^{\mathrm{HR}}_{0.25}$, $\beta = 0.9$

By hand: $\varepsilon = 0.25$, $H = 0.5$, $\beta \cdot H/2 = 0.225$.
Gap $= 0.225 - 0.25 = -0.025 < 0$ ⇒ candidate fails. Confirm
numerically.
"""

# ╔═╡ a000000a-0000-0000-0000-000000000013
let
    α = 0.25; βt = 0.9
    b = bracket_at(Π_HR(α)...)
    cand = βt * b.upper
    (ε=b.ε, upper=b.upper, candidate=cand, gap=cand - b.ε,
     fails=cand < b.ε)
end

# ╔═╡ a000000a-0000-0000-0000-000000000014
md"""
### E4. The **lower** envelope is also unimprovable — refute $H_{\mathrm{bin}}^{-1}(\gamma H)$ for $\gamma > 1$

If you try to push the lower envelope *up* by replacing $H$ with
$\gamma H$ for $\gamma > 1$, you get a tighter-looking lower
bound; the J witness $\Pi^{\mathrm{J}}_\alpha$ refutes it because
$H_{\mathrm{bin}}^{-1}(\gamma H_{\mathrm{bin}}(\alpha)) > \alpha = \varepsilon$
for any $\gamma > 1$ (on the increasing branch).
"""

# ╔═╡ a000000a-0000-0000-0000-000000000015
let
    function Hbin_inv(h; tol=1e-12)
        h ≤ 0 && return 0.0
        h ≥ 1 && return 0.5
        lo, hi = 0.0, 0.5
        while hi - lo > tol
            mid = 0.5*(lo + hi)
            Hbin(mid) < h ? (lo = mid) : (hi = mid)
        end
        0.5*(lo + hi)
    end
    γ = 1.05
    α = 0.2
    H_J = Hbin(α)
    cand_lower = Hbin_inv(min(γ*H_J, 1.0))
    (α=α, H=H_J, true_lower=α, cand_lower=cand_lower,
     fails=cand_lower > α + 1e-9)
end

# ╔═╡ a000000a-0000-0000-0000-000000000016
md"""
## 8. Next — Unit IV: aggregator triple on Cora (NB11)
"""

# ╔═╡ Cell order:
# ╠═a000000a-0000-0000-0000-000000000001
# ╟─a000000a-0000-0000-0000-000000000002
# ╟─a000000a-0000-0000-0000-000000000003
# ╠═a000000a-0000-0000-0000-000000000004
# ╟─a000000a-0000-0000-0000-000000000005
# ╠═a000000a-0000-0000-0000-000000000006
# ╟─a000000a-0000-0000-0000-000000000007
# ╠═a000000a-0000-0000-0000-000000000008
# ╟─a000000a-0000-0000-0000-000000000009
# ╠═a000000a-0000-0000-0000-00000000000a
# ╟─a000000a-0000-0000-0000-00000000000b
# ╠═a000000a-0000-0000-0000-00000000000c
# ╟─a000000a-0000-0000-0000-00000000000d
# ╟─a000000a-0000-0000-0000-00000000000e
# ╠═a000000a-0000-0000-0000-00000000000f
# ╟─a000000a-0000-0000-0000-000000000010
# ╠═a000000a-0000-0000-0000-000000000011
# ╟─a000000a-0000-0000-0000-000000000012
# ╠═a000000a-0000-0000-0000-000000000013
# ╟─a000000a-0000-0000-0000-000000000014
# ╠═a000000a-0000-0000-0000-000000000015
# ╟─a000000a-0000-0000-0000-000000000016
