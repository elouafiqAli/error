### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Binary entropy — the smallest object"
#> date = "2026-06-02"
#> tags = ["information-theory", "primitives", "unit-1"]
#> description = "Reactive playground for H_bin(p). Slider, symbolic derivative, falsification."

using Markdown
using InteractiveUtils

# ╔═╡ a0000001-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings, Symbolics

# ╔═╡ a0000001-0000-0000-0000-000000000002
md"""
# Notebook 01 — Binary entropy `Hbin`

> **Unit I, primitive 1.** The smallest object in the paper.
> A slider, three constructions (numeric, symbolic, visual), and
> one falsification.
>
> **Punchline.** $H_{\mathrm{bin}}(p) = -p \log_2 p - (1-p)\log_2(1-p)$
> is symmetric about $p = 1/2$, peaks at $1$ bit, and has derivative
> $\log_2 \tfrac{1-p}{p}$ that vanishes exactly at $p = 1/2$. You
> are going to *deform the curve with a slider* and *let Julia
> compute the derivative symbolically* — that is the entire notebook.
>
> **Inspiration.** Slider/section structure adapted from
> [SISL StanfordAA228V.jl](https://github.com/sisl/StanfordAA228V.jl);
> symbolic-then-numerical pedagogy from
> [MIT 18.S096 — Matrix Calculus](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/pages/lecture-notes/)
> (Edelman & Johnson, IAP 2023).
"""

# ╔═╡ a0000001-0000-0000-0000-000000000003
md"""
## 1. The numeric construction

We define `Hbin(p)` from the definition. Convention: $0 \log_2 0 = 0$.
"""

# ╔═╡ a0000001-0000-0000-0000-000000000004
function Hbin(p::Real)
    0 ≤ p ≤ 1 || throw(ArgumentError("Hbin expects p ∈ [0,1], got $p"))
    (p == 0 || p == 1) && return 0.0
    return -p * log2(p) - (1 - p) * log2(1 - p)
end

# ╔═╡ a0000001-0000-0000-0000-000000000005
md"""
**Sanity check** (these should all return `true`):
"""

# ╔═╡ a0000001-0000-0000-0000-000000000006
(Hbin(0.0) == 0.0, Hbin(1.0) == 0.0, Hbin(0.5) == 1.0,
 abs(Hbin(0.1) - 0.4689955935892813) < 1e-12,
 abs(Hbin(0.3) - Hbin(0.7)) < 1e-15)

# ╔═╡ a0000001-0000-0000-0000-000000000007
md"""
## 2. The slider

Drag `p` and watch the value, then the curve.
"""

# ╔═╡ a0000001-0000-0000-0000-000000000008
@bind p Slider(0.0:0.001:1.0, default=0.5, show_value=true)

# ╔═╡ a0000001-0000-0000-0000-000000000009
md"""
At $p = $(round(p; digits=3))$:

- $H_{\mathrm{bin}}(p) = $(round(Hbin(p); digits=4))$ bits
- Bayes error $\varepsilon(p) = \min(p, 1-p) = $(round(min(p, 1 - p); digits=4))$
- HR upper $\tfrac{1}{2} H_{\mathrm{bin}}(\varepsilon(p)) = $(round(Hbin(min(p, 1-p))/2; digits=4))$ — pre-tasting Lemma 1
"""

# ╔═╡ a0000001-0000-0000-0000-00000000000a
let
    ps = 0:0.001:1
    plt = plot(ps, Hbin.(ps);
               label=L"H_{\mathrm{bin}}(p)",
               xlabel=L"p", ylabel="bits",
               title="Binary entropy",
               linewidth=2, legend=:bottom)
    vline!([p]; label="slider", linestyle=:dash, color=:red)
    scatter!([p], [Hbin(p)]; label=nothing, markersize=6, color=:red)
    plt
end

# ╔═╡ a0000001-0000-0000-0000-00000000000b
md"""
## 3. The symbolic derivative (Edelman moment)

We declare $p$ as a symbolic variable and ask `Symbolics.jl` to
differentiate $H_{\mathrm{bin}}$ on its behalf. The textbook identity
$H_{\mathrm{bin}}'(p) = \log_2 \tfrac{1-p}{p}$ should print.
"""

# ╔═╡ a0000001-0000-0000-0000-00000000000c
@variables ps

# ╔═╡ a0000001-0000-0000-0000-00000000000d
H_sym = -ps * log(ps) / log(2) - (1 - ps) * log(1 - ps) / log(2)

# ╔═╡ a0000001-0000-0000-0000-00000000000e
H_prime_sym = simplify(Symbolics.derivative(H_sym, ps))

# ╔═╡ a0000001-0000-0000-0000-00000000000f
md"""
**Read it.** $H'_{\mathrm{bin}}(p) = \log_2 \tfrac{1-p}{p}$. This
vanishes at $p = 1/2$ (top of the curve) and diverges at the endpoints
(infinite slope, finite value).

**Numerical cross-check.** Build a Float64 callable from the symbolic
expression and compare to a finite-difference estimate:
"""

# ╔═╡ a0000001-0000-0000-0000-000000000010
H_prime_fn = eval(build_function(H_prime_sym, ps; expression=Val{false}))

# ╔═╡ a0000001-0000-0000-0000-000000000011
let
    ps_grid = 0.01:0.01:0.99
    h = 1e-6
    fd = [(Hbin(q + h) - Hbin(q - h)) / (2h) for q in ps_grid]
    sym = H_prime_fn.(ps_grid)
    plot(ps_grid, sym; label="symbolic", linewidth=2, xlabel=L"p", ylabel=L"H_{\mathrm{bin}}'(p)")
    plot!(ps_grid, fd; label="finite-difference", linestyle=:dash, linewidth=2)
