import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging


class COCOSplitter:
    """
    A class to split a COCO format JSON file into individual JSON files,
    one per image, with all annotations for that image.

    Each split JSON file contains:
    - Only the image entry for that specific image
    - Only the annotations for that image
    - Only the categories used in those annotations
    - The original info section (metadata)
    """

    def __init__(self,
                 output_directory: str = "split_annotations",
                 include_only_used_categories: bool = True,
                 skip_images_without_annotations: bool = False):
        """
        Initialize the COCOSplitter.

        Args:
            output_directory: Directory where split JSON files will be saved
            include_only_used_categories: If True, only include categories that are
                                         actually used in the image's annotations
            skip_images_without_annotations: If True, don't create JSON files for
                                            images with no annotations
        """
        self.output_directory = Path(output_directory)
        self.include_only_used_categories = include_only_used_categories
        self.skip_images_without_annotations = skip_images_without_annotations
        self.logger = logging.getLogger(__name__)

        # Create output directory if it doesn't exist
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def split_coco_json(self, combined_json_file_path: Union[str, Path]) -> Dict[str, bool]:
        """
        Split a COCO format JSON file into individual files per image.

        Args:
            combined_json_file_path: Path to the COCO format JSON file

        Returns:
            Dictionary mapping output filenames to success status
        """
        combined_json_file_path = Path(combined_json_file_path)

        # Validate input file exists
        if not combined_json_file_path.exists():
            self.logger.error(f"Input JSON file not found: {combined_json_file_path}")
            return {}

        try:
            # Load the combined JSON file
            self.logger.info(f"Loading combined JSON file: {combined_json_file_path}")
            with open(combined_json_file_path, 'r', encoding='utf-8') as f:
                combined_data = json.load(f)

            # Extract main sections
            images = combined_data.get('images', [])
            annotations = combined_data.get('annotations', [])
            categories = combined_data.get('categories', [])
            info = combined_data.get('info', {})

            self.logger.info(f"Found {len(images)} images, {len(annotations)} annotations, "
                           f"{len(categories)} categories")

            # Create category lookup dictionary
            category_dict = {cat['id']: cat for cat in categories}

            # Group annotations by image_id
            annotations_by_image = self._group_annotations_by_image(annotations)

            # Process each image
            results = {}
            processed_count = 0
            skipped_count = 0

            for image in images:
                image_id = image['id']
                file_name = image['file_name']

                # Get annotations for this image
                image_annotations = annotations_by_image.get(image_id, [])

                # Skip if no annotations and skip flag is set
                if not image_annotations and self.skip_images_without_annotations:
                    self.logger.info(f"Skipping image {file_name} (no annotations)")
                    skipped_count += 1
                    continue

                # Create individual JSON file
                success = self._create_individual_json(
                    image,
                    image_annotations,
                    category_dict,
                    info
                )

                results[file_name] = success
                if success:
                    processed_count += 1

            self.logger.info(f"Processing complete: {processed_count} files created, "
                           f"{skipped_count} skipped")

            return results

        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON file: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Error splitting COCO JSON: {e}")
            return {}

    def _group_annotations_by_image(self, annotations: List[Dict]) -> Dict[int, List[Dict]]:
        """
        Group annotations by their image_id.

        Args:
            annotations: List of annotation dictionaries

        Returns:
            Dictionary mapping image_id to list of annotations
        """
        grouped = {}
        for annotation in annotations:
            image_id = annotation.get('image_id')
            if image_id is not None:
                if image_id not in grouped:
                    grouped[image_id] = []
                grouped[image_id].append(annotation)

        return grouped

    def _create_individual_json(self,
                                image: Dict,
                                annotations: List[Dict],
                                category_dict: Dict[int, Dict],
                                info: Dict) -> bool:
        """
        Create an individual JSON file for a single image.

        Args:
            image: Image dictionary
            annotations: List of annotations for this image
            category_dict: Dictionary mapping category_id to category info
            info: Info section from original JSON

        Returns:
            True if successful, False otherwise
        """
        try:
            file_name = image['file_name']

            # Determine which categories to include
            if self.include_only_used_categories and annotations:
                # Get unique category IDs from annotations
                used_category_ids = set(ann['category_id'] for ann in annotations)
                categories_list = [category_dict[cat_id] for cat_id in used_category_ids
                                  if cat_id in category_dict]
            else:
                # Include all categories
                categories_list = list(category_dict.values())

            # Sort categories by ID for consistency
            categories_list = sorted(categories_list, key=lambda x: x['id'])

            # Create the individual JSON structure
            individual_json = {
                "images": [image],
                "categories": categories_list,
                "annotations": annotations,
                "info": info
            }

            # Generate output filename (replace image extension with .json)
            image_stem = Path(file_name).stem
            output_filename = f"{image_stem}.json"
            output_path = self.output_directory / output_filename

            # Write the JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(individual_json, f, indent=2)

            self.logger.info(f"Created: {output_filename} ({len(annotations)} annotations, "
                           f"{len(categories_list)} categories)")

            return True

        except Exception as e:
            self.logger.error(f"Error creating JSON for image {image.get('file_name', 'unknown')}: {e}")
            return False

# ########################################################60

# # Example usage
# if __name__ == "__main__":
#     # Setup logging
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s - %(message)s'
#     )

#     # Initialize the splitter
#     splitter = COCOSplitter(
#         output_directory="split_annotations",
#         include_only_used_categories=True,  # Only include used categories
#         skip_images_without_annotations=True  # Skip images with no annotations
#     )

#     # Split the combined JSON file
#     results = splitter.split_coco_json("path/to/your/combined_annotations.json")

#     # Check results
#     print(f"Successfully created {sum(results.values())} JSON files")