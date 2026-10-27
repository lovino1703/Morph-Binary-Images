"""Helpers for loading, binarizing and saving images."""

import cv2
import numpy as np


def binarize_otsu(
    gray: np.ndarray, invert: bool = False
) -> tuple[np.ndarray, float]:
    """Binarize a grayscale image to {0, 1} (uint8) using Otsu's thresholding.

    Returns:
        binary_img: np.ndarray of shape (H, W) with values in {0, 1} (uint8).
        otsu_thresh: float, the optimal threshold value computed by Otsu.
    """
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    otsu_thresh, binary_255 = cv2.threshold(
        gray, 0, 255, thresh_type + cv2.THRESH_OTSU
    )
    binary_01 = (binary_255 > 0).astype(np.uint8)
    return binary_01, float(otsu_thresh)


def load_binary(
    path: str,
    threshold: int | None = 127,
    use_otsu: bool = False,
    invert: bool = False,
) -> np.ndarray:
    """Load an image as grayscale and binarize to {0, 1} (uint8).

    If use_otsu=True or threshold is None, Otsu's method is used.
    Otherwise, a fixed threshold (default 127) is applied.
    """
    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise FileNotFoundError(path)

    if use_otsu or threshold is None:
        binary_01, _ = binarize_otsu(gray, invert=invert)
        return binary_01

    if invert:
        return (gray <= threshold).astype(np.uint8)
    return (gray > threshold).astype(np.uint8)


def save_binary(path: str, img: np.ndarray) -> None:
    """Save a {0, 1} image as a 0/255 PNG."""
    cv2.imwrite(path, (img * 255).astype(np.uint8))