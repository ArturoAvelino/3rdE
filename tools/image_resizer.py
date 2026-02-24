from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Tuple, Union

from PIL import Image


DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 853
DEFAULT_DPI = 350
DEFAULT_JPEG_QUALITY = 85
DEFAULT_SUFFIX = "_resized"


def _apply_suffix(path: Path, suffix: str) -> Path:
    """Return a new path with the suffix inserted before the file extension."""
    if not suffix:
        return path
    return path.with_name(f"{path.stem}{suffix}{path.suffix}")


def _target_size(
    original: Tuple[int, int],
    width: Optional[int],
    height: Optional[int],
    keep_aspect: bool,
) -> Tuple[int, int]:
    """Compute the target size from an original size and optional overrides."""
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
    output_path: Optional[str | Path],
    *,
    width: Optional[int] = DEFAULT_WIDTH,
    height: Optional[int] = DEFAULT_HEIGHT,
    dpi: Optional[int] = DEFAULT_DPI,
    keep_aspect: bool = True,
    jpeg_quality: Optional[int] = None,
    optimize: bool = False,
    suffix: str = DEFAULT_SUFFIX,
    allow_overwrite: bool = False,
) -> Tuple[int, int]:
    """
    Resize a single image to reduce file size while preserving color profile and DPI.

    Args:
        input_path: Path to the source image.
        output_path: Path to the resized image (file) or a directory to place it in.
        width: Target width in pixels. If keep_aspect=True, height is recomputed.
        height: Target height in pixels. If keep_aspect=True, width is recomputed.
        dpi: Output DPI. If None, preserve source DPI or default to 350.
        keep_aspect: Preserve the original aspect ratio when True.
        jpeg_quality: JPEG quality (1-95). Only applies to JPEG outputs.
        optimize: Enable JPEG optimizer if True.
        suffix: Filename suffix used when output_path is a directory or None.
        allow_overwrite: Allow overwriting the target file if it exists.

    Returns:
        (width, height) of the saved image.
    """
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path is not None else None

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

        if output_path is None or output_path.is_dir():
            target_dir = output_path if output_path is not None else input_path.parent
            target_path = _apply_suffix(target_dir / input_path.name, suffix)
        else:
            target_path = output_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if target_path.exists() and not allow_overwrite:
            raise FileExistsError(f"Refusing to overwrite existing file: {target_path}")

        out_suffix = target_path.suffix.lower()
        is_jpeg = out_suffix in {".jpg", ".jpeg"} or img.format == "JPEG"
        if is_jpeg and jpeg_quality is not None:
            save_kwargs["quality"] = int(jpeg_quality)
        if is_jpeg and optimize:
            save_kwargs["optimize"] = True

        resized.save(target_path, **save_kwargs)
        return target_w, target_h


