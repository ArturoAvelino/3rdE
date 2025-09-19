
#!/usr/bin/env python3
"""
Image Processing Pipeline

A comprehensive Python pipeline for batch processing images through multiple stages:
1. Background removal using color clustering
2. Object Segmentation
3. Bounding box drawing on processed images

The pipeline processes images organized in subfolders and maintains an organized
output structure for each processing step.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import json
import time
from dataclasses import dataclass, field

# Import your existing modules
from autosegmentation.background_remover import ImageSegmentationProcessor
from batch_processor import (
    generate_and_process_batch_configs,
    setup_logging
)
from computer_vision.bounding_box_drawer_image_annotation import BoundingBoxDrawer


@dataclass
class PipelineConfig:
    """Configuration settings for the image processing pipeline."""
    
    # Input/Output paths
    input_root_dir: Union[str, Path]
    output_root_dir: Optional[Union[str, Path]] = None
    
    # Image patterns
    image_pattern: str = "*.jpg"
    
    # Background removal settings
    n_clusters: int = 5
    background_clusters: List[int] = field(default_factory=lambda: [0, 4])
    
    # Segmentation settings
    max_distance: float = 4.0
    min_pixels: int = 1000
    padding: int = 35
    cropping: bool = True
    use_nonwhitepixel_as_bboxcenter: bool = False
    create_cropped_images: bool = True
    include_segmentation: bool = True
    
    # Bounding box settings
    font_size: int = 16
    bbox_color: Optional[str] = "red"
    text_color: Optional[str] = "white"
    text_position: str = "top"
    show_summary: bool = True
    show_id: bool = True
    show_label: bool = False
    show_confidence: bool = False
    show_center: bool = False
    center_dot_size: int = 8
    
    # Pipeline control
    skip_existing: bool = True
    parallel_processing: bool = False
    

class ImageProcessingPipeline:
    """
    A comprehensive pipeline for batch image processing through multiple stages.
    
    This class orchestrates the sequential execution of:
    1. Background removal
    2. Segmentation and cropping
    3. Bounding box visualization
    
    Features:
    - Processes images organized in subfolders
    - Maintains organized output structure
    - Handles errors gracefully with detailed logging
    - Supports skipping already processed images
    - Provides progress tracking and statistics
    """
    
    def __init__(self, config: PipelineConfig):
        """
        Initialize the pipeline with configuration settings.
        
        Args:
            config: PipelineConfig object containing all pipeline settings
        """
        self.config = config
        self.input_root = Path(config.input_root_dir)
        
        # Set the output root directory
        if config.output_root_dir:
            self.output_root = Path(config.output_root_dir)
        else:
            self.output_root = self.input_root
            
        self.logger = logging.getLogger(__name__)
        
        # Statistics tracking
        self.stats = {
            'total_images': 0,
            'processed_images': 0,
            'skipped_images': 0,
            'failed_images': 0,
            'step1_success': 0,
            'step2_success': 0,
            'step3_success': 0,
            'processing_times': []
        }
        
    def discover_images(self) -> Dict[str, List[Path]]:
        """
        Discover all images organized by subfolder.
        
        Returns:
            Dictionary mapping subfolder names to lists of image paths
        """
        self.logger.info(f"Discovering images in {self.input_root}")
        
        image_groups = {}
        
        # Find all subfolders
        for subfolder in self.input_root.iterdir():
            if not subfolder.is_dir():
                continue
                
            # Find images in this subfolder
            image_files = list(subfolder.glob(self.config.image_pattern))
            
            if image_files:
                image_groups[subfolder.name] = image_files
                self.logger.info(f"Found {len(image_files)} images in {subfolder.name}")
        
        total_images = sum(len(images) for images in image_groups.values())
        self.stats['total_images'] = total_images
        
        self.logger.info(f"Total discovered: {total_images} images in {len(image_groups)} subfolders")
        
        return image_groups
    
    def create_output_structure(self, subfolder_name: str, image_name: str) -> Dict[str, Path]:
        """
        Create organized output directory structure for an image.
        
        Args:
            subfolder_name: Name of the source subfolder
            image_name: Name of the image (without extension)
            
        Returns:
            Dictionary mapping step names to output directories
        """
        base_output = self.output_root / subfolder_name / image_name
        
        structure = {
            'base': base_output,
            'step1_background_removal': base_output / "1_background_removal",
            'step2_segmentation': base_output / "2_segmentation",
            'step3_bounding_boxes': base_output / "3_bounding_boxes"
        }
        
        # Create all directories
        for path in structure.values():
            path.mkdir(parents=True, exist_ok=True)
            
        return structure
    
    def step1_background_removal(self, image_path: Path, output_dir: Path) -> Tuple[bool, Optional[Path]]:
        """
        Execute step 1: Background removal using color clustering.
        
        Args:
            image_path: Path to the input image
            output_dir: Directory for background removal outputs
            
        Returns:
            Tuple of (success_flag, path_to_no_background_image)
        """
        try:
            self.logger.info(f"Step 1: Removing background from {image_path.name}")
            
            # Check if already processed
            no_bg_image_path = output_dir / f"{image_path.stem}_no_bkgd.png"
            if self.config.skip_existing and no_bg_image_path.exists():
                self.logger.info(f"Background removal already completed for {image_path.name}")
                return True, no_bg_image_path
            
            # Process background removal
            processor = ImageSegmentationProcessor(image_path, output_dir)
            processor.cluster_rgb_colors(n_clusters=self.config.n_clusters)
            processor.plot_rgb_rawdata()
            processor.plot_rgb_clusters()
            processor.plot_rgb_clusters_colorful()
            processor.plot_replaced_colors_in_image()
            processor.remove_background(background_clusters=self.config.background_clusters)
            
            if no_bg_image_path.exists():
                self.logger.info(f"Step 1 completed successfully for {image_path.name}")
                return True, no_bg_image_path
            else:
                self.logger.error(f"Step 1 failed: No background image not created for {image_path.name}")
                return False, None
                
        except Exception as e:
            self.logger.error(f"Step 1 failed for {image_path.name}: {str(e)}")
            return False, None
    
    def step2_segmentation(self, raw_image_path: Path, no_bg_image_path: Path, 
                          output_dir: Path) -> Tuple[bool, Optional[Path]]:
        """
        Execute step 2: Generate configurations and process segmentations.
        
        Args:
            raw_image_path: Path to the original image
            no_bg_image_path: Path to the background-removed image
            output_dir: Directory for segmentation outputs
            
        Returns:
            Tuple of (success_flag, path_to_json_directory)
        """
        try:
            self.logger.info(f"Step 2: Processing segmentation for {raw_image_path.name}")
            
            # Check if already processed
            json_output_dir = output_dir / "json_files"
            if (self.config.skip_existing and json_output_dir.exists() and 
                list(json_output_dir.glob("*.json"))):
                self.logger.info(f"Segmentation already completed for {raw_image_path.name}")
                return True, json_output_dir
            
            # Create subdirectories
            config_dir = output_dir / "configs"
            json_output_dir.mkdir(exist_ok=True)
            
            # Use the batch processing function
            results = generate_and_process_batch_configs(
                sample_name=raw_image_path.stem,
                raw_image_pattern=raw_image_path.name,
                raw_image_batch_path=str(raw_image_path.parent),
                no_background_image_pattern=no_bg_image_path.name,
                no_background_image_batch_path=str(no_bg_image_path.parent),
                max_distance=self.config.max_distance,
                min_pixels=self.config.min_pixels,
                padding=self.config.padding,
                cropping=self.config.cropping,
                config_output_path=str(config_dir),
                use_nonwhitepixel_as_bboxcenter=self.config.use_nonwhitepixel_as_bboxcenter,
                create_cropped_images=self.config.create_cropped_images,
                include_segmentation=self.config.include_segmentation
            )
            
            success = len(results.get('successful', [])) > 0
            
            if success:
                # Move/copy generated JSON files to our organized structure
                self._organize_segmentation_outputs(output_dir, raw_image_path.stem)
                self.logger.info(f"Step 2 completed successfully for {raw_image_path.name}")
                return True, json_output_dir
            else:
                self.logger.error(f"Step 2 failed: No successful segmentations for {raw_image_path.name}")
                return False, None
                
        except Exception as e:
            self.logger.error(f"Step 2 failed for {raw_image_path.name}: {str(e)}")
            return False, None
    
    def _organize_segmentation_outputs(self, output_dir: Path, image_stem: str):
        """
        Organize segmentation outputs into the pipeline structure.
        
        Args:
            output_dir: Base segmentation output directory
            image_stem: Image name without extension
        """
        try:
            # Look for generated segmentation directories
            segm_pattern = f"{image_stem}*_segm"
            
            for segm_dir in output_dir.parent.parent.glob(f"*/{segm_pattern}"):
                if segm_dir.is_dir():
                    # Copy JSON files to our json_files directory
                    json_files = list(segm_dir.glob("*.json"))
                    if json_files:
                        json_output = output_dir / "json_files"
                        json_output.mkdir(exist_ok=True)
                        
                        for json_file in json_files:
                            target = json_output / json_file.name
                            if not target.exists():
                                target.write_text(json_file.read_text())
                    
                    # Move crops if they exist
                    crops_source = segm_dir / "crops"
                    if crops_source.exists():
                        crops_target = output_dir / "crops"
                        if not crops_target.exists():
                            crops_source.rename(crops_target)
                            
        except Exception as e:
            self.logger.warning(f"Could not organize segmentation outputs: {str(e)}")
    
    def step3_bounding_boxes(self, no_bg_image_path: Path, json_dir: Path, 
                           output_dir: Path) -> bool:
        """
        Execute step 3: Draw bounding boxes on images.
        
        Args:
            no_bg_image_path: Path to the background-removed image
            json_dir: Directory containing JSON annotation files
            output_dir: Directory for bounding box outputs
            
        Returns:
            Success flag
        """
        try:
            self.logger.info(f"Step 3: Drawing bounding boxes for {no_bg_image_path.name}")
            
            # Check if already processed
            output_image_path = output_dir / f"{no_bg_image_path.stem}_with_bboxes.jpg"
            if self.config.skip_existing and output_image_path.exists():
                self.logger.info(f"Bounding box drawing already completed for {no_bg_image_path.name}")
                return True
            
            # Find JSON files for this image
            json_files = list(json_dir.glob("*.json"))
            if not json_files:
                self.logger.warning(f"No JSON files found for {no_bg_image_path.name}")
                return False
            
            # Use the first JSON file (you might want to modify this logic)
            json_file = json_files[0]
            
            # Initialize bounding box drawer
            drawer = BoundingBoxDrawer(
                json_format="coco",  # Adjust based on your JSON format
                output_directory=str(output_dir),
                font_size=self.config.font_size,
                bbox_color=self.config.bbox_color,
                text_color=self.config.text_color,
                text_position=self.config.text_position,
                show_summary=self.config.show_summary,
                show_id=self.config.show_id,
                show_confidence=self.config.show_confidence,
                show_center=self.config.show_center,
                center_dot_size=self.config.center_dot_size
            )
            
            # Process the image
            success = drawer.process_image_with_annotations(
                str(no_bg_image_path),
                str(json_file),
                output_filename=output_image_path.name
            )
            
            if success:
                self.logger.info(f"Step 3 completed successfully for {no_bg_image_path.name}")
                return True
            else:
                self.logger.error(f"Step 3 failed for {no_bg_image_path.name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Step 3 failed for {no_bg_image_path.name}: {str(e)}")
            return False
    
    def process_single_image(self, image_path: Path, subfolder_name: str) -> bool:
        """
        Process a single image through all pipeline steps.
        
        Args:
            image_path: Path to the input image
            subfolder_name: Name of the source subfolder
            
        Returns:
            Success flag
        """
        start_time = time.time()
        image_name = image_path.stem
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Processing: {subfolder_name}/{image_path.name}")
        self.logger.info(f"{'='*60}")
        
        try:
            # Create output structure
            output_dirs = self.create_output_structure(subfolder_name, image_name)
            
            # Step 1: Background removal
            step1_success, no_bg_image_path = self.step1_background_removal(
                image_path, output_dirs['step1_background_removal']
            )
            
            if step1_success:
                self.stats['step1_success'] += 1
            else:
                self.logger.error(f"Pipeline stopped at Step 1 for {image_path.name}")
                return False
            
            # Step 2: Segmentation
            step2_success, json_dir = self.step2_segmentation(
                image_path, no_bg_image_path, output_dirs['step2_segmentation']
            )
            
            if step2_success:
                self.stats['step2_success'] += 1
            else:
                self.logger.error(f"Pipeline stopped at Step 2 for {image_path.name}")
                return False
            
            # Step 3: Bounding boxes
            step3_success = self.step3_bounding_boxes(
                no_bg_image_path, json_dir, output_dirs['step3_bounding_boxes']
            )
            
            if step3_success:
                self.stats['step3_success'] += 1
            
            # Calculate processing time
            processing_time = time.time() - start_time
            self.stats['processing_times'].append(processing_time)
            
            success = step1_success and step2_success and step3_success
            
            if success:
                self.stats['processed_images'] += 1
                self.logger.info(f"✅ Successfully processed {image_path.name} in {processing_time:.2f}s")
            else:
                self.stats['failed_images'] += 1
                self.logger.error(f"❌ Failed to complete pipeline for {image_path.name}")
            
            return success
            
        except Exception as e:
            self.stats['failed_images'] += 1
            self.logger.error(f" Unexpected error processing {image_path.name}: {str(e)}")
            return False
    
    def run_pipeline(self) -> Dict:
        """
        Execute the complete pipeline on all discovered images.
        
        Returns:
            Dictionary containing processing statistics
        """
        self.logger.info(" Starting Image Processing Pipeline")
        self.logger.info(f"Input directory: {self.input_root}")
        self.logger.info(f"Output directory: {self.output_root}")
        
        # Discover images
        image_groups = self.discover_images()
        
        if not image_groups:
            self.logger.error("No images found to process")
            return self.stats
        
        # Process each image
        total_start_time = time.time()
        
        for subfolder_name, image_files in image_groups.items():
            self.logger.info(f"\n🔄 Processing subfolder: {subfolder_name}")
            
            for image_path in image_files:
                self.process_single_image(image_path, subfolder_name)
        
        # Calculate total processing time
        total_time = time.time() - total_start_time
        
        # Final statistics
        self.logger.info(f"\n{'='*60}")
        self.logger.info(" PIPELINE COMPLETE - FINAL STATISTICS")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Total images found: {self.stats['total_images']}")
        self.logger.info(f"Successfully processed: {self.stats['processed_images']}")
        self.logger.info(f"Failed: {self.stats['failed_images']}")
        self.logger.info(f"Skipped (already processed): {self.stats['skipped_images']}")
        self.logger.info(f"")
        self.logger.info(f"Step 1 (Background Removal) success rate: {self.stats['step1_success']}/{self.stats['total_images']}")
        self.logger.info(f"Step 2 (Segmentation) success rate: {self.stats['step2_success']}/{self.stats['total_images']}")
        self.logger.info(f"Step 3 (Bounding Boxes) success rate: {self.stats['step3_success']}/{self.stats['total_images']}")
        
        if self.stats['processing_times']:
            avg_time = sum(self.stats['processing_times']) / len(self.stats['processing_times'])
            self.logger.info(f"Average processing time per image: {avg_time:.2f}s")
        
        self.logger.info(f"Total processing time: {total_time:.2f}s")
        
        return self.stats


def create_sample_pipeline():
    """Create a sample pipeline configuration and demonstrate usage."""
    
    # Create configuration
    config = PipelineConfig(
        input_root_dir="/path/to/your/images_main_folder",
        output_root_dir="/path/to/your/output_folder",  # Optional, uses input_root if None
        image_pattern="*.jpg",
        
        # Background removal settings
        n_clusters=5,
        background_clusters=[0, 4],
        
        # Segmentation settings
        max_distance=4.0,
        min_pixels=1000,
        padding=35,
        cropping=True,
        create_cropped_images=True,
        include_segmentation=True,
        
        # Bounding box settings
        font_size=16,
        bbox_color="red",
        text_color="white",
        show_summary=True,
        show_id=True,
        
        # Pipeline control
        skip_existing=True  # Skip images that are already processed
    )
    
    return config


def main():
    """Main function demonstrating pipeline usage."""
    
    # Setup logging
    log_dir = Path("./pipeline_logs")
    log_dir.mkdir(exist_ok=True)
    setup_logging(log_dir)
    
    # Create pipeline configuration
    config = PipelineConfig(

        # 0. Input/Output paths
        input_root_dir="/Users/aavelino/Downloads/2025_09_10_Emilie/try_1/",
        # output_root_dir="/path/to/output",  # Optional
        image_pattern="*.jpg",
        
        # 1. Background removal settings
        # n_clusters=5, # Optional. Usually 5.
        # background_clusters=[0, 4], # Optional. Usually [0, 4].

        # 2. Segmentation settings
        max_distance=4.0,
        min_pixels=1000,
        padding=35,
        cropping = False,
        use_nonwhitepixel_as_bboxcenter=True,
        create_cropped_images=False,
        include_segmentation=True,

        # 3. Draw bounding box settings
        font_size=60,
        bbox_color="red",
        text_color="white",
        text_position="top",
        show_center=True,
        center_dot_size=12,
        show_id=True,
        show_label=False,
        show_summary=True,

        # 4. Pipeline control
        skip_existing=True
    )
    
    # Initialize and run a pipeline
    pipeline = ImageProcessingPipeline(config)
    results = pipeline.run_pipeline()
    
    # Print final results
    print(f"\n Pipeline completed!")
    print(f"Processed: {results['processed_images']}/{results['total_images']} images")


if __name__ == "__main__":
    main()

###############################################################

## Usage Examples
# # Here are several ways to use the pipeline:

# #!/usr/bin/env python3
# """
# Example usage scripts for the Image Processing Pipeline
# """

