import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

class SegmentationProcessor:
    def __init__(self, json_file_path, output_dir='output', padding=0, use_bbox=False):
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
                max(0, min(x_coords) - self.padding),
                max(0, min(y_coords) - self.padding),
                min(self.image_width, max(x_coords) + self.padding),
                min(self.image_height, max(y_coords) + self.padding)
            )

    def compute_normalized_values(self, min_x, min_y, max_x, max_y):
        """
        Compute normalized center coordinates and dimensions.
        
        Args:
            min_x, min_y, max_x, max_y (float): Boundary coordinates
            
        Returns:
            tuple: (center_x, center_y, width, height) normalized to [0,1]
        """
        width = max_x - min_x
        height = max_y - min_y
        center_x = (min_x + width/2) / self.image_width
        center_y = (min_y + height/2) / self.image_height
        norm_width = width / self.image_width
        norm_height = height / self.image_height
        return center_x, center_y, norm_width, norm_height

    def process_annotation(self, annotation):
        """
        Process a single annotation: crop image and save metadata.
        
        Args:
            annotation (dict): Annotation data from JSON
        """
        annotation_id = annotation['id']
        category_id = annotation['category_id']
        
        # Get bounds and crop image
        min_x, min_y, max_x, max_y = self.get_segment_bounds(annotation)
        cropped_image = self.image.crop((min_x, min_y, max_x, max_y))
        
        # Save cropped image
        image_output_path = self.output_dir / f"{annotation_id}.png"
        cropped_image.save(image_output_path)
        
        # Compute normalized values and save metadata
        center_x, center_y, norm_width, norm_height = self.compute_normalized_values(
            min_x, min_y, max_x, max_y)
        
        # Save metadata to text file
        text_output_path = self.output_dir / f"{annotation_id}.txt"
        with open(text_output_path, 'w') as f:
            f.write(f"{category_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}")

    def process_all(self):
        """Process all annotations in the JSON file."""
        for annotation in self.data['annotations']:
            self.process_annotation(annotation)

# Example usage:
# processor = SegmentationProcessor('path/to/your/file.json', padding=10)
# processor.process_all()