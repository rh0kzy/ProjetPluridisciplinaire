import numpy as np
import pyvista as pv

# 1. Generate or load your antenna gain data
n_points_phi = 100
n_points_theta = 100
phi_angles = np.linspace(0, 2 * np.pi, n_points_phi)
theta_angles = np.linspace(0, np.pi, n_points_theta)

PHI, THETA = np.meshgrid(phi_angles, theta_angles)

gain_linear = (np.sin(THETA)**2 * np.sin(2 * PHI)**2 + 0.1) * np.sin(THETA)
gain_linear = gain_linear / np.max(gain_linear)
gain_db = 20 * np.log10(gain_linear)
gain_db[gain_db < -30] = -30

# 2. Convert spherical coordinates to Cartesian coordinates for the antenna pattern
R = 10**(gain_db / 20.0)

X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)

points = np.c_[X.flatten(), Y.flatten(), Z.flatten()]
values = gain_db.flatten()

mesh = pv.StructuredGrid(X, Y, Z)
mesh.point_data['Gain_dB'] = gain_db.flatten()
surf = mesh.extract_surface()

# 3. Create the transparent sphere with lines
max_r_pattern = np.max(R) * 1.1 # Add padding
sphere = pv.Sphere(radius=max_r_pattern, theta_resolution=20, phi_resolution=20) # Fewer points for clearer lines


# 4. Plotting with PyVista
plotter = pv.Plotter(notebook=False)

# Add the transparent sphere with wireframe style
plotter.add_mesh(sphere, color='lightgray', opacity=0.15, show_edges=True, style='wireframe')

# Add the antenna radiation pattern
plotter.add_mesh(surf,
                 scalars='Gain_dB',
                 cmap='jet',
                 opacity=0.8,
                 show_edges=False,  # Optional: Don't show edges of the radiation pattern
                 smooth_shading=True,
                 lighting=True
                )

plotter.add_scalar_bar('Gain (dB)', vertical=True, interactive=True)
plotter.add_title('3D Antenna Radiation Pattern with Reference Sphere')

# Add orientation widget (like N, S markers)
plotter.add_axes()

# plotter.show() # Original call replaced by the block below

print("Preparing to display plot...")
try:
    # Using explicit interactive mode; defaults for notebook=False are usually interactive.
    # auto_close=False is also typical for interactive mode.
    plotter.show(interactive=True, auto_close=False)
    print("Plot window should have been displayed and awaiting user interaction to close.")
except Exception as e:
    print(f"ERROR: An exception occurred while trying to display the PyVista plot:")
    # Import traceback here to print detailed error information if an exception occurs.
    import traceback
    traceback.print_exc()
    print("Plotting failed. Please check the error message above.")
else:
    # This block executes if the try block completes without raising an exception.
    print("PyVista plot window closed normally (e.g., by the user).")
finally:
    # This block always executes after the try-except-else blocks.
    print("Script execution has reached its end.")
    # If running this script by double-clicking the .py file, the console window
    # might close immediately upon script completion or error.
    # Uncomment the following line to pause the script and keep the console open
    # until you press Enter, allowing you to read any output or error messages.
    # input("Press Enter to close the console window...")