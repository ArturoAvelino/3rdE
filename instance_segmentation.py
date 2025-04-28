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

plt.figure(figsize=(10, 10))
plt.imshow(image_np / 255)
plt.axis('off')
# plt.title("Original image without background")
# save_fig("image_no_background_check", tight_layout=False)
save_fig("image_no_background_check_no_margins", tight_layout=True)
# plt.show()
