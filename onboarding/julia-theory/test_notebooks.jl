# Harness: load each Pluto notebook, evaluate every code cell in a fresh
# module via Core.eval (Pluto's actual semantics: each cell evaluated at
# the top of the workspace, soft-scope = interactive). Reports per-cell
# success/failure. Skips @bind cells gracefully (the shim sets vars to
# missing; cells that consume them may still error — that's reported).
using Pluto

const NOTEBOOK_DIR = joinpath(@__DIR__, "notebooks")

function run_notebook(path::AbstractString)
    println("=== ", basename(path))
    nb = Pluto.load_notebook(path; disable_writing_notebook_files=true)
    M  = Module(:NB)
    # Bring required base into M and let it `eval` symbolic build_functions.
    Core.eval(M, :(using Markdown, InteractiveUtils))
    Core.eval(M, :(const eval = Core.eval; const include = Base.include))
    # Evaluate the file preamble (the @bind shim macro lives there).
    src = read(path, String)
    pre_end = findfirst("# ╔═╡", src)
    if pre_end !== nothing
        preamble = src[1:first(pre_end)-1]
        try
            Core.eval(M, Meta.parseall(preamble))
        catch e
            println("  ✗ preamble: ", first(sprint(showerror, e), 200))
        end
    end
    n_ok = 0
    n_err = 0
    for cid in nb.cell_order
        c = nb.cells_dict[cid]
        code = strip(c.code)
        isempty(code) && continue
        startswith(string(cid), "00000000") && continue
        try
            Core.eval(M, Meta.parseall(code))
            n_ok += 1
        catch e
            n_err += 1
            short = sprint(showerror, e)
            println("  ✗ cell ", cid)
            println("    code: ", first(replace(code, '\n' => " | "), 120))
            println("    err:  ", first(short, 200))
        end
    end
    println("  → ", n_ok, " ok, ", n_err, " err")
    return n_err
end

total = Ref(0)
for f in sort(readdir(NOTEBOOK_DIR; join=true))
    endswith(f, ".jl") || continue
    occursin("backup", f) && continue
    try
        total[] += run_notebook(f)
    catch e
        println("  ✗✗ load failed: ", basename(f), " — ", sprint(showerror, e))
        total[] += 1
    end
end
println("=== TOTAL errors: ", total[])
exit(total[] == 0 ? 0 : 1)
