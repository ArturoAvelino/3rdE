# Color segmentation to remove the background color

from utils.figure_saving_utils import IMAGES_PATH, save_fig

filename = "image_original.png"
filepath = IMAGES_PATH / filename

from utils.rgb_scatter_plotter import create_rgb_scatter_plot, create_cluster_scatter_plot
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Upload the image:
image_np = np.asarray(Image.open(filepath))
# print(image_np.shape)
#out (1774, 1774, 3)

# print(image_np[:1])
#out [[[  2  93 177]
#out   [  2  95 179]
#out   [  2  95 179]
#out   ...
#out   [  1  94 176]
#out   [  1  90 172]
#out   [  1  90 172]]]

# (Optional) Save the array data to a text file
# with open('array_values_1.txt', 'w') as f:
#     f.write(str(image_np[:1]))

# --------------------------30
# Plot the original image to check that it is correctly processed by the code
# and also to easily compare with the other processed images that this code
# produces.

#pl plt.figure(figsize=(10, 10))
#pl plt.imshow(image_np / 255)
#pl plt.axis('off')
#pl plt.title("Original image - No clustering")
#pl save_fig("image_original_no_clustering", tight_layout=False)
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
#out (3147076, 3)

# print(X[:5])
#out [[  2  93 177]
#out  [  2  95 179]
#out  [  2  95 179]
#out  [  2  93 177]
#out  [  2  93 177]]

# --------------------------30
# Create a 3D scatter plot of RGB colors.

# Scatter plot of the raw RGB data
# fig, ax = create_rgb_scatter_plot(X)
# save_fig("3D_scatter_plot_data_row", tight_layout=False)
# plt.show()

# --------------------------------------------------------60
# Feature scaling the RBG values.

# --------------------------30
# Min-max scaling

from sklearn.preprocessing import MinMaxScaler

rgb_min_max_scaler = MinMaxScaler(feature_range=(0,1))

X_scale = rgb_min_max_scaler.fit_transform(X)

# print(X_scale.shape)
#out (3147076, 3)

# print(X_scale[:5])
# Minmax to (0,1)
#out [[0.00843882 0.37651822 0.71020408]
#out  [0.00843882 0.38461538 0.71836735]
#out  [0.00843882 0.38461538 0.71836735]
#out  [0.00843882 0.37651822 0.71020408]
#out  [0.00843882 0.37651822 0.71020408]]

# Minmax to (-1,1)
#out [[-0.98312236 -0.24696356  0.42040816]
#out  [-0.98312236 -0.23076923  0.43673469]
#out  [-0.98312236 -0.23076923  0.43673469]
#out  [-0.98312236 -0.24696356  0.42040816]
#out  [-0.98312236 -0.24696356  0.42040816]]

# 3D scatter plot of scaled RGB colors.
#pl fig, ax = create_rgb_scatter_plot(X_scale, xyz_limits=[0,1])
#pl save_fig("3D_scatter_data_scaled_minmax", tight_layout=False)
#pl plt.show()

# --------------------------30
# Standardization scaling

#c from sklearn.preprocessing import StandardScaler

#c X_scale = StandardScaler().fit_transform(X)

# print(X_scale.shape)
#out (3147076, 3)

# print(X_scale[:5])
#out [[-0.3886278  -0.63483976 -0.40989422]
#out  [-0.3886278  -0.49507547 -0.32828273]
#out  [-0.3886278  -0.49507547 -0.32828273]
#out  [-0.3886278  -0.63483976 -0.40989422]
#out  [-0.3886278  -0.63483976 -0.40989422]]

# 3D scatter plot of scaled RGB colors.
#pl fig, ax = create_rgb_scatter_plot(X_scale, xyz_limits=[-7,7])
#pl save_fig("3D_scatter_data_scaled_std", tight_layout=False)
#pl plt.show()

# ========================================================60
# Cluster the RGB colors using k-means, for one given number of clusters.

num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(X_scale)

# print(kmeans.cluster_centers_)
# Using minmax (0,1) scaled data as input
#out [[0.02849851 0.45114902 0.80280148]
#out  [0.04873553 0.30753323 0.54082359]
#out  [0.065207   0.10839564 0.16722482]
#out  [0.00797904 0.39934334 0.74267494]]

# Using the standardized data as input
#out [[ 0.35528753  0.65323557  0.50628813]
#out  [-0.40808366 -0.29847904 -0.14710305]
#out  [10.04393369 -0.80567403 -3.04937622]
#out  [ 1.11338711 -4.98331563 -5.42917336]]

# Using the raw (i.e., unscaled) data as input
#out [[  6.7428771  111.41620266 199.67297223] <-- light blue
#out  [ 11.57404477  75.91582813 135.40045584] <-- the "shadows"
#out  [ 15.39406447  26.70399306  43.90020637] <-- the "black color"
#out  [  1.89296706  98.62630945 184.93387298]] <-- light blue

# Based on the result above, the background colors correspond to
# the 0, 1 and 3 clusters, and the objects I'm interested in are in the
# "2" cluster.

# --------------------------30
# Unscale the `kmeans.cluster_centers_` values to the original RGB scale
kmeans_centers_unscaled = rgb_min_max_scaler.inverse_transform(kmeans.cluster_centers_)

# print(kmeans_centers_unscaled)
#out [[  6.75414749 111.4338081  199.68636363]
#out  [ 11.55032022  75.96070846 135.5017801 ]
#out  [ 15.45405794  26.77372311  43.97008044]
#out  [  1.89103352  98.63780482 184.95536129]]

