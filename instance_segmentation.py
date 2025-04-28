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
# Add the x-y values of each pixel to a the 3d array

# Get the dimensions of the image
height, width = image_np.shape[:2]

# Create meshgrid for x and y coordinates
x_coords, y_coords = np.meshgrid(np.arange(height), np.arange(width),
                                 indexing='ij')

#old Create new array with 5 channels
# Create new array with 6 channels
image_with_coords = np.zeros((height, width, 6))

# Copy the original RGB values to first 3 channels and "alpha" values to 4th
# channel
image_with_coords[:, :, :4] = image_np

# Add x coordinates to 5th channel
image_with_coords[:, :, 4] = x_coords

# Add y coordinates to 6th channel
image_with_coords[:, :, 5] = y_coords

# Now image_with_coords has shape (1774, 1774, 6) where:
# - channels 0,1,2 contain the RGB values
# - channel 3 contains x coordinates (row numbers)
# - channel 4 contains y coordinates (column numbers)

# print(image_with_coords.shape)
#out (3000, 3000, 6)

print(image_with_coords[:1])
#out [[[2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 0.000e+00]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 1.000e+00]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 2.000e+00]
#out   ...
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 2.997e+03]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 2.998e+03]
#out   [2.550e+02 2.550e+02 2.550e+02 2.550e+02 0.000e+00 2.999e+03]]]



# ########################################################60

print("\nEnd of code!")