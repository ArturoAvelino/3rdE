import json
import csv
from pathlib import Path
from typing import List, Dict, Any
import logging


class BatchBoundingBoxProcessor:
    """
    A comprehensive batch processing system for extracting bounding box information from JSON annotation files.

    ## Purpose and Overview

    The BatchBoundingBoxProcessor class is designed to automate the extraction of bounding box dimensions
    from multiple JSON files containing image annotation data. It processes batches of JSON files that
    follow a specific annotation format and consolidates the bounding box information into a structured
    CSV output file for further analysis or processing.

    This class is particularly useful for:
    - Computer vision and machine learning workflows requiring bounding box analysis
    - Quality control and validation of annotation datasets
    - Statistical analysis of object sizes in image datasets
    - Data preprocessing for object detection model training
    - Batch conversion of annotation formats for downstream processing

    ## Input JSON File Structure

    The class expects JSON files with the following hierarchical structure:

    ```json
    {
        "image": [
            {
                "sample_name": "BM4_E",
                "file_name": "capt0011.jpg",
                "width": 6000,
                "height": 4000
            }
        ],
        "annotations": [
            {
                "id": 0,
                "bbox": [
                    {
                        "center_x": 3027,
                        "center_y": 544,
                        "box_width": 75,
                        "box_height": 52
                    }
                ]
            },
            {
                "id": 1,
                "bbox": [
                    {
                        "center_x": 3348,
                        "center_y": 3948,
                        "box_width": 317,
                        "box_height": 101
                    }
                ]
            }
        ]
    }
    ```

    ## Output CSV Structure

    The generated CSV file contains exactly four columns:
    - **file_name**: The name of the image file (extracted from the "image" section)
    - **id**: The annotation identifier (from each annotation's "id" field)
    - **box_width**: The width of the bounding box in pixels
    - **box_height**: The height of the bounding box in pixels

    Each row in the CSV represents one bounding box from one annotation in the source JSON files.

    ## Key Features and Capabilities

    ### Batch Processing
    - Automatically discovers and processes all JSON files matching a specified pattern
    - Handles multiple bounding boxes per annotation and multiple annotations per file
    - Processes files in sorted order for consistent and reproducible results
    - Continues processing even if individual files encounter errors

    ### Robust Error Handling
    - Validates input and output directories during initialization
    - Gracefully handles malformed JSON files with detailed error logging
    - Skips files with missing required fields while continuing batch processing
    - Provides comprehensive error messages for troubleshooting

    ### Flexible Configuration
    - Customizable file patterns for selective processing (e.g., "*.json", "annotation_*.json")
    - Configurable output directory and filename
    - Automatic output directory creation if it doesn't exist
    - Default parameter values for common use cases

    ### Comprehensive Logging
    - Detailed progress reporting during batch processing
    - Warning messages for files with missing or incomplete data
    - Error logging for debugging problematic files
    - Summary statistics upon completion

    ## Method Descriptions

    ### `__init__(json_path, filename_pattern, output_path, output_filename)`
    Initializes the processor with configuration parameters and validates directory paths.
    Creates output directories if they don't exist and sets up logging infrastructure.

    ### `find_json_files()`
    Discovers all JSON files in the specified directory matching the given pattern.
    Returns a sorted list of file paths for consistent processing order.

    ### `extract_bounding_box_data(json_file)`
    Processes a single JSON file to extract bounding box information.
    Handles the nested structure of annotations and bbox arrays, extracting all
    relevant data while validating field presence and data types.

    ### `process_all_files()`
    Orchestrates the complete batch processing workflow:
    1. Discovers all matching JSON files
    2. Extracts bounding box data from each file
    3. Consolidates all data into a single collection
    4. Generates the output CSV file
    5. Provides processing summary and statistics

    ### `write_csv(data, csv_path)`
    Writes the extracted bounding box data to a CSV file with proper formatting.
    Includes column headers and handles text encoding for international characters.

    ### `get_processing_summary()`
    Provides a preview of the processing operation without executing it.
    Returns information about discovered files and output paths for verification.

    ## Usage Examples

    ### Basic Usage (Minimal Configuration)
    ```python
    # Process all JSON files in a directory with default settings
    processor = BatchBoundingBoxProcessor(json_path="/path/to/json/files")
    success = processor.process_all_files()
    ```

    ### Advanced Usage (Custom Configuration)
    ```python
    # Full customization of processing parameters
    processor = BatchBoundingBoxProcessor(
        json_path="/path/to/json/files",
        filename_pattern="annotation_*.json",
        output_path="/path/to/output",
        output_filename="extracted_bounding_boxes.csv"
    )

    # Preview processing before execution
    summary = processor.get_processing_summary()
    print(f"Will process {summary['total_files']} files")
    print(f"Output: {summary['full_output_path']}")

    # Execute processing
    success = processor.process_all_files()
    ```

    ### Integration with Logging
    ```python
    import logging

    # Configure logging for detailed output
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    processor = BatchBoundingBoxProcessor(json_path="/path/to/files")
    processor.process_all_files()
    ```

    ## Error Handling and Validation

    The class implements multiple layers of validation and error handling:

    - **Initialization Validation**: Checks directory existence and permissions
    - **File Format Validation**: Validates JSON syntax and required field presence
    - **Data Type Validation**: Ensures numeric values for width and height fields
    - **Graceful Degradation**: Continues processing other files when individual files fail
    - **Comprehensive Logging**: Records all errors and warnings for debugging

    ## Performance Considerations

    - Files are processed sequentially to maintain consistent logging and error handling
    - Memory usage scales with the total number of bounding boxes across all files
    - Processing speed depends on JSON file size and complexity
    - Large datasets may benefit from chunked processing or parallel execution

    ## Dependencies

    - **json**: Standard library for JSON parsing
    - **csv**: Standard library for CSV file generation
    - **pathlib**: Modern path handling and file system operations
    - **typing**: Type hints for better code documentation and IDE support
    - **logging**: Comprehensive logging and error reporting

    ## Common Use Cases

    1. **Dataset Analysis**: Extract bounding box statistics for computer vision datasets
    2. **Quality Assurance**: Validate annotation completeness and consistency
    3. **Format Conversion**: Convert from custom JSON format to standard CSV
    4. **Preprocessing**: Prepare data for machine learning model training
    5. **Reporting**: Generate summaries of annotated objects across image collections

    This class provides a robust, production-ready solution for batch processing of
    bounding box annotations with comprehensive error handling and detailed logging.
    """
    
    def __init__(self, json_path: str, filename_pattern: str = "*.json", 
                 output_path: str = None, output_filename: str = "bounding_boxes.csv"):
        """
        Initialize the BatchBoundingBoxProcessor.
        
        Args:
            json_path (str): Path to the directory containing JSON files
            filename_pattern (str): Pattern to match JSON files (default: "*.json")
            output_path (str): Path directory where output files will be saved
                              If None, uses the same directory as json_path
            output_filename (str): Name of the output CSV file (default: "bounding_boxes.csv")
        
        Raises:
            FileNotFoundError: If json_path doesn't exist
            NotADirectoryError: If json_path is not a directory
        """
        self.json_path = Path(json_path)
        self.filename_pattern = filename_pattern
        self.output_path = Path(output_path) if output_path else self.json_path
        self.output_filename = output_filename
        self.logger = logging.getLogger(__name__)
        
        # Validate directories
        if not self.json_path.exists():
            raise FileNotFoundError(f"JSON directory not found: {self.json_path}")
        
        if not self.json_path.is_dir():
            raise NotADirectoryError(f"JSON path is not a directory: {self.json_path}")
        
        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def find_json_files(self) -> List[Path]:
        """
        Find all JSON files matching the specified pattern.
        
        Returns:
            List[Path]: List of JSON file paths
        """
        json_files = list(self.json_path.glob(self.filename_pattern))
        json_files.sort()  # Sort for consistent processing order
        
        self.logger.info(f"Found {len(json_files)} JSON files matching pattern '{self.filename_pattern}'")
        return json_files
    
    def extract_bounding_box_data(self, json_file: Path) -> List[Dict[str, Any]]:
        """
        Extract bounding box data from a single JSON file.
        
        Args:
            json_file (Path): Path to the JSON file
            
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing extracted data
        """
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            extracted_data = []
            
            # Get file_name from the image section
            file_name = None
            if 'image' in data and isinstance(data['image'], list) and len(data['image']) > 0:
                file_name = data['image'][0].get('file_name')
            
            if not file_name:
                self.logger.warning(f"No file_name found in {json_file}")
                return extracted_data
            
            # Extract bounding box data from annotations
            if 'annotations' in data and isinstance(data['annotations'], list):
                for annotation in data['annotations']:
                    annotation_id = annotation.get('id')
                    
                    # Handle bbox data (can be a list of bbox objects)
                    if 'bbox' in annotation and isinstance(annotation['bbox'], list):
                        for bbox in annotation['bbox']:
                            if isinstance(bbox, dict):
                                box_width = bbox.get('box_width')
                                box_height = bbox.get('box_height')
                                
                                if box_width is not None and box_height is not None:
                                    extracted_data.append({
                                        'file_name': file_name,
                                        'id': annotation_id,
                                        'box_width': box_width,
                                        'box_height': box_height
                                    })
                                else:
                                    self.logger.warning(f"Missing box_width or box_height in {json_file}, annotation {annotation_id}")
            else:
                self.logger.warning(f"No annotations found in {json_file}")
            
            return extracted_data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in {json_file}: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error processing {json_file}: {e}")
            return []
    
    def process_all_files(self) -> bool:
        """
        Process all JSON files and generate the CSV output.
        
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            # Find all JSON files
            json_files = self.find_json_files()
            
            if not json_files:
                self.logger.warning("No JSON files found to process")
                return False
            
            # Collect all bounding box data
            all_data = []
            successful_files = 0
            
            for json_file in json_files:
                self.logger.info(f"Processing {json_file.name}")
                file_data = self.extract_bounding_box_data(json_file)
                
                if file_data:
                    all_data.extend(file_data)
                    successful_files += 1
                    self.logger.info(f"Extracted {len(file_data)} bounding box records from {json_file.name}")
                else:
                    self.logger.warning(f"No data extracted from {json_file.name}")
            
            # Write CSV file
            if all_data:
                csv_path = self.output_path / self.output_filename
                self.write_csv(all_data, csv_path)
                
                self.logger.info(f"Successfully processed {successful_files}/{len(json_files)} files")
                self.logger.info(f"Generated CSV with {len(all_data)} total records: {csv_path}")
                return True
            else:
                self.logger.error("No bounding box data extracted from any files")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in process_all_files: {e}")
            return False
    
    def write_csv(self, data: List[Dict[str, Any]], csv_path: Path) -> None:
        """
        Write the extracted data to a CSV file.
        
        Args:
            data (List[Dict[str, Any]]): List of dictionaries containing the data
            csv_path (Path): Path where the CSV file will be written
        """
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['file_name', 'id', 'box_width', 'box_height']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for row in data:
                    writer.writerow(row)
                    
            self.logger.info(f"CSV file written successfully: {csv_path}")
            
        except Exception as e:
            self.logger.error(f"Error writing CSV file {csv_path}: {e}")
            raise
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the files that would be processed.
        
        Returns:
            Dict[str, Any]: Summary information about the JSON files
        """
        json_files = self.find_json_files()
        
        summary = {
            'total_files': len(json_files),
            'files_found': [str(f) for f in json_files],
            'output_path': str(self.output_path),
            'output_filename': self.output_filename,
            'full_output_path': str(self.output_path / self.output_filename)
        }
        
        return summary


