# Tests using image segmentation

# k-means

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

filename = "image_test_1.png"
filepath = IMAGES_PATH / filename

# Upload the image:
image_np = np.asarray(Image.open(filepath))
print(image_np.shape)
#out (1774, 1774, 3)

# Reshape the array to get a list of the RGB colors
X = image_np.reshape(-1, 3)

#TODO: Replace one of the clusters of colors found by k-means by another color, just to play and to gain control in changing the colors. The actual goal will be to remove the background color from the images I'm going to work on.
