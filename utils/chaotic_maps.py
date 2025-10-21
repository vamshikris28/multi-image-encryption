import numpy as np
from math import sin, pi
from typing import Tuple, List, Union

def generate_3d_sine_sequences(x0: float, y0: float, z0: float, 
                             a: float, b: float, c: float, 
                             length: int) -> Tuple[List[float], List[float], List[float]]:
    """
    Generate 3D sine chaotic sequences
    
    Args:
        x0, y0, z0: Initial values
        a, b, c: Control parameters
        length: Desired sequence length
        
    Returns:
        Tuple of three lists containing chaotic sequences
    """
    # Input validation
    for val in [x0, y0, z0, a, b, c]:
        if not isinstance(val, (int, float)):
            raise TypeError(f"Expected numeric value, got {type(val)}")
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer")

    # Initialize empty lists
    X1, X2, X3 = [], [], []
    
    # Convert to numpy arrays for calculations
    x, y, z = np.float64(x0), np.float64(y0), np.float64(z0)
    
    # Warmup phase
    for _ in range(1000):
        x = a * sin(pi*(1-x))*sin(pi*(1-y)) % 1
        y = b * sin(pi*(1-y))*sin(pi*(1-z)) % 1
        z = c * sin(pi*(1-z))*sin(pi*(1-x)) % 1
    
    # Generate sequences
    for _ in range(length):
        x = a * sin(pi*(1-x))*sin(pi*(1-y)) % 1
        y = b * sin(pi*(1-y))*sin(pi*(1-z)) % 1
        z = c * sin(pi*(1-z))*sin(pi*(1-x)) % 1
        X1.append(float(x))
        X2.append(float(y))
        X3.append(float(z))
    
    return X1, X2, X3

def generate_2d_lasm_sequences(p0: float, q0: float, mu: float, length: int) -> Tuple[List[float], List[float]]:
    """
    Generate chaotic sequences using 2D Logistic Adjusted Sine Map (LASM)
    
    Args:
        p0, q0: Initial seeds (0 < p0, q0 < 1)
        mu: Control parameter (0.5 <= mu <= 1)
        length: Sequence length
    Returns:
        Tuple[List[float], List[float]]: Two chaotic sequences Y, Z
    """
    # Initialize empty lists
    Y, Z = [], []
    p, q = float(p0), float(q0)

    # Discard first 1000 iterations (transient)
    for _ in range(1000):
        p = mu * sin(pi * q) + (4 - mu) * p * (1 - p)
        q = mu * sin(pi * p) + (4 - mu) * q * (1 - q)
        p, q = p % 1, q % 1

    # Generate sequences
    for _ in range(length):
        p = mu * sin(pi * q) + (4 - mu) * p * (1 - p)
        q = mu * sin(pi * p) + (4 - mu) * q * (1 - q)
        p, q = p % 1, q % 1
        Y.append(p)
        Z.append(q)

    return Y, Z

def scramble_z_planes(planes: np.ndarray, chaotic_seq: List[float]) -> np.ndarray:
    """
    Scramble bit planes in Z-dimension using chaotic sequence
    
    Args:
        planes: Input bit planes array of shape (height, width, depth)
        chaotic_seq: Chaotic sequence for generating permutation
        
    Returns:
        np.ndarray: Scrambled bit planes
    """
    if len(chaotic_seq) < planes.shape[2]:
        raise ValueError("Chaotic sequence length must be >= number of planes")
        
    # Get array dimensions
    height, width, depth = planes.shape
    
    # Create permutation indices from chaotic sequence
    perm_indices = np.argsort(chaotic_seq[:depth])
    
    # Create output array
    scrambled = np.zeros_like(planes)
    
    # Scramble each x,y position across z-planes
    for i in range(height):
        for j in range(width):
            bit_values = planes[i,j,:]
            scrambled[i,j,:] = bit_values[perm_indices]
            
    return scrambled

def scramble_y_planes(planes: np.ndarray, chaotic_seq: List[float]) -> np.ndarray:
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
        
    # Get dimensions
    height, width, depth = planes.shape
    
    # Generate permutation indices
    perm_indices = np.argsort(chaotic_seq[:width])
    
    # Create output array
    scrambled = np.zeros_like(planes)
    
    # Scramble each x,z position across y-planes
    for i in range(height):
        for k in range(depth):
            values = planes[i,:,k]
            scrambled[i,:,k] = values[perm_indices]
            
    return scrambled

def scramble_x_planes(planes: np.ndarray, chaotic_seq: List[float]) -> np.ndarray:
    """
    Scramble planes along X-dimension using chaotic sequence
    
    Args:
        planes: Input array of shape (height, width, depth)
        chaotic_seq: Chaotic sequence for generating permutation
        
    Returns:
        np.ndarray: Scrambled array with same shape as input
    
    Raises:
        ValueError: If chaotic sequence length is insufficient
    """
    if len(chaotic_seq) < planes.shape[0]:
        raise ValueError("Chaotic sequence length must be >= height dimension")
        
    # Get dimensions
    height, width, depth = planes.shape
    
    # Generate permutation indices
    perm_indices = np.argsort(chaotic_seq[:height])
    
    # Create output array
    scrambled = np.zeros_like(planes)
    
    # Scramble each y,z position across x-planes
    for j in range(width):
        for k in range(depth):
            values = planes[:,j,k]
            scrambled[:,j,k] = values[perm_indices]
            
    return scrambled
