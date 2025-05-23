import numpy as np
import plotly.graph_objects as go

# Paramètres normalisés
f = 2.45e9            # fréquence (Hz)
c = 3e8               # vitesse de la lumière
lambda0 = c / f       # longueur d'onde
L = lambda0 / 2       # longueur du patch
W = lambda0 / 2       # largeur du patch
h = 1.6e-3            # épaisseur du substrat (ex: 1.6 mm)
epsilon_r = 2.22      # constante diélectrique (ex: fleece fabric)

# Grilles sphériques
theta = np.linspace(0.01, np.pi - 0.01, 180)
phi = np.linspace(0, 2 * np.pi, 360)
theta_grid, phi_grid = np.meshgrid(theta, phi)

# Modèle simplifié de rayonnement (comme patch idéal)
kx = (np.pi * L / lambda0) * np.sin(theta_grid) * np.cos(phi_grid)
ky = (np.pi * W / lambda0) * np.sin(theta_grid) * np.sin(phi_grid)

def sinc(x):
    return np.where(x == 0, 1, np.sin(x) / x)

# Motif de rayonnement approximé
E = np.abs(sinc(kx) * sinc(ky) * np.cos(theta_grid))

# Normalisation + passage en dB
E = E / np.max(E)
E_dB = 20 * np.log10(E + 1e-12)  # éviter log(0)

# Coordonnées sphériques → cartésiennes
r = E
x = r * np.sin(theta_grid) * np.cos(phi_grid)
y = r * np.sin(theta_grid) * np.sin(phi_grid)
z = r * np.cos(theta_grid)

# Tracé 3D avec Plotly
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, surfacecolor=E_dB, colorscale='Jet')])
fig.update_layout(
    title="Diagramme 3D du gain en dB – Antenne patch (εr = 2.22, Fleece)",
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectratio=dict(x=1, y=1, z=0.7)
    ),
    coloraxis_colorbar=dict(title="Gain (dB)")
)
fig.show()
