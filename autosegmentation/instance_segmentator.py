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

    This class implements instance segmentation on images by grouping
    pixels based on spatial proximity and connectivity. It is designed
    to process images containing multiple distinct objects and
    separate them into individual instances using a KD-tree based
    spatial indexing approach.

    Key Features:
    -------------
    1. Flexible initialization through JSON configuration or direct parameters
    2. Efficient pixel grouping using KD-tree spatial indexing
    3. Configurable object size and distance thresholds
    4. Optional thin-object selection via length strategies (bbox, PCA, skeleton)
    5. Automated output generation including visualizations and statistics
    6. Support for both original and background-removed images
    7. Batch processing capability

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
       - Optionally keeps thin objects by length threshold (min_pixels OR min_length)
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
        ```
        # Path to your JSON config file
        config_path='/path/to/config_file.json'

        # Initialize and process
        processor = InstanceSegmentation(config_path=config_path)
        processor.process()  # This will run all steps
        ```
        or

        ```python
        processor = InstanceSegmentation(config_path='/path/to/config_file.json')
        processor.create_image_with_coordinates()
        processor.segment_image_kdtree()
        processor.generate_plot()
        processor.write_metadata()
        ```

    2. Using Direct Parameters:
        ```python
        processor = InstanceSegmentation(
            nobackground_image_path="/path/to/image_without_background.jpg",
            output_dir="/path/to/output",
            min_pixels=1000,
            min_length=200,
            length_strategy="bbox",
            max_distance=4.0,
            sample_name="sample_name"
        )
        processor.process()
        ```

    Configuration Parameters:
    -----------------------
    - nobackground_image_path: Path to the input image with no background
    - output_dir: Directory for saving outputs
    - min_pixels: Minimum pixel count for valid objects (default: 1000)
    - min_length: Minimum length (pixels) for valid thin objects (default: 200)
    - length_strategy: Length strategy ("bbox", "pca", "skeleton"; default: "bbox")
      Note: "bbox" is the fastest strategy and is used by default.
    - max_distance: Maximum pixel-to-pixel distance for grouping (default: 4.0)
    - sample_name: Sample name.

    JSON Configuration Format:
    ------------------------
    {
        "image_info": {
            "no_background_image": {
                "path": "path/to/image_without_background.png"
                "sample_name": "my_sample_name"
            }
        },
        "processing_parameters": {
            "max_distance": 4.0,
            "min_pixels": 1000,
            "min_length": 200,
            "length_strategy": "bbox"
        },
        "output": {
            "directory": "output_dir_path"
        }
    }

    Output Files:
    ------------
    1. Visualization:
       - PNG file showing detected objects with different colors

    2. Statistics:
       - Text file with object statistics
         (e.g., `{image_stem}_pixel_groups.txt`)

    3. Metadata:
       - Processing parameters
       - Object counts and sizes
       - Image information

    Output Summary:
    --------------
    - Segmentation plot(s): saved to the output directory with group labels
    - Per-image statistics text file with parameters and group sizes
    - Cropped images and JSON metadata when cropping is enabled via downstream
      processing (see CropImageAndWriteBBox in batch processing)
    - In-memory arrays: `segmented_image` (with group labels) and `filtered_image`

    Dependencies:
    ------------
    - numpy: Array processing and numerical operations
    - PIL: Image loading and manipulation
    - matplotlib: Visualization and plotting
    - scipy: KD-tree implementation for spatial indexing
    - pathlib: Path handling
    - json: Configuration file parsing
    - time
    - collections.deque
    - contextlib.redirect_stdout

    Notes:
    ------
    - The class assumes input images are in a standard format (JPEG, PNG)
    - Memory usage scales with image size and number of non-background pixels
    - Processing time depends on image size and max_distance parameter
    - Large max_distance values can significantly increase processing time
    - Length strategy "bbox" is fastest; "pca" and "skeleton" are more expensive
    - Use "pca" for oriented thin objects, "skeleton" for curvy thin objects
    """

    def __init__(self, config_path=None, **kwargs):
        """
        Initialize the InstanceSegmentation class.

        Args:
            config_path (str or Path, optional): Path to JSON configuration file
            **kwargs: Optional parameters that override JSON config:
                - nobackground_image_path (str or Path): Path to the input image with no background
                - output_dir (str or Path): Directory to save output files
                - min_pixels (int): Minimum size area of objects
                - min_length (float): Minimum length in pixels for thin objects
                - length_strategy (str): Length strategy ("bbox", "pca", "skeleton")
                - max_distance (float): Maximum distance between pixels to be considered part of the same object
                - no_margins (bool): Generate plot without margins/borders (default: False)
                - generate_both_plots (bool): Generate both regular and no-margins plots (default: False)
        """
        if config_path:
            self.load_config(config_path)
        if 'sample_name' in kwargs:
            self.sample_name = kwargs['sample_name']
        if 'nobackground_image_path' in kwargs:
            self.nobackground_image_path = Path(
                kwargs['nobackground_image_path'])
        if 'raw_image_path' in kwargs:
            self.raw_image_path = Path(kwargs['raw_image_path'])
        if 'output_dir' in kwargs:
            self.output_dir = Path(kwargs['output_dir'])
        if 'min_pixels' in kwargs:
            self.min_pixels = kwargs['min_pixels']
        if 'min_length' in kwargs:
            self.min_length = kwargs['min_length']
        if 'length_strategy' in kwargs:
            self.length_strategy = kwargs['length_strategy']
        if 'max_distance' in kwargs:
            self.max_distance = kwargs['max_distance']
        if 'padding' in kwargs:
            self.padding = kwargs['padding']
        if 'cropping' in kwargs:
            self.cropping = kwargs['cropping']
        if 'no_margins' in kwargs:
            self.no_margins = kwargs['no_margins']
        if 'generate_both_plots' in kwargs:
            self.generate_both_plots = kwargs['generate_both_plots']

        # Validate required attributes
        required_attrs = ['nobackground_image_path', 'output_dir', 'min_pixels',
                          'max_distance']
        missing_attrs = [attr for attr in required_attrs if
                         not hasattr(self, attr)]
        if missing_attrs:
            raise ValueError(
                f"Missing required attributes: {', '.join(missing_attrs)}")

        # Initialize other attributes
        self.image_np = None
        self.image_with_coords = None
        self.filtered_image = None
        self.segmented_image = None
        self.height = None
        self.width = None
        self.image_proportion = None

        # Set default values if not provided
        if not hasattr(self, 'no_margins'):
            self.no_margins = False
        if not hasattr(self, 'generate_both_plots'):
            self.generate_both_plots = False
        if not hasattr(self, 'min_length'):
            self.min_length = 200
        if not hasattr(self, 'length_strategy'):
            self.length_strategy = 'bbox'


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
                content = f.read()

            # Try to parse JSON with better error reporting
            try:
                config = json.loads(content)
            except json.JSONDecodeError as json_err:
                # Provide more detailed error information
                lines = content.split('\n')
                error_line_num = json_err.lineno
                error_col = json_err.colno

                print(f"JSON parsing error at line {error_line_num}, column {error_col}")
                if error_line_num <= len(lines):
                    print(f"Problematic line: {lines[error_line_num - 1]}")
                    print(f"Error position: {' ' * (error_col - 1)}^")

                # Common fixes for JSON syntax errors
                error_msg = f"Invalid JSON format in config file at line {error_line_num}, column {error_col}: {json_err.msg}\n"
                error_msg += "Common fixes:\n"
                error_msg += "1. Ensure all property names are enclosed in double quotes (not single quotes)\n"
                error_msg += "2. Remove any trailing commas after the last element in objects or arrays\n"
                error_msg += "3. Remove any comments (JSON doesn't support comments)\n"
                error_msg += "4. Escape special characters in strings with backslashes\n"

                raise ValueError(error_msg)

            # Validate required sections
            required_sections = ['image_info', 'processing_parameters', 'output']
            for section in required_sections:
                if section not in config:
                    raise ValueError(f"Missing required section '{section}' in config file")

            # Extract and validate image paths
            image_info = config['image_info']
            if not all(key in image_info for key in ['sample_name', 'no_background_image']):
                raise ValueError("Missing image path information or sample name in config file")

            self.nobackground_image_path = Path(image_info['no_background_image']['path'])
            if not self.nobackground_image_path.exists():
                raise FileNotFoundError(
                    f"Image without background not found: {self.nobackground_image_path}")

            # Raw image file path definition, i.e., the one with still the
            # background color. This info is not used in this class but will be
            # passed to the 'CropImageAndWriteBBox' class as an input parameter
            # for cropping, so that the croppings are also done from the raw image.
            self.raw_image_path = Path(image_info['raw_image']['path'])

            # Info only to write it down as metadata in the output JSON file
            self.sample_name = image_info['sample_name']

            # Extract processing parameters
            proc_params = config['processing_parameters']
            self.max_distance = float(proc_params.get('max_distance', 4.0))
            self.min_pixels = int(proc_params.get('min_pixels', 1000))
            min_length_value = proc_params.get('min_length', 200)
            if min_length_value is None:
                self.min_length = None
            else:
                self.min_length = float(min_length_value)
            self.length_strategy = proc_params.get('length_strategy', 'bbox')

            # This info is not used in this class but will be passed to the
            # 'CropImageAndWriteBBox' class as an input parameter for cropping:
            self.padding = int(proc_params.get('padding', 35))

            # Read if the user wants to generate cropped images. This information
            # will be passed to the 'CropImageAndWriteBBox' class as an input
            # parameter for cropping.
            # Some extra lines of code to make sure that the "cropping" parameter
            # defined in the JSON file is correctly read as boolean instead of
            # as string.
            cropping_value = proc_params.get('cropping', False)
            if isinstance(cropping_value, str):
                self.cropping = cropping_value.lower() in ('true', 'True', 'TRUE',
                                                           '1', 'yes', 'Yes', 'YES', 'on')
            else:
                self.cropping = bool(cropping_value)

            # Read the no_margins parameter from configuration
            no_margins_value = proc_params.get('no_margins', False)
            if isinstance(no_margins_value, str):
                self.no_margins = no_margins_value.lower() in ('true', 'True', 'TRUE',
                                                              '1', 'yes', 'Yes', 'YES', 'on')
            else:
                self.no_margins = bool(no_margins_value)

            # Read the generate_both_plots parameter from configuration
            generate_both_value = proc_params.get('generate_both_plots', False)
            if isinstance(generate_both_value, str):
                self.generate_both_plots = generate_both_value.lower() in ('true', 'True', 'TRUE',
                                                                          '1', 'yes', 'Yes', 'YES', 'on')
            else:
                self.generate_both_plots = bool(generate_both_value)

            # Set the output directory. Create it if it doesn't exist.
            self.output_dir = Path(config['output']['directory'])
            self.output_dir.mkdir(parents=True, exist_ok=True)

            return True

        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {json_path}")
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")


    def create_image_with_coordinates(self):
        """Load and process the input image."""
        self.image_np = np.asarray(Image.open(self.nobackground_image_path))
        self.height, self.width = self.image_np.shape[:2]
        self.image_proportion = self.height / self.width

        # Create meshgrid for coordinates
        y_coords, x_coords = np.meshgrid(np.arange(self.height),
                                       np.arange(self.width),
                                       indexing='ij')

        # Create an array with coordinates
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
        self.total_groups = labels_all_groups

        end_time = time.time()
        print(f"Segmentation completed in {end_time - start_time:.2f} seconds")
        print(f"Found {new_label} valid groups (with ≥{self.min_pixels} pixels) "
              f"out of {labels_all_groups} total groups")


    def generate_plot(self, padding=35, no_margins=None, generate_both=False):
        """
        Generate and save plot of segmented image.

        Args:
            padding (int): Padding parameter (for compatibility, not used in current implementation)
            no_margins (bool, optional): If True, creates plot without margins/borders.
                                       If None, uses the instance's no_margins setting.
            generate_both (bool): If True, generates both regular and no-margins plots.
        """
        # Use parameter value if provided, otherwise use instance setting
        use_no_margins = no_margins if no_margins is not None else self.no_margins

        valid_points = self.segmented_image[self.segmented_image[:, -1] >= 0]

        # If generate_both is True, create both versions
        if generate_both:
            # Generate regular plot first
            self._create_single_plot(valid_points, with_margins=True)
            # Generate no-margins plot
            self._create_single_plot(valid_points, with_margins=False)
        else:
            # Generate single plot based on use_no_margins setting
            self._create_single_plot(valid_points,
                                     with_margins=not use_no_margins)


    def _create_single_plot(self, valid_points, with_margins=True):
        """
        Create a single plot (either with or without margins).

        Args:
            valid_points: Array of valid segmentation points
            with_margins (bool): If True, creates standard plot with margins, axes, etc.
                                If False, creates plot without any margins or decorations.
        """
        width_image = 12
        height_image = width_image * self.image_proportion

        if with_margins:
            # Standard plot with margins
            plt.figure(figsize=(width_image, height_image))

            plt.scatter(valid_points[:, 4], valid_points[:, 5],
                        c=valid_points[:, -1],
                        cmap='tab20',
                        alpha=0.6,
                        s=1)

            plt.colorbar(label='Group Label')
            plt.xlabel('X coordinate')
            plt.ylabel('Y coordinate')
            plt.gca().invert_yaxis()
            plt.title(
                f'Filtered Pixel Groups (minimum {self.min_pixels} pixels, '
                f'distance <= {self.max_distance} pixels)')
            plt.tight_layout()

            filename_suffix = "_pixel_groups.jpg"
            output_path = self.output_dir / f"{self.nobackground_image_path.stem}{filename_suffix}"
            plt.savefig(output_path, dpi=150, format='jpg')

        else:
            # No-margins plot - completely eliminate all white space
            fig = plt.figure(figsize=(width_image, height_image), frameon=False)
            ax = fig.add_axes([0, 0, 1, 1])  # Use entire figure area
            ax.axis('off')  # Remove axes

            # Create scatter plot
            ax.scatter(valid_points[:, 4], valid_points[:, 5],
                       c=valid_points[:, -1],
                       cmap='tab20',
                       alpha=0.6,
                       s=1)

            # Set exact limits to data bounds to eliminate any white space
            ax.set_xlim(valid_points[:, 4].min(), valid_points[:, 4].max())
            ax.set_ylim(valid_points[:, 5].min(), valid_points[:, 5].max())
            ax.invert_yaxis()

            # Remove all margins and padding
            ax.set_position([0, 0, 1, 1])

            filename_suffix = "_pixel_groups_no_margins.jpg"
            output_path = self.output_dir / f"{self.nobackground_image_path.stem}{filename_suffix}"

            # Save with absolute no padding/margins
            plt.savefig(output_path, dpi=150, bbox_inches='tight',
                        pad_inches=0, facecolor='none', edgecolor='none',
                        format='jpg')

        plt.close()


    def write_metadata(self):
        """
        Write metadata and statistics to output file.
        """
        output_file = self.output_dir / f'{self.nobackground_image_path.stem}_pixel_groups.txt'

        with open(output_file, 'w') as f:
            with redirect_stdout(f):
                print("Settings used for the segmentation process:\n")
                print(f"- Sample name: {self.sample_name}")
                print(f"- Image filename: {self.nobackground_image_path.name}")
                print(f"- Minimal size area of the objects: {self.min_pixels} pixels")
                print(f"- Maximum distance between pixels: {self.max_distance} pixels")
                print("\n------------------------\n")

                valid_labels = self.segmented_image[self.segmented_image[:, -1] >= 0][:, -1]
                unique_labels = np.unique(valid_labels)

                print(f"Found {len(unique_labels)} valid groups (i.e., that are >= {self.min_pixels} pixels) "
                      f"out of {self.total_groups} total groups.")
                print("Note: the segmentation has been done on the image without background.")
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
            self.create_image_with_coordinates()
            self.segment_image_kdtree()

            # Generate plots based on configuration
            if self.generate_both_plots:
                self.generate_plot(generate_both=True)
            else:
                self.generate_plot()

            self.write_metadata()
            return True
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Cleaning up...")
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

# ------------------------------------------------------

### Usage Examples

# processor = InstanceSegmentation(
#     nobackground_image_path="path/to/image.png",
#     output_dir="output/",
#     min_pixels=1000,
#     max_distance=4.0,
#     generate_both_plots=True  # This will create both versions
# )
# processor.process()
#
#
# # Manual control over plot generation:
# processor = InstanceSegmentation(config_path="config.json")
# # Generate both plots manually
# processor.generate_plot(generate_both=True)
#
# # **JSON configuration for both plots:**
#
# {
#     "processing_parameters": {
#         "max_distance": 4.0,
#         "min_pixels": 1000,
#         "generate_both_plots": true
#     }
# }