# from pathlib import Path
# from image_processing_pipeline import ImageProcessingPipeline, PipelineConfig
# from batch_processor import setup_logging


# def example_basic_usage():
#     """Basic pipeline usage example."""

#     # Setup logging
#     log_dir = Path("./logs")
#     log_dir.mkdir(exist_ok=True)
#     setup_logging(log_dir)

#     # Create basic configuration
#     config = PipelineConfig(
#         input_root_dir="/path/to/your/images_main_folder"
#     )

#     # Run pipeline
#     pipeline = ImageProcessingPipeline(config)
#     results = pipeline.run_pipeline()

#     print(f"Processed {results['processed_images']} images successfully")


# def example_custom_settings():
#     """Example with custom processing settings."""

#     # Setup logging
#     setup_logging(Path("./logs"))

#     # Custom configuration
#     config = PipelineConfig(
#         input_root_dir="/path/to/images",
#         output_root_dir="/path/to/output",

#         # Custom image pattern (e.g., for PNG files)
#         image_pattern="*.png",

#         # Background removal settings
#         n_clusters=6,  # More clusters for complex backgrounds
#         background_clusters=[0, 3, 5],  # Remove multiple background colors

#         # Segmentation settings
#         max_distance=3.0,  # Stricter distance for better separation
#         min_pixels=500,    # Smaller minimum object size
#         padding=50,        # Larger padding for crops

