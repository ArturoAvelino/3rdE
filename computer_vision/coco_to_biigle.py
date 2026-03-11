import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple


logger = logging.getLogger(__name__)


class COCOJSON_to_BiigleCSV:
    """
    Convert a directory of per-image COCO-style JSON files into Biigle CSV files.

    Input expectation (per JSON file):
      - images: list with at least one entry containing "file_name" and "date_captured"
      - annotations: list of one or more entries containing "id", "image_id",
        "category_id", and "segmentation"

    Output mapping:
      - image_annotations.csv:
        id <- annotations.id
        image_id <- annotations.image_id
        shape_id <- 3
        created_at <- images.date_captured
        updated_at <- images.date_captured
        points <- annotations.segmentation (first polygon list)
      - image_annotation_labels.csv:
        annotation_id <- annotations.id
        label_id <- annotations.category_id
        user_id <- configurable
        confidence <- configurable
        created_at <- images.date_captured
        updated_at <- images.date_captured
      - images.csv:
        id <- annotations.image_id
        filename <- images.file_name
        volume_id <- configurable
    """

    def __init__(
        self,
        json_dir: str,
        output_dir: str,
        json_glob: str = "*.json",
        user_id: int = 5,
        confidence: float = 0.2,
        volume_id: int = 1,
    ) -> None:
        self.json_dir = Path(json_dir)
        self.output_dir = Path(output_dir)
        self.json_glob = json_glob
        self.user_id = user_id
        self.confidence = confidence
        self.volume_id = volume_id

    def _load_json(self, json_path: Path) -> dict:
        with json_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _extract_points(segmentation: List) -> List[float]:
        if not segmentation:
            return []
        if isinstance(segmentation[0], list):
            return segmentation[0]
        return segmentation

    def _collect_rows(
        self,
    ) -> Tuple[List[Tuple], List[Tuple], Dict[int, Tuple[int, str, int]]]:
        annotations_rows: List[Tuple] = []
        labels_rows: List[Tuple] = []
        images_rows: Dict[int, Tuple[int, str, int]] = {}

        patterns = {self.json_glob, self.json_glob.replace(".json", ".JSON"), self.json_glob.replace(".JSON", ".json")}
        json_files: List[Path] = []
        for pattern in sorted(patterns):
            json_files.extend(self.json_dir.glob(pattern))
        json_files = sorted(set(json_files), key=lambda p: str(p))
        if not json_files:
            patterns_hint = ", ".join(sorted(patterns))
            raise FileNotFoundError(
                f"No JSON files found in {self.json_dir} with patterns {patterns_hint}"
            )

        for json_path in json_files:
            data = self._load_json(json_path)

            images = data.get("images", [])
            annotations = data.get("annotations", [])
            if not images or not annotations:
                logger.warning("Skipping %s (missing images or annotations)", json_path.name)
                continue

            image = images[0]
            if len(images) > 1:
                logger.warning("Using first image entry in %s (found %d)", json_path.name, len(images))

            if len(annotations) > 1:
                logger.warning("Using all annotations in %s (found %d)", json_path.name, len(annotations))

            for ann in annotations:
                ann_id = ann.get("id")
                image_id = ann.get("image_id")
                category_id = ann.get("category_id")
                date_captured = image.get("date_captured")
                points = self._extract_points(ann.get("segmentation", []))

                annotations_rows.append(
                    (
                        ann_id,
                        image_id,
                        3,
                        date_captured,
                        date_captured,
                        json.dumps(points),
                    )
                )

                labels_rows.append(
                    (
                        ann_id,
                        category_id,
                        self.user_id,
                        self.confidence,
                        date_captured,
                        date_captured,
                    )
                )

                image_filename = image.get("file_name")
                if image_id in images_rows and images_rows[image_id][1] != image_filename:
                    logger.warning(
                        "Image id %s has multiple filenames (%s vs %s); keeping first",
                        image_id,
                        images_rows[image_id][1],
                        image_filename,
                    )
                images_rows.setdefault(image_id, (image_id, image_filename, self.volume_id))

        return annotations_rows, labels_rows, images_rows

    def _write_static_files(self) -> List[Path]:
        template_dir = Path(__file__).resolve().parent / "biigle_templates"
        template_files = [
            "video_annotation_labels.csv",
            "video_annotations.csv",
            "users.json",
            "volumes.json",
            "label_trees.json",
            "video_labels.csv",
            "image_labels.csv",
            "videos.csv",
        ]
        written: List[Path] = []
        for filename in template_files:
            source_path = template_dir / filename
            if not source_path.exists():
                raise FileNotFoundError(f"Missing template file: {source_path}")
            target_path = self.output_dir / filename
            target_path.write_bytes(source_path.read_bytes())
            written.append(target_path)
        return written

    def write_csv_files(self) -> Tuple[Path, Path, Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        annotations_rows, labels_rows, images_rows = self._collect_rows()

        annotations_csv = self.output_dir / "image_annotations.csv"
        labels_csv = self.output_dir / "image_annotation_labels.csv"
        images_csv = self.output_dir / "images.csv"

        with annotations_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
            writer.writerow(["id", "image_id", "shape_id", "created_at", "updated_at", "points"])
            writer.writerows(annotations_rows)

        with labels_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
            writer.writerow(["annotation_id", "label_id", "user_id", "confidence", "created_at", "updated_at"])
            writer.writerows(labels_rows)

        with images_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            writer.writerow(["id", "filename", "volume_id"])
            writer.writerows(images_rows.values())

        self._write_static_files()

        return annotations_csv, labels_csv, images_csv


def coco_to_biiggle(
    json_dir: str,
    output_dir: str,
    json_glob: str = "*.json",
    user_id: int = 5,
    confidence: float = 0.2,
    volume_id: int = 1,
) -> Tuple[Path, Path, Path]:
    """
    Convert a directory of COCO-style JSON files into Biigle CSV files.

    Args:
        json_dir: Directory containing COCO-style JSON files.
        output_dir: Directory where CSV files will be written.
        json_glob: Glob pattern used to select JSON files.
        user_id: Value written to image_annotation_labels.csv "user_id" column.
        confidence: Value written to image_annotation_labels.csv "confidence" column.
        volume_id: Value written to images.csv "volume_id" column.

    Returns:
        Tuple with paths to (image_annotations.csv, image_annotation_labels.csv, images.csv).
    """
    converter = COCOJSON_to_BiigleCSV(
        json_dir=json_dir,
        output_dir=output_dir,
        json_glob=json_glob,
        user_id=user_id,
        confidence=confidence,
        volume_id=volume_id,
    )
    return converter.write_csv_files()


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Convert per-image COCO-style JSON files into Biigle CSV files."
    )
    parser.add_argument("--json-dir", required=True, help="Directory containing COCO JSON files.")
    parser.add_argument("--out-dir", required=True, help="Directory to write CSV output files.")
    parser.add_argument(
        "--json-glob",
        default="*.json",
        help="Glob pattern for JSON files (default: *.json; also matches *.JSON).",
    )
    parser.add_argument("--user-id", type=int, default=5, help="Value for user_id column.")
    parser.add_argument("--confidence", type=float, default=0.2, help="Value for confidence column.")
    parser.add_argument("--volume-id", type=int, default=1, help="Value for volume_id column.")

    args = parser.parse_args()

    coco_to_biiggle(
        json_dir=args.json_dir,
        output_dir=args.out_dir,
        json_glob=args.json_glob,
        user_id=args.user_id,
        confidence=args.confidence,
        volume_id=args.volume_id,
    )
