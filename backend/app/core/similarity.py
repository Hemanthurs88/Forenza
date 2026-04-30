import numpy as np
from PIL import Image
import os

def compute_phash(image_path_or_bytes, hash_size=8, highfreq_factor=4):
    """
    Computes a perceptual hash of an image using 2D DCT.
    Accepts a file path or raw image bytes.
    """
    img_size = hash_size * highfreq_factor
    
    if isinstance(image_path_or_bytes, bytes):
        import io
        img = Image.open(io.BytesIO(image_path_or_bytes)).convert('L')
    else:
        img = Image.open(image_path_or_bytes).convert('L')
        
    try:
        resample_mode = Image.Resampling.LANCZOS
    except AttributeError:
        resample_mode = Image.LANCZOS
        
    img = img.resize((img_size, img_size), resample_mode)
    pixels = np.array(img, dtype=np.float32)
    
    # Compute 2D DCT matrix
    D = np.zeros((img_size, img_size), dtype=np.float32)
    D[0, :] = 1.0 / np.sqrt(img_size)
    for i in range(1, img_size):
        for j in range(img_size):
            D[i, j] = np.sqrt(2.0 / img_size) * np.cos(np.pi * i * (2.0 * j + 1.0) / (2.0 * img_size))
    
    # Apply 2D DCT
    dct = np.dot(np.dot(D, pixels), D.T)
    
    # Extract top-left 8x8 (lowest frequencies)
    dctlowfreq = dct[:hash_size, :hash_size]
    
    # Compute mean, excluding the DC component
    avg = (np.sum(dctlowfreq) - dctlowfreq[0, 0]) / (hash_size * hash_size - 1)
    
    # Compute hash bits
    hash_mat = dctlowfreq > avg
    return hash_mat.flatten()

def hamming_distance(hash1, hash2):
    """Calculate the Hamming distance between two boolean hash arrays."""
    return np.count_nonzero(hash1 != hash2)

def similarity_score(hash1, hash2):
    """Calculate a percentage similarity score (0-100)."""
    dist = hamming_distance(hash1, hash2)
    return (1 - dist / 64) * 100

def hash_to_string(hash_arr):
    """Convert boolean hash array to 64-character bit string."""
    return "".join(["1" if b else "0" for b in hash_arr])

def string_to_hash(hash_str):
    """Convert 64-character bit string back to boolean hash array."""
    return np.array([b == "1" for b in hash_str])
