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
# - channel 4 contains alpha values
# - channel 5 contains x coordinates (row numbers)
# - channel 6 contains y coordinates (column numbers)

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
#[[ 254.  254.  254.  255.  417. 1546.]
# [  85.  114.  144.  255.  417. 1547.]
# [  66.   95.  128.  255.  417. 1548.]
# [  66.   93.  125.  255.  417. 1549.]
# [  70.   96.  127.  255.  417. 1550.]]

# print(filtered_image[:5, 4:6])
#out [[ 417. 1546.]
#out  [ 417. 1547.]
#out  [ 417. 1548.]
#out  [ 417. 1549.]
#out  [ 417. 1550.]]

# ========================================================60
#tmp # Clustering by simply choosing pixels that are together.

#tmp # Create a mask for consecutive rows where 6th values are equal or differ by 1
#tmp mask = np.zeros(filtered_image.shape[0], dtype=bool)
#tmp
#tmp # Compare 6th value (index 5) of consecutive rows
#tmp for i in range(filtered_image.shape[0] - 1):
#tmp     current_value = filtered_image[i, 5]
#tmp
#tmp     for j in range(filtered_image.shape[0] - 1):
#tmp         next_value = filtered_image[i + 1 + j, 5]
#tmp
#tmp         # Check if values are equal or differ by 1
#tmp         if (current_value == next_value or
#tmp                 current_value == next_value + 1 or
#tmp                 current_value == next_value - 1):
#tmp             mask[i] = True
#tmp
#tmp print("Number of matching consecutive rows:", np.sum(mask))

#tmp # --------------------------------------------------------60

#tmp # Create a mask for consecutive rows where both 5th and 6th values are equal or differ by 1
#tmp
#tmp mask = np.zeros(filtered_image.shape[0], dtype=bool)
#tmp
#tmp # Compare both 5th and 6th values (indices 4 and 5) of consecutive rows
#tmp for i in range(filtered_image.shape[0] - 1):
#tmp     current_value_5th = filtered_image[i, 4]
#tmp     next_value_5th = filtered_image[i + 1, 4]
#tmp     current_value_6th = filtered_image[i, 5]
#tmp     next_value_6th = filtered_image[i + 1, 5]
#tmp
#tmp     # Check if both 5th and 6th values are equal or differ by 1
#tmp     fifth_value_condition = (current_value_5th == next_value_5th or
#tmp                              current_value_5th == next_value_5th + 1 or
#tmp                              current_value_5th == next_value_5th - 1)
#tmp
#tmp     sixth_value_condition = (current_value_6th == next_value_6th or
#tmp                              current_value_6th == next_value_6th + 1 or
#tmp                              current_value_6th == next_value_6th - 1)
#tmp
#tmp     # Set mask to True only if both conditions are met
#tmp     if fifth_value_condition and sixth_value_condition:
#tmp         mask[i] = True
#tmp
#tmp print("Number of matching consecutive rows:", np.sum(mask))
#tmp #out Number of matching consecutive rows: 232594

#tmp # --------------------------------------------------------60

#tmp # Create a mask for consecutive rows where both 5th and 6th values are equal or differ by 1
#tmp
#tmp mask = np.zeros(filtered_image.shape[0], dtype=bool)
#tmp print(mask.shape)
#tmp #out (252349,)
#tmp
#tmp # Compare rows
#tmp for i in range(filtered_image.shape[0] - 1):
#tmp     # Skip if this row was already processed
#tmp     if mask[i]:
#tmp         continue
#tmp
#tmp     current_value_5th = filtered_image[i, 4]
#tmp     current_value_6th = filtered_image[i, 5]
#tmp
#tmp     # Compare current row with all subsequent rows until condition is false
#tmp     for j in range(i + 1, filtered_image.shape[0]):
#tmp         next_value_5th = filtered_image[j, 4]
#tmp         next_value_6th = filtered_image[j, 5]
#tmp
#tmp         # Check if both 5th and 6th values are equal or differ by 1
#tmp         fifth_value_condition = (current_value_5th == next_value_5th or
#tmp                                  current_value_5th == next_value_5th + 1 or
#tmp                                  current_value_5th == next_value_5th - 1)
#tmp
#tmp         sixth_value_condition = (current_value_6th == next_value_6th or
#tmp                                  current_value_6th == next_value_6th + 1 or
#tmp                                  current_value_6th == next_value_6th - 1)
#tmp
#tmp         # If both conditions are met, mark this pair of rows
#tmp         if fifth_value_condition and sixth_value_condition:
#tmp             mask[i] = True
#tmp             mask[j] = True
#tmp         else:
#tmp             # If condition is not met, stop checking further rows for current i
#tmp             break
#tmp
#tmp print("Number of rows that meet the conditions:", np.sum(mask))
#tmp #out Number of rows that meet the conditions: 242732

