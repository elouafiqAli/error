### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "Fano vs Hellman–Raviv"
#> tags = ["information-theory", "primitives", "unit-1"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a0000003-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings

# ╔═╡ a0000003-0000-0000-0000-000000000002
md"""
# Notebook 03 — Fano vs Hellman–Raviv

> **Unit I, primitive 3.** Two classical bounds on the Bayes error
> sit on either side of the binary case:
>
> - **Fano** (any $K \ge 2$) bounds $H(Y\mid\hat Y)$ from above by
>   $H_{\mathrm{bin}}(\varepsilon) + \varepsilon \log_2 (K-1)$.
> - **Hellman–Raviv** (binary, $K=2$) bounds $\varepsilon$ from
>   above by $H_{\mathrm{bin}}(\varepsilon) / 2$ — sharper but
>   doesn't generalise cleanly.
>
> This notebook *shows* both inequalities live. The §Exercises ask
> you to replicate the demonstration with different $K$ and to
> falsify the HR bound by feeding it to $K = 3$.
"""

# ╔═╡ a0000003-0000-0000-0000-000000000003
md"""
## 1. The binary entropy helper (recap from NB01)
"""

# ╔═╡ a0000003-0000-0000-0000-000000000004
Hbin(p::Real) = (p ≤ 0 || p ≥ 1) ? 0.0 : -p*log2(p) - (1-p)*log2(1-p)

# ╔═╡ a0000003-0000-0000-0000-000000000005
md"""
## 2. Sliders — $\varepsilon$ and $K$
"""

# ╔═╡ a0000003-0000-0000-0000-000000000006
@bind ε Slider(0.0:0.001:0.5, default=0.2, show_value=true)

# ╔═╡ a0000003-0000-0000-0000-000000000007
@bind K Select([2, 3, 4, 5, 10])

# ╔═╡ a0000003-0000-0000-0000-000000000008
md"""
## 3. The two bounds, evaluated at the slider position

- `fano_upper_HY(ε, K)` $= H_{\mathrm{bin}}(\varepsilon) + \varepsilon \log_2 (K-1)$ —
  an upper bound on $H(Y\mid\hat Y)$.
- `hr_upper_ε(ε)` $= H_{\mathrm{bin}}(\varepsilon) / 2$ — an upper
  bound on $\varepsilon$ itself (the Bayes error for $K=2$).
"""

# ╔═╡ a0000003-0000-0000-0000-000000000009
begin
    fano_upper_HY(ε, K) = K == 1 ? 0.0 : Hbin(ε) + ε * log2(max(K-1, 1))
    hr_upper_ε(ε)       = Hbin(ε) / 2

    md"""
    | quantity | value (bits) |
    |---|---|
    | $\varepsilon$ (slider) | $(round(ε; digits=4)) |
    | $K$ (slider) | $(K) |
    | Fano upper on $H(Y\mid\hat Y)$ | $(round(fano_upper_HY(ε, K); digits=4)) |
    | HR upper on $\varepsilon$ (binary only) | $(round(hr_upper_ε(ε); digits=4)) |
    | HR holds? $\varepsilon \le H_{\mathrm{bin}}(\varepsilon)/2$ | $(ε ≤ hr_upper_ε(ε) + 1e-12) |
    """
end

# ╔═╡ a0000003-0000-0000-0000-00000000000a
md"""
## 4. Plot — Fano across $\varepsilon$, one curve per $K$

The curves separate as $K$ grows: more classes give Fano more room
to absorb a mistake.
"""

# ╔═╡ a0000003-0000-0000-0000-00000000000b
begin
    εs   = 0.0:0.001:0.5
    plt1 = plot(legend = :topleft, xlabel = L"\varepsilon",
                ylabel = L"\mathrm{Fano\ upper\ on\ } H(Y\mid\hat Y)")
    for Ki in (2, 3, 5, 10)
        plot!(plt1, εs, [fano_upper_HY(εi, Ki) for εi in εs];
              label = "K = $(Ki)", lw=2)
    end
    vline!(plt1, [ε]; label = L"\mathrm{slider}\;\varepsilon",
           c=:red, ls=:dot)
    plt1
end

# ╔═╡ a0000003-0000-0000-0000-00000000000c
md"""
## 5. Plot — HR (binary) vs the trivial $\varepsilon \le 1/2$

HR is **tighter** than the trivial bound on every $\varepsilon$;
it's the binary special case of the partition bracket NB05 builds.
"""

