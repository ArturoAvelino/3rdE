import logging
from pathlib import Path
from typing import List

from tools.read_json_and_plot_contour_objects import read_json_plot_contours
from tools.read_json_and_crop_objects import CropIndividualObjects
from tools.mesh_drawer import MeshDrawer
from PIL import Image

from autosegmentation.background_remover import BackgroundRemover
from autosegmentation.batch_config_JSON_generator import BatchConfigGenerator
from autosegmentation.batch_config_JSON_processor import BatchConfigProcessor
from computer_vision.bounding_box_drawer import BoundingBoxDrawer


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


def process_background_remover(input_dir, output_dir=None,
                               image_pattern="capt*.jpg"):
    """
    Process a batch of images, creating
    visualization plots and organizing outputs in dedicated directories.
    """
    # Configuration constants
    DEFAULT_N_CLUSTERS = 5
    DEFAULT_BACKGROUND_CLUSTERS = [0, 4]

    logger = logging.getLogger(__name__)
    input_path = Path(input_dir)

    if output_dir is None:
        output_dir = input_path
    else:
        output_dir = Path(output_dir)

    # Find all image files matching the pattern
    image_files = list(input_path.glob(image_pattern))
    if not image_files:
        logger.warning(
            f"No image files found matching pattern '{image_pattern}' in {input_path}")
        return

    logger.info(f"Found {len(image_files)} image files to process")

    for image_file in image_files:
        try:
            # Validate image file existence
            if not image_file.exists():
                logger.warning(
                    f"Image file not found for image {image_file.name}, skipping")
                continue

            # Create output directory with same name as the image file
            image_output_dir = output_dir / image_file.stem
            image_output_dir.mkdir(exist_ok=True)
            logger.info(f"Processing {image_file.name}")

            # -----------
            # Remove color background from the images.
            processor = BackgroundRemover(image_file, image_output_dir)
            processor.cluster_rgb_colors(n_clusters=DEFAULT_N_CLUSTERS)
            processor.plot_rgb_rawdata()
            processor.plot_rgb_clusters()
            processor.plot_rgb_clusters_colorful()
            processor.plot_replaced_colors_in_image()
            processor.remove_background(
                background_clusters=DEFAULT_BACKGROUND_CLUSTERS)
            # -----------

            logger.info(f"Successfully processed {image_file.name}")
        except Exception as e:
            logger.error(f"Error processing {image_file.name}: {str(e)}")


def generate_configuration_files_only(
        sample_name: str,
        raw_image_pattern: str,
        raw_image_batch_path: str,
        no_background_image_pattern: str,
        no_background_image_batch_path: str,
        max_distance: float = 4.0,
        min_pixels: int = 1000,
        padding: int = 35,
        cropping: bool = True,
        config_output_path: str = None
    ) -> List[str]:
    """
    Generate configuration JSON files only using the BatchConfigGenerator class.

    This function creates configuration files for batch processing without actually
    processing the images. Useful for preparing configurations that will be processed
    later or for reviewing configuration parameters before processing.

    Args:
        sample_name (str): Name of the sample
        raw_image_pattern (str): Pattern for raw images (e.g., "*.jpg")
        raw_image_batch_path (str): Path to raw images directory
        no_background_image_pattern (str): Pattern for no-background images
        no_background_image_batch_path (str): Path to no-background images directory
        max_distance (float): Maximum distance for segmentation
        min_pixels (int): Minimum pixels for valid objects
        padding (int): Padding for cropping
        cropping (bool): Enable/disable cropping
        config_output_path (str): Where to save config files (if None, uses no_background path)

    Returns:
        List[str]: List of paths to generated configuration files
    """
    logger = logging.getLogger(__name__)

    try:
        # Set the default config output path if not provided
        if config_output_path is None:
            config_output_path = str(
                Path(no_background_image_batch_path) / "configs")

        logger.info("=== GENERATING CONFIGURATION FILES ONLY ===")
        logger.info(f"Sample name: {sample_name}")
        logger.info(f"Raw images pattern: {raw_image_pattern}")
        logger.info(f"Raw images path: {raw_image_batch_path}")
        logger.info(
            f"No-background images pattern: {no_background_image_pattern}")
        logger.info(
            f"No-background images path: {no_background_image_batch_path}")
        logger.info(f"Configuration output path: {config_output_path}")
        logger.info(
            f"Processing parameters: max_distance={max_distance}, min_pixels={min_pixels}, padding={padding}, cropping={cropping}")

        # Initialize the BatchConfigGenerator
        generator = BatchConfigGenerator(
            sample_name=sample_name,
            raw_image_pattern=raw_image_pattern,
            raw_image_batch_path=raw_image_batch_path,
            no_background_image_pattern=no_background_image_pattern,
            no_background_image_batch_path=no_background_image_batch_path,
            max_distance=max_distance,
            min_pixels=min_pixels,
            padding=padding,
            cropping=cropping,
            output_path=config_output_path
        )

        # Generate configuration files
        config_files = generator.generate_config_files()

        if config_files:
            logger.info(
                f"Successfully generated {len(config_files)} configuration files:")
            for config_file in config_files:
                logger.info(f"  - {Path(config_file).name}")

            logger.info(f"Configuration files saved to: {config_output_path}")
            logger.info(
                "These configuration files can be processed later using the BatchConfigProcessor class.")
        else:
            logger.warning(
                "No configuration files were generated. Check your input parameters and image files.")

        return config_files

    except FileNotFoundError as e:
        logger.error(f"Directory not found: {str(e)}")
        return []
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error generating configuration files: {str(e)}")
        return []


