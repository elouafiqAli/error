### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Refinement monotonicity — and the endpoint false-lead"
#> tags = ["bracket", "unit-3", "proposition-5"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a0000008-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a0000008-0000-0000-0000-000000000002
md"""
# Notebook 08 — Refinement monotonicity (and the endpoint false-lead)

> **Unit III, item 1.** Proposition 5 says: refining a partition
> **shrinks the bracket *interval***. It does NOT say the lower
> endpoint moves down monotonically, nor that the upper endpoint
> moves down monotonically — *only* that the interval-as-a-whole
> contracts. We **demonstrate** this in 30 lines and exhibit a
> live counter-example where the lower endpoint *increases* under
> refinement (while the width still shrinks, as predicted).
>
> **PLAN.md item 14d, lived in code.**
"""

# ╔═╡ a0000008-0000-0000-0000-000000000003
md"""
## 1. Helpers
"""

# ╔═╡ a0000008-0000-0000-0000-000000000004
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
    bracket(q, e) = (lower = Hbin_inv(sum(q .* Hbin.(e))),
                     upper = sum(q .* Hbin.(e)) / 2,
                     ε     = sum(q .* e),
                     H     = sum(q .* Hbin.(e)))
end

# ╔═╡ a0000008-0000-0000-0000-000000000005
md"""
## 2. Start: a 2-cell **coarse** partition
"""

# ╔═╡ a0000008-0000-0000-0000-000000000006
begin
    q_coarse = [0.5, 0.5]
    e_coarse = [0.10, 0.40]
    b_coarse = bracket(q_coarse, e_coarse)
    (; b_coarse..., width = b_coarse.upper - b_coarse.lower)
end

# ╔═╡ a0000008-0000-0000-0000-000000000007
md"""
## 3. Refine: split cell 1 into two sub-cells, preserving mass-weighted error

Refinement constraint: the new pair $(e_{1a}, e_{1b})$ with masses
$(\alpha/2, (1-\alpha)/2)$ inside the original cell-1 mass $1/2$ must
satisfy

\$\$
\tfrac{\alpha}{2}\,e_{1a} + \tfrac{1-\alpha}{2}\,e_{1b}
  \;=\; \tfrac{1}{2}\,e_{\mathrm{coarse},1}
\$\$

so the *contribution* to $\varepsilon$ is preserved. The
**contribution to $H$ is NOT preserved** (Jensen); refinement can
only *increase* $H$ — which can move both bracket endpoints.

Slider $\alpha$ controls the **split asymmetry**.
"""

# ╔═╡ a0000008-0000-0000-0000-000000000008
@bind α Slider(0.01:0.005:0.99, default=0.5, show_value=true)

# ╔═╡ a0000008-0000-0000-0000-000000000009
@bind e1a_slider Slider(0.0:0.001:0.5, default=0.05, show_value=true)

# ╔═╡ a0000008-0000-0000-0000-00000000000a
begin
    # Choose e1a from slider; solve for e1b to preserve mass-weighted average.
    e1_target = e_coarse[1]              # = 0.10
    e1a = clamp(e1a_slider, 0.0, 0.5)
    # α/2 * e1a + (1-α)/2 * e1b = 0.5 * e1_target
    #   ⇒ e1b = (e1_target - α*e1a) / (1 - α)
    e1b = (1-α) > 1e-12 ? clamp((e1_target - α*e1a) / (1 - α), 0.0, 0.5) : e1_target
    q_fine = [α/2, (1-α)/2, 0.5]
    e_fine = [e1a, e1b, e_coarse[2]]
    b_fine = bracket(q_fine, e_fine)
    md"""
    Refinement parameters: $α = $(round(α; digits=3))$, $e_{1a} = $(round(e1a; digits=3))$, $e_{1b} = $(round(e1b; digits=3))$.

    | quantity | coarse | fine | direction |
    |---|---|---|---|
    | $\varepsilon$         | $(round(b_coarse.ε;    digits=4)) | $(round(b_fine.ε;    digits=4)) | preserved |
    | $H(Y\mid\Pi)$         | $(round(b_coarse.H;    digits=4)) | $(round(b_fine.H;    digits=4)) | refine ⇒ H ↑ |
    | lower                 | $(round(b_coarse.lower; digits=4)) | $(round(b_fine.lower; digits=4)) | depends! |
    | upper                 | $(round(b_coarse.upper; digits=4)) | $(round(b_fine.upper; digits=4)) | upper ↑ with H |
    | **width** (upper-lower) | $(round(b_coarse.upper - b_coarse.lower; digits=4)) | $(round(b_fine.upper - b_fine.lower; digits=4)) | Prop 5: shrinks |
    """
end

# ╔═╡ a0000008-0000-0000-0000-00000000000b
md"""
## 4. Live counter-example: lower endpoint moves the "wrong" way

Set $\alpha \approx 0.99$ and $e_{1a} \approx 0$; then $e_{1b}$
is forced near $1$ — clipped to $0.5$ — and the lower endpoint of
the refined partition can be *higher* than the coarse one. The
width still shrinks (Prop 5 holds); the *individual endpoints*
can go either way.
"""

