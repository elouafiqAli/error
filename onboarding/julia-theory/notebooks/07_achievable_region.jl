### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "The achievable region in the (ε, H(Y|Π)) plane"
#> tags = ["bracket", "unit-2", "proposition-3"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a0000007-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings, Random

# ╔═╡ a0000007-0000-0000-0000-000000000002
md"""
# Notebook 07 — The achievable region

> **Unit II, capstone.** *Proposition 3 made visual.* Sample $N$
> random partitions $(q, e)$; scatter their
> $(\varepsilon(\Pi), H(Y\mid\Pi))$ points; overlay the two
> envelopes from NB05. **Every** sample lies in the band — the
> bracket is *not* a worst-case fact, it's a *region* fact.
>
> The §Exercises replicate with different $m$, different prior
> distributions, and demonstrate the **boundary** is reached only
> by the two witness families NB09 will name explicitly.
"""

# ╔═╡ a0000007-0000-0000-0000-000000000003
md"""
## 1. Helpers — bracket primitives reused from NB05
"""

# ╔═╡ a0000007-0000-0000-0000-000000000004
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
    ε_of(q, e) = sum(q .* e)
    H_of(q, e) = sum(q .* Hbin.(e))
end

# ╔═╡ a0000007-0000-0000-0000-000000000005
md"""
## 2. Random partition sampler (Dirichlet $q$ + uniform $e$)
"""

# ╔═╡ a0000007-0000-0000-0000-000000000006
function random_partition(m::Int, rng::AbstractRNG)
    raw = randexp(rng, m)
    q   = raw ./ sum(raw)
    e   = rand(rng, m) .* 0.5
    q, e
end

# ╔═╡ a0000007-0000-0000-0000-000000000007
md"""
## 3. Sliders — cell count $m$, sample count $N$, seed
"""

# ╔═╡ a0000007-0000-0000-0000-000000000008
@bind m Select([3, 5, 7, 10, 20])

# ╔═╡ a0000007-0000-0000-0000-000000000009
@bind N Select([100, 1000, 5000, 20000])

# ╔═╡ a0000007-0000-0000-0000-00000000000a
@bind seed NumberField(0:10_000, default=42)

# ╔═╡ a0000007-0000-0000-0000-00000000000b
md"""
## 4. Sample $N$ partitions and verify the bracket on **every** one
"""

# ╔═╡ a0000007-0000-0000-0000-00000000000c
begin
    rng = MersenneTwister(seed)
    εs_sample = Vector{Float64}(undef, N)
    Hs_sample = Vector{Float64}(undef, N)
    violations = 0
    for i in 1:N
        q, e = random_partition(m, rng)
        εs_sample[i] = ε_of(q, e)
        Hs_sample[i] = H_of(q, e)
        lo = Hbin_inv(Hs_sample[i])
        hi = Hs_sample[i] / 2
        if !(lo - 1e-9 ≤ εs_sample[i] ≤ hi + 1e-9)
            violations += 1
        end
    end
    md"""
    Sampled $(N) partitions with m = $(m), seed = $(seed).
    - bracket holds on **all** samples? $(violations == 0)
    - violations: $(violations)
    """
end

# ╔═╡ a0000007-0000-0000-0000-00000000000d
md"""
## 5. Scatter + the two envelopes

The cloud fills a 2-D region. The two envelopes (parametrised by
$\varepsilon$ through $H = H_{\mathrm{bin}}(\varepsilon)$ for the
lower side, and by $H$ directly for the upper) are visible as
solid curves.
"""

