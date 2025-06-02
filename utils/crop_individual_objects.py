import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path


class SegmentationProcessor:
    def __init__(self, json_file_path, output_dir='output', padding=0,
                 normalize_coords=False, use_bbox=False):
        """
        This class processes image segmentation data from a JSON file
        containing annotations with pixel coordinates. For each
        annotation, it crops the corresponding region from the original
        image and saves it as a PNG file. It also generates a text file
        with normalized coordinates (center_x, center_y, width, height)
        and category ID. The script supports optional padding around
        segments and can use either segmentation or bounding box
        coordinates.

        Initialize the processor with file paths and options.

        Args:
            json_file_path (str): Path to the JSON file
            output_dir (str): Directory for output files
            padding (int): Padding around segmentation coordinates
            use_bbox (bool): Whether to use bbox values instead of segmentation
        """
        self.json_file_path = Path(json_file_path)
        self.output_dir = Path(output_dir)
        self.padding = padding
        self.normalize_coords = normalize_coords
        self.use_bbox = use_bbox
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load and parse JSON file
        with open(json_file_path, 'r') as f:
            self.data = json.load(f)

        # Load the image
        image_filename = self.data['images'][0]['file_name']
        self.image_path = self.json_file_path.parent / image_filename
        self.image = Image.open(self.image_path)
        self.image_width = self.data['images'][0]['width']
        self.image_height = self.data['images'][0]['height']

    def get_segment_bounds(self, annotation):
        """
        Get the bounds of a segment either from segmentation or bbox.

        Args:
            annotation (dict): Annotation data from JSON

        Returns:
            tuple: (min_x, min_y, max_x, max_y)
        """
        if self.use_bbox and annotation['bbox']:
            x, y, w, h = annotation['bbox']
            return x, y, x + w, y + h
        else:
            coords = annotation['segmentation'][0]
            x_coords = coords[::2]
            y_coords = coords[1::2]
            return (
                max(0, min(x_coords)),
                max(0, min(y_coords)),
                min(self.image_width, max(x_coords)),
                min(self.image_height, max(y_coords))
            )

    def compute_normalized_values(self, min_x, min_y, max_x, max_y):
        """
        Computes normalized or non-normalized values based on the coordinates of
        the bounding box and the size of the image if normalization is enabled.

        Args:
            min_x: The x-coordinate of the top-left corner of the bounding box.
            min_y: The y-coordinate of the top-left corner of the bounding box.
            max_x: The x-coordinate of the bottom-right corner of the bounding box.
            max_y: The y-coordinate of the bottom-right corner of the bounding box.

        Returns:
            A tuple containing the computed center_x, center_y, width, and height of the bounding box. If
            normalization is enabled via self.normalize_coords, the values are normalized using the image
            dimensions (self.image_width and self.image_height). Otherwise, non-normalized values are returned.
        """

        if self.normalize_coords:
            width = max_x - min_x
            height = max_y - min_y
            center_x = (min_x + width / 2) / self.image_width
            center_y = (min_y + height / 2) / self.image_height
            norm_width = width / self.image_width
            norm_height = height / self.image_height
            return center_x, center_y, norm_width, norm_height

        else:
            width = max_x - min_x
            height = max_y - min_y
            center_x = round(width / 2, 0)
            center_y = round(height / 2, 0)
            return center_x, center_y, width, height

    def process_annotation(self, annotation):
        """
        Process a single annotation: crop image and save metadata.

        Args:
            annotation (dict): Annotation data from JSON
        """
        annotation_id = annotation['id']
        category_id = annotation['category_id']

        # Get bounds
        min_x, min_y, max_x, max_y = self.get_segment_bounds(annotation)

        # Compute the bounds with padding and crop the image.
        min_x_padded = max(0, min_x - self.padding)
        min_y_padded = max(0, min_y - self.padding)
        max_x_padded = min(self.image_width, max_x + self.padding)
        max_y_padded = min(self.image_height, max_y + self.padding)

        cropped_image = self.image.crop((min_x_padded, min_y_padded,
                                         max_x_padded, max_y_padded))

        # Save cropped image
        image_output_path = self.output_dir / f"{annotation_id}.png"
        cropped_image.save(image_output_path)

        # Compute normalized values and save metadata
        center_x, center_y, norm_width, norm_height = self.compute_normalized_values(
            min_x, min_y, max_x, max_y)

        # Save metadata to text file
        text_output_path = self.output_dir / f"{annotation_id}.txt"
        with open(text_output_path, 'w') as f:
            f.write(
                f"{category_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}")

    def process_all(self):
        """Process all annotations in the JSON file."""
        for annotation in self.data['annotations']:
            self.process_annotation(annotation)

# Example usage:
# processor = SegmentationProcessor('path/to/your/file.json', padding=10)
# processor.process_all()