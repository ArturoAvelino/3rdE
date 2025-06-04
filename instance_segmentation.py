# Instance segmentation  by grouping pixels that are together or closer to
# each other

from utils.figure_saving_utils import IMAGES_PATH, save_fig
from pathlib import Path

sample_name = "BM4_E"

image_no_bkground = "capt0044_no_bkgd.png"
path_image_no_bkground = IMAGES_PATH / "outputs" / image_no_bkground

image_original = "capt0044_no_bkgd.png"
path_image_original = IMAGES_PATH / "outputs" / image_no_bkground

# image_original = "capt0044.jpg"
# path_image_original = IMAGES_PATH / image_original

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Upload the image:
image_np = np.asarray(Image.open(path_image_no_bkground))

# print(image_np.shape)
# (2000, 3000, 4)

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

# plt.figure(figsize=(10, 10))
# plt.imshow(image_np / 255)
# plt.axis('off')
# save_fig("image_no_background_check", tight_layout=True)
# # plt.show()

# ========================================================60
# Add the x-y values of the location of each pixel to the 3d image array

# Get the dimensions of the image
height, width = image_np.shape[:2]
# print(f"Image dimensions: {height} x {width}")
# Image dimensions: 2000 x 3000

# Image proportion (width/height)
image_proportion = height / width
print(f"Image proportion: {image_proportion:.2f}")
# Image proportion: 0.67

# Create meshgrid for y and x coordinates
y_coords, x_coords = np.meshgrid(np.arange(height), np.arange(width),
                                 indexing='ij')

# print(x_coords.shape)
# (2000, 3000)

# print(x_coords[:5])
#out [[   0    1    2 ... 2997 2998 2999]
#out  [   0    1    2 ... 2997 2998 2999]
#out  [   0    1    2 ... 2997 2998 2999]
#out  [   0    1    2 ... 2997 2998 2999]
#out  [   0    1    2 ... 2997 2998 2999]]

# print(y_coords.shape)
# (2000, 3000)

# print(y_coords[:5])
#out [[0 0 0 ... 0 0 0]
#out  [1 1 1 ... 1 1 1]
#out  [2 2 2 ... 2 2 2]
#out  [3 3 3 ... 3 3 3]
#out  [4 4 4 ... 4 4 4]]

# Create a new array with 6 channels
image_with_coords = np.zeros((height, width, 6))

# print(image_with_coords.shape)
# (2000, 3000, 6)

# Copy the original RGB values to the first 3 channels and the "alpha" values to
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
#out [[[2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 1.999e+03]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 1.000e+00 1.999e+03]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 2.000e+00 1.999e+03]
#out   ...
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 2.997e+03 1.999e+03]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 2.998e+03 1.999e+03]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 2.999e+03 1.999e+03]]]

# ========================================================60
# Drop all the white pixels, so I'm just left with those pixels containing
# objects.

# Create a boolean mask for rows where the first 3 values are NOT 255

# Reshape the array to 2D (all pixels x 6 features)
reshaped_image = image_with_coords.reshape(-1, 6)

# print(reshaped_image.shape)

# print(reshaped_image[:5])

# Create a mask where any of the first 3 values are not 255
mask = ~np.all(reshaped_image[:, :3] == 255, axis=1)

# print(mask.shape)

# print(mask[:10])

# Drop all the rows (pixels) where the first 3 values are
# 255 (white color pixels).
filtered_image = reshaped_image[mask]

# print(filtered_image.shape)

# print(filtered_image[:5])
# [[ 252.  252.  253.  255. 1574. 1708.]
#  [ 191.  200.  206.  255. 1575. 1708.]
#  [ 161.  170.  173.  255. 1576. 1708.]
#  [ 175.  178.  173.  255. 1577. 1708.]
#  [ 182.  180.  168.  255. 1578. 1708.]]

# print(filtered_image[-5:])
# [[ 172.  181.  199.  255. 1907.  159.]
#  [ 163.  170.  190.  255. 1908.  159.]
#  [ 163.  169.  188.  255. 1909.  159.]
#  [ 159.  168.  188.  255. 1910.  159.]
#  [ 218.  223.  230.  255. 1911.  159.]]

#[[ 254.  254.  254.  255.  417. 1546.]
# [  85.  114.  144.  255.  417. 1547.]
# [  66.   95.  128.  255.  417. 1548.]
# [  66.   93.  125.  255.  417. 1549.]
# [  70.   96.  127.  255.  417. 1550.]]

