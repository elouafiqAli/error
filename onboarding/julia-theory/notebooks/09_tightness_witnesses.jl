### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Tightness witnesses Π^HR and Π^J"
#> tags = ["bracket", "unit-3", "witnesses"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a0000009-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings, Random

# ╔═╡ a0000009-0000-0000-0000-000000000002
md"""
# Notebook 09 — Tightness witnesses

> **Unit III, item 2.** The bracket's two envelopes — lower
> $\mathrm{lo}(\Pi) = H_{\mathrm{bin}}^{-1}(H(Y\mid\Pi))$ and
> upper $\mathrm{up}(\Pi) = H(Y\mid\Pi)/2$ — are each **achieved
> with equality** by an explicit family of partitions.
>
> - $\Pi^{\mathrm{HR}}_\alpha$ (Hellman–Raviv side): a 2-cell
>   partition with mass $(1-2\alpha, 2\alpha)$ and per-cell errors
>   $(0, 1/2)$. Yields $\varepsilon = \alpha$, $H = 2\alpha$, and
>   $\mathrm{up}(\Pi) = H/2 = \alpha = \varepsilon$ ⇒ **upper tight**.
> - $\Pi^{\mathrm{J}}_\alpha$ (Jensen side): a 1-cell partition
>   with per-cell error $\alpha$. Yields $\varepsilon = \alpha$,
>   $H = H_{\mathrm{bin}}(\alpha)$, $\mathrm{lo}(\Pi) = H_{\mathrm{bin}}^{-1}(H) = \alpha = \varepsilon$
>   ⇒ **lower tight** (and trivially also upper-tight is *not* the
>   case unless $\alpha = 0$ or $\alpha = 1/2$).
>
> NB07's scatter cloud's *boundary* IS traced exactly by these two
> families.
"""

# ╔═╡ a0000009-0000-0000-0000-000000000003
md"""
## 1. Helpers
"""

# ╔═╡ a0000009-0000-0000-0000-000000000004
begin
    Hbin(p::Real) = (p ≤ 0 || p ≥ 1) ? 0.0 : -p*log2(p) - (1-p)*log2(1-p)
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
end

# ╔═╡ a0000009-0000-0000-0000-000000000005
md"""
## 2. The two witness families (closed-form, **no slider needed for the math**)
"""

# ╔═╡ a0000009-0000-0000-0000-000000000006
begin
    # Π^HR_α: q = (1-2α, 2α), e = (0, 1/2). ε = α, H = 2α (bits).
    Π_HR(α) = ([1 - 2α, 2α], [0.0, 0.5])

    # Π^J_α: q = (1,), e = (α,). ε = α, H = Hbin(α).
    Π_J(α)  = ([1.0],          [α])

    bracket_at(q, e) = (ε     = sum(q .* e),
                        H     = sum(q .* Hbin.(e)),
                        lower = Hbin_inv(sum(q .* Hbin.(e))),
                        upper = sum(q .* Hbin.(e)) / 2)
end

# ╔═╡ a0000009-0000-0000-0000-000000000007
md"""
## 3. Verify tightness symbolically (== floating point) at $\alpha = 0.25$
"""

# ╔═╡ a0000009-0000-0000-0000-000000000008
let
    α = 0.25
    bHR = bracket_at(Π_HR(α)...)
    bJ  = bracket_at(Π_J(α)...)
    md"""
    | family | $\varepsilon$ | $H$ | lower | upper | upper-tight? | lower-tight? |
    |---|---|---|---|---|---|---|
    | $\Pi^{\mathrm{HR}}_{0.25}$ | $(round(bHR.ε; digits=6)) | $(round(bHR.H; digits=6)) | $(round(bHR.lower; digits=6)) | $(round(bHR.upper; digits=6)) | $(isapprox(bHR.upper, bHR.ε; atol=1e-9)) | $(isapprox(bHR.lower, bHR.ε; atol=1e-9)) |
    | $\Pi^{\mathrm{J}}_{0.25}$  | $(round(bJ.ε;  digits=6)) | $(round(bJ.H;  digits=6)) | $(round(bJ.lower;  digits=6)) | $(round(bJ.upper;  digits=6)) | $(isapprox(bJ.upper,  bJ.ε;  atol=1e-9)) | $(isapprox(bJ.lower,  bJ.ε;  atol=1e-9)) |
    """
end

# ╔═╡ a0000009-0000-0000-0000-000000000009
md"""
## 4. Slider — trace both witnesses across $\alpha$
"""

