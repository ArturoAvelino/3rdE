# Instance segmentation using clustering

from utils.figure_saving_utils import IMAGES_PATH, save_fig

filename = "image_no_background_for_input.png"
filepath = IMAGES_PATH / filename

import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

# Upload the image:
image_np = np.asarray(Image.open(filepath))
# print(image_np.shape)
#out (3000, 3000, 4)

# print(image_np[:1])
#out [[[255 255 255 255]
#out   [255 255 255 255]
#out   [255 255 255 255]
#out   ...
#out   [255 255 255 255]
#out   [255 255 255 255]
#out   [255 255 255 255]]]

# --------------------------30
# Plot the original image to check that it is correctly processed by the code
# and also to easily compare with the other processed images that this code
# produces.

#pl plt.figure(figsize=(10, 10))
#pl plt.imshow(image_np / 255)
#pl plt.axis('off')
#pl save_fig("image_no_background_check", tight_layout=True)
# plt.show()

# ========================================================60
# Add the x-y values of the position of each pixel to the 3d image array

# Get the dimensions of the image
height, width = image_np.shape[:2]

# Create meshgrid for x and y coordinates
x_coords, y_coords = np.meshgrid(np.arange(height), np.arange(width),
                                 indexing='ij')

# Create a new array with 6 channels
image_with_coords = np.zeros((height, width, 6))

# Copy the original RGB values to the first 3 channels and "alpha" values to
# the 4th channel
image_with_coords[:, :, :4] = image_np

# Add x coordinates to the 5th channel
image_with_coords[:, :, 4] = x_coords

# Add y coordinates to the 6th channel
image_with_coords[:, :, 5] = y_coords

# Now image_with_coords has shape (1774, 1774, 6) where:
# - channels 0,1,2 contain the RGB values
# - channel 3 contains x coordinates (row numbers)
# - channel 4 contains y coordinates (column numbers)

# print(image_with_coords.shape)
#out (3000, 3000, 6)

# print(image_with_coords[:1])
#out [[[2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 0.000e+00]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 1.000e+00]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 2.000e+00]
#out   ...
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 2.997e+03]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 2.998e+03]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 2.999e+03]]]

# ========================================================60
# Drop all the white pixels, so I'm just left with those pixels containing
# objects.

# Create a boolean mask for rows where the first 3 values are NOT 255
# Reshape the array to 2D (all pixels x 6 features)
reshaped_image = image_with_coords.reshape(-1, 6)

# print(reshaped_image.shape)
#out (9000000, 6)

# print(reshaped_image[:5])
#out [[255. 255. 255. 255.   0.   0.]
#out  [255. 255. 255. 255.   0.   1.]
#out  [255. 255. 255. 255.   0.   2.]
#out  [255. 255. 255. 255.   0.   3.]
#out  [255. 255. 255. 255.   0.   4.]]

# Create mask where any of the first 3 values are not 255
mask = ~np.all(reshaped_image[:, :3] == 255, axis=1)

# print(mask.shape)
#out (9000000,)

# print(mask[:10])
#out [False False False False False False False False False False]

# Drop all the rows (pixels) where the first 3 values are
# 255 (white color pixels).
filtered_image = reshaped_image[mask]

# print(filtered_image.shape)
#out (119471, 6)

# print(filtered_image[:5])
#out [[ 254.  254.  254.  255.  417. 1546.]
#out  [  85.  114.  144.  255.  417. 1547.]
#out  [  66.   95.  128.  255.  417. 1548.]
#out  [  66.   93.  125.  255.  417. 1549.]
#out  [  70.   96.  127.  255.  417. 1550.]]

# print(filtered_image[:5, 4:6])
#out [[ 417. 1546.]
#out  [ 417. 1547.]
#out  [ 417. 1548.]
#out  [ 417. 1549.]
#out  [ 417. 1550.]]

# --------------------------30
# Tmp: not really needed, but I'll keep it for now.

# Reshape back to original dimensions
new_height = filtered_image.shape[0]  # Number of remaining pixels

# print(new_height)
# 119471

image_with_coords = filtered_image.reshape(new_height, 1, 6)

# print(image_with_coords.shape)
#out (119471, 1, 6)

# print(image_with_coords[:1])
#out [[[ 254.  254.  254.  255.  417. 1546.]]]

# ========================================================60
# Feature scaling

#TODO: feature scaling

# ========================================================60
# Clustering / k-means for instance segmentation

from sklearn.cluster import KMeans

num_clusters = 24
kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(filtered_image[:, 4:6])

# print(kmeans.cluster_centers_[:5])
#out [[1258.92688828  859.49274143]
#out  [2218.29268038 2374.686123  ]
#out  [1541.96963902 1863.79954578]
#out  [2352.22126984 1594.66507937]
#out  [ 456.05953533 1523.28896418]]

# Add a 7th column containing the cluster index for each pixel.
X_with_clusters = np.column_stack((filtered_image, kmeans.labels_))

# print(X_with_clusters.shape)
#out (119471, 7)

# print(X_with_clusters[:5])
#out [[ 254.  254.  254.  255.  417. 1546.    4.]
#out  [  85.  114.  144.  255.  417. 1547.    4.]
#out  [  66.   95.  128.  255.  417. 1548.    4.]
#out  [  66.   93.  125.  255.  417. 1549.    4.]
#out  [  70.   96.  127.  255.  417. 1550.    4.]]

# --------------------------------------------------------60
# Inspect how well the clustering has been done

from utils.rgb_scatter_plotter import create_cluster_scatter_plot

# Create a 3D scatter plot of the `X_with_clusters` array.
fig, ax = create_cluster_scatter_plot(X_with_clusters)
save_fig("3D_plot_with_clusters_", tight_layout=False)
plt.show()

# ########################################################60

print("\nEnd of code!")