# print(filtered_image[:5, 4:6])

# ========================================================60
# Find all the group of pixels that are connected or close to each other

# Optimized solution using a spatial indexing approach with scipy's KDTree,
# which is much more efficient for nearest neighbor searches.
# Ignore groups with less than a given amount of pixels.

import numpy as np
from scipy.spatial import KDTree
from collections import deque
import time

def segment_image_kdtree(filtered_image, max_distance=5.0, min_pixels=400):
    """
    Performs image segmentation by grouping pixels that are spatially close
    to each other using KD-tree spatial indexing.

    This function implements a clustering algorithm that groups pixels based
    on their spatial proximity. It uses a KD-tree data structure for
    efficient nearest neighbor searches and breadth-first search (BFS) for
    finding connected components.

    Parameters:
    -----------
    filtered_image : numpy.ndarray
        Input image array of shape (N, 6) where N is the number of pixels and
        each row contains:
        - First 4 values: RGB and alpha values
        - Last 2 values: x and y coordinates of the pixel
    max_distance : float, optional (default=5.0)
        Maximum distance between pixels to be considered part of the same group
    min_pixels : int, optional (default=400)
        Minimum number of pixels required for a group to be considered valid

    Returns:
    --------
    numpy.ndarray
        Array of shape (N, 7) containing the original pixel data plus a label column.
        The label column (-1 for invalid groups, ≥0 for valid groups) is
        appended as the last column.

    Process:
    --------
    1. Extracts pixel coordinates and builds a KD-tree for efficient spatial searching
    2. Uses breadth-first search to find connected components (groups of nearby pixels)
    3. Labels pixels with their group ID during the BFS process
    4. Filters out groups that don't meet the minimum pixel count requirement
    5. Relabels the remaining valid groups with consecutive numbers
    6. Returns the original pixel data with an additional column for group labels

    Notes:
    ------
    - The function prints timing information and statistics about the found groups
    - Invalid groups (smaller than min_pixels) are labeled as -1 in the output
    - Valid groups are labeled with consecutive integers starting from 0
    """

    start_time = time.time()
    print("Starting segmentation...")
    # Get coordinates
    coords = filtered_image[:, 4:6]

    # Build KD-tree for efficient nearest neighbor searches
    tree = KDTree(coords)

    # Initialize labels array with -1 (unlabeled)
    labels = np.full(len(coords), -1)
    current_label = 0

    # Dictionary to store pixels for each label
    group_pixels = {}

    def bfs_labeling(start_idx, label):
        """Breadth-first search to find connected components"""
        pixels_in_group = []
        queue = deque([start_idx])

        while queue:
            current_idx = queue.popleft()
            if labels[current_idx] != -1:
                continue

            labels[current_idx] = label
            pixels_in_group.append(coords[current_idx])

            # Find all points within max_distance
            nearby_points = tree.query_ball_point(coords[current_idx],
                                                  max_distance)

            # Add unlabeled nearby points to the queue
            for idx in nearby_points:
                if labels[idx] == -1:
                    queue.append(idx)

        return np.array(pixels_in_group)

    # Process all points
    for i in range(len(coords)):
        if labels[i] == -1:
            group_pixels[current_label] = bfs_labeling(i, current_label)
            current_label += 1

    # Filter groups based on size
    valid_labels = set()
    for label, pixels in group_pixels.items():
        if len(pixels) >= min_pixels:
            valid_labels.add(label)

    # Create new labels array with only valid groups
    final_labels = np.full(len(coords), -1)
    new_label = 0

    # Relabel valid groups with consecutive numbers
    label_mapping = {}
    for old_label in valid_labels:
        label_mapping[old_label] = new_label
        mask = (labels == old_label)
        final_labels[mask] = new_label
        new_label += 1

    # Add final labels as a new column
    result = np.column_stack((filtered_image, final_labels))

    end_time = time.time()
    print(f"Segmentation completed in {end_time - start_time:.2f} seconds")
    print(
        f"Found {new_label} valid groups (with ≥{min_pixels} pixels) out of {current_label} total groups")

    return result


# Run the segmentation
max_distance = 4.0
min_pixels = 10000
segmented_image = segment_image_kdtree(filtered_image,
                                       max_distance=max_distance,
                                       min_pixels=min_pixels)

