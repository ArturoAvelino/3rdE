# Preeliminary script for data augmentation

# Data augmentation on a single arthropod image

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from keras_preprocessing.image import ImageDataGenerator


# Full path and name of the image file.
# filepath = "/Users/aavelino/Downloads/images/BM4_E_sandbox/crops_all_together/color/capt0033_4.png"
filepath = "/Users/aavelino/Downloads/images/BM4_E_sandbox/crops_all_together/color/capt0020_34.png"

# ========================================================60
# Upload an image
image_np = np.asarray(Image.open(filepath))

# print(image_np.shape)
#out (192, 288, 3)
#out (112, 123, 3)


# Print the shape to verify dimensions
original_shape = image_np.shape
print(f"Original image shape: {original_shape}")
#out Original image shape: (192, 288, 3)

# Plot the image to check that it is correctly uploaded
#pl plt.figure(figsize=(10,6))
#pl plt.imshow(image_np)
#pl plt.axis('off')
#pl plt.title("Original image")
#pl plt.tight_layout()
#pl plt.show()

# -------------------------------------------------
# Do data augmentation using Keras

import numpy as np
import matplotlib.pyplot as plt
from keras_preprocessing.image import ImageDataGenerator

# Vertical and horizontal shifting of the image
shifting = 0

data_gen = ImageDataGenerator(rotation_range=180,
                              width_shift_range=shifting,  # pixels
                              height_shift_range=shifting,  # pixels
                              horizontal_flip=True,
                              vertical_flip=True,
                              brightness_range=[0.5, 1.5]
                              )

# Reshape the image correctly - use the original dimensions
data_gen.fit(image_np.reshape((1,) + original_shape))

# We call the flow method to generate the new images:
data_generator = data_gen.flow(image_np.reshape((1,) + original_shape),
                             shuffle=False,
                             batch_size=1)

# print(type(data_generator))
#out <class 'keras_preprocessing.image.numpy_array_iterator.NumpyArrayIterator'>

# --------------------------30
# Prepare to use the data generator with a sklearn ML model

# The new data is an iterator, ideal for incremental learners, but our
# model expects an array-like list. We have to materialize the iterator to
# using the comprehension list.

# This step will turn the iterator into a list. The "num_augmentations" is a
# multiplier for how many sets to generate
num_augmentations = 5
image_aug = [data_generator.next() for i in range(0, num_augmentations)]

# Reshape the new images from rank 4 to its original shape of rank 2:
image_aug_reshaped = np.asarray(image_aug).reshape(num_augmentations, *original_shape)

# Create a mini-dataset using the original image + the augmented images.
# Before stacking, expand dimensions of image_np
image_np_expanded = np.expand_dims(image_np, axis=0)
# Now both arrays should have 4 dimensions
image_aug_ext = np.vstack((image_np_expanded, image_aug_reshaped))

print(image_aug_ext.shape)
#out (6, 192, 288, 3)
#out (6, 112, 123, 3)

# --------------------------30

def plot_augmented_images_mosaic(image_aug_ext, save_path=None, show_plot=False):
    """
    Plot multiple images in a mosaic layout using matplotlib and optionally save to file.

    Args:
        image_aug_ext: List or array of images to display
        save_path: Optional path where to save the plot as PNG file
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import math

    # Get the number of images
    n_images = len(image_aug_ext)

    # Calculate the grid size (trying to make it as square as possible)
    n_cols = math.ceil(math.sqrt(n_images))
    n_rows = math.ceil(n_images / n_cols)

    # Create a new figure with a reasonable size
    plt.figure(figsize=(2 * n_cols, 2 * n_rows))

    # Plot each image in the grid
    for idx, img in enumerate(image_aug_ext):
        plt.subplot(n_rows, n_cols, idx + 1)

        # Normalize the image data to [0, 1] range
        img_normalized = (img - img.min()) / (img.max() - img.min())

        plt.imshow(img_normalized, cmap='gray')
        plt.axis('off')  # Turn off axis labels

    # Adjust the layout to prevent overlap
    plt.tight_layout()

    # Save the figure if a save path is provided
    if save_path:
        plt.savefig(save_path, format='png', dpi=150, bbox_inches='tight')

    if show_plot:
        plt.show()

# --------------------------30

# Plot the original image + the augmentated data and save the plot

savefig_path = (f'/Users/aavelino/PycharmProjects/Book_HandsOnML_withTF/Github/\
3rdEd/images/09_unsupervised_learning/augmentation/test_2_capt0020_34/\
capt0020_34_aug_shift_{shifting}.png')

plot_augmented_images_mosaic(image_aug_ext, save_path=savefig_path)
plt.close()
print("Plot saved to file :)")


