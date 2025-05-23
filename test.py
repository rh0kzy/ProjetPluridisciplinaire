import numpy as np
import plotly.graph_objects as go

# Créer une grille de coordonnées sphériques
theta = np.linspace(0, np.pi, 100)  # Angle polaire (0 à pi)
phi = np.linspace(0, 2 * np.pi, 100)  # Angle azimutal (0 à 2pi)
theta, phi = np.meshgrid(theta, phi)

# Motif de rayonnement d'une antenne dipôle (proportionnel à sin²(theta))
pattern = np.sin(theta)**2

# Conversion en coordonnées cartésiennes
x = pattern * np.sin(theta) * np.cos(phi)
y = pattern * np.sin(theta) * np.sin(phi)
z = pattern * np.cos(theta)

# Créer la figure 3D avec Plotly
fig = go.Figure(data=[
    go.Surface(x=x, y=y, z=z, colorscale='Viridis', showscale=True)
])

# Configurer la mise en page
fig.update_layout(
    title='Motif de Rayonnement 3D d\'une Antenne Dipôle',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Afficher la figure
fig.show()