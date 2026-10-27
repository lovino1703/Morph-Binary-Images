# Test Images & Otsu Binarization Log

All test images in `images/` are binarized using **Otsu's automatic thresholding method** (`src/io_utils.py:binarize_otsu`).

| Binary Image (`images/`) | Raw Input (`images/raw/`) | Category | Resolution | Otsu Threshold ($T$) | Threshold Mode | Source / Origin | Testing Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `synthetic_shapes.png` | `raw/synthetic_shapes_raw.jpg` | Synthetic shapes | 604x784 | `131.0` | `THRESH_BINARY + OTSU` | User-prepared test image (`raw/synthetic_shapes_raw.jpg`) | Baseline geometric shapes to test Dilation hole-filling and Erosion bridge-breaking. |
| `noisy_image.png` | `raw/noisy_image_raw.png` | Noisy image | 498x638 | `134.0` | `THRESH_BINARY + OTSU` | User-prepared test image (`raw/noisy_image_raw.png`) | Evaluate background noise removal via Erosion and foreground hole filling via Dilation. |
| `text_scan.png` | `raw/text_scan_raw.tif` | Text scan | 508x444 | `0.0` | `THRESH_BINARY_INV + OTSU` | User-prepared test image (`raw/text_scan_raw.tif`) | Reconnect broken character strokes via Dilation and separate touching characters via Erosion. |
| `fingerprint.png` | `raw/fingerprint_raw.tif` | Fingerprint | 798x958 | `125.0` | `THRESH_BINARY_INV + OTSU` | User-prepared test image (`raw/fingerprint_raw.tif`) | Denoise background speckles and bridge small gaps in fingerprint ridges. |

## Reproducibility

```bash
python src/prepare_images.py
```