def process_batch_of_config_files(
        config_directory: str,
        filename_pattern: str = "*_config.json",
        use_nonwhitepixel_as_bboxcenter: bool = False,
        create_cropped_images: bool = True,
        include_segmentation: bool = True
    ) -> dict:
    """
    Process a batch of images using configuration JSON files with the BatchConfigProcessor.

    This function replaces the previous process_batch_with_configs function and uses
    the new BatchConfigProcessor class to find and process configuration files.

    Args:
        config_directory (str): Directory containing configuration JSON files
        filename_pattern (str): Pattern to match configuration files (default: "*_config.json")

    Returns:
        dict: Processing results with 'successful' and 'failed' lists
    """
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Starting batch processing with config files from: {config_directory}")

        # Initialize the BatchConfigProcessor
        processor = BatchConfigProcessor(
            json_path=config_directory,
            filename_pattern=filename_pattern,
            use_nonwhitepixel_as_bboxcenter = use_nonwhitepixel_as_bboxcenter,
            create_cropped_images = create_cropped_images,
            include_segmentation = include_segmentation
        )

        # Get information about found config files (optional - for logging)
        files_info = processor.get_config_files_info()
        logger.info(f"Found {len(files_info)} configuration files")

        # Log details about each file
        for info in files_info:
            if info['valid']:
                logger.info(f"Valid config: {info['file_name']} - Sample: {info.get('sample_name', 'N/A')}")
            else:
                logger.warning(f"Invalid config: {info['file_name']} - Error: {info.get('error', 'Unknown error')}")

        # Process all configuration files
        results = processor.process_all_configs(validate_before_processing=True)

        # Log summary
        logger.info(f"Batch processing completed:")
        logger.info(f"  - Successfully processed: {len(results['successful'])} files")
        logger.info(f"  - Failed to process: {len(results['failed'])} files")

        if results['failed']:
            logger.warning("Failed files:")
            for failed_file in results['failed']:
                logger.warning(f"  - {failed_file}")

        return results

    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        return {'successful': [], 'failed': []}


