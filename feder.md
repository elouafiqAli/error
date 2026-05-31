# Relations Between Entropy and Error Probability 

**Meir Feder**, *Senior Member, IEEE*, and **Neri Merhav**, *Senior Member, IEEE* 

**Abstract**—The relation between the entropy of a discrete random variable and the minimum attainable probability of error made in guessing its value is examined. While Fano's inequality provides a tight lower bound on the error probability in terms of the entropy, we derive a converse result a tight upper bound on the minimal error probability in terms of the entropy. Both bounds are sharp, and can draw a relation, as well, between the error probability for the maximum a posteriori (MAP) rule, and the conditional entropy (equivocation), which is a useful uncertainty measure in several applications. Combining this relation and the classical channel coding theorem, we present a channel coding theorem for the equivocation which, unlike the channel coding theorem for error probability, is meaningful at all rates. This theorem is proved directly for DMC's, and from this proof it is further concluded that for $R\ge C$ the equivocation achieves its minimal value of $R-C$ at the rate of $n^{1/2}$ where n is the block length. 

**Index Terms**—Entropy, error probability, equivocation, predictability, Fano's inequality, channel coding theorem. 

---

I. INTRODUCTION 

Intuitively, the entropy H of a random variable measures its complexity, or its degree of randomness. It seems plausible that the higher the entropy the harder it is to predict the value taken by this random variable. If the money made in gambling on the predicted value is a criterion for good prediction, this intuitive notion is affirmed by the observation (see, e.g., [10], [3]) that the optimal capital growth rate achievable by gambling on the outcome of, say, a binary random variable is $1-H$, i.e., the smaller the entropy the larger is the achievable capital growth rate. However, the degree of difficulty in predicting the value of the random variable is more naturally assessed by the minimal possible error probability associated with any prediction procedure. As was observed in [5], this prediction error is not uniquely determined by the entropy, i.e., two random variables with the same entropy may have different minimal prediction error probabilities. 

In this work we further explore the relationship between the entropy of a random variable and the minimal error probability in guessing its value. While the well-known Fano inequality provides a tight lower bound on the error probability in terms of the entropy, we derive a converse result-a tight upper bound on the minimal error probability in terms of the entropy. This converse result is known in the binary case, see, e.g.. [1] and [8], but we derive here the bound for the general case and show that it is tight. Since both Fano's inequality and the new bound are sharp, they determine the region of all allowable pairs of entropy and minimal error probability. These bounds are also applied to conditional entropies and the error probabilities obtained in the maximum a posteriori (MAP) rule: thus they also draw a relation between the entropy rate of a process (the process compressibility) and the minimal expected fraction of errors made by predicting its future outcome (the process predictability). Similar relations exist between the minimal average fraction of errors made in sequential prediction of sequences from a given set, and the size of the set. 

