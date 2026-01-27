import csv
from typing import Union, Iterable


def filter_annotations_by_labels(
    annotations_csv: str,
    labels_csv: str,
    output_csv: str,
    annotations_id_col: str = "id",
    labels_id_col: str = "annotation_id",
    *,
    encoding: str = "utf-8",
) -> None:
    """
    Filter an annotations CSV by IDs present in a labels CSV and write the result.

    This function keeps only the rows from ``annotations_csv`` whose identifier
    in ``annotations_id_col`` also appears in ``labels_csv`` under
    ``labels_id_col``. The filtered rows are written to ``output_csv`` with the
    same header as the input annotations file.

    Args:
        annotations_csv: Path to the annotations CSV (e.g., image_annotations.csv).
        labels_csv: Path to the labels CSV (e.g., image_annotation_labels.csv).
        output_csv: Path for the filtered annotations CSV output.
        annotations_id_col: Column name in annotations_csv used for matching.
        labels_id_col: Column name in labels_csv containing valid IDs.
        encoding: Text encoding for all CSV files.

    Raises:
        ValueError: If the required ID column is missing in either input file.

    Example:
        filter_annotations_by_labels(
            "image_annotations.csv",
            "image_annotation_labels.csv",
            "image_annotations_filtered.csv",
        )
    """
    # Collect valid annotation IDs from labels CSV
    valid_ids = set()
    with open(labels_csv, newline="", encoding=encoding) as f_labels:
        reader = csv.DictReader(f_labels)
        if labels_id_col not in reader.fieldnames:
            raise ValueError(f"Missing column '{labels_id_col}' in {labels_csv}")
        for row in reader:
            valid_ids.add(row[labels_id_col])

    # Stream annotations and write only matching rows
    with open(annotations_csv, newline="", encoding=encoding) as f_ann, \
         open(output_csv, "w", newline="", encoding=encoding) as f_out:
        reader = csv.DictReader(f_ann)
        if annotations_id_col not in reader.fieldnames:
            raise ValueError(f"Missing column '{annotations_id_col}' in {annotations_csv}")
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row[annotations_id_col] in valid_ids:
                writer.writerow(row)


# ########################################################60

# Example use

# filter_annotations_by_labels(
#     "image_annotations.csv",
#     "image_annotation_labels.csv",
#     "image_annotations_filtered.csv",
# )
