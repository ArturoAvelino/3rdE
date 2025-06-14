import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def read_json_plot_contours(json_file_path, output_path=None):
    """
    Code to read and create a 2D plot a JSON file having a structure
    generated by the command line “coco_tkit svg2coco”.

    The "segmentation" section corresponds to the location of pixels in an
    image, where the first and second rows correspond to the x and y axis
    values of the first pixel, the third and fourth rows correspond to the x
    and y axis values of the second pixel, and so on.

    These kind of JSON files look like this:
    {
        "images": [
            {
                "id": 1,
                "file_name": "capt0044.jpg",
                "height": 4000,
                "width": 6000
            }
        ],
        "annotations": [
            {
                "id": 1,
                "segmentation": [
                    [
                      1539,
                      3889,
                      1540,
                      3888,
                      1541,
                      3888,
                      AND SO ON.
                    ]
                ],
                "image_id": 1,
                "iscrowd": 0,
                "bbox": [
                    1479,
                    3888,
                    113,
                    112
                ],
                "area": 12656,
                "category_id": 1
            },
            {
                AND SO ON.
            }
        ],
        "categories": [
            {
                "id": 1,
                "name": "Organism",
                "supercategory": ""
            }
        ],
        "type": "",
        "licenses": "",
        "info": ""
    }
    """
    # Read the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Create a figure with a fixed size
    plt.figure(figsize=(15, 10))  # Make it square and reasonable size

    # Initialize min/max values for axis scaling
    x_min, x_max, y_min, y_max = float('inf'), float('-inf'), float('inf'), float('-inf')

    # Plot segmentations for each annotation
    for annotation in data['annotations']:
        segments = annotation['segmentation'][0]
        x_coords = segments[::2]
        y_coords = segments[1::2]

        # Update min/max values
        x_min = min(x_min, min(x_coords))
        x_max = max(x_max, max(x_coords))
        y_min = min(y_min, min(y_coords))
        y_max = max(y_max, max(y_coords))

        plt.plot(x_coords, y_coords, 'o-', label=f'Object {annotation["id"]}',
                markersize=2, linewidth=0.5)  # Reduced marker size and line width

    # Set axis limits with a small margin
    margin = 0.05  # 5% margin
    x_range = x_max - x_min
    y_range = y_max - y_min
    plt.xlim(x_min - margin * x_range, x_max + margin * x_range)
    # Reversed for image coordinates:
    plt.ylim(y_max + margin * y_range, y_min - margin * y_range)

    # Customize the plot
    plt.title('Segmentation Coordinates')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    # Move legend outside:
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)  # Lighter grid

    # Make layout tight before saving
    plt.tight_layout()

    # Save the figure if output_path is provided
    if output_path:
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        plt.savefig(output_path, dpi=300, bbox_inches='tight',
                    format=str(output_path.suffix[1:]))  # Convert suffix to string

    # plt.show()
    plt.close()

# Example usage:

# json_path = '/Users/aavelino/Downloads/images/BM4_E/BM4_E.json'
# output_path = Path('/Users/aavelino/Downloads/images/BM4_E/outputs/BM4_E.png')

json_path = '/Users/aavelino/Downloads/images/Guillaume/2025_05_15/im44.json'
output_path = Path('/Users/aavelino/Downloads/images/Guillaume/2025_05_15/output/im44.png')

read_json_plot_contours(json_path, output_path)
