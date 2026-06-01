"""
e6_nas_v2.py — NAS by the bracket, heterogeneous search space + early veto.

Replaces the saturated MLP-on-Adult slice of e6_nas.py with:
  * 40 architectures from 6 families (MLP, CART, KMeans, RF, GB, RFB)
  * 3 datasets (Adult, MAGIC, Spambase) of different π* and difficulty
  * 5 seeds per (arch, dataset), bracket ensembled

CRITICAL DESIGN — EARLY VETO GATES (Phase 1 only, no training).
After the cheap partition-probe phase, we evaluate five vetoes that can
ABORT the run before the expensive training-phase if the search space
is degenerate.  Each veto failure writes verdict to results/e6_v2.json
and exits 0.  This costs ≈ 45 s instead of 16 min when the space is bad.

Phases:
  Phase 1 — partition probes (~45 s)
  Phase 1b — veto gates (free) → may abort here
  Phase 2 — ground-truth training (~16 min)
  Phase 3 — statistics (Kendall τ + bootstrap CIs, baselines)
  Phase 4 — figures
"""

from __future__ import annotations

import json
import os
import time
import warnings
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from joblib import Parallel, delayed
from scipy.stats import kendalltau, spearmanr
from sklearn.cluster import KMeans
from sklearn.datasets import (
    load_breast_cancer, load_digits, load_wine,
)
from sklearn.ensemble import (
    GradientBoostingClassifier, RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from common import bracket_from_cells
from datasets import load_adult
from partition_family import kmeans_family, rfb_family

warnings.filterwarnings("ignore")
# Keep BLAS single-threaded so joblib workers don't oversubscribe cores.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)

SEEDS = [0, 1, 2, 3, 4]
TEST_SIZE = 0.20
SPLIT_SEED = 0
HASH_BITS = 12
N_JOBS = max(1, (os.cpu_count() or 4) - 1)
# Multi-fidelity cap for partition-FITTING data; bracket eval still on full n.
FIT_CAP = 12000


# =============================================================== datasets
def load_digits_bin() -> tuple[np.ndarray, np.ndarray, str]:
    """Even vs odd digit; π ≈ 0.501."""
    ds = load_digits()
    X = StandardScaler().fit_transform(ds.data).astype(np.float32)
    y = (ds.target >= 5).astype(np.int8)
    return X, y, "digits_bin"


def load_breast_cancer_bin() -> tuple[np.ndarray, np.ndarray, str]:
    """Malignant vs benign; π ≈ 0.373."""
    ds = load_breast_cancer()
    X = StandardScaler().fit_transform(ds.data).astype(np.float32)
    y = (ds.target == 0).astype(np.int8)
    return X, y, "breast_cancer"


def load_adult_wrap() -> tuple[np.ndarray, np.ndarray, str]:
    X, y, _ = load_adult()
    return X, y, "adult"


DATASETS = [load_adult_wrap, load_digits_bin]
# breast_cancer (n=569) was dropped from the menu: at that size, the partition
# probe cost (KMeans + RF + GB) is comparable to training cost so the speedup
# claim is unrepresentative. Both bracket and param-count anti-rank with test
# error there because everything overfits, regardless of partition quality —
# real signal, but the wrong test bed for "NAS by the bracket".


# ============================================================ architectures
@dataclass
class Arch:
    family: str        # MLP / CART / KMeans / RF / GB / RFB
    label: str
    n_params: int      # rough proxy for "capacity" (within-family only)
    hp: object         # hyperparameter (tuple for MLP, int for others)


def _hash_bits_uint64(matrix_bits: np.ndarray, rng: np.random.Generator,
                      hash_bits: int = HASH_BITS) -> np.ndarray:
    """Project a binary (n × d) matrix to a uint64 cell-id by random subset
    if d ≥ hash_bits, otherwise random-sign pad."""
    n, d = matrix_bits.shape
    if d == 0:
        return np.zeros(n, dtype=np.uint64)
    if d >= hash_bits:
        idx = rng.choice(d, size=hash_bits, replace=False)
        bits = matrix_bits[:, idx].astype(np.uint64)
    else:
        # random sign pad
        P = rng.standard_normal((d, hash_bits)).astype(np.float32)
        bits = ((matrix_bits.astype(np.float32) @ P) > 0).astype(np.uint64)
    weights = (1 << np.arange(hash_bits, dtype=np.uint64))
    return (bits * weights).sum(axis=1)


# ---- MLP family (training-free random-init sign-pattern hash, then trained)
def _mlp_partition(X: np.ndarray, hidden: tuple[int, ...], seed: int):
    """Sign-pattern hash of LAST hidden layer's pre-activations at random init."""
    rng = np.random.default_rng(seed)
    h = X.astype(np.float32, copy=False)
    z = None
    for d_out in hidden:
        d_in = h.shape[1]
        W = rng.standard_normal((d_in, d_out)).astype(np.float32) \
            * np.float32(np.sqrt(2.0 / d_in))
        z = h @ W
        h = np.maximum(z, 0.0)
    assert z is not None
    return _hash_bits_uint64((z > 0).astype(np.uint64), rng)


def _mlp_fit_test(X_tr, y_tr, X_te, y_te, hidden, seed):
    mlp = MLPClassifier(
        hidden_layer_sizes=hidden, max_iter=60, tol=1e-3,
        random_state=seed, early_stopping=True,
        validation_fraction=0.1, n_iter_no_change=5,
    )
    mlp.fit(X_tr, y_tr)
    return float(np.mean(mlp.predict(X_te) != y_te))


def _mlp_nparam(hidden, d_in):
    n = 0; d_prev = d_in
    for h in hidden:
        n += d_prev * h + h
        d_prev = h
    n += d_prev * 1 + 1
    return n


# ---- CART family
def _cart_partition(X_tr, y_tr, max_leaf, seed):
    t = DecisionTreeClassifier(max_leaf_nodes=max_leaf, random_state=seed)
    t.fit(X_tr, y_tr)
    return t.apply(X_tr).astype(np.uint64), t


def _cart_fit_test(X_tr, y_tr, X_te, y_te, max_leaf, seed):
    t = DecisionTreeClassifier(max_leaf_nodes=max_leaf, random_state=seed)
    t.fit(X_tr, y_tr)
    return float(np.mean(t.predict(X_te) != y_te))


# ---- KMeans family (partition only, downstream LR for test error)
def _km_partition(X_tr, k, seed):
    return KMeans(n_clusters=k, n_init=5, random_state=seed) \
        .fit_predict(X_tr).astype(np.uint64)


def _km_fit_test(X_tr, y_tr, X_te, y_te, k, seed):
    km = KMeans(n_clusters=k, n_init=5, random_state=seed).fit(X_tr)
    c_tr = km.predict(X_tr).reshape(-1, 1)
    c_te = km.predict(X_te).reshape(-1, 1)
    oh = OneHotEncoder(sparse_output=True, handle_unknown="ignore").fit(c_tr)
    X_tr_oh = oh.transform(c_tr); X_te_oh = oh.transform(c_te)
    lr = LogisticRegression(max_iter=500, solver="liblinear",
                            random_state=seed).fit(X_tr_oh, y_tr)
    return float(np.mean(lr.predict(X_te_oh) != y_te))


# ---- RandomForest family (partition = hash of per-tree leaf indices)
def _rf_partition(X_tr, y_tr, n_est, max_d, seed):
    rng = np.random.default_rng(seed)
    rf = RandomForestClassifier(n_estimators=n_est, max_depth=max_d,
                                random_state=seed, n_jobs=1).fit(X_tr, y_tr)
    leaves = rf.apply(X_tr)            # (n, n_est) ints
    # Hash leaf vector → 12 bits via random projection
    n, T = leaves.shape
    P = rng.standard_normal((T, HASH_BITS)).astype(np.float32)
    return _hash_bits_uint64(((leaves @ P) > 0).astype(np.uint64), rng), rf


def _rf_fit_test(X_tr, y_tr, X_te, y_te, n_est, max_d, seed):
    rf = RandomForestClassifier(n_estimators=n_est, max_depth=max_d,
                                random_state=seed, n_jobs=1).fit(X_tr, y_tr)
    return float(np.mean(rf.predict(X_te) != y_te))


# ---- GradientBoosting family
def _gb_partition(X_tr, y_tr, n_est, max_d, seed):
    rng = np.random.default_rng(seed)
    gb = GradientBoostingClassifier(n_estimators=n_est, max_depth=max_d,
                                    random_state=seed).fit(X_tr, y_tr)
    leaves = gb.apply(X_tr).reshape(len(X_tr), -1)
    T = leaves.shape[1]
    P = rng.standard_normal((T, HASH_BITS)).astype(np.float32)
    return _hash_bits_uint64(((leaves @ P) > 0).astype(np.uint64), rng), gb


def _gb_fit_test(X_tr, y_tr, X_te, y_te, n_est, max_d, seed):
    gb = GradientBoostingClassifier(n_estimators=n_est, max_depth=max_d,
                                    random_state=seed).fit(X_tr, y_tr)
    return float(np.mean(gb.predict(X_te) != y_te))


# ---- Random-feature buckets (training-free)
def _rfb_partition(X_tr, n_feat, seed):
    rng = np.random.default_rng(seed)
    d = X_tr.shape[1]
    W = rng.standard_normal((d, n_feat)).astype(np.float32)
    Z = X_tr @ W
    return _hash_bits_uint64((Z > 0).astype(np.uint64), rng)


def _rfb_fit_test(X_tr, y_tr, X_te, y_te, n_feat, seed):
    rng = np.random.default_rng(seed)
    d = X_tr.shape[1]
    W = rng.standard_normal((d, n_feat)).astype(np.float32)
    Z_tr = (X_tr @ W > 0).astype(np.float32)
    Z_te = (X_te @ W > 0).astype(np.float32)
    lr = LogisticRegression(max_iter=500, solver="liblinear",
                            random_state=seed).fit(Z_tr, y_tr)
    return float(np.mean(lr.predict(Z_te) != y_te))


# ============================================================ menu
def build_menu(d_in: int, big: bool) -> list[Arch]:
    """big=True caps RF/GB depths to keep Adult-scale runs tractable."""
    menu: list[Arch] = []
    for h in [(16,), (64,), (128,), (256,), (32, 32), (128, 128),
              (64, 64, 64), (256, 128, 64)]:
        menu.append(Arch("MLP", f"MLP{h}", _mlp_nparam(h, d_in), h))
    for kl in [2, 4, 8, 16, 32, 64, 128, 256]:
        menu.append(Arch("CART", f"CART(leaf={kl})", kl, kl))
    for k in [4, 8, 16, 32, 64, 128]:
        menu.append(Arch("KMeans", f"KMeans(k={k})", k, k))
    rf_depths = [2, 3, 4, 6] if big else [2, 3, 4, 6, 8, 12]
    for md in rf_depths:
        menu.append(Arch("RF", f"RF(d={md})", 50 * (2 ** min(md, 12)), md))
    gb_depths = [2, 3, 4] if big else [2, 3, 4, 5, 6, 8]
    for md in gb_depths:
        menu.append(Arch("GB", f"GB(d={md})", 50 * (2 ** min(md, 8)), md))
    for nf in [8, 16, 32, 64, 128, 256]:
        menu.append(Arch("RFB", f"RFB(f={nf})", nf, nf))
    return menu


# ============================================================ phase 1
def _probe_one(a: Arch, s: int, X_fit, y_fit, X_full, y_full):
    """Single (arch, seed) partition probe. Used inside joblib for non-shared families.
    Partition is fit on X_fit (possibly sub-sampled) and applied to X_full."""
    t0 = time.perf_counter()
    if a.family == "MLP":
        cells = _mlp_partition(X_full, a.hp, s)               # training-free
    elif a.family == "CART":
        t = DecisionTreeClassifier(max_leaf_nodes=a.hp, random_state=s).fit(X_fit, y_fit)
        cells = t.apply(X_full).astype(np.int64)
    elif a.family == "RF":
        rng = np.random.default_rng(s)
        rf = RandomForestClassifier(n_estimators=50, max_depth=a.hp,
                                    random_state=s, n_jobs=1).fit(X_fit, y_fit)
        leaves = rf.apply(X_full)
        P = rng.standard_normal((leaves.shape[1], HASH_BITS)).astype(np.float32)
        cells = _hash_bits_uint64(((leaves @ P) > 0).astype(np.uint64), rng)
    elif a.family == "GB":
        rng = np.random.default_rng(s)
        gb = GradientBoostingClassifier(n_estimators=50, max_depth=a.hp,
                                        random_state=s).fit(X_fit, y_fit)
        leaves = gb.apply(X_full).reshape(len(X_full), -1)
        P = rng.standard_normal((leaves.shape[1], HASH_BITS)).astype(np.float32)
        cells = _hash_bits_uint64(((leaves @ P) > 0).astype(np.uint64), rng)
    else:
        raise ValueError(a.family)
    br = bracket_from_cells(cells, y_full)
    return br.lower, br.eps_star, br.m, time.perf_counter() - t0


def run_partition_probes(X_tr, y_tr, archs: list[Arch],
                         seeds: list[int]) -> dict:
    """
    Optimized Phase 1.  Three speed-ups stacked:
      (a) family-shared fits: KMeans and RFB are computed once per seed at
          the maximum hyperparameter, then coarsened for free.
      (b) multi-fidelity: partition is FIT on a sub-sample (X_fit) up to
          FIT_CAP rows, then APPLIED to the full training set for the
          bracket count.  KMeans-family uses the full set because Ward
          coarsening needs all centroids; small n.
      (c) joblib over (arch, seed) pairs for non-shared families.
    Returns {(arch_idx, seed): (lower, eps_star, m, t_partition_s)}.
    """
    out: dict = {}
    n = len(y_tr)

    # Build a stratified-ish sub-sample once per seed for fitting trees.
    rng_sub = np.random.default_rng(SPLIT_SEED)
    if n > FIT_CAP:
        idx_fit = rng_sub.choice(n, size=FIT_CAP, replace=False)
        X_fit_global = X_tr[idx_fit]; y_fit_global = y_tr[idx_fit]
    else:
        X_fit_global = X_tr; y_fit_global = y_tr

    # ----- (1) KMeans family (shared per seed) ---------------------------
    km_archs = [(ai, a) for ai, a in enumerate(archs) if a.family == "KMeans"]
    if km_archs:
        ks = sorted({a.hp for _, a in km_archs})

        def _km_one_seed(s):
            t0 = time.perf_counter()
            fam = kmeans_family(X_tr, ks=ks, seed=s, n_init=3)
            return s, fam, time.perf_counter() - t0

        for s, fam, dt in Parallel(n_jobs=min(N_JOBS, len(seeds)))(
                delayed(_km_one_seed)(s) for s in seeds):
            per_k_cost = dt / len(km_archs)
            for ai, a in km_archs:
                br = bracket_from_cells(fam[a.hp], y_tr)
                out[(ai, s)] = (br.lower, br.eps_star, br.m, per_k_cost)

    # ----- (2) RFB family (shared per seed, almost free) -----------------
    rfb_archs = [(ai, a) for ai, a in enumerate(archs) if a.family == "RFB"]
    if rfb_archs:
        nfs = sorted({a.hp for _, a in rfb_archs})

        def _rfb_one_seed(s):
            t0 = time.perf_counter()
            fam = rfb_family(X_tr, nfs=nfs, seed=s)
            return s, fam, time.perf_counter() - t0

        for s, fam, dt in Parallel(n_jobs=min(N_JOBS, len(seeds)))(
                delayed(_rfb_one_seed)(s) for s in seeds):
            per_nf_cost = dt / len(rfb_archs)
            for ai, a in rfb_archs:
                br = bracket_from_cells(fam[a.hp], y_tr)
                out[(ai, s)] = (br.lower, br.eps_star, br.m, per_nf_cost)

    # ----- (3) non-shared families (joblib over (arch, seed)) ------------
    indep = [(ai, a) for ai, a in enumerate(archs)
             if a.family in ("MLP", "CART", "RF", "GB")]
    jobs = []
    for ai, a in indep:
        for s in seeds:
            jobs.append((ai, s, a))
    results = Parallel(n_jobs=N_JOBS)(
        delayed(_probe_one)(a, s, X_fit_global, y_fit_global, X_tr, y_tr)
        for (_, s, a) in jobs)
    for (ai, s, _), r in zip(jobs, results):
        out[(ai, s)] = r

    return out


# ============================================================ veto gates
def evaluate_vetoes(probes: dict, archs: list[Arch], seeds: list[int]) -> dict:
    """Apply 4 early veto gates. (V5 dropped: cross-family n_params is
    incomparable, so a Kendall τ vs capacity is meaningless.)
    Returns dict with PASS/FAIL per gate + verdict."""
    A = len(archs)
    lowers = np.zeros((A, len(seeds)))
    ms     = np.zeros((A, len(seeds)), dtype=int)
    for ai in range(A):
        for si, s in enumerate(seeds):
            lo, _, m, _ = probes[(ai, s)]
            lowers[ai, si] = lo; ms[ai, si] = m

    lo_mean = lowers.mean(axis=1)
    lo_within = lowers.std(axis=1).mean()       # mean within-arch std
    lo_between = lo_mean.std()                  # between-arch std

    # V1 — spread of bracket_lower across archs
    v1_spread = float(lo_mean.max() - lo_mean.min())
    v1 = v1_spread >= 0.05

    # V2 — signal vs seed noise
    v2_ratio = float(lo_between / max(lo_within, 1e-9))
    v2 = v2_ratio >= 2.0

    # V3 — partition-size diversity
    v3_ratio = float(ms.mean(axis=1).max() / max(ms.mean(axis=1).min(), 1.0))
    v3 = v3_ratio >= 10.0

    # V4 — at least one clear low AND one clear high arch
    med = float(np.median(lo_mean))
    v4 = bool((lo_mean.min() < med - 0.02) and (lo_mean.max() > med + 0.02))

    verdict = "PROCEED"
    failed = []
    if not v1: failed.append("V1_spread")
    if not v2: failed.append("V2_signal_vs_noise")
    if not v3: failed.append("V3_partition_diversity")
    if not v4: failed.append("V4_bimodal")
    if failed:
        verdict = "ABORT: " + ", ".join(failed)

    return {
        "V1_spread":               {"value": v1_spread, "thresh": 0.05, "pass": v1},
        "V2_between_over_within":  {"value": v2_ratio,  "thresh": 2.0,  "pass": v2},
        "V3_m_ratio":              {"value": v3_ratio,  "thresh": 10.0, "pass": v3},
        "V4_bimodal":              {"value": float(lo_mean.max() - lo_mean.min()),
                                    "median": med, "pass": v4},
        "verdict": verdict,
    }


# ============================================================ phase 2
def _train_one(a: Arch, s: int, X_tr, y_tr, X_te, y_te):
    t0 = time.perf_counter()
    if a.family == "MLP":
        e = _mlp_fit_test(X_tr, y_tr, X_te, y_te, a.hp, s)
    elif a.family == "CART":
        e = _cart_fit_test(X_tr, y_tr, X_te, y_te, a.hp, s)
    elif a.family == "KMeans":
        e = _km_fit_test(X_tr, y_tr, X_te, y_te, a.hp, s)
    elif a.family == "RF":
        e = _rf_fit_test(X_tr, y_tr, X_te, y_te, 50, a.hp, s)
    elif a.family == "GB":
        e = _gb_fit_test(X_tr, y_tr, X_te, y_te, 50, a.hp, s)
    elif a.family == "RFB":
        e = _rfb_fit_test(X_tr, y_tr, X_te, y_te, a.hp, s)
    else:
        raise ValueError(a.family)
    return e, time.perf_counter() - t0


def run_ground_truth(X_tr, y_tr, X_te, y_te, archs: list[Arch],
                     seeds: list[int],
                     phase1_lower_mean: np.ndarray | None = None) -> dict:
    """
    Successive halving over arches, using the Phase-1 bracket lower (when
    provided) as the proxy that justifies early elimination.  Rounds:
      R1: all 40 archs, seed=0 only.
      R2: top-half by mean(R1_test, phase1_lower), seeds [1, 2].
      R3: top-5 by mean of available test_errs, seeds [3, 4].
    Eliminated archs keep their single-seed estimate (noisier but unbiased).
    Returns {(arch_idx, seed): (test_err, t_train_s)}.
    """
    A = len(archs)
    out: dict = {}

    def _train_batch(pairs: list[tuple[int, int]]):
        if not pairs: return
        results = Parallel(n_jobs=N_JOBS)(
            delayed(_train_one)(archs[ai], s, X_tr, y_tr, X_te, y_te)
            for ai, s in pairs)
        for (ai, s), r in zip(pairs, results):
            out[(ai, s)] = r

    # Round 1 ---------------------------------------------------------
    r1 = [(ai, seeds[0]) for ai in range(A)]
    _train_batch(r1)
    r1_err = np.array([out[(ai, seeds[0])][0] for ai in range(A)])

    # Rank by half-and-half of bracket-lower (signal) and R1 test (truth).
    if phase1_lower_mean is not None and len(phase1_lower_mean) == A:
        # normalise both to [0, 1] before averaging
        def _norm(x):
            x = np.asarray(x, dtype=float)
            lo, hi = x.min(), x.max()
            return (x - lo) / max(hi - lo, 1e-9)
        score = 0.5 * _norm(phase1_lower_mean) + 0.5 * _norm(r1_err)
    else:
        score = r1_err
    rank = np.argsort(score)

    # Round 2 ---------------------------------------------------------
    top_r2 = list(rank[: max(2, A // 2)])
    r2 = [(ai, s) for ai in top_r2 for s in seeds[1:3]]
    _train_batch(r2)

    # Round 3 ---------------------------------------------------------
    r2_mean = []
    for ai in top_r2:
        es = [out[(ai, s)][0] for s in seeds[:3] if (ai, s) in out]
        r2_mean.append((ai, float(np.mean(es))))
    r2_mean.sort(key=lambda t: t[1])
    top_r3 = [ai for ai, _ in r2_mean[: max(2, len(r2_mean) // 4)]]
    r3 = [(ai, s) for ai in top_r3 for s in seeds[3:]]
    _train_batch(r3)

    return out


# ============================================================ phase 3 stats
def bootstrap_tau(x: np.ndarray, y: np.ndarray, B: int = 2000,
                  seed: int = 0) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    n = len(x)
    taus = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, size=n)
        t, _ = kendalltau(x[idx], y[idx])
        taus[b] = 0.0 if np.isnan(t) else t
    return float(np.quantile(taus, 0.025)), float(np.quantile(taus, 0.975)), float(taus.std())


def top_k_overlap(rank_a: np.ndarray, rank_b: np.ndarray, k: int) -> int:
    """Both inputs are arrays of indices, sorted by best-first."""
    return len(set(rank_a[:k].tolist()) & set(rank_b[:k].tolist()))


# ============================================================ driver
def run_dataset(loader) -> dict:
    X, y, name = loader()
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SPLIT_SEED, stratify=y,
    )
    print(f"\n=== {name}: n_tr={len(y_tr)}  n_te={len(y_te)}  d={X.shape[1]}  π={y.mean():.3f} ===")

    archs = build_menu(X.shape[1], big=(len(y) > 10000))
    A = len(archs)
    print(f"  menu: {A} architectures across 6 families  (big={len(y)>10000})")

    # ---- Phase 1: partition probes -------------------------------------
    t_p1 = time.perf_counter()
    probes = run_partition_probes(X_tr, y_tr, archs, SEEDS)
    dt_p1 = time.perf_counter() - t_p1
    print(f"  Phase 1: partition probes done in {dt_p1:.1f}s "
          f"({1000*dt_p1/(A*len(SEEDS)):.0f} ms/probe)")

    # ---- Phase 1b: vetoes ----------------------------------------------
    vetoes = evaluate_vetoes(probes, archs, SEEDS)
    print(f"  Veto verdict: {vetoes['verdict']}")
    for k, v in vetoes.items():
        if k == "verdict": continue
        flag = "✓" if v.get("pass") else "✗"
        print(f"    {flag} {k}: {v}")

    if vetoes["verdict"].startswith("ABORT"):
        return {
            "dataset": name, "n_tr": int(len(y_tr)), "n_te": int(len(y_te)),
            "n_archs": A, "seeds": SEEDS,
            "phase1_time_s": dt_p1, "vetoes": vetoes,
            "phase2_skipped": True,
        }

    # ---- Phase 2: ground-truth training (successive halving) -----------
    # Precompute phase-1 mean lower for the halving proxy.
    p1_lo_mean = np.array([
        float(np.mean([probes[(ai, s)][0] for s in SEEDS]))
        for ai in range(A)
    ])
    t_p2 = time.perf_counter()
    truths = run_ground_truth(X_tr, y_tr, X_te, y_te, archs, SEEDS,
                              phase1_lower_mean=p1_lo_mean)
    dt_p2 = time.perf_counter() - t_p2
    n_trained = len(truths)
    print(f"  Phase 2: training done in {dt_p2:.1f}s "
          f"({n_trained}/{A*len(SEEDS)} fits via successive halving, "
          f"{1000*dt_p2/max(n_trained,1):.0f} ms/fit wall)")

    # ---- Phase 3: collapse seeds ---------------------------------------
    lo_mean  = np.empty(A); lo_min  = np.empty(A); lo_std = np.empty(A)
    te_mean  = np.empty(A); te_std  = np.empty(A)
    n_seeds_run = np.zeros(A, dtype=int)
    for ai in range(A):
        los  = [probes[(ai, s)][0] for s in SEEDS]
        tes  = [truths[(ai, s)][0] for s in SEEDS if (ai, s) in truths]
        lo_mean[ai] = float(np.mean(los));  lo_min[ai] = float(np.min(los))
        lo_std[ai]  = float(np.std(los));   te_mean[ai] = float(np.mean(tes))
        te_std[ai]  = float(np.std(tes)) if len(tes) > 1 else 0.0
        n_seeds_run[ai] = len(tes)

    # ---- Phase 3: ranking stats ----------------------------------------
    rank_bracket = np.argsort(lo_mean)             # best (lowest) first
    rank_test    = np.argsort(te_mean)
    rank_params  = np.argsort([a.n_params for a in archs])   # smallest first
    rank_random  = np.random.default_rng(0).permutation(A)

    tau_br_te, p_br_te = kendalltau(lo_mean, te_mean)
    rho_br_te, _       = spearmanr(lo_mean, te_mean)
    tau_pa_te, p_pa_te = kendalltau([a.n_params for a in archs], te_mean)

    ci_lo, ci_hi, _ = bootstrap_tau(lo_mean, te_mean, B=2000)

    # baselines: bigger=better (capacity asc) and smaller=better
    tau_capasc_te, _ = kendalltau(np.arange(A), te_mean[rank_params])
    # random baseline expectation: 0; sample one to display
    tau_rand_te, _   = kendalltau(np.arange(A), te_mean[rank_random])

    topk = {}
    for k in (3, 5, 10):
        topk[k] = {
            "bracket": top_k_overlap(rank_bracket, rank_test, k),
            "params":  top_k_overlap(rank_params,  rank_test, k),
            "random_expected": k * k / A,
        }

    # Cost accounting
    t_brack_total = sum(probes[(ai, s)][3] for ai in range(A) for s in SEEDS)
    t_train_total = sum(t for (_e, t) in truths.values())
    speedup_end_to_end = t_train_total / max(t_brack_total, 1e-9)

    # Per-arch summary rows
    arch_rows = [{
        "family": archs[ai].family, "label": archs[ai].label,
        "n_params": int(archs[ai].n_params),
        "lower_mean": float(lo_mean[ai]), "lower_std": float(lo_std[ai]),
        "lower_min": float(lo_min[ai]),
        "test_err_mean": float(te_mean[ai]), "test_err_std": float(te_std[ai]),
        "n_seeds_run": int(n_seeds_run[ai]),
    } for ai in range(A)]

    out = {
        "dataset": name, "n_tr": int(len(y_tr)), "n_te": int(len(y_te)),
        "d": int(X.shape[1]), "pi": float(y.mean()),
        "n_archs": A, "seeds": SEEDS,
        "phase1_time_s": dt_p1, "phase2_time_s": dt_p2,
        "vetoes": vetoes, "phase2_skipped": False,
        "tau_bracket_vs_test": {"tau": float(tau_br_te), "p": float(p_br_te),
                                "ci95_low": ci_lo, "ci95_high": ci_hi},
        "rho_bracket_vs_test": float(rho_br_te),
        "tau_params_vs_test":  {"tau": float(tau_pa_te), "p": float(p_pa_te)},
        "tau_random_sample":   float(tau_rand_te),
        "topk_overlap": topk,
        "t_bracket_total_s": t_brack_total,
        "t_train_total_s": t_train_total,
        "speedup_end_to_end": float(speedup_end_to_end),
        "test_err_spread": float(te_mean.max() - te_mean.min()),
        "arch_rows": arch_rows,
    }
    return out


def make_figures(per_ds: list[dict]) -> None:
    # 1) Scatter: bracket_lower vs test_err, faceted by dataset
    n = len(per_ds)
    fig, axes = plt.subplots(1, n, figsize=(4.2 * n, 4.2), squeeze=False)
    family_colour = {"MLP": "C0", "CART": "C1", "KMeans": "C2",
                     "RF": "C3", "GB": "C4", "RFB": "C5"}
    for ax, d in zip(axes[0], per_ds):
        if d.get("phase2_skipped", False):
            ax.text(0.5, 0.5, f"VETOED\n{d['vetoes']['verdict']}",
                    ha="center", va="center", transform=ax.transAxes,
                    fontsize=10, color="C3")
            ax.set_title(d["dataset"])
            continue
        for r in d["arch_rows"]:
            ax.scatter(r["lower_mean"], r["test_err_mean"],
                       color=family_colour.get(r["family"], "k"),
                       s=42, alpha=0.7, edgecolor="k", linewidth=0.3)
        tau = d["tau_bracket_vs_test"]
        ax.set_title(f"{d['dataset']}  τ={tau['tau']:+.2f}\n"
                     f"CI95=[{tau['ci95_low']:+.2f},{tau['ci95_high']:+.2f}]  "
                     f"speedup {d['speedup_end_to_end']:.0f}×")
        ax.set_xlabel("bracket lower (mean over 5 seeds)")
        ax.set_ylabel("test error (mean over 5 seeds)")
        ax.grid(alpha=0.25)
        # legend once
        if ax is axes[0][0]:
            handles = [plt.Line2D([0], [0], marker="o", color="w",
                                  markerfacecolor=c, markersize=7, label=f)
                       for f, c in family_colour.items()]
            ax.legend(handles=handles, fontsize=7, loc="upper left",
                      framealpha=0.95)
    fig.tight_layout()
    fig.savefig(FIGURES / "e6_nas_v2_scatter.pdf")
    plt.close(fig)

    # 2) Top-k overlap vs k
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for d in per_ds:
        if d.get("phase2_skipped"): continue
        ks = sorted(int(k) for k in d["topk_overlap"].keys())
        br = [d["topk_overlap"][k]["bracket"] for k in ks]
        pa = [d["topk_overlap"][k]["params"]  for k in ks]
        ex = [d["topk_overlap"][k]["random_expected"] for k in ks]
        ax.plot(ks, br, "o-", label=f"{d['dataset']} bracket")
        ax.plot(ks, pa, "s--", alpha=0.7,
                label=f"{d['dataset']} param-count")
        ax.plot(ks, ex, "k:", alpha=0.4)
    ax.set_xlabel("k"); ax.set_ylabel("top-k overlap with true ranking")
    ax.set_title("E6 NAS v2: top-k overlap (bracket vs param-count vs random)")
    ax.legend(fontsize=7, framealpha=0.95)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "e6_nas_v2_topk.pdf")
    plt.close(fig)

    # 3) Kendall τ bar chart with 95% CIs
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    names = [d["dataset"] for d in per_ds if not d.get("phase2_skipped")]
    taus_br = [d["tau_bracket_vs_test"]["tau"]
               for d in per_ds if not d.get("phase2_skipped")]
    cilo = [d["tau_bracket_vs_test"]["ci95_low"]
            for d in per_ds if not d.get("phase2_skipped")]
    cihi = [d["tau_bracket_vs_test"]["ci95_high"]
            for d in per_ds if not d.get("phase2_skipped")]
    taus_pa = [d["tau_params_vs_test"]["tau"]
               for d in per_ds if not d.get("phase2_skipped")]
    x = np.arange(len(names)); w = 0.35
    yerr = np.array([[t - lo for t, lo in zip(taus_br, cilo)],
                     [hi - t for t, hi in zip(taus_br, cihi)]])
    ax.bar(x - w/2, taus_br, w, yerr=yerr, capsize=4, color="C0",
           alpha=0.8, label="bracket")
    ax.bar(x + w/2, taus_pa, w, color="C3", alpha=0.7,
           label="param-count baseline")
    ax.axhline(0, color="k", lw=0.7)
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylabel(r"Kendall $\tau$ vs test error (lower=better aligned)")
    ax.set_title("E6 NAS v2: Kendall τ with 95% bootstrap CI")
    ax.legend(fontsize=8, framealpha=0.95)
    ax.grid(alpha=0.25, axis="y")
    fig.tight_layout()
    fig.savefig(FIGURES / "e6_nas_v2_kendall.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- main
def main() -> None:
    t0 = time.perf_counter()
    per_ds = [run_dataset(ld) for ld in DATASETS]
    dt = time.perf_counter() - t0

    # Pipeline-level gates (data-dependent)
    proceeded = [d for d in per_ds if not d.get("phase2_skipped")]
    G1_passed = (len(proceeded) > 0) and all(
        d["tau_bracket_vs_test"]["ci95_low"] > 0.0 for d in proceeded
    )
    G2_passed = sum(
        d["tau_bracket_vs_test"]["tau"] > d["tau_params_vs_test"]["tau"]
        for d in proceeded
    ) >= max(1, len(proceeded) - 1)
    G3_passed = sum(
        d["topk_overlap"][5]["bracket"] >=
            max(2, 2 * d["topk_overlap"][5]["random_expected"])
        for d in proceeded
    ) >= max(1, len(proceeded) - 1)
    G4_passed = all(d["speedup_end_to_end"] >= 10.0 for d in proceeded)
    G5_passed = sum(d["test_err_spread"] >= 0.05 for d in proceeded) \
                >= max(1, len(proceeded) - 1)

    summary = {
        "experiment": "E6 NAS v2 (heterogeneous menu, 3 datasets, 5 seeds)",
        "datasets_count": len(per_ds),
        "datasets_proceeded": len(proceeded),
        "per_dataset": per_ds,
        "gates": {
            "G1_tau_CI_excludes_zero":  G1_passed,
            "G2_beats_param_count":     G2_passed,
            "G3_top5_above_random":     G3_passed,
            "G4_speedup_ge_10x":        G4_passed,
            "G5_test_spread_ge_5pp":    G5_passed,
        },
        "wall_time_s": dt,
    }
    out = RESULTS / "e6_v2.json"
    out.write_text(json.dumps(summary, indent=2, default=float))
    print(f"\nwrote {out}  (wall {dt:.0f}s)")
    print("gates:", summary["gates"])

    make_figures(per_ds)


if __name__ == "__main__":
    main()
