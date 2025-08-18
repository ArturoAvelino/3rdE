# Color segmentation using unsupervised machine-learning / clustering, to
# remove the background color of each image

from autosegmentation.figure_saving_utils import IMAGES_PATH, save_fig
from pathlib import Path

filename = Path("capt0044.jpg")
filepath = IMAGES_PATH / filename

from autosegmentation.rgb_scatter_plotter import create_rgb_scatter_plot, create_cluster_scatter_plot
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Upload the image:
image_np = np.asarray(Image.open(filepath))
# print(image_np.shape)

# print(image_np[:1])

# --------------------------30
# Plot the original image to check that it is correctly processed by the code
# and also to easily compare with the other processed images that this code
# produces.

plt.figure(figsize=(10, 6))
plt.imshow(image_np / 255)
plt.axis('off')
#old save_fig(f"{filename.stem}_original")
plt.title("Original image - No clustering")
save_fig(f"{filename.stem}_original_with_margins")
# plt.show()

# --------------------------30
# Reshape the array to subtract and get a list of the RGB colors. The X
# variable is a 2D array with one row per pixel, and three columns for the
# RGB values. The "X" variable only contains the RGB values.
# - The `-1` tells numpy to automatically calculate the first dimension
# - The `3` preserves the RGB channels in the second dimension
# - The resulting shape will be (1774*1774, 3) = (3147076, 3)
X = image_np.reshape(-1, 3)

# print(X.shape)

# print(X[:5])

# --------------------------30
# Create a 3D scatter plot of RGB colors of the original image.

# Scatter 3D plot of the raw RGB data
fig, ax = create_rgb_scatter_plot(X)
save_fig("3D_scatter_plot_data_row")
# plt.show()

# --------------------------------------------------------60
# Feature scaling the RBG values.

# Min-max scaling

from sklearn.preprocessing import MinMaxScaler

rgb_min_max_scaler = MinMaxScaler(feature_range=(0,1))
X_scale = rgb_min_max_scaler.fit_transform(X)

# print(X_scale.shape)

# print(X_scale[:5])
# Minmax to (0,1)

# 3D scatter plot of scaled RGB colors.
# fig, ax = create_rgb_scatter_plot(X_scale, xyz_limits=[0,1])
# save_fig("3D_scatter_data_scaled_minmax")
# plt.show()

# ========================================================60
# Cluster the RGB colors using k-means, for one given number of clusters.

num_clusters = 5

# Initial cluster centers. The values are scaled to (0,1).
if num_clusters == 5:
    kmeans_init_centers = np.asarray(
        [[0.308, 0.545, 0.753],
         [0.528, 0.448, 0.303],
         [0.725, 0.728, 0.633],
         [0.173, 0.112, 0.075],
         [0.455, 0.612, 0.745]]
    )

kmeans = KMeans(n_clusters=num_clusters, init=kmeans_init_centers,
                random_state=42).fit(X_scale)

print(kmeans.cluster_centers_) # Using minmax (0,1) scaled data as input
#out [[0.30878605 0.54503053 0.75334311]
#out  [0.52875339 0.44859306 0.30302907]
#out  [0.72518628 0.72811655 0.63300725]
#out  [0.17311289 0.11289412 0.07501406]
#out  [0.45567637 0.61260482 0.74593946]]

# Unscale the `kmeans.cluster_centers_` values to the original RGB scale
kmeans_centers_unscaled = rgb_min_max_scaler.inverse_transform(kmeans.cluster_centers_)

print(kmeans_centers_unscaled)
#out [[ 79.49107931 130.62720454 189.8424633 ]
#out  [131.84330787 107.86796212  76.36332492]
#out  [178.59433574 173.83550631 159.51782587]
#out  [ 47.20086737  28.64301149  18.90354355]
#out  [114.45097666 146.57473714 187.97674488]]

# --------------------------30
# Create a `X_with_clusters` array, using the first
# 3 values of each row as the x,y,z values, and the 4th value for the color
# of the data points in the scatter plot.

# Add to "X" a 4th column containing the cluster index for each pixel.
X_with_clusters = np.column_stack((X, kmeans.labels_))

