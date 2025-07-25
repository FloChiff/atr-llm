import os
import sys
import subprocess
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# 🚀 Script de traitement OCR avec Kraken (segmentation + reco)
# Utilise un modèle de segmentation (-i) et un modèle de reconnaissance (-m)
# ─────────────────────────────────────────────────────────────

# ─── Configuration des chemins ────────────────────────────────
if len(sys.argv) != 5:
    print("❌ Usage: python kraken_batch.py <images_dir> <output_dir> <model_atr_path> <model_seg_path>")
    sys.exit(1)

images_dir = Path(sys.argv[1])
output_dir = Path(sys.argv[2])
model_atr_path = sys.argv[3]
model_seg_path = sys.argv[4]

# ─── Vérifications initiales ─────────────────────────────────
if not images_dir.exists() or not images_dir.is_dir():
    print(f"❌ Dossier d'images introuvable : {images_dir}")
    sys.exit(1)

if not Path(model_atr_path).exists():
    print(f"❌ Modèle de reconnaissance introuvable : {model_atr_path}")
    sys.exit(1)

if not Path(model_seg_path).exists():
    print(f"❌ Modèle de segmentation introuvable : {model_seg_path}")
    sys.exit(1)

# ─── Création du dossier de sortie ───────────────────────────
output_dir.mkdir(parents=True, exist_ok=True)
print(f"📁 Dossier de sortie créé : {output_dir}")

# ─── Traitement OCR image par image ──────────────────────────
image_files = sorted([f for f in images_dir.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".tif", ".tiff"]])
if not image_files:
    print(f"⚠️  Aucun fichier .jpg trouvé dans {images_dir}")
    sys.exit(0)

print(f"🚀 Début du traitement OCR avec Kraken - {len(image_files)} images")

success_count = 0
error_count = 0

for img_path in image_files:
    out_txt = output_dir / f"{img_path.stem}.txt"

    try:
        result = subprocess.run([
            "kraken",
            "-i", str(img_path),
            str(out_txt),
            "binarize",
            "segment",
            "-bl",
            "-i", model_seg_path,
            "ocr",
            "-m", model_atr_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"   ❌ Erreur Kraken : {result.stderr.strip()}")
            error_count += 1
        else:
            success_count += 1

    except Exception as e:
        print(f"   ❌ Exception lors du traitement : {str(e)}")
        error_count += 1

print(f"✅ Traitement terminé")