#tmp # --------------------------------------------------------60

#old # Mark and label connected non-white pixels: a solution that uses a
#old # distance-based approach to group pixels
#old
#old import numpy as np
#old from scipy.spatial.distance import pdist, squareform
#old from sklearn.preprocessing import LabelEncoder
#old
#old
#old # Function to calculate Euclidean distance between two points
#old def euclidean_distance(p1, p2):
#old     return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
#old
#old
#old # Get the x,y coordinates of non-white pixels
#old coords = filtered_image[:, 4:6]  # columns 4 and 5 contain x,y coordinates
#old
#old # Initialize labels array with -1 (unlabeled)
#old labels = np.full(filtered_image.shape[0], -1)
#old
#old # Current label counter
#old current_label = 0
#old
#old # For each unlabeled point
#old for i in range(len(coords)):
#old     if labels[i] == -1:  # If point is not labeled yet
#old         # Start a new group with this point
#old         labels[i] = current_label
#old
#old         # Check all other unlabeled points
#old         for j in range(len(coords)):
#old             if labels[j] == -1:  # Only check unlabeled points
#old                 # Calculate distance between points
#old                 dist = euclidean_distance(coords[i], coords[j])
#old
#old                 # If distance is less than or equal to 5 pixels
#old                 if dist <= 5:
#old                     labels[j] = current_label
#old
#old         current_label += 1
#old
#old # Add labels as a new column to filtered_image
#old filtered_image = np.column_stack((filtered_image, labels))
#old
#old # Print some statistics
#old print(f"Number of different groups found: {len(np.unique(labels))}")
#old print(f"Shape of filtered_image after adding labels: {filtered_image.shape}")


#old # --------------------------------------------------------60

#old # Clustering by grouping pixels that are together or closer to each other

