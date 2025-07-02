import logging
from pathlib import Path
import json

from tools.read_json_plot_contour_objects import read_json_plot_contours
from tools.read_json_crop_objects import CropIndividualObjects

from utils.background_remover import ImageSegmentationProcessor
from utils.crop_and_compute_boundingbox import CropImageAndWriteBBox
from utils.instance_segmentator import InstanceSegmentation

def setup_logging(input_dir):
    """
    Configure and initialize the logging system for both console and file output.

    This function sets up a comprehensive logging system that:
    1. Creates a root logger that handles both console and file output
    2. Sets up formatted log messages including timestamp, log level, and message content
    3. Creates a log file in the specified input directory
    4. Configures console output for immediate feedback during execution

    The logging system is configured with the following features:
    - Log Level: INFO (captures Info, Warning, Error, and Critical messages)
    - Message Format: "timestamp - log_level - message"
    - Console Output: Immediate display of all log messages
    - File Output: All messages saved to 'processing.log' in the input directory
    - File Mode: 'w' (creates new log file each run, overwriting any existing file)

    Args:
        input_dir (Path): Path object representing the directory where the log file
                         will be created. The log file 'processing.log' will be
                         placed in this directory.

    Returns:
        None

    Creates:
        - processing.log: Log file in the specified input directory
        - Console output stream for immediate logging feedback

    Log Format:
        All log entries follow the format:
        "YYYY-MM-DD HH:MM:SS,mmm - LEVEL - message"
        Example: "2025-06-10 14:30:45,123 - INFO - Processing started"

    Initial Log Entries:
        The function automatically logs:
        1. The input directory path
        2. The log file location

    Example:
        ```python
        from pathlib import Path

        # Setup logging for a specific directory
        input_directory = Path("/path/to/input/dir")
        setup_logging(input_directory)

        # After setup, you can use logging throughout your code
        logger = logging.getLogger(__name__)
        logger.info("Starting process...")
        ```

    Notes:
        - Previous log handlers are not removed, so calling this function multiple
          times will add additional handlers
        - The function creates the log file immediately, even if no log messages
          are generated
        - Console output provides immediate feedback while file output ensures
          permanent record keeping

    Dependencies:
        - logging: Python's built-in logging module
        - pathlib.Path: For path handling
    """

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create console handler and set formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create file handler and set formatter
    log_file = input_dir / "processing.log"
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Log initial information
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Log file location: {log_file}")


def process_json_plot_contours(input_dir, image_pattern="capt*.jpg"):
    """
    Process a batch of images and their corresponding JSON segmentation files, creating
    visualization plots and organizing outputs in dedicated directories.

    This function performs the following operations for each image:
    1. Identifies image files matching the specified pattern in the input directory
    2. Locates corresponding JSON files containing segmentation data
    3. Creates a dedicated output directory named after each image
    4. Generates visualization plots of the segmentations using read_and_plot_segmentations
    5. Copies and formats the JSON data into the output directory

    The function expects image and JSON files to follow these conventions:
    - Image files follow the pattern specified (default: "captXXXX.jpg")
    - JSON files have the same name as their corresponding images but with .json extension
    - JSON files contain segmentation data in the format required by read_and_plot_segmentations

    For each processed image, the function creates:
    - A new directory named after the image file
    - A PNG file containing the visualization plot of the segmentations
    - A copy of the JSON file with formatted indentation

    Args:
        input_dir (str or Path): Path to the directory containing the input images and JSON files.
                                Can be provided as a string or Path object.
        image_pattern (str): Glob pattern to match image files. Defaults to "capt*.jpg".
                           Modify this if your image files follow a different naming convention.

    Returns:
        None

    Raises:
        No exceptions are raised directly - all exceptions are caught, logged, and processing
        continues with the next image.

    Logs:
        INFO: Number of files found, processing start/completion for each file
        WARNING: When no files are found or when JSON files are missing
        ERROR: Any exceptions that occur during processing of individual files

    Example:
        ```python
        # Process all images in a directory with default pattern
        process_image_segmentations("/path/to/images")

        # Process images with a different naming pattern
        process_image_segmentations("/path/to/images", image_pattern="image_*.jpg")
        ```

    Notes:
        - The function requires logging to be configured before use
        - Existing output directories and files will be overwritten
        - The function continues processing remaining images even if some fail
        - All operations are logged to both console and log file (if configured)

    Dependencies:
        - pathlib.Path for path handling
        - logging for operation logging
        - json for JSON file operations
        - read_and_plot_segmentations function for visualization generation
    """
    logger = logging.getLogger(__name__)
    input_dir = Path(input_dir)

    # Find all image files matching the pattern
    image_files = list(input_dir.glob(image_pattern))

    if not image_files:
        logger.warning(
            f"No image files found matching pattern '{image_pattern}' in {input_dir}")
        return

    logger.info(f"Found {len(image_files)} image files to process")

    for image_file in image_files:
        try:
            # Construct JSON file path (same name as image but .json extension)
            json_file = image_file.with_suffix('.json')

            if not json_file.exists():
                logger.warning(
                    f"JSON file not found for image {image_file.name}, skipping")
                continue

            # Create output directory with same name as the image file
            output_dir = input_dir / image_file.stem
            output_dir.mkdir(exist_ok=True)

            logger.info(f"Processing {image_file.name}")

            # Process the JSON file and create the plot
            output_path = output_dir / f"{image_file.stem}.png"
            read_json_plot_contours(json_file, output_path)

            #old # Copy the JSON file to the output directory
            #old with open(json_file, 'r') as f:
            #old     json_data = json.load(f)
            #old
            #old output_json = output_dir / json_file.name
            #old with open(output_json, 'w') as f:
            #old     json.dump(json_data, f, indent=4)

            logger.info(f"Successfully processed {image_file.name}")

        except Exception as e:
            logger.error(f"Error processing {image_file.name}: {str(e)}")


