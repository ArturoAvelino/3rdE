import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Tuple, Optional, Union
import logging


class BoundingBoxDrawer:
    """
    A comprehensive Python class for drawing bounding boxes on images with annotation data from JSON files.

    OVERVIEW:
    =========
    The BoundingBoxDrawer class is a powerful tool for visualizing object detection results by overlaying
    bounding boxes, labels, and metadata onto images. It supports two major annotation formats (COCO and Roboflow)
    and provides extensive customization options for appearance, filtering, and output generation.

    KEY FEATURES:
    =============
    • Dual Format Support: Handles both COCO and Roboflow JSON annotation formats
    • Smart Filtering: Filter objects by confidence levels (Roboflow format)
    • Visual Customization: Configurable colors, fonts, text positioning, and box styles
    • Object Summaries: Display object count summaries with flexible positioning
    • Batch Processing: Process multiple images with consistent settings
    • Error Handling: Robust error handling with detailed logging
    • Flexible Output: Custom output directories and filename generation
    • ID & Confidence Display: Optional display of object IDs and confidence scores

    SUPPORTED ANNOTATION FORMATS:
    ============================
    1. COCO Format:
       - Standard COCO dataset annotation format
       - bbox format: [x, y, width, height] (top-left corner + dimensions)
       - Categories defined separately with IDs

    2. Roboflow Format:
       - Roboflow export format with confidence scores
       - bbox format: center coordinates (x, y) + width, height
       - Built-in confidence scores for filtering

    USAGE EXAMPLES:
    ==============

    # Example 1: Basic Usage - Simple COCO annotation processing
    drawer = BoundingBoxDrawer(json_format="coco", output_directory="results")
    success = drawer.process_image_with_annotations("image.jpg", "annotations.json")

    # Example 2: Roboflow with Confidence Filtering
    drawer = BoundingBoxDrawer(
        json_format="roboflow",
        confidence_range=(0.6, 0.9),     # Only show 60-90% confidence objects
        bbox_color="blue",               # Use blue for all boxes
        font_size=18,                    # Larger text
        show_summary=True,               # Display object count summary
        summary_position="top_left"      # Position summary at top-left
    )
    success = drawer.process_image_with_annotations("photo.jpg", "predictions.json")

    # Example 3: Custom Visual Styling
    drawer = BoundingBoxDrawer(
        json_format="roboflow",
        font_size=20,
        bbox_color="red",                # Red bounding boxes
        text_color="yellow",             # Yellow text
        text_position="bottom",          # Text below boxes
        show_id=False,                   # Hide object IDs
        show_confidence=True             # Show confidence scores
    )

    # Example 4: Per-Image Custom Overrides
    success = drawer.process_image_with_annotations(
        "special_image.jpg",
        "special_annotations.json",
        custom_font_size=24,                    # Override font size for this image
        custom_bbox_color="green",              # Override box color
        custom_confidence_range=(0.8, 1.0),    # Override confidence filter
        custom_show_summary=True,               # Override summary display
        output_filename="special_result.jpg"    # Custom output name
    )

    # Example 5: Dynamic Configuration Changes
    drawer.set_font_size(22)                   # Change font size
    drawer.set_colors("purple", "white")       # Change box and text colors
    drawer.set_confidence_range(0.7, 0.95)     # Update confidence filter
    drawer.set_summary_options(True, "center") # Enable centered summary

    # Example 6: Using Convenience Functions
    from bounding_box_drawer import draw_roboflow_bounding_boxes

    success = draw_roboflow_bounding_boxes(
        image_path="image.jpg",
        json_path="predictions.json",
        output_dir="output",
        confidence_range=(0.5, 0.8),
        show_summary=True,
        summary_position="bottom_right",
        font_size=16
    )

    # Example 7: Batch Processing Setup
    drawer = BoundingBoxDrawer(
        json_format="roboflow",
        output_directory="batch_results",
        confidence_range=(0.6, 1.0),
        show_summary=True,
        show_id=False
    )

    # Process multiple images
    image_files = ["img1.jpg", "img2.jpg", "img3.jpg"]
    json_files = ["pred1.json", "pred2.json", "pred3.json"]

    for img, json_file in zip(image_files, json_files):
        success = drawer.process_image_with_annotations(img, json_file)
        if success:
            print(f"Successfully processed {img}")

    CORE METHODS:
    ============

    __init__(parameters...):
        Initialize the drawer with default settings for all processing operations.

    process_image_with_annotations(image_path, json_path, **options):
        Main method to process a single image with its annotation file.
        Returns True if successful, False otherwise.

    set_font_size(size):
        Update the default font size (clamped between 8-72).

    set_colors(bbox_color=None, text_color=None):
        Update default colors for bounding boxes and text.

    set_text_position(position):
        Set text position relative to bounding boxes ("top" or "bottom").

    set_confidence_range(min_conf, max_conf):
        Set confidence filtering range for Roboflow format (0.0 to 1.0).

    set_summary_options(show_summary, position):
        Configure object count summary display and positioning.

    CONFIGURATION OPTIONS:
    =====================

    Visual Appearance:
    • font_size: Text size (8-72, default: 16)
    • bbox_color: Single color for all boxes, or None for cycling colors
    • text_color: Text color, or None for white text on colored backgrounds
    • text_position: "top" (above boxes) or "bottom" (below boxes)

    Filtering & Display:
    • confidence_range: Tuple (min, max) for confidence filtering (Roboflow only)
    • show_id: Display object IDs in labels (boolean)
    • show_confidence: Display confidence scores in labels (boolean)

    Summary Options:
    • show_summary: Enable object count summary display (boolean)
    • summary_position: "top_left", "top_right", "bottom_left", "bottom_right", "center"

    Output Control:
    • output_directory: Directory for saving annotated images
    • Custom output filenames with automatic generation fallback

    ERROR HANDLING:
    ==============
    The class provides comprehensive error handling:
    • File existence validation for images and JSON files
    • JSON parsing error detection
    • Image loading and format validation
    • Graceful handling of missing annotation data
    • Detailed logging for debugging and monitoring

    RETURN VALUES:
    =============
    • process_image_with_annotations(): Returns boolean success status
    • Convenience functions: Return boolean success status
    • Setter methods: No return value, log changes

    DEPENDENCIES:
    ============
    • PIL (Pillow): Image processing and drawing
    • json: JSON file parsing
    • pathlib: Path handling
    • typing: Type hints
    • logging: Error and info logging

    This class is ideal for:
    • Computer vision result visualization
    • Object detection pipeline debugging
    • Dataset annotation review
    • Batch processing of detection results
    • Creating annotated images for presentations or reports
    """

    def __init__(self, json_format: str = "coco",
                 output_directory: str = "output",
                 image_path: Optional[str] = None,
                 json_path: Optional[str] = None,
                 font_size: int = 16,
                 bbox_color: Optional[str] = None,
                 text_color: Optional[str] = None,
                 text_position: str = "top",
                 confidence_range: Optional[Tuple[float, float]] = None,
                 show_summary: bool = False,
                 summary_position: str = "bottom_right",
                 show_id: bool = True,
                 show_confidence: bool = True,
                 show_center: bool = False,
                 center_dot_size: int = 8,
                 show_label: bool = True):
        """
            Initialize the BoundingBoxDrawer.

            Args:
                json_format (str): Format type - either "coco" or "roboflow"
                output_directory (str): Directory path where output images will be saved
                image_path (str, optional): Path to the directory containing images
                json_path (str, optional): Path to the directory containing JSON files
                font_size (int): Font size for text labels (default: 16)
                bbox_color (str, optional): Single color for all bounding boxes. If None, uses cycling colors
                text_color (str, optional): Single color for all text. If None, uses white text on colored backgrounds
                text_position (str): Position of text - either "top" or "bottom" (default: "top")
                confidence_range (Tuple[float, float], optional): Min and max confidence levels (e.g., (0.5, 0.8))
                show_summary (bool): Whether to show object count summary on image
                summary_position (str): Position for summary text - "bottom_left", "bottom_right",
                                      "top_left", "top_right", "center"
                show_id (bool): Whether to show object ID in bounding box labels
                show_confidence (bool): Whether to show confidence in bounding box labels
                show_center (bool): Whether to draw a dot at the center of each bounding box
                center_dot_size (int): Radius of center dot in pixels (default: 4)
                show_label (bool): Whether to show object labels (class names) in bounding box labels

            Raises:
                ValueError: If json_format is not "coco" or "roboflow" or text_position is invalid
            """
        if json_format.lower() not in ["coco", "roboflow"]:
            raise ValueError("json_format must be either 'coco' or 'roboflow'")

        if text_position.lower() not in ["top", "bottom"]:
            raise ValueError("text_position must be either 'top' or 'bottom'")

        valid_summary_positions = ["bottom_left", "bottom_right", "top_left",
                                   "top_right", "center"]
        if summary_position.lower() not in valid_summary_positions:
            raise ValueError(
                f"summary_position must be one of: {valid_summary_positions}")

        self.json_format = json_format.lower()
        self.output_directory = Path(output_directory)
        self.image_path = Path(image_path) if image_path else None
        self.json_path = Path(json_path) if json_path else None
        self.font_size = max(8,
                             min(72, font_size))  # Clamp font size between 8-72
        self.bbox_color = bbox_color
        self.text_color = text_color
        self.text_position = text_position.lower()
        self.confidence_range = confidence_range
        self.show_summary = show_summary
        self.summary_position = summary_position.lower()
        self.show_id = show_id
        self.show_confidence = show_confidence
        self.show_center = show_center
        self.center_dot_size = max(1, center_dot_size)  # Ensure minimum size of 1
        self.show_label = show_label


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
                                       custom_font_size: Optional[int] = None,
                                       custom_bbox_color: Optional[str] = None,
                                       custom_text_color: Optional[str] = None,
                                       custom_text_position: Optional[
                                           str] = None,
                                       custom_confidence_range: Optional[
                                           Tuple[float, float]] = None,
                                       custom_show_summary: Optional[
                                           bool] = None,
                                       custom_summary_position: Optional[
                                           str] = None,
                                       custom_show_id: Optional[
                                           bool] = None,
                                       custom_show_confidence: Optional[
                                           bool] = None,
                                       custom_show_center: Optional[
                                           bool] = None,
                                       custom_center_dot_size: Optional[
                                           int] = None,
                                       custom_show_label: Optional[
                                           bool] = None) -> bool:
        """
            Process a single image with its corresponding JSON annotation file.

            Args:
                image_file_path (Union[str, Path]): Path to the image file
                json_file_path (Union[str, Path]): Path to the JSON annotation file
                output_filename (str, optional): Custom output filename. If None, generates automatically
                custom_font_size (int, optional): Custom font size for this specific image
                custom_bbox_color (str, optional): Custom bounding box color for this image
                custom_text_color (str, optional): Custom text color for this image
                custom_text_position (str, optional): Custom text position for this image ("top" or "bottom")
                custom_confidence_range (Tuple[float, float], optional): Custom confidence range for filtering
                custom_show_summary (bool, optional): Whether to show summary for this image
                custom_summary_position (str, optional): Custom summary position for this image
                custom_show_id (bool, optional): Whether to show IDs for this image
                custom_show_confidence (bool, optional): Whether to show confidence for this image
                custom_show_center (bool, optional): Whether to show center dots for this image
                custom_center_dot_size (int, optional): Custom center dot size for this image
                custom_show_label (bool, optional): Whether to show labels for this image

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

            # Use custom parameters if provided, otherwise use instance defaults
            font_size = custom_font_size if custom_font_size is not None else self.font_size
            bbox_color = custom_bbox_color if custom_bbox_color is not None else self.bbox_color
            text_color = custom_text_color if custom_text_color is not None else self.text_color
            text_position = custom_text_position if custom_text_position is not None else self.text_position
            confidence_range = custom_confidence_range if custom_confidence_range is not None else self.confidence_range
            show_summary = custom_show_summary if custom_show_summary is not None else self.show_summary
            summary_position = custom_summary_position if custom_summary_position is not None else self.summary_position
            show_id = custom_show_id if custom_show_id is not None else self.show_id
            show_confidence = custom_show_confidence if custom_show_confidence is not None else self.show_confidence
            show_center = custom_show_center if custom_show_center is not None else self.show_center
            center_dot_size = custom_center_dot_size if custom_center_dot_size is not None else self.center_dot_size
            show_label = custom_show_label if custom_show_label is not None else self.show_label

            # Extract bounding box data
            all_bbox_data = self.processor.extract_bbox_data(json_data,
                                                             image.size,
                                                             show_id,
                                                             show_confidence)
            if not all_bbox_data:
                self.logger.warning(
                    f"No bounding box data found in {json_file_path}")
                return False

            # Validate custom text position
            if text_position and text_position.lower() not in ["top", "bottom"]:
                self.logger.warning(
                    f"Invalid text_position '{text_position}', using 'top'")
                text_position = "top"

            # Filter bbox data by confidence range
            filtered_bbox_data = self._filter_by_confidence(all_bbox_data,
                                                            confidence_range)

            if not filtered_bbox_data:
                self.logger.warning(
                    f"No objects match confidence criteria in {json_file_path}")
                # Still create the image but without bounding boxes
                filtered_bbox_data = []

            # Create class summary if requested
            class_summary = None
            if show_summary:
                class_summary = self._create_class_summary(filtered_bbox_data)

            # Draw bounding boxes and summary
            annotated_image = self._draw_bounding_boxes(
                image, filtered_bbox_data, font_size, bbox_color, text_color,
                text_position, show_id, show_confidence, class_summary,
                summary_position, show_center, center_dot_size, show_label
            )

            # Generate output filename if not provided
            if output_filename is None:
                output_filename = self._generate_output_filename(
                    image_file_path)

            output_path = self.output_directory / output_filename
            annotated_image.save(output_path)

            self.logger.info(
                f"Successfully processed {image_file_path.name} -> {output_path}")
            self.logger.info(
                f"Displayed {len(filtered_bbox_data)} objects (filtered from {len(all_bbox_data)} total)")
            return True

        except Exception as e:
            self.logger.error(f"Error processing {image_file_path}: {str(e)}")
            return False

    def _filter_by_confidence(self, bbox_data: List[Dict],
                              confidence_range: Optional[
                                  Tuple[float, float]]) -> List[Dict]:
        """Filter bounding box data by confidence range."""
        if not confidence_range or self.json_format != "roboflow":
            return bbox_data

        min_conf, max_conf = confidence_range
        filtered_data = []

        for bbox in bbox_data:
            # Extract confidence from the original data
            confidence = bbox.get('raw_confidence',
                                  1.0)  # Default to 1.0 for COCO format

            if min_conf <= confidence <= max_conf:
                filtered_data.append(bbox)

        return filtered_data

    def _create_class_summary(self, bbox_data: List[Dict]) -> Dict[str, int]:
        """Create a summary of object counts by class."""
        class_counts = {}

        for bbox in bbox_data:
            label = bbox['label']
            class_counts[label] = class_counts.get(label, 0) + 1

        # Sort by count (descending) then by name
        return dict(sorted(class_counts.items(), key=lambda x: (-x[1], x[0])))

    def _draw_bounding_boxes(self, image: Image.Image,
                             bbox_data: List[Dict],
                             font_size: int,
                             bbox_color: Optional[str] = None,
                             text_color: Optional[str] = None,
                             text_position: str = "top",
                             show_id: bool = True,
                             show_confidence: bool = True,
                             class_summary: Optional[Dict[str, int]] = None,
                             summary_position: str = "bottom_right",
                             show_center: bool = False,
                             center_dot_size: int = 4,
                             show_label: bool = True) -> Image.Image:
        """Draw bounding boxes, labels, center dots, and summary on the image."""
        # Create a copy of the image to draw on
        annotated_image = image.copy()
        draw = ImageDraw.Draw(annotated_image)

        # Try to load font with specified size
        font = self._get_font(font_size)

        # Default colors for cycling if no single color is specified
        default_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown',
                          'pink', 'gray', 'cyan', 'magenta', 'yellow', 'lime',
                          'navy', 'maroon', 'olive', 'teal']

        # Draw bounding boxes
        for i, bbox in enumerate(bbox_data):
            # Determine color to use
            if bbox_color:
                color = bbox_color
            else:
                color = default_colors[i % len(default_colors)]

            # Extract coordinates and data
            x1, y1, x2, y2 = bbox['coordinates']
            label = bbox['label']

            # Calculate line width based on font size (proportional scaling)
            line_width = max(2, font_size // 6)

            # Draw bounding box rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)

            # Draw center dot if requested, using center coordinates from JSON
            if show_center and 'center_x' in bbox and 'center_y' in bbox:
                center_x = bbox['center_x']
                center_y = bbox['center_y']

                # Use configurable dot size
                dot_radius = center_dot_size
                draw.ellipse(
                    [center_x - dot_radius, center_y - dot_radius,
                     center_x + dot_radius, center_y + dot_radius],
                    fill=color, outline=color
                )

            # Prepare label text based on show_label, show_id and show_confidence settings
            label_parts = []

            if show_label:
                label_parts.append(label)

            if show_confidence and 'confidence' in bbox:
                label_parts.append(bbox['confidence'])

            if show_id and 'id' in bbox:
                label_parts.append(f"({bbox['id']})")

            # Only draw text if there are label parts to display
            if label_parts:
                label_text = " ".join(label_parts)

                # Calculate text position based on preference
                text_x = x1
                if text_position.lower() == "top":
                    text_y = max(0, y1 - font_size - 5)  # Above the box
                else:  # bottom
                    text_y = min(image.height - font_size, y2 + 5)  # Below the box

                # Determine text fill color
                if text_color:
                    fill_color = text_color
                    bg_color = self._get_complementary_color(
                        text_color) if not bbox_color else color
                else:
                    fill_color = 'white'
                    bg_color = color

                # Draw text background for better visibility
                if font:
                    bbox_text = draw.textbbox((text_x, text_y), label_text,
                                              font=font)
                    padding = 2
                    bg_bbox = (bbox_text[0] - padding, bbox_text[1] - padding,
                               bbox_text[2] + padding, bbox_text[3] + padding)
                    draw.rectangle(bg_bbox, fill=bg_color)
                    draw.text((text_x, text_y), label_text, fill=fill_color,
                              font=font)
                else:
                    # Fallback without font
                    text_width = len(label_text) * (font_size // 2)
                    text_height = font_size
                    bg_bbox = (text_x, text_y, text_x + text_width,
                               text_y + text_height)
                    draw.rectangle(bg_bbox, fill=bg_color)
                    draw.text((text_x, text_y), label_text, fill=fill_color)

        # Draw class summary if provided
        if class_summary:
            self._draw_class_summary(draw, class_summary, image.size, font,
                                     summary_position)

        return annotated_image

    def _draw_class_summary(self, draw: ImageDraw.ImageDraw,
                            class_summary: Dict[str, int],
                            image_size: Tuple[int, int],
                            font: Optional[ImageFont.ImageFont],
                            position: str) -> None:
        """Draw class summary text on the image."""
        # Prepare summary text lines
        summary_lines = []
        for class_name, count in class_summary.items():
            summary_lines.append(f"{count} {class_name}")

        if not summary_lines:
            return

        # Calculate text dimensions
        line_height = font.size if font else 20
        max_width = 0

        for line in summary_lines:
            if font:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
            else:
                line_width = len(line) * 8  # Estimate
            max_width = max(max_width, line_width)

        total_height = len(summary_lines) * line_height + 10  # 10px padding

        # Calculate position coordinates
        img_width, img_height = image_size

        if position == "bottom_right":
            start_x = img_width - max_width - 20
            start_y = img_height - total_height - 20
        elif position == "bottom_left":
            start_x = 20
            start_y = img_height - total_height - 20
        elif position == "top_right":
            start_x = img_width - max_width - 20
            start_y = 20
        elif position == "top_left":
            start_x = 20
            start_y = 20
        elif position == "center":
            start_x = (img_width - max_width) // 2
            start_y = (img_height - total_height) // 2
        else:
            start_x = img_width - max_width - 20  # Default to bottom_right
            start_y = img_height - total_height - 20

        # Draw background
        bg_padding = 10
        bg_rect = (start_x - bg_padding, start_y - bg_padding,
                   start_x + max_width + bg_padding,
                   start_y + total_height + bg_padding)
        draw.rectangle(bg_rect, fill='black', outline='white', width=2)

        # Draw text lines
        for i, line in enumerate(summary_lines):
            text_x = start_x
            text_y = start_y + i * line_height

            if font:
                draw.text((text_x, text_y), line, fill='white', font=font)
            else:
                draw.text((text_x, text_y), line, fill='white')

    def set_font_size(self, font_size: int) -> None:
        """Update the default font size for the drawer."""
        self.font_size = max(8, min(72, font_size))
        self.logger.info(f"Font size updated to: {self.font_size}")

    def set_colors(self, bbox_color: Optional[str] = None,
                   text_color: Optional[str] = None) -> None:
        """Update the default colors for bounding boxes and text."""
        if bbox_color is not None:
            self.bbox_color = bbox_color
            self.logger.info(f"Bounding box color updated to: {bbox_color}")

        if text_color is not None:
            self.text_color = text_color
            self.logger.info(f"Text color updated to: {text_color}")

    def set_text_position(self, position: str) -> None:
        """Update the default text position."""
        if position.lower() not in ["top", "bottom"]:
            raise ValueError("Text position must be either 'top' or 'bottom'")

        self.text_position = position.lower()
        self.logger.info(f"Text position updated to: {position}")

    def set_confidence_range(self, min_conf: float, max_conf: float) -> None:
        """Update the confidence range for filtering."""
        self.confidence_range = (min_conf, max_conf)
        self.logger.info(
            f"Confidence range updated to: {min_conf} - {max_conf}")

    def set_summary_options(self, show_summary: bool,
                            position: str = "bottom_right") -> None:
        """Update summary display options."""
        valid_positions = ["bottom_left", "bottom_right", "top_left",
                           "top_right", "center"]
        if position.lower() not in valid_positions:
            raise ValueError(f"Position must be one of: {valid_positions}")

        self.show_summary = show_summary
        self.summary_position = position.lower()
        self.logger.info(
            f"Summary options updated: show={show_summary}, position={position}")

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
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            self.logger.error(f"Error loading image {image_path}: {e}")
            return None

    def _find_corresponding_json(self, image_file: Path, json_pattern: str) -> \
    Optional[Path]:
        """Find JSON file corresponding to an image file."""
        json_file = self.json_path / f"{image_file.stem}.json"
        if json_file.exists():
            return json_file

        json_files = list(self.json_path.glob(json_pattern))
        for json_file in json_files:
            if json_file.stem == image_file.stem:
                return json_file

        return None

    def _get_complementary_color(self, color: str) -> str:
        """Get a complementary color for better text visibility."""
        light_colors = ['white', 'yellow', 'cyan', 'lime', 'pink', 'lightblue',
                        'lightgreen']
        dark_colors = ['black', 'navy', 'maroon', 'purple', 'brown',
                       'darkgreen', 'darkblue']

        if color.lower() in light_colors:
            return 'black'
        elif color.lower() in dark_colors:
            return 'white'
        else:
            return 'black'

    def _get_font(self, font_size: int) -> Optional[ImageFont.ImageFont]:
        """Get font with specified size, with fallback options."""
        font_options = [
            "arial.ttf", "Arial.ttf", "helvetica.ttf", "Helvetica.ttf",
            "DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "liberation-sans.ttf"
        ]

        for font_name in font_options:
            try:
                return ImageFont.truetype(font_name, size=font_size)
            except (OSError, IOError):
                continue

        try:
            return ImageFont.load_default(size=font_size)
        except (OSError, IOError, TypeError):
            pass

        try:
            return ImageFont.load_default()
        except Exception:
            return None

    def process_batch(self,
                      input_image_dir: Union[str, Path],
                      input_json_dir: Union[str, Path],
                      input_json_format: str,
                      output_dir: Union[str, Path],
                      font_size: Optional[int] = None,
                      bbox_color: Optional[str] = None,
                      text_color: Optional[str] = None,
                      text_position: Optional[str] = None,
                      show_center: Optional[bool] = None,
                      center_dot_size: Optional[int] = None,
                      show_id: Optional[bool] = None,
                      show_label: Optional[bool] = None,
                      summary_position: Optional[str] = None,
                      show_confidence: Optional[bool] = None,
                      confidence_range: Optional[Tuple[float, float]] = None,
                      show_summary: Optional[bool] = None,
                      image_extensions: List[str] = None,
                      json_extensions: List[str] = None) -> Dict[
        str, Union[List[str], int]]:
        """
            Process a batch of images and their corresponding JSON files in a single operation.

            This method enables batch processing of multiple images with their annotation files,
            eliminating the need to process each image individually. It automatically matches
            image files with their corresponding JSON files based on filename (without extension).

            Args:
                input_image_dir (Union[str, Path]): Path to directory containing images
                input_json_dir (Union[str, Path]): Path to directory containing JSON files
                input_json_format (str): Format of JSON files ("coco" or "roboflow")
                output_dir (Union[str, Path]): Path to output directory (will be created if doesn't exist)
                font_size (int, optional): Override default font size for this batch
                bbox_color (str, optional): Override default bounding box color
                text_color (str, optional): Override default text color
                text_position (str, optional): Override default text position ("top" or "bottom")
                show_center (bool, optional): Override default center dot display
                center_dot_size (int, optional): Override default center dot size
                show_id (bool, optional): Override default ID display
                show_label (bool, optional): Override default label display
                summary_position (str, optional): Override default summary position
                show_confidence (bool, optional): Override default confidence display
                confidence_range (Tuple[float, float], optional): Override default confidence filtering
                show_summary (bool, optional): Override default summary display
                image_extensions (List[str], optional): List of image file extensions to process
                                                       (default: ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'])
                json_extensions (List[str], optional): List of JSON file extensions to process
                                                      (default: ['.json'])

            Returns:
                Dict[str, Union[List[str], int]]: Dictionary containing:
                    - 'successful': List of successfully processed image filenames
                    - 'failed': List of failed image filenames
                    - 'skipped': List of skipped image filenames (no matching JSON)
                    - 'total_processed': Total number of images processed
                    - 'success_count': Number of successful processes
                    - 'failure_count': Number of failed processes
                    - 'skipped_count': Number of skipped images

            Example:
                ```python
                drawer = BoundingBoxDrawer(json_format="coco")

                results = drawer.process_batch(
                    input_image_dir="/path/to/images",
                    input_json_dir="/path/to/json",
                    input_json_format="coco",
                    output_dir="/path/to/output",
                    font_size=20,
                    bbox_color="red",
                    show_confidence=True
                )

                print(f"Successfully processed: {results['success_count']} images")
                print(f"Failed: {results['failure_count']} images")
                ```
            """

        # Convert paths to Path objects
        input_image_dir = Path(input_image_dir)
        input_json_dir = Path(input_json_dir)
        output_dir = Path(output_dir)

        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Set default extensions
        if image_extensions is None:
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        if json_extensions is None:
            json_extensions = ['.json']

        # Validate input format
        if input_json_format.lower() not in ["coco", "roboflow"]:
            raise ValueError(
                "input_json_format must be either 'coco' or 'roboflow'")

        # Validate directories
        if not input_image_dir.exists():
            raise FileNotFoundError(f"Image directory not found: {input_image_dir}")
        if not input_json_dir.exists():
            raise FileNotFoundError(f"JSON directory not found: {input_json_dir}")

        self.logger.info(f"Starting batch processing...")
        self.logger.info(f"Image directory: {input_image_dir}")
        self.logger.info(f"JSON directory: {input_json_dir}")
        self.logger.info(f"Output directory: {output_dir}")
        self.logger.info(f"JSON format: {input_json_format}")

        # Find all image files
        image_files = []
        for ext in image_extensions:
            image_files.extend(input_image_dir.glob(f"*{ext}"))
            image_files.extend(input_image_dir.glob(f"*{ext.upper()}"))

        if not image_files:
            self.logger.warning(f"No image files found in {input_image_dir}")
            return {
                'successful': [],
                'failed': [],
                'skipped': [],
                'total_processed': 0,
                'success_count': 0,
                'failure_count': 0,
                'skipped_count': 0
            }

        self.logger.info(f"Found {len(image_files)} image files to process")

        # Initialize results tracking
        results = {
            'successful': [],
            'failed': [],
            'skipped': [],
            'total_processed': 0,
            'success_count': 0,
            'failure_count': 0,
            'skipped_count': 0
        }

        # Create a temporary instance with updated format if needed
        original_format = self.json_format
        if input_json_format.lower() != self.json_format:
            self.json_format = input_json_format.lower()
            # Reinitialize processor for the new format
            if self.json_format == "coco":
                self.processor = COCOProcessor()
            else:
                self.processor = RoboflowProcessor()

        # Process each image file
        for image_file in image_files:
            try:
                # Look for matching JSON file
                json_file = None
                base_name = image_file.stem

                for ext in json_extensions:
                    potential_json = input_json_dir / f"{base_name}{ext}"
                    if potential_json.exists():
                        json_file = potential_json
                        break

                if json_file is None:
                    self.logger.warning(
                        f"No matching JSON file found for {image_file.name}")
                    results['skipped'].append(image_file.name)
                    results['skipped_count'] += 1
                    continue

                # Generate output filename
                output_filename = f"{base_name}_with_bboxes{image_file.suffix}"

                self.logger.info(
                    f"Processing {image_file.name} with {json_file.name}")

                # Process the image with optional parameter overrides
                success = self.process_image_with_annotations(
                    image_file_path=image_file,
                    json_file_path=json_file,
                    output_filename=output_filename,
                    custom_font_size=font_size,
                    custom_bbox_color=bbox_color,
                    custom_text_color=text_color,
                    custom_text_position=text_position,
                    custom_confidence_range=confidence_range,
                    custom_show_summary=show_summary,
                    custom_summary_position=summary_position,
                    custom_show_id=show_id,
                    custom_show_confidence=show_confidence,
                    custom_show_center=show_center,
                    custom_center_dot_size=center_dot_size,
                    custom_show_label=show_label
                )

                # Update output directory for the processed file
                if success:
                    # Move the file from default output directory to specified output directory
                    source_file = self.output_directory / output_filename
                    target_file = output_dir / output_filename

                    if source_file.exists() and source_file != target_file:
                        source_file.rename(target_file)

                    results['successful'].append(image_file.name)
                    results['success_count'] += 1
                    self.logger.info(f"Successfully processed {image_file.name}")
                else:
                    results['failed'].append(image_file.name)
                    results['failure_count'] += 1
                    self.logger.error(f"Failed to process {image_file.name}")

                results['total_processed'] += 1

            except Exception as e:
                self.logger.error(f"Error processing {image_file.name}: {str(e)}")
                results['failed'].append(image_file.name)
                results['failure_count'] += 1
                results['total_processed'] += 1

        # Restore original format if it was changed
        if input_json_format.lower() != original_format:
            self.json_format = original_format
            # Reinitialize processor for the original format
            if self.json_format == "coco":
                self.processor = COCOProcessor()
            else:
                self.processor = RoboflowProcessor()

        # Log summary
        self.logger.info(f"Batch processing completed:")
        self.logger.info(f"  Total images found: {len(image_files)}")
        self.logger.info(f"  Successfully processed: {results['success_count']}")
        self.logger.info(f"  Failed: {results['failure_count']}")
        self.logger.info(f"  Skipped (no JSON): {results['skipped_count']}")
        self.logger.info(
            f"  Success rate: {(results['success_count'] / max(results['total_processed'], 1)) * 100:.1f}%")

        return results


class COCOProcessor:
    """Processor for COCO format JSON files."""

    def extract_bbox_data(self, json_data: Dict, image_size: Tuple[int, int],
                          show_id: bool = True, show_confidence: bool = True) -> \
    List[Dict]:
        """
        Extract bounding box data from COCO format JSON.

        Args:
            json_data (Dict): Loaded JSON data in COCO format
            image_size (Tuple[int, int]): (width, height) of the image
            show_id (bool): Whether to include ID information
            show_confidence (bool): Whether to include confidence information

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
                x1 = x - (width / 2)
                y1 = y - (height / 2)
                x2 = x1 + width
                y2 = y1 + height

                # Calculate center from original COCO data (if available) or from bounding box
                if 'center_x' in annotation and 'center_y' in annotation:
                    center_x = annotation['center_x']
                    center_y = annotation['center_y']
                else:
                    # For COCO format, x and y are typically top-left corner
                    # but we'll handle both cases - check if it's center or corner based on values
                    center_x = x
                    center_y = y
                    # If the values seem to be corner coordinates, calculate center
                    if x < width and y < height:  # Likely corner coordinates
                        center_x = x + width / 2
                        center_y = y + height / 2

                # Get category information
                category_id = annotation.get('category_id')
                category_name = category_mapping.get(category_id,
                                                     f"Unknown_{category_id}")

                bbox_dict = {
                    'coordinates': (x1, y1, x2, y2),
                    'label': category_name,
                    'center_x': center_x,
                    'center_y': center_y
                }

                # Add ID if requested
                if show_id:
                    annotation_id = annotation.get('id', 'N/A')
                    bbox_dict['id'] = str(annotation_id)

                # COCO format doesn't typically have confidence scores
                # But if they exist in the annotation, include them if requested
                if show_confidence and 'score' in annotation:
                    confidence_percent = int(
                        round(annotation['score'] * 100, 0))
                    bbox_dict['confidence'] = f"{confidence_percent}%"

                bbox_data.append(bbox_dict)

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

    def extract_bbox_data(self, json_data: Dict, image_size: Tuple[int, int],
                          show_id: bool = True, show_confidence: bool = True) -> \
    List[Dict]:
        """
        Extract bounding box data from Roboflow format JSON.

        Args:
            json_data (Dict): Loaded JSON data in Roboflow format
            image_size (Tuple[int, int]): (width, height) of the image
            show_id (bool): Whether to include ID information
            show_confidence (bool): Whether to include confidence information

        Returns:
            List[Dict]: List of bounding box data dictionaries
        """
        bbox_data = []

        predictions = json_data.get('predictions', [])

        for prediction in predictions:
            try:
                # Extract center coordinates directly from Roboflow JSON
                center_x = prediction.get('x', 0)
                center_y = prediction.get('y', 0)
                width = prediction.get('width', 0)
                height = prediction.get('height', 0)

                # Convert center coordinates to corner coordinates for bounding box
                x1 = center_x - width / 2
                y1 = center_y - height / 2
                x2 = center_x + width / 2
                y2 = center_y + height / 2

                # Get class information
                class_name = prediction.get('class', 'Unknown')

                bbox_dict = {
                    'coordinates': (x1, y1, x2, y2),
                    'label': class_name,
                    'raw_confidence': prediction.get('confidence', 1.0),
                    # Store raw confidence for filtering
                    'center_x': center_x,  # Use center coordinates from JSON
                    'center_y': center_y
                }

                # Add confidence if requested
                if show_confidence:
                    raw_confidence = prediction.get('confidence', 1.0)
                    confidence_percent = int(round(raw_confidence * 100, 0))
                    bbox_dict['confidence'] = f"{confidence_percent}%"

                # Add ID if requested
                if show_id:
                    detection_id = prediction.get('detection_id', 'N/A')
                    if len(detection_id) > 8:
                        detection_id = detection_id[:8]
                    bbox_dict['id'] = detection_id

                bbox_data.append(bbox_dict)

            except Exception as e:
                logging.getLogger(__name__).warning(
                    f"Error processing prediction: {e}")
                continue

        return bbox_data


def draw_coco_bounding_boxes(image_path: str, json_path: str,
                             output_dir: str = "output",
                             output_filename: Optional[str] = None,
                             font_size: int = 16,
                             bbox_color: Optional[str] = None,
                             text_color: Optional[str] = None,
                             text_position: str = "top",
                             show_summary: bool = False,
                             summary_position: str = "bottom_right",
                             show_id: bool = True,
                             show_confidence: bool = True,
                             show_center: bool = False,
                             center_dot_size: int = 4,
                             show_label: bool = True) -> bool:
    """
    Convenience function to draw bounding boxes from COCO format JSON.

    Args:
        image_path (str): Path to the image file
        json_path (str): Path to the COCO format JSON file
        output_dir (str): Output directory for the annotated image
        output_filename (str, optional): Custom output filename
        font_size (int): Font size for text labels
        bbox_color (str, optional): Single color for all bounding boxes
        text_color (str, optional): Single color for all text
        text_position (str): Position of text ("top" or "bottom")
        show_summary (bool): Whether to show object count summary
        summary_position (str): Position of summary text
        show_id (bool): Whether to show object IDs
        show_confidence (bool): Whether to show confidence scores
        show_center (bool): Whether to draw center dots on bounding boxes
        center_dot_size (int): Size of center dots in pixels
        show_label (bool): Whether to show object labels (class names)

    Returns:
        bool: True if successful, False otherwise
    """
    drawer = BoundingBoxDrawer(
        json_format="coco", output_directory=output_dir,
        font_size=font_size, bbox_color=bbox_color,
        text_color=text_color, text_position=text_position,
        show_summary=show_summary, summary_position=summary_position,
        show_id=show_id, show_confidence=show_confidence,
        show_center=show_center, center_dot_size=center_dot_size,
        show_label=show_label
    )
    return drawer.process_image_with_annotations(image_path, json_path,
                                                 output_filename)


def draw_roboflow_bounding_boxes(image_path: str, json_path: str,
                                 output_dir: str = "output",
                                 output_filename: Optional[str] = None,
                                 font_size: int = 16,
                                 bbox_color: Optional[str] = None,
                                 text_color: Optional[str] = None,
                                 text_position: str = "top",
                                 confidence_range: Optional[
                                     Tuple[float, float]] = None,
                                 show_summary: bool = False,
                                 summary_position: str = "bottom_right",
                                 show_id: bool = True,
                                 show_confidence: bool = True,
                                 show_center: bool = False,
                                 center_dot_size: int = 4,
                                 show_label: bool = True) -> bool:
    """
    Convenience function to draw bounding boxes from Roboflow format JSON.

    Args:
        image_path (str): Path to the image file
        json_path (str): Path to the Roboflow format JSON file
        output_dir (str): Output directory for the annotated image
        output_filename (str, optional): Custom output filename
        font_size (int): Font size for text labels
        bbox_color (str, optional): Single color for all bounding boxes
        text_color (str, optional): Single color for all text
        text_position (str): Position of text ("top" or "bottom")
        confidence_range (Tuple[float, float], optional): Min and max confidence (e.g., (0.5, 0.8))
        show_summary (bool): Whether to show object count summary
        summary_position (str): Position of summary text
        show_id (bool): Whether to show object IDs
        show_confidence (bool): Whether to show confidence scores
        show_center (bool): Whether to draw center dots on bounding boxes
        center_dot_size (int): Size of center dots in pixels
        show_label (bool): Whether to show object labels (class names)

    Returns:
        bool: True if successful, False otherwise
    """
    drawer = BoundingBoxDrawer(
        json_format="roboflow", output_directory=output_dir,
        font_size=font_size, bbox_color=bbox_color,
        text_color=text_color, text_position=text_position,
        confidence_range=confidence_range, show_summary=show_summary,
        summary_position=summary_position, show_id=show_id,
        show_confidence=show_confidence, show_center=show_center,
        center_dot_size=center_dot_size, show_label=show_label
    )
    return drawer.process_image_with_annotations(image_path, json_path,
                                                 output_filename)


def process_batch_bounding_boxes(input_image_dir: Union[str, Path],
                                 input_json_dir: Union[str, Path],
                                 input_json_format: str,
                                 output_dir: Union[str, Path],
                                 font_size: int = 16,
                                 bbox_color: Optional[str] = None,
                                 text_color: Optional[str] = None,
                                 text_position: str = "top",
                                 show_center: bool = False,
                                 center_dot_size: int = 8,
                                 show_id: bool = True,
                                 show_label: bool = True,
                                 summary_position: str = "bottom_right",
                                 show_confidence: bool = True,
                                 confidence_range: Optional[
                                     Tuple[float, float]] = None,
                                 show_summary: bool = False) -> Dict[
    str, Union[List[str], int]]:
    """
    Convenience function for batch processing of images with bounding box annotations.

    This function creates a BoundingBoxDrawer instance and processes a batch of images
    with their corresponding JSON annotation files in a single operation.

    Args:
        input_image_dir (Union[str, Path]): Path to directory containing images
        input_json_dir (Union[str, Path]): Path to directory containing JSON files
        input_json_format (str): Format of JSON files ("coco" or "roboflow")
        output_dir (Union[str, Path]): Path to output directory
        font_size (int): Font size for text labels (default: 16)
        bbox_color (str, optional): Color for all bounding boxes
        text_color (str, optional): Color for all text
        text_position (str): Text position ("top" or "bottom")
        show_center (bool): Whether to show center dots
        center_dot_size (int): Size of center dots
        show_id (bool): Whether to show object IDs
        show_label (bool): Whether to show object labels
        summary_position (str): Position for object count summary
        show_confidence (bool): Whether to show confidence scores
        confidence_range (Tuple[float, float], optional): Range for confidence filtering
        show_summary (bool): Whether to show object count summary

    Returns:
        Dict containing processing results and statistics

    Example:
        ```python
        results = process_batch_bounding_boxes(
            input_image_dir="/path/to/images",
            input_json_dir="/path/to/json",
            input_json_format="coco",
            output_dir="/path/to/output",
            font_size=24,
            bbox_color="red",
            show_confidence=True
        )
        ```
    """

    # Create BoundingBoxDrawer instance
    drawer = BoundingBoxDrawer(
        json_format=input_json_format,
        output_directory=str(output_dir),
        font_size=font_size,
        bbox_color=bbox_color,
        text_color=text_color,
        text_position=text_position,
        show_center=show_center,
        center_dot_size=center_dot_size,
        show_id=show_id,
        show_label=show_label,
        summary_position=summary_position,
        show_confidence=show_confidence,
        confidence_range=confidence_range,
        show_summary=show_summary
    )

    # Process the batch
    return drawer.process_batch(
        input_image_dir=input_image_dir,
        input_json_dir=input_json_dir,
        input_json_format=input_json_format,
        output_dir=output_dir
    )


# ----------------------------------------------------------
# Example usage

# # Basic usage
# drawer = BoundingBoxDrawer()
# results = drawer.process_batch(
#     input_image_dir="/path/to/images",
#     input_json_dir="/path/to/json",
#     input_json_format="coco",
#     output_dir="/path/to/output"
# )

# # Advanced usage with customization
# results = drawer.process_batch(
#     input_image_dir="/path/to/images",
#     input_json_dir="/path/to/json",
#     input_json_format="roboflow",
#     output_dir="/path/to/output",
#     font_size=24,
#     bbox_color="red",
#     confidence_range=(0.5, 0.9),
#     show_summary=True,
#     show_center=True
# )

# # Using convenience function
# results = process_batch_bounding_boxes(
#     input_image_dir="/path/to/images",
#     input_json_dir="/path/to/json",
#     input_json_format="coco",
#     output_dir="/path/to/output",
#     font_size=20,
#     show_confidence=True
# )

# ----------------------------

# if __name__ == "__main__":
#     # Setup logging
#     logging.basicConfig(level=logging.INFO,
#                        format='%(asctime)s - %(levelname)s - %(message)s')

#     # Example 1: Roboflow with confidence filtering and summary
#     drawer = BoundingBoxDrawer(
#         json_format="roboflow",
#         output_directory="output/filtered",
#         font_size=18,
#         bbox_color="blue",
#         confidence_range=(0.5, 0.8),  # Only show objects with 50-80% confidence
#         show_summary=True,             # Show object count summary
#         summary_position="top_left",   # Position summary at top-left
#         show_id=False,                  # Hide ID and confidence on boxes
#         show_confidence=False          # Hide confidence on boxes
#     )

#     success = drawer.process_image_with_annotations(
#         "image.jpg",
#         "predictions.json",
#         output_filename="filtered_result.jpg"
#     )

#     # Example 2: COCO with summary at bottom right
#     coco_drawer = BoundingBoxDrawer(
#         json_format="coco",
#         output_directory="output/coco_summary",
#         show_summary=True,
#         summary_position="bottom_right",
#         show_id=True,
#         show_confidence=False          # Hide confidence on boxes
#     )

#     # Example 3: Using convenience function with all options
#     success = draw_roboflow_bounding_boxes(
#         "image.jpg",
#         "predictions.json",
#         "output_dir",
#         output_filename="confidence_filtered.jpg",
#         font_size=20,
#         bbox_color="green",
#         confidence_range=(0.6, 0.9),
#         show_summary=True,
#         summary_position="center",
#         show_id=False
#     )

#     # Example 4: Dynamic configuration changes
#     drawer.set_confidence_range(0.3, 0.7)
#     drawer.set_summary_options(True, "top_right")

# # Filter by confidence and show summary
# drawer = BoundingBoxDrawer(
#     json_format="roboflow",
#     confidence_range=(0.5, 0.8),    # 50-80% confidence only
#     show_summary=True,               # Show count summary
#     summary_position="top_left",     # Position at top-left
#     show_id=False                    # Hide IDs on boxes
# )
#
# # Process with custom overrides
# success = drawer.process_image_with_annotations(
#     "image.jpg", "predictions.json",
#     custom_confidence_range=(0.6, 0.9),  # Override confidence range
#     custom_summary_position="center"      # Override summary position
# )
#
# # Convenience function with all features
# draw_roboflow_bounding_boxes(
#     "image.jpg", "predictions.json", "output/",
#     confidence_range=(0.7, 1.0),
#     show_summary=True,
#     summary_position="bottom_right",
#     show_id=False
# )
