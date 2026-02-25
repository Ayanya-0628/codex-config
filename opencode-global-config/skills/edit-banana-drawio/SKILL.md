---
name: edit-banana-drawio
description: Convert a NanoBanana/LLM-generated diagram image (PNG/JPG/WebP) or PDF pages into an editable draw.io (mxGraph) .drawio.xml file using the Edit-Banana pipeline locally (no API by default). Use when the user sends a diagram screenshot/PDF and asks to "make it editable", "convert to drawio", or "turn this into editable shapes/arrows/text boxes", and you can run local scripts. Also use to generate a fallback draw.io file that embeds the original image when the ML pipeline is unavailable.
---

# Edit Banana Drawio

## Workflow

### 1) Choose a conversion mode

- Prefer **local Edit-Banana reconstruction** (editable shapes/arrows; optional editable text) when SAM3 weights and runtime are available.
- Use **fallback embed** (editable as a movable/resizable image) when the ML pipeline cannot run (missing weights/GPU/deps).

### 2) Run conversion

- Run `python C:/Users/16342/.codex/skills/edit-banana-drawio/scripts/convert_to_drawio.py --input <path> --output-dir <dir>`
- For PDFs: the script renders pages (requires `pymupdf`) and converts each page separately.

### 3) Hand off results

- Return the output `.drawio.xml` path(s).
- Tell the user to open the file in `draw.io / diagrams.net` (File → Import / Open) to edit.

## Local prerequisites (Edit-Banana mode)

- Clone the repo somewhere (example already present in this workspace): `c:/Users/16342/Documents/BaiduSyncdisk/APP/技术路线图绘制/_tmp/Edit-Banana`
- Create `config/config.yaml` in the repo (copy from `config/config.yaml.example`) and set `sam3.checkpoint_path` to your weights.
- If you need editable text boxes, enable OCR separately (not required by default).

## Notes on “editability”

- “Editable” here means the output is reconstructed as **draw.io objects** (mxCells) rather than a flat bitmap.
- Without OCR, shapes/arrows can still be editable; text may be missing or end up as part of fallback image regions.

## Script

- `scripts/convert_to_drawio.py`: converts image/PDF into `.drawio.xml` via Edit-Banana when available; otherwise outputs a fallback draw.io file embedding the original image.
