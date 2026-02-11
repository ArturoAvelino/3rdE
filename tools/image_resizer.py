from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image


DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 853
DEFAULT_DPI = 350
DEFAULT_JPEG_QUALITY = 85


def _target_size(
    original: Tuple[int, int],
    width: Optional[int],
    height: Optional[int],
    keep_aspect: bool,
) -> Tuple[int, int]:
    orig_w, orig_h = original
    if width is None and height is None:
        width, height = DEFAULT_WIDTH, DEFAULT_HEIGHT

    if keep_aspect:
        if width is not None and height is not None:
            # Prefer width; recompute height to preserve aspect ratio.
            height = int(round(width * orig_h / orig_w))
        elif width is not None:
            height = int(round(width * orig_h / orig_w))
        else:
            width = int(round(height * orig_w / orig_h))
    else:
        if width is None or height is None:
            raise ValueError("Both width and height are required when keep_aspect is False.")

    return int(width), int(height)


def reduce_image(
    input_path: str | Path,
    output_path: str | Path,
    *,
    width: Optional[int] = DEFAULT_WIDTH,
    height: Optional[int] = DEFAULT_HEIGHT,
    dpi: Optional[int] = DEFAULT_DPI,
    keep_aspect: bool = True,
    jpeg_quality: Optional[int] = None,
    optimize: bool = False,
) -> Tuple[int, int]:
    """
    Resize an image to reduce file size while preserving color profile and DPI.
    Returns the (width, height) of the saved image.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    with Image.open(input_path) as img:
        target_w, target_h = _target_size(img.size, width, height, keep_aspect)
        resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        save_kwargs = {}
        icc_profile = img.info.get("icc_profile")
        if icc_profile:
            save_kwargs["icc_profile"] = icc_profile
        exif = img.info.get("exif")
        if exif:
            save_kwargs["exif"] = exif

        if dpi is None:
            dpi_value = img.info.get("dpi", (DEFAULT_DPI, DEFAULT_DPI))
            dpi = int(dpi_value[0]) if isinstance(dpi_value, tuple) else int(dpi_value)
        save_kwargs["dpi"] = (int(dpi), int(dpi))

        out_suffix = output_path.suffix.lower()
        is_jpeg = out_suffix in {".jpg", ".jpeg"} or img.format == "JPEG"
        if is_jpeg and jpeg_quality is not None:
            save_kwargs["quality"] = int(jpeg_quality)
        if is_jpeg and optimize:
            save_kwargs["optimize"] = True

        resized.save(output_path, **save_kwargs)
        return target_w, target_h


def reduce_folder(
    input_dir: str | Path,
    output_dir: str | Path,
    *,
    width: Optional[int] = DEFAULT_WIDTH,
    height: Optional[int] = DEFAULT_HEIGHT,
    dpi: Optional[int] = DEFAULT_DPI,
    keep_aspect: bool = True,
    jpeg_quality: Optional[int] = None,
    optimize: bool = False,
    recursive: bool = True,
) -> Tuple[int, int, int]:
    """
    Resize all images in a folder (optionally including subfolders).
    Returns (processed, skipped, failed).
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_exts = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".gif", ".webp"}
    entries = input_dir.rglob("*") if recursive else input_dir.glob("*")

    processed = 0
    skipped = 0
    failed = 0
    for path in entries:
        if not path.is_file():
            continue
        if path.suffix.lower() not in image_exts:
            skipped += 1
            continue
        rel_path = path.relative_to(input_dir)
        out_path = output_dir / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            reduce_image(
                path,
                out_path,
                width=width,
                height=height,
                dpi=dpi,
                keep_aspect=keep_aspect,
                jpeg_quality=jpeg_quality,
                optimize=optimize,
            )
            processed += 1
        except OSError:
            failed += 1
    return processed, skipped, failed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reduce image size by resizing while preserving DPI and ICC profile."
    )
    parser.add_argument("input_path", help="Path to the source image.")
    parser.add_argument("output_path", help="Path to the resized image.")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI)
    parser.add_argument("--jpeg-quality", type=int, default=None)
    parser.add_argument("--optimize", action="store_true", default=False)
    parser.add_argument(
        "--keep-aspect",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Preserve the original aspect ratio (default: True).",
    )
    parser.add_argument(
        "--recursive",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include subfolders when input_path is a directory (default: True).",
    )

    args = parser.parse_args()
    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    if input_path.is_dir():
        reduce_folder(
            input_path,
            output_path,
            width=args.width,
            height=args.height,
            dpi=args.dpi,
            keep_aspect=args.keep_aspect,
            jpeg_quality=args.jpeg_quality,
            optimize=args.optimize,
            recursive=args.recursive,
        )
    else:
        reduce_image(
            input_path,
            output_path,
            width=args.width,
            height=args.height,
            dpi=args.dpi,
            keep_aspect=args.keep_aspect,
            jpeg_quality=args.jpeg_quality,
            optimize=args.optimize,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