def process_json_crop(input_dir, image_pattern="capt*.jpg", padding = 0):
    """
    Process a batch of images and their corresponding JSON segmentation files, creating
    visualization plots and organizing outputs in dedicated directories.

    This function performs the following operations for each image:
    1. Identifies image files matching the specified pattern in the input directory
    2. Locates corresponding JSON files containing segmentation data
    3. Creates a dedicated output directory named after each image
    4. Generates visualization plots of the segmentations using read_and_plot_segmentations
    5. Copies and formats the JSON data into the output directory

    The function expects image and JSON files to follow these conventions:
    - Image files follow the pattern specified (default: "captXXXX.jpg")
    - JSON files have the same name as their corresponding images but with .json extension
    - JSON files contain segmentation data in the format required by read_and_plot_segmentations

    For each processed image, the function creates:
    - A new directory named after the image file
    - A PNG file containing the visualization plot of the segmentations
    - A copy of the JSON file with formatted indentation

    Args:
        input_dir (str or Path): Path to the directory containing the input images and JSON files.
                                Can be provided as a string or Path object.
        image_pattern (str): Glob pattern to match image files. Defaults to "capt*.jpg".
                           Modify this if your image files follow a different naming convention.

    Returns:
        None

    Raises:
        No exceptions are raised directly - all exceptions are caught, logged, and processing
        continues with the next image.

    Logs:
        INFO: Number of files found, processing start/completion for each file
        WARNING: When no files are found or when JSON files are missing
        ERROR: Any exceptions that occur during processing of individual files

    Example:
        ```python
        # Process all images in a directory with default pattern
        process_image_segmentations("/path/to/images")

        # Process images with a different naming pattern
        process_image_segmentations("/path/to/images", image_pattern="image_*.jpg")
        ```

    Notes:
        - The function requires logging to be configured before use
        - Existing output directories and files will be overwritten
        - The function continues processing remaining images even if some fail
        - All operations are logged to both console and log file (if configured)

    Dependencies:
        - pathlib.Path for path handling
        - logging for operation logging
        - json for JSON file operations
        - read_and_plot_segmentations function for visualization generation
    """
    logger = logging.getLogger(__name__)
    input_dir = Path(input_dir)

    # Find all image files matching the pattern
    image_files = list(input_dir.glob(image_pattern))

    if not image_files:
        logger.warning(
            f"No image files found matching pattern '{image_pattern}' in {input_dir}")
        return

    logger.info(f"Found {len(image_files)} image files to process")

    for image_file in image_files:
        try:
            # Construct JSON file path (same name as image but .json extension)
            json_file = image_file.with_suffix('.json')

            if not json_file.exists():
                logger.warning(
                    f"JSON file not found for image {image_file.name}, skipping")
                continue

            # Create output directory with same name as the image file
            output_dir = input_dir / image_file.stem
            output_dir.mkdir(exist_ok=True)

            logger.info(f"Processing {image_file.name}")

            #old # Process the JSON file and create the plot
            #old output_path = output_dir / f"{image_file.stem}.png"
            #old read_json_plot_contours(json_file, output_path)

            # -----------
            # Process the reading of JSON file and cropping the images
            processor = CropIndividualObjects(
                json_file_path=json_file,
                output_dir=output_dir,
                normalize_coords=False,
                padding=padding,
                use_bbox=False
            )
            processor.process_all()

            # -----------

            logger.info(f"Successfully processed {image_file.name}")

        except Exception as e:
            logger.error(f"Error processing {image_file.name}: {str(e)}")