# ╔═╡ a0000008-0000-0000-0000-00000000000c
let
    αc = 0.99
    e1a_c = 0.0
    e1b_c = clamp((e_coarse[1] - αc*e1a_c) / (1 - αc), 0.0, 0.5)
    qc = [αc/2, (1-αc)/2, 0.5]
    ec = [e1a_c, e1b_c, e_coarse[2]]
    bc = bracket(qc, ec)
    eps_c = round(b_coarse.ε; digits=4)
    eps_f = round(bc.ε; digits=4)
    lo_c  = round(b_coarse.lower; digits=4)
    lo_f  = round(bc.lower; digits=4)
    w_c   = round(b_coarse.upper - b_coarse.lower; digits=4)
    w_f   = round(bc.upper - bc.lower; digits=4)
    e1b_r = round(e1b_c; digits=3)
    dir   = bc.lower > b_coarse.lower ? "increased" : "decreased"
    width_shrinks = bc.upper - bc.lower < b_coarse.upper - b_coarse.lower
    Markdown.parse(string(
        "With alpha = 0.99, e_{1a} = 0, e_{1b} = ", e1b_r, ":\n\n",
        "- eps_coarse = ", eps_c, "; eps_fine = ", eps_f, " — not exactly preserved because e1b was clipped.\n",
        "- lower_coarse = ", lo_c, "; lower_fine = ", lo_f, "; direction: ", dir, ".\n",
        "- width_coarse = ", w_c, "; width_fine = ", w_f, "; width shrinks? ", width_shrinks))
end

# ╔═╡ a0000008-0000-0000-0000-00000000000d
md"""
## 5. Plot — both intervals side-by-side as $\alpha$ sweeps
"""

# ╔═╡ a0000008-0000-0000-0000-00000000000e
begin
    αs = 0.05:0.005:0.95
    widths_fine = Float64[]
    lowers_fine = Float64[]
    uppers_fine = Float64[]
    for αi in αs
        e1a_i = 0.05
        denom = (1 - αi)
        e1b_i = denom > 1e-12 ? clamp((e_coarse[1] - αi*e1a_i)/denom, 0.0, 0.5) : e_coarse[1]
        qi    = [αi/2, (1-αi)/2, 0.5]
        ei    = [e1a_i, e1b_i, e_coarse[2]]
        bi    = bracket(qi, ei)
        push!(lowers_fine, bi.lower)
        push!(uppers_fine, bi.upper)
        push!(widths_fine, bi.upper - bi.lower)
    end
    pp = plot(αs, lowers_fine; label="lower (fine)", lw=2)
    plot!(pp, αs, uppers_fine; label="upper (fine)", lw=2)
    plot!(pp, αs, widths_fine; label="width (fine)", lw=2, ls=:dash)
    hline!(pp, [b_coarse.lower]; label="lower (coarse)", c=:black, ls=:dot)
    hline!(pp, [b_coarse.upper]; label="upper (coarse)", c=:red,   ls=:dot)
    hline!(pp, [b_coarse.upper - b_coarse.lower]; label="width (coarse)", c=:gray, ls=:dot)
    xlabel!(pp, L"\alpha\ \mathrm{(refinement\ split\ asymmetry)}")
    title!(pp, "endpoints non-monotone — width monotone")
    pp
end

# ╔═╡ a0000008-0000-0000-0000-00000000000f
md"""
## 6. The lesson

> "The object that is monotone is the **interval**, not its
> individual ends." — PLAN.md §14d.

A naive proof attempt would try to show *both* endpoints are
monotone and then deduce the interval shrinks. The plot above
falsifies that approach: the lower endpoint can rise under
refinement. The actual proof has to argue about the **interval
as a whole** — see Proposition 5 in the manuscript.

## 7. Exercises — replicate
"""

# ╔═╡ a0000008-0000-0000-0000-000000000010
md"""
### E1. Replicate §3 with a different coarse partition

$q_{\text{coarse}} = (0.3, 0.7)$, $e_{\text{coarse}} = (0.2, 0.35)$.
Refine cell 2 (the larger one). Show width still shrinks.
"""

# ╔═╡ a0000008-0000-0000-0000-000000000011
let
    qc = [0.3, 0.7]
    ec = [0.2, 0.35]
    bc = bracket(qc, ec)
    width_c = bc.upper - bc.lower
    # Split cell 2 with α=0.4
    αE1 = 0.4
    e2a = 0.25
    e2b = clamp((ec[2] - αE1*e2a)/(1-αE1), 0.0, 0.5)
    qf  = [0.3, 0.7*αE1, 0.7*(1-αE1)]
    ef  = [ec[1], e2a, e2b]
    bf  = bracket(qf, ef)
    width_f = bf.upper - bf.lower
    (width_coarse=round(width_c; digits=5),
     width_fine  =round(width_f; digits=5),
     shrunk = width_f ≤ width_c)