While the entropy is the basic measure of uncertainty used in information theory, the channel coding theorems are usually stated in terms of the error probability. The relation between entropy and error probability allows us to state these theorems in terms of the entropy. In this work we prove directly the channel coding theorem for discrete memoryless channels (DMC's) using the conditional entropy of the channel input given the channel output (equivocation) as the desired error measure. Unlike the standard coding theorem, this coding theorem is relevant in describing the behavior of information transmission at rates below capacity, at capacity, and above the channel capacity. 

Let us first recall the definitions of the entropy and the minimal error probability. Let X be a random variable over the alphabet $\{1,\cdot\cdot\cdot,M\}$, and suppose its probability distribution $\{p(x)\}_{x=1}^{M}$ is given.  The entropy of the random variable is


$$H(X)=-\sum_{x=1}^{M}p(x)\log p(x)$$

where throughout the paper $\log=\log_{2}$ and the entropy is measured in bits. In the absence of any other knowledge regarding X, the estimator of X that minimizes the error probability is the value with the highest probability. Let $\hat{p}=p(\hat{x})=\max_{x}p(x)$.  The minimal error probability in guessing the value of X is thus,


$$\pi(X)=\sum_{x\ne\hat{x}}p(x)=1-\hat{p}.$$



The maximal entropy over an alphabet of size M is $\log M$, while the highest possible minimal error probability is $(M-1)/M$ both attained by a uniform random variable. On the other extreme, a random variable for which the entire probability mass is concentrated on a single value, has both a zero entropy and a zero minimal error probability. 

The "uncertainty" in X given another random variable Y is usually assessed by the conditional entropy, or the equivocation. Let Y be a random variable (or vector) over an arbitrary sample space with a well-defined probability distribution $P(y)$, such that for each $y\in\mathcal{Y}$ (with a possible exception of a zero measure set), a probability mass function $p(\cdot|y)$ is well defined.  Then we define the equivocation as


$$H(X|Y)=-\int_{\mathcal{Y}}\sum_{x}p(x|y)\log p(x|y)dP(y)$$

The minimum probability of error in estimating X given an observation y of Y is attained by the maximum a posteriori (MAP) estimator, i.e., by $\hat{x}(y)=\arg\max_{x}p(x|y)$.  Thus, the expected minimal error probability is


$$\pi(X|Y)=\int_{\mathcal{Y}}[1-\max_{x}p(x|y)]dP(y).$$



Let $\mathcal{X}=\{X_{t}\}_{t=-\infty}^{\infty}$ be a stationary ergodic random process.  The entropy rate of this process is given by


$$\mathcal{H}(\mathcal{X})=\lim_{n\rightarrow\infty}H(X_{n}|X_{n-1},\cdot\cdot\cdot,X_{1}).$$


Similarly, we define the predictability of the process as


$$\Pi(\mathcal{X})=\lim_{n\rightarrow\infty}\pi(X_{n}|X_{n-1},\cdot\cdot\cdot,X_{1})$$

where this quantity is the expected minimal error probability in predicting the future value of the process given its past. The limits exist since both the conditional entropy and the predictability are positive and monotonically nonincreasing with n. 

In the next section we present the bounds and the relation between the entropy and the minimal error probability. Despite the fact [5] that there is no one-to-one relation between the entropy and the minimal error probability, the bounds affirm that a variable is totally random (i.e., its entropy $\log M$) iff it is totally unpredictable (i.e., its minimal error probability is $(M-1)/M$) and conversely, a variable is totally redundant (i.e., its entropy is zero) iff it is fully predictable (its minimal probability of error is zero). In Section III, the relations are applied to derive a bound on the fraction of errors made by arbitrary predictors over a set of arbitrary sequences. Finally, in the last section, we present a channel coding theorem in terms of the equivocation.  This theorem could have been derived by combining the classical coding theorem which deals with the error probability and the relations presented here. We chose to develop in this work a direct proof, which we believe provides more insight on the behavior of the equivocation at rates equal or greater than the channel capacity. 

---

### II. 

THE BOUNDS 

Consider first a discrete random variable X taking values in the set $\{1,\cdot\cdot\cdot,M\}$ with probabilities $p(1),p(2),\cdot\cdot\cdot,p(M)$, and assume without loss of generality that $p(1)\ge p(2)\ge\cdot\cdot\cdot\ge p(M)$. We define the probability vector $p=[p(1),\cdot\cdot\cdot,p(M)]$, and use interchangeably the notation $H(p)$ or $H(X)$ for the entropy and similarly we use interchangeably $\pi(p)$ or $\pi(X)$ for the minimal error probability (or the predictability). Note that $p(1)=1-\pi(p).$  Clearly given $\pi$ we can bound the entropy as


$$\max_{p\in P_{\pi}}H(p)\ge H(X)\ge \min_{p\in P_{\pi}}H(p)$$

where $P_{\pi}$ is the set of all vectors p such that $p(i)\ge 0\forall i$, $\sum_{i}p(i)=1$ and $p(1)=1-\pi$. As shown in the following two lemmas, the maximization and minimization can be solved explicitly. 

**Lemma 1:** The maximum is achieved by


$$p_{max}(\pi)=[1-\pi,\frac{\pi}{M-1},\cdot\cdot\cdot,\frac{\pi}{M-1}]$$


and the corresponding maximum entropy is


$$\Phi(\pi)=H(p_{max}(\pi))=h(\pi)+\pi\log(M-1)$$

where $h(\alpha)=-\alpha\log\alpha-(1-\alpha)\log(1-\alpha)$ is the binary entropy function.  Note that for any random variable X over an alphabet of size M, it implies that


$$H(X)\le h(\pi)+\pi\log(M-1).$$

which is a special case of Fano's inequality.  The proof of Lemma 1 is straightforward and is given, for example, in [4, p. 39 and p. 48]. In fact, the proof in [4] was provided to show that Fano's inequality is sharp. 

**Lemma 2:** The minimum is achieved by $p_{min}(\pi)=[p(1),\cdot\cdot\cdot,p(M)]$ where

* 
$p(1)=1-\pi, p(2)=\pi, p(3)=\cdot\cdot\cdot=p(M)=0$, for $0\le\pi\le\frac{1}{2}$ 


* 
$p(1)=p(2)=1-\pi, p(3)=2\pi-1, p(4)=\cdot\cdot\cdot=p(M)=0$, for $\frac{1}{2}\le\pi\le\frac{2}{3}$ 


* ...
* 
$p(1)=\cdot\cdot\cdot=p(M-1)=1-\pi, p(M)=1-(M-1)(1-\pi)$, for $\frac{M-2}{M-1}\le\pi\le\frac{M-1}{M}$ 



And the corresponding minimum entropy $\phi(\pi)$ is shown as:

* 
$\phi(\pi) = h(\pi)$, for $0\le\pi\le\frac{1}{2}$ 


* 
$\phi(\pi) = 2h(1-\pi) + (2\pi-1)\log(2)$, for $\frac{1}{2}\le\pi\le\frac{2}{3}$ 


* 
$\phi(\pi) = i\log i (1-\pi) + h(i\pi-(i-1))$, for $\frac{i-1}{i}\le\pi\le\frac{i}{i+1}$ 


* 
$\phi(\pi) = (M-1)\log(M-1)(1-\pi) + h((M-1)\pi-M+2)$, for $\frac{M-2}{M-1}\le\pi\le\frac{M-1}{M}$ 



This lemma is easily shown by straightforward verification of the Kuhn-Tucker conditions. Note that $\phi(\pi)$ is a continuous function with a piecewise continuous derivative, composed of $M-1$ concave segments where the ith segment is composed of a linear term with a slope $i\log i$ and a concave binary entropy function whose argument takes values in the interval $[0, 1/(i+1)]$. 

Since both $\phi(\cdot)$ and $\Phi(\cdot)$ are strictly monotonically increasing continuous functions, they have well defined inverses.  Thus, if the entropy of the random variable is known, say H, we can find upper and lower bounds on the minimal error probability $\pi(X)$ i.e.,


$$\phi^{-1}(H)\ge\pi(X)\ge\Phi^{-1}(H).$$



Consider now the relation between the conditional entropy (equivocation) $H(X|Y)$ and the MAP error probability, $\pi(X|Y)$. It will be useful to define the following function $\phi^{*}(\pi)$:

* 
$\phi^{*}(\pi) = a_{1}\pi+b_{1}$ for $0\le\pi\le\frac{1}{2}$ 


* 
$\phi^{*}(\pi) = a_{i}(\pi-\frac{i-1}{i})+b_{i}$ for $\frac{i-1}{i}\le\pi\le\frac{i}{i+1}$ 



where $a_{i}=i(i+1)\log((i+1)/i)$ and $b_{i}=\log i$. This function, composed of $M-1$ piecewise linear segments is continuous and convex. It is the largest convex function that is still smaller than or equal to $\phi(\pi)$, for $0\le\pi\le(M-1)/M$. It coincides with $\phi(\pi)$ at $\pi=0, 1/2, 2/3, \cdot\cdot\cdot, (M-1)/M$ where it takes the values $0, 1, \log 3, \cdot\cdot\cdot, \log M$. It also coincides with $\Phi(\pi)$ at $\pi=0$ and $\pi=(M-1)/M$ where both functions take the values 0 and $\log M$, respectively.  Actually, if A is the set of all points in the $\pi-H$ plane that satisfy the prior bounds, the convex hull of A, denoted $\tilde{A}$ is the set of all points for which


$$\Phi(\pi)\ge H\ge\phi^{*}(\pi)$$



**Theorem 1:** The equivocation and the MAP error probability lie in the set $\tilde{A}$ in the $\pi-H$ plane, i.e., the equivocation can be bounded in terms of the MAP error probability as


$$\Phi(\pi(X|Y))\ge H(X|Y)\ge\phi^{*}(\pi(X|Y))$$



**Proof:** We may write the equivocation as


$$H(X|Y)=\int_{\mathcal{Y}}H(X|y)dP(y)$$


and the MAP error probability as,


$$\pi(X|Y)=\int_{\mathcal{Y}}\pi(X|y)dP(y)$$

where for each $y\in\mathcal{Y}$, $H(X|y)=H(X|Y=y)$ and $\pi(X|y)=\pi(X|Y=y)$ are the entropy and the predictability, respectively, of a discrete random variable that can take M values. Thus, the points $\{c(y)=(\pi(X|y), H(X|y)), y\in\mathcal{Y}\}$ lie in the region A in the $\pi-H$ plane. Clearly, the point $c=(\pi(X|Y),H(X|Y))$ is a convex combination of the points $c(y)$ where the weights of this combination are given by the distribution $P(y)$. Thus, the point c must lie in $\tilde{A}$, the convex hull of A. 

Observe that both inequalities are tight, i.e., both inequalities can be obtained with equality and so every point on the boundary of the region $\tilde{A}$ can be attained. The upper bound is attained when the conditional distribution $p(x|y)$ is the same for all $y\in\mathcal{Y}$ with a non-zero measure, and is such that $H(X|y)=h(\pi(X|y))+\pi(X|y)\log(M-1).$ The lower bound is attained with equality when for some $y\in\mathcal{Y}, p(x|y)$ has a uniform probability mass of $1/i$ over i values and so $\pi(X|y)=(i-1)/i$ and $H(X|y)=\log i$, while for the rest $y\in\mathcal{Y}$, $p(x|y)$ has a uniform probability mass of $1/(i+1)$ over $i+1$ values and so $\pi(X|y)=i/(i+1)$ and $H(X|y)=\log(i+1)$. 

An immediate corollary of the theorem above is that the entropy rate $\mathcal{H}(\mathcal{X})$ and the predictability $\Pi(\mathcal{X})$ of any stationary process $\mathcal{X}$ over an alphabet of size M also lie in the region $\tilde{A}$ in the $\pi-H$ plane, i.e.,


$$\Phi(\Pi(\mathcal{X}))\ge\mathcal{H}(\mathcal{X})\ge\phi^{*}(\Pi(\mathcal{X})).$$



When we closely observe the points $c_{i}$ where $\pi=[(i-1)/i]$ and $H=\log i, i=1,\cdot\cdot\cdot,M-1$ i.e., the points which lie on the lower bound and at which $\phi(\pi)=\phi^{*}(\pi)$, we observe that at these points $H=\log[1/(1-\pi)]$.  Define


$$\phi^{\prime}(\pi)=\log\frac{1}{1-\pi}$$

and observe that $\phi^{\prime}(\cdot)$ is a convex function that underbounds $\phi(\cdot)$ and $\phi^{*}(\cdot)$. Thus, a lower bound on the entropy in terms of the predictability is $H\ge\phi^{\prime}(\pi)$. Of course this bound is tight only at the points $c_{i}$.  Nevertheless this bound is interesting, recognizing that


$$R_{\infty}(X)\triangleq\lim_{q\rightarrow\infty}R_{q}(X)=\lim_{q\rightarrow\infty}\frac{1}{1-q}\log\sum_{x}p(x)^{q}$$



$$=\log\frac{1}{\max_{x}p(x)}=\log\frac{1}{1-\pi(X)}$$

where $R_{q}(X)$ is the Rényi entropy of order q of X. We recall that Shannon's entropy is the Rényi entropy of order 1. The bound thus follows from the known fact [9], asserting that for all $q>1$, $R_{q}(X)\le R_{1}(X)=H(X)$. 

In this respect we further note that due to the one-to-one relationship between $\pi(X)$ and $R_{\infty}(X)$, Fano's inequality together with our Lemma 2 provide the region of allowable pairs of $R_{\infty}(X)$ and $H(X)$ i.e., for any value of $R_{\infty}(X)$


$$\phi(1-2^{-R_{\infty}(X)})\le H(X)\le\Phi(1-2^{-R_{\infty}(X)}).$$



Now, it should be observed that while $\pi(X)$ and $R_{\infty}(X)$ have a one-to-one relationship, this is no longer true for $\pi(X|Y)$ and $R_{\infty}(X|Y)$.  Thus, while the convex hull of the region provides all allowable pairs of $R_{\infty}(X|Y)$ and $H(X|Y)$, this convex hull is different from the one-to-one transformation of A, given by


$$\phi^{*}(1-2^{-R_{\infty}(X|Y)})\le H(X|Y)\le\Phi(1-2^{-R_{\infty}(X|Y)}),$$


Nevertheless, one may observe that for large, or even moderate, values of $R_{\infty}$


$$R_{\infty}\approx\phi^{*}(1-2^{-R_{\infty}(X|Y)})$$

and so in this case the bound $R_{\infty}<H$ at $R_{\infty}=-\log(1-\pi)$ is indeed a good lower bound on the entropy as a function of the error probability. 

In the binary case, the relevant bounds are


$$h(\pi)\ge H\ge 2\pi$$


or equivalently,


$$\frac{1}{2}H\ge\pi\ge h^{-1}(H)$$



We finally point out that the techniques presented here can be used to derive upper and lower bound on the average loss in terms of the entropy, for general loss functions. 

---

### III. 

PREDICTION OF DETERMINISTIC SEQUENCES FROM A FINITE SET 

We now confine our attention to sequential prediction of arbitrary deterministic sequences. To simplify the exposition we consider in this section binary sequences.  Recall that a sequential predictor of a binary sequence is a procedure for producing at each instant t, upon observing the data $x_{1},\cdot\cdot\cdot,x_{t}$, an estimate of the next outcome $\hat{x}_{t+1}$,


$$\hat{x}_{t+1}=f_{t}(x_{t},\cdot\cdot\cdot,x_{1}).$$

In general $f_{t}(\cdot)$ can either be deterministic or stochastic.  The performance of a deterministic sequential predictor is measured in terms of the fraction of prediction errors along the sequence, i.e., for a sequence $x=x_{1},\cdot\cdot\cdot,x_{n}$ of length n,


$$\pi_{f}(x)=\frac{1}{n}\sum_{t=1}^{n}[1-\delta(x_{t},\hat{x}_{t})]$$

where $\delta(a,b)$ is 1 for $a=b$ and 0, otherwise.  For stochastic predictors, the performance is given by


$$\pi_{f}(x)=E\{\frac{1}{n}\sum_{t=1}^{n}[1-\delta(x_{t},\hat{x}_{t})]\}=\frac{1}{n}\sum_{t=1}^{n}Pr\{x_{t}\ne\hat{x}_{t}\}$$

where it should be kept in mind that the expectation is with respect to the predictor's randomness while the sequence x is fixed. 

Now, as noted in [2], for any sequence there is a predictor that happens to guess correctly its future values, but this predictor may not perform well on other sequences. Thus, we consider the average performance of any predictor over a set of deterministic sequences. Suppose we have a set $\mathcal{X}$ of N binary sequences $\{x^{(1)},\cdot\cdot\cdot,x^{(N)}\}$ each of length n.  The performance of any predictor over this set is


$$\overline{\pi}_{f}(\mathcal{X})=\frac{1}{N}\sum_{j=1}^{N}\pi_{f}(x^{(j)})$$


and so the performance of the best predictor for this set is


$$\overline{\pi}(\mathcal{X})=\min_{f}\overline{\pi}_{f}(\mathcal{X})$$

where the minimization is over all predictors, deterministic or stochastic. We claim the following theorem. 

**Theorem 2:** For any set $\mathcal{X}$ of N binary sequences of length n


$$\frac{1}{2}\cdot\frac{\log N}{n}\ge\overline{\pi}(\mathcal{X})\ge h^{-1}(\frac{\log N}{n})$$



**Proof:** We begin with the lower bound. As was observed in [2], Proposition I, when all $2^{n}$ binary sequences of length n are considered, any deterministic predictor makes exactly k errors over $\binom{n}{k}$ sequences. Thus, the best one can hope for, is to exhaust all possibilities of making i errors or less before making $i+1$ errors.  Let m be the largest integer such that


$$\sum_{i=0}^{m}\binom{n}{i}\le N$$


The minimal total number of errors made by any deterministic predictor over N sequences of length n is lower bounded by


$$k_{n}(N)=\sum_{i=0}^{m}i\binom{n}{i}+(m+1)\cdot(N-\sum_{i=0}^{m}\binom{n}{i})$$


and so


$$\overline{\pi}(\mathcal{X})\ge\frac{1}{nN}k_{n}(N).$$

Since $k_{n}(\cdot)$ is convex and since the performance of any stochastic predictor is a convex combination of deterministic predictors, the lower bound (33) holds for stochastic predictors as well. It is easy to verify that $k_{n}(x)\ge nx h^{-1}(\log x/n)$, $1<x<2^{n}$.  Thus,


$$\frac{1}{nN}k_{n}(N)\ge h^{-1}(\frac{\log N}{n})$$

and the lower bound is proved. 

We now prove the upper bound. Let $N(\nu)$ be the number of sequences in $\mathcal{X}$ that begin with the string $\nu$. In this notation $N=N(\Lambda)$ where $\Lambda$ is the empty string. The predictor that minimizes the total number of errors predicts "0," upon observing the string $\nu$, if $N(\nu 0)>N(\nu 1)$ and "1," otherwise.  Thus, the minimum total number of errors over all sequences is


$$n\cdot N\cdot\overline{\pi}(\mathcal{X})=\sum_{i=0}^{n-1}\sum_{\nu\in\{0,1\}^{i}}\min\{N(\nu 0),N(\nu 1)\}.$$

Since for $0\le\alpha\le 1$, $\min\{\alpha,1-\alpha\}\le\frac{1}{2}h(\alpha)$, 

$$\min\{\frac{N(\nu 0)}{N(\nu)},\frac{N(\nu 1)}{N(\nu)}\}\le\frac{1}{2}(-\frac{N(\nu 0)}{N(\nu)}\log\frac{N(\nu 0)}{N(\nu)}-\frac{N(\nu 1)}{N(\nu)}\log\frac{N(\nu 1)}{N(\nu)})$$

Multiplying both sides by $N(\nu)$ and rearranging the summation, we get 

$$n\cdot N\cdot\overline{\pi}(\mathcal{X})\le-\frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{n}\log\frac{N(p_{j}(x^{(i)}))}{N(p_{j-1}(x^{(i)}))}$$



$$=-\frac{1}{2}\sum_{i=1}^{N}\log\prod_{j=1}^{n}\frac{N(p_{j}(x^{(i)}))}{N(p_{j-1}(x^{(i)}))}$$

where $p_{j}(x^{(i)})$ denotes the prefix of length j of the sequence $x^{(i)}$.  Now observe that due to telescopic multiplication


$$\prod_{j=1}^{n}\frac{N(p_{j}(x^{(i)}))}{N(p_{j-1}(x^{(i)}))}=\frac{N(p_{n}(x^{(i)}))}{N(p_{0}(x^{(i)}))}=\frac{1}{N}$$

for each sequence $x^{(i)}$. Substituting proves the upper bound. 

---

### IV. 

A CHANNEL CODING THEOREM FOR THE EQUIVOCATION 

The coding theorems of information theory are usually stated in terms of error probability. However, it might be useful to state the theorems in terms of the equivocation, for the following reasons. First, the equivocation is a useful uncertainty measure with applications, e.g., in cryptology, see [11] and references therein. Second, the equivocation measures naturally the minimal residual uncertainty about the input, achievable in, e.g., observing the data via a noisy channel. Also, this statement is simpler; in transmitting information at rate R via a noisy channel, the equivocation of the input can be made $R-C$ if $R\ge C$, and 0 if $R\le C$ where C is the channel capacity. 

**Theorem 3:** Consider a DMC with a transition distribution $p(y|x)$. Let a codebook be reconstructed by choosing randomly $M=2^{nR}$ codewords, of length n, using an i.i.d. distribution $q(x)$.  Then, for any $0\le\rho\le 1$, the equivocation, averaged over all codebook selections, satisfies


$$\overline{H}(X|Y)\le(1+\frac{1}{\rho})(\log e)2^{-n[E_{0}(\rho,q)-\rho R]}$$


where $E_{0}(\rho,q)$ is the random coding exponent,


$$E_{0}(\rho,q)=-\log\sum_{y}[\sum_{x}q(x)p(y|x)^{1/(1+\rho)}]^{1+\rho}$$



**Proof:** In the proof we bound from below the average mutual information between the codeword input and the channel output, and the bound then implies the desired upper bound on the equivocation.  For a given codebook $C=\{x_{1},\cdot\cdot\cdot,x_{M}\}$, define


$$J_{C}(x_{m};y)=\log\frac{p(y|x_{m})}{\frac{1}{M}\sum_{m^{\prime}=1}^{M}p(y|x_{m^{\prime}})}.$$


Define


$$J(x_{m};y)=E_{C}\{J_{C}(x_{m};y)\}$$

where the expectation is with respect to all codewords $x_{m^{\prime}}\ne x_{m}$, each chosen with the i.i.d. distribution $q(\cdot)$.  The desired average mutual information is


$$\overline{I}(X;Y)=\frac{1}{M}\sum_{m=1}^{M}E\{J(x_{m};y)\}=E\{J(x_{m};y)\}$$


Calculating $J(x_{m};y)$ explicitly we get,


$$J(x_{m};y)=\log M-E_{C}\{\log\sum_{m^{\prime}=1}^{M}\frac{p(y|x_{m^{\prime}})}{p(y|x_{m})}\}$$



$$=nR-E_{C}\{\log(1+\sum_{m^{\prime}\ne m}\frac{p(y|x_{m^{\prime}})}{p(y|x_{m})})\}$$

Now for any $0\le\rho\le 1$ and nonnegative numbers $\{a_{i}\}$ we have both $\sum_{i}a_{i}\le(\sum_{i}(a_{i})^{1/1+\rho})^{1+\rho}$ and $\sum_{i}a_{i}\le(\sum_{i}(a_{i})^{\rho})^{1/\rho}$.  Thus, we can lower bound $J(x_{m};y)$


$$J(x_{m};y)\ge nR-(1+\rho)E_{C}\{\log(1+\sum_{m^{\prime}\ne m}[\frac{p(y|x_{m^{\prime}})}{p(y|x_{m})}]^{1/1+\rho})\}$$



$$\ge nR-(1+\frac{1}{\rho})E_{C}\{\log(1+[\sum_{m^{\prime}\ne m}[\frac{p(y|x_{m^{\prime}})}{p(y|x_{m})}]^{1/1+\rho}]^{\rho})\}$$



$$\ge nR-(1+\frac{1}{\rho})(\log e)E_{C}\{[\sum_{m^{\prime}\ne m}[\frac{p(y|x_{m^{\prime}})}{p(y|x_{m})}]^{1/1+\rho}]^{\rho}\}$$

where for the first inequality we used (45), for the second inequality we used (46) and the third inequality follows from the relation $x\log e\ge\log(1+x)$.  Now


$$J(x_{m};y)\ge nR-(1+\frac{1}{\rho})(\log e)[E_{C}\{\sum_{m^{\prime}\ne m}[\frac{p(y|x_{m^{\prime}})}{p(y|x_{m})}]^{1/1+\rho}\}]^{\rho}$$



$$\ge nR-(1+\frac{1}{\rho})(\log e)M^{\rho}[\sum_{x^{\prime}}q(x^{\prime})[\frac{p(y|x^{\prime})}{p(y|x_{m})}]^{1/1+\rho}]^{\rho}$$

where the first line follows from Jensen's inequality, the second line follows by writing the expectation over all $x_{m^{\prime}}\ne x_{m}$ explicitly, and the inequality in the third line follows since $M-1$ is replaced by M. 

We now take the second expectation to get a bound for $\overline{I}(X;Y)$


$$\overline{I}(X;Y)\ge nR-(1+\frac{1}{\rho})(\log e)2^{\rho nR}\sum_{y}\sum_{x}q(x)p(y|x)[\sum_{x^{\prime}}q(x^{\prime})[\frac{p(y|x^{\prime})}{p(y|x)}]^{1/1+\rho}]^{\rho}$$



$$=nR-(1+\frac{1}{\rho})(\log e)2^{\rho nR}\sum_{y}[\sum_{x}q(x)p(y|x)^{1/1+\rho}][\sum_{x^{\prime}}q(x^{\prime})p(y|x^{\prime})^{1/1+\rho}]^{\rho}$$



$$=nR-(1+\frac{1}{\rho})(\log e)2^{\rho nR}\sum_{y}[\sum_{x}q(x)p(y|x)^{1/(1+\rho)}]^{1+\rho}$$

Using the definition of the random coding exponent (40), and recalling that $\overline{H}(X|Y)=\overline{H}(X)-\overline{I}(X;Y)$ where $H(X)=\overline{H}(X)=nR$, the desired result (39) follows. 

When $R=C$ we find that the optimal $\rho$ approaches zero.  In this case by letting $\rho=\rho_{n}$ to vanish with n, and using a Taylor expansion of $E_{0}(\rho,q)$ about $\rho=0$ we obtain


$$E_{0}(\rho_{n},q)-\rho_{n}C=-\gamma\rho_{n}^{2}+o(\rho_{n}^{2}),$$


leading to the bound


$$\overline{H}(X|Y)\le(1+\frac{1}{\rho_{n}})(\log e)2^{n\gamma\rho_{n}^{2}}$$

It is clear that the optimal choice is $\rho_{n}=\beta/\sqrt{n}$ for some constant $\beta$, which cancels the exponential growth, with the smallest increase of the $1/\rho_{n}$ term.  With this choice, at $R=C$ the average equivocation of the codebook satisfies


$$\overline{H}(X|Y)\le\alpha\sqrt{n}$$

where $\alpha>0$ is some constant. Thus, the average equivocation rate decays at the rate of $n^{-1/2}$. 

---

ACKNOWLEDGMENT 

The author is particularly indebted to Prof. T. Cover for the wonderful time spent with his group at Stanford where he learned about rate distortion theory and successive refinement. He also wishes to thank his colleague, M. Miller, whose questions about Equitz and Cover's result initiated this work. Finally, he would like to thank Prof. T. Berger, H. Yamamoto, and J. O'Sullivan for helpful comments and, in particular, an anonymous reviewer for pointing out the alternative proof of Theorem 1. We thank N. Shulman for a useful suggestion concerning the proof of Theorem 1. We also acknowledge S. Verdu for his suggestion to present the region of allowable pairs of $R_{\infty}(X)$ and $H(X)$. 

---

REFERENCES 

* [1] T. Berger, Rate Distortion Theory: A Mathematical Basis for Data Compression. Englewood Cliffs, NJ: Prentice-Hall, 1971. 


* [2] R. E. Blahut, Theory and Practice of Information Theory. Reading. MA: Addison-Wesley, 1987. 


* [3] T. M. Cover and J. A. Thomas, Elements of Information Theory. New York: Wiley, 1991. 


* [4] I. Csiszár and J. Körner, Information Theory: Coding Theorems for Discrete Memoryless Systems. New York: Academic, 1981. 


* [5] M. Feder, N. Merhav, and M. Gutman, "Universal prediction of individual sequences," IEEE Trans. Inform. Theory, vol. 38, pp. 1258-1270, July 1992. 


* [6] R. G. Gallager, "A simple derivation of the coding theorem and some applications," IEEE Trans. Inform. Theory, vol. IT-11, pp. 3-18, Jan. 1965. 


* [7] R. G. Gallager, Information Theory and Reliable Communication. New York: Wiley, 1968. 


* [8] M. E. Hellman and J. Raviv, "Probability of error, equivocation, and the Chernoff bound," IEEE Trans. Inform. Theory, vol. IT-16, pp. 368-372, July 1970. 


* [9] G. Jumarie, Relative Information: Theory and Applications. New York: Springer-Verlag, 1990. 


* [10] J. L. Kelly, Jr., "A new interpretation of information rate," Bell Syst. Tech. J., vol. 35, pp. 917-926, 1956. 


* [11] H. Yamamoto, "Information theory in cryptology," IEICE Trans., vol. Е-74, по. 9, pp. 2456-2464, 1991.