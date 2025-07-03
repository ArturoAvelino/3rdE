import json
import glob
import os
from pathlib import Path
from typing import List, Dict, Any


def generate_batch_config_files(
        sample_name: str,
        raw_image_pattern: str,
        raw_image_batch_path: str,
        no_background_image_pattern: str,
        no_background_image_batch_path: str,
        max_distance: float,
        min_pixels: int,
        padding: int,
        cropping: bool,
        output_path: str
    ) -> List[str]:
    """
    Generate configuration JSON files for batch processing of images.
    
    This function creates individual JSON configuration files for each image pair
    (raw image and no-background image) found in the specified directories.
    Each configuration file contains all the parameters needed for image processing.
    
    Args:
        sample_name (str): Name identifier for the sample batch
        raw_image_pattern (str): Glob pattern to match raw image files (e.g., "*.jpg")
        raw_image_batch_path (str): Path to directory containing raw images
        no_background_image_pattern (str): Glob pattern to match no-background images (e.g., "*_no_bkgd.png")
        no_background_image_batch_path (str): Path to directory containing no-background images
        max_distance (float): Maximum distance between pixels for grouping
        min_pixels (int): Minimum number of pixels for valid objects
        padding (int): Padding value for cropping operations
        cropping (bool): Whether to enable cropping functionality
        output_path (str): Directory path where configuration files will be saved
    
    Returns:
        List[str]: List of paths to the generated configuration files
    
    Raises:
        FileNotFoundError: If any of the specified directories don't exist
        ValueError: If no matching images are found in the directories
    
    Example:
        >>> config_files = generate_batch_config_files(
        ...     sample_name="BM4_E",
        ...     raw_image_pattern="*.jpg",
        ...     raw_image_batch_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/for_background_removal/",
        ...     no_background_image_pattern="*_no_bkgd.png",
        ...     no_background_image_batch_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/segmentation/",
        ...     max_distance=4.0,
        ...     min_pixels=1000,
        ...     padding=35,
        ...     cropping=True,
        ...     output_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/segmentation/"
        ... )
        >>> print(f"Generated {len(config_files)} configuration files")
    """
    
    # Convert paths to Path objects for easier manipulation
    raw_image_path = Path(raw_image_batch_path)
    no_background_path = Path(no_background_image_batch_path)
    output_dir = Path(output_path)
    
    # Validate that directories exist
    if not raw_image_path.exists():
        raise FileNotFoundError(f"Raw image directory not found: {raw_image_batch_path}")
    
    if not no_background_path.exists():
        raise FileNotFoundError(f"No-background image directory not found: {no_background_image_batch_path}")
    
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all raw images matching the pattern
    raw_image_files = list(raw_image_path.glob(raw_image_pattern))
    
    if not raw_image_files:
        raise ValueError(f"No raw images found matching pattern '{raw_image_pattern}' in {raw_image_batch_path}")
    
    # Find all no-background images matching the pattern
    no_background_files = list(no_background_path.glob(no_background_image_pattern))
    
    if not no_background_files:
        raise ValueError(f"No no-background images found matching pattern '{no_background_image_pattern}' in {no_background_image_batch_path}")
    
    # Create dictionaries for a quick lookup by base name
    raw_images_dict = {file.stem: file for file in raw_image_files}
    no_background_dict = {}
    
    # Process no-background images to extract base names
    # Handle the case where no-background images have suffixes like "_no_bkgd"
    for file in no_background_files:
        # Extract the base name by removing common suffixes
        base_name = file.stem
        # Remove common suffixes like "_no_bkgd", "_no_background", etc.
        suffixes_to_remove = ["_no_bkgd", "_no_background", "_nobkgd", "_nobackground"]
        for suffix in suffixes_to_remove:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
                break
        no_background_dict[base_name] = file
    
    generated_config_files = []
    matched_pairs = []
    
    print(f"Found {len(raw_image_files)} raw images and {len(no_background_files)} no-background images")
    
    # Find matching pairs of raw and no-background images
    for base_name, raw_file in raw_images_dict.items():
        if base_name in no_background_dict:
            matched_pairs.append((base_name, raw_file, no_background_dict[base_name]))
        else:
            print(f"Warning: No matching no-background image found for {raw_file.name}")
    
    if not matched_pairs:
        raise ValueError("No matching image pairs found between raw and no-background images")
    
    print(f"Found {len(matched_pairs)} matching image pairs")

    # Generate configuration files for each matched pair
    for base_name, raw_file, no_background_file in matched_pairs:

        # Create a configuration dictionary
        config_data = {
            "image_info": {
                "sample_name": sample_name,
                "raw_image": {
                    "path": str(raw_file.absolute())
                },
                "no_background_image": {
                    "path": str(no_background_file.absolute())
                }
            },
            "processing_parameters": {
                "max_distance": max_distance,
                "min_pixels": min_pixels,
                "padding": padding,
                "cropping": "true" if cropping else "false"
            },
            "output": {
                "directory": f"{output_dir}/{base_name}_segm"
            }
        }
        
        # Create an output filename based on the base name
        config_filename = f"{base_name}_config.json"
        config_filepath = output_dir / config_filename
        
        # Write a configuration file
        try:
            with open(config_filepath, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            generated_config_files.append(str(config_filepath))
            print(f"Generated config file: {config_filename}")
            
        except Exception as e:
            print(f"Error writing config file {config_filename}: {str(e)}")
            continue
    
    print(f"\nSuccessfully generated {len(generated_config_files)} configuration files")
    return generated_config_files


def process_batch_with_configs(config_files: List[str]) -> None:
    """
    Process a batch of images using the generated configuration files.
    
    This function takes a list of configuration file paths and processes each one
    using the InstanceSegmentation class, similar to the single image processing
    shown in the main() function.
    
    Args:
        config_files (List[str]): List of paths to configuration JSON files
    
    Example:
        >>> config_files = generate_batch_config_files(...)
        >>> process_batch_with_configs(config_files)
    """
    
    logger = logging.getLogger(__name__)
    
    for config_file in config_files:
        try:
            logger.info(f"Processing configuration: {config_file}")
            
            # Initialize and process using the configuration file
            processor = InstanceSegmentation(config_path=config_file)
            processor.process()  # This will run all steps
            
            # Extract the computed values from the processor
            segmented_image = processor.segmented_image
            
            # Get other required values from the processor's configuration
            path_raw_image = processor.raw_image_path
            path_no_bkground_image = processor.image_path
            sample_name = processor.sample_name
            output_dir = processor.output_dir
            padding = processor.padding
            
            # Check if cropping is enabled
            cropping = bool(processor.cropping)
            
            if cropping:
                try:
                    processor_crop = CropImageAndWriteBBox(
                        segmented_image=segmented_image,
                        path_raw_image=path_raw_image,
                        path_image_no_bkgd=path_no_bkground_image,
                        sample_name=sample_name,
                        output_dir=output_dir,
                        padding=padding
                    )
                    
                    # Process all groups
                    processor_crop.process_all_groups(combine_json_data=True)
                    
                except Exception as e:
                    logger.error(f"Error in cropping process for {config_file}: {str(e)}")
                    continue
            
            logger.info(f"Successfully processed: {config_file}")
            
        except Exception as e:
            logger.error(f"Error processing {config_file}: {str(e)}")
            continue


# Example 1: Generate configuration files and then process them.
config_files = generate_batch_config_files(
    sample_name="BM4_E",
    raw_image_pattern="*.jpg",
    raw_image_batch_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/for_background_removal/",
    no_background_image_pattern="*_no_bkgd.png",
    no_background_image_batch_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/segmentation/",
    max_distance=4.0,
    min_pixels=1000,
    padding=35,
    cropping=True,
    output_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/segmentation/"
    )

# Process all generated configurations
# process_batch_with_configs(config_files)


# Example 2: Everything packed in a single function
def example_batch_processing():
    """
    Example function showing how to use the batch configuration generator.
    """
    
    # Example parameters
    sample_name = "BM4_E"
    raw_image_pattern = "*.jpg"
    raw_image_batch_path = "/Users/aavelino/Downloads/images/BM4_E_sandbox/"
    no_background_image_pattern = "*_no_bkgd.png"
    no_background_image_batch_path = "/Users/aavelino/Downloads/images/BM4_E_sandbox/clustering_crops/capt0011/"
    max_distance = 4.0
    min_pixels = 1000
    padding = 35
    cropping = True
    output_path = "/Users/aavelino/Downloads/images/BM4_E_sandbox/clustering_crops/capt0011/segmentation/"
    
    try:
        # Generate configuration files
        config_files = generate_batch_config_files(
            sample_name=sample_name,
            raw_image_pattern=raw_image_pattern,
            raw_image_batch_path=raw_image_batch_path,
            no_background_image_pattern=no_background_image_pattern,
            no_background_image_batch_path=no_background_image_batch_path,
            max_distance=max_distance,
            min_pixels=min_pixels,
            padding=padding,
            cropping=cropping,
            output_path=output_path
        )
        
        print(f"Generated {len(config_files)} configuration files")
        
        # Optionally process all generated configurations
        # process_batch_with_configs(config_files)
        
    except Exception as e:
        print(f"Error in batch processing: {str(e)}")

# example_batch_processing()
# -----------------

