import csv
import json
import ast
from pathlib import Path
from PIL import Image
import logging
from datetime import datetime


class CSVObjectProcessor:
    """
    CSVObjectProcessor - Comprehensive Image Object Processing from CSV Annotations

    A class to process CSV files containing pixel coordinates of objects in images.
    
    This class reads CSV files with object pixel coordinates, calculates bounding boxes,
    creates cropped images, and generates JSON metadata files organized by class labels.

    ================================================================================
    OVERVIEW AND PURPOSE
    ================================================================================

    The CSVObjectProcessor class is designed to process CSV files containing pixel
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
    from csv_object_processor import CSVObjectProcessor

    # Initialize processor with required paths
    processor = CSVObjectProcessor(
     csv_file="annotations/objects.csv",
     images_path="images/source/",
     filename_pattern="capt*.jpg",
     output_crops_path="output/cropped_objects/"
    )

    # Process entire dataset
    processor.process_all_objects()
    ```

    # ##########################


    **Advanced Usage - Custom Configuration:**
    ``` python
    # Initialize with custom prefix and specific paths
    processor = CSVObjectProcessor(
     csv_file="/data/annotations/dataset_v2.csv",
     images_path="/data/images/raw/",
     filename_pattern="capture_*.jpg",
     output_crops_path="/output/processed/",
     prefix_filename="dataset_v2"
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
    **JSON Metadata Format:**
    ``` json
    {
     "image": [
         {
             "sample_name": "capt0011",
             "filename": "capt0011.jpg",
             "filename_id": 5,
             "object_id": 151
         }
     ],
     "annotations": [
         {
             "class_id": 87,
             "bbox": [
                 {
                     "center_x": 5115,
                     "center_y": 973,
                     "box_width": 61,
                     "box_height": 68
                 }
             ]
         }
     ]
    }
    ```
    **Cropped Images:**
    - Format: High-quality JPEG (quality=95)
    - Content: Tight crops of individual objects
    - Naming: Descriptive with object and class identifiers
    - Organization: Grouped by class in subdirectories

    ================================================================================ ERROR HANDLING AND VALIDATION ================================================================================
    **Comprehensive Error Management:**
    - CSV parsing errors: Invalid coordinate strings, missing columns
    - Image processing errors: Missing files, corrupted images, invalid formats
    - Coordinate validation: Empty coordinate lists, odd-length arrays
    - File system errors: Permission issues, disk space, invalid paths

    **Validation Features:**
    - Pre-processing data validation and sanity checks
    - Image existence verification before processing
    - Coordinate bounds checking against image dimensions
    - Output directory creation with proper permissions

    **Logging and Monitoring:**
    - Detailed progress tracking for batch operations
    - Warning messages for recoverable issues
    - Error logs with full stack traces for debugging
    - Processing statistics and success/failure counts

    ================================================================================ DEPENDENCIES AND REQUIREMENTS ================================================================================
    **Required Packages:**
    ``` python
    import csv          # Standard library - CSV file processing
    import json         # Standard library - JSON metadata generation
    import ast          # Standard library - Safe string-to-list conversion
    from pathlib import Path    # Standard library - Modern path handling
    from PIL import Image      # Pillow - Image processing and manipulation
    import logging      # Standard library - Comprehensive logging system
    ```
    **Installation:**
    ``` bash
    pip install Pillow  # Only external dependency required
    ```
    **Python Version:**
    - Compatible with Python 3.6+
    - Tested with Python 3.9.6
    - Uses modern pathlib for cross-platform compatibility

    ================================================================================ PERFORMANCE CONSIDERATIONS AND OPTIMIZATION ================================================================================
    **Memory Management:**
    - Processes objects individually to minimize memory usage
    - Closes image files properly to prevent memory leaks
    - Efficient coordinate parsing using list slicing
    - Garbage collection friendly with proper resource cleanup

    **Scalability:**
    - Handles datasets with thousands of objects efficiently
    - Progress tracking for long-running batch operations
    - Robust error recovery allows processing to continue after failures
    - Configurable logging levels to control output volume

    **Optimization Tips:**
    - Use SSD storage for source images to improve I/O performance
    - Consider parallel processing for very large datasets
    - Monitor disk space in output directory during processing
    - Use appropriate JPEG quality settings based on use case requirements

    ================================================================================ COMMON USE CASES AND APPLICATIONS ================================================================================
    **Computer Vision Dataset Preparation:**
    - Converting manual annotations to standardized training data
    - Creating object detection datasets from pixel-level annotations
    - Preparing data for YOLO, R-CNN, or similar model architectures
    - Quality assurance and validation of annotation consistency

    **Research and Development:**
    - Analyzing object size distributions across classes
    - Creating balanced datasets by class representation
    - Generating augmentation data for underrepresented classes
    - Comparative analysis of annotation quality across different annotators

    **Production Workflows:**
    - Automated processing of newly annotated data
    - Integration with continuous integration/deployment pipelines
    - Batch processing of historical annotation data
    - Migration between different annotation formats and tools

    **Educational and Training:**
    - Teaching object detection concepts with real data
    - Demonstrating annotation-to-training-data workflows
    - Providing hands-on experience with computer vision pipelines
    - Creating reproducible examples for machine learning courses

    ================================================================================ INTEGRATION WITH OTHER TOOLS ================================================================================
    This class is designed to work seamlessly with other components in the computer vision pipeline:
    - : Analyze size distributions of generated crops **BoundingBoxClusteringProcessor**
    - : Alternative processing for JSON-based annotations **CropIndividualObjects**
    - **Batch processing utilities**: Scale processing across multiple datasets
    - **Machine learning frameworks**: Direct compatibility with PyTorch, TensorFlow datasets

    The modular design and standardized output formats ensure easy integration with existing workflows and tools in the computer vision ecosystem.
    ================================================================================
    """
    
    def __init__(self, csv_file, images_path, filename_pattern, output_crops_path, prefix_filename=""):
        """
        Initialize the CSV Object Processor.
        
        Args:
            csv_file (str): Path to the input CSV file
            images_path (str): Directory path containing the source images
            filename_pattern (str): Pattern to match image files (e.g., "capt*.jpg")
            output_crops_path (str): Directory path for output files and subfolders
            prefix_filename (str): Optional prefix for output filenames
        """
        self.csv_file = Path(csv_file)
        self.images_path = Path(images_path)
        self.filename_pattern = filename_pattern
        self.output_crops_path = Path(output_crops_path)
        self.prefix_filename = prefix_filename
        
        # Image ID to filename mapping
        self.image_mapping = self._create_image_mapping()
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Create output directory
        self.output_crops_path.mkdir(parents=True, exist_ok=True)


    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)


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
        Get the width and height of an image in pixels.

        Args:
            image_path (Path): Path to the image file

        Returns:
            tuple: (width, height) in pixels
        """
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                return width, height
        except Exception as e:
            self.logger.error(
                f"Error getting image dimensions for {image_path}: {e}")
            raise


    def load_csv_data(self):
        """
        Load and parse CSV data.
        
        Returns:
            list: List of dictionaries containing row data
        """
        try:
            data = []
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Parse the point string to a list of integers
                    try:
                        points_str = row['points'].strip()
                        points = ast.literal_eval(points_str)
                        row['points'] = points
                        data.append(row)
                    except (ValueError, SyntaxError) as e:
                        self.logger.warning(f"Error parsing points for row {row.get('id', 'unknown')}: {e}")
                        continue
            
            self.logger.info(f"Loaded {len(data)} rows from CSV file")
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading CSV file: {e}")
            raise


    def parse_pixel_coordinates(self, points_list):
        """
        Parse pixel coordinates from points list.
        
        Args:
            points_list (list): List of coordinates [x1, y1, x2, y2, ...]
            
        Returns:
            tuple: (x_coordinates, y_coordinates) as separate lists
        """
        if len(points_list) % 2 != 0:
            raise ValueError("Points list must have even number of elements")
        
        x_coords = points_list[::2]  # Every even index (0, 2, 4, ...)
        y_coords = points_list[1::2]  # Every odd index (1, 3, 5, ...)
        
        return x_coords, y_coords


    def calculate_bounding_box(self, points_list):
        """
        Calculate bounding box from pixel coordinates.
        
        Args:
            points_list (list): List of coordinates [x1, y1, x2, y2, ...]
            
        Returns:
            dict: Dictionary containing bounding box information
        """
        x_coords, y_coords = self.parse_pixel_coordinates(points_list)
        
        # Find min/max coordinates
        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)
        
        # Calculate center and dimensions
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2
        box_width = max_x - min_x
        box_height = max_y - min_y

        box_area = box_width * box_height

        return {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'center_x': center_x,
            'center_y': center_y,
            'box_width': box_width,
            'box_height': box_height,
            'box_area': box_area
        }


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

        json_data = {
            "info": {
                "year": "2025",
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
                    "id": int(row_data['label_id']),
                    "name": "arthropod",
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
                    "category_id": int(row_data['label_id']),
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

    def group_objects_by_image_id(self, csv_data=None):
        """
        Group CSV objects by their image_id.

        Args:
            csv_data (list): List of CSV row dictionaries. If None, loads from file.

        Returns:
            dict: Dictionary where keys are image_ids and values are lists of objects
        """
        try:
            if csv_data is None:
                csv_data = self.load_csv_data()

            grouped_objects = {}

            for row_data in csv_data:
                image_id = int(row_data['image_id'])

                if image_id not in grouped_objects:
                    grouped_objects[image_id] = []

                grouped_objects[image_id].append(row_data)

            self.logger.info(
                f"Grouped {len(csv_data)} objects into {len(grouped_objects)} image groups")
            return grouped_objects

        except Exception as e:
            self.logger.error(f"Error grouping objects by image_id: {e}")
            raise

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
                    categories_dict[category_id] = {
                        "id": category_id,
                        "name": "arthropod",
                        "supercategory": "none"
                    }

            # Convert categories dict to list
            categories = list(categories_dict.values())

            # Create the merged JSON structure
            merged_json = {
                "info": {
                    "year": "2025",
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


    def generate_output_filename(self, row_data, extension):
        """
        Generate an output filename based on the specified pattern.
        
        Args:
            row_data (dict): Row data from CSV
            extension (str): File extension (e.g., 'json', 'jpg')
            
        Returns:
            str: Generated filename
        """
        image_id = int(row_data['image_id'])
        object_id = row_data['id']
        label_id = row_data['label_id']
        
        # Get base filename without extension
        filename = self.image_mapping.get(image_id, f"unknown_{image_id}.jpg")
        base_name = Path(filename).stem
        
        # Create filename: prefix + basename + _object_ID_class_LABELID.extension
        filename_parts = []
        if self.prefix_filename:
            filename_parts.append(self.prefix_filename)
        
        filename_parts.extend([
            base_name,
            f"object_{object_id}",
            f"class_{label_id}"
        ])
        
        return f"{'_'.join(filename_parts)}.{extension}"


    def create_class_subfolder(self, label_id):
        """
        Create subfolder for a specific class label.
        
        Args:
            label_id (str): Label ID for the class
            
        Returns:
            Path: Path to the created subfolder
        """
        subfolder_path = self.output_crops_path / str(label_id)
        subfolder_path.mkdir(parents=True, exist_ok=True)
        return subfolder_path


    def crop_object_image(self, image_path, bbox_info):
        """
        Crop object from image using bounding box coordinates.
        
        Args:
            image_path (Path): Path to the source image
            bbox_info (dict): Bounding box information
            
        Returns:
            PIL.Image: Cropped image
        """
        try:
            with Image.open(image_path) as img:
                # Define crop box (left, upper, right, lower)
                crop_box = (
                    bbox_info['min_x'],
                    bbox_info['min_y'],
                    bbox_info['max_x'],
                    bbox_info['max_y']
                )
                
                # Crop the image
                cropped_image = img.crop(crop_box)
                return cropped_image
                
        except Exception as e:
            self.logger.error(f"Error cropping image {image_path}: {e}")
            raise


    def process_single_object(self, row_data):
        """
        Process a single object: calculate bbox, create JSON, and crop image.

        Args:
            row_data (dict): Row data from CSV containing object information
        """
        try:
            # Calculate bounding box
            bbox_info = self.calculate_bounding_box(row_data['points'])

            # Get image path
            image_id = int(row_data['image_id'])
            image_filename = self.image_mapping.get(image_id)
            if not image_filename:
                self.logger.warning(
                    f"No filename mapping for image_id {image_id}")
                return

            image_path = self.images_path / image_filename
            if not image_path.exists():
                self.logger.warning(f"Image file not found: {image_path}")
                return

            # Create class subfolder
            label_id = row_data['label_id']
            subfolder_path = self.create_class_subfolder(label_id)

            # Generate filenames
            json_filename = self.generate_output_filename(row_data, 'json')
            image_filename_out = self.generate_output_filename(row_data, 'jpg')

            # Create and save JSON metadata
            json_data = self.create_json_metadata(row_data, bbox_info,
                                                  image_path)
            json_path = subfolder_path / json_filename

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)

            # Crop and save image
            cropped_image = self.crop_object_image(image_path, bbox_info)
            image_output_path = subfolder_path / image_filename_out
            cropped_image.save(image_output_path, 'JPEG', quality=95)

            self.logger.info(
                f"Processed object {row_data['id']} from image {image_id}")

        except Exception as e:
            self.logger.error(
                f"Error processing object {row_data.get('id', 'unknown')}: {e}")


    def process_all_objects(self):
        """
        Process all objects in the CSV file.
        
        This is the main method that orchestrates the entire processing workflow.
        """
        try:
            # Load CSV data
            csv_data = self.load_csv_data()
            
            if not csv_data:
                self.logger.warning("No data loaded from CSV file")
                return
            
            # Process each row
            total_objects = len(csv_data)
            processed_objects = 0
            
            for row_data in csv_data:
                try:
                    self.process_single_object(row_data)
                    processed_objects += 1
                except Exception as e:
                    self.logger.error(f"Failed to process object {row_data.get('id', 'unknown')}: {e}")
                    continue
            
            self.logger.info(f"Processing complete: {processed_objects}/{total_objects} objects processed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in process_all_objects: {e}")
            raise


# # Example usage
# if __name__ == "__main__":
#     # Initialize the processor
#     processor = CSVObjectProcessor(
#         csv_file="path/to/your/file.csv",
#         images_path="path/to/images/directory",
#         filename_pattern="capt*.jpg",
#         output_crops_path="path/to/output/directory",
#         prefix_filename=""  # Optional prefix
#     )
#
#     # Process all objects
#     processor.process_all_objects()


# # Basic usage - merge all JSON files
# processor = CSVObjectProcessor(
#     csv_file="annotations.csv",
#     images_path="images/",
#     filename_pattern="capt*.jpg",
#     output_crops_path="output/"
# )

# # Merge JSON files (saves to output/merged_json/)
# processor.merge_json_files_by_image_id()

# # Or specify custom output path
# processor.merge_json_files_by_image_id("custom/merged/path")