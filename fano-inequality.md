## Generalizing the Fano Inequality

**Te Sun Han, Fellow, IEEE, and Sergio Verdú, Fellow, IEEE**

### Abstract

The Fano inequality gives a lower bound on the mutual information between two random variables that take values on an M-element set, provided at least one of the random variables is equiprobable. We show several simple lower bounds on mutual information which do not assume such a restriction. In particular, this can be accomplished by replacing $\log M$ with the infinite-order Rényi entropy in the Fano inequality. Applications to hypothesis testing are exhibited along with bounds on mutual information in terms of the a priori and a posteriori error probabilities.

**Index Terms:** Shannon theory, Fano inequality, mutual information, hypothesis testing.

I. THE FANO INEQUALITY

One of the most useful results in the Shannon theory is the following lower bound on mutual information, which, in the last forty years, has proven to be the key tool in the proof of converse results in information theory.

**Theorem 1:** Suppose that $X$ and $Y$ are random variables that satisfy the following.

- a) $X$ and $Y$ take values on the same finite set with cardinality $M$.
    
- b) either $X$ or $Y$ is equiprobable.
    

Then, the mutual information between $X$ and $Y$ satisfies:

$$I(X;Y)\ge P[X=Y]\log M-h(P[X=Y])$$

where $h$ is the binary entropy function, i.e., the continuous extension on [0, 1] of $h(x)=x\log\frac{1}{x}+(1-x)\log\frac{1}{1-x}$.

_Proof:_ If $X$ is equiprobable, then $H(X)=\log M$ and $I(X;Y)=\log M-H(X|Y)$, which is then lower bounded, using the Fano inequality [1]: $H(X|Y)\le P[X\ne Y]\log(M-1)+h(P[X=Y])$. If $Y$ (instead of $X$) is equiprobable, then the bound must still be true because of the symmetry of both sides of the inequality.

The power of Theorem 1 stems from its ability to lower bound the mutual information between two random variables in terms of a single quantity easily computable from their joint distribution: the probability that the random variables take the same value. The purpose of Section II is to generalize Theorem 1 so that mutual-information lower bounds can be given without the assumptions therein, i.e., that the random variables are finitely valued, and more important, that at least one of them is equiprobable. As a bonus, the proofs of the new bounds of Section II are particularly simple and intuitive. Since it is possible to construct independent (nonequiprobable) random variables $(X, Y)$ for any arbitrarily specified $P[X=Y]$, it is apparent that dropping the assumptions of Theorem 1 will require a lower bound that depends on the distribution of $X$ and $Y$ not only through $P[X=Y]$, but through some other, hopefully simple, quantity.

Several of the mutual-information lower bounds found in Section II involve the Rényi entropy, which is defined as:

$$R_{\alpha}(X)=\frac{1}{1-\alpha}\log\sum_{\omega\in\Omega}P_{X}^{\alpha}(\omega)$$

for $\alpha>0$ and $\alpha\ne1$. $R_{\alpha}(X)$ is monotone decreasing in $\alpha$. $R_{0}(X)$ is equal to the log of the number of nonzero atoms, and the infinite-order Rényi entropy is equal to $R_{\infty}(X)=\log\frac{1}{\max_{\omega\in\Omega}P_{X}(\omega)}$.

It is shown in Section II that one way to generalize Theorem 1 is to replace the zero-order Rényi entropy ($\log M$) that appears in the standard formulation by the infinite-order Rényi entropy $R_{\infty}(X)$ (or $R_{\infty}(Y)$). Then, the resulting general bound reduces to the standard formulation when the assumptions of Theorem 1 are satisfied. This new bound finds applications in the proof of a generalized source-channel separation theorem in a nonstandard setting [3]. Other applications of the mutual-information lower bounds of Section II are illustrated in Section III, where their relationship with minimum error probability in hypothesis testing is explored.

### II.

NEW MUTUAL-INFORMATION LOWER BOUNDS

First, we observe a simple inequality between information divergences.

**Theorem 2:** Suppose that the random variables $X, Y, \overline{X}, \overline{Y}$ satisfy the following: b) $\overline{X}$ and $\overline{Y}$ are independent. Then,

$$I(X;Y)\ge d(P[X=Y]||P[\overline{X}=\overline{Y}])-D(P_{X}||P_{\overline{X}})-D(P_{Y}||P_{\overline{Y}})$$

where $P_{X}$ denotes the distribution of the random variable $X$, $D(P||Q)$ denotes the information divergence, and the binary divergence function $d(x||y)$ is defined as the continuous extension on [0, 1] of $d(x||y)=x\log\frac{x}{y}+(1-x)\log\frac{1-x}{1-y}$. This is equivalent to $d(x||y)=D([x,1-x]||[y,1-y])$.