# ╔═╡ a0000007-0000-0000-0000-00000000000e
begin
    # Lower envelope: parametrise by ε, then H = Hbin(ε) and ε is on the lower curve.
    εs_curve = 0.001:0.001:0.499
    H_lower_curve = [Hbin(εi) for εi in εs_curve]   # at lower curve, H = Hbin(ε)
    # Upper envelope: ε ≤ H/2, so at upper, H = 2ε  (the witness identity).
    H_upper_curve = [2*εi for εi in εs_curve]

    pp = scatter(εs_sample, Hs_sample;
                 ms=2, ma=0.25, label="$(N) random Π (m = $(m))",
                 xlabel=L"\varepsilon(\Pi)", ylabel=L"H(Y\mid\Pi)\ [\mathrm{bits}]",
                 legend=:topleft)
    plot!(pp, εs_curve, H_lower_curve;
          label=L"H = H_{\mathrm{bin}}(\varepsilon)\ \mathrm{(lower\ envelope)}",
          lw=2, c=:black)
    plot!(pp, εs_curve, H_upper_curve;
          label=L"H = 2\varepsilon\ \mathrm{(upper\ envelope\ at\ HR\ witness)}",
          lw=2, c=:red, ls=:dash)
    pp
end

# ╔═╡ a0000007-0000-0000-0000-00000000000f
md"""
## 6. Falsify — "the cloud is a curve" (it is not)

A naive intuition: $\varepsilon$ and $H$ should be in 1-to-1
correspondence. The scatter refutes this in one glance: at any
fixed $\varepsilon$, you observe a *range* of $H$ values. The
bracket is the band; refining the partition (NB08) shrinks the
band, but never collapses it to a curve.
"""

# ╔═╡ a0000007-0000-0000-0000-000000000010
let
    target_ε = 0.25
    band_window = 0.01
    in_band_idx = findall(εi -> abs(εi - target_ε) < band_window, εs_sample)
    if isempty(in_band_idx)
        md"No samples near ε = $(target_ε); try a bigger N."
    else
        Hs_at_band = Hs_sample[in_band_idx]
        md"""
        At $\varepsilon \approx $(target_ε)$ ($(length(in_band_idx)) samples
        within ±$(band_window)):
        - min $H$: $(round(minimum(Hs_at_band); digits=4))
        - max $H$: $(round(maximum(Hs_at_band); digits=4))
        - spread: $(round(maximum(Hs_at_band) - minimum(Hs_at_band); digits=4)) — strictly positive ⇒ NOT a curve.
        """
    end
end

# ╔═╡ a0000007-0000-0000-0000-000000000011
md"""
## 7. Take-aways

- For any random partition with $m$ cells, $(\varepsilon, H)$ lies
  in the band bounded by $H_{\mathrm{bin}}(\varepsilon) \le H$ (from
  the lower side of the bracket) and $H \ge 2\varepsilon$ (from
  the upper side rearranged).
- The boundary is reached only by the *tightness witness* families
  named in NB09.
- Larger $m$ does **not** widen the band; if anything the cloud
  concentrates near the lower envelope (Jensen tightens as the
  partition refines uniformly).

## 8. Exercises — replicate
"""

# ╔═╡ a0000007-0000-0000-0000-000000000012
md"""
### E1. Replicate §4 with $m = 2$

The cloud collapses to a 2-D region whose boundary IS the two
witness families. Verify all samples lie in the band; observe
visually that the cloud's extremes touch the envelopes.
"""

# ╔═╡ a0000007-0000-0000-0000-000000000013
let
    rng = MersenneTwister(1)
    Nx = 3000
    εs_ = Float64[]; Hs_ = Float64[]
    for _ in 1:Nx
        q, e = random_partition(2, rng)
        push!(εs_, ε_of(q, e))
        push!(Hs_, H_of(q, e))
    end
    εs_curve = 0.001:0.001:0.499
    scatter(εs_, Hs_; ms=2, ma=0.3, label="m=2", legend=:topleft)
    plot!(εs_curve, Hbin.(εs_curve); label="lower env", lw=2, c=:black)
    plot!(εs_curve, 2 .* εs_curve;    label="upper env", lw=2, c=:red, ls=:dash)
    xlabel!(L"\varepsilon"); ylabel!(L"H(Y\mid\Pi)")
end

# ╔═╡ a0000007-0000-0000-0000-000000000014
md"""
### E2. Replicate §4 with a **non-Dirichlet** prior (uniform on the simplex via "stick-breaking")
"""

