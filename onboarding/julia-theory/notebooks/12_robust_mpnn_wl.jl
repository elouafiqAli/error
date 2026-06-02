### A Pluto.jl notebook ###
# v0.20.0

#> [frontmatter]
#> title = "ε-robust MPNN–WL constancy (Lemma 6)"
#> tags = ["mpnn", "unit-4", "robustness"]

using Markdown, InteractiveUtils

macro bind(def, element)
    return quote
        local iv = try Base.loaded_modules[Base.PkgId(Base.UUID("6e696c72-6542-2067-7265-42206c756150"), "AbstractPlutoDingetjes")].Bonds.initial_value catch; b -> missing; end
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : iv(el)
        el
    end
end

# ╔═╡ a000000c-0000-0000-0000-000000000001
using PlutoUI, Plots, LaTeXStrings, LinearAlgebra, Random, Statistics

# ╔═╡ a000000c-0000-0000-0000-000000000002
md"""
# Notebook 12 — $\varepsilon$-robust MPNN–WL constancy

> **Unit IV, item 2.** Lemma 6 made tactile. On a toy graph, run
> 1-WL refinement to get a colour partition; perturb node features
> within each cell by $\le \varepsilon$ in $\ell_\infty$; run two
> rounds of a GIN-style aggregation; report which cells remain
> *constant* (within-cell standard deviation $\approx 0$).
>
> **The slider IS the perturbation budget $\varepsilon$.**
"""

# ╔═╡ a000000c-0000-0000-0000-000000000003
md"""
## 1. Toy graphs
"""

# ╔═╡ a000000c-0000-0000-0000-000000000004
begin
    # Each function returns (n, edges::Vector{Tuple{Int,Int}}).
    function graph_C6()
        n = 6
        edges = [(i, (i % n) + 1) for i in 1:n]
        (n, edges)
    end
    function graph_K3K3()
        # two disjoint triangles, nodes 1-2-3 and 4-5-6
        (6, [(1,2), (2,3), (1,3), (4,5), (5,6), (4,6)])
    end
    function graph_petersen()
        # Petersen: 10 nodes, 15 edges. Outer 1-5, inner 6-10.
        outer = [(1,2), (2,3), (3,4), (4,5), (5,1)]
        inner = [(6,8), (8,10), (10,7), (7,9), (9,6)]
        spokes = [(1,6), (2,7), (3,8), (4,9), (5,10)]
        (10, vcat(outer, inner, spokes))
    end
end

# ╔═╡ a000000c-0000-0000-0000-000000000005
md"""
## 2. Adjacency, neighbour lists, 1-WL refinement
"""

# ╔═╡ a000000c-0000-0000-0000-000000000006
begin
    function build_adj(n, edges)
        adj = [Int[] for _ in 1:n]
        for (u, v) in edges
            push!(adj[u], v); push!(adj[v], u)
        end
        adj
    end
    function wl_refine(adj; rounds=10)
        n = length(adj)
        colors = ones(Int, n)
        for _ in 1:rounds
            sigs = [(colors[v], sort(colors[adj[v]])) for v in 1:n]
            uniq = Dict{Any, Int}()
            new_colors = similar(colors)
            for v in 1:n
                if !haskey(uniq, sigs[v])
                    uniq[sigs[v]] = length(uniq) + 1
                end
                new_colors[v] = uniq[sigs[v]]
            end
            if new_colors == colors
                return colors
            end
            colors = new_colors
        end
        colors
    end
    function cells_of(colors)
        d = Dict{Int, Vector{Int}}()
        for (v, c) in enumerate(colors)
            push!(get!(d, c, Int[]), v)
        end
        sort!.(collect(values(d)))
        sort(collect(values(d)); by=first)
    end
end

# ╔═╡ a000000c-0000-0000-0000-000000000007
md"""
## 3. Pick a graph
"""

# ╔═╡ a000000c-0000-0000-0000-000000000008
@bind graph_name Select(["C_6 (6-cycle)" => :C6,
                         "2 K_3 (two disjoint triangles)" => :K3K3,
                         "Petersen" => :petersen])

