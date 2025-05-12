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

# print(image_np[:1])

# --------------------------30
# Plot the original image to check that it is correctly processed by the code
# and also to easily compare with the other processed images that this code
# produces.

plt.figure(figsize=(10, 10))
plt.imshow(image_np / 255)
plt.axis('off')
save_fig("image_no_background_check", tight_layout=True)
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
# - channel 4 contains alpha values
# - channel 5 contains x coordinates (row numbers)
# - channel 6 contains y coordinates (column numbers)

# print(image_with_coords.shape)

# print(image_with_coords[:1])

# ========================================================60
# Drop all the white pixels, so I'm just left with those pixels containing
# objects.

# Create a boolean mask for rows where the first 3 values are NOT 255
# Reshape the array to 2D (all pixels x 6 features)
reshaped_image = image_with_coords.reshape(-1, 6)

# print(reshaped_image.shape)

# print(reshaped_image[:5])

# Create mask where any of the first 3 values are not 255
mask = ~np.all(reshaped_image[:, :3] == 255, axis=1)

# print(mask.shape)

# print(mask[:10])

# Drop all the rows (pixels) where the first 3 values are
# 255 (white color pixels).
filtered_image = reshaped_image[mask]

# print(filtered_image.shape)

# print(filtered_image[:5])
#out [[ 254.  254.  254.  255.  417. 1546.]
#out  [  85.  114.  144.  255.  417. 1547.]
#out  [  66.   95.  128.  255.  417. 1548.]
#out  [  66.   93.  125.  255.  417. 1549.]
#out  [  70.   96.  127.  255.  417. 1550.]]

# print(filtered_image[:5, 4:6])

# --------------------------------------------------------60

# Clustering by simply grouping pixels that are together or closer to each other

# Optimized solution using a spatial indexing approach with scipy's KDTree,
# which is much more efficient for nearest neighbor searches

# print("I start:")

import numpy as np
from scipy.spatial import KDTree
from collections import deque
import time

def segment_image_kdtree(filtered_image, max_distance=5.0):
    start_time = time.time()

    # Get coordinates
    coords = filtered_image[:, 4:6]

    # Build KD-tree for efficient nearest neighbor searches
    tree = KDTree(coords)

    # Initialize labels array with -1 (unlabeled)
    labels = np.full(len(coords), -1)
    current_label = 0

    def bfs_labeling(start_idx, label):
        """Breadth-first search to find connected components"""
        queue = deque([start_idx])
        while queue:
            current_idx = queue.popleft()
            if labels[current_idx] != -1:
                continue

            labels[current_idx] = label

            # Find all points within max_distance
            nearby_points = tree.query_ball_point(coords[current_idx],
                                                  max_distance)

            # Add unlabeled nearby points to queue
            for idx in nearby_points:
                if labels[idx] == -1:
                    queue.append(idx)

    # Process all points
    for i in range(len(coords)):
        if labels[i] == -1:
            bfs_labeling(i, current_label)
            current_label += 1

    # Add labels as a new column
    result = np.column_stack((filtered_image, labels))

    end_time = time.time()
    print(f"Segmentation completed in {end_time - start_time:.2f} seconds")
    print(f"Found {current_label} distinct groups")

    return result

# Run the segmentation
segmented_image = segment_image_kdtree(filtered_image)

# Visualize the results
plt.figure(figsize=(12, 12))

# Create scatter plot
plt.scatter(segmented_image[:, 4], segmented_image[:, 5],  # x and y coordinates
            c=segmented_image[:, -1],  # color by label
            cmap='tab20',
            alpha=0.6,
            s=1)  # smaller point size for better visualization

plt.colorbar(label='Group Label')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Pixel Groups (KDTree-based segmentation)')
save_fig("pixel_groups_kdtree", tight_layout=True)

# ########################################################60

# print("\nEnd of code!")
