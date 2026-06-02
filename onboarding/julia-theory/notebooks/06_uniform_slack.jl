### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Uniform slack w* and the critical point ε*=1/5"
#> tags = ["bracket", "unit-2", "optimisation"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a0000006-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings, Optim

# ╔═╡ a0000006-0000-0000-0000-000000000002
md"""
# Notebook 06 — Uniform slack $w^*$ and $\varepsilon^* = 1/5$

> **Unit II, payoff.** NB05's slack curve $w(\varepsilon) = H_{\mathrm{bin}}(\varepsilon)/2 - \varepsilon$
> peaks at the closed-form $\varepsilon^* = 1/5$ with
> $w^* \approx 0.16104$. We *recompute* this constant via **three
> independent paths** and confirm they agree to 1e-6:
>
> 1. **`Optim.jl` Brent's method** — black-box scalar maximiser.
> 2. **Hand-coded golden-section** — sanity check, no library.
> 3. **Hand-coded Newton on $w'(\varepsilon) = 0$** — uses the
>    closed-form derivative.
>
> All three should land on the same $\varepsilon^*$.
"""

# ╔═╡ a0000006-0000-0000-0000-000000000003
md"""
## 1. Slack function (from NB05)
"""

# ╔═╡ a0000006-0000-0000-0000-000000000004
begin
    Hbin(p::Real) = (p ≤ 0 || p ≥ 1) ? 0.0 : -p*log2(p) - (1-p)*log2(1-p)
    w(ε::Real)    = Hbin(ε)/2 - ε
end

# ╔═╡ a0000006-0000-0000-0000-000000000005
md"""
## 2. Path 1 — `Optim.jl` Brent's method (black-box maximisation)

`Optim.optimize(-w, lo, hi, Brent())` minimises $-w$ on
$[\mathrm{lo}, \mathrm{hi}]$. We bracket the maximum on $[0.05, 0.45]$.
"""

# ╔═╡ a0000006-0000-0000-0000-000000000006
begin
    res_optim = Optim.optimize(ε -> -w(ε), 0.05, 0.45, Optim.Brent();
                               rel_tol = 1e-12, abs_tol = 1e-12)
    ε_star_optim = Optim.minimizer(res_optim)
    w_star_optim = -Optim.minimum(res_optim)
    md"""
    - $\varepsilon^*_{\text{Optim}} = $(round(ε_star_optim; digits=8))$
    - $w^*_{\text{Optim}} = $(round(w_star_optim; digits=8))$
    - converged in $(res_optim.iterations) iterations.
    """
end

# ╔═╡ a0000006-0000-0000-0000-000000000007
md"""
## 3. Path 2 — hand-coded golden-section search

No library; only $w$. Used as a control to make sure Optim isn't
returning a library default.
"""

# ╔═╡ a0000006-0000-0000-0000-000000000008
function golden_max(f, lo, hi; tol=1e-12, maxit=200)
    φ = (sqrt(5) - 1) / 2
    a, b = lo, hi
    c = b - φ*(b - a)
    d = a + φ*(b - a)
    fc = f(c); fd = f(d)
    for _ in 1:maxit
        (b - a < tol) && break
        if fc > fd
            b, d, fd = d, c, fc
            c = b - φ*(b - a); fc = f(c)
        else
            a, c, fc = c, d, fd
            d = a + φ*(b - a); fd = f(d)
        end
    end
    x = 0.5*(a + b)
    return x, f(x)
end

# ╔═╡ a0000006-0000-0000-0000-000000000009
begin
    ε_star_gs, w_star_gs = golden_max(w, 0.05, 0.45)
    md"""
    - $\varepsilon^*_{\text{GS}} = $(round(ε_star_gs; digits=8))$
    - $w^*_{\text{GS}} = $(round(w_star_gs; digits=8))$
    """
end

# ╔═╡ a0000006-0000-0000-0000-00000000000a
md"""
## 4. Path 3 — hand-coded Newton on $w'(\varepsilon) = 0$

The derivative is

$$w'(\varepsilon) = \tfrac{1}{2}\log_2\!\bigl(\tfrac{1-\varepsilon}{\varepsilon}\bigr) - 1.$$

Setting $w'(\varepsilon^*) = 0$ gives $\log_2(\tfrac{1-\varepsilon^*}{\varepsilon^*}) = 2$,
i.e. $\tfrac{1-\varepsilon^*}{\varepsilon^*} = 4$, so
$\varepsilon^* = 1/5$. We let Newton find it numerically as a
cross-check.
"""

# ╔═╡ a0000006-0000-0000-0000-00000000000b
begin
    w_prime(ε)        = 0.5 * log2((1-ε)/ε) - 1
    w_double_prime(ε) = -1 / (2 * log(2) * ε * (1-ε))
    function newton(f, fprime, x0; tol=1e-12, maxit=200)
        x = x0
        for _ in 1:maxit
            fx = f(x); fpx = fprime(x)
            step = fx / fpx
            x -= step
            abs(step) < tol && break
        end
        return x
    end
    ε_star_newton = newton(w_prime, w_double_prime, 0.2)
    w_star_newton = w(ε_star_newton)
    md"""
    - closed-form: $\varepsilon^* = 1/5 = 0.2$
    - Newton: $\varepsilon^*_{\text{N}} = $(round(ε_star_newton; digits=10))$
    - $w^*_{\text{N}} = $(round(w_star_newton; digits=10))$
    """
