import logging
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.cluster import KMeans
from typing import List, Optional, Union
import matplotlib.pyplot as plt


class ImageSegmentationProcessor:

    def __init__(self,
                 image_path: Union[str, Path],
                 output_dir: Union[str, Path],
                 enable_logging: bool = False):
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

        # or:
        processor = ImageSegmentationProcessor(
          image_path="input/image.jpg",
          output_dir="output",
          enable_logging=True
        )

        # Individual method usage
        processor.cluster_rgb_colors(n_clusters=8)
        processor.remove_background(background_clusters=0, output_suffix="_nobg")
        processor.plot_rgb_clusters(save=True)

        # Method chaining example
        processor.cluster_rgb_colors(n_clusters=8) \
              .remove_background(background_clusters=[0, 1]) \
              .plot_rgb_clusters(sample_step=1000)
        ```
        --------
        Initialize the image segmentation processor.

        Args:
            image_path: Path to the input image file
            output_dir: Directory where output files will be saved
            enable_logging: Whether to create a log file for this image

        Raises:
            FileNotFoundError: If image_path doesn't exist
            NotADirectoryError: If output_dir doesn't exist or can't be created
        """

        # Convert paths to Path objects
        self.image_path = Path(image_path)
        self.output_dir = Path(output_dir)

        # Validate input image
        if not self.image_path.is_file():
            raise FileNotFoundError(f"Input image not found: {self.image_path}")

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

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
                           n_clusters: int = 5,
                           random_state: int = 42) -> 'ImageSegmentationProcessor':
        """
        Perform K-means clustering on the image pixels.

        Args:
            n_clusters: Number of clusters for K-means
            random_state: Random seed for reproducibility

        Returns:
            self for method chaining
        """
        if self.logger:
            self.logger.info(f"Clustering RGB colors into {n_clusters} clusters")

        if n_clusters == 5:
            self.kmeans_init_centers = np.asarray(
                [[79.49, 130.62, 189.84],
                 [131.84, 107.86, 76.36],
                 [178.59, 173.83, 159.51],
                 [47.20, 28.64, 18.90],
                 [114.45, 146.57, 187.97]]
            )
            self.kmeans = KMeans(n_clusters=n_clusters,
                                 init=self.kmeans_init_centers,
                                 random_state=random_state)
        else:
            self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)

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

        # Create new image with white background (255, 255, 255)
        img_array = np.array(self.image)
        new_img = np.full_like(img_array, 255)  # Create white background
        new_img[mask] = img_array[mask]  # Copy non-background pixels

        # Save the image
        output_image = Image.fromarray(new_img)
        output_path = self.output_dir / f"{self.image_path.stem}{output_suffix}.png"
        output_image.save(output_path, format='PNG')

        if self.logger:
            self.logger.info(f"Saved background-removed image to {output_path}")

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

        # Map each point to its cluster center color
        cluster_colors = self.cluster_centers[labels_sample] / 255.0  # Normalize to [0,1] range

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
        cmap = plt.cm.colors.ListedColormap(self.cluster_centers / 255.0)
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

