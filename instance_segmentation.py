# Instance segmentation using clustering

from utils.figure_saving_utils import IMAGES_PATH, save_fig

filename = "image_no_background_for_input.png"
filepath = IMAGES_PATH / filename

import matplotlib.pyplot as plt

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

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

print(filtered_image[:5])
#out [[ 254.  254.  254.  255.  417. 1546.]
#out  [  85.  114.  144.  255.  417. 1547.]
#out  [  66.   95.  128.  255.  417. 1548.]
#out  [  66.   93.  125.  255.  417. 1549.]
#out  [  70.   96.  127.  255.  417. 1550.]]

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

# ########################################################60

print("\nEnd of code!")