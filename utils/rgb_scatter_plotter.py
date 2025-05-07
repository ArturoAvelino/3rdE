import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting


def create_rgb_scatter_plot(X, sample_step=1000, figsize=(10, 10),
                            xyz_limits=[0,255]):
    """
    Create a 3D scatter plot of RGB values
    
    Parameters:
    -----------
    X : numpy.ndarray
        Array of RGB values with shape (n_samples, 3)
    sample_step : int
        Step size for sampling points to avoid overcrowding
    figsize : tuple
        Figure size as (width, height)
        
    Returns:
    --------
    fig, ax : tuple
        Matplotlib figure and axis objects
    """
    # Create a 3D scatter plot
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    # Sample points to avoid overcrowding
    sample_indices = np.arange(0, len(X), sample_step)
    X_sample = X[sample_indices]

    # Create the scatter plot
    scatter = ax.scatter(X_sample[:, 0],  # Red channel
                        X_sample[:, 1],  # Green channel
                        X_sample[:, 2],  # Blue channel
                        c=X_sample/255, # Color points according to their RGB values
                        marker='.')

    # Set labels and title
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_title('3D Scatter Plot of RGB Values')

    # Set axis limits
    ax.set_xlim(xyz_limits)
    ax.set_ylim(xyz_limits)
    ax.set_zlim(xyz_limits)
    
    return fig, ax


def create_cluster_scatter_plot(X_with_clusters, sample_step=1000,
                                figsize=(10, 10), xyz_limits=[0,255]):
    """
    Create a 3D scatter plot of RGB values colored by cluster.
    
    Parameters:
    -----------
    X_with_clusters : numpy.ndarray
        Array with shape (n_samples, 4) where the first 3 columns are RGB values
        and the 4th column contains cluster labels
    sample_step : int
        Step size for sampling points to avoid overcrowding
    figsize : tuple
        Figure size as (width, height)
        
    Returns:
    --------
    fig, ax : tuple
        Matplotlib figure and axis objects
    """
    # Create a 3D scatter plot
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    # Sample points to avoid overcrowding
    sample_indices = np.arange(0, len(X_with_clusters), sample_step)
    X_sample = X_with_clusters[sample_indices]

    # Create the scatter plot
    scatter = ax.scatter(X_sample[:, 0],    # Red channel
                        X_sample[:, 1],    # Green channel
                        X_sample[:, 2],    # Blue channel
                        c=X_sample[:, 3],  # color based on cluster labels
                        cmap='viridis',    # color map
                        marker='.')

    # Set labels and title
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_title('3D Scatter Plot of RGB Values with Cluster Colors')

    # Set axis limits
    ax.set_xlim(xyz_limits)
    ax.set_ylim(xyz_limits)
    ax.set_zlim(xyz_limits)

    # Add a color bar
    plt.colorbar(scatter, label='Cluster')
    
    return fig, ax

