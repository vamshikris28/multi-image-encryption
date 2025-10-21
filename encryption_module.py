from utils.hash_utils import md5_hash, sha256_hash, hash_to_bytes
from utils.chaotic_maps import *
from utils.bitplane_ops import *
from utils.image_utils import *
from math import sin, pi
import numpy as np
from utils.bitplane_ops import (
    construct_3d_cube,
    bytes_to_cube,
    scramble_x_planes,
    scramble_y_planes,
    scramble_z_planes,
    extract_images_from_cube,
    reverse_scramble_x_planes,
    reverse_scramble_y_planes,
    reverse_scramble_z_planes,
)

# Modified Multiple-Image Encryption Algorithm
# Using MD5 + SHA-256 Hybrid Hashing
def concatenate(images, password):
    """
    Combine all image data + password into one byte stream
    for hashing (MD5 + SHA256).
    """
    try:
        # Initialize bytearray with password bytes
        combined_data = bytearray()
        combined_data.extend(password.encode('utf-8'))
        
        # Add each image's bytes
        for img in images:
            # Convert image to numpy array if not already
            if not isinstance(img, np.ndarray):
                img_array = np.array(img, dtype=np.uint8)
            else:
                img_array = img.astype(np.uint8)
            # Extend bytearray with image bytes
            combined_data.extend(img_array.tobytes())
        
        return combined_data
    except Exception as e:
        raise ValueError(f"Error concatenating data: {str(e)}")

def modified_encryption(images, password):
    """
    Encrypt multiple images using hybrid hash-based approach.
    """
    print("Phase 1: Hybrid Key Generation")
    data = concatenate(images, password)
    H_md5 = md5_hash(data)
    H_sha = sha256_hash(data)
    x0, y0, z0, p0, q0 = extract_initial_values(H_md5)
    a, b, c, mu = extract_control_params(H_sha)

    keys = {
        'H_md5': H_md5,
        'H_sha': H_sha,
        'x0': x0, 'y0': y0, 'z0': z0,
        'p0': p0, 'q0': q0,
        'a': a, 'b': b, 'c': c, 'mu': mu
    }

    # Phase 2: 3D Bit-Plane Scrambling
    print("Phase 2: 3D Bit-Plane Scrambling")
    cube_3d = construct_3d_cube(images)
    h, w, d = cube_3d.shape
    X1, X2, X3 = generate_3d_sine_sequences(x0, y0, z0, a, b, c, h)
    Y, Z = generate_2d_lasm_sequences(p0, q0, mu, h)
    cube_scrambled = scramble_z_planes(cube_3d, X1)
    cube_scrambled = scramble_y_planes(cube_scrambled, X2)
    cube_scrambled = scramble_x_planes(cube_scrambled, X3)

    # Phase 3: Multi-Layer Hash Diffusion
    print("Phase 3: Multi-Layer Hash Diffusion")
    byte_array = cube_to_bytes(cube_scrambled)
    byte_array_1 = apply_md5_diffusion(byte_array, H_md5)
    byte_array_2 = apply_sha256_diffusion(byte_array_1, H_sha)
    encrypted_bytes = apply_hybrid_diffusion(byte_array_2, H_md5, H_sha)
    encrypted_cube = bytes_to_cube(encrypted_bytes, (h, w, d))
    encrypted_images = extract_images_from_cube(encrypted_cube, images)

    return encrypted_images, keys


def extract_initial_values(H_md5):
    """Extract chaotic initial values from MD5 hash"""
    bytes_md5 = hash_to_bytes(H_md5)  # 16 bytes
    
    x0 = ((bytes_md5[0] ^ bytes_md5[1] ^ bytes_md5[2] ^ bytes_md5[3]) 
          % 10**8) / 10**8
    y0 = ((bytes_md5[4] ^ bytes_md5[5] ^ bytes_md5[6] ^ bytes_md5[7]) 
          % 10**8) / 10**8
    z0 = ((bytes_md5[8] ^ bytes_md5[9] ^ bytes_md5[10] ^ bytes_md5[11]) 
          % 10**8) / 10**8
    p0 = ((bytes_md5[12] ^ bytes_md5[13]) % 10**8) / 10**8
    q0 = ((bytes_md5[14] ^ bytes_md5[15]) % 10**8) / 10**8
    
    return x0, y0, z0, p0, q0


