"""
apply_5of5_manuscript_patch.py
==============================

One-shot, idempotent manuscript patch: after merge_to_5of5.py has
produced experiments/results/e3d_arch_full.5of5.json, this script:

  1. Loads the 5/5 JSON.
  2. Computes the ogbn-arxiv per-arch mean ± std at the largest
     k_grid point (matched to the existing E3d-arch-full table
     convention: largest k <= k_WL, capped at 4096).
  3. Appends a new row block to BOTH main.md and main.tex inside the
     existing E3d-arch-full table (between the Twitch-EN block and
     the closing of tab:e3d-arch-full).
  4. Replaces the 'limitation' paragraph that says ogbn-arxiv is
     excluded with a closing-the-loop paragraph that cites the 5/5
     JSON and notes the same k-mismatch caveat already applied to
     PubMed and Twitch-EN.
  5. Rebuilds the PDF (calls `make` in partition-sandwich-preprint).

Idempotency:
  Detects the existing 'ogbn-arxiv ...' table row and 'Limitation.'
  paragraph; aborts with a no-op if the patch has already been
  applied.

Usage (from repo root):
  python3 partition-sandwich-preprint/experiments/runpod/apply_5of5_manuscript_patch.py \\
      --jsondir partition-sandwich-preprint/experiments/results

The defaults assume the canonical paths in the repo.
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PAPER_DIR = REPO_ROOT / "partition-sandwich-preprint"


def _mean_std(xs):
    return st.mean(xs), st.pstdev(xs)


def _compute_ogbn_summary(jsondir: Path) -> dict:
    five = json.loads((jsondir / "e3d_arch_full.5of5.json").read_text())
    ogbn = next(d for d in five["datasets"] if d["name"] == "ogbn_arxiv")
    eps_WL = ogbn["eps_WL"]
    k_WL = ogbn["k_WL"]
    k_grid = ogbn["k_grid"]
    K = max(k for k in k_grid if k <= k_WL)
    out = {"eps_WL": eps_WL, "k_WL": k_WL, "K_eval": K,
           "n": ogbn["n"], "pi": ogbn["pi"], "rows": {}}
    for arch in ["GCN", "GAT", "GIN", "SAGE"]:
        runs = [r for r in ogbn["runs"] if r["arch"] == arch]
        cells = [next(c for c in r["k_sweep"] if c["k_requested"] == K)
                 for r in runs]
        Rh = [r["Rhat"] for r in runs]
        Et = [c["eps_trained"] for c in cells]
        Fg = [c["feature_gap_at_k"] for c in cells]
        Hs = [c["head_signal_at_k"] for c in cells]
        out["rows"][arch] = {
            "Rhat": _mean_std(Rh),
            "eps_tr": _mean_std(Et),
            "feat_gap": _mean_std(Fg),
            "head_sig": _mean_std(Hs),
        }
    return out


def _fmt_md_row(arch: str, s: dict) -> str:
    def msd(t, signed=False):
        m, sd = t
        if signed:
            return f"{m:+.3f} ± {sd:.3f}"
        return f"{m:.3f} ± {sd:.3f}"

    fg_m = s["feat_gap"][0]
    bold_open, bold_close = ("**", "**") if fg_m < 0 else ("", "")
    return (
        f"| | {arch} | {msd(s['Rhat'])} | {msd(s['eps_tr'])} | "
        f"{bold_open}{msd(s['feat_gap'], signed=True)}{bold_close} | "
        f"{msd(s['head_sig'], signed=True).replace('+', '−' if s['head_sig'][0] < 0 else '+')} |"
    )


def _fmt_tex_row(arch: str, s: dict) -> str:
    def msd(t, signed=False):
        m, sd = t
        if signed:
            sign = "+" if m >= 0 else "-"
            return f"${sign}{abs(m):.3f}{{\\pm}}{sd:.3f}$"
        return f"${m:.3f}{{\\pm}}{sd:.3f}$"

    fg = s["feat_gap"]
    fg_str = msd(fg, signed=True)
    if fg[0] < 0:
        fg_str = f"$\\mathbf{{{fg_str.strip('$')}}}$"
    return (
        f" & {arch:5s} & {msd(s['Rhat'])} & {msd(s['eps_tr'])} & "
        f"{fg_str} & {msd(s['head_sig'], signed=True)} \\\\"
    )


def _patch_md(md_path: Path, summary: dict) -> bool:
    src = md_path.read_text()
    if "ogbn-arxiv (0.0169" in src or "ogbn-arxiv (0.0" in src and "k=4096" in src:
        # Already patched (best-effort detection).
        return False

    # Build the ogbn-arxiv markdown rows.
    s = summary
    K = s["K_eval"]
    k_WL = s["k_WL"]
    eps_WL = s["eps_WL"]
    header = (
        f"| ogbn-arxiv ({eps_WL:.4f}, k={K}<k_WL={k_WL}) |"
    )
    md_rows_lines = [header + _fmt_md_row("GCN", s["rows"]["GCN"]).split("| |", 1)[1]]
    for arch in ["GAT", "GIN", "SAGE"]:
        md_rows_lines.append(_fmt_md_row(arch, s["rows"][arch]))
    md_block = "\n".join(md_rows_lines) + "\n"

    # Insert just before the empty line that follows the Twitch-EN/SAGE row.
    marker = "| | SAGE | 0.376 ± 0.009 | 0.181 ± 0.005 | **−0.154 ± 0.005** | −0.195 ± 0.012 |\n"
    if marker not in src:
        print("[patch-md] WARN: Twitch-EN/SAGE marker row not found; "
              "the manuscript may have drifted. Aborting MD patch.",
              file=sys.stderr)
        return False
    src = src.replace(marker, marker + md_block)

    # Replace the 'Limitation. ogbn-arxiv ... not included' paragraph.
    old_limit = "**Limitation.** ogbn-arxiv (the fifth dataset of E3) is not\nincluded in this sweep:"
    if old_limit in src:
        # Cut from old_limit up to the next '#### ' heading.
        start = src.index(old_limit)
        end_marker = "\n#### "
        end = src.index(end_marker, start)
        new_block = (
            "**Closing the loop on ogbn-arxiv.** The ogbn-arxiv row\n"
            f"(eval $k = {K} < k_{{\\mathrm{{WL}}}} = {k_WL}$, 5 seeds,\n"
            "CUDA + CPU two-phase split, see\n"
            "`experiments/runpod/README.md`) inherits the same\n"
            "$k$-budget caveat as PubMed and Twitch-EN: $\\varepsilon^*\n"
            "_{\\Pi^{\\mathrm{tr}}_k}$ is evaluated on a coarser\n"
            "partition than $\\varepsilon_{\\mathrm{WL}}$, so a negative\n"
            "feat\\_gap conflates features-vs-WL with $k$-mismatch. The\n"
            "raw 5/5 merge is at\n"
            "`experiments/results/e3d_arch_full.5of5.json`\n"
            "(merge provenance recorded inline; CUDA L4 Phase 1 + CPU\n"
            "Phase 2 walls separately stamped).\n\n"
        )
        src = src[:start] + new_block + src[end:]
    md_path.write_text(src)
    return True


def _patch_tex(tex_path: Path, summary: dict) -> bool:
    src = tex_path.read_text()
    if "ogbn-arxiv ($k{=}" in src:
        return False

    s = summary
    K = s["K_eval"]
    k_WL = s["k_WL"]
    eps_WL = s["eps_WL"]
    k_WL_tex = f"{k_WL:,}".replace(",", r"\,")
    header = (
        f"\\midrule\n"
        f"ogbn-arxiv ($k{{=}}{K}{{<}}k_{{\\mathrm{{WL}}}}{{=}}{k_WL_tex}$)\n"
    )
    tex_rows = [_fmt_tex_row(a, s["rows"][a]) for a in ["GCN", "GAT", "GIN", "SAGE"]]
    tex_block = header + "\n".join(tex_rows) + "\n"

    # Insert just before the \bottomrule of tab:e3d-arch-full.
    marker = " & SAGE & $0.376{\\pm}0.009$ & $0.181{\\pm}0.005$ & $\\mathbf{-0.154{\\pm}0.005}$ & $-0.195{\\pm}0.012$ \\\\\n\\bottomrule"
    if marker not in src:
        print("[patch-tex] WARN: Twitch-EN/SAGE \\bottomrule marker not "
              "found; aborting TeX patch.",
              file=sys.stderr)
        return False
    insert = marker.replace("\\bottomrule", tex_block + "\\bottomrule")
    src = src.replace(marker, insert)

    # Replace the \textbf{Limitation:} clause about ogbn-arxiv in the caption.
    old_lim = "\\textbf{Limitation:} ogbn-arxiv (fifth E3 dataset,\n$n = 169\\,343$, $k_{\\mathrm{WL}} = 161\\,943$) is not in this\nsweep;"
    if old_lim in src:
        end = src.index("in the raw output.", src.index(old_lim))
        # Re-find the end of that sentence.
        end = src.index(".", end) + 1
        new_clause = (
            "\\textbf{Closing the loop on ogbn-arxiv:} the ogbn-arxiv "
            f"block uses the same evaluation budget caveat ($k={K}<k_{{\\mathrm{{WL}}}}={k_WL_tex}$); "
            "the 5/5 merge is at "
            "\\texttt{experiments/results/e3d\\_arch\\_full.5of5.json}; "
            "two-phase split docs in \\texttt{experiments/runpod/README.md}."
        )
        src = src[:src.index(old_lim)] + new_clause + src[end:]
    tex_path.write_text(src)
    return True


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--jsondir",
                   default=str(PAPER_DIR / "experiments" / "results"))
    p.add_argument("--md",
                   default=str(PAPER_DIR / "main.md"))
    p.add_argument("--tex",
                   default=str(PAPER_DIR / "main.tex"))
    p.add_argument("--no-build", action="store_true",
                   help="skip `make` after patching")
    args = p.parse_args()

    jsondir = Path(args.jsondir)
    if not (jsondir / "e3d_arch_full.5of5.json").exists():
        print(f"[apply] ERROR: {jsondir}/e3d_arch_full.5of5.json missing.\n"
              f"        Run merge_to_5of5.py first.", file=sys.stderr)
        return 2

    summary = _compute_ogbn_summary(jsondir)

    print(f"[apply] ogbn-arxiv summary @ k={summary['K_eval']} "
          f"(k_WL={summary['k_WL']}, eps_WL={summary['eps_WL']:.4f}):")
    for arch, s in summary["rows"].items():
        print(f"  {arch:5s}  Rhat={s['Rhat'][0]:.3f}+-{s['Rhat'][1]:.3f}  "
              f"eps_tr={s['eps_tr'][0]:.3f}+-{s['eps_tr'][1]:.3f}  "
              f"feat_gap={s['feat_gap'][0]:+.3f}+-{s['feat_gap'][1]:.3f}  "
              f"head_sig={s['head_sig'][0]:+.3f}+-{s['head_sig'][1]:.3f}")

    md_changed = _patch_md(Path(args.md), summary)
    tex_changed = _patch_tex(Path(args.tex), summary)
    print(f"[apply] md_changed={md_changed}  tex_changed={tex_changed}")

    if (md_changed or tex_changed) and not args.no_build:
        print("[apply] running make to rebuild main.pdf ...")
        rc = subprocess.call(["make"], cwd=str(PAPER_DIR))
        if rc != 0:
            print(f"[apply] ERROR: make exited {rc}", file=sys.stderr)
            return rc

    print("[apply] done. Review the diff, then commit with the suggested")
    print("        conventional-commit template from")
    print("        runpod/README.md (5/5 section).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
