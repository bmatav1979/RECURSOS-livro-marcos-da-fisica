import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parâmetros orbitais: unidades astronômicas (UA) e anos
a = 1.0                 # semieixo maior [UA]
e = 0.40                # excentricidade: 0 <= e < 1
T = np.sqrt(a**3)       # 3ª lei de Kepler para órbita solar
n_frames = 500


def resolver_equacao_kepler(M, e, tol=1e-12, max_iter=50):
    """Resolve E - e sen(E) = M pelo método de Newton."""
    E = M if e < 0.8 else np.pi
    for _ in range(max_iter):
        delta = (E - e*np.sin(E) - M) / (1 - e*np.cos(E))
        E -= delta
        if abs(delta) < tol:
            break
    return E


# Tempos igualmente espaçados: o movimento respeita a lei das áreas
t = np.linspace(0.0, T, n_frames, endpoint=False)
M_anom = 2*np.pi*t/T
E_anom = np.array([resolver_equacao_kepler(Mi, e) for Mi in M_anom])

# Sol no foco da elipse
x = a*(np.cos(E_anom) - e)
y = a*np.sqrt(1 - e**2)*np.sin(E_anom)

fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(x, y, color="royalblue", lw=1.5, label="órbita")
ax.scatter(0, 0, s=180, color="gold", edgecolor="darkorange",
           zorder=3, label="Sol")
planeta, = ax.plot([], [], "o", color="crimson", ms=8, label="planeta")
raio, = ax.plot([], [], color="gray", lw=0.8, alpha=0.7)
tempo = ax.text(0.03, 0.95, "", transform=ax.transAxes)

lim = a*(1 + e) + 0.15*a
ax.set(xlim=(-lim, lim), ylim=(-lim, lim),
       xlabel="x [UA]", ylabel="y [UA]",
       title=f"Órbita kepleriana: a = {a:.2f} UA, e = {e:.2f}")
ax.set_aspect("equal")
ax.grid(alpha=0.25)
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig("orbita_kepler.png", dpi=200, bbox_inches="tight")


def atualizar(i):
    planeta.set_data([x[i]], [y[i]])
    raio.set_data([0, x[i]], [0, y[i]])
    tempo.set_text(f"t = {t[i]:.3f} ano")
    return planeta, raio, tempo


animacao = FuncAnimation(
    fig, atualizar, frames=n_frames, interval=25, blit=True
)

plt.show()

# Para salvar também a animação, instale Pillow ou FFmpeg e
# descomente UMA das linhas abaixo:
# animacao.save("orbita_kepler.gif", writer="pillow", fps=30)
# animacao.save("orbita_kepler.mp4", writer="ffmpeg", fps=30, dpi=150)
