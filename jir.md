#A Tight Upper Bound on the Bayesian Probability of Error

This is the complete text of a paper authored by W. A. Hashlamoun, P. K. Varshney, and V. N. S. Samarasooriya.

**Abstract**
The authors present a new upper bound on the minimum probability of error for Bayesian decision systems. This new bound is continuous everywhere and tighter than existing bounds, such as the Bhattacharyya and Bayesian bounds.

**I. Introduction**
In statistical pattern recognition, system performance is measured by the probability of error (misrecognition/misclassification). Evaluating this is difficult because it relies on the discontinuous $min(\cdot)$ function. Researchers often use tight upper and lower analytical bounds to compare the performance of optimum systems. Existing bounds include:

* 
**Bhattacharyya Bound:** Simple to evaluate and has closed-form expressions for common distributions, but it is a loose bound.


* 
**Chernoff Bound:** Uses an optimizing scalar $s$ ($0<s<1$), but is mathematically difficult to evaluate and does not generally provide tighter bounds than Bhattacharyya.


* 
**Equivocation Bound:** Tighter than the Bhattacharyya bound.


* 
**Bayesian Distance Bound:** Tighter than both Bhattacharyya and equivocation bounds.



**II. A Tight Upper Bound on the Probability of Error**
For a two-class problem, let $C_{1}$ and $C_{2}$ be two pattern classes with a priori probabilities $\pi_{1}$ and $\pi_{2}$. A decision is made based on a random feature $X$ with conditional probability density functions $f_{1}(x)$ and $f_{2}(x)$.

The optimum system uses the maximum a posteriori probability (MAP) selection rule. If we denote $p=P(C_{1}|x)$, the conditional probability of error is:


$$P(E|x)=\min(p,1-p)\triangleq g(p)$$



The total expected probability of error is:


$$P(E)=\int_{x}g(p)(\pi_{1}f_{1}(x)+\pi_{2}f_{2}(x))dx$$



Because $g(p)$ is discontinuous at $p=0.5$, the authors seek a continuous approximation function $g^{*}(p)$ to form a bound. The function $g^{*}(p)$ must satisfy five conditions:

1. 
$g^{*}(p)\ge g(p)$ for all $0\le p\le1$, and $g^{*}(0)=g^{*}(1)=0$.


2. It must be continuous and differentiable everywhere.


3. It must be symmetrical about $p=0.5$.


4. 
$g^{*}(0.5)=0.5$.


5. 
$dg^{*}/dp(0)\ge1$ and $dg^{*}/dp(1)\le-1$.



*Existing functions that meet these criteria include:*

* Bhattacharyya: 


$$g_{B}(p)=(p(1-p))^{0.5}$$





* Equivocation: 


$$g_{E}(p)=0.5(p\log(p)+(1-p)\log(1-p))/\log(0.5)$$





* Bayesian distance: 


$$g_{Y}(p)=2p(1-p)$$






*The Proposed Function:*
The authors introduce a sinusoidal function $g_{s}(p)=0.5\sin\pi p$. To tighten the bound and match the correct slopes at $p=0$ and $p=1$, they weight it by an exponentially decaying Gaussian function:


$$g_{N}(p)=0.5(\sin\pi p)\exp[-\alpha(p-0.5)^{2}]$$



By setting the derivative at $p=0$ equal to $1$, they solve for $\alpha=1.8063$. This yields the final proposed approximating function:


$$g_{N}(p)=0.5(\sin\pi p)\exp[-1.8063(p-0.5)^{2}]$$



This leads to the new tight upper bound on the probability of error:


$$P(E)\le\int_{x}(0.5(\sin\pi p)\exp[-1.8063(p-0.5)^{2}])f(x)dx$$



**III. Examples**
The authors test their new bound against exact minimum errors, the Bhattacharyya bound, and the Bayesian bound.

* **Example 1 (Univariate Gaussian):** Evaluates a feature $X$ as a Gaussian random variable. Under $C_{1}$, $X\sim N(m_{1},\sigma_{1}^{2})$ and under $C_{2}$, $X\sim N(m_{2},\sigma_{2}^{2})$. The authors evaluated cases where parameters are known exactly, and where parameters are unknown and estimated using maximum likelihood (ML) estimates ($\overline{m}_{1}$) from $n_{1}$ training samples. They showed that by selecting enough training samples, they can obtain a **95%** assurance that the estimation error ($m_{e}$) for $m_{1}$ does not exceed an allowable error limit of **±5%**.