# ╔═╡ a0000007-0000-0000-0000-000000000015
let
    function stick_break(m, rng)
        ws = rand(rng, m-1) .^ (1 ./ (m-1:-1:1))
        q  = Vector{Float64}(undef, m)
        rem = 1.0
        for i in 1:m-1
            q[i] = rem * (1 - ws[i])
            rem *= ws[i]
        end
        q[m] = rem
        e = rand(rng, m) .* 0.5
        q, e
    end
    rng = MersenneTwister(7)
    Nx = 2000
    viols = 0
    for _ in 1:Nx
        q, e = stick_break(5, rng)
        ε = ε_of(q, e); H = H_of(q, e)
        lo = Hbin_inv(H); hi = H/2
        if !(lo - 1e-9 ≤ ε ≤ hi + 1e-9)
            viols += 1
        end
    end
    (samples=Nx, violations=viols)
end

# ╔═╡ a0000007-0000-0000-0000-000000000016
md"""
### E3. Verify the slack scales as $w \le w^*$ on every sample

For each sample, compute slack $= H/2 - H_{\mathrm{bin}}^{-1}(H)$;
the maximum across the sample should not exceed $w^* \approx 0.16104$
from NB06.
"""

# ╔═╡ a0000007-0000-0000-0000-000000000017
let
    rng = MersenneTwister(13)
    Nx = 5000
    max_slack = 0.0
    for _ in 1:Nx
        q, e = random_partition(5, rng)
        H = H_of(q, e)
        slack = H/2 - Hbin_inv(H)
        max_slack = max(max_slack, slack)
    end
    (max_slack=max_slack, w_star_ref=0.16104, holds=max_slack ≤ 0.16104 + 1e-6)
end

# ╔═╡ a0000007-0000-0000-0000-000000000018
md"""
### E4. Sweep $m \in \{2, 5, 20, 100\}$; plot how the cloud's *upper edge* of $H$ at $\varepsilon = 0.25$ evolves
"""

# ╔═╡ a0000007-0000-0000-0000-000000000019
let
    rng_seed = 42
    band_w   = 0.01
    target_ε = 0.25
    rows = []
    for mm in (2, 5, 20, 100)
        rng = MersenneTwister(rng_seed)
        upper = 0.0
        for _ in 1:5000
            q, e = random_partition(mm, rng)
            ε = ε_of(q, e); H = H_of(q, e)
            if abs(ε - target_ε) < band_w
                upper = max(upper, H)
            end
        end
        push!(rows, (m=mm, max_H_at_ε025=round(upper; digits=4)))
    end
    rows
end

# ╔═╡ a0000007-0000-0000-0000-00000000001a
md"""
## 9. Next — Unit III, NB08: refinement monotonicity
"""

# ╔═╡ Cell order:
# ╠═a0000007-0000-0000-0000-000000000001
# ╟─a0000007-0000-0000-0000-000000000002
# ╟─a0000007-0000-0000-0000-000000000003
# ╠═a0000007-0000-0000-0000-000000000004
# ╟─a0000007-0000-0000-0000-000000000005
# ╠═a0000007-0000-0000-0000-000000000006
# ╟─a0000007-0000-0000-0000-000000000007
# ╠═a0000007-0000-0000-0000-000000000008
# ╠═a0000007-0000-0000-0000-000000000009
# ╠═a0000007-0000-0000-0000-00000000000a
# ╟─a0000007-0000-0000-0000-00000000000b
# ╠═a0000007-0000-0000-0000-00000000000c
# ╟─a0000007-0000-0000-0000-00000000000d
# ╠═a0000007-0000-0000-0000-00000000000e
# ╟─a0000007-0000-0000-0000-00000000000f
# ╠═a0000007-0000-0000-0000-000000000010
# ╟─a0000007-0000-0000-0000-000000000011
# ╟─a0000007-0000-0000-0000-000000000012
# ╠═a0000007-0000-0000-0000-000000000013
# ╟─a0000007-0000-0000-0000-000000000014
# ╠═a0000007-0000-0000-0000-000000000015
# ╟─a0000007-0000-0000-0000-000000000016
# ╠═a0000007-0000-0000-0000-000000000017
# ╟─a0000007-0000-0000-0000-000000000018
# ╠═a0000007-0000-0000-0000-000000000019
# ╟─a0000007-0000-0000-0000-00000000001a