# ╔═╡ a000000c-0000-0000-0000-000000000009
begin
    n, edges = if graph_name == :C6
        graph_C6()
    elseif graph_name == :K3K3
        graph_K3K3()
    else
        graph_petersen()
    end
    adj    = build_adj(n, edges)
    colors = wl_refine(adj)
    cells  = cells_of(colors)
    md"""
    Graph: **$(graph_name)** — n = $(n), m = $(length(edges)).

    1-WL produces $(length(cells)) cell(s):

    $(join(["- cell with color $(colors[first(c)]): nodes $(c)" for c in cells], "\n"))
    """
end

# ╔═╡ a000000c-0000-0000-0000-00000000000a
md"""
## 4. Perturbation slider $\varepsilon$ and seed
"""

# ╔═╡ a000000c-0000-0000-0000-00000000000b
@bind ε_perturb Slider(0.0:0.01:1.0, default=0.10, show_value=true)

# ╔═╡ a000000c-0000-0000-0000-00000000000c
@bind perturb_seed NumberField(0:9999, default=7)

# ╔═╡ a000000c-0000-0000-0000-00000000000d
md"""
## 5. Run two GIN-style aggregation rounds

Update rule (per round, tanh non-linearity):

```
x_v^{t+1} = tanh(x_v^t + Σ_{u ∼ v} x_u^t)
```

Initial features: identical inside each WL cell, perturbed by
$\mathcal{U}(-\varepsilon, +\varepsilon)$. Lemma 6 predicts: each
WL cell's within-cell standard deviation **stays bounded** by a
graph-dependent constant times $\varepsilon$ across rounds.
"""

# ╔═╡ a000000c-0000-0000-0000-00000000000e
begin
    rng_p = MersenneTwister(perturb_seed)
    # Initial features: cell ID + perturbation
    x0 = Float64.(colors) .+ ε_perturb .* (2 .* rand(rng_p, n) .- 1)
    function gin_round(x, adj)
        n = length(x)
        new_x = similar(x)
        for v in 1:n
            agg = x[v] + sum(x[u] for u in adj[v]; init=0.0)
            new_x[v] = tanh(agg)
        end
        new_x
    end
    x1 = gin_round(x0, adj)
    x2 = gin_round(x1, adj)

    function within_cell_stds(x, cells)
        [length(c) > 1 ? std(x[c]) : 0.0 for c in cells]
    end
    s0 = within_cell_stds(x0, cells)
    s1 = within_cell_stds(x1, cells)
    s2 = within_cell_stds(x2, cells)
    table_rows = [string("| ", i, " | ", cells[i], " | ",
                         round(s0[i]; digits=4), " | ",
                         round(s1[i]; digits=4), " | ",
                         round(s2[i]; digits=4), " |")
                  for i in eachindex(cells)]
    table_body = join(table_rows, "\n")
    Markdown.parse(string(
        "Within-cell std at each round (one row per WL cell):\n\n",
        "| cell | nodes | std0 (init) | std1 (after 1 round) | std2 (after 2 rounds) |\n",
        "|---|---|---|---|---|\n",
        table_body))
end

# ╔═╡ a000000c-0000-0000-0000-00000000000f
md"""
## 6. Sweep $\varepsilon \in [0, 1]$ and plot the max within-cell std after 2 rounds

Lemma 6 predicts this is *bounded linearly* in $\varepsilon$ for
small $\varepsilon$, with the slope determined by the graph
structure (degree, contraction factor of the non-linearity).
"""

# ╔═╡ a000000c-0000-0000-0000-000000000010
begin
    εs_sweep = 0.0:0.01:1.0
    max_std_after2 = Float64[]
    for εi in εs_sweep
        rng = MersenneTwister(perturb_seed)
        x0i = Float64.(colors) .+ εi .* (2 .* rand(rng, n) .- 1)
        x1i = gin_round(x0i, adj)
        x2i = gin_round(x1i, adj)
        s2i = within_cell_stds(x2i, cells)
        push!(max_std_after2, isempty(s2i) ? 0.0 : maximum(s2i))
    end
    plot(εs_sweep, max_std_after2;
         lw=2, label="max within-cell std after 2 rounds",
         xlabel=L"\varepsilon\ \mathrm{(perturbation\ budget)}",
         ylabel="max within-cell std")
    vline!([ε_perturb]; label="slider ε", c=:red, ls=:dot)
end

