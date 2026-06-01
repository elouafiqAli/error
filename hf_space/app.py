"""
HF Space app for D-Full (partition-bracket post-hoc architecture audit).

Runs the 5 dataset x 4 arch x 5 seed = 100-cell grid on ZeroGPU
(H200, on-demand per-call), one dataset per @spaces.GPU(duration=300) call.

UI:
  - "Run dataset" buttons for each of the 5 graphs
  - "Run all" runs them sequentially; results streamed to a JSON viewer.
  - Download button for results/e3d_arch_full.json.

The heavy lifting is in `e3d_arch_full.run_dataset`, imported from the
repo's experiment code which is mounted at the Space root.
"""
import json
import os
import time
from pathlib import Path

import gradio as gr

# spaces.GPU is the ZeroGPU decorator; only available in the Spaces runtime.
try:
    import spaces  # noqa: F401
    HAVE_ZGPU = True
except Exception:
    HAVE_ZGPU = False

    class _FakeSpaces:
        @staticmethod
        def GPU(*a, **kw):
            def deco(f):
                return f
            return deco
    spaces = _FakeSpaces()

# Make the repo's experiments/ importable.
ROOT = Path(__file__).resolve().parent
EXP = ROOT / "experiments"
if EXP.exists():
    import sys
    sys.path.insert(0, str(EXP))

from e3d_arch_full import (DATASET_ORDER, ARCH_ORDER,  # type: ignore
                           run_dataset as _run_dataset_core)
from e3d_data_full import load_wl_ceilings  # type: ignore

RESULTS = EXP / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT_JSON = RESULTS / "e3d_arch_full.json"


def _load_state() -> dict:
    if OUT_JSON.exists():
        try:
            return json.loads(OUT_JSON.read_text())
        except Exception:
            pass
    return {"experiment": "e3d_arch_full",
            "depth_L": 3, "hidden": 128, "epochs": 200,
            "seeds": [0, 1, 2, 3, 4],
            "archs": ARCH_ORDER,
            "datasets_order": DATASET_ORDER,
            "datasets": []}


def _save_state(state: dict) -> None:
    OUT_JSON.write_text(json.dumps(state, indent=2))


def _upsert_dataset(state: dict, ds_result: dict) -> dict:
    out = [d for d in state["datasets"] if d["name"] != ds_result["name"]]
    out.append(ds_result)
    state["datasets"] = sorted(
        out, key=lambda d: DATASET_ORDER.index(d["name"]))
    return state


@spaces.GPU(duration=300)
def _run_one_dataset_gpu(name: str, seeds: tuple[int, ...],
                         epochs: int, hidden: int):
    """Per-dataset GPU call: trains 4 arch x len(seeds) cells on H200."""
    import torch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return _run_dataset_core(name, seeds=tuple(seeds), epochs=epochs,
                             hidden=hidden, device=device, verbose=True)


def run_dataset_ui(name: str, n_seeds: int, epochs: int, hidden: int):
    t0 = time.perf_counter()
    seeds = tuple(range(int(n_seeds)))
    res = _run_one_dataset_gpu(name, seeds, int(epochs), int(hidden))
    state = _load_state()
    state["seeds"] = list(seeds)
    state["epochs"] = int(epochs)
    state["hidden"] = int(hidden)
    state = _upsert_dataset(state, res)
    _save_state(state)
    wall = time.perf_counter() - t0
    summary = _summarise(res, wall)
    return summary, str(OUT_JSON)


def run_all_ui(n_seeds: int, epochs: int, hidden: int):
    seeds = tuple(range(int(n_seeds)))
    state = _load_state()
    state["seeds"] = list(seeds)
    state["epochs"] = int(epochs)
    state["hidden"] = int(hidden)
    lines = []
    t_all = time.perf_counter()
    for name in DATASET_ORDER:
        t0 = time.perf_counter()
        res = _run_one_dataset_gpu(name, seeds, int(epochs), int(hidden))
        state = _upsert_dataset(state, res)
        _save_state(state)
        lines.append(_summarise(res, time.perf_counter() - t0))
    lines.append(f"\n**TOTAL WALL** {time.perf_counter() - t_all:.0f}s")
    return "\n\n".join(lines), str(OUT_JSON)


def _summarise(res: dict, wall: float) -> str:
    name = res["name"]
    head = (f"### {name}  (n={res['n']}, d_in={res['in_dim']}, "
            f"pi={res['pi']:.3f}, eps_WL={res['eps_WL']:.4f})  "
            f"wall {wall:.0f}s")
    rows = []
    by_arch = {}
    for r in res["runs"]:
        by_arch.setdefault(r["arch"], []).append(r)
    import statistics as st
    for arch in ARCH_ORDER:
        rs = by_arch.get(arch, [])
        if not rs:
            continue
        Rhat = [r["Rhat"] for r in rs]
        # last k in sweep is the largest k (closest to k_WL)
        kref = [r["k_sweep"][-1] for r in rs]
        eps = [k["eps_trained"] for k in kref]
        fg = [k["feature_gap_at_k"] for k in kref]
        def ms(xs):
            return (st.mean(xs), st.stdev(xs) if len(xs) > 1 else 0.0)
        rh = ms(Rhat); ep = ms(eps); fgv = ms(fg)
        rows.append(
            f"| {arch} | {rh[0]:.3f}\u00b1{rh[1]:.3f} | "
            f"{ep[0]:.3f}\u00b1{ep[1]:.3f} | "
            f"{fgv[0]:+.3f}\u00b1{fgv[1]:.3f} |")
    tbl = ("| arch | R\u0302 | eps_tr(largest_k) | feat_gap |\n"
           "|---|---|---|---|\n" + "\n".join(rows))
    return head + "\n\n" + tbl


with gr.Blocks(title="D-Full: Partition-Bracket GNN Audit") as demo:
    gr.Markdown(
        "# D-Full: Post-hoc architecture-vs-WL bracket audit\n"
        "**5 datasets x 4 archs x 5 seeds = 100 cells.** "
        "Each dataset runs in a single ZeroGPU H200 call "
        "(`duration=300s`). Results stream to "
        "`results/e3d_arch_full.json`. See the partition-sandwich "
        "paper for the bracket framework; see `e3d_arch_full.py` for "
        "the core training + measurement code."
    )
    with gr.Row():
        n_seeds = gr.Slider(1, 5, value=5, step=1, label="seeds (0..n-1)")
        epochs = gr.Slider(50, 400, value=200, step=50, label="epochs")
        hidden = gr.Slider(32, 256, value=128, step=32, label="hidden")
    with gr.Row():
        for ds in DATASET_ORDER:
            btn = gr.Button(f"Run {ds}")
            btn.click(
                fn=lambda n_s, ep, hi, _ds=ds:
                    run_dataset_ui(_ds, n_s, ep, hi),
                inputs=[n_seeds, epochs, hidden],
                outputs=[gr.Markdown(), gr.File()])
    run_all_btn = gr.Button("Run ALL datasets sequentially",
                            variant="primary")
    out_md = gr.Markdown()
    out_file = gr.File(label="results/e3d_arch_full.json")
    run_all_btn.click(fn=run_all_ui,
                      inputs=[n_seeds, epochs, hidden],
                      outputs=[out_md, out_file])

    gr.Markdown(
        f"\n---\n"
        f"ZeroGPU available in runtime: **{HAVE_ZGPU}** | "
        f"results path: `{OUT_JSON}`"
    )


if __name__ == "__main__":
    demo.queue().launch()