# ╔═╡ a0000009-0000-0000-0000-00000000000a
@bind α Slider(0.001:0.001:0.5, default=0.2, show_value=true)

# ╔═╡ a0000009-0000-0000-0000-00000000000b
begin
    bHR_α = bracket_at(Π_HR(α)...)
    bJ_α  = bracket_at(Π_J(α)...)
    md"""
    At $\alpha = $(round(α; digits=3))$:
    - $\Pi^{\mathrm{HR}}$: $\varepsilon = $(round(bHR_α.ε; digits=4))$, $H = $(round(bHR_α.H; digits=4))$, upper-tight gap = $(round(bHR_α.upper - bHR_α.ε; digits=8))
    - $\Pi^{\mathrm{J}}$:  $\varepsilon = $(round(bJ_α.ε;  digits=4))$, $H = $(round(bJ_α.H;  digits=4))$, lower-tight gap = $(round(bJ_α.ε - bJ_α.lower; digits=8))
    """
end

# ╔═╡ a0000009-0000-0000-0000-00000000000c
md"""
## 5. Overlay both families on the achievable region scatter (NB07)
"""

# ╔═╡ a0000009-0000-0000-0000-00000000000d
begin
    rng_loc = MersenneTwister(42)
    Nx = 4000
    εs_ = Float64[]; Hs_ = Float64[]
    for _ in 1:Nx
        m = 5
        raw = randexp(rng_loc, m)
        q   = raw ./ sum(raw)
        e   = rand(rng_loc, m) .* 0.5
        push!(εs_, sum(q .* e))
        push!(Hs_, sum(q .* Hbin.(e)))
    end
    αs = 0.001:0.001:0.5
    HRεs = [bracket_at(Π_HR(αi)...).ε for αi in αs]
    HRHs = [bracket_at(Π_HR(αi)...).H for αi in αs]
    Jεs  = [bracket_at(Π_J(αi)...).ε  for αi in αs]
    JHs  = [bracket_at(Π_J(αi)...).H  for αi in αs]

    pp = scatter(εs_, Hs_; ms=2, ma=0.25, label="$(Nx) random Π (m=5)",
                 xlabel=L"\varepsilon(\Pi)", ylabel=L"H(Y\mid\Pi)",
                 legend=:topleft)
    plot!(pp, HRεs, HRHs; label=L"\Pi^{\mathrm{HR}}_\alpha\ \mathrm{(upper\ edge)}", lw=3, c=:red)
    plot!(pp, Jεs,  JHs;  label=L"\Pi^{\mathrm{J}}_\alpha\ \mathrm{(lower\ edge)}",  lw=3, c=:black)
    scatter!(pp, [bHR_α.ε], [bHR_α.H]; ms=8, c=:red,   label="α slider (HR)")
    scatter!(pp, [bJ_α.ε],  [bJ_α.H];  ms=8, c=:black, label="α slider (J)")
    pp
end

# ╔═╡ a0000009-0000-0000-0000-00000000000e
md"""
## 6. The witnesses sweep the **entire boundary** of the cloud

By construction the HR family traces $H = 2\varepsilon$ — the
upper edge — and the J family traces $H = H_{\mathrm{bin}}(\varepsilon)$
— the lower edge. Any candidate "third boundary family" would
have to coincide with one of these, which is the Prop 7
(unimprovability) argument made visual.

## 7. Exercises — replicate
"""

# ╔═╡ a0000009-0000-0000-0000-00000000000f
md"""
### E1. A 3-cell HR-like witness

Generalise: $q = (1 - 2\alpha, \alpha, \alpha)$, $e = (0, 0, 1/2)$.
Compute $\varepsilon$, $H$, upper, and check upper-tightness.
"""

# ╔═╡ a0000009-0000-0000-0000-000000000010
let
    α  = 0.25
    q  = [1 - 2α, α, α]
    e  = [0.0, 0.0, 0.5]
    b  = bracket_at(q, e)
    (ε=round(b.ε; digits=4), H=round(b.H; digits=4),
     upper=round(b.upper; digits=4),
     upper_tight=isapprox(b.upper, b.ε; atol=1e-9))
end

# ╔═╡ a0000009-0000-0000-0000-000000000011
md"""
### E2. **Two-cell J-like witness with constant per-cell error**

$q = (q_1, 1-q_1)$, $e = (e_0, e_0)$ for any $e_0 \in [0, 1/2]$.
Then $\varepsilon = e_0$ and $H = H_{\mathrm{bin}}(e_0)$, so
$\mathrm{lower} = e_0 = \varepsilon$ — lower-tight for **any** $q_1$.
"""

