
"""
Batch Processor for IoU Metric Calculation

This module provides batch processing capabilities for matching bounding boxes
between Biigle and Roboflow JSON files using the IoUMetric_for_BBoxMatch class.

The processor automatically pairs JSON files by filename and generates IoU metrics
for multiple file pairs in a single operation.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime
import sys

# Add the computer_vision directory to the path to import IoUMetric_for_BBoxMatch
sys.path.append(str(Path(__file__).parent / 'computer_vision'))

from computer_vision.IoU_metric_for_bbox_match import IoUMetric_for_BBoxMatch


class BatchIoUProcessor:
    """
    Batch processor for calculating IoU metrics between multiple pairs of
    Biigle and Roboflow JSON files.

    This class automates the process of:
    1. Discovering JSON files in specified directories
    2. Matching Biigle and Roboflow files by filename
    3. Processing each pair using IoUMetric_for_BBoxMatch
    4. Generating comprehensive reports and logs

    Key Features:
    - Automatic file discovery and pairing
    - Configurable filename patterns
    - Detailed logging and error handling
    - Summary reports with statistics
    - Flexible output directory management
    - Support for multiple CSV output formats

    Attributes:
        biigle_dir: Directory containing Biigle JSON files
        roboflow_dir: Directory containing Roboflow JSON files
        output_dir: Directory for output CSV files and logs
        biigle_pattern: Glob pattern to identify Biigle JSON files
        roboflow_pattern: Glob pattern to identify Roboflow JSON files
        iou_threshold: IoU threshold for matching (default: 0.8)
        logger: Logger instance for tracking operations
    """

    def __init__(
        self,
        biigle_dir: Union[str, Path],
        roboflow_dir: Union[str, Path],
        output_dir: Union[str, Path],
        biigle_pattern: str = "*_biigle.json",
        roboflow_pattern: str = "*_roboflow.json",
        iou_threshold: float = 0.8
    ):
        """
        Initialize the batch IoU processor.

        Args:
            biigle_dir: Directory containing Biigle JSON files
            roboflow_dir: Directory containing Roboflow JSON files
            output_dir: Directory for output files (created if not exists)
            biigle_pattern: Glob pattern for Biigle files (default: "*_biigle.json")
            roboflow_pattern: Glob pattern for Roboflow files (default: "*_roboflow.json")
            iou_threshold: IoU threshold for matching (default: 0.8)
        """
        self.biigle_dir = Path(biigle_dir)
        self.roboflow_dir = Path(roboflow_dir)
        self.output_dir = Path(output_dir)
        self.biigle_pattern = biigle_pattern
        self.roboflow_pattern = roboflow_pattern
        self.iou_threshold = iou_threshold

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = self._setup_logging()

        # Validate input directories
        self._validate_directories()

    def _setup_logging(self) -> logging.Logger:
        """
        Configure logging for batch processing.

        Returns:
            Configured logger instance
        """
        log_file = self.output_dir / f"batch_iou_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Create logger
        logger = logging.getLogger(f"BatchIoUProcessor_{id(self)}")
        logger.setLevel(logging.INFO)

        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()

        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info("=" * 80)
        logger.info("Batch IoU Processor Initialized")
        logger.info("=" * 80)
        logger.info(f"Biigle directory: {self.biigle_dir}")
        logger.info(f"Roboflow directory: {self.roboflow_dir}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info(f"Biigle pattern: {self.biigle_pattern}")
        logger.info(f"Roboflow pattern: {self.roboflow_pattern}")
        logger.info(f"IoU threshold: {self.iou_threshold}")
        logger.info("=" * 80)

        return logger

    def _validate_directories(self) -> None:
        """
        Validate that input directories exist and are accessible.

        Raises:
            FileNotFoundError: If input directories don't exist
        """
        if not self.biigle_dir.exists():
            error_msg = f"Biigle directory not found: {self.biigle_dir}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        if not self.roboflow_dir.exists():
            error_msg = f"Roboflow directory not found: {self.roboflow_dir}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        self.logger.info("Input directories validated successfully")

    def _extract_base_filename(self, file_path: Path, pattern: str) -> str:
        """
        Extract the base filename from a file path by removing the pattern suffix.

        For example:
        - "image001_biigle.json" with pattern "*_biigle.json" -> "image001"
        - "sample_roboflow.json" with pattern "*_roboflow.json" -> "sample"

        Args:
            file_path: Path to the JSON file
            pattern: Glob pattern used to find the file

        Returns:
            Base filename without pattern suffix
        """
        # Remove the wildcard and extension from pattern to get the suffix
        # e.g., "*_biigle.json" -> "_biigle.json"
        suffix = pattern.replace("*", "")

        # Remove the suffix from filename
        filename = file_path.name
        if filename.endswith(suffix):
            base_name = filename[:-len(suffix)]
        else:
            # If suffix doesn't match, just use stem
            base_name = file_path.stem

        return base_name

    def find_file_pairs(self) -> List[Tuple[Path, Path, str]]:
        """
        Find and match pairs of Biigle and Roboflow JSON files by filename.

        Files are matched based on their base filename (the part before the pattern suffix).
        For example:
        - "image001_biigle.json" matches "image001_roboflow.json"
        - Base filename is "image001"

        Returns:
            List of tuples: (biigle_path, roboflow_path, base_filename)
        """
        self.logger.info("Discovering JSON files...")

        # Find all Biigle files
        biigle_files = list(self.biigle_dir.glob(self.biigle_pattern))
        self.logger.info(f"Found {len(biigle_files)} Biigle files")

        # Find all Roboflow files
        roboflow_files = list(self.roboflow_dir.glob(self.roboflow_pattern))
        self.logger.info(f"Found {len(roboflow_files)} Roboflow files")

        # Create mapping of base filenames to full paths
        biigle_map = {
            self._extract_base_filename(f, self.biigle_pattern): f
            for f in biigle_files
        }

        roboflow_map = {
            self._extract_base_filename(f, self.roboflow_pattern): f
            for f in roboflow_files
        }

        # Find matching pairs
        pairs = []
        matched_base_names = set(biigle_map.keys()) & set(roboflow_map.keys())

        for base_name in sorted(matched_base_names):
            biigle_path = biigle_map[base_name]
            roboflow_path = roboflow_map[base_name]
            pairs.append((biigle_path, roboflow_path, base_name))
            self.logger.info(f"Matched pair: {base_name}")
            self.logger.info(f"  - Biigle:   {biigle_path.name}")
            self.logger.info(f"  - Roboflow: {roboflow_path.name}")

        # Report unmatched files
        unmatched_biigle = set(biigle_map.keys()) - matched_base_names
        unmatched_roboflow = set(roboflow_map.keys()) - matched_base_names

        if unmatched_biigle:
            self.logger.warning(f"Unmatched Biigle files ({len(unmatched_biigle)}):")
            for name in sorted(unmatched_biigle):
                self.logger.warning(f"  - {biigle_map[name].name}")

        if unmatched_roboflow:
            self.logger.warning(f"Unmatched Roboflow files ({len(unmatched_roboflow)}):")
            for name in sorted(unmatched_roboflow):
                self.logger.warning(f"  - {roboflow_map[name].name}")

        self.logger.info(f"Total matched pairs: {len(pairs)}")
        return pairs

    def process_single_pair(
        self,
        biigle_path: Path,
        roboflow_path: Path,
        base_filename: str,
        output_format: str = "robo_to_biigle"
    ) -> bool:
        """
        Process a single pair of Biigle and Roboflow JSON files.

        Args:
            biigle_path: Path to Biigle JSON file
            roboflow_path: Path to Roboflow JSON file
            base_filename: Base filename for output files
            output_format: Output format - "robo_to_biigle", "biigle_to_robo", or "for_biigle"

        Returns:
            True if processing succeeded, False otherwise
        """
        try:
            self.logger.info(f"Processing pair: {base_filename}")

            # Create IoU matcher instance
            matcher = IoUMetric_for_BBoxMatch(
                roboflow_json_path=str(roboflow_path),
                biigle_json_path=str(biigle_path),
                iou_threshold=self.iou_threshold
            )

            # Generate output path based on format
            if output_format == "robo_to_biigle":
                output_csv = self.output_dir / f"{base_filename}_robo_to_biigle.csv"
                matcher.save_to_csv_robo_to_biigle(str(output_csv))
            elif output_format == "biigle_to_robo":
                output_csv = self.output_dir / f"{base_filename}_biigle_to_robo.csv"
                matcher.save_to_csv_biigle_to_robo(str(output_csv))
            elif output_format == "for_biigle":
                output_csv = self.output_dir / f"{base_filename}_for_biigle.csv"
                matcher.save_to_csv_for_biigle(str(output_csv))
            else:
                raise ValueError(f"Unknown output format: {output_format}")

            self.logger.info(f"Successfully processed {base_filename}")
            return True

        except Exception as e:
            self.logger.error(f"Error processing {base_filename}: {str(e)}")
            self.logger.exception("Detailed error information:")
            return False

    def process_batch(
        self,
        output_format: str = "robo_to_biigle"
    ) -> Dict[str, bool]:
        """
        Process all matched pairs of JSON files in batch.

        Args:
            output_format: Output format - "robo_to_biigle", "biigle_to_robo", or "for_biigle"

        Returns:
            Dictionary mapping base filenames to success status
        """
        self.logger.info("=" * 80)
        self.logger.info("Starting batch processing")
        self.logger.info("=" * 80)

        # Find all matching pairs
        pairs = self.find_file_pairs()

        if not pairs:
            self.logger.warning("No matching file pairs found. Nothing to process.")
            return {}

        # Process each pair
        results = {}
        for biigle_path, roboflow_path, base_filename in pairs:
            success = self.process_single_pair(
                biigle_path=biigle_path,
                roboflow_path=roboflow_path,
                base_filename=base_filename,
                output_format=output_format
            )
            results[base_filename] = success

        # Generate summary
        successful = sum(results.values())
        total = len(results)

        self.logger.info("=" * 80)
        self.logger.info("Batch processing completed")
        self.logger.info(f"Total pairs processed: {total}")
        self.logger.info(f"Successful: {successful}")
        self.logger.info(f"Failed: {total - successful}")
        self.logger.info(f"Success rate: {successful/total*100:.1f}%")
        self.logger.info("=" * 80)

        return results

    def generate_summary_report(self, results: Dict[str, bool]) -> None:
        """
        Generate a comprehensive summary report of batch processing results.

        Args:
            results: Dictionary mapping base filenames to success status
        """
        report_path = self.output_dir / "batch_iou_summary.txt"

        if not results:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("BATCH IoU PROCESSING SUMMARY REPORT\n")
                f.write("=" * 80 + "\n\n")
                f.write("No file pairs were processed.\n")
                f.write("Please check:\n")
                f.write("- Input directories contain JSON files\n")
                f.write("- File patterns match existing files\n")
                f.write("- Biigle and Roboflow files have matching base names\n")

            self.logger.warning("No results to report - no pairs were processed")
            return

        successful = [name for name, success in results.items() if success]
        failed = [name for name, success in results.items() if not success]

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("BATCH IoU PROCESSING SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("CONFIGURATION:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Biigle directory:    {self.biigle_dir}\n")
            f.write(f"Roboflow directory:  {self.roboflow_dir}\n")
            f.write(f"Output directory:    {self.output_dir}\n")
            f.write(f"Biigle pattern:      {self.biigle_pattern}\n")
            f.write(f"Roboflow pattern:    {self.roboflow_pattern}\n")
            f.write(f"IoU threshold:       {self.iou_threshold}\n\n")

            f.write("PROCESSING STATISTICS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total pairs processed: {len(results)}\n")
            f.write(f"Successful:            {len(successful)}\n")
            f.write(f"Failed:                {len(failed)}\n")
            f.write(f"Success rate:          {len(successful)/len(results)*100:.1f}%\n\n")

            if successful:
                f.write("SUCCESSFULLY PROCESSED PAIRS:\n")
                f.write("-" * 40 + "\n")
                for name in successful:
                    f.write(f"✓ {name}\n")
                f.write("\n")

            if failed:
                f.write("FAILED PROCESSING:\n")
                f.write("-" * 40 + "\n")
                for name in failed:
                    f.write(f"✗ {name}\n")
                f.write("\n")

            f.write("OUTPUT FILES:\n")
            f.write("-" * 40 + "\n")
            output_files = sorted(self.output_dir.glob("*.csv"))
            for output_file in output_files:
                f.write(f"  {output_file.name}\n")
            f.write("\n")

        self.logger.info(f"Summary report saved to: {report_path}")
        print(f"\n{'='*80}")
        print(f"Summary report saved to: {report_path}")
        print(f"{'='*80}\n")


def batch_process_iou_metrics(
    biigle_dir: Union[str, Path],
    roboflow_dir: Union[str, Path],
    output_dir: Union[str, Path],
    biigle_pattern: str = "*_biigle.json",
    roboflow_pattern: str = "*_roboflow.json",
    iou_threshold: float = 0.8,
    output_format: str = "robo_to_biigle"
) -> Dict[str, bool]:
    """
    Convenience function for batch processing IoU metrics.

    This is a simplified interface to the BatchIoUProcessor class that handles
    the complete workflow in a single function call.

    Args:
        biigle_dir: Directory containing Biigle JSON files
        roboflow_dir: Directory containing Roboflow JSON files
        output_dir: Directory for output files (created if not exists)
        biigle_pattern: Glob pattern for Biigle files (default: "*_biigle.json")
        roboflow_pattern: Glob pattern for Roboflow files (default: "*_roboflow.json")
        iou_threshold: IoU threshold for matching (default: 0.8)
        output_format: Output CSV format - "robo_to_biigle", "biigle_to_robo", or "for_biigle"

    Returns:
        Dictionary mapping base filenames to success status

    Example:
        >>> results = batch_process_iou_metrics(
        ...     biigle_dir="/path/to/biigle",
        ...     roboflow_dir="/path/to/roboflow",
        ...     output_dir="/path/to/output",
        ...     iou_threshold=0.8
        ... )
        >>> print(f"Processed {len(results)} pairs")
    """
    # Create processor instance
    processor = BatchIoUProcessor(
        biigle_dir=biigle_dir,
        roboflow_dir=roboflow_dir,
        output_dir=output_dir,
        biigle_pattern=biigle_pattern,
        roboflow_pattern=roboflow_pattern,
        iou_threshold=iou_threshold
    )

    # Process batch
    results = processor.process_batch(output_format=output_format)

    # Generate report
    processor.generate_summary_report(results)

    return results

# ########################################################60
# # Example usage
# if __name__ == "__main__":
#     """
#     Example demonstrating how to use the batch IoU processor.