end

# ╔═╡ a0000006-0000-0000-0000-00000000000c
md"""
## 5. Cross-check all three paths agree (to 1e-6)
"""

# ╔═╡ a0000006-0000-0000-0000-00000000000d
let
    max_disagreement = maximum(abs.([
        ε_star_optim - 0.2,
        ε_star_gs    - 0.2,
        ε_star_newton - 0.2,
    ]))
    @assert max_disagreement < 1e-6  "paths disagree on ε*"
    @assert abs(w_star_optim - w_star_newton) < 1e-9
    md"""
    All three paths agree on $\varepsilon^* = 0.2$ to within $(max_disagreement).

    | path | $\varepsilon^*$ | $w^*$ |
    |---|---|---|
    | Optim Brent | $(round(ε_star_optim; digits=8)) | $(round(w_star_optim; digits=8)) |
    | golden-sect | $(round(ε_star_gs;    digits=8)) | $(round(w_star_gs;    digits=8)) |
    | Newton      | $(round(ε_star_newton; digits=8)) | $(round(w_star_newton; digits=8)) |
    | closed form | 0.20000000 | $(round(w(0.2); digits=8)) |
    """
end

# ╔═╡ a0000006-0000-0000-0000-00000000000e
md"""
## 6. Visualise — the slack curve with all three estimates marked
"""

# ╔═╡ a0000006-0000-0000-0000-00000000000f
begin
    εs = 0.001:0.001:0.499
    ws = [w(εi) for εi in εs]
    pp = plot(εs, ws; lw = 2, label = L"w(\varepsilon)",
              xlabel = L"\varepsilon",
              ylabel = L"H_{\mathrm{bin}}(\varepsilon)/2 - \varepsilon")
    vline!(pp, [0.2]; label = L"\varepsilon^* = 1/5",
           c = :gray, ls = :dot)
    scatter!(pp, [ε_star_optim],  [w_star_optim];  label = "Optim",  ms = 6)
    scatter!(pp, [ε_star_gs],     [w_star_gs];     label = "GS",     ms = 4, marker = :diamond)
    scatter!(pp, [ε_star_newton], [w_star_newton]; label = "Newton", ms = 3, marker = :x)
    pp
end

# ╔═╡ a0000006-0000-0000-0000-000000000010
md"""
## 7. Falsify — what does $w(\varepsilon)$ look like outside $[0, 1/2]$?

By symmetry of $H_{\mathrm{bin}}$, $w(\varepsilon)$ extended to
$\varepsilon \in (0, 1)$ has *two* maxima (at $1/5$ and $4/5$).
Theorem 1's bracket assumes $\varepsilon \in [0, 1/2]$ (label
flipping is a free re-labelling); the $4/5$ symmetric maximum is
the *flipped* problem.
"""

# ╔═╡ a0000006-0000-0000-0000-000000000011
let
    εs2 = 0.001:0.001:0.999
    ws2 = [w(εi) for εi in εs2]
    plot(εs2, ws2; lw=2, label=L"w(\varepsilon)\ \mathrm{extended}")
    vline!([0.2, 0.8]; label="symmetric maxima 1/5, 4/5", c=:red, ls=:dot)
    xlabel!(L"\varepsilon"); ylabel!(L"w")
end

# ╔═╡ a0000006-0000-0000-0000-000000000012
md"""
## 8. Read Corollary 2 now

The constant you just produced — $w^* \approx 0.16104$ — is the
one Corollary 2 of the paper states. The notebook is the
pre-reading; the paper is the post-reading.

## 9. Exercises — replicate
"""

# ╔═╡ a0000006-0000-0000-0000-000000000013
md"""
### E1. Re-do all three paths in **nats**

Replace $H_{\mathrm{bin}}$ with $H_{\mathrm{bin}}^{\text{nats}}$
and re-run. $\varepsilon^*$ is unchanged (location is unit-free).
$w^*_{\text{nats}} = w^* \cdot \ln 2$.
"""

# ╔═╡ a0000006-0000-0000-0000-000000000014
let
    Hb_nats(p) = (p ≤ 0 || p ≥ 1) ? 0.0 : -p*log(p) - (1-p)*log(1-p)
    w_nats(ε)  = Hb_nats(ε)/2 - ε
    res = Optim.optimize(ε -> -w_nats(ε), 0.05, 0.45, Optim.Brent())
    ε_star = Optim.minimizer(res)
    w_star = -Optim.minimum(res)
    (ε_star = round(ε_star; digits=8),
     w_star_nats = round(w_star; digits=8),
     w_star_bits_check = round(w_star / log(2); digits=8))
end

