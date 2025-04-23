
# Image segmentation using clustering / k-means and DBSCAN

from figure_saving_utils import IMAGES_PATH, save_fig
import matplotlib.pyplot as plt

# ########################################################60
# Image segmentation using k.means

import urllib.request

homl3_root = "https://github.com/ageron/handson-ml3/raw/main/"
filename = "ladybug.png"
filepath = IMAGES_PATH / filename

# Download the image if it doesn't already exist:
if not filepath.is_file():
    print("Downloading", filename)
    url = f"{homl3_root}/images/unsupervised_learning/{filename}"
    urllib.request.urlretrieve(url, filepath)

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Upload the image:
image_np = np.asarray(Image.open(filepath))
#pr print(image_np.shape)
#out (533, 800, 3)

# Reshape the array to get a list of the RGB colors
X = image_np.reshape(-1, 3)

# --------------------------30
# Cluster the RGB colors using k-means, for one given number of clusters.

kmeans = KMeans(n_clusters=8, random_state=42).fit(X)

#IDEA: I think it could be interesting to create the 3D or 2D scatter plot of RBG color numbers to visualize the distribution of the colors and distinguish by eye some the number of clusters, their shapes and how far or close they are between each other.

# Creates a segmented_img array containing the nearest cluster center for
# each pixel (i.e., the mean color of each pixel's cluster). It is,
# replace the RGB numbers of each pixel for the average RGB number (the
# center of its corresponding cluster) for that pixel.
segmented_img = kmeans.cluster_centers_[kmeans.labels_]

# Reshape this array to the original image shape.
segmented_img = segmented_img.reshape(image_np.shape)

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

save_fig('image_segmentation_plot', tight_layout=False)
#pl plt.show()

# ########################################################60

print("Stop code here while debugging.")
print("here!")

print("\nEnd of code!")