import logging
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.cluster import KMeans
from typing import List, Optional, Union
import matplotlib.pyplot as plt


class ImageSegmentationProcessor:
    """
    ImageSegmentationProcessor: A class for image segmentation and background removal using K-means clustering.

    This class provides a comprehensive solution for image segmentation using color-based clustering,
    with support for background removal, visualization, and detailed analysis of color distributions.
    It implements a fluent interface (method chaining) pattern and includes optional logging capabilities.

    Key Features:
    ------------
    1. Image Processing:
     - Loads and validates RGB images
     - Performs K-means clustering on pixel colors
     - Supports background removal with configurable cluster selection
     - Creates visualizations of clustering results

    2. Data Export:
     - Saves processed images with configurable naming
     - Exports cluster centers to CSV files (with "_cluster_centers" suffix)
     - Generates 3D scatter plots of RGB color distributions

    3. Logging:
     - Optional per-image logging
     - Creates individual log files named "<image_name>_processing.log"
     - Logs all major operations and potential errors

    Usage Example:
    -------------
    ```python
    # Basic usage:

    # input_dir = Path("/Users/aavelino/PycharmProjects/Book_HandsOnML_withTF/Github/3rdEd/images/09_unsupervised_learning/soil_fauna/BM4_E/capt0044/capt0044.jpg")
    # output_dir = Path("/Users/aavelino/PycharmProjects/Book_HandsOnML_withTF/Github/3rdEd/images/09_unsupervised_learning/soil_fauna/BM4_E/capt0044/outputs/")
    processor = ImageSegmentationProcessor(image_path, output_dir)
    processor.cluster_rgb_colors(n_clusters=5)
    processor.plot_rgb_rawdata()
    processor.plot_rgb_clusters()
    processor.remove_background(background_clusters=[0, 4])

    # With custom cluster centers:
    custom_centers = np.array([
        [255, 0, 0],    # Red
        [0, 255, 0],    # Green
        [0, 0, 255],    # Blue
        [255, 255, 0],  # Yellow
        [128, 128, 128] # Gray
    ])
    processor = ImageSegmentationProcessor(
        image_path="input/image.jpg",
        output_dir="output",
        enable_logging=True,
        n_clusters=5,
        kmeans_init_centers=custom_centers
    )

    # Individual method usage
    processor.cluster_rgb_colors()  # Uses predefined settings
    processor.remove_background(background_clusters=0, output_suffix="_nobg")
    processor.plot_rgb_clusters(save=True)

    # Method chaining example
    processor.cluster_rgb_colors() \
          .remove_background(background_clusters=[0, 1]) \
          .plot_rgb_clusters(sample_step=1000)
    ```
    --------
    Initialize the image segmentation processor.

    Args:
        image_path: Path to the input image file
        output_dir: Directory where output files will be saved
        enable_logging: Whether to create a log file for this image
        n_clusters: Default number of clusters for K-means (optional)
        kmeans_init_centers: Default initial cluster centers (optional, shape: [n_clusters, 3])

    Raises:
        FileNotFoundError: If image_path doesn't exist
        NotADirectoryError: If output_dir doesn't exist or can't be created
        ValueError: If kmeans_init_centers shape doesn't match n_clusters
    """

    def __init__(self,
                 image_path: Union[str, Path],
                 output_dir: Union[str, Path],
                 enable_logging: bool = False,
                 n_clusters: Optional[int] = None,
                 kmeans_init_centers: Optional[np.ndarray] = None):

        # Convert paths to Path objects
        self.image_path = Path(image_path)
        self.output_dir = Path(output_dir)

        # Validate input image
        if not self.image_path.is_file():
            raise FileNotFoundError(f"Input image not found: {self.image_path}")

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Validate cluster parameters
        if kmeans_init_centers is not None and n_clusters is not None:
            if kmeans_init_centers.shape != (n_clusters, 3):
                raise ValueError(
                    f"kmeans_init_centers shape {kmeans_init_centers.shape} doesn't match "
                    f"expected shape ({n_clusters}, 3)"
                )

        # Store default clustering parameters
        self.default_n_clusters = n_clusters
        self.default_kmeans_init_centers = kmeans_init_centers

        # Initialize logging if enabled
        self.logger = None
        if enable_logging:
            self._setup_logging()

        # Initialize internal state
        self.image = None
        self.rgb_data = None
        self.kmeans = None
        self.cluster_labels = None
        self.cluster_centers = None
        self.kmeans_init_centers = None

        # Load and validate the image
        self._load_image()


    def _setup_logging(self) -> None:
        """Configure logging for this image processing session."""
        # Create a logger with the image name
        self.logger = logging.getLogger(self.image_path.stem)
        self.logger.setLevel(logging.INFO)

        # Create handlers
        log_file = self.output_dir / f"{self.image_path.stem}_processing.log"
        file_handler = logging.FileHandler(log_file, mode='w')
        console_handler = logging.StreamHandler()

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info(f"Started processing image: {self.image_path.name}")


    def _load_image(self) -> None:
        """
        Load and validate the input image.

        Raises:
            ValueError: If the image is not in RGB mode
        """
        self.image = Image.open(self.image_path)

        if self.image.mode != 'RGB':
            raise ValueError("Image must be in RGB mode")

        # Convert image to numpy array and reshape for clustering
        img_array = np.array(self.image)
        self.rgb_data = img_array.reshape(-1, 3)

        if self.logger:
            self.logger.info(
                f"Loaded image: {self.image_path.name} ({self.image.size[0]}x{self.image.size[1]})")

    def cluster_rgb_colors(self,
                           n_clusters: Optional[int] = None,
                           random_state: int = 42,
                           kmeans_init_centers: Optional[
                               np.ndarray] = None) -> 'ImageSegmentationProcessor':
        """
        Perform K-means clustering on the image pixels.

        Args:
            n_clusters: Number of clusters for K-means. If None, uses default from constructor or 5
            random_state: Random seed for reproducibility
            kmeans_init_centers: Initial cluster centers. If None, uses default from constructor

        Returns:
            self for method chaining

        Raises:
            ValueError: If kmeans_init_centers shape doesn't match n_clusters
        """
        # Determine n_clusters: method param -> constructor param -> default 5
        if n_clusters is None:
            n_clusters = self.default_n_clusters if self.default_n_clusters is not None else 5

        # Determine init_centers: method param -> constructor param -> auto for n_clusters=5 -> None
        if kmeans_init_centers is None:
            if self.default_kmeans_init_centers is not None:
                kmeans_init_centers = self.default_kmeans_init_centers
            elif n_clusters == 5:
                # Use hardcoded centers for backward compatibility
                kmeans_init_centers = np.asarray([
                    [79.49, 130.62, 189.84],
                    [131.84, 107.86, 76.36],
                    [178.59, 173.83, 159.51],
                    [47.20, 28.64, 18.90],
                    [114.45, 146.57, 187.97]
                ])

        # Validate init_centers if provided
        if kmeans_init_centers is not None:
            if kmeans_init_centers.shape != (n_clusters, 3):
                raise ValueError(
                    f"kmeans_init_centers shape {kmeans_init_centers.shape} doesn't match "
                    f"expected shape ({n_clusters}, 3)"
                )

        if self.logger:
            self.logger.info(
                f"Clustering RGB colors into {n_clusters} clusters")
            if kmeans_init_centers is not None:
                self.logger.info("Using provided initial cluster centers")

        # Store the init centers for potential later use
        self.kmeans_init_centers = kmeans_init_centers

        # Create KMeans object
        if kmeans_init_centers is not None:
            self.kmeans = KMeans(
                n_clusters=n_clusters,
                init=kmeans_init_centers,
                random_state=random_state
            )
        else:
            self.kmeans = KMeans(n_clusters=n_clusters,
                                 random_state=random_state)

        self.cluster_labels = self.kmeans.fit_predict(self.rgb_data)
        self.cluster_centers = self.kmeans.cluster_centers_

        # Save cluster centers
        centers_df = pd.DataFrame(
            self.cluster_centers,
            columns=['R', 'G', 'B']
        )
        csv_path = self.output_dir / f"{self.image_path.stem}_cluster_centers.csv"
        centers_df.to_csv(csv_path, index=True)

        if self.logger:
            self.logger.info(f"Saved cluster centers to {csv_path}")

        return self


    def remove_background(self,
                          background_clusters: Union[int, List[int]],
                          output_suffix: str = "_no_bkgd") -> 'ImageSegmentationProcessor':
        """
        Remove background pixels by replacing them with white color.

        Args:
            background_clusters: Cluster index or list of indices to be treated as background
            output_suffix: Custom suffix for the output image file (default: "_no_bkgd")

        Returns:
            self for method chaining

        Raises:
            ValueError: If background_clusters contains invalid cluster indices
            RuntimeError: If cluster_rgb_colors() hasn't been called yet
        """
        if self.cluster_labels is None:
            raise RuntimeError(
                "Must run 'cluster_rgb_colors()' before removing background")

        # Convert single cluster index to list
        if isinstance(background_clusters, int):
            background_clusters = [background_clusters]

        # Validate background cluster indices
        n_clusters = len(self.cluster_centers)
        max_cluster = n_clusters - 1
        for cluster in background_clusters:
            if cluster < 0 or cluster > max_cluster:
                raise ValueError(
                    f"Invalid background cluster index: {cluster}. "
                    f"Must be between 0 and {max_cluster}")

        if self.logger:
            self.logger.info(
                f"Removing background clusters: {background_clusters}")

        # Create a mask for non-background pixels
        mask = ~np.isin(self.cluster_labels, background_clusters)
        mask = mask.reshape(self.image.size[::-1])

        # Create new image with a white background (255, 255, 255)
        img_array = np.array(self.image)
        new_img = np.full_like(img_array, 255)  # Create a white background
        # new_img = np.full_like(img_array, 95)  # Create a color background
        new_img[mask] = img_array[mask]  # Copy non-background pixels

        # Save the image
        output_image = Image.fromarray(new_img)
        output_path = self.output_dir / f"{self.image_path.stem}{output_suffix}.png"
        output_image.save(output_path, format='PNG')

        if self.logger:
            self.logger.info(f"Saved background-removed image to {output_path}")

        return self

    def plot_replaced_colors_in_image(self,
                                      save: bool = True,
                                      output_suffix: str = "_segmented") -> 'ImageSegmentationProcessor':
        """
        Plot the input image with pixel colors replaced by their cluster center colors.

        This method creates a segmented version of the original image where each pixel
        is replaced with the RGB color of its assigned cluster center. This provides
        a visual representation of the image segmentation results.

        Args:
            save: Whether to save the segmented image to a file (default: True)
            output_suffix: Custom suffix for the output image file (default: "_segmented")

        Returns:
            self for method chaining

        Raises:
            RuntimeError: If cluster_rgb_colors() hasn't been called yet
        """
        if self.cluster_labels is None or self.cluster_centers is None:
            raise RuntimeError(
                "Must run 'cluster_rgb_colors()' before plotting segmented image")

        if self.logger:
            self.logger.info(
                "Creating segmented image with cluster center colors")

        # Create a segmented image by replacing each pixel with its cluster center color
        segmented_rgb_data = self.cluster_centers[self.cluster_labels]

        # Ensure cluster centers are in valid RGB range [0, 255] and convert to uint8
        segmented_rgb_data = np.clip(segmented_rgb_data, 0, 255).astype(
            np.uint8)

        # Reshape back to original image dimensions
        segmented_image_array = segmented_rgb_data.reshape(
            self.image.size[::-1] + (3,))

        # Create PIL Image
        segmented_image = Image.fromarray(segmented_image_array)

        # Display the image
        plt.figure(figsize=(12, 8))

        # Create subplot for original and segmented images
        plt.subplot(1, 2, 1)
        plt.imshow(self.image)
        plt.title('Original Image')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(segmented_image)
        plt.title(f'Segmented Image ({len(self.cluster_centers)} clusters)')
        plt.axis('off')

        plt.tight_layout()

        if save:
            # Save the comparison plot
            plot_path = self.output_dir / f"{self.image_path.stem}{output_suffix}_comparison.png"
            plt.savefig(plot_path, dpi=150, bbox_inches='tight')

            # Save just the segmented image
            segmented_path = self.output_dir / f"{self.image_path.stem}{output_suffix}.png"
            segmented_image.save(segmented_path, format='PNG')

            if self.logger:
                self.logger.info(
                    f"Saved segmented image comparison to {plot_path}")
                self.logger.info(f"Saved segmented image to {segmented_path}")

        # plt.show()
        return self


    def plot_rgb_rawdata(self,
                          sample_step: int = 1000,
                          save: bool = True) -> 'ImageSegmentationProcessor':
        """
        Create a 3D scatter plot of the RGB values colored by cluster.

        Args:
            sample_step: Step size for sampling points to avoid overcrowding
            save: Whether to save the plot to a file

        Returns:
            self for method chaining
        """
        if self.cluster_labels is None:
            raise RuntimeError("Must run cluster_rgb_colors before plotting")

        if self.logger:
            self.logger.info("Creating 3D scatter plot of RGB clusters")

        # Sample points to avoid overcrowding
        sample_indices = np.arange(0, len(self.rgb_data), sample_step)
        rgb_sample = self.rgb_data[sample_indices]

        # Create the plot
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        scatter = ax.scatter(rgb_sample[:, 0],
                             rgb_sample[:, 1],
                             rgb_sample[:, 2],
                             c=rgb_sample/255,
                             marker='.')

        ax.set_xlabel('Red')
        ax.set_ylabel('Green')
        ax.set_zlabel('Blue')
        ax.set_title('3D Scatter plot of the raw RGB values')

        if save:
            plot_path = self.output_dir / f"{self.image_path.stem}_3d_scatter_raw.png"
            plt.savefig(plot_path)
            if self.logger:
                self.logger.info(f"Saved cluster plot to {plot_path}")

        plt.close()
        return self



    def plot_rgb_clusters(self,
                         sample_step: int = 1000,
                         save: bool = True) -> 'ImageSegmentationProcessor':
        """
        Create a 3D scatter plot of the RGB values colored by their cluster centers.

        Args:
            sample_step: Step size for sampling points to avoid overcrowding
            save: Whether to save the plot to a file

        Returns:
            self for method chaining
        """
        if self.cluster_labels is None:
            raise RuntimeError("Must run cluster_rgb_colors before plotting")

        if self.logger:
            self.logger.info("Creating 3D scatter plot of RGB clusters")

        # Sample points to avoid overcrowding
        sample_indices = np.arange(0, len(self.rgb_data), sample_step)
        rgb_sample = self.rgb_data[sample_indices]
        labels_sample = self.cluster_labels[sample_indices]

        # Create the plot
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Map each point to its cluster center color with proper normalization
        cluster_colors = self.cluster_centers[labels_sample] / 255.0
        # Ensure values are in valid range [0,1]
        cluster_colors = np.clip(cluster_colors, 0.0, 1.0)

        scatter = ax.scatter(rgb_sample[:, 0],
                            rgb_sample[:, 1],
                            rgb_sample[:, 2],
                            c=cluster_colors,
                            marker='.')

        ax.set_xlabel('Red')
        ax.set_ylabel('Green')
        ax.set_zlabel('Blue')
        ax.set_title('3D Scatter Plot of RGB Values')

        # Create a custom colorbar with discrete cluster colors
        unique_labels = np.arange(len(self.cluster_centers))
        # Ensure cluster centers are properly normalized for colormap
        normalized_centers = np.clip(self.cluster_centers / 255.0, 0.0, 1.0)
        cmap = plt.cm.colors.ListedColormap(normalized_centers)
        norm = plt.cm.colors.BoundaryNorm(boundaries=np.arange(len(self.cluster_centers) + 1) - 0.5,
                                         ncolors=len(self.cluster_centers))

        # Add colorbar with cluster numbers
        cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap),
                           ax=ax,
                           label='Cluster',
                           ticks=unique_labels)
        cbar.ax.set_yticklabels([f'Cluster {i}' for i in unique_labels])

        if save:
            plot_path = self.output_dir / f"{self.image_path.stem}_3d_scatter.png"
            plt.savefig(plot_path)
            if self.logger:
                self.logger.info(f"Saved cluster plot to {plot_path}")

        plt.close()
        return self


    def plot_rgb_clusters_colorful(self,
                         sample_step: int = 1000,
                         save: bool = True) -> 'ImageSegmentationProcessor':
        """
        Create a 3D scatter plot of the RGB values colored by their cluster centers.

        Args:
            sample_step: Step size for sampling points to avoid overcrowding
            save: Whether to save the plot to a file

        Returns:
            self for method chaining
        """
        if self.cluster_labels is None:
            raise RuntimeError("Must run cluster_rgb_colors before plotting")

        if self.logger:
            self.logger.info("Creating 3D scatter plot of RGB clusters")

        # Sample points to avoid overcrowding
        sample_indices = np.arange(0, len(self.rgb_data), sample_step)
        rgb_sample = self.rgb_data[sample_indices]
        labels_sample = self.cluster_labels[sample_indices]

        # Create the plot
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        scatter = ax.scatter(rgb_sample[:, 0],
                            rgb_sample[:, 1],
                            rgb_sample[:, 2],
                            marker='.',

                            c=labels_sample,
                            cmap='viridis'
                           )

        ax.set_xlabel('Red')
        ax.set_ylabel('Green')
        ax.set_zlabel('Blue')
        ax.set_title('3D Scatter Plot of RGB Values')

        plt.colorbar(scatter, label='Cluster')

        if save:
            plot_path = self.output_dir / f"{self.image_path.stem}_3d_scatter_color.png"
            plt.savefig(plot_path)
            if self.logger:
                self.logger.info(f"Saved colorful cluster plot to {plot_path}")

        plt.close()
        return self

# ## Usage Examples

# # Basic usage (unchanged behavior)
# processor = ImageSegmentationProcessor("image.jpg", "output/")
# processor.cluster_rgb_colors()

# # Set defaults in constructor
# custom_centers = np.array([[255,0,0], [0,255,0], [0,0,255]])
# processor = ImageSegmentationProcessor(
#     "image.jpg", "output/",
#     n_clusters=3,
#     kmeans_init_centers=custom_centers
# )
# processor.cluster_rgb_colors()  # Uses constructor defaults

# # Override in method call
# processor.cluster_rgb_colors(n_clusters=8)  # Override n_clusters only
# processor.cluster_rgb_colors(kmeans_init_centers=new_centers)  # Override centers only
