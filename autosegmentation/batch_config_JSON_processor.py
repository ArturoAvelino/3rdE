
import logging
from pathlib import Path
import glob
import json
from typing import List
from autosegmentation.instance_segmentator import InstanceSegmentation
from autosegmentation.crop_and_compute_boundingbox import CropImageAndWriteBBox


class BatchConfigProcessor:
    """
    A comprehensive batch processing system for image segmentation and cropping operations.

    The BatchConfigProcessor class provides a robust framework for processing multiple JSON
    configuration files that define image segmentation and cropping tasks. It automates the
    entire pipeline from configuration file discovery to final processing results.

    ## Purpose
    This class is designed to:
    - Discover and validate JSON configuration files in a specified directory
    - Process images through instance segmentation using the InstanceSegmentation class
    - Optionally crop segmented objects and compute bounding boxes using CropImageAndWriteBBox
    - Provide comprehensive error handling and logging for batch operations
    - Generate detailed reports of processing results

    ## Processing Pipeline
    The class orchestrates a two-stage processing pipeline:
    1. **Instance Segmentation**: Uses InstanceSegmentation to process images and identify objects
    2. **Cropping & Bounding Box Generation**: Optionally crops individual objects and generates
       bounding box data using CropImageAndWriteBBox

    ## Configuration File Structure
    Expected JSON configuration files should contain:
    - `image_info`: Contains image paths and sample information
      - `no_background_image.path`: Path to the source image
      - `sample_name`: Identifier for the sample
    - `processing_parameters`: Processing settings
      - `max_distance`: Maximum distance parameter for segmentation
      - `min_pixels`: Minimum pixel count for object detection
      - `cropping`: Boolean flag to enable/disable cropping operations
    - `output`: Output directory specifications

    ## Key Features
    - **Automatic File Discovery**: Finds all JSON files matching a specified pattern
    - **Validation**: Validates configuration files before processing to catch errors early
    - **Robust Error Handling**: Continues processing even if individual files fail
    - **Comprehensive Logging**: Detailed logging for troubleshooting and monitoring
    - **Batch Results**: Returns detailed success/failure reports for all processed files
    - **File Information**: Can extract and summarize configuration file contents

    ## Usage Example
    ```python
    # Initialize processor for a directory containing configuration files
    processor = BatchConfigProcessor(
        json_path="/path/to/config/files",
        filename_pattern="*.json"
    )

    # Process all configuration files with validation
    results = processor.process_all_configs(validate_before_processing=True)

    # Check results
    print(f"Successfully processed: {len(results['successful'])} files")
    print(f"Failed to process: {len(results['failed'])} files")

    # Get detailed information about all configuration files
    files_info = processor.get_config_files_info()
    ```

    ## Error Handling
    The class provides multiple layers of error handling:
    - Directory validation during initialization
    - Configuration file validation before processing
    - Individual file processing error isolation
    - Comprehensive logging of all errors and warnings

    ## Dependencies
    - `InstanceSegmentation`: Handles the core image segmentation processing
    - `CropImageAndWriteBBox`: Handles object cropping and bounding box generation
    - Standard libraries: `pathlib`, `json`, `logging`, `glob`

    Args:
        json_path (str or Path): Path to the directory containing JSON configuration files
        filename_pattern (str): Glob pattern to match configuration files (default: "*.json")

    Raises:
        FileNotFoundError: If the specified directory doesn't exist
        NotADirectoryError: If the specified path is not a directory

    Attributes:
        json_path (Path): Path object for the configuration directory
        filename_pattern (str): Pattern used to match configuration files
        config_files (List[Path]): List of discovered configuration files
        logger (logging.Logger): Logger instance for the class
    """

    def __init__(self, json_path: str, filename_pattern: str = "*.json",
                 check_white_center: bool = False,
                 use_non_white_center: bool = False):
        """
        Initialize the BatchConfigProcessor.

        Args:
            json_path (str or Path): Path to the directory containing JSON files
            filename_pattern (str): Pattern to match all the configuration files
            check_white_center (bool): Whether to check for a white center in a
                cropping process (default: False)
        """
        self.json_path = Path(json_path)
        self.filename_pattern = filename_pattern
        self.check_white_center = check_white_center
        self.use_non_white_center = use_non_white_center
        self.config_files = []
        self.logger = logging.getLogger(__name__)

        # Validate the directory exists
        if not self.json_path.exists():
            raise FileNotFoundError(f"Directory not found: {self.json_path}")

        if not self.json_path.is_dir():
            raise NotADirectoryError(
                f"Path is not a directory: {self.json_path}")
    
    def find_config_files(self) -> List[Path]:
        """
        Find all configuration JSON files matching the pattern.
        
        Returns:
            List[Path]: List of paths to configuration files
        """
        # Use glob to find matching files
        pattern_path = self.json_path / self.filename_pattern
        self.config_files = list(self.json_path.glob(self.filename_pattern))
        
        if not self.config_files:
            self.logger.warning(f"No configuration files found matching pattern '{self.filename_pattern}' in {self.json_path}")
            return []
        
        # Sort files for a consistent processing order
        self.config_files.sort()
        self.logger.info(f"Found {len(self.config_files)} configuration files")
        
        return self.config_files
    
    def validate_config_file(self, config_path: Path) -> bool:
        """
        Validate a single configuration file.
        
        Args:
            config_path (Path): Path to the configuration file
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Check for required sections
            required_sections = ['image_info', 'processing_parameters', 'output']
            for section in required_sections:
                if section not in config:
                    self.logger.error(f"Missing required section '{section}' in {config_path}")
                    return False
            
            # Check for required image info
            image_info = config['image_info']
            if 'no_background_image' not in image_info or 'path' not in image_info['no_background_image']:
                self.logger.error(f"Missing image path information in {config_path}")
                return False
            
            # Check if the image file exists
            image_path = Path(image_info['no_background_image']['path'])
            if not image_path.exists():
                self.logger.error(f"Image file not found: {image_path} (referenced in {config_path})")
                return False
            
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in {config_path}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error validating {config_path}: {e}")
            return False
    
    def process_single_config(self, config_path: Path) -> bool:
        """
        Process a single configuration file.
        
        Args:
            config_path (Path): Path to the configuration file
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            self.logger.info(f"Processing configuration: {config_path}")
            
            # Initialize and process using InstanceSegmentation
            processor = InstanceSegmentation(config_path=config_path)
            processor.process()  # This will run all steps
            
            # Extract the computed values from the processor
            segmented_image = processor.segmented_image
            
            # Get other required values from the processor's configuration
            path_raw_image = processor.raw_image_path  # This should be the original raw image path
            path_no_bkground_image = processor.image_path  # This is the no-background image from config
            sample_name = processor.sample_name
            output_dir = processor.output_dir
            padding = processor.padding
            
            # ----------------------------
            # Crop and compute the bounding boxes for each object in the image
            cropping = bool(processor.cropping)
            
            if cropping:
                try:
                    processor_crop = CropImageAndWriteBBox(
                        segmented_image=segmented_image,
                        path_raw_image=path_raw_image,
                        path_image_no_bkgd=path_no_bkground_image,
                        sample_name=sample_name,
                        output_dir=output_dir,
                        padding=padding  # pixel units.
                    )
                    
                    # Process all groups
                    processor_crop.process_all_groups(
                        combine_json_data = True,
                        image_format = 'JPG', # JPG or PNG. Format of the output cropped images
                        check_white_center = self.check_white_center,
                        use_non_white_center = self.use_non_white_center
                    )
                    
                except Exception as e:
                    raise Exception(f"Error processing cropping for {config_path}: {str(e)}")
            
            self.logger.info(f"Successfully processed: {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing {config_path}: {str(e)}")
            return False
    
    def process_all_configs(self, validate_before_processing: bool = True) -> dict:
        """
        Process all configuration files found in the directory.
        
        Args:
            validate_before_processing (bool): Whether to validate config files before processing
            
        Returns:
            dict: Dictionary containing processing results with 'successful' and 'failed' lists
        """
        # Find configuration files
        config_files = self.find_config_files()
        
        if not config_files:
            return {'successful': [], 'failed': []}
        
        results = {
            'successful': [],
            'failed': []
        }
        
        for config_file in config_files:
            try:
                # Validate configuration file if requested
                if validate_before_processing:
                    if not self.validate_config_file(config_file):
                        results['failed'].append(str(config_file))
                        continue
                
                # Process the configuration file
                if self.process_single_config(config_file):
                    results['successful'].append(str(config_file))
                else:
                    results['failed'].append(str(config_file))
                    
            except Exception as e:
                self.logger.error(f"Unexpected error processing {config_file}: {str(e)}")
                results['failed'].append(str(config_file))
        
        # Log summary
        self.logger.info(f"Processing complete. Successful: {len(results['successful'])}, Failed: {len(results['failed'])}")
        
        return results
    
    def get_config_files_info(self) -> List[dict]:
        """
        Get information about all configuration files.
        
        Returns:
            List[dict]: List of dictionaries containing file information
        """
        config_files = self.find_config_files()
        files_info = []
        
        for config_file in config_files:
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                info = {
                    'file_path': str(config_file),
                    'file_name': config_file.name,
                    'valid': self.validate_config_file(config_file)
                }
                
                # Extract basic info if available
                if 'image_info' in config:
                    if 'sample_name' in config['image_info']:
                        info['sample_name'] = config['image_info']['sample_name']
                    if 'no_background_image' in config['image_info']:
                        info['image_path'] = config['image_info']['no_background_image'].get('path', 'N/A')
                
                if 'processing_parameters' in config:
                    info['max_distance'] = config['processing_parameters'].get('max_distance', 'N/A')
                    info['min_pixels'] = config['processing_parameters'].get('min_pixels', 'N/A')
                    info['cropping'] = config['processing_parameters'].get('cropping', 'N/A')
                
                files_info.append(info)
                
            except Exception as e:
                files_info.append({
                    'file_path': str(config_file),
                    'file_name': config_file.name,
                    'valid': False,
                    'error': str(e)
                })
        
        return files_info

# # Example usage with check_white_center=True
# processor = BatchConfigProcessor(
#     json_path="/path/to/config/files",
#     filename_pattern="*.json",
#     check_white_center=True
# )

# # Example usage with check_white_center=False (default)
# processor = BatchConfigProcessor(
#     json_path="/path/to/config/files",
#     filename_pattern="*.json",
#     check_white_center=False
# )

# # Or simply use the default value (False)
# processor = BatchConfigProcessor(
#     json_path="/path/to/config/files",
#     filename_pattern="*.json"
# )