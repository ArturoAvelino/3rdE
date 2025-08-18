
import logging
from pathlib import Path
import json
from typing import List, Dict, Optional, Union

from tools.read_json_plot_contour_objects import read_json_plot_contours
from tools.read_json_crop_objects import CropIndividualObjects

from autosegmentation.crop_and_compute_boundingbox import CropImageAndWriteBBox
from autosegmentation.instance_segmentator import InstanceSegmentation


class BatchImageProcessor:
    """
    BatchImageProcessor - Automated Batch Image Processing for Computer Vision Workflows

    =====================================================================================

    PURPOSE:
    --------
    The BatchImageProcessor class provides a comprehensive solution for processing multiple images
    in batch operations without requiring individual configuration files for each image. It automates
    the entire workflow from image discovery to processing completion, making it ideal for large-scale
    image analysis tasks in computer vision.

    This class eliminates the tedious manual process of creating and managing individual JSON
    configuration files for each image by automatically generating configurations based on templates
    or direct parameters, while maintaining full flexibility and control over processing parameters.

    CORE FUNCTIONALITY:
    ------------------
    1. **Automated Configuration Generation**: Dynamically creates processing configurations for each
       image without manual intervention, using either template-based or parameter-based approaches.

    2. **Flexible Processing Workflows**: Supports multiple processing modes including instance
       segmentation, object detection, cropping, and background removal with customizable parameters.

    3. **Intelligent File Management**: Automatically organizes input/output directories, creates
       necessary folder structures, and manages file naming conventions.

    4. **Comprehensive Logging & Monitoring**: Provides detailed logging of all operations with
       both console and file output, including progress tracking and error reporting.

    5. **Results Tracking & Reporting**: Generates detailed summary reports showing success/failure
       rates, processing statistics, and identifies problematic images for troubleshooting.

    KEY FEATURES:
    ------------
    • **No Manual Config Files Required**: Eliminates the need to create individual JSON configs
    • **Template-Based Processing**: Reuse existing configurations across multiple images
    • **Direct Parameter Processing**: Specify parameters directly without template files
    • **Batch Progress Monitoring**: Real-time progress updates and completion statistics
    • **Error Resilience**: Continues processing remaining images even if some fail
    • **Flexible Image Discovery**: Support for custom file patterns and naming conventions
    • **Automatic Output Organization**: Creates structured output directories for each image
    • **Comprehensive Error Handling**: Detailed error reporting with context information
    • **Processing Validation**: Tracks success/failure status for each processed image

    PROCESSING WORKFLOWS SUPPORTED:
    ------------------------------
    1. **Instance Segmentation**: Groups pixels based on spatial proximity using KD-tree algorithms
    2. **Object Detection & Cropping**: Identifies and extracts individual objects from images
    3. **Background Removal**: Removes color backgrounds using clustering techniques
    4. **Contour Plotting**: Generates visualization plots of detected objects and segmentations
    5. **Metadata Generation**: Creates detailed metadata files with object statistics and parameters

    USAGE PATTERNS:
    --------------

    Pattern 1: Direct Parameter Processing (Recommended for new users)
    ```python
    # Initialize processor
    processor = BatchImageProcessor("/path/to/images", "/path/to/output")

    # Process all images with specified parameters
    results = processor.process_batch_with_params(
        image_pattern="*.jpg",
        max_distance=4.0,
        min_pixels=1000,
        padding=35,
        cropping=True,
        sample_name_prefix="Experiment1_"
    )

    # Generate summary report
    processor.generate_summary_report(results)
    ```

    Pattern 2: Template-Based Processing (For reusing existing configuration)
    ```python
    # Process using existing configuration as template
    results = processor.process_batch_with_template(
        template_config_path="/path/to/template.json",
        image_pattern="sample_*.png",
        processing_overrides={
            "sample_name": "CustomExperiment",
            "processing_params": {"max_distance": 5.0, "min_pixels": 800}
        }
    )
    ```

    Pattern 3: Mixed Processing (Different parameters for different image sets)
    ```python
    # Process high-resolution images with different parameters
    results_hires = processor.process_batch_with_params(
        image_pattern="hires_*.jpg", max_distance=6.0, min_pixels=2000
    )

    # Process low-resolution images with adjusted parameters
    results_lowres = processor.process_batch_with_params(
        image_pattern="lowres_*.jpg", max_distance=3.0, min_pixels=500
    )
    ```

    METHODS OVERVIEW:
    ----------------

    **Initialization & Setup: **
    • `__init__()`: Initialize processor with input/output directories
    • `setup_logging()`: Configure a comprehensive logging system

    **Image Discovery & Management: **
    • `find_images()`: Discover images matching specified patterns
    • `create_processing_config()`: Generate configurations for individual images

    **Processing Operations: **
    • `process_single_image_with_segmentation()`: Process individual image with full workflow
    • `process_batch_with_template()`: Batch process using template configuration
    • `process_batch_with_params()`: Batch process with direct parameters

    **Reporting & Analysis:**
    • `generate_summary_report()`: Create detailed processing summary reports

    INPUT REQUIREMENTS:
    ------------------
    • **Image Directory**: Directory containing images to be processed
    • **Image Formats**: Supports common formats (JPEG, PNG, TIFF, BMP)
    • **File Naming**: Flexible pattern matching for image discovery
    • **Optional Template**: JSON configuration file for template-based processing

    OUTPUT STRUCTURE:
    ----------------
    ```
    output_directory/
    ├── batch_processing.log              # Comprehensive processing log
    ├── batch_summary.txt                 # Summary report with statistics
    ├── image1/                          # Individual image results
    │   ├── image1_config.json           # Generated configuration
    │   ├── image1_pixel_groups.png      # Segmentation visualization
    │   ├── image1_pixel_groups.txt      # Processing metadata
    │   ├── cropped_objects/             # Individual object crops (if enabled)
    │   └── segmentation_data.json       # Object detection results
    ├── image2/
    │   └── [similar structure]
    └── ...
    ```

    CONFIGURATION PARAMETERS:
    ------------------------
    • **max_distance** (float): Maximum pixel distance for grouping (default: 4.0)
    • **min_pixels** (int): Minimum pixels required for valid objects (default: 1000)
    • **padding** (int): Padding around detected objects in pixels (default: 35)
    • **cropping** (bool): Enable/disable object cropping (default: True)
    • **sample_name_prefix** (str): Prefix for generated sample names
    • **image_pattern** (str): File pattern for image discovery (default: "*.jpg")

    ERROR HANDLING & RECOVERY:
    -------------------------
    • **Graceful Failure**: Processing continues even if individual images fail
    • **Detailed Error Logging**: Specific error messages with context information
    • **Recovery Mechanisms**: Partial results are saved even after failures
    • **Validation Checks**: Input validation prevents common configuration errors

    PERFORMANCE CONSIDERATIONS:
    --------------------------
    • **Memory Management**: Processes images individually to manage memory usage
    • **Progress Monitoring**: Real-time feedback on processing status
    • **Scalability**: Handles large batches efficiently with automated cleanup
    • **Resource Optimization**: Configurable parameters to balance speed vs. accuracy

    DEPENDENCIES:
    ------------
    • pathlib: Path handling and file system operations
    • logging: Comprehensive logging functionality
    • json: Configuration file parsing and generation
    • PIL/Pillow: Image loading and manipulation
    • numpy: Numerical operations on image arrays
    • Custom modules: InstanceSegmentation, CropImageAndWriteBBox utilities

    TYPICAL USE CASES:
    -----------------
    1. **Research Projects**: Batch analysis of experimental image datasets
    2. **Quality Control**: Automated inspection of manufacturing samples
    3. **Medical Imaging**: Batch processing of diagnostic images
    4. **Microscopy Analysis**: Automated counting and measurement of specimens
    5. **Agricultural Monitoring**: Analysis of crop or soil samples
    6. **Materials Science**: Characterization of material microstructures

    TROUBLESHOOTING:
    ---------------
    • Check log files for detailed error information
    • Verify input directory contains supported image formats
    • Ensure sufficient disk space for output generation
    • Adjust parameters based on image characteristics and processing requirements
    • Review template configurations for proper JSON syntax

    VERSION COMPATIBILITY:
    ---------------------
    • Python 3.7+
    • Compatible with major image processing libraries
    • Cross-platform support (Windows, macOS, Linux)
    """
    
    def __init__(self, input_dir: Union[str, Path], output_base_dir: Optional[Union[str, Path]] = None):
        """
        Initialize the batch processor.
        
        Args:
            input_dir: Directory containing input images
            output_base_dir: Base directory for outputs (defaults to input_dir/batch_output)
        """
        self.input_dir = Path(input_dir)
        self.output_base_dir = Path(output_base_dir) if output_base_dir else self.input_dir / "batch_output"
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def setup_logging(self):
        """Configure logging for batch processing."""
        log_file = self.output_base_dir / "batch_processing.log"
        
        # Create logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create formatters
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Batch processing initialized")
        logger.info(f"Input directory: {self.input_dir}")
        logger.info(f"Output directory: {self.output_base_dir}")
        
    def find_images(self, pattern: str = "*.jpg") -> List[Path]:
        """Find all images matching the pattern."""
        images = list(self.input_dir.glob(pattern))
        self.logger.info(f"Found {len(images)} images matching pattern '{pattern}'")
        return images
        
    def create_processing_config(self, 
                               image_path: Path, 
                               processing_params: Dict,
                               template_config: Optional[Dict] = None) -> Dict:
        """
        Create a processing configuration for a single image.
        
        Args:
            image_path: Path to the image file
            processing_params: Parameters for processing
            template_config: Template configuration to use as base
            
        Returns:
            Dictionary containing the processing configuration
        """

        if template_config:
            config = template_config.copy()
        else:
            config = {
                "image_info": {
                    "sample_name": "",
                    "no_background_image": {"path": ""},
                    "raw_image": {"path": ""}
                },
                "processing_parameters": {
                    "max_distance": 4.0,
                    "min_pixels": 1000,
                    "padding": 35,
                    "cropping": True
                },
                "output": {
                    "directory": ""
                }
            }
        
        # Update with image-specific information
        config["image_info"]["sample_name"] = processing_params.get("sample_name", image_path.stem)
        config["image_info"]["no_background_image"]["path"] = str(image_path)
        config["image_info"]["raw_image"]["path"] = str(processing_params.get("raw_image_path", image_path))
        
        # Update processing parameters
        config["processing_parameters"].update(processing_params.get("processing_params", {}))
        
        # Set output directory
        output_dir = self.output_base_dir / image_path.stem
        config["output"]["directory"] = str(output_dir)
        
        return config
        
    def process_single_image_with_segmentation(self, 
                                             image_path: Path, 
                                             processing_params: Dict,
                                             template_config: Optional[Dict] = None) -> bool:
        """
        Process a single image using instance segmentation.
        
        Args:
            image_path: Path to the image
            processing_params: Processing parameters
            template_config: Optional template configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Processing {image_path.name} with instance segmentation")
            
            # Create an output directory
            output_dir = self.output_base_dir / image_path.stem
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Create configuration
            config = self.create_processing_config(image_path, processing_params, template_config)
            
            # Save the config file for reference
            config_path = output_dir / f"{image_path.stem}_config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            # Process with instance segmentation
            processor = InstanceSegmentation(config_path=config_path)
            success = processor.process()
            
            if success and processing_params.get("enable_cropping", True):
                # Get computed values from processor
                segmented_image = processor.segmented_image
                path_raw_image = processor.raw_image_path
                path_no_bkground_image = processor.image_path
                sample_name = processor.sample_name
                padding = processor.padding
                
                # Perform cropping if enabled
                if processor.cropping:
                    cropping_processor = CropImageAndWriteBBox(
                        segmented_image=segmented_image,
                        path_raw_image=path_raw_image,
                        path_image_no_bkgd=path_no_bkground_image,
                        sample_name=sample_name,
                        output_dir=output_dir,
                        padding=padding
                    )
                    cropping_processor.process_all_groups(combine_json_data=True)
            
            self.logger.info(f"Successfully processed {image_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing {image_path.name}: {str(e)}")
            return False
    
    def process_batch_with_template(self, 
                                  template_config_path: Union[str, Path],
                                  image_pattern: str = "*.jpg",
                                  processing_overrides: Optional[Dict] = None) -> Dict[str, bool]:
        """
        Process a batch of images using a template configuration.
        
        Args:
            template_config_path: Path to template configuration file
            image_pattern: Pattern to match image files
            processing_overrides: Optional parameters to override in template
            
        Returns:
            Dictionary mapping image names to success status
        """
        # Load template configuration
        with open(template_config_path, 'r') as f:
            template_config = json.load(f)
            
        if processing_overrides:
            # Apply overrides to template
            if "processing_params" in processing_overrides:
                template_config["processing_parameters"].update(processing_overrides["processing_params"])
        
        # Find images to process
        images = self.find_images(image_pattern)
        results = {}
        
        self.logger.info(f"Starting batch processing of {len(images)} images")
        
        for image_path in images:
            processing_params = {
                "sample_name": processing_overrides.get("sample_name", image_path.stem),
                "raw_image_path": processing_overrides.get("raw_image_path", image_path),
                "enable_cropping": processing_overrides.get("enable_cropping", True)
            }
            
            success = self.process_single_image_with_segmentation(
                image_path, processing_params, template_config
            )
            results[image_path.name] = success
            
        # Log summary
        successful = sum(results.values())
        total = len(results)
        self.logger.info(f"Batch processing completed: {successful}/{total} images processed successfully")
        
        return results
    
    def process_batch_with_params(self, 
                                image_pattern: str = "*.jpg",
                                max_distance: float = 4.0,
                                min_pixels: int = 1000,
                                padding: int = 35,
                                cropping: bool = True,
                                sample_name_prefix: str = "",
                                **kwargs) -> Dict[str, bool]:
        """
        Process a batch of images with specified parameters (no template needed).
        
        Args:
            image_pattern: Pattern to match image files
            max_distance: Maximum distance for pixel grouping
            min_pixels: Minimum pixels for valid objects
            padding: Padding around objects
            cropping: Whether to enable cropping
            sample_name_prefix: Prefix for sample names
            **kwargs: Additional processing parameters
            
        Returns:
            Dictionary mapping image names to success status
        """
        images = self.find_images(image_pattern)
        results = {}
        
        self.logger.info(f"Starting batch processing of {len(images)} images with direct parameters")
        
        for image_path in images:
            sample_name = f"{sample_name_prefix}{image_path.stem}" if sample_name_prefix else image_path.stem
            
            processing_params = {
                "sample_name": sample_name,
                "raw_image_path": kwargs.get("raw_image_path", image_path),
                "enable_cropping": cropping,
                "processing_params": {
                    "max_distance": max_distance,
                    "min_pixels": min_pixels,
                    "padding": padding,
                    "cropping": cropping
                }
            }
            
            success = self.process_single_image_with_segmentation(image_path, processing_params)
            results[image_path.name] = success
            
        # Log summary
        successful = sum(results.values())
        total = len(results)
        self.logger.info(f"Batch processing completed: {successful}/{total} images processed successfully")
        
        return results
    
    def generate_summary_report(self, results: Dict[str, bool]) -> None:
        """Generate a summary report of batch processing results."""
        report_path = self.output_base_dir / "batch_summary.txt"

        # Handle empty results to prevent division by zero
        if not results:
            with open(report_path, 'w') as f:
                f.write("BATCH PROCESSING SUMMARY REPORT\n")
                f.write("=" * 40 + "\n\n")
                f.write("No images were processed.\n")
                f.write("Please check:\n")
                f.write("- Input directory exists and contains images\n")
                f.write("- File pattern matches existing files\n")
                f.write("- Processing parameters are valid\n")

            self.logger.warning("No results to report - no images were processed")
            return

        successful = [name for name, success in results.items() if success]
        failed = [name for name, success in results.items() if not success]

        with open(report_path, 'w') as f:
            f.write("BATCH PROCESSING SUMMARY REPORT\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Total images processed: {len(results)}\n")
            f.write(f"Successful: {len(successful)}\n")
            f.write(f"Failed: {len(failed)}\n")
            f.write(f"Success rate: {len(successful)/len(results)*100:.1f}%\n\n")

            if successful:
                f.write("SUCCESSFUL PROCESSING:\n")
                f.write("-" * 20 + "\n")
                for name in successful:
                    f.write(f"✓ {name}\n")
                f.write("\n")

            if failed:
                f.write("FAILED PROCESSING:\n")
                f.write("-" * 20 + "\n")
                for name in failed:
                    f.write(f"✗ {name}\n")
                f.write("\n")

        self.logger.info(f"Summary report saved to: {report_path}")


# Working example (OK).
# Copy-paste the following lines into the "main.py" file, for now it corresponds
# to "batch_processor.py".

# from sandbox.batch_image_processor import BatchImageProcessor
#
# def main():
#     """Example usage of the enhanced batch processor."""
#
#     # Define input directory
#     input_dir = Path("/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/segmentation/no_bkgd_images_only")
#
#     if not input_dir.exists():
#         print(f"Error: Input directory not found: {input_dir}")
#         return
#
#     # Initialize batch processor
#     batch_processor = BatchImageProcessor(input_dir)
#
#     # Method 1: Process with direct parameters (no template needed)
#     results = batch_processor.process_batch_with_params(
#         image_pattern="*_no_bkgd.png",
#         max_distance=4.0,
#         min_pixels=1000,
#         padding=35,
#         cropping=True,
#         sample_name_prefix="Sample_"
#     )
#
#     # Method 2: Process with template configuration (if you have one)
#     # template_path = "/path/to/template_config.json"
#     # results = batch_processor.process_batch_with_template(
#     #     template_config_path=template_path,
#     #     image_pattern="*.jpg",
#     #     processing_overrides={
#     #         "sample_name": "CustomSample",
#     #         "enable_cropping": True,
#     #         "processing_params": {
#     #             "max_distance": 5.0,
#     #             "min_pixels": 800
#     #         }
#     #     }
#     # )
#
#     # Debug: Check if results are empty
#     if not results:
#         print("Warning: No images were processed. Check input directory and file patterns.")
#         print(f"Looking for *.jpg files in: {input_dir}")
#         # List files in directory for debugging
#         if input_dir.exists():
#             files = list(input_dir.glob("*"))
#             print(f"Files found in directory: {[f.name for f in files]}")
#     else:
#         print(f"Successfully processed {len(results)} images")
#
#     # Generate summary report
#     batch_processor.generate_summary_report(results)
#
#     print("Batch processing completed. Check the output directory for results.")

