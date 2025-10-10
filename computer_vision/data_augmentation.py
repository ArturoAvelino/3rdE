import cv2
import numpy as np
import json
import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict
from dataclasses import dataclass


@dataclass
class BoundingBox:
    """Data class to represent a bounding box."""
    center_x: float
    center_y: float
    width: float
    height: float
    
    def to_list(self) -> List[float]:
        """Convert bounding box to list format [x_top_left, y_top_left, width, height]."""
        x_tl = self.center_x - self.width / 2
        y_tl = self.center_y - self.height / 2
        return [x_tl, y_tl, self.width, self.height]
    
    @classmethod
    def from_top_left(cls, x: float, y: float, w: float, h: float) -> "BoundingBox":
        """Create a BoundingBox from top-left x,y and width,height."""
        center_x = x + w / 2
        center_y = y + h / 2
        return cls(center_x, center_y, w, h)
    
    def get_corners(self) -> np.ndarray:
        """Get the four corners of the bounding box as a numpy array."""
        half_w = self.width / 2
        half_h = self.height / 2
        
        corners = np.array([
            [self.center_x - half_w, self.center_y - half_h],  # Top-left
            [self.center_x + half_w, self.center_y - half_h],  # Top-right
            [self.center_x + half_w, self.center_y + half_h],  # Bottom-right
            [self.center_x - half_w, self.center_y + half_h]   # Bottom-left
        ])
        return corners


