import json
import csv
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import os

from mediapipe.python._framework_bindings import timestamp


@dataclass
class BoundingBox:
    """Data class to represent a bounding box in min-max format."""
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    
    def area(self) -> float:
        """Calculate the area of the bounding box."""
        return max(0, self.x_max - self.x_min) * max(0, self.y_max - self.y_min)


class IoUMetric_for_BBoxMatch:
    """
    High-performance class for matching bounding boxes between Roboflow and Biigle (COCO) formats
    using Intersection over Union (IoU) metric.

    Key Features:

        1. High Performance:
            - Vectorized IoU calculation using NumPy broadcasting for computing all pairwise IoU scores in a single operation
            - Processes hundreds of bounding boxes efficiently by avoiding nested loops
            - Time complexity: O(N×M) with vectorized operations vs O(N×M) with Python loops, but ~10-100x faster in practice

        2. Format Conversion:
            - Automatically converts Roboflow's center-based format to min-max coordinates
            - Automatically converts Biigle's (COCO) top-left format to min-max coordinates
            - All comparisons use a consistent [x_min, y_min, x_max, y_max] format internally

        3. Smart Matching Logic:
            - For each Roboflow object, finds the Biigle object with the highest IoU score
            - Only creates a match if the IoU ≥ threshold
            - Returns empty string for Biigle ID and 0.0 IoU when no match is found

        4. Robust IoU Calculation:
            - Handles edge cases (no intersection, zero-area boxes)
            - Prevents division by zero
            - Uses NumPy's efficient array operations

        5. CSV Output:
            - Generates a clean CSV with exactly 4 columns as specified
            - Includes summary statistics after processing

        6. Logging:
            - Automatically generates log files with matching statistics
            - Appends timestamped entries to existing log files
    """
    
    def __init__(self, roboflow_json_path: str, biigle_json_path: str, iou_threshold: float = 0.8):
        """
        Initialize the IoUMetric_for_BBoxMatch.
        
        Args:
            roboflow_json_path: Path to the Roboflow JSON file
            biigle_json_path: Path to the Biigle (COCO format) JSON file
            iou_threshold: Minimum IoU score required for a match (default: 0.8)
        """
        self.roboflow_json_path = roboflow_json_path
        self.biigle_json_path = biigle_json_path
        self.iou_threshold = iou_threshold
        
        self.roboflow_data = []
        self.biigle_data = []
        
    def load_data(self) -> None:
        """Load and parse both JSON files."""
        # Load Roboflow data
        with open(self.roboflow_json_path, 'r') as f:
            roboflow_raw = json.load(f)

        # Extract predictions from Roboflow format
        self.roboflow_data = []

        # Handle both single dictionary (standard Roboflow) and list of dictionaries
        roboflow_items = roboflow_raw if isinstance(roboflow_raw, list) else [
            roboflow_raw]

        for item in roboflow_items:
            if isinstance(item, dict) and 'predictions' in item:
                # Some formats have nested predictions, others don't
                preds_source = item['predictions']
                if isinstance(preds_source,
                              dict) and 'predictions' in preds_source:
                    actual_predictions = preds_source['predictions']
                elif isinstance(preds_source, list):
                    actual_predictions = preds_source
                else:
                    continue

                for pred in actual_predictions:
                    self.roboflow_data.append({
                        'detection_id': pred['detection_id'],
                        'bbox': self._roboflow_to_minmax(
                            pred['x'], pred['y'], pred['width'], pred['height']
                        ),
                        'class': pred['class'],
                        'confidence': pred['confidence']
                    })

        # Load Biigle data
        with open(self.biigle_json_path, 'r') as f:
            biigle_raw = json.load(f)
        
        # Extract annotations from Biigle (COCO) format
        self.biigle_data = []
        for ann in biigle_raw.get('annotations', []):
            bbox = ann['bbox']  # [x_top_left, y_top_left, width, height]
            self.biigle_data.append({
                'id': ann['id'],
                'class_id': ann['category_id'],
                'bbox': self._biigle_to_minmax(bbox[0], bbox[1], bbox[2], bbox[3])
            })
    
    @staticmethod
    def _roboflow_to_minmax(center_x: float, center_y: float, width: float, height: float) -> BoundingBox:
        """
        Convert Roboflow format (center coordinates) to min-max format.
        
        Args:
            center_x: X coordinate of the center
            center_y: Y coordinate of the center
            width: Width of the bounding box
            height: Height of the bounding box
            
        Returns:
            BoundingBox in min-max format
        """
        x_min = center_x - width / 2
        y_min = center_y - height / 2
        x_max = center_x + width / 2
        y_max = center_y + height / 2
        return BoundingBox(x_min, y_min, x_max, y_max)
    
    @staticmethod
    def _biigle_to_minmax(x_top_left: float, y_top_left: float, width: float, height: float) -> BoundingBox:
        """
        Convert Biigle (COCO) format (top-left coordinates) to min-max format.
        
        Args:
            x_top_left: X coordinate of the top-left corner
            y_top_left: Y coordinate of the top-left corner
            width: Width of the bounding box
            height: Height of the bounding box
            
        Returns:
            BoundingBox in min-max format
        """
        x_min = x_top_left
        y_min = y_top_left
        x_max = x_top_left + width
        y_max = y_top_left + height
        return BoundingBox(x_min, y_min, x_max, y_max)
    
    @staticmethod
    def calculate_iou(bbox1: BoundingBox, bbox2: BoundingBox) -> float:
        """
        Calculate Intersection over Union (IoU) between two bounding boxes.
        
        Args:
            bbox1: First bounding box
            bbox2: Second bounding box
            
        Returns:
            IoU score (0.0 to 1.0)
        """
        # Calculate intersection coordinates
        x_left = max(bbox1.x_min, bbox2.x_min)
        y_top = max(bbox1.y_min, bbox2.y_min)
        x_right = min(bbox1.x_max, bbox2.x_max)
        y_bottom = min(bbox1.y_max, bbox2.y_max)
        
        # Calculate intersection area
        if x_right < x_left or y_bottom < y_top:
            intersection_area = 0.0
        else:
            intersection_area = (x_right - x_left) * (y_bottom - y_top)
        
        # Calculate union area
        bbox1_area = bbox1.area()
        bbox2_area = bbox2.area()
        union_area = bbox1_area + bbox2_area - intersection_area
        
        # Avoid division by zero
        if union_area == 0:
            return 0.0
        
        # Calculate IoU
        iou = intersection_area / union_area
        return iou
    
    def calculate_iou_vectorized(self, roboflow_boxes: np.ndarray, biigle_boxes: np.ndarray) -> np.ndarray:
        """
        Calculate IoU between all pairs of bounding boxes using vectorized operations.
        
        Args:
            roboflow_boxes: Array of shape (N, 4) with [x_min, y_min, x_max, y_max]
            biigle_boxes: Array of shape (M, 4) with [x_min, y_min, x_max, y_max]
            
        Returns:
            IoU matrix of shape (N, M) where element [i, j] is IoU between roboflow_boxes[i] and biigle_boxes[j]
        """
        N = roboflow_boxes.shape[0]
        M = biigle_boxes.shape[0]
        
        # Expand dimensions for broadcasting
        # roboflow_boxes: (N, 1, 4)
        # biigle_boxes: (1, M, 4)
        rf_boxes = roboflow_boxes[:, np.newaxis, :]
        bg_boxes = biigle_boxes[np.newaxis, :, :]
        
        # Calculate intersection coordinates (N, M)
        x_left = np.maximum(rf_boxes[:, :, 0], bg_boxes[:, :, 0])
        y_top = np.maximum(rf_boxes[:, :, 1], bg_boxes[:, :, 1])
        x_right = np.minimum(rf_boxes[:, :, 2], bg_boxes[:, :, 2])
        y_bottom = np.minimum(rf_boxes[:, :, 3], bg_boxes[:, :, 3])
        
        # Calculate intersection area
        intersection_width = np.maximum(0, x_right - x_left)
        intersection_height = np.maximum(0, y_bottom - y_top)
        intersection_area = intersection_width * intersection_height
        
        # Calculate areas of each bounding box
        rf_area = (rf_boxes[:, :, 2] - rf_boxes[:, :, 0]) * (rf_boxes[:, :, 3] - rf_boxes[:, :, 1])
        bg_area = (bg_boxes[:, :, 2] - bg_boxes[:, :, 0]) * (bg_boxes[:, :, 3] - bg_boxes[:, :, 1])
        
        # Calculate union area
        union_area = rf_area + bg_area - intersection_area
        
        # Calculate IoU, avoid division by zero
        iou_matrix = np.where(union_area > 0, intersection_area / union_area, 0.0)
        
        return iou_matrix
    
    def match_boxes(self) -> List[Dict]:
        """
        Match Roboflow objects to Biigle objects based on IoU threshold.
        For each Roboflow object, find the best matching Biigle object.
        
        Returns:
            List of match results with Roboflow ID, Biigle ID, IoU score, and class
        """
        if not self.roboflow_data:
            return []
        
        # Convert to numpy arrays for vectorized computation
        roboflow_boxes = np.array([
            [obj['bbox'].x_min, obj['bbox'].y_min, obj['bbox'].x_max, obj['bbox'].y_max]
            for obj in self.roboflow_data
        ])
        
        biigle_boxes = np.array([
            [obj['bbox'].x_min, obj['bbox'].y_min, obj['bbox'].x_max, obj['bbox'].y_max]
            for obj in self.biigle_data
        ])
        
        # Calculate IoU matrix for all pairs
        iou_matrix = self.calculate_iou_vectorized(roboflow_boxes, biigle_boxes)
        
        # Find best matches
        results = []
        for i, roboflow_obj in enumerate(self.roboflow_data):
            # Get IoU scores for current Roboflow object with all Biigle objects
            iou_scores = iou_matrix[i, :]
            
            # Find the best match
            best_match_idx = np.argmax(iou_scores)
            best_iou = iou_scores[best_match_idx]
            
            # Check if best match exceeds threshold
            if best_iou >= self.iou_threshold:
                biigle_id = self.biigle_data[best_match_idx]['id']
                #old. class_id = self.biigle_data[best_match_idx]['class_id']
            else:
                biigle_id = ''  # No match found
                best_iou = 0.0
                #old. class_id = ''
            
            results.append({
                'roboflow_id': roboflow_obj['detection_id'],
                'biigle_id': biigle_id,
                'iou_score': best_iou,
                #old. 'class_id': class_id,
                'class': roboflow_obj['class'],
                'confidence': roboflow_obj['confidence']
            })
        
        return results
    
    def match_boxes_Biigle_to_robo(self) -> List[Dict]:
        """
        Match Biigle-to-Roboflow objects based on IoU threshold.
        For each Biigle object, find the best matching Roboflow object.

        Returns:
            List of match results with Biigle ID, Roboflow ID, IoU score, and class
        """
        if not self.biigle_data:
            return []

        # Convert to numpy arrays for vectorized computation
        roboflow_boxes = np.array([
            [obj['bbox'].x_min, obj['bbox'].y_min, obj['bbox'].x_max, obj['bbox'].y_max]
            for obj in self.roboflow_data
        ])

        biigle_boxes = np.array([
            [obj['bbox'].x_min, obj['bbox'].y_min, obj['bbox'].x_max, obj['bbox'].y_max]
            for obj in self.biigle_data
        ])

        # Calculate IoU matrix for all pairs
        iou_matrix = self.calculate_iou_vectorized(roboflow_boxes, biigle_boxes)

        # Find the best matches
        results = []
        for j, biigle_obj in enumerate(self.biigle_data):
            # Get IoU scores for the current Biigle object with all Roboflow objects
            # Note: iou_matrix[i, j] where i is roboflow, j is biigle
            # So for each biigle j, we need column j
            iou_scores = iou_matrix[:, j]

            # Find the best match
            best_match_idx = np.argmax(iou_scores)
            best_iou = iou_scores[best_match_idx]

            # Check if best match exceeds threshold
            if best_iou >= self.iou_threshold:
                roboflow_id = self.roboflow_data[best_match_idx]['detection_id']
                class_name = self.roboflow_data[best_match_idx]['class']
                confidence = self.roboflow_data[best_match_idx]['confidence']
            else:
                roboflow_id = ''  # No match found
                best_iou = 0.0
                class_name = 'Unclassified'
                confidence = 0.0

            # Use Biigle label for the object if it is different to "4196" (i.e.,
            # "category_id": 4196 = 'Unclassified').
            if biigle_obj['class_id'] != 4196:
                class_name_id = biigle_obj['class_id']
                class_name = f'met{class_name_id}'
                confidence = 0.99

            results.append({
                'biigle_id': biigle_obj['id'],
                'roboflow_id': roboflow_id,
                'iou_score': best_iou,
                #old1. 'class_id': biigle_obj['class_id'] if roboflow_id != '' else 1,   # original
                #old2. 'class': f"'{class_name}'",  # with quotation marks
                #old3. 'class_id': biigle_obj['class_id'],
                'class': class_name,
                'confidence': confidence
            })

        return results

    def _write_log_entry(self, log_file_path: str, method_name: str, results: List[Dict]) -> None:
        """
        Write a log entry with matching statistics to a plain text log file.

        Args:
            log_file_path: Path to the log file
            method_name: Name of the matching method that was called
            results: List of matching results
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate statistics
        total_roboflow = len(self.roboflow_data)
        total_biigle = len(self.biigle_data)

        if 'roboflow_id' in results[0]:
            # Roboflow to Biigle matching
            matched = sum(1 for r in results if r['biigle_id'] != '')
            unmatched = sum(1 for r in results if r['biigle_id'] == '')
            direction = "Roboflow → Biigle"
        else:
            # Biigle to Roboflow matching
            matched = sum(1 for r in results if r['roboflow_id'] != '')
            unmatched = sum(1 for r in results if r['roboflow_id'] == '')
            direction = "Biigle → Roboflow"

        # Create log entry
        log_entry = f"""
{'='*80}
Timestamp: {timestamp}
Matching Direction: {direction}
Method Called: {method_name}
{'='*80}