#old # Optimized solution using a spatial indexing approach with scipy's KDTree,
#old # which is much more efficient for nearest neighbor searches
#old
#old import numpy as np
#old from scipy.spatial import KDTree
#old from collections import deque
#old import time
#old
#old
#old def segment_image_kdtree(filtered_image, max_distance=5.0):
#old     start_time = time.time()
#old
#old     # Get coordinates
#old     coords = filtered_image[:, 4:6]
#old
#old     # Build KD-tree for efficient nearest neighbor searches
#old     tree = KDTree(coords)
#old
#old     # Initialize labels array with -1 (unlabeled)
#old     labels = np.full(len(coords), -1)
#old     current_label = 0
#old
#old     def bfs_labeling(start_idx, label):
#old         # Breadth-first search to find connected components
#old         queue = deque([start_idx])
#old         while queue:
#old             current_idx = queue.popleft()
#old             if labels[current_idx] != -1:
#old                 continue
#old
#old             labels[current_idx] = label
#old
#old             # Find all points within max_distance
#old             nearby_points = tree.query_ball_point(coords[current_idx],
#old                                                   max_distance)
#old
#old             # Add unlabeled nearby points to queue
#old             for idx in nearby_points:
#old                 if labels[idx] == -1:
#old                     queue.append(idx)
#old
#old     # Process all points
#old     for i in range(len(coords)):
#old         if labels[i] == -1:
#old             bfs_labeling(i, current_label)
#old             current_label += 1
#old
#old     # Add labels as a new column
#old     result = np.column_stack((filtered_image, labels))
#old
#old     end_time = time.time()
#old     print(f"Segmentation completed in {end_time - start_time:.2f} seconds")
#old     print(f"Found {current_label} distinct groups")
#old
#old     return result
#old
#old
#old # Run the segmentation
#old segmented_image = segment_image_kdtree(filtered_image)
#old print(segmented_image.shape)
#old #out (252349, 7)
#old
#old # print(segmented_image[:10])
#old #out [[240. 244. 248. 255. 740. 946.   0.]
#old #out  [155. 179. 206. 255. 740. 947.   0.]
#old #out  [130. 158. 191. 255. 740. 948.   0.]
#old #out  [135. 161. 190. 255. 740. 949.   0.]
#old #out  [138. 162. 188. 255. 740. 950.   0.]
#old #out  [140. 163. 188. 255. 740. 951.   0.]
#old #out  [142. 164. 189. 255. 740. 952.   0.]
#old #out  [142. 165. 190. 255. 740. 953.   0.]
#old #out  [137. 160. 187. 255. 740. 954.   0.]
#old #out  [131. 156. 186. 255. 740. 955.   0.]]
#old
#old print(segmented_image[-10:])
#old #out [[  56.   37.   30.  255. 2289. 1977. 1211.]
#old #out  [  65.   49.   36.  255. 2289. 1978. 1211.]
#old #out  [  68.   62.   49.  255. 2289. 1979. 1211.]
#old #out  [  75.   87.   86.  255. 2289. 1980. 1211.]
#old #out  [ 219.  223.  226.  255. 2289. 1981. 1211.]
#old #out  [ 250.  251.  252.  255. 2289. 1983. 1211.]
#old #out  [ 214.  224.  236.  255. 2289. 1984. 1211.]
#old #out  [ 215.  223.  237.  255. 2289. 2265. 1220.]
#old #out  [ 168.  186.  216.  255. 2289. 2266. 1220.]
#old #out  [ 245.  247.  250.  255. 2289. 2267. 1220.]]
#old
#old # Visualize the results
#old plt.figure(figsize=(12, 12))
#old
#old # Create scatter plot
#old plt.scatter(segmented_image[:, 4], segmented_image[:, 5],  # x and y coordinates
#old             c=segmented_image[:, -1],  # color by label
#old             cmap='tab20',
#old             alpha=0.6,
#old             s=1)  # smaller point size for better visualization
#old
#old plt.colorbar(label='Group Label')
#old plt.xlabel('X coordinate')
#old plt.ylabel('Y coordinate')
#old plt.title('Pixel Groups (KDTree-based segmentation)')
#old save_fig("pixel_groups_kdtree", tight_layout=True)

#old # --------------------------------------------------------60