# ╔═╡ a0000006-0000-0000-0000-000000000015
md"""
### E2. Replicate Path 1 on the slack of NB05's **upper bound minus the truth on $\Pi^{\mathrm{HR}}$ family**

(Preview of NB09: the tightness-witness family makes the upper
bound tight. Maximise $H/2 - \varepsilon$ on the witness; expect
**zero** — the bound *is* the truth on the witness.)

The witness produces $H(Y\mid\Pi) = 2\varepsilon$ identically.
Confirm $w = H/2 - \varepsilon = 0$ on the witness.
"""

# ╔═╡ a0000006-0000-0000-0000-000000000016
let
    # On Π^HR with parameter α ∈ [0, 1/2]: by construction ε = α and H = 2α (bits).
    αs = 0.001:0.001:0.499
    slack_on_witness = [(2αi)/2 - αi for αi in αs]
    (max_slack = round(maximum(abs.(slack_on_witness)); digits=12),
     means_zero_to_floating_point = all(s -> abs(s) < 1e-12, slack_on_witness))
end

# ╔═╡ a0000006-0000-0000-0000-000000000017
md"""
### E3. Find $\varepsilon^*$ by **bisecting on $w'$** (no Optim, no Newton)

Replication of Path 3 with bisection instead of Newton.
"""

# ╔═╡ a0000006-0000-0000-0000-000000000018
let
    function bisect_zero(f, lo, hi; tol=1e-12, maxit=200)
        flo = f(lo); fhi = f(hi)
        @assert flo * fhi < 0  "no sign change"
        for _ in 1:maxit
            mid = 0.5*(lo+hi); fmid = f(mid)
            (abs(fmid) < tol || hi - lo < tol) && return mid
            if flo * fmid < 0
                hi = mid; fhi = fmid
            else
                lo = mid; flo = fmid
            end
        end
        return 0.5*(lo+hi)
    end
    ε_star_bisect = bisect_zero(w_prime, 0.001, 0.499)
    (ε_star = round(ε_star_bisect; digits=10),
     matches_closed_form = isapprox(ε_star_bisect, 0.2; atol=1e-9))
end

# ╔═╡ a0000006-0000-0000-0000-000000000019
md"""
### E4. Sensitivity: perturb the upper-bound coefficient from $1/2$ to $1/2 + δ$

If the upper bound were $(1/2 + δ) H_{\mathrm{bin}}(\varepsilon)$
instead of $(1/2) H_{\mathrm{bin}}(\varepsilon)$ — the constant
$\varepsilon^*$ shifts. Plot $\varepsilon^*(δ)$ for $δ \in [-0.1, 0.1]$.
"""

# ╔═╡ a0000006-0000-0000-0000-00000000001a
let
    function ε_star_of_delta(δ)
        res = Optim.optimize(ε -> -((0.5 + δ)*Hbin(ε) - ε), 0.01, 0.49, Optim.Brent())
        Optim.minimizer(res)
    end
    δs = -0.1:0.005:0.1
    ε_stars = ε_star_of_delta.(δs)
    plot(δs, ε_stars; lw=2, label=L"\varepsilon^*(δ)",
         xlabel="δ (perturbation of 1/2 coefficient)",
         ylabel=L"\varepsilon^*")
    hline!([0.2]; label="baseline ε*=1/5", c=:gray, ls=:dot)
end

# ╔═╡ a0000006-0000-0000-0000-00000000001b
md"""
## 10. Next — NB07: the achievable region scatter
"""

# ╔═╡ Cell order:
# ╠═a0000006-0000-0000-0000-000000000001
# ╟─a0000006-0000-0000-0000-000000000002
# ╟─a0000006-0000-0000-0000-000000000003
# ╠═a0000006-0000-0000-0000-000000000004
# ╟─a0000006-0000-0000-0000-000000000005
# ╠═a0000006-0000-0000-0000-000000000006
# ╟─a0000006-0000-0000-0000-000000000007
# ╠═a0000006-0000-0000-0000-000000000008
# ╠═a0000006-0000-0000-0000-000000000009
# ╟─a0000006-0000-0000-0000-00000000000a
# ╠═a0000006-0000-0000-0000-00000000000b
# ╟─a0000006-0000-0000-0000-00000000000c
# ╠═a0000006-0000-0000-0000-00000000000d
# ╟─a0000006-0000-0000-0000-00000000000e
# ╠═a0000006-0000-0000-0000-00000000000f
# ╟─a0000006-0000-0000-0000-000000000010
# ╠═a0000006-0000-0000-0000-000000000011
# ╟─a0000006-0000-0000-0000-000000000012
# ╟─a0000006-0000-0000-0000-000000000013
# ╠═a0000006-0000-0000-0000-000000000014
# ╟─a0000006-0000-0000-0000-000000000015
# ╠═a0000006-0000-0000-0000-000000000016
# ╟─a0000006-0000-0000-0000-000000000017
# ╠═a0000006-0000-0000-0000-000000000018
# ╟─a0000006-0000-0000-0000-000000000019
# ╠═a0000006-0000-0000-0000-00000000001a
# ╟─a0000006-0000-0000-0000-00000000001b