# ╔═╡ a0000003-0000-0000-0000-00000000000d
begin
    plt2 = plot(εs, [hr_upper_ε(εi) for εi in εs];
                label = L"\mathrm{HR}: \varepsilon \le H_{\mathrm{bin}}(\varepsilon)/2",
                lw = 2, xlabel = L"\varepsilon",
                ylabel = "upper bound on " * L"\varepsilon")
    plot!(plt2, εs, fill(0.5, length(εs));
          label = L"\mathrm{trivial}: \varepsilon \le 1/2",
          lw = 2, ls = :dash)
    plot!(plt2, εs, εs; label = L"y=\varepsilon",
          lw = 1, c = :black, ls = :dot)
    plt2
end

# ╔═╡ a0000003-0000-0000-0000-00000000000e
md"""
## 6. Falsify — try to use HR for $K = 3$

HR is **not** a valid upper bound on $\varepsilon$ when $K > 2$.
Construct a 3-class distribution whose Bayes error exceeds
$H_{\mathrm{bin}}(\varepsilon)/2$: take $P_Y = (1/3, 1/3, 1/3)$,
optimal classifier always wrong; then $\varepsilon = 2/3$, but
$H_{\mathrm{bin}}(2/3)/2 \approx 0.459$. HR would 'predict'
$\varepsilon \le 0.459 < 2/3$ — wrong.
"""

# ╔═╡ a0000003-0000-0000-0000-00000000000f
let
    ε3 = 2/3
    hr = Hbin(ε3) / 2
    @assert ε3 > hr  # HR fails on K=3
    md"""
    For 3 uniform classes with a constant-prediction classifier:
    - true $\varepsilon = 2/3 \approx $(round(ε3; digits=4))$
    - HR 'upper bound' $= H_{\mathrm{bin}}(2/3)/2 \approx $(round(hr; digits=4))$
    - $\varepsilon > \text{HR}$? **$(ε3 > hr)** — HR violated.

    Fano on the same instance:
    \$\$
    H(Y) = \log_2 3 \approx $(round(log2(3); digits=4)) \le H_{\mathrm{bin}}(2/3) + (2/3) \log_2 2 \approx $(round(Hbin(2/3) + (2/3)*log2(2); digits=4))
    \$\$
    — Fano still holds, as advertised.
    """
end

# ╔═╡ a0000003-0000-0000-0000-000000000010
md"""
## 7. Distinguish (the two-line drill)

- **Fano** bounds $H(Y\mid\hat Y)$ — the *residual uncertainty*
  about $Y$ after seeing the predictor — from above, in terms of
  $\varepsilon$ and $K$. Holds for all $K$.
- **HR** bounds $\varepsilon$ — the *Bayes error itself* — from
  above, in terms of $H_{\mathrm{bin}}(\varepsilon)$. Binary only.

What fails for $K \ge 3$: HR's derivation uses
$H(Y\mid\hat Y) \le H_{\mathrm{bin}}(\varepsilon)$, which is only
the binary special case of Fano (the $\varepsilon \log_2 (K-1)$
term is absent at $K=2$).
"""

# ╔═╡ a0000003-0000-0000-0000-000000000011
md"""
## 8. Exercises — replicate, don't derive

### E1. Re-plot Fano for $K \in \{2, 4, 8, 16\}$

Re-do §4 with the new set of $K$ values; observe the spacing
between curves is roughly $\log_2 K$ apart at $\varepsilon = 1/2$.
"""

# ╔═╡ a0000003-0000-0000-0000-000000000012
let
    εs2 = 0.0:0.001:0.5
    pp = plot(xlabel = L"\varepsilon",
              ylabel = L"\mathrm{Fano\ upper}", legend=:topleft)
    for Ki in (2, 4, 8, 16)
        plot!(pp, εs2, [fano_upper_HY(εi, Ki) for εi in εs2];
              label = "K = $(Ki)", lw=2)
    end
    pp
end

# ╔═╡ a0000003-0000-0000-0000-000000000013
md"""
### E2. Falsify HR on $K = 5$

Build a 5-class uniform distribution. Compute $\varepsilon$ and HR
'upper'. Confirm HR is violated. (Replication of §6 with $K = 5$.)
"""

