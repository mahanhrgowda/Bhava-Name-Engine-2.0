import pandas as pd
from bhava_vector_tagger import get_bhava_vector, get_dominant_bhava
from name_similarity import cosine_similarity

def generate_similarity_clusters(name_list, top_n=3):
    # Precompute vectors
    name_vectors = {name: get_bhava_vector(name) for name in name_list}
    clusters = []

    for base_name, base_vector in name_vectors.items():
        sims = []
        for other_name, other_vector in name_vectors.items():
            if base_name != other_name:
                sim_score = cosine_similarity(base_vector, other_vector)
                sims.append((other_name, round(sim_score, 3)))
        # Top matches
        top_matches = sorted(sims, key=lambda x: x[1], reverse=True)[:top_n]
        for match_name, score in top_matches:
            clusters.append({
                "Base Name": base_name,
                "Similar Name": match_name,
                "Similarity Score": score
            })
    return pd.DataFrame(clusters)

import json

def generate_similarity_clusters_json(name_list, top_n=3):
    name_vectors = {name: get_bhava_vector(name) for name in name_list}
    cluster_dict = {}

    for base_name, base_vector in name_vectors.items():
        sims = []
        for other_name, other_vector in name_vectors.items():
            if base_name != other_name:
                sim_score = cosine_similarity(base_vector, other_vector)
                sims.append({
                    "name": other_name,
                    "score": round(sim_score, 3)
                })
        cluster_dict[base_name] = sorted(sims, key=lambda x: x["score"], reverse=True)[:top_n]

    return cluster_dict

def save_clusters_to_json(cluster_dict, filename="name_similarity_clusters.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(cluster_dict, f, ensure_ascii=False, indent=2)
