from utils.segmentation_image_processor import SegmentationProcessor
import logging
from pathlib import Path


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Define the path to your JSON file
    json_file_path = "/Users/aavelino/Downloads/images/Guillaume/2025_05_15/im44.json"

    # Verify that the JSON file exists
    if not Path(json_file_path).is_file():
        logger.error(f"JSON file not found: {json_file_path}")
        return

    # Create output directory if it doesn't exist
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    logger.info("Starting image processing...")

    # Create an instance of SegmentationProcessor with custom parameters
    try:
        processor = SegmentationProcessor(
            json_file_path=json_file_path,
            output_dir=output_dir,
            padding=10,
            use_bbox=False
        )

        # Process all annotations
        processor.process_all()
        logger.info("Successfully processed all annotations!")

    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
    except PermissionError as e:
        logger.error(f"Permission error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise  # Re-raise the exception for debugging


if __name__ == "__main__":
    main()