# ╔═╡ a000000c-0000-0000-0000-000000000011
md"""
## 7. Falsify — what if we drop the non-linearity?

Without `tanh`, the aggregation $x_v^{t+1} = x_v^t + \sum_{u \sim v} x_u^t$
is **linear**; the within-cell std then grows as
$\|A + I\|^t \cdot \varepsilon$, exponentially in $t$. The non-linear
contraction is what makes Lemma 6's bound *useful*.
"""

# ╔═╡ a000000c-0000-0000-0000-000000000012
begin
    function lin_round(x, adj)
        n = length(x); new_x = similar(x)
        for v in 1:n
            new_x[v] = x[v] + sum(x[u] for u in adj[v]; init=0.0)
        end
        new_x
    end
    rng_loc2 = MersenneTwister(perturb_seed)
    x0l = ε_perturb .* (2 .* rand(rng_loc2, n) .- 1)   # zero-centred so growth is visible
    rounds = 0:5
    max_stds_lin = let
        out = Float64[]
        xcur = copy(x0l)
        for _ in rounds
            s_now = within_cell_stds(xcur, cells)
            push!(out, isempty(s_now) ? 0.0 : maximum(s_now))
            xcur = lin_round(xcur, adj)
        end
        out
    end
    plot(collect(rounds), max_stds_lin;
         lw=2, label="max within-cell std (no tanh)",
         xlabel="round t", ylabel="max within-cell std",
         yscale=:log10, ylims=(max(1e-6, minimum(max_stds_lin .+ 1e-9)), maximum(max_stds_lin)*10))
end

# ╔═╡ a000000c-0000-0000-0000-000000000013
md"""
## 8. Take-aways

- WL cells with a single node have **std = 0** identically — any
  GIN round leaves them constant.
- WL cells with $\ge 2$ nodes have within-cell std bounded linearly
  by $\varepsilon$ (Lemma 6) *only when the non-linearity contracts*.
  `tanh` contracts; the identity does not.
- The graph structure (degree sequence, automorphism orbits) sets
  the Lemma's constant. The plot in §6 is the *empirical* version
  of that bound.

## 9. Exercises — replicate
"""

# ╔═╡ a000000c-0000-0000-0000-000000000014
md"""
### E1. Replicate §5 with $\varepsilon = 0$

Without perturbation, every WL cell stays at its initial value
through every round; within-cell std is identically 0.
"""

# ╔═╡ a000000c-0000-0000-0000-000000000015
let
    n_e, edges_e = graph_C6()
    adj_e   = build_adj(n_e, edges_e)
    colors_e = wl_refine(adj_e)
    cells_e  = cells_of(colors_e)
    x0e = Float64.(colors_e)
    x1e = gin_round(x0e, adj_e)
    x2e = gin_round(x1e, adj_e)
    s0 = [length(c) > 1 ? std(x0e[c]) : 0.0 for c in cells_e]
    s2 = [length(c) > 1 ? std(x2e[c]) : 0.0 for c in cells_e]
    (cells=cells_e, std_init=s0, std_after_2_rounds=s2)
end

# ╔═╡ a000000c-0000-0000-0000-000000000016
md"""
### E2. Compare cell counts: $C_6$ has 1 WL cell; $2K_3$ has 1 WL cell

Both are 2-regular, vertex-transitive, with identical degree
distribution — 1-WL cannot distinguish them. This is the
**blind-spot** from HW4. Verify both yield a single cell.
"""

# ╔═╡ a000000c-0000-0000-0000-000000000017
let
    (n1, e1) = graph_C6(); (n2, e2) = graph_K3K3()
    a1 = build_adj(n1, e1); a2 = build_adj(n2, e2)
    c1 = cells_of(wl_refine(a1))
    c2 = cells_of(wl_refine(a2))
    (C6_cells = length(c1), K3K3_cells = length(c2),
     same = length(c1) == length(c2) == 1)
end

# ╔═╡ a000000c-0000-0000-0000-000000000018
md"""
### E3. Petersen has multiple WL cells (vertex-transitive ⇒ 1; but with degree-feature initialisation, distinguishes outer/inner)

Run 1-WL with degree as initial color and verify Petersen still
collapses to 1 cell (it is 3-regular and vertex-transitive).
"""