* 
**Example 2 (Bivariate Gaussian):** Evaluates a feature $\underline{X}$ as a jointly Gaussian random vector with mean vector $\underline{m}_{j}$ and a common covariance matrix $\Sigma$. A plot was constructed comparing the exact probability of error against the new bound and Bhattacharyya bound against correlation variable $m_{12}$ with variance $\sigma^{2}=1.0$.



**IV. Summary**
The paper concludes that evaluating the exact probability of error analytically is often difficult. The authors successfully developed a new upper bound based on functional approximation and demonstrated through numerical results that it is tighter than several currently available bounds.

While the provided text does not contain formal mathematical proofs in the traditional "Theorem-to-Q.E.D." format, it does provide the step-by-step mathematical derivations the authors used to construct their new upper bound and estimate the required sample size for unknown parameters.

Here are the full mathematical derivations extracted exactly as they are presented in the paper:

### Derivation 1: Constructing the New Upper Bound Function $g_N(p)$

The authors seek to find a function $g^*(p)$ that closely approximates the exact minimum probability of error $g(p) = \min(p, 1-p)$.

* First, they consider a sinusoidal function:


$$g_s(p) = 0.5 \sin \pi p$$





* They demonstrate that for all values of $p$ in the range $0 \le p \le 1$, this function is tighter than the Bayesian bound $g_Y(p)$, establishing the inequality:


$$0.5 \sin \pi p \le 2p(1-p)$$





* Differentiating the sinusoidal function $g_s(p)$ and evaluating it at $p=0$ yields a slope of **1.57**.


* Because the true slope of $g(p)$ at $p=0$ is exactly **1**, they tighten the bound by weighting the sinusoidal function with a Gaussian function to form $g_N(p)$:


$$g_N(p) = 0.5(\sin \pi p)\exp[-\alpha(p-0.5)^2]$$





* The Gaussian function exhibits exponential decay, allowing it to approximate $g(p)$ better than the sinusoidal function alone.


* To find the parameter $\alpha$, the authors differentiate $g_N(p)$ with respect to $p$ and set the derivative at $p=0$ equal to **1**. This forces both $g_N(p)$ and $g(p)$ to have the same slope at the points $p=0$ and $p=1$.


* Solving this derivative yields $\alpha = 1.8063$.


* Therefore, the final approximating function is:


$$g_N(p) = 0.5(\sin \pi p)\exp[-1.8063(p-0.5)^2]$$





* When substituted into the unconditional probability of error integral, this provides the new upper bound:


$$P(E) \le \int_x (0.5(\sin \pi p)\exp[-1.8063(p-0.5)^2])f(x)dx$$






---

### Derivation 2: Maximum Likelihood Estimation Bounds (Finite Sample Size)

In Example 1 (Case ii), the authors derive the necessary sample size $n_1$ to ensure the estimation error of an unknown mean $m_1$ remains within a specified limit $m_e$ with a 95% degree of confidence.

* Using $n_1$ training samples from class 1, the maximum likelihood estimate of the mean is:


$$\bar{m}_1 = \frac{1}{n_1}\sum_{j=1}^{n_1}X_j^{(1)}$$





* This estimate is normally distributed with an expected value $E(\bar{m}_1) = m_1$ and a variance $Var(\bar{m}_1) = \sigma^2/n_1 = \sigma_*^2$.


* The maximum allowable estimation error is defined as:


$$m_e = |(\bar{m}_1)_{max} - m_1|$$





* To ensure 95% or more of the area under the density function of $\bar{m}_1$ falls within the band $(\bar{m}_1)_{max} - m_e \le \bar{m}_1 \le (\bar{m}_1)_{max} + m_e$, they establish the condition:


$$2\sigma_* \le m_e$$





* Squaring both sides and substituting the definitions of $m_e$ and $\sigma_*^2$ yields:


$$[(\bar{m}_1)_{max} - m_1]^2 \ge 4\sigma_*^2 = 4\sigma^2/n_1$$





* Rearranging this inequality to solve for the required sample size $n_1$ gives the final bound:


$$n_1 \ge \left(\frac{2\sigma}{(\bar{m}_1)_{max} - m_1}\right)^2$$