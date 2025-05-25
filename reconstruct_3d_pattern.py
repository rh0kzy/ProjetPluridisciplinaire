import numpy as np
from mayavi import mlab

def reconstruct_3d_pattern(vertSlice, theta, horizSlice=None, phi=None, method='Summation'):
    """
    Reconstruct 3D radiation pattern from 2D orthogonal slices.

    Parameters:
    vertSlice : array_like
        1D array of magnitude values vs theta (radians).
    theta : array_like
        1D array of theta angles (radians).
    horizSlice : array_like, optional
        1D array of magnitude values vs phi (radians).
    phi : array_like, optional
        1D array of phi angles (radians).
    method : str, optional
        'Summation' or 'CrossWeighted'. Default 'Summation'.

    Returns:
    pattern3d : 2D ndarray
        Magnitude pattern of shape (len(theta), len(phi)).
    theta_grid, phi_grid : 2D ndarrays
        Meshgrid arrays of theta and phi for plotting.
    """
    theta = np.asarray(theta).reshape(-1)
    r_vert = np.asarray(vertSlice).reshape(-1)

    # Omnidirectional case if no horizontal slice provided
    if horizSlice is None or phi is None:
        phi = np.linspace(0, 2*np.pi, 361)
        pattern3d = np.tile(r_vert[:, None], (1, len(phi)))
        theta_grid, phi_grid = np.meshgrid(theta, phi, indexing='ij')
        return pattern3d, theta_grid, phi_grid

    phi = np.asarray(phi).reshape(-1)
    r_horiz = np.asarray(horizSlice).reshape(-1)

    # Create meshgrids
    theta_grid, phi_grid = np.meshgrid(theta, phi, indexing='ij')
    v = r_vert[:, None]
    h = r_horiz[None, :]

    if method.lower() == 'summation':
        pat = v + h
    elif method.lower() == 'crossweighted':
        pat = np.sqrt(v * h)
    else:
        raise ValueError(f"Unknown method '{method}'. Choose 'Summation' or 'CrossWeighted'.")
    # Normalize pattern to its maximum value
    pat = pat / np.max(pat)
    return pat, theta_grid, phi_grid


def plot_3d_pattern(pattern3d, theta_grid, phi_grid, in_db=False, db_scale=20, title='3D Radiation Pattern'):
    """
    Plot a 3D radiation pattern using Mayavi.

    Parameters:
    pattern3d : 2D ndarray
        Magnitude or dB pattern.
    theta_grid, phi_grid : 2D ndarrays
        Meshgrids of theta and phi.
    in_db : bool, optional
        True if pattern3d is in dB scale. Default False.
    db_scale : float, optional
        Scale for dB conversion (20 for voltage, 10 for power).
    title : str, optional
        Title for the plot. Default '3D Radiation Pattern'.
    """
    # Prepare pattern data
    pat = np.copy(pattern3d)
    if in_db:
        pat = 10 ** (pat / db_scale)
    
    # Convert spherical to Cartesian coordinates
    x = pat * np.sin(theta_grid) * np.cos(phi_grid)
    y = pat * np.sin(theta_grid) * np.sin(phi_grid)
    z = pat * np.cos(theta_grid)

    # Create Mayavi figure
    mlab.figure(title, size=(800, 600))
    
    # Create the surface plot
    surf = mlab.mesh(x, y, z, scalars=pat, colormap='viridis')
    
    # Add colorbar
    mlab.colorbar(surf, title='Magnitude')
    
    # Add axes labels
    mlab.xlabel('X')
    mlab.ylabel('Y')
    mlab.zlabel('Z')
    
    # Show the plot
    mlab.show()

if __name__ == '__main__':
    # Example: Omni-directional dipole
    theta = np.deg2rad(np.linspace(0, 180, 37))  # 0 to 180 degrees
    vertSlice = np.sin(theta)  # Ideal dipole pattern ~ sin(theta)
    pattern3d, th_grid, ph_grid = reconstruct_3d_pattern(vertSlice, theta)
    plot_3d_pattern(pattern3d, th_grid, ph_grid)

    # Example: Directional antenna with both slices (placeholder data)
    # horizSlice = some_horizontal_data
    # phi = np.deg2rad(np.linspace(-180, 180, len(horizSlice)))
    # pattern3d_sum, thg, phg = reconstruct_3d_pattern(vertSlice, theta, horizSlice, phi, method='Summation')
    # plot_3d_pattern(pattern3d_sum, thg, phg)
    # pattern3d_cw, thg, phg = reconstruct_3d_pattern(vertSlice, theta, horizSlice, phi, method='CrossWeighted')
    # plot_3d_pattern(pattern3d_cw, thg, phg)