_Proof:_ Under the assumption that $\overline{X}$ and $\overline{Y}$ are independent, $D(P_{XY}||P_{\overline{X}\overline{Y}})=D(P_{XY}||P_{\overline{X}}P_{\overline{Y}})=I(X;Y)+D(P_{X}||P_{\overline{X}})+D(P_{Y}||P_{\overline{Y}})$. Now, the inequality follows by applying the data processing theorem for divergence ("processing reduces divergence") to a processor whose input is $(x,y)$ and whose output is $1\{x=y\}$ under the different input distributions $P_{XY}$ and $P_{\overline{X}\overline{Y}}$.

Various useful lower bounds can be derived from Theorem 2 depending on the choice of the auxiliary random variables $\overline{X}$ and $\overline{Y}$. We will consider three different choices:

- 1) $\overline{X}$ is a finite set with cardinality $M$, $\overline{X}$ is equiprobable, and $P_{\overline{Y}}=P_{Y}$. It is easy to check that with this choice, the inequality becomes the standard Fano inequality. This way of deriving the Fano inequality is due to Blahut [4].
    
- 2) $P_{\overline{X}}=P_{X}$ and $P_{\overline{Y}}=P_{X}$. Then, the theorem becomes the general mutual information lower bound $I(X; Y) \ge P[X = Y]R_{\infty}(X) - h(P[X=Y]) - D(P_{Y}||P_{X})$.
    
- 3) $P_{\overline{X}}=P_{X}$ and $P_{\overline{Y}}=P_{Y}$. This leads to the following result.
    

**Theorem 3:** If $X$ and $Y$ take values on the same set, then

$$I(X;Y)\ge d(P[X=Y]||P[\overline{X}=\overline{Y}])$$

where $\overline{X}$ and $\overline{Y}$ are independent, and have the same marginal distributions as $X$ and $Y$, respectively. Furthermore, equality holds if and only if for some constants $\alpha$ and $\beta$, $P_{XY}(x,y) = \alpha P_{X}(x)P_{Y}(y)$ for $x=y$, and $\beta P_{X}(x)P_{Y}(y)$ for $x\ne y$.

_Proof:_ The bound follows from Theorem 2 as noted. The necessary and sufficient condition for equality follows from the identity $D(P_{U}||Q_{U})=D(P_{V}||Q_{V})+D(P_{U|V}||Q_{U|V}|P_{V})$, applied to the case where $U=(X,Y)$, $V=1\{X=Y\}$, $P_{U}=P_{XY}$, and $Q_{U}=P_{X}P_{Y}$.

Regarding the lower bound, note that $P[\overline{X}=\overline{Y}]=\sum_{\omega\in\Omega}P_{X}(\omega)P_{Y}(\omega)$, i.e., the inner product between the marginals of $X$ and $Y$, which is often easy to obtain from the description of $X$ and $Y$. It can be checked that except in the trivial case where $X$ and $Y$ are independent, the equality condition implies that the marginals are either nonoverlapping or both equiprobable (on a subset of $\Omega$). We will now loosen the bound so that we can obtain bounds with the same structure as Theorem 1. We do so simply by lower bounding binary divergence.

**Theorem 4:** If $X$ and $Y$ take values on the same set, then

$$I(X;Y)\ge P[X=Y]\log\frac{1}{P[\overline{X}=\overline{Y}]}-h(P[X=Y])$$

_Proof:_ The desired inequality follows from Theorem 3 and the lower bound on binary divergence $d(x||y)\ge x\log\frac{1}{y}-h(x)$.

In some cases, the marginal distribution of $Y$ may not be immediately available, in which case it is convenient to replace $P[\overline{X}=\overline{Y}]$ by a quantity which is a function of the marginal distribution of $X$ only. This is done in the next result.

**Theorem 5:** If $X$ and $Y$ take values on the same set, then

$$I(X;Y)\ge P[X=Y]R_{\infty}(X)-h(P[X=Y])$$

where by symmetry we can replace $R_{\infty}(X)$ by $R_{\infty}(Y)$.

_Proof:_ The result follows from Theorem 4 and the fact that $P[\overline{X}=\overline{Y}]\le \min\{\max_{\omega\in\Omega}P_{X}(\omega),\max_{\omega\in\Omega}P_{Y}(\omega)\}$.

