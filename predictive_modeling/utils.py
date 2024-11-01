# predictive_modeling/utils.py

import numpy as np

def normalize_data(data: np.ndarray) -> np.ndarray:
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0) + 1e-8  # Avoid division by zero
    normalized = (data - mean) / std
    return normalized

def create_sequences(data: np.ndarray, sequence_length: int = 100) -> np.ndarray:
    sequences = []
    for i in range(len(data) - sequence_length):
        sequences.append(data[i:i+sequence_length])
    return np.array(sequences)