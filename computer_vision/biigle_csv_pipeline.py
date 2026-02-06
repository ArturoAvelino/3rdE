#!/usr/bin/env python3
"""Run the CSV combine + label name to ID conversion pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from combine_biigle_csv_files import combine_csv_files, find_csv_files
from label_names_to_ids_csv import build_label_mapping, convert_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Combine matching CSV files, then replace label_name with label_id."
        )
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing the CSV files to combine.",
    )
    parser.add_argument(
        "labels_json",
        type=Path,
        help="Path to the label_trees.json file.",
    )
    parser.add_argument(
        "--match-text",
        default="_for_biigle.csv",
        help="Text that CSV filenames must contain to be included.",
    )
    parser.add_argument(
        "--combined-dir",
        type=Path,
        default=None,
        help="Directory to save the combined CSV file. Defaults to input_dir.",
    )
    parser.add_argument(
        "--combined-name",
        default="image_annotation_labels_names.csv",
        help="Name of the combined CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to save the final CSV file. Defaults to combined-dir.",
    )
    parser.add_argument(
        "--output-name",
        default="image_annotation_labels.csv",
        help="Name of the final CSV file.",
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


def main() -> None:
    """Orchestrates CSV combination, conversion, and missing label reporting"""
    args = parse_args()

    combined_dir = args.combined_dir or args.input_dir
    combined_path = combined_dir / args.combined_name

    csv_files = find_csv_files(args.input_dir, args.match_text)
    csv_files = [p for p in csv_files if p.resolve() != combined_path.resolve()]

    combine_csv_files(csv_files, combined_path)

    output_dir = args.output_dir or combined_dir
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
        combined_path,
        output_path,
        mapping,
        args.strict,
        missing_report=missing_report,
    )

    print(f"Wrote combined CSV to {combined_path}")
    print(f"Wrote converted CSV to {output_path}")


if __name__ == "__main__":
    main()

# ########################################################60
# Usage examples as a command line in a terminal

# python computer_vision/biigle_csv_pipeline.py /path/to/csvs /path/to/label_trees.json
# python computer_vision/biigle_csv_pipeline.py /path/to/csvs /path/to/label_trees.json --missing-report
# python computer_vision/biigle_csv_pipeline.py /path/to/csvs /path/to/label_trees.json --missing-report /path/to/missing_labels.csv
