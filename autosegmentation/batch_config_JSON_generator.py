import json
from pathlib import Path
from typing import List, Tuple, Dict


class BatchConfigGenerator:
    """
    A utility class for generating JSON configuration files for batch image processing workflows.

    This class automates the creation of individual configuration files for image processing tasks
    by matching pairs of raw images and their corresponding no-background (processed) images.
    It's designed to facilitate batch processing of large image datasets where each image pair
    requires the same processing parameters but separate configuration files.

    Purpose:
    --------
    The BatchConfigGenerator streamlines the workflow for image processing pipelines by:
    - Automatically discovering and pairing raw images with their no-background counterparts
    - Generating standardized JSON configuration files for each image pair
    - Ensuring consistent processing parameters across all images in a batch
    - Handling file naming conventions and directory structure validation

    Key Features:
    -------------
    - Intelligent image pairing based on filename matching with suffix removal
    - Flexible file pattern matching using glob patterns
    - Robust error handling with informative error messages
    - Automatic output directory creation
    - Comprehensive validation of input directories and file existence
    - Support for various no-background image naming conventions

    Workflow:
    ---------
    1. Initialize with processing parameters and directory paths
    2. Validate that input directories exist and contain matching images
    3. Discover and pair raw images with their no-background counterparts
    4. Generate individual JSON configuration files for each matched pair
    5. Return list of generated configuration file paths for further processing

    Configuration File Structure:
    ----------------------------
    Each generated JSON file contains:
    - image_info: Paths to raw and no-background images, sample name
    - processing_parameters: Algorithm settings (max_distance, min_pixels, padding, cropping)
    - output: Directory path for processing results

    Supported Naming Conventions:
    ----------------------------
    The class automatically handles common no-background image suffixes:
    - "_no_bkgd", "_no_background", "_nobkgd", "_nobackground"

    Example Usage:
    --------------
    ```python
    # Initialize the generator
    generator = BatchConfigGenerator(
        sample_name="BM4_E",
        raw_image_pattern="*.jpg",
        raw_image_batch_path="/path/to/raw/images/",
        no_background_image_pattern="*_no_bkgd.png",
        no_background_image_batch_path="/path/to/processed/images/",
        max_distance=4.0,
        min_pixels=1000,
        padding=35,
        cropping=True,
        output_path="/path/to/output/configs/"
    )

    # Generate configuration files
    config_files = generator.generate_config_files()
    print(f"Generated {len(config_files)} configuration files")

    # Use the generated config files with your processing pipeline
    for config_file in config_files:
        # Process using your image processing classes
        processor = YourImageProcessor(config_path=config_file)
        processor.process()
    ```

    Error Handling:
    ---------------
    The class provides comprehensive error handling for common issues:
    - FileNotFoundError: When specified directories don't exist
    - ValueError: When no matching images are found or patterns don't match any files
    - Detailed warning messages for unmatched images
    - Graceful handling of file I/O errors during config generation

    Integration:
    ------------
    This class is designed to work seamlessly with image processing pipelines that
    accept JSON configuration files. It's particularly useful for:
    - Computer vision batch processing workflows
    - Scientific image analysis pipelines
    - Automated image segmentation and analysis tasks
    - Quality control and validation processes

    Parameters:
    -----------
    sample_name (str): Identifier for the sample batch
    raw_image_pattern (str): Glob pattern for raw image files (e.g., "*.jpg", "*.png")
    raw_image_batch_path (str): Directory path containing raw images
    no_background_image_pattern (str): Glob pattern for no-background images
    no_background_image_batch_path (str): Directory path containing no-background images
    max_distance (float): Maximum distance parameter for image processing algorithms
    min_pixels (int): Minimum pixel count threshold for object detection
    padding (int): Padding value for cropping operations
    cropping (bool): Enable/disable cropping functionality
    output_path (str): Directory where configuration files will be saved

    Returns:
    --------
    List[str]: Paths to generated configuration files

    Raises:
    -------
    FileNotFoundError: If input directories don't exist
    ValueError: If no matching image pairs are found
    """
    
    def __init__(self, sample_name: str, raw_image_pattern: str, raw_image_batch_path: str,
                 no_background_image_pattern: str, no_background_image_batch_path: str,
                 max_distance: float, min_pixels: int, padding: int, cropping: bool, output_path: str):
        """Initialize the batch config generator with processing parameters."""
        self.sample_name = sample_name
        self.raw_image_pattern = raw_image_pattern
        self.raw_image_batch_path = Path(raw_image_batch_path)
        self.no_background_image_pattern = no_background_image_pattern
        self.no_background_image_batch_path = Path(no_background_image_batch_path)
        self.max_distance = max_distance
        self.min_pixels = min_pixels
        self.padding = padding
        self.cropping = cropping
        self.output_path = Path(output_path)
    
    def generate_config_files(self) -> List[str]:
        """Generate configuration JSON files for batch processing of images."""
        self._validate_directories()
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        matched_pairs = self._find_matching_image_pairs()
        return self._create_config_files(matched_pairs)
    
    def _validate_directories(self) -> None:
        """Validate that required directories exist."""
        if not self.raw_image_batch_path.exists():
            raise FileNotFoundError(f"Raw image directory not found: {self.raw_image_batch_path}")
        
        if not self.no_background_image_batch_path.exists():
            raise FileNotFoundError(f"No-background image directory not found: {self.no_background_image_batch_path}")
    
    def _find_matching_image_pairs(self) -> List[Tuple[str, Path, Path]]:
        """Find and return matching pairs of raw and no-background images."""
        raw_images_dict = self._get_raw_images_dict()
        no_background_dict = self._get_no_background_images_dict()
        
        matched_pairs = []
        for base_name, raw_file in raw_images_dict.items():
            if base_name in no_background_dict:
                matched_pairs.append((base_name, raw_file, no_background_dict[base_name]))
            else:
                print(f"Warning: No matching no-background image found for {raw_file.name}")
        
        if not matched_pairs:
            raise ValueError("No matching image pairs found between raw and no-background images")
        
        print(f"Found {len(matched_pairs)} matching image pairs")
        return matched_pairs
    
    def _get_raw_images_dict(self) -> Dict[str, Path]:
        """Get a dictionary of raw images indexed by base name."""
        raw_image_files = list(self.raw_image_batch_path.glob(self.raw_image_pattern))
        
        if not raw_image_files:
            raise ValueError(f"No raw images found matching pattern '{self.raw_image_pattern}' in {self.raw_image_batch_path}")
        
        return {file.stem: file for file in raw_image_files}
    
    def _get_no_background_images_dict(self) -> Dict[str, Path]:
        """Get a dictionary of no-background images indexed by base name."""
        no_background_files = list(self.no_background_image_batch_path.glob(self.no_background_image_pattern))
        
        if not no_background_files:
            raise ValueError(f"No no-background images found matching pattern '{self.no_background_image_pattern}' in {self.no_background_image_batch_path}")
        
        no_background_dict = {}
        suffixes_to_remove = ["_no_bkgd", "_no_background", "_nobkgd", "_nobackground"]
        
        for file in no_background_files:
            base_name = file.stem
            for suffix in suffixes_to_remove:
                if base_name.endswith(suffix):
                    base_name = base_name[:-len(suffix)]
                    break
            no_background_dict[base_name] = file
        
        return no_background_dict
    
    def _create_config_files(self, matched_pairs: List[Tuple[str, Path, Path]]) -> List[str]:
        """Create configuration files for matched image pairs."""
        generated_config_files = []
        
        for base_name, raw_file, no_background_file in matched_pairs:
            config_data = self._create_config_data(base_name, raw_file, no_background_file)
            config_filepath = self.output_path / f"{base_name}_config.json"
            
            try:
                with open(config_filepath, 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                generated_config_files.append(str(config_filepath))
                print(f"Generated config file: {config_filepath.name}")
                
            except Exception as e:
                print(f"Error writing config file {config_filepath.name}: {str(e)}")
                continue
        
        print(f"\nSuccessfully generated {len(generated_config_files)} configuration files")
        return generated_config_files
    
    def _create_config_data(self, base_name: str, raw_file: Path, no_background_file: Path) -> Dict:
        """Create a configuration data dictionary for a single image pair."""
        return {
            "image_info": {
                "sample_name": self.sample_name,
                "raw_image": {
                    "path": str(raw_file.absolute())
                },
                "no_background_image": {
                    "path": str(no_background_file.absolute())
                }
            },
            "processing_parameters": {
                "max_distance": self.max_distance,
                "min_pixels": self.min_pixels,
                "padding": self.padding,
                "cropping": "true" if self.cropping else "false"
            },
            "output": {
                "directory": f"{self.output_path}/{base_name}_segm/"
            }
        }


# For backward compatibility, but I don't need it.
#
# def generate_batch_config_files(
#         sample_name: str,
#         raw_image_pattern: str,
#         raw_image_batch_path: str,
#         no_background_image_pattern: str,
#         no_background_image_batch_path: str,
#         max_distance: float,
#         min_pixels: int,
#         padding: int,
#         cropping: bool,
#         output_path: str
#     ) -> List[str]:
#     """Generate configuration JSON files for batch processing of images."""
#     generator = BatchConfigGenerator(
#         sample_name, raw_image_pattern, raw_image_batch_path,
#         no_background_image_pattern, no_background_image_batch_path,
#         max_distance, min_pixels, padding, cropping, output_path
#     )
#     return generator.generate_config_files()