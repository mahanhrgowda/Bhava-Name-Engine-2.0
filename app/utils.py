import numpy as np

def normalize_vector(vector):
    total = sum(vector)
    if total == 0:
        return vector
    return [round(v / total, 3) for v in vector]

def format_name(name):
    return name.strip().capitalize()