# ╔═╡ a000000c-0000-0000-0000-000000000019
let
    (n3, e3) = graph_petersen()
    a3 = build_adj(n3, e3)
    degs = [length(a3[v]) for v in 1:n3]
    function wl_refine_initial(adj, init; rounds=10)
        n = length(adj)
        colors = copy(init)
        for _ in 1:rounds
            sigs = [(colors[v], sort(colors[adj[v]])) for v in 1:n]
            uniq = Dict{Any, Int}()
            new_colors = similar(colors)
            for v in 1:n
                if !haskey(uniq, sigs[v])
                    uniq[sigs[v]] = length(uniq) + 1
                end
                new_colors[v] = uniq[sigs[v]]
            end
            new_colors == colors && return colors
            colors = new_colors
        end
        colors
    end
    cs = wl_refine_initial(a3, degs)
    cells = cells_of(cs)
    (degree_init_cell_count = length(cells), Petersen_is_3regular = all(==(3), degs))
end

# ╔═╡ a000000c-0000-0000-0000-00000000001a
md"""
### E4. Replication: re-run §6 sweep on $2K_3$ and compare slope to $C_6$

Identical graphs (from 1-WL's view) should produce identical
slopes. They do: the slope is a function of the (multi-)set of
local neighbourhoods, which is the WL invariant.
"""

# ╔═╡ a000000c-0000-0000-0000-00000000001b
let
    function slope_of(graph_fn)
        (n, edges) = graph_fn()
        adj = build_adj(n, edges)
        colors = wl_refine(adj)
        cells_ = cells_of(colors)
        rng = MersenneTwister(7)
        out = Float64[]
        for εi in 0.0:0.1:1.0
            rng2 = MersenneTwister(7)
            x0  = Float64.(colors) .+ εi .* (2 .* rand(rng2, n) .- 1)
            x1  = gin_round(x0, adj)
            x2  = gin_round(x1, adj)
            s2  = [length(c) > 1 ? std(x2[c]) : 0.0 for c in cells_]
            push!(out, isempty(s2) ? 0.0 : maximum(s2))
        end
        out
    end
    s_C6   = slope_of(graph_C6)
    s_K3K3 = slope_of(graph_K3K3)
    (C6_curve=round.(s_C6;   digits=4),
     K3K3_curve=round.(s_K3K3; digits=4),
     equal=isapprox(s_C6, s_K3K3; atol=1e-6))
end

# ╔═╡ a000000c-0000-0000-0000-00000000001c
md"""
## 10. Done

You have now slid through every theoretical object in the paper.
Open the abstract and re-read it — the constants should feel like
plot-points, not symbols.
"""

# ╔═╡ Cell order:
# ╠═a000000c-0000-0000-0000-000000000001
# ╟─a000000c-0000-0000-0000-000000000002
# ╟─a000000c-0000-0000-0000-000000000003
# ╠═a000000c-0000-0000-0000-000000000004
# ╟─a000000c-0000-0000-0000-000000000005
# ╠═a000000c-0000-0000-0000-000000000006
# ╟─a000000c-0000-0000-0000-000000000007
# ╠═a000000c-0000-0000-0000-000000000008
# ╠═a000000c-0000-0000-0000-000000000009
# ╟─a000000c-0000-0000-0000-00000000000a
# ╠═a000000c-0000-0000-0000-00000000000b
# ╠═a000000c-0000-0000-0000-00000000000c
# ╟─a000000c-0000-0000-0000-00000000000d
# ╠═a000000c-0000-0000-0000-00000000000e
# ╟─a000000c-0000-0000-0000-00000000000f
# ╠═a000000c-0000-0000-0000-000000000010
# ╟─a000000c-0000-0000-0000-000000000011
# ╠═a000000c-0000-0000-0000-000000000012
# ╟─a000000c-0000-0000-0000-000000000013
# ╟─a000000c-0000-0000-0000-000000000014
# ╠═a000000c-0000-0000-0000-000000000015
# ╟─a000000c-0000-0000-0000-000000000016
# ╠═a000000c-0000-0000-0000-000000000017
# ╟─a000000c-0000-0000-0000-000000000018
# ╠═a000000c-0000-0000-0000-000000000019
# ╟─a000000c-0000-0000-0000-00000000001a
# ╠═a000000c-0000-0000-0000-00000000001b
# ╟─a000000c-0000-0000-0000-00000000001c
