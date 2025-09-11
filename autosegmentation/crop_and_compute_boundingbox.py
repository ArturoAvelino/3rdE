from datetime import datetime
import numpy as np
from pathlib import Path
import json
from PIL import Image
import os

class CropImageAndWriteBBox:
    """
    CropImageAndWriteBBox - Class for processing segmented image data and
    creating bounding boxes around pixel groups.

    CropImageAndWriteBBox is a class designed to process segmented image data
    and extract individual objects by creating bounding boxes around pixel
    groups. It handles the creation of cropped images and associated
    metadata for each identified object in the segmentation.

    Args:
        segmented_image (np.ndarray): Array containing pixel data and group information
        path_raw_image (str): Path to the original image file
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
    - path_raw_image: Path to the original image file.
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
    processor = CropImageAndWriteBBox(
        segmented_image = segmented_image,
        path_raw_image = path_raw_image,
        path_image_no_bkgd  = path_image_no_bkground,
        sample_name = "BM4_E",
        output_dir = output_dir,
        padding = 10  # pixel units.
    )

    # Process all groups and save as PNG
    processor.process_all_groups(image_format='PNG')

    # Or process a specific group
    # processor.crop_and_write_bbox(group_number=1, image_format='PNG')

    Note:
    -----
    The class assumes that the input segmented_image array contains valid
    group labels and coordinate data. Groups labeled as -1 are ignored
    during processing.
    """

    def __init__(self, segmented_image, path_raw_image, path_image_no_bkgd,
                 sample_name, output_dir, padding=0):
        self.segmented_image = segmented_image
        self.path_raw_image = Path(path_raw_image)
        self.path_image_no_bkgd = Path(path_image_no_bkgd)
        self.sample_name = sample_name
        self.output_dir = Path(output_dir)
        self.padding = padding
        self.image_original = None
        self.image_no_bkgd = None

        # Create the output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load the original image
        self.load_original_image()


    def is_pixel_white(self, x, y, image):
        """
            Check if a pixel at the given coordinates is white [255, 255, 255].

            Args:
                x (int): X coordinate of the pixel
                y (int): Y coordinate of the pixel
                image (PIL.Image): The image to check

            Returns:
                bool: True if pixel is white, False otherwise
            """
        try:
            pixel = image.getpixel((x, y))
            # Handle both RGB and RGBA images
            if len(pixel) >= 3:
                return pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255
            return False
        except (IndexError, TypeError):
            return False

    def find_closest_non_white_pixel(self, center_x, center_y, group_number):
        """
            Find the closest non-white pixel to the center within the specific group of pixels.

            Args:
                center_x (int): X coordinate of the bounding box center
                center_y (int): Y coordinate of the bounding box center
                group_number (int): The group number to search within

            Returns:
                tuple: (new_x, new_y) coordinates of closest non-white pixel, or original center if none found
            """
        # Get pixels belonging to the specified group
        group_pixels = self.segmented_image[
            self.segmented_image[:, 6] == group_number]

        if len(group_pixels) == 0:
            return center_x, center_y

        # Extract x, y coordinates of group pixels
        group_x_coords = group_pixels[:, 4].astype(int)
        group_y_coords = group_pixels[:, 5].astype(int)

        # Create a set of group pixel coordinates for fast lookup
        group_pixel_set = set(zip(group_x_coords, group_y_coords))

        # Calculate maximum possible distance within the group
        max_x = np.max(group_x_coords)
        min_x = np.min(group_x_coords)
        max_y = np.max(group_y_coords)
        min_y = np.min(group_y_coords)

        max_radius = max(
            abs(center_x - min_x), abs(center_x - max_x),
            abs(center_y - min_y), abs(center_y - max_y)
        )

        # Spiral search from center outward, but only check pixels in the group
        for radius in range(1, max_radius + 1):
            # Check all pixels in the current radius ring
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    # Only check pixels at the current radius (not inside)
                    if max(abs(dx), abs(dy)) != radius:
                        continue

                    new_x = center_x + dx
                    new_y = center_y + dy

                    # Check if this pixel is part of the group
                    if (new_x, new_y) in group_pixel_set:
                        # Check if pixel is within image bounds
                        if (0 <= new_x < self.image_no_bkgd.width and
                                0 <= new_y < self.image_no_bkgd.height):
                            # Check if pixel is not white
                            if not self.is_pixel_white(new_x, new_y,
                                                       self.image_no_bkgd):
                                return new_x, new_y

        # If no non-white pixel found, return original center
        return center_x, center_y


    def load_original_image(self):
        """Load the original image for cropping."""
        try:
            self.image_original = Image.open(self.path_raw_image)
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

        # Padding
        # Before adding padding, check if any of the borders are in the edge of
        # the image before adding padding. If any of the borders are on
        # the edge then don't pad that border.
        if left == 0:
            left_padded = left
        # If the left border is closer to the image edge than the padding
        # value, then set the left border to be simply equal to
        # zero:
        elif 0 < left <= self.padding:
            left_padded = 0
        else:
            left_padded = left - self.padding

        if right == self.image_original.width - 1:
            right_padded = right
        # If the right border is closer to the image edge than the padding
        # value, then set the right border to be simply equal to
        # the right edge value:
        elif self.image_original.width - 1 - self.padding <= right < self.image_original.width - 1:
            right_padded = self.image_original.width - 1
        else:
            right_padded = right + self.padding

        if upper == 0:
            upper_padded = upper
        elif 0 < upper <= self.padding:
            upper_padded = 0
        else:
            upper_padded = upper - self.padding

        if lower == self.image_original.height - 1:
            lower_padded = lower
        elif self.image_original.height - 1 - self.padding <= lower < self.image_original.height - 1:
            lower_padded = self.image_original.height - 1
        else:
            lower_padded = lower + self.padding

        return left_padded, upper_padded, right_padded, lower_padded, left, upper, right, lower


    def create_json_metadata(self, group_number, bbox_coords,
                             use_alternative_center=False,
                             alternative_center_coords=None):
        """
            Create JSON metadata for a specific group.

            Args:
                group_number (int): The group number
                bbox_coords (tuple): (left, upper, right, lower) coordinates
                use_alternative_center (bool): Whether to use alternative center coordinates
                alternative_center_coords (tuple): (center_x, center_y) alternative coordinates

            Returns:
                dict: JSON metadata structure
            """

        left, upper, right, lower = bbox_coords

        # Determine the center of the box
        width = right - left
        height = lower - upper

        if use_alternative_center and alternative_center_coords:
            center_x, center_y = alternative_center_coords
        else:
            center_x = left + width // 2
            center_y = upper + height // 2

        area = width * height

        current_time = datetime.now().strftime("%Y-%m-%d / %H:%M:%S")
        current_year = datetime.now().strftime("%Y")

        return {
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
                    "id": 1000,
                    "name": "object",
                    "supercategory": "none"
                }
            ],
            "images": [
                {
                    "id": self.sample_name,
                    "license": 1,
                    "file_name": self.path_raw_image.name,
                    "height": self.image_original.height,
                    "width": self.image_original.width,
                    "date_captured": "none"
                }
            ],
            "annotations": [
                {
                    "id": group_number,
                    "image_id": self.path_raw_image.name,
                    "category_id": 1000,
                    "bbox": [
                        center_x,
                        center_y,
                        width,
                        height
                    ],
                    "area": area,
                    "segmentation": [],
                    "iscrowd": 0
                }
            ]
        }


    def crop_and_write_bbox(self, group_number,
                            image_format='JPG',
                            #old. check_white_center=False,
                            use_nonwhitepixel_as_bboxcenter=False):
        """
            Process a specific group: create crop and save metadata.

            Args:
                group_number (int): The group number to process
                image_format (str): Format to save the image ('PNG' or 'JPEG')
                #old. check_white_center (bool): Whether to check if center pixel is white
                use_nonwhitepixel_as_bboxcenter (bool): Whether to find and use closest non-white pixel as center
        """

        # Validate and normalize image format
        image_format = image_format.upper()
        if image_format not in ['PNG', 'JPEG', 'JPG']:
            raise ValueError(
                "Image format must be either 'PNG' or 'JPEG'/'JPG'")

        # Convert 'JPG' to 'JPEG' for PIL compatibility
        save_format = 'JPEG' if image_format in ['JPG',
                                                 'JPEG'] else image_format
        extension = 'jpg' if save_format == 'JPEG' else 'png'

        try:
            # Get bounding box coordinates
            (left_padded, upper_padded, right_padded, lower_padded, left, upper,
             right, lower) = self.get_bounding_box(group_number)

            crop_coords = left_padded, upper_padded, right_padded, lower_padded
            bbox_coords = left, upper, right, lower

            # Calculate original center
            width = right - left
            height = lower - upper
            center_x = left + width // 2
            center_y = upper + height // 2

            # Initialize variables for alternative center
            use_alternative_center = False
            alternative_center_coords = None

            # Check if center pixel is white and find an alternative if requested
            if use_nonwhitepixel_as_bboxcenter:
                if self.is_pixel_white(center_x, center_y, self.image_no_bkgd):
                    # Find closest non-white pixel within the specific group
                    alt_x, alt_y = self.find_closest_non_white_pixel(
                        center_x, center_y, group_number)

                    # Only use alternative if it's different from original
                    if alt_x != center_x or alt_y != center_y:
                        use_alternative_center = True
                        alternative_center_coords = (alt_x, alt_y)

            #old. if check_white_center:
            #old.     if self.is_pixel_white(center_x, center_y, self.image_no_bkgd):
            #old.         if use_nonwhitepixel_as_bboxcenter:
            #old.             # Find closest non-white pixel within the specific group
            #old.             alt_x, alt_y = self.find_closest_non_white_pixel(
            #old.                 center_x, center_y, group_number)
            #old.
            #old.             # Only use alternative if it's different from original
            #old.             if alt_x != center_x or alt_y != center_y:
            #old.                 use_alternative_center = True
            #old.                 alternative_center_coords = (alt_x, alt_y)

            # Crop the image
            cropped_image = self.image_original.crop(crop_coords)
            cropped_image_no_bkgd = self.image_no_bkgd.crop(crop_coords)

            # Generate output image filenames
            base_name = self.path_raw_image.stem
            base_no_bkgd_name = self.path_image_no_bkgd.stem
            crop_filename = f"crop_{group_number}_{base_name}.{extension}"
            crop_no_bkgd_filename = f"crop_{group_number}_{base_no_bkgd_name}.{extension}"

            # Generate output JSON filename
            json_filename = f"crop_{group_number}_{base_name}.json"

            # Save cropped image
            crop_path = self.output_dir / crop_filename
            crop_no_bkgd_path = self.output_dir / crop_no_bkgd_filename
            cropped_image.save(crop_path, format=save_format)
            cropped_image_no_bkgd.save(crop_no_bkgd_path, format=save_format)

            # Create and save JSON metadata
            json_data = self.create_json_metadata(
                group_number, bbox_coords,
                use_alternative_center=use_alternative_center,
                alternative_center_coords=alternative_center_coords
            )
            json_path = self.output_dir / json_filename
            with open(json_path, 'w') as f:
                json.dump(json_data, f, indent=4)

        except Exception as e:
            raise Exception(f"Error processing group {group_number}: {e}")


    def combine_json_metadata(self, output_filename='combined_metadata.json'):
        """
        Combines all individual JSON metadata files into a single COCO-format JSON file.

        This method reads all individual JSON files created by create_json_metadata(),
        combines their annotations into a single file while preserving the COCO format
        structure (info, licenses, categories, images, annotations).

        Args:
            output_filename (str): Name of the output combined JSON file

        Returns:
            Path: Path to the created combined JSON file
        """

        input_dir = Path(self.output_dir)

        # Get all JSON files in the input directory
        json_files = list(input_dir.glob('crop_*_*.json'))

        # Check if any JSON files were found
        if not json_files:
            raise FileNotFoundError(
                f"No JSON metadata files found in {input_dir}")

        # Initialize the combined data structure with COCO format
        combined_data = {
            "info": {},
            "licenses": [],
            "categories": [],
            "images": [],
            "annotations": []
        }

        # Use dictionaries to avoid duplicates
        categories_dict = {}
        images_dict = {}

        # Read and combine data from each JSON file
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                # For the first file, set the info and licenses sections
                if not combined_data["info"]:
                    combined_data["info"] = data.get("info", {})

                if not combined_data["licenses"]:
                    combined_data["licenses"] = data.get("licenses", [])

                # Add categories (avoid duplicates)
                for category in data.get("categories", []):
                    category_id = category["id"]
                    if category_id not in categories_dict:
                        categories_dict[category_id] = category

                # Add images (avoid duplicates)
                for image in data.get("images", []):
                    image_id = image["id"]
                    if image_id not in images_dict:
                        images_dict[image_id] = image

                # Add all annotations (these should be unique by design)
                combined_data["annotations"].extend(data.get("annotations", []))

            except json.JSONDecodeError as e:
                print(f"Error reading {json_file}: {e}")
                continue
            except KeyError as e:
                print(f"Invalid JSON structure in {json_file}: {e}")
                continue

        # Convert dictionaries back to lists
        combined_data["categories"] = list(categories_dict.values())
        combined_data["images"] = list(images_dict.values())

        # Sort annotations by id for consistency
        combined_data["annotations"].sort(key=lambda x: x["id"])

        # Sort categories and images by id for consistency
        combined_data["categories"].sort(key=lambda x: x["id"])
        # Sort images by id (handling both string and numeric ids)
        try:
            combined_data["images"].sort(
                key=lambda x: int(x["id"]) if isinstance(x["id"],
                                                         (str, int)) and str(
                    x["id"]).isdigit() else x["id"])
        except (ValueError, TypeError):
            combined_data["images"].sort(key=lambda x: str(x["id"]))

        # Save the combined data
        output_path = input_dir / output_filename
        try:
            with open(output_path, 'w') as f:
                json.dump(combined_data, f, indent=4)

            print(f"Successfully combined {len(json_files)} JSON files")
            print(f"Combined file contains:")
            print(f"  - {len(combined_data['categories'])} categories")
            print(f"  - {len(combined_data['images'])} images")
            print(f"  - {len(combined_data['annotations'])} annotations")
            print(f"Combined JSON saved to: {output_path}")

            return output_path
        except Exception as e:
            raise IOError(f"Error writing combined JSON file: {e}")


    def process_all_groups(self, combine_json_data=True,
                           image_format='JPG',
                           #old. check_white_center=False,
                           use_nonwhitepixel_as_bboxcenter=False):
        """
            Process all valid groups in the segmented image.

            Args:
                combine_json_data (bool): Whether to combine individual JSON files into one
                image_format (str): Format to save the images ('PNG' or 'JPG')
                #old. check_white_center (bool): Whether to check if center pixel is white
                use_nonwhitepixel_as_bboxcenter (bool): Whether to find and use closest non-white pixel as center
            """

        # Get unique group numbers (excluding -1 which typically represents invalid/background)
        unique_groups = np.unique(self.segmented_image[:, 6])
        valid_groups = unique_groups[unique_groups >= 0]

        for group_number in valid_groups:
            self.crop_and_write_bbox(
                int(group_number),
                image_format=image_format,
                #old. check_white_center=check_white_center,
                use_nonwhitepixel_as_bboxcenter=use_nonwhitepixel_as_bboxcenter
            )

        if combine_json_data:
            self.combine_json_metadata(
                output_filename=f"{self.path_raw_image.stem}_combined_metadata.json")


# # Basic usage (no white pixel checking)
# processor.process_all_groups(image_format='PNG')

# # Check for white center but don't replace coordinates
#old. processor.process_all_groups(check_white_center=True, image_format='PNG')

# # Check for white center and replace with closest non-white pixel
# processor.process_all_groups(
#     #old. check_white_center=True,
#     use_nonwhitepixel_as_bboxcenter=True,
#     image_format='PNG'
# )
