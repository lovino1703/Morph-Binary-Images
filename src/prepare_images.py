"""Script to binarise user-prepared raw images with Otsu and log sources."""

import os
import sys
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.io_utils import binarize_otsu, save_binary

IMAGES_DIR = "images"
RAW_DIR = os.path.join(IMAGES_DIR, "raw")

# =====================================================================
# ĐIỀN ĐÚNG TÊN 4 FILE ẢNH CỦA BẠN TRONG THƯ MỤC images/raw/ VÀO ĐÂY:
# =====================================================================
MY_RAW_FILES = {
    "synthetic": "synthetic_shapes_raw.jpg",  
    "noisy": "noisy_image_raw.png",          
    "text_scan": "text_scan_raw.tif",  
    "fingerprint": "fingerprint_raw.tif",   
}


def main():
    # Cấu hình: (Tên ảnh xuất ra, Tên ảnh gốc trong raw/, Phân loại, Đảo màu invert, Mô tả mục đích)
    # Lưu ý: Đặt invert=True nếu vật thể/chữ có màu ĐEN trên nền TRẮNG. Đặt False nếu vật thể TRẮNG trên nền ĐEN.
    tasks = [
        (
            "synthetic_shapes.png",
            MY_RAW_FILES["synthetic"],
            "Synthetic shapes",
            False,
            "Baseline geometric shapes to test Dilation hole-filling and Erosion bridge-breaking.",
        ),
        (
            "noisy_image.png",
            MY_RAW_FILES["noisy"],
            "Noisy image",
            False,
            "Evaluate background noise removal via Erosion and foreground hole filling via Dilation.",
        ),
        (
            "text_scan.png",
            MY_RAW_FILES["text_scan"],
            "Text scan",
            True,
            "Reconnect broken character strokes via Dilation and separate touching characters via Erosion.",
        ),
        (
            "fingerprint.png",
            MY_RAW_FILES["fingerprint"],
            "Fingerprint",
            True,
            "Denoise background speckles and bridge small gaps in fingerprint ridges.",
        ),
    ]

    log_rows = []
    print("=== CHẠY OTSU TRÊN ẢNH CỦA BẠN ===")
    for out_name, raw_filename, category, invert, purpose in tasks:
        raw_path = os.path.join(RAW_DIR, raw_filename)
        if not os.path.exists(raw_path):
            raise FileNotFoundError(
                f"Không tìm thấy file '{raw_path}'! Hãy kiểm tra lại tên file trong thư mục images/raw/."
            )

        gray = cv2.imread(raw_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise ValueError(f"Không thể đọc được ảnh: {raw_path}")

        bin_01, otsu_t = binarize_otsu(gray, invert=invert)
        out_path = os.path.join(IMAGES_DIR, out_name)
        save_binary(out_path, bin_01)

        h, w = gray.shape
        mode_str = "THRESH_BINARY_INV + OTSU" if invert else "THRESH_BINARY + OTSU"
        source_desc = f"User-prepared test image (`raw/{raw_filename}`)"

        print(f"[OK] {out_path:<26} <- raw/{raw_filename:<24} | {w}x{h} | Otsu T = {otsu_t:5.1f}")
        log_rows.append(
            (out_name, f"raw/{raw_filename}", category, f"{w}x{h}", f"{otsu_t:.1f}", mode_str, source_desc, purpose)
        )

    # Ghi file images/SOURCES.md
    sources_md_path = os.path.join(IMAGES_DIR, "SOURCES.md")
    with open(sources_md_path, "w", encoding="utf-8") as f:
        f.write("# Test Images & Otsu Binarization Log\n\n")
        f.write(
            "All test images in `images/` are binarized using **Otsu's automatic thresholding method** (`src/io_utils.py:binarize_otsu`).\n\n"
        )
        f.write(
            "| Binary Image (`images/`) | Raw Input (`images/raw/`) | Category | Resolution | Otsu Threshold ($T$) | Threshold Mode | Source / Origin | Testing Purpose |\n"
        )
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for row in log_rows:
            f.write(
                f"| `{row[0]}` | `{row[1]}` | {row[2]} | {row[3]} | `{row[4]}` | `{row[5]}` | {row[6]} | {row[7]} |\n"
            )
        f.write("\n## Reproducibility\n\n")
        f.write("```bash\npython src/prepare_images.py\n```\n")

    print(f"[+] Đã cập nhật file log: {sources_md_path}")


if __name__ == "__main__":
    main()