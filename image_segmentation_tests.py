# Tests using image segmentation

# k-means

from figure_saving_utils import IMAGES_PATH, save_fig

filename = "image_test_1.png"
filepath = IMAGES_PATH / filename

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Upload the image:
image_np = np.asarray(Image.open(filepath))
#pr print(image_np.shape)
#out (1774, 1774, 3)

# Reshape the array to get a list of the RGB colors. The X variable
# is a 2D array with one row per pixel, and three columns for the RGB values.
X = image_np.reshape(-1, 3)

#pr print(X.shape)
#out (3147076, 3)

print(X[:5])
#out [[  2  93 177]
#out  [  2  95 179]
#out  [  2  95 179]
#out  [  2  93 177]
#out  [  2  93 177]]

# --------------------------30
# Create a 3D scatter plot of RGB colors.

"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot a subset of points to avoid overcrowding (every 1000th point)
sample_indices = np.arange(0, len(X), 1000)
X_sample = X[sample_indices]

# Create the scatter plot
scatter = ax.scatter(X_sample[:, 0],  # Red channel
                    X_sample[:, 1],  # Green channel
                    X_sample[:, 2],  # Blue channel
                    c=X_sample/255,   # Color points according to their RGB values
                    marker='.')

# Set labels
ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')
ax.set_title('3D Scatter Plot of RGB Values')

# Set axis limits
ax.set_xlim([0, 255])
ax.set_ylim([0, 255])
ax.set_zlim([0, 255])

save_fig(f"3D_scatter_plot_test", tight_layout=False)
#pl plt.show() # It opens an interactive 3D window.
"""

# --------------------------------------------------------60
#"""
# Cluster the RGB colors using k-means, for one given number of clusters.
num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(X)

#pr print(kmeans.cluster_centers_)
#out [[  6.7428771  111.41620266 199.67297223] <-- light blue
#out  [ 11.57404477  75.91582813 135.40045584] <-- the "shadows"
#out  [ 15.39406447  26.70399306  43.90020637] <-- the "black color"
#out  [  1.89296706  98.62630945 184.93387298]] <-- light blue

# "kmeans.labels_" contains the index of the cluster each pixel belongs to. For
# a number of clusters equal to 4, it is a 1774x1 array of integers from 0 to 3.
#pr print(len(kmeans.labels_))
#out 3147076

#pr print(kmeans.labels_.shape)
#out (3147076,)

# Add to "X" a 4th column containing the cluster index for each pixel.
X_with_clusters = np.column_stack((X, kmeans.labels_))

print(X_with_clusters.shape)  # Should show (3147076, 4)
#out (3147076, 4)

print(X_with_clusters[:5])    # Show first 5 rows as example
#out [[  2  93 177   3]
#out  [  2  95 179   3]
#out  [  2  95 179   3]
#out  [  2  93 177   3]
#out  [  2  93 177   3]]

print("Stop code here while debugging.")
print("here!")


# Creates a segmented_img array containing the nearest cluster center for
# each pixel (i.e., the mean color of each pixel's cluster). It is,
# replace the RGB numbers of each pixel for the average RGB number (the
# center of its corresponding cluster) for that pixel.
segmented_img = kmeans.cluster_centers_[kmeans.labels_]

#pr print(segmented_img.shape)
#out (3147076, 3)

# Reshape this array to the original image shape.
segmented_img = segmented_img.reshape(image_np.shape)

#pr print(segmented_img.shape)
#out (1774, 1774, 3)

print("Stop code here while debugging.")
print("here!")

plt.figure(figsize=(10, 10))
plt.imshow(segmented_img / 255)
plt.axis('off')
plt.title(f"Segmented image in {num_clusters} clusters")
save_fig(f"segmented image in {num_clusters} clusters_test", tight_layout=False)
#pl plt.show()
#"""




#TODO: Replace one of the clusters of colors found by k-means by another color, just to play and to gain control in changing the colors. The actual goal will be to remove the background color from the images I'm going to work on.

# --------------------------30
# Try different number of clusters and plot the resulting images.

segmented_imgs = []
n_colors = (10, 8, 6, 4, 2)
for n_clusters in n_colors:
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42).fit(X)
    segmented_img = kmeans.cluster_centers_[kmeans.labels_]
    segmented_imgs.append(segmented_img.reshape(image_np.shape))

plt.figure(figsize=(10, 10))
plt.subplots_adjust(wspace=0.05, hspace=0.1)

plt.subplot(2, 3, 1)
plt.imshow(image_np)
plt.title("Original image")
plt.axis('off')

for idx, n_clusters in enumerate(n_colors):
    plt.subplot(2, 3, 2 + idx)
    plt.imshow(segmented_imgs[idx] / 255)
    plt.title(f"{n_clusters} colors")
    plt.axis('off')

save_fig(f"segmented image in multiple clusters_test",
         tight_layout=False)
#pl plt.show()

# ########################################################60

print("Stop code here while debugging.")
print("here!")

print("\nEnd of code!")