#     This example shows three different approaches:
#     1. Using the convenience function (simplest)
#     2. Using the class directly (more control)
#     3. Processing with different output formats
#     """

#     # Example 1: Simple batch processing using convenience function
#     print("Example 1: Using convenience function")
#     print("-" * 40)

#     # results = batch_process_iou_metrics(
#     #     biigle_dir="/path/to/biigle/jsons",
#     #     roboflow_dir="/path/to/roboflow/jsons",
#     #     output_dir="/path/to/output",
#     #     biigle_pattern="*_biigle.json",
#     #     roboflow_pattern="*_roboflow.json",
#     #     iou_threshold=0.8,
#     #     output_format="robo_to_biigle"
#     # )

#     # Example 2: Using the class directly for more control
#     print("\nExample 2: Using class directly")
#     print("-" * 40)

#     # processor = BatchIoUProcessor(
#     #     biigle_dir="/path/to/biigle/jsons",
#     #     roboflow_dir="/path/to/roboflow/jsons",
#     #     output_dir="/path/to/output",
#     #     biigle_pattern="*_biigle.json",
#     #     roboflow_pattern="*_roboflow.json",
#     #     iou_threshold=0.85  # Custom threshold
#     # )
#     #
#     # # Find pairs first to inspect
#     # pairs = processor.find_file_pairs()
#     # print(f"Found {len(pairs)} matching pairs")
#     #
#     # # Process with custom format
#     # results = processor.process_batch(output_format="biigle_to_robo")
#     #
#     # # Generate report
#     # processor.generate_summary_report(results)

