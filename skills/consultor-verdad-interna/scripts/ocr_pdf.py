"""OCR de PDFs escaneados -> .txt (uso: python ocr_pdf.py salida_dir pdf1 pdf2 ...)"""
import sys, os
import pymupdf
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
out_dir = sys.argv[1]
for pdf in sys.argv[2:]:
    name = os.path.splitext(os.path.basename(pdf))[0]
    doc = pymupdf.open(pdf)
    parts = []
    for i, page in enumerate(doc):
        png = page.get_pixmap(dpi=200).tobytes("png")
        result, _ = engine(png)
        lines = [r[1] for r in (result or [])]
        parts.append(f"\n--- Página {i + 1} ---\n" + "\n".join(lines))
        print(f"{name}: {i + 1}/{len(doc)}", flush=True)
    with open(os.path.join(out_dir, name + ".txt"), "w", encoding="utf-8") as f:
        f.write("".join(parts))
