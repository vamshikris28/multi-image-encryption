import numpy as np
import math
from PIL import Image
from scipy.stats import entropy as scipy_entropy

# ---- 1. Information Entropy ----
def image_entropy(image):
    """Calculate Shannon entropy of image"""
    hist, _ = np.histogram(image.flatten(), bins=256, range=(0, 255))
    hist = hist / np.sum(hist)
    return -np.sum([p * math.log2(p) for p in hist if p > 0])


# ---- 2. NPCR (Number of Pixel Change Rate) ----
def npcr(img1, img2):
    """Compare two images pixel-wise"""
    if img1.shape != img2.shape:
        raise ValueError("Images must have same shape for NPCR.")
    diff = np.not_equal(img1, img2)
    npcr_value = np.sum(diff) / diff.size * 100
    return npcr_value


# ---- 3. UACI (Unified Average Changing Intensity) ----
def uaci(img1, img2):
    """Measures average pixel change intensity"""
    if img1.shape != img2.shape:
        raise ValueError("Images must have same shape for UACI.")
    diff = np.abs(img1.astype(np.int16) - img2.astype(np.int16))
    uaci_value = np.sum(diff) / (255 * img1.size) * 100
    return uaci_value


# ---- 4. Correlation Coefficient ----
def correlation_coefficient(image):
    """Compute correlation of adjacent pixels (horizontal, vertical, diagonal)"""
    h, w = image.shape
    pairs = 5000  # random sample size

    x, y = np.random.randint(0, h-1, pairs), np.random.randint(0, w-1, pairs)
    horiz = [image[x[i], y[i]] for i in range(pairs)]
    vert = [image[x[i], y[i]+1] for i in range(pairs)]
    diag = [image[x[i]+1, y[i]+1] for i in range(pairs)]

    def corr(a, b):
        a, b = np.array(a), np.array(b)
        return np.corrcoef(a, b)[0, 1]

    return {
        "Horizontal": corr(horiz, vert),
        "Vertical": corr(vert, diag),
        "Diagonal": corr(horiz, diag)
    }


# ---- 5. Combined Test Function ----
def evaluate_performance(original, encrypted):
    metrics = {}
    metrics["Entropy (H)"] = image_entropy(encrypted)
    metrics["NPCR (%)"] = npcr(original, encrypted)
    metrics["UACI (%)"] = uaci(original, encrypted)
    metrics.update(correlation_coefficient(encrypted))
    return metrics