# print(X_with_clusters.shape)  # Should show (3147076, 4)

# print(X_with_clusters[:5])    # Show first 5 rows as example

# --------------------------------------------------------60
# Inspect how well the clustering has been done

# Create a 3D scatter plot of the `X_with_clusters` array.
fig, ax = create_cluster_scatter_plot(X_with_clusters)
save_fig("3D_scatter_plot_with_clusters")
# plt.show()

# --------------------------30
# Plot the original image but with clustered colors

# Creates a segmented_img array with the nearest cluster center for each
# pixel (mean color of its cluster) as its RGB value. Replace each pixel’s
# RGB numbers with the average RGB number (cluster center) for that
# pixel.
segmented_img = kmeans_centers_unscaled[kmeans.labels_]

# print(segmented_img.shape)

# print("segmented_img[:2]:\n")
# print(segmented_img[:2])

# Reshape this array to the original image shape.
segmented_img = segmented_img.reshape(image_np.shape)

# print(segmented_img.shape)

# print("segmented_img reshaped:\n")
# print(segmented_img[:2])

# Plot the clustered image.
plt.figure(figsize=(10, 10))
plt.imshow(segmented_img / 255)
plt.axis('off')
plt.title(f"Segmented image in {num_clusters} clusters")
save_fig(f"image_{num_clusters}_clusters")
# plt.show()

# ========================================================60
# Remove the background colors

# Create a new array where the RGB values (first three columns) are set to
# 255 when the cluster value (fourth column) is not 2.

# Create a copy of X_with_clusters to avoid modifying the original array
modified_array = X_with_clusters.copy()

# Create a mask for rows where the cluster value is the ones I want to remove.
mask = np.isin(modified_array[:, 3], [0, 4]) # when "num_clusters = 4"

# Set RGB values to 255 where mask is True
modified_array[mask, 0:3] = 255

# print(modified_array[:5])

# Reshape to image dimensions (excluding the cluster column)
modified_image = modified_array[:, 0:3].reshape(image_np.shape)

# print(modified_image[:1])

# --------------------------------------------------------60
# Plot the image with background color removed

# Plot with margins like the previous output images
plt.figure(figsize=(10, 6))
plt.imshow(modified_image / 255)
plt.axis('off')
plt.title("Image with background color removed")
save_fig(f"{filename.stem}_no_bkgd_with_margins")
# plt.show()


# Plot without margins and the same pixel size as the original input image
def save_image_same_size(image_data, output_path, output_name, extension="png",
                         add_title=None):
    """
    Save an image maintaining the same dimensions as the input image data.

    Parameters:
    -----------
    image_data : numpy.ndarray
        The input image data with shape (height, width, channels)
    output_path : str or Path
        Directory path where the image will be saved
    output_name : str
        Name of the output file (without extension)
    extension : str, optional
        File extension for the output image (default: "png")
    add_title : str, optional
        Title to add to the image (default: None)
        If provided, two versions will be saved: one without margins and one with title

    Returns:
    --------
    None
    """
    # Get the dimensions of the input image
    img_height, img_width = image_data.shape[:2]

    # Calculate the figure size in inches to match the aspect ratio
    dpi = plt.rcParams['figure.dpi']
    figsize = (img_width / dpi, img_height / dpi)

    # Create the figure with the calculated size
    plt.figure(figsize=figsize)

    # Display the image without margins
    plt.imshow(image_data / 255)
    plt.axis('off')

    # Remove padding/margins
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Ensure the output path exists
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save with tight layout and the same dimensions as input
    output_file = output_path / f"{output_name}.{extension}"
    plt.savefig(output_file,
                bbox_inches='tight',
                pad_inches=0,
                dpi=dpi)

    if add_title:
        # Add title and save the version with margins
        plt.title(add_title)
        output_file_with_title = output_path / f"{output_name}_with_margins.{extension}"
        plt.savefig(output_file_with_title)

    # Close the figure to free memory
    plt.close()

# Example usage:
save_image_same_size(
    image_data=modified_image,
    output_path=IMAGES_PATH / "outputs",
    output_name=f"{filename.stem}_no_bkgd",
    extension="png"
)