#         # Bounding box visualization
#         font_size=24,
#         bbox_color="blue",
#         text_color="yellow",
#         show_center=True,
#         center_dot_size=10,

#         # Don't skip existing files (reprocess everything)
#         skip_existing=False
#     )

#     # Run pipeline
#     pipeline = ImageProcessingPipeline(config)
#     results = pipeline.run_pipeline()


# def example_production_settings():
#     """Example for production/batch processing with optimized settings."""

#     config = PipelineConfig(
#         input_root_dir="/data/images",
#         output_root_dir="/data/processed",

#         # Production settings
#         skip_existing=True,     # Skip already processed
#         parallel_processing=False,  # Set to True if you implement parallel processing

#         # Optimized for large batches
#         n_clusters=5,
#         max_distance=4.0,
#         min_pixels=1000,

#         # Minimal bounding box visualization for speed
#         font_size=16,
#         show_summary=False,
#         show_id=False
#     )

#     # Setup logging with timestamps
#     log_dir = Path("/data/logs")
#     log_dir.mkdir(exist_ok=True)
#     setup_logging(log_dir)

#     # Run pipeline
#     pipeline = ImageProcessingPipeline(config)
#     results = pipeline.run_pipeline()

#     # Log final statistics
#     if results['failed_images'] > 0:
#         print(f"⚠️  {results['failed_images']} images failed processing")