Note that Theorem 5 takes the same form as Theorem 1, replacing the zero-order Rényi entropy by the infinite-order Rényi entropy. If the conditions of Theorem 1 are satisfied, then both bounds are identical. However, Theorem 5 holds in full generality; neither $X$ nor $Y$ need be equiprobable or even finitely valued. The infinite-order Rényi entropy $R_{\infty}(X)$ is a measure of the randomness of $X$, which quantifies how hard it is to guess the value of $X$ knowing only its distribution. The probability of error with no information on $X$, $\epsilon_{X}$ (prior Bayes risk with a Hamming loss function), is the monotonic transformation $\epsilon_{X}=1-(\exp(-R_{\infty}(X)))$. The infinite-order Rényi entropy satisfies the properties $0\le R_{\infty}(X)\le H(X)$ and $R_{\infty}(X_{1},\cdots X_{n})=R_{\infty}(X_{1})+\cdots+R_{\infty}(X_{n})$ if $X_{1},\cdots X_{n}$ are independent. If $X$ is restricted to take $M$ values, then these bounds can be improved. The region of allowable $(R_{\infty}(X),H(X))$ pairs as a function of $M$ has been determined in [5]. If the cardinality of $X$ is not bounded, then the bounds cannot be improved.

It is now tempting to strengthen the lower bound in Theorem 4 with $I(X;Y)\ge P[X=Y]H(X)-h(P[X=Y])$. However, this bound does not hold in general. For example, if $X$ and $Y$ are independent with identical distribution, then the left side is 0, whereas the right side is positive for any $0<q<1$ provided $N$ is large enough. Introducing the maximal probability of error in lieu of the average probability of error, it is possible to modify the incorrect bound and obtain the following result involving the input entropy.

**Theorem 6:** Assume that $X$ and $Y$ take values on the same set $\Omega$ and denote $\rho=\inf_{\omega\in\Omega}P[X=Y|X=\omega]=\inf_{\omega\in\Omega}P_{Y|X}(\omega|\omega)$. Then,

$$I(X;Y)\ge\rho H(X)-h(P[X=Y])$$

_Proof:_ Expanding mutual information, we obtain:

$$I(X;Y)=\sum_{a\in\Omega}P_{Y|X}(a|a)P_{X}(a)\log\frac{1}{P_{X}(a)} + \sum_{a\in\Omega}P_{Y|X}(a|a)P_{X}(a)\log\frac{P_{Y|X}(a|a)P_{X}(a)}{P_{Y}(a)} + \sum_{a\in\Omega}\sum_{b\ne a}P_{Y|X}(b|a)P_{X}(a)\log\frac{P_{Y|X}(b|a)P_{X}(a)}{P_{Y}(b)P_{X}(a)}$$

$$\ge\rho H(X) + P[X=Y]\log P[X=Y] + P[X\ne Y]\log\frac{P[X\ne Y]}{P[\overline{X}\ne\overline{Y}]}$$

where we have used the definition of $\rho$, the log-sum inequality, and the notation $P[\overline{X}=\overline{Y}]=\sum_{\omega\in\Omega}P_{X}(\omega)P_{Y}(\omega)$.

If, in addition to the sufficient condition in Theorem 6, the following condition holds: $\rho\ge P[X\ne Y]$ (which occurs, for example, when $\rho>\frac{1}{2}$), then the bound in Theorem 6 can be replaced by the weaker bound $I(X;Y)\ge\rho H(X)-h(\rho)$, which was known to hold in the special case $\rho>1-e^{-1}$.

To conclude this section, we note that the restriction that $X$ and $Y$ take values on the same set has been made throughout for convenience in expressing the results. It is easy to see from the mutual-information data processing lemma that the restriction can be lifted in the foregoing results by replacing $P[X=Y]$ and $P[\overline{X}=\overline{Y}]$ by $P[X=\phi(Y)]$ and $P[\overline{X}=\phi(\overline{Y})]$ respectively, where $\phi$ is an arbitrary function mapping the set of $Y$ values to the set of $X$ values.

### III.

MUTUAL INFORMATION AND ERROR PROBABILITY

In this section we illustrate the use of the results found in Section II in order to lower bound the error probability of $M$-ary hypothesis testing. Let $X$ take values on $\{1,\cdots M\}$, and let $Z$ be the observable whose conditional distribution given that $X=j$ is $Q_{j}$. Define $\epsilon_{X}=1-\max_{1\le j\le M}P_{X}(j)$ and $\epsilon_{X|Z}=1-E[\max_{1\le j\le M}Q_{j}(Z)P_{X}(j)/P_{Z}(Z)]$, where $P_{Z}(b)=\sum_{j=1}^{M}P_{X}(j)Q_{j}(b)$. Note that $\epsilon_{X}$ and $\epsilon_{X|Z}$ are the a priori and a posteriori minimum probabilities of error, respectively. In decision theory, the following bound on the error probability of equiprobable hypothesis testing is well known.

**Theorem 7:** The minimum probability of error for any test between equiprobable hypotheses $\{Q_{i},i=1,\cdots M\}$ is lower bounded by

$$\epsilon_{X|Z}\ge1-\frac{1}{\log M}\left(\frac{1}{M^{2}}\sum_{i=1}^{M}\sum_{j=1}^{M}D(Q_{i}||Q_{j})+\log 2\right)$$