#may print("I start:")
#may
#may import numpy as np
#may from scipy.spatial import KDTree
#may from collections import deque
#may import time
#may
#may
#may def segment_image_kdtree(filtered_image, max_distance=5.0, min_pixels=100, box_size=10):
#may     start_time = time.time()
#may
#may     # Get coordinates
#may     coords = filtered_image[:, 4:6]
#may
#may     # Build KD-tree for efficient nearest neighbor searches
#may     tree = KDTree(coords)
#may
#may     # Initialize labels array with -1 (unlabeled)
#may     labels = np.full(len(coords), -1)
#may     current_label = 0
#may
#may     # Dictionary to store pixels for each label
#may     group_pixels = {}
#may
#may     def bfs_labeling(start_idx, label):
#may         """Breadth-first search to find connected components"""
#may         pixels_in_group = []  # Store coordinates for this group
#may         queue = deque([start_idx])
#may
#may         while queue:
#may             current_idx = queue.popleft()
#may             if labels[current_idx] != -1:
#may                 continue
#may
#may             labels[current_idx] = label
#may             pixels_in_group.append(coords[current_idx])
#may
#may             # Find all points within max_distance
#may             nearby_points = tree.query_ball_point(coords[current_idx],
#may                                                   max_distance)
#may
#may             # Add unlabeled nearby points to queue
#may             for idx in nearby_points:
#may                 if labels[idx] == -1:
#may                     queue.append(idx)
#may
#may         return np.array(pixels_in_group)
#may
#may     # Process all points
#may     for i in range(len(coords)):
#may         if labels[i] == -1:
#may             group_pixels[current_label] = bfs_labeling(i, current_label)
#may             current_label += 1
#may
#may     # Filter groups based on size and bounding box
#may     valid_labels = set()
#may     for label, pixels in group_pixels.items():
#may         if len(pixels) >= min_pixels:  # Check minimum number of pixels
#may             # Calculate bounding box
#may             min_x, min_y = np.min(pixels, axis=0)
#may             max_x, max_y = np.max(pixels, axis=0)
#may             width = max_x - min_x
#may             height = max_y - min_y
#may
#may             # Check if bounding box is within size limits
#may             if width <= box_size and height <= box_size:
#may                 valid_labels.add(label)
#may
#may     # Create new labels array with only valid groups
#may     final_labels = np.full(len(coords), -1)
#may     new_label = 0
#may
#may     # Relabel valid groups with consecutive numbers
#may     label_mapping = {}
#may     for old_label in valid_labels:
#may         label_mapping[old_label] = new_label
#may         mask = (labels == old_label)
#may         final_labels[mask] = new_label
#may         new_label += 1
#may
#may     # Add final labels as a new column
#may     result = np.column_stack((filtered_image, final_labels))
#may
#may     end_time = time.time()
#may     print(f"Segmentation completed in {end_time - start_time:.2f} seconds")
#may     print(f"Found {new_label} valid groups out of {current_label} total groups")
#may
#may     return result
#may
#may # Run the segmentation
#may segmented_image = segment_image_kdtree(filtered_image,
#may                                        max_distance=5.0,
#may                                        min_pixels=100,
#may                                        box_size=10)
#may
#may # Visualize the results
#may plt.figure(figsize=(12, 12))
#may
#may # Create scatter plot only for valid groups (labels >= 0)
#may valid_points = segmented_image[segmented_image[:, -1] >= 0]
#may plt.scatter(valid_points[:, 4], valid_points[:, 5],  # x and y coordinates
#may             c=valid_points[:, -1],  # color by label
#may             cmap='tab20',
#may             alpha=0.6,
#may             s=1)  # smaller point size for better visualization
#may
#may plt.colorbar(label='Group Label')
#may plt.xlabel('X coordinate')
#may plt.ylabel('Y coordinate')
#may plt.title('Filtered Pixel Groups (minimum 400 pixels in 20x20 box)')
#may save_fig("pixel_groups_kdtree_filtered", tight_layout=True)
#may
#may # Print some statistics about the groups
#may valid_labels = segmented_image[segmented_image[:, -1] >= 0][:, -1]
#may unique_labels = np.unique(valid_labels)
#may print("\nStatistics for valid groups:")
#may for label in unique_labels:
#may     group_pixels = segmented_image[segmented_image[:, -1] == label]
#may     min_x, min_y = np.min(group_pixels[:, 4:6], axis=0)
#may     max_x, max_y = np.max(group_pixels[:, 4:6], axis=0)
#may     width = max_x - min_x
#may     height = max_y - min_y
#may     print(f"\nGroup {int(label)}:")
#may     print(f"Number of pixels: {len(group_pixels)}")
#may     print(f"Bounding box size: {width:.1f} x {height:.1f} pixels")

#may # --------------------------------------------------------60

# Clustering by grouping pixels that are together or closer to each other

# Optimized solution using a spatial indexing approach with scipy's KDTree,
# which is much more efficient for nearest neighbor searches.
# Ignore groups with less than a given amount of pixels.