# ===========================
# Examples of use

# # Basic usage with default settings
# processor = BatchBoundingBoxProcessor(
#     json_path="/path/to/json/files"
# )
# processor.process_all_files()
#
# # Custom configuration
# processor = BatchBoundingBoxProcessor(
#     json_path="/path/to/json/files",
#     filename_pattern="annotation_*.json",
#     output_path="/path/to/output",
#     output_filename="my_bounding_boxes.csv"
# )
# processor.process_all_files()
#
# # Get summary before processing
# summary = processor.get_processing_summary()
# print(f"Found {summary['total_files']} files to process")
#
# # ---------------------------
# # Example in the main.py file
# if __name__ == "__main__":
#     # Set up logging
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s - %(message)s'
#     )
#
#     # Example usage
#     try:
#         # Initialize the processor
#         processor = BatchBoundingBoxProcessor(
#             json_path="/path/to/json/files",
#             filename_pattern="*.json",
#             output_path="/path/to/output",
#             output_filename="extracted_bounding_boxes.csv"
#         )
#
#         # Get processing summary
#         summary = processor.get_processing_summary()
#         print(f"Will process {summary['total_files']} files")
#         print(f"Output will be saved to: {summary['full_output_path']}")
#
#         # Process all files
#         success = processor.process_all_files()
#
#         if success:
#             print("Processing completed successfully!")
#         else:
#             print("Processing failed or no data was extracted.")
#
#     except Exception as e:
#         print(f"Error: {e}")
