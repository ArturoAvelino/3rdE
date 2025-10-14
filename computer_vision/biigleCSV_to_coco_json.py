import json
import csv
import logging
from pathlib import Path
from datetime import datetime
from PIL import Image
import shutil


class BiigleCSV_to_COCO_JSON:
    """
    BiigleCSV_to_COCO_JSON - Comprehensive Image Object Processing from CSV Annotations

    A class to process CSV files containing pixel coordinates of objects in images.

    This class reads CSV files with object pixel coordinates, calculates bounding boxes,
    creates cropped images, and generates JSON metadata files organized by class labels.

    NOTE: The first two numbers in the output JSON file with COCO format of the
        bounding box information (see section "bbox" for each object) correspond
        to the pixel coordinates of *top-left corner* of the bounding box! Not to
        the bounding-box center. This, because the standard COCO format has been
        defined like this.
        The second two numbers in the output JSON file with COCO format correspond
        to the width and height of the bounding box.


    ================================================================================
    OVERVIEW AND PURPOSE
    ================================================================================

    The BiigleCSV_to_COCO_JSON class is designed to process CSV files containing pixel
    coordinates of annotated objects in images. It automates the workflow of reading
    object annotations, calculating bounding boxes, cropping individual objects, and
    generating structured metadata files for computer vision and machine learning tasks.

    This class is particularly useful for:
    - Preparing datasets for object detection and classification models
    - Converting pixel-level annotations to standardized bounding box format
    - Creating organized training data from manual annotations
    - Batch processing large datasets with multiple object classes
    - Quality assurance and validation of annotation data

    ================================================================================
    KEY FEATURES AND CAPABILITIES
    ================================================================================

    1. **CSV Annotation Processing**
    - Reads CSV files with object pixel coordinates stored as lists
    - Handles variable-length coordinate arrays (different object sizes)
    - Robust parsing of string-formatted coordinate lists
    - Comprehensive error handling for malformed data

    2. **Automatic Bounding Box Calculation**
    - Computes tight bounding boxes from pixel coordinates
    - Calculates center points, width, and height
    - Handles edge cases and validates coordinate bounds
    - Provides both min/max coordinates and geometric properties

    3. **Intelligent File Organization**
    - Creates class-based directory structure automatically
    - Generates descriptive filenames with object and class identifiers
    - Supports custom filename prefixes for dataset organization
    - Maps image IDs to actual filenames using predefined mapping

    4. **Image Cropping and Processing**
    - Extracts object regions from source images using PIL
    - Maintains image quality with configurable JPEG compression
    - Handles various image formats and error conditions
    - Validates image existence before processing

    5. **Structured Metadata Generation**
    - Creates JSON files with comprehensive object information
    - Includes image metadata, object IDs, and bounding box data
    - Compatible with common machine learning annotation formats
    - Facilitates integration with training pipelines

    6. **Comprehensive Logging and Error Handling**
    - Detailed logging of all processing steps
    - Graceful handling of missing files and invalid data
    - Progress tracking for batch operations
    - Informative error messages for debugging

    ================================================================================
    INPUT DATA FORMAT AND REQUIREMENTS
    ================================================================================

    **CSV File Structure:**
    The input CSV file must contain the following columns:
    - `id`: Unique object identifier (integer)
    - `label_id`: Class/category identifier (integer)
    - `image_id`: Image identifier matching the predefined mapping
    - `points`: String representation of pixel coordinates list

    **Example CSV Row:**
    id,label_id,image_id,shape_id,created_at,updated_at,points 149,126,3,3,2025-05-07 16:24:40,2025-05-07 16:24:40,"[4796,2984,4797,2983,4801,2983,4802,2984,...]"


    **Points Format:**
    Coordinates are stored as alternating x,y pairs: [x1,y1,x2,y2,x3,y3,...]
    - Even indices (0,2,4,...): X-coordinates
    - Odd indices (1,3,5,...): Y-coordinates
    - Coordinate system: Origin at top-left, Y increases downward

    **Image Requirements:**
    - Source images must exist in the specified images directory
    - Image filenames must match the predefined ID-to-filename mapping
    - Supported formats: JPEG, PNG, and other PIL-compatible formats

    ================================================================================
    DETAILED METHOD DESCRIPTIONS
    ================================================================================

    **Initialization Methods:**
    - `__init__()`: Sets up processor with paths, patterns, and configuration
    - `_setup_logging()`: Configures logging for monitoring and debugging
    - `_create_image_mapping()`: Establishes ID-to-filename relationships

    **Data Processing Methods:**
    - `load_csv_data()`: Reads and parses CSV file, converts string coordinates to lists
    - `parse_pixel_coordinates()`: Separates coordinate list into x,y arrays
    - `calculate_bounding_box()`: Computes geometric properties from coordinates

    **File Generation Methods:**
    - `create_json_metadata()`: Generates structured metadata in JSON format
    - `generate_output_filename()`: Creates descriptive filenames following naming convention
    - `create_class_subfolder()`: Establishes directory structure by object class

    **Image Processing Methods:**
    - `crop_object_image()`: Extracts object regions using bounding box coordinates
    - `process_single_object()`: Complete processing pipeline for individual objects
    - `process_all_objects()`: Batch processing orchestration with progress tracking

    ================================================================================
    COMPREHENSIVE USAGE EXAMPLES
    ================================================================================

    **Basic Usage - Process All Objects:**
    ```python
    from csv_object_processor import BiigleCSV_to_COCO_JSON

    # Initialize processor with required paths
    processor = BiigleCSV_to_COCO_JSON(
     csv_file="annotations/objects.csv",
     images_path="images/source/",
     filename_pattern="capt*.jpg",
     output_crops_path="output/cropped_objects/",
     json_label_tree_path="labels/categories.json"
    )

    # Process entire dataset
    processor.process_all_objects()
    ```

    # ##########################


    **Advanced Usage - Custom Configuration:**
    ``` python
    # Initialize with custom prefix and specific paths
    processor = BiigleCSV_to_COCO_JSON(
     csv_file="/data/annotations/dataset_v2.csv",
     images_path="/data/images/raw/",
     filename_pattern="capture_*.jpg",
     output_crops_path="/output/processed/",
     prefix_filename="dataset_v2",
     json_label_tree_path="/data/labels/categories.json"
    )

    # Load data first to inspect
    csv_data = processor.load_csv_data()
    print(f"Loaded {len(csv_data)} annotations")

    # Process all objects with logging
    processor.process_all_objects()
    ```
    **Processing Individual Objects:**
    ``` python
    # Load CSV data
    csv_data = processor.load_csv_data()

    # Process specific objects by filtering
    for row in csv_data:
     if int(row['label_id']) == 126:  # Process only class 126
         try:
             processor.process_single_object(row)
             print(f"Processed object {row['id']} successfully")
         except Exception as e:
             print(f"Failed to process object {row['id']}: {e}")
    ```
    **Bounding Box Calculation Only:**
    ``` python
    # Calculate bounding boxes without image processing
    csv_data = processor.load_csv_data()

    for row in csv_data:
     try:
         bbox_info = processor.calculate_bounding_box(row['points'])
         print(
             f"Object {row['id']}: Center=({bbox_info['center_x']}, {bbox_info['center_y']}), "
             f"Size={bbox_info['box_width']}x{bbox_info['box_height']}")
     except Exception as e:
         print(f"Error calculating bbox for object {row['id']}: {e}")
    ```
    **Quality Assurance and Validation:**
    ``` python
    # Validate data before processing
    csv_data = processor.load_csv_data()
    valid_objects = []
    invalid_objects = []

    for row in csv_data:
     try:
         # Test coordinate parsing
         x_coords, y_coords = processor.parse_pixel_coordinates(row['points'])

         # Validate image exists
         image_id = int(row['image_id'])
         if image_id in processor.image_mapping:
             image_path = processor.images_path / processor.image_mapping[
                 image_id]
             if image_path.exists():
                 valid_objects.append(row)
             else:
                 invalid_objects.append(
                     (row['id'], f"Image not found: {image_path}"))
         else:
             invalid_objects.append((row['id'], f"Unknown image_id: {image_id}"))
     except Exception as e:
         invalid_objects.append((row['id'], str(e)))

    print(f"Valid objects: {len(valid_objects)}")
    print(f"Invalid objects: {len(invalid_objects)}")
    ```
    ================================================================================ OUTPUT FILES AND DIRECTORY STRUCTURE ================================================================================
    **Directory Structure:**
    ```
    output_crops_path/
    ├── 87/                           # Class subdirectory (label_id)
    │   ├── capt0011_object_151_class_87.json
    │   ├── capt0011_object_151_class_87.jpg
    │   └── ...
    ├── 117/                          # Another class subdirectory
    │   ├── capt0010_object_150_class_117.json
    │   ├── capt0010_object_150_class_117.jpg
    │   └── ...
    └── 126/                          # Third class subdirectory
     ├── capt0004_object_149_class_126.json
     ├── capt0004_object_149_class_126.jpg
     └── ...
    ```

    """

    def __init__(self, csv_file, images_path, filename_pattern,
                 output_crops_path, prefix_filename="", json_label_tree_path=None):
        """
        Initialize the BiigleCSV_to_COCO_JSON.

        Args:
            csv_file (str): Path to the CSV file containing object annotations
            images_path (str): Path to the directory containing source images
            filename_pattern (str): Pattern to match image filenames (e.g., "capt*.jpg")
            output_crops_path (str): Path to the output directory for cropped images
            prefix_filename (str): Optional prefix for output filenames
            json_label_tree_path (str): Path to JSON file containing category names mapping
        """
        # Convert string paths to Path objects
        self.csv_file = Path(csv_file)
        self.images_path = Path(images_path)
        self.filename_pattern = filename_pattern
        self.output_crops_path = Path(output_crops_path)
        self.prefix_filename = prefix_filename
        self.json_label_tree_path = Path(
            json_label_tree_path) if json_label_tree_path else None

        # Create output directory
        self.output_crops_path.mkdir(parents=True, exist_ok=True)

        # Set up logging
        self._setup_logging()

        # Create image mapping
        self.image_mapping = self._create_image_mapping()

        # Load category names mapping
        self.category_names = self._load_category_names()

    def _setup_logging(self):
        """Set up logging configuration."""
        log_file = self.output_crops_path / "processing_log.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _load_category_names(self):
        """
        Load category names from JSON file.

        Returns:
            dict: Mapping from category ID to category name
        """
        category_names = {}

        if not self.json_label_tree_path or not self.json_label_tree_path.exists():
            self.logger.warning(
                f"Labels JSON file not found at {self.json_label_tree_path}. Using default 'arthropod' name.")
            return category_names

        try:
            with open(self.json_label_tree_path, 'r', encoding='utf-8') as f:
                labels_data = json.load(f)

            # Extract labels and create mapping
            labels_list = labels_data.get('labels', [])
            for label in labels_list:
                category_id = label.get('id')
                category_name = label.get('name')
                if category_id is not None and category_name:
                    category_names[category_id] = category_name

            self.logger.info(
                f"Loaded {len(category_names)} category names from {self.json_label_tree_path}")

        except Exception as e:
            self.logger.error(
                f"Error loading category names from {self.json_label_tree_path}: {e}")

        return category_names

    def _get_category_name(self, category_id):
        """
        Get category name for given category ID.

        Args:
            category_id (int): The category ID

        Returns:
            str: Category name, defaults to "arthropod" if not found
        """
        return self.category_names.get(category_id, "arthropod")


    # def _create_image_mapping(self):
    #     """
    #     Create a mapping of image_id to filename based on the pattern.
    #
    #     Returns:
    #         dict: Dictionary mapping image_id to filename
    #     """
    #     try:
    #         # Get all files matching the pattern
    #         matching_files = list(self.images_path.glob(self.filename_pattern))
    #
    #         if not matching_files:
    #             self.logger.warning(
    #                 f"No files found matching pattern '{self.filename_pattern}' in {self.images_path}")
    #             return {}
    #
    #         # Sort files to ensure consistent mapping
    #         matching_files.sort()
    #
    #         # Create mapping: image_id (1-based) -> filename
    #         image_mapping = {}
    #         for idx, file_path in enumerate(matching_files, start=1):
    #             image_mapping[idx] = file_path.name
    #
    #         self.logger.info(
    #             f"Created image mapping for {len(image_mapping)} images")
    #         return image_mapping
    #
    #     except Exception as e:
    #         self.logger.error(f"Error creating image mapping: {e}")
    #         return {}


    def _create_image_mapping(self):
        """
        Create mapping from image_id to filename based on the provided mapping.

        Returns:
            dict: Mapping from image_id to filename
        """
        return {
            3: "capt0004.jpg",
            4: "capt0010.jpg",
            5: "capt0011.jpg",
            6: "capt0012.jpg",
            7: "capt0013.jpg",
            8: "capt0017.jpg",
            9: "capt0018.jpg",
            10: "capt0019.jpg",
            11: "capt0020.jpg",
            12: "capt0021.jpg",
            13: "capt0022.jpg",
            14: "capt0025.jpg",
            15: "capt0026.jpg",
            16: "capt0027.jpg",
            17: "capt0028.jpg",
            18: "capt0029.jpg",
            19: "capt0030.jpg",
            20: "capt0033.jpg",
            21: "capt0034.jpg",
            105: "capt0035.jpg",
            106: "capt0036.jpg",
            107: "capt0037.jpg",
            108: "capt0038.jpg",
            109: "capt0039.jpg",
            110: "capt0040.jpg",
            111: "capt0041.jpg",
            112: "capt0042.jpg",
            113: "capt0043.jpg",
            114: "capt0044.jpg",
            115: "capt0045.jpg",
            116: "capt0046.jpg",
            117: "capt0047.jpg",
            118: "capt0048.jpg",
            119: "capt0049.jpg",
            120: "capt0050.jpg",
            121: "capt0051.jpg",
            122: "capt0052.jpg",
            123: "capt0053.jpg",
            124: "capt0054.jpg",
            125: "capt0055.jpg",
            126: "capt0057.jpg",
            127: "capt0058.jpg",
            128: "capt0059.jpg",
            129: "capt0060.jpg",
            130: "capt0061.jpg",
            131: "capt0062.jpg",
            132: "capt0064.jpg",
            133: "capt0065.jpg",
            134: "capt0066.jpg",
            135: "capt0067.jpg",
            136: "capt0068.jpg",
            137: "capt0069.jpg",
            138: "capt0070.jpg",
            139: "capt0073.jpg",
            140: "capt0074.jpg",
            141: "capt0075.jpg",
            142: "capt0076.jpg",
            143: "capt0077.jpg",
            144: "capt0078.jpg",
            145: "capt0083.jpg",
            146: "capt0084.jpg",
            147: "capt0086.jpg",
            148: "capt0090.jpg",
            149: "capt0091.jpg"
        }


    def get_image_dimensions(self, image_path):
        """
        Get the dimensions of an image file.

        Args:
            image_path (Path): Path to the image file

        Returns:
            tuple: (width, height) of the image

        Raises:
            Exception: If the image cannot be opened or processed
        """
        try:
            with Image.open(image_path) as img:
                return img.size  # Returns (width, height)
        except Exception as e:
            self.logger.error(f"Error getting dimensions for {image_path}: {e}")
            raise

    def load_csv_data(self):
        """
        Load and parse CSV data, converting string coordinate lists to Python lists.

        Returns:
            list: List of dictionaries containing parsed CSV data

        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            Exception: If there's an error reading or parsing the CSV file
        """
        if not self.csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")

        csv_data = []
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row_num, row in enumerate(reader,
                                              start=2):  # start=2 because row 1 is header
                    try:
                        # Parse the points string to a Python list
                        if 'points' in row and row['points']:
                            # Remove surrounding quotes and brackets, then split
                            points_str = row['points'].strip('"[]')
                            if points_str:
                                # Split by comma and convert to integers with validation
                                raw_coordinates = points_str.split(',')
                                validated_coordinates = []

                                for i, coord_str in enumerate(raw_coordinates):
                                    try:
                                        # Strip whitespace and convert to float first, then round to nearest integer
                                        coord_float = float(coord_str.strip())
                                        coord_value = int(round(coord_float))
                                        validated_coordinates.append(
                                            coord_value)
                                    except ValueError as coord_error:
                                        self.logger.error(
                                            f"Row {row_num}: Invalid coordinate value '{coord_str}' at position {i}: {coord_error}")
                                        raise ValueError(
                                            f"Invalid coordinate value: {coord_str}")
                                    except Exception as coord_error:
                                        self.logger.error(
                                            f"Row {row_num}: Unexpected error parsing coordinate '{coord_str}' at position {i}: {coord_error}")
                                        raise

                                # Ensure all values are integers before assigning
                                row['points'] = validated_coordinates
                            else:
                                row['points'] = []
                        else:
                            self.logger.warning(
                                f"Row {row_num}: No 'points' data found")
                            row['points'] = []

                        # Additional validation: ensure points list has even number of elements
                        if len(row['points']) % 2 != 0:
                            self.logger.error(
                                f"Row {row_num}: Points list has odd number of elements ({len(row['points'])})")
                            continue

                        csv_data.append(row)

                    except ValueError as e:
                        self.logger.error(
                            f"Row {row_num}: Error parsing points data: {e}")
                        continue
                    except Exception as e:
                        self.logger.error(
                            f"Row {row_num}: Unexpected error: {e}")
                        continue

        except Exception as e:
            self.logger.error(f"Error reading CSV file {self.csv_file}: {e}")
            raise

        self.logger.info(f"Loaded {len(csv_data)} rows from CSV file")
        return csv_data


    def parse_pixel_coordinates(self, points_list):
        """
        Parse pixel coordinates from a list into separate x and y coordinate arrays.

        Args:
            points_list (list): List of coordinates in format [x1, y1, x2, y2, ...]

        Returns:
            tuple: (x_coordinates, y_coordinates) as separate lists

        Raises:
            ValueError: If the points list has an odd number of elements
        """
        if len(points_list) % 2 != 0:
            raise ValueError(
                "Points list must have an even number of elements (x, y pairs)")

        x_coords = []
        y_coords = []

        for i in range(0, len(points_list), 2):
            x_coords.append(points_list[i])
            y_coords.append(points_list[i + 1])

        return x_coords, y_coords

    def calculate_bounding_box(self, points_list):
        """
        Calculate bounding box information from pixel coordinates.

        Args:
            points_list (list): List of pixel coordinates [x1, y1, x2, y2, ...]

        Returns:
            dict: Dictionary containing bounding box information with keys:
                - min_x, min_y: Top-left corner coordinates
                - max_x, max_y: Bottom-right corner coordinates
                - center_x, center_y: Center point coordinates
                - box_width, box_height: Dimensions of the bounding box
                - box_area: Area of the bounding box

        Raises:
            ValueError: If the points list is empty or invalid
        """
        if not points_list:
            raise ValueError("Points list cannot be empty")

        try:
            x_coords, y_coords = self.parse_pixel_coordinates(points_list)

            # Calculate bounding box
            min_x = min(x_coords)
            max_x = max(x_coords)
            min_y = min(y_coords)
            max_y = max(y_coords)

            # Calculate center and dimensions
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            box_width = max_x - min_x
            box_height = max_y - min_y
            box_area = box_width * box_height

            return {
                'min_x': min_x,
                'min_y': min_y,
                'max_x': max_x,
                'max_y': max_y,
                'center_x': center_x,
                'center_y': center_y,
                'box_width': box_width,
                'box_height': box_height,
                'box_area': box_area
            }

        except Exception as e:
            self.logger.error(f"Error calculating bounding box: {e}")
            raise

    def create_json_metadata(self, row_data, bbox_info, image_path=None):
        """
        Create a JSON metadata structure for an object.

        Args:
            row_data (dict): Row data from CSV
            bbox_info (dict): Bounding box information
            image_path (Path): Path to the source image (optional)

        Returns:
            dict: JSON metadata structure
        """
        image_id = int(row_data['image_id'])
        filename = self.image_mapping.get(image_id, f"unknown_{image_id}.jpg")

        # Extract base filename without extension for sample_name
        sample_name = Path(filename).stem

        current_time = datetime.now().isoformat() + "-01:00"
        current_year = datetime.now().strftime("%Y")

        # Get actual image dimensions
        if image_path and image_path.exists():
            try:
                width, height = self.get_image_dimensions(image_path)
            except Exception as e:
                self.logger.warning(
                    f"Could not get dimensions for {image_path}, using defaults: {e}")
                width, height = 6000, 4000  # fallback values
        else:
            width, height = 6000, 4000  # fallback values

        # Get category name using the mapping
        category_id = int(row_data['label_id'])
        category_name = self._get_category_name(category_id)

        json_data = {
            "info": {
                "year": current_year,
                "version": "1",
                "description": "arthropods bounding boxes",
                "contributor": "Arturo_Avelino",
                "url": "https://www.unine.ch/biolsol",
                "date_created": current_time
            },
            "licenses": [
                {
                    "id": 1,
                    "url": "https://www.unine.ch/biolsol",
                    "name": "Research"
                }
            ],
            "categories": [
                {
                    "id": category_id,
                    "name": category_name,
                    "supercategory": "none"
                }
            ],
            "images": [
                {
                    "id": sample_name,
                    "license": 1,
                    "file_name": filename,
                    "height": height,
                    "width": width,
                    "date_captured": row_data['created_at']
                }
            ],
            "annotations": [
                {
                    "id": int(row_data['id']),
                    "image_id": image_id,
                    "category_id": category_id,
                    "bbox": [
                        bbox_info['center_x'],
                        bbox_info['center_y'],
                        bbox_info['box_width'],
                        bbox_info['box_height']
                    ],
                    "area": bbox_info['box_area'],
                    "segmentation": [],
                    "iscrowd": 0
                }
            ]
        }

        return json_data

    def group_objects_by_image_id(self, csv_data):
        """
        Group objects by their image_id for merged processing.

        Args:
            csv_data (list): List of dictionaries from CSV data

        Returns:
            dict: Dictionary where keys are image_ids and values are lists of objects
        """
        grouped_objects = {}

        for row in csv_data:
            try:
                image_id = int(row['image_id'])
                if image_id not in grouped_objects:
                    grouped_objects[image_id] = []
                grouped_objects[image_id].append(row)
            except (ValueError, KeyError) as e:
                self.logger.warning(
                    f"Skipping row due to invalid image_id: {e}")
                continue

        self.logger.info(
            f"Grouped {len(csv_data)} objects into {len(grouped_objects)} image groups")
        return grouped_objects

    def create_merged_json_metadata(self, image_id, objects_list,
                                    output_path=None):
        """
        Create a merged JSON metadata file for all objects belonging to the same image_id.

        Args:
            image_id (int): The image ID for grouping objects
            objects_list (list): List of object dictionaries from CSV
            output_path (Path): Optional output path. If None, uses default location.

        Returns:
            dict: The merged JSON metadata structure
        """
        try:
            # Get image information
            filename = self.image_mapping.get(image_id,
                                              f"unknown_{image_id}.jpg")
            sample_name = Path(filename).stem
            image_path = self.images_path / filename

            # Get image dimensions
            if image_path.exists():
                try:
                    width, height = self.get_image_dimensions(image_path)
                except Exception as e:
                    self.logger.warning(
                        f"Could not get dimensions for {image_path}, using defaults: {e}")
                    width, height = 6000, 4000
            else:
                width, height = 6000, 4000

            current_time = datetime.now().isoformat() + "-01:00"
            current_year = datetime.now().strftime("%Y")

            # Create an annotation list
            annotations = []
            categories_dict = {}  # Use dict to avoid duplicates

            for obj_data in objects_list:
                # Calculate a bounding box for each object
                bbox_info = self.calculate_bounding_box(obj_data['points'])

                # Create annotation entry
                annotation = {
                    "id": int(obj_data['id']),
                    "image_id": image_id,
                    "category_id": int(obj_data['label_id']),
                    "bbox": [
                        bbox_info['min_x'],
                        bbox_info['min_y'],
                        bbox_info['box_width'],
                        bbox_info['box_height']
                    ],
                    "area": bbox_info['box_area'],
                    "segmentation": [],
                    "iscrowd": 0
                }
                annotations.append(annotation)

                # Add a category (using dict to avoid duplicates)
                category_id = int(obj_data['label_id'])
                if category_id not in categories_dict:
                    category_name = self._get_category_name(category_id)
                    categories_dict[category_id] = {
                        "id": category_id,
                        "name": category_name,
                        "supercategory": "none"
                    }

            # Convert categories dict to list
            categories = list(categories_dict.values())

            # Create the merged JSON structure
            merged_json = {
                "info": {
                    "year": current_year,
                    "version": "1",
                    "description": "arthropods bounding boxes",
                    "contributor": "Arturo_Avelino",
                    "url": "https://www.unine.ch/biolsol",
                    "date_created": current_time
                },
                "licenses": [
                    {
                        "id": 1,
                        "url": "https://www.unine.ch/biolsol",
                        "name": "Research"
                    }
                ],
                "categories": categories,
                "images": [
                    {
                        "id": image_id,
                        "license": 1,
                        "file_name": filename,
                        "height": height,
                        "width": width,
                        "date_captured": objects_list[0][
                            'created_at'] if objects_list else current_time
                    }
                ],
                "annotations": annotations
            }

            # Save to file if output_path is provided
            if output_path:
                output_path.mkdir(parents=True, exist_ok=True)
                json_filename = f"{sample_name}_image_{image_id}_merged.json"
                json_file_path = output_path / json_filename

                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(merged_json, f, indent=4)

                self.logger.info(
                    f"Saved merged JSON for image_id {image_id} with {len(annotations)} objects to {json_file_path}")

            return merged_json

        except Exception as e:
            self.logger.error(
                f"Error creating merged JSON for image_id {image_id}: {e}")
            raise

    def merge_json_files_by_image_id(self, output_merged_path=None):
        """
        Main method to merge all individual JSON files by image_id into consolidated files.

        Args:
            output_merged_path (str): Output directory for merged JSON files.
                                    If None, creates 'merged_json' subdirectory in output_crops_path.
        """
        try:
            # Set default output path if none provided
            if output_merged_path is None:
                output_merged_path = self.output_crops_path / "merged_json"
            else:
                output_merged_path = Path(output_merged_path)

            # Load CSV data and group by image_id
            csv_data = self.load_csv_data()
            grouped_objects = self.group_objects_by_image_id(csv_data)

            if not grouped_objects:
                self.logger.warning("No grouped objects found")
                return

            # Process each image group
            total_images = len(grouped_objects)
            processed_images = 0

            for image_id, objects_list in grouped_objects.items():
                try:
                    # Create merged JSON for this image_id
                    self.create_merged_json_metadata(image_id, objects_list,
                                                     output_merged_path)
                    processed_images += 1

                except Exception as e:
                    self.logger.error(
                        f"Failed to merge JSON for image_id {image_id}: {e}")
                    continue

            self.logger.info(
                f"JSON merging complete: {processed_images}/{total_images} image groups processed successfully")
            self.logger.info(
                f"Merged JSON files saved to: {output_merged_path}")

        except Exception as e:
            self.logger.error(f"Error in merge_json_files_by_image_id: {e}")
            raise

    def generate_output_filename(self, row_data, file_extension):
        """
        Generate output filename based on image mapping and row data.

        Args:
            row_data (dict): Row data from CSV containing object information
            file_extension (str): File extension (e.g., '.jpg', '.json')

        Returns:
            str: Generated filename

        Raises:
            ValueError: If required data is missing from row_data
        """
        try:
            # Get basic information from row data
            object_id = row_data['id']
            label_id = row_data['label_id']
            image_id = int(row_data['image_id'])

            # Get the actual image filename from mapping
            if image_id in self.image_mapping:
                image_filename = self.image_mapping[image_id]
                # Extract base filename without extension
                base_name = Path(image_filename).stem
            else:
                # Fallback if image_id not found in mapping
                base_name = f"unknown_image_{image_id}"
                self.logger.warning(
                    f"Image ID {image_id} not found in mapping, using fallback name")

            # Create output filename with prefix if provided
            if self.prefix_filename:
                filename = f"{self.prefix_filename}_{base_name}_object_{object_id}_class_{label_id}{file_extension}"
            else:
                filename = f"{base_name}_object_{object_id}_class_{label_id}{file_extension}"

            return filename

        except KeyError as e:
            raise ValueError(f"Required field missing from row data: {e}")
        except Exception as e:
            self.logger.error(f"Error generating filename: {e}")
            raise

    def create_class_subfolder(self, label_id):
        """
        Create a subfolder for the given class label if it doesn't exist.

        Args:
            label_id (str or int): The class label identifier

        Returns:
            Path: Path to the created subfolder
        """
        subfolder_path = self.output_crops_path / str(label_id)
        subfolder_path.mkdir(parents=True, exist_ok=True)
        return subfolder_path

    def crop_object_image(self, image_path, bbox_info, output_path):
        """
        Crop an object from an image using bounding box coordinates and save it.

        Args:
            image_path (Path): Path to the source image
            bbox_info (dict): Bounding box information containing coordinates
            output_path (Path): Path where the cropped image will be saved

        Raises:
            FileNotFoundError: If the source image doesn't exist
            Exception: If there's an error during image processing
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Source image not found: {image_path}")

        try:
            with Image.open(image_path) as img:
                # Define crop box (left, upper, right, lower)
                crop_box = (
                    int(bbox_info['min_x']),
                    int(bbox_info['min_y']),
                    int(bbox_info['max_x']),
                    int(bbox_info['max_y'])
                )

                # Crop the image
                cropped_img = img.crop(crop_box)

                # Save the cropped image
                cropped_img.save(output_path, format='JPEG', quality=95)

        except Exception as e:
            self.logger.error(f"Error cropping image {image_path}: {e}")
            raise

    def process_single_object(self, row_data):
        """
        Process a single object: calculate bounding box, crop image, and create JSON metadata.

        Args:
            row_data (dict): Single row of data from CSV file

        Returns:
            dict: Processing results with status and file paths

        Raises:
            Exception: If processing fails for any reason
        """
        try:
            # Validate required fields
            required_fields = ['id', 'label_id', 'image_id', 'points']
            for field in required_fields:
                if field not in row_data:
                    raise ValueError(
                        f"Required field '{field}' missing from row data")

            object_id = row_data['id']
            label_id = row_data['label_id']
            image_id = int(row_data['image_id'])

            # Calculate bounding box
            bbox_info = self.calculate_bounding_box(row_data['points'])

            # Get image path
            if image_id not in self.image_mapping:
                raise ValueError(
                    f"Image ID {image_id} not found in image mapping")

            image_filename = self.image_mapping[image_id]
            image_path = self.images_path / image_filename

            # Create class subfolder
            subfolder_path = self.create_class_subfolder(label_id)

            # Generate output filenames
            jpg_filename = self.generate_output_filename(row_data, '.jpg')
            json_filename = self.generate_output_filename(row_data, '.json')

            # Full output paths
            jpg_output_path = subfolder_path / jpg_filename
            json_output_path = subfolder_path / json_filename

            # Crop and save image
            self.crop_object_image(image_path, bbox_info, jpg_output_path)

            # Create and save JSON metadata
            json_metadata = self.create_json_metadata(row_data, bbox_info,
                                                      image_path)
            with open(json_output_path, 'w', encoding='utf-8') as f:
                json.dump(json_metadata, f, indent=4)

            result = {
                'status': 'success',
                'object_id': object_id,
                'image_path': jpg_output_path,
                'json_path': json_output_path,
                'bbox_info': bbox_info
            }

            self.logger.info(
                f"Successfully processed object {object_id} from image {image_id}")
            return result

        except Exception as e:
            self.logger.error(
                f"Error processing object {row_data.get('id', 'unknown')}: {e}")
            raise

    def process_all_objects(self):
        """
        Process all objects from the CSV file: crop images and generate JSON metadata files.

        This method orchestrates the entire processing workflow:
        1. Load CSV data
        2. Process each object individually
        3. Create cropped images and JSON metadata
        4. Organize output by class labels

        Returns:
            dict: Summary statistics of the processing results
        """
        try:
            # Load CSV data
            csv_data = self.load_csv_data()

            if not csv_data:
                self.logger.warning("No data found in CSV file")
                return {'processed': 0, 'failed': 0, 'total': 0}

            total_objects = len(csv_data)
            processed_count = 0
            failed_count = 0
            failed_objects = []

            self.logger.info(f"Starting processing of {total_objects} objects")

            # Process each object
            for idx, row_data in enumerate(csv_data, 1):
                try:
                    self.process_single_object(row_data)
                    processed_count += 1

                    # Log progress every 100 objects
                    if idx % 100 == 0:
                        self.logger.info(
                            f"Progress: {idx}/{total_objects} objects processed")

                except Exception as e:
                    failed_count += 1
                    object_id = row_data.get('id', 'unknown')
                    failed_objects.append(
                        {'object_id': object_id, 'error': str(e)})
                    self.logger.error(
                        f"Failed to process object {object_id}: {e}")

            # Log final results
            self.logger.info(
                f"Processing complete: {processed_count} successful, {failed_count} failed")

            if failed_objects:
                self.logger.warning(
                    f"Failed objects: {[obj['object_id'] for obj in failed_objects[:10]]}")

            return {
                'processed': processed_count,
                'failed': failed_count,
                'total': total_objects,
                'failed_objects': failed_objects
            }

        except Exception as e:
            self.logger.error(f"Error in process_all_objects: {e}")
            raise

# # Example usage
# if __name__ == "__main__":
#     # Initialize the processor
#     processor = BiigleCSV_to_COCO_JSON(
#         csv_file="path/to/your/file.csv",
#         images_path="path/to/images/directory",
#         filename_pattern="capt*.jpg",
#         output_crops_path="output/cropped_objects/",
#         prefix_filename=""  # Optional prefix
# 		json_label_tree_path="labels/categories.json"
#     )
#
#     # Process all objects
#     processor.process_all_objects()
#
#
# # Basic usage - merge all JSON files
# processor = BiigleCSV_to_COCO_JSON(
#     csv_file="annotations.csv",
#     images_path="images/",
#     filename_pattern="capt*.jpg",
#     output_crops_path="output/"
# )
#
# # Merge JSON files (saves to output/merged_json/)
# processor.merge_json_files_by_image_id()
#
# # Or specify custom output path
# processor.merge_json_files_by_image_id("custom/merged/path")