def generate_and_process_batch_configs(
        sample_name: str,
        raw_image_pattern: str,
        raw_image_batch_path: str,
        no_background_image_pattern: str,
        no_background_image_batch_path: str,
        max_distance: float = 4.0,
        min_pixels: int = 1000,
        padding: int = 35,
        cropping: bool = True,
        config_output_path: str = None,
        use_nonwhitepixel_as_bboxcenter: bool = False,
        create_cropped_images: bool = True,
        include_segmentation: bool = True
    ) -> dict:
    """
    Complete workflow: Generate configuration files and then process them.

    This function combines the BatchConfigGenerator and BatchConfigProcessor
    to provide a complete end-to-end processing workflow.

    Args:
        sample_name (str): Name of the sample
        raw_image_pattern (str): Pattern for raw images (e.g., "*.jpg")
        raw_image_batch_path (str): Path to raw images directory
        no_background_image_pattern (str): Pattern for no-background images
        no_background_image_batch_path (str): Path to no-background images directory
        max_distance (float): Maximum distance for segmentation
        min_pixels (int): Minimum pixels for valid objects
        padding (int): Padding for cropping
        cropping (bool): Enable/disable cropping
        config_output_path (str): Where to save config files (if None, uses no_background path)

    Returns:
        dict: Processing results
    """
    logger = logging.getLogger(__name__)

    try:
        # Set the default config output path if not provided
        if config_output_path is None:
            config_output_path = str(Path(no_background_image_batch_path) / "configs")

        logger.info("Step 1: Generating configuration files...")

        # Generate configuration files
        generator = BatchConfigGenerator(
            sample_name=sample_name,
            raw_image_pattern=raw_image_pattern,
            raw_image_batch_path=raw_image_batch_path,
            no_background_image_pattern=no_background_image_pattern,
            no_background_image_batch_path=no_background_image_batch_path,
            max_distance=max_distance,
            min_pixels=min_pixels,
            padding=padding,
            cropping=cropping,
            output_path=config_output_path
        )

        config_files = generator.generate_config_files()
        logger.info(f"Generated {len(config_files)} configuration files")

        if not config_files:
            logger.warning("No configuration files were generated")
            return {'successful': [], 'failed': []}

        logger.info("Step 2: Processing generated configuration files...")

        # Process the generated configuration files
        results = process_batch_of_config_files(
            config_directory=config_output_path,
            filename_pattern="*_config.json",
            use_nonwhitepixel_as_bboxcenter = use_nonwhitepixel_as_bboxcenter,
            create_cropped_images  = create_cropped_images,
            include_segmentation = include_segmentation
        )

        return results

    except Exception as e:
        logger.error(f"Error in generate_and_process_batch_configs: {str(e)}")
        return {'successful': [], 'failed': []}