# --------------------------30
# "kmeans.labels_" contains the index of the cluster each pixel belongs to. For
# a number of clusters equal to 4, it is a 1774x1 array of integers from 0 to 3.
# print(len(kmeans.labels_))
#out 3147076

# print(kmeans.labels_.shape)
#out (3147076,)

# print(kmeans.labels_[:5])
#out [3 3 3 3 3]

# --------------------------30
# Create a `X_with_clusters` array, using the first
# 3 values of each row as the x,y,z values, and the 4th value for the color
# of the data points in the scatter plot.

# Add to "X" a 4th column containing the cluster index for each pixel.
X_with_clusters = np.column_stack((X, kmeans.labels_))

# print(X_with_clusters.shape)  # Should show (3147076, 4)
#out (3147076, 4)

# print(X_with_clusters[:5])    # Show first 5 rows as example
#out [[  2  93 177   3]
#out  [  2  95 179   3]
#out  [  2  95 179   3]
#out  [  2  93 177   3]
#out  [  2  93 177   3]]

# --------------------------------------------------------60
# Inspect how well the clustering has been done

"""
# Create a 3D scatter plot of the `X_with_clusters` array.
fig, ax = create_cluster_scatter_plot(X_with_clusters)
save_fig("3D_scatter_plot_with_clusters", tight_layout=False)
plt.show()

# --------------------------30
# Creates a segmented_img array containing the nearest cluster center for
# each pixel (i.e., the mean color of each pixel's cluster) as its RGB value,
# it is, replace the RGB numbers of each pixel for the average RGB number (the
# center of its corresponding cluster) for that pixel.
#old segmented_img = kmeans.cluster_centers_[kmeans.labels_]
segmented_img = kmeans_centers_unscaled[kmeans.labels_]

# print(segmented_img.shape)
#out (3147076, 3)

# print("segmented_img[:2]:\n")
# print(segmented_img[:2])
#out [[  1.89103352  98.63780482 184.95536129]
#out  [  1.89103352  98.63780482 184.95536129]]

# Reshape this array to the original image shape.
segmented_img = segmented_img.reshape(image_np.shape)

# print(segmented_img.shape)
#out (1774, 1774, 3)

# print("segmented_img reshaped:\n")
# print(segmented_img[:2])
#out [[[  1.89103352  98.63780482 184.95536129]
#out   [  1.89103352  98.63780482 184.95536129]
#out   [  1.89103352  98.63780482 184.95536129]
#out   ...
#out   [  1.89103352  98.63780482 184.95536129]
#out   [  1.89103352  98.63780482 184.95536129]
#out   [  1.89103352  98.63780482 184.95536129]]
#out  [[  1.89103352  98.63780482 184.95536129]
#out   [  1.89103352  98.63780482 184.95536129]

# Plot the clustered image.
plt.figure(figsize=(10, 10))
plt.imshow(segmented_img / 255)
plt.axis('off')
plt.title(f"Segmented image in {num_clusters} clusters")
save_fig(f"image_{num_clusters}_clusters", tight_layout=False)
#pl plt.show()
"""
# --------------------------30
# Try different number of clusters and plot the resulting images.

# Watch out. This clustering is done using the *unscaled* RGB data.

#pl segmented_imgs = []
#pl n_colors = (10, 8, 6, 4, 2)
#pl for n_clusters in n_colors:
#pl     kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42).fit(X)
#pl     segmented_img = kmeans.cluster_centers_[kmeans.labels_]
#pl     segmented_imgs.append(segmented_img.reshape(image_np.shape))

#pl plt.figure(figsize=(10, 10))
#pl plt.subplots_adjust(wspace=0.05, hspace=0.1)

#pl plt.subplot(2, 3, 1)
#pl plt.imshow(image_np)
#pl plt.title("Original image")
#pl plt.axis('off')

#pl for idx, n_clusters in enumerate(n_colors):
#pl     plt.subplot(2, 3, 2 + idx)
#pl     plt.imshow(segmented_imgs[idx] / 255)
#pl     plt.title(f"{n_clusters} colors")
#pl     plt.axis('off')

#pl save_fig("image_multiple_clusters", tight_layout=False)
#plt.show()

# ========================================================60
# Remove the background colors

# Create a new array where the RGB values (first three columns) are set to
# 255 when the cluster value (fourth column) is not 2.

# Create a copy of X_with_clusters to avoid modifying the original array
modified_array = X_with_clusters.copy()

# Create a mask for rows where the cluster value (4th column) is not 2
mask = modified_array[:, 3] != 2

# Set RGB values to 255 where mask is True
modified_array[mask, 0:3] = 255

# print(modified_array[:5])
#out [[255 255 255   3]
#out  [255 255 255   3]
#out  [255 255 255   3]
#out  [255 255 255   3]
#out  [255 255 255   3]]

# Reshape to image dimensions (excluding the cluster column)
modified_image = modified_array[:, 0:3].reshape(image_np.shape)

# Plot the modified image.
plt.figure(figsize=(10, 10))
plt.imshow(modified_image / 255)
plt.axis('off')
save_fig("image_no_background_for_input_", tight_layout=False)
plt.title("Image with background color removed")
save_fig("image_no_background_with_margins", tight_layout=False)
# plt.show()

# ########################################################60

print("\nEnd of code!")