#     print(f" Production run complete: {results['processed_images']} images processed")


# def example_selective_processing():
#     """Example showing how to process only specific subfolders or images."""

#     config = PipelineConfig(
#         input_root_dir="/path/to/images",
#         # Only process JPEG files from a specific pattern
#         image_pattern="sample_*.jpg"
#     )

#     pipeline = ImageProcessingPipeline(config)

#     # You could extend this to process only specific subfolders
#     # by modifying the discover_images method or filtering the results

#     results = pipeline.run_pipeline()


# if __name__ == "__main__":
#     # Run the basic example
#     example_basic_usage()

# # ------------------------------------

# ## How to Use
# # 1. **Install the pipeline**: Copy `image_processing_pipeline.py` to your project directory
# # 2. **Modify paths**: Update the paths in the configuration to match your setup
# # 3. **Run the pipeline**:

# from image_processing_pipeline import ImageProcessingPipeline, PipelineConfig
# from batch_processor import setup_logging

# # Setup logging
# setup_logging(Path("./logs"))

# # Configure pipeline
# config = PipelineConfig(
#    input_root_dir="/path/to/your/images_main_folder",
#    n_clusters=5,
#    background_clusters=[0, 4],
#    max_distance=4.0,
#    min_pixels=1000
# )

# # Run pipeline
# pipeline = ImageProcessingPipeline(config)
# results = pipeline.run_pipeline()