# ##############################################################################
# v2. OK


    # def main():

    #     # sample_name = "F13_CL"

    #     # Setup logging (will create processing.log in the input directory)
    #     log_output_dir = Path(
    #         # f"/Users/aavelino/Downloads/2025_09_10_Emilie/{sample_name}"
    #         "/Users/aavelino/Downloads/2025_09_10_Emilie/"
    #     )

    #     if not log_output_dir.exists():
    #         print(f"Error: Log save directory not found: {log_output_dir}")
    #         return

    #     setup_logging(log_output_dir)
    #     logger = logging.getLogger(__name__)
    #     logger.info("Starting batch processing of images ...")

    #     try:

    #         # =========================================
    #         # Remove the color background from images using clustering (OK).
    #         #
    #         # Comment these lines if you don't want to remove background from the images.

    #         # # SINGLE IMAGE PROCESSING (OK!)

    #         # import numpy as np
    #         # # custom_centers = np.array([[255,0,0], [0,255,0], [0,0,255]])
    #         # custom_centers = np.asarray([[79.49, 130.62, 189.84], [131.84, 107.86, 76.36], [178.59, 173.83, 159.51], [47.20, 28.64, 18.90], [114.45, 146.57, 187.97]])
    #         #
    #         # processor = BackgroundRemover(
    #         #     image_path = "/Users/aavelino/Downloads/images/BM4_E_sandbox/For_Robin/capt0053_segmentation/capt0053.jpg",
    #         #     # image_path = "/Users/aavelino/Downloads/images/BM4_E_sandbox/For_Robin/tests_segmentations/crop_45_capt0053_trimmed_no_bkgd.png",
    #         #     output_dir = "/Users/aavelino/Downloads/images/BM4_E_sandbox/For_Robin/capt0053_segmentation/",
    #         #     n_clusters = 5,  # Default: 5
    #         #     # kmeans_init_centers = custom_centers # (optional)
    #         # )
    #         #
    #         # sampling_ratio = 1000 # For regular images use 1000, for cropped-small images use 10
    #         # processor.cluster_rgb_colors()
    #         # processor.plot_rgb_rawdata(sample_step=sampling_ratio)
    #         # processor.plot_rgb_clusters(sample_step=sampling_ratio)
    #         # processor.plot_rgb_clusters_colorful(sample_step=sampling_ratio)
    #         # processor.plot_replaced_colors_in_image()
    #         #
    #         # # Optional. Remove (i.e., transform to white color) some specific colors.
    #         # color_clusters_to_remove = [0, 4]  # Use [0, 4] to remove the blue background in images.
    #         # processor.remove_background(background_clusters=color_clusters_to_remove)


    #         # -----------------------------------------
    #         # BATCH PROCESSING (OK!)

    #         # sample_name =  "R04_B"

    #         # input_dir = f"/Users/aavelino/Downloads/2025_09_10_Emilie/{sample_name}"
    #         # output_dir = Path(f"/Users/aavelino/Downloads/2025_09_10_Emilie/{sample_name}/")
    #         # logger.info(f"Input directory: {input_dir}")
    #         # logger.info(f"Output directory: {output_dir}")

    #         # process_background_remover(input_dir=input_dir,
    #         #                            output_dir=output_dir,
    #         #                            image_pattern=f"{sample_name}*.jpg")

    #         # logger.info("Successfully completed batch processing")

    #         # =========================================
    #         # # Segmentation and cropping
    #         # #
    #         # -----------------------------------------
    #         # # Option 1 (OK): Generate Configuration Files Only.

    #         # logger.info("=== OPTION 1: Generate Configuration Files Only ===")
    #         #
    #         # config_files = generate_configuration_files_only(
    #         #     sample_name="BM3-F",
    #         #     raw_image_pattern="BM3-F*.jpg",
    #         #     raw_image_batch_path="/Users/aavelino/Downloads/2025_09_10_Emilie/BM3-F/",
    #         #     no_background_image_pattern="*_no_bkgd.png",
    #         #     no_background_image_batch_path="/Users/aavelino/Downloads/2025_09_10_Emilie/BM3-F/",
    #         #     max_distance=4.0,
    #         #     min_pixels=1000,
    #         #     padding=35,
    #         #     cropping=True,
    #         #     config_output_path="/Users/aavelino/Downloads/2025_09_10_Emilie/BM3-F/2_configs_for_segm/"
    #         # )
    #         #
    #         # if config_files:
    #         #     logger.info(
    #         #         f"Configuration generation completed successfully. Created {len(config_files)} files.")
    #         #     logger.info(
    #         #         "You can now process these configurations using the other options below.")
    #         # else:
    #         #     logger.error(
    #         #         "No configuration files were generated. Please check your parameters.")

    #         # -----------------------------------------
    #         # # Option 2 (OK): Process existing configuration files only

    #         # logger.info("=== OPTION 2: Process Existing Configuration Files ===")

    #         # # If you already have configuration files and just want to process them
    #         # config_directory = "/Users/aavelino/Downloads/2025_09_10_Emilie/BM3-F/2_configs_for_segm/"

    #         # if Path(config_directory).exists():
    #         #     results_existing = process_batch_of_config_files(
    #         #         config_directory=config_directory,
    #         #         filename_pattern="*_config.json",
    #         #         use_nonwhitepixel_as_bboxcenter=True,
    #         #         create_cropped_images=False,
    #         #         include_segmentation=False
    #         #     )

    #         #     logger.info(
    #         #         f"Existing configs processing results: {len(results_existing['successful'])} successful, {len(results_existing['failed'])} failed")
    #         # else:
    #         #     logger.info(f"Config directory not found: {config_directory}")

    #         # -----------------------------------------
    #         # # Option 3 (OK): Complete workflow - Generate configs and process them
    #         # # generating the segmentation plot and the individual cropped images.

    #         sample_name =  "R21-A"

    #         logger.info("=== OPTION 3: Generate and Process Configuration Files ===")

    #         results = generate_and_process_batch_configs(
    #             sample_name = sample_name,
    #             raw_image_pattern = f"{sample_name}*.jpg",
    #             raw_image_batch_path = f"/Users/aavelino/Downloads/2025_09_10_Emilie/{sample_name}",
    #             no_background_image_pattern = "*_no_bkgd.png",
    #             no_background_image_batch_path = f"/Users/aavelino/Downloads/2025_09_10_Emilie/{sample_name}",
    #             max_distance=4.0,
    #             min_pixels=1000,
    #             padding=35,
    #             cropping=True,
    #             # config_output_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/For_Robin/tests_segmentations/clustering_crops/"
    #             use_nonwhitepixel_as_bboxcenter = True,
    #             create_cropped_images = False,
    #             include_segmentation = False
    #         )

    #         logger.info(
    #             f"Complete workflow results: {len(results['successful'])} successful, {len(results['failed'])} failed")

    #         # -----------------------------------------
    #         # Option 4 (OK): Process individual configuration file (for testing/debugging)
    #         # logger.info("=== OPTION 4: Single Configuration File Processing ===")
    #         #
    #         # single_config_path = "/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/segmentation/capt0011_config.json"
    #         # if Path(single_config_path).exists():
    #         #     processor_single = BatchConfigProcessor(
    #         #         json_path=str(Path(single_config_path).parent),
    #         #         filename_pattern=Path(single_config_path).name
    #         #     )
    #         #
    #         #     # Process just this one file
    #         #     single_result = processor_single.process_single_config(
    #         #         Path(single_config_path))
    #         #     if single_result:
    #         #         logger.info("Single file processing successful")
    #         #     else:
    #         #         logger.error("Single file processing failed")

    #         # =========================================
    #         # # Segmentation by color (No Ok, old)

    #         # processor = InstanceSegmentationByColor(
    #         #     image_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/For_Robin/capt0053_segmentation/crop_45_capt0053_trimmed_no_bkgd.png",
    #         #     raw_image_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/For_Robin/capt0053_segmentation/tmp_2/clustering_crops/capt0053_trimmed_segm/crop_45_capt0053_trimmed.png",
    #         #     sample_name="BM4_E",
    #         #     output_dir="/Users/aavelino/Downloads/images/BM4_E_sandbox/For_Robin/capt0053_segmentation",
    #         #     n_clusters=5,
    #         #     min_pixels=400,
    #         #     padding=10
    #         # )

    #         # results = processor.process()

    #         # # =========================================

    #         # OK!
    #         # Read the width and height of bounding boxes from a batch of JSON files
    #         # and save them in a single comma-separated value (.CSV) text file.
    #         # This processing is useful for unsupervised clustering techniques to determine
    #         # the most common bounding box sizes of objects. Based on this information,
    #         # I can crop individual objects to a fixed size using the most common sizes
    #         # to get images of the same pixel size as required for clustering and
    #         # label propagation.

    #         # processor = BatchBoundingBoxProcessor(
    #         #     json_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/clustering_crops/4_bbox_sizes/",
    #         #     filename_pattern="*_metadata.json",
    #         #     output_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/clustering_crops/4_bbox_sizes/",
    #         #     output_filename="extracted_bounding_boxes.csv"
    #         # )
    #         #
    #         # # Get processing summary
    #         # summary = processor.get_processing_summary()
    #         # print(f"Will process {summary['total_files']} files")
    #         # print(f"Output will be saved to: {summary['full_output_path']}")
    #         #
    #         # # Process all files
    #         # success = processor.process_all_files()
    #         #
    #         # if success:
    #         #     print("Processing completed successfully!")
    #         # else:
    #         #     print("Processing failed or no data was extracted.")

    #         # # =========================================
    #         # OK!
    #         # K-means clustering on the bounding-boxes sizes to determine the most
    #         # common bbox sizes.

    #         # processor = BoundingBoxClusteringProcessor(
    #         #     cluster_number=6,
    #         #     input_file_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/clustering_crops/4_bbox_sizes/extracted_bounding_boxes.csv",
    #         #     output_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/clustering_crops/4_bbox_sizes/",
    #         #     output_filename="clustering_results"
    #         # )

    #         # # Execute the complete workflow
    #         # summary = processor.process_complete_workflow(
    #         #     algorithm='kmeans',
    #         #     redefine_dims=False,
    #         #     create_raw_plot=True,
    #         #     random_state=42
    #         # )

    #         # print("Clustering Summary:")
    #         # for key, value in summary.items():
    #         #     print(f"  {key}: {value}")

    #         # # Example with DBSCAN
    #         # # processor_dbscan = BoundingBoxClusteringProcessor(
    #         # #     cluster_number=5,  # Not used for DBSCAN but required for initialization
    #         # #     input_file_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/segmentation/bbox_sizes/extracted_bounding_boxes.csv",
    #         # #     output_path="/Users/aavelino/Downloads/images/BM4_E_sandbox/tests/segmentation/bbox_sizes/",
    #         # #     output_filename="clustering_results_dbscan"
    #         # # )
    #         # #
    #         # # summary_dbscan = processor_dbscan.process_complete_workflow(
    #         # #     algorithm='dbscan',
    #         # #     redefine_dims=True,
    #         # #     eps=0.5,
    #         # #     min_samples=5
    #         # # )

    #     except Exception as e:
    #         logger.error(f"An unexpected error occurred: {str(e)}")
    #         raise

    # if __name__ == "__main__":
    #     main()