# Print all the rows of a given group
group_id = 1

print(f"Number of pixels in group {group_id}: {len(segmented_image[segmented_image[:, -1] == group_id])}")
#out Number of pixels in group 1: 12751

# print(segmented_image[segmented_image[:, -1] == group_id])
#out [[2.390e+02 2.390e+02 2.380e+02 ... 7.400e+02 2.129e+03 1.000e+00]
#out  [1.520e+02 1.520e+02 1.480e+02 ... 7.400e+02 2.130e+03 1.000e+00]
#out  [1.280e+02 1.270e+02 1.220e+02 ... 7.400e+02 2.131e+03 1.000e+00]
#out  ...
#out  [2.540e+02 2.540e+02 2.540e+02 ... 8.410e+02 2.004e+03 1.000e+00]
#out  [2.540e+02 2.540e+02 2.540e+02 ... 8.410e+02 2.005e+03 1.000e+00]
#out  [2.540e+02 2.540e+02 2.540e+02 ... 8.410e+02 2.006e+03 1.000e+00]]

# print(segmented_image[:5])
#out [[ 252.  252.  253.  255.  740. 1574.    0.]
#out  [ 191.  200.  206.  255.  740. 1575.    0.]
#out  [ 161.  170.  173.  255.  740. 1576.    0.]
#out  [ 175.  178.  173.  255.  740. 1577.    0.]
#out  [ 182.  180.  168.  255.  740. 1578.    0.]]

# print(segmented_image[-5:])
#out [[ 1.720e+02  1.810e+02  1.990e+02  2.550e+02  1.907e+03  1.590e+02 -1.000e+00]
#out  [ 1.630e+02  1.700e+02  1.900e+02  2.550e+02  1.908e+03  1.590e+02 -1.000e+00]
#out  [ 1.630e+02  1.690e+02  1.880e+02  2.550e+02  1.909e+03  1.590e+02 -1.000e+00]
#out  [ 1.590e+02  1.680e+02  1.880e+02  2.550e+02  1.910e+03  1.590e+02 -1.000e+00]
#out  [ 2.180e+02  2.230e+02  2.300e+02  2.550e+02  1.911e+03  1.590e+02 -1.000e+00]]

# Visualize the results

# Calculate figure size maintaining the image proportion
width_image = 12  # base width
# adjust height according to image proportion:
height_image = width_image * image_proportion

plt.figure(figsize=(width_image, height_image))

# Create a scatter plot only for valid groups (labels >= 0)
valid_points = segmented_image[segmented_image[:, -1] >= 0]
plt.scatter(valid_points[:, 4], valid_points[:, 5],  # x and y coordinates
            c=valid_points[:, -1],  # color by label
            cmap='tab20',
            alpha=0.6,
            s=1)  # smaller point size for better visualization

plt.colorbar(label='Group Label')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.gca().invert_yaxis()  # This makes y-axis increase downward
plt.title(f'Filtered Pixel Groups (minimum {min_pixels} pixels, distance <= {max_distance} pixels)')
save_fig("pixel_groups_kdtree_filtered", tight_layout=True)

# --------------------------------------------------------60
# Print statistics about the groups

valid_labels = segmented_image[segmented_image[:, -1] >= 0][:, -1]
unique_labels = np.unique(valid_labels)
print(f"Found {len(unique_labels)} valid groups (with ≥{min_pixels} pixels) out of {len(valid_labels)} total groups")
# Found 7 valid groups (with ≥10000 pixels) out of 157785 total groups

print("\nStatistics for valid groups:")
for label in unique_labels:
    group_pixels = segmented_image[segmented_image[:, -1] == label]
    print(f"\nGroup {int(label)}:")
    print(f"Number of pixels: {len(group_pixels)}")

# ========================================================60

from utils.bounding_box_metadata_processor import BoxAndCrop

# Example usage
processor = BoxAndCrop(
    segmented_image=segmented_image,
    path_image_original= path_image_original,
    sample_name="BM4_E",
    output_dir="/Users/aavelino/PycharmProjects/Book_HandsOnML_withTF/Github/3rdEd/images/09_unsupervised_learning/soil_fauna/BM4_E/outputs/3_crop/"
)

# Process all groups and save as PNG
processor.process_all_groups(image_format='PNG')

# Or process a specific group
# processor.process_group(group_number=1, image_format='PNG')