# ╔═╡ a0000003-0000-0000-0000-000000000014
let
    K5  = 5
    εK  = 1 - 1/K5
    hrK = Hbin(εK)/2
    md"""
    - true $\varepsilon = 1 - 1/K = $(round(εK; digits=4))$
    - HR 'upper' $= $(round(hrK; digits=4))$
    - HR violated? $(εK > hrK)
    """
end

# ╔═╡ a0000003-0000-0000-0000-000000000015
md"""
### E3. Verify HR is **tight** at $\varepsilon = 0$ and $\varepsilon = 1/2$

At the two extremes the HR upper coincides with the truth's
boundary. Plot the gap $\mathrm{HR}(\varepsilon) - \varepsilon$
and read off the maximum gap location (it's at the same
$\varepsilon^* = 1/5$ NB05 finds for the partition bracket).
"""

# ╔═╡ a0000003-0000-0000-0000-000000000016
let
    εs3 = 0.001:0.001:0.499
    gap = [Hbin(εi)/2 - εi for εi in εs3]
    i_max = argmax(gap)
    pp = plot(εs3, gap; lw=2,
              xlabel=L"\varepsilon", ylabel=L"HR - \varepsilon",
              label="HR gap")
    scatter!(pp, [εs3[i_max]], [gap[i_max]];
             label="max gap at ε ≈ $(round(εs3[i_max]; digits=3))",
             ms=6, c=:red)
    pp
end

# ╔═╡ a0000003-0000-0000-0000-000000000017
md"""
### E4. Compare Fano on $K = 2$ to HR

For $K = 2$ Fano reduces to $H_{\mathrm{bin}}(\varepsilon)$;
HR is $H_{\mathrm{bin}}(\varepsilon)/2$. The two bound *different
quantities* — Fano bounds $H(Y\mid\hat Y)$, HR bounds
$\varepsilon$. Plot both and note: they share the same shape but
not the same target.
"""

# ╔═╡ a0000003-0000-0000-0000-000000000018
let
    εs4 = 0.0:0.001:0.5
    plot(εs4, [fano_upper_HY(εi, 2) for εi in εs4];
         label = "Fano K=2 bounds H(Y|Ŷ)", lw=2)
    plot!(εs4, [hr_upper_ε(εi) for εi in εs4];
          label = "HR binary bounds ε", lw=2, ls=:dash)
    xlabel!(L"\varepsilon"); ylabel!("bits  /  error")
end

# ╔═╡ a0000003-0000-0000-0000-000000000019
md"""
## 9. Next — NB04: Bayes-error landscape on a 3-cell partition

NB04 starts the bracket story by computing $\varepsilon(\Pi)$ and
$H(Y\mid\Pi)$ on a sliding 3-cell partition. NB05 then assembles
the bracket itself.
"""

# ╔═╡ Cell order:
# ╠═a0000003-0000-0000-0000-000000000001
# ╟─a0000003-0000-0000-0000-000000000002
# ╟─a0000003-0000-0000-0000-000000000003
# ╠═a0000003-0000-0000-0000-000000000004
# ╟─a0000003-0000-0000-0000-000000000005
# ╠═a0000003-0000-0000-0000-000000000006
# ╠═a0000003-0000-0000-0000-000000000007
# ╟─a0000003-0000-0000-0000-000000000008
# ╠═a0000003-0000-0000-0000-000000000009
# ╟─a0000003-0000-0000-0000-00000000000a
# ╠═a0000003-0000-0000-0000-00000000000b
# ╟─a0000003-0000-0000-0000-00000000000c
# ╠═a0000003-0000-0000-0000-00000000000d
# ╟─a0000003-0000-0000-0000-00000000000e
# ╠═a0000003-0000-0000-0000-00000000000f
# ╟─a0000003-0000-0000-0000-000000000010
# ╟─a0000003-0000-0000-0000-000000000011
# ╠═a0000003-0000-0000-0000-000000000012
# ╟─a0000003-0000-0000-0000-000000000013
# ╠═a0000003-0000-0000-0000-000000000014
# ╟─a0000003-0000-0000-0000-000000000015
# ╠═a0000003-0000-0000-0000-000000000016
# ╟─a0000003-0000-0000-0000-000000000017
# ╠═a0000003-0000-0000-0000-000000000018
# ╟─a0000003-0000-0000-0000-000000000019
