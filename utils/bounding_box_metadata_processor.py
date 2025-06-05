import numpy as np
from pathlib import Path
import json
from PIL import Image
import os

class BoxAndCrop:
    def __init__(self, segmented_image, path_image_original, path_image_no_bkgd,
                 sample_name, output_dir):
        """
        BoxAndCrop is a class designed to process segmented image data
        and extract individual objects by creating bounding boxes around pixel
        groups. It handles the creation of cropped images and associated
        metadata for each identified object in the segmentation.

        Args:
            segmented_image (np.ndarray): Array containing pixel data and group information
            path_image_original (str): Path to the original image file
            sample_name (str): Name of the sample for JSON metadata
            output_dir (str): Directory where outputs will be saved

        Key Features:
        -------------
        - Creates bounding boxes around pixel groups using coordinate data
        - Crops original image based on computed bounding boxes
        - Generates standardized JSON metadata for each crop
        - Supports both PNG and JPG output formats
        - Creates output directory structure automatically

        Input Requirements:
        ------------------
        - segmented_image: Numpy array with shape (N, 7) where:
            * Columns 0-3: RGB and alpha values (not used)
            * Column 4: x-coordinates
            * Column 5: y-coordinates
            * Column 6: group labels (-1 for background, ≥0 for valid groups)
        - path_image_original: Path to the original image file.
        - path_image_no_bkgd : Path to the image file with background removed.
        - sample_name: Identifier for the sample being processed.
        - output_dir: Directory path where outputs will be saved.

        Output Structure:
        ----------------
        For each valid group, generates:
        1. Cropped image file:
           - Named as: "{original_filename}_{group_number}.{format}"
           - Format: PNG or JPG (user-selectable)

        2. JSON metadata file:
           - Named as: "{original_filename}_{group_number}.json"
           - Contains:
             * Sample information (name, original filename, dimensions)
             * Bounding box details (center coordinates, width, height)

        Usage Example:
        -------------
        processor = BoxAndCrop(
            segmented_image=segmented_image,
            path_image_original="path/to/image.jpg",
            path_image_no_bkgd = "path/to/image_no_background.jpg",
            sample_name="BM4_E",
            output_dir="path/to/output"
        )

        # Process all groups
        processor.process_all_groups(image_format='PNG')

        # Or process specific group
        # processor.process_group(group_number=1, image_format='JPG')

        Note:
        -----
        The class assumes that the input segmented_image array contains valid
        group labels and coordinate data. Groups labeled as -1 are ignored
        during processing.
        """

        self.segmented_image = segmented_image
        self.path_image_original = Path(path_image_original)
        self.path_image_no_bkgd = Path(path_image_no_bkgd)
        self.sample_name = sample_name
        self.output_dir = Path(output_dir)
        self.image_original = None
        self.image_no_bkgd  = None
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load the original image
        self.load_original_image()

    def load_original_image(self):
        """Load the original image for cropping."""
        try:
            self.image_original = Image.open(self.path_image_original)
            self.image_no_bkgd  = Image.open(self.path_image_no_bkgd)
        except Exception as e:
            raise Exception(f"Failed to load original image: {e}")

    def get_bounding_box(self, group_number):
        """
        Get the bounding box coordinates for a specific group.
        
        Args:
            group_number (int): The group number to process
            
        Returns:
            tuple: (left, upper, right, lower) coordinates of the bounding box
        """
        # Get pixels belonging to the specified group
        group_pixels = self.segmented_image[self.segmented_image[:, 6] == group_number]
        
        if len(group_pixels) == 0:
            raise ValueError(f"No pixels found for group {group_number}")
        
        # Get min and max coordinates (x: column 4, y: column 5)
        left = int(np.min(group_pixels[:, 4]))
        right = int(np.max(group_pixels[:, 4]))
        upper = int(np.min(group_pixels[:, 5]))
        lower = int(np.max(group_pixels[:, 5]))
        
        return left, upper, right, lower

    def create_json_metadata(self, group_number, bbox_coords):
        """
        Create JSON metadata for a specific group.
        
        Args:
            group_number (int): The group number
            bbox_coords (tuple): (left, upper, right, lower) coordinates
        
        Returns:
            dict: JSON metadata structure
        """
        left, upper, right, lower = bbox_coords
        width = right - left
        height = lower - upper
        center_x = left + width // 2
        center_y = upper + height // 2
        
        return {
            "image": [{
                "sample_name": self.sample_name,
                "file_name": self.path_image_original.name,
                "width": self.image_original.width,
                "height": self.image_original.height
            }],
            "annotations": [{
                "category_id": group_number,
                "bbox": [{
                    "center_x": center_x,
                    "center_y": center_y,
                    "box_width": width,
                    "box_height": height
                }]
            }]
        }

    def process_group(self, group_number, image_format='PNG'):
        """
        Process a specific group: create crop and save metadata.

        Args:
            group_number (int): The group number to process
            image_format (str): Format to save the image ('PNG' or 'JPEG')
        """
        # Validate and normalize image format
        image_format = image_format.upper()
        if image_format not in ['PNG', 'JPEG', 'JPG']:
            raise ValueError("Image format must be either 'PNG' or 'JPEG'/'JPG'")

        # Convert 'JPG' to 'JPEG' for PIL compatibility
        save_format = 'JPEG' if image_format in ['JPG', 'JPEG'] else image_format
        extension = 'jpg' if save_format == 'JPEG' else 'png'

        try:
            # Get bounding box coordinates
            bbox_coords = self.get_bounding_box(group_number)

            # Crop the image
            cropped_image         = self.image_original.crop(bbox_coords)
            cropped_image_no_bkgd = self.image_no_bkgd.crop(bbox_coords)

            # Generate output filenames
            base_name = self.path_image_original.stem
            base_no_bkgd_name = self.path_image_no_bkgd.stem
            crop_filename         = f"{base_name}_{group_number}.{extension}"
            crop_no_bkgd_filename = f"{base_no_bkgd_name}_{group_number}.{extension}"
            json_filename = f"{base_name}_{group_number}.json"

            # Save cropped image
            crop_path = self.output_dir / crop_filename
            crop_no_bkgd_path = self.output_dir / crop_no_bkgd_filename
            cropped_image.save(crop_path, format=save_format)
            cropped_image_no_bkgd.save(crop_no_bkgd_path, format=save_format)

            # Create and save JSON metadata
            json_data = self.create_json_metadata(group_number, bbox_coords)
            json_path = self.output_dir / json_filename
            with open(json_path, 'w') as f:
                json.dump(json_data, f, indent=4)

        except Exception as e:
            raise Exception(f"Error processing group {group_number}: {e}")

    def process_all_groups(self, image_format='PNG'):
        """
        Process all valid groups in the segmented image.
        
        Args:
            image_format (str): Format to save the images ('PNG' or 'JPG')
        """
        # Get unique group numbers (excluding -1 which typically represents invalid/background)
        unique_groups = np.unique(self.segmented_image[:, 6])
        valid_groups = unique_groups[unique_groups >= 0]
        
        for group_number in valid_groups:
            self.process_group(int(group_number), image_format)

# -----------------------------
# # Example usage

# from utils.bounding_box_metadata_processor import BoxAndCrop

# processor = BoxAndCrop(
#     segmented_image=segmented_image,
#     path_image_original= path_image_original,
#     sample_name="BM4_E",
#     output_dir="/Users/aavelino/PycharmProjects/Book_HandsOnML_withTF/Github/3rdEd/images/09_unsupervised_learning/soil_fauna/BM4_E/outputs/3_crop/"
# )

# # Process all groups and save as PNG
# processor.process_all_groups(image_format='PNG')

# # Or process a specific group and save as JPG
# # processor.process_group(group_number=1, image_format='JPG')
