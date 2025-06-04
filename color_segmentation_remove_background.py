# Color segmentation using unsupervised machine-learning / clustering, to
# remove the background color of each image

from utils.figure_saving_utils import IMAGES_PATH, save_fig
from pathlib import Path

filename = Path("capt0044.jpg")
filepath = IMAGES_PATH / filename

from utils.rgb_scatter_plotter import create_rgb_scatter_plot, create_cluster_scatter_plot
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

plt.figure(figsize=(10, 10))
plt.imshow(image_np / 255)
plt.axis('off')
plt.title("Original image - No clustering")
save_fig("image_original_no_clustering", tight_layout=False)
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
save_fig("3D_scatter_plot_data_row", tight_layout=False)
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
fig, ax = create_rgb_scatter_plot(X_scale, xyz_limits=[0,1])
save_fig("3D_scatter_data_scaled_minmax", tight_layout=False)
plt.show()

# ========================================================60
# Cluster the RGB colors using k-means, for one given number of clusters.

num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(X_scale)

# print(kmeans.cluster_centers_) # Using minmax (0,1) scaled data as input

# Unscale the `kmeans.cluster_centers_` values to the original RGB scale
kmeans_centers_unscaled = rgb_min_max_scaler.inverse_transform(kmeans.cluster_centers_)

# print(kmeans_centers_unscaled)


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
save_fig("3D_scatter_plot_with_clusters", tight_layout=False)
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
save_fig(f"image_{num_clusters}_clusters", tight_layout=False)
# plt.show()

# ========================================================60
# Remove the background colors

# Create a new array where the RGB values (first three columns) are set to
# 255 when the cluster value (fourth column) is not 2.

# Create a copy of X_with_clusters to avoid modifying the original array
modified_array = X_with_clusters.copy()

#
# Create a mask for rows where the cluster value is the ones I want to remove.
mask = np.isin(modified_array[:, 3], [0, 4])

# Set RGB values to 255 where mask is True
modified_array[mask, 0:3] = 255

# print(modified_array[:5])

# Reshape to image dimensions (excluding the cluster column)
modified_image = modified_array[:, 0:3].reshape(image_np.shape)

# print(modified_image[:1])

# Plot the modified image.
plt.figure(figsize=(10, 10))
plt.imshow(modified_image / 255)
plt.axis('off')
save_fig(f"{filename.stem}_no_bkgd", tight_layout=False)
plt.title("Image with background color removed")
save_fig(f"{filename.stem}_no_bkgd_with_margins", tight_layout=False)
# plt.show()
