import os
import sys
import subprocess
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# 🚀 OCR processing script with Kraken (segmentation + recognition)
# Uses a segmentation model (-i) and a recognition model (-m)
# ─────────────────────────────────────────────────────────────

# ─── Path configuration ───────────────────────────────────────
if len(sys.argv) != 6:
    print("❌ Usage: python kraken_batch.py <images_dir> <output_dir> <recognition_model_path> <segmentation_model_path> <output_format>")
    sys.exit(1)

images_dir = Path(sys.argv[1])
output_dir = Path(sys.argv[2])
model_seg_path = sys.argv[3]
model_atr_path = sys.argv[4]
output_format = sys.argv[5]

# ─── Initial checks ───────────────────────────────────────────
if not images_dir.exists() or not images_dir.is_dir():
    print(f"❌ Image folder not found: {images_dir}")
    sys.exit(1)

if not Path(model_atr_path).exists():
    print(f"❌ Recognition model not found: {model_atr_path}")
    sys.exit(1)

if not Path(model_seg_path).exists():
    print(f"❌ Segmentation model not found: {model_seg_path}")
    sys.exit(1)

# ─── Create output folder ─────────────────────────────────────
output_dir.mkdir(parents=True, exist_ok=True)
print(f"📁 Output folder created: {output_dir}")

# ─── OCR processing image by image ────────────────────────────
image_files = sorted([f for f in images_dir.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".tif", ".tiff"]])
if not image_files:
    print(f"⚠️  No images files found in {images_dir}")
    sys.exit(0)

print(f"🚀 Starting OCR processing with Kraken - {len(image_files)} images")

success_count = 0
error_count = 0

for img_path in image_files:
    print(f"   ⏳ Processing {img_path}")
    if sys.argv[5] == "-n":
        out_txt = output_dir / f"{img_path.stem}.txt"
    else:
        out_txt = output_dir / f"{img_path.stem}.xml"

    try:
        result = subprocess.run([
            "kraken",
            "-i", str(img_path),
            str(out_txt),
            output_format,
            "binarize",
            "segment",
            "-bl",
            "-i", model_seg_path,
            "ocr",
            "-m", model_atr_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"   ❌ Kraken error: {result.stderr.strip()}")
            error_count += 1
        else:
            success_count += 1

    except Exception as e:
        print(f"   ❌ Exception during processing: {str(e)}")
        error_count += 1

print(f"✅ Processing completed")
