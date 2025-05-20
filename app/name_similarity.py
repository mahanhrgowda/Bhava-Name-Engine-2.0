import numpy as np
from bhava_vector_tagger import get_bhava_vector

def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def find_similar_names(target_name, name_list, top_n=5):
    target_vector = get_bhava_vector(target_name)
    similarities = []

    for name in name_list:
        sim = cosine_similarity(target_vector, get_bhava_vector(name))
        similarities.append((name, round(sim, 3)))

    # Sort by similarity descending
    sorted_similar = sorted(similarities, key=lambda x: x[1], reverse=True)
    return sorted_similar[:top_n]
