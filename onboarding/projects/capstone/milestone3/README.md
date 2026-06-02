# Capstone M3 — Train a GCN and audit against the bracket

> **Stub.** README only; starter and tests will be fleshed out after
> M2 is validated.
>
> **Goal.** Train a 2-layer GCN on Cora to ~80% accuracy; record its
> per-node predictions; audit them against M2's bracket using the
> label and 1-WL(L=2) partitions; produce the E3-style scatter plot.

**Points.** 25. **Tests.** 6 (planned).

## Planned deliverables

- `train.py` (≤ 80 LOC) producing a checkpoint and a
  `predictions.npy`.
- `audit.py` consuming the checkpoint and M2's bracket; produces
  `plots/m3_scatter.png` with the bracket interval and the
  realised error per partition.
- Distinguish: training accuracy vs Bayes error on a partition;
  which is the bracket bounding?

## Rubric (planned)

| Item | Correctness | Pedagogy | Calibration | Total |
|---|---|---|---|---|
| `train.py` reaches ≥ 75% test acc | 6 | 1 | 1 | 8 |
| `audit.py` produces scatter | 5 | 2 | 1 | 8 |
| GCN error sits inside the 1-WL(L=2) bracket | 4 | 2 | 1 | 7 |
| Distinguish entry in writeup | 0 | 1 | 1 | 2 |
| **Total** | **15** | **6** | **4** | **25** |