Configuration:
  - Roboflow JSON: {self.roboflow_json_path}
  - Biigle JSON: {self.biigle_json_path}
  - IoU Threshold: {self.iou_threshold}

Statistics:
  - Total Roboflow objects: {total_roboflow}
  - Total Biigle objects: {total_biigle}
  - Matched objects: {matched}
  - Unmatched objects: {unmatched}
  - Match rate: {(matched/len(results)*100):.2f}%

{'='*80}

"""

        # Append to log file
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry)

        print(f"Log entry written to: {log_file_path}")

    def save_to_csv_robo_to_biigle(self, output_csv_path: str) -> None:
        """
        Perform matching and save results to a CSV file.

        Args:
            output_csv_path: Path to the output CSV file
        """
        # Load data
        self.load_data()

        # Perform matching
        results = self.match_boxes()

        # Write to CSV
        with open(output_csv_path, 'w', newline='') as csvfile:
            #old. fieldnames = ['Roboflow_ID', 'Biigle_ID', 'Class_ID', 'Class', 'Confidence', 'IoU_Score']
            fieldnames = ['Roboflow_ID', 'Biigle_ID', 'Class',
                          'Confidence', 'IoU_Score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for result in results:
                writer.writerow({
                    'Roboflow_ID': result['roboflow_id'],
                    'Biigle_ID': result['biigle_id'],
                    'Class': result['class'],
                    #old. 'Class_ID': result['class_id'],
                    'Confidence': f"{result['confidence']:.3f}",
                    'IoU_Score': f"{result['iou_score']:.3f}"
                })

        print(f"Matching complete! Results saved to: {output_csv_path}")
        print(f"Total Roboflow objects: {len(results)}")
        print(f"Matched objects: {sum(1 for r in results if r['biigle_id'] != '')}")
        print(f"Unmatched objects: {sum(1 for r in results if r['biigle_id'] == '')}")

        # Generate log file path and write log entry
        log_file_path = os.path.splitext(output_csv_path)[0] + '_log.txt'
        self._write_log_entry(log_file_path, 'save_to_csv_robo_to_biigle', results)

    def save_to_csv_biigle_to_robo(self, output_csv_path: str) -> None:
            """
            Perform matching (Biigle to Roboflow) and save results to a CSV file.

            Args:
                output_csv_path: Path to the output CSV file
            """
            # Load data
            self.load_data()

            # Perform matching
            results = self.match_boxes_Biigle_to_robo()

            # Write to CSV
            with open(output_csv_path, 'w', newline='') as csvfile:
                #old. fieldnames = ['Biigle_ID', 'Roboflow_ID', 'Class_ID', 'Class', 'Confidence', 'IoU_Score']
                fieldnames = ['Biigle_ID', 'Roboflow_ID', 'Class',
                              'Confidence', 'IoU_Score']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for result in results:
                    writer.writerow({
                        'Biigle_ID': result['biigle_id'],
                        'Roboflow_ID': result['roboflow_id'],
                        #old. 'Class_ID': result['class_id'],
                        'Class': result['class'],
                        'Confidence': f"{result['confidence']:.3f}",
                        'IoU_Score': f"{result['iou_score']:.3f}"
                    })

            print(f"Matching complete! Results saved to: {output_csv_path}")
            print(f"Total Biigle objects: {len(results)}")
            print(f"Matched objects: {sum(1 for r in results if r['roboflow_id'] != '')}")
            print(f"Unmatched objects: {sum(1 for r in results if r['roboflow_id'] == '')}")

            # Generate log file path and write log entry
            log_file_path = os.path.splitext(output_csv_path)[0] + '_log.txt'
            self._write_log_entry(log_file_path, 'save_to_csv_biigle_to_robo', results)

    def save_to_csv_for_biigle(self, output_csv_path: str) -> None:
            """
            Create the CSV file suitable for Biigle.

            Args:
                output_csv_path: Path to the output CSV file
            """
            # Load data
            self.load_data()

            # Perform matching
            results = self.match_boxes_Biigle_to_robo()

            # Get current timestamp for Biigle format
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Write to CSV
            with open(output_csv_path, 'w', newline='') as csvfile:
                fieldnames = ['annotation_id', 'label_name', 'user_id','confidence', 'created_at', 'updated_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for result in results:
                    if result['class'] == 'Unclassified':
                        user_id_value = 5 # 5 = SAM (Robin Danz)
                    else: user_id_value = 9 # 9 = YOLO (Arturo Avelino)
                    writer.writerow({
                        'annotation_id': result['biigle_id'],
                        'label_name': result['class'],
                        #old. 'label_id': result['class_id'],
                        'user_id': user_id_value,
                        'confidence': f"{result['confidence']:.3f}",
                        'created_at': current_time,
                        'updated_at': current_time
                    })

            print(f"Matching complete! Results saved to: {output_csv_path}")
            print(f"Total Biigle objects: {len(results)}")
            print(f"Matched objects: {sum(1 for r in results if r['roboflow_id'] != '')}")
            print(f"Unmatched objects: {sum(1 for r in results if r['roboflow_id'] == '')}")

            # Generate log file path and write log entry
            log_file_path = os.path.splitext(output_csv_path)[0] + '_log.txt'
            self._write_log_entry(log_file_path, 'save_to_csv_for_biigle', results)


# ####################################################
# # Example usage
# if __name__ == "__main__":
#     # Initialize the matcher
#     matcher = IoUMetric_for_BBoxMatch(
#         roboflow_json_path='path/to/roboflow.json',
#         biigle_json_path='path/to/biigle.json',
#         iou_threshold=0.8
#     )
#
#     # Roboflow to Biigle matching
#     matcher.save_to_csv('roboflow_to_biigle.csv')
#
#     # Biigle to Roboflow matching
#     matcher.save_to_csv_Biigle_to_robo('biigle_to_roboflow.csv')