#     # Example 3: Processing with different output formats
#     print("\nExample 3: Multiple output formats")
#     print("-" * 40)

#     # processor = BatchIoUProcessor(
#     #     biigle_dir="/path/to/biigle/jsons",
#     #     roboflow_dir="/path/to/roboflow/jsons",
#     #     output_dir="/path/to/output",
#     #     iou_threshold=0.8
#     # )
#     #
#     # # Generate all three output formats
#     # for output_format in ["robo_to_biigle", "biigle_to_robo", "for_biigle"]:
#     #     print(f"\nProcessing with format: {output_format}")
#     #     results = processor.process_batch(output_format=output_format)
#     #     print(f"Completed {sum(results.values())}/{len(results)} pairs")

#     print("\nUncomment the example code above to run batch processing")

# # ========================================================60

# # Example 1: Simple Batch Processing (Recommended for most users)

# from batch_processor import batch_process_iou_metrics

# # Process all matching pairs with default settings
# results = batch_process_iou_metrics(
#     biigle_dir="/path/to/biigle_jsons",
#     roboflow_dir="/path/to/roboflow_jsons",
#     output_dir="/path/to/output",
#     iou_threshold=0.8
# )

# print(f"Successfully processed {sum(results.values())}/{len(results)} pairs")

# # --------------------------------------------------------60
# # Example 2: Advanced Usage with Custom Patterns