def process_background_remover(input_dir, image_pattern="capt*.jpg"):
    """
    Process a batch of images, creating
    visualization plots and organizing outputs in dedicated directories.
    """
    logger = logging.getLogger(__name__)
    input_dir = Path(input_dir)

    # Find all image files matching the pattern
    image_files = list(input_dir.glob(image_pattern))

    if not image_files:
        logger.warning(
            f"No image files found matching pattern '{image_pattern}' in {input_dir}")
        return

    logger.info(f"Found {len(image_files)} image files to process")

    for image_file in image_files:
        try:
            # Construct the image file path
            image_path = input_dir / image_file

            if not image_path.exists():
                logger.warning(
                    f"Image file not found for image {image_file.name}, skipping")
                continue

            # Create output directory with same name as the image file
            output_dir = input_dir / image_file.stem
            output_dir.mkdir(exist_ok=True)

            logger.info(f"Processing {image_file.name}")

            # -----------
            # Remove color background from the images.

            processor = ImageSegmentationProcessor(image_path, output_dir)
            processor.cluster_rgb_colors(n_clusters=5)
            processor.plot_rgb_rawdata()
            processor.plot_rgb_clusters()
            processor.plot_rgb_clusters_colorful()
            processor.remove_background(background_clusters=[0, 4])

            # -----------

            logger.info(f"Successfully processed {image_file.name}")

        except Exception as e:
            logger.error(f"Error processing {image_file.name}: {str(e)}")


# Not ready yet:
def process_crop_objects(input_dir, image_pattern="capt*.jpg",
                        sample_name="sample_name"):
    """
    Process a batch of images.
    """
    logger = logging.getLogger(__name__)
    input_dir = Path(input_dir)

    # Find all image files matching the pattern
    image_files = list(input_dir.glob(image_pattern))

    if not image_files:
        logger.warning(
            f"No image files found matching pattern '{image_pattern}' in {input_dir}")
        return

    logger.info(f"Found {len(image_files)} image files to process")

    for image_file in image_files:
        try:
            # Construct an image file path
            image_path = input_dir / image_file


            if not image_path.exists():
                logger.warning(
                    f"Image file not found for image {image_file.name}, skipping")
                continue

            # Create output directory with same name as the image file
            output_dir = input_dir / image_file.stem
            output_dir.mkdir(exist_ok=True)

            # Construct an image file path of the image without a background.
            image_no_bkgd_path = output_dir / f"{image_file.stem}_no_bkgd.png"

            logger.info(f"Processing {image_file.name}")

            # -----------
            # Crop objects from the image.

            processor = CropImageAndWriteBBox(
                segmented_image = image_no_bkgd_path,
                path_raw_image= image_path,
                sample_name = sample_name,
                output_dir = output_dir
            )

            # Process all groups and save them as PNG
            processor.process_all_groups(image_format='PNG')

            # -----------

            logger.info(f"Successfully processed {image_file.name}")

        except Exception as e:
            logger.error(f"Error processing {image_file.name}: {str(e)}")


def main():

    # Define input directory
    # input_dir = Path("/Volumes/ARTURO_USB/Guillaume/2025_06_04/BM4_E/images")
    input_dir = Path("/Users/aavelino/Downloads/images/Small_acarians_Loic")

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return

    # Setup logging (will create processing.log in the input directory)
    setup_logging(input_dir)
    logger = logging.getLogger(__name__)

    logger.info("Starting batch processing of images ...")

    # =========================================
    # Remove color background from a batch of images, using clustering. OK
    # Comment these lines if you don't want to remove background from the images.
    # try:
    #     process_background_remover(input_dir, image_pattern="F40_A_*.jpg")
    #     logger.info("Successfully completed batch processing")

    # =========================================
    # SINGLE image

    # Grouping pixels to segment the objects present in a SINGLE image and then
    # plotting the map of these objects.
    try:
        # Path to the JSON config file
        config_path = '/Users/aavelino/Downloads/images/BM4_E_sandbox/clustering_crops/capt0011/capt0011_config.json'

        # Initialize and process
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

        # Debugging lines
        print(f"- Raw cropping value: {repr(processor.cropping)}")
        print(f"- Type of cropping value: {type(processor.cropping)}")
        print(f"- Boolean conversion result: {cropping}")

        if cropping == True:

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
                processor_crop.process_all_groups(combine_json_data=True)
            except Exception as e:
                raise Exception(f"Error processing info defined in the config file: {str(e)}")

    # =========================================
    # Not ready yet:

    # Crop objects from a batch of images.
    # try:
    #     process_crop_objects(input_dir, padding=1, sample_name="BM4_E")
    #     logger.info("Successfully completed batch processing")

    # --------------------------30
    # Not ready yet:

    # Crop and write JSON metadata from a single image
    # try:
    #     processor = CropImageAndWriteBox()

    # =========================================
    # # Plot CONTOURS based on the JSON files.
    # # Comment these 3 lines if you don't want to plot contours.
    # try:
    #     process_json_plot_contours(input_dir)
    #     logger.info("Successfully completed batch processing")

    # =========================================
    # # Create CROP images based on the JSON files.
    # # Comment these 3 lines if you don't want to crop.
    # try:
    #     process_json_crop(input_dir, padding=1)
    #     logger.info("Successfully completed batch processing")

    # =========================================

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()