# ########################################################60

# OK!

    # if __name__ == "__main__":
    #     # From the CSV file containing the bounding boxes
    #     # and the output path for the extracted images
    #     # and the output filename for the extracted images
    #     # from the JSON file containing the metadata
    #     # for the bounding boxes.
    #     # The processor will extract the bounding boxes
    #     # and save them in a single comma-separated value (.CSV) text file.
    #     # This file will be used for the next processing step.
    #     # The processor will then extract the bounding boxes
    #     # and save them in a single comma-separated value (.CSV) text file.
    #     processor = CSVObjectProcessor(
    #         csv_file = "/Users/aavelino/Downloads/images_biigle/Volumes_biigle_annotation_done/biigle_volume_03/image_annotations_unsure_removed.csv",
    #         labels_json_path = "/Users/aavelino/Downloads/images_biigle/Volumes_biigle_annotation_done/label_trees_arranged_all.json",
    #         images_path="/Users/aavelino/Downloads/images_biigle/Archives_biigle_Arthuro-2/Images/BM4_E",
    #         filename_pattern="capt*.jpg",
    #         output_crops_path="/Users/aavelino/Downloads/images_biigle/tests/5",
    #         prefix_filename=""  # Optional prefix
    #     )
    #
    #     # Process all objects
    #     processor.process_all_objects()
    #
    #     # Merge JSON files (saves to output/merged_json/)
    #     processor.merge_json_files_by_image_id()

    # --------------------------------------------------------60

    # Simple usage - process all configs in a directory
    #c results = process_batch_of_config_files(
    #c     config_directory="/path/to/configs",
    #c     filename_pattern="*.json"
    #c )

    # Complete workflow
    #c results = generate_and_process_batch_configs(
    #c     sample_name="BM4_E",
    #c     raw_image_pattern="*.jpg",
    #c     raw_image_batch_path="/path/to/raw/images/",
    #c     no_background_image_pattern="*_no_bkgd.png",
    #c     no_background_image_batch_path="/path/to/processed/images/",
    #c     cropping=True
    #c )

    # Custom processor for specific needs
    #c processor = BatchConfigProcessor(
    #c     json_path="/path/to/configs",
    #c     filename_pattern="experiment_*_config.json"
    #c )
    #c results = processor.process_all_configs()

