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
from autosegmentation.background_remover import BackgroundRemover
from batch_processor import (
    generate_and_process_batch_configs,
    setup_logging
)
from computer_vision.bounding_box_drawer import BoundingBoxDrawer


@dataclass
class PipelineConfig:
    """Configuration settings for the image processing pipeline."""
    
    # 0. Input/Output paths
    input_root_dir: Union[str, Path]
    output_root_dir: Optional[Union[str, Path]] = None
    
    # Image patterns
    image_pattern: str = "*.jpg"
    
    # 1. Background removal settings
    n_clusters: int = 5
    background_clusters: List[int] = field(default_factory=lambda: [0, 4])
    
    # 2. Object segmentation settings
    max_distance: float = 4.0
    min_pixels: int = 1000
    padding: int = 35
    cropping: bool = True
    use_nonwhitepixel_as_bboxcenter: bool = False
    create_cropped_images: bool = True
    include_segmentation: bool = True
    
    # 3. Draw bounding box settings
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
    

class Bkgd_Segm_Bbox_pipe:
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
            processor = BackgroundRemover(image_path, output_dir)
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
            self.logger.info(
                f"Step 2: Processing segmentation for {raw_image_path.name}")

            # Check if already processed
            json_output_dir = output_dir / "json_files"
            if (self.config.skip_existing and json_output_dir.exists() and
                    list(json_output_dir.glob("*.json"))):
                self.logger.info(
                    f"Segmentation already completed for {raw_image_path.name}")
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
                # Debug: Check what was actually created
                self._debug_segmentation_outputs(output_dir,
                                                 raw_image_path.stem)

                # Move/copy generated JSON files to our organized structure
                self._organize_segmentation_outputs(output_dir,
                                                    raw_image_path.stem)
                self.logger.info(
                    f"Step 2 completed successfully for {raw_image_path.name}")
                return True, json_output_dir
            else:
                self.logger.error(
                    f"Step 2 failed: No successful segmentations for {raw_image_path.name}")
                return False, None

        except Exception as e:
            self.logger.error(
                f"Step 2 failed for {raw_image_path.name}: {str(e)}")
            return False, None

    def _organize_segmentation_outputs(self, output_dir: Path, image_stem: str):
        """
        Organize segmentation outputs into the pipeline structure.

        Args:
            output_dir: Base segmentation output directory (step2_segmentation)
            image_stem: Image name without extension
        """
        try:
            self.logger.info(
                f"Organizing segmentation outputs for {image_stem}")

            # Initialize counters
            json_files_copied = 0
            crops_moved = 0
            other_files_copied = 0

            # The batch processor typically creates outputs in these patterns:
            # 1. Config directory and its subdirectories
            # 2. Segmentation directories with pattern "*_segm"
            # 3. Output directories created by the batch processor

            search_locations = [
                output_dir,  # Current segmentation output dir
                output_dir.parent,  # Parent directory
                self.input_root,  # Input root directory
                self.output_root,  # Output root directory
            ]

            # Add config directory if it exists
            config_dir = output_dir / "configs"
            if config_dir.exists():
                search_locations.append(config_dir)

            # Search for segmentation output directories
            segmentation_dirs = set()

            for location in search_locations:
                if not location.exists():
                    continue

                self.logger.debug(f"Searching in: {location}")

                # Look for directories that match segmentation patterns
                patterns_to_search = [
                    f"{image_stem}*_segm",
                    f"*{image_stem}*_segm",
                    f"{image_stem}_segm",
                    f"{image_stem}*segmentation*",
                    f"*{image_stem}*segmentation*"
                ]

                for pattern in patterns_to_search:
                    try:
                        # Use both glob and rglob for thorough search
                        found_dirs = list(location.glob(pattern))
                        found_dirs.extend(list(location.rglob(pattern)))

                        for found_dir in found_dirs:
                            if found_dir.is_dir():
                                segmentation_dirs.add(found_dir)
                                self.logger.debug(
                                    f"Found segmentation directory: {found_dir}")

                    except Exception as search_error:
                        self.logger.warning(
                            f"Error searching pattern {pattern} in {location}: {search_error}")

            # Also look for batch_output directories (from BatchImageProcessor)
            for location in search_locations:
                if not location.exists():
                    continue

                batch_outputs = list(location.rglob("batch_output"))
                for batch_output in batch_outputs:
                    if batch_output.is_dir():
                        # Look for directories matching our image stem
                        image_dirs = list(batch_output.glob(f"*{image_stem}*"))
                        segmentation_dirs.update(
                            [d for d in image_dirs if d.is_dir()])

            self.logger.info(
                f"Found {len(segmentation_dirs)} potential segmentation directories")

            # Process each segmentation directory
            for segm_dir in segmentation_dirs:
                self.logger.debug(
                    f"Processing segmentation directory: {segm_dir}")

                try:
                    # 1. Copy JSON files
                    json_files = list(segm_dir.glob("*.json"))
                    if json_files:
                        json_output = output_dir / "json_files"
                        json_output.mkdir(exist_ok=True)

                        for json_file in json_files:
                            target = json_output / json_file.name
                            if not target.exists():
                                try:
                                    target.write_text(
                                        json_file.read_text(encoding='utf-8'))
                                    json_files_copied += 1
                                    self.logger.debug(
                                        f"Copied JSON file: {json_file.name}")
                                except Exception as copy_error:
                                    self.logger.warning(
                                        f"Failed to copy JSON file {json_file.name}: {copy_error}")

                    # 2. Handle crops directory
                    crops_source = segm_dir / "crops"
                    if crops_source.exists() and crops_source.is_dir():
                        crops_target = output_dir / "crops"
                        try:
                            if not crops_target.exists():
                                # Move the entire crops directory
                                import shutil
                                shutil.move(str(crops_source),
                                            str(crops_target))
                                crops_moved += 1
                                self.logger.debug(
                                    f"Moved crops directory from {crops_source}")
                            else:
                                # Copy individual files if target exists
                                for crop_file in crops_source.iterdir():
                                    if crop_file.is_file():
                                        target_crop = crops_target / crop_file.name
                                        if not target_crop.exists():
                                            target_crop.write_bytes(
                                                crop_file.read_bytes())
                                            self.logger.debug(
                                                f"Copied crop file: {crop_file.name}")
                                crops_moved += 1
                        except Exception as move_error:
                            self.logger.warning(
                                f"Failed to handle crops directory: {move_error}")

                    # 3. Handle cropped_objects directory (alternative naming)
                    cropped_objects_source = segm_dir / "cropped_objects"
                    if cropped_objects_source.exists() and cropped_objects_source.is_dir():
                        crops_target = output_dir / "crops"
                        crops_target.mkdir(exist_ok=True)
                        try:
                            for crop_file in cropped_objects_source.iterdir():
                                if crop_file.is_file():
                                    target_crop = crops_target / crop_file.name
                                    if not target_crop.exists():
                                        target_crop.write_bytes(
                                            crop_file.read_bytes())
                                        self.logger.debug(
                                            f"Copied crop file from cropped_objects: {crop_file.name}")
                            crops_moved += 1
                        except Exception as copy_error:
                            self.logger.warning(
                                f"Failed to copy from cropped_objects: {copy_error}")

                    # 4. Copy other important files
                    for pattern in [
                                    "*_metadata.json", "*_summary.*"
                                    # , "*.txt", "*.png"
                                    ]:
                        try:
                            other_files = list(segm_dir.glob(pattern))
                            for other_file in other_files:
                                if other_file.is_file():
                                    target = output_dir / other_file.name
                                    if not target.exists():
                                        try:
                                            if other_file.suffix.lower() in [
                                                '.txt', '.json']:
                                                target.write_text(
                                                    other_file.read_text(
                                                        encoding='utf-8'))
                                            else:
                                                target.write_bytes(
                                                    other_file.read_bytes())
                                            other_files_copied += 1
                                            self.logger.debug(
                                                f"Copied additional file: {other_file.name}")
                                        except Exception as copy_error:
                                            self.logger.warning(
                                                f"Failed to copy file {other_file.name}: {copy_error}")
                        except Exception as pattern_error:
                            self.logger.warning(
                                f"Error processing pattern {pattern}: {pattern_error}")

                except Exception as dir_error:
                    self.logger.warning(
                        f"Error processing directory {segm_dir}: {dir_error}")

            # Summary logging
            total_files = json_files_copied + crops_moved + other_files_copied
            if total_files > 0:
                self.logger.info(
                    f"Successfully organized outputs: {json_files_copied} JSON files, "
                    f"{crops_moved} crops directories, {other_files_copied} other files")

                # Verify that we have JSON files for the next step
                json_output = output_dir / "json_files"
                if json_output.exists():
                    json_count = len(list(json_output.glob("*.json")))
                    self.logger.info(
                        f"JSON files available for next step: {json_count}")

            else:
                self.logger.warning(
                    f"No segmentation outputs found to organize for {image_stem}")

                # Enhanced debugging when nothing is found
                self.logger.debug(
                    f"Searched directories: {[str(d) for d in segmentation_dirs]}")

                # List what actually exists in the output directory
                if output_dir.exists():
                    all_files = []
                    for root, dirs, files in output_dir.rglob("*"):
                        for file in files:
                            all_files.append(str(Path(root) / file))
                    self.logger.debug(
                        f"Current output directory structure: {all_files}")

        except Exception as e:
            self.logger.error(
                f"Error organizing segmentation outputs for {image_stem}: {str(e)}")
            # Don't re-raise the exception, just log it and continue


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
            #old. json_files = list(json_dir.glob("*.json"))
            json_files = list(json_dir.glob(f"{no_bg_image_path.stem}*.json"))
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
                show_label=self.config.show_label,
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

    def _debug_segmentation_outputs(self, output_dir: Path,
                                    image_stem: str) -> None:
        """
        Debug method to help identify where segmentation outputs are created.
        Call this after step2_segmentation to see what was actually generated.
        """
        self.logger.info(
            f"=== DEBUG: Segmentation outputs for {image_stem} ===")

        # Check multiple possible locations
        search_locations = [
            output_dir,  # Current segmentation output dir
            output_dir.parent,  # Parent of segmentation dir
            output_dir.parent.parent,  # Two levels up
            self.input_root,  # Input root directory
            self.output_root,  # Output root directory
        ]

        # Add config directory if it exists
        config_dir = output_dir / "configs"
        if config_dir.exists():
            search_locations.append(config_dir)

        for location in search_locations:
            if not location.exists():
                self.logger.debug(f"Location does not exist: {location}")
                continue

            self.logger.info(f"Checking location: {location}")

            # Look for any directories containing the image stem
            matching_items = []
            try:
                # Check immediate children
                for item in location.iterdir():
                    if item.is_dir() and image_stem.lower() in item.name.lower():
                        matching_items.append(item)

                # Check subdirectories recursively (limited depth)
                for item in location.rglob("*"):
                    if (item.is_dir() and
                            image_stem.lower() in item.name.lower() and
                            item not in matching_items):
                        matching_items.append(item)

            except Exception as e:
                self.logger.warning(f"Error searching in {location}: {e}")
                continue

            if matching_items:
                self.logger.info(
                    f"  Found matching directories: {[str(d) for d in matching_items]}")

                # Check contents of each matching directory
                for match_dir in matching_items:
                    try:
                        contents = list(match_dir.iterdir())
                        file_contents = [c for c in contents if c.is_file()]
                        dir_contents = [c for c in contents if c.is_dir()]

                        self.logger.info(f"    Contents of {match_dir.name}:")
                        if file_contents:
                            self.logger.info(
                                f"      Files: {[c.name for c in file_contents]}")
                        if dir_contents:
                            self.logger.info(
                                f"      Directories: {[c.name for c in dir_contents]}")

                    except Exception as e:
                        self.logger.warning(
                            f"    Error reading contents of {match_dir}: {e}")
            else:
                self.logger.info(f"  No matching directories found")

            # Also look for any JSON or image files that might be related
            try:
                json_files = list(location.glob(f"*{image_stem}*.json"))
                if json_files:
                    self.logger.info(
                        f"  Found related JSON files: {[f.name for f in json_files]}")

                img_files = list(location.glob(f"*{image_stem}*.png")) + list(
                    location.glob(f"*{image_stem}*.jpg"))
                if img_files:
                    self.logger.info(
                        f"  Found related image files: {[f.name for f in img_files]}")

            except Exception as e:
                self.logger.warning(
                    f"Error searching for related files in {location}: {e}")

        self.logger.info("=== END DEBUG ===")

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
        input_root_dir="/Users/aavelino/Downloads/2025_09_10_Emilie/",
        # output_root_dir="/path/to/output",  # Optional
        image_pattern="*.jpg",
        
        # 1. Background removal settings
        # n_clusters=5, # Optional. Usually 5.
        # background_clusters=[0, 4], # Optional. Usually [0, 4].

        # 2. Object segmentation settings
        max_distance=4.0,
        min_pixels=1000,
        padding=35,
        cropping = True,
        use_nonwhitepixel_as_bboxcenter=True,
        create_cropped_images = False,
        include_segmentation = False,

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
    pipeline = Bkgd_Segm_Bbox_pipe(config)
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
# from image_processing_pipeline import Bkgd_Segm_Bbox_pipe, PipelineConfig
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
#     pipeline = Bkgd_Segm_Bbox_pipe(config)
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
#     pipeline = Bkgd_Segm_Bbox_pipe(config)
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
#     pipeline = Bkgd_Segm_Bbox_pipe(config)
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

#     pipeline = Bkgd_Segm_Bbox_pipe(config)

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

# from image_processing_pipeline import Bkgd_Segm_Bbox_pipe, PipelineConfig
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
# pipeline = Bkgd_Segm_Bbox_pipe(config)
# results = pipeline.run_pipeline()
