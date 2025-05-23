import numpy as np

def pattern_from_slices(vert_slice, theta, horiz_slice=None, phi=None, method='Summation'):
    """
    Reconstruct a 3D radiation pattern from one or two orthogonal 2D slices.

    Parameters
    ----------
    vert_slice : array_like
        Magnitude (linear or dB) of the elevation slice vs. θ (radians or degrees).
    theta : array_like
        Elevation angles corresponding to vert_slice (radians or degrees).
    horiz_slice : array_like, optional
        Magnitude of the azimuth slice vs. φ (radians or degrees). If not given,
        an omnidirectional assumption (azimuthal symmetry) is used.
    phi : array_like, optional
        Azimuth angles corresponding to horiz_slice (radians or degrees).
    method : {'Summation', 'CrossWeighted'}, optional
        Reconstruction algorithm:
          Summation    : E(θ,φ)=E_vert(θ)+E_horiz(φ)
          CrossWeighted: E(θ,φ)=√[E_vert(θ)·E_horiz(φ)]
        Default is 'Summation'.

    Returns
    -------
    pattern3d : 2D ndarray
        Reconstructed magnitude pattern on a grid [θ×φ].
    theta_grid, phi_grid : 2D ndarrays
        Meshgrid arrays (θ, φ) for plotting in spherical coords.

    Notes
    -----
    - If horiz_slice or φ is omitted, φ=0…2π and the 3D pattern is just the
      elevation slice revolved around z.
    - Outputs are normalized to peak=1.
    - Input angles may be in degrees or radians; be consistent.
    """
    # ensure numpy arrays
    theta = np.asarray(theta).flatten()
    r_vert = np.asarray(vert_slice).flatten()

    # omnidirectional case
    if horiz_slice is None or phi is None:
        phi = np.linspace(0, 2*np.pi, 361)
        pattern3d = np.tile(r_vert[:, None], (1, phi.size))
        θg, φg = np.meshgrid(theta, phi, indexing='ij')
        return pattern3d / np.max(pattern3d), θg, φg

    # directional case
    phi = np.asarray(phi).flatten()
    r_horiz = np.asarray(horiz_slice).flatten()

    # optional: discard extra points if spans exceed 360°/180° in φ/θ
    # here we simply assume inputs are already in the correct spans

    θg, φg = np.meshgrid(theta, phi, indexing='ij')
    v = r_vert[:, None]
    h = r_horiz[None, :]

    if method.lower() == 'summation':
        pat = v + h
    elif method.lower() == 'crossweighted':
        pat = np.sqrt(v * h)
    else:
        raise ValueError("method must be 'Summation' or 'CrossWeighted'")

    # normalize and return
    pat /= np.max(pat)
    return pat, θg, φg