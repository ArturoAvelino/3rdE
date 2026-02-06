import csv
import os
from pathlib import Path
from typing import Dict

class CSVLabelPredictionsMerger:
    """
    Combines predictions from a 'generalist' model and a 'metazoa' model.
    The generalist file acts as the primary template, but specific objects are
    updated with metazoa labels based on user-defined confidence thresholds.

	- This class merges two label-prediction CSV files—generalist
	  (primary) and metazoa—into a single image_annotation_labels.csv,
	  keyed by annotation_id.

	- The generalist file is the baseline. Rows are updated only when
	  confidence is low or the generalist prediction is
	  missing/unclassified.

	Decision rules (per annotation_id):

		- If the generalist prediction has confidence >= gen_threshold,
		  keep the generalist (label_id, user_id, confidence) unchanged.

		- If the generalist prediction has confidence < gen_threshold:

			- If metazoa has a prediction with confidence >=
			  met_threshold, replace the generalist fields with
			  metazoa’s (label_id, user_id, confidence).

			- If metazoa has a prediction but confidence < met_threshold,
			  output an unclassified prediction: label_id = 4196, user_id
			  = 5, confidence = 0.000.

			- If metazoa has no prediction, output unclassified with the
			  same default values.

		- If the generalist prediction is unclassified (label_id = 4196)
		  and metazoa has a prediction with confidence >= met_threshold,
		  replace the unclassified entry with metazoa’s prediction.

		- If the generalist has no prediction for an object but metazoa
		  does (with confidence >= met_threshold), use metazoa’s
		  prediction; otherwise keep it unclassified.

	Defaults:

	- Unclassified prediction is always recorded as label_id = 4196,
	  user_id = 5, confidence = 0.000.
	- Missing prediction is recorded as label_id = 4196, user_id = 5,
	  confidence = 0.000.
	- Unspecified confidence threshold defaults to 0.000.
	- Unspecified default label ID defaults to 4196.

    """

    def __init__(
        self,
        generalist_path: str,
        metazoa_path: str,
        default_label_id: str = "4196"
    ):
        self.generalist_path = Path(generalist_path)
        self.metazoa_path = Path(metazoa_path)
        self.default_label_id = self._normalize_id(default_label_id)
        self.stats = {"total_rows": 0, "labels_replaced": 0}

    def _normalize_id(self, value: str) -> str:
        """Normalizes ID-like fields so lookups match across CSVs."""
        if value is None:
            return ""
        text = str(value).strip()
        if text.endswith(".0") and text.count(".") == 1 and text.replace(".", "").isdigit():
            return text[:-2]
        return text

    def _load_metazoa_lookup(self) -> Dict[str, Dict]:
        """Loads metazoa CSV into a dictionary for O(1) lookup speed."""
        metazoa_lookup = {}
        with open(self.metazoa_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ann_id = self._normalize_id(row.get('annotation_id'))
                if not ann_id:
                    continue
                metazoa_lookup[ann_id] = row
        return metazoa_lookup

    def merge(
        self,
        output_path: str,
        gen_threshold: float,
        met_threshold: float
    ):
        """
        Creates a new CSV based on the generalist file with metazoa refinements.

        Args:
            output_path: Destination for the combined CSV.
            gen_threshold: Confidence threshold for the generalist model.
            met_threshold: Confidence threshold for the metazoa model.
        """
        met_lookup = self._load_metazoa_lookup()
        self.stats = {"total_rows": 0, "labels_replaced": 0, "labels_set_unclassified": 0}

        output_path_str = str(output_path)
        output_path_obj = Path(output_path_str)
        treat_as_dir = output_path_str.endswith(os.sep) or (output_path_obj.exists() and output_path_obj.is_dir())
        if treat_as_dir:
            output_path_obj.mkdir(parents=True, exist_ok=True)
            output_file_path = output_path_obj / "image_annotation_labels.csv"
        else:
            output_path_obj.parent.mkdir(parents=True, exist_ok=True)
            output_file_path = output_path_obj

        with open(self.generalist_path, mode='r', encoding='utf-8') as f_in, \
             open(output_file_path, mode='w', newline='', encoding='utf-8') as f_out:

            reader = csv.DictReader(f_in)
            writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                self.stats["total_rows"] += 1
                ann_id = self._normalize_id(row.get('annotation_id'))

                # Always keep confidence formatted to 3 decimals in the output
                row['confidence'] = f"{float(row['confidence']):.3f}"

                # If the object exists in the metazoa predictions, evaluate for replacement
                if ann_id and ann_id in met_lookup:
                    met_row = met_lookup[ann_id]

                    gen_label = self._normalize_id(row.get('label_id'))
                    gen_conf = float(row['confidence'])

                    met_label = self._normalize_id(met_row.get('label_id'))
                    met_conf = float(met_row['confidence'])
                    met_user = met_row['user_id']

                    # NEW RULE (highest priority):
                    # If both models are below their thresholds => force Unclassified.
                    if gen_conf < gen_threshold and met_conf < met_threshold:
                        row['label_id'] = self.default_label_id  # 4196
                        row['user_id'] = "5"
                        row['confidence'] = "0.000"  # always 3 decimals
                        self.stats["labels_set_unclassified"] += 1

                    else:
                        should_replace = False

                        # Condition 1: Non-default label with low confidence
                        if gen_label != self.default_label_id:
                            if gen_conf < gen_threshold and met_conf > met_threshold:
                                should_replace = True

                        # Condition 2: Default label (4196) being refined by metazoa
                        elif gen_label == self.default_label_id:
                            if met_label != self.default_label_id and met_conf > met_threshold:
                                should_replace = True

                        if should_replace:
                            row['label_id'] = met_label
                            row['user_id'] = met_user  # Update user_id
                            row['confidence'] = f"{met_conf:.3f}"  # always 3 decimals
                            self.stats["labels_replaced"] += 1

                writer.writerow(row)

        print("Merge Complete!")
        print(f"- Processed:            {self.stats['total_rows']} rows")
        print(f"- Replaced by metazoa:  {self.stats['labels_replaced']} rows")
        print(f"- Forced unclassified:  {self.stats['labels_set_unclassified']} rows")
        print(f"- Output:               {output_path}")


# # --- Example Usage ---
# if __name__ == "__main__":
#     # Initialize with the two prediction files
#     merger = CSVLabelPredictionsMerger(
#         generalist_path="generalist_results.csv",
#         metazoa_path="metazoa_results.csv"
#     )
#
#     # Run the merge with your specific thresholds
#     merger.merge(
#         output_path="refined_predictions.csv",
#         gen_threshold=0.45,  # Replace if generalist is less than 45% confident
#         met_threshold=0.80   # And metazoa is at least 80% confident
#     )