class ImageBoundingBoxTransformer:
    """
    A class to rotate and flip images along with their bounding boxes.
    
    This class handles transformations of images and their associated bounding boxes
    for computer vision tasks, particularly for data augmentation in object detection.
    """
    
    # Default fill color (blue) in BGR format for OpenCV
    DEFAULT_FILL_COLOR = (177.8, 119.4, 67.9)  # RGB [67.9, 119.4, 177.8] -> BGR
    
    def __init__(
        self,
        image_path: str,
        json_path: str,
        output_dir: str,
        angle: float = 0.0,
        flip_horizontal: bool = False,
        flip_vertical: bool = False,
        fill_color: Optional[Tuple[float, float, float]] = None,
        output_filename_pattern: Optional[str] = None
    ):
        """
        Initialize the ImageBoundingBoxTransformer.
        
        Args:
            image_path: Path to the input image file
            json_path: Path to the COCO format JSON file with bounding boxes
            output_dir: Directory where output files will be saved
            angle: Rotation angle in degrees (positive = counter-clockwise)
            flip_horizontal: Whether to flip the image horizontally
            flip_vertical: Whether to flip the image vertically
            fill_color: RGB tuple for border fill color (default: blue [67.9, 119.4, 177.8])
            output_filename_pattern: Custom pattern for output filenames (without extension)
                                    If None, auto-generates based on transformations
        """
        self.image_path = Path(image_path)
        self.json_path = Path(json_path)
        self.output_dir = Path(output_dir)
        self.angle = angle
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical
        
        # Set fill color (convert RGB to BGR for OpenCV)
        if fill_color is not None:
            self.fill_color = (fill_color[2], fill_color[1], fill_color[0])  # RGB to BGR
        else:
            self.fill_color = self.DEFAULT_FILL_COLOR
        
        self.output_filename_pattern = output_filename_pattern
        
        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Validate inputs
        self._validate_inputs()
        
        # Load image and annotations
        self.image = None
        self.annotations_data = None
        self.transformed_image = None
        self.transformed_annotations = None
        
    def _validate_inputs(self):
        """Validate input paths and parameters."""
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image file not found: {self.image_path}")
        
        if not self.json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Output directory ready: {self.output_dir}")
    
    def _load_data(self):
        """Load image and JSON annotations."""
        # Load image
        self.image = cv2.imread(str(self.image_path))
        if self.image is None:
            raise ValueError(f"Failed to load image: {self.image_path}")
        
        self.logger.info(f"Loaded image: {self.image.shape}")
        
        # Load JSON annotations
        with open(self.json_path, 'r') as f:
            self.annotations_data = json.load(f)
        
        # Validate JSON structure
        if 'annotations' not in self.annotations_data:
            raise ValueError("JSON file must contain 'annotations' field")
        
        self.logger.info(f"Loaded {len(self.annotations_data['annotations'])} annotations")
    
    def _flip_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply flip transformations to the image.
        
        Args:
            image: Input image
            
        Returns:
            Flipped image
        """
        flipped = image.copy()
        
        if self.flip_horizontal and self.flip_vertical:
            flipped = cv2.flip(flipped, -1)  # Flip both
            self.logger.info("Applied horizontal and vertical flip")
        elif self.flip_horizontal:
            flipped = cv2.flip(flipped, 1)  # Flip horizontally
            self.logger.info("Applied horizontal flip")
        elif self.flip_vertical:
            flipped = cv2.flip(flipped, 0)  # Flip vertically
            self.logger.info("Applied vertical flip")
        
        return flipped
    
    def _flip_bounding_box(
        self,
        bbox: BoundingBox,
        image_width: int,
        image_height: int
    ) -> BoundingBox:
        """
        Apply flip transformations to a bounding box.
        
        Args:
            bbox: Input bounding box
            image_width: Width of the image
            image_height: Height of the image
            
        Returns:
            Flipped bounding box
        """
        center_x = bbox.center_x
        center_y = bbox.center_y
        
        if self.flip_horizontal:
            center_x = image_width - center_x
        
        if self.flip_vertical:
            center_y = image_height - center_y
        
        return BoundingBox(center_x, center_y, bbox.width, bbox.height)
    
    def _rotate_image(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Rotate the image around its center.
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (rotated_image, rotation_matrix)
        """
        if abs(self.angle) < 1e-6:  # No rotation needed
            return image.copy(), np.eye(3)
        
        height, width = image.shape[:2]
        center = (width / 2, height / 2)
        
        # Get rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        
        # Calculate new image dimensions to fit the entire rotated image
        abs_cos = abs(rotation_matrix[0, 0])
        abs_sin = abs(rotation_matrix[0, 1])
        
        new_width = int(height * abs_sin + width * abs_cos)
        new_height = int(height * abs_cos + width * abs_sin)
        
        # Adjust the rotation matrix to account for translation
        rotation_matrix[0, 2] += (new_width / 2) - center[0]
        rotation_matrix[1, 2] += (new_height / 2) - center[1]
        
        # Perform rotation with border fill
        rotated = cv2.warpAffine(
            image,
            rotation_matrix,
            (new_width, new_height),
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=self.fill_color
        )
        
        self.logger.info(f"Rotated image by {self.angle} degrees")
        
        # Convert 2x3 matrix to 3x3 for easier computation
        rotation_matrix_3x3 = np.vstack([rotation_matrix, [0, 0, 1]])
        
        return rotated, rotation_matrix_3x3
    
    def _rotate_bounding_box(
        self,
        bbox: BoundingBox,
        rotation_matrix: np.ndarray
    ) -> BoundingBox:
        """
        Rotate a bounding box and compute new axis-aligned bounding box.
        
        Args:
            bbox: Input bounding box
            rotation_matrix: 3x3 rotation matrix
            
        Returns:
            New axis-aligned bounding box encompassing the rotated box
        """
        # Get the four corners of the bounding box
        corners = bbox.get_corners()
        
        # Add homogeneous coordinate (1) to each corner
        corners_homogeneous = np.hstack([corners, np.ones((4, 1))])
        
        # Apply rotation matrix to all corners
        rotated_corners = corners_homogeneous @ rotation_matrix.T
        
        # Extract x and y coordinates
        rotated_x = rotated_corners[:, 0]
        rotated_y = rotated_corners[:, 1]
        
        # Calculate new axis-aligned bounding box
        min_x = np.min(rotated_x)
        max_x = np.max(rotated_x)
        min_y = np.min(rotated_y)
        max_y = np.max(rotated_y)
        
        new_center_x = (min_x + max_x) / 2
        new_center_y = (min_y + max_y) / 2
        new_width = max_x - min_x
        new_height = max_y - min_y
        
        return BoundingBox(new_center_x, new_center_y, new_width, new_height)
    
    def _generate_output_filename(self) -> str:
        """
        Generate output filename based on transformations applied.
        
        Returns:
            Filename without extension
        """
        if self.output_filename_pattern is not None:
            return self.output_filename_pattern
        
        # Start with the original image name (without extension)
        base_name = self.image_path.stem
        
        transformations = []
        
        # Add flip information
        if self.flip_horizontal and self.flip_vertical:
            transformations.append("flip_HV")
        elif self.flip_horizontal:
            transformations.append("flip_H")
        elif self.flip_vertical:
            transformations.append("flip_V")
        
        # Add rotation information
        if abs(self.angle) > 1e-6:
            angle_str = f"rot{int(self.angle)}" if self.angle == int(self.angle) else f"rot{self.angle}"
            transformations.append(angle_str)
        
        # Combine all transformations
        if transformations:
            return f"{base_name}_{'_'.join(transformations)}"
        else:
            return f"{base_name}_transformed"
    
    def transform(self):
        """
        Apply all transformations to the image and bounding boxes.
        """
        self.logger.info("Starting transformation process...")
        
        # Load data
        self._load_data()
        
        # Step 1: Apply flip transformations first
        transformed_image = self._flip_image(self.image)
        height, width = self.image.shape[:2]
        
        # Transform bounding boxes for flip
        flipped_annotations = []
        for annotation in self.annotations_data['annotations']:
            bbox_data = annotation['bbox']
            bbox = BoundingBox.from_top_left(bbox_data[0], bbox_data[1], bbox_data[2], bbox_data[3])
            
            # Apply flip to bounding box
            flipped_bbox = self._flip_bounding_box(bbox, width, height)
            
            # Create new annotation with flipped bbox
            new_annotation = annotation.copy()
            new_annotation['bbox'] = flipped_bbox.to_list()
            flipped_annotations.append(new_annotation)
        
        # Step 2: Apply rotation
        rotated_image, rotation_matrix = self._rotate_image(transformed_image)
        
        # Transform bounding boxes for rotation
        rotated_annotations = []
        for annotation in flipped_annotations:
            bbox_data = annotation['bbox']
            bbox = BoundingBox.from_top_left(bbox_data[0], bbox_data[1], bbox_data[2], bbox_data[3])
            
            # Apply rotation to bounding box
            rotated_bbox = self._rotate_bounding_box(bbox, rotation_matrix)
            
            # Create new annotation with rotated bbox and area
            new_annotation = annotation.copy()

            # Round bbox values to integers for output JSON
            new_bbox_list = rotated_bbox.to_list()
            rounded_bbox = [int(round(v)) for v in new_bbox_list]
            new_annotation['bbox'] = rounded_bbox

            # Compute area as width * height of the final bbox and round to int
            #old area = float(rotated_bbox.width * rotated_bbox.height)
            #old new_annotation['area'] = int(round(area))
            area = rounded_bbox[2] * rounded_bbox[3]
            new_annotation['area'] = area
            rotated_annotations.append(new_annotation)
        
        # Store results
        self.transformed_image = rotated_image
        self.transformed_annotations = self.annotations_data.copy()
        self.transformed_annotations['annotations'] = rotated_annotations
        
        # Update image info if present
        if 'images' in self.transformed_annotations and len(self.transformed_annotations['images']) > 0:
            self.transformed_annotations['images'][0]['width'] = rotated_image.shape[1]
            self.transformed_annotations['images'][0]['height'] = rotated_image.shape[0]
        
        self.logger.info("Transformation completed successfully")
    
    def save(self):
        """
        Save the transformed image and annotations.
        """
        if self.transformed_image is None or self.transformed_annotations is None:
            raise RuntimeError("No transformed data to save. Call transform() first.")
        
        # Generate output filename
        output_name = self._generate_output_filename()
        
        # Save image
        image_output_path = self.output_dir / f"{output_name}.jpg"
        cv2.imwrite(str(image_output_path), self.transformed_image)
        self.logger.info(f"Saved transformed image: {image_output_path}")
        
        # Save JSON
        json_output_path = self.output_dir / f"{output_name}.json"
        with open(json_output_path, 'w') as f:
            json.dump(self.transformed_annotations, f, indent=2)
        self.logger.info(f"Saved transformed annotations: {json_output_path}")
        
        return image_output_path, json_output_path
    
    def process(self) -> Tuple[Path, Path]:
        """
        Complete processing: transform and save.
        
        Returns:
            Tuple of (image_output_path, json_output_path)
        """
        self.transform()
        return self.save()


