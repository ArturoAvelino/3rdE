import csv
import json
import ast
from pathlib import Path
from PIL import Image
import logging


class CSVObjectProcessor:
    """
    A class to process CSV files containing pixel coordinates of objects in images.
    
    This class reads CSV files with object pixel coordinates, calculates bounding boxes,
    creates cropped images, and generates JSON metadata files organized by class labels.
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
                    # Parse the points string to a list of integers
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
        
        return {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'center_x': center_x,
            'center_y': center_y,
            'box_width': box_width,
            'box_height': box_height
        }

    def create_json_metadata(self, row_data, bbox_info):
        """
        Create JSON metadata structure for an object.
        
        Args:
            row_data (dict): Row data from CSV
            bbox_info (dict): Bounding box information
            
        Returns:
            dict: JSON metadata structure
        """
        image_id = int(row_data['image_id'])
        filename = self.image_mapping.get(image_id, f"unknown_{image_id}.jpg")
        
        # Extract base filename without extension for sample_name
        sample_name = Path(filename).stem
        
        json_data = {
            "image": [
                {
                    "sample_name": sample_name,
                    "filename": filename,
                    "filename_id": image_id,
                    "object_id": int(row_data['id'])
                }
            ],
            "annotations": [
                {
                    "class_id": int(row_data['label_id']),
                    "bbox": [
                        {
                            "center_x": bbox_info['center_x'],
                            "center_y": bbox_info['center_y'],
                            "box_width": bbox_info['box_width'],
                            "box_height": bbox_info['box_height']
                        }
                    ]
                }
            ]
        }
        
        return json_data

    def generate_output_filename(self, row_data, extension):
        """
        Generate output filename based on the specified pattern.
        
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
                self.logger.warning(f"No filename mapping for image_id {image_id}")
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
            json_data = self.create_json_metadata(row_data, bbox_info)
            json_path = subfolder_path / json_filename
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)
            
            # Crop and save image
            cropped_image = self.crop_object_image(image_path, bbox_info)
            image_output_path = subfolder_path / image_filename_out
            cropped_image.save(image_output_path, 'JPEG', quality=95)
            
            self.logger.info(f"Processed object {row_data['id']} from image {image_id}")
            
        except Exception as e:
            self.logger.error(f"Error processing object {row_data.get('id', 'unknown')}: {e}")

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
