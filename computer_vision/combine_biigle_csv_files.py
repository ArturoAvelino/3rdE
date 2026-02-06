#!/usr/bin/env python3
"""Combine CSV files that share the same header into a single CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Combine CSV files ending with a specific text into a single CSV file."
        )
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing the CSV files to combine.",
    )
    parser.add_argument(
        "--match-text",
        default="_for_biigle.csv",
        help="Text that CSV filenames must contain to be included.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Directory to save the combined CSV file. Defaults to the input directory."
        ),
    )
    parser.add_argument(
        "--output-name",
        default="image_annotation_labels_names.csv",
        help="Name of the output CSV file.",
    )
    return parser.parse_args()


def find_csv_files(input_dir: Path, match_text: str) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")

    return sorted(
        p for p in input_dir.iterdir() if p.is_file() and match_text in p.name
    )


def combine_csv_files(csv_files: list[Path], output_path: Path) -> None:
    if not csv_files:
        raise ValueError("No matching CSV files found to combine.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    header: list[str] | None = None

    with output_path.open("w", newline="", encoding="utf-8") as out_f:
        writer = csv.writer(out_f)

        for csv_path in csv_files:
            with csv_path.open("r", newline="", encoding="utf-8") as in_f:
                reader = csv.reader(in_f)
                file_header = next(reader, None)

                if file_header is None:
                    raise ValueError(f"CSV file is empty: {csv_path}")

                if header is None:
                    header = file_header
                    writer.writerow(header)
                elif file_header != header:
                    raise ValueError(
                        "CSV header mismatch in file: "
                        f"{csv_path}. Expected {header} but got {file_header}"
                    )

                for row in reader:
                    writer.writerow(row)


def main() -> None:
    """Combines matching CSV files into single output"""
    args = parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir or input_dir
    output_path = output_dir / args.output_name

    csv_files = find_csv_files(input_dir, args.match_text)
    csv_files = [p for p in csv_files if p.resolve() != output_path.resolve()]

    combine_csv_files(csv_files, output_path)

    print(f"Combined {len(csv_files)} files into {output_path}")


if __name__ == "__main__":
    main()

# ########################################################60
# Usage examples as a command line in a terminal

# python computer_vision/combine_biigle_csv_files.py /path/to/csvs --match-text "_for_biigle.csv"
# python computer_vision/combine_biigle_csv_files.py /path/to/csvs --match-text "_for_biigle.csv" --output-dir /path/to/out --output-name image_annotation_labels_names.csv
# python computer_vision/combine_biigle_csv_files.py /path/to/csvs
