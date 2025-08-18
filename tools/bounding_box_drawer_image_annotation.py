import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Tuple, Optional, Union
import logging


class BoundingBoxDrawer:
    """
    A comprehensive class for drawing bounding boxes on images using annotation data
    from JSON files in either COCO or Roboflow format.

    This class supports two different JSON annotation formats:
    1. COCO format: Standard COCO dataset annotation format
    2. Roboflow format: Roboflow export format

    Features:
    - Automatic format detection and processing
    - Configurable output directory creation
    - Custom output filename specification
    - Adjustable font size for text labels
    - Flexible file path handling for images and JSON files
    - Text labels with object IDs on bounding boxes
    - Error handling and logging
    - Image dimension validation
    """

    def __init__(self, json_format: str = "coco",
                 output_directory: str = "output",
                 image_path: Optional[str] = None,
                 json_path: Optional[str] = None,
                 font_size: int = 16):
        """
        Initialize the BoundingBoxDrawer.

        Args:
            json_format (str): Format type - either "coco" or "roboflow"
            output_directory (str): Directory path where output images will be saved
            image_path (str, optional): Path to the directory containing images
            json_path (str, optional): Path to the directory containing JSON files
            font_size (int): Font size for text labels (default: 16)

        Raises:
            ValueError: If json_format is not "coco" or "roboflow"
        """
        if json_format.lower() not in ["coco", "roboflow"]:
            raise ValueError("json_format must be either 'coco' or 'roboflow'")

        self.json_format = json_format.lower()
        self.output_directory = Path(output_directory)
        self.image_path = Path(image_path) if image_path else None
        self.json_path = Path(json_path) if json_path else None
        self.font_size = max(8,
                             min(72, font_size))  # Clamp font size between 8-72

        # Create output directory if it doesn't exist
        self.output_directory.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Initialize format-specific processor
        if self.json_format == "coco":
            self.processor = COCOProcessor()
        else:
            self.processor = RoboflowProcessor()

    def process_image_with_annotations(self, image_file_path: Union[str, Path],
                                       json_file_path: Union[str, Path],
                                       output_filename: Optional[str] = None,
                                       custom_font_size: Optional[
                                           int] = None) -> bool:
        """
        Process a single image with its corresponding JSON annotation file.

        Args:
            image_file_path (Union[str, Path]): Path to the image file
            json_file_path (Union[str, Path]): Path to the JSON annotation file
            output_filename (str, optional): Custom output filename. If None, generates automatically
            custom_font_size (int, optional): Custom font size for this specific image. 
                                           If None, uses instance font_size

        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            # Convert to Path objects
            image_file_path = Path(image_file_path)
            json_file_path = Path(json_file_path)

            # Validate file existence
            if not image_file_path.exists():
                self.logger.error(f"Image file not found: {image_file_path}")
                return False

            if not json_file_path.exists():
                self.logger.error(f"JSON file not found: {json_file_path}")
                return False

            # Load and validate JSON data
            json_data = self._load_json_file(json_file_path)
            if not json_data:
                return False

            # Load image
            image = self._load_image(image_file_path)
            if not image:
                return False

            # Extract bounding box data
            bbox_data = self.processor.extract_bbox_data(json_data, image.size)
            if not bbox_data:
                self.logger.warning(
                    f"No bounding box data found in {json_file_path}")
                return False

            # Use custom font size if provided, otherwise use instance font size
            font_size = custom_font_size if custom_font_size is not None else self.font_size

            # Draw bounding boxes
            annotated_image = self._draw_bounding_boxes(image, bbox_data,
                                                        font_size)

            # Generate output filename if not provided
            if output_filename is None:
                output_filename = self._generate_output_filename(
                    image_file_path)

            output_path = self.output_directory / output_filename
            annotated_image.save(output_path)

            self.logger.info(
                f"Successfully processed {image_file_path.name} -> {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error processing {image_file_path}: {str(e)}")
            return False

    def process_batch(self, image_pattern: str = "*.jpg",
                      json_pattern: str = "*.json",
                      output_filename_template: Optional[str] = None,
                      custom_font_size: Optional[int] = None) -> Dict[
        str, List[str]]:
        """
        Process a batch of images with their corresponding JSON files.

        Args:
            image_pattern (str): Glob pattern to match image files
            json_pattern (str): Glob pattern to match JSON files
            output_filename_template (str, optional): Template for output filenames.
                                                    Use {stem} for original filename without extension.
                                                    Example: "annotated_{stem}.jpg"
            custom_font_size (int, optional): Custom font size for batch processing

        Returns:
            Dict[str, List[str]]: Dictionary with 'successful' and 'failed' lists
        """
        if not self.image_path or not self.json_path:
            self.logger.error(
                "Both image_path and json_path must be set for batch processing")
            return {'successful': [], 'failed': []}

        results = {'successful': [], 'failed': []}

        # Find image files
        image_files = list(self.image_path.glob(image_pattern))
        self.logger.info(f"Found {len(image_files)} image files")

        for image_file in image_files:
            # Find corresponding JSON file
            json_file = self._find_corresponding_json(image_file, json_pattern)

            if not json_file:
                self.logger.warning(
                    f"No corresponding JSON file found for {image_file.name}")
                results['failed'].append(str(image_file))
                continue

            # Generate output filename from template
            output_filename = None
            if output_filename_template:
                output_filename = output_filename_template.format(
                    stem=image_file.stem)

            # Process the image-JSON pair
            success = self.process_image_with_annotations(
                image_file, json_file, output_filename, custom_font_size
            )

            if success:
                results['successful'].append(str(image_file))
            else:
                results['failed'].append(str(image_file))

        self.logger.info(
            f"Batch processing completed: {len(results['successful'])} successful, "
            f"{len(results['failed'])} failed")

        return results

    def set_font_size(self, font_size: int) -> None:
        """
        Update the default font size for the drawer.

        Args:
            font_size (int): New font size (will be clamped between 8-72)
        """
        self.font_size = max(8, min(72, font_size))
        self.logger.info(f"Font size updated to: {self.font_size}")

    def _generate_output_filename(self, image_file_path: Path) -> str:
        """Generate automatic output filename based on input image name."""
        base_name = image_file_path.stem
        extension = image_file_path.suffix if image_file_path.suffix else '.jpg'
        return f"annotated_{base_name}{extension}"

    def _load_json_file(self, json_file_path: Path) -> Optional[Dict]:
        """Load and parse JSON file."""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in {json_file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading JSON file {json_file_path}: {e}")
            return None

    def _load_image(self, image_path: Path) -> Optional[Image.Image]:
        """Load and validate image file."""
        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            self.logger.error(f"Error loading image {image_path}: {e}")
            return None

    def _find_corresponding_json(self, image_file: Path, json_pattern: str) -> \
    Optional[Path]:
        """Find JSON file corresponding to an image file."""
        # Try exact name match first
        json_file = self.json_path / f"{image_file.stem}.json"
        if json_file.exists():
            return json_file

        # Try pattern matching
        json_files = list(self.json_path.glob(json_pattern))
        for json_file in json_files:
            if json_file.stem == image_file.stem:
                return json_file

        return None

    def _draw_bounding_boxes(self, image: Image.Image,
                             bbox_data: List[Dict],
                             font_size: int) -> Image.Image:
        """Draw bounding boxes and labels on the image with specified font size."""
        # Create a copy of the image to draw on
        annotated_image = image.copy()
        draw = ImageDraw.Draw(annotated_image)

        # Try to load font with specified size
        font = self._get_font(font_size)

        # Colors for bounding boxes (cycling through different colors)
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink',
                  'gray',
                  'cyan', 'magenta', 'yellow', 'lime', 'navy', 'maroon',
                  'olive', 'teal']

        for i, bbox in enumerate(bbox_data):
            color = colors[i % len(colors)]

            # Extract coordinates
            x1, y1, x2, y2 = bbox['coordinates']
            label = bbox['label']
            object_id = bbox['id']

            # Calculate line width based on font size (proportional scaling)
            line_width = max(2, font_size // 6)

            # Draw bounding box rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)

            # Prepare label text
            label_text = f"{label} {object_id}"

            # Calculate text position (above the bounding box)
            text_x = x1
            text_y = max(0, y1 - font_size - 5)  # Position based on font size

            # Draw text background for better visibility
            if font:
                # Get text bounding box
                bbox_text = draw.textbbox((text_x, text_y), label_text,
                                          font=font)
                # Add padding to background
                padding = 2
                bg_bbox = (bbox_text[0] - padding, bbox_text[1] - padding,
                           bbox_text[2] + padding, bbox_text[3] + padding)
                draw.rectangle(bg_bbox, fill=color)
                draw.text((text_x, text_y), label_text, fill='white', font=font)
            else:
                # Fallback without font - estimate text size
                text_width = len(label_text) * (font_size // 2)
                text_height = font_size
                bg_bbox = (text_x, text_y, text_x + text_width,
                           text_y + text_height)
                draw.rectangle(bg_bbox, fill=color)
                draw.text((text_x, text_y), label_text, fill='white')

        return annotated_image

    def _get_font(self, font_size: int) -> Optional[ImageFont.ImageFont]:
        """Get font with specified size, with fallback options."""
        # Try different font options
        font_options = [
            "arial.ttf", "Arial.ttf", "helvetica.ttf", "Helvetica.ttf",
            "DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "liberation-sans.ttf"
        ]

        # Try system fonts first
        for font_name in font_options:
            try:
                return ImageFont.truetype(font_name, size=font_size)
            except (OSError, IOError):
                continue

        # Try default font with size (PIL >= 8.0.0)
        try:
            return ImageFont.load_default(size=font_size)
        except (OSError, IOError, TypeError):
            pass

        # Fallback to basic default font
        try:
            return ImageFont.load_default()
        except Exception:
            return None


class COCOProcessor:
    """Processor for COCO format JSON files."""

    def extract_bbox_data(self, json_data: Dict, image_size: Tuple[int, int]) -> \
    List[Dict]:
        """
        Extract bounding box data from COCO format JSON.

        Args:
            json_data (Dict): Loaded JSON data in COCO format
            image_size (Tuple[int, int]): (width, height) of the image

        Returns:
            List[Dict]: List of bounding box data dictionaries
        """
        bbox_data = []

        # Create category mapping
        category_mapping = self._create_category_mapping(json_data)

        # Extract image information
        image_info = self._get_image_info(json_data)
        if not image_info:
            return bbox_data

        # Process annotations
        annotations = json_data.get('annotations', [])

        for annotation in annotations:
            try:
                # Extract bbox coordinates (COCO format: [x, y, width, height])
                bbox = annotation.get('bbox', [])
                if len(bbox) != 4:
                    continue

                x, y, width, height = bbox

                # Convert to corner coordinates
                x1, y1 = x, y
                x2, y2 = x + width, y + height

                # Get category information
                category_id = annotation.get('category_id')
                category_name = category_mapping.get(category_id,
                                                     f"Unknown_{category_id}")

                # Get annotation ID
                annotation_id = annotation.get('id', 'N/A')

                bbox_data.append({
                    'coordinates': (x1, y1, x2, y2),
                    'label': category_name,
                    'id': str(annotation_id)
                })

            except Exception as e:
                logging.getLogger(__name__).warning(
                    f"Error processing annotation: {e}")
                continue

        return bbox_data

    def _create_category_mapping(self, json_data: Dict) -> Dict[int, str]:
        """Create mapping from category ID to category name."""
        category_mapping = {}
        categories = json_data.get('categories', [])

        for category in categories:
            category_id = category.get('id')
            category_name = category.get('name', f"Category_{category_id}")
            if category_id is not None:
                category_mapping[category_id] = category_name

        return category_mapping

    def _get_image_info(self, json_data: Dict) -> Optional[Dict]:
        """Extract image information from COCO JSON."""
        images = json_data.get('images', [])
        if not images:
            return None

        # Return the first image info (assuming single image per JSON)
        return images[0]


class RoboflowProcessor:
    """Processor for Roboflow format JSON files."""

    def extract_bbox_data(self, json_data: Dict, image_size: Tuple[int, int]) -> \
    List[Dict]:
        """
        Extract bounding box data from Roboflow format JSON.

        Args:
            json_data (Dict): Loaded JSON data in Roboflow format
            image_size (Tuple[int, int]): (width, height) of the image

        Returns:
            List[Dict]: List of bounding box data dictionaries
        """
        bbox_data = []

        predictions = json_data.get('predictions', [])

        for prediction in predictions:
            try:
                # Extract center coordinates and dimensions
                center_x = prediction.get('x', 0)
                center_y = prediction.get('y', 0)
                width = prediction.get('width', 0)
                height = prediction.get('height', 0)

                # Convert center coordinates to corner coordinates
                x1 = center_x - width / 2
                y1 = center_y - height / 2
                x2 = center_x + width / 2
                y2 = center_y + height / 2

                # Get class information
                class_name = prediction.get('class', 'Unknown')

                # Get detection ID (first 8 characters)
                detection_id = prediction.get('detection_id', 'N/A')
                if len(detection_id) > 8:
                    detection_id = detection_id[:8]

                bbox_data.append({
                    'coordinates': (x1, y1, x2, y2),
                    'label': class_name,
                    'id': detection_id
                })

            except Exception as e:
                logging.getLogger(__name__).warning(
                    f"Error processing prediction: {e}")
                continue

        return bbox_data


# Enhanced convenience functions with new parameters
def draw_coco_bounding_boxes(image_path: str, json_path: str,
                             output_dir: str = "output",
                             output_filename: Optional[str] = None,
                             font_size: int = 16) -> bool:
    """
    Convenience function to draw bounding boxes from COCO format JSON.

    Args:
        image_path (str): Path to the image file
        json_path (str): Path to the COCO format JSON file
        output_dir (str): Output directory for the annotated image
        output_filename (str, optional): Custom output filename
        font_size (int): Font size for text labels

    Returns:
        bool: True if successful, False otherwise
    """
    drawer = BoundingBoxDrawer(json_format="coco", output_directory=output_dir,
                               font_size=font_size)
    return drawer.process_image_with_annotations(image_path, json_path,
                                                 output_filename)


def draw_roboflow_bounding_boxes(image_path: str, json_path: str,
                                 output_dir: str = "output",
                                 output_filename: Optional[str] = None,
                                 font_size: int = 16) -> bool:
    """
    Convenience function to draw bounding boxes from Roboflow format JSON.

    Args:
        image_path (str): Path to the image file
        json_path (str): Path to the Roboflow format JSON file
        output_dir (str): Output directory for the annotated image
        output_filename (str, optional): Custom output filename
        font_size (int): Font size for text labels

    Returns:
        bool: True if successful, False otherwise
    """
    drawer = BoundingBoxDrawer(json_format="roboflow",
                               output_directory=output_dir,
                               font_size=font_size)
    return drawer.process_image_with_annotations(image_path, json_path,
                                                 output_filename)


# # Example usage
# if __name__ == "__main__":
#     # Setup logging
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(levelname)s - %(message)s')
#
#     # Example 1: Process single COCO format file with custom output name and font size
#     coco_drawer = BoundingBoxDrawer(
#         json_format="coco",
#         output_directory="output/coco_results",
#         font_size=20  # Larger font
#     )
#
#     success = coco_drawer.process_image_with_annotations(
#         "path/to/image.jpg",
#         "path/to/annotations.json",
#         output_filename="my_custom_annotated_image.jpg",
#         custom_font_size=24  # Even larger font for this specific image
#     )
#
#     # Example 2: Batch processing with template and custom font
#     batch_drawer = BoundingBoxDrawer(
#         json_format="coco",
#         output_directory="output/batch_results",
#         image_path="path/to/images",
#         json_path="path/to/json_files",
#         font_size=18
#     )
#
#     results = batch_drawer.process_batch(
#         image_pattern="*.jpg",
#         json_pattern="*.json",
#         output_filename_template="bbox_{stem}_processed.jpg",
#         custom_font_size=22
#     )
#
#     # Example 3: Using convenience functions
#     success = draw_coco_bounding_boxes(
#         "image.jpg",
#         "annotations.json",
#         "output_dir",
#         output_filename="result.jpg",
#         font_size=14
#     )
#
#     # Example 4: Change font size dynamically
#     drawer = BoundingBoxDrawer(json_format="roboflow")
#     drawer.set_font_size(28)  # Update font size

# # Custom output filename and font size
# drawer = BoundingBoxDrawer(json_format="coco", font_size=20)
# drawer.process_image_with_annotations(
#     "input.jpg",
#     "annotations.json",
#     output_filename="my_results.jpg",
#     custom_font_size=24
# )
#
# # Batch with template and custom font
# results = drawer.process_batch(
#     output_filename_template="annotated_{stem}_final.jpg",
#     custom_font_size=18
# )
#
# # Convenience function with custom options
# draw_coco_bounding_boxes(
#     "image.jpg",
#     "data.json",
#     "output/",
#     output_filename="custom_name.jpg",
#     font_size=22
# )
#
# # Dynamic font size adjustment
# drawer.set_font_size(28)
