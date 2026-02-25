#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class OutputItem:
    input_path: Path
    output_path: Path
    mode: str  # "edit-banana" | "fallback-embed"


def _find_edit_banana_repo(explicit: str | None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))

    env = os.environ.get("EDIT_BANANA_REPO")
    if env:
        candidates.append(Path(env))

    candidates.extend(
        [
            Path.cwd() / "Edit-Banana",
            Path.cwd() / "_tmp" / "Edit-Banana",
            Path("c:/Users/16342/Documents/BaiduSyncdisk/APP/技术路线图绘制/_tmp/Edit-Banana"),
        ]
    )

    for candidate in candidates:
        try:
            if (candidate / "main.py").exists() and (candidate / "modules").exists():
                return candidate
        except Exception:
            continue
    return None


def _ensure_config_yaml(repo_root: Path) -> Path:
    cfg_dir = repo_root / "config"
    cfg = cfg_dir / "config.yaml"
    example = cfg_dir / "config.yaml.example"
    if cfg.exists():
        return cfg
    if example.exists():
        cfg_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(example, cfg)
        return cfg
    raise FileNotFoundError(f"Missing {cfg} and {example}")


def _load_image_size(image_path: Path) -> tuple[int, int]:
    from PIL import Image

    with Image.open(image_path) as img:
        w, h = img.size
    return int(w), int(h)


def _embed_image_drawio_xml(image_path: Path) -> str:
    import xml.etree.ElementTree as ET

    w, h = _load_image_size(image_path)
    ext = image_path.suffix.lower().lstrip(".")
    mime = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
        "bmp": "image/bmp",
        "tif": "image/tiff",
        "tiff": "image/tiff",
    }.get(ext, "application/octet-stream")
    payload = base64.b64encode(image_path.read_bytes()).decode("ascii")
    # mxGraph styles use ';' as a separator. A literal ';' inside the image URL
    # (like data:*;base64,...) breaks parsing, so percent-encode it.
    data_uri = f"data:{mime}%3Bbase64,{payload}"

    mxfile = ET.Element("mxfile", host="app.diagrams.net", version="1.0.0", type="device")
    diagram = ET.SubElement(mxfile, "diagram", name="Page-1", id="diagram-1")
    graph_model = ET.SubElement(
        diagram,
        "mxGraphModel",
        dx="0",
        dy="0",
        grid="1",
        gridSize="10",
        guides="1",
        tooltips="1",
        connect="1",
        arrows="1",
        fold="1",
        page="1",
        pageScale="1",
        pageWidth=str(w),
        pageHeight=str(h),
    )
    root = ET.SubElement(graph_model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    style = f"shape=image;image={data_uri};aspect=fixed;verticalLabelPosition=bottom;verticalAlign=top;"
    cell = ET.SubElement(root, "mxCell", id="2", value="", style=style, vertex="1", parent="1")
    geom = ET.SubElement(
        cell,
        "mxGeometry",
        attrib={"x": "0", "y": "0", "width": str(w), "height": str(h), "as": "geometry"},
    )
    _ = geom

    return ET.tostring(mxfile, encoding="unicode")


def _render_pdf_to_pngs(pdf_path: Path, out_dir: Path, dpi: int) -> list[Path]:
    try:
        import fitz  # type: ignore
    except Exception as e:
        raise RuntimeError("PDF input requires PyMuPDF. Install with: pip install pymupdf") from e

    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    if doc.page_count <= 0:
        return []
    scale = dpi / 72.0
    mat = fitz.Matrix(scale, scale)
    outputs: list[Path] = []
    for idx in range(doc.page_count):
        page = doc.load_page(idx)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = out_dir / f"{pdf_path.stem}_page_{idx+1:03d}.png"
        pix.save(str(out_path))
        outputs.append(out_path)
    doc.close()
    return outputs


def _run_edit_banana(repo_root: Path, input_image: Path, output_dir: Path, with_text: bool) -> Path:
    sys.path.insert(0, str(repo_root))
    try:
        from main import load_config, Pipeline  # type: ignore
    finally:
        try:
            sys.path.remove(str(repo_root))
        except ValueError:
            pass

    config = load_config()
    pipeline = Pipeline(config)
    xml_path = pipeline.process_image(
        str(input_image),
        output_dir=str(output_dir),
        with_refinement=False,
        with_text=with_text,
    )
    if not xml_path:
        raise RuntimeError("Edit-Banana pipeline returned no output path")
    out = Path(xml_path)
    if not out.exists():
        raise FileNotFoundError(f"Edit-Banana output not found: {out}")
    return out


def _iter_inputs(input_path: Path, tmp_dir: Path, dpi: int) -> Iterable[Path]:
    if input_path.suffix.lower() == ".pdf":
        yield from _render_pdf_to_pngs(input_path, tmp_dir / f"{input_path.stem}_pages", dpi=dpi)
        return
    yield input_path


def convert(input_path: Path, output_dir: Path, repo_root: Path | None, with_text: bool, pdf_dpi: int) -> list[OutputItem]:
    output_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(prefix="edit-banana-drawio-"))
    items: list[OutputItem] = []
    try:
        for image_path in _iter_inputs(input_path, tmp_dir=tmp_dir, dpi=pdf_dpi):
            if repo_root is not None:
                try:
                    _ensure_config_yaml(repo_root)
                    out = _run_edit_banana(repo_root, image_path, output_dir, with_text=with_text)
                    items.append(OutputItem(input_path=image_path, output_path=out, mode="edit-banana"))
                    continue
                except Exception:
                    pass

            fallback_name = f"{image_path.stem}.fallback.drawio.xml"
            fallback_path = output_dir / fallback_name
            fallback_path.write_text(_embed_image_drawio_xml(image_path), encoding="utf-8")
            items.append(OutputItem(input_path=image_path, output_path=fallback_path, mode="fallback-embed"))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert image/PDF to editable draw.io XML via Edit-Banana (offline).")
    parser.add_argument("--input", required=True, help="Input image/PDF path.")
    parser.add_argument("--output-dir", required=True, help="Output directory for .drawio.xml files.")
    parser.add_argument("--repo", default=None, help="Path to Edit-Banana repo (or set EDIT_BANANA_REPO).")
    parser.add_argument("--with-text", action="store_true", help="Enable text restoration (requires OCR deps/service).")
    parser.add_argument("--pdf-dpi", type=int, default=200, help="Render DPI for PDF pages (requires pymupdf).")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        return 2

    repo_root = _find_edit_banana_repo(args.repo)
    if repo_root is None:
        print("Edit-Banana repo not found; using fallback embed mode.", file=sys.stderr)
    else:
        print(f"Using Edit-Banana repo: {repo_root}", file=sys.stderr)

    results = convert(
        input_path=input_path,
        output_dir=output_dir,
        repo_root=repo_root,
        with_text=bool(args.with_text),
        pdf_dpi=int(args.pdf_dpi),
    )

    for item in results:
        print(f"{item.mode}\t{item.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