# Convenience function for quick usage
def transform_image_and_boxes(
    image_path: str,
    json_path: str,
    output_dir: str,
    angle: float = 0.0,
    flip_horizontal: bool = False,
    flip_vertical: bool = False,
    fill_color: Optional[Tuple[float, float, float]] = None,
    output_filename_pattern: Optional[str] = None
) -> Tuple[Path, Path]:
    """
    Transform an image and its bounding boxes with rotation and/or flipping.
    
    Args:
        image_path: Path to the input image file
        json_path: Path to the COCO format JSON file with bounding boxes
        output_dir: Directory where output files will be saved
        angle: Rotation angle in degrees (positive = counter-clockwise)
        flip_horizontal: Whether to flip the image horizontally
        flip_vertical: Whether to flip the image vertically
        fill_color: RGB tuple for border fill color (default: blue [67.9, 119.4, 177.8])
        output_filename_pattern: Custom pattern for output filenames (without extension)
        
    Returns:
        Tuple of (image_output_path, json_output_path)
    
    Example:
        >>> transform_image_and_boxes(
        ...     "input/image.jpg",
        ...     "input/annotations.json",
        ...     "output/",
        ...     angle=45,
        ...     flip_horizontal=True
        ... )
    """
    transformer = ImageBoundingBoxTransformer(
        image_path=image_path,
        json_path=json_path,
        output_dir=output_dir,
        angle=angle,
        flip_horizontal=flip_horizontal,
        flip_vertical=flip_vertical,
        fill_color=fill_color,
        output_filename_pattern=output_filename_pattern
    )
    
    return transformer.process()