def reduce_folder(
    input_dir: str | Path,
    output_dir: Optional[str | Path],
    *,
    width: Optional[int] = DEFAULT_WIDTH,
    height: Optional[int] = DEFAULT_HEIGHT,
    dpi: Optional[int] = DEFAULT_DPI,
    keep_aspect: bool = True,
    jpeg_quality: Optional[int] = None,
    optimize: bool = False,
    recursive: bool = True,
    log_filename: str = "resize_log.txt",
    suffix: str = DEFAULT_SUFFIX,
    allow_overwrite: bool = False,
) -> Tuple[int, int, int, Path]:
    """
    Resize all images in a folder (optionally including subfolders).

    Args:
        input_dir: Folder containing source images.
        output_dir: Folder to write resized images into (mirrors subfolders).
            If None, writes next to the originals using the suffix.
        width: Target width in pixels. If keep_aspect=True, height is recomputed.
        height: Target height in pixels. If keep_aspect=True, width is recomputed.
        dpi: Output DPI. If None, preserve source DPI or default to 350.
        keep_aspect: Preserve the original aspect ratio when True.
        jpeg_quality: JPEG quality (1-95). Only applies to JPEG outputs.
        optimize: Enable JPEG optimizer if True.
        recursive: Include subfolders when True.
        log_filename: Log file name created under output_dir.
        suffix: Filename suffix used when output_dir is None or same as input_dir.
        allow_overwrite: Allow overwriting existing files in output_dir.

    Returns:
        (processed, skipped, failed, log_path).
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir) if output_dir is not None else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    image_exts = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".gif", ".webp"}
    entries = input_dir.rglob("*") if recursive else input_dir.glob("*")

    processed = 0
    skipped = 0
    failed = 0
    log_lines = [
        "Input settings:",
        "",
        f"- input_path={input_dir!s}",
        f"- output_path={output_dir!s}",
        f"- width={width!r}",
        f"- height={height!r}",
        f"- dpi={dpi!r}",
        f"- jpeg_quality={jpeg_quality!r}",
        f"- optimize={optimize!r}",
        f"- recursive={recursive!r}",
        f"- log_filename={log_filename!r}",
        f"- suffix={suffix!r}",
        f"- allow_overwrite={allow_overwrite!r}",
        "",
        "Files:",
    ]
    for path in entries:
        if not path.is_file():
            continue
        if path.suffix.lower() not in image_exts:
            skipped += 1
            continue
        rel_path = path.relative_to(input_dir)
        out_path = output_dir / rel_path
        if output_dir.resolve() == input_dir.resolve():
            out_path = _apply_suffix(out_path, suffix)
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
                suffix=suffix,
                allow_overwrite=allow_overwrite,
            )
            processed += 1
            log_lines.append(f"OK {rel_path}")
        except (OSError, FileExistsError) as exc:
            failed += 1
            log_lines.append(f"FAILED {rel_path} ({exc})")
    log_lines.append("")
    log_lines.append(f"processed={processed}")
    log_lines.append(f"skipped={skipped}")
    log_lines.append(f"failed={failed}")
    log_path = output_dir / log_filename
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    return processed, skipped, failed, log_path


def resize_path(
    input_path: str | Path,
    output_path: Optional[str | Path],
    *,
    width: Optional[int] = DEFAULT_WIDTH,
    height: Optional[int] = DEFAULT_HEIGHT,
    dpi: Optional[int] = DEFAULT_DPI,
    keep_aspect: bool = True,
    jpeg_quality: Optional[int] = None,
    optimize: bool = False,
    recursive: bool = True,
    log_filename: str = "resize_log.txt",
    suffix: str = DEFAULT_SUFFIX,
    allow_overwrite: bool = False,
) -> Union[Tuple[int, int], Tuple[int, int, int, Path]]:
    """
    Resize a file or a folder depending on input_path.

    Args:
        input_path: File or folder to resize.
        output_path: Output file path or output folder path. If None, writes next to input.
        width: Target width in pixels. If keep_aspect=True, height is recomputed.
        height: Target height in pixels. If keep_aspect=True, width is recomputed.
        dpi: Output DPI. If None, preserve source DPI or default to 350.
        keep_aspect: Preserve the original aspect ratio when True.
        jpeg_quality: JPEG quality (1-95). Only applies to JPEG outputs.
        optimize: Enable JPEG optimizer if True.
        recursive: Include subfolders when input_path is a directory.
        log_filename: Log file name created under output_path (folder mode only).
        suffix: Filename suffix used when output_path is None or a directory.
        allow_overwrite: Allow overwriting target files if they exist.

    Returns:
        (width, height) for single-image mode, or (processed, skipped, failed, log_path)
        for folder mode.
    """
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path is not None else None
    if input_path.is_dir():
        return reduce_folder(
            input_path,
            output_path,
            width=width,
            height=height,
            dpi=dpi,
            keep_aspect=keep_aspect,
            jpeg_quality=jpeg_quality,
            optimize=optimize,
            recursive=recursive,
            log_filename=log_filename,
            suffix=suffix,
            allow_overwrite=allow_overwrite,
        )
    return reduce_image(
        input_path,
        output_path,
        width=width,
        height=height,
        dpi=dpi,
        keep_aspect=keep_aspect,
        jpeg_quality=jpeg_quality,
        optimize=optimize,
        suffix=suffix,
        allow_overwrite=allow_overwrite,
    )


def main() -> int:
    """Parse CLI arguments and run resize_path()."""
    parser = argparse.ArgumentParser(
        description="Reduce image size by resizing while preserving DPI and ICC profile."
    )
    parser.add_argument("input_path", help="Path to the source image or folder.")
    parser.add_argument(
        "output_path",
        nargs="?",
        default=None,
        help="Path to the resized image or output folder (default: next to input).",
    )
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
    parser.add_argument(
        "--log-filename",
        default="resize_log.txt",
        help="Log filename written under output_path when input_path is a directory.",
    )
    parser.add_argument(
        "--suffix",
        default=DEFAULT_SUFFIX,
        help="Filename suffix for resized images (default: _resized). Use empty string to keep names.",
    )
    parser.add_argument(
        "--allow-overwrite",
        action="store_true",
        default=False,
        help="Allow overwriting existing output files.",
    )

    args = parser.parse_args()
    resize_path(
        args.input_path,
        args.output_path,
        width=args.width,
        height=args.height,
        dpi=args.dpi,
        keep_aspect=args.keep_aspect,
        jpeg_quality=args.jpeg_quality,
        optimize=args.optimize,
        recursive=args.recursive,
        log_filename=args.log_filename,
        suffix=args.suffix,
        allow_overwrite=args.allow_overwrite,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# ########################################################60
# Example of usage

# from tools.image_resizer import resize_path
#

# # It can call a single function regardless of whether you pass a
# # file or a folder:
# result = resize_path(
#     input_path="/path/to/images",
#     output_path="/path/to/output",
#     width=1280,
#     height=853,
#     dpi=350,
#     jpeg_quality=80,
#     optimize=True,
#     recursive=True,
#     log_filename="resize_log.txt",
#     suffix="_resized",
# )

# # If you pass a single image path, the same call returns (width,
# # height) of the saved image:
# result = resize_path(
#     input_path="/path/to/image.jpg",
#     output_path=None,  # saves next to input with suffix
#     jpeg_quality=85,
#     optimize=True,
#     suffix="_resized",
# )
# new_w, new_h = result

# --------------------------------------------------------60
# # Other examples

# from tools.image_resizer import reduce_image, reduce_folder

# reduce_image("input.jpg", None, jpeg_quality=80, optimize=True, suffix="_resized")
# reduce_folder("images", None, jpeg_quality=75, optimize=True, recursive=True)

# --------------------------------------------------------60
# # Examples of using the function as command line in a terminal

# python tools/image_resizer.py input.jpg --jpeg-quality 80 --optimize
# python tools/image_resizer.py /path/in /path/out --jpeg-quality 75 --optimize
# python tools/image_resizer.py /path/in /path/out --no-recursive

# python tools/image_resizer.py input.jpg
# python tools/image_resizer.py input.jpg --width 1600 --dpi 300
# python tools/image_resizer.py input.jpg --height 1000
