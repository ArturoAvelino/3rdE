import json
import time
import numpy as np
from PIL import Image
from pathlib import Path
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from typing import Union, List, Dict, Tuple, Optional


class InstanceSegmentationByColor:
    """
    InstanceSegmentationByColor - Image Processing and Object Detection Class using Color Clustering

    This class implements instance segmentation on images by grouping pixels based on color similarity
    using K-means clustering. It is designed to process images containing multiple distinct objects
    and separate them into individual instances based on their color characteristics.

    Key Features:
    -------------
    1. Flexible initialization through JSON configuration or direct parameters
    2. Efficient pixel grouping using K-means clustering on RGB values
    3. Configurable cluster count and minimum pixel thresholds
    4. Automated bounding box computation for each color cluster
    5. Compatible JSON output format with existing CropImageAndWriteBBox class
    6. Support for both original and background-removed images
    7. Cropping and metadata generation for individual color clusters

    Main Functionalities:
    -------------------
    1. Image Loading and Preprocessing:
       - Loads images in various formats (JPEG, PNG)
       - Handles both original and background-removed images
       - Converts images to numpy arrays for processing

    2. Color Cluster Detection:
       - Groups pixels based on RGB color similarity using K-means
       - Applies configurable cluster count and minimum pixel thresholds
       - Creates pixel coordinate mappings for each color cluster

    3. Bounding Box Computation:
       - Computes bounding boxes for each valid color cluster
       - Applies padding with boundary checks
       - Calculates center coordinates, width, and height

    4. Output Generation:
       - Creates cropped images for each color cluster
       - Generates JSON metadata compatible with existing workflow
       - Supports both individual and combined JSON output files

    Usage:
    ------
    1. Using JSON Configuration:
        ```python
        processor = InstanceSegmentationByColor(config_path='/path/to/config.json')
        results = processor.process()
        ```

    2. Using Direct Parameters:
        ```python
        processor = InstanceSegmentationByColor(
            image_path="/path/to/image_no_background.png",
            raw_image_path="/path/to/raw_image.jpg",
            sample_name="sample_01",
            output_dir="/path/to/output",
            n_clusters=5,
            min_pixels=400,
            padding=10
        )
        results = processor.process()
        ```

    Configuration Parameters:
    -----------------------
    - image_path: Path to the input image with no background
    - raw_image_path: Path to the original image with background
    - sample_name: Sample identifier for metadata
    - output_dir: Directory for saving outputs
    - n_clusters: Number of color clusters to identify (default: 5)
    - min_pixels: Minimum pixel count for valid clusters (default: 400)
    - padding: Padding around bounding boxes in pixels (default: 0)

    Output Files:
    ------------
    1. Cropped Images:
       - Individual PNG/JPG files for each valid color cluster
       - Named as: "color_cluster_{id}_{filename}.{ext}"

    2. JSON Metadata:
       - Individual JSON files for each cluster with bounding box data
       - Combined JSON file with all clusters (optional)
       - Compatible with existing CropImageAndWriteBBox format

    Dependencies:
    ------------
    - numpy: Array processing and numerical operations
    - PIL: Image loading and manipulation
    - scikit-learn: K-means clustering implementation
    - matplotlib: Visualization capabilities
    - pathlib: Path handling
    - json: Configuration and metadata file handling
    """

    def __init__(self, config_path: Optional[Union[str, Path]] = None, **kwargs):
        """
        Initialize the InstanceSegmentationByColor class.

        Args:
            config_path (str or Path, optional): Path to JSON configuration file
            **kwargs: Optional parameters that override JSON config:
                - image_path (str or Path): Path to image with no background
                - raw_image_path (str or Path): Path to original image with background
                - sample_name (str): Sample identifier
                - output_dir (str or Path): Directory to save output files
                - n_clusters (int): Number of color clusters (default: 5)
                - min_pixels (int): Minimum pixels for valid clusters (default: 400)
                - padding (int): Padding around bounding boxes (default: 0)
        """
        # Initialize default values
        self._set_default_values()

        # Load configuration if provided
        if config_path:
            self._load_config(config_path)

        # Override with kwargs
        self._apply_kwargs(kwargs)

        # Validate required attributes
        self._validate_required_attributes()

        # Initialize processing attributes
        self._initialize_processing_attributes()

    def _set_default_values(self):
        """Set default values for all attributes."""
        self.n_clusters = 5
        self.min_pixels = 400
        self.padding = 0

    def _apply_kwargs(self, kwargs):
        """Apply keyword arguments to override default or config values."""
        if 'image_path' in kwargs:
            self.image_path = Path(kwargs['image_path'])
        if 'raw_image_path' in kwargs:
            self.raw_image_path = Path(kwargs['raw_image_path'])
        if 'sample_name' in kwargs:
            self.sample_name = kwargs['sample_name']
        if 'output_dir' in kwargs:
            self.output_dir = Path(kwargs['output_dir'])
        if 'n_clusters' in kwargs:
            self.n_clusters = int(kwargs['n_clusters'])
        if 'min_pixels' in kwargs:
            self.min_pixels = int(kwargs['min_pixels'])
        if 'padding' in kwargs:
            self.padding = int(kwargs['padding'])

    def _validate_required_attributes(self):
        """Validate that all required attributes are present."""
        required_attrs = ['image_path', 'raw_image_path', 'sample_name', 'output_dir']
        missing_attrs = [attr for attr in required_attrs if not hasattr(self, attr)]
        if missing_attrs:
            raise ValueError(f"Missing required attributes: {', '.join(missing_attrs)}")

        # Validate paths exist
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image file not found: {self.image_path}")
        if not self.raw_image_path.exists():
            raise FileNotFoundError(f"Raw image file not found: {self.raw_image_path}")

    def _initialize_processing_attributes(self):
        """Initialize attributes used during processing."""
        self.image_original = None
        self.image_no_bkgd = None
        self.rgb_data = None
        self.cluster_labels = None
        self.cluster_centers = None
        self.pixel_map = None
        self.valid_clusters = None

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: Union[str, Path]):
        """
        Load and validate configuration from a JSON file.

        Args:
            config_path (str or Path): Path to the JSON configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If required configuration fields are missing
        """
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            # Validate required sections
            required_sections = ['image_info', 'processing_parameters', 'output']
            for section in required_sections:
                if section not in config:
                    raise ValueError(f"Missing required section '{section}' in config file")

            # Extract image information
            image_info = config['image_info']
            self.image_path = Path(image_info['no_background_image']['path'])
            self.raw_image_path = Path(image_info['raw_image']['path'])
            self.sample_name = image_info['sample_name']

            # Extract processing parameters
            proc_params = config['processing_parameters']
            self.n_clusters = int(proc_params.get('n_clusters', self.n_clusters))
            self.min_pixels = int(proc_params.get('min_pixels', self.min_pixels))
            self.padding = int(proc_params.get('padding', self.padding))

            # Set output directory
            self.output_dir = Path(config['output']['directory'])

        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Error parsing configuration file: {e}")

    def load_images(self):
        """
        Load both original and no-background images.

        Raises:
            Exception: If images cannot be loaded
        """
        try:
            self.image_original = Image.open(self.raw_image_path)
            self.image_no_bkgd = Image.open(self.image_path)

            # Ensure images are in RGB mode
            if self.image_original.mode != 'RGB':
                self.image_original = self.image_original.convert('RGB')
            if self.image_no_bkgd.mode != 'RGB':
                self.image_no_bkgd = self.image_no_bkgd.convert('RGB')

            print(f"Loaded images: {self.image_original.size}")

        except Exception as e:
            raise Exception(f"Failed to load images: {e}")

    def extract_color_clusters(self, random_state: int = 42):
        """
        Extract color clusters from the no-background image using K-means clustering.

        Args:
            random_state (int): Random state for reproducible results

        Returns:
            tuple: (rgb_data, cluster_labels, cluster_centers)
        """
        print(f"Extracting {self.n_clusters} color clusters...")
        start_time = time.time()

        # Convert image to numpy array and reshape for clustering
        img_array = np.array(self.image_no_bkgd)
        self.rgb_data = img_array.reshape(-1, 3)

        # Perform K-means clustering on RGB values
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=random_state, n_init=10)
        self.cluster_labels = kmeans.fit_predict(self.rgb_data)
        self.cluster_centers = kmeans.cluster_centers_

        end_time = time.time()
        print(f"Color clustering completed in {end_time - start_time:.2f} seconds")

        return self.rgb_data, self.cluster_labels, self.cluster_centers

    def create_pixel_coordinate_map(self):
        """
        Create a mapping from cluster labels to pixel coordinates.

        Returns:
            dict: Dictionary mapping cluster_id -> list of (x, y) coordinates
        """
        print("Creating pixel coordinate mapping...")

        self.pixel_map = {}
        height, width = self.image_no_bkgd.height, self.image_no_bkgd.width

        # Create coordinate arrays
        y_coords, x_coords = np.mgrid[0:height, 0:width]

        # Flatten coordinates to match cluster_labels shape
        x_flat = x_coords.flatten()
        y_flat = y_coords.flatten()

        # Group pixels by cluster
        for cluster_id in np.unique(self.cluster_labels):
            mask = self.cluster_labels == cluster_id
            cluster_x = x_flat[mask]
            cluster_y = y_flat[mask]
            self.pixel_map[cluster_id] = list(zip(cluster_x, cluster_y))

        print(f"Created pixel maps for {len(self.pixel_map)} clusters")
        return self.pixel_map

    def filter_valid_clusters(self):
        """
        Filter color clusters based on minimum pixel count requirement.

        Returns:
            dict: Filtered pixel_map containing only valid clusters
        """
        if self.pixel_map is None:
            raise RuntimeError("Must create pixel coordinate map first")

        self.valid_clusters = {}

        for cluster_id, pixel_coords in self.pixel_map.items():
            if len(pixel_coords) >= self.min_pixels:
                self.valid_clusters[cluster_id] = pixel_coords
            else:
                print(f"Cluster {cluster_id} has {len(pixel_coords)} pixels, "
                      f"below threshold of {self.min_pixels}")

        print(f"Found {len(self.valid_clusters)} valid color clusters out of "
              f"{len(self.pixel_map)} total clusters")

        return self.valid_clusters

    def compute_cluster_bounding_box(self, pixel_coords: List[Tuple[int, int]]):
        """
        Compute bounding box coordinates for a given set of pixel coordinates.

        Args:
            pixel_coords (list): List of (x, y) tuples representing pixel coordinates

        Returns:
            tuple: (left_padded, upper_padded, right_padded, lower_padded,
                   left, upper, right, lower, center_x, center_y, width, height)
        """
        if not pixel_coords:
            raise ValueError("No pixel coordinates provided")

        # Extract x and y coordinates
        x_coords, y_coords = zip(*pixel_coords)

        # Find bounding box coordinates
        left = min(x_coords)
        right = max(x_coords)
        upper = min(y_coords)
        lower = max(y_coords)

        # Calculate width, height, and center
        width = right - left + 1
        height = lower - upper + 1
        center_x = left + width / 2
        center_y = upper + height / 2

        # Apply padding with image boundary checks
        left_padded = self._apply_padding_left(left)
        right_padded = self._apply_padding_right(right)
        upper_padded = self._apply_padding_upper(upper)
        lower_padded = self._apply_padding_lower(lower)

        return (left_padded, upper_padded, right_padded, lower_padded,
                left, upper, right, lower, center_x, center_y, width, height)

    def _apply_padding_left(self, left: int) -> int:
        """Apply padding to left coordinate with boundary checks."""
        if left == 0:
            return left
        elif 0 < left <= self.padding:
            return 0
        else:
            return left - self.padding

    def _apply_padding_right(self, right: int) -> int:
        """Apply padding to right coordinate with boundary checks."""
        max_width = self.image_original.width - 1
        if right == max_width:
            return right
        elif max_width - self.padding <= right < max_width:
            return max_width
        else:
            return right + self.padding

    def _apply_padding_upper(self, upper: int) -> int:
        """Apply padding to upper coordinate with boundary checks."""
        if upper == 0:
            return upper
        elif 0 < upper <= self.padding:
            return 0
        else:
            return upper - self.padding

    def _apply_padding_lower(self, lower: int) -> int:
        """Apply padding to lower coordinate with boundary checks."""
        max_height = self.image_original.height - 1
        if lower == max_height:
            return lower
        elif max_height - self.padding <= lower < max_height:
            return max_height
        else:
            return lower + self.padding

    def create_cluster_json_metadata(self, cluster_id: int, bbox_coords: tuple,
                                   cluster_center: np.ndarray, pixel_count: int) -> dict:
        """
        Create JSON metadata for a specific color cluster.

        Args:
            cluster_id (int): The cluster identifier
            bbox_coords (tuple): Bounding box coordinates tuple
            cluster_center (numpy.ndarray): RGB values of cluster center
            pixel_count (int): Number of pixels in this cluster

        Returns:
            dict: JSON metadata structure
        """
        (left_padded, upper_padded, right_padded, lower_padded,
         left, upper, right, lower, center_x, center_y, width, height) = bbox_coords

        json_data = {
            "sample_name": self.sample_name,
            "original_filename": self.raw_image_path.name,
            "image_dimensions": {
                "width": self.image_original.width,
                "height": self.image_original.height
            },
            "cluster_info": {
                "cluster_id": int(cluster_id),
                "pixel_count": int(pixel_count),
                "cluster_center_rgb": [float(cluster_center[0]),
                                     float(cluster_center[1]),
                                     float(cluster_center[2])]
            },
            "bounding_box": {
                "center_x": float(center_x),
                "center_y": float(center_y),
                "width": int(width),
                "height": int(height),
                "coordinates": {
                    "left": int(left),
                    "upper": int(upper),
                    "right": int(right),
                    "lower": int(lower)
                },
                "padded_coordinates": {
                    "left": int(left_padded),
                    "upper": int(upper_padded),
                    "right": int(right_padded),
                    "lower": int(lower_padded)
                }
            }
        }

        return json_data

    def crop_and_save_cluster(self, cluster_id: int, bbox_coords: tuple,
                            image_format: str = 'PNG') -> Tuple[str, str]:
        """
        Crop and save image for a specific color cluster.

        Args:
            cluster_id (int): The cluster identifier
            bbox_coords (tuple): Bounding box coordinates
            image_format (str): Format to save the image ('PNG' or 'JPEG')

        Returns:
            tuple: (crop_filename, crop_no_bkgd_filename) - names of saved images
        """
        # Validate and normalize image format
        image_format = image_format.upper()
        if image_format not in ['PNG', 'JPEG', 'JPG']:
            raise ValueError("Image format must be either 'PNG' or 'JPEG'/'JPG'")

        save_format = 'JPEG' if image_format in ['JPG', 'JPEG'] else image_format
        extension = 'jpg' if save_format == 'JPEG' else 'png'

        # Extract padded coordinates for cropping
        left_padded, upper_padded, right_padded, lower_padded = bbox_coords[:4]
        crop_coords = left_padded, upper_padded, right_padded, lower_padded

        # Crop both images
        cropped_image = self.image_original.crop(crop_coords)
        cropped_image_no_bkgd = self.image_no_bkgd.crop(crop_coords)

        # Generate output filenames
        base_name = self.raw_image_path.stem
        base_no_bkgd_name = self.image_path.stem
        crop_filename = f"color_cluster_{cluster_id}_{base_name}.{extension}"
        crop_no_bkgd_filename = f"color_cluster_{cluster_id}_{base_no_bkgd_name}.{extension}"

        # Save cropped images
        crop_path = self.output_dir / crop_filename
        crop_no_bkgd_path = self.output_dir / crop_no_bkgd_filename
        cropped_image.save(crop_path, format=save_format)
        cropped_image_no_bkgd.save(crop_no_bkgd_path, format=save_format)

        return crop_filename, crop_no_bkgd_filename


    def process_all_clusters(self, image_format: str = 'PNG',
                           combine_json_data: bool = True) -> dict:
        """
        Process all valid color clusters and generate outputs.

        Args:
            image_format (str): Format to save images ('PNG' or 'JPEG')
            combine_json_data (bool): Whether to create a combined JSON file

        Returns:
            dict: Summary of processing results
        """
        if self.valid_clusters is None:
            raise RuntimeError("Must filter valid clusters first")

        if not self.valid_clusters:
            return {"success": False, "message": "No valid clusters to process"}

        print(f"Processing {len(self.valid_clusters)} valid color clusters...")

        results = []
        all_json_data = []

        for cluster_id in sorted(self.valid_clusters.keys()):
            pixel_coords = self.valid_clusters[cluster_id]
            cluster_center = self.cluster_centers[cluster_id]
            pixel_count = len(pixel_coords)

            print(f"Processing color cluster {cluster_id} with {pixel_count} pixels...")

            try:
                # Compute bounding box
                bbox_coords = self.compute_cluster_bounding_box(pixel_coords)

                # Create JSON metadata
                json_data = self.create_cluster_json_metadata(
                    cluster_id, bbox_coords, cluster_center, pixel_count)
                all_json_data.append(json_data)

                # Crop and save images
                crop_files = self.crop_and_save_cluster(
                    cluster_id, bbox_coords, image_format)

                # Save individual JSON metadata
                json_filename = f"color_cluster_{cluster_id}_{self.raw_image_path.stem}.json"
                json_path = self.output_dir / json_filename
                with open(json_path, 'w') as f:
                    json.dump(json_data, f, indent=4)

                results.append({
                    "cluster_id": cluster_id,
                    "pixel_count": pixel_count,
                    "bbox_coords": bbox_coords,
                    "crop_files": crop_files,
                    "json_file": json_filename
                })

            except Exception as e:
                print(f"Error processing cluster {cluster_id}: {e}")
                continue

        # Create combined JSON file if requested
        if combine_json_data and all_json_data:
            self._create_combined_json(all_json_data)

        print(f"Successfully processed {len(results)} color clusters")

        return {
            "success": True,
            "total_clusters": len(self.pixel_map),
            "valid_clusters": len(self.valid_clusters),
            "processed_clusters": len(results),
            "results": results
        }

    def _create_combined_json(self, all_json_data: List[dict]):
        """Create a combined JSON file with all cluster data."""
        combined_filename = f"color_clusters_combined_{self.raw_image_path.stem}.json"
        combined_path = self.output_dir / combined_filename

        combined_data = {
            "sample_name": self.sample_name,
            "original_filename": self.raw_image_path.name,
            "processing_info": {
                "method": "color_clustering",
                "n_clusters": self.n_clusters,
                "min_pixels": self.min_pixels,
                "total_valid_clusters": len(self.valid_clusters)
            },
            "clusters": all_json_data
        }

        with open(combined_path, 'w') as f:
            json.dump(combined_data, f, indent=4)

        print(f"Created combined JSON file: {combined_filename}")

    def process(self, image_format: str = 'PNG',
               combine_json_data: bool = True, random_state: int = 42) -> dict:
        """
        Complete processing pipeline for color-based instance segmentation.

        Args:
            image_format (str): Format to save images ('PNG' or 'JPEG')
            combine_json_data (bool): Whether to create a combined JSON file
            random_state (int): Random state for reproducible clustering

        Returns:
            dict: Summary of processing results
        """
        try:
            print(f"Starting color-based instance segmentation for {self.sample_name}...")
            start_time = time.time()

            # Step 1: Load images
            self.load_images()

            # Step 2: Extract color clusters
            self.extract_color_clusters(random_state=random_state)

            # Step 3: Create pixel coordinate mapping
            self.create_pixel_coordinate_map()

            # Step 4: Filter valid clusters
            self.filter_valid_clusters()

            # Step 5: Process all valid clusters
            results = self.process_all_clusters(image_format, combine_json_data)

            end_time = time.time()

            if results["success"]:
                print(f"\nColor-based segmentation completed successfully!")
                print(f"Total processing time: {end_time - start_time:.2f} seconds")
                print(f"Found {results['valid_clusters']} valid clusters out of {results['total_clusters']} total")
                print(f"Successfully processed {results['processed_clusters']} clusters")
                print(f"Output directory: {self.output_dir}")

            return results

        except Exception as e:
            error_msg = f"Error in color-based segmentation process: {str(e)}"
            print(error_msg)
            return {"success": False, "error": error_msg}


# # Example usage:
# if __name__ == "__main__":
#     # Using direct parameters
#     processor = InstanceSegmentationByColor(
#         image_path="path/to/image_no_background.png",
#         raw_image_path="path/to/raw_image.jpg",
#         sample_name="sample_01",
#         output_dir="path/to/output",
#         n_clusters=5,
#         min_pixels=400,
#         padding=10
#     )

#     results = processor.process()

#     # Using JSON configuration
#     # processor = InstanceSegmentationByColor(config_path="config.json")
#     # results = processor.process()

# ## Usage:
# # The class can be used in two ways:

# # 1. **Direct Parameters**:

# processor = InstanceSegmentationByColor(
#     image_path="image_no_bg.png",
#     raw_image_path="raw_image.jpg",
#     sample_name="sample_01",
#     output_dir="output/",
#     n_clusters=5,
#     min_pixels=400,
#     padding=10
# )
# results = processor.process()

# # 2. **JSON Configuration**:

# processor = InstanceSegmentationByColor(config_path="config.json")
# results = processor.process()