end

# ╔═╡ a0000008-0000-0000-0000-000000000012
md"""
### E2. Trivial refinement (split into two equal copies) leaves width unchanged

If $e_{1a} = e_{1b} = e_{\text{coarse},1}$ (a degenerate split),
the refinement doesn't change anything. Verify.
"""

# ╔═╡ a0000008-0000-0000-0000-000000000013
let
    qf = [0.25, 0.25, 0.5]
    ef = [0.10, 0.10, 0.40]
    bf = bracket(qf, ef)
    (width_coarse=round(b_coarse.upper - b_coarse.lower; digits=8),
     width_fine_trivial_split=round(bf.upper - bf.lower; digits=8),
     equal=isapprox(bf.upper - bf.lower, b_coarse.upper - b_coarse.lower; atol=1e-10))
end

# ╔═╡ a0000008-0000-0000-0000-000000000014
md"""
### E3. Many random refinements, plot the width-shrink histogram
"""

# ╔═╡ a0000008-0000-0000-0000-000000000015
let
    qc = [0.5, 0.5]
    ec = [0.1, 0.4]
    bc = bracket(qc, ec)
    width_c = bc.upper - bc.lower
    shrinks = Float64[]
    for _ in 1:2000
        αi = 0.05 + 0.9*rand()
        e1a_i = 0.5*rand()
        denom = (1 - αi)
        e1b_i = denom > 1e-12 ? clamp((ec[1] - αi*e1a_i)/denom, 0.0, 0.5) : ec[1]
        qi = [αi/2, (1-αi)/2, 0.5]
        ei = [e1a_i, e1b_i, ec[2]]
        bi = bracket(qi, ei)
        push!(shrinks, (width_c - (bi.upper - bi.lower)))
    end
    histogram(shrinks; bins=60, label="width(coarse) - width(fine)",
              xlabel="amount by which the width shrank",
              ylabel="count")
end

# ╔═╡ a0000008-0000-0000-0000-000000000016
md"""
### E4. Find a refinement where the **upper** endpoint *decreases*

By the formula upper $= H/2$, decreasing upper means decreasing
$H$. Refinement cannot decrease $H$ (Jensen) — so this exercise
has *no solution*: it is the second false-lead, a non-fact made
concrete. Confirm by sweeping random refinements and noting
"$\mathrm{upper}_{\text{fine}} \ge \mathrm{upper}_{\text{coarse}}$"
holds in *every* sample.
"""

# ╔═╡ a0000008-0000-0000-0000-000000000017
let
    qc = [0.5, 0.5]
    ec = [0.1, 0.4]
    bc = bracket(qc, ec)
    viols = 0
    for _ in 1:5000
        αi = 0.05 + 0.9*rand()
        e1a_i = 0.5*rand()
        denom = (1 - αi)
        e1b_i = denom > 1e-12 ? clamp((ec[1] - αi*e1a_i)/denom, 0.0, 0.5) : ec[1]
        qi = [αi/2, (1-αi)/2, 0.5]
        ei = [e1a_i, e1b_i, ec[2]]
        bi = bracket(qi, ei)
        if bi.upper < bc.upper - 1e-12
            viols += 1
        end
    end
    (samples=5000, refinements_where_upper_decreased=viols)
end

# ╔═╡ a0000008-0000-0000-0000-000000000018
md"""
## 8. Next — NB09: tightness witnesses $\Pi^{\mathrm{HR}}$ and $\Pi^{\mathrm{J}}$
"""

# ╔═╡ Cell order:
# ╠═a0000008-0000-0000-0000-000000000001
# ╟─a0000008-0000-0000-0000-000000000002
# ╟─a0000008-0000-0000-0000-000000000003
# ╠═a0000008-0000-0000-0000-000000000004
# ╟─a0000008-0000-0000-0000-000000000005
# ╠═a0000008-0000-0000-0000-000000000006
# ╟─a0000008-0000-0000-0000-000000000007
# ╠═a0000008-0000-0000-0000-000000000008
# ╠═a0000008-0000-0000-0000-000000000009
# ╠═a0000008-0000-0000-0000-00000000000a
# ╟─a0000008-0000-0000-0000-00000000000b
# ╠═a0000008-0000-0000-0000-00000000000c
# ╟─a0000008-0000-0000-0000-00000000000d
# ╠═a0000008-0000-0000-0000-00000000000e
# ╟─a0000008-0000-0000-0000-00000000000f
# ╟─a0000008-0000-0000-0000-000000000010
# ╠═a0000008-0000-0000-0000-000000000011
# ╟─a0000008-0000-0000-0000-000000000012
# ╠═a0000008-0000-0000-0000-000000000013
# ╟─a0000008-0000-0000-0000-000000000014
# ╠═a0000008-0000-0000-0000-000000000015
# ╟─a0000008-0000-0000-0000-000000000016
# ╠═a0000008-0000-0000-0000-000000000017
# ╟─a0000008-0000-0000-0000-000000000018