def extract_control_params(H_sha):
    """Extract chaotic control parameters from SHA-256 hash"""
    bytes_sha = hash_to_bytes(H_sha)  # 32 bytes
    
    a = 1 + ((bytes_sha[0] ^ bytes_sha[1] ^ bytes_sha[2]) % 300) / 100
    b = 1 + ((bytes_sha[3] ^ bytes_sha[4] ^ bytes_sha[5]) % 300) / 100
    c = 1 + ((bytes_sha[6] ^ bytes_sha[7] ^ bytes_sha[8]) % 300) / 100
    mu = ((bytes_sha[9] ^ bytes_sha[10]) % 100) / 100
    
    return a, b, c, mu


def generate_3d_sine_sequences(x0, y0, z0, a, b, c, length):
    """Generate chaotic sequences from 3D Sine Map"""
    X1, X2, X3 = [], [], []
    x, y, z = x0, y0, z0
    
    # Discard first 1000 iterations
    for _ in range(1000):
        x = a * sin(pi * (1-x)) * sin(pi * (1-y)) % 1
        y = b * sin(pi * (1-y)) * sin(pi * (1-z)) % 1
        z = c * sin(pi * (1-z)) * sin(pi * (1-x)) % 1
    
    # Generate sequences
    for _ in range(length):
        x = a * sin(pi * (1-x)) * sin(pi * (1-y)) % 1
        y = b * sin(pi * (1-y)) * sin(pi * (1-z)) % 1
        z = c * sin(pi * (1-z)) * sin(pi * (1-x)) % 1
        X1.append(x)
        X2.append(y)
        X3.append(z)
    
    return X1, X2, X3


def apply_md5_diffusion(byte_array, H_md5):
    """Apply MD5-based XOR diffusion"""
    if not isinstance(byte_array, (bytes, bytearray)):
        byte_array = bytes(byte_array)
    result = bytearray(byte_array)
    chunk_size = 1024
    
    K_prev = bytes(H_md5, 'utf-8') if isinstance(H_md5, str) else bytes(H_md5)
    
    for i in range(0, len(byte_array), chunk_size):
        chunk = bytes(byte_array[i:i+chunk_size])
        K = md5_hash(K_prev + chunk)
        K_bytes = hash_to_bytes(K)
        
        for j in range(len(chunk)):
            result[i+j] = chunk[j] ^ K_bytes[j % 16]
        
        K_prev = K_bytes
    
    return result


def apply_sha256_diffusion(byte_array, H_sha):
    """Apply SHA-256-based addition diffusion"""
    if not isinstance(byte_array, (bytes, bytearray)):
        byte_array = bytes(byte_array)
    result = bytearray(byte_array)
    chunk_size = 1024
    
    S_prev = bytes(H_sha, 'utf-8') if isinstance(H_sha, str) else bytes(H_sha)
    
    for i in range(0, len(byte_array), chunk_size):
        chunk = bytes(byte_array[i:i+chunk_size])
        S = sha256_hash(S_prev + chunk)
        S_bytes = hash_to_bytes(S)
        
        for j in range(len(chunk)):
            result[i+j] = (chunk[j] + S_bytes[j % 32]) % 256
        
        S_prev = S_bytes
    
    return result


def apply_hybrid_diffusion(byte_array, H_md5, H_sha):
    """Apply chained hybrid diffusion"""
    if not isinstance(byte_array, (bytes, bytearray)):
        byte_array = bytes(byte_array)
    result = bytearray([0] * len(byte_array))
    
    H_md5_bytes = bytes(H_md5, 'utf-8') if isinstance(H_md5, str) else bytes(H_md5)
    H_sha_bytes = bytes(H_sha, 'utf-8') if isinstance(H_sha, str) else bytes(H_sha)
    
    for i in range(len(byte_array)):
        prev_byte = result[i-1] if i > 0 else 0

        # Ensure all are strings before concatenation
        M_hash = md5_hash(str(prev_byte) + str(H_md5))
        S_hash = sha256_hash(str(prev_byte) + str(H_sha))

        M = hash_to_bytes(M_hash)[i % 16]
        S = hash_to_bytes(S_hash)[i % 32]

        result[i] = ((byte_array[i] ^ M) + S) % 256

    
    return result

