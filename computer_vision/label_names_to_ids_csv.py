#!/usr/bin/env python3
"""Replace label names with label IDs in a CSV using a label_trees.json file."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert the label_name column to label_id using a label_trees.json file."
        )
    )
    parser.add_argument(
        "labels_json",
        type=Path,
        help="Path to the label_trees.json file.",
    )
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Path to the input CSV (e.g., image_annotation_labels_names.csv).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to save the output CSV file. Defaults to input CSV directory.",
    )
    parser.add_argument(
        "--output-name",
        default="image_annotation_labels.csv",
        help="Name of the output CSV file.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any label_name values are missing from the JSON mapping.",
    )
    parser.add_argument(
        "--missing-report",
        action="store_true",
        help=(
            "Write a CSV summary of missing label_name values next to the output "
            "CSV file."
        ),
    )
    parser.add_argument(
        "--missing-report-path",
        type=Path,
        default=None,
        help=(
            "Optional path to write a CSV summary of missing label_name values "
            "and their counts."
        ),
    )
    return parser.parse_args()


def build_label_mapping(labels_json: Path) -> dict[str, int]:
    if not labels_json.exists():
        raise FileNotFoundError(f"Label JSON file not found: {labels_json}")

    with labels_json.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected the JSON root to be a list of label trees.")

    mapping: dict[str, int] = {}
    conflicts: list[str] = []

    for tree in data:
        labels = tree.get("labels", []) if isinstance(tree, dict) else []
        for label in labels:
            name = label.get("name")
            label_id = label.get("id")
            if name is None or label_id is None:
                continue
            if name in mapping and mapping[name] != label_id:
                conflicts.append(f"{name}: {mapping[name]} vs {label_id}")
            mapping[name] = label_id

    if conflicts:
        print(
            "Warning: conflicting IDs found for some label names:\n"
            + "\n".join(conflicts[:10])
            + ("\n..." if len(conflicts) > 10 else ""),
            file=sys.stderr,
        )

    return mapping


def convert_csv(
    input_csv: Path,
    output_path: Path,
    mapping: dict[str, int],
    strict: bool,
    missing_report: Path | None = None,
) -> None:
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV file not found: {input_csv}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    missing_counts: dict[str, int] = {}

    with input_csv.open("r", newline="", encoding="utf-8") as in_f:
        reader = csv.DictReader(in_f)
        if reader.fieldnames is None:
            raise ValueError("Input CSV file is missing a header row.")
        if "label_name" not in reader.fieldnames:
            raise ValueError("Input CSV is missing the 'label_name' column.")

        fieldnames = [
            "label_id" if name == "label_name" else name
            for name in reader.fieldnames
        ]

        with output_path.open("w", newline="", encoding="utf-8") as out_f:
            writer = csv.DictWriter(out_f, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                label_name = row.pop("label_name")
                if label_name in mapping:
                    row["label_id"] = str(mapping[label_name])
                else:
                    missing_counts[label_name] = missing_counts.get(label_name, 0) + 1
                    row["label_id"] = label_name
                writer.writerow(row)

    if missing_counts and missing_report is not None:
        missing_report.parent.mkdir(parents=True, exist_ok=True)
        with missing_report.open("w", newline="", encoding="utf-8") as report_f:
            writer = csv.writer(report_f)
            writer.writerow(["label_name", "count"])
            for label_name in sorted(missing_counts):
                writer.writerow([label_name, missing_counts[label_name]])

    if missing_counts:
        message = (
            f"Missing {len(missing_counts)} label_name value(s) in mapping."
            " Keeping original label_name in label_id column."
        )
        if strict:
            raise ValueError(message)
        print(message, file=sys.stderr)


def main() -> None:
    """Converts CSV using mapping; reports missing labels"""
    args = parse_args()

    output_dir = args.output_dir or args.input_csv.parent
    output_path = output_dir / args.output_name

    mapping = build_label_mapping(args.labels_json)
    if args.missing_report_path is not None:
        missing_report = args.missing_report_path
    elif args.missing_report:
        missing_report = output_path.with_name(
            f"{output_path.stem}_missing_labels.csv"
        )
    else:
        missing_report = None

    convert_csv(
        args.input_csv,
        output_path,
        mapping,
        args.strict,
        missing_report=missing_report,
    )

    print(f"Wrote converted CSV to {output_path}")


if __name__ == "__main__":
    main()

# ########################################################60
# Usage examples as a command line in a terminal

# python computer_vision/label_names_to_ids_csv.py /path/to/label_trees.json /path/to/image_annotation_labels_names.csv --missing-report
# python computer_vision/label_names_to_ids_csv.py /path/to/label_trees.json /path/to/image_annotation_labels_names.csv --missing-report /path/to/missing_labels.csv
# python computer_vision/label_names_to_ids_csv.py /path/to/label_trees.json /path/to/image_annotation_labels_names.csv --output-name image_annotation_labels.csv --output-dir /path/to/out