_Proof:_ Fix a test, and let $Y$ be its output. Theorem 7 follows by applying Theorem 1 to $(X, Y)$ and bounding: $I(X;Y)\le I(X;Z) = \frac{1}{M}\sum_{i=1}^{M}D(Q_{i}||\frac{1}{M}\sum_{j=1}^{M}Q_{j}) \le\frac{1}{M^{2}}\sum_{i=1}^{M}\sum_{j=1}^{M}D(Q_{i}||Q_{j})$, where the inequalities follow from the data processing lemma and the convexity of divergence, respectively.

Following a similar proof, Theorem 7, which holds only for equiprobable hypotheses, can be generalized via Theorem 5 as follows.

**Theorem 8:** The minimum probability of error for any test between hypotheses $\{Q_{i},i=1,\cdots M\}$ is lower bounded by

$$\epsilon_{X|Z}\ge1+\frac{1}{\log \max_{j}q_{j}}\left(\sum_{i=1}^{M}\sum_{j=1}^{M}q_{i}q_{j}D(Q_{i}||Q_{j})+\log 2\right)$$

where $q_{j}$ is the a priori probability of the $j$-th hypothesis. (Note here that $M$ need not be finite.)

Rather than using Theorem 7, it is more common in information theory to use (in converse proofs) the tighter result $\epsilon_{X|Z}\ge1-\frac{I(X;Z)+\log 2}{\log M}$ which follows directly from Theorem 1. However, this holds only for equiprobable hypotheses. In the general nonequiprobable case, Theorem 5 results in $\epsilon_{X|Z}\ge1+\frac{I(X;Z)+\log 2}{\log(1-\epsilon_{X})}$, which can be viewed as a lower bound on mutual information as a function of $\epsilon_{X|Z}$ and $\epsilon_{X}$. A tighter such bound is given by the following result.

**Theorem 9:** If $X$ is finitely valued (or countably infinite), $I(X;Z)\ge d(\epsilon_{X|Z}||\epsilon_{X})$.

_Proof:_ Let $\hat{X}(Z)$ be the maximum a posteriori estimate of $X$ given $Z$. The mutual-information data processing theorem and Theorem 3 yield $I(X;Z)\ge I(X;\hat{X}(Z)) \ge d(P[X\ne\hat{X}(Z)]||P[\overline{X}\ne\hat{X}(Z)]) \ge d(\epsilon_{X|Z}||\epsilon_{X})$ where $\overline{X}$ is independent of $Z$ and has the same distribution as $X$. In order to check this, note that $\epsilon_{X|Z}=P[X\ne\hat{X}(Z)]$ and $\epsilon_{X}\le P[\overline{X}\ne\hat{X}(Z)]$, because when the maximum a posteriori estimator is driven by observations that are independent of $X$, it cannot achieve better error probability than the minimum a priori error probability $\epsilon_{X}$. Finally, it is easy to check that $d(a||b)\le d(a||c)$ if $0\le a\le b\le c\le1$.

In Theorem 3 we derived a necessary and sufficient condition for equality, which leads us to conclude that the bound in Theorem 9 will not be tight unless $X$ is equiprobable. If $X$ is indeed equiprobable over the $M$ elements, then, for every value $\delta\le1-1/M$, it is possible to find $Z$ such that $\delta=\epsilon_{X|Z}$ and $I(X;Z)=d(\epsilon_{X|Z}||\epsilon_{X})$ because $\epsilon_{X}=1-1/M$. (For example, given $X$, let $Z=X$ with probability $1-\delta$ and let it be equidistributed on the other $M-1$ values, with probability $\delta$.)

Conversely to Theorem 9, we can find upper bounds on mutual information as a function of the a priori and a posteriori error probabilities: $I(X;Z)=H(X)-H(X|Z) \le \log M-\epsilon_{X|Z}\log 4$, where the last inequality follows from Gallager ([9], p. 520). It is possible to tighten this using the sharp bounds $H(X)\le\epsilon_{X}\log(M-1)+h(\epsilon_{X})$ and $H(X|Z)\ge\phi^{*}(\epsilon_{X|Z})$, where $\phi^{*}(\epsilon_{X|Z})$ is the piecewise linear convex function defined in [5] and shown to be the tightest lower bound on the conditional entropy $H(X|Z)$ as a function of $\epsilon_{X|Z}$. However, it does not follow that $I(X;Z)\le\epsilon_{X}\log(M-1)+h(\epsilon_{X})-\phi^{*}(\epsilon_{X|Z})$ is the tightest possible bound in terms of $\epsilon_{X}$ and $\epsilon_{X|Z}$ because the foregoing bounds have not been shown to be simultaneously tight.