# from batch_processor import BatchIoUProcessor

# # Initialize with custom patterns
# processor = BatchIoUProcessor(
#     biigle_dir="/data/annotations/biigle",
#     roboflow_dir="/data/annotations/roboflow",
#     output_dir="/data/results",
#     biigle_pattern="sample_*_biigle.json",      # Custom pattern
#     roboflow_pattern="sample_*_roboflow.json",  # Custom pattern
#     iou_threshold=0.85                           # Higher threshold
# )

# # Find and inspect pairs before processing
# pairs = processor.find_file_pairs()
# print(f"Found {len(pairs)} matching pairs")

# # Process with specific output format
# results = processor.process_batch(output_format="for_biigle")

# # Generate summary report
# processor.generate_summary_report(results)

# # --------------------------------------------------------60
# # Example 3: Processing Multiple Output Formats

# from batch_processor import BatchIoUProcessor

# processor = BatchIoUProcessor(
#     biigle_dir="/data/biigle",
#     roboflow_dir="/data/roboflow",
#     output_dir="/data/output"
# )

# # Generate all three CSV formats
# for format_type in ["robo_to_biigle", "biigle_to_robo", "for_biigle"]:
#     results = processor.process_batch(output_format=format_type)
#     print(f"Format {format_type}: {sum(results.values())}/{len(results)} successful")

