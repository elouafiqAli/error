"""
merge_to_5of5.py
================

Final assembly: merge e3d_arch_full.4of5.json (cora+citeseer+pubmed+
twitch_en) with the ogbn-arxiv JSON produced by
runpod/e3d_arch_ogbn_kmeans.py into a 5-of-5 file matching the original
DATASET_ORDER from e3d_data_full.py:

    [cora, citeseer, pubmed, twitch_en, ogbn_arxiv]
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--four",
                   default="experiments/results/e3d_arch_full.4of5.json")
    p.add_argument("--ogbn", required=True,
                   help="JSON from runpod/e3d_arch_ogbn_kmeans.py "
                        "(typically e3d_arch_full.ogbn_only.json)")
    p.add_argument("--out",
                   default="experiments/results/e3d_arch_full.5of5.json")
    args = p.parse_args()

    d4_path = Path(args.four)
    do_path = Path(args.ogbn)
    out_path = Path(args.out)

    d4 = json.loads(d4_path.read_text())
    do = json.loads(do_path.read_text())

    # Sanity: configurations must match.
    for k in ("depth_L", "hidden", "epochs", "seeds", "archs"):
        if d4[k] != do[k]:
            print(f"[merge] WARNING: {k} mismatch  4of5={d4[k]!r}  "
                  f"ogbn={do[k]!r}", file=sys.stderr)

    ogbn_datasets = [d for d in do["datasets"] if d.get("name") == "ogbn_arxiv"]
    if not ogbn_datasets:
        print(f"[merge] ERROR: no ogbn_arxiv entry in {do_path}",
              file=sys.stderr)
        return 2

    d5 = copy.deepcopy(d4)
    d5["datasets"] = d4["datasets"] + ogbn_datasets
    d5["datasets_order"] = ["cora", "citeseer", "pubmed",
                            "twitch_en", "ogbn_arxiv"]
    d5["total_wall_s"] = float(d4["total_wall_s"]) + float(do["total_wall_s"])

    prov = dict(d4.get("merge_provenance", {}))
    prov["sources"] = list(prov.get("sources", [])) + [str(do_path)]
    prov["merged_datasets"] = d5["datasets_order"]
    prov["coverage"] = "5_of_5"
    prov.pop("missing_dataset", None)
    prov["phase2_provenance"] = do.get("phase2_provenance")
    d5["merge_provenance"] = prov

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(d5, indent=2))
    print(f"[merge] wrote {out_path}  "
          f"({len(d5['datasets'])} datasets, total_wall_s={d5['total_wall_s']:.0f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