# ########################################################60

# # Usage examples

# import logging
# from pathlib import Path
# from image_bbox_transformer import ImageBoundingBoxTransformer, transform_image_and_boxes


# def setup_logging():
#     """Setup logging configuration"""
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )


# def main():
#     setup_logging()
#     logger = logging.getLogger(__name__)

#     logger.info("Starting image and bounding box transformation examples...")

#     # Example 1: Rotate image by 45 degrees
#     logger.info("\n=== Example 1: Rotation only (45 degrees) ===")
#     try:
#         img_path, json_path = transform_image_and_boxes(
#             image_path="input/sample_image.jpg",
#             json_path="input/sample_annotations.json",
#             output_dir="output/",
#             angle=45
#         )
#         logger.info(f"Output saved to: {img_path} and {json_path}")
#     except Exception as e:
#         logger.error(f"Example 1 failed: {e}")

#     # Example 2: Horizontal flip and rotate 40 degrees
#     logger.info("\n=== Example 2: Horizontal flip + 40 degree rotation ===")
#     try:
#         img_path, json_path = transform_image_and_boxes(
#             image_path="input/sample_image.jpg",
#             json_path="input/sample_annotations.json",
#             output_dir="output/",
#             angle=40,
#             flip_horizontal=True
#         )
#         logger.info(f"Output saved to: {img_path} and {json_path}")
#     except Exception as e:
#         logger.error(f"Example 2 failed: {e}")

#     # Example 3: Vertical flip and rotate -30 degrees
#     logger.info("\n=== Example 3: Vertical flip + (-30) degree rotation ===")
#     try:
#         img_path, json_path = transform_image_and_boxes(
#             image_path="input/sample_image.jpg",
#             json_path="input/sample_annotations.json",
#             output_dir="output/",
#             angle=-30,
#             flip_vertical=True
#         )
#         logger.info(f"Output saved to: {img_path} and {json_path}")
#     except Exception as e:
#         logger.error(f"Example 3 failed: {e}")

#     # Example 4: Using the class directly with custom settings
#     logger.info("\n=== Example 4: Using class directly with custom filename ===")
#     try:
#         transformer = ImageBoundingBoxTransformer(
#             image_path="input/sample_image.jpg",
#             json_path="input/sample_annotations.json",
#             output_dir="output/custom/",
#             angle=90,
#             flip_horizontal=True,
#             flip_vertical=False,
#             fill_color=(255, 0, 0),  # Red fill color (RGB)
#             output_filename_pattern="my_custom_output"
#         )

#         img_path, json_path = transformer.process()
#         logger.info(f"Output saved to: {img_path} and {json_path}")
#     except Exception as e:
#         logger.error(f"Example 4 failed: {e}")

#     # Example 5: Batch processing multiple angles
#     logger.info("\n=== Example 5: Batch processing ===")
#     angles = [0, 30, 60, 90, 120, 150, 180]
#     for angle in angles:
#         try:
#             img_path, json_path = transform_image_and_boxes(
#                 image_path="input/sample_image.jpg",
#                 json_path="input/sample_annotations.json",
#                 output_dir="output/batch/",
#                 angle=angle
#             )
#             logger.info(f"Processed angle {angle}: {img_path.name}")
#         except Exception as e:
#             logger.error(f"Failed to process angle {angle}: {e}")

#     logger.info("\n=== All examples completed ===")

# if __name__ == "__main__":
#     main()

# --------------------------------------------------------60

# # **Simple usage:**
#
# from image_bbox_transformer import transform_image_and_boxes
#
# transform_image_and_boxes(
#     image_path="path/to/image.jpg",
#     json_path="path/to/annotations.json",
#     output_dir="path/to/output/",
#     angle=45,
#     flip_horizontal=True
# )
#
# # **Advanced usage with custom settings:**
#
# from image_bbox_transformer import ImageBoundingBoxTransformer
#
# transformer = ImageBoundingBoxTransformer(
#     image_path="path/to/image.jpg",
#     json_path="path/to/annotations.json",
#     output_dir="path/to/output/",
#     angle=30,
#     flip_vertical=True,
#     fill_color=(255, 0, 0),  # Custom red color
#     output_filename_pattern="custom_name"
# )
#
# img_path, json_path = transformer.process()