end

# ╔═╡ a0000001-0000-0000-0000-000000000012
md"""
## 4. Concavity, made visual

The second derivative is $H_{\mathrm{bin}}''(p) = -\tfrac{1}{p(1-p) \ln 2}$
— negative on $(0,1)$, so $H_{\mathrm{bin}}$ is strictly concave.
Let Julia confirm:
"""

# ╔═╡ a0000001-0000-0000-0000-000000000013
H_double_sym = simplify(Symbolics.derivative(H_prime_sym, ps))

# ╔═╡ a0000001-0000-0000-0000-000000000014
let
    H_dd_fn = eval(build_function(H_double_sym, ps; expression=Val{false}))
    qs = 0.05:0.01:0.95
    plot(qs, H_dd_fn.(qs); label=L"H_{\mathrm{bin}}''(p)",
         linewidth=2, xlabel=L"p", ylabel="bits", title="strictly negative ⇒ concave")
    hline!([0]; label=nothing, linestyle=:dot)
end

# ╔═╡ a0000001-0000-0000-0000-000000000015
md"""
## 5. Falsify — change the base, watch the peak move

The choice of $\log_2$ vs $\ln$ vs $\log_3$ is a units choice. Define
the same function in base $b$:
"""

# ╔═╡ a0000001-0000-0000-0000-000000000016
@bind base_choice Select(["2 (bits)" => 2, "e (nats)" => exp(1), "3 (trits)" => 3, "10 (digits)" => 10])

# ╔═╡ a0000001-0000-0000-0000-000000000017
function H_in_base(p, b)
    (p == 0 || p == 1) && return 0.0
    return -(p * log(p) + (1 - p) * log(1 - p)) / log(b)
end

# ╔═╡ a0000001-0000-0000-0000-000000000018
let
    ps_grid = 0:0.001:1
    plot(ps_grid, [H_in_base(q, base_choice) for q in ps_grid];
         label="base $base_choice", linewidth=2, xlabel=L"p",
         ylabel="units", title="Binary entropy in different bases")
    hline!([H_in_base(0.5, base_choice)]; label="peak = $(round(H_in_base(0.5, base_choice); digits=4))",
           linestyle=:dot)
end

# ╔═╡ a0000001-0000-0000-0000-000000000019
md"""
**Observation.** The *shape* of the curve does not change. The
*peak height* does: 1 bit, $\ln 2 \approx 0.693$ nat,
$\log_3 2 \approx 0.631$ trit. The choice of base picks a unit, not
a physics.

**Take-away.** Every appearance of $H_{\mathrm{bin}}$ in the paper is
in *bits*. The verifier in `verify.jl` and the Lean mechanisation in
`partition-sandwich-preprint/formal/` both use base 2. If you ever
see "0.693" in a numeric output that you expected to be near $1$,
your library defaulted to nats — switch it.

## 6. Investigate (reader exercises, ungraded)

1. Move the slider to $p = 0.1$. Read the upper-HR value $\tfrac12 H_{\mathrm{bin}}(0.1)$.
   Compare to $\min(p, 1-p) = 0.1$. The HR bound is loose by
   ${\approx}\,0.134$. That number is *not* the $w^* \approx 0.1610$
   from the abstract — why? (Hint: $w^*$ is the slack at the
   *maximising* $\varepsilon$, not at the maximising $p$.)
2. What's the smallest $p$ at which $H_{\mathrm{bin}}(p) < 0.1$? Read
   it off the slider to 2 decimals. (Answer near $0.014$.)
3. Set the base slider to $e$ (nats). What is $H_{\mathrm{bin}}'(0.5)$
   numerically? (Should still be 0 — the *location* of the critical
   point doesn't depend on the units.)

## 7. Next

Notebook **02 — Information quantities $H(X)$, $H(Y\mid X)$,
$I(X;Y)$** lifts this to *joint* distributions. The slider becomes
a 3-simplex (3 sliders, sum-to-one); the punchline becomes the chain
rule.
"""

# ╔═╡ Cell order:
# ╠═a0000001-0000-0000-0000-000000000001
# ╟─a0000001-0000-0000-0000-000000000002
# ╟─a0000001-0000-0000-0000-000000000003
# ╠═a0000001-0000-0000-0000-000000000004
# ╟─a0000001-0000-0000-0000-000000000005
# ╠═a0000001-0000-0000-0000-000000000006
# ╟─a0000001-0000-0000-0000-000000000007
# ╠═a0000001-0000-0000-0000-000000000008
# ╠═a0000001-0000-0000-0000-000000000009
# ╠═a0000001-0000-0000-0000-00000000000a
# ╟─a0000001-0000-0000-0000-00000000000b
# ╠═a0000001-0000-0000-0000-00000000000c
# ╠═a0000001-0000-0000-0000-00000000000d
# ╠═a0000001-0000-0000-0000-00000000000e
# ╟─a0000001-0000-0000-0000-00000000000f
# ╠═a0000001-0000-0000-0000-000000000010
# ╠═a0000001-0000-0000-0000-000000000011
# ╟─a0000001-0000-0000-0000-000000000012
# ╠═a0000001-0000-0000-0000-000000000013
# ╠═a0000001-0000-0000-0000-000000000014
# ╟─a0000001-0000-0000-0000-000000000015
# ╠═a0000001-0000-0000-0000-000000000016
# ╠═a0000001-0000-0000-0000-000000000017
# ╠═a0000001-0000-0000-0000-000000000018
# ╟─a0000001-0000-0000-0000-000000000019
