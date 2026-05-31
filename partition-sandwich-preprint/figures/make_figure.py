import numpy as np
import matplotlib.pyplot as plt

def Hbin(p):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -p*np.log2(p) - (1-p)*np.log2(1-p)

# Lower Fano boundary: parameterise by eps in [0, 0.5]
eps = np.linspace(0, 0.5, 400)
H_fano = Hbin(eps)
eps_fano = eps

# Upper HR boundary: eps = H/2 for H in [0, 1]
H_hr = np.linspace(0, 1, 400)
eps_hr = H_hr / 2

fig, ax = plt.subplots(figsize=(5.2, 3.6))
# Shade region
H_grid = np.linspace(1e-4, 1, 400)
def Hinv(h):
    out = np.zeros_like(h)
    for i, hi in enumerate(h):
        lo, hi_ = 0.0, 0.5
        for _ in range(60):
            m = (lo+hi_)/2
            if Hbin(m) < hi:
                lo = m
            else:
                hi_ = m
        out[i] = (lo+hi_)/2
    return out

lower = Hinv(H_grid)
upper = H_grid/2
ax.fill_between(H_grid, lower, upper, color='#cfe2f3', alpha=0.8, label=r'$\widetilde{A}_2$')

ax.plot(H_fano, eps_fano, color='#1f4e79', lw=1.8, label=r'$\varepsilon=H_{\mathrm{bin}}^{-1}(H)$ (Fano)')
ax.plot(H_hr, eps_hr, color='#a30000', lw=1.8, label=r'$\varepsilon=H/2$ (Hellman--Raviv)')

# Slack maximiser
eps_star = 0.2
H_star = Hbin(eps_star)
w_star = 0.5*H_star - eps_star
ax.plot([H_star, H_star], [eps_star, H_star/2], color='black', lw=1.0, linestyle=':')
ax.plot(H_star, eps_star, 'o', color='#1f4e79', ms=5)
ax.plot(H_star, H_star/2, 'o', color='#a30000', ms=5)
ax.annotate(f'$w^*\\approx{w_star:.3f}$', xy=(H_star, (eps_star+H_star/2)/2),
            xytext=(H_star+0.05, (eps_star+H_star/2)/2 - 0.02),
            fontsize=9)

# Witness points
ax.plot(Hbin(0.3), 0.3, 's', color='#1f4e79', ms=5)
ax.annotate(r'$\Pi_{0.3}^{\mathrm{F}}$', xy=(Hbin(0.3), 0.3), xytext=(Hbin(0.3)-0.18, 0.31), fontsize=9)
ax.plot(0.6, 0.3, 's', color='#a30000', ms=5)
ax.annotate(r'$\Pi_{0.6}^{\mathrm{HR}}$', xy=(0.6, 0.3), xytext=(0.62, 0.30), fontsize=9)

ax.set_xlim(0, 1.02)
ax.set_ylim(0, 0.52)
ax.set_xlabel(r'$H(f\mid\Pi)$ (bits)')
ax.set_ylabel(r'$\varepsilon^*_\Pi$')
ax.grid(alpha=0.3)
ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
plt.tight_layout()
plt.savefig('achievable_region.pdf', bbox_inches='tight')
print("saved")
