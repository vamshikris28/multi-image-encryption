import numpy as np

def construct_3d_cube(images):
    """
    Stack all grayscale images into a 3D cube (H×W×N)
    """
    imgs = [np.array(img, dtype=np.uint8) for img in images]
    h, w = imgs[0].shape
    for i, im in enumerate(imgs):
        if im.shape != (h, w):
            raise ValueError(f"Image {i+1} has different shape {im.shape} from {h}x{w}")
    cube = np.stack(imgs, axis=-1)
    return cube


def cube_to_bytes(cube):
    """Flatten 3D cube to 1D byte list"""
    return cube.flatten().tolist()

def bytes_to_cube(byte_array, shape):
    """Rebuild 3D cube from byte list"""
    return np.array(byte_array, dtype=np.uint8).reshape(shape)

def extract_images_from_cube(cube_3d, reference_images):
    """
    Split a 3D cube (H x W x D) into a list of 2D images (for saving).
    Uses reference_images just to match the number of slices.
    """
    num_images = len(reference_images)
    h, w, d = cube_3d.shape

    if d < num_images:
        raise ValueError(f"Cube depth {d} < number of images {num_images}")

    extracted = []
    for i in range(num_images):
        # Extract each plane and convert back to uint8
        img = np.uint8(cube_3d[:, :, i])
        extracted.append(img)

    return extracted

def scramble_x_planes(planes: np.ndarray, chaotic_seq):
    """
    Scramble planes along X-dimension using chaotic sequence

    Args:
        planes: Input array of shape (height, width, depth)
        chaotic_seq: Chaotic sequence for generating permutation

    Returns:
        np.ndarray: Scrambled array with same shape as input
    """
    if len(chaotic_seq) < planes.shape[0]:
        raise ValueError("Chaotic sequence length must be >= height dimension")
    height, width, depth = planes.shape
    perm_indices = np.argsort(chaotic_seq[:height])
    scrambled = np.zeros_like(planes)
    for j in range(width):
        for k in range(depth):
            values = planes[:, j, k]
            scrambled[:, j, k] = values[perm_indices]
    return scrambled

def scramble_y_planes(planes: np.ndarray, chaotic_seq):
    """
    Scramble planes along Y-dimension using chaotic sequence

    Args:
        planes: Input array of shape (height, width, depth)
        chaotic_seq: Chaotic sequence for generating permutation

    Returns:
        np.ndarray: Scrambled array with same shape as input
    """
    if len(chaotic_seq) < planes.shape[1]:
        raise ValueError("Chaotic sequence length must be >= width dimension")
    height, width, depth = planes.shape
    perm_indices = np.argsort(chaotic_seq[:width])
    scrambled = np.zeros_like(planes)
    for i in range(height):
        for k in range(depth):
            values = planes[i, :, k]
            scrambled[i, :, k] = values[perm_indices]
    return scrambled

def scramble_z_planes(planes: np.ndarray, chaotic_seq):
    """
    Scramble planes along Z-dimension using chaotic sequence

    Args:
        planes: Input array of shape (height, width, depth)
        chaotic_seq: Chaotic sequence for generating permutation

    Returns:
        np.ndarray: Scrambled array with same shape as input
    """
    if len(chaotic_seq) < planes.shape[2]:
        raise ValueError("Chaotic sequence length must be >= depth dimension")
    height, width, depth = planes.shape
    perm_indices = np.argsort(chaotic_seq[:depth])
    scrambled = np.zeros_like(planes)
    for i in range(height):
        for j in range(width):
            values = planes[i, j, :]
            scrambled[i, j, :] = values[perm_indices]
    return scrambled

def reverse_scramble_x_planes(planes: np.ndarray, chaotic_seq):
    """
    Reverse the scrambling of planes along X-dimension using chaotic sequence

    Args:
        planes: Input array of shape (height, width, depth)
        chaotic_seq: Chaotic sequence used for original scrambling

    Returns:
        np.ndarray: Unscrambled array with same shape as input
    """
    if len(chaotic_seq) < planes.shape[0]:
        raise ValueError("Chaotic sequence length must be >= height dimension")
    height, width, depth = planes.shape
    perm_indices = np.argsort(chaotic_seq[:height])
    reverse_indices = np.argsort(perm_indices)
    unscrambled = np.zeros_like(planes)
    for j in range(width):
        for k in range(depth):
            values = planes[:, j, k]
            unscrambled[:, j, k] = values[reverse_indices]
    return unscrambled

def reverse_scramble_y_planes(planes: np.ndarray, chaotic_seq):
    """
    Reverse the scrambling of planes along Y-dimension using chaotic sequence

    Args:
        planes: Input array of shape (height, width, depth)
        chaotic_seq: Chaotic sequence used for original scrambling

    Returns:
        np.ndarray: Unscrambled array with same shape as input
    """
    if len(chaotic_seq) < planes.shape[1]:
        raise ValueError("Chaotic sequence length must be >= width dimension")
    height, width, depth = planes.shape
    perm_indices = np.argsort(chaotic_seq[:width])
    reverse_indices = np.argsort(perm_indices)
    unscrambled = np.zeros_like(planes)
    for i in range(height):
        for k in range(depth):
            values = planes[i, :, k]
            unscrambled[i, :, k] = values[reverse_indices]
    return unscrambled

def reverse_scramble_z_planes(planes: np.ndarray, chaotic_seq):
    """
    Reverse the scrambling of planes along Z-dimension using chaotic sequence

    Args:
        planes: Input array of shape (height, width, depth)
        chaotic_seq: Chaotic sequence used for original scrambling

    Returns:
        np.ndarray: Unscrambled array with same shape as input
    """
    if len(chaotic_seq) < planes.shape[2]:
        raise ValueError("Chaotic sequence length must be >= depth dimension")
    height, width, depth = planes.shape
    perm_indices = np.argsort(chaotic_seq[:depth])
    reverse_indices = np.argsort(perm_indices)
    unscrambled = np.zeros_like(planes)
    for i in range(height):
        for j in range(width):
            values = planes[i, j, :]
            unscrambled[i, j, :] = values[reverse_indices]
    return unscrambled