import numpy as np
from scipy.spatial import KDTree
from collections import deque
import time


def segment_image_kdtree(filtered_image, max_distance=5.0, min_pixels=400):
    start_time = time.time()

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

            # Add unlabeled nearby points to queue
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
max_distance=4.0
min_pixels=500
segmented_image = segment_image_kdtree(filtered_image,
                                       max_distance=max_distance,
                                       min_pixels=min_pixels)
#out Segmentation completed in 5.52 seconds
#out Found 118 valid groups (with ≥400 pixels) out of 1225 total groups

# print(segmented_image[:10])
#out [[240. 244. 248. 255. 740. 946.  -1.]
#out  [155. 179. 206. 255. 740. 947.  -1.]
#out  [130. 158. 191. 255. 740. 948.  -1.]
#out  [135. 161. 190. 255. 740. 949.  -1.]
#out  [138. 162. 188. 255. 740. 950.  -1.]
#out  [140. 163. 188. 255. 740. 951.  -1.]
#out  [142. 164. 189. 255. 740. 952.  -1.]
#out  [142. 165. 190. 255. 740. 953.  -1.]
#out  [137. 160. 187. 255. 740. 954.  -1.]
#out  [131. 156. 186. 255. 740. 955.  -1.]]

# print(segmented_image[-10:])
#out [[ 5.600e+01  3.700e+01  3.000e+01  2.550e+02  2.289e+03  1.977e+03
#out   -1.000e+00]
#out  [ 6.500e+01  4.900e+01  3.600e+01  2.550e+02  2.289e+03  1.978e+03
#out   -1.000e+00]
#out  [ 6.800e+01  6.200e+01  4.900e+01  2.550e+02  2.289e+03  1.979e+03
#out   -1.000e+00]
#out  [ 7.500e+01  8.700e+01  8.600e+01  2.550e+02  2.289e+03  1.980e+03
#out   -1.000e+00]
#out  [ 2.190e+02  2.230e+02  2.260e+02  2.550e+02  2.289e+03  1.981e+03
#out   -1.000e+00]
#out  [ 2.500e+02  2.510e+02  2.520e+02  2.550e+02  2.289e+03  1.983e+03
#out   -1.000e+00]
#out  [ 2.140e+02  2.240e+02  2.360e+02  2.550e+02  2.289e+03  1.984e+03
#out   -1.000e+00]
#out  [ 2.150e+02  2.230e+02  2.370e+02  2.550e+02  2.289e+03  2.265e+03
#out   -1.000e+00]
#out  [ 1.680e+02  1.860e+02  2.160e+02  2.550e+02  2.289e+03  2.266e+03
#out   -1.000e+00]
#out  [ 2.450e+02  2.470e+02  2.500e+02  2.550e+02  2.289e+03  2.267e+03
#out   -1.000e+00]]

# Visualize the results
plt.figure(figsize=(12, 12))

# Create scatter plot only for valid groups (labels >= 0)
valid_points = segmented_image[segmented_image[:, -1] >= 0]
plt.scatter(valid_points[:, 4], valid_points[:, 5],  # x and y coordinates
            c=valid_points[:, -1],  # color by label
            cmap='tab20',
            alpha=0.6,
            s=1)  # smaller point size for better visualization

plt.colorbar(label='Group Label')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title(f'Filtered Pixel Groups (minimum {min_pixels} pixels, distance <= {max_distance} pixels)')
save_fig("pixel_groups_kdtree_filtered", tight_layout=True)

# Print statistics about the groups
valid_labels = segmented_image[segmented_image[:, -1] >= 0][:, -1]
unique_labels = np.unique(valid_labels)
print("\nStatistics for valid groups:")
for label in unique_labels:
    group_pixels = segmented_image[segmented_image[:, -1] == label]
    print(f"\nGroup {int(label)}:")
    print(f"Number of pixels: {len(group_pixels)}")

# ########################################################60

print("\nEnd of code!")