def modified_decryption(encrypted_images, keys):
    """
    Decrypt images using the same keys.
    """
    H_md5 = keys['H_md5']
    H_sha = keys['H_sha']
    x0, y0, z0 = keys['x0'], keys['y0'], keys['z0']
    p0, q0 = keys['p0'], keys['q0']
    a, b, c, mu = keys['a'], keys['b'], keys['c'], keys['mu']

    encrypted_cube = construct_3d_cube(encrypted_images)
    h, w, d = encrypted_cube.shape
    encrypted_bytes = cube_to_bytes(encrypted_cube)

    # Reverse Phase 3: Multi-Layer Hash Diffusion
    print("Reversing Phase 3: Hybrid Diffusion")
    byte_array_2 = reverse_hybrid_diffusion(encrypted_bytes, H_md5, H_sha)
    byte_array_1 = reverse_sha256_diffusion(byte_array_2, H_sha)
    byte_array = reverse_md5_diffusion(byte_array_1, H_md5)

    # Reverse Phase 2: 3D Bit-Plane Scrambling
    print("Reversing Phase 2: Bit-Plane Scrambling")
    cube_scrambled = bytes_to_cube(byte_array, (h, w, d))
    X1, X2, X3 = generate_3d_sine_sequences(x0, y0, z0, a, b, c, h)
    cube_3d = reverse_scramble_x_planes(cube_scrambled, X3)
    cube_3d = reverse_scramble_y_planes(cube_3d, X2)
    cube_3d = reverse_scramble_z_planes(cube_3d, X1)
    decrypted_images = extract_images_from_cube(cube_3d, encrypted_images)

    return decrypted_images


def reverse_hybrid_diffusion(encrypted_bytes, H_md5, H_sha):
    """Reverse chained hybrid diffusion"""
    result = [0] * len(encrypted_bytes)
    
    for i in range(len(encrypted_bytes)):
        if i == 0:
            prev_byte = 0
        else:
            prev_byte = result[i-1]
        
        # Generate same hash components
        M_hash = md5_hash(str(prev_byte) + str(H_md5))
        M = hash_to_bytes(M_hash)[i % 16]
        
        S_hash = sha256_hash(str(prev_byte)+ str(H_sha))
        S = hash_to_bytes(S_hash)[i % 32]
        
        # Reverse hybrid operation
        result[i] = ((encrypted_bytes[i] - S) % 256) ^ M
    
    return result

def reverse_sha256_diffusion(byte_array, H_sha):
    """Reverse SHA-256-based addition diffusion"""
    result = byte_array.copy()
    chunk_size = 1024
    S_prev = H_sha

    for i in range(0, len(byte_array), chunk_size):
        chunk = byte_array[i:i+chunk_size]
        S = sha256_hash(str(S_prev) + str(chunk))
        S_bytes = hash_to_bytes(S)

        for j in range(len(chunk)):
            # Reverse (addition % 256)
            result[i+j] = (chunk[j] - S_bytes[j % 32]) % 256

        S_prev = S

    return result

def reverse_md5_diffusion(byte_array, H_md5):
    """Reverse MD5-based XOR diffusion"""
    result = byte_array.copy()
    chunk_size = 1024
    K_prev = H_md5

    for i in range(0, len(byte_array), chunk_size):
        chunk = byte_array[i:i+chunk_size]
        K = md5_hash(str(K_prev) + str(chunk))
        K_bytes = hash_to_bytes(K)

        for j in range(len(chunk)):
            # Reverse XOR (same operation)
            result[i+j] = chunk[j] ^ K_bytes[j % 16]

        K_prev = K

    return result