# ╔═╡ a0000009-0000-0000-0000-000000000012
let
    rows = []
    e₀ = 0.3
    for q₁ in (0.1, 0.3, 0.5, 0.7, 0.9)
        b = bracket_at([q₁, 1-q₁], [e₀, e₀])
        push!(rows, (q₁=q₁, ε=round(b.ε; digits=4),
                     lower=round(b.lower; digits=4),
                     lower_tight=isapprox(b.lower, b.ε; atol=1e-9)))
    end
    rows
end

# ╔═╡ a0000009-0000-0000-0000-000000000013
md"""
### E3. Stress-test the boundary: sample $N$ partitions and find the **closest** to each witness

Pick the nearest sample to $\Pi^{\mathrm{HR}}_{0.25}$ in
$(\varepsilon, H)$ Euclidean distance and report it. None should
beat the witness (slack = 0).
"""

# ╔═╡ a0000009-0000-0000-0000-000000000014
let
    rng = MersenneTwister(11)
    Nx = 10_000
    best_dist = Inf
    best_q = nothing; best_e = nothing
    target = bracket_at(Π_HR(0.25)...)
    for _ in 1:Nx
        m = 5
        raw = randexp(rng, m); q = raw ./ sum(raw)
        e   = rand(rng, m) .* 0.5
        b   = bracket_at(q, e)
        d   = (b.ε - target.ε)^2 + (b.H - target.H)^2
        if d < best_dist
            best_dist = d; best_q = q; best_e = e
        end
    end
    (best_dist=round(sqrt(best_dist); digits=4),
     target_ε=round(target.ε; digits=4),
     target_H=round(target.H; digits=4))
end

# ╔═╡ a0000009-0000-0000-0000-000000000015
md"""
### E4. Verify the J witness in **nats**

Re-do §3 in nats. Both bracket and tightness statements are
unit-free; numerical values rescale by $\ln 2$.
"""

# ╔═╡ a0000009-0000-0000-0000-000000000016
let
    Hb_nats(p) = (p ≤ 0 || p ≥ 1) ? 0.0 : -p*log(p) - (1-p)*log(1-p)
    function Hb_inv_nats(h; tol=1e-12)
        h ≤ 0 && return 0.0
        h ≥ log(2) && return 0.5
        lo, hi = 0.0, 0.5
        while hi - lo > tol
            mid = 0.5*(lo+hi)
            Hb_nats(mid) < h ? (lo = mid) : (hi = mid)
        end
        0.5*(lo+hi)
    end
    α = 0.25
    H_J = Hb_nats(α)
    lower_nats = Hb_inv_nats(H_J)
    (ε=α, H_nats=round(H_J; digits=6),
     lower_nats=round(lower_nats; digits=6),
     lower_tight=isapprox(lower_nats, α; atol=1e-9))
end

# ╔═╡ a0000009-0000-0000-0000-000000000017
md"""
## 8. Next — NB10: unimprovability live (try to lower the upper envelope and let the HR witness refute you)
"""

# ╔═╡ Cell order:
# ╠═a0000009-0000-0000-0000-000000000001
# ╟─a0000009-0000-0000-0000-000000000002
# ╟─a0000009-0000-0000-0000-000000000003
# ╠═a0000009-0000-0000-0000-000000000004
# ╟─a0000009-0000-0000-0000-000000000005
# ╠═a0000009-0000-0000-0000-000000000006
# ╟─a0000009-0000-0000-0000-000000000007
# ╠═a0000009-0000-0000-0000-000000000008
# ╟─a0000009-0000-0000-0000-000000000009
# ╠═a0000009-0000-0000-0000-00000000000a
# ╠═a0000009-0000-0000-0000-00000000000b
# ╟─a0000009-0000-0000-0000-00000000000c
# ╠═a0000009-0000-0000-0000-00000000000d
# ╟─a0000009-0000-0000-0000-00000000000e
# ╟─a0000009-0000-0000-0000-00000000000f
# ╠═a0000009-0000-0000-0000-000000000010
# ╟─a0000009-0000-0000-0000-000000000011
# ╠═a0000009-0000-0000-0000-000000000012
# ╟─a0000009-0000-0000-0000-000000000013
# ╠═a0000009-0000-0000-0000-000000000014
# ╟─a0000009-0000-0000-0000-000000000015
# ╠═a0000009-0000-0000-0000-000000000016
# ╟─a0000009-0000-0000-0000-000000000017
