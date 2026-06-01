# Partition Brackets: A Framework with Entropy, Variance, and Noise-Robust Instances

**Status: SCAFFOLD (Phase 2a).** This KaTeX twin tracks
[`main.tex`](main.tex). All numbered statements are skeletons;
proofs deferred to Phase 2b. The twin will be filled in
lock-step during Phase 2d.

---

## Abstract

The companion paper [Paper A](../partition-sandwich-preprint/main.md)
proves an elementary two-sided closed-form bracket between the
partition-restricted Bayes risk $\varepsilon^{*}_{\Pi}$ of a
binary label $f$ under a partition $\Pi$ and its
partition-conditional Shannon entropy $H(f\mid\Pi)$. The present
paper argues that this bracket is one instance of a single
**recipe**: pick any concave **score functional** $\bar\varphi$
of a label distribution, take its partition-conditional
expectation, and read off a two-sided bracket on the
corresponding partition-restricted Bayes loss.

Three instances (Shannon entropy, conditional variance, Pinsker /
KL) plus three robustness extensions (label noise, soft / Markov
kernel partitions, refinement consistency) follow from a single
meta-theorem.

---

## Layout placeholder

- §1 Introduction
- §2 The $\bar\varphi$-bracket meta-theorem
- §3 Three named instances (Shannon, variance, Pinsker)
- §4 Robustness (noise, soft, refinement)
- §5 Aggregator-typed MPNN Lipschitz, $\bar\varphi$-version
- §6 Experiments E8 / E9 (zero new training)
- §7 Discussion

Full body to be mirrored from `main.tex` in Phase 2d.
