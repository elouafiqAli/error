"""
partition_family.py - share one expensive model fit across many partition labels.

The bracket is a monotone, additive functional of a (2 x m) contingency
table.  A *nested* family of partitions {Pi_k}_k (each Pi_{k+1} refining
Pi_k) can therefore reuse a single base fit:
    fit at finest k_max once  ->  coarsen for free.

Two families exploit this structure:
  * KMeans : fit k_max once; agglomerate centroids (Ward) for each k < k_max.
  * RFB    : random sign-pattern hash with k_max bits; smaller k is a
             literal prefix of the bits (zero cost).

CART, RF, GB and MLP are NOT shared (each hyperparameter setting needs its
own fit). CART pruning via ccp_alpha requires one fit per alpha in sklearn
public API, so the apparent saving is illusory.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans


# ---------------------------------------------------------------- KMeans family
def kmeans_family(X: np.ndarray, ks: Iterable[int], seed: int = 0,
                  n_init: int = 5) -> dict[int, np.ndarray]:
    """
    Fit one KMeans at k_max; coarsen centroids by Ward agglomeration to
    obtain nested partitions for each smaller k.

    For each k < k_max: cluster the k_max centroids into k Ward clusters
    -> centroid -> super-cluster mapping; relabel each sample by that map.
    """
    ks = sorted(set(int(k) for k in ks))
    k_max = max(ks)
    km = KMeans(n_clusters=k_max, n_init=n_init, random_state=seed).fit(X)
    base = km.predict(X).astype(np.int64)  # cell id in [0, k_max)

    out: dict[int, np.ndarray] = {k_max: base.copy()}
    for k in ks:
        if k == k_max:
            continue
        if k >= k_max:
            out[k] = base.copy()
            continue
        agg = AgglomerativeClustering(
            n_clusters=k, linkage="ward",
        ).fit(km.cluster_centers_)
        # centroid c -> super-cluster agg.labels_[c]
        mapping = agg.labels_.astype(np.int64)
        out[k] = mapping[base]
    return out


# ---------------------------------------------------------------- RFB family
HASH_BITS = 12  # matches e6_nas_v2 cap to keep partition sizes comparable


def rfb_family(X: np.ndarray, nfs: Iterable[int],
               seed: int = 0) -> dict[int, np.ndarray]:
    """
    Random feature buckets: project X with a single random matrix of size
    (d, max(nfs)); for each n_feat, hash the first n_feat sign bits down
    to HASH_BITS via a second random projection (matches non-shared variant).
    """
    nfs = sorted(set(int(n) for n in nfs))
    n_max = max(nfs)
    rng = np.random.default_rng(seed)
    d = X.shape[1]
    W = rng.standard_normal((d, n_max)).astype(np.float32)
    bits = (X @ W > 0).astype(np.float32)         # (n, n_max)
    weights = (1 << np.arange(HASH_BITS, dtype=np.uint64))
    out: dict[int, np.ndarray] = {}
    for nf in nfs:
        if nf >= HASH_BITS:
            # second random projection -> HASH_BITS sign bits (matches non-shared)
            P = rng.standard_normal((nf, HASH_BITS)).astype(np.float32)
            h = ((bits[:, :nf] @ P) > 0).astype(np.uint64)
        else:
            h = bits[:, :nf].astype(np.uint64)
        out[nf] = (h * weights[:h.shape[1]]).sum(axis=1)
    return out