# ########################################################60

# OK!


if __name__ == "__main__":

    # # Setup logging
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(levelname)s - %(message)s')

    # ------------------------------
    # Draw bounding boxes of images using the info from JSON files.

    # ------------------------------
    # Batch processing, either "coco" and "robo" JSON format

    drawer = BoundingBoxDrawer()

    # Confidence range to plot
    min_confidence = 0.5
    max_confidence = 1.0

    # Advanced usage with customization
    results = drawer.process_batch(
        input_image_dir="/Users/aavelino/Downloads/BiosoilAI/5_images_for_segm_class/3_classification/R21-A",
        input_json_dir="/Users/aavelino/Downloads/BiosoilAI/5_images_for_segm_class/3_classification/R21-A",
        input_json_format="roboflow",
        output_dir="/Users/aavelino/Downloads/BiosoilAI/5_images_for_segm_class/3_classification/R21-A/bboxes",
        suffix_output_imagefiles= f"_bbox_c_{min_confidence}_{max_confidence}",
        font_size=60,
        bbox_color="red",
        text_color="white",
        text_position="top",
        show_center=True,
        center_dot_size=12,
        show_id=False,
        show_label=True,
        show_summary=True,
        confidence_range=(min_confidence, max_confidence)
    )

    # ------------------------------
    # Single file

    # # # Process a single COCO format file. OK!
    # coco_drawer = BoundingBoxDrawer(
    #     json_format="coco",
    #     output_directory="/Users/aavelino/Downloads/2025_09_10_Emilie/BM3-F",
    #     font_size = 55,
    #     bbox_color = "red",
    #     text_color = "white",
    #     text_position = "top",  # (top, bottom) Text below bounding boxes
    #     show_center=True,
    #     center_dot_size=14,
    #     show_id = True,
    #     show_label = False
    # )
    #
    # image_name = "BM3-F_r3c2"
    # success = coco_drawer.process_image_with_annotations(
    #     # image_file_path=f"/Users/aavelino/Downloads/2025_09_10_Emilie/BM3-F/{image_name}.jpg",
    #     image_file_path=f"/Users/aavelino/Downloads/2025_09_10_Emilie/BM3-F/{image_name}_no_bkgd.png",
    #     json_file_path=f"/Users/aavelino/Downloads/2025_09_10_Emilie/BM3-F/3_segmentation/{image_name}_segm/{image_name}_combined_metadata.json",
    #     output_filename=f"{image_name}_with_bboxes.jpg"
    # )

    # ---------------------------------------

    # # Process a single Robo format file. OK!
    # roboflow_drawer = BoundingBoxDrawer(
    #     json_format="roboflow",
    #     output_directory = "/Users/aavelino/Downloads/BiosoilAI/5_images_for_segm_class/3_classification/R21-A/",
    #     # output_directory="/Users/aavelino/Downloads/images_biigle/tests/biigle_volume_02_03/bbox/",
    #     # output_directory="/Users/aavelino/Downloads/images/Sandbox/BM4_F_capt0029/capt0029_gray/roboflow_deploy_detect_count_visualize/",
    #     # output_directory="/Users/aavelino/Downloads/images_biigle/tests/roboflow/predictions/deploy_detect_count_visualize/BM4_F_capt0029/",
    #     font_size = 60,
    #     bbox_color="red",  # All boxes will be red
    #     text_color="white",  # All text will be yellow
    #     text_position="top",  # Text below bounding boxes
    #     confidence_range = (0.2, 1.0),  # Only show objects within a given confidence range.
    #     show_confidence = True,
    #     show_summary = True,  # Show object count summary
    #     summary_position = "bottom_right",  # Position summary: "top_left"
    #     show_center = True,
    #     center_dot_size = 8,
    #     show_id = True  # ID on boxes
    # )
    # success = roboflow_drawer.process_image_with_annotations(
    #     "/Users/aavelino/Downloads/BiosoilAI/5_images_for_segm_class/3_classification/R21-A/R21-A_r7c6.jpg",
    #     "/Users/aavelino/Downloads/BiosoilAI/5_images_for_segm_class/3_classification/R21-A/R21-A_r7c6.json",
    #     output_filename="R21-A_r7c6_bbox.jpg"
    #     # "/Users/aavelino/Downloads/images/Sandbox/BM4_F_capt0029/capt0029_gray/capt0029_no_bkgd.jpg",
    #     # "/Users/aavelino/Downloads/images/Sandbox/BM4_F_capt0029/capt0029_gray/roboflow_deploy_detect_count_visualize/prediction_confidence_0.0.json",
    #     # output_filename = "capt0029_predict_confidence_.jpg"
    # )

    # --------------------------------------------------------60

    # # Example 3: Batch processing
    # batch_drawer = BoundingBoxDrawer(
    #     json_format="coco",
    #     output_directory="/Users/aavelino/Downloads/bbox_tmp/",
    #     image_path="/Users/aavelino/Downloads/bbox_tmp/capt0044.jpg",
    #     json_path="/Users/aavelino/Downloads/bbox_tmp/capt0044_image_114_merged.json"
    # )

    # Process batch
    # results = batch_drawer.process_batch(image_pattern="*.jpg", json_pattern="*.json")
    # print(f"Batch processing: {len(results['successful'])} successful, {len(results['failed'])} failed")

    # ##########################################################

    # DRAW A MILLIMETRIC MESH ON TOP OF IMAGES (OK!)

    # line_color = "white"
    # line_width = 2
    #
    # # Advanced usage with all features
    # mesh_drawer = MeshDrawer(
    #     line_color = line_color,
    #     line_width = line_width,
    #     pixels_per_mm=476,
    #     line_distance_mm=1,
    #     draw_scale=True,
    #     scale_position="top_left",
    #     scale_size_mm=2.0,
    #     draw_subscales=True,
    #     subscale_distance_mm=0.2
    # )
    #
    # # Apply to existing image
    # input_image_path = "/Users/aavelino/Downloads/BiosoilAI/1_images_miniset/BM4_E_sandbox/tests/mesh_on_top_image/capt0011.jpg"
    # output_image_path = f"/Users/aavelino/Downloads/BiosoilAI/1_images_miniset/BM4_E_sandbox/tests/mesh_on_top_image/capt0011_mesh_{line_color}_lw_{line_width}.jpg"
    #
    # existing_image = Image.open(input_image_path)
    # result = mesh_drawer.draw_mesh_on_image(existing_image)
    # result.save(output_image_path)

