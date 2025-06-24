import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pathlib import Path
from contextlib import redirect_stdout
from scipy.spatial import KDTree
from collections import deque
import time
import json


class InstanceSegmentation:
    """
    InstanceSegmentation - Image Processing and Object Detection Class

    This class implements instance segmentation on images by grouping pixels based on spatial proximity
    and connectivity. It is designed to process images containing multiple distinct objects and separate
    them into individual instances using a KD-tree based spatial indexing approach.

    Key Features:
    -------------
    1. Flexible initialization through JSON configuration or direct parameters
    2. Efficient pixel grouping using KD-tree spatial indexing
    3. Configurable object size and distance thresholds
    4. Automated output generation including visualizations and statistics
    5. Support for both original and background-removed images
    6. Batch processing capability

    Main Functionalities:
    -------------------
    1. Image Loading and Preprocessing:
       - Loads images in various formats
       - Handles both original and background-removed images
       - Converts images to numpy arrays for processing

    2. Pixel Group Detection:
       - Groups pixels based on spatial proximity
       - Uses KD-tree for efficient nearest neighbor searches
       - Applies configurable distance thresholds

    3. Object Filtering:
       - Filters objects based on minimum pixel count
       - Removes noise and insignificant pixel groups
       - Labels valid objects with unique identifiers

    4. Visualization and Output:
       - Generates plots of detected objects
       - Creates labeled visualizations
       - Saves results in various formats

    5. Metadata Management:
       - Tracks processing parameters
       - Generates statistics for detected objects
       - Creates detailed output reports

    Usage:
    ------
    1. Using JSON Configuration:
        ```python
        processor = InstanceSegmentation(config_path='config.json')
        processor.load_image()
        processor.segment_image_kdtree()
        processor.generate_plot()
        processor.write_metadata(sample_name="Sample1")
        ```

    2. Using Direct Parameters:
        ```python
        processor = InstanceSegmentation(
            image_path="/path/to/image.jpg",
            output_dir="/path/to/output",
            min_pixels=1000,
            max_distance=4.0
        )
        processor.process()
        ```

    Configuration Parameters:
    -----------------------
    - image_path: Path to the input image
    - output_dir: Directory for saving outputs
    - min_pixels: Minimum pixel count for valid objects (default: 1000)
    - max_distance: Maximum pixel-to-pixel distance for grouping (default: 4.0)

    JSON Configuration Format:
    ------------------------
    {
        "image_info": {
            "original_image": {
                "filename": "image.jpg",
                "path": "path/to/image.jpg"
            },
            "no_background_image": {
                "filename": "image_no_bkgd.png",
                "path": "path/to/image_no_bkgd.png"
            }
        },
        "processing_parameters": {
            "max_distance": 4.0,
            "min_pixels": 1000
        },
        "output": {
            "directory": "output_dir_path"
        }
    }

    Output Files:
    ------------
    1. Visualization:
       - PNG file showing detected objects with different colors
       - Plot with bounding boxes around detected objects

    2. Statistics:
       - Text file with object statistics
       - JSON file with detailed metadata

    3. Metadata:
       - Processing parameters
       - Object counts and sizes
       - Image information

    Dependencies:
    ------------
    - numpy: Array processing and numerical operations
    - PIL: Image loading and manipulation
    - matplotlib: Visualization and plotting
    - scipy: KD-tree implementation for spatial indexing
    - pathlib: Path handling
    - json: Configuration file parsing

    Notes:
    ------
    - The class assumes input images are in a standard format (JPEG, PNG)
    - Memory usage scales with image size and number of non-background pixels
    - Processing time depends on image size and max_distance parameter
    - Large max_distance values can significantly increase processing time

    Example:
    --------
    ```python
    from instance_segmentation import InstanceSegmentation

    # Initialize processor
    processor = InstanceSegmentation(config_path='config.json')

    # Process single image
    processor.load_image()
    processor.segment_image_kdtree()
    processor.generate_plot()
    processor.write_metadata(sample_name="Sample1")

    # Or use the convenience method for batch processing
    processor.process_batch('input_directory/*.jpg')
    """
    def __init__(self, config_path=None, **kwargs):
        """
        Initialize the InstanceSegmentation class.

        Args:
            config_path (str or Path, optional): Path to JSON configuration file
            **kwargs: Optional parameters that override JSON config:
                - image_path (str or Path): Path to the input image
                - output_dir (str or Path): Directory to save output files
                - min_pixels (int): Minimum size area of objects
                - max_distance (float): Maximum distance between pixels to be considered part of the same object
        """
        if config_path:
            self.load_config(config_path)
        if 'image_path' in kwargs:
            self.image_path = Path(kwargs['image_path'])
        if 'output_dir' in kwargs:
            self.output_dir = Path(kwargs['output_dir'])
        if 'min_pixels' in kwargs:
            self.min_pixels = kwargs['min_pixels']
        if 'max_distance' in kwargs:
            self.max_distance = kwargs['max_distance']
        # Validate required attributes
        required_attrs = ['image_path', 'output_dir', 'min_pixels', 'max_distance']
        missing_attrs = [attr for attr in required_attrs if not hasattr(self, attr)]
        if missing_attrs:
            raise ValueError(f"Missing required attributes: {', '.join(missing_attrs)}")

            # Initialize other attributes
        self.image_np = None
        self.image_with_coords = None
        self.filtered_image = None
        self.segmented_image = None
        self.height = None
        self.width = None
        self.image_proportion = None

    def load_config(self, json_path):
        """
        Load and validate configuration from a JSON file.

        Args:
            json_path (str or Path): Path to the JSON configuration file

        Returns:
            bool: True if configuration was loaded successfully

        Raises:
            FileNotFoundError: If a JSON file doesn't exist
            ValueError: If required configuration fields are missing or invalid
        """
        try:
            with open(json_path, 'r') as f:
                config = json.load(f)

            # Validate required sections
            required_sections = ['image_info', 'processing_parameters', 'output']
            for section in required_sections:
                if section not in config:
                    raise ValueError(f"Missing required section '{section}' in config file")

            # Extract and validate image paths
            image_info = config['image_info']
            if not all(key in image_info for key in ['original_image', 'no_background_image']):
                raise ValueError("Missing image path information in config file, either to the original image or the no-background image, or both")

            #ori. self.image_path = Path(image_info['original_image']['path'])
            self.image_path = Path(image_info['no_background_image']['path'])
            self.no_background_image_path = Path(image_info['no_background_image']['path'])

            if not self.image_path.exists():
                raise FileNotFoundError(f"Original image not found: {self.image_path}")
            if not self.no_background_image_path.exists():
                raise FileNotFoundError(f"No-background image not found: {self.no_background_image_path}")

            # Extract processing parameters
            proc_params = config['processing_parameters']
            self.max_distance = float(proc_params.get('max_distance', 4.0))
            self.min_pixels = int(proc_params.get('min_pixels', 1000))

            # Set output directory
            self.output_dir = Path(config['output']['directory'])
            self.output_dir.mkdir(parents=True, exist_ok=True)

            return True

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in config file: {e}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")

    def load_image(self):
        """Load and process the input original image."""
        self.image_np = np.asarray(Image.open(self.image_path))
        self.height, self.width = self.image_np.shape[:2]
        self.image_proportion = self.height / self.width

        # Create meshgrid for coordinates
        y_coords, x_coords = np.meshgrid(np.arange(self.height),
                                       np.arange(self.width),
                                       indexing='ij')

        # Create array with coordinates
        self.image_with_coords = np.zeros((self.height, self.width, 6))
        self.image_with_coords[:, :, :3] = self.image_np
        self.image_with_coords[:, :, 4] = x_coords
        self.image_with_coords[:, :, 5] = y_coords

        # Filter white pixels
        reshaped_image = self.image_with_coords.reshape(-1, 6)
        mask = ~np.all(reshaped_image[:, :3] == 255, axis=1)
        self.filtered_image = reshaped_image[mask]

    def segment_image_kdtree(self):
        """
        Perform image segmentation using KD-tree spatial indexing with optimizations.
        """
        print("Starting segmentation...")
        start_time = time.time()

        # Use only coordinates for KD-tree
        coords = self.filtered_image[:, 4:6]
        tree = KDTree(coords)
        labels = np.full(len(coords), -1)
        labels_all_groups = 0
        group_pixels = {}

        def bfs_labeling(start_idx, label):
            pixels_in_group = []
            queue = deque([start_idx])
            visited = set()  # Track visited points

            while queue:
                current_idx = queue.popleft()
                if current_idx in visited:
                    continue

                visited.add(current_idx)
                labels[current_idx] = label
                pixels_in_group.append(coords[current_idx])

                # Query points in chunks to improve performance
                nearby_points = tree.query_ball_point(
                    coords[current_idx],
                    self.max_distance,
                    workers=-1  # Use all available CPU cores
                )

                for idx in nearby_points:
                    if idx not in visited and labels[idx] == -1:
                        queue.append(idx)

            return np.array(pixels_in_group)

        # Process points in chunks
        chunk_size = 1000
        for i in range(0, len(coords), chunk_size):
            chunk_indices = range(i, min(i + chunk_size, len(coords)))
            for idx in chunk_indices:
                if labels[idx] == -1:
                    group_pixels[labels_all_groups] = bfs_labeling(idx, labels_all_groups)
                    labels_all_groups += 1

            # Print progress
            if (i + chunk_size) % 10000 == 0:
                print(f"Processed {i + chunk_size}/{len(coords)} points...")

        # Filter and relabel groups
        valid_labels = {label for label, pixels in group_pixels.items()
                       if len(pixels) >= self.min_pixels}

        final_labels = np.full(len(coords), -1)
        new_label = 0

        for old_label in valid_labels:
            mask = (labels == old_label)
            final_labels[mask] = new_label
            new_label += 1

        self.segmented_image = np.column_stack((self.filtered_image, final_labels))
        self.total_groups = new_label

        end_time = time.time()
        print(f"Segmentation completed in {end_time - start_time:.2f} seconds")
        print(f"Found {new_label} valid groups (with ≥{self.min_pixels} pixels) "
              f"out of {labels_all_groups} total groups")

    def generate_plot(self, padding=35):
        """Generate and save plot of segmented image."""
        width_image = 12
        height_image = width_image * self.image_proportion

        plt.figure(figsize=(width_image, height_image))
        valid_points = self.segmented_image[self.segmented_image[:, -1] >= 0]

        plt.scatter(valid_points[:, 4], valid_points[:, 5],
                   c=valid_points[:, -1],
                   cmap='tab20',
                   alpha=0.6,
                   s=1)

        plt.colorbar(label='Group Label')
        plt.xlabel('X coordinate')
        plt.ylabel('Y coordinate')
        plt.gca().invert_yaxis()
        plt.title(f'Filtered Pixel Groups (minimum {self.min_pixels} pixels, '
                 f'distance <= {self.max_distance} pixels)')
        plt.tight_layout()

        output_path = self.output_dir / f"{self.image_path.stem}_pixel_groups.png"
        plt.savefig(output_path, dpi=150)
        plt.close()

    def write_metadata(self, sample_name):
        """
        Write metadata and statistics to output file.

        Args:
            sample_name (str): Name of the sample being processed
        """
        output_file = self.output_dir / f'{self.image_path.stem}_pixel_groups.txt'

        with open(output_file, 'w') as f:
            with redirect_stdout(f):
                print("Settings for the segmentation process:\n")
                print(f"- Sample name: {sample_name}")
                print(f"- Image filename: {self.image_path.name}")
                print(f"- Minimal size area of the objects: {self.min_pixels} pixels")
                print(f"- Maximum distance between pixels: {self.max_distance} pixels")
                print("\n------------------------\n")

                valid_labels = self.segmented_image[self.segmented_image[:, -1] >= 0][:, -1]
                unique_labels = np.unique(valid_labels)

                print(f"Found {len(unique_labels)} valid groups")
                print("\nStatistics for valid groups:")

                for label in unique_labels:
                    group_pixels = self.segmented_image[self.segmented_image[:, -1] == label]
                    print(f"\nObject {int(label)}:")
                    print(f"Number of pixels: {len(group_pixels)}")

    def process(self):
        """
        Process the image through all steps with error handling.
        """
        try:
            self.load_image()
            self.segment_image_kdtree()
            self.generate_plot()
            self.write_metadata(sample_name="Sample1")
            return True
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Cleaning up...")
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


# USE

from pathlib import Path
from instance_segmentator import InstanceSegmentation

# Path to your JSON config file
config_path='/Users/aavelino/Downloads/images/BM4_E_sandbox/clustering_crops/capt0011/capt0011_config.json'

# Initialize and process
processor = InstanceSegmentation(config_path=config_path)
processor.process()